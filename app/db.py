"""SQLite storage. One local file, no server."""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime
from pathlib import Path

from .parser import Message

DB_PATH = Path(os.environ.get("PANO_DB", Path(__file__).resolve().parent.parent / "data" / "pano.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS chats (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    units         TEXT NOT NULL DEFAULT '[]',
    imported_at   TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'imported',
    error         TEXT,
    analyzed_upto INTEGER NOT NULL DEFAULT -1,
    file_hash     TEXT
);
CREATE TABLE IF NOT EXISTS messages (
    chat_id INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    idx     INTEGER NOT NULL,
    ts      TEXT NOT NULL,
    sender  TEXT,
    text    TEXT NOT NULL,
    kind    TEXT NOT NULL,
    PRIMARY KEY (chat_id, idx)
);
CREATE TABLE IF NOT EXISTS items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id      INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    kind         TEXT NOT NULL,            -- task | question | decision | event
    title        TEXT NOT NULL,
    owner        TEXT,
    due          TEXT,
    time         TEXT,
    place        TEXT,
    unit         TEXT,
    status       TEXT NOT NULL DEFAULT 'open',  -- open | done | answered
    source_idx   INTEGER,
    resolved_idx INTEGER,
    user_edited  INTEGER NOT NULL DEFAULT 0,
    review       TEXT NOT NULL DEFAULT 'approved',  -- proposed | approved | rejected
    needs_review INTEGER NOT NULL DEFAULT 0,        -- 1 no source message | 2 date unclear
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS changes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id    INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    item_id    INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    old        TEXT NOT NULL,          -- JSON {field: value} at proposal time
    new        TEXT NOT NULL,          -- JSON {field: value} to apply on approval
    source_idx INTEGER,
    review     TEXT NOT NULL DEFAULT 'proposed',  -- proposed | approved | rejected
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS items_chat ON items(chat_id, kind);
"""

_lock = threading.RLock()
_conn: sqlite3.Connection | None = None


def conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA foreign_keys = ON")
        _conn.executescript(SCHEMA)
        if "review" not in {r["name"] for r in _conn.execute("PRAGMA table_info(items)")}:
            _conn.execute("ALTER TABLE items ADD COLUMN review TEXT NOT NULL DEFAULT 'approved'")
            _conn.commit()
        if "file_hash" not in {r["name"] for r in _conn.execute("PRAGMA table_info(chats)")}:
            _conn.execute("ALTER TABLE chats ADD COLUMN file_hash TEXT")
            _conn.commit()
        if "needs_review" not in {r["name"] for r in _conn.execute("PRAGMA table_info(items)")}:
            _conn.execute("ALTER TABLE items ADD COLUMN needs_review INTEGER NOT NULL DEFAULT 0")
            _conn.commit()
    return _conn


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _rows(sql: str, args=()) -> list[dict]:
    with _lock:
        return [dict(r) for r in conn().execute(sql, args).fetchall()]


# ---- chats -----------------------------------------------------------------

def find_by_hash(file_hash: str) -> dict | None:
    rows = _rows("SELECT id, name, imported_at FROM chats WHERE file_hash = ? ORDER BY id LIMIT 1", (file_hash,))
    return rows[0] if rows else None


def create_chat(name: str, units: list[str], messages: list[Message], file_hash: str | None = None) -> int:
    with _lock, conn() as c:
        cur = c.execute(
            "INSERT INTO chats (name, units, imported_at, file_hash) VALUES (?, ?, ?, ?)",
            (name, json.dumps(units, ensure_ascii=False), _now(), file_hash),
        )
        chat_id = cur.lastrowid
        _insert_messages(c, chat_id, messages, start=0)
    return chat_id


def _insert_messages(c: sqlite3.Connection, chat_id: int, messages: list[Message], start: int) -> None:
    c.executemany(
        "INSERT INTO messages (chat_id, idx, ts, sender, text, kind) VALUES (?, ?, ?, ?, ?, ?)",
        [(chat_id, start + i, m.ts.isoformat(timespec="minutes"), m.sender, m.text, m.kind)
         for i, m in enumerate(messages)],
    )


def append_messages(chat_id: int, messages: list[Message]) -> int:
    """Add only messages we have not seen (re-importing a newer export of the same chat)."""
    existing = {(r["ts"], r["sender"], r["text"]) for r in _rows(
        "SELECT ts, sender, text FROM messages WHERE chat_id = ?", (chat_id,))}
    fresh = [m for m in messages
             if (m.ts.isoformat(timespec="minutes"), m.sender, m.text) not in existing]
    if fresh:
        with _lock, conn() as c:
            start = c.execute("SELECT COALESCE(MAX(idx), -1) + 1 FROM messages WHERE chat_id = ?",
                              (chat_id,)).fetchone()[0]
            _insert_messages(c, chat_id, fresh, start)
    return len(fresh)


def get_chat(chat_id: int) -> dict | None:
    rows = _rows("""
        SELECT c.*, COUNT(m.idx) AS message_count, MIN(m.ts) AS first_ts, MAX(m.ts) AS last_ts
        FROM chats c LEFT JOIN messages m ON m.chat_id = c.id
        WHERE c.id = ? GROUP BY c.id""", (chat_id,))
    if not rows:
        return None
    chat = rows[0]
    chat["units"] = json.loads(chat["units"])
    return chat


def list_chats() -> list[dict]:
    chats = _rows("""
        SELECT c.id, c.name, c.status, c.imported_at, COUNT(m.idx) AS message_count
        FROM chats c LEFT JOIN messages m ON m.chat_id = c.id
        GROUP BY c.id ORDER BY c.id DESC""")
    return chats


def update_chat(chat_id: int, **fields) -> None:
    if "units" in fields:
        fields["units"] = json.dumps(fields["units"], ensure_ascii=False)
    cols = ", ".join(f"{k} = ?" for k in fields)
    with _lock, conn() as c:
        c.execute(f"UPDATE chats SET {cols} WHERE id = ?", (*fields.values(), chat_id))


def delete_chat(chat_id: int) -> None:
    with _lock, conn() as c:
        c.execute("DELETE FROM chats WHERE id = ?", (chat_id,))


def reset_analysis(chat_id: int) -> None:
    with _lock, conn() as c:
        c.execute("DELETE FROM items WHERE chat_id = ?", (chat_id,))
        c.execute("UPDATE chats SET analyzed_upto = -1, status = 'imported', error = NULL WHERE id = ?",
                  (chat_id,))


# ---- messages --------------------------------------------------------------

def get_messages(chat_id: int, start: int = 0, end: int | None = None) -> list[dict]:
    if end is None:
        return _rows("SELECT * FROM messages WHERE chat_id = ? AND idx >= ? ORDER BY idx",
                     (chat_id, start))
    return _rows("SELECT * FROM messages WHERE chat_id = ? AND idx BETWEEN ? AND ? ORDER BY idx",
                 (chat_id, start, end))


def senders(chat_id: int) -> list[str]:
    return [r["sender"] for r in _rows(
        "SELECT sender, COUNT(*) n FROM messages WHERE chat_id = ? AND sender IS NOT NULL "
        "GROUP BY sender ORDER BY n DESC", (chat_id,))]


# ---- items -----------------------------------------------------------------

ITEM_FIELDS = ("title", "owner", "due", "time", "place", "unit", "status", "source_idx", "resolved_idx", "review", "needs_review")


def add_item(chat_id: int, kind: str, **fields) -> int:
    """Manual items are approved at once; the analyzer passes review="proposed"."""
    data = {k: fields.get(k) for k in ITEM_FIELDS}
    data["status"] = data["status"] or "open"
    data["review"] = data["review"] or "approved"
    data["needs_review"] = data["needs_review"] or 0
    now = _now()
    with _lock, conn() as c:
        cur = c.execute(
            f"INSERT INTO items (chat_id, kind, {', '.join(ITEM_FIELDS)}, created_at, updated_at) "
            f"VALUES (?, ?, {', '.join('?' * len(ITEM_FIELDS))}, ?, ?)",
            (chat_id, kind, *data.values(), now, now),
        )
        return cur.lastrowid


def update_item(item_id: int, user: bool = False, **fields) -> None:
    fields = {k: v for k, v in fields.items() if k in ITEM_FIELDS}
    if not fields:
        return
    fields["updated_at"] = _now()
    if user:
        fields["user_edited"] = 1
    cols = ", ".join(f"{k} = ?" for k in fields)
    with _lock, conn() as c:
        c.execute(f"UPDATE items SET {cols} WHERE id = ?", (*fields.values(), item_id))


def delete_item(item_id: int) -> None:
    with _lock, conn() as c:
        c.execute("DELETE FROM items WHERE id = ?", (item_id,))


def get_item(item_id: int) -> dict | None:
    rows = _rows("SELECT * FROM items WHERE id = ?", (item_id,))
    return rows[0] if rows else None


def get_items(chat_id: int, kind: str | None = None, review: str | None = "approved") -> list[dict]:
    """Approved items only by default; review=None returns every item, rejected ones included."""
    sql, args = "SELECT * FROM items WHERE chat_id = ?", [chat_id]
    if kind:
        sql += " AND kind = ?"; args.append(kind)
    if review:
        sql += " AND review = ?"; args.append(review)
    return _rows(sql + " ORDER BY id", args)


# ---- change proposals (AI edits to approved items wait for the user) -------

def has_change(item_id: int, new: dict) -> bool:
    """True if this exact change was proposed before, in any state (rejected ones must not return)."""
    want = json.dumps(new, sort_keys=True, ensure_ascii=False)
    return any(json.dumps(json.loads(r["new"]), sort_keys=True, ensure_ascii=False) == want
               for r in _rows("SELECT new FROM changes WHERE item_id = ?", (item_id,)))


def add_change(chat_id: int, item_id: int, old: dict, new: dict, source_idx: int | None) -> int:
    with _lock, conn() as c:
        return c.execute(
            "INSERT INTO changes (chat_id, item_id, old, new, source_idx, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (chat_id, item_id, json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False),
             source_idx, _now())).lastrowid


def get_change(change_id: int) -> dict | None:
    rows = _rows("SELECT * FROM changes WHERE id = ?", (change_id,))
    return _decode_change(rows[0]) if rows else None


def get_changes(chat_id: int, review: str = "proposed") -> list[dict]:
    rows = _rows("""SELECT ch.*, i.title AS item_title, i.kind AS item_kind FROM changes ch
                    JOIN items i ON i.id = ch.item_id
                    WHERE ch.chat_id = ? AND ch.review = ? ORDER BY ch.id""", (chat_id, review))
    return [_decode_change(r) for r in rows]


def _decode_change(r: dict) -> dict:
    r["old"], r["new"] = json.loads(r["old"]), json.loads(r["new"])
    return r


def decide_change(change_id: int, approve: bool) -> None:
    """Approving applies the change to the item; rejecting leaves the item untouched."""
    ch = get_change(change_id)
    if not ch or ch["review"] != "proposed":
        return
    if approve:
        update_item(ch["item_id"], **ch["new"])
    with _lock, conn() as c:
        c.execute("UPDATE changes SET review = ? WHERE id = ?",
                  ("approved" if approve else "rejected", change_id))


def recover_stale_analyses() -> int:
    """After a crash/restart nothing is really analysing: make those chats retryable."""
    with _lock, conn() as c:
        return c.execute(
            "UPDATE chats SET status = 'error', error = ? WHERE status = 'analyzing'",
            ("Analiz yarıda kaldı (uygulama kapandı); 'Tekrar dene' kaldığı yerden devam eder / "
             "analysis was interrupted; retry resumes where it stopped",)).rowcount
