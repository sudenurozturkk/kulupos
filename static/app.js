"use strict";

// ---------------------------------------------------------------- i18n
const I18N = {
  tr: {
    eyebrow: "Gemma 4 · tamamen yerel · açık kaynak",
    hero_h1: ["Kulübün dağınık işleri,", "tek yerde ve yapay zekâyla düzende."],
    hero_lead: "Toplantıda, etkinlikte, istediğin an görev, karar, etkinlik ve not gir; hepsi bu bilgisayarda kalır. Yerel Gemma yapay zekâsı kulübünü analiz eder: neler yapıldı, neler geride, etkinlik nasıl geçti, sırada ne var. Öğrenciler için ücretsiz. WhatsApp sohbeti yalnızca içe aktarılabilen kaynaklardan biridir.",
    cta_demo: "Demo kulübü aç", demo_timeout: "Sunucu yanıt vermedi. Eski bir KulüpOS süreci açık olabilir; kapatıp `python -m app` ile yeniden başlatın.", cta_upload: "Kendi grubumu yükle",
    trust: ["İnternetsiz çalışır", "API anahtarı yok", "Her kart kaynağına bağlı (mesaj veya not)"],
    mock_chat: [["Elif", "Salon dilekçesini kim verir?"], ["Deniz", "Ben perşembe veririm"], ["Mert", "Ahmet Bey 24'ünde yok, 31 Ekim olur diyor"], ["Elif", "Tamam karar: söyleşi 31 Ekim 14:00", true]],
    mock_cards: [["Salon dilekçesi", "Deniz", "Per 8 Eki"], ["Söyleşi 31 Eki", "Etkinlik", "taşındı"], ["Projeksiyon dilekçesi", "sahibi yok", ""]],
    feat: [
      ["chart", "Panel", "Bugün ilgilenilecekler, riskler, yaklaşan etkinlik ve toplantılar tek bakışta. Haftalık özet ve “sohbete sor” da burada."],
      ["calendar", "Etkinlikler", "Her etkinlik tek sayfada: bağlı görev, karar, soru, toplantı, katılım, geri bildirim ve yalnızca girilen veriden yazılan rapor."],
      ["calendar", "Toplantılar", "Notları yapıştırın ya da .txt/.md yükleyin; görev, karar ve sorular önce incelemeye düşer. Özet yalnızca notlardan ve onaylı kayıtlardan yazılır."],
      ["pin", "Görevler", "Komite bazlı pano ve onay bekleyen AI önerileri (inceleme kuyruğu). Her kayıt geldiği mesaj veya notla birlikte."],
      ["person", "Kişiler ve komiteler", "Görev sahiplerinden türeyen kişi sayfaları (yalnızca sayılar, performans yargısı yok) ve komite üye listeleri."],
      ["transfer", "İçe/Dışa aktar", "WhatsApp dışa aktarımını al, onaylı kayıtları CSV/JSON/Markdown olarak ver. Veri bilgisayardan çıkmaz."],
    ],
    why_title: "Neden açık model, neden yerel?",
    why_sub: "Bir kulüp sohbetinde onlarca öğrencinin telefon numarası ve özel mesajı var.",
    why: [["0", "mesaj buluta gider", "Gemma 4, Ollama ile bu laptopta çalışır. Sunucu sadece 127.0.0.1'i dinler."], ["₺0", "kullanım ücreti", "Kulüplerin bütçesi yok. İstediğiniz kadar yeniden analiz edin."], ["1", "satırla model değişir", "PANO_MODEL ile istediğiniz açık modeli takın; kimsenin fiyatına kilitlenmezsiniz."]],
    tab_overview: "Kulüp durumu", tab_plan: "Etkinlik planla",
    k_open: "Açık görev", k_done: "tamamlandı", k_missed: "Gözden kaçan", k_missed_sub: "soru + sahipsiz iş", k_decisions: "Alınan karar", k_next: "Sıradaki etkinlik", k_days: d => d === 0 ? "bugün" : `${d} gün kaldı`, k_none: "—",
    units_title: "Birimlerin durumu", h_ok: "Yolunda", h_warn: "Dikkat", h_bad: "Gecikme var", h_idle: "Boş",
    n_open: "açık", n_done: "bitti", n_late: "gecikmiş", n_orphan: "sahipsiz",
    alerts_title: "Riskler ve uyarılar", no_alerts: "Şimdilik risk görünmüyor ",
    a_event: a => `<b>${a.event}</b> etkinliğine ${a.days} gün kaldı`, a_event_sub: a => `${a.open} açık iş${a.orphans ? `, ${a.orphans} tanesinin sahibi yok` : ""}`,
    a_overdue: a => `<b>${a.title}</b> gecikti`, a_overdue_sub: a => `${a.owner ? a.owner.split(" ")[0] : "sahibi yok"} · ${a.due}`,
    a_question: a => `Cevapsız: <b>${a.title}</b>`, a_question_sub: a => `soran ${a.owner ? a.owner.split(" ")[0] : "?"}`,
    a_load: a => `<b>${a.owner.split(" ")[0]}</b> üzerinde ${a.open} açık iş var`, a_load_sub: () => "iş yükünü dağıtmayı düşünün",
    load_title: "Kimin elinde ne var?", l_open: "açık", l_done: "biten",
    timeline_title: "Yaklaşan tarihler", recent_decisions: "Son kararlar",
    plan_intro: "Etkinliği tarif edin. Gemma, kulübün birimlerini ve üyelerin mevcut iş yükünü dikkate alarak tarihli bir hazırlık planı önerir. Hiçbir şey siz onaylamadan panoya eklenmez.",
    plan_ph: "Örn: 14 Kasım'da 200 kişilik bir siber güvenlik zirvesi yapmak istiyoruz, iki konuşmacı ve bir sponsor hedefliyoruz.",
    plan_btn: "Plan öner", plan_wait: "Gemma planı hazırlıyor…", plan_add: n => `Seçili ${n} görevi panoya ekle`, plan_added: n => `${n} görev panoya eklendi`,
    plan_examples: ["3 hafta sonra 150 kişilik bir yapay zeka söyleşisi", "Kasım sonunda 24 saatlik bir hackathon", "Gelecek ay yeni üyeler için tanışma etkinliği"],
    suggested: "öneri",
    hero_title: "WhatsApp grubundaki karmaşayı panoya çevirin",
    hero_sub: "Kulübünüzün sohbet dışa aktarımını bırakın. Gemma 4 bu bilgisayarda okur; görevleri, kararları, tarihleri ve cevapsız soruları çıkarır. Hiçbir mesaj internete gitmez.",
    drop: "WhatsApp dışa aktarımını buraya bırakın",
    drop_hint: ".txt ya da .zip · tıklayıp dosya da seçebilirsiniz",
    units_label: "Kulübünüzün birimleri (virgülle ayırın)",
    units_default: "Yönetim, Etkinlik, İletişim, Sponsorluk",
    name_label: "Grup adı (isteğe bağlı)",
    try_demo: "Demo sohbetle dene",
    how_export: "WhatsApp'tan nasıl dışa aktarılır?",
    how_steps: ["Grubu açın, grup adına dokunun", "En alttaki <b>Sohbeti dışa aktar</b>'ı seçin", "<b>Medya olmadan</b> deyin, dosyayı bu bilgisayara gönderin"],
    privacy: "<b>Veri bu bilgisayardan çıkmaz.</b> Model Ollama ile yerelde çalışır; üye numaraları ve mesajlar hiçbir buluta gönderilmez.",
    recent: "Önceki gruplar",
    messages: "mesaj",
    health_ok: "Yerel · Gemma 4 hazır",
    health_nomodel: "Model yok: ollama pull",
    health_down: "Ollama kapalı",
    tab_board: "Pano", tab_review: "AI incelemesi", review_intro: "Gemma bunları öneriyor. Onaylamadıkların panoya girmez.", review_empty: "İncelenecek öneri yok.", pv_title: "İçe aktarma ön izlemesi", pv_msgs: "mesaj", pv_senders: "gönderen", pv_skipped: n => `${n} satır ayrıştırılamadı ve atlanacak`, pv_dup: n => `Bu dosya daha önce içe aktarıldı (“${n}”). Yine de eklemek istiyor musun?`, pv_go: "İçe aktar", changes_title: "Değişiklik önerileri", f_status_l: "durum", f_owner_l: "sorumlu", f_due_l: "tarih", f_time_l: "saat", f_place_l: "yer", units_btn: "Komiteler", units_add: "Yeni komite adı", units_add_btn: "Ekle", unit_members_ph: "Üyeler (virgülle ayır, serbest metin)", units_note: "Silinen komitenin görevleri “Komitesiz” sütununa düşer.", ev_add: "Etkinlik ekle", ev_edit: "Etkinliği düzenle", ev_type: "Tür", ev_date: "Tarih", ev_time: "Saat", ev_place: "Mekân", ev_owner: "Sorumlu",
    ev_units: "Komiteler", ev_phase: "Durum", ev_exp: "Beklenen katılımcı", ev_act: "Gerçekleşen katılımcı", ev_bud_est: "Bütçe tahmini", ev_bud_act: "Gerçekleşen bütçe", ev_apps: "Başvuru sayısı", ev_fb_score: "Geri bildirim puanı (1-5, isteğe bağlı)", ev_fb_note: "Kısa geri bildirim notu",
    tab_analysis: "Etkinlik analizi", an_none: "Girilmedi", an_intro: "Sayılar yalnızca girilen etkinlik verisinden hesaplanır (iptal edilenler dışarıda); Gemma gerekmez. Eksik veri “Girilmedi” yazar.",
    an_total: "Etkinlik", an_avg_att: "Ortalama katılım", an_avg_rate: "Ortalama katılım oranı", an_avg_fb: "Ortalama geri bildirim", an_high: "En yüksek katılım", an_low: "En düşük katılım",
    an_low_need: "Karşılaştırma için en az 2 etkinlikte gerçekleşen katılım gerekir.", an_committee: "Komite bazında etkinlik sayısı", an_committee_note: "Birden fazla komiteli etkinlik her komitede sayılır.", an_no_unit: "Komite girilmedi",
    an_per_event: "Etkinlik başına", an_c_event: "Etkinlik", an_c_rate: "Katılım oranı (gerçekleşen/beklenen)", an_c_conv: "Başvuru katılım", an_c_budget: "Bütçe sapması", an_c_fb: "Geri bildirim",
    an_empty: "Henüz etkinlik yok. Panodan etkinlik ekleyin.", an_insight: "Dönem içgörüsü", an_insight_btn: "Dönem içgörüsü yaz", an_insight_re: "Yeniden yaz",
    an_insight_none: "Henüz içgörü yok. Gemma yalnızca yukarıdaki hesaplanmış sayılardan kısa bir yorum yazar; sayılarda olmayan rakam içeren metin reddedilir.",
    an_wait: "Gemma yerelde yazıyor; bu birkaç dakika sürebilir", an_src_sample: "Örnek veri: önceden hesaplanmış içgörü", an_src_ai: "Gemma yazdı, yalnızca hesaplanan sayılardan", an_stale: "Etkinlik verisi bu içgörüden sonra değişti; yeniden yazın.", an_rejected: "İçgörü reddedildi",
    ev_notes: "Notlar", ev_none: "Etkinlik yok", ev_linked: n => `${n} bağlı iş`, ev_link: "Etkinlik",
    ph: { idea: "Fikir", planning: "Planlanıyor", confirmed: "Kesinleşti", held: "Gerçekleşti", cancelled: "İptal" }, rp_btn: "Rapor", rp_title: "Etkinlik raporu", rp_make: "Gemma ile rapor üret", rp_remake: "Yeniden üret", rp_none: "Henüz rapor yok.",
    rp_wait: "Gemma yerelde yazıyor; bu birkaç dakika sürebilir", rp_elapsed: "geçen süre", rp_stale: "Etkinlik verisi bu rapordan sonra değişti; raporu yeniden üretin.",
    rp_src_sample: "Önceden hesaplanmış örnek rapor (demo verisi)", rp_src_ai: "Gemma tarafından, yalnızca girilen veriden yazıldı", rp_rejected: "Rapor reddedildi",
    rp_figs: "Veride olmayan sayılar", rp_note: "Rapor yalnızca bu etkinlik için girilen alanlardan, bağlı görevlerden ve kararlardan üretilir; boş alanlar “Girilmedi” kalır.",
    rp_copy: "Kopyala", ev_sample: "Örnek etkinlik ekle", c_tasks: "Görevler", c_approved_tasks: "onaylı görev", c_tasks_note: "Açık, onaylı görevler. AI önerileri dahil değil.",
    c_soon: "Yaklaşan işler", c_soon_sub: "önümüzdeki 7 gün", c_soon_none: "Tarihli görev yok", c_soon_note: "Son tarihi 7 gün içinde olan açık görevler.",
    c_q: "Açık sorular", c_q_total: "soru kayıtlı", c_q_none: "Henüz soru kaydı yok", c_q_note: "Henüz cevaplanmamış sorular.",
    c_ai: "AI incelemesi", c_ai_sub: "onay bekliyor", c_ai_running: "analiz sürüyor", c_ai_waiting: "analiz bekleniyor", c_ai_note: "Gemma önerileri ve değişiklik önerileri; gerçek görev sayısına dahil değil.",
    no_data: "Henüz veri yok",
    cards_overlap: "Kartlar birbirini dışlamaz: gecikmiş bir iş hem “Görevler”de hem “Bugün”de görünebilir.",
    focus_title: "Bugün ilgilenilmesi gerekenler", f_overdue: "Gecikmiş görevler", f_orphans: "Atanmamış görevler",
    f_conflicts: "Tarihi çelişkili kayıtlar", f_decisions: "Sonuçlandırılmamış kararlar", f_none: "Bekleyen yok", f_more: n => `+${n} daha`,
    f_decisions_hint: "Pano’da “Kesinleşti” kutusunu işaretleyene kadar açık sayılır.",
    why_after_event: e => `etkinlikten (${e}) sonraya planlı`, why_held_in_future: "“Gerçekleşti” ama tarihi gelecekte", why_past_not_held: "tarihi geçti, durumu hâlâ güncel değil",
    up_events: "Yaklaşan etkinlikler", ev_open_n: (o, n) => `${o}/${n} iş açık`, imp_title: "Son içe aktarımlar",
    imp_review: n => `${n} inceleme bekliyor`, imp_st: { imported: "içe aktarıldı", analyzing: "analiz ediliyor", ready: "hazır", error: "hata" },
    sample_tag: "Örnek veri", sample_banner: "Bu panel sahte örnek veriyle dolu; gerçek kulübünüz değil.", sample_clear: "Örnek veriyi temizle",
    sample_confirm: "Örnek kulüp ve içindeki tüm kayıtlar silinsin mi? Gerçek verilerine dokunulmaz.",
    flt_label: "Filtre", flt_clear: "Temizle", flt_open: "Açık görevler", flt_soon: "Yaklaşan işler", flt_overdue: "Gecikmiş görevler",
    flt_orphans: "Atanmamış görevler", flt_questions: "Açık sorular", dec_final: "Kesinleşti", help_btn: "Nasıl çalışır?", exp_btn: "Dışa aktar", exp_title: "Dışa aktar", exp_what: "Ne aktarılsın?", exp_tasks: "Görevler (CSV)", exp_decisions: "Kararlar", exp_questions: "Açık sorular", exp_summary: "Analiz özeti (Markdown)", exp_format: "Biçim", exp_status: "Durum", exp_all: "Hepsi", exp_open: "Açık", exp_done: "Tamamlandı", exp_owner: "Sorumlu", exp_from: "Başlangıç tarihi", exp_to: "Bitiş tarihi", exp_note: "Yalnızca onaylı kayıtlar aktarılır. Görevlerde tarih aralığı son tarihe, kararlarda ve sorularda kaynak mesaj tarihine uygulanır; seçilen filtreler dosyanın başında yazar.", exp_go: "İndir", exp_bad: "Başlangıç tarihi bitişten sonra olamaz.",
    wl_title: "KulüpOS’a hoş geldin", wl_ok: "Anladım",
    wl: [
      ["KulüpOS ne yapıyor?", "Kulübün görev, karar, etkinlik ve toplantılarını tek yerde tutar. Bilgiyi istediğin an elle girersin; istersen WhatsApp sohbetini ya da toplantı notunu da yüklersin, Gemma öneri çıkarır, sen onaylarsın."],
      ["Hangi dosyayı yüklemeliyim?", "WhatsApp’ta grup Sohbeti dışa aktar medyasız. Çıkan .txt (ya da .zip) dosyası. Yüklemeden önce bir ön izleme görürsün."],
      ["Verilerim nereye gidiyor?", "Hiçbir yere. Dosya yalnızca bu bilgisayarda işlenir; analiz yerel Gemma ile yapılır, uzak servise veri gitmez."],
      ["Analiz başladı mı?", "Dosyayı yüklediğinde analiz kendiliğinden başlar; sayfanın üstünde ilerleme çubuğu ve bulunanlar görünür. Bu örnek zaten hazır."],
      ["Sonuçları nereden kontrol ederim?", "“AI incelemesi” sekmesinden. Gemma’nın önerileri sen onaylayana kadar Pano’ya ve sayılara girmez. Her kartta ile kaynak mesaj var."],
      ["Yapay zekâ hata yaparsa?", "Düzenle, Reddet ya da Onayla. Düzelttiğin kayıt sonraki analizlerde ezilmez, reddedilen geri gelmez; kaynağı bulunamayan öneri onaylanamaz."],
    ],
    chip_soon: "yakında", tag_conflict: "çelişki", tag_open: "açık", all_clear: "Bugün acil bir şey yok Gecikmiş, sahipsiz ya da çelişkili kayıt görünmüyor.",
    empty_col: "Bu komitede görev yok", empty_col_hint: "ile ekleyin ya da AI incelemesini kontrol edin.", src_show: "Kaynağı göster", src_none: "Kaynak mesaj bulunamadı", approve_why_not: "Kaynak mesaj bulunamadığı için onaylanamaz; düzenleyin ya da reddedin.",
    new_proposals: "Yeni öneriler", change_badge: "Değişiklik önerisi", src_of: "Kaynak mesaj",
    review_empty_t: "İncelenecek öneri yok", review_empty_d: "Bir sohbet dosyası yüklediğinizde ya da “Baştan analiz et” dediğinizde Gemma’nın önerileri burada onayınızı bekler. Onaylamadığınız hiçbir şey panoya girmez.",
    approve: "Onayla", no_source: "kaynak bulunamadı", date_unclear: "tarih belirsiz", reject: "Reddet", edit: "Düzenle", k_task: "Görev", k_question: "Soru", k_decision: "Karar", k_event: "Etkinlik", tab_summary: "Haftalık özet", tab_ask: "Sohbete sor",
    analyzing: "Gemma sohbeti okuyor…", queued: "Sırada bekliyor…", part: "parça",
    analysis_error: "Analiz durdu",
    retry: "Tekrar dene",
    found: { task: "görev", question: "soru", decision: "karar", event: "etkinlik", update: "güncellendi", change: "değişiklik önerisi" },
    no_unit: "Birimsiz",
    everyone: "Herkes",
    show_done: "Bitenleri göster",
    copy_member: n => `${n} için WhatsApp mesajı`,
    member_msg_head: n => `Selam ${n}, Panoda senin üzerinde görünen işler:`,
    member_msg_empty: "Şu an açık bir işin yok ",
    missed: "Gözden kaçanlar",
    m_questions: "Cevapsız sorular", m_orphans: "Kimsenin üstlenmediği işler", m_overdue: "Tarihi geçenler", m_soon: "3 gün içinde",
    nothing_missed: "Şimdilik gözden kaçan bir şey yok ",
    decisions: "Kararlar", events: "Takvim",
    none_yet: "Henüz yok",
    q_resolve: "Çözüldü", q_invalid: "Geçersiz", q_reopen: "Yeniden aç", q_closed: "Kapatılan sorular", q_hist: "Geçmiş", q_hist_none: "Henüz değişiklik yok.",
    st_name: { open: "Açık", answered: "Cevaplandı", resolved: "Çözüldü", invalid: "Geçersiz", done: "Kesinleşti" },
    val_name: { valid: "Geçerli", changed: "Değişti", cancelled: "İptal" }, val_changed: "Değişti", val_cancelled: "İptal", val_valid_btn: "Yine geçerli",
    q_note: "Not (isteğe bağlı)", q_save: "Kaydet", q_close_title: s => `“${s}” olarak işaretle`,
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
    summary_intro: "Son 7 günün özeti: Gemma kısa bir değerlendirme yazar, KulüpOS açık görevleri, cevapsız soruları ve yaklaşan tarihleri ekler. Tek tıkla gruba yapıştırın.",
    summary_btn: "Bu haftanın özetini çıkar", summary_wait: "Gemma özet yazıyor…",
    copy: "WhatsApp için kopyala", copied: "Kopyalandı Gruba yapıştırabilirsiniz",
    ask_intro: "Sohbette kaybolan bir bilgiyi sorun. Cevap, kaynak mesajlarıyla gelir.",
    ask_ph: "Örn: Salon onaylandı mı?", ask_btn: "Sor", ask_wait: "Gemma mesajlara bakıyor…",
    suggestions: ["Etkinlik ne zaman ve nerede?", "Sponsor karşılığında ne istiyor?", "Hangi işler hâlâ bekliyor?"],
    sources: "Kaynaklar",
    need_model: "Önce analiz bitsin ya da model hazır olsun.",
    err: "Bir şeyler ters gitti",
  },
  en: {
    eyebrow: "Gemma 4 · fully local · open source",
    hero_h1: ["All of your club's scattered work,", "in one place and in order with AI."],
    hero_lead: "Enter tasks, decisions, events and notes any time, during a meeting or an event; everything stays on this computer. A local Gemma AI analyses your club: what was done, what is behind, how an event went, what comes next. Free for students. A WhatsApp chat is just one source you can import.",
    cta_demo: "Open the demo club", demo_timeout: "The server did not respond. An old KulüpOS process may still be running; close it and restart with `python -m app`.", cta_upload: "Upload my group",
    trust: ["Works offline", "No API keys", "Every card links to its source (message or note)"],
    mock_chat: [["Maya", "Who can book the lab?"], ["Leo", "I'll book it today"], ["Noah", "They moved our booth to Oct 30"], ["Maya", "Decision: booth on Friday Oct 30", true]],
    mock_cards: [["Book the lab", "Leo", "Thu 8 Oct"], ["Fair Oct 30", "Events", "moved"], ["Print the banner", "no owner", ""]],
    feat: [
      ["chart", "Dashboard", "What needs attention today, risks, upcoming events and meetings at a glance. The weekly recap and “ask the chat” live here too."],
      ["calendar", "Events", "Each event on one page: linked tasks, decisions, questions, meetings, attendance, feedback and a report written only from what was entered."],
      ["calendar", "Meetings", "Paste notes or upload .txt/.md; tasks, decisions and questions go to review first. The summary is written only from the notes and approved records."],
      ["pin", "Tasks", "A board per committee plus the AI suggestions waiting for approval (review queue). Every record keeps the message or note it came from."],
      ["person", "People and committees", "Person pages derived from task owners (numbers only, no performance verdict) and committee member lists."],
      ["transfer", "Import / Export", "Bring in a WhatsApp export, take approved records out as CSV/JSON/Markdown. The data never leaves this computer."],
    ],
    why_title: "Why an open model, and why local?",
    why_sub: "A club chat holds dozens of students' phone numbers and private messages.",
    why: [["0", "messages sent to a cloud", "Gemma 4 runs on this laptop via Ollama. The server only listens on 127.0.0.1."], ["$0", "per-use cost", "Clubs have no budget. Re-analyse as often as you like."], ["1", "line to swap the model", "Plug any open model in with PANO_MODEL. No vendor lock-in."]],
    tab_overview: "Club status", tab_plan: "Plan an event",
    k_open: "Open tasks", k_done: "done", k_missed: "Slipping through", k_missed_sub: "questions + unowned work", k_decisions: "Decisions", k_next: "Next event", k_days: d => d === 0 ? "today" : `in ${d} days`, k_none: "—",
    units_title: "Team status", h_ok: "On track", h_warn: "Watch", h_bad: "Overdue", h_idle: "Empty",
    n_open: "open", n_done: "done", n_late: "late", n_orphan: "unowned",
    alerts_title: "Risks and alerts", no_alerts: "No risks right now ",
    a_event: a => `<b>${a.event}</b> is in ${a.days} days`, a_event_sub: a => `${a.open} open tasks${a.orphans ? `, ${a.orphans} with no owner` : ""}`,
    a_overdue: a => `<b>${a.title}</b> is overdue`, a_overdue_sub: a => `${a.owner ? a.owner.split(" ")[0] : "no owner"} · ${a.due}`,
    a_question: a => `Unanswered: <b>${a.title}</b>`, a_question_sub: a => `asked by ${a.owner ? a.owner.split(" ")[0] : "?"}`,
    a_load: a => `<b>${a.owner.split(" ")[0]}</b> has ${a.open} open tasks`, a_load_sub: () => "consider spreading the load",
    load_title: "Who's carrying what?", l_open: "open", l_done: "done",
    timeline_title: "Coming up", recent_decisions: "Latest decisions",
    plan_intro: "Describe the event. Gemma proposes a dated preparation plan using your teams and each member's current load. Nothing goes on the board until you approve it.",
    plan_ph: "e.g. We want a 200-person cybersecurity summit on Nov 14 with two speakers and one sponsor.",
    plan_btn: "Propose a plan", plan_wait: "Gemma is drafting the plan…", plan_add: n => `Add ${n} selected tasks to the board`, plan_added: n => `${n} tasks added to the board`,
    plan_examples: ["A 150-person AI talk in 3 weeks", "A 24-hour hackathon at the end of November", "A welcome event for new members next month"],
    suggested: "suggested",
    hero_title: "Turn your club's WhatsApp chaos into a board",
    hero_sub: "Drop your group's chat export. Gemma 4 reads it on this computer and pulls out tasks, decisions, dates and unanswered questions. Not a single message leaves the device.",
    drop: "Drop a WhatsApp export here",
    drop_hint: ".txt or .zip · or click to choose a file",
    units_label: "Your club's teams (comma separated)",
    units_default: "Board, Events, Communications, Sponsorship",
    name_label: "Group name (optional)",
    try_demo: "Try a demo chat",
    how_export: "How do I export from WhatsApp?",
    how_steps: ["Open the group and tap its name", "Scroll down and choose <b>Export chat</b>", "Pick <b>Without media</b> and send the file to this computer"],
    privacy: "<b>Your data never leaves this computer.</b> The model runs locally with Ollama; member phone numbers and messages are never sent to any cloud.",
    recent: "Previous groups",
    messages: "messages",
    health_ok: "Local · Gemma 4 ready",
    health_nomodel: "Model missing: ollama pull",
    health_down: "Ollama is not running",
    tab_board: "Board", tab_review: "AI review", review_intro: "Gemma suggests these. Anything you do not approve stays off the board.", review_empty: "Nothing to review.", pv_title: "Import preview", pv_msgs: "messages", pv_senders: "senders", pv_skipped: n => `${n} lines could not be parsed and will be skipped`, pv_dup: n => `This file was already imported (“${n}”). Add it anyway?`, pv_go: "Import", changes_title: "Change proposals", f_status_l: "status", f_owner_l: "owner", f_due_l: "date", f_time_l: "time", f_place_l: "place", units_btn: "Teams", units_add: "New team name", units_add_btn: "Add", unit_members_ph: "Members (comma separated, free text)", units_note: "Tasks of a deleted team move to the “no team” column.", ev_add: "Add event", ev_edit: "Edit event", ev_type: "Type", ev_date: "Date", ev_time: "Time", ev_place: "Venue", ev_owner: "Owner",
    ev_units: "Teams", ev_phase: "Status", ev_exp: "Expected attendees", ev_act: "Actual attendees", ev_bud_est: "Budget estimate", ev_bud_act: "Actual budget", ev_apps: "Applications", ev_fb_score: "Feedback score (1-5, optional)", ev_fb_note: "Short feedback note",
    tab_analysis: "Event analysis", an_none: "Not entered", an_intro: "Figures are computed only from the entered event data (cancelled events excluded); no model needed. Missing data reads “Not entered”.",
    an_total: "Events", an_avg_att: "Average attendance", an_avg_rate: "Average attendance rate", an_avg_fb: "Average feedback", an_high: "Highest attendance", an_low: "Lowest attendance",
    an_low_need: "Needs actual attendance on at least 2 events to compare.", an_committee: "Events per committee", an_committee_note: "An event with several committees counts in each.", an_no_unit: "No committee entered",
    an_per_event: "Per event", an_c_event: "Event", an_c_rate: "Attendance rate (actual/expected)", an_c_conv: "Application attendance", an_c_budget: "Budget deviation", an_c_fb: "Feedback",
    an_empty: "No events yet. Add events on the board.", an_insight: "Period insight", an_insight_btn: "Write period insight", an_insight_re: "Regenerate",
    an_insight_none: "No insight yet. Gemma writes a short comment from the computed figures above only; text with a figure that is not in them is rejected.",
    an_wait: "Gemma is writing locally; this can take a few minutes", an_src_sample: "Sample data: precomputed insight", an_src_ai: "Written by Gemma from the computed figures only", an_stale: "The event data changed after this insight; regenerate it.", an_rejected: "Insight rejected",
    ev_notes: "Notes", ev_none: "No event", ev_linked: n => `${n} linked`, ev_link: "Event",
    ph: { idea: "Idea", planning: "Planning", confirmed: "Confirmed", held: "Held", cancelled: "Cancelled" }, rp_btn: "Report", rp_title: "Event report", rp_make: "Write report with Gemma", rp_remake: "Regenerate", rp_none: "No report yet.",
    rp_wait: "Gemma is writing locally; this can take a few minutes", rp_elapsed: "elapsed", rp_stale: "The event data changed after this report; regenerate it.",
    rp_src_sample: "Precomputed sample report (demo data)", rp_src_ai: "Written by Gemma from the entered data only", rp_rejected: "Report rejected",
    rp_figs: "Figures not in the data", rp_note: "The report is built only from the fields entered for this event, its linked tasks and decisions; empty fields stay “Not entered”.",
    rp_copy: "Copy", ev_sample: "Add sample event", c_tasks: "Tasks", c_approved_tasks: "approved tasks", c_tasks_note: "Open, approved tasks. AI proposals not included.",
    c_soon: "Coming up", c_soon_sub: "next 7 days", c_soon_none: "No task has a date", c_soon_note: "Open tasks due within 7 days.",
    c_q: "Open questions", c_q_total: "questions recorded", c_q_none: "No questions recorded yet", c_q_note: "Questions nobody has answered yet.",
    c_ai: "AI review", c_ai_sub: "awaiting approval", c_ai_running: "analysis running", c_ai_waiting: "waiting for analysis", c_ai_note: "Gemma proposals and change proposals; not part of the real task count.",
    no_data: "No data yet",
    cards_overlap: "Cards are not mutually exclusive: an overdue task can appear under “Tasks” and under “Today”.",
    focus_title: "Needs attention today", f_overdue: "Overdue tasks", f_orphans: "Unassigned tasks",
    f_conflicts: "Records with conflicting dates", f_decisions: "Decisions not finalised", f_none: "Nothing pending", f_more: n => `+${n} more`,
    f_decisions_hint: "Stays open until you tick “Final” on the board.",
    why_after_event: e => `scheduled after its event (${e})`, why_held_in_future: "marked “Held” but dated in the future", why_past_not_held: "date has passed, status not updated",
    up_events: "Upcoming events", ev_open_n: (o, n) => `${o}/${n} tasks open`, imp_title: "Recent imports",
    imp_review: n => `${n} awaiting review`, imp_st: { imported: "imported", analyzing: "analysing", ready: "ready", error: "error" },
    sample_tag: "Sample data", sample_banner: "This panel is filled with fake sample data; it is not your club.", sample_clear: "Clear sample data",
    sample_confirm: "Delete the sample club and everything in it? Your own data is not touched.",
    flt_label: "Filter", flt_clear: "Clear", flt_open: "Open tasks", flt_soon: "Coming up", flt_overdue: "Overdue tasks",
    flt_orphans: "Unassigned tasks", flt_questions: "Open questions", dec_final: "Final", help_btn: "How it works", exp_btn: "Export", exp_title: "Export", exp_what: "What to export?", exp_tasks: "Tasks (CSV)", exp_decisions: "Decisions", exp_questions: "Open questions", exp_summary: "Analysis summary (Markdown)", exp_format: "Format", exp_status: "Status", exp_all: "All", exp_open: "Open", exp_done: "Done", exp_owner: "Owner", exp_from: "From date", exp_to: "To date", exp_note: "Only approved records are exported. The date range applies to the due date for tasks and to the source message date for decisions and questions; the chosen filters are written at the top of the file.", exp_go: "Download", exp_bad: "The start date cannot be after the end date.",
    wl_title: "Welcome to KulüpOS", wl_ok: "Got it",
    wl: [
      ["What does KulüpOS do?", "It keeps your club’s tasks, decisions, events and meetings in one place. You enter information any time; you can also upload a WhatsApp chat or meeting notes and Gemma suggests records for you to approve. Previously: it turns tasks, decisions, open questions and events into one clear board, each linked to its source message."],
      ["Which file do I upload?", "In WhatsApp: group Export chat without media. Upload the .txt (or .zip) file. You see a preview before anything is imported."],
      ["Where does my data go?", "Nowhere. The file is processed on this computer only; analysis runs on local Gemma and nothing is sent to a remote service."],
      ["Has the analysis started?", "It starts by itself after you upload; a progress bar and the items found so far show at the top of the page. This sample is already done."],
      ["Where do I check the results?", "In the “AI review” tab. Gemma’s proposals stay out of the board and the numbers until you approve them. Every card has a source message."],
      ["What if the AI is wrong?", "Edit, Reject or Approve. Your corrections are not overwritten by later analyses and rejected items do not return; proposals without a source cannot be approved."],
    ],
    chip_soon: "soon", tag_conflict: "conflict", tag_open: "open", all_clear: "Nothing urgent today No overdue, unassigned or conflicting records.",
    empty_col: "No tasks in this team", empty_col_hint: "Add one with or check the AI review.", src_show: "Show source", src_none: "Source message not found", approve_why_not: "Cannot be approved because no source message was found; edit or reject it.",
    new_proposals: "New proposals", change_badge: "Change proposal", src_of: "Source message",
    review_empty_t: "Nothing to review", review_empty_d: "When you upload a chat file or choose “Re-analyse”, Gemma’s proposals wait here for your approval. Nothing you do not approve reaches the board.",
    approve: "Approve", no_source: "source not found", date_unclear: "date unclear", reject: "Reject", edit: "Edit", k_task: "Task", k_question: "Question", k_decision: "Decision", k_event: "Event", tab_summary: "Weekly recap", tab_ask: "Ask the chat",
    analyzing: "Gemma is reading the chat…", queued: "Waiting in line…", part: "part",
    analysis_error: "Analysis stopped",
    retry: "Retry",
    found: { task: "task", question: "question", decision: "decision", event: "event", update: "updated", change: "change proposed" },
    no_unit: "No team",
    everyone: "Everyone",
    show_done: "Show done",
    copy_member: n => `WhatsApp message for ${n}`,
    member_msg_head: n => `Hi ${n}, here's what's on you on the board:`,
    member_msg_empty: "Nothing open right now ",
    missed: "Slipping through",
    m_questions: "Unanswered questions", m_orphans: "Nobody took these", m_overdue: "Overdue", m_soon: "Due within 3 days",
    nothing_missed: "Nothing is slipping through right now ",
    decisions: "Decisions", events: "Calendar",
    none_yet: "Nothing yet",
    q_resolve: "Resolved", q_invalid: "Not valid", q_reopen: "Reopen", q_closed: "Closed questions", q_hist: "History", q_hist_none: "No changes yet.",
    st_name: { open: "Open", answered: "Answered", resolved: "Resolved", invalid: "Not valid", done: "Final" },
    val_name: { valid: "Valid", changed: "Changed", cancelled: "Cancelled" }, val_changed: "Changed", val_cancelled: "Cancel", val_valid_btn: "Valid again",
    q_note: "Note (optional)", q_save: "Save", q_close_title: s => `Mark the question as “${s}”`,
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
    summary_intro: "A recap of the last 7 days: Gemma writes a short overview, KulüpOS adds open tasks, unanswered questions and upcoming dates. Paste it into the group in one click.",
    summary_btn: "Write this week's recap", summary_wait: "Gemma is writing…",
    copy: "Copy for WhatsApp", copied: "Copied Paste it into the group",
    ask_intro: "Ask about something that got buried in the chat. The answer comes with its source messages.",
    ask_ph: "e.g. Did we get the room?", ask_btn: "Ask", ask_wait: "Gemma is looking through the messages…",
    suggestions: ["When and where is the event?", "What does the sponsor want in return?", "Which tasks are still open?"],
    sources: "Sources",
    need_model: "Wait for the analysis or the model first.",
    err: "Something went wrong",
  },
};
const MEET_I18N = {
  tr: {
    tab_meetings: "Toplantılar",
    mt_intro: "Toplantı notlarını yapıştır veya .txt/.md olarak yükle. Notlardan çıkan görev, karar ve sorular önce AI incelemesine düşer; sen onaylamadan panoya girmez.",
    mt_add: "Toplantı ekle", mt_edit: "Toplantıyı düzenle", mt_empty: "Henüz toplantı yok.",
    mt_nodate: "tarih belirsiz", mt_status: "Durum", mt_st: { planned: "Planlandı", held: "Yapıldı", cancelled: "İptal" },
    mt_date_hint: "Tarih boş bırakılabilir; bu durumda “tarih belirsiz” işaretlenir ve notlardaki göreli tarihler (“haftaya”) çözülmez.",
    mt_attendees: "Katılımcılar", mt_att_ph: "Ad Soyad, Ad Soyad", mt_fill: "Seçili komitelerin üyelerini ekle", mt_no_members: "Seçili komitelerde üye listesi yok (Komiteler düğmesinden girilir).",
    mt_agenda: "Gündem", mt_notes: "Notlar", mt_upload: ".txt / .md yükle", mt_no_notes: "Not girilmedi.",
    mt_notes_note: "Notlar güvenilmeyen veri sayılır: içindeki “talimatlar” modele komut olmaz. En fazla 100 KB, UTF-8.",
    mt_counts: m => `${m.tasks} görev · ${m.decisions} karar · ${m.questions} açık soru${m.orphan_tasks ? ` ·  ${m.orphan_tasks} sorumlusuz` : ""}`,
    mt_tasks: "Bağlı görevler", mt_decisions: "Bağlı kararlar", mt_questions: "Bağlı açık sorular", mt_none: "Henüz onaylı kayıt yok.",
    mt_analyze: "Notlardan öneri üret", mt_an_wait: "Gemma notları okuyor…", mt_elapsed: "geçen süre",
    mt_an_done: s => `${s.tasks} görev, ${s.decisions} karar, ${s.questions} soru önerildi${s.duplicates ? ` · ${s.duplicates} tanesi zaten kayıtlı olduğu için atlandı` : ""}.`,
    mt_an_stale: "Notlar son analizden sonra değişti; yeniden analiz yalnızca yeni öneriler ekler.",
    mt_pending: n => `AI incelemesinde ${n} öneri bekliyor`, mt_go_review: "İncelemeye git", mt_src_meeting: "Toplantı notu",
    mt_sum_title: "Toplantı özeti", mt_sum_make: "Toplantı özeti", mt_sum_remake: "Özeti yeniden yaz", mt_sum_wait: "Gemma özeti yazıyor…",
    mt_sum_note: "Yalnızca toplantı notlarından ve onaylı bağlı kayıtlardan yazılır; kayıtta olmayan sayı veya isim içeren özet reddedilir.",
    mt_sum_none: "Henüz özet yok.", mt_sum_stale: " ESKİ: notlar, toplantı bilgileri veya onaylı kayıtlar özetten sonra değişti.",
    mt_sum_rejected: "Özet reddedildi", mt_sum_cut: "Notların yalnızca ilk 12.000 karakteri özete girdi.", mt_sum_copy: "Kopyala",
    mt_sum_src_sample: "Örnek veri · önceden hesaplanmış özet", mt_sum_src_ai: "Yerel Gemma ile yazıldı",
    mt_orphans: n => `${icon("alert")} Bu toplantıdan çıkan ${n} görevin sorumlusu yok`, mt_warn_title: "Bilgi: komite üye listesinde olmayan sorumlu",
    mt_warn: w => `<b>${esc(w.owner)}</b> “${esc(w.title)}” görevinin sorumlusu, ama ${w.units.map(esc).join(", ")} komite üye listesinde yok. Engellenmedi; listeyi ya da sorumluyu gözden geçir.`,
    pc_upcoming: "Yaklaşan toplantılar", pc_upcoming_none: "Planlanmış yaklaşan toplantı yok.", pc_held: "Yapıldı ama sorumlusuz görev var",
    pc_held_none: "Yapılan toplantılarda sorumlusuz görev yok.", pc_orphans: n => `${n} sorumlusuz görev`, pc_all: "Tüm toplantılar", pc_nodate: "tarih belirsiz",
    mt_noowner: "sorumlusu yok", mt_confirm_del: "Toplantı silinsin mi? Onaylı kayıtlar panoda kalır ama toplantıyla bağı ve kaynak notu kalkar; bekleyen öneriler silinir.",
  },
  en: {
    tab_meetings: "Meetings",
    mt_intro: "Paste meeting notes or upload them as .txt/.md. Tasks, decisions and questions found in them go to AI review first; nothing reaches the board until you approve.",
    mt_add: "Add meeting", mt_edit: "Edit meeting", mt_empty: "No meetings yet.",
    mt_nodate: "date unclear", mt_status: "Status", mt_st: { planned: "Planned", held: "Held", cancelled: "Cancelled" },
    mt_date_hint: "The date may be left empty; it is then marked “date unclear” and relative dates in the notes (“next week”) are not resolved.",
    mt_attendees: "Attendees", mt_att_ph: "Name Surname, Name Surname", mt_fill: "Add members of the selected teams", mt_no_members: "The selected teams have no member list (set it under Teams).",
    mt_agenda: "Agenda", mt_notes: "Notes", mt_upload: "Upload .txt / .md", mt_no_notes: "No notes entered.",
    mt_notes_note: "Notes count as untrusted data: any “instructions” inside never become commands for the model. Max 100 KB, UTF-8.",
    mt_counts: m => `${m.tasks} tasks · ${m.decisions} decisions · ${m.questions} open questions${m.orphan_tasks ? ` ·  ${m.orphan_tasks} without owner` : ""}`,
    mt_tasks: "Linked tasks", mt_decisions: "Linked decisions", mt_questions: "Linked open questions", mt_none: "No approved records yet.",
    mt_analyze: "Suggest from notes", mt_an_wait: "Gemma is reading the notes…", mt_elapsed: "elapsed",
    mt_an_done: s => `${s.tasks} tasks, ${s.decisions} decisions, ${s.questions} questions suggested${s.duplicates ? ` · ${s.duplicates} skipped (already recorded)` : ""}.`,
    mt_an_stale: "The notes changed since the last analysis; re-analysing only adds new suggestions.",
    mt_pending: n => `${n} suggestion(s) waiting in AI review`, mt_go_review: "Go to review", mt_src_meeting: "Meeting note",
    mt_sum_title: "Meeting summary", mt_sum_make: "Meeting summary", mt_sum_remake: "Rewrite summary", mt_sum_wait: "Gemma is writing the summary…",
    mt_sum_note: "Written only from the meeting notes and the approved linked records; a summary with figures or names that are not in the record is rejected.",
    mt_sum_none: "No summary yet.", mt_sum_stale: " OUTDATED: the notes, meeting details or approved records changed after this summary.",
    mt_sum_rejected: "Summary rejected", mt_sum_cut: "Only the first 12,000 characters of the notes went into the summary.", mt_sum_copy: "Copy",
    mt_sum_src_sample: "Sample data · precomputed summary", mt_sum_src_ai: "Written by local Gemma",
    mt_orphans: n => `${icon("alert")} ${n} task(s) from this meeting have no owner`, mt_warn_title: "Note: owner not on the committee's member list",
    mt_warn: w => `<b>${esc(w.owner)}</b> owns “${esc(w.title)}” but is not on the member list of ${w.units.map(esc).join(", ")}. Not blocked; review the list or the owner.`,
    pc_upcoming: "Upcoming meetings", pc_upcoming_none: "No upcoming planned meetings.", pc_held: "Held, but tasks without an owner",
    pc_held_none: "No ownerless tasks from held meetings.", pc_orphans: n => `${n} task(s) without owner`, pc_all: "All meetings", pc_nodate: "date unclear",
    mt_noowner: "no owner", mt_confirm_del: "Delete this meeting? Approved records stay on the board but lose the meeting link and source note; pending suggestions are deleted.",
  },
};
const HUB_I18N = {
  tr: {
    nav_main: "Ana menü", nav_panel: "Panel", nav_list: "Etkinlik listesi", nav_tasks: "Görevler", tab_units: "Komiteler", nav_data: "İçe/Dışa aktar",
    sec_work: "Çalışma", sec_people: "İnsanlar", sec_ai: "AI", sec_data: "Veri", more: "Diğer işlemler", menu: "Menü",
    ov_hello: n => `${n} için bugünkü durum.`,
    ov_clear: "Gecikmiş, sahipsiz, çelişkili kayıt veya açık karar yok.",
    ov_ai: "Son AI önerileri", ov_empty_ai: "Onay bekleyen öneri yok.",
    ov_see_board: "Görevlere git", ov_see_events: "Etkinliklere git", ov_see_review: "İncelemeye git",
    sample_hide: "Gizle",
    un_intro: "Komiteler, üye listeleri ve onlara bağlı işler. Sayılar yalnızca girilmiş görev ve etkinlik kayıtlarından gelir.", un_members: "Üyeler (serbest metin)",
    un_add_member: "Üye ekle",
    un_loose: n => `${n} görev komitesiz.`,
    da_intro: "Sohbeti içeri al, verini dışarı ver. Veri bilgisayardan çıkmaz.", da_import: "İçe aktar", da_new: "Başka sohbet / yeni kulüp",
    da_import_note: "Aynı sohbetin daha yeni bir dışa aktarımı eklenirse yalnızca yeni mesajlar alınır. “Baştan analiz et” modelin tüm sohbeti yeniden okumasını ister (yavaştır); kendi düzeltmelerin ezilmez.",
    da_export: "Dışa aktar", da_export_note: "Yalnızca onaylı kayıtlar. CSV/JSON penceresinde filtre ve tarih aralığı seçilir.", da_danger: "Tehlikeli bölge",
    tab_people: "Kişiler", pp_intro: "Görev sahiplerinden otomatik türeyen isimler. Bir kişiye tıklayınca görevleri, etkinlikleri ve toplantıları açılır.",
    pp_note: "Yalnızca sayılar: görev sayısı zorluğu yansıtmaz; bu sayfa bir performans değerlendirmesi değildir.",
    pp_name: "Kişi", pp_committees: "Komiteler", pp_open: "Açık", pp_late: "Geciken görevler", pp_done: "Tamamlanan", pp_done_l: "Tamamladıkları",
    pp_upcoming: "Yaklaşan teslimler", pp_undated: "Tarihsiz açık görevler", pp_events: "Etkinlikler", pp_meetings: "Toplantılar (katılımcı listesinde adı geçen)",
    pp_role_owner: "etkinlik sorumlusu", pp_role_task: "görevi bu etkinliğe bağlı", pp_empty: "Henüz sorumlusu olan görev yok.",
    tab_events: "Etkinlikler", evs_intro: "Bir etkinliğe tıkla: bilgi, bağlı görevler, kararlar, sorular, toplantılar, katılım, geri bildirim ve rapor tek sayfada açılır.",
    evp_open: "Aç", evp_info: "Bilgi", evp_attend: "Katılım", evp_applied: "Kayıt / başvuru (ilgi)", evp_tasks: "Bağlı görevler", evp_decisions: "Bağlı kararlar",
    evp_questions: "Bağlı açık sorular", evp_meetings: "Bağlı toplantılar", evp_none: "Bağlı kayıt yok.",
    evp_meet_note: "Bu etkinliğe bağlı kayıtların geldiği toplantılar (toplantıdan etkinliğe doğrudan bağ yok).",
    evp_feedback: "Geri bildirim", fb_score: "Puan ortalaması (1–5, isteğe bağlı)", fb_good: "İyi giden", fb_bad: "Aksayan",
    fb_comments: "Katılımcı yorumları", fb_comments_ph: "Yorumları yapıştır; her satıra bir yorum", fb_count: "Yorum sayısı",
    fb_empty: "Geri bildirim girilmedi. Elle girilir; uydurulmaz.", fb_note_hint: "Geri bildirimler elle girilir. Rapor yalnızca bu alanlardan ve etkinliğin kayıtlarından yazılır.",
    cmp_title: "Etkinlik karşılaştırması", cmp_att: "Katılım oranı", cmp_late: "Geciken görev", cmp_score: "Puan ortalaması",
    cmp_note: "— : veri girilmemiş; tahmin yazılmaz. Geciken görev: bağlı açık görevlerden tarihi geçmiş olanlar / bağlı görev sayısı.",
  },
  en: {
    nav_main: "Main menu", nav_panel: "Dashboard", nav_list: "Event list", nav_tasks: "Tasks", tab_units: "Committees", nav_data: "Import / Export",
    sec_work: "Work", sec_people: "People", sec_ai: "AI", sec_data: "Data", more: "More actions", menu: "Menu",
    ov_hello: n => `Today in ${n}.`,
    ov_clear: "No overdue, unassigned or conflicting records, and no open decisions.",
    ov_ai: "Recent AI suggestions", ov_empty_ai: "No proposals waiting for approval.",
    ov_see_board: "Open tasks", ov_see_events: "Open events", ov_see_review: "Open review",
    sample_hide: "Hide",
    un_intro: "Committees, their member lists and the work tied to them. Counts come only from entered task and event records.", un_members: "Members (free text)",
    un_add_member: "Add member",
    un_loose: n => `${n} task(s) without a committee.`,
    da_intro: "Bring a chat in, take your data out. The data never leaves this computer.", da_import: "Import", da_new: "Another chat / new club",
    da_import_note: "Adding a newer export of the same chat only takes the new messages. “Re-analyse from scratch” makes the model read the whole chat again (slow); your own corrections are not overwritten.",
    da_export: "Export", da_export_note: "Approved records only. The CSV/JSON dialog lets you pick a filter and a date range.", da_danger: "Danger zone",
    tab_people: "People", pp_intro: "Names derived from task owners. Click a person to see their tasks, events and meetings.",
    pp_note: "Numbers only: a task count does not reflect difficulty; this page is not a performance review.",
    pp_name: "Person", pp_committees: "Committees", pp_open: "Open", pp_late: "Late tasks", pp_done: "Completed", pp_done_l: "Completed",
    pp_upcoming: "Upcoming deadlines", pp_undated: "Open tasks without a date", pp_events: "Events", pp_meetings: "Meetings (named in the attendee list)",
    pp_role_owner: "event owner", pp_role_task: "task linked to this event", pp_empty: "No task has an owner yet.",
    tab_events: "Events", evs_intro: "Click an event: info, linked tasks, decisions, questions, meetings, attendance, feedback and report open on one page.",
    evp_open: "Open", evp_info: "Info", evp_attend: "Attendance", evp_applied: "Registered / applied (interest)", evp_tasks: "Linked tasks", evp_decisions: "Linked decisions",
    evp_questions: "Linked open questions", evp_meetings: "Linked meetings", evp_none: "No linked records.",
    evp_meet_note: "Meetings that produced records linked to this event (there is no direct meeting-to-event link).",
    evp_feedback: "Feedback", fb_score: "Average score (1–5, optional)", fb_good: "What went well", fb_bad: "What fell short",
    fb_comments: "Participant comments", fb_comments_ph: "Paste the comments; one per line", fb_count: "Number of comments",
    fb_empty: "No feedback entered. It is entered by hand; nothing is made up.", fb_note_hint: "Feedback is entered by hand. The report is written only from these fields and the event's records.",
    cmp_title: "Event comparison", cmp_att: "Attendance rate", cmp_late: "Late tasks", cmp_score: "Average score",
    cmp_note: "— : not entered; nothing is estimated. Late tasks: linked open tasks past their date / number of linked tasks.",
  },
};
Object.assign(I18N.tr, MEET_I18N.tr, HUB_I18N.tr);
Object.assign(I18N.en, MEET_I18N.en, HUB_I18N.en);
let lang = (() => {
  try { return localStorage.getItem("pano.lang") || (navigator.language.startsWith("tr") ? "tr" : "en"); }
  catch { return "tr"; }
})();
const t = key => I18N[lang][key] ?? key;

