"use strict";

// ---------------------------------------------------------------- i18n
const I18N = {
  tr: {
    hero_title: "WhatsApp grubundaki karmaşayı panoya çevirin",
    hero_sub: "Kulübünüzün sohbet dışa aktarımını bırakın. Gemma 4 bu bilgisayarda okur; görevleri, kararları, tarihleri ve cevapsız soruları çıkarır. Hiçbir mesaj internete gitmez.",
    drop: "WhatsApp dışa aktarımını buraya bırakın",
    drop_hint: ".txt ya da .zip · tıklayıp dosya da seçebilirsiniz",
    units_label: "Kulübünüzün birimleri (virgülle ayırın)",
    units_default: "Yönetim, Etkinlik, Sosyal Medya, Sponsorluk, Teknik",
    name_label: "Grup adı (isteğe bağlı)",
    try_demo: "Demo sohbetle dene",
    how_export: "WhatsApp'tan nasıl dışa aktarılır?",
    how_steps: ["Grubu açın, grup adına dokunun", "En alttaki <b>Sohbeti dışa aktar</b>'ı seçin", "<b>Medya olmadan</b> deyin, dosyayı bu bilgisayara gönderin"],
    privacy: "🔒 <b>Veri bu bilgisayardan çıkmaz.</b> Model Ollama ile yerelde çalışır; üye numaraları ve mesajlar hiçbir buluta gönderilmez.",
    recent: "Önceki gruplar",
    messages: "mesaj",
    health_ok: "Yerel · Gemma 4 hazır",
    health_nomodel: "Model yok: ollama pull",
    health_down: "Ollama kapalı",
    tab_board: "Pano", tab_summary: "Haftalık özet", tab_ask: "Sohbete sor",
    analyzing: "Gemma sohbeti okuyor…", queued: "Sırada bekliyor…", part: "parça",
    analysis_error: "Analiz durdu",
    retry: "Tekrar dene",
    found: { task: "görev", question: "soru", decision: "karar", event: "etkinlik", update: "güncellendi" },
    no_unit: "Birimsiz",
    everyone: "Herkes",
    show_done: "Bitenleri göster",
    copy_member: n => `${n} için WhatsApp mesajı`,
    member_msg_head: n => `Selam ${n} 👋 Panoda senin üzerinde görünen işler:`,
    member_msg_empty: "Şu an açık bir işin yok 🎉",
    missed: "Gözden kaçanlar",
    m_questions: "Cevapsız sorular", m_orphans: "Kimsenin üstlenmediği işler", m_overdue: "Tarihi geçenler", m_soon: "3 gün içinde",
    nothing_missed: "Şimdilik gözden kaçan bir şey yok 🎉",
    decisions: "Kararlar", events: "Takvim",
    none_yet: "Henüz yok",
    no_owner: "sahibi yok", no_due: "tarih yok",
    asked_by: "soran",
    add_task: "Görev ekle", edit_task: "Görevi düzenle",
    f_title: "Görev", f_owner: "Sorumlu", f_due: "Son tarih", f_unit: "Birim", f_status: "Durum",
    st_open: "Açık", st_done: "Bitti",
    save: "Kaydet", cancel: "Vazgeç", del: "Sil", close: "Kapat",
    source: "Kaynak mesaj", source_title: "Sohbette nerede geçti?",
    reanalyze: "Baştan analiz et", add_export: "Yeni dışa aktarımı ekle", delete_chat: "Grubu sil",
    confirm_delete: "Bu grubun panosu silinsin mi? (WhatsApp'taki sohbet etkilenmez)",
    added_msgs: n => `${n} yeni mesaj eklendi, analiz ediliyor`,
    no_new: "Yeni mesaj yok",
    summary_intro: "Son 7 günün özeti: Gemma kısa bir değerlendirme yazar, Pano açık görevleri, cevapsız soruları ve yaklaşan tarihleri ekler. Tek tıkla gruba yapıştırın.",
    summary_btn: "Bu haftanın özetini çıkar", summary_wait: "Gemma özet yazıyor…",
    copy: "WhatsApp için kopyala", copied: "Kopyalandı ✓ Gruba yapıştırabilirsiniz",
    ask_intro: "Sohbette kaybolan bir bilgiyi sorun. Cevap, kaynak mesajlarıyla gelir.",
    ask_ph: "Örn: Salon onaylandı mı?", ask_btn: "Sor", ask_wait: "Gemma mesajlara bakıyor…",
    suggestions: ["Etkinlik ne zaman ve nerede?", "Sponsor karşılığında ne istiyor?", "Hangi işler hâlâ bekliyor?"],
    sources: "Kaynaklar",
    need_model: "Önce analiz bitsin ya da model hazır olsun.",
    err: "Bir şeyler ters gitti",
  },
  en: {
    hero_title: "Turn your club's WhatsApp chaos into a board",
    hero_sub: "Drop your group's chat export. Gemma 4 reads it on this computer and pulls out tasks, decisions, dates and unanswered questions. Not a single message leaves the device.",
    drop: "Drop a WhatsApp export here",
    drop_hint: ".txt or .zip · or click to choose a file",
    units_label: "Your club's teams (comma separated)",
    units_default: "Board, Events, Social Media, Sponsorship, Tech",
    name_label: "Group name (optional)",
    try_demo: "Try a demo chat",
    how_export: "How do I export from WhatsApp?",
    how_steps: ["Open the group and tap its name", "Scroll down and choose <b>Export chat</b>", "Pick <b>Without media</b> and send the file to this computer"],
    privacy: "🔒 <b>Your data never leaves this computer.</b> The model runs locally with Ollama; member phone numbers and messages are never sent to any cloud.",
    recent: "Previous groups",
    messages: "messages",
    health_ok: "Local · Gemma 4 ready",
    health_nomodel: "Model missing: ollama pull",
    health_down: "Ollama is not running",
    tab_board: "Board", tab_summary: "Weekly recap", tab_ask: "Ask the chat",
    analyzing: "Gemma is reading the chat…", queued: "Waiting in line…", part: "part",
    analysis_error: "Analysis stopped",
    retry: "Retry",
    found: { task: "task", question: "question", decision: "decision", event: "event", update: "updated" },
    no_unit: "No team",
    everyone: "Everyone",
    show_done: "Show done",
    copy_member: n => `WhatsApp message for ${n}`,
    member_msg_head: n => `Hi ${n} 👋 Here's what's on you on the board:`,
    member_msg_empty: "Nothing open right now 🎉",
    missed: "Slipping through",
    m_questions: "Unanswered questions", m_orphans: "Nobody took these", m_overdue: "Overdue", m_soon: "Due within 3 days",
    nothing_missed: "Nothing is slipping through right now 🎉",
    decisions: "Decisions", events: "Calendar",
    none_yet: "Nothing yet",
    no_owner: "no owner", no_due: "no date",
    asked_by: "asked by",
    add_task: "Add task", edit_task: "Edit task",
    f_title: "Task", f_owner: "Owner", f_due: "Due date", f_unit: "Team", f_status: "Status",
    st_open: "Open", st_done: "Done",
    save: "Save", cancel: "Cancel", del: "Delete", close: "Close",
    source: "Source message", source_title: "Where was this said?",
    reanalyze: "Re-analyse from scratch", add_export: "Add a newer export", delete_chat: "Delete group",
    confirm_delete: "Delete this group's board? (The WhatsApp chat itself is not affected)",
    added_msgs: n => `${n} new messages added, analysing`,
    no_new: "No new messages",
    summary_intro: "A recap of the last 7 days: Gemma writes a short overview, Pano adds open tasks, unanswered questions and upcoming dates. Paste it into the group in one click.",
    summary_btn: "Write this week's recap", summary_wait: "Gemma is writing…",
    copy: "Copy for WhatsApp", copied: "Copied ✓ Paste it into the group",
    ask_intro: "Ask about something that got buried in the chat. The answer comes with its source messages.",
    ask_ph: "e.g. Did we get the room?", ask_btn: "Ask", ask_wait: "Gemma is looking through the messages…",
    suggestions: ["When and where is the event?", "What does the sponsor want in return?", "Which tasks are still open?"],
    sources: "Sources",
    need_model: "Wait for the analysis or the model first.",
    err: "Something went wrong",
  },
};
let lang = (() => {
  try { return localStorage.getItem("pano.lang") || (navigator.language.startsWith("tr") ? "tr" : "en"); }
  catch { return "tr"; }
})();
const t = key => I18N[lang][key] ?? key;

