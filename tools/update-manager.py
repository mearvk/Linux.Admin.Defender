#!/usr/bin/env python3
"""Daily update manager with mandatory SHA-256 verification.

Updates are staged and verified before installation. Internet manifests and
local update directories use the same manifest format. Unlisted files are
rejected by default. The program never installs a file whose SHA-256 digest
does not exactly match the manifest.
"""

import argparse
import hashlib
import json
import os
import shutil
import ssl
import tempfile
import time
import urllib.request

DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "update-manager.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_manifest(cfg, work):
    mode = cfg.get("source_mode", "local")
    if mode == "local":
        path = os.path.join(cfg["local_update_folder"], "updates.json")
        return load_json(path), cfg["local_update_folder"]
    if mode == "internet":
        url = cfg["internet_manifest"]
        if not url.startswith("https://"):
            raise RuntimeError("internet manifests must use HTTPS")
        manifest_path = os.path.join(work, "updates.json")
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, context=context, timeout=30) as r:
            with open(manifest_path, "wb") as f:
                shutil.copyfileobj(r, f)
        return load_json(manifest_path), work
    raise RuntimeError("source_mode must be 'internet' or 'local'")


def obtain_file(item, source_root, work):
    name = item["path"]
    if os.path.isabs(name) or ".." in name.split(os.sep):
        raise RuntimeError(f"unsafe update path: {name}")
    source = os.path.join(source_root, name)
    if os.path.isfile(source):
        return source
    if source_root == work and item.get("url"):
        url = item["url"]
        if not url.startswith("https://"):
            raise RuntimeError("update file URLs must use HTTPS")
        target = os.path.join(work, "downloads", name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, context=context, timeout=60) as r:
            with open(target, "wb") as f:
                shutil.copyfileobj(r, f)
        return target
    raise FileNotFoundError(source)


def verify_manifest(manifest, source_root, work):
    if manifest.get("algorithm", "sha256").lower() != "sha256":
        raise RuntimeError("manifest must use SHA-256")
    verified = []
    for item in manifest.get("files", []):
        expected = item.get("sha256", "").lower()
        if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise RuntimeError(f"invalid SHA-256 for {item.get('path')}")
        source = obtain_file(item, source_root, work)
        actual = sha256(source)
        if actual != expected:
            raise RuntimeError(f"SHA-256 verification failed: {item['path']} expected={expected} actual={actual}")
        verified.append((source, item["path"]))
    return verified


def install(verified, cfg):
    root = os.path.abspath(cfg.get("install_root", "/"))
    stage = cfg.get("staging_directory", "/var/lib/linux-admin-defender/staging")
    backup = cfg.get("backup_directory", "/var/lib/linux-admin-defender/backups")
    os.makedirs(stage, exist_ok=True)
    os.makedirs(backup, exist_ok=True)

    # Copy verified files into a staging tree first. Nothing is installed until
    # every manifest entry has passed verification.
    staged = []
    for source, relative in verified:
        target = os.path.join(stage, relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(source, target)
        if sha256(target) != sha256(source):
            raise RuntimeError(f"staging verification failed: {relative}")
        staged.append((target, relative))

    for target, relative in staged:
        destination = os.path.join(root, relative.lstrip("/"))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        if os.path.exists(destination):
            stamp = str(int(time.time()))
            backup_path = os.path.join(backup, stamp, relative.lstrip("/"))
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(destination, backup_path)
        os.replace(target, destination)


def main():
    ap = argparse.ArgumentParser(description="Linux.Admin.Defender daily update manager")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--check", action="store_true", help="check and verify without installing")
    ap.add_argument("--install", action="store_true", help="verify and install updates")
    args = ap.parse_args()
    cfg = load_json(args.config)
    if not cfg.get("enabled", True):
        print("update-manager: disabled")
        return 0
    if not args.check and not args.install:
        args.install = cfg.get("automatic_install", False)
    with tempfile.TemporaryDirectory(prefix="linux-admin-defender-update-") as work:
        manifest, source_root = fetch_manifest(cfg, work)
        verified = verify_manifest(manifest, source_root, work)
        print(f"update-manager: SHA-256 verified {len(verified)} file(s)")
        if args.install and verified:
            if os.geteuid() != 0:
                raise RuntimeError("installation requires root")
            install(verified, cfg)
            print(f"update-manager: installed {len(verified)} verified file(s)")
        else:
            print("update-manager: no files installed")


if __name__ == "__main__":
    main()
