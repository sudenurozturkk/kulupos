# 📌 Pano

**[Türkçe özet](#türkçe-özet) · [English](#english)**

---

## Türkçe özet

**Pano**, öğrenci kulüplerinin WhatsApp yönetim grubunu bilgisayarda çalışan açık model **Gemma 4 (`gemma4:e4b`, Ollama)** ile okuyup görev, karar, açık soru ve etkinlik panosuna çeviren yerel bir uygulamadır.

**Sorun:** Kulüpler WhatsApp'ta yürüyor. Görevler 200 mesajlık bir akşamda dağıtılıyor, etkinlik tarihi iki kez değişiyor, "sponsor dosyası kimde?" sorusu iki hafta cevapsız kalıyor.

**Ne yapıyor:**
- Sohbet dışa aktarımını (.txt / .zip) okur; yüklemeden önce ön izleme gösterir.
- Gemma görev, karar, soru ve etkinlikleri **öneri** olarak çıkarır. Her öneri kaynak mesajına bağlıdır.
- Öneriler **sen onaylayana kadar panoya girmez** (AI incelemesi sekmesi: Onayla / Düzenle / Reddet). Kaynak mesajı bulunamayan öneri onaylanamaz.
- Onaylananlar panoya geçer: komite bazlı görev panosu, gecikenler, atanmamışlar, tarihi çelişenler, yaklaşan etkinlikler.
- Etkinlik kaydı elle girilir; AI etkinlik raporu **yalnızca girilen veriden** yazılır, boş alan "Girilmedi" kalır, veride olmayan sayı içeren rapor reddedilir.

**Neden açık model, neden yerel?** Kulüp sohbetinde onlarca öğrencinin adı, numarası ve özel mesajı var. Pano'da sohbet bilgisayardan çıkmaz: analiz yerel Gemma ile yapılır, sunucu yalnızca `127.0.0.1`'i dinler, harici font/CDN/API anahtarı yoktur. Kullanım ücreti sıfırdır ve model indirildikten sonra internetsiz çalışır. (Bu, veri maruziyetini azaltır; KVKK uyumu garantisi veya hukuki görüş değildir.)

**Hızlı başlangıç:** [Ollama](https://ollama.com/download) kur, `ollama pull gemma4:e4b`, sonra Windows'ta `run.bat`, macOS/Linux'ta `./run.sh`. Veritabanı boşken ilk açılışta **sahte örnek veriyle dolu bir panel** gelir; tek tıkla temizlenir.

**Ölçülen sonuç (dürüst sürüm):** Türkçe demo sohbette (127 mesaj, RTX 3050 4 GB laptop) 14 elle yazılmış kontrolden **10'u geçti, analiz ~230 sn** sürdü. Önceki koşularda 7/14 ve 11/14 görüldü. Model devredilen işleri ve sahip atamalarını bazen kaçırıyor; bu yüzden hiçbir öneri otomatik onaylanmıyor. Ayrıntılar ve bilinen sınırlar aşağıda İngilizce bölümde.

Kodun büyük kısmı **Claude Code** ile yazıldı; insan incelemesi ve otomatik testlerle ilerledi (aşağıya bakın). Lisans: MIT.

---

## English

**Pano turns a student club's WhatsApp group into a task board, using Gemma 4 running on the club lead's own laptop. Every item is a proposal with a source message, and nothing reaches the board until a human approves it.**

Started at **Hacktoberfest Elazığ Fest 2026** (Week 2: *Side Hustle*).

### The problem

Student clubs run on WhatsApp. Tasks are handed out during a 200-message evening, the event date changes twice, someone asks "who has the sponsor file?" and nobody answers for two weeks. The information exists, but it is buried in the chat.

### What it does

1. **Import** a WhatsApp export (`.txt` or `.zip`; Android/iOS, Turkish/English date formats). A preview shows message count, date range, senders and unparseable lines before anything is saved. Files over 5 MB and re-imports of the same file are flagged.
2. **Analyse** with a local Gemma 4 model (`gemma4:e4b` through Ollama): tasks, decisions, open questions, events.
3. **Evidence.** Each proposal links to the message it came from and shows the quote with sender and time.
4. **Human approval.** Proposals sit in an *AI review* queue (Approve / Edit / Reject). They do not count as real tasks until approved. A proposal without a valid source message cannot be approved; an unclear date is flagged. Later AI edits to an already approved record arrive as *change proposals*, never as silent overwrites, and your own edits are not overwritten by later analyses.
5. **Board and panel.** Per-team (editable committees) task board, a "needs attention today" panel (overdue, unassigned, conflicting dates, decisions not yet marked final), upcoming events, import history. Counts of AI proposals are kept apart from real task counts, and "no data" is shown as "—", not as a zero.
6. **Events.** Manual event records (type, status, attendees, budget, committees, linked tasks and decisions). The AI event report is built **only from the recorded fields**; empty fields stay "Girilmedi / Not entered", and a report containing a number that is not in the input is rejected.
7. Also: weekly recap formatted for WhatsApp, "ask the chat" with source links, an AI event planner, Markdown export.

### How it works

```
WhatsApp export (.txt / .zip)
   │  parser.py: Android/iOS, TR/EN dates, multi-line, media/system lines, size + duplicate checks
   ▼
analyzer.py: sliding windows of ~30 messages + the CURRENT board state
   │  ──► Gemma 4 via Ollama, JSON-schema constrained output
   ▼
proposals (review = "proposed", source message attached, flags for no-source / unclear date)
   │  ──► human: approve / edit / reject
   ▼
SQLite (one local file) ──► FastAPI (127.0.0.1) ──► vanilla JS UI (no framework, no CDN, no web fonts)
```

Gemma sees the board as it currently stands together with the new messages, so it can close a task ("dilekçeyi verdim ✅"), reassign one or move an event instead of piling up duplicates. Guardrails around the small model: structured output, a calendar in the prompt instead of date arithmetic, owners matched against the real member list, units matched against the club's teams, date validation, source ids that must lie inside the current window, fuzzy de-duplication.

### Why an open model, run locally

| | Pano (Gemma 4 + Ollama) | A hosted API |
|---|---|---|
| **Privacy** | Names, phone numbers and private messages of dozens of students stay on the laptop. This reduces exposure; it is not legal advice or a compliance guarantee (KVKK/GDPR) | The whole chat is sent to a third party |
| **Cost** | No per-use fees; re-analyse as often as you like | Needs a budget and a payment method that clubs rarely have |
| **Offline** | Works without internet once the model is pulled | Needs a connection |
| **Lock-in** | `PANO_MODEL` swaps in any Ollama model | Pricing and terms can change |

The server binds to `127.0.0.1`, the UI loads no external script, stylesheet or font, and the only network calls go to your local Ollama. Error messages can contain up to 200 characters of raw model output; they are stored in the local database only.

### Setup

Requirements: [Ollama](https://ollama.com/download), Python 3.10+, roughly 8 GB of free RAM.

```bash
ollama pull gemma4:e4b          # tested tag
git clone <this repo> && cd <repo>
pip install -r requirements.txt
python -m app                   # http://127.0.0.1:8000  (PANO_PORT=8010 if 8000 is taken)
```

Windows: double-click `run.bat`. macOS/Linux: `./run.sh` (both check for Ollama, pull the model if missing, create a venv and start the app).

| env var | default | |
|---|---|---|
| `PANO_MODEL` | `gemma4:e4b` | any Ollama model, e.g. `gemma4:e2b` for weaker machines |
| `OLLAMA_URL` | `http://localhost:11434` | |
| `PANO_PORT` | `8000` | |
| `PANO_DB` | `data/pano.db` | database file |
| `PANO_CHUNK` / `PANO_NUM_CTX` | `30` / `8192` | messages per window / context length |
| `PANO_TODAY` | today | pin "today" for demos and tests |

### First run and screen flow

With an empty database the app opens on a **sample club filled with fake data** (clearly labelled "Örnek veri / Sample data", removable with one click, and it does not come back once cleared). A short welcome answers: what it does, which file to upload, where the data goes, whether analysis started, where to check results, and what to do when the AI is wrong.

Flow: **Club status** (today's focus, cards that link to filtered lists) → **AI review** (approve / edit / reject with the source quote) → **Board** (teams, events, decisions) → **Plan an event** → **Weekly recap** → **Ask the chat**. The event form has an event report button; the sample event ships with a precomputed report.

You can also try the Turkish or English demo chats from the home page, or upload your own export (*WhatsApp → group → Export chat → Without media*).

### Measured results

`scripts/eval_demo.py` runs the whole pipeline on a demo chat and checks it against 14 hand-written expectations (moved event dates, reassigned tasks, unanswered questions, decisions). Turkish demo, 127 messages, `gemma4:e4b` via Ollama on a laptop with an RTX 3050 (4 GB VRAM) and 16 GB RAM:

| run | checks passed | time |
|---|---|---|
| baseline prompt | 7 / 14 | 432 s |
| + few-shot example, unit rules | 11 / 14 | 344 s |
| final prompt (earlier run) | 10 / 14 | 379 s |
| latest (current code) | **10 / 14** | **~230 s** |

Results vary by one or two checks between runs. The latest run produced 17 proposals (6 decisions, 5 tasks, 3 questions, 3 events); none was flagged as source-less or date-unclear. The checks it misses are of two kinds: **task handovers** (a task passed from one person to another) and **owner assignment** ("Afiş → Zeynep", "Story series → Ece"), plus one question that only carries a time. That is exactly why nothing is auto-approved: the model is useful as a fast first pass, not as a source of truth. Other timings measured earlier on the same machine: weekly recap about 30 s, ask-the-chat about 15 s, event plan about 75 s. The English demo's checks exist but have never been run.

### Known limits

- **Speed.** On this hardware Gemma 4 e4b needs minutes for a few hundred messages. That is why the first-run sample data and the sample event's precomputed report exist: the app can be explored without waiting for the model. A smaller model (`gemma4:e2b`) or a GPU with more VRAM is faster.
- **Figure check is coarse.** The event-report check compares digit groups against the input. A made-up number is caught, but reusing a digit group that exists elsewhere in the data (say "10" from a date) in a wrong context is not. Only one real model run of the event report was done (on the sample event).
- **Accuracy.** About 10 of 14 on one demo chat is not a general accuracy figure; it is one small hand-labelled test on a fictional chat.
- **Not built yet** (the working checklist is `DURUM.md`, which lags behind recent work; this list is what the code does today): club profile and permissions (there is no login on purpose), universal search, task search/sort/filter, CSV/JSON export (Markdown only), sub-tasks, dependencies and comment history, a "resolved / invalid" button for open questions, decision history, month/week calendar and clash warnings, duplicate/conflict suggestions shown to the user (fuzzy duplicates are only skipped), source links inside the weekly recap. `DURUM.md` also lists a known bug in the recap's "completed" list that has not been re-checked.
- **Testing.** Backend and API are covered by automated tests with a fake model. There are no automated UI tests; the interface was inspected by hand in Chrome only. The live-model path is covered by the eval script, not by the test suite.
- **Privacy scope.** Deleting a club removes its rows from the local SQLite file; backups or copies of that file are yours to manage.

### Project structure

```
app/        parser, analyzer (windows + guardrails), llm (Ollama client), db (SQLite), insights (panel, planner),
            assistant (recap, ask), report (event report + figure check), seed (sample club), main (FastAPI)
static/     index.html, app.js, style.css  (vanilla JS, light theme only)
demo/       fictional TR/EN chats, sample-club and sample-event data
scripts/    eval_demo.py (pipeline eval), make_sample_report.py (regenerates the sample event report)
tests/      pytest suites (no Ollama needed)
run.bat, run.sh, requirements.txt (fastapi, uvicorn, httpx)
```

### Tests

```bash
pip install pytest
python -m pytest tests -q          # fake model, no Ollama required
python scripts/eval_demo.py        # live model on the Turkish demo (a few minutes); `en` for the English one
```

`scripts/eval_demo.py` uses a throwaway database and also saves the raw proposals as JSON under `data/eval_runs/` (git-ignored; demo data only).

### AI-assisted development

Most of the code was written with **Claude Code** (Anthropic's coding agent) in sessions guided and reviewed by the author, working task by task from a written plan, with automated tests for each step and the author's approval before commits. The product itself runs on an open-weight model (Gemma 4) and never calls a hosted AI API.

### Data and licence

All demo and sample data is fictional. Real chats, the local database and evaluation runs are git-ignored and must never be committed.

MIT License, © 2026 Sudenur Öztürk. See [LICENSE](LICENSE).