// ---------------------------------------------------------------- helpers
const $ = sel => document.querySelector(sel);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function api(path, opts = {}) {
  const res = await fetch(path, {
    ...opts,
    headers: opts.body && !(opts.body instanceof ArrayBuffer) ? { "Content-Type": "application/json" } : {},
  });
  if (!res.ok) {
    let detail = res.statusText;
    try { detail = (await res.json()).detail || detail; } catch {}
    throw new Error(detail);
  }
  return res.json();
}
const post = (path, body) => api(path, { method: "POST", body: body instanceof ArrayBuffer ? body : JSON.stringify(body ?? {}) });
const patch = (path, body) => api(path, { method: "PATCH", body: JSON.stringify(body) });

function toast(msg, ms = 2600) {
  const el = $("#toast");
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => (el.hidden = true), ms);
}

function hue(name) {
  let h = 0;
  for (const c of name || "") h = (h * 31 + c.charCodeAt(0)) % 360;
  return h;
}
function avatar(name) {
  if (!name) return "";
  const initials = name.split(/\s+/).map(p => p[0]).slice(0, 2).join("").toUpperCase();
  return `<span class="avatar" style="background:hsl(${hue(name)} 55% 45%)">${esc(initials)}</span>`;
}
const firstName = n => (n || "").split(/\s+/)[0];

