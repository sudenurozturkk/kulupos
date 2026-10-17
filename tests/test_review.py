import asyncio
import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = ("17.10.2026 19:33 - Ayşe: Afişi ben yaparım\n"
        "17.10.2026 19:34 - Mert: Salon dilekçesini kim verir?\n")


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "t.db"))
    from app import db
    importlib.reload(db)
    from app import analyzer, main
    importlib.reload(analyzer)
    importlib.reload(main)
    return db, analyzer, TestClient(main.app)


def fake(monkeypatch, analyzer):
    async def chat_json(*a, **k):
        return {"new_tasks": [{"title": "Afiş hazırla", "owner": "Ayşe", "due": "", "unit": "", "source": 0}],
                "new_questions": [{"text": "Salon dilekçesini kim verir?", "asked_by": "Mert", "source": 1}]}
    monkeypatch.setattr(analyzer.llm, "chat_json", chat_json)


def run(analyzer, chat_id):
    asyncio.run(analyzer.analyze(chat_id))


def test_ai_items_wait_for_approval(env, monkeypatch):
    db, analyzer, client = env
    fake(monkeypatch, analyzer)
    chat = client.post("/api/chats", content=CHAT.encode()).json()
    run(analyzer, chat["id"])
    b = client.get(f"/api/chats/{chat['id']}/board").json()
    assert b["tasks"] == [] and b["questions"] == []
    assert {i["title"] for i in b["review"]} == {"Afiş hazırla", "Salon dilekçesini kim verir?"}

    task = next(i for i in b["review"] if i["kind"] == "task")
    client.patch(f"/api/items/{task['id']}", json={"review": "approved"})
    b = client.get(f"/api/chats/{chat['id']}/board").json()
    assert [t["title"] for t in b["tasks"]] == ["Afiş hazırla"]
    assert len(b["review"]) == 1


def test_rejected_does_not_return_and_manual_is_approved(env, monkeypatch):
    db, analyzer, client = env
    fake(monkeypatch, analyzer)
    chat = client.post("/api/chats", content=CHAT.encode()).json()
    cid = chat["id"]
    run(analyzer, cid)
    for i in client.get(f"/api/chats/{cid}/board").json()["review"]:
        client.patch(f"/api/items/{i['id']}", json={"review": "rejected"})
    db.update_chat(cid, analyzed_upto=-1)  # force a re-run over the same messages
    run(analyzer, cid)
    b = client.get(f"/api/chats/{cid}/board").json()
    assert b["review"] == [] and b["tasks"] == []

    client.post(f"/api/chats/{cid}/items", json={"kind": "task", "title": "Elle eklendi"})
    assert [t["title"] for t in client.get(f"/api/chats/{cid}/board").json()["tasks"]] == ["Elle eklendi"]
