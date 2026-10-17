"""Weekly recap (ready to paste back into WhatsApp) and Q&A over the chat."""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta

from . import db, llm
from .analyzer import detect_lang, norm, render_messages

LABELS = {
    "tr": {"title": "Haftalık Özet", "done": "✅ Tamamlananlar", "open": "📌 Açık görevler",
           "orphan": "🙋 Sahibi olmayan görevler", "questions": "❓ Cevap bekleyen sorular",
           "events": "📅 Yaklaşan", "decisions": "🧭 Alınan kararlar", "nobody": "sahibi yok",
           "footer": "_KulüpOS ile bu bilgisayarda hazırlandı · Gemma 4 · veri dışarı çıkmadı_"},
    "en": {"title": "Weekly Recap", "done": "✅ Done", "open": "📌 Open tasks",
           "orphan": "🙋 Tasks nobody owns", "questions": "❓ Waiting for an answer",
           "events": "📅 Coming up", "decisions": "🧭 Decisions", "nobody": "no owner",
           "footer": "_Made on this laptop with KulüpOS · Gemma 4 · no data left the device_"},
}
MONTHS = {"tr": ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"],
          "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}


def short_date(iso: str | None, lang: str) -> str:
    if not iso:
        return ""
    d = date.fromisoformat(iso[:10])
    return f"{d.day} {MONTHS[lang][d.month - 1]}"


async def weekly_summary(chat_id: int, days: int = 7) -> dict:
    chat = db.get_chat(chat_id)
    msgs = db.get_messages(chat_id)
    lang = detect_lang(msgs)
    L = LABELS[lang]
    end = datetime.fromisoformat(chat["last_ts"])
    since = end - timedelta(days=days)
    recent = [m for m in msgs if datetime.fromisoformat(m["ts"]) >= since]
    recent_idx = {m["idx"] for m in recent}
    items = db.get_items(chat_id)

    prompt = (
        f"Here are the last {days} days of a student club's WhatsApp group "
        f"({since:%Y-%m-%d} – {end:%Y-%m-%d}).\n\n{render_messages(recent)[-14000:]}\n\n"
        f"Write a warm, concise recap of what happened this week for the club members: 3 to 5 "
        f"sentences, in {'Turkish' if lang == 'tr' else 'English'}, plain text, no lists, no "
        f"headings, no emojis. Mention concrete progress and what still needs attention. "
        f"Skip memes and small talk."
    )
    recap = (await llm.chat([{"role": "user", "content": prompt}], temperature=0.4)).strip()

    refs: list[int] = []

    def ref(i):
        if i.get("source_idx") is None:
            return ""
        if i["source_idx"] not in refs:
            refs.append(i["source_idx"])
        return f" [#{i['source_idx']}]"

    def line(i):
        bits = [i["title"]]
        if i["owner"]:
            bits.append(i["owner"].split()[0])
        if i["due"]:
            bits.append(f"📅 {short_date(i['due'], lang)}")
        return "• " + " — ".join(bits) + ref(i)

    tasks = [i for i in items if i["kind"] == "task"]
    # done = resolved by a message in the window, or marked done by the user within the window (wall clock);
    # a done task with no resolution info is not "this week's" and stays out
    now_since = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
    done = [t for t in tasks if t["status"] == "done" and (
        t["resolved_idx"] in recent_idx
        or (t["resolved_idx"] is None and t["user_edited"] and t["updated_at"] >= now_since))]
    open_ = [t for t in tasks if t["status"] == "open" and t["owner"]]
    orphan = [t for t in tasks if t["status"] == "open" and not t["owner"]]
    questions = [q for q in items if q["kind"] == "question" and q["status"] == "open"]
    upcoming = sorted((e for e in items if e["kind"] == "event" and e["due"]
                       and e["due"] >= end.date().isoformat()), key=lambda e: e["due"])
    decisions = [d for d in items if d["kind"] == "decision" and d["source_idx"] in recent_idx]

    parts = [f"*📋 {chat['name']} — {L['title']}*",
             f"_{short_date(since.date().isoformat(), lang)} – {short_date(end.date().isoformat(), lang)}_",
             "", recap]
    for label, rows, fmt in (
        (L["done"], done, line), (L["open"], open_, line), (L["orphan"], orphan, line),
        (L["questions"], questions, lambda q: f"• {q['title']}" + (f" — {q['owner'].split()[0]}" if q["owner"] else "") + ref(q)),
        (L["decisions"], decisions, lambda d: f"• {d['title']}" + ref(d)),
        (L["events"], upcoming, lambda e: f"• {e['title']} — {short_date(e['due'], lang)}"
                                          + (f" {e['time']}" if e["time"] else "") + ref(e)),
    ):
        if rows:
            parts += ["", f"*{label}*", *map(fmt, rows)]
    parts += ["", L["footer"]]
    by_idx = {m["idx"]: m for m in msgs}
    return {"text": "\n".join(parts), "lang": lang,
            "sources": [{"idx": i, "sender": by_idx[i]["sender"], "ts": by_idx[i]["ts"]} for i in refs if i in by_idx]}


STOP = set("""ve veya ile bir bu şu o ne mi mı mu mü da de ki için gibi kadar daha en çok
var yok mu ben sen biz siz onlar ama fakat hangi kim kimde kime neden nasıl zaman when what who
which the a an is are was were to of in on for and or do does did we you i it this that how why""".split())


def _terms(text: str) -> list[str]:
    # Turkish is agglutinative: compare 5-letter stems ("afişi", "afişin" -> "afis").
    return [w[:5] for w in norm(text).split() if w not in STOP and len(w) > 1]


def club_context(chat_id: int) -> tuple[str, dict[str, dict]]:
    """The club's own approved records as text lines with citable ids, plus an index id -> record."""
    idx: dict[str, dict] = {}
    lines: list[str] = []

    def add(ref, kind, rec, text, href=None):
        idx[ref] = {"ref": ref, "kind": kind, "id": rec["id"], "title": rec["title"], "href": href}
        lines.append(f"[{ref}] {text}")

    def v(x):
        return "-" if x in (None, "", []) else str(x)

    items = db.get_items(chat_id)
    events = {e["id"]: e for e in items if e["kind"] == "event"}
    for e in events.values():
        fb = " ".join(x for x in (e.get("feedback_note"), e.get("feedback_good"), e.get("feedback_bad")) if x)
        add(f"E{e['id']}", "event", e,
            f"EVENT {e['title']} | status {v(e['phase'])} | date {v(e['due'])} | place {v(e['place'])} | owner {v(e['owner'])} | "
            f"teams {v(', '.join(e['event_units']))} | applications {v(e['applications'])} | expected {v(e['attendees_expected'])} | "
            f"actual {v(e['attendees_actual'])} | budget plan {v(e['budget_est'])} | budget actual {v(e['budget_actual'])} | "
            f"feedback score {v(e['feedback_score'])} | feedback {v(fb)}", href=f"#/c/{chat_id}/event/{e['id']}")
    for t in (i for i in items if i["kind"] == "task"):
        ev = events.get(t["event_id"])
        add(f"T{t['id']}", "task", t, f"TASK {t['title']} | {t['status']} | team {v(t['unit'])} | owner {v(t['owner'])} | "
            f"due {v(t['due'])} | event {v(ev['title'] if ev else None)}")
    for d in (i for i in items if i["kind"] == "decision" and i["validity"] == "valid"):
        add(f"D{d['id']}", "decision", d, f"DECISION {d['title']} | {d['status']}")
    for q in (i for i in items if i["kind"] == "question"):
        add(f"Q{q['id']}", "question", q, f"OPEN QUESTION {q['title']} | {q['status']}")
    for m in db.get_meetings(chat_id):
        notes = " ".join((m.get("notes") or "").split())[:300]
        add(f"M{m['id']}", "meeting", m, f"MEETING {m['title']} | {v(m['date'])} | {m['status']} | notes: {v(notes)}",
            href=f"#/c/{chat_id}/meeting/{m['id']}")
    return "\n".join(lines), idx


async def ask(chat_id: int, question: str) -> dict:
    """Answer from the club's records (tasks, events, feedback, decisions, meetings) and, if the club imported one,
    the relevant chat excerpts. The answer cites record ids [T12] and message ids [#12]."""
    msgs = [m for m in db.get_messages(chat_id) if m["kind"] in ("text", "media")]
    data, idx = club_context(chat_id)
    context = []
    if msgs:
        q_terms = set(_terms(question))
        scored = [(len(q_terms & set(_terms(m["text"]))), pos) for pos, m in enumerate(msgs)]
        keep: set[int] = set()
        for _, pos in sorted([x for x in scored if x[0]], reverse=True)[:15]:
            keep.update(range(max(0, pos - 1), min(len(msgs), pos + 2)))
        keep.update(range(max(0, len(msgs) - 8), len(msgs)))
        context = [msgs[p] for p in sorted(keep)]

    lang = detect_lang(msgs) if msgs else "tr"
    chat_part = "\n\nIMPORTED CHAT EXCERPTS:\n" + render_messages(context) if context else ""
    prompt = (
        "CLUB RECORDS (entered or approved by the club; '-' means not entered):\n" + data + chat_part + "\n\n"
        f"Today is {date.today().isoformat()}. Answer the question using ONLY the records and excerpts above; do not "
        "use outside knowledge and never invent names, numbers or dates. Be concrete and brief (2-5 sentences, or a short "
        "list). Cite the records you used like [T12], [E3], [D5], [M2] and chat messages like [#12]. If the data does not "
        "contain the answer, say what is missing. "
        f"Answer in {'Turkish' if lang == 'tr' else 'English'}.\n\nQuestion: {question}"
    )
    answer = (await llm.chat([{"role": "user", "content": prompt}], temperature=0.2)).strip()
    cited = sorted({int(n) for n in re.findall(r"#(\d+)", answer)})
    by_idx = {m["idx"]: m for m in msgs}
    refs = list(dict.fromkeys(re.findall(r"\b([TEDQM]\d+)\b", answer)))
    return {"answer": answer, "sources": [by_idx[i] for i in cited if i in by_idx], "records": [idx[r] for r in refs if r in idx]}