const MONTHS = {
  tr: ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"],
  en: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
};
const DAYS = { tr: ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"], en: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] };
function fmtDate(iso, withDay = true) {
  if (!iso) return "";
  const d = new Date(iso.slice(0, 10) + "T12:00:00");
  return `${withDay ? DAYS[lang][d.getDay()] + " " : ""}${d.getDate()} ${MONTHS[lang][d.getMonth()]}`;
}
function fmtTs(ts) {
  const d = new Date(ts);
  return `${d.getDate()} ${MONTHS[lang][d.getMonth()]} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

// ---------------------------------------------------------------- state
const S = { chats: [], board: null, health: null, member: "", showDone: false, poll: null, summary: null, answer: null };

function route() {
  const [, kind, id, view] = location.hash.split("/");
  return kind === "c" ? { chatId: Number(id), view: view || "board" } : { chatId: null, view: "home" };
}

async function refreshHealth() {
  try { S.health = await api("/api/health"); } catch { S.health = null; }
  const el = $("#health");
  const h = S.health;
  if (h && h.model_ready) { el.className = "badge ok"; el.innerHTML = `<span class="dot"></span>${t("health_ok")} <small>(${esc(h.model)})</small>`; }
  else if (h && h.ollama) { el.className = "badge warn"; el.innerHTML = `<span class="dot"></span>${t("health_nomodel")} ${esc(h.model)}`; }
  else { el.className = "badge bad"; el.innerHTML = `<span class="dot"></span>${t("health_down")}`; }
}

async function refreshChats() {
  try { S.chats = await api("/api/chats"); } catch { S.chats = []; }
  const { chatId } = route();
  const box = $("#chat-switch");
  if (!S.chats.length || !chatId) { box.innerHTML = ""; return; }
  box.innerHTML = `<select id="chat-select">${S.chats.map(c =>
    `<option value="${c.id}" ${c.id === chatId ? "selected" : ""}>${esc(c.name)}</option>`).join("")}
    <option value="new">＋</option></select>`;
  $("#chat-select").onchange = e => {
    location.hash = e.target.value === "new" ? "#/" : `#/c/${e.target.value}/board`;
  };
}

