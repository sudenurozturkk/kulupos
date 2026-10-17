# KulüpRadar (KulüpOS) — çalışma kuralları

Kaynaklar: `OZELLIKLER.md` (katalog), `DURUM.md` (mevcut durum), `PLAN.md` (görev sırası). Yerel Gemma 4 (Ollama, `gemma4:e4b`), FastAPI + SQLite + sade JS.

## Değişmez kurallar (OZELLIKLER Bölüm 17)
1. Kaynak mesajı olmayan AI kaydı kesin sayılmaz; incelemeye işaretlenir.
2. AI önerisi otomatik onaylanmaz; onay bekleyenler ayrı tutulur.
3. Bilinmeyeni uydurma: sorumlu/tarih/birim/etkinlik boş kalabilir. Raporlar yalnızca girilmiş veriden üretilir.
4. Mesaj geçmişi ile güncel durum ayrı; eski değer güncel gibi gösterilmez.
5. Kullanıcı düzeltmeleri sonraki analizlerce ezilmez.
6. Yinelenenler denetlenir; belirsizde otomatik birleştirme yok, kullanıcıya öner.
7. Dosya/model/DB hatası uygulamayı çökertmez, kullanıcıya anlaşılır mesaj.
8. Gizlilik: veri uzak servise gitmez, günlüğe mesaj metni yazılmaz, sahte demo verisi dışında gerçek sohbet repoya girmez.
9. Çalışmayan düğme, sahte istatistik yok. 10. Test edilmeyen şey "hazır" denmez; eksikler açıkça yazılır.
11. Mevcut yapı korunur. 12. Görev/karar/etkinlik/birim aynı veriyi tutarlı gösterir.
Rol/yetki sistemi kurma (sahte yetki yok). İstisna: kullanıcının isteğiyle tek yerel hesap + giriş/çıkış (`app/auth.py`, PANO_AUTH=0 kapatır) var; roller yok.

## Token kuralları
- Tek seferde tek görev (PLAN.md'deki G numarası). Büyük refactor ve baştan yazım yok.
- Mevcut dosya yapısını ve adlandırmayı koru; yeni bağımlılık ekleme.
- Tarayıcı veya ekran görüntüsü ile kontrol yok; arayüze kullanıcı bakar.
- Uzun log/çıktı okuma; `tail`/`grep` ile sınırla. Dosyayı baştan sona okuma, ilgili bölüme bak.
- Sadece ilgili testi çalıştır (`pytest tests/test_x.py`); Gemma'yı gerekmedikçe çağırma (sahte LLM kullan, canlı analiz ~6 dk).
- Sunucu: `python -m app` (port 8000 takılıysa `PANO_PORT=8010`).
- Commit mesajı kısa; push yalnızca kullanıcı isterse.
- İş bitince dur; en çok 5 satır özet ver (ne değişti, hangi test geçti, bilinen eksik).
