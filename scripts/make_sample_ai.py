"""Write what the local model produces for the sample club into demo/seed-ai-tr.json (needs Ollama running; ~5 min):
task/decision/question suggestions from the held meeting's notes, event ideas from the held events, and an event plan.

    python scripts/make_sample_ai.py

Uses a throwaway database. Nothing is edited by hand; the seed loads this file so the sample club ships with real
model output (source = sample).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["PANO_DB"] = str(Path(tempfile.mkdtemp()) / "sample.db")

from app import db, insights, llm, meetings, seed  # noqa: E402

PATH = ROOT / "demo" / "seed-ai-tr.json"
HELD_MEETING = "yonetim"
GOAL = "Kasım ayında 150 kişilik bir siber güvenlik çalıştayı düzenlemek istiyoruz"


async def main() -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    PATH.unlink(missing_ok=True)
    today = date.today()
    chat_id = seed.seed_sample(today)
    spec = json.loads(seed.MEETINGS.read_text(encoding="utf-8"))
    title = next(m["title"] for m in spec["meetings"] if m["key"] == HELD_MEETING)
    meeting = next(m for m in db.get_meetings(chat_id) if m["title"] == title)
    for i in db.get_items(chat_id, review="proposed"):
        if i["meeting_id"] == meeting["id"]:
            db.delete_item(i["id"])
    db.update_meeting(meeting["id"], analyzed_fp=None)
    stats = await meetings.analyze(meeting["id"])
    proposals = [{"kind": i["kind"], "title": i["title"], "unit": i["unit"], "owner": i["owner"], "due": i["due"],
                  "source_text": i["source_text"]}
                 for i in db.get_items(chat_id, review="proposed") if i["meeting_id"] == meeting["id"]]
    ideas = await insights.suggest_events(chat_id, today)
    plan = await insights.plan_event(chat_id, GOAL, today)
    PATH.write_text(json.dumps({"model": llm.MODEL, "meeting": HELD_MEETING, "proposals": proposals,
                                "ideas": ideas, "plan": {**plan, "goal": GOAL}}, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print(stats, len(proposals), "proposals;", len(ideas["ideas"]), "ideas;", len(plan["tasks"]), "plan tasks;",
          len(plan["meetings"]), "plan meetings")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
