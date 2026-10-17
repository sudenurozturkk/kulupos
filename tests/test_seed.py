import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "s.db"))
    monkeypatch.setenv("PANO_TODAY", "2026-10-17")
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import seed, main
    importlib.reload(seed)
    importlib.reload(main)
    return TestClient(main.app)


def board(c, cid):
    return c.get(f"/api/chats/{cid}/board").json()


def test_empty_database_gets_a_labelled_sample_panel(client):
    r = client.post("/api/seed").json()
    assert r["created"] is True
    b = board(client, r["chat_id"])
    assert b["chat"]["is_sample"] == 1 and b["chat"]["status"] == "ready"
    assert b["chat"]["units"] == ["Yönetim", "Etkinlik", "İletişim", "Sponsorluk"]
    assert len(b["tasks"]) == 14 and len(b["decisions"]) == 6 and len(b["events"]) == 3  # incl. 3 + 2 from the held sample meeting
    assert sum(1 for q in b["questions"] if q["status"] == "open") == 4
    # every approved card points at a real source message; the unsourced proposal is flagged
    assert all(i["source_idx"] is not None for i in [*b["tasks"], *b["questions"], *b["decisions"], *b["events"]]
               if "(örnek veri)" not in i["title"] and not i["meeting_id"])  # the held sample event is hand-entered data, not from the chat
    assert len(b["review"]) == 4 and sum(1 for i in b["review"] if i["needs_review"] == 1) == 1
    # AI proposals are counted apart from real tasks
    assert b["review_total"] == 4 and all(i["review"] == "approved" for i in b["tasks"])
    chats = client.get("/api/chats").json()
    assert chats[0]["is_sample"] == 1 and chats[0]["review_count"] == 4 and chats[0]["source_name"].endswith(".txt")


def test_panel_focus_lists(client):
    cid = client.post("/api/seed").json()["chat_id"]
    o = board(client, cid)["overview"]
    f = o["focus"]
    assert {x["title"] for x in f["overdue"]} == {"Kahveciye teslimat saatini bildir", "Geçen yılın sponsor dosyasını bul"}
    assert {x["title"] for x in f["orphans"]} == {"Projeksiyon ve ses sistemi için Teknik İşler'e dilekçe yaz",
                                                 "Geçen yılın sponsor dosyasını bul",
                                                 "Basın bülteni taslağını yaz"}  # overlap with overdue is intended; the last one comes from the held meeting
    assert [c["why"] for c in f["conflicts"]] == ["after_event"]
    assert len(f["decisions"]) == 3  # three decisions not yet marked final (one from the held meeting)
    k = o["kpi"]
    assert k["open"] == 10 and k["done"] == 4 and k["questions"] == 4
    assert len(k["upcoming_ids"]) == 1  # only "Sertifikaları hazırla" (+7) falls in the next 7 days
    assert [e["title"] for e in o["events"]] == ["Online hazırlık toplantısı", "Yapay Zeka ile Kariyer Söyleşisi"]
    assert o["events"][0]["days"] == 6


def test_decision_can_be_marked_final(client):
    cid = client.post("/api/seed").json()["chat_id"]
    d = board(client, cid)["overview"]["focus"]["decisions"][0]
    client.patch(f"/api/items/{d['id']}", json={"status": "done"})
    assert len(board(client, cid)["overview"]["focus"]["decisions"]) == 2


def test_seed_only_on_an_empty_database(client):
    client.post("/api/chats", content=b"17.10.2026 19:33 - Ayse: selam\n")
    assert client.post("/api/seed").json() == {"created": False, "chat_id": None}


def test_clear_sample_removes_everything_and_stays_gone(client):
    cid = client.post("/api/seed").json()["chat_id"]
    own = client.post("/api/chats", content=b"17.10.2026 19:33 - Ayse: selam\n").json()["id"]
    assert client.delete("/api/sample").json() == {"removed": 1}
    assert [c["id"] for c in client.get("/api/chats").json()] == [own]
    assert client.get(f"/api/chats/{cid}/board").status_code == 404
    client.delete(f"/api/chats/{own}")
    assert client.post("/api/seed").json()["created"] is False  # cleared once: not brought back


