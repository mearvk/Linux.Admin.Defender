-- Linux.Admin.Defender protected system store
-- SQLite is the default embedded implementation. The relational model is
-- intentionally MySQL-like so it can be migrated to MySQL/MariaDB later.

CREATE TABLE IF NOT EXISTS objects (
    object_id INTEGER PRIMARY KEY,
    sha256 CHAR(64) NOT NULL UNIQUE,
    size_bytes BIGINT NOT NULL,
    object_path TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS files (
    file_id INTEGER PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    object_id INTEGER NOT NULL,
    mode INTEGER,
    uid INTEGER,
    gid INTEGER,
    size_bytes BIGINT NOT NULL,
    mtime_ns BIGINT,
    protected INTEGER NOT NULL DEFAULT 1,
    last_seen TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (object_id) REFERENCES objects(object_id)
);

CREATE INDEX IF NOT EXISTS idx_files_object_id ON files(object_id);
CREATE INDEX IF NOT EXISTS idx_files_protected ON files(protected);
CREATE INDEX IF NOT EXISTS idx_files_last_seen ON files(last_seen);

CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY,
    path TEXT,
    action TEXT NOT NULL,
    sha256 CHAR(64),
    detail TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
