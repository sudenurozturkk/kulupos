"""Write the precomputed report of the held sample event (Python workshop, with feedback) into
demo/seed-report-tr.json (needs Ollama running; ~1-2 min).

    python scripts/make_sample_event_report.py

Uses a throwaway database. The text is whatever the local model produced and passed the figure and quotation
checks; nothing is edited by hand.
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

from app import db, llm, report, seed  # noqa: E402

PATH = ROOT / "demo" / "seed-report-tr.json"
KEY = "atolye"


async def main() -> None:
    health = await llm.health()
    if not health["model_ready"]:
        sys.exit(f"Model not ready: {health}")
    PATH.unlink(missing_ok=True)
    chat_id = seed.seed_sample(date.today())
    title = next(e["title"] for e in json.loads(seed.SPEC.read_text(encoding="utf-8"))["events"] if e["key"] == KEY)
    ev = next(e for e in db.get_items(chat_id, "event") if e["title"] == title)
    r = await report.generate(ev, "tr")
    PATH.write_text(json.dumps({"key": KEY, "lang": "tr", "model": r["model"], "report": r["report"]},
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(r["report"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