// ---------------------------------------------------------------- home
function renderHome() {
  const app = $("#app");
  app.innerHTML = `
  <section class="home">
    <div class="hero">
      <h1>${t("hero_title")}</h1>
      <p>${t("hero_sub")}</p>
    </div>
    <div class="home-grid">
      <div class="panel">
        <div class="drop" id="drop" tabindex="0" role="button">
          <div class="big">💬 → 📌</div>
          <b>${t("drop")}</b>
          <small>${t("drop_hint")}</small>
        </div>
        <input type="file" id="file" accept=".txt,.zip,text/plain,application/zip" hidden>
        <label for="units">${t("units_label")}</label>
        <input type="text" id="units" value="${esc(t("units_default"))}">
        <label for="gname">${t("name_label")}</label>
        <input type="text" id="gname" placeholder="FÜBET Yönetim">
        <div class="demo-row">
          <button class="primary" data-demo="${lang}">✨ ${t("try_demo")}</button>
          <button class="ghost" data-demo="${lang === "tr" ? "en" : "tr"}">${lang === "tr" ? "English demo" : "Türkçe demo"}</button>
        </div>
      </div>
      <div class="panel">
        <h3>${t("how_export")}</h3>
        <ol class="steps">${t("how_steps").map(s => `<li>${s}</li>`).join("")}</ol>
        <div class="privacy">${t("privacy")}</div>
        ${S.chats.length ? `<div class="recent"><h3>${t("recent")}</h3>${S.chats.map(c =>
          `<a href="#/c/${c.id}/board"><span>${esc(c.name)}</span><small>${c.message_count} ${t("messages")}</small></a>`).join("")}</div>` : ""}
      </div>
    </div>
  </section>`;

  const drop = $("#drop"), file = $("#file");
  drop.onclick = () => file.click();
  drop.onkeydown = e => (e.key === "Enter" || e.key === " ") && file.click();
  drop.ondragover = e => { e.preventDefault(); drop.classList.add("over"); };
  drop.ondragleave = () => drop.classList.remove("over");
  drop.ondrop = e => { e.preventDefault(); drop.classList.remove("over"); if (e.dataTransfer.files[0]) upload(e.dataTransfer.files[0]); };
  file.onchange = () => file.files[0] && upload(file.files[0]);
  app.querySelectorAll("[data-demo]").forEach(b => (b.onclick = async () => {
    b.disabled = true;
    try { openChat(await post(`/api/demo/${b.dataset.demo}`)); }
    catch (e) { toast(e.message); b.disabled = false; }
  }));
}

async function upload(f) {
  const units = $("#units").value;
  const name = $("#gname").value;
  const qs = new URLSearchParams({ filename: f.name, units, name });
  $("#drop").innerHTML = `<span class="spinner"></span>`;
  try { openChat(await post(`/api/chats?${qs}`, await f.arrayBuffer())); }
  catch (e) { toast(e.message, 5000); renderHome(); }
}

async function openChat(chat) {
  await post(`/api/chats/${chat.id}/analyze`);
  location.hash = `#/c/${chat.id}/board`;
}

// ---------------------------------------------------------------- chat page shell
async function loadBoard(chatId) {
  S.board = await api(`/api/chats/${chatId}/board`);
  return S.board;
}

function shell(view) {
  const b = S.board, c = b.chat;
  const missedCount = Object.values(b.missed).reduce((n, l) => n + l.length, 0);
  const range = c.first_ts ? `${fmtDate(c.first_ts, false)} – ${fmtDate(c.last_ts, false)}` : "";
  return `
  <div class="page-head">
    <h2>${esc(c.name)}</h2>
    <span class="meta">${c.message_count} ${t("messages")} · ${range} · ${b.members.length} 👥</span>
    <div class="actions">
      <button class="ghost small" id="btn-add-export">⤓ ${t("add_export")}</button>
      <button class="ghost small" id="btn-reanalyze">↻ ${t("reanalyze")}</button>
      <button class="ghost small danger" id="btn-delete">${t("delete_chat")}</button>
      <input type="file" id="file2" accept=".txt,.zip" hidden>
    </div>
  </div>
  <nav class="tabs">
    <a href="#/c/${c.id}/board" class="${view === "board" ? "active" : ""}">📌 ${t("tab_board")}${missedCount ? `<span class="count">${missedCount}</span>` : ""}</a>
    <a href="#/c/${c.id}/summary" class="${view === "summary" ? "active" : ""}">🗞️ ${t("tab_summary")}</a>
    <a href="#/c/${c.id}/ask" class="${view === "ask" ? "active" : ""}">💬 ${t("tab_ask")}</a>
  </nav>
  <div id="progress-slot">${progressHtml(b.progress)}</div>
  <div id="view"></div>`;
}

function progressHtml(p) {
  if (!p || p.state === "idle" || p.state === "done") return "";
  if (p.state === "error") {
    return `<div class="progress error"><div class="progress-top"><span>⚠️ ${t("analysis_error")}</span>
      <button class="small" id="btn-retry">${t("retry")}</button></div><small>${esc(p.error)}</small></div>`;
  }
  const pct = p.total ? Math.round((p.done / p.total) * 100) : 0;
  const found = I18N[lang].found;
  return `<div class="progress">
    <div class="progress-top"><span><span class="spinner"></span> ${p.state === "queued" ? t("queued") : t("analyzing")}</span>
    <span class="muted">${p.done}/${p.total} ${t("part")}</span></div>
    <div class="bar"><div style="width:${pct}%"></div></div>
    <div class="feed">${(p.found || []).slice().reverse().map(f => `<span>${f.kind === "update" ? "↻" : "＋"} ${esc(found[f.kind] || f.kind)}: ${esc(f.text)}</span>`).join("")}</div>
  </div>`;
}