// ---------------------------------------------------------------- helpers
const $ = sel => document.querySelector(sel);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function icon(name) {
  const paths = {
    alert: '<path d="M12 9v4M12 17h.01"/><path d="M10.3 4.8 2.8 18a2 2 0 0 0 1.7 3h15a2 2 0 0 0 1.7-3L13.7 4.8a2 2 0 0 0-3.4 0z"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
    chat: '<path d="M21 12a8 8 0 0 1-8 8H7l-4 3V12a8 8 0 1 1 18 0z"/>',
    pin: '<path d="M12 17v5M9 10.8 8 17h8l-1-6.2M8 10h8l-1-6H9z"/>',
    chart: '<path d="M4 19V5M4 19h16M8 16v-5M12 16V8M16 16v-3"/>',
    person: '<circle cx="12" cy="8" r="3"/><path d="M5 19c1.5-3 3.8-4.5 7-4.5S17.5 16 19 19"/>',
    people: '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2"/><path d="M3 19c1.2-3 3.2-4.5 6-4.5S13.8 16 15 19M16 14.5c2 .3 3.5 1.5 4.5 4.5"/>',
    spark: '<path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5z"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    compass: '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 6-6 2 2-6z"/>',
    note: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M8 13h8M8 17h5"/>',
    search: '<circle cx="11" cy="11" r="6"/><path d="m20 20-3.5-3.5"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/>',
    check: '<path d="M5 12.5 9.5 17 19 7"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    edit: '<path d="M4 20h4l10-10-4-4L4 16z"/><path d="m13 7 4 4"/>',
    copy: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V6a2 2 0 0 1 2-2h10"/>',
    download: '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
    upload: '<path d="M12 20V9M7 13l5-5 5 5M5 4h14"/>',
    target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
    users: '<circle cx="8" cy="9" r="3"/><circle cx="16" cy="9" r="3"/><path d="M2 19c1-3 3-4.5 6-4.5S13 16 14 19M12 14.5c3 0 5 1.5 6 4.5"/>',
    folder: '<path d="M3 7h6l2 2h10v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 8h.01"/>',
    file: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
    image: '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="m21 16-5-4-9 7"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.8.4-1 1-1 1.7V14"/>',
    refresh: '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v6h-6"/>',
    transfer: '<path d="M7 7h11l-3-3M17 17H6l3 3"/>',
    back: '<path d="M15 6 9 12l6 6"/>',
    next: '<path d="m9 6 6 6-6 6"/>',
    coin: '<ellipse cx="12" cy="7" rx="7" ry="3"/><path d="M5 7v10c0 1.7 3.1 3 7 3s7-1.3 7-3V7"/>',
    offline: '<path d="M3 8a12 12 0 0 1 18 0M6 12a8 8 0 0 1 12 0M4 4l16 16"/><circle cx="12" cy="18" r="1"/>',
    news: '<path d="M5 5h11v14H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M16 8h3v9a2 2 0 0 1-2 2M8 9h5M8 13h5"/>',
    paperclip: '<path d="m16 8-6.5 6.5a3 3 0 0 1-4-4L12 4a4 4 0 0 1 6 6l-7 7"/>',
    dots: '<circle cx="6" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="18" cy="12" r="1"/>',
    wave: '<path d="M4 14c2-4 4-4 6 0s4 4 6 0 4-4 4 0"/>',
  };
  const d = paths[name];
  if (!d) return "";
  return `<svg class="ico" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
}


async function api(path, opts = {}) {
  const res = await fetch(path, {
    ...opts,
    headers: opts.body && !(opts.body instanceof ArrayBuffer) ? { "Content-Type": "application/json" } : {},
  });
  if (!res.ok) {
    let detail = res.statusText;
    if (res.status === 401 && !path.startsWith("/api/auth/")) { showPublic(); throw new Error(lang === "tr" ? "Oturum gerekli" : "Sign-in required"); }
    try { detail = (await res.json()).detail || detail; } catch {}
    if (detail && typeof detail === "object") {  // 422 from report/insight checks: {message, unsupported}
      detail = (detail.message || res.statusText) + (detail.unsupported?.length ? " — " + detail.unsupported.join(", ") : "");
    }
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
function avatarStack(text) {
  const names = String(text || "").split(",").map(s => s.trim()).filter(Boolean);
  if (!names.length) return "";
  const shown = names.slice(0, 4), extra = names.length - shown.length;
  return `<span class="avatars" title="${esc(names.join(", "))}">${shown.map(avatar).join("")}${extra ? `<span class="avatar more">+${extra}</span>` : ""}</span>`;
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
const S = { chats: [], board: null, health: null, member: "", showDone: true, group: "status", poll: null, summary: null, answer: null };

function route() {
  const [, kind, id, view, mid] = location.hash.split("/");
  return kind === "c" ? { chatId: Number(id), view: view || "overview", mid: Number(mid) || null, arg: decodeURIComponent(mid || "") } : { chatId: null, view: "home" };
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
  if (!S.chats.length) { box.innerHTML = ""; return; }
  box.innerHTML = `<select id="chat-select" aria-label="${esc(t("recent"))}">${S.chats.map(c =>
    `<option value="${c.id}" ${c.id === chatId ? "selected" : ""}>${esc(c.name)}${c.is_sample ? " · " + t("sample_tag") : ""}</option>`).join("")}
    <option value="new">${t("da_new")}</option></select>`;
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
        <div class="phone"><div class="hd">WhatsApp</div>${t("mock_chat").map(([w, m, me]) =>
          `<div class="b ${me ? "me" : ""}"><b style="color:hsl(${hue(w)} 55% 42%)">${w}</b>${m}</div>`).join("")}</div>
        <div class="arrow"></div>
        <div class="board"><div class="hd"><span>KulüpOS</span><span class="muted">Gemma 4</span></div>${t("mock_cards").map(([ti, o, d], i) =>
          `<div class="mc"><b>${ti}</b><div class="m"><span class="chip ${i === 2 ? "none" : ""}">${o}</span><span class="chip ${i === 2 ? "overdue" : i === 1 ? "ai" : ""}">${d}</span></div></div>`).join("")}</div>
      </div>
    </div>
    <div class="features">${t("feat").map(([ic, h, p]) =>
      `<div class="feature"><div class="ic">${icon(ic)}</div><h4>${h}</h4><p>${p}</p></div>`).join("")}</div>
    <h2 class="section-title" id="upload-title">${t("drop")}</h2>
    <p class="section-sub">${t("drop_hint")}</p>
    <div class="upload">
      <div class="panel">
        <div class="drop" id="drop" tabindex="0" role="button">
          <div class="big"></div>
          <b>${t("drop")}</b>
          <small>${t("drop_hint")}</small>
        </div>
        <input type="file" id="file" accept=".txt,.zip,text/plain,application/zip" hidden>
        <label for="units">${t("units_label")}</label>
        <input type="text" id="units" value="${esc(t("units_default"))}">
        <label for="gname">${t("name_label")}</label>
        <input type="text" id="gname" placeholder="FUB3V Yönetim">
        <div class="demo-row">
          <button class="primary" data-demo="${lang}">${t("try_demo")}</button>
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
    try {
      const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 15000);  // the server answers within 5 s or with an error
      const res = await fetch(`/api/demo/${b.dataset.demo}`, { method: "POST", signal: ctl.signal }).finally(() => clearTimeout(timer));
      if (!res.ok) { let d = res.statusText; try { d = (await res.json()).detail || d; } catch {} throw new Error(d); }
      openChat(await res.json());
    } catch (e) { toast(e.name === "AbortError" ? t("demo_timeout") : e.message, 6000); b.disabled = false; }
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
    <p><b>${esc(f.name)}</b><br>${pv.messages} ${t("pv_msgs")} · ${fmtDate(pv.first_ts, false)} – ${fmtDate(pv.last_ts, false)} · ${pv.senders.length} ${t("pv_senders")}</p>
    <p class="muted">${pv.senders.map(esc).join(", ")}</p>
    ${pv.skipped_lines ? `<p> ${t("pv_skipped")(pv.skipped_lines)}</p>` : ""}
    ${pv.duplicate_of ? `<p> ${t("pv_dup")(esc(pv.duplicate_of.name))}</p>` : ""}
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

// Sidebar groups. Routes stay #/c/:id/<view>. Event list / analysis / plan stay as an in-page segment.
const SIDE = [
  { label: "sec_work", items: [["overview", "tab_overview"], ["board", "nav_tasks"], ["events", "tab_events"], ["meetings", "tab_meetings"]] },
  { label: "sec_people", items: [["people", "tab_people"], ["units", "tab_units"]] },
  { label: "sec_ai", items: [["review", "tab_review"], ["plan", "tab_plan"], ["summary", "tab_summary"], ["ask", "tab_ask"]] },
  { label: "sec_data", items: [["data", "nav_data"]] },
];
const TITLE = {
  overview: "tab_overview", summary: "tab_summary", ask: "tab_ask",
  events: "tab_events", event: "tab_events", analysis: "tab_analysis", plan: "tab_plan",
  meetings: "tab_meetings", meeting: "tab_meetings", board: "nav_tasks", review: "tab_review",
  people: "tab_people", person: "tab_people", units: "tab_units", data: "nav_data",
};

function renderSideNav() {
  const nav = $("#side-nav");
  if (!nav) return;
  const { chatId, view } = route();
  const id = chatId || (S.chats[0] && S.chats[0].id);
  nav.setAttribute("aria-label", t("nav_main"));
  if (!id) { nav.innerHTML = ""; return; }
  const here = S.board && S.board.chat.id === id ? S.board : null;
  const reviewN = here ? here.review.length + here.changes.length : 0;
  const missedN = here ? Object.values(here.missed).reduce((n, l) => n + l.length, 0) : 0;
  const on = v => v === view || (v === "events" && view === "event") || (v === "people" && view === "person") || (v === "meetings" && view === "meeting");
  nav.innerHTML = SIDE.map(g => `<div class="side-label">${t(g.label)}</div>` + g.items.map(([v, key]) => {
    const n = v === "review" ? reviewN : v === "board" ? missedN : 0;
    return `<a href="#/c/${id}/${v}" class="${on(v) ? "active" : ""}"><span>${t(key)}</span>${n ? `<span class="side-count">${n}</span>` : ""}</a>`;
  }).join("")).join("");
}

function closeSidebar() { $("#sidebar")?.classList.remove("open"); }

function segmentHtml(view) {
  if (!["events", "event", "analysis", "plan"].includes(view)) return "";
  const id = S.board.chat.id;
  const cur = view === "event" ? "events" : view;
  return `<div class="segment" role="tablist">${[["events", "nav_list"], ["analysis", "tab_analysis"], ["plan", "tab_plan"]].map(([v, k]) =>
    `<a href="#/c/${id}/${v}" class="${v === cur ? "on" : ""}" role="tab">${t(k)}</a>`).join("")}</div>`;
}

function pageActionsHtml(view) {
  const primary = view === "events" ? `<button type="button" class="primary" id="btn-ev-add">${t("ev_add")}</button>`
    : view === "meetings" ? `<button type="button" class="primary" id="mt-add">${t("mt_add")}</button>`
    : view === "units" ? `<button type="button" class="primary" id="btn-units">${t("units_btn")}</button>`
    : "";
  return `<div class="page-actions">${primary}<div class="more">
    <button type="button" class="ghost icon-btn" id="btn-more" aria-haspopup="menu" aria-expanded="false" aria-label="${esc(t("more"))}">${icon("dots")}</button>
    <div class="more-menu" id="more-menu" role="menu" hidden>
      <button type="button" role="menuitem" id="menu-export">${t("exp_btn")}</button>
      <button type="button" role="menuitem" id="menu-reanalyze">${t("reanalyze")}</button>
      <button type="button" role="menuitem" class="danger" id="menu-delete">${t("delete_chat")}</button>
    </div></div></div>`;
}

function shell(view) {
  const b = S.board, c = b.chat;
  const range = c.first_ts ? `${fmtDate(c.first_ts, false)} – ${fmtDate(c.last_ts, false)}` : "";
  let sampleHidden = false;
  try { sampleHidden = sessionStorage.getItem("pano.sample.hide." + c.id) === "1"; } catch { /* keep it visible */ }
  const sample = c.is_sample && !sampleHidden ? `<div class="sample-banner" id="sample-banner"><span>${icon("info")} <b>${t("sample_tag")}</b> · ${t("sample_banner")}</span>
    <span class="sample-actions"><button type="button" class="ghost small" id="btn-dismiss-sample">${t("sample_hide")}</button>
    <button type="button" class="small danger" id="btn-clear-sample">${t("sample_clear")}</button></span></div>` : "";
  return `
  ${sample}
  <header class="page-head">
    <div class="page-title">
      <p class="crumb"><a href="#/c/${c.id}/overview">${esc(c.name)}</a></p>
      <h2>${esc(t(TITLE[view] || "tab_overview"))}</h2>
      <p class="meta">${c.message_count} ${t("messages")}${range ? " · " + range : ""} · ${b.members.length} ${lang === "tr" ? "kişi" : "people"}</p>
    </div>
    ${pageActionsHtml(view)}
  </header>
  ${segmentHtml(view)}
  <div id="progress-slot">${progressHtml(b.progress)}</div>
  <div id="view"></div>`;
}

function progressHtml(p) {
  if (!p || p.state === "idle" || p.state === "done") return "";
  if (p.state === "error") {
    return `<div class="progress error"><div class="progress-top"><span> ${t("analysis_error")}</span>
      <button class="small" id="btn-retry">${t("retry")}</button></div><small>${esc(p.error)}</small></div>`;
  }
  const pct = p.total ? Math.round((p.done / p.total) * 100) : 0;
  const found = I18N[lang].found;
  return `<div class="progress">
    <div class="progress-top"><span><span class="spinner"></span> ${p.state === "queued" ? t("queued") : t("analyzing")}</span>
    <span class="muted">${p.done}/${p.total} ${t("part")}</span></div>
    <div class="bar"><div style="width:${pct}%"></div></div>
    <div class="feed">${(p.found || []).slice().reverse().map(f => `<span>${f.kind === "update" ? icon("refresh") : icon("plus")} ${esc(found[f.kind] || f.kind)}: ${esc(f.text)}</span>`).join("")}</div>
  </div>`;
}

function bindShell() {
  const id = S.board.chat.id;
  const help = $("#btn-help");
  if (help) { help.textContent = t("help_btn"); help.onclick = showWelcome; }
  const clr = $("#btn-clear-sample");
  if (clr) clr.onclick = async () => {
    if (!confirm(t("sample_confirm"))) return;
    await api("/api/sample", { method: "DELETE" });
    S.seedTried = true;
    location.hash = "#/";
  };
  const hideSample = $("#btn-dismiss-sample");
  if (hideSample) hideSample.onclick = () => {
    try { sessionStorage.setItem("pano.sample.hide." + id, "1"); } catch { /* hiding still works this view */ }
    $("#sample-banner")?.remove();
  };
  document.querySelectorAll(".side-nav a, .segment a").forEach(a => a.addEventListener("click", () => { S.taskFilter = null; closeSidebar(); }));
  const more = $("#btn-more"), menu = $("#more-menu");
  if (more && menu) more.onclick = e => {
    e.stopPropagation();
    menu.hidden = !menu.hidden;
    more.setAttribute("aria-expanded", menu.hidden ? "false" : "true");
  };
  const exp = $("#menu-export");
  if (exp) exp.onclick = () => { if (menu) menu.hidden = true; showExport(); };
  const re = $("#menu-reanalyze");
  if (re) re.onclick = async () => {
    if (menu) menu.hidden = true;
    await post(`/api/chats/${id}/analyze?reset=true`);
    startPolling(id);
    render();
  };
  const del = $("#menu-delete");
  if (del) del.onclick = async () => {
    if (!confirm(t("confirm_delete"))) return;
    await api(`/api/chats/${id}`, { method: "DELETE" });
    location.hash = "#/";
  };
  const retry = $("#btn-retry");
  if (retry) retry.onclick = async () => { await post(`/api/chats/${id}/analyze`); startPolling(id); };
}

function bindDataActions() {
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
  const unitsBtn = $("#btn-units");
  if (unitsBtn) unitsBtn.onclick = manageUnits;
  $("#btn-export").onclick = showExport;
}

function showWelcome() {
  modal(`<h3>${t("wl_title")}</h3>
    <ol class="welcome">${t("wl").map(([q, a]) => `<li><b>${q}</b><p>${a}</p></li>`).join("")}</ol>
    <div class="modal-actions"><button class="primary" data-close>${t("wl_ok")}</button></div>`, m => {
    m.querySelector("[data-close]").addEventListener("click", () => {
      try { localStorage.setItem("pano.welcomed", "1"); } catch { /* optional */ }
    });
  });
}

async function manageUnits() {
  const c = S.board.chat;
  const save = async body => {
    try { await patch(`/api/chats/${c.id}`, body); await render(); manageUnits(); }
    catch (e) { toast(e.message); }
  };
  modal(`<h3>${t("units_btn")}</h3>
    <ul class="list">${c.units.map((u, n) => `<li class="unit-row"><input type="text" value="${esc(u)}" data-unit="${n}" aria-label="${esc(u)}">
      <button class="small ghost danger" data-del="${n}" aria-label="${t("del")}"></button>
      <input type="text" class="unit-members" value="${esc((c.unit_members || {})[u] || "")}" data-members="${n}" placeholder="${t("unit_members_ph")}" aria-label="${esc(u)}: ${t("unit_members_ph")}"></li>`).join("")}</ul>
    <div class="row-actions"><input type="text" id="u-new" placeholder="${t("units_add")}">
      <button class="small primary" id="u-add">${t("units_add_btn")}</button></div>
    <p class="muted">${t("units_note")}</p>
    <div class="modal-actions"><button data-close>${t("close")}</button></div>`, m => {
    m.querySelectorAll("[data-unit]").forEach(el => (el.onchange = () => {
      const old = c.units[Number(el.dataset.unit)], next = el.value.trim();
      if (next && next !== old) save({ renames: { [old]: next } }); else el.value = old;
    }));
    m.querySelectorAll("[data-members]").forEach(el => (el.onchange = () => save({ unit_members: { [c.units[Number(el.dataset.members)]]: el.value } })));
    m.querySelectorAll("[data-del]").forEach(el => (el.onclick = () => save({ units: c.units.filter((_, n) => n !== Number(el.dataset.del)) })));
    const add = () => { const v = m.querySelector("#u-new").value.trim(); if (v) save({ units: [...c.units, v] }); };
    m.querySelector("#u-add").onclick = add;
    m.querySelector("#u-new").onkeydown = e => e.key === "Enter" && add();
  });
}

// ---------------------------------------------------------------- board view
function dueChip(item, today) {
  if (!item.due) return `<span class="chip none">${t("no_due")}</span>`;
  const soon = new Date(today + "T12:00:00"); soon.setDate(soon.getDate() + 3);
  const late = item.status !== "done" && item.due < today;
  const soonish = item.status !== "done" && !late && item.due <= soon.toISOString().slice(0, 10);
  if (late) return `<span class="due late">${icon("clock")} <time>${fmtDate(item.due)}</time> <span>${t("n_late")}</span></span>`;
  if (soonish) return `<span class="chip soon">${icon("clock")} ${fmtDate(item.due)} · ${t("chip_soon")}</span>`;
  return `<span class="chip">${icon("calendar")} ${fmtDate(item.due)}</span>`;
}

function card(task, today) {
  return `<div class="card ${task.status === "done" ? "done" : ""}" data-id="${task.id}">
    <div class="card-top">
      <input type="checkbox" data-toggle="${task.id}" ${task.status === "done" ? "checked" : ""} aria-label="done">
      <span class="card-title" data-edit="${task.id}">${esc(task.title)}</span>
    </div>
    <div class="card-meta">
      ${task.owner ? `<span class="chip">${avatar(task.owner)}${esc(firstName(task.owner))}</span>` : `<span class="chip none">${t("no_owner")}</span>`}
      ${dueChip(task, today)}
      ${task.source_idx != null ? `<button class="src" data-src="${task.source_idx}" title="${t("source")}" aria-label="${t("source")}">${icon("chat")}</button>` : ""}
    </div>
  </div>`;
}

function renderBoardView() {
  const b = S.board;
  const units = [...b.chat.units];
  const F = S.taskFilter, k = b.overview.kpi, fo = b.overview.focus;
  const ids = F === "soon" ? new Set(k.upcoming_ids) : F === "overdue" ? new Set(fo.overdue.map(x => x.id))
    : F === "orphans" ? new Set(fo.orphans.map(x => x.id)) : null;
  let tasks = b.tasks.filter(x => (S.showDone || x.status !== "done") && (!S.member || x.owner === S.member));
  if (F === "open") tasks = tasks.filter(x => x.status === "open");
  else if (ids) tasks = tasks.filter(x => ids.has(x.id));
  if (tasks.some(x => !x.unit || !units.includes(x.unit))) units.push("");
  const stCols = [["overdue", lang === "tr" ? "Gecikmiş" : "Overdue", x => x.status !== "done" && x.due && x.due < b.today],
    ["open", lang === "tr" ? "Açık" : "Open", x => x.status !== "done" && !(x.due && x.due < b.today)],
    ["done", lang === "tr" ? "Tamamlandı" : "Done", x => x.status === "done"]];
  const statusHtml = stCols.map(([key, label, test]) => {
    const list = tasks.filter(test);
    return `<div class="column st-${key}"><div class="column-head"><span>${label} <span class="n">${list.length}</span></span></div>
      ${list.map(x => card(x, b.today)).join("") || `<div class="empty"><b>${t("empty_col")}</b></div>`}</div>`;
  }).join("");
  const unitCols = units.map(u => {
    const list = tasks.filter(x => (u ? x.unit === u : !x.unit || !b.chat.units.includes(x.unit)));
    return `<div class="column">
      <div class="column-head"><span>${esc(u || t("no_unit"))} <span class="n">${list.length}</span></span>
        <button class="ghost icon-btn" data-add="${esc(u)}" title="${t("add_task")}" aria-label="${t("add_task")}">${icon("plus")}</button></div>
      ${list.map(x => card(x, b.today)).join("") || `<div class="empty"><b>${t("empty_col")}</b>${t("empty_col_hint")}</div>`}
    </div>`;
  }).join("");
  const cols = S.group === "unit" ? unitCols : statusHtml;

  const m = b.missed;
  const miss = (title, list, fmt) => list.length ? `<h4>${title} (${list.length})</h4><ul class="list">${list.map(fmt).join("")}</ul>` : "";
  const srcBtn = i => i.source_idx != null ? `<button class="src" data-src="${i.source_idx}" title="${t("source")}" aria-label="${t("source")}">${icon("chat")}</button>` : "";
  const decBtns = d => (d.validity === "valid"
    ? `<button class="small ghost" data-qset="${d.id}" data-field="validity" data-st="changed">${t("val_changed")}</button><button class="small ghost" data-qset="${d.id}" data-field="validity" data-st="cancelled">${t("val_cancelled")}</button>`
    : `<button class="small ghost" data-qset="${d.id}" data-field="validity" data-st="valid">${t("val_valid_btn")}</button>`)
    + `<button class="small ghost" data-qhist="${d.id}">${t("q_hist")}</button>`;
  const closedQ = b.questions.filter(q => q.status !== "open");
  const qBtns = q => (q.status === "open" || q.status === "answered"
    ? `<button class="small ghost" data-qset="${q.id}" data-st="resolved">${t("q_resolve")}</button><button class="small ghost" data-qset="${q.id}" data-st="invalid">${t("q_invalid")}</button>`
    : `<button class="small ghost" data-qset="${q.id}" data-st="open">${t("q_reopen")}</button>`)
    + `<button class="small ghost" data-qhist="${q.id}">${t("q_hist")}</button>`;
  const taskLi = i => `<li><span class="grow"><a href="javascript:void 0" data-edit="${i.id}">${esc(i.title)}</a>
    <small>${i.owner ? esc(firstName(i.owner)) : t("no_owner")}${i.due ? " · " + fmtDate(i.due) : ""}</small></span>${srcBtn(i)}</li>`;
  const missedHtml = miss(t("m_questions"), m.questions, q => `<li><span class="grow">${esc(q.title)}
      <small>${t("asked_by")} ${esc(firstName(q.owner)) || "?"}</small></span>${srcBtn(q)}${qBtns(q)}</li>`)
    + miss(t("m_orphans"), m.orphans, taskLi) + miss(t("m_overdue"), m.overdue, taskLi) + miss(t("m_soon"), m.soon, taskLi);

  const missedN = m.questions.length + m.orphans.length + m.overdue.length + m.soon.length;
  const drawerOpen = !!($("#missed-drawer") && !$("#missed-drawer").hidden);
  const openQs = b.questions.filter(q => q.status === "open");
  const qList = items => items.map(q => `<li><span class="grow">${esc(q.title)}
        <small>${t("asked_by")} ${esc(firstName(q.owner)) || "?"} · ${esc(t("st_name")[q.status] || q.status)}</small></span>${srcBtn(q)}${qBtns(q)}</li>`).join("");
  const boardHtml = F === "questions"
    ? `<div class="column questions"><div class="column-head"><span>${t("flt_questions")} <span class="n">${openQs.length}</span></span></div>
        <ul class="list">${qList(openQs) || `<li class="muted">${t("none_yet")}</li>`}</ul></div>`
    : cols;
  const decisionsHtml = b.decisions.length ? `<ul class="list">${b.decisions.map(d =>
        `<li class="${d.validity !== "valid" ? "muted" : ""}"><input type="checkbox" data-final="${d.id}" ${d.status === "done" ? "checked" : ""} title="${t("dec_final")}" aria-label="${t("dec_final")}"><span class="grow">${d.validity !== "valid" ? `<s>${esc(d.title)}</s> <span class="chip">${esc(t("val_name")[d.validity])}</span>` : esc(d.title)}</span>${srcBtn(d)}${decBtns(d)}</li>`).join("")}</ul>`
    : `<p class="muted">${t("none_yet")}</p>`;

  $("#view").innerHTML = `
  <div class="filters board-filters">
    ${F ? `<span class="chip ai">${t("flt_label")}: ${t("flt_" + F)} <button class="small" id="clear-flt">${t("flt_clear")}</button></span>` : ""}
    <span class="segment seg-group" role="group"><button type="button" data-group="status" class="${S.group === "unit" ? "" : "on"}">${lang === "tr" ? "Duruma göre" : "By status"}</button><button type="button" data-group="unit" class="${S.group === "unit" ? "on" : ""}">${lang === "tr" ? "Komiteye göre" : "By committee"}</button></span>
    <select id="member"><option value="">${t("everyone")}</option>${b.members.map(n =>
      `<option ${n === S.member ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>
    <label><input type="checkbox" id="showdone" ${S.showDone ? "checked" : ""}> ${t("show_done")}</label>
    ${S.member ? `<button class="small" id="copy-member">${t("copy_member")(firstName(S.member))}</button>` : ""}
    <button type="button" class="primary" data-add="">${icon("plus")} ${t("add_task")}</button>
    <button type="button" class="ghost" id="btn-missed">${icon("alert")} ${t("missed")}${missedN ? ` <span class="side-count">${missedN}</span>` : ""}</button>
  </div>
  <div class="board-scroll"><div class="columns">${boardHtml}</div></div>
  <div class="drawer-back" id="drawer-back" ${drawerOpen ? "" : "hidden"}></div>
  <aside class="drawer" id="missed-drawer" aria-label="${esc(t("missed"))}" ${drawerOpen ? "" : "hidden"}>
    <div class="drawer-head"><h3>${icon("alert")} ${t("missed")}</h3>
      <button type="button" class="ghost icon-btn" id="drawer-close" aria-label="${esc(t("close"))}">${icon("close")}</button></div>
    <div class="drawer-body">
      ${missedHtml || `<p class="muted">${t("nothing_missed")}</p>`}
      ${closedQ.length ? `<details class="compact"><summary>${t("q_closed")} (${closedQ.length})</summary><ul class="list">${qList(closedQ)}</ul></details>` : ""}
      <h3>${t("decisions")}</h3>${decisionsHtml}
    </div>
  </aside>`;

  document.querySelectorAll("[data-group]").forEach(bt => (bt.onclick = () => { S.group = bt.dataset.group; renderBoardView(); }));
  $("#member").onchange = e => { S.member = e.target.value; renderBoardView(); };
  const cf = $("#clear-flt");
  if (cf) cf.onclick = () => { S.taskFilter = null; renderBoardView(); };
  const cm = $("#copy-member");
  if (cm) cm.onclick = () => copyText(memberMessage(S.member));
  $("#showdone").onchange = e => { S.showDone = e.target.checked; renderBoardView(); };
  const closeDrawer = () => { const d = $("#missed-drawer"), back = $("#drawer-back"); if (d) d.hidden = true; if (back) back.hidden = true; };
  $("#btn-missed").onclick = () => { $("#missed-drawer").hidden = false; $("#drawer-back").hidden = false; };
  $("#drawer-close").onclick = closeDrawer;
  $("#drawer-back").onclick = closeDrawer;
  const view = $("#view");
  view.querySelectorAll("[data-toggle]").forEach(el => (el.onchange = async () => {
    await patch(`/api/items/${el.dataset.toggle}`, { status: el.checked ? "done" : "open" });
    await reloadBoard();
  }));
  view.querySelectorAll("[data-edit]").forEach(el => (el.onclick = () => editTask(b.tasks.find(x => x.id === Number(el.dataset.edit)))));
  view.querySelectorAll("[data-add]").forEach(el => (el.onclick = () => editTask({ unit: el.dataset.add || null })));
  view.querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
  view.querySelectorAll("[data-final]").forEach(el => (el.onchange = async () => {
    await patch(`/api/items/${el.dataset.final}`, { status: el.checked ? "done" : "open" });
    await reloadBoard();
  }));
  view.querySelectorAll("[data-qset]").forEach(el => (el.onclick = () => setQuestionStatus(Number(el.dataset.qset), el.dataset.st, el.dataset.field || "status")));
  view.querySelectorAll("[data-qhist]").forEach(el => (el.onclick = () => showHistory(Number(el.dataset.qhist))));
  view.querySelectorAll("[data-ev-edit]").forEach(el => (el.onclick = () => editEvent(b.events.find(x => x.id === Number(el.dataset.evEdit)))));
  view.querySelectorAll("[data-ev-add]").forEach(el => (el.onclick = () => editEvent({})));
  view.querySelectorAll("[data-ev-sample]").forEach(el => (el.onclick = async () => {
    try { const r = await post(`/api/chats/${b.chat.id}/sample-event`); await reloadBoard(); showReport(r.event_id); }
    catch (e) { toast(e.message); }
  }));
}

// Question status (resolved / not valid / reopen) with an optional note; every change is kept in the item's history.
function setQuestionStatus(id, status, field = "status") {
  const q = S.board.questions.find(x => x.id === id) || S.board.decisions.find(x => x.id === id);
  modal(`<h3>${esc(t("q_close_title")(t(field === "status" ? "st_name" : "val_name")[status]))}</h3><p>${esc(q ? q.title : "")}</p>
    <label for="q-note">${t("q_note")}</label><textarea id="q-note" rows="3" maxlength="500"></textarea>
    <div class="row"><button class="ghost" data-close></button><button class="primary" id="q-save">${t("q_save")}</button></div>`, (m, close) => {
    m.querySelector("#q-save").onclick = async () => {
      try { await patch(`/api/items/${id}`, { [field]: status, note: m.querySelector("#q-note").value }); close(); await reloadBoard(); }
      catch (e) { toast(e.message); }
    };
  });
}

async function showHistory(id) {
  let h = [];
  try { h = await api(`/api/items/${id}/history`); } catch (e) { return toast(e.message); }
  const name = v => esc(t("st_name")[v] || t("val_name")[v] || v || "—");
  modal(`<h3>${t("q_hist")}</h3>${h.length ? `<ul class="list">${h.map(x => `<li><span class="grow">${esc(x.created_at.replace("T", " "))}
    <small>${x.field === "title" ? esc(x.old || "—") + " → " + esc(x.new || "—") : name(x.old) + " → " + name(x.new)}${x.note ? " · " + esc(x.note) : ""}</small></span></li>`).join("")}</ul>` : `<p class="muted">${t("q_hist_none")}</p>`}
    <div class="row"><button class="primary" data-close>OK</button></div>`);
}

// Event report. Generation is slow on a local model, so the modal shows the real elapsed time.
async function showReport(eventId) {
  const ev = S.board.events.find(x => x.id === eventId);
  let timer = null;
  const draw = (m, close, r, extra = "") => {
    const has = r && r.report;
    m.querySelector(".modal-box").innerHTML = `<h3>${t("rp_title")}: ${esc(ev ? ev.title : "")}</h3>
      <p class="muted">${t("rp_note")}</p>
      ${has ? `<p class="muted">${t(r.source === "sample" ? "rp_src_sample" : "rp_src_ai")}${r.model ? " · " + esc(r.model) : ""}</p>
        ${r.stale ? `<p> ${t("rp_stale")}</p>` : ""}<pre class="report" style="white-space:pre-wrap">${esc(r.report)}</pre>` : `<p>${t("rp_none")}</p>`}
      ${extra}
      <div id="rp-wait"></div>
      <div class="modal-actions">${has ? `<button class="ghost" id="rp-copy">${t("rp_copy")}</button>` : ""}
        <button data-close>${t("close")}</button>
        <button class="primary" id="rp-make">${has ? t("rp_remake") : t("rp_make")}</button></div>`;
    m.querySelector("[data-close]").onclick = () => { clearInterval(timer); close(); };
    const cp = m.querySelector("#rp-copy");
    if (cp) cp.onclick = () => copyText(r.report);
    m.querySelector("#rp-make").onclick = async () => {
      const t0 = Date.now(), btn = m.querySelector("#rp-make");
      btn.disabled = true;
      const wait = m.querySelector("#rp-wait");
      const tick = () => (wait.innerHTML = `<div class="progress"><div class="progress-top"><span><span class="spinner"></span> ${t("rp_wait")}</span>
        <span class="muted">${t("rp_elapsed")}: ${Math.round((Date.now() - t0) / 1000)} s</span></div></div>`);
      tick(); timer = setInterval(tick, 1000);
      try {
        const next = await post(`/api/events/${eventId}/report`);
        clearInterval(timer); draw(m, close, next);
      } catch (e) {
        clearInterval(timer);
        draw(m, close, r, `<div class="progress error"><b>${t("rp_rejected")}</b><br><small>${esc(e.message)}</small></div>`);
      }
    };
  };
  let saved = { report: null };
  try { saved = await api(`/api/events/${eventId}/report`); } catch (e) { toast(e.message); }
  modal("", (m, close) => draw(m, close, saved));
}

function editEvent(ev) {
  const b = S.board, isNew = !ev.id;
  const opt = (v, label, sel) => `<option value="${esc(v)}" ${v === sel ? "selected" : ""}>${esc(label)}</option>`;
  const num = (id, label, v, step = "1", min = "0", max = "") => `<div><label>${label}</label><input type="number" min="${min}" ${max ? `max="${max}"` : ""} step="${step}" id="${id}" value="${v ?? ""}"></div>`;
  modal(`<h3>${isNew ? t("ev_add") : t("ev_edit")}</h3>
    <label>${t("f_title")}</label><input type="text" id="v-title" value="${esc(ev.title || "")}">
    <div class="grid2">
      <div><label>${t("ev_type")}</label><input type="text" id="v-type" value="${esc(ev.event_type || "")}"></div>
      <div><label>${t("ev_phase")}</label><select id="v-phase">${Object.entries(t("ph")).map(([k, l]) => opt(k, l, ev.phase || "idea")).join("")}</select></div>
      <div><label>${t("ev_date")}</label><input type="date" id="v-due" value="${esc(ev.due || "")}"></div>
      <div><label>${t("ev_time")}</label><input type="text" id="v-time" placeholder="14:00" value="${esc(ev.time || "")}"></div>
      <div><label>${t("ev_place")}</label><input type="text" id="v-place" value="${esc(ev.place || "")}"></div>
      <div><label>${t("ev_owner")}</label><select id="v-owner">${opt("", "—", ev.owner || "")}${b.members.map(n => opt(n, n, ev.owner)).join("")}
        ${ev.owner && !b.members.includes(ev.owner) ? opt(ev.owner, ev.owner, ev.owner) : ""}</select></div>
      ${num("v-exp", t("ev_exp"), ev.attendees_expected)}${num("v-act", t("ev_act"), ev.attendees_actual)}
      ${num("v-best", t("ev_bud_est"), ev.budget_est, "any")}${num("v-bact", t("ev_bud_act"), ev.budget_actual, "any")}
      ${num("v-apps", t("ev_apps"), ev.applications)}${num("v-fbs", t("ev_fb_score"), ev.feedback_score, "0.1", "1", "5")}
    </div>
    <label>${t("ev_fb_note")}</label><input type="text" id="v-fbn" value="${esc(ev.feedback_note || "")}">
    <p class="muted small">${t("fb_note_hint")}</p>
    <div class="grid2"><div><label>${t("fb_good")}</label><textarea id="v-fbg" rows="2">${esc(ev.feedback_good || "")}</textarea></div>
      <div><label>${t("fb_bad")}</label><textarea id="v-fbb" rows="2">${esc(ev.feedback_bad || "")}</textarea></div></div>
    <label>${t("fb_comments")}</label><textarea id="v-fbc" rows="4" placeholder="${esc(t("fb_comments_ph"))}">${esc(ev.feedback_comments || "")}</textarea>
    <label>${t("ev_units")}</label>
    <div class="filters">${b.chat.units.map(u => `<label><input type="checkbox" data-vu="${esc(u)}" ${(ev.event_units || []).includes(u) ? "checked" : ""}> ${esc(u)}</label>`).join("")}</div>
    <label>${t("ev_notes")}</label><textarea id="v-notes" rows="3">${esc(ev.notes || "")}</textarea>
    ${ev.source_idx != null ? `<p><button class="ghost small" id="v-src">${t("source")}</button></p>` : ""}
    <div class="modal-actions">
      ${isNew ? "" : `<button class="danger ghost left" id="v-del">${t("del")}</button><button class="ghost" id="v-report">${t("rp_btn")}</button>`}
      <button data-close>${t("cancel")}</button><button class="primary" id="v-save">${t("save")}</button>
    </div>`, (m, close) => {
    const q = id => m.querySelector(id);
    const src = q("#v-src");
    if (src) src.onclick = () => showSource(ev.source_idx);
    const del = q("#v-del");
    if (del) del.onclick = async () => {
      await api(`/api/items/${ev.id}`, { method: "DELETE" }); close();
      if (route().view === "event") location.hash = `#/c/${b.chat.id}/events`; else reloadBoard();
    };
    const rp = q("#v-report");
    if (rp) rp.onclick = () => { close(); showReport(ev.id); };
    const n = id => (q(id).value === "" ? null : Number(q(id).value));
    q("#v-save").onclick = async () => {
      const body = {
        title: q("#v-title").value.trim(), event_type: q("#v-type").value, phase: q("#v-phase").value,
        due: q("#v-due").value, time: q("#v-time").value, place: q("#v-place").value, owner: q("#v-owner").value,
        attendees_expected: n("#v-exp"), attendees_actual: n("#v-act"), budget_est: n("#v-best"), budget_actual: n("#v-bact"),
        applications: n("#v-apps"), feedback_score: n("#v-fbs"), feedback_note: q("#v-fbn").value,
        feedback_good: q("#v-fbg").value, feedback_bad: q("#v-fbb").value, feedback_comments: q("#v-fbc").value,
        event_units: [...m.querySelectorAll("[data-vu]:checked")].map(x => x.dataset.vu), notes: q("#v-notes").value,
      };
      if (!body.title) return;
      try {
        if (isNew) await post(`/api/chats/${b.chat.id}/items`, { kind: "event", ...body });
        else await patch(`/api/items/${ev.id}`, body);
        close();
        reloadBoard();
      } catch (e) { toast(e.message); }
    };
  });
}

async function reloadBoard() {
  const { chatId, view } = route();
  await loadBoard(chatId);
  $("#progress-slot").innerHTML = progressHtml(S.board.progress);
  bindShell();
  renderSideNav();
  if (["board", "overview", "review", "events", "event", "people", "person", "units", "data"].includes(view)) VIEWS[view]();
}

// ---------------------------------------------------------------- modals
function modal(html, bind) {
  const m = $("#modal");
  const opener = document.activeElement;
  m.innerHTML = `<div class="modal-box" role="dialog" aria-modal="true">${html}</div>`;
  m.hidden = false;
  const close = () => {
    m.hidden = true; m.innerHTML = ""; document.removeEventListener("keydown", onKey);
    if (opener && opener.focus) opener.focus();  // hand the keyboard back to where the user was
  };
  const focusables = () => [...m.querySelectorAll("a[href], button:not(:disabled), input, select, textarea")];
  const onKey = e => {
    if (e.key === "Escape") return close();
    if (e.key !== "Tab") return;  // keep Tab inside the dialog
    const f = focusables();
    if (!f.length) return;
    const first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };
  document.addEventListener("keydown", onKey);
  m.onclick = e => e.target === m && close();
  m.querySelectorAll("[data-close]").forEach(b => (b.onclick = close));
  bind?.(m, close);
  if (!m.contains(document.activeElement)) (m.querySelector("button.primary") || focusables()[0])?.focus();
}

function showExport() {
  const b = S.board, id = b.chat.id;
  modal(`<h3>${t("exp_title")}</h3>
    <p class="muted">${t("exp_note")}</p>
    <label for="x-what">${t("exp_what")}</label>
    <select id="x-what"><option value="tasks">${t("exp_tasks")}</option><option value="decisions">${t("exp_decisions")}</option>
      <option value="questions">${t("exp_questions")}</option><option value="summary">${t("exp_summary")}</option></select>
    <label for="x-format">${t("exp_format")}</label>
    <select id="x-format"><option value="csv">CSV</option><option value="json">JSON</option></select>
    <div class="grid2"><div><label for="x-status">${t("exp_status")}</label>
      <select id="x-status"><option value="">${t("exp_all")}</option><option value="open">${t("exp_open")}</option><option value="done">${t("exp_done")}</option></select></div>
      <div><label for="x-owner">${t("exp_owner")}</label>
      <select id="x-owner"><option value="">${t("exp_all")}</option>${b.members.map(m => `<option>${esc(m)}</option>`).join("")}</select></div></div>
    <div class="grid2"><div><label for="x-from">${t("exp_from")}</label><input type="date" id="x-from"></div>
      <div><label for="x-to">${t("exp_to")}</label><input type="date" id="x-to"></div></div>
    <p class="muted" id="x-err" role="alert"></p>
    <div class="modal-actions"><button data-close>${t("close")}</button><button class="primary" id="x-go">${t("exp_go")}</button></div>`, (m, close) => {
    const what = $("#x-what"), fmt = $("#x-format");
    const sync = () => {
      const sum = what.value === "summary";
      fmt.disabled = sum; if (sum) fmt.value = "csv";
      $("#x-status").disabled = what.value === "decisions";
    };
    what.onchange = sync; sync();
    $("#x-go").onclick = () => {
      const from = $("#x-from").value, to = $("#x-to").value;
      if (from && to && from > to) { $("#x-err").textContent = t("exp_bad"); return; }
      const q = new URLSearchParams({ what: what.value, format: fmt.value });
      if (!$("#x-status").disabled && $("#x-status").value) q.set("status", $("#x-status").value);
      if ($("#x-owner").value) q.set("owner", $("#x-owner").value);
      if (from) q.set("date_from", from);
      if (to) q.set("date_to", to);
      const a = document.createElement("a"); a.href = `/api/chats/${id}/export?${q}`; a.download = ""; document.body.append(a); a.click(); a.remove();
      close();
    };
  });
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
      <div><label>${t("ev_link")}</label><select id="e-event">${opt("", "—", String(task.event_id ?? ""))}${b.events.map(x => opt(String(x.id), x.title, String(task.event_id ?? ""))).join("")}</select></div>
      <div><label>${t("f_status")}</label><select id="e-status">${opt("open", t("st_open"), task.status || "open")}${opt("done", t("st_done"), task.status)}</select></div>
    </div>
    ${task.source_idx != null ? `<p><button class="ghost small" id="e-src">${t("source")}</button></p>` : ""}
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
        event_id: m.querySelector("#e-event").value ? Number(m.querySelector("#e-event").value) : null,
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
          <div class="body">${m.kind === "media" ? icon("image") + " <i>media</i>" : esc(m.text)}</div></div>`).join("")}</div>
    <div class="modal-actions"><button data-close>${t("close")}</button></div>`);
  $("#hl")?.scrollIntoView({ block: "center" });
}

// ---------------------------------------------------------------- summary view
function renderReviewView() {
  const b = S.board;
  const kindIc = { task: "pin", question: "help", decision: "compass", event: "calendar" };
  const quote = src => `<blockquote class="srcbox" aria-label="${t("src_of")}">${src
    ? (src.meeting_id
      ? `<div class="srcmeta"><b> ${t("mt_src_meeting")}</b> · <a href="#/c/${b.chat.id}/meeting/${src.meeting_id}">${esc(src.meeting_title || "")}</a></div><p>${esc(src.text)}</p>`
      : `<div class="srcmeta"><b>${esc(src.sender || "")}</b> · <time>${fmtTs(src.ts)}</time></div><p>${esc(src.text)}</p>`)
    : `<span class="muted">${t("src_none")}</span>`}</blockquote>`;
  const showSrc = (idx, title) => idx != null
    ? `<button class="small" data-src="${idx}" aria-label="${t("src_show")}: ${esc(title)}">${t("src_show")}</button>` : "";
  const card = i => {
    const lbl = x => `aria-label="${x}: ${esc(i.title)}"`;
    const noSrc = i.needs_review === 1;
    return `<article class="rcard" data-id="${i.id}">
      <header><span class="chip ai">${icon("spark")} AI</span><span class="chip">${icon(kindIc[i.kind] || "pin")} ${t("k_" + i.kind)}</span>
        ${i.needs_review ? `<span class="chip overdue"> ${t(noSrc ? "no_source" : "date_unclear")}</span>` : ""}</header>
      <h4 class="rtitle">${esc(i.title)}</h4>
      ${i.owner || i.due || i.unit ? `<p class="rmeta">${[i.owner && esc(firstName(i.owner)), i.due && fmtDate(i.due), i.unit && esc(i.unit)].filter(Boolean).join(" · ")}</p>` : ""}
      ${quote(i.source)}
      <footer class="ractions">
        <button class="small primary" data-ok="${i.id}" ${lbl(t("approve"))} ${noSrc ? `disabled title="${t("approve_why_not")}"` : ""}>${t("approve")}</button>
        <button class="small" data-edit="${i.id}" ${lbl(t("edit"))}>${t("edit")}</button>
        <button class="small danger" data-no="${i.id}" ${lbl(t("reject"))}>${t("reject")}</button>
        ${showSrc(i.source_idx, i.title)}
      </footer>
      ${noSrc ? `<p class="rwhy">${t("approve_why_not")}</p>` : ""}</article>`;
  };
  const val = v => v == null || v === "" ? "—" : esc(String(v));
  const ccard = c => `<article class="rcard">
      <header><span class="chip soon">${t("change_badge")}</span></header>
      <h4 class="rtitle">${esc(c.item_title)}</h4>
      <ul class="diff">${["status", "owner", "due", "time", "place"].filter(k => k in c.new).map(k =>
        `<li>${t("f_" + k + "_l")}: ${val(c.old[k])} <b>${val(c.new[k])}</b></li>`).join("")}</ul>
      ${quote(c.source)}
      <footer class="ractions">
        <button class="small primary" data-cok="${c.id}" aria-label="${t("approve")}: ${esc(c.item_title)}">${t("approve")}</button>
        <button class="small danger" data-cno="${c.id}" aria-label="${t("reject")}: ${esc(c.item_title)}">${t("reject")}</button>
        ${showSrc(c.source_idx, c.item_title)}
      </footer></article>`;
  const empty = !b.review.length && !b.changes.length;
  $("#view").innerHTML = `<div class="narrow review">
    <p class="muted">${t("review_intro")}</p>
    ${empty ? `<div class="empty review-empty"><b>${t("review_empty_t")}</b>${t("review_empty_d")}</div>` : ""}
    ${b.changes.length ? `<h3>${t("changes_title")} <span class="n">${b.changes.length}</span></h3><div class="rgrid">${b.changes.map(ccard).join("")}</div>` : ""}
    ${b.review.length ? `<h3>${t("new_proposals")} <span class="n">${b.review.length}</span></h3><div class="rgrid">${b.review.map(card).join("")}</div>` : ""}</div>`;
  const view = $("#view");
  const decide = (id, review) => async () => {
    try { await patch(`/api/items/${id}`, { review }); await render(); } catch (e) { toast(e.message); }
  };
  const decideChange = (id, review) => async () => {
    try { await patch(`/api/changes/${id}`, { review }); await render(); } catch (e) { toast(e.message); }
  };
  view.querySelectorAll("[data-cok]").forEach(el => (el.onclick = decideChange(el.dataset.cok, "approved")));
  view.querySelectorAll("[data-cno]").forEach(el => (el.onclick = decideChange(el.dataset.cno, "rejected")));
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
    <div class="row-actions"><button class="primary" id="btn-sum"> ${t("summary_btn")}</button>
      ${cached ? `<button id="btn-copy">${t("copy")}</button>` : ""}</div>
    <div id="sum-out">${cached ? `<div class="wa"><div class="bubble mine">${waFormat(cached.text)}</div></div>` : ""}</div>
  </div>`;
  $("#btn-sum").onclick = async e => {
    e.target.disabled = true;
    $("#sum-out").innerHTML = `<p class="muted"><span class="spinner"></span> ${t("summary_wait")}</p>`;
    try {
      const r = await post(`/api/chats/${id}/summary`, { days: 7 });
      S.summary = { chatId: id, text: r.text };
      renderSummaryView();
    } catch (err) { $("#sum-out").innerHTML = `<p class="muted"> ${esc(err.message)}</p>`; e.target.disabled = false; }
  };
  $("#sum-out").querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
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
  const lines = mine.map(x => `• ${x.title}${x.due ? ` (${fmtDate(x.due)})` : ""}`);
  return [t("member_msg_head")(firstName(name)), "", ...(lines.length ? lines : [t("member_msg_empty")]), "", `_${b.chat.name} · KulüpOS_`].join("\n");
}

// WhatsApp markup preview: *bold* and _italic_
function waFormat(text) {
  return esc(text).replace(/\[#(\d+)\]/g, '<button class="small srclink" data-src="$1" aria-label="Kaynak mesaj $1">#$1</button>').replace(/\*([^*\n]+)\*/g, "<b>$1</b>").replace(/(^|\s)_([^_\n]+)_/g, "$1<i>$2</i>");
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
    } catch (e) { $("#answer").innerHTML = `<p class="muted"> ${esc(e.message)}</p>`; }
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
  const b = S.board, o = b.overview, fo = o.focus, id = b.chat.id;
  const whyTxt = c => c.why === "after_event" ? t("why_after_event")(esc(c.event)) : t("why_" + c.why);
  const stats = [
    ["overdue", fo.overdue.length, "bad", "f_overdue"],
    ["orphans", fo.orphans.length, "warn", "f_orphans"],
    ["conflicts", fo.conflicts.length, "info", "f_conflicts"],
    ["decisions", fo.decisions.length, "accent", "f_decisions"],
  ];
  const pri = [];
  fo.overdue.slice(0, 3).forEach(x => pri.push({
    html: `<a href="javascript:void 0" data-edit="${x.id}">${esc(x.title)}</a><small>${x.owner ? esc(firstName(x.owner)) : t("no_owner")} · ${fmtDate(x.due)}</small>`,
    label: t("n_late"),
  }));
  fo.orphans.filter(x => !fo.overdue.some(o => o.id === x.id)).slice(0, 3).forEach(x => pri.push({
    html: `<a href="javascript:void 0" data-edit="${x.id}">${esc(x.title)}</a><small>${x.due ? fmtDate(x.due) : t("no_due")}</small>`,
    label: t("n_orphan"),
  }));
  fo.conflicts.slice(0, 3).forEach(x => pri.push({
    html: x.kind === "task"
      ? `<a href="javascript:void 0" data-edit="${x.id}">${esc(x.title)}</a><small>${whyTxt(x)}</small>`
      : `<a href="#/c/${id}/event/${x.id}">${esc(x.title)}</a><small>${whyTxt(x)}</small>`,
    label: t("tag_conflict"),
  }));
  fo.decisions.slice(0, 3).forEach(x => pri.push({ html: esc(x.title), label: t("tag_open") }));
  const allClear = ![fo.overdue, fo.orphans, fo.conflicts, fo.decisions].some(list => list.length);
  const priHtml = allClear
    ? `<div class="empty-quiet">${icon("check")}<p>${t("ov_clear")}</p><button type="button" class="primary" id="ov-add">${t("add_task")}</button></div>`
    : `<ul class="list">${pri.map(item => `<li><span class="grow">${item.html}<span class="chip">${esc(item.label)}</span></span></li>`).join("")}</ul>
       ${fo.decisions.length ? `<p class="muted small">${t("f_decisions_hint")}</p>` : ""}
       <p class="muted"><a href="#/c/${id}/board">${t("ov_see_board")}</a></p>`;
  const eventsHtml = o.events.length
    ? `<ul class="list">${o.events.map(e => `<li><span class="grow"><a href="#/c/${id}/event/${e.id}"><b>${esc(e.title)}</b></a>
        <small>${fmtDate(e.date)}${e.place ? " · " + esc(e.place) : ""}${e.time ? " · " + esc(e.time) : ""}</small></span>
        <span class="chip">${t("k_days")(e.days)}</span></li>`).join("")}</ul>`
    : `<div class="empty-quiet">${icon("calendar")}<p>${t("none_yet")}</p><a class="btn" href="#/c/${id}/events">${t("ov_see_events")}</a></div>`;
  const ai = (b.review || []).slice(0, 4);
  const aiHtml = ai.length
    ? `<ul class="list">${ai.map(i => `<li><span class="grow"><a href="#/c/${id}/review">${esc(i.title)}</a>
        <small>${esc(t("k_" + i.kind))}</small></span><span class="chip ai">${icon("spark")} AI</span></li>`).join("")}</ul>`
    : `<div class="empty-quiet">${icon("spark")}<p>${t("ov_empty_ai")}</p><a class="btn" href="#/c/${id}/review">${t("ov_see_review")}</a></div>`;
  const TR = lang === "tr";
  const open = b.tasks.filter(x => x.status !== "done"), done = b.tasks.filter(x => x.status === "done");
  const pct = b.tasks.length ? Math.round(done.length / b.tasks.length * 100) : 0;
  const L = TR ? { hi: "Merhaba 👋", sum: (o, e, l) => `${o} açık görev · ${e} yaklaşan etkinlik · ${l} geciken iş`, prog: "Görev ilerlemesi", of: "tamamlandı",
    addT: "Görev ekle", addE: "Etkinlik ekle", prio: "Öncelikli işler", prioSub: "Önce bunlara bak", all: "Tüm görevler →", ev: "Yaklaşan etkinlikler", allE: "Tüm etkinlikler →",
    com: "Komiteler", comSub: "açık / biten görev", ai: "Yapay zekâ önerileri", aiSub: "Onayını bekliyor", review: "İncele →", view: "Görüntüle →" }
    : { hi: "Hello 👋", sum: (o, e, l) => `${o} open tasks · ${e} upcoming events · ${l} overdue`, prog: "Task progress", of: "done",
    addT: "Add task", addE: "Add event", prio: "Priorities", prioSub: "Look at these first", all: "All tasks →", ev: "Upcoming events", allE: "All events →",
    com: "Committees", comSub: "open / done tasks", ai: "AI suggestions", aiSub: "Waiting for your approval", review: "Review →", view: "View →" };
  const tones = { overdue: ["bad", "alert"], orphans: ["warn", "person"], conflicts: ["info", "calendar"], decisions: ["accent", "check"] };
  const rows = [];
  const seen = new Set();
  const addRow = (x, pill, tone, extra) => { if (x.kind && x.kind !== "task" || seen.has(x.id)) return; seen.add(x.id); rows.push({ x, pill, tone, extra }); };
  fo.overdue.forEach(x => addRow(x, t("n_late"), "bad"));
  fo.orphans.forEach(x => addRow(x, t("n_orphan"), "warn"));
  fo.conflicts.filter(x => x.kind === "task").forEach(x => addRow(x, t("tag_conflict"), "info"));
  const prioRows = rows.slice(0, 7).map(({ x, pill, tone }) => `<li class="prio-row">
      <span class="pill ${tone}">${esc(pill)}</span>
      <a class="prio-title" href="javascript:void 0" data-edit="${x.id}">${esc(x.title)}</a>
      <span class="prio-meta">${x.owner ? avatar(x.owner) + esc(firstName(x.owner)) : `<i class="muted">${t("no_owner")}</i>`}</span>
      <span class="prio-due ${tone === "bad" ? "late" : ""}">${x.due ? fmtDate(x.due) : t("no_due")}</span></li>`).join("");
  const decRows = fo.decisions.slice(0, 3).map(x => `<li class="prio-row"><span class="pill accent">${esc(t("tag_open"))}</span><span class="prio-title">${esc(x.title)}</span></li>`).join("");
  const prioBody = allClear
    ? `<div class="empty-quiet">${icon("check")}<p>${t("ov_clear")}</p><button type="button" class="primary" id="ov-add">${t("add_task")}</button></div>`
    : `<ul class="prio-list">${prioRows}${decRows}</ul><a class="more-link" href="#/c/${id}/board">${L.all}</a>`;
  const MON = TR ? ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"] : ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const evHtml = o.events.length ? `<ul class="ev-list">${o.events.map(e => { const d = new Date(e.date + "T00:00"); return `<li>
      <a class="ev-row" href="#/c/${id}/event/${e.id}"><span class="ev-date"><b>${d.getDate()}</b>${MON[d.getMonth()]}</span>
      <span class="grow"><b>${esc(e.title)}</b><small>${e.place ? esc(e.place) : ""}${e.time ? " · " + esc(e.time) : ""}</small></span>
      <span class="chip ${e.days <= 7 ? "soon" : ""}">${t("k_days")(e.days)}</span></a></li>`; }).join("")}</ul><a class="more-link" href="#/c/${id}/events">${L.allE}</a>`
    : `<div class="empty-quiet">${icon("calendar")}<p>${t("none_yet")}</p><a class="btn" href="#/c/${id}/events">${t("ov_see_events")}</a></div>`;
  const units = b.chat.units.map(u => ({ u, o: open.filter(x => x.unit === u).length, d: done.filter(x => x.unit === u).length })).filter(r => r.o + r.d);
  const comHtml = units.length ? `<ul class="com-list">${units.map(r => `<li><span class="com-name">${esc(r.u)}</span>
      <span class="com-bar"><i style="width:${Math.round(r.d / (r.o + r.d) * 100)}%"></i></span><span class="com-n">${r.o} / ${r.d}</span></li>`).join("")}</ul>` : "";
  const ai2 = (b.review || []).slice(0, 3);
  const aiHtml2 = ai2.length ? `<ul class="list">${ai2.map(i => `<li><span class="grow"><a href="#/c/${id}/review">${esc(i.title)}</a><small>${esc(t("k_" + i.kind))}</small></span><span class="chip ai">${icon("spark")} AI</span></li>`).join("")}</ul><a class="more-link" href="#/c/${id}/review">${L.review}</a>`
    : `<p class="muted small" style="margin:0">${t("ov_empty_ai")}</p>`;
  const totalHint = { overdue: TR ? "bugün öncelik" : "do first", orphans: TR ? "sorumlu ata" : "assign someone", conflicts: TR ? "tarihi kontrol et" : "check dates", decisions: TR ? "karara bağla" : "finalise" };
  $("#view").innerHTML = `
    <section class="ov-hero">
      <div><p class="ov-kicker">${L.hi}</p><h3>${esc(b.chat.name)}</h3><p class="ov-sum">${L.sum(open.length, o.events.length, fo.overdue.length)}</p>
        <div class="ov-actions"><button type="button" class="hero-btn" id="ov-add2">${icon("plus")} ${L.addT}</button><a class="hero-btn ghost" href="#/c/${id}/events">${icon("calendar")} ${L.addE}</a></div></div>
      <div class="ov-prog"><div class="ov-ring" style="--p:${pct}"><b>${pct}%</b></div><span>${L.prog}<br><small>${done.length} / ${b.tasks.length} ${L.of}</small></span></div>
    </section>
    <div class="stat-grid">${stats.map(([f, n, tone, key]) => `
      <button type="button" class="stat tone-${tone}" data-card="${f}">
        <span class="stat-ic">${icon(tones[f][1])}</span>
        <span class="num">${n}</span>
        <span class="lbl">${t(key)}</span>
        <span class="hint">${totalHint[f]} →</span>
      </button>`).join("")}</div>
    <div class="split">
      <section class="panel"><div class="panel-head"><div><h3>${L.prio}</h3><p class="muted small">${L.prioSub}</p></div></div>${prioBody}</section>
      <div class="stack">
        <section class="panel"><div class="panel-head"><h3>${L.ev}</h3></div>${evHtml}</section>
        ${comHtml ? `<section class="panel"><div class="panel-head"><div><h3>${L.com}</h3><p class="muted small">${L.comSub}</p></div></div>${comHtml}</section>` : ""}
        <section class="panel"><div class="panel-head"><div><h3>${L.ai}</h3><p class="muted small">${L.aiSub}</p></div></div>${aiHtml2}</section>
      </div>
    </div>`;
  const add2 = $("#ov-add2");
  if (add2) add2.onclick = () => editTask({});
  $("#view").querySelectorAll("[data-card]").forEach(el => {
    el.onclick = () => {
      const f = el.dataset.card;
      S.taskFilter = f === "overdue" || f === "orphans" ? f : null;
      location.hash = `#/c/${id}/board`;
    };
  });
  $("#view").querySelectorAll("[data-edit]").forEach(el => (el.onclick = () => editTask(b.tasks.find(x => x.id === Number(el.dataset.edit)))));
  const add = $("#ov-add");
  if (add) add.onclick = () => editTask({});
}

