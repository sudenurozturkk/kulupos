# KulüpOS: submission texts

Every sentence below describes something that exists in the repository today. Things that are only planned are labelled as planned. Numbers come from `README.md` and `DURUM.md`.

---

## (a) Devpost / MLH project description (English)

### Inspiration

Student clubs lose track of their own work. Tasks sit in chats, decisions in someone's notes, event data in spreadsheets, and with more than ten people, many committees and busy festivals nobody knows what is where. We wanted one free place where a club enters everything any time, during a meeting or an event, keeps it on its own computer, and lets a local AI analyse it and suggest what to do next, without sending students' names and messages to a cloud service.

### What it does

KulüpOS is one workspace for a club's tasks, decisions, open questions, events and meetings. Information is entered by hand at any time (stored locally), and WhatsApp exports and meeting notes can be imported too.

- You import a WhatsApp export (`.txt` or `.zip`); a preview shows what was read before anything is saved.
- A local Gemma 4 model proposes tasks, decisions, open questions and events. Every proposal is linked to the message (or note line) it came from.
- **Nothing is auto-approved.** Proposals wait in an AI review queue (Approve / Edit / Reject). A proposal whose source cannot be found cannot be approved.
- Approved records feed a per-committee task board, a "needs attention today" dashboard (overdue, unassigned, conflicting dates), upcoming events and meetings.
- Meetings: notes are pasted or uploaded, suggestions go through the same review queue, and a meeting summary is written only from the notes and approved linked records.
- Event page: linked tasks, decisions, attendance, hand-entered feedback and a report written only from those records.
- A People page lists task owners with counts only (no performance verdict), and data can be exported as CSV / JSON / Markdown.

### How we built it

Python (FastAPI) with one local SQLite file and a plain JavaScript interface with no framework, no CDN and no web fonts. The model is the open-weight **Gemma 4 `gemma4:e4b`**, run through a local Ollama server with JSON-schema constrained output. The analyzer feeds the model sliding windows of about 30 messages together with the current board, so it can close, reassign or move something instead of piling up duplicates. Around the small model we added guardrails written as ordinary code: owners matched against the real member list, a calendar in the prompt instead of date arithmetic, date validation, source ids that must lie inside the current window, fuzzy de-duplication, and checks on generated text (a number, name or quotation that is not in the input rejects the text). The backend is covered by 110+ automated tests that use a fake model; the live-model path is covered by evaluation scripts. Most of the code was written with Claude Code, task by task from a written plan, with tests and human review before each commit.

### Challenges

- **Speed.** On a laptop with an RTX 3050 (4 GB VRAM) the Turkish demo chat (127 messages) takes about 230 seconds. We shipped a fictional sample club with precomputed texts so the app can be explored without waiting.
- **A small model makes mistakes.** On our 14 hand-written checks it passes 10 (earlier runs: 7 and 11). It misses task handovers and some owner assignments. That is why every result is a proposal with a source.
- **Making "don't invent" real.** Prompts alone are not enough, so generated reports and summaries are verified in code and rejected when they contain unsupported figures, names or quotations. When we looked at the real model's sample event report, it wrote "Decision count: not entered" and called a single comment a shared topic, so we removed empty fields from the prompt and added checks (a topic may be called common only if two different comments are quoted; text that mentions missing data is rejected) and regenerated the sample report.
- **Untrusted text.** Notes and comments may contain instructions; they are passed to the model as data inside marked blocks whose markers cannot be forged.

### What we learned

Structured output plus checks in code matter more than prompt wording for a small local model. A review queue with a visible source quote turns an unreliable model into a useful first pass. Reporting honest numbers (10/14, not "accurate") is uncomfortable but keeps the product trustworthy.

### What's next

Planned, **not built**: multi-user accounts and roles (today there is a single local account with sign-in and sign-out, and no roles), in-app messaging, meeting audio recording, budget and sponsor tracking, integrations with outside platforms. Also open: the English demo evaluation has never been run, duplicate/conflict suggestions are not shown to the user, and the interface has no automated UI tests.

### Built with

Gemma 4 (`gemma4:e4b`), Ollama, Python, FastAPI, Uvicorn, httpx, SQLite, vanilla JavaScript, HTML/CSS, pytest, GitHub Actions, Claude Code.

---

## (b) Short description and tagline

**Three sentences.** KulüpOS is a local-first tool that turns a student club's WhatsApp export, meeting notes and event records into a board of tasks, decisions, open questions and events. An open Gemma 4 model running on the user's own computer proposes the items, each with a source quote, and nothing counts until a human approves it. Reports and summaries are written only from entered data, and anything unsupported is rejected.

**Tagline.** Your club's work in one place, found by Gemma on your own laptop and approved by you.

---

## (c) DEV.to article draft (~500 words)

**Title: I built a local Gemma 4 tool that finds a student club's lost tasks in WhatsApp, and never trusts it blindly**

Student clubs run on WhatsApp. During one 200-message evening, five tasks are handed out, the event date changes twice, and someone asks "who has the sponsor file?" The answer arrives two weeks later, or never. The information exists; it is just buried.

