"""SQLite implementation behind data/store.sh. Nothing else opens data/evidence/.

Tables
  items(item_id, kind, latest_version_id, first_seen_run, first_seen_at, last_seen_run, last_seen_at)
  versions(item_id, version_id, seq, record, first_seen_run, created_at)   -- full item record per version
  observations(run_id, item_id, version_id, change, retrieved_at, observed_at)  -- every sighting

version_id is computed upstream (processing/extract_content.sh) from substantive content and
evidence-relevant metadata only, so a refreshed retrieved_at never creates a version.
"""
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

ITEM_FIELDS = ["item_id", "source_id", "publisher_id", "kind", "title", "url", "published_at",
               "retrieved_at", "media_url", "version_id", "text_path", "segments_path"]

EVIDENCE_DIR = os.environ.get("PIPELINE_EVIDENCE_DIR", os.path.join("data", "evidence"))
DB_PATH = os.path.join(EVIDENCE_DIR, "evidence.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  item_id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  latest_version_id TEXT NOT NULL,
  first_seen_run TEXT, first_seen_at TEXT,
  last_seen_run TEXT, last_seen_at TEXT
);
CREATE TABLE IF NOT EXISTS versions (
  item_id TEXT NOT NULL,
  version_id TEXT NOT NULL,
  seq INTEGER NOT NULL,
  record TEXT NOT NULL,
  first_seen_run TEXT,
  created_at TEXT NOT NULL,
  PRIMARY KEY (item_id, version_id)
);
CREATE TABLE IF NOT EXISTS observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id TEXT, item_id TEXT NOT NULL, version_id TEXT NOT NULL,
  change TEXT NOT NULL, retrieved_at TEXT, observed_at TEXT NOT NULL
);
"""


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def die(code, msg):
    print(f"store: {msg}", file=sys.stderr)
    sys.exit(code)


def connect(create=False):
    if not os.path.exists(DB_PATH) and not create:
        die(1, f"evidence store not initialised ({DB_PATH}); run: bash data/store.sh init")
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)
    return con


def cmd_init():
    connect(create=True).close()


def emit_record(con, item_id, version_id):
    row = con.execute("SELECT record, seq, first_seen_run FROM versions WHERE item_id=? AND version_id=?",
                      (item_id, version_id)).fetchone()
    meta = con.execute("SELECT first_seen_run, first_seen_at, last_seen_run, last_seen_at, latest_version_id, "
                       "(SELECT COUNT(*) FROM versions v WHERE v.item_id=items.item_id) FROM items WHERE item_id=?",
                       (item_id,)).fetchone()
    rec = json.loads(row[0])
    last_ret = con.execute("SELECT retrieved_at FROM observations WHERE item_id=? AND version_id=? "
                           "ORDER BY id DESC LIMIT 1", (item_id, version_id)).fetchone()
    rec["store"] = {
        "version_seq": row[1],
        "version_first_seen_run": row[2],
        "version_count": meta[5],
        "is_latest": meta[4] == version_id,
        "item_first_seen_run": meta[0],
        "item_first_seen_at": meta[1],
        "last_seen_run": meta[2],
        "last_retrieved_at": last_ret[0] if last_ret else rec.get("retrieved_at"),
    }
    return rec


def cmd_upsert(run_dir):
    run_id = None
    try:
        with open(os.path.join(run_dir, "run.json"), encoding="utf-8") as fh:
            run_id = json.load(fh).get("run_id")
    except (OSError, json.JSONDecodeError):
        die(2, f"cannot read {run_dir}/run.json")

    records = []
    for n, line in enumerate(sys.stdin, 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            die(2, f"line {n}: invalid JSON ({exc}); nothing was written")
        missing = [f for f in ITEM_FIELDS if f not in rec]
        if not isinstance(rec, dict) or missing or not rec.get("item_id") or not rec.get("version_id"):
            die(2, f"line {n}: not an item record (missing {missing}); nothing was written")
        records.append(rec)

    con = connect()
    ts = now()
    out = []
    with con:  # one transaction: all records or none
        for rec in records:
            item_id, version_id = rec["item_id"], rec["version_id"]
            item = con.execute("SELECT latest_version_id FROM items WHERE item_id=?", (item_id,)).fetchone()
            known = con.execute("SELECT 1 FROM versions WHERE item_id=? AND version_id=?",
                                (item_id, version_id)).fetchone()
            stored = {k: v for k, v in rec.items() if k != "store"}
            if item is None:
                change = "new"
                con.execute("INSERT INTO items VALUES (?,?,?,?,?,?,?)",
                            (item_id, rec["kind"], version_id, run_id, ts, run_id, ts))
                con.execute("INSERT INTO versions VALUES (?,?,?,?,?,?)",
                            (item_id, version_id, 1, json.dumps(stored, sort_keys=True), run_id, ts))
            elif not known:
                change = "changed"
                seq = con.execute("SELECT COALESCE(MAX(seq),0)+1 FROM versions WHERE item_id=?", (item_id,)).fetchone()[0]
                con.execute("INSERT INTO versions VALUES (?,?,?,?,?,?)",
                            (item_id, version_id, seq, json.dumps(stored, sort_keys=True), run_id, ts))
                con.execute("UPDATE items SET latest_version_id=?, last_seen_run=?, last_seen_at=? WHERE item_id=?",
                            (version_id, run_id, ts, item_id))
            else:
                # Known version: only the sighting is recorded; retrieval time never creates a version.
                change = "unchanged"
                con.execute("UPDATE items SET last_seen_run=?, last_seen_at=? WHERE item_id=?",
                            (run_id, ts, item_id))
            con.execute("INSERT INTO observations (run_id,item_id,version_id,change,retrieved_at,observed_at) "
                        "VALUES (?,?,?,?,?,?)", (run_id, item_id, version_id, change, rec.get("retrieved_at"), ts))
            out.append({"item_id": item_id, "version_id": version_id, "change": change})
    for o in out:
        print(json.dumps(o))


def cmd_list():
    con = connect()
    for item_id, version_id in con.execute("SELECT item_id, latest_version_id FROM items ORDER BY item_id"):
        print(json.dumps(emit_record(con, item_id, version_id)))


def cmd_get(item_id, version_id=None):
    con = connect()
    item = con.execute("SELECT latest_version_id FROM items WHERE item_id=?", (item_id,)).fetchone()
    if item is None:
        die(1, f"no item {item_id}")
    version_id = version_id or item[0]
    if not con.execute("SELECT 1 FROM versions WHERE item_id=? AND version_id=?", (item_id, version_id)).fetchone():
        die(1, f"no version {version_id} of {item_id}")
    print(json.dumps(emit_record(con, item_id, version_id)))


def cmd_history(item_id):
    con = connect()
    rows = con.execute("SELECT version_id, seq, first_seen_run, created_at FROM versions WHERE item_id=? ORDER BY seq",
                       (item_id,)).fetchall()
    if not rows:
        die(1, f"no item {item_id}")
    for v, seq, run, at in rows:
        runs = [r[0] for r in con.execute("SELECT DISTINCT run_id FROM observations WHERE item_id=? AND version_id=?",
                                          (item_id, v))]
        print(json.dumps({"item_id": item_id, "version_id": v, "seq": seq, "first_seen_run": run,
                          "created_at": at, "observed_in_runs": runs}))


def main(argv):
    if not argv:
        die(2, "usage: store.sh init | upsert RUN_DIR | list | get ITEM_ID [VERSION_ID] | history ITEM_ID")
    cmd, args = argv[0], argv[1:]
    if cmd == "init" and not args:
        cmd_init()
    elif cmd == "upsert" and len(args) == 1:
        cmd_upsert(args[0])
    elif cmd == "list" and not args:
        cmd_list()
    elif cmd == "get" and len(args) in (1, 2):
        cmd_get(*args)
    elif cmd == "history" and len(args) == 1:
        cmd_history(args[0])
    else:
        die(2, f"invalid arguments: {' '.join(argv)}")


if __name__ == "__main__":
    main(sys.argv[1:])
