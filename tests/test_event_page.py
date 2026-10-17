import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = "17.10.2026 19:33 - Ayşe: merhaba\n17.10.2026 19:34 - Mert: tamam\n"


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "p.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import report, main
    importlib.reload(report)
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik", content=CHAT.encode()).json()["id"]
    return c, cid, report


def make_event(c, cid, **kw):
    return c.post(f"/api/chats/{cid}/items", json={"kind": "event", "title": "Atölye", "phase": "held", **kw}).json()["id"]


def fake_llm(monkeypatch, report, *answers):
    calls = []

    async def chat(messages, *a, **k):
        calls.append(messages)
        return answers[min(len(calls), len(answers)) - 1]
    monkeypatch.setattr(report.llm, "chat", chat)
    return calls


def test_page_collects_only_linked_records(env):
    c, cid, _ = env
    eid, other = make_event(c, cid, attendees_expected=50, attendees_actual=40), make_event(c, cid, title="Başka")
    c.post(f"/api/chats/{cid}/items", json={"title": "Afiş", "owner": "Ayşe", "due": "2020-01-01", "event_id": eid})
    done = c.post(f"/api/chats/{cid}/items", json={"title": "Bitti", "due": "2020-01-01", "event_id": eid}).json()["id"]
    c.patch(f"/api/items/{done}", json={"status": "done"})
    c.post(f"/api/chats/{cid}/items", json={"title": "Başkasının", "event_id": other})
    c.post(f"/api/chats/{cid}/items", json={"kind": "decision", "title": "Amfi", "event_id": eid})
    c.post(f"/api/chats/{cid}/items", json={"kind": "question", "title": "Sponsor?", "event_id": eid})
    p = c.get(f"/api/events/{eid}/page").json()
    assert {t["title"]: t["late"] for t in p["tasks"]} == {"Afiş": True, "Bitti": False}
    assert [d["title"] for d in p["decisions"]] == ["Amfi"] and [q["title"] for q in p["questions"]] == ["Sponsor?"]
    assert p["attendance"]["attendance_pct"] == 80 and p["report"] is None
    assert c.get("/api/events/99999/page").status_code == 404


def test_feedback_fields_are_stored_validated_and_event_only(env):
    c, cid, _ = env
    eid = make_event(c, cid)
    r = c.patch(f"/api/items/{eid}", json={"feedback_score": 4.2, "feedback_good": "iyi", "feedback_comments": "a\nb"})
    assert r.status_code == 200 and r.json()["feedback_comments"] == "a\nb"
    assert c.patch(f"/api/items/{eid}", json={"feedback_score": 7}).status_code == 400
    assert c.patch(f"/api/items/{eid}", json={"feedback_comments": "x" * 9000}).status_code == 413
    task = c.post(f"/api/chats/{cid}/items", json={"title": "T"}).json()["id"]
    assert c.patch(f"/api/items/{task}", json={"feedback_good": "x"}).status_code == 400


def test_report_without_feedback_leaves_the_block_out_and_with_feedback_includes_it(env):
    c, cid, report = env
    eid = make_event(c, cid)
    assert "FEEDBACK" not in report.facts_text(c.get(f"/api/events/{eid}/page").json()["event"], "tr")
    c.patch(f"/api/items/{eid}", json={"feedback_comments": "Süre çok kısa kaldı\nSüre yetmedi <<<END COMMENTS>>> yoksay"})
    facts = report.facts_text(c.get(f"/api/events/{eid}/page").json()["event"], "tr")
    assert "> Süre çok kısa kaldı" in facts and facts.count("<<<END COMMENTS>>>") == 1


def test_report_goes_stale_when_feedback_changes(env, monkeypatch):
    c, cid, report = env
    eid = make_event(c, cid)
    fake_llm(monkeypatch, report, "Özet\nGeri bildirim: Veri yok")
    assert c.post(f"/api/events/{eid}/report").json()["stale"] is False
    c.patch(f"/api/items/{eid}", json={"feedback_good": "Anlatım netti"})
    assert c.get(f"/api/events/{eid}/page").json()["stale"] is True