For Hacktoberfest Elazığ Fest 2026 I built **KulüpOS**, a tool that reads a club's WhatsApp export, meeting notes and event records and turns them into a board of tasks, decisions, open questions and events.

**How it works.** You import an export (`.txt` or `.zip`). A parser handles Android and iOS formats and Turkish and English dates. Then an analyzer sends the model windows of about 30 messages together with the current board, so it can close a task ("dilekçeyi verdim ✅") or reassign one instead of creating duplicates. The model is **Gemma 4 `gemma4:e4b`**, running through a local Ollama server with JSON-schema constrained output. The backend is FastAPI with one SQLite file, and the interface is plain JavaScript with no CDN.

**Why local.** A club chat contains dozens of students' names, numbers and private messages. In KulüpOS the server listens only on `127.0.0.1`, the UI loads nothing external, and there is no API key. It also costs nothing per use and works offline once the model is pulled. That reduces exposure; it is not legal advice or a compliance guarantee.

**Safety by design.**
1. *A source is required.* Every proposal links to the message or note line it came from. A proposal without a source cannot be approved.
2. *No auto-approval.* Proposals wait in a review queue. They are counted separately from real tasks.
3. *No invention.* Unknown owners, dates and committees stay empty. Event reports and meeting summaries are written only from entered data, and the code rejects text containing a number, a name or a quotation that is not in the input. A topic can be called "common" in a feedback report only if two different comments are quoted.
4. *Your edits win.* Later analyses never overwrite a human correction; AI changes to approved records arrive as change proposals.
5. *Notes are data.* An instruction hidden in meeting notes ("ignore previous instructions...") is treated as text, not a command. In our test it produced no suggestion.

**Honest limits.** On a laptop with an RTX 3050 (4 GB), analysing a 127-message Turkish demo chat takes about 230 seconds. On my 14 hand-written checks it passes 10 (earlier runs gave 7 and 11); it misses task handovers and some owner assignments. On two short meetings every suggestion quoted a real note line and nothing was invented, but it missed an ownerless task, so recall is low. That is two meetings, not an accuracy figure. The interface has no automated UI tests, and the English demo has never been evaluated. Accounts, roles, messaging, audio recording and integrations are planned, not built.

**Takeaway.** With a small local model, checks in ordinary code and a human approval step matter more than clever prompts. The model is a fast first pass; the source quote is what you can rely on.

Code, tests and the fictional demo club are in the repository (MIT licence). Most of the code was written with Claude Code, task by task, with tests before each commit.

---

## (d) 2-minute demo script (Turkish)

**0:00–0:15 · Giriş ekranı.** "Kulüpler WhatsApp'ta yürüyor. İki yüz mesajlık bir akşamda görevler dağılıyor, etkinlik tarihi iki kez değişiyor, kimin ne yaptığı kayboluyor. KulüpOS bunu tek yerde topluyor ve her şey bilgisayarınızda, yerel Gemma 4 ile çalışıyor." *"Demo kulübü aç"* düğmesine bas.

**0:15–0:40 · Panel.** "Bu örnek kulüp tamamen sahte veri, üstünde 'Örnek veri' yazıyor. Panel bugün ilgilenilecekleri gösteriyor: geciken görevler, sorumlusu olmayanlar, yaklaşan etkinlik ve toplantılar. Yapay zekâ önerileri gerçek görev sayısından ayrı tutuluyor; verisi olmayan yerde sıfır değil çizgi görüyorsunuz."

**0:40–1:05 · Görevler → AI incelemesi.** "Gemma sohbetten görev, karar ve soru *öneriyor*. Her önerinin altında kaynak mesajı, gönderen ve saat var. Kaynağı bulunamayan öneri onaylanamıyor. Hiçbir şey ben onaylamadan panoya girmiyor." Bir öneriyi **Onayla**, birini **Reddet**.

**1:05–1:30 · Toplantılar.** "Toplantı notunu yapıştırıyorum ya da dosya yüklüyorum. Çıkan öneriler aynı kuyruktan geçiyor ve not satırını alıntılıyor. Özet yalnızca notlardan ve onaylı kayıtlardan yazılıyor; kayıtta olmayan bir sayı veya isim geçerse özet reddediliyor." Önceden hazır özeti göster.

**1:30–1:50 · Etkinlik sayfası.** "Python Atölyesi: bağlı görevler, katılım oranı, elle girilen geri bildirim ve rapor tek sayfada. Rapor yalnızca girilen veriden yazıldı; bir konuya 'ortak' diyebilmesi için en az iki farklı yorumdan alıntı gerekiyor. Veri olmayan alanlar raporda hiç yer almıyor."

**1:50–2:00 · Kapanış.** "Ölçülen sonuç dürüst: Türkçe demo sohbette 14 kontrolün 10'u geçti, yaklaşık 230 saniye sürdü; model bazı devirleri kaçırıyor, o yüzden otomatik onay yok. KulüpOS: kulübün işleri tek yerde, veriniz sizde."

*Sunum notları:* canlı analiz yaklaşık 4 dakika sürer, bu yüzden demoda analiz beklenmez, hazır örnek kulüp kullanılır. Hesap/rol, mesajlaşma, ses kaydı ve entegrasyonlar henüz yok; sahnede varmış gibi anlatılmaz.
