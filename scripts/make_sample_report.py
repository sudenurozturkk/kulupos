"""Write the precomputed report of the demo event into demo/sample-event.json (needs Ollama running).

    python scripts/make_sample_report.py

Uses a throwaway database. The text is whatever the local model produced and passed the figure check;
nothing is edited by hand.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["PANO_DB"] = str(Path(tempfile.mkdtemp()) / "sample.db")

from app import db, llm, report  # noqa: E402
from app.parser import Message  # noqa: E402
from datetime import datetime  # noqa: E402

PATH = ROOT / "demo" / "sample-event.json"


async def main() -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    spec = json.loads(PATH.read_text(encoding="utf-8"))
    chat_id = db.create_chat("sample", [], [Message(0, datetime(2026, 3, 1), "Ayşe", "merhaba", "text")])
    event_id = db.add_item(chat_id, "event", **spec["event"])
    for t in spec["tasks"]:
        db.add_item(chat_id, "task", event_id=event_id, **t)
    for d in spec["decisions"]:
        db.add_item(chat_id, "decision", event_id=event_id, title=d)
    r = await report.generate(db.get_item(event_id), spec["lang"])
    spec["report"], spec["model"] = r["report"], r["model"]
    PATH.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(r["report"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
