# DURUM — KulüpRadar / KulüpOS

Güncelleme: 2026-10-17 · Kaynak: koddaki mevcut hal (`app/`, `static/`, `tests/`). Etiketler: YAPILDI · KISMEN · YOK · DOĞRULANMADI.
Doğrulama: `python -m pytest tests -q` (111 test, sahte LLM, Ollama gerekmez) · `scripts/eval_demo.py` (TR demo, 127 mesaj: **10/14, ~230 sn**; önceki koşular 7/14 ve 11/14; EN demo hiç koşulmadı) · gerçek Gemma ile elle API denemesi (analiz → öneri kuyruğu → onay → yeniden başlatma sonrası kalıcılık).
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
- Haftalık özet: "Tamamlananlar" yalnızca pencerede çözülen/kullanıcının işaretlediği görevleri alır; maddelerde kaynak mesaj bağlantısı (G14).
- Dışa aktarma: görev CSV, karar/açık soru CSV veya JSON, analiz özeti Markdown; yalnızca onaylı kayıtlar, kaynak metni korunur, `= + - @` ile başlayan hücreler `'` ile etkisizleştirilir, filtre/tarih aralığı dosyada yazar (G11).
- Etkinlik analizi: başvuru sayısı, geri bildirim puanı/notu alanları (eski veritabanları göçle), kodun hesapladığı katılım oranı / başvuru→katılım / bütçe sapması / ortalama / en yüksek-düşük / komite sayıları; eksik veri "Girilmedi"; "Dönem içgörüsü" yalnızca hesaplanan sayılardan, sayı denetimli; örnek kulüpte "gerçekleşti" etkinlik + önceden hesaplanmış içgörü (G18).
- Toplantılar (G20, ürün mesajı: "kulübün tüm işleri tek yerde", WhatsApp yalnızca girdi kaynağı):
  - Komiteye serbest metin üye listesi (yeniden adlandırma/silme ile birlikte gider) (G20a).
  - Toplantı: başlık, tarih (boş = "tarih belirsiz"), saat, komite(ler), katılımcılar, gündem, notlar, durum planlandı/yapıldı/iptal; notlar yapıştırılır veya .txt/.md yüklenir (100 KB, UTF-8/BOM'lu UTF-16, ikili/boş dosya reddi, kaydetmeden önce yalnızca doğrulanır) (G20b).
  - Notlardan görev/karar/açık soru önerisi: inceleme kuyruğu, not satırı alıntısı (uydurma gönderen/zaman yok), kaynaksız onaylanamaz, sorumlu yalnızca üye listesinde veya satırda geçiyorsa, tarih yalnızca toplantı tarihine göre çözülür (tarih yoksa çözülmez, `needs_review=2`); onaylı/reddedilmiş kayıtlarla eşleşen öneri atlanır, hiçbir kayıt ezilmez; notlar prompt'ta `<<<NOTES>>>` bloğunda "güvenilmeyen veri" olarak, işaretler taklit edilemez (G20c).
  - Toplantı özeti: yalnızca notlar + onaylı bağlı kayıtlar; sayı denetimi (G7) ve yeni isim denetimi (büyük harfli, veride olmayan kelime) → bir yeniden deneme → ret (422); geçen süre göstergesi; notlar/alanlar/onaylı kayıtlar değişince "ESKİ" (G20d).
  - Kontroller: toplantı komitesinin üye listesinde olmayan sorumlu → bilgi amaçlı uyarı (engelleme yok); toplantıdaki sorumlusuz görev sayısı; panelde "Yaklaşan toplantılar" ve "Yapıldı ama sorumlusuz görev var" kartları (G20e).
  - Örnek kulüpte 2 toplantı (yapıldı: notlar, 3 görev/2 karar/1 soru, 1 bekleyen öneri, önceden hesaplanmış özet; planlandı: 4 gün sonra); özet gerçek Gemma ile `scripts/make_sample_meeting_summary.py` ile üretildi, elle düzenlenmedi; eski örnek kulüp demo düğmesinde toplantıları kazanır (G20f).
  - Landing ve README ana mesajı değişti (G20g). "Haftalık özet / WhatsApp'a geri dön" kartı landing'den çıktı, özellik duruyor.
- Etkinlik sayfası (G21): `#/c/ID/event/EID` ve `GET /api/events/{id}/page` — bilgi, bağlı görev (gecikme işaretli), karar, açık soru, katılım (G18 verisi), geri bildirim ve rapor tek sayfada; bağlı toplantı = bu etkinliğe bağlı kayıtların geldiği toplantılar (doğrudan toplantı→etkinlik bağı yok). Geri bildirim elle girilir: puan ortalaması (1–5), katılımcı yorumları (satır başına bir yorum), iyi giden / aksayan (`feedback_*` sütunları, eski veritabanları göçle). Rapor girdisine geri bildirim eklendi (veri yoksa “Veri yok”); yorumlar güvenilmeyen veri bloğunda; rapordaki tırnak içi alıntı yorumlarda/notlarda yoksa → bir yeniden deneme → ret (422); kayıtlar değişince ESKİ. Etkinlik karşılaştırma tablosu (katılım oranı, geciken görev, puan; veri yoksa “—”) `board.event_compare` ile.
- Örnek veri (G21e): “Python Atölyesi” sabit tarihli (2026-09-26) ve geri bildirimli; raporu gerçek Gemma ile `scripts/make_sample_event_report.py` üretti (`demo/seed-report-tr.json`), elle düzenlenmedi. Bu betikten önce oluşmuş örnek kulüplerde geri bildirim/rapor YOKTUR (demo düğmesi yeni kulüp açmaz; örneği silip yeniden aç).
- Kişi sayfası (G22): `#/c/ID/people`, `person/<ad>`; `GET /api/chats/{id}/people` ve `/person?name=` — kişiler onaylı görev sahiplerinden türer (yeni tablo yok), ad büyük/küçük harf ve boşluk farkını yok sayar. Komiteler (üye listesi + görev komitesi), geciken / yaklaşan / tarihsiz açık / tamamlanan görevler, sorumlu olduğu veya görevi bağlı etkinlikler, katılımcı listesinde adı geçen toplantılar. Görev durumu/sorumlu/tarih mevcut `editTask` ve PATCH ile düzenlenir. Yalnızca sayı; “görev sayısı zorluğu yansıtmaz” notu; puan/sıralama yok.
- Menü (G23): Panel · Etkinlikler · Toplantılar · Görevler · Kişiler · Komiteler · İçe/Dışa aktar. Eski sayfalar silinmedi: Haftalık özet ve Sohbete sor → Panel sekmeleri; Etkinlik analizi ve Etkinlik planla → Etkinlikler sekmeleri; KulüpOS ve AI incelemesi → Görevler sekmeleri; eski rotalar (`#/c/ID/board` vb.) aynen çalışır. Sayfa başlığındaki dışa/içe aktar, komite, yeniden analiz, silme düğmeleri İçe/Dışa aktar ve Komiteler sayfalarına taşındı. Landing özellik kartları ve README bu yapıya uydu; README'de “Yol haritası” (hesap/roller, sistem içi mesajlaşma, toplantı ses kaydı, bütçe/sponsor takibi, dış entegrasyonlar: hiçbiri yok, planlı).
- Yerel çalışma: sunucu `127.0.0.1`, harici CDN/font yok.

- Açık soru durumu (G10): açık / cevaplandı / çözüldü / geçersiz; panoda “Çözüldü / Geçersiz / Yeniden aç” düğmeleri, isteğe bağlı not; her değişiklik `item_history`'ye yazılır (`GET /api/items/{id}/history`), “Geçmiş” penceresi. Kullanıcı kapatınca model yeniden açmaz.
- Karar durumu ve geçmişi (G12): `validity` geçerli / değişti / iptal (Kesinleşti kutusundan ayrı); değişti/iptal kararlar güncel sayı, uyarı, toplantı özeti ve etkinlik raporu girdisinden çıkar (özet “ESKİ” olur), kayıt listede üstü çizili kalır; durum ve başlık değişikliği geçmişe yazılır; dışa aktarmada son sütun `validity`.
- CI: `.github/workflows/test.yml` (push + PR, Python 3.11, sahte LLM) + README rozeti. İlk koşu GitHub'da henüz görülmedi.
- Canlı toplantı analizi (17 Ekim): `scripts/eval_meeting.py`, 2 toplantı (örnek + tuzaklı sahte not): uydurma kişi/tarih yok, 12 alıntının hepsi notta var, tuzaklar (fikir, geçmiş iş, enjeksiyon) öneri üretmedi; ama sorumlusuz görev ve üye listesinde olmayan kişinin görevi kaçtı (geri çağırma düşük), başlıklar bazen bozuk Türkçe. Ham çıktı `data/eval_runs/` (git dışı). Ayrıntı README “Known limits”.

## KISMEN
- Görev listesi: panelden filtre (açık/yaklaşan/gecikmiş/atanmamış) ve üye filtresi var; arama, sıralama, öncelik yok.
- Karar: geçmiş var; bir kararın hangi yeni kararla değiştiği bağlanmıyor (yalnızca not).
- Kanıt: tek kaynak mesaj; çoklu kaynak yok.
- Takvim: yaklaşan liste ve panel; ay/hafta görünümü, çakışma uyarısı yok.
- Yinelenenler: bulanık eşleşmeyle otomatik atlanır; kullanıcıya öneri/çelişki uyarısı yok.
- Etkinlik raporu: sayı denetimi rakam grubu düzeyinde; gerçek modelle yalnızca örnek etkinlikte denendi.
- AI değerlendirmesi: tek elle etiketli TR demo; EN kontrol listesi var ama koşulmadı.

## YOK
Toplantı: tekrarlayan toplantı, toplantıdan etkinliğe bağlama, katılım yoklaması, toplantı araması, notlardaki göreli tarihin canlı modelle doğruluk ölçümü · Kulüp profili · evrensel arama · alt görev/bağımlılık/yorum günlüğü · birimler arası görev/bekleyen yanıt · bildirim/mesajlaşma · giriş/rol sistemi (bilerek yok, sahte yetki istenmiyor) · kararı etkinliğe bağlamak için arayüz (yalnızca API).

## DOĞRULANMADI
- Toplantı ekranları (liste, form, ayrıntı, özet kutusu, panel kartları, komite üye alanı) ekranda görülmedi; yalnızca `node --check`, API testleri ve HTTP duman denemesi yapıldı.
- Toplantı analizi canlı Gemma ile yalnızca 2 kısa toplantıda denendi (bkz. YAPILDI); doğruluk oranı değil, tek örnek. Canlı modelle yalnızca örnek toplantının özeti üretildi (geçti). İsim denetimi sezgisel: cümle ortasındaki büyük harfli kelimelere bakar, iyi bir özeti reddedebilir ya da veride başka yerde geçen yanlış ismi kaçırabilir. Özet notların ilk 12.000 karakterini okur (kesilirse arayüz söyler).
- Arayüz: otomatik UI testi yok; yalnızca Chrome'da elle bakıldı. 390 px genişlik iframe ile ölçüldü, gerçek telefon denenmedi; ekran okuyucu denenmedi.
- Dışa aktarma penceresi, Etkinlik analizi ekranı ve yeni form alanları ekranda görülmedi (yalnızca `node --check` ve API testleri). Etkinlik raporunun girdisine yeni alanlar eklenmedi.
- Etkinlik formu, rapor penceresi, komite penceresi ekranda görülmedi (JS sözdizimi ve DOM/odak kontrolleri yapıldı).
- Canlı Gemma ile arayüzden uçtan uca onay akışı (API düzeyinde denendi).

- G10/G12 ekranları (düğmeler, Geçmiş penceresi, üstü çizili karar) gözle görülmedi; yalnızca `node --check`, API testleri ve HTTP duman testi. Yapay zekâ önerisi onaylanınca karar/soru başlığı değişirse (değişiklik önerisi) geçmişe yazılmaz.

- G21–G23 ekranları (etkinlik sayfası, karşılaştırma tablosu, kişi sayfası, iki katmanlı menü, Komiteler ve İçe/Dışa aktar sayfaları) gözle görülmedi. Yapılan: `node --check`, API testleri (sahte LLM), ve her görünümü canlı sunucuya karşı sahte DOM ile çizip hata / “undefined” / “NaN” arayan bir betik (TR ve EN; yerleşim, taşma, dar ekran denenmedi).
- Örnek etkinlik raporu (gerçek Gemma, 18 Ekim yeniden üretildi, elle düzenlenmedi): verisi olmayan alan/bölüm prompt'tan ve metinden çıktı, “veri yok/girilmedi/Yok” diyen satır reddedilir, ‘ortak’ denen konu en az iki farklı yorumdan alıntı ister (satır düzeyinde denetim). Son rapor temiz ama yorumları ortak konu olarak gruplamadı, yalnızca listeledi. Tırnaksız aktarım ve para birimi eklenmesi koddan denetlenmez (yalnızca prompt'ta yasak).
- Rapordaki alıntı denetimi yalnızca tırnak içi parçalara bakar; tırnaksız yorum aktarımı denetlenmez.
- Kişi eşleşmesi tam ad eşitliğidir (“Ayşe” ≠ “Ayşe Yılmaz”); toplantı katılımı serbest metin listeden gelir, gerçek yoklama değildir.
- Menü: sayfa başlığındaki eski düğmelerin yeni yerleri ve yeniden analiz / silme akışı tarayıcıda denenmedi.

