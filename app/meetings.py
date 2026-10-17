"""Meetings: notes handling and checks. Meeting notes are untrusted data, like chat text:
they are size- and encoding-checked here and only ever enter a prompt as quoted data."""
from __future__ import annotations

import re
from datetime import date

MAX_NOTES_BYTES = 100_000
NOTES_EXT = (".txt", ".md")
STATUSES = ("planned", "held", "cancelled")


class NotesError(ValueError):
    pass


def decode_notes(data: bytes, filename: str = "") -> str:
    """Bytes of an uploaded .txt/.md file -> text. Raises NotesError with a readable message."""
    if filename and not filename.lower().endswith(NOTES_EXT):
        raise NotesError("Yalnızca .txt veya .md dosyaları yüklenebilir / only .txt or .md files can be uploaded")
    if not data.strip():
        raise NotesError("Dosya boş / the file is empty")
    if len(data) > MAX_NOTES_BYTES:
        raise NotesError(f"Dosya {MAX_NOTES_BYTES // 1000} KB sınırını aşıyor / file exceeds the {MAX_NOTES_BYTES // 1000} KB limit")
    try:
        text = data.decode("utf-16") if data[:2] in (b"\xff\xfe", b"\xfe\xff") else data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise NotesError("Dosya UTF-8 (veya BOM'lu UTF-16) metin değil; UTF-8 olarak kaydedip tekrar deneyin / "
                         "the file is not UTF-8 (or BOM'd UTF-16) text; save it as UTF-8 and retry")
    return clean_notes(text)


def clean_notes(text: str) -> str:
    """Normalise line endings; refuse binary content. Length is checked by the caller's field limit."""
    if "\x00" in text or sum(1 for ch in text if ord(ch) < 32 and ch not in "\n\r\t") > 5:
        raise NotesError("Dosya metin gibi görünmüyor / the file does not look like text")
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def note_lines(notes: str | None) -> list[str]:
    """The numbered units a source can point at: non-empty lines, trimmed."""
    return [ln.strip() for ln in (notes or "").split("\n") if ln.strip()]


def valid_date(s: str | None) -> str | None:
    s = (s or "").strip()
    if not s:
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        raise ValueError("date")
    date.fromisoformat(s)  # ValueError for 2026-02-31
    return s


def valid_time(s: str | None) -> str | None:
    s = (s or "").strip()
    if not s:
        return None
    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", s):
        raise ValueError("time")
    return s