// ---------------------------------------------------------------- AI event planner
function renderPlanView() {
  const id = S.board.chat.id;
  const p = S.plan && S.plan.chatId === id ? S.plan : null;
  $("#view").innerHTML = `<div class="narrow">
    <div class="panel planner-box">
      <h3>${t("tab_plan")}</h3>
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
    } catch (err) { $("#plan-out").innerHTML = `<p class="muted"> ${esc(err.message)}</p>`; }
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
        <div class="meta">${x.unit ? `<span class="chip"> ${esc(x.unit)}</span>` : ""}
          ${x.owner ? `<span class="chip ai">${avatar(x.owner)}${esc(firstName(x.owner))} · ${t("suggested")}</span>` : `<span class="chip none">${t("no_owner")}</span>`}</div></div>
      <span class="chip">${x.due ? icon("calendar") + " " + fmtDate(x.due) : t("no_due")}</span></label>`).join("")}</div>`;
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

// ---------------------------------------------------------------- event analysis view
async function renderAnalysisView() {
  const id = S.board.chat.id;
  const view = $("#view");
  view.innerHTML = `<div class="narrow"><p class="muted"><span class="spinner"></span></p></div>`;
  let a;
  try { a = await api(`/api/chats/${id}/event-analysis`); } catch (e) { view.innerHTML = `<div class="narrow"><p class="muted"> ${esc(e.message)}</p></div>`; return; }
  if (route().view !== "analysis" || S.board.chat.id !== id) return;  // user navigated away while loading
  const no = `<span class="muted">${t("an_none")}</span>`;
  const val = (x, suffix = "") => x == null ? no : `${esc(x)}${suffix}`;
  const kpi = (l, v, sub = "") => `<div class="kpi"><div class="lbl">${l}</div><div class="val">${v}</div><div class="sub">${sub}</div></div>`;
  const ev = r => r ? `${esc(r.title)} <span class="muted">(${r.actual})</span>` : no;
  const dev = r => {
    if (r.budget_dev == null) return no;
    const sign = r.budget_dev > 0 ? "+" : "";
    return `${sign}${r.budget_dev}${r.budget_dev_pct != null ? ` <span class="muted">(${r.budget_dev_sign > 0 ? "+" : r.budget_dev_sign < 0 ? "−" : ""}${r.budget_dev_pct}%)</span>` : ""}`;
  };
  const rows = a.events.map(r => `<tr><th scope="row">${esc(r.title)}<div class="muted small">${esc(t("ph")[r.phase] || "")}</div></th>
    <td>${r.actual == null && r.expected == null ? no : `${val(r.actual)} / ${val(r.expected)}`}${r.attendance_pct != null ? ` <b>${r.attendance_pct}%</b>` : ""}</td>
    <td>${r.conversion_pct != null ? `${r.actual} / ${r.applications} <b>${r.conversion_pct}%</b>` : no}</td>
    <td>${dev(r)}</td>
    <td>${r.feedback_score != null ? `<b>${r.feedback_score}</b>/5` : no}${r.feedback_note ? `<div class="muted small">${esc(r.feedback_note)}</div>` : ""}</td></tr>`).join("");
  view.innerHTML = `<div class="narrow wide">
    <p class="muted">${t("an_intro")}</p>
    ${a.total ? `<div class="kpis">
      ${kpi(t("an_total"), a.total)}${kpi(t("an_avg_att"), val(a.avg_attendees), a.with_attendance ? `${a.with_attendance}/${a.total}` : "")}
      ${kpi(t("an_avg_rate"), val(a.avg_attendance_pct, "%"))}${kpi(t("an_avg_fb"), val(a.avg_feedback))}</div>
    <div class="grid2"><div class="card"><b>${t("an_high")}</b><p>${ev(a.highest)}</p></div>
      <div class="card"><b>${t("an_low")}</b><p>${ev(a.lowest)}</p>${!a.lowest && a.highest ? `<p class="muted small">${t("an_low_need")}</p>` : ""}</div></div>
    <h3>${t("an_committee")}</h3><p class="muted small">${t("an_committee_note")}</p>
    <ul class="list">${a.committees.map(c => `<li><span class="grow">${c.unit ? esc(c.unit) : t("an_no_unit")}</span><b>${c.events}</b></li>`).join("")}</ul>
    <h3>${t("an_per_event")}</h3>
    <div class="tscroll"><table class="atable"><thead><tr><th>${t("an_c_event")}</th><th>${t("an_c_rate")}</th><th>${t("an_c_conv")}</th><th>${t("an_c_budget")}</th><th>${t("an_c_fb")}</th></tr></thead><tbody>${rows}</tbody></table></div>
    <h3>${t("an_insight")}</h3><div id="an-insight"></div>` : `<div class="empty"><b>${t("an_empty")}</b></div>`}</div>`;
  if (!a.total) return;
  let timer = null;
  const draw = (r, extra = "") => {
    const box = $("#an-insight");
    if (!box) return;
    box.innerHTML = `${r.insight ? `<p class="muted">${t(r.source === "sample" ? "an_src_sample" : "an_src_ai")}${r.model ? " · " + esc(r.model) : ""}</p>
      ${r.stale ? `<p> ${t("an_stale")}</p>` : ""}<p class="insight">${esc(r.insight)}</p>` : `<p class="muted">${t("an_insight_none")}</p>`}
      ${extra}<div id="an-wait"></div>
      <div class="row-actions">${r.insight ? `<button class="ghost" id="an-copy">${t("rp_copy")}</button>` : ""}
        <button class="primary" id="an-make">${r.insight ? t("an_insight_re") : t("an_insight_btn")}</button></div>`;
    const cp = $("#an-copy");
    if (cp) cp.onclick = () => copyText(r.insight);
    $("#an-make").onclick = async e => {
      const t0 = Date.now(); e.target.disabled = true;
      const tick = () => { const w = $("#an-wait"); if (w) w.innerHTML = `<div class="progress"><div class="progress-top"><span><span class="spinner"></span> ${t("an_wait")}</span>
        <span class="muted">${t("rp_elapsed")}: ${Math.round((Date.now() - t0) / 1000)} s</span></div></div>`; };
      tick(); timer = setInterval(tick, 1000);
      try { const next = await post(`/api/chats/${id}/event-analysis/insight`); clearInterval(timer); draw(next); }
      catch (err) { clearInterval(timer); draw(r, `<div class="progress error"><b>${t("an_rejected")}</b><br><small>${esc(err.message)}</small></div>`); }
    };
  };
  draw(a);
}

// ---------------------------------------------------------------- events hub (list + comparison) and event page
const dash = `<span class="muted">—</span>`;

async function renderEventsView() {
  const b = S.board, id = b.chat.id, cmp = b.event_compare || [];
  const link = e => `#/c/${id}/event/${e.id}`;
  const linked = e => b.tasks.filter(x => x.event_id === e.id).length + b.decisions.filter(x => x.event_id === e.id).length;
  const list = b.events.length ? `<div class="ev-list">${b.events.map(e => {
    const n = linked(e);
    return `<a class="ev-row" href="${link(e)}">
      <span class="ev-title">${esc(e.title)}</span>
      <span class="chip">${esc(e.phase ? (t("ph")[e.phase] || e.phase) : "—")}</span>
      <span class="muted">${e.due ? fmtDate(e.due) : "—"}</span>
      <span class="muted">${e.place ? esc(e.place) : "—"}</span>
      <span class="muted">${n ? t("ev_linked")(n) : "—"}</span>
    </a>`;
  }).join("")}</div>`
    : `<div class="empty-quiet">${icon("calendar")}<p>${t("ev_none")}</p><button type="button" class="ghost" data-ev-sample>${t("ev_sample")}</button></div>`;
  const bar = pct => `<span class="meter" aria-hidden="true"><span style="width:${Math.max(0, Math.min(100, pct))}%"></span></span>`;
  const rows = cmp.map(r => `<tr><th scope="row"><a href="${link(r)}">${esc(r.title)}</a><div class="muted small">${esc(t("ph")[r.phase] || "")}${r.date ? " · " + fmtDate(r.date, false) : ""}</div></th>
    <td>${r.attendance_pct != null ? `<span class="metric"><b>${r.attendance_pct}%</b>${bar(r.attendance_pct)}</span>` : dash}</td>
    <td class="${r.late_tasks > 0 ? "num-late" : ""}">${r.late_tasks != null ? `<b>${r.late_tasks}</b> <span class="muted small">/ ${r.tasks}</span>` : dash}</td>
    <td>${r.feedback_score != null ? `<span class="chip">${r.feedback_score}/5</span>` : dash}</td></tr>`).join("");
  $("#view").innerHTML = `
    <p class="muted">${t("evs_intro")}</p>
    ${list}
    <section class="cmp">
      <h3>${t("cmp_title")}</h3>
      ${cmp.length ? `<p class="muted small">${t("cmp_note")}</p>
        <div class="tscroll"><table class="atable cmp-table"><thead><tr><th>${t("an_c_event")}</th><th>${t("cmp_att")}</th><th>${t("cmp_late")}</th><th>${t("cmp_score")}</th></tr></thead><tbody>${rows}</tbody></table></div>`
        : `<div class="empty-quiet">${icon("chart")}<p>${t("none_yet")}</p></div>`}
    </section>`;
  const add = $("#btn-ev-add");
  if (add) add.onclick = () => editEvent({});
  const view = $("#view");
  view.querySelectorAll("[data-ev-sample]").forEach(el => (el.onclick = async () => {
    try { const r = await post(`/api/chats/${id}/sample-event`); location.hash = `#/c/${id}/event/${r.event_id}`; }
    catch (e) { toast(e.message); }
  }));
}