function bindShell() {
  const id = S.board.chat.id;
  const f2 = $("#file2");
  $("#btn-add-export").onclick = () => f2.click();
  f2.onchange = async () => {
    if (!f2.files[0]) return;
    try {
      const r = await post(`/api/chats/${id}/import`, await f2.files[0].arrayBuffer());
      toast(r.added ? t("added_msgs")(r.added) : t("no_new"));
      startPolling(id);
    } catch (e) { toast(e.message); }
  };
  $("#btn-reanalyze").onclick = async () => { await post(`/api/chats/${id}/analyze?reset=true`); startPolling(id); render(); };
  $("#btn-delete").onclick = async () => {
    if (!confirm(t("confirm_delete"))) return;
    await api(`/api/chats/${id}`, { method: "DELETE" });
    location.hash = "#/";
  };
  const retry = $("#btn-retry");
  if (retry) retry.onclick = async () => { await post(`/api/chats/${id}/analyze`); startPolling(id); };
}

// ---------------------------------------------------------------- board view
function dueChip(item, today) {
  if (!item.due) return `<span class="chip none">📅 ${t("no_due")}</span>`;
  const soon = new Date(today + "T12:00:00"); soon.setDate(soon.getDate() + 3);
  const cls = item.status === "done" ? "" : item.due < today ? "overdue" : item.due <= soon.toISOString().slice(0, 10) ? "soon" : "";
  return `<span class="chip ${cls}">📅 ${fmtDate(item.due)}</span>`;
}

function card(task, today) {
  return `<div class="card ${task.status === "done" ? "done" : ""}" data-id="${task.id}">
    <div class="card-top">
      <input type="checkbox" data-toggle="${task.id}" ${task.status === "done" ? "checked" : ""} aria-label="done">
      <span class="card-title" data-edit="${task.id}">${esc(task.title)}</span>
    </div>
    <div class="card-meta">
      ${task.owner ? `<span class="chip">${avatar(task.owner)}${esc(firstName(task.owner))}</span>` : `<span class="chip none">🙋 ${t("no_owner")}</span>`}
      ${dueChip(task, today)}
      ${task.source_idx != null ? `<button class="src" data-src="${task.source_idx}" title="${t("source")}">💬</button>` : ""}
    </div>
  </div>`;
}

