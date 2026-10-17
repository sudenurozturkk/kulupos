"""Event analysis: every figure is computed here from entered data; missing inputs stay None ("not entered").

The optional period insight is a short model comment written ONLY from these computed figures. Its text is
checked with the same digit-group rule as event reports (report.unsupported_figures) and rejected if it
contains a figure that is not in the computed facts.
"""
from __future__ import annotations

from . import db, llm, report


def _pct(num, den) -> int | None:
    """Whole percent, half up; None when an input is missing or the denominator is not positive."""
    if num is None or den is None or den <= 0:
        return None
    return int(num * 100 / den + 0.5)


def _n(x) -> str:
    """Compact number: 1720.0 -> 1720, 1720.5 -> 1720.5."""
    return f"{x:.2f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x)


def event_row(e: dict) -> dict:
    est, act = e["budget_est"], e["budget_actual"]
    dev = round(act - est, 2) if est is not None and act is not None else None
    return {
        "id": e["id"], "title": e["title"], "phase": e["phase"], "date": e["due"],
        "units": e["event_units"], "expected": e["attendees_expected"], "actual": e["attendees_actual"],
        "applications": e["applications"],
        "attendance_pct": _pct(e["attendees_actual"], e["attendees_expected"]),
        "conversion_pct": _pct(e["attendees_actual"], e["applications"]),
        "budget_est": est, "budget_actual": act, "budget_dev": dev,
        "budget_dev_pct": None if dev is None else _pct(abs(dev), est) if est and est > 0 else None,
        "budget_dev_sign": None if dev is None else (1 if dev > 0 else -1 if dev < 0 else 0),
        "feedback_score": e["feedback_score"], "feedback_note": e["feedback_note"],
        "feedback_good": e.get("feedback_good"), "feedback_bad": e.get("feedback_bad"),
    }


def compute(items: list[dict]) -> dict:
    """Approved, non-cancelled events only. Aggregates use only the events that have the needed inputs."""
    events = sorted((e for e in items if e["kind"] == "event" and e["phase"] != "cancelled"),
                    key=lambda e: (e["due"] or "9999", e["id"]))
    rows = [event_row(e) for e in events]
    with_att = [r for r in rows if r["actual"] is not None]
    rates = [r["attendance_pct"] for r in rows if r["attendance_pct"] is not None]
    scores = [r["feedback_score"] for r in rows if r["feedback_score"] is not None]
    hi = max(with_att, key=lambda r: r["actual"], default=None)
    # a lowest event only means something when at least two events have an attendance figure
    lo = min(with_att, key=lambda r: r["actual"]) if len(with_att) >= 2 else None
    committees: dict[str | None, int] = {}
    for r in rows:
        for u in (r["units"] or [None]):
            committees[u] = committees.get(u, 0) + 1
    return {
        "events": rows,
        "total": len(rows),
        "with_attendance": len(with_att),
        "avg_attendees": round(sum(r["actual"] for r in with_att) / len(with_att), 1) if with_att else None,
        "avg_attendance_pct": int(sum(rates) / len(rates) + 0.5) if rates else None,
        "avg_feedback": round(sum(scores) / len(scores), 1) if scores else None,
        "highest": {"title": hi["title"], "actual": hi["actual"]} if hi else None,
        "lowest": {"title": lo["title"], "actual": lo["actual"]} if lo else None,
        "committees": [{"unit": u, "events": n} for u, n in
                       sorted(committees.items(), key=lambda kv: (kv[0] is None, -kv[1], kv[0] or ""))],
    }


def compare(items: list[dict], today: str) -> list[dict]:
    """One row per non-cancelled event for the club-wide comparison. None = not enough recorded data (shown as "—"):
    no late-task count when no task is linked, no rate without both attendee figures, no score unless entered."""
    out = []
    for e in sorted((e for e in items if e["kind"] == "event" and e["phase"] != "cancelled"),
                    key=lambda e: (e["due"] or "9999", e["id"])):
        tasks = [i for i in items if i["kind"] == "task" and i["event_id"] == e["id"]]
        late = sum(1 for t in tasks if t["status"] == "open" and t["due"] and t["due"] < today)
        out.append({"id": e["id"], "title": e["title"], "phase": e["phase"], "date": e["due"],
                    "attendance_pct": _pct(e["attendees_actual"], e["attendees_expected"]),
                    "tasks": len(tasks) if tasks else None, "late_tasks": late if tasks else None,
                    "feedback_score": e["feedback_score"]})
    return out