async function renderEventView() {
  const { chatId, mid: eid } = route(), view = $("#view");
  const back = `<p><a href="#/c/${chatId}/events">${t("tab_events")}</a></p>`;
  view.innerHTML = `<div class="narrow wide">${back}<p class="muted"><span class="spinner"></span></p></div>`;
  let p;
  try { p = await api(`/api/events/${eid}/page`); }
  catch { location.hash = `#/c/${chatId}/events`; return; }
  const r = route();
  if (r.view !== "event" || r.mid !== eid) return;  // user navigated away while loading
  const ev = p.event, a = p.attendance, no = `<span class="muted">${t("an_none")}</span>`;
  const val = (x, suffix = "") => x == null || x === "" ? no : `${esc(x)}${suffix}`;
  const srcBtn = i => i.source_idx != null ? `<button class="src" data-src="${i.source_idx}" title="${t("source")}" aria-label="${t("source")}"></button>` : "";
  const none = `<p class="muted">${t("evp_none")}</p>`;
  const taskLi = x => `<li><input type="checkbox" data-toggle="${x.id}" ${x.status === "done" ? "checked" : ""} aria-label="${t("st_done")}">
    <span class="grow ${x.status === "done" ? "muted" : ""}"><a href="javascript:void 0" data-edit="${x.id}">${esc(x.title)}</a>
    <small>${x.owner ? esc(firstName(x.owner)) : t("no_owner")}</small></span>${dueChip(x, p.today)}${srcBtn(x)}</li>`;
  const decLi = d => `<li class="${d.validity !== "valid" ? "muted" : ""}"><span class="grow">${d.validity !== "valid" ? `<s>${esc(d.title)}</s> <small>${esc(t("val_name")[d.validity] || d.validity)}</small>` : esc(d.title)}</span>${srcBtn(d)}</li>`;
  const qLi = q => `<li><span class="grow">${esc(q.title)} <small>${esc(t("st_name")[q.status] || q.status)}</small></span>${srcBtn(q)}</li>`;
  const meetLi = m => `<li><span class="grow"><a href="#/c/${chatId}/meeting/${m.id}">${esc(m.title)}</a>
    <small>${m.date ? fmtDate(m.date) : t("mt_nodate")} · ${esc(t("mt_st")[m.status] || m.status)} · ${t("mt_counts")(m)}</small></span></li>`;
  const sect = (title, body, count) => `<div class="panel"><h3>${title}${count != null ? ` <span class="n">${count}</span>` : ""}</h3>${body}</div>`;
  const ul = (items, fmt) => items.length ? `<ul class="list">${items.map(fmt).join("")}</ul>` : none;
  const kv = (l, v) => `<div><label>${l}</label><div>${v}</div></div>`;
  const fbLines = (l, v) => v ? `<h4>${l}</h4><p style="white-space:pre-wrap">${esc(v)}</p>` : "";
  const hasFb = ev.feedback_score != null || ev.feedback_note || ev.feedback_good || ev.feedback_bad || ev.feedback_comments;
  const nComments = (ev.feedback_comments || "").split("\n").filter(x => x.trim()).length;
  view.innerHTML = `<div class="narrow wide">${back}
    <div class="row-actions"><h2 style="margin:0" class="grow">${esc(ev.title)}</h2><button class="ghost small" id="evp-edit"> ${t("edit")}</button></div>
    ${sect(t("evp_info"), `<div class="grid2">${kv(t("ev_date"), ev.due ? fmtDate(ev.due) : no)}${kv(t("ev_time"), val(ev.time))}${kv(t("ev_place"), val(ev.place))}
      ${kv(t("ev_owner"), val(ev.owner))}${kv(t("ev_phase"), val(t("ph")[ev.phase] || ev.phase))}${kv(t("ev_type"), val(ev.event_type))}
      ${kv(t("ev_units"), ev.event_units.length ? ev.event_units.map(esc).join(", ") : no)}</div>${ev.notes ? `<p class="muted" style="white-space:pre-wrap">${esc(ev.notes)}</p>` : ""}`)}
    ${sect(t("evp_attend"), `<div class="grid2">${kv(t("evp_applied"), val(a.applications))}${kv(t("ev_exp"), val(a.expected))}${kv(t("ev_act"), val(a.actual))}
      ${kv(t("an_c_rate"), a.attendance_pct != null ? `<b>${a.attendance_pct}%</b>` : no)}${kv(t("an_c_conv"), a.conversion_pct != null ? `<b>${a.conversion_pct}%</b>` : no)}</div>`)}
    ${sect(t("evp_tasks"), ul(p.tasks, taskLi), p.tasks.length)}
    ${sect(t("evp_decisions"), ul(p.decisions, decLi), p.decisions.length)}
    ${sect(t("evp_questions"), ul(p.questions, qLi), p.questions.length)}
    ${sect(t("evp_meetings"), `<p class="muted small">${t("evp_meet_note")}</p>${ul(p.meetings, meetLi)}`, p.meetings.length)}
    ${sect(t("evp_feedback"), hasFb ? `<div class="grid2">${kv(t("fb_score"), ev.feedback_score != null ? `<b>${ev.feedback_score}</b>/5` : no)}${kv(t("fb_count"), nComments || no)}</div>
      ${fbLines(t("ev_fb_note"), ev.feedback_note)}${fbLines(t("fb_good"), ev.feedback_good)}${fbLines(t("fb_bad"), ev.feedback_bad)}${fbLines(t("fb_comments"), ev.feedback_comments)}`
      : `<p class="muted">${t("fb_empty")}</p>`)}
    ${sect(t("rp_title"), `<div id="evp-report"></div>`)}</div>`;
  view.querySelector("#evp-edit").onclick = () => editEvent(ev);
  view.querySelectorAll("[data-toggle]").forEach(el => (el.onchange = async () => {
    await patch(`/api/items/${el.dataset.toggle}`, { status: el.checked ? "done" : "open" });
    await reloadBoard();
  }));
  view.querySelectorAll("[data-edit]").forEach(el => (el.onclick = () => editTask(p.tasks.find(x => x.id === Number(el.dataset.edit)))));
  view.querySelectorAll("[data-src]").forEach(el => (el.onclick = () => showSource(Number(el.dataset.src))));
  drawEventReport(eid, p);
}