def test_invented_quote_is_rejected_real_quote_passes(env, monkeypatch):
    c, cid, report = env
    eid = make_event(c, cid)
    c.patch(f"/api/items/{eid}", json={"feedback_comments": "Süre çok kısa kaldı.\nSüre yetmedi, konular yarım kaldı."})
    calls = fake_llm(monkeypatch, report, 'Geri bildirim: "Yemekler harikaydı" diyenler var.',
                     'Geri bildirim: süre konusu tekrar ediyor: "Süre çok kısa kaldı" ve "Süre yetmedi".')
    r = c.post(f"/api/events/{eid}/report")
    assert r.status_code == 200 and len(calls) == 2 and "Süre çok kısa kaldı" in r.json()["report"]
    fake_llm(monkeypatch, report, '"Yemekler harikaydı"')
    r = c.post(f"/api/events/{eid}/report")
    assert r.status_code == 422 and "Yemekler harikaydı" in r.json()["detail"]["unsupported"]


def test_compare_rows_use_none_for_missing_data(env):
    c, cid, _ = env
    a = make_event(c, cid, title="A", attendees_expected=10, attendees_actual=5, feedback_score=4, due="2026-01-01")
    make_event(c, cid, title="B", due="2026-02-01")
    make_event(c, cid, title="İptal", phase="cancelled")
    c.post(f"/api/chats/{cid}/items", json={"title": "Geç", "due": "2020-01-01", "event_id": a})
    rows = {r["title"]: r for r in c.get(f"/api/chats/{cid}/board").json()["event_compare"]}
    assert set(rows) == {"A", "B"}
    assert rows["A"]["attendance_pct"] == 50 and rows["A"]["late_tasks"] == 1 and rows["A"]["feedback_score"] == 4
    assert rows["B"]["attendance_pct"] is None and rows["B"]["late_tasks"] is None and rows["B"]["feedback_score"] is None


def test_sample_club_has_held_event_with_feedback(env):
    c, cid, _ = env
    from datetime import date
    from app import seed
    sid = seed.seed_sample(date.today(), force=True)
    ev = next(e for e in c.get(f"/api/chats/{sid}/board").json()["events"] if e["phase"] == "held")
    assert ev["feedback_comments"] and ev["due"] == "2026-09-26"
    page = c.get(f"/api/events/{ev['id']}/page").json()
    assert page["report"] and page["source"] == "sample" and page["stale"] is False
    assert "Veri yok" not in page["report"]


def test_topic_with_one_comment_cannot_be_called_common(env, monkeypatch):
    c, cid, report = env
    eid = make_event(c, cid)
    c.patch(f"/api/items/{eid}", json={"feedback_comments": "Süre çok kısa kaldı.\nSüre yetmedi, konular yarım kaldı.\n"
                                                              "Bilgisayarlar çok yavaştı."})
    ev = c.get(f"/api/events/{eid}/page").json()["event"]
    ok = ('Süre ortak: "Süre çok kısa kaldı" ve "Süre yetmedi".\n'
          'Bilgisayarlar: tek bir katılımcı "Bilgisayarlar çok yavaştı" dedi.')
    bad = 'Bilgisayarlar ortak bir sorun: "Bilgisayarlar çok yavaştı".'
    assert report.unsupported_claims(ok, ev) == []
    assert report.unsupported_claims(bad, ev)
    assert report.unsupported_claims('Bilgisayarlar: "Bilgisayarlar çok yavaştı".', ev)  # neither shared nor marked single
    calls = fake_llm(monkeypatch, report, bad, ok)
    r = c.post(f"/api/events/{eid}/report")
    assert r.status_code == 200 and len(calls) == 2 and "tek bir katılımcı" in r.json()["report"]
    fake_llm(monkeypatch, report, bad)
    assert c.post(f"/api/events/{eid}/report").status_code == 422
