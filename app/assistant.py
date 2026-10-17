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
           "footer": "_Pano ile bu bilgisayarda hazırlandı · Gemma 4 · veri dışarı çıkmadı_"},
    "en": {"title": "Weekly Recap", "done": "✅ Done", "open": "📌 Open tasks",
           "orphan": "🙋 Tasks nobody owns", "questions": "❓ Waiting for an answer",
           "events": "📅 Coming up", "decisions": "🧭 Decisions", "nobody": "no owner",
           "footer": "_Made on this laptop with Pano · Gemma 4 · no data left the device_"},
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


async def ask(chat_id: int, question: str) -> dict:
    msgs = [m for m in db.get_messages(chat_id) if m["kind"] in ("text", "media")]
    q_terms = set(_terms(question))
    scored = []
    for pos, m in enumerate(msgs):
        hits = len(q_terms & set(_terms(m["text"])))
        if hits:
            scored.append((hits, pos))
    keep: set[int] = set()
    for _, pos in sorted(scored, reverse=True)[:25]:
        keep.update(range(max(0, pos - 2), min(len(msgs), pos + 3)))
    keep.update(range(max(0, len(msgs) - 15), len(msgs)))  # always include the latest messages
    context = [msgs[p] for p in sorted(keep)]

    lang = detect_lang(msgs)
    prompt = (
        f"Excerpts from a student club's WhatsApp group:\n\n{render_messages(context)}\n\n"
        f"Today is {date.today().isoformat()}. Answer the question using ONLY these messages. "
        f"Be brief (1-3 sentences) and cite the message ids you used like [#12]. If the messages "
        f"do not contain the answer, say so. Answer in {'Turkish' if lang == 'tr' else 'English'}."
        f"\n\nQuestion: {question}"
    )
    answer = (await llm.chat([{"role": "user", "content": prompt}], temperature=0.2)).strip()
    cited = sorted({int(n) for n in re.findall(r"#(\d+)", answer)})
    by_idx = {m["idx"]: m for m in msgs}
    return {"answer": answer, "sources": [by_idx[i] for i in cited if i in by_idx]}
