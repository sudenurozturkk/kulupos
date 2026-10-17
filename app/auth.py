"""Local account: one sign-in for the person running KulüpOS. No roles, no per-record permissions.

Anyone can create an account (all accounts share the same club data: there are no roles or per-user data). A demo
visitor gets a guest session that sees only the sample club. Passwords are stored as
salted PBKDF2 hashes in the local database, sessions are random tokens in an HttpOnly cookie kept in memory
(restarting the server signs everyone out). Set PANO_AUTH=0 to turn the check off (tests, demos on a trusted machine).
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets

from . import db

COOKIE = "pano_session"
OPEN = ("/api/auth/", "/api/health")
GUEST = "Demo"
_sessions: dict[str, str] = {}

TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, salt TEXT NOT NULL, pw_hash TEXT NOT NULL)"


def enabled() -> bool:
    return os.environ.get("PANO_AUTH", "1") != "0"


def _hash(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 120_000).hex()


def _users() -> list[dict]:
    with db._lock, db.conn() as c:
        c.execute(TABLE)
    return db._rows("SELECT * FROM users ORDER BY id")


def has_users() -> bool:
    return bool(_users())


def register(username: str, password: str) -> str:
    username = username.strip()
    if len(username) < 3 or len(password) < 6:
        raise ValueError("Kullanıcı adı en az 3, parola en az 6 karakter olmalı / username 3+ and password 6+ characters")
    if any(u["username"].casefold() == username.casefold() for u in _users()) or username.casefold() == GUEST.casefold():
        raise PermissionError("Bu kullanıcı adı alınmış / that username is taken")
    salt = secrets.token_hex(16)
    with db._lock, db.conn() as c:
        c.execute("INSERT INTO users (username, salt, pw_hash) VALUES (?, ?, ?)", (username, salt, _hash(password, salt)))
    return login(username, password)


def login(username: str, password: str) -> str:
    row = next((u for u in _users() if u["username"].casefold() == username.strip().casefold()), None)
    ok = row is not None and hmac.compare_digest(_hash(password, row["salt"]), row["pw_hash"])
    if not ok:
        raise PermissionError("Kullanıcı adı veya parola yanlış / wrong username or password")
    token = secrets.token_urlsafe(32)
    _sessions[token] = row["username"]
    return token


def guest() -> str:
    """Demo visitor: can open the sample club only; their chat list is limited to sample clubs."""
    token = secrets.token_urlsafe(32)
    _sessions[token] = GUEST
    return token


def is_guest(token: str | None) -> bool:
    return _sessions.get(token or "") == GUEST


def user_of(token: str | None) -> str | None:
    return _sessions.get(token or "")


def logout(token: str | None) -> None:
    _sessions.pop(token or "", None)
