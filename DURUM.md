# DURUM — OZELLIKLER.md'ye göre mevcut kod (17 Ekim, ~20:45)

Etiketler: YAPILDI · KISMEN · YOK · BOZUK · DOĞRULANMADI. Doğrulama: `pytest` (7 test geçti, sadece parser), `scripts/eval_demo.py` (TR demo 10–11/14), elle API testi (özet, sor, plan çalıştı).
Yapı: `app/` (parser, db, llm, analyzer, assistant, insights, main), `static/` (tek sayfa JS), `scripts/eval_demo.py`, `tests/test_parser.py`, `demo/` (TR + EN sahte sohbet).

## P0
- 3.1 Dosya yükleme — KISMEN: .txt/.zip + sürükle-bırak var (`main.py:upload`, `app.js:upload`). Boş/geçersiz dosya reddi var (gönderen bulunamazsa 400). Boyut sınırı YOK, ön izleme YOK, tekrar yükleme uyarısı YOK, iptal YOK.
- 3.2 WhatsApp ayrıştırıcı — KISMEN: Android/iOS, TR/EN, çok satırlı, sistem/medya/silinmiş ayrımı, 12/24 saat (`parser.py`, 7 test). Ayrıştırılamayan satırları RAPORLAMA YOK; kaç mesaj okundu bilgisi sadece toplam sayı.
- 4.1 Bilgi türleri (görev/karar/soru/etkinlik) — YAPILDI: `analyzer.py` SCHEMA; eval 10–11/14.
- 4.2 Görev çıkarma alanları — KISMEN: başlık, sorumlu, birim, son tarih, kaynak, durum var. Açıklama, öncelik, etkinlik bağı, bağımlılık, belirsizlik işareti, onay durumu YOK.
- 4.3 Karar kaydı — KISMEN: kısa karar + kaynak mesaj var; durum/geçmiş/önceki karar ilişkisi YOK.
- 4.5 Tarih yönetimi — KISMEN: modele takvim verilir, `valid_date` aralığı doğrular. Belirsiz/çelişkili tarih işaretleme YOK; "12/11" belirsizliği işaretlenmiyor.
- 4.6 Kanıt — KISMEN: her kartta tek kaynak mesaj + çevresi (`/messages`). Kaynaksız çıkarım işaretlenmiyor (`source_idx` NULL kalabilir); çoklu kaynak YOK.
- 4.7 Yerel model/hata toleransı — KISMEN: `llm.health`, Ollama model seçimi (`PANO_MODEL`), bozuk JSON'da 1 yeniden deneme, 30'luk pencere, ilerleme. Model sürümü kaydı YOK, analiz iptali YOK. Ollama kapalıyken davranış DOĞRULANMADI. Yarıda kalan analiz sunucu yeniden başlayınca "analyzing" takılabilir: DOĞRULANMADI.
- 5.1 Görev listesi — KISMEN: birim sütunlu pano, üye filtresi, elle ekle/düzenle/sil, bitti işaretleme. Arama, sıralama, durum/öncelik filtresi, görev geçmişi YOK.
- Öneri → onay/düzenle/reddet akışı (15.3 adım 8) — YOK: AI çıktısı doğrudan "open" kayıt oluyor. En büyük P0 eksiği.
- Kalıcı saklama — YAPILDI: SQLite `data/pano.db`, sunucu yeniden başlayınca veri duruyor.
- 11.1 Yerel çalışma — YAPILDI: sunucu 127.0.0.1, CDN yok, grup silme (`DELETE /api/chats`). Silme kapsamı açıklaması YOK; hata günlüğüne mesaj sızması DOĞRULANMADI (hata metni modelin ilk 200 karakterini içerebilir).
- 12.1 İlk kullanım akışı — KISMEN: ana sayfa, demo butonu, dışa aktarma adımları, gizlilik notu var. Açılışta dolu panel YOK (kullanıcı butona basıyor).
- 8.1 Kontrol paneli — KISMEN: `insights.overview` + "Kulüp durumu" (KPI, birim sağlığı, risk, iş yükü, yaklaşan). "AI incelemesi", "bugün ilgilenilecekler", "son içe aktarımlar" bölümleri YOK.
- 15.1 Parser testleri — KISMEN: 7 test; boş dosya, çok büyük dosya, hatalı satır, tekrar yükleme YOK.
- 15.2 AI testleri — KISMEN: `eval_demo.py` (TR 14, EN 13 kontrol; EN hiç çalıştırılmadı). Bozuk JSON testi YOK.
- 15.3 Uçtan uca test — YOK: otomatik test yok; akış elle denendi.
- Model kapalı hata yönetimi — DOĞRULANMADI: rozet + `LLMError` var, Ollama durdurulup denenmedi.
- README / lisans — YAPILDI. Demo/teslim materyalleri — KISMEN: ekran görüntüsü yok, DEV yazısı yok, `static/pitch.html` taslak (commit dışı).

