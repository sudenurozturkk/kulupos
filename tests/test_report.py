import importlib

import pytest
from fastapi.testclient import TestClient

CHAT = ("17.10.2026 19:33 - Ayşe: gizli sohbet cümlesi 777\n"
        "17.10.2026 19:34 - Mert: tamam\n")


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "r.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import report, main
    importlib.reload(report)
    importlib.reload(main)
    c = TestClient(main.app)
    cid = c.post("/api/chats?units=Etkinlik", content=CHAT.encode()).json()["id"]
    ev = c.post(f"/api/chats/{cid}/items", json={
        "kind": "event", "title": "Söyleşi", "due": "2026-10-31", "time": "14:00", "phase": "held",
        "attendees_expected": 120, "attendees_actual": 95}).json()
    c.post(f"/api/chats/{cid}/items", json={"title": "Afiş", "owner": "Ayşe", "event_id": ev["id"]})
    c.post(f"/api/chats/{cid}/items", json={"kind": "decision", "title": "Amfi 2 kullanılacak", "event_id": ev["id"]})
    return c, cid, ev["id"], report


def fake_llm(monkeypatch, report, *answers):
    calls = []

    async def chat(messages, *a, **k):
        calls.append(messages)
        return answers[min(len(calls), len(answers)) - 1]
    monkeypatch.setattr(report.llm, "chat", chat)
    return calls


def test_prompt_has_only_recorded_data_and_omits_empty_fields(env, monkeypatch):
    c, cid, eid, report = env
    calls = fake_llm(monkeypatch, report, "Özet: 95 kişi katıldı.")
    assert c.post(f"/api/events/{eid}/report").status_code == 200
    prompt = "\n".join(m["content"] for m in calls[0])
    assert "Girilmedi" not in prompt and "Venue" not in prompt and "Actual budget" not in prompt and "Notes:" not in prompt
    assert "FEEDBACK (" not in prompt and "<<<COMMENTS>>>" not in prompt  # a block with no data is left out entirely
    assert "Expected attendees: 120" in prompt and "Actual attendees: 95" in prompt
    assert "Afiş" in prompt and "Amfi 2 kullanılacak" in prompt
    assert "gizli sohbet" not in prompt and "777" not in prompt  # chat text never reaches the report prompt


def test_invented_figure_is_rejected_and_nothing_saved(env, monkeypatch):
    c, cid, eid, report = env
    calls = fake_llm(monkeypatch, report, "95 kişi geldi, bütçe 4300 TL idi.")  # 4300 is made up, twice
    r = c.post(f"/api/events/{eid}/report")
    assert r.status_code == 422 and r.json()["detail"]["unsupported"] == ["4300"]
    assert len(calls) == 2  # one retry that names the offending figure
    assert "4300" in calls[1][-1]["content"]
    assert c.get(f"/api/events/{eid}/report").json() == {"report": None}


def test_retry_can_fix_the_report(env, monkeypatch):
    c, cid, eid, report = env
    fake_llm(monkeypatch, report, "Bütçe 4300 TL.", "Katılım: 95 kişi, 120 kişi beklenmişti (31 Ekim).")
    r = c.post(f"/api/events/{eid}/report")
    assert r.status_code == 200 and "4300" not in r.json()["report"] and r.json()["stale"] is False


def test_list_numbering_is_not_a_figure(env, monkeypatch):
    c, cid, eid, report = env
    fake_llm(monkeypatch, report, "1. Görevler: 1 görev\n2. Kararlar: 1 karar")
    assert c.post(f"/api/events/{eid}/report").status_code == 200


def test_report_goes_stale_when_data_changes(env, monkeypatch):
    c, cid, eid, report = env
    fake_llm(monkeypatch, report, "95 kişi geldi.")
    c.post(f"/api/events/{eid}/report")
    assert c.get(f"/api/events/{eid}/report").json()["stale"] is False
    c.patch(f"/api/items/{eid}", json={"attendees_actual": 96})
    assert c.get(f"/api/events/{eid}/report").json()["stale"] is True


def test_model_down_and_non_event(env, monkeypatch):
    c, cid, eid, report = env

    async def down(*a, **k):
        raise report.llm.LLMError("Ollama'ya ulaşılamadı")
    monkeypatch.setattr(report.llm, "chat", down)
    assert c.post(f"/api/events/{eid}/report").status_code == 503
    task = c.post(f"/api/chats/{cid}/items", json={"title": "iş"}).json()
    assert c.post(f"/api/events/{task['id']}/report").status_code == 404


def test_sample_event_comes_with_a_valid_precomputed_report(env):
    c, cid, eid, report = env
    r = c.post(f"/api/chats/{cid}/sample-event").json()
    assert r["created"] is True
    again = c.post(f"/api/chats/{cid}/sample-event").json()
    assert again == {"event_id": r["event_id"], "created": False}
    got = c.get(f"/api/events/{r['event_id']}/report").json()
    assert got["source"] == "sample" and got["stale"] is False and got["report"].strip()
    b = c.get(f"/api/chats/{cid}/board").json()
    ev = next(e for e in b["events"] if e["id"] == r["event_id"])
    assert "demo" in ev["title"].lower()
    # the shipped text itself obeys the rule: no figure outside the recorded data
    facts = report.facts_text(ev, "tr")
    assert report.unsupported_figures(got["report"], facts) == []
