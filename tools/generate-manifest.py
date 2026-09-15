#!/usr/bin/env python3
"""Regenerate updates/build-manifest.json with current SHA-256 digests.

Computes the SHA-256 digest of each protected build input and writes a
verification manifest consumable by tools/verify-before-execution.py. Run this
whenever a listed source file changes so the verification gate reflects the
intended bytes.

This helper only records digests. It does not establish publisher identity and
does not weaken any platform security control.
"""

import argparse
import datetime
import hashlib
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Protected build inputs, repository-relative, forward-slash paths.
PROTECTED_FILES = [
    "kernel/file-locker/linux_admin_defender_lock.c",
    "kernel/file-locker/Makefile",
    "kernel/file-locker/control.sh",
    "tools/protected-store.py",
    "tools/update-manager.py",
    "tools/verify-before-execution.py",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Regenerate the build verification manifest")
    ap.add_argument("--output", default=os.path.join(REPO_ROOT, "updates", "build-manifest.json"))
    args = ap.parse_args()

    files = []
    for rel in PROTECTED_FILES:
        full = os.path.join(REPO_ROOT, rel)
        if not os.path.isfile(full):
            raise SystemExit(f"generate-manifest: protected file not found: {rel}")
        files.append({"path": rel, "sha256": sha256(full)})

    manifest = {
        "manifest_version": "1.0",
        "product": "Linux.Admin.Defender",
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "algorithm": "sha256",
        "description": "Verification manifest for the protected build inputs. Each digest is the SHA-256 of the exact file bytes.",
        "files": files,
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print(f"generate-manifest: wrote {args.output} ({len(files)} files)")


if __name__ == "__main__":
    raise SystemExit(main())