# ---- period insight -----------------------------------------------------------

NO = {"tr": "Girilmedi", "en": "Not entered"}


def facts_text(stats: dict, lang: str) -> str:
    """The only input the model sees: computed figures, gaps spelled out."""
    no = NO[lang]

    def v(x, suffix=""):
        return no if x is None else f"{_n(x)}{suffix}"

    held = sum(1 for r in stats["events"] if r["phase"] == "held")
    lines = [f"Events recorded (planned or held, cancelled ones excluded): {stats['total']}",
             f"Events already held: {held}",
             f"Events with an actual attendance figure: {stats['with_attendance']}",
             f"Average actual attendees per event: {v(stats['avg_attendees'])}",
             f"Average attendance rate (actual/expected): {v(stats['avg_attendance_pct'], '%')}",
             f"Average feedback score (1-5): {v(stats['avg_feedback'])}",
             "Highest attendance: " + (no if not stats["highest"] else f"{stats['highest']['title']} ({stats['highest']['actual']})"),
             "Lowest attendance: " + (no if not stats["lowest"] else f"{stats['lowest']['title']} ({stats['lowest']['actual']})"),
             "Events per committee: " + (", ".join(f"{c['unit'] or no}: {c['events']}" for c in stats["committees"]) or no),
             "", "PER EVENT:"]
    for r in stats["events"]:
        dev = no if r["budget_dev"] is None else (
            ("+" if r["budget_dev"] > 0 else "") + _n(r["budget_dev"])
            + (f" ({'+' if r['budget_dev_sign'] > 0 else '-' if r['budget_dev_sign'] < 0 else ''}{r['budget_dev_pct']}%)"
               if r["budget_dev_pct"] is not None else ""))
        lines.append(f"- {r['title']} [{r['phase'] or no}]: expected {v(r['expected'])}, actual {v(r['actual'])}, applications {v(r['applications'])}, "
                     f"attendance rate {v(r['attendance_pct'], '%')}, application-to-attendance {v(r['conversion_pct'], '%')}, "
                     f"budget deviation {dev}, feedback {v(r['feedback_score'])}"
                     + (f"; went well: {r['feedback_good']}" if r.get("feedback_good") else "")
                     + (f"; fell short: {r['feedback_bad']}" if r.get("feedback_bad") else ""))
    return "\n".join(lines)


def _prompt(lang: str, facts: str, extra: str = "") -> list[dict]:
    language = "Turkish" if lang == "tr" else "English"
    no = NO[lang]
    system = (
        f"You write a period analysis (plain text, no emojis, about 8 to 12 sentences) in {language} on a student "
        f"club's events, for the club board, with four short headings: Genel görünüm, Güçlü yönler, Sorunlar, Sonraki "
        f"etkinlikler için öneriler (write the headings in {language}). Use ONLY the computed figures and feedback texts "
        f"below. Where a figure says \"{no}\", say it was not entered or leave it out; never guess, estimate, round, or "
        f"invent names, numbers or causes. Recommendations must follow from the feedback texts and figures (for example a "
        f"repeated problem). "
        f"Do not compute anything new: no extra percentages, sums or differences. Copy figures exactly as written. "
        f"Only events marked [held] have taken place; the others are planned, so do not describe them as done."
    )
    return [{"role": "system", "content": system},
            {"role": "user", "content": f"COMPUTED FIGURES:\n{facts}\n\nWrite the comment.{extra}"}]


async def generate(stats: dict, lang: str) -> dict:
    facts = facts_text(stats, lang)
    text = (await llm.chat(_prompt(lang, facts), temperature=0.2)).strip()
    bad = report.unsupported_figures(text, facts)
    if bad:
        extra = (f"\nYour previous draft contained figures that are not in the data: {', '.join(bad)}. "
                 f"Remove them; use only figures that appear in the data.")
        text = (await llm.chat(_prompt(lang, facts, extra), temperature=0.0)).strip()
        bad = report.unsupported_figures(text, facts)
        if bad:
            raise report.ReportRejected(bad)
    return {"insight": text, "fingerprint": report.fingerprint(facts), "model": llm.MODEL}


def insight_view(stats: dict, row: dict | None) -> dict:
    if not row:
        return {"insight": None}
    fresh = report.fingerprint(facts_text(stats, row["lang"])) == row["fingerprint"]
    return {"insight": row["body"], "stale": not fresh, "source": row["source"], "model": row["model"],
            "created_at": row["created_at"]}
