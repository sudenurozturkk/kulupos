"""End to end through the HTTP API with a fake model. No Ollama needed."""
import asyncio
import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = ("17.10.2026 19:33 - Ayşe: Afişi ben yaparım\n"
        "17.10.2026 19:34 - Mert: Salon dilekçesini kim verir?\n"
        "17.10.2026 19:35 - Ayşe: Karar: söyleşi 31 Ekim\n")

RESULT = {
    "new_tasks": [{"title": "Afiş hazırla", "owner": "Ayşe", "due": "", "unit": "", "source": 0}],
    "new_questions": [{"text": "Salon dilekçesini kim verir?", "asked_by": "Mert", "source": 1}],
    "decisions": [{"text": "Söyleşi 31 Ekim", "source": 2}],
}


def load(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "e2e.db"))
    from app import db
    db._conn = None  # drop the old connection, as a restart would
    importlib.reload(db)
    from app import analyzer, main
    importlib.reload(analyzer)
    importlib.reload(main)
    return db, analyzer, main


def analyze(analyzer, chat_id):
    asyncio.run(analyzer.analyze(chat_id))


def test_full_flow_and_persistence(tmp_path, monkeypatch):
    db, analyzer, main = load(tmp_path, monkeypatch)

    async def fake(*a, **k):
        return RESULT
    monkeypatch.setattr(analyzer.llm, "chat_json", fake)

    with TestClient(main.app) as c:
        cid = c.post("/api/chats?name=KBK&units=Etkinlik,Sosyal", content=CHAT.encode()).json()["id"]
        analyze(analyzer, cid)
        b = c.get(f"/api/chats/{cid}/board").json()
        assert b["chat"]["status"] == "ready" and b["tasks"] == [] and len(b["review"]) == 3

        for i in b["review"]:
            assert c.patch(f"/api/items/{i['id']}", json={"review": "approved"}).status_code == 200
        task = c.get(f"/api/chats/{cid}/board").json()["tasks"][0]
        assert c.patch(f"/api/items/{task['id']}", json={"status": "done"}).json()["status"] == "done"

    # "restart": fresh module state and connection, same database file
    db2, _, main2 = load(tmp_path, monkeypatch)
    with TestClient(main2.app) as c:
        b = c.get(f"/api/chats/{cid}/board").json()
        assert [(t["title"], t["status"]) for t in b["tasks"]] == [("Afiş hazırla", "done")]
        assert b["review"] == [] and len(b["decisions"]) == 1
        md = c.get(f"/api/chats/{cid}/export.md").text
        assert "- [x] Afiş hazırla" in md and "Söyleşi 31 Ekim" in md and "Salon dilekçesini kim verir?" in md


def test_ollama_down_is_a_readable_error_not_a_crash(tmp_path, monkeypatch):
    db, analyzer, main = load(tmp_path, monkeypatch)
    monkeypatch.setattr(analyzer.llm, "OLLAMA_URL", "http://127.0.0.1:1")  # nothing listens here
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        analyze(analyzer, cid)
        b = c.get(f"/api/chats/{cid}/board").json()
        assert b["chat"]["status"] == "error" and "Ollama" in b["chat"]["error"]
        assert b["progress"]["state"] == "error"
        assert c.post(f"/api/chats/{cid}/summary", json={"days": 7}).status_code == 503
        assert c.get("/api/health").json()["ollama"] is False

        async def fake(*a, **k):
            return RESULT
        monkeypatch.setattr(analyzer.llm, "chat_json", fake)
        analyze(analyzer, cid)  # retry works after the model comes back
        assert c.get(f"/api/chats/{cid}/board").json()["chat"]["status"] == "ready"


def test_bad_model_json_is_an_error_then_retry_recovers(tmp_path, monkeypatch):
    db, analyzer, main = load(tmp_path, monkeypatch)

    async def junk(*a, **k):
        return "bu JSON değil"
    monkeypatch.setattr(analyzer.llm, "chat", junk)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        analyze(analyzer, cid)
        chat = c.get(f"/api/chats/{cid}/board").json()["chat"]
        assert chat["status"] == "error" and chat["error"] and chat["analyzed_upto"] == -1

        async def wrapped(*a, **k):  # chatter around valid JSON is tolerated
            import json
            return "Tabii:\n" + json.dumps(RESULT)
        monkeypatch.setattr(analyzer.llm, "chat", wrapped)
        analyze(analyzer, cid)
        b = c.get(f"/api/chats/{cid}/board").json()
        assert b["chat"]["status"] == "ready" and len(b["review"]) == 3


def test_stale_analyzing_becomes_retryable_on_startup(tmp_path, monkeypatch):
    db, analyzer, main = load(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        db.update_chat(cid, status="analyzing", analyzed_upto=1)
    db, analyzer, main = load(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        chat = c.get(f"/api/chats/{cid}/board").json()["chat"]
        assert chat["status"] == "error" and "yarıda" in chat["error"]
        assert chat["analyzed_upto"] == 1  # retry resumes after message 1


def test_analyze_endpoint_runs_in_background_and_persists(tmp_path, monkeypatch):
    import time
    db, analyzer, main = load(tmp_path, monkeypatch)

    async def fake(*a, **k):
        await asyncio.sleep(0.2)  # long enough to observe the running state
        return RESULT
    monkeypatch.setattr(analyzer.llm, "chat_json", fake)

    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        r = c.post(f"/api/chats/{cid}/analyze")
        assert r.status_code == 200 and r.json()["state"] in ("queued", "running")
        assert c.post(f"/api/chats/{cid}/analyze").json()["state"] in ("queued", "running")  # no second run

        deadline = time.time() + 10
        while c.get(f"/api/chats/{cid}/progress").json()["state"] != "done":
            assert time.time() < deadline, "analysis did not finish"
            time.sleep(0.05)

        b = c.get(f"/api/chats/{cid}/board").json()
        assert b["chat"]["status"] == "ready" and b["tasks"] == []
        assert len(b["review"]) == 3 and {i["review"] for i in b["review"]} == {"proposed"}
        task = next(i for i in b["review"] if i["kind"] == "task")
        assert c.patch(f"/api/items/{task['id']}", json={"review": "approved"}).status_code == 200

    db, analyzer, main = load(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        b = c.get(f"/api/chats/{cid}/board").json()
        assert [t["title"] for t in b["tasks"]] == ["Afiş hazırla"] and len(b["review"]) == 2