## P1
- 2.1 Kulüp profili — YOK (yalnızca grup adı). 2.2 Birim yönetimi — KISMEN: birimler yüklemede girilir, `PATCH /api/chats` var, arayüzde düzenleme YOK. 2.3 Roller — YOK (kasıtlı, 2.3).
- 3.3 İçe aktarım geçmişi — KISMEN: grup listesi, durum, yeni dışa aktarım ekleme (`/import`, yalnızca yeni mesajlar). Dosya parmak izi YOK.
- 4.4 Açık soru takibi — KISMEN: model "cevaplandı" işaretliyor; kullanıcı "çözüldü/geçersiz" düğmesi YOK.
- 5.5 Alt görev/bağımlılık — YOK. 5.6 Yorum/etkinlik günlüğü — YOK.
- 6.1 Etkinlik kaydı — KISMEN: sohbetten ad/tarih/saat/mekân; elle form, tür, durum, katılımcı, bütçe YOK.
- 6.2 Hazırlık listesi — KISMEN: `insights.plan_event` AI plan önerir, seçilenleri panoya ekler (şablon kaydı YOK).
- 6.3 Takvim — KISMEN: "yaklaşan tarihler" zaman çizelgesi; ay/hafta görünümü, çakışma uyarısı YOK.
- 7.1/7.2 Birimler arası görev/bekleyen yanıt — YOK (görev tek birime bağlı).
- 9.1 Evrensel arama — YOK. 9.3 Yinelenen/çelişki — KISMEN: bulanık eşleşmeyle otomatik atlama var, kullanıcıya öneri/çelişki uyarısı YOK.
- 10.1 Temel raporlar — KISMEN: haftalık özet. 10.2 Dışa aktarma — KISMEN: Markdown var, CSV/JSON YOK.
- 13.1 Konuşma özeti — KISMEN: haftalık özet çalışıyor (32 sn); maddelerde kaynak bağlantısı YOK. BOZUK: "Tamamlananlar" `resolved_idx` boş görevleri de alıyor (`assistant.py`).
- Komiteler (varsayılan 4 + düzenleme) — YOK: varsayılan birimler Yönetim/Etkinlik/Sosyal Medya/Sponsorluk/Teknik.
- Başkan paneli, etkinlik raporu (yalnızca girilen veriden) — YOK.

## P2 (tek satır)
Sohbete sor (`assistant.ask`) ve iş yükü görünümü KISMEN var; sohbet karşılaştırma, özel iş akışları, bildirim, mesajlaşma YOK.

## Bölüm 17 — 12 değişmez kural
1. Kaynaksız kayıt yok — UYMUYOR (kaynaksız kayıt işaretlenmiyor).
2. AI otomatik onaylanmaz — UYMUYOR (her şey doğrudan açık görev).
3. Belirsiz bilgi uydurulmaz — KISMEN (boş sorumlu/tarih bırakılıyor; plan önerisi AI üretimi ama onay yok).
4. Geçmiş ≠ güncel durum — UYMUYOR (etkinlik tarihi güncellenince eski değer saklanmıyor).
5. Kullanıcı düzeltmeleri korunur — UYUYOR (`user_edited`, analyzer atlıyor; test YOK).
6. Yinelenenler denetlenir — UYMUYOR (sessiz otomatik atlama, kullanıcıya gösterilmiyor).
7. Hata yönetimi — KISMEN UYUYOR (analiz hatası UI'da; DB/dosya/model-kapalı DOĞRULANMADI).
8. Gizlilik — UYUYOR.
9. Görünen her işlev çalışır — UYUYOR (tüm düğmeler tek tek DOĞRULANMADI).
10. Test edilmeyen hazır sayılmaz — KISMEN (README sınırları yazıyor; E2E test yok).
11. Yapı korunur — UYUYOR.
12. Tutarlılık — KISMEN UYUYOR (özet "Tamamlananlar" hatası).

## Bilinen ortam sorunları
Port 8000'i ölü bir süreç tutuyor (8010 kullanılıyor). Gemma 4 E4B bu laptopta (RTX 3050 4 GB) ~5 token/sn: 127 mesajlık analiz ~6 dk, plan ~75 sn.

## Sayım
P0: YAPILDI 3 · KISMEN 11 · YOK 2 · BOZUK 0 · DOĞRULANMADI 1 (model kapalı).
P1: YAPILDI 0 · KISMEN 11 · YOK 8 · BOZUK 1 (özet "Tamamlananlar").
