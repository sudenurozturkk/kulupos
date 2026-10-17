# DURUM — KulüpRadar / Pano

Güncelleme: 2026-10-17 · Kaynak: koddaki mevcut hal (`app/`, `static/`, `tests/`). Etiketler: YAPILDI · KISMEN · YOK · DOĞRULANMADI.
Doğrulama: `python -m pytest tests -q` (42 test, sahte LLM, Ollama gerekmez) · `scripts/eval_demo.py` (TR demo, 127 mesaj: **10/14, ~230 sn**; önceki koşular 7/14 ve 11/14; EN demo hiç koşulmadı) · gerçek Gemma ile elle API denemesi (analiz → öneri kuyruğu → onay → yeniden başlatma sonrası kalıcılık).
Donanım notu: Gemma 4 e4b, RTX 3050 4 GB laptopta ~4 dk / 127 mesaj; bu yüzden örnek veri ve önceden hesaplanmış örnek rapor var.

## YAPILDI (testli)
- Dosya yükleme: .txt/.zip, 5 MB sınırı, boş dosya reddi, SHA-256 ile "daha önce içe aktarıldı" uyarısı, `/api/preview` ön izleme (mesaj sayısı, tarih aralığı, gönderenler, atlanan satır).
- Ayrıştırıcı: Android/iOS, TR/EN, çok satırlı, sistem/medya/silinmiş ayrımı, geçersiz tarih çökmez.
- Öneri → onay: AI kayıtları `proposed`; yalnızca onaylılar pano/sayı/özette. Onayla/Düzenle/Reddet, reddedilen geri gelmez (G1).
- Değişiklik önerisi: AI, onaylı kaydı doğrudan değiştirmez; eski → yeni değer + kaynakla kuyruğa girer (G1b).
- Kaynaksız / tarihi belirsiz bayrağı; kaynaksız öneri onaylanamaz (G2).
- Hata dayanıklılığı: Ollama kapalı, bozuk JSON, yarım kalan analiz → anlaşılır hata, "tekrar dene" kaldığı yerden devam eder (G4).
- Komiteler: ekle / yeniden adlandır (görevler korunur) / sil (görevler "Komitesiz"e); modele giden liste güncel (G5).
- Etkinlik kaydı (elle): tür, durum, tarih/saat/mekân, sorumlu, komiteler, katılımcı, bütçe, notlar; görev/karar bağlantısı API'de (G6).
- Etkinlik raporu: yalnızca girilen veriden, boş alan "Girilmedi", veride olmayan sayı → ret; örnek etkinlik için hazır rapor (G7).
- Ana panel (OZELLIKLER 8): filtreli listeye giden kartlar, AI önerisi gerçek görev sayısından ayrı, "bugün ilgilenilecekler", komite iş yükü, yaklaşan etkinlikler, son içe aktarımlar; veri yoksa "—" (G8a).
- İlk açılış: boş veritabanında sahte örnek panel ("Örnek veri", tek tıkla temizlenir, geri gelmez); 6 soruluk karşılama (G8a).
- Tasarım: tek açık tema, CSS değişkenleri, metinli rozetler, kaynak alıntılı inceleme kartları, diyalog odak yönetimi (G8b/c).
- Yerel çalışma: sunucu `127.0.0.1`, harici CDN/font yok.

## KISMEN
- Görev listesi: panelden filtre (açık/yaklaşan/gecikmiş/atanmamış) ve üye filtresi var; arama, sıralama, öncelik yok.
- Karar: "Kesinleşti" kutusu var; geçmiş ve önceki karar ilişkisi yok.
- Açık soru: model "cevaplandı" işaretler (artık öneri olarak); kullanıcı "çözüldü/geçersiz" düğmesi yok.
- Kanıt: tek kaynak mesaj; çoklu kaynak yok.
- Takvim: yaklaşan liste ve panel; ay/hafta görünümü, çakışma uyarısı yok.
- Haftalık özet: çalışıyor; maddelerde kaynak bağlantısı yok. Eski notta "Tamamlananlar" hatası vardı, yeniden kontrol edilmedi.
- Dışa aktarma: yalnızca Markdown (CSV/JSON yok).
- Yinelenenler: bulanık eşleşmeyle otomatik atlanır; kullanıcıya öneri/çelişki uyarısı yok.
- Etkinlik raporu: sayı denetimi rakam grubu düzeyinde; gerçek modelle yalnızca örnek etkinlikte denendi.
- AI değerlendirmesi: tek elle etiketli TR demo; EN kontrol listesi var ama koşulmadı.

## YOK
Kulüp profili · evrensel arama · alt görev/bağımlılık/yorum günlüğü · birimler arası görev/bekleyen yanıt · bildirim/mesajlaşma · giriş/rol sistemi (bilerek yok, sahte yetki istenmiyor) · kararı etkinliğe bağlamak için arayüz (yalnızca API).

## DOĞRULANMADI
- Arayüz: otomatik UI testi yok; yalnızca Chrome'da elle bakıldı. 390 px genişlik iframe ile ölçüldü, gerçek telefon denenmedi; ekran okuyucu denenmedi.
- Etkinlik formu, rapor penceresi, komite penceresi ekranda görülmedi (JS sözdizimi ve DOM/odak kontrolleri yapıldı).
- Canlı Gemma ile arayüzden uçtan uca onay akışı (API düzeyinde denendi).

## Değişmez kurallar (CLAUDE.md)
1 kaynaksız → işaretli: UYUYOR · 2 otomatik onay yok: UYUYOR · 3 uydurma yok: UYUYOR (rapor sayı denetimi kaba) · 4 geçmiş ≠ güncel: UYUYOR (değişiklik önerisi) · 5 düzeltmeler ezilmez: UYUYOR (testli) · 6 yinelenen: KISMEN · 7 hata çökertmez: UYUYOR (testli) · 8 gizlilik: KISMEN (hata mesajı ≤200 karakter model çıktısı içerebilir, yalnızca yerel DB'de) · 9 çalışmayan düğme yok: KISMEN (tüm düğmeler tek tek denenmedi) · 10 test edilmeyen hazır değil: UYUYOR · 11 mevcut yapı: UYUYOR · 12 tutarlılık: UYUYOR (pano/panel yalnızca onaylı veriden).

## Sıradaki
G10 soru "çözüldü/geçersiz" · G11 CSV/JSON dışa aktarma · G12 karar durumu ve geçmiş · G13 yinelenen/çelişki önerisi · G14 haftalık özet düzeltmesi (+kaynak bağlantısı) · G15 EN demo analizi + eval · G16 README ekran görüntüleri · G17 sunum. (Ayrıntı: yerel `PLAN.md`, repoda yok.)