// Inline version of the report box: same endpoints and checks as the report dialog.
function drawEventReport(eid, r, extra = "") {
  const box = $("#evp-report");
  if (!box) return;
  box.innerHTML = `<p class="muted">${t("rp_note")}</p>
    ${r.report ? `<p class="muted">${t(r.source === "sample" ? "rp_src_sample" : "rp_src_ai")}${r.model ? " · " + esc(r.model) : ""}</p>
      ${r.stale ? `<p> ${t("rp_stale")}</p>` : ""}<pre class="report" style="white-space:pre-wrap">${esc(r.report)}</pre>` : `<p>${t("rp_none")}</p>`}
    ${extra}<div id="rp-wait"></div>
    <div class="row-actions">${r.report ? `<button class="ghost" id="rp-copy">${t("rp_copy")}</button>` : ""}
      <button class="primary" id="rp-make">${r.report ? t("rp_remake") : t("rp_make")}</button></div>`;
  const cp = $("#rp-copy");
  if (cp) cp.onclick = () => copyText(r.report);
  $("#rp-make").onclick = async e => {
    const t0 = Date.now(); e.target.disabled = true;
    const tick = () => { const w = $("#rp-wait"); if (w) w.innerHTML = `<div class="progress"><div class="progress-top"><span><span class="spinner"></span> ${t("rp_wait")}</span>
      <span class="muted">${t("rp_elapsed")}: ${Math.round((Date.now() - t0) / 1000)} s</span></div></div>`; };
    tick(); const timer = setInterval(tick, 1000);
    try { const next = await post(`/api/events/${eid}/report`); clearInterval(timer); drawEventReport(eid, next); }
    catch (err) { clearInterval(timer); drawEventReport(eid, r, `<div class="progress error"><b>${t("rp_rejected")}</b><br><small>${esc(err.message)}</small></div>`); }
  };
}

