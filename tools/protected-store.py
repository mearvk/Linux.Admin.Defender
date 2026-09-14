#!/usr/bin/env python3
"""Content-addressed protected system-file store.

Default mode is enabled by config. Use --store-mode off to make a one-shot
non-destructive dry bypass, or --store-mode on to force the store on.
The store records metadata in SQLite and keeps file contents by SHA-256.
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import stat
import sys
import time

DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "protected-store.json")
SCHEMA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "protected-store", "schema.sql")


def load_config(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def is_excluded(path, excludes):
    path = os.path.abspath(path)
    return any(path == e or path.startswith(e.rstrip("/") + "/") for e in excludes)


def digest_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def init_db(cfg):
    os.makedirs(os.path.dirname(cfg["database"]), exist_ok=True)
    os.makedirs(cfg["objects"], exist_ok=True)
    with sqlite3.connect(cfg["database"]) as db:
        with open(SCHEMA, "r", encoding="utf-8") as fh:
            db.executescript(fh.read())


def store_file(path, cfg, db):
    st = os.stat(path, follow_symlinks=False)
    if not stat.S_ISREG(st.st_mode):
        return False
    sha = digest_file(path)
    obj = os.path.join(cfg["objects"], sha[:2], sha[2:])
    os.makedirs(os.path.dirname(obj), exist_ok=True)
    if not os.path.exists(obj):
        tmp = obj + ".tmp-" + str(os.getpid())
        shutil.copy2(path, tmp, follow_symlinks=False)
        os.replace(tmp, obj)
    cur = db.execute("SELECT object_id FROM objects WHERE sha256 = ?", (sha,))
    row = cur.fetchone()
    if row is None:
        cur = db.execute(
            "INSERT INTO objects(sha256,size_bytes,object_path) VALUES(?,?,?)",
            (sha, st.st_size, obj),
        )
        object_id = cur.lastrowid
    else:
        object_id = row[0]
    db.execute(
        "INSERT INTO files(path,object_id,mode,uid,gid,size_bytes,mtime_ns,protected) "
        "VALUES(?,?,?,?,?,?,?,1) "
        "ON CONFLICT(path) DO UPDATE SET object_id=excluded.object_id,mode=excluded.mode,"
        "uid=excluded.uid,gid=excluded.gid,size_bytes=excluded.size_bytes,"
        "mtime_ns=excluded.mtime_ns,protected=1,last_seen=CURRENT_TIMESTAMP",
        (path, object_id, stat.S_IMODE(st.st_mode), st.st_uid, st.st_gid, st.st_size, st.st_mtime_ns),
    )
    db.execute("INSERT INTO events(path,action,sha256,detail) VALUES(?,?,?,?)",
               (path, "snapshot", sha, "content stored and marked protected"))
    return True


def walk_roots(cfg):
    excludes = [os.path.abspath(x) for x in cfg.get("exclude", [])]
    for root in cfg.get("roots", []):
        root = os.path.abspath(root)
        if not os.path.exists(root) or is_excluded(root, excludes):
            continue
        if os.path.isfile(root):
            yield root
            continue
        for base, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [d for d in dirs if not is_excluded(os.path.join(base, d), excludes)]
            for name in files:
                path = os.path.join(base, name)
                if not is_excluded(path, excludes):
                    yield path


def snapshot(cfg):
    init_db(cfg)
    count = 0
    with sqlite3.connect(cfg["database"]) as db:
        for path in walk_roots(cfg):
            try:
                count += int(store_file(path, cfg, db))
            except (OSError, PermissionError) as exc:
                db.execute("INSERT INTO events(path,action,detail) VALUES(?,?,?)",
                           (path, "error", str(exc)))
        db.commit()
    print(f"protected-store: snapshotted {count} regular files")


def status(cfg):
    if not os.path.exists(cfg["database"]):
        print("protected-store: not initialized")
        return 1
    with sqlite3.connect(cfg["database"]) as db:
        files = db.execute("SELECT COUNT(*) FROM files WHERE protected=1").fetchone()[0]
        objects = db.execute("SELECT COUNT(*) FROM objects").fetchone()[0]
    print(f"protected-store: enabled={cfg.get('enabled', True)} files={files} objects={objects}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Linux.Admin.Defender protected system store")
    ap.add_argument("command", choices=["init", "snapshot", "status"])
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--store-mode", choices=["on", "off"], default=None,
                    help="override configured protected-store mode for this invocation")
    args = ap.parse_args()
    cfg = load_config(args.config)
    enabled = cfg.get("enabled", True) if args.store_mode is None else args.store_mode == "on"
    if not enabled:
        print("protected-store: disabled by configuration/flag")
        return 0
    if args.command == "init":
        init_db(cfg)
        print(f"protected-store: initialized {cfg['database']}")
        return 0
    if args.command == "snapshot":
        snapshot(cfg)
        return 0
    return status(cfg)


if __name__ == "__main__":
    sys.exit(main())