function renderBoardView() {
  const b = S.board;
  const units = [...b.chat.units];
  let tasks = b.tasks.filter(x => (S.showDone || x.status !== "done") && (!S.member || x.owner === S.member));
  if (tasks.some(x => !x.unit || !units.includes(x.unit))) units.push("");
  const cols = units.map(u => {
    const list = tasks.filter(x => (u ? x.unit === u : !x.unit || !b.chat.units.includes(x.unit)));
    return `<div class="column">
      <div class="column-head"><span>${esc(u || t("no_unit"))} <span class="n">${list.length}</span></span>
        <button data-add="${esc(u)}" title="${t("add_task")}">＋</button></div>
      ${list.map(x => card(x, b.today)).join("") || `<div class="empty">—</div>`}
    </div>`;
  }).join("");

  const m = b.missed;
  const miss = (title, list, fmt) => list.length ? `<h4>${title} (${list.length})</h4><ul class="list">${list.map(fmt).join("")}</ul>` : "";
  const srcBtn = i => i.source_idx != null ? `<button class="src" data-src="${i.source_idx}" title="${t("source")}">💬</button>` : "";
  const taskLi = i => `<li><span class="grow"><a href="javascript:void 0" data-edit="${i.id}">${esc(i.title)}</a>
    <small>${i.owner ? esc(firstName(i.owner)) : t("no_owner")}${i.due ? " · " + fmtDate(i.due) : ""}</small></span>${srcBtn(i)}</li>`;
  const missedHtml = miss(t("m_questions"), m.questions, q => `<li><span class="grow">${esc(q.title)}
      <small>${t("asked_by")} ${esc(firstName(q.owner)) || "?"}</small></span>${srcBtn(q)}</li>`)
    + miss(t("m_orphans"), m.orphans, taskLi) + miss(t("m_overdue"), m.overdue, taskLi) + miss(t("m_soon"), m.soon, taskLi);

  $("#view").innerHTML = `
  <div class="filters">
    <select id="member"><option value="">👥 ${t("everyone")}</option>${b.members.map(n =>
      `<option ${n === S.member ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>
    <label><input type="checkbox" id="showdone" ${S.showDone ? "checked" : ""}> ${t("show_done")}</label>
    ${S.member ? `<button class="small" id="copy-member">📋 ${t("copy_member")(firstName(S.member))}</button>` : ""}
  </div>
  <div class="layout">
    <div class="columns">${cols}</div>
    <aside class="side">
      <div class="panel missed"><h3>⚠️ ${t("missed")}</h3>${missedHtml || `<p class="muted">${t("nothing_missed")}</p>`}</div>
      <div class="panel"><h3>📅 ${t("events")}</h3>${b.events.length ? `<ul class="list">${b.events.map(e =>
        `<li><span class="grow"><b>${esc(e.title)}</b><small>${fmtDate(e.due)}${e.time ? " · " + esc(e.time) : ""}${e.place ? " · " + esc(e.place) : ""}</small></span>${srcBtn(e)}</li>`).join("")}</ul>`
        : `<p class="muted">${t("none_yet")}</p>`}</div>
      <div class="panel"><h3>🧭 ${t("decisions")}</h3>${b.decisions.length ? `<ul class="list">${b.decisions.map(d =>
        `<li><span class="grow">${esc(d.title)}</span>${srcBtn(d)}</li>`).join("")}</ul>` : `<p class="muted">${t("none_yet")}</p>`}</div>
    </aside>
  </div>`;

  $("#member").onchange = e => { S.member = e.target.value; renderBoardView(); };
  const cm = $("#copy-member");
  if (cm) cm.onclick = () => copyText(memberMessage(S.member));
  $("#showdone").onchange = e => { S.showDone = e.target.checked; renderBoardView(); };
  const view = $("#view");
  view.querySelectorAll("[data-toggle]").forEach(el => (el.onchange = async () => {
    await patch(`/api/items/${el.dataset.toggle}`, { status: el.checked ? "done" : "open" });
    await reloadBoard();
  }));
  view.querySelectorAll("[data-edit]").forEach(el => (el.onclick = () => editTask(b.tasks.find(x => x.id === Number(el.dataset.edit)))));
  view.querySelectorAll("[data-add]").forEach(el => (el.onclick = () => editTask({ unit: el.dataset.add || null })));
  view.querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
}

async function reloadBoard() {
  const { chatId, view } = route();
  await loadBoard(chatId);
  $("#progress-slot").innerHTML = progressHtml(S.board.progress);
  bindShell();
  if (view === "board") renderBoardView();
}

// ---------------------------------------------------------------- modals
function modal(html, bind) {
  const m = $("#modal");
  m.innerHTML = `<div class="modal-box" role="dialog" aria-modal="true">${html}</div>`;
  m.hidden = false;
  const close = () => { m.hidden = true; m.innerHTML = ""; document.removeEventListener("keydown", onKey); };
  const onKey = e => e.key === "Escape" && close();
  document.addEventListener("keydown", onKey);
  m.onclick = e => e.target === m && close();
  m.querySelectorAll("[data-close]").forEach(b => (b.onclick = close));
  bind?.(m, close);
}

function editTask(task) {
  if (!task) return;
  const b = S.board, isNew = !task.id;
  const opt = (v, label, sel) => `<option value="${esc(v)}" ${v === sel ? "selected" : ""}>${esc(label)}</option>`;
  modal(`
    <h3>${isNew ? t("add_task") : t("edit_task")}</h3>
    <label>${t("f_title")}</label><input type="text" id="e-title" value="${esc(task.title || "")}">
    <div class="grid2">
      <div><label>${t("f_owner")}</label><select id="e-owner">${opt("", "—", task.owner || "")}
        ${b.members.map(n => opt(n, n, task.owner)).join("")}
        ${task.owner && !b.members.includes(task.owner) ? opt(task.owner, task.owner, task.owner) : ""}</select></div>
      <div><label>${t("f_due")}</label><input type="date" id="e-due" value="${esc(task.due || "")}"></div>
      <div><label>${t("f_unit")}</label><select id="e-unit">${opt("", "—", task.unit || "")}${b.chat.units.map(u => opt(u, u, task.unit)).join("")}</select></div>
      <div><label>${t("f_status")}</label><select id="e-status">${opt("open", t("st_open"), task.status || "open")}${opt("done", t("st_done"), task.status)}</select></div>
    </div>
    ${task.source_idx != null ? `<p><button class="ghost small" id="e-src">💬 ${t("source")}</button></p>` : ""}
    <div class="modal-actions">
      ${isNew ? "" : `<button class="danger ghost left" id="e-del">${t("del")}</button>`}
      <button data-close>${t("cancel")}</button>
      <button class="primary" id="e-save">${t("save")}</button>
    </div>`, (m, close) => {
    m.querySelector("#e-title").focus();
    const src = m.querySelector("#e-src");
    if (src) src.onclick = () => showSource(task.source_idx);
    const del = m.querySelector("#e-del");
    if (del) del.onclick = async () => { await api(`/api/items/${task.id}`, { method: "DELETE" }); close(); reloadBoard(); };
    m.querySelector("#e-save").onclick = async () => {
      const body = {
        title: m.querySelector("#e-title").value.trim(), owner: m.querySelector("#e-owner").value,
        due: m.querySelector("#e-due").value, unit: m.querySelector("#e-unit").value, status: m.querySelector("#e-status").value,
      };
      if (!body.title) return;
      try {
        if (isNew) {
          const created = await post(`/api/chats/${b.chat.id}/items`, { kind: "task", ...body });
          if (body.status === "done") await patch(`/api/items/${created.id}`, { status: "done" });
        } else await patch(`/api/items/${task.id}`, body);
        close();
        reloadBoard();
      } catch (e) { toast(e.message); }
    };
  });
}

async function showSource(idx) {
  const msgs = await api(`/api/chats/${S.board.chat.id}/messages?around=${idx}&radius=4`);
  modal(`<h3>${t("source_title")}</h3>
    <div class="transcript">${msgs.map(m => m.kind === "system"
      ? `<div class="msg system">${esc(m.text)}</div>`
      : `<div class="msg ${m.idx === idx ? "hl" : ""}" ${m.idx === idx ? 'id="hl"' : ""}>
          <span class="who" style="color:hsl(${hue(m.sender)} 55% 42%)">${esc(m.sender)}</span><span class="when">${fmtTs(m.ts)}</span>
          <div class="body">${m.kind === "media" ? "🖼️ <i>media</i>" : esc(m.text)}</div></div>`).join("")}</div>
    <div class="modal-actions"><button data-close>${t("close")}</button></div>`);
  $("#hl")?.scrollIntoView({ block: "center" });
}

// ---------------------------------------------------------------- summary view
function renderSummaryView() {
  const id = S.board.chat.id;
  const cached = S.summary && S.summary.chatId === id ? S.summary : null;
  $("#view").innerHTML = `<div class="narrow">
    <p class="muted">${t("summary_intro")}</p>
    <div class="row-actions"><button class="primary" id="btn-sum">🗞️ ${t("summary_btn")}</button>
      ${cached ? `<button id="btn-copy">📋 ${t("copy")}</button>` : ""}</div>
    <div id="sum-out">${cached ? `<div class="wa"><div class="bubble mine">${waFormat(cached.text)}</div></div>` : ""}</div>
  </div>`;
  $("#btn-sum").onclick = async e => {
    e.target.disabled = true;
    $("#sum-out").innerHTML = `<p class="muted"><span class="spinner"></span> ${t("summary_wait")}</p>`;
    try {
      const r = await post(`/api/chats/${id}/summary`, { days: 7 });
      S.summary = { chatId: id, text: r.text };
      renderSummaryView();
    } catch (err) { $("#sum-out").innerHTML = `<p class="muted">⚠️ ${esc(err.message)}</p>`; e.target.disabled = false; }
  };
  const copy = $("#btn-copy");
  if (copy) copy.onclick = () => copyText(cached.text);
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); }
  catch {
    const ta = document.createElement("textarea"); ta.value = text; document.body.append(ta); ta.select();
    document.execCommand("copy"); ta.remove();
  }
  toast(t("copied"));
}

// A personal to-do list the club lead can DM to one member.
function memberMessage(name) {
  const b = S.board;
  const mine = b.tasks.filter(x => x.owner === name && x.status === "open")
    .sort((a, c) => (a.due || "9999").localeCompare(c.due || "9999"));
  const lines = mine.map(x => `• ${x.title}${x.due ? ` (📅 ${fmtDate(x.due)})` : ""}`);
  return [t("member_msg_head")(firstName(name)), "", ...(lines.length ? lines : [t("member_msg_empty")]), "", `_${b.chat.name} · Pano_`].join("\n");
}

// WhatsApp markup preview: *bold* and _italic_
function waFormat(text) {
  return esc(text).replace(/\*([^*\n]+)\*/g, "<b>$1</b>").replace(/(^|\s)_([^_\n]+)_/g, "$1<i>$2</i>");
}

// ---------------------------------------------------------------- ask view
function renderAskView() {
  const id = S.board.chat.id;
  const a = S.answer && S.answer.chatId === id ? S.answer : null;
  $("#view").innerHTML = `<div class="narrow">
    <p class="muted">${t("ask_intro")}</p>
    <form class="ask-form" id="ask-form"><input type="text" id="q" placeholder="${esc(t("ask_ph"))}" value="${esc(a?.question || "")}" autocomplete="off">
      <button class="primary">${t("ask_btn")}</button></form>
    <div class="suggest">${t("suggestions").map(s => `<button type="button" data-q="${esc(s)}">${esc(s)}</button>`).join("")}</div>
    <div id="answer" class="answer">${a ? answerHtml(a) : ""}</div>
  </div>`;
  const ask = async question => {
    if (!question.trim()) return;
    $("#answer").innerHTML = `<p class="muted"><span class="spinner"></span> ${t("ask_wait")}</p>`;
    try {
      const r = await post(`/api/chats/${id}/ask`, { question });
      S.answer = { chatId: id, question, ...r };
      $("#answer").innerHTML = answerHtml(S.answer);
      bindAnswer();
    } catch (e) { $("#answer").innerHTML = `<p class="muted">⚠️ ${esc(e.message)}</p>`; }
  };
  $("#ask-form").onsubmit = e => { e.preventDefault(); ask($("#q").value); };
  $("#view").querySelectorAll("[data-q]").forEach(b => (b.onclick = () => { $("#q").value = b.dataset.q; ask(b.dataset.q); }));
  bindAnswer();
  $("#q").focus();
}

function answerHtml(a) {
  return `<div class="wa">
    <div class="bubble mine" style="max-width:420px">${esc(a.question)}</div>
    <div class="bubble" style="margin-top:8px">${esc(a.answer).replace(/\[?#(\d+)\]?/g, '<a href="javascript:void 0" data-src="$1">[#$1]</a>')}</div>
  </div>
  ${a.sources.length ? `<h4 class="muted">${t("sources")}</h4><div class="transcript">${a.sources.map(m =>
    `<div class="msg"><span class="who" style="color:hsl(${hue(m.sender)} 55% 42%)">${esc(m.sender)}</span><span class="when">${fmtTs(m.ts)}</span>
      <a href="javascript:void 0" data-src="${m.idx}" class="when">#${m.idx}</a><div class="body">${esc(m.text)}</div></div>`).join("")}</div>` : ""}`;
}
function bindAnswer() {
  $("#answer")?.querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
}

// ---------------------------------------------------------------- render & polling
function startPolling(chatId) {
  clearInterval(S.poll);
  S.poll = setInterval(async () => {
    if (route().chatId !== chatId) return clearInterval(S.poll);
    const p = await api(`/api/chats/${chatId}/progress`).catch(() => null);
    const running = p && (p.state === "running" || p.state === "queued");
    await reloadBoard();
    if (!running) clearInterval(S.poll);
  }, 1500);
}

async function render() {
  const { chatId, view } = route();
  clearInterval(S.poll);
  await refreshChats();
  if (!chatId) return renderHome();
  try { await loadBoard(chatId); }
  catch { location.hash = "#/"; return; }
  $("#app").innerHTML = `<section class="page">${shell(view)}</section>`;
  bindShell();
  ({ board: renderBoardView, summary: renderSummaryView, ask: renderAskView }[view] || renderBoardView)();
  if (["running", "queued"].includes(S.board.progress.state)) startPolling(chatId);
}

$("#lang").onclick = () => {
  lang = lang === "tr" ? "en" : "tr";
  try { localStorage.setItem("pano.lang", lang); } catch {}
  document.documentElement.lang = lang;
  $("#lang").textContent = lang === "tr" ? "EN" : "TR";
  refreshHealth();
  render();
};
$("#lang").textContent = lang === "tr" ? "EN" : "TR";
document.documentElement.lang = lang;
window.addEventListener("hashchange", render);
refreshHealth();
setInterval(refreshHealth, 15000);
render();