// ---------------------------------------------------------------- people (derived from task owners; counts only)
async function renderPeopleView() {
  const id = S.board.chat.id, view = $("#view");
  view.innerHTML = `<div class="narrow"><p class="muted"><span class="spinner"></span></p></div>`;
  let d;
  try { d = await api(`/api/chats/${id}/people`); }
  catch (e) { view.innerHTML = `<div class="narrow"><p class="muted"> ${esc(e.message)}</p></div>`; return; }
  if (route().view !== "people" || S.board.chat.id !== id) return;
  const rows = d.people.map(p => `<tr><th scope="row"><a href="#/c/${id}/person/${encodeURIComponent(p.name)}">${avatar(p.name)} ${esc(p.name)}</a></th>
    <td>${p.committees.length ? p.committees.map(esc).join(", ") : dash}</td><td><b>${p.open}</b></td><td class="${p.late > 0 ? "num-late" : ""}">${p.late ? `<b>${p.late}</b>` : "0"}</td><td>${p.done}</td></tr>`).join("");
  view.innerHTML = `<p class="muted">${t("pp_intro")}</p><p class="muted small">${t("pp_note")}</p>
    ${d.people.length ? `<div class="tscroll wide-table"><table class="atable"><thead><tr><th>${t("pp_name")}</th><th>${t("pp_committees")}</th><th>${t("pp_open")}</th><th>${t("pp_late")}</th><th>${t("pp_done")}</th></tr></thead><tbody>${rows}</tbody></table></div>`
      : `<div class="empty-quiet">${icon("person")}<p>${t("pp_empty")}</p></div>`}`;
}

