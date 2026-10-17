"use strict";

// ---------------------------------------------------------------- i18n
const I18N = {
  tr: {
    eyebrow: "🔒 Gemma 4 · tamamen yerel · açık kaynak",
    hero_h1: ["Kulübünüzün WhatsApp grubu,", "tek bakışta düzenli bir pano."],
    hero_lead: "Görevler mesajların arasında kayboluyor, etkinlik tarihi iki kez değişiyor, \"sponsor dosyası kimde?\" sorusu iki hafta cevapsız kalıyor. Pano sohbeti bu bilgisayarda okur ve kulübe neyin nerede olduğunu geri verir.",
    cta_demo: "✨ Demo kulübü aç", cta_upload: "Kendi grubumu yükle",
    trust: ["📴 İnternetsiz çalışır", "💸 API anahtarı yok", "🧾 Her kart kaynak mesajına bağlı"],
    mock_chat: [["Elif", "Salon dilekçesini kim verir?"], ["Deniz", "Ben perşembe veririm"], ["Mert", "Ahmet Bey 24'ünde yok, 31 Ekim olur diyor"], ["Elif", "Tamam karar: söyleşi 31 Ekim 14:00", true]],
    mock_cards: [["Salon dilekçesi", "Deniz", "Per 8 Eki"], ["Söyleşi → 31 Eki", "Etkinlik", "taşındı"], ["Projeksiyon dilekçesi", "sahibi yok", "⚠️"]],
    feat: [
      ["🗂️", "Birim bazlı pano", "Her görev sorumlusu, son tarihi ve geldiği mesajla birlikte doğru birimin sütununda."],
      ["⚠️", "Gözden kaçanlar", "Cevapsız sorular, kimsenin üstlenmediği işler, geciken ve yaklaşan tarihler."],
      ["🧭", "Etkinlik planlayıcı", "\"3 hafta sonra 200 kişilik etkinlik\" deyin; Gemma birimlere bölünmüş, tarihli bir plan önersin."],
      ["🗞️", "WhatsApp'a geri dön", "Haftalık özeti ve kişiye özel görev listesini tek tıkla gruba yapıştırın."],
    ],
    why_title: "Neden açık model, neden yerel?",
    why_sub: "Bir kulüp sohbetinde onlarca öğrencinin telefon numarası ve özel mesajı var.",
    why: [["0", "mesaj buluta gider", "Gemma 4, Ollama ile bu laptopta çalışır. Sunucu sadece 127.0.0.1'i dinler."], ["₺0", "kullanım ücreti", "Kulüplerin bütçesi yok. İstediğiniz kadar yeniden analiz edin."], ["1", "satırla model değişir", "PANO_MODEL ile istediğiniz açık modeli takın; kimsenin fiyatına kilitlenmezsiniz."]],
    tab_overview: "Kulüp durumu", tab_plan: "Etkinlik planla",
    k_open: "Açık görev", k_done: "tamamlandı", k_missed: "Gözden kaçan", k_missed_sub: "soru + sahipsiz iş", k_decisions: "Alınan karar", k_next: "Sıradaki etkinlik", k_days: d => d === 0 ? "bugün" : `${d} gün kaldı`, k_none: "—",
    units_title: "Birimlerin durumu", h_ok: "Yolunda", h_warn: "Dikkat", h_bad: "Gecikme var", h_idle: "Boş",
    n_open: "açık", n_done: "bitti", n_late: "gecikmiş", n_orphan: "sahipsiz",
    alerts_title: "Riskler ve uyarılar", no_alerts: "Şimdilik risk görünmüyor 🎉",
    a_event: a => `<b>${a.event}</b> etkinliğine ${a.days} gün kaldı`, a_event_sub: a => `${a.open} açık iş${a.orphans ? `, ${a.orphans} tanesinin sahibi yok` : ""}`,
    a_overdue: a => `<b>${a.title}</b> gecikti`, a_overdue_sub: a => `${a.owner ? a.owner.split(" ")[0] : "sahibi yok"} · ${a.due}`,
    a_question: a => `Cevapsız: <b>${a.title}</b>`, a_question_sub: a => `soran ${a.owner ? a.owner.split(" ")[0] : "?"}`,
    a_load: a => `<b>${a.owner.split(" ")[0]}</b> üzerinde ${a.open} açık iş var`, a_load_sub: () => "iş yükünü dağıtmayı düşünün",
    load_title: "Kimin elinde ne var?", l_open: "açık", l_done: "biten",
    timeline_title: "Yaklaşan tarihler", recent_decisions: "Son kararlar",
    plan_intro: "Etkinliği tarif edin. Gemma, kulübün birimlerini ve üyelerin mevcut iş yükünü dikkate alarak tarihli bir hazırlık planı önerir. Hiçbir şey siz onaylamadan panoya eklenmez.",
    plan_ph: "Örn: 14 Kasım'da 200 kişilik bir siber güvenlik zirvesi yapmak istiyoruz, iki konuşmacı ve bir sponsor hedefliyoruz.",
    plan_btn: "🧭 Plan öner", plan_wait: "Gemma planı hazırlıyor…", plan_add: n => `Seçili ${n} görevi panoya ekle`, plan_added: n => `${n} görev panoya eklendi`,
    plan_examples: ["3 hafta sonra 150 kişilik bir yapay zeka söyleşisi", "Kasım sonunda 24 saatlik bir hackathon", "Gelecek ay yeni üyeler için tanışma etkinliği"],
    suggested: "öneri",
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
    tab_board: "Pano", tab_review: "AI incelemesi", review_intro: "Gemma bunları öneriyor. Onaylamadıkların panoya girmez.", review_empty: "İncelenecek öneri yok.", pv_title: "İçe aktarma ön izlemesi", pv_msgs: "mesaj", pv_senders: "gönderen", pv_skipped: n => `${n} satır ayrıştırılamadı ve atlanacak`, pv_dup: n => `Bu dosya daha önce içe aktarıldı (“${n}”). Yine de eklemek istiyor musun?`, pv_go: "İçe aktar", approve: "Onayla", no_source: "kaynak bulunamadı", date_unclear: "tarih belirsiz", reject: "Reddet", edit: "Düzenle", k_task: "Görev", k_question: "Soru", k_decision: "Karar", k_event: "Etkinlik", tab_summary: "Haftalık özet", tab_ask: "Sohbete sor",
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
    eyebrow: "🔒 Gemma 4 · fully local · open source",
    hero_h1: ["Your club's WhatsApp group,", "as one clear board."],
    hero_lead: "Tasks get lost between messages, the event date changes twice, and \"who has the sponsor file?\" goes unanswered for two weeks. Pano reads the chat on this computer and gives your club back what's where.",
    cta_demo: "✨ Open the demo club", cta_upload: "Upload my group",
    trust: ["📴 Works offline", "💸 No API keys", "🧾 Every card links to its source message"],
    mock_chat: [["Maya", "Who can book the lab?"], ["Leo", "I'll book it today"], ["Noah", "They moved our booth to Oct 30"], ["Maya", "Decision: booth on Friday Oct 30", true]],
    mock_cards: [["Book the lab", "Leo", "Thu 8 Oct"], ["Fair → Oct 30", "Events", "moved"], ["Print the banner", "no owner", "⚠️"]],
    feat: [
      ["🗂️", "A board per team", "Every task with its owner, due date and the message it came from, in the right team's column."],
      ["⚠️", "Slipping through", "Unanswered questions, work nobody took, overdue and due-soon tasks."],
      ["🧭", "Event planner", "Say \"a 200-person event in 3 weeks\" and Gemma proposes a dated plan split across your teams."],
      ["🗞️", "Back to WhatsApp", "Paste a weekly recap or a personal to-do list into the group in one click."],
    ],
    why_title: "Why an open model, and why local?",
    why_sub: "A club chat holds dozens of students' phone numbers and private messages.",
    why: [["0", "messages sent to a cloud", "Gemma 4 runs on this laptop via Ollama. The server only listens on 127.0.0.1."], ["$0", "per-use cost", "Clubs have no budget. Re-analyse as often as you like."], ["1", "line to swap the model", "Plug any open model in with PANO_MODEL. No vendor lock-in."]],
    tab_overview: "Club status", tab_plan: "Plan an event",
    k_open: "Open tasks", k_done: "done", k_missed: "Slipping through", k_missed_sub: "questions + unowned work", k_decisions: "Decisions", k_next: "Next event", k_days: d => d === 0 ? "today" : `in ${d} days`, k_none: "—",
    units_title: "Team status", h_ok: "On track", h_warn: "Watch", h_bad: "Overdue", h_idle: "Empty",
    n_open: "open", n_done: "done", n_late: "late", n_orphan: "unowned",
    alerts_title: "Risks and alerts", no_alerts: "No risks right now 🎉",
    a_event: a => `<b>${a.event}</b> is in ${a.days} days`, a_event_sub: a => `${a.open} open tasks${a.orphans ? `, ${a.orphans} with no owner` : ""}`,
    a_overdue: a => `<b>${a.title}</b> is overdue`, a_overdue_sub: a => `${a.owner ? a.owner.split(" ")[0] : "no owner"} · ${a.due}`,
    a_question: a => `Unanswered: <b>${a.title}</b>`, a_question_sub: a => `asked by ${a.owner ? a.owner.split(" ")[0] : "?"}`,
    a_load: a => `<b>${a.owner.split(" ")[0]}</b> has ${a.open} open tasks`, a_load_sub: () => "consider spreading the load",
    load_title: "Who's carrying what?", l_open: "open", l_done: "done",
    timeline_title: "Coming up", recent_decisions: "Latest decisions",
    plan_intro: "Describe the event. Gemma proposes a dated preparation plan using your teams and each member's current load. Nothing goes on the board until you approve it.",
    plan_ph: "e.g. We want a 200-person cybersecurity summit on Nov 14 with two speakers and one sponsor.",
    plan_btn: "🧭 Propose a plan", plan_wait: "Gemma is drafting the plan…", plan_add: n => `Add ${n} selected tasks to the board`, plan_added: n => `${n} tasks added to the board`,
    plan_examples: ["A 150-person AI talk in 3 weeks", "A 24-hour hackathon at the end of November", "A welcome event for new members next month"],
    suggested: "suggested",
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
    tab_board: "Board", tab_review: "AI review", review_intro: "Gemma suggests these. Anything you do not approve stays off the board.", review_empty: "Nothing to review.", pv_title: "Import preview", pv_msgs: "messages", pv_senders: "senders", pv_skipped: n => `${n} lines could not be parsed and will be skipped`, pv_dup: n => `This file was already imported (“${n}”). Add it anyway?`, pv_go: "Import", approve: "Approve", no_source: "source not found", date_unclear: "date unclear", reject: "Reject", edit: "Edit", k_task: "Task", k_question: "Question", k_decision: "Decision", k_event: "Event", tab_summary: "Weekly recap", tab_ask: "Ask the chat",
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
const S = { chats: [], board: null, health: null, member: "", showDone: true, poll: null, summary: null, answer: null };

function route() {
  const [, kind, id, view] = location.hash.split("/");
  return kind === "c" ? { chatId: Number(id), view: view || "overview" } : { chatId: null, view: "home" };
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
    location.hash = e.target.value === "new" ? "#/" : `#/c/${e.target.value}/overview`;
  };
}

// ---------------------------------------------------------------- home
function renderHome() {
  const app = $("#app");
  const h1 = t("hero_h1");
  app.innerHTML = `
  <section class="home">
    <div class="hero">
      <div>
        <span class="eyebrow">${t("eyebrow")}</span>
        <h1>${h1[0]}<br><span class="grad">${h1[1]}</span></h1>
        <p class="lead">${t("hero_lead")}</p>
        <div class="hero-cta">
          <button class="primary big" data-demo="${lang}">${t("cta_demo")}</button>
          <button class="big" id="go-upload">${t("cta_upload")}</button>
        </div>
        <div class="trust">${t("trust").map(s => `<span>${s}</span>`).join("")}</div>
      </div>
      <div class="mock" aria-hidden="true">
        <div class="phone"><div class="hd">💬 WhatsApp</div>${t("mock_chat").map(([w, m, me]) =>
          `<div class="b ${me ? "me" : ""}"><b style="color:hsl(${hue(w)} 55% 42%)">${w}</b>${m}</div>`).join("")}</div>
        <div class="arrow">✨</div>
        <div class="board"><div class="hd"><span>📌 Pano</span><span class="muted">Gemma 4</span></div>${t("mock_cards").map(([ti, o, d], i) =>
          `<div class="mc"><b>${ti}</b><div class="m"><span class="chip ${i === 2 ? "none" : ""}">${o}</span><span class="chip ${i === 2 ? "overdue" : i === 1 ? "ai" : ""}">${d}</span></div></div>`).join("")}</div>
      </div>
    </div>
    <div class="features">${t("feat").map(([ic, h, p]) =>
      `<div class="feature"><div class="ic">${ic}</div><h4>${h}</h4><p>${p}</p></div>`).join("")}</div>
    <h2 class="section-title" id="upload-title">${t("drop")}</h2>
    <p class="section-sub">${t("drop_hint")}</p>
    <div class="upload">
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
          `<a href="#/c/${c.id}/overview"><span>${esc(c.name)}</span><small>${c.message_count} ${t("messages")}</small></a>`).join("")}</div>` : ""}
      </div>
    </div>
    <h2 class="section-title">${t("why_title")}</h2>
    <p class="section-sub">${t("why_sub")}</p>
    <div class="why">${t("why").map(([n, l, p]) => `<div class="panel"><b>${n}</b><h3>${l}</h3><p class="muted" style="margin:0">${p}</p></div>`).join("")}</div>
  </section>`;
  $("#go-upload").onclick = () => $("#upload-title").scrollIntoView({ behavior: "smooth" });

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
  const buf = await f.arrayBuffer();
  let pv;
  try { pv = await post("/api/preview", buf); }
  catch (e) { toast(e.message, 5000); return; }
  modal(`<h3>${t("pv_title")}</h3>
    <p><b>${esc(f.name)}</b><br>💬 ${pv.messages} ${t("pv_msgs")} · 📅 ${fmtDate(pv.first_ts, false)} – ${fmtDate(pv.last_ts, false)} · 👥 ${pv.senders.length} ${t("pv_senders")}</p>
    <p class="muted">${pv.senders.map(esc).join(", ")}</p>
    ${pv.skipped_lines ? `<p>⚠️ ${t("pv_skipped")(pv.skipped_lines)}</p>` : ""}
    ${pv.duplicate_of ? `<p>⚠️ ${t("pv_dup")(esc(pv.duplicate_of.name))}</p>` : ""}
    <div class="modal-actions"><button data-close>${t("cancel")}</button><button class="primary" id="pv-go">${t("pv_go")}</button></div>`,
  (m, close) => {
    m.querySelector("#pv-go").onclick = async () => {
      close();
      $("#drop").innerHTML = `<span class="spinner"></span>`;
      try { openChat(await post(`/api/chats?${qs}`, buf)); }
      catch (e) { toast(e.message, 5000); renderHome(); }
    };
  });
}

async function openChat(chat) {
  if (chat.status !== "ready") await post(`/api/chats/${chat.id}/analyze`);
  location.hash = `#/c/${chat.id}/overview`;
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
    <div class="club-ic">${esc(c.name.trim()[0] || "P")}</div>
    <div><h2>${esc(c.name)}</h2>
    <span class="meta">💬 ${c.message_count} ${t("messages")} · 📅 ${range} · 👥 ${b.members.length}</span></div>
    <div class="actions">
      <a class="btn ghost small" href="/api/chats/${c.id}/export.md" download="${esc(c.name)}.md">⤓ Markdown</a>
      <button class="ghost small" id="btn-add-export">⤓ ${t("add_export")}</button>
      <button class="ghost small" id="btn-reanalyze">↻ ${t("reanalyze")}</button>
      <button class="ghost small danger" id="btn-delete">${t("delete_chat")}</button>
      <input type="file" id="file2" accept=".txt,.zip" hidden>
    </div>
  </div>
  <nav class="tabs">
    <a href="#/c/${c.id}/overview" class="${view === "overview" ? "active" : ""}">📊 ${t("tab_overview")}</a>
    <a href="#/c/${c.id}/board" class="${view === "board" ? "active" : ""}">📌 ${t("tab_board")}${missedCount ? `<span class="count">${missedCount}</span>` : ""}</a>
    <a href="#/c/${c.id}/review" class="${view === "review" ? "active" : ""}">🔎 ${t("tab_review")}${b.review.length ? `<span class="count">${b.review.length}</span>` : ""}</a>
    <a href="#/c/${c.id}/plan" class="${view === "plan" ? "active" : ""}">🧭 ${t("tab_plan")}<span class="new">AI</span></a>
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
  if (view === "board" || view === "overview" || view === "review") VIEWS[view]();
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
function renderReviewView() {
  const b = S.board;
  const row = i => `<li class="review-row" data-id="${i.id}">
    <span class="grow"><b>${t("k_" + i.kind)}</b> · ${esc(i.title)}${i.needs_review ? ` <span class="chip overdue">⚠️ ${t(i.needs_review === 1 ? "no_source" : "date_unclear")}</span>` : ""}
      <small>${i.owner ? esc(firstName(i.owner)) : ""}${i.due ? " · " + fmtDate(i.due) : ""}${i.unit ? " · " + esc(i.unit) : ""}</small></span>
    ${i.source_idx != null ? `<button class="src" data-src="${i.source_idx}" title="${t("source")}">💬</button>` : ""}
    <button class="small" data-edit="${i.id}">${t("edit")}</button>
    <button class="small primary" data-ok="${i.id}" ${i.needs_review === 1 ? "disabled" : ""}>${t("approve")}</button>
    <button class="small ghost danger" data-no="${i.id}">${t("reject")}</button></li>`;
  $("#view").innerHTML = `<div class="narrow"><p class="muted">${t("review_intro")}</p>
    ${b.review.length ? `<ul class="list">${b.review.map(row).join("")}</ul>` : `<p class="muted">${t("review_empty")}</p>`}</div>`;
  const view = $("#view");
  const decide = (id, review) => async () => {
    try { await patch(`/api/items/${id}`, { review }); await render(); } catch (e) { toast(e.message); }
  };
  view.querySelectorAll("[data-ok]").forEach(el => (el.onclick = decide(el.dataset.ok, "approved")));
  view.querySelectorAll("[data-no]").forEach(el => (el.onclick = decide(el.dataset.no, "rejected")));
  view.querySelectorAll("[data-edit]").forEach(el => (el.onclick = () => editTask(b.review.find(x => x.id === Number(el.dataset.edit)))));
  view.querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
}

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

// ---------------------------------------------------------------- overview (club status)
function renderOverview() {
  const b = S.board, o = b.overview, k = o.kpi;
  const pct = k.total ? Math.round((k.done / k.total) * 100) : 0;
  const missed = k.questions + k.orphans;
  const escObj = a => Object.fromEntries(Object.entries(a).map(([key, v]) => [key, typeof v === "string" ? esc(v) : v]));
  const alertIc = { event: "📅", overdue: "⏰", question: "❓", load: "🏋️" };
  const maxLoad = Math.max(1, ...o.workload.map(w => w.open + w.done));
  const health = { ok: t("h_ok"), warn: t("h_warn"), bad: t("h_bad"), idle: t("h_idle") };

  $("#view").innerHTML = `
  <div class="kpis">
    <div class="kpi hero-kpi"><div class="lbl">📅 ${t("k_next")}</div>
      <div class="val" style="font-size:22px;margin-top:6px">${k.next_event ? esc(k.next_event.title) : t("k_none")}</div>
      <div class="sub">${k.next_event ? `${fmtDate(k.next_event.date)}${k.next_event.time ? " · " + esc(k.next_event.time) : ""} · <b>${t("k_days")(k.next_event.days)}</b>` : ""}</div></div>
    <div class="kpi"><div class="lbl">${t("k_open")}</div><div class="val">${k.open}</div>
      <div class="sub">${k.done} ${t("k_done")}</div><div class="ring" style="--p:${pct}" data-l="${pct}%"></div></div>
    <div class="kpi ${missed ? "warn" : "ok"}"><div class="lbl">⚠️ ${t("k_missed")}</div><div class="val">${missed}</div><div class="sub">${t("k_missed_sub")}</div></div>
    <div class="kpi"><div class="lbl">🧭 ${t("k_decisions")}</div><div class="val">${k.decisions}</div><div class="sub">&nbsp;</div></div>
    <div class="kpi"><div class="lbl">👥 ${lang === "tr" ? "Aktif üye" : "Active members"}</div><div class="val">${o.workload.length}<span class="muted" style="font-size:16px">/${b.members.length}</span></div><div class="sub">${lang === "tr" ? "görev alan" : "with tasks"}</div></div>
  </div>
  <div class="ov-grid">
    <div class="ov-col">
      <div class="panel"><h3>🗂️ ${t("units_title")}</h3>
        <div class="units">${o.units.map(u => `
          <div class="unit ${u.health}" data-unit="${esc(u.name || "")}">
            <div class="nm"><span>${esc(u.name || t("no_unit"))}</span><span class="st">${health[u.health]}</span></div>
            <div class="mini"><div style="width:${u.total ? Math.round(u.done / u.total * 100) : 0}%"></div></div>
            <div class="nums"><span><b>${u.open}</b> ${t("n_open")}</span><span><b>${u.done}</b> ${t("n_done")}</span>
              ${u.overdue ? `<span style="color:var(--danger)"><b>${u.overdue}</b> ${t("n_late")}</span>` : ""}
              ${u.orphans ? `<span style="color:var(--warn)"><b>${u.orphans}</b> ${t("n_orphan")}</span>` : ""}</div>
          </div>`).join("")}</div>
      </div>
      <div class="panel"><h3>🚨 ${t("alerts_title")}</h3>
        ${o.alerts.length ? `<ul class="alerts">${o.alerts.slice(0, 8).map(a => {
          const e = escObj(a);
          return `<li class="${a.level}"><span class="ic">${alertIc[a.type]}</span><span>${t("a_" + a.type)(e)}<small>${t("a_" + a.type + "_sub")(e)}</small></span></li>`;
        }).join("")}</ul>` : `<p class="muted">${t("no_alerts")}</p>`}
      </div>
    </div>
    <div class="ov-col">
      <div class="panel"><h3>🏋️ ${t("load_title")}</h3>
        ${o.workload.length ? o.workload.map(w => `<div class="load-row"><span class="nm">${avatar(w.name)}${esc(firstName(w.name))}</span>
          <div class="load-bar"><div class="o" style="width:${w.open / maxLoad * 100}%"></div><div class="d" style="width:${w.done / maxLoad * 100}%"></div></div>
          <b>${w.open}</b></div>`).join("") + `<div class="legend"><span><i style="background:var(--brand)"></i>${t("l_open")}</span><span><i style="background:var(--ok)"></i>${t("l_done")}</span></div>`
        : `<p class="muted">${t("none_yet")}</p>`}
      </div>
      <div class="panel"><h3>🗓️ ${t("timeline_title")}</h3>
        ${o.timeline.length ? `<ul class="timeline">${o.timeline.map(r => `<li><span class="d">${fmtDate(r.date, false).replace(" ", "<br>")}</span>
          <span class="pt ${r.kind}"></span><span>${r.kind === "event" ? "<b>" + esc(r.title) + "</b>" : esc(r.title)}<small>${r.owner ? esc(firstName(r.owner)) : r.kind === "event" ? "📅" : t("no_owner")}</small></span></li>`).join("")}</ul>`
        : `<p class="muted">${t("none_yet")}</p>`}
      </div>
      <div class="panel"><h3>🧭 ${t("recent_decisions")}</h3>
        ${b.decisions.length ? `<ul class="list">${b.decisions.slice(-5).reverse().map(d => `<li><span class="grow">${esc(d.title)}</span>${d.source_idx != null ? `<button class="src" data-src="${d.source_idx}">💬</button>` : ""}</li>`).join("")}</ul>` : `<p class="muted">${t("none_yet")}</p>`}
      </div>
    </div>
  </div>`;
  $("#view").querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
  $("#view").querySelectorAll("[data-unit]").forEach(el => (el.onclick = () => { location.hash = `#/c/${b.chat.id}/board`; }));
}

// ---------------------------------------------------------------- AI event planner
function renderPlanView() {
  const id = S.board.chat.id;
  const p = S.plan && S.plan.chatId === id ? S.plan : null;
  $("#view").innerHTML = `<div class="narrow">
    <div class="panel planner-box">
      <h3>🧭 ${t("tab_plan")}</h3>
      <p class="muted" style="margin:0">${t("plan_intro")}</p>
      <textarea id="goal" placeholder="${esc(t("plan_ph"))}">${esc(p?.goal || "")}</textarea>
      <div class="suggest" style="margin:0">${t("plan_examples").map(s => `<button type="button" data-ex="${esc(s)}">${esc(s)}</button>`).join("")}</div>
      <div><button class="primary" id="btn-plan">${t("plan_btn")}</button></div>
    </div>
    <div id="plan-out">${p ? planHtml(p) : ""}</div>
  </div>`;
  $("#view").querySelectorAll("[data-ex]").forEach(b => (b.onclick = () => { $("#goal").value = b.dataset.ex; }));
  $("#btn-plan").onclick = async e => {
    const goal = $("#goal").value.trim();
    if (!goal) return $("#goal").focus();
    e.target.disabled = true;
    $("#plan-out").innerHTML = `<div class="thinking"><span class="spinner"></span> ${t("plan_wait")}</div>`;
    try {
      S.plan = { chatId: id, goal, ...(await post(`/api/chats/${id}/plan`, { goal })) };
      $("#plan-out").innerHTML = planHtml(S.plan);
      bindPlan();
    } catch (err) { $("#plan-out").innerHTML = `<p class="muted">⚠️ ${esc(err.message)}</p>`; }
    e.target.disabled = false;
  };
  bindPlan();
}

function planHtml(p) {
  return `<div class="plan-head"><h3>${esc(p.title)}${p.event_date ? ` · <span class="muted">${fmtDate(p.event_date)}</span>` : ""}</h3>
    <button class="primary" id="btn-accept">${t("plan_add")(p.tasks.length)}</button></div>
    <div class="plan-list">${p.tasks.map((x, i) => `<label class="plan-item" style="margin:0;color:var(--text);font-size:15px;font-weight:400">
      <input type="checkbox" data-i="${i}" checked>
      <div><div class="t">${esc(x.title)}</div>${x.why ? `<div class="why">${esc(x.why)}</div>` : ""}
        <div class="meta">${x.unit ? `<span class="chip">🗂️ ${esc(x.unit)}</span>` : ""}
          ${x.owner ? `<span class="chip ai">${avatar(x.owner)}${esc(firstName(x.owner))} · ${t("suggested")}</span>` : `<span class="chip none">🙋 ${t("no_owner")}</span>`}</div></div>
      <span class="chip">${x.due ? "📅 " + fmtDate(x.due) : t("no_due")}</span></label>`).join("")}</div>`;
}

function bindPlan() {
  const btn = $("#btn-accept");
  if (!btn) return;
  const boxes = () => [...document.querySelectorAll("[data-i]")];
  const sync = () => { btn.textContent = t("plan_add")(boxes().filter(b => b.checked).length); };
  boxes().forEach(b => (b.onchange = sync));
  btn.onclick = async () => {
    const tasks = boxes().filter(b => b.checked).map(b => S.plan.tasks[Number(b.dataset.i)]);
    if (!tasks.length) return;
    btn.disabled = true;
    await post(`/api/chats/${S.board.chat.id}/plan/accept`, { tasks, event_title: S.plan.title, event_date: S.plan.event_date });
    toast(t("plan_added")(tasks.length));
    S.plan = null;
    location.hash = `#/c/${S.board.chat.id}/board`;
  };
}

const VIEWS = { overview: renderOverview, board: renderBoardView, review: renderReviewView, plan: renderPlanView, summary: renderSummaryView, ask: renderAskView };

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
  (VIEWS[view] || renderOverview)();
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
const setThemeIcon = () => ($("#theme").textContent = document.documentElement.dataset.theme === "dark" ? "☀️" : "🌙");
$("#theme").onclick = () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem("pano.theme", next); } catch {}
  setThemeIcon();
};
setThemeIcon();
window.addEventListener("hashchange", render);
refreshHealth();
setInterval(refreshHealth, 15000);
render();
