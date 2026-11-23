"""Search, calendar export and comments."""
import importlib
import re

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "t.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import analyzer, main
    importlib.reload(analyzer)
    importlib.reload(main)
    client = TestClient(main.app)
    chat = client.post("/api/chats", content=b"17.10.2026 19:33 - Ay\xc5\x9fe: Merhaba\n").json()
    return db, client, chat["id"]


def add(client, chat_id, kind, title):
    return client.post(f"/api/chats/{chat_id}/items", json={"kind": kind, "title": title}).json()["id"]


def test_search_finds_items_meetings_messages_turkish_case_insensitive(env):
    db, client, cid = env
    t = client.post(f"/api/chats/{cid}/items", json={"kind": "task", "title": "İmza kâğıdı hazırla", "owner": "Ayşe"}).json()["id"]
    client.post(f"/api/chats/{cid}/meetings", json={"title": "Sponsor görüşmesi", "date": "2026-11-02", "agenda": "bütçe"})
    r = client.get(f"/api/chats/{cid}/search", params={"q": "imza"}).json()
    assert [i["id"] for i in r["items"]] == [t] and r["total"] == 1
    r = client.get(f"/api/chats/{cid}/search", params={"q": "SPONSOR"}).json()
    assert len(r["meetings"]) == 1
    r = client.get(f"/api/chats/{cid}/search", params={"q": "merhaba"}).json()
    assert len(r["messages"]) == 1 and r["messages"][0]["sender"] == "Ayşe"


def test_search_short_or_empty_query_returns_nothing_and_long_is_rejected(env):
    db, client, cid = env
    assert client.get(f"/api/chats/{cid}/search", params={"q": "a"}).json()["total"] == 0
    assert client.get(f"/api/chats/{cid}/search").json()["total"] == 0
    assert client.get(f"/api/chats/{cid}/search", params={"q": "x" * 101}).status_code == 400
    assert client.get("/api/chats/999/search", params={"q": "ab"}).status_code == 404


def test_search_ignores_unapproved_proposals(env):
    db, client, cid = env
    db.add_item(cid, "task", title="Gizli öneri", review="proposed")
    assert client.get(f"/api/chats/{cid}/search", params={"q": "gizli"}).json()["total"] == 0


def test_calendar_has_events_meetings_open_tasks_only(env):
    db, client, cid = env
    client.post(f"/api/chats/{cid}/items", json={"kind": "event", "title": "Hackathon, Final", "due": "2026-11-20", "time": "14:30", "place": "Salon;A"})
    client.post(f"/api/chats/{cid}/items", json={"kind": "task", "title": "Afiş", "due": "2026-11-10"})
    done = client.post(f"/api/chats/{cid}/items", json={"kind": "task", "title": "Bitti", "due": "2026-11-11"}).json()["id"]
    client.patch(f"/api/items/{done}", json={"status": "done"})
    client.post(f"/api/chats/{cid}/items", json={"kind": "task", "title": "Tarihsiz"})
    client.post(f"/api/chats/{cid}/meetings", json={"title": "Yönetim", "date": "2026-11-05", "time": "18:00"})
    client.post(f"/api/chats/{cid}/meetings", json={"title": "İptal", "date": "2026-11-06", "status": "cancelled"})
    r = client.get(f"/api/chats/{cid}/calendar.ics")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/calendar")
    ics = r.text
    assert ics.startswith("BEGIN:VCALENDAR\r\n") and ics.endswith("END:VCALENDAR\r\n")
    assert ics.count("BEGIN:VEVENT") == 3
    assert "SUMMARY:Hackathon\\, Final" in ics and "LOCATION:Salon\\;A" in ics
    assert "DTSTART:20261120T143000" in ics and "DTSTART;VALUE=DATE:20261110" in ics
    assert "Bitti" not in ics and "Tarihsiz" not in ics and "İptal" not in ics
    assert all(len(line.encode()) <= 75 for line in ics.split("\r\n"))
    no_tasks = client.get(f"/api/chats/{cid}/calendar.ics", params={"tasks": "false"}).text
    assert no_tasks.count("BEGIN:VEVENT") == 2


def test_calendar_long_line_folding_keeps_utf8_intact(env):
    db, client, cid = env
    client.post(f"/api/chats/{cid}/items", json={"kind": "event", "title": "�?" * 120, "due": "2026-11-20"})
    ics = client.get(f"/api/chats/{cid}/calendar.ics").text
    assert all(len(line.encode()) <= 75 for line in ics.split("\r\n"))
    unfolded = re.sub(r"\r\n ", "", ics)
    assert "SUMMARY:" + "�?" * 120 in unfolded


def test_comments_are_logged_in_history_and_validated(env):
    db, client, cid = env
    t = add(client, cid, "task", "Afiş")
    r = client.post(f"/api/items/{t}/comments", json={"text": "  Baskıya gitti  "})
    assert r.status_code == 200
    h = client.get(f"/api/items/{t}/history").json()
    assert [(x["field"], x["note"]) for x in h] == [("comment", "Baskıya gitti")]
    assert client.post(f"/api/items/{t}/comments", json={"text": "   "}).status_code == 400
    assert client.post(f"/api/items/{t}/comments", json={"text": "x" * 501}).status_code == 400
    assert client.post("/api/items/9999/comments", json={"text": "a"}).status_code == 404
