"""G11 exports: approved only, source text kept, CSV formula injection guard, filters written into the file."""
import csv
import importlib
import io
import json

from fastapi.testclient import TestClient

CHAT = ("01.10.2026 10:00 - Ayşe: =HYPERLINK(\"http://x\") afişi ben yaparım\n"
        "02.10.2026 10:00 - Mert: Salon dilekçesini kim verir?\n"
        "03.10.2026 10:00 - Ayşe: Karar: söyleşi 31 Ekim\n"
        "04.10.2026 10:00 - Mert: önerilen görev\n")


def setup(tmp_path, monkeypatch):
    monkeypatch.setenv("PANO_DB", str(tmp_path / "x.db"))
    from app import db
    db._conn = None
    importlib.reload(db)
    from app import export, main
    importlib.reload(export)
    importlib.reload(main)
    return db, main


def parse(text):
    rows = list(csv.reader(io.StringIO(text.lstrip("﻿"))))
    return rows[:2], rows[2], rows[3:]


def test_exports(tmp_path, monkeypatch):
    db, main = setup(tmp_path, monkeypatch)
    with TestClient(main.app) as c:
        cid = c.post("/api/chats", content=CHAT.encode()).json()["id"]
        db.add_item(cid, "task", title="=SUM(A1)", owner="+evil", unit="@x", due="2026-10-10", source_idx=0)
        db.add_item(cid, "task", title="Bitmiş", owner="Mert", due="2026-12-01", status="done", source_idx=3)
        db.add_item(cid, "task", title="Önerilen", source_idx=3, review="proposed")
        db.add_item(cid, "question", title="Salon dilekçesini kim verir?", source_idx=1)
        db.add_item(cid, "question", title="Kapanmış soru", status="answered", source_idx=1)
        db.add_item(cid, "decision", title="Söyleşi 31 Ekim", source_idx=2)

        r = c.get(f"/api/chats/{cid}/export?what=tasks")
        assert r.status_code == 200 and "attachment" in r.headers["content-disposition"]
        meta, head, rows = parse(r.text)
        assert "date_from=-" in meta[1][0] and "only approved" in meta[1][0]
        assert len(rows) == 2 and "Önerilen" not in r.text  # proposed excluded
        by = {x[1].lstrip("'"): x for x in rows}
        evil = [x for x in rows if x[2].startswith("'+")][0]
        assert evil[1] == "'=SUM(A1)" and evil[3] == "'@x"
        assert evil[9].startswith("'=HYPERLINK")  # source text kept, only neutralised
        assert "afişi ben yaparım" in evil[9]
        for x in rows:  # no cell may start with a formula character
            assert not any(cell.startswith(("=", "+", "-", "@")) for cell in x)

        f = parse(c.get(f"/api/chats/{cid}/export?what=tasks&date_from=2026-11-01&date_to=2026-12-31").text)
        assert [x[1] for x in f[2]] == ["Bitmiş"] and "date_from=2026-11-01" in f[0][1][0]
        assert len(parse(c.get(f"/api/chats/{cid}/export?what=tasks&owner=Mert").text)[2]) == 1

        q = c.get(f"/api/chats/{cid}/export?what=questions&format=json").json()
        assert q["count"] == 1 and q["rows"][0]["source_text"] == "Salon dilekçesini kim verir?"
        assert q["filters"]["status"] == "open" and q["only_approved"] is True
        d = c.get(f"/api/chats/{cid}/export?what=decisions&format=json").json()
        assert d["rows"][0]["source_sender"] == "Ayşe"

        md = c.get(f"/api/chats/{cid}/export?what=summary").text
        assert "Söyleşi 31 Ekim" in md and "Önerilen" not in md and "date_from=-" in md
        assert c.get(f"/api/chats/{cid}/export?what=tasks&date_from=bad").status_code == 400
        assert c.get(f"/api/chats/{cid}/export?what=tasks&date_from=2026-12-01&date_to=2026-01-01").status_code == 400
        assert c.get(f"/api/chats/{cid}/export?what=nope").status_code == 400
        assert c.get("/api/chats/999/export").status_code == 404
