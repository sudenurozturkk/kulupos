"""AI event report built only from what was entered about the event.

The prompt contains the event's recorded fields plus its linked tasks and decisions; empty fields are
written as "Girilmedi" / "Not entered" and the model is told never to fill them in. Afterwards every
number in the answer must be traceable to the input, otherwise the report is rejected.
"""
from __future__ import annotations

import hashlib
import re

from . import db, llm

PHASE = {
    "tr": {"idea": "Fikir", "planning": "Planlanıyor", "confirmed": "Kesinleşti", "held": "Gerçekleşti",
           "cancelled": "İptal"},
    "en": {"idea": "Idea", "planning": "Planning", "confirmed": "Confirmed", "held": "Held",
           "cancelled": "Cancelled"},
}
EMPTY = {"tr": "Girilmedi", "en": "Not entered"}
SECTIONS = {"tr": "Özet, Görevler, Kararlar, Açık noktalar", "en": "Summary, Tasks, Decisions, Open points"}


class ReportRejected(Exception):
    """The model's text contained figures that are not in the recorded data."""

    def __init__(self, unsupported: list[str]):
        super().__init__("unsupported figures: " + ", ".join(unsupported))
        self.unsupported = unsupported


def _linked(event: dict) -> tuple[list[dict], list[dict]]:
    items = db.get_items(event["chat_id"])
    tasks = [i for i in items if i["kind"] == "task" and i["event_id"] == event["id"]]
    decisions = [i for i in items if i["kind"] == "decision" and i["event_id"] == event["id"]]
    return tasks, decisions


def facts_text(event: dict, lang: str) -> str:
    """The only input the model sees. Empty fields are spelled out, never omitted."""
    no = EMPTY[lang]
    tasks, decisions = _linked(event)
    done = [t for t in tasks if t["status"] == "done"]

    def v(x):
        return no if x in (None, "", []) else str(x)

    lines = [
        f"EVENT: {event['title']}",
        f"Type: {v(event['event_type'])}",
        f"Status: {v(PHASE[lang].get(event['phase'] or '', event['phase']))}",
        f"Date: {v(event['due'])}",
        f"Time: {v(event['time'])}",
        f"Venue: {v(event['place'])}",
        f"Responsible: {v(event['owner'])}",
        f"Teams: {v(', '.join(event['event_units']))}",
        f"Expected attendees: {v(event['attendees_expected'])}",
        f"Actual attendees: {v(event['attendees_actual'])}",
        f"Budget estimate: {v(event['budget_est'])}",
        f"Actual budget: {v(event['budget_actual'])}",
        f"Notes: {v(event['notes'])}",
        "",
        f"LINKED TASKS (total {len(tasks)}, done {len(done)}, open {len(tasks) - len(done)}):",
    ]
    lines += [f"- [{'done' if t['status'] == 'done' else 'open'}] {t['title']} | owner: {v(t['owner'])} | "
              f"due: {v(t['due'])}" for t in tasks] or ["(none entered)"]
    lines.append("LINKED DECISIONS:")
    lines += [f"- {d['title']}" for d in decisions] or ["(none entered)"]
    return "\n".join(lines)


def _prompt(event: dict, lang: str, facts: str, extra: str = "") -> list[dict]:
    language = "Turkish" if lang == "tr" else "English"
    no = EMPTY[lang]
    system = (
        f"You write a short factual event report for a student club, in {language}. Use ONLY the "
        f"recorded data below. Where a field says \"{no}\", write \"{no}\" for it or leave it out; "
        f"never guess, estimate, round, or invent names, numbers, dates, places or outcomes. Do not "
        f"compute percentages or differences. Do not add numbers that are not in the data. "
        f"Plain text with these short sections, headings written in {language}: {SECTIONS[lang]}. "
        f"List open (not done) tasks under the last section. No emojis."
    )
    return [{"role": "system", "content": system},
            {"role": "user", "content": f"RECORDED DATA:\n{facts}\n\nWrite the report.{extra}"}]


_LIST_MARK = re.compile(r"^\s*(?:\d+[.)]|[-*•])\s+", re.M)
_NUM = re.compile(r"\d+")


def _digits(text: str) -> set[str]:
    return {n.lstrip("0") or "0" for n in _NUM.findall(text)}


def unsupported_figures(report: str, facts: str) -> list[str]:
    """Digit groups in the report that do not occur in the input (list numbering ignored)."""
    allowed = _digits(facts)
    body = _LIST_MARK.sub("", report)
    return sorted({n for n in _digits(body) if n not in allowed}, key=int)


def fingerprint(facts: str) -> str:
    return hashlib.sha256(facts.encode("utf-8")).hexdigest()[:16]


def language_of(chat_id: int) -> str:
    from .analyzer import detect_lang
    return detect_lang(db.get_messages(chat_id)[:200])


async def generate(event: dict, lang: str) -> dict:
    """Ask the model, check the figures, retry once with the offending figures named."""
    facts = facts_text(event, lang)
    text = (await llm.chat(_prompt(event, lang, facts), temperature=0.2)).strip()
    bad = unsupported_figures(text, facts)
    if bad:
        extra = (f"\nYour previous draft contained figures that are not in the data: {', '.join(bad)}. "
                 f"Remove them; use only figures that appear in the data.")
        text = (await llm.chat(_prompt(event, lang, facts, extra), temperature=0.0)).strip()
        bad = unsupported_figures(text, facts)
        if bad:
            raise ReportRejected(bad)
    return {"report": text, "fingerprint": fingerprint(facts), "model": llm.MODEL}