## Değişmez kurallar (CLAUDE.md)
1 kaynaksız → işaretli: UYUYOR · 2 otomatik onay yok: UYUYOR · 3 uydurma yok: UYUYOR (rapor sayı denetimi kaba) · 4 geçmiş ≠ güncel: UYUYOR (değişiklik önerisi) · 5 düzeltmeler ezilmez: UYUYOR (testli) · 6 yinelenen: KISMEN · 7 hata çökertmez: UYUYOR (testli) · 8 gizlilik: KISMEN (hata mesajı ≤200 karakter model çıktısı içerebilir, yalnızca yerel DB'de) · 9 çalışmayan düğme yok: KISMEN (tüm düğmeler tek tek denenmedi) · 10 test edilmeyen hazır değil: UYUYOR · 11 mevcut yapı: UYUYOR · 12 tutarlılık: UYUYOR (pano/panel yalnızca onaylı veriden).

- 18 Ekim: “Demo kulübü aç” eski örnek kulübü (toplantı/geri bildirim/rapor eksik) silip yeniden kurar; `is_sample=0` kulüplere dokunmaz (testli, sunucuda doğrulandı). README İngilizce üstte, Türkçe altta; `SUBMISSION.md` ve `docs/screenshots/` (görseller kullanıcıdan) eklendi. `ui-redesign` dalı (başka oturum: tokenlar, kenar çubuğu, SVG ikonlar, kanban, genel bakış kartları) ve `demo-submission` main'e birleştirildi; UI değişikliği ekranda **görülmedi** (yalnızca `node --check` + testler). Rol/giriş sistemi, kanban sürükle-bırak kalıcılığı, görev detay paneli, AI sohbetin yetkili sorgusu bu oturumda yapılmadı.

- 18 Ekim (2): açılışta tanıtım sayfası (Giriş yap / Kayıt ol / Hesapsız demo); `app/auth.py`: PBKDF2 parola, HttpOnly çerez, herkes kayıt olabilir, tüm hesaplar aynı veriyi görür (kullanıcı başına veri ayrımı ve rol YOK); demo ziyaretçisi misafir oturumuyla yalnızca örnek kulübü görür (`/api/chats/{id}` ve liste süzülür; `/api/items`, `/api/events` vb. kimlikle erişim süzülmez, yerel kullanım varsayımı); PANO_AUTH=0 kapatır; testli. Demo kulübü adı FUB3V Yönetim 2026; örnekte 6 etkinlik, 27 görev, 9 karar, 6 açık soru (yeni kayıtlar elle girilmiş sayılır, sohbet kaynağı yok); dönem içgörüsü yeniden üretildi. Kenar çubuğu, kartlar, giriş ekranı için CSS cilası eklendi: **ekranda görülmedi**.

- 18 Ekim (3): `docs/KulupOS-Sunum.pdf` (8 slayt, 4 dk sunum için; kaynağı `docs/kulupos-sunum.html`, Chrome headless ile basıldı, PDF gözle kontrol edilmedi) eklendi. Görevler panosu varsayılan olarak duruma göre. `static/pitch.html` eski ve içinde “ilk kullanıcı” yer tutucusu var: sunumda KULLANMA. Son teslim 19 Ekim 09:59 (repo public + MLH formu kullanıcıda; SUBMISSION.md metinleri hazır).

- 18 Ekim (4): ürün adı KulüpOS (repo `kulupos`); anlatım “WhatsApp odaklı” değil: bilgi istendiği an elle girilir, yerelde kalır, Gemma analiz/rapor/öneri verir; WhatsApp/not yalnızca içe aktarma kaynağı. Landing, hoş geldin, README, SUBMISSION, PDF güncellendi. Ortam değişkenleri hâlâ `PANO_*` (uyumluluk için değiştirilmedi); ekranda görülmedi.

- 18 Ekim (5): Kulüp durumu, Etkinlikler (kart ızgarası), Etkinlik sayfası (başlık kartı, sayı karoları, AI raporu paneli, geri bildirim alıntıları), Kişiler (kartlar), Kişi sayfası yeniden tasarlandı; tablolar ve paneller cilalandı. Ekranda bakılanlar: landing, demo geçişi, Kulüp durumu, Etkinlikler, Etkinlik sayfası. **Bakılmayanlar:** Toplantılar, Toplantı sayfası, Kişi sayfası, Komiteler, İçe/Dışa aktar, AI incelemesi, Etkinlik analizi/planla, Haftalık özet, Sohbete sor (yalnızca ortak CSS cilası aldı). Demo: 10 etkinlik (6'sı gerçekleşti, 5'inde geri bildirim), 35 görev, 11 karar; dönem içgörüsü yeniden üretildi.

- 18 Ekim (6): giriş sonrası `#/` artık eski WhatsApp tanıtımını değil kulüp durumunu açar (yeni kulüp için `#/new`). “Sohbete sor” → “Kulüpe sor”: Gemma görev/etkinlik/geri bildirim/karar/toplantı kayıtlarından cevaplar, dayandığı kayıtları gösterir (canlı denendi: en düşük puanlı etkinlik doğru bulundu). Haftalık özet kulüp kayıtlarından yazılıyor (canlı denendi, ~70 sn). Toplantılar kart ızgarası, Toplantı sayfası yeniden tasarlandı. Ekranda bakılan: landing, Kulüp durumu, Görevler, Etkinlikler, Etkinlik sayfası, Toplantılar, Toplantı sayfası, Kişiler, Kişi sayfası, Komiteler, İncelemesi, Analiz, Planla, Haftalık özet, Kulübe sor, İçe/Dışa aktar (analiz/plan/komite/içe-dışa yalnızca CSS cilası).

## Sıradaki
Toplantıdan etkinliğe doğrudan bağlama · G13 yinelenen/çelişki önerisi · G15 EN demo analizi + eval · G16 README ekran görüntüleri · G17 sunum. (Ayrıntı: yerel `PLAN.md`, repoda yok.)
