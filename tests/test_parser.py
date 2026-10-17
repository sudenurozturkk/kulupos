from datetime import datetime
from pathlib import Path

from app.parser import parse_chat, read_export

DEMO = Path(__file__).resolve().parent.parent / "demo"


def test_android_tr():
    msgs = parse_chat(
        "17.10.2026 19:32 - Mesajlar ve aramalar uçtan uca şifrelidir.\n"
        "17.10.2026 19:33 - Ayşe Kaya: Afişi ben yaparım\n"
        "ikinci satır\n"
        "17.10.2026 19:34 - Mert: <Medya dahil edilmedi>\n"
        "17.10.2026 19:35 - Mert: Bu mesaj silindi\n"
    )
    assert [m.kind for m in msgs] == ["system", "text", "media", "deleted"]
    assert msgs[1].sender == "Ayşe Kaya"
    assert msgs[1].text == "Afişi ben yaparım\nikinci satır"
    assert msgs[1].ts == datetime(2026, 10, 17, 19, 33)


def test_ios_tr_with_seconds_and_marks():
    msgs = parse_chat(
        "‎[17.10.2026 19:32:05] KBK: ‎Mesajlar ve aramalar uçtan uca şifrelidir.\n"
        "[17.10.2026 19:33:10] Ayşe: Tamam\n"
        "‎[17.10.2026 19:34:00] Ayşe: ‎görüntü dahil edilmedi\n"
    )
    assert [m.kind for m in msgs] == ["system", "text", "media"]
    assert msgs[0].sender is None
    assert msgs[1].ts == datetime(2026, 10, 17, 19, 33, 10)


def test_android_en_us_dates_and_ampm():
    msgs = parse_chat(
        "10/17/26, 7:32 PM - Sam: we need a banner\n"
        "10/18/26, 12:05 AM - Leo: on it\n"
    )
    assert msgs[0].ts == datetime(2026, 10, 17, 19, 32)
    assert msgs[1].ts == datetime(2026, 10, 18, 0, 5)


def test_ios_en_narrow_space_before_pm():
    msgs = parse_chat("[10/5/26, 6:03:40 PM] Maya Chen: Hi all!\n")
    assert msgs[0].ts == datetime(2026, 10, 5, 18, 3, 40)
    assert msgs[0].sender == "Maya Chen"


def test_day_first_slash_dates():
    msgs = parse_chat("05/10/2026, 21:00 - A: x\n25/10/2026, 21:00 - B: y\n")
    assert msgs[0].ts.month == 10 and msgs[0].ts.day == 5


def test_zip_and_encodings(tmp_path):
    import zipfile
    z = tmp_path / "chat.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("WhatsApp Chat - KBK.txt", "17.10.2026 19:33 - Ayşe: selam".encode("utf-8"))
    assert "Ayşe" in read_export(z.read_bytes())
    assert "Ayşe" in read_export("17.10.2026 19:33 - Ayşe: selam".encode("utf-16"))
    assert "Ayşe" in read_export("17.10.2026 19:33 - Ayşe: selam".encode("cp1254"))


def test_demo_chats_parse_cleanly():
    tr = parse_chat((DEMO / "kbk-yonetim-tr.txt").read_text(encoding="utf-8"))
    en = parse_chat((DEMO / "robotics-club-en.txt").read_text(encoding="utf-8"))
    for msgs, members in ((tr, 8), (en, 6)):
        assert len({m.sender for m in msgs if m.sender}) == members
        assert all(m.ts for m in msgs)
