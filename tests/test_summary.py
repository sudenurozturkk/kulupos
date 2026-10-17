"""Weekly recap: "Done" section and source references. Fake model, no Ollama."""
import asyncio
import importlib

from fastapi.testclient import TestClient

CHAT = ("01.09.2026 10:00 - Ayşe: Afişi ben yaparım\n"
        "02.09.2026 10:00 - Mert: Salonu ben ayarlarım\n"
        "16.10.2026 10:00 - Ayşe: Afiş bitti\n"
        "17.10.2026 10:00 - Mert: Sponsor mektubu hazır\n")


def load(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "s.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import assistant, main
    importlib.reload(assistant)
    importlib.reload(main)

    async def fake(*a, **k):
        return "Kısa özet."
    monkeypatch.setattr(assistant.llm, "chat", fake)
    return db, assistant, main


def test_done_section_only_this_week_and_has_source_refs(tmp_path, monkeypatch):
    db, assistant, main = load(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        old = db.add_item(cid, "task", title="Eski afiş", status="done", source_idx=0, resolved_idx=0)
        new = db.add_item(cid, "task", title="Yeni afiş", status="done", source_idx=0, resolved_idx=2)
        unknown = db.add_item(cid, "task", title="Tarihsiz bitti", status="done", source_idx=1)  # no resolution info
        db.add_item(cid, "task", title="Sponsor mektubu", status="open", owner="Mert", source_idx=3)
        db.add_item(cid, "decision", title="Etkinlik 31 Ekim", source_idx=3)
        db.add_item(cid, "task", title="Kaynaksız açık", status="open", owner="Ayşe")
        r = c.post(f"/api/chats/{cid}/summary", json={"days": 7}).json()
    text = r["text"]
    done_block = text.split("✅ Tamamlananlar*")[1].split("*")[0]
    assert "Yeni afiş" in done_block
    assert "Eski afiş" not in text and "Tarihsiz bitti" not in text
    assert "Sponsor mektubu — Mert [#3]" in text or "Sponsor mektubu — Mert" in text and "[#3]" in text
    assert "Kaynaksız açık" in text and "Kaynaksız açık — Ayşe [#" not in text
    assert {s["idx"] for s in r["sources"]} == {0, 3}