def test_no_data_is_not_reported_as_zero(client):
    cid = client.post("/api/chats", content=b"17.10.2026 19:33 - Ayse: selam\n").json()["id"]
    k = board(client, cid)["overview"]["kpi"]
    # the UI shows "-" when these totals are 0 instead of a real-looking zero
    assert k["total"] == 0 and k["dated"] == 0 and k["questions_total"] == 0


# ---- "Demo kulübü aç" button: instant, no model, guarded ----------------------

def test_demo_button_opens_sample_instantly_without_the_model(client, monkeypatch):
    import time
    from app import llm

    async def boom(*a, **k):
        raise AssertionError("the demo must not call the model")
    monkeypatch.setattr(llm, "chat", boom)
    monkeypatch.setattr(llm, "chat_json", boom)
    own = client.post("/api/chats", content=b"17.10.2026 19:33 - Ayse: selam\n").json()["id"]  # not an empty database
    t0 = time.perf_counter()
    r = client.post("/api/demo/tr").json()
    assert time.perf_counter() - t0 < 5
    assert r["status"] == "ready" and r["is_sample"] == 1 and r["id"] != own
    assert client.post("/api/demo/tr").json()["id"] == r["id"]  # second click reuses it
    assert len(client.get("/api/chats").json()) == 2
    client.delete("/api/sample")  # cleared, then clicked again on purpose: it comes back
    assert client.post("/api/demo/tr").json()["is_sample"] == 1


def test_demo_button_times_out_with_a_message_instead_of_hanging(client, monkeypatch):
    import time
    from app import main, seed
    monkeypatch.setattr(main, "SEED_TIMEOUT", 0.2)
    monkeypatch.setattr(seed, "ensure_sample", lambda today: time.sleep(1))
    r = client.post("/api/demo/tr")
    assert r.status_code == 504 and "saniyede" in r.json()["detail"]


def test_demo_button_database_error_is_a_readable_message(client, monkeypatch):
    import sqlite3
    from app import seed

    def locked(today):
        raise sqlite3.OperationalError("database is locked")
    monkeypatch.setattr(seed, "ensure_sample", locked)
    r = client.post("/api/demo/tr")
    assert r.status_code == 503 and "OperationalError" in r.json()["detail"]


def test_sample_has_two_meetings_held_and_planned(client):
    cid = client.post("/api/seed").json()["chat_id"]
    ms = client.get(f"/api/chats/{cid}/meetings").json()
    held = next(m for m in ms if m["status"] == "held")
    planned = next(m for m in ms if m["status"] == "planned")
    assert held["has_notes"] and (held["tasks"], held["decisions"], held["questions"], held["orphan_tasks"]) == (3, 2, 1, 1)
    assert planned["date"] == "2026-10-21" and not planned["has_notes"]   # PANO_TODAY + 4 days
    d = client.get(f"/api/meetings/{held['id']}").json()
    assert d["proposed"] == 1 and d["analyzed"] and not d["notes_changed"]
    assert [w["owner"] for w in d["warnings"]] == ["Burak Yıldız"]   # sample shows the informational check
    cards = board(client, cid)["meetings"]
    assert [m["title"] for m in cards["upcoming"]] == ["Haftalık yönetim toplantısı"]
    assert [m["id"] for m in cards["held_orphans"]] == [held["id"]]
    # the sample suggestion waits in the review queue with its note quote; nothing about it is invented
    rev = next(i for i in board(client, cid)["review"] if i["meeting_id"] == held["id"])
    assert rev["source"]["sender"] is None and rev["source"]["ts"] is None and "e-sertifika" in rev["source"]["text"]
    assert client.delete("/api/sample").json() == {"removed": 1}
    assert client.get(f"/api/meetings/{held['id']}").status_code == 404   # sample meetings go with the sample
