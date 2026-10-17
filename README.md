# 📌 Pano

**Your student club's WhatsApp group, turned into a task board, by Gemma 4 running on your own laptop.**

Student clubs run on WhatsApp. Tasks get handed out in a 200-message evening, the event date changes
twice, someone asks "who has the sponsor file?" and nobody answers for two weeks. Pano reads the group's
chat export with a local open-weight model and gives the club back:

- **A board per team.** Every task with its owner, due date and the exact message it came from
- **"Slipping through"**: unanswered questions, work nobody took, overdue and due-soon tasks
- **Decisions and a calendar** that follow the chat when plans change ("let's move it to Oct 31")
- **A weekly recap formatted for WhatsApp**, so the club lead can paste it back into the group in one click
- **Ask the chat**: "Did we get the room?", answered with links to the source messages

Nothing leaves the machine. No API keys, no cloud and no per-message fees, and it works offline once the model is installed.

> Built in one night at **Hacktoberfest Elazığ Fest 2026** (Week 2: *Side Hustle*).

---

## Why an open model, and not a closed API?

| | Pano (Gemma 4 + Ollama, local) | A closed API |
|---|---|---|
| **Privacy** | Phone numbers, names and private messages of 30+ students stay on the laptop (this reduces exposure; it is not legal advice) | The whole chat is uploaded to a third party |
| **Cost** | No per-use fees, only your own electricity. Re-analyse as often as you like | Student clubs have no budget and no credit card |
| **Offline** | Works on the campus Wi-Fi, or with no Wi-Fi at all | Needs a connection |
| **Lock-in** | Swap `gemma4:e4b` for any Ollama model with one env var | Pricing and terms can change any time |

## How it works

```
WhatsApp export (.txt / .zip)
        │
        ▼
  parser.py  ── Android/iOS, TR/EN date formats, multi-line messages, media & system lines
        │
        ▼
  analyzer.py ── sliding windows of ~30 messages
        │        each window + the CURRENT board state  ──►  Gemma 4 (Ollama, JSON-schema constrained)
        │        ◄── new tasks · updates to existing tasks · questions · answers · decisions · events
        ▼
  SQLite (local file)  ──►  FastAPI  ──►  board UI (vanilla JS, no CDN, works offline)
```

The key design choice is that **Gemma sees the board as it currently stands, along with the new messages**.
That way it can close a task ("dilekçeyi verdim ✅"), hand it to someone else ("I can't make it, Selin takes it")
or move an event ("they moved us to the 30th") rather than piling up duplicates. Every item links back to its
source message, so nothing on the board is unverifiable.

Small-model guardrails:
- Structured outputs via Ollama's `format` JSON schema, so the response is always valid JSON
- A calendar is passed to the model, so it doesn't have to do date arithmetic for "next Thursday"
- Owners are matched against the real member list, units against the club's units, dates are validated, and source ids must sit inside the current window
- Fuzzy de-duplication, plus manual edits always win over later model updates

## Quick start

Requirements: [Ollama](https://ollama.com/download), Python 3.10+, about 8 GB of free RAM.

```bash
ollama pull gemma4:e4b      # tested tag: gemma4:e4b
git clone <this repo> && cd pano
pip install -r requirements.txt
python -m app            # opens http://127.0.0.1:8000
```

On Windows you can also double-click `run.bat`; on macOS or Linux run `./run.sh`.

Click **Try a demo chat** to see it on a realistic (fictional) club chat, or drop your own export:
*WhatsApp → group → Export chat → Without media*.

### Configuration

| env var | default | |
|---|---|---|
| `PANO_MODEL` | `gemma4:e4b` | any Ollama model, e.g. `gemma4:e2b` for weaker laptops |
| `OLLAMA_URL` | `http://localhost:11434` | |
| `PANO_CHUNK` | `30` | messages per window |
| `PANO_NUM_CTX` | `8192` | context length |
| `PANO_TODAY` | today | pin "today", handy for demos |

## Evaluation

`scripts/eval_demo.py` runs the full pipeline on a demo chat and checks it against hand-written expectations
(moved event dates, reassigned tasks, unanswered questions, decisions):

```bash
python scripts/eval_demo.py      # Turkish demo
python scripts/eval_demo.py en   # English demo
```

Measured on the Turkish demo (127 messages) with `gemma4:e4b` via Ollama 0.32.9, on a laptop with an
RTX 3050 (4 GB VRAM) and 16 GB RAM:

| run | checks passed | time |
|---|---|---|
| baseline prompt | 7 / 14 | 432 s |
| + few-shot example, unit rules | 11 / 14 | 344 s |
| final prompt | 10 / 14 | 379 s |

Results vary by one or two checks between runs. Typical misses: a task handed over between two people,
a question that only has a time attached, and occasionally the wrong unit for a task. Every card links to its
source message and is editable for exactly this reason. Other timings on the same machine: weekly recap about
30 s, ask-the-chat about 15 s, event plan about 75 s. A smaller `gemma4:e2b` or a GPU with more VRAM is faster.

## Privacy notes

- The server binds to `127.0.0.1` only.
- The UI loads no external fonts, scripts or CDNs.
- Chats live in `data/pano.db`, which is git-ignored. Delete a group from the UI and its board is gone.
- The demo chats in `demo/` are fictional.

## Roadmap

- Incremental weekly imports (already supported: "Add a newer export" only analyses new messages)
- Per-member "my tasks" view, shareable as a WhatsApp message
- Fine-tuning a smaller Gemma on annotated club chats

## License

MIT
