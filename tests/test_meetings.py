import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe Demir: Afişi ben yaparım\n17.10.2026 19:34 - Mert Kaya: tamam\n"


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "m.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import meetings, main
    importlib.reload(meetings)
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik,Teknik", content=CHAT.encode()).json()["id"]
    return c, cid


def test_create_update_list_delete(env):
    c, cid = env
    m = c.post(f"/api/chats/{cid}/meetings", json={
        "title": "Yönetim toplantısı", "date": "2026-10-20", "time": "19:00", "units": ["Etkinlik"],
        "attendees": "Ayşe Demir, Mert Kaya", "agenda": "Söyleşi", "notes": "Salon ayarlandı.\r\nAfiş bekleniyor."}).json()
    assert m["status"] == "planned" and m["units"] == ["Etkinlik"] and "\r" not in m["notes"]
    r = c.patch(f"/api/meetings/{m['id']}", json={"status": "held", "date": ""}).json()
    assert r["status"] == "held" and r["date"] is None  # blank date = unknown, never invented
    cards = c.get(f"/api/chats/{cid}/meetings").json()
    assert len(cards) == 1 and cards[0]["has_notes"] and "notes" not in cards[0]
    assert c.get(f"/api/meetings/{m['id']}").json()["lines"] == 2
    assert c.delete(f"/api/meetings/{m['id']}").json() == {"ok": True}
    assert c.get(f"/api/chats/{cid}/meetings").json() == []


@pytest.mark.parametrize("body", [
    {"title": ""}, {"title": "x", "date": "31.10.2026"}, {"title": "x", "date": "2026-02-31"},
    {"title": "x", "time": "25:00"}, {"title": "x", "status": "done"}, {"title": "x", "units": ["Yok"]},
    {"title": "x", "notes": "a\x00b"}])
def test_invalid_input_rejected(env, body):
    c, cid = env
    assert c.post(f"/api/chats/{cid}/meetings", json=body).status_code == 400


def test_notes_too_long_rejected(env):
    c, cid = env
    assert c.post(f"/api/chats/{cid}/meetings", json={"title": "x", "notes": "a" * 100_001}).status_code == 413


def test_notes_file_validation(env):
    c, cid = env
    url = f"/api/chats/{cid}/meetings/notes-file"
    ok = c.post(url + "?filename=n.md", content="# Notlar\r\nSalon tamam ✓".encode("utf-8-sig"))
    assert ok.status_code == 200 and ok.json()["text"] == "# Notlar\nSalon tamam ✓"
    assert c.post(url + "?filename=n.txt", content="Çalışma".encode("utf-16")).json()["text"] == "Çalışma"
    assert c.post(url + "?filename=n.pdf", content=b"x").status_code == 400          # extension
    assert c.post(url + "?filename=n.txt", content=b"").status_code == 400           # empty
    assert c.post(url + "?filename=n.txt", content="ç".encode("cp1254")).status_code == 400   # not UTF-8
    assert c.post(url + "?filename=n.txt", content=b"ab\x00cd").status_code == 400   # binary
    assert c.post(url + "?filename=n.txt", content=b"a" * 100_001).status_code == 400  # too big
    assert c.get(f"/api/chats/{cid}/meetings").json() == []                          # nothing saved


def test_committee_rename_and_delete_follow_into_meetings(env):
    c, cid = env
    m = c.post(f"/api/chats/{cid}/meetings", json={"title": "t", "units": ["Etkinlik", "Teknik"]}).json()
    c.patch(f"/api/chats/{cid}", json={"renames": {"Etkinlik": "Organizasyon"}})
    assert c.get(f"/api/meetings/{m['id']}").json()["meeting"]["units"] == ["Organizasyon", "Teknik"]
    c.patch(f"/api/chats/{cid}", json={"units": ["Organizasyon"]})
    assert c.get(f"/api/meetings/{m['id']}").json()["meeting"]["units"] == ["Organizasyon"]


def _link(cid, mid, title, **kw):
    from app import db
    return db.add_item(cid, "task", title=title, meeting_id=mid, **kw)


def test_owner_outside_committee_list_warns_but_does_not_block(env):
    c, cid = env
    c.patch(f"/api/chats/{cid}", json={"unit_members": {"Etkinlik": "Ayşe Demir, Mert Kaya"}})
    m2 = c.post(f"/api/chats/{cid}/meetings", json={"title": "T", "units": ["Etkinlik"]}).json()["id"]
    _link(cid, m2, "Salon", owner="Ayşe Demir")
    _link(cid, m2, "Afiş", owner="Mert")             # first name of a listed member: fine
    _link(cid, m2, "Sponsor", owner="Can Yıldız")    # not on the list
    _link(cid, m2, "Bütçe")                          # no owner: counted, not a warning
    d = c.get(f"/api/meetings/{m2}").json()
    assert [w["owner"] for w in d["warnings"]] == ["Can Yıldız"] and d["orphan_tasks"] == 1
    assert c.get(f"/api/chats/{cid}/meetings").json()[0]["orphan_tasks"] == 1


def test_no_warning_without_committee_or_member_list(env):
    c, cid = env
    no_units = c.post(f"/api/chats/{cid}/meetings", json={"title": "A"}).json()["id"]
    no_list = c.post(f"/api/chats/{cid}/meetings", json={"title": "B", "units": ["Etkinlik"]}).json()["id"]
    for m in (no_units, no_list):
        _link(cid, m, "İş", owner="Kim Bilir")
        assert c.get(f"/api/meetings/{m}").json()["warnings"] == []


def test_dashboard_cards_upcoming_and_held_with_orphans(env, monkeypatch):
    c, cid = env
    monkeypatch.setenv("PANO_TODAY", "2026-10-18")
    c.post(f"/api/chats/{cid}/meetings", json={"title": "Yakın", "date": "2026-10-21", "time": "19:00", "status": "planned"}).json()["id"]
    c.post(f"/api/chats/{cid}/meetings", json={"title": "Geçmiş planlı", "date": "2026-10-01", "status": "planned"})
    c.post(f"/api/chats/{cid}/meetings", json={"title": "Tarihsiz", "status": "planned"})
    c.post(f"/api/chats/{cid}/meetings", json={"title": "İptal", "date": "2026-10-25", "status": "cancelled"})
    held = c.post(f"/api/chats/{cid}/meetings", json={"title": "Yapıldı", "date": "2026-10-10", "status": "held"}).json()["id"]
    clean = c.post(f"/api/chats/{cid}/meetings", json={"title": "Temiz", "date": "2026-10-11", "status": "held"}).json()["id"]
    _link(cid, held, "Sahipsiz 1"); _link(cid, held, "Sahipsiz 2"); _link(cid, held, "Sahipli", owner="Ayşe")
    _link(cid, held, "Biten sahipsiz", status="done"); _link(cid, clean, "Sahipli", owner="Mert")
    cards = c.get(f"/api/chats/{cid}/board").json()["meetings"]
    assert [m["title"] for m in cards["upcoming"]] == ["Yakın"] and cards["upcoming"][0]["days"] == 3
    assert cards["held_orphans"] == [{"id": held, "title": "Yapıldı", "date": "2026-10-10", "orphans": 2}]
