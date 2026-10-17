"""WhatsApp chat export parser.

Handles the four common export flavours:
  Android TR  17.10.2026 19:32 - Ayşe: mesaj
  iOS TR      [17.10.2026 19:32:05] Ayşe: mesaj
  Android EN  10/17/26, 7:32 PM - Ayşe: message
  iOS EN      [10/17/26, 7:32:05 PM] Ayşe: message
Multi-line messages, system lines, media placeholders and the invisible
unicode marks WhatsApp sprinkles into exports are handled too.
"""
from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime

INVISIBLE = dict.fromkeys(map(ord, "‎‏‪‫‬‭‮﻿"), None)
SPACES = {ord(" "): " ", ord(" "): " ", ord(" "): " "}

_DATE = r"(\d{1,2})[./-](\d{1,2})[./-](\d{2,4}),?\s+(\d{1,2})[:.](\d{2})(?:[:.](\d{2}))?\s*([AaPp]\.?\s?[Mm]\.?)?"
IOS_LINE = re.compile(r"^\[" + _DATE + r"\]\s*(.*)$")
ANDROID_LINE = re.compile(r"^" + _DATE + r"\s*[-–]\s*(.*)$")

MEDIA_MARKERS = (
    "<medya dahil edilmedi>", "<media omitted>", "dahil edilmedi", "omitted>",
    "image omitted", "video omitted", "audio omitted", "sticker omitted",
    "document omitted", "gif omitted", "<attached:", "(dosya ekli)", "(file attached)",
)
# Phrases that only ever appear in WhatsApp's own notices, never in normal chat.
SYSTEM_MARKERS = (
    "end-to-end encrypted", "uçtan uca şifreli", "created group", "grubunu oluşturdu",
    "changed the subject", "konusunu değiştirdi", "security code changed", "güvenlik kodu değişti",
)
DELETED_MARKERS = (
    "bu mesaj silindi", "this message was deleted", "you deleted this message",
    "bu mesajı sildiniz",
)


@dataclass
class Message:
    idx: int
    ts: datetime
    sender: str | None
    text: str
    kind: str  # text | media | system | deleted

    def to_dict(self) -> dict:
        d = asdict(self)
        d["ts"] = self.ts.isoformat(timespec="minutes")
        return d


def _clean(line: str) -> str:
    return line.translate(INVISIBLE).translate(SPACES).rstrip("\r\n")


def _match(line: str):
    return IOS_LINE.match(line) or ANDROID_LINE.match(line)


def _detect_day_first(lines: list[str]) -> bool:
    """Decide between DD/MM and MM/DD by looking at the whole file."""
    seps, ampm = set(), False
    for line in lines:
        m = _match(line)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            return True
        if b > 12:
            return False
        sep = re.search(r"\d([./-])\d", line)
        if sep:
            seps.add(sep.group(1))
        ampm = ampm or bool(m.group(7))
    if "." in seps:
        return True
    return not ampm  # "/" with AM/PM is almost always a US export


def _to_datetime(m: re.Match, day_first: bool) -> datetime:
    a, b, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    day, month = (a, b) if day_first else (b, a)
    if year < 100:
        year += 2000
    hour, minute = int(m.group(4)), int(m.group(5))
    second = int(m.group(6) or 0)
    meridiem = (m.group(7) or "").lower().replace(".", "").replace(" ", "")
    if meridiem == "pm" and hour < 12:
        hour += 12
    elif meridiem == "am" and hour == 12:
        hour = 0
    return datetime(year, month, day, hour, minute, second)


def _classify(text: str) -> str:
    low = text.strip().lower()
    if any(mark in low for mark in DELETED_MARKERS):
        return "deleted"
    if any(mark in low for mark in MEDIA_MARKERS):
        return "media"
    return "text"


def parse_chat(raw: str) -> list[Message]:
    return parse_report(raw)[0]


def parse_report(raw: str) -> tuple[list[Message], int]:
    """Messages plus the number of non-empty lines that could not be placed anywhere."""
    skipped = 0
    raw_lines = raw.splitlines()
    lines = [_clean(line) for line in raw_lines]
    day_first = _detect_day_first(lines)
    messages: list[Message] = []

    for raw_line, line in zip(raw_lines, lines):
        m = _match(line)
        if not m:
            # Continuation of a multi-line message.
            if messages and line.strip():
                messages[-1].text += "\n" + line
            elif line.strip():
                skipped += 1  # text before the first message
            continue

        try:
            ts = _to_datetime(m, day_first)
        except ValueError:  # e.g. 31.02.2026
            skipped += 1
            continue
        body = m.group(8)
        sender, sep, text = body.partition(": ")
        if not sep:
            # Android: "Ayşe gruba katıldı", encryption notice, etc.
            messages.append(Message(len(messages), ts, None, body.strip(), "system"))
            continue
        sender = sender.strip().lstrip("~").strip()
        text = text.strip()
        # iOS marks system lines and attachments with a left-to-right mark after "Name: ".
        marked = ": ‎" in raw_line
        low = text.lower()
        if _classify(text) == "text" and (
            (marked and len(text) < 160) or any(s in low for s in SYSTEM_MARKERS)
        ):
            messages.append(Message(len(messages), ts, None, text, "system"))
            continue
        messages.append(Message(len(messages), ts, sender, text, "text"))

    for msg in messages:
        if msg.kind == "text":
            msg.kind = _classify(msg.text)
    return messages, skipped


MAX_BYTES = 5 * 1024 * 1024


def read_export(data: bytes) -> str:
    """Accept a raw .txt export or the .zip WhatsApp produces with media."""
    if data[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            txts = [n for n in zf.namelist() if n.lower().endswith(".txt")]
            if not txts:
                raise ValueError("Zip içinde .txt sohbet dosyası yok / no .txt chat in zip")
            name = next((n for n in txts if "chat" in n.lower() or "sohbet" in n.lower()), txts[0])
            if zf.getinfo(name).file_size > MAX_BYTES:
                raise ValueError("Dosya 5 MB sınırını aşıyor / file exceeds the 5 MB limit")
            data = zf.read(name)
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("cp1254", errors="replace")  # old Turkish Windows exports