async function renderPersonView() {
  const { chatId, arg: name } = route(), view = $("#view");
  const back = `<p><a href="#/c/${chatId}/people">${t("tab_people")}</a></p>`;
  view.innerHTML = `<div class="narrow wide">${back}<p class="muted"><span class="spinner"></span></p></div>`;
  let p;
  try { p = await api(`/api/chats/${chatId}/person?name=${encodeURIComponent(name)}`); }
  catch { location.hash = `#/c/${chatId}/people`; return; }
  const r = route();
  if (r.view !== "person" || r.arg !== name) return;
  const none = `<p class="muted">${t("evp_none")}</p>`;
  const taskLi = x => `<li><input type="checkbox" data-toggle="${x.id}" ${x.status === "done" ? "checked" : ""} aria-label="${t("st_done")}">
    <span class="grow ${x.status === "done" ? "muted" : ""}"><a href="javascript:void 0" data-edit="${x.id}">${esc(x.title)}</a>
    <small>${x.unit ? esc(x.unit) : t("no_unit")}</small></span>${dueChip(x, p.today)}</li>`;
  const sect = (title, items, fmt) => `<div class="panel"><h3>${title} <span class="n">${items.length}</span></h3>${items.length ? `<ul class="list">${items.map(fmt).join("")}</ul>` : none}</div>`;
  const all = [...p.late, ...p.open, ...p.done];
  view.innerHTML = `${back}
    <h2>${avatar(p.name)} ${esc(p.name)}</h2>
    <p class="muted small">${t("pp_note")}</p>
    <div class="panel"><h3>${t("pp_committees")}</h3>${p.committees.length ? `<p>${p.committees.map(esc).join(", ")}</p>` : none}</div>
    ${sect(t("pp_late"), p.late, taskLi)}
    ${sect(t("pp_upcoming"), p.upcoming, taskLi)}
    ${sect(t("pp_undated"), p.open.filter(x => !x.due), taskLi)}
    ${sect(t("pp_done_l"), p.done, taskLi)}
    ${sect(t("pp_events"), p.events, e => `<li><span class="grow"><a href="#/c/${chatId}/event/${e.id}">${esc(e.title)}</a>
      <small>${e.due ? fmtDate(e.due) : "—"} · ${e.role.map(k => t(k === "owner" ? "pp_role_owner" : "pp_role_task")).join(", ")}</small></span></li>`)}
    ${sect(t("pp_meetings"), p.meetings, m => `<li><span class="grow"><a href="#/c/${chatId}/meeting/${m.id}">${esc(m.title)}</a>
      <small>${m.date ? fmtDate(m.date) : t("mt_nodate")} · ${esc(t("mt_st")[m.status] || m.status)}</small></span></li>`)}`;
  view.querySelectorAll("[data-toggle]").forEach(el => (el.onchange = async () => {
    await patch(`/api/items/${el.dataset.toggle}`, { status: el.checked ? "done" : "open" });
    await reloadBoard();
  }));
  view.querySelectorAll("[data-edit]").forEach(el => (el.onclick = () => editTask(all.find(x => x.id === Number(el.dataset.edit)))));
}

// ---------------------------------------------------------------- committees and import/export pages
function renderUnitsView() {
  const b = S.board, units = b.chat.units, members = b.chat.unit_members || {};
  const rows = units.map(u => {
    const tasks = b.tasks.filter(x => x.unit === u), open = tasks.filter(x => x.status === "open");
    const late = open.filter(x => x.due && x.due < b.today).length;
    const evs = b.events.filter(e => (e.event_units || []).includes(u)).length;
    const who = avatarStack(members[u]) || `<button type="button" class="ghost small" data-add-members>${t("un_add_member")}</button>`;
    return `<tr><th scope="row">${esc(u)}</th><td>${who}</td><td><b>${open.length}</b></td><td class="${late > 0 ? "num-late" : ""}">${late ? `<b>${late}</b>` : "0"}</td><td>${evs}</td></tr>`;
  }).join("");
  const loose = b.tasks.filter(x => !x.unit || !units.includes(x.unit)).length;
  $("#view").innerHTML = `<p class="muted">${t("un_intro")}</p>
    ${units.length ? `<div class="tscroll wide-table"><table class="atable"><thead><tr><th>${t("tab_units")}</th><th>${t("un_members")}</th><th>${t("pp_open")}</th><th>${t("pp_late")}</th><th>${t("tab_events")}</th></tr></thead><tbody>${rows}</tbody></table></div>`
      : `<div class="empty-quiet">${icon("people")}<p>${t("none_yet")}</p><button type="button" class="ghost" data-add-members>${t("un_add_member")}</button></div>`}
    ${loose ? `<p class="muted small">${t("un_loose")(loose)}</p>` : ""}`;
  const openMembers = () => manageUnits();
  const head = $("#btn-units");
  if (head) head.onclick = openMembers;
  $("#view").querySelectorAll("[data-add-members]").forEach(el => (el.onclick = openMembers));
}

function renderDataView() {
  const c = S.board.chat;
  $("#view").innerHTML = `<div class="narrow"><p class="muted">${t("da_intro")}</p>
    <div class="panel"><h3>${t("da_import")}</h3><p class="muted small">${t("da_import_note")}</p>
      <div class="row-actions"><button class="ghost" id="btn-add-export">${t("add_export")}</button>
      <button class="ghost" id="btn-reanalyze">${t("reanalyze")}</button>
      <a class="btn ghost" href="#/">${t("da_new")}</a></div>
      <input type="file" id="file2" accept=".txt,.zip" hidden></div>
    <div class="panel"><h3>${t("da_export")}</h3><p class="muted small">${t("da_export_note")}</p>
      <div class="row-actions"><a class="btn ghost" href="/api/chats/${c.id}/export.md" download="${esc(c.name)}.md">Markdown</a>
      <button class="ghost" id="btn-export">${t("exp_btn")}</button></div></div>
    <div class="panel"><h3>${t("da_danger")}</h3><div class="row-actions"><button class="ghost danger" id="btn-delete">${t("delete_chat")}</button></div></div></div>`;
  bindDataActions();
}

const VIEWS = { units: renderUnitsView, data: renderDataView, people: renderPeopleView, person: renderPersonView, events: renderEventsView, event: renderEventView, meetings: renderMeetingsView, meeting: renderMeetingView, analysis: renderAnalysisView, overview: renderOverview, board: renderBoardView, review: renderReviewView, plan: renderPlanView, summary: renderSummaryView, ask: renderAskView };

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
  if (!chatId && !S.chats.length && !S.seedTried) {
    S.seedTried = true;  // fresh install: open on a filled sample panel
    try {
      const r = await post("/api/seed");
      if (r.created) { location.hash = `#/c/${r.chat_id}/overview`; return; }
    } catch { /* fall through to the normal home page */ }
  }
  if (!chatId) { renderSideNav(); return renderHome(); }
  try { await loadBoard(chatId); }
  catch { location.hash = "#/"; return; }
  $("#app").innerHTML = `<section class="page">${shell(view)}</section>`;
  bindShell();
  renderSideNav();
  closeSidebar();
  (VIEWS[view] || renderOverview)();
  let welcomed = true;
  try { welcomed = !!localStorage.getItem("pano.welcomed"); } catch { /* private mode: show it */ welcomed = false; }
  if (!welcomed && view === "overview") showWelcome();
  if (["running", "queued"].includes(S.board.progress.state)) startPolling(chatId);
}

