#!/usr/bin/env python3
"""Verify Defender-controlled files before build, execution, or diagnostics.

The manifest must contain SHA-256 values. Verification fails closed.
"""

import argparse
import hashlib
import json
import os
import sys

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)

    if manifest.get("algorithm", "sha256").lower() != "sha256":
        print("verification: FAIL: manifest is not SHA-256", file=sys.stderr)
        return 2

    failures = []
    checked = 0
    for item in manifest.get("files", []):
        rel = item.get("path", "")
        expected = item.get("sha256", "").lower()
        if os.path.isabs(rel) or ".." in rel.replace("\\", "/").split("/"):
            failures.append((rel, "unsafe path"))
            continue
        if len(expected) != 64:
            failures.append((rel, "invalid SHA-256"))
            continue
        path = os.path.join(args.root, rel)
        if not os.path.isfile(path):
            failures.append((rel, "missing"))
            continue
        actual = sha256(path)
        checked += 1
        if actual != expected:
            failures.append((rel, f"expected {expected}, got {actual}"))

    if failures:
        print(f"verification: FAIL ({len(failures)} failure(s), {checked} checked)", file=sys.stderr)
        for path, reason in failures:
            print(f"  {path}: {reason}", file=sys.stderr)
        return 1

    print(f"verification: PASS ({checked} file(s), SHA-256)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
