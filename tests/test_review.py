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


def test_unsourced_item_flagged_and_not_approvable(env, monkeypatch):
    db, analyzer, client = env

    async def chat_json(*a, **k):
        return {"new_tasks": [{"title": "Kaynaksız iş", "owner": "", "due": "", "unit": "", "source": 99},
                              {"title": "Tarihi bozuk iş", "owner": "", "due": "2099-13-45", "unit": "", "source": 0}]}
    monkeypatch.setattr(analyzer.llm, "chat_json", chat_json)
    cid = client.post("/api/chats", content=CHAT.encode()).json()["id"]
    run(analyzer, cid)
    rev = {i["title"]: i for i in client.get(f"/api/chats/{cid}/board").json()["review"]}
    assert rev["Kaynaksız iş"]["needs_review"] == 1
    assert rev["Tarihi bozuk iş"]["needs_review"] == 2

    r = client.patch(f"/api/items/{rev['Kaynaksız iş']['id']}", json={"review": "approved"})
    assert r.status_code == 409
    client.patch(f"/api/items/{rev['Kaynaksız iş']['id']}", json={"title": "Düzeltildi"})
    assert client.patch(f"/api/items/{rev['Kaynaksız iş']['id']}", json={"review": "approved"}).status_code == 409
    assert client.patch(f"/api/items/{rev['Kaynaksız iş']['id']}", json={"review": "rejected"}).status_code == 200

    tid = rev["Tarihi bozuk iş"]["id"]
    assert client.patch(f"/api/items/{tid}", json={"review": "approved"}).status_code == 409
    client.patch(f"/api/items/{tid}", json={"due": "2026-10-20"})
    assert client.patch(f"/api/items/{tid}", json={"review": "approved"}).status_code == 200


def test_ai_update_to_approved_item_becomes_a_proposal(env, monkeypatch):
    db, analyzer, client = env
    fake(monkeypatch, analyzer)
    cid = client.post("/api/chats", content=CHAT.encode()).json()["id"]
    run(analyzer, cid)
    task = next(i for i in client.get(f"/api/chats/{cid}/board").json()["review"] if i["kind"] == "task")
    client.patch(f"/api/items/{task['id']}", json={"review": "approved"})

    async def chat_json(*a, **k):
        return {"task_updates": [{"id": task["id"], "status": "done", "owner": "Mert", "due": "", "source": 1}]}
    monkeypatch.setattr(analyzer.llm, "chat_json", chat_json)

    def rerun():
        db.update_chat(cid, analyzed_upto=-1)
        run(analyzer, cid)

    rerun()
    b = client.get(f"/api/chats/{cid}/board").json()
    t = next(x for x in b["tasks"] if x["id"] == task["id"])
    assert t["status"] == "open" and t["owner"] == "Ayşe"          # approved record untouched
    assert len(b["changes"]) == 1 and b["changes"][0]["new"]["status"] == "done"
    assert b["changes"][0]["old"]["owner"] == "Ayşe"

    rerun()                                                          # same proposal is not repeated
    assert len(client.get(f"/api/chats/{cid}/board").json()["changes"]) == 1

    chg = b["changes"][0]
    assert client.patch(f"/api/changes/{chg['id']}", json={"review": "approved"}).status_code == 200
    b = client.get(f"/api/chats/{cid}/board").json()
    t = next(x for x in b["tasks"] if x["id"] == task["id"])
    assert t["status"] == "done" and t["owner"] == "Mert" and b["changes"] == []


def test_rejected_change_leaves_item_and_does_not_return(env, monkeypatch):
    db, analyzer, client = env
    fake(monkeypatch, analyzer)
    cid = client.post("/api/chats", content=CHAT.encode()).json()["id"]
    run(analyzer, cid)
    q = next(i for i in client.get(f"/api/chats/{cid}/board").json()["review"] if i["kind"] == "question")
    client.patch(f"/api/items/{q['id']}", json={"review": "approved"})

    async def chat_json(*a, **k):
        return {"answered_questions": [{"id": q["id"], "source": 1}]}
    monkeypatch.setattr(analyzer.llm, "chat_json", chat_json)
    for _ in range(2):
        db.update_chat(cid, analyzed_upto=-1)
        run(analyzer, cid)
        b = client.get(f"/api/chats/{cid}/board").json()
        if b["changes"]:
            client.patch(f"/api/changes/{b['changes'][0]['id']}", json={"review": "rejected"})
    b = client.get(f"/api/chats/{cid}/board").json()
    assert b["changes"] == [] and b["questions"][0]["status"] == "open"