// ---------------------------------------------------------------- meetings
// Notes are untrusted data: they are shown as plain text (esc) and only reach the model as quoted data.
async function renderMeetingsView() {
  const id = S.board.chat.id;
  $("#view").innerHTML = `<p class="muted">${t("mt_intro")}</p>
    <div id="mt-list"><p class="muted"><span class="spinner"></span></p></div>`;
  const add = $("#mt-add");
  if (add) add.onclick = () => editMeeting({});
  let list = [];
  try { list = await api(`/api/chats/${id}/meetings`); } catch (e) { toast(e.message); }
  $("#mt-list").innerHTML = list.length ? `<div class="mt-list">${list.map(m => `<a class="ev-row" href="#/c/${id}/meeting/${m.id}">
      <span class="ev-title">${esc(m.title)}</span>
      ${avatarStack(m.attendees)}
      <span class="muted">${m.date ? `${fmtDate(m.date)}${m.time ? " " + esc(m.time) : ""}` : t("mt_nodate")}</span>
      <span class="chip">${esc(t("mt_st")[m.status] || m.status)}</span>
      ${m.units.map(u => `<span class="chip">${esc(u)}</span>`).join("")}
      <span class="muted">${t("mt_counts")(m)}</span></a>`).join("")}</div>`
    : `<div class="empty-quiet">${icon("people")}<p>${t("mt_empty")}</p></div>`;
}

function editMeeting(m) {
  const b = S.board, isNew = !m.id;
  let notesSource = m.notes_source || null;
  const opt = (v, label, sel) => `<option value="${esc(v)}" ${v === sel ? "selected" : ""}>${esc(label)}</option>`;
  modal(`<h3>${isNew ? t("mt_add") : t("mt_edit")}</h3>
    <label for="m-title">${t("f_title")}</label><input type="text" id="m-title" maxlength="200" value="${esc(m.title || "")}">
    <div class="grid2">
      <div><label for="m-date">${t("ev_date")}</label><input type="date" id="m-date" value="${esc(m.date || "")}"></div>
      <div><label for="m-time">${t("ev_time")}</label><input type="time" id="m-time" value="${esc(m.time || "")}"></div>
      <div><label for="m-status">${t("mt_status")}</label><select id="m-status">${Object.entries(t("mt_st")).map(([k, l]) => opt(k, l, m.status || "planned")).join("")}</select></div>
    </div>
    <p class="muted">${t("mt_date_hint")}</p>
    <label>${t("ev_units")}</label>
    <div class="filters">${b.chat.units.map(u => `<label><input type="checkbox" data-mu="${esc(u)}" ${(m.units || []).includes(u) ? "checked" : ""}> ${esc(u)}</label>`).join("")}</div>
    <label for="m-att">${t("mt_attendees")}</label>
    <input type="text" id="m-att" maxlength="2000" value="${esc(m.attendees || "")}" placeholder="${t("mt_att_ph")}">
    <p><button type="button" class="ghost small" id="m-fill">${t("mt_fill")}</button></p>
    <label for="m-agenda">${t("mt_agenda")}</label><textarea id="m-agenda" rows="3" maxlength="5000">${esc(m.agenda || "")}</textarea>
    <label for="m-notes">${t("mt_notes")}</label>
    <textarea id="m-notes" rows="8">${esc(m.notes || "")}</textarea>
    <div class="row-actions"><button type="button" class="ghost small" id="m-file-btn">${t("mt_upload")}</button>
      <input type="file" id="m-file" accept=".txt,.md,text/plain,text/markdown" hidden>
      <small class="muted" id="m-file-info">${notesSource ? icon("paperclip") + " " + esc(notesSource) : ""}</small></div>
    <p class="muted">${t("mt_notes_note")}</p>
    <div class="modal-actions"><button data-close>${t("cancel")}</button><button class="primary" id="m-save">${t("save")}</button></div>`, (mm, close) => {
    const q = id => mm.querySelector(id);
    const checked = () => [...mm.querySelectorAll("[data-mu]:checked")].map(x => x.dataset.mu);
    q("#m-fill").onclick = () => {
      const names = checked().flatMap(u => (b.chat.unit_members?.[u] || "").split(",").map(x => x.trim()).filter(Boolean));
      const have = q("#m-att").value.split(",").map(x => x.trim()).filter(Boolean);
      q("#m-att").value = [...new Set([...have, ...names])].join(", ");
      if (!names.length) toast(t("mt_no_members"));
    };
    q("#m-file-btn").onclick = () => q("#m-file").click();
    q("#m-file").onchange = async () => {
      const f = q("#m-file").files[0];
      if (!f) return;
      try {
        const r = await post(`/api/chats/${b.chat.id}/meetings/notes-file?filename=${encodeURIComponent(f.name)}`, await f.arrayBuffer());
        q("#m-notes").value = r.text;
        notesSource = f.name;
        q("#m-file-info").textContent = f.name;
      } catch (e) { toast(e.message, 6000); }
      q("#m-file").value = "";
    };
    q("#m-save").onclick = async () => {
      const body = {
        title: q("#m-title").value.trim(), date: q("#m-date").value, time: q("#m-time").value, status: q("#m-status").value,
        units: checked(), attendees: q("#m-att").value, agenda: q("#m-agenda").value, notes: q("#m-notes").value,
        notes_source: q("#m-notes").value.trim() ? notesSource : null,
      };
      if (!body.title) { q("#m-title").focus(); return; }
      try {
        const saved = isNew ? await post(`/api/chats/${b.chat.id}/meetings`, body) : await patch(`/api/meetings/${m.id}`, body);
        close();
        if (isNew) location.hash = `#/c/${b.chat.id}/meeting/${saved.id}`; else render();
      } catch (e) { toast(e.message, 6000); }
    };
  });
}

// Summary box: saved text with a real "outdated" flag, a make/remake button and the real elapsed time while the local model works.
function drawMeetingSummary(mid, r, extra, cut = false) {
  const box = $("#mt-sum"), has = r && r.summary;
  box.innerHTML = `${has ? `<p class="muted">${t(r.source === "sample" ? "mt_sum_src_sample" : "mt_sum_src_ai")}${r.model ? " · " + esc(r.model) : ""}</p>
      ${r.stale ? `<p><b>${t("mt_sum_stale")}</b></p>` : ""}${cut ? `<p class="muted">${t("mt_sum_cut")}</p>` : ""}
      <pre class="report" style="white-space:pre-wrap">${esc(r.summary).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")}</pre>` : `<p class="muted">${t("mt_sum_none")}</p>`}
    ${extra}<div id="mt-sum-wait"></div>
    <div class="row-actions">${has ? `<button class="ghost" id="mt-sum-copy">${t("mt_sum_copy")}</button>` : ""}
      <button class="primary" id="mt-sum-make">${has ? t("mt_sum_remake") : t("mt_sum_make")}</button></div>`;
  const cp = $("#mt-sum-copy");
  if (cp) cp.onclick = () => copyText(r.summary);
  $("#mt-sum-make").onclick = async e => {
    const t0 = Date.now(), wait = $("#mt-sum-wait");
    e.target.disabled = true;
    const tick = () => (wait.innerHTML = `<div class="progress"><div class="progress-top"><span><span class="spinner"></span> ${t("mt_sum_wait")}</span>
      <span class="muted">${t("mt_elapsed")}: ${Math.round((Date.now() - t0) / 1000)} s</span></div></div>`);
    tick();
    const timer = setInterval(tick, 1000);
    try {
      const next = await post(`/api/meetings/${mid}/summary`);
      clearInterval(timer);
      drawMeetingSummary(mid, next, "", next.notes_cut);
    } catch (err) {
      clearInterval(timer);
      drawMeetingSummary(mid, r, `<div class="progress error"><b>${t("mt_sum_rejected")}</b><br><small>${esc(err.message)}</small></div>`);
    }
  };
}

async function renderMeetingView() {
  const { mid } = route(), chatId = S.board.chat.id;
  let d;
  try { d = await api(`/api/meetings/${mid}`); } catch { location.hash = `#/c/${chatId}/meetings`; return; }
  try { d.summary = await api(`/api/meetings/${mid}/summary`); } catch { d.summary = null; }
  const m = d.meeting;
  const rec = (items, empty) => items.length ? `<ul class="list">${items.map(i => `<li><span class="grow">${esc(i.title)}
      <small>${[i.owner ? icon("person") + " " + esc(i.owner) : (i.kind === "task" ? t("mt_noowner") : ""), i.due ? icon("calendar") + " " + fmtDate(i.due) : ""].filter(Boolean).join(" · ")}</small></span>
      ${i.kind === "task" ? `<span class="chip ${i.status === "done" ? "" : "ai"}">${i.status === "done" ? t("n_done") : t("n_open")}</span>` : ""}</li>`).join("")}</ul>` : `<p class="muted">${empty}</p>`;
  $("#view").innerHTML = `<div class="meet-page">
    <p><a href="#/c/${chatId}/meetings">${t("tab_meetings")}</a></p>
    <h3>${esc(m.title)}</h3>
    <div class="meta">${avatarStack(m.attendees)} ${m.date ? `${fmtDate(m.date)}${m.time ? " " + esc(m.time) : ""}` : `<span class="chip none">${t("mt_nodate")}</span>`}
      <span class="chip ${m.status === "held" ? "" : "ai"}">${t("mt_st")[m.status]}</span>
      ${m.units.map(u => `<span class="chip">${esc(u)}</span>`).join("")}</div>
    ${m.attendees ? `<p><b>${t("mt_attendees")}:</b> ${esc(m.attendees)}</p>` : ""}
    ${m.agenda ? `<h4>${t("mt_agenda")}</h4><pre class="report" style="white-space:pre-wrap">${esc(m.agenda)}</pre>` : ""}
    <h4>${t("mt_notes")}${m.notes_source ? ` <small class="muted">${esc(m.notes_source)}</small>` : ""}</h4>
    ${m.notes ? `<pre class="report" style="white-space:pre-wrap">${esc(m.notes)}</pre>` : `<p class="muted">${t("mt_no_notes")}</p>`}
    <div class="row-actions"><button id="mt-edit"> ${t("mt_edit")}</button>
      ${d.lines ? `<button class="primary" id="mt-analyze">${t("mt_analyze")}</button>` : ""}
      <button class="danger ghost" id="mt-del">${t("del")}</button></div>
    <div id="mt-wait"></div>
    ${d.orphan_tasks ? `<p><span class="chip overdue">${t("mt_orphans")(d.orphan_tasks)}</span></p>` : ""}
    ${d.warnings.length ? `<div class="panel"><b> ${t("mt_warn_title")}</b><ul class="list">${d.warnings.map(w => `<li><span class="grow">${t("mt_warn")(w)}</span></li>`).join("")}</ul></div>` : ""}
    ${d.notes_changed ? `<p class="muted"> ${t("mt_an_stale")}</p>` : ""}
    ${d.proposed ? `<p><span class="chip ai">${t("mt_pending")(d.proposed)}</span> <a href="#/c/${chatId}/review">${t("mt_go_review")} </a></p>` : ""}
    <h4>${t("mt_sum_title")}</h4><p class="muted">${t("mt_sum_note")}</p>
    <div id="mt-sum"></div>
    <div id="mt-extra"></div>
    <h4>${t("mt_tasks")}</h4>${rec(d.tasks, t("mt_none"))}
    <h4>${t("mt_decisions")}</h4>${rec(d.decisions, t("mt_none"))}
    <h4>${t("mt_questions")}</h4>${rec(d.questions, t("mt_none"))}
  </div>`;
  $("#mt-edit").onclick = () => editMeeting(m);
  drawMeetingSummary(mid, d.summary, "");
  const an = $("#mt-analyze");
  if (an) an.onclick = async () => {
    const t0 = Date.now(), wait = $("#mt-wait");
    an.disabled = true;
    const tick = () => (wait.innerHTML = `<div class="progress"><div class="progress-top"><span><span class="spinner"></span> ${t("mt_an_wait")}</span>
      <span class="muted">${t("mt_elapsed")}: ${Math.round((Date.now() - t0) / 1000)} s</span></div></div>`);
    tick();
    const timer = setInterval(tick, 1000);
    try {
      const r = await post(`/api/meetings/${mid}/analyze`);
      toast(t("mt_an_done")(r), 6000);
      await render();
    } catch (e) {
      wait.innerHTML = `<div class="progress error"><b>${t("analysis_error")}</b><br><small>${esc(e.message)}</small></div>`;
      an.disabled = false;
    } finally { clearInterval(timer); }
  };
  $("#mt-del").onclick = async () => {
    if (!confirm(t("mt_confirm_del"))) return;
    await api(`/api/meetings/${mid}`, { method: "DELETE" });
    location.hash = `#/c/${chatId}/meetings`;
  };
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
$("#btn-help").textContent = t("help_btn");
$("#btn-help").onclick = showWelcome;
$("#nav-toggle").onclick = () => $("#sidebar").classList.toggle("open");
document.addEventListener("keydown", e => {
  if (e.key !== "Escape") return;
  const menu = $("#more-menu");
  if (menu && !menu.hidden) { menu.hidden = true; $("#btn-more")?.setAttribute("aria-expanded", "false"); return; }
  const drawer = $("#missed-drawer");
  if (drawer && !drawer.hidden) { drawer.hidden = true; const back = $("#drawer-back"); if (back) back.hidden = true; return; }
  closeSidebar();
});
document.addEventListener("click", e => {
  const menu = $("#more-menu");
  if (menu && !menu.hidden && !e.target.closest(".more")) { menu.hidden = true; $("#btn-more")?.setAttribute("aria-expanded", "false"); }
  const side = $("#sidebar");
  if (side && side.classList.contains("open") && !e.target.closest("#sidebar") && !e.target.closest("#nav-toggle")) side.classList.remove("open");
});
window.addEventListener("hashchange", render);

// ---- public landing + sign-in --------------------------------------------------
const PUB = {
  tr: { tag: "Öğrenci kulüpleri için · ücretsiz", h1: "Kulübün işleri dağılmasın.", lead: "Görev, etkinlik ve toplantı bilgilerini tek yerde tut, istediğin an gir. Yapay zekâ kulübünü analiz etsin: neler yapıldı, etkinlik nasıl geçti, sırada ne var. Veriler bu bilgisayarda kalır.",
        login: "Giriş yap", signup: "Kayıt ol", demo: "Demo kulübünü dene", demoNote: "Hesap gerekmez · örnek kulüp: FUB3V Yönetim 2026",
        f: [["Her şey tek yerde", "Görevler, etkinlikler, toplantılar, kişiler ve komiteler birbirine bağlı."], ["İstediğin an gir", "Toplantı sırasında not, görev veya karar ekle; yerelde kalıcı olur."], ["Yapay zekâ analizi", "Etkinlik sonuçları, haftalık özet, rapor ve gelecek plan önerisi."], ["Güvenli ve ücretsiz", "Kaynak şart, otomatik onay yok, veri bilgisayarından çıkmaz."]] },
  en: { tag: "For student clubs · free", h1: "Keep your club's work from scattering.", lead: "Keep tasks, events and meeting notes in one place and enter them any time. Let AI analyse your club: what was done, how an event went, what is next. Data stays on this computer.",
        login: "Sign in", signup: "Sign up", demo: "Try the demo club", demoNote: "No account needed · sample data: FUB3V Management 2026",
        f: [["Everything in one place", "Tasks, events, meetings, people and committees are linked."], ["Enter it any time", "Add a note, task or decision during a meeting; it is stored locally."], ["AI analysis", "Event results, weekly recap, reports and suggestions for what to plan next."], ["Safe and free", "Source required, no auto-approval, data never leaves your computer."]] },
};
const AUTH_TXT = {
  tr: { login: "Giriş yap", signup: "Kayıt ol", user: "Kullanıcı adı", pass: "Parola", back: "← Ana sayfa", logout: "Çıkış yap",
        toSignup: "Hesabın yok mu? Kayıt ol", toLogin: "Hesabın var mı? Giriş yap", note: "Veriler bu bilgisayarda kalır; yapay zekâ yerel Gemma ile çalışır." },
  en: { login: "Sign in", signup: "Sign up", user: "Username", pass: "Password", back: "← Home", logout: "Sign out",
        toSignup: "No account? Sign up", toLogin: "Have an account? Sign in", note: "Data stays on this computer; AI runs locally with Gemma." },
};
let started = false;

function showPublic() {
  document.body.classList.add("public");
  const p = PUB[lang];
  $("#app").innerHTML = `<div class="pub">
    <header class="pub-nav"><span class="brand"><span class="logo" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"></rect><rect x="14" y="3" width="7" height="7" rx="1.5"></rect><rect x="3" y="14" width="7" height="7" rx="1.5"></rect><rect x="14" y="14" width="7" height="7" rx="1.5"></rect></svg></span>KulüpOS</span>
      <span class="pub-actions"><button class="ghost" id="pub-lang" type="button">${lang === "tr" ? "EN" : "TR"}</button><button class="ghost" id="pub-login" type="button">${p.login}</button><button class="primary" id="pub-signup" type="button">${p.signup}</button></span></header>
    <section class="pub-hero"><span class="pub-tag">${p.tag}</span><h1>${p.h1}</h1><p>${p.lead}</p>
      <div class="pub-cta"><button class="primary big" id="pub-demo" type="button">${p.demo}</button><button class="ghost big" id="pub-login2" type="button">${p.login}</button></div>
      <small>${p.demoNote}</small></section>
    <section class="pub-grid">${p.f.map(([h, d]) => `<div class="pub-card"><h3>${h}</h3><p>${d}</p></div>`).join("")}</section></div>`;
  $("#pub-login").onclick = $("#pub-login2").onclick = () => showLogin(false);
  $("#pub-signup").onclick = () => showLogin(true);
  $("#pub-lang").onclick = () => { lang = lang === "tr" ? "en" : "tr"; try { localStorage.setItem("pano.lang", lang); } catch {} showPublic(); };
  $("#pub-demo").onclick = async e => {
    e.target.disabled = true;
    try {
      await post("/api/auth/guest");
      const res = await fetch("/api/demo/tr", { method: "POST" });
      if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
      const chat = await res.json();
      await boot(true);
      openChat(chat);
    } catch (err) { toast(err.message, 6000); e.target.disabled = false; }
  };
}

function showLogin(signup) {
  let box = $("#login");
  if (!box) { box = document.createElement("div"); box.id = "login"; box.className = "login"; document.body.appendChild(box); }
  const a = AUTH_TXT[lang];
  box.hidden = false;
  box.innerHTML = `<form class="login-card" id="login-form">
    <button type="button" class="linkish" id="login-back">${a.back}</button>
    <h1>${signup ? a.signup : a.login}</h1>
    <label>${a.user}<input name="u" autocomplete="username" required minlength="3" autofocus></label>
    <label>${a.pass}<input name="p" type="password" autocomplete="${signup ? "new-password" : "current-password"}" required minlength="6"></label>
    <div class="login-err" id="login-err" role="alert"></div>
    <button class="primary" type="submit">${signup ? a.signup : a.login}</button>
    <button type="button" class="linkish" id="login-switch">${signup ? a.toLogin : a.toSignup}</button>
    <p class="login-note">${a.note}</p></form>`;
  $("#login-back").onclick = () => { box.hidden = true; };
  $("#login-switch").onclick = () => showLogin(!signup);
  $("#login-form").onsubmit = async e => {
    e.preventDefault();
    const f = e.target;
    try {
      await post(signup ? "/api/auth/register" : "/api/auth/login", { username: f.u.value, password: f.p.value });
      box.hidden = true;
      boot(true);
    } catch (err) { $("#login-err").textContent = err.message; }
  };
}

async function boot(force) {
  let me = { auth: false, user: null };
  try { me = await (await fetch("/api/auth/me")).json(); } catch {}
  if (me.auth && !me.user) return showPublic();
  document.body.classList.remove("public");
  const out = $("#btn-logout");
  if (out) {
    out.hidden = !me.auth;
    out.textContent = (me.user ? me.user + " · " : "") + AUTH_TXT[lang].logout;
    out.onclick = async () => { await post("/api/auth/logout"); location.hash = "#/"; location.reload(); };
  }
  if (started) { if (!force) render(); return; }
  started = true;
  refreshHealth();
  setInterval(refreshHealth, 15000);
  render();
}
boot();
