# KulüpRadar — Uygulamanın kapsamlı özellik ve işlev tasarımı

Bence KulüpRadar'ı yalnızca WhatsApp mesajlarından görev çıkaran bir yapay zekâ aracı olarak düşünmemeliyiz. Bir öğrenci kulübünün iletişim karmaşasını, kararlarını, görevlerini, etkinliklerini ve sorumluluklarını düzenli bir çalışma sistemine dönüştüren; yerel yapay zekâ destekli, açık kaynaklı bir organizasyon asistanı olarak tasarlamalıyız.

Ancak kapsamı mantıklı kurmak önemli: Her özelliği eklemek, her özelliği doğru yapmak anlamına gelmez. Birimler arası ilişkiler, yetkiler, veri modeli, hata durumları ve kullanıcı onayı baştan tasarlanmalı. Özellikle yapay zekâ, konuşmada geçmeyen bir görevi, tarihi veya sorumluyu kesin bilgiymiş gibi üretmemeli.

Aşağıdaki tasarımda üç seviye kullanacağım:

- P0 — Temel: İlk sürümün güvenilir biçimde çalışması için gerekli.
- P1 — Güçlendirme: Ürünü daha kullanışlı ve profesyonel yapacak özellikler.
- P2 — İleri seviye: Temel sistem doğrulandıktan sonra eklenmesi gereken gelişmiş yetenekler.

Bunlar ayrı ayrı bağımsız özellikler değil; birbirine bağlı modüller. Örneğin bir WhatsApp mesajından çıkarılan görev, onaylandığında ilgili birime, sorumluya, etkinliğe ve takvime bağlanabilmeli.

## 1. Uygulamanın temel mantığı

1\. Veri içe aktarımı

Kullanıcı WhatsApp konuşmasını dışa aktarır ve `.txt` dosyasını uygulamaya ekler.

2\. Mesajları anlama

Mesajlar ayrıştırılır; tarihler, gönderenler, konuşma sırası ve mesaj kanıtları korunur.

3\. Yerel yapay zekâ analizi

Görevler, kararlar, açık sorular, etkinlik bilgileri ve belirsizlikler tespit edilir.

4\. İnsan kontrolü

Kullanıcı sonuçları kanıt mesajlarıyla inceler; onaylar, düzenler veya reddeder.

5\. Organizasyon paneli

Onaylanan bilgiler görevlerde, etkinliklerde, birimlerde, karar kayıtlarında ve raporlarda kullanılır.

Bu akışta çok önemli bir ayrım var: Mesaj, yapay zekâ önerisi ve onaylanmış kayıt aynı şey değildir. Sistem bu üç durumu ayrı tutmalı. Böylece hatalı bir çıkarım doğrudan gerçek göreve veya kesinleşmiş karara dönüşmez.

## 2. Organizasyon ve ana çalışma alanı

### 2.1. Kulüp profili ve çalışma alanı — P1

Her kulüp için ayrı bir çalışma alanı oluşturulabilir.

- Kulüp adı, kısa adı, açıklaması ve logosu.
- Akademik yıl veya dönem bilgisi.
- Yönetim kurulu ve organizasyon şeması.
- Aktif birimler ve çalışma grupları.
- Dönem hedefleri ve öncelikleri.
- Aktif, tamamlanmış ve arşivlenmiş etkinlikler.
- Kulübün görev ve karar kayıtları.
- Kulübün veri saklama ve gizlilik ayarları.
- İçe aktarılan konuşmaların hangi çalışma alanına ait olduğu.
- Aynı etkinliğe ilişkin farklı birimlerden gelen kayıtların ilişkilendirilmesi.

Mantıksal kural: Bir çalışma alanındaki veri başka bir kulübün çalışma alanına otomatik olarak karışmamalı. Birden fazla kulüpte görev alan kişi ileride birden fazla alana erişebilse bile veriler birbirinden ayrılmalı.

### 2.2. Birim yönetimi — P1

Örnek bir organizasyon yapısı şöyle olabilir:

Kulüp yönetimi

Etkinlik

İletişim

Finans

Sponsorluk

İnsan kaynakları

Teknik ekip

Örnek organizasyon. Kulüp kendi birimlerini ekleyebilir, yeniden adlandırabilir veya arşivleyebilir.

Her birimin özellikleri:

- Birim adı, açıklaması ve amacı.
- Birim sorumlusu ve üyeleri.
- Birim görevleri ve iş yükü.
- İlgili etkinlikler, kararlar ve açık sorular.
- Birime ait konuşma dosyaları veya içe aktarımlar.
- Başka birimlerle ortak görevler.
- Birim hedefleri ve dönem sonu raporu.
- Aktif ve arşivlenmiş kayıtlar.
- Birim değişikliği geçmişi.

Bir görev iki birimi ilgilendirebilir. Örneğin sponsorluk birimi firmalarla görüşürken iletişim birimi sponsor logolarını paylaşabilir. Bu durumda görev tek bir ana kayda sahip olmalı; iki birime ilişkilendirilebilmeli. Aynı görevi iki ayrı görev olarak oluşturmak gereksiz tekrar ve raporlama hatası doğurur.

### 2.3. Kullanıcılar ve roller — P1

- Yönetici: Çalışma alanı, kullanıcılar ve genel ayarları yönetir.
- Kulüp yöneticisi: Kulüp çapındaki görevleri ve kayıtları yönetir.
- Birim sorumlusu: Kendi biriminin görevlerini ve kayıtlarını yönetir.
- Üye: Yetkisi dâhilindeki görevleri görüntüler ve günceller.
- Salt okunur kullanıcı: İzin verilen kayıtları görüntüler.
- Misafir veya geçici katılımcı: Gerektiğinde yalnızca kendisiyle paylaşılan belirli içeriklere erişir.

Rol sistemi yalnızca arayüzde buton gizlemekten ibaret olmamalı. Gerçek bir kullanıcı ve yetkilendirme altyapısı eklenirse her veri isteğinde sunucu tarafında yetki kontrolü yapılmalı.

İlk yerel demo tek kullanıcılı olabilir. Bu durumda çok kullanıcılıymış gibi görünen ama gerçekte güvenlik sağlamayan sahte bir rol sistemi kurulmamalı.

## 3. Konuşma dosyası içe aktarma ve yönetimi

Bu modül, KulüpRadar'ın temelidir. Mesajları doğru okuyamazsa yapay zekâ ve sonraki bütün modüller yanlış veriyle çalışır.

### 3.1. Dosya yükleme — P0

- WhatsApp'ın metin biçimindeki dışa aktarım dosyalarını (`.txt`) seçebilme.
- Dosyayı sürükleyip bırakabilme.
- Dosya seçimi öncesinde desteklenen biçimlerin açıklanması.
- Dosya boyutu sınırı ve dosya doğrulaması.
- Boş veya yalnızca boşluk içeren dosyaların reddedilmesi.
- Bozuk kodlama veya okunamayan karakterler için anlaşılır hata mesajı.
- Dosyanın daha önce içe aktarılmış olabileceğine dair uyarı.
- Analiz başlamadan önce dosyanın kısa bir ön izlemesini gösterme.
- Kullanıcının yanlış dosya seçmesi durumunda işlemi iptal edebilmesi.
- Başarılı içe aktarma, kısmi başarı ve başarısızlık durumlarını ayırma.

### 3.2. WhatsApp mesaj ayrıştırıcısı — P0

Ayrıştırıcı, metni gelişigüzel satırlara bölmemeli. WhatsApp dışa aktarımlarında tarih biçimi, saat biçimi, dil, sistem mesajları ve çok satırlı mesajlar değişebilir.

Desteklenmesi gereken durumlar:

- Farklı tarih biçimleri ve saat gösterimleri.
- 12 ve 24 saatlik saat biçimleri.
- Türkçe karakterler ve UTF-8 kodlaması.
- Mesajı gönderen kişinin adını doğru ayırma.
- Aynı mesajın devamı olan çok satırlı metinleri birleştirme.
- Grup oluşturuldu, kişi eklendi gibi sistem mesajlarını normal kullanıcı mesajlarından ayırma.
- Medya, belge ve ses mesajı yer tutucularını metin mesajı gibi değerlendirmeme.
- Düzenlenmiş veya silinmiş mesajlara ilişkin dışa aktarım yer tutucularını uygun şekilde işaretleme.
- Dosyadaki sıralamayı ve mümkün olduğunda orijinal tarih-saat bilgisini koruma.
- Bir mesajın göndereni belirlenemiyorsa uydurma bir isim vermeme.
- Ayrıştırılamayan satırları sessizce silmek yerine raporlama.
- Boş satırları ve gereksiz biçimlendirmeyi güvenli biçimde işleme.
- Dosyanın hangi biçimle ayrıştırıldığını ve kaç mesajın başarıyla okunduğunu gösterme.

Her mesaj için mümkün olduğunca şu bilgiler tutulmalı:

| Alan                 | Amaç                                          |
| -------------------- | --------------------------------------------- |
| Mesaj kimliği        | Mesajı diğerlerinden ayırmak                  |
| Kaynak dosya         | Mesajın hangi içe aktarımdan geldiğini bulmak |
| Gönderen adı         | Konuşmacıyı belirlemek                        |
| Tarih ve saat        | Olay sırasını korumak                         |
| Orijinal mesaj metni | Kanıtı değiştirmeden saklamak                 |
| Mesaj sıra numarası  | Konuşma sırasını yeniden kurmak               |
| Ayrıştırma durumu    | Hatalı veya şüpheli satırları izlemek         |

Tarih ve saat bilinmiyorsa sistem bunu tahmin ederek gerçek tarih gibi saklamamalı.

### 3.3. İçe aktarım geçmişi — P1

- İçe aktarımların adlandırılması.
- İçe aktarılan dosyanın ait olduğu grup veya çalışma alanının belirtilmesi.
- İçe aktarım tarihi ve mesaj sayısının gösterilmesi.
- İşlem durumunun izlenmesi: bekliyor, ayrıştırılıyor, analiz ediliyor, tamamlandı, hata oluştu.
- Daha önce işlenmiş dosyaların bulunabilmesi.
- Bir içe aktarımı arşivleme veya silme.
- Aynı dosya tekrar işlendiğinde yinelenen kayıt riskini azaltma.
- Her içe aktarımın oluşturduğu görev ve kararları kaynak dosyaya bağlama.
- Hata oluşursa dosyanın tamamını yeniden yüklemek zorunda kalmadan yeniden deneme.

Önemli teknik ayrıntı: Aynı dosyanın iki kez içe aktarılması, görevlerin iki katına çıkmasına yol açmamalı. Bunun için dosya parmak izi, kaynak mesaj kimliği ve benzer kayıt kontrolleri birlikte kullanılabilir. Benzerlik kontrolü tek başına kayıt silmek için yeterli değildir; kullanıcıya olası tekrarları göstermelidir.

## 4. Yapay zekâ analiz motoru

### 4.1. Analiz edilecek bilgi türleri — P0

Yapay zekâ, konuşmadan aşağıdaki türlerde aday kayıtlar çıkarmalı:

Görevler

Kim ne yapacak, hangi tarihe kadar yapacak, hangi etkinlik veya birimle ilgili?

Örnek: “Cuma gününe kadar afiş taslağını hazırlayalım.”

Kararlar

Üzerinde uzlaşılan veya yetkili kişi tarafından kesinleştirilen konular.

Örnek: “Etkinliği 12 Kasım'da yapmaya karar verdik.”

Açık sorular

Yanıtlanmamış sorular, eksik bilgiler ve bekleyen onaylar.

Örnek: “Salon rezervasyonunu kim yapacak?”

Etkinlik bilgileri

Etkinlik adı, tarih, saat, mekân, konuşmacı ve hazırlık ihtiyaçları.

Takip gerektiren konular

Yanıt bekleyen kişiler, tamamlanmamış işler ve sonuçlandırılmamış görüşmeler.

İlerleyen sürümlerde bütçe kalemleri, sponsorluk görüşmeleri, satın alma ihtiyaçları, gönüllü katılımları, riskler ve toplantı özetleri de çıkarılabilir. Bunlar ilk sürümün zorunlu kapsamına alınmamalı.

### 4.2. Görev çıkarma mantığı — P0

Her görev adayı şu alanları taşımalı:

- Görev başlığı.
- Kısa açıklama.
- Kaynak mesaj veya mesajlar.
- Görevi üstlendiği açıkça belirtilen kişi.
- İlgili birim.
- İlgili etkinlik veya proje.
- Son tarih ve varsa başlangıç tarihi.
- Öncelik.
- Durum.
- Bağımlı olduğu başka görevler.
- Yapay zekânın belirsizlik işaretleri.
- Kullanıcı onay durumu.

Her alan zorunlu olmamalı. Mesela bir mesajda “afişi hazırlayalım” deniyor ama kim hazırlayacak belirtilmiyorsa sorumlu alanı boş kalmalı ve “sorumlu atanmadı” olarak görünmeli.

Görev olarak yanlış sınıflandırılmaması gerekenler:

- Geçmişte yapılmış işler.
- Yalnızca fikir olarak sunulan öneriler.
- Gerçekleşeceği kesin olmayan olasılıklar.
- Şaka veya alay içeren mesajlar.
- Bir kişinin başkasına ait iş hakkında yaptığı tahmin.
- İptal edilmiş ya da değiştirilmiş eski görevler.
- Sadece soru biçiminde söylenen ve henüz kabul edilmemiş teklifler.

Örneğin “Belki cuma günü afişi paylaşırız” ile “Afişi cuma günü paylaşacağız” aynı kesinlikte değerlendirilmemeli.

### 4.3. Karar çıkarma ve karar geçmişi — P0/P1

Kararlar görevlerden farklı tutulmalı. Bir karar, bir veya daha fazla görevin oluşmasına neden olabilir.

Karar kaydında:

- Karar başlığı ve açıklaması.
- Kararla ilgili kaynak mesajlar.
- Kararın alındığı tarih veya tarihin bilinmediği bilgisi.
- Kararın durumu: öneri, tartışılıyor, onaylandı, reddedildi, değiştirildi, iptal edildi.
- Kararı onaylayan kişinin açıkça belirtilip belirtilmediği.
- İlgili etkinlik, birim veya görevler.
- Önceki karar ile ilişkisi.
- Sonradan neden değiştirildiği.

Mantıksal kural: Bir mesajın içinde “bence böyle yapalım” denmesi, tek başına kulüp kararı oluşturmaz. Sistem bunu öneri olarak göstermeli; kesin karar olarak işaretlememeli.

### 4.4. Açık soru ve takip sistemi — P1

- Cevap bekleyen soruların listelenmesi.
- Sorunun hangi mesajdan doğduğunun gösterilmesi.
- Sorunun ilgili olduğu birim veya etkinlik.
- Cevap verilmiş olabileceğini gösteren sonraki mesajların bulunması.
- Kullanıcıya “çözüldü”, “yanıt bekliyor” ve “geçersiz” seçenekleri sunulması.
- Sorunun sorumlusu belli değilse atama yapılabilmesi.
- Yanıtı kesin olmayan konuların “çözüldü” sayılmaması.

Yapay zekâ bir sorunun cevaplandığını önerebilir; ancak cevabın gerçekten yeterli olup olmadığı kullanıcı tarafından kontrol edilebilmeli.

### 4.5. Tarih, zaman ve belirsizlik yönetimi — P0

Bu konu özellikle önemli çünkü tarihler yanlış yorumlanırsa bütün görev planı bozulur.

- “Yarın”, “haftaya”, “cuma günü” gibi göreli ifadeleri tespit etme.
- Bu ifadelerin hangi mesaj tarihine göre yorumlandığını saklama.
- Saat dilimini açık biçimde yönetme.
- Tarih kesin değilse kesin tarih üretmeme.
- Birbiriyle çelişen tarihleri işaretleme.
- Geçmiş tarihli görevleri otomatik tamamlanmış saymama.
- Tarih değişikliğinde eski ve yeni değeri ilişkilendirme.
- “12/11” gibi farklı yorumlanabilen tarihleri doğrulama gerektiren alan olarak işaretleme.
- Tarihin mesajda açıkça yazılmasıyla model tarafından yorumlanması arasındaki farkı gösterme.

### 4.6. Kanıt ve güvenilirlik — P0

Her yapay zekâ çıktısı, kendisini destekleyen kaynak mesajlara bağlanmalı.

- Kaynak mesajın göndereni ve zaman bilgisi.
- Mesajın orijinal metni.
- Mesajı konuşma içinde açma veya çevresindeki mesajları görme.
- Birden fazla mesajdan çıkarım yapıldıysa hepsini gösterme.
- Kaynak mesaj bulunamayan çıkarımı işaretleme.
- Yapay zekâ güven puanını, doğruluk garantisi olarak göstermeme.
- Çelişkili kaynaklar varsa bunları birlikte sunma.
- Kullanıcının kaynağı inceleyip öneriyi kabul veya reddetmesi.

Güven puanı kullanılacaksa bu puan modelin kendi beyanından ibaret olmamalı. Kalibre edilmemiş bir puanı “%95 doğru” gibi kesin bir doğruluk göstergesi olarak sunmak yanıltıcı olur.

### 4.7. Yerel model ve hata toleransı — P0

- Ollama üzerinden yerel model çalıştırma.
- Modelin kurulu ve erişilebilir olup olmadığını kontrol etme.
- Seçilen modelin mevcut olup olmadığını doğrulama.
- Model başlatılamadığında anlaşılır hata verme.
- Model yanıtı bozuk JSON ise kontrollü doğrulama ve sınırlı yeniden deneme.
- Beklenmeyen alanları ve geçersiz tarihleri reddetme.
- Çok uzun konuşmaları kontrollü parçalara ayırma.
- Parçalar arasında yinelenen görevleri belirleme.
- Modelin her parçayı işleyip işlemediğini takip etme.
- Analiz yarıda kalırsa işlemin durumunu koruma.
- Analiz sırasında iptal edebilme.
- Model ve sürüm bilgisini kaydetme.
- Farklı modelleri yapılandırılabilir hâle getirme.

Gizlilik ilkesi: Varsayılan akışta konuşma içeriği uzak bir yapay zekâ API'sine gönderilmemeli. Model yerel çalışıyorsa bile uygulamanın kendi hata kayıtlarına veya tanılama günlüklerine özel mesaj metinleri gereksiz yere yazılmamalı.

## 5. Görev yönetimi

Görev modülü, uygulamanın yalnızca analiz yapan değil, günlük kullanımda da işe yarayan kısmı olmalı.

### 5.1. Görev listesi — P0

- Tüm görevleri tek ekranda görüntüleme.
- Görevleri durum, birim, sorumlu, öncelik ve son tarihe göre filtreleme.
- Başlığa ve açıklamaya göre arama.
- Görevleri son tarihe veya önceliğe göre sıralama.
- Görev detaylarını açma.
- Yeni görevi elle oluşturma.
- Yapay zekâ önerisini göreve dönüştürme.
- Görevi düzenleme, iptal etme ve arşivleme.
- Bir görev için birden fazla kaynak mesaj bağlayabilme.
- Görev geçmişini görüntüleme.

### 5.2. Görev durumları

Önerilen temel durum akışı:

Önerildi

Yapay zekâ tarafından çıkarıldı veya yeni kayıt oluşturuldu.

Onay bekliyor

Kullanıcı görevi kontrol ediyor.

Yapılacak

Görev kabul edildi.

Devam ediyor

Tamamlandı

İptal edildi ve engellendi durumları ayrıca tanımlanmalı. Onay bekleyen bir kayıt, aktif görevle aynı şey değildir.

### 5.3. Görev atama ve sorumluluk

- Görevi belirli bir kişiye atama.
- Göreve yardımcı olacak ek üyeler ekleme.
- Birim veya çalışma grubu belirleme.
- Sorumlu değişikliğini kaydetme.
- Sorumlusu olmayan görevleri özel filtrede gösterme.
- Bir kişinin aynı anda kaç aktif görevi olduğunu gösterme.
- Görev atamasını kaynak konuşmadaki ifadeden ayırma.
- Kullanıcının görev sahibini yapay zekâ önerisinden farklı seçebilmesi.

Bir kişinin adının mesajda geçmesi, otomatik olarak görevin ona atandığı anlamına gelmemeli. “Ayşe afişi hazırladı” geçmiş bir olayı anlatabilir; “Ayşe, afişi hazırlayabilir misin?” ise henüz kabul edilmemiş bir görev teklifi olabilir.

### 5.4. Öncelik ve son tarih

- Düşük, normal, yüksek ve acil öncelik.
- Son tarihi yaklaşan görevler.
- Süresi geçmiş görevler.
- Tarihi olmayan görevler.
- Son tarihi değiştirilen görevlerin geçmişi.
- Görevin aciliyetini etkileyen bağımlılıklar.
- Son tarih ve önceliğe göre filtreleme.
- Kullanıcıya özel bir “Bugün” görünümü.

Son tarihi geçmiş bir görev otomatik olarak başarısız sayılmamalı; yalnızca gecikmiş olarak işaretlenmeli.

### 5.5. Alt görevler ve bağımlılıklar — P1

Örneğin bir etkinliğin düzenlenmesi tek görev değil, bir iş paketi olabilir:

- Salon rezervasyonu.
- Konuşmacıyla iletişim.
- Afiş tasarımı.
- Duyurunun yayımlanması.
- Kayıt formunun hazırlanması.
- Teknik ekipmanın kontrolü.
- Etkinlik sonrası geri bildirim.

Her alt görevin ayrı sorumlusu ve tarihi olabilir. Üst görev, alt görevlerden bağımsız olarak tamamlanmış gösterilmemeli; tamamlanma durumu ile alt görevlerin durumu arasındaki ilişki açık olmalı.

### 5.6. Görev yorumları ve etkinlik günlüğü — P1

- Göreve açıklama ekleme.
- Yapılan işi veya karşılaşılan engeli not etme.
- Durum değişikliklerini zaman sırasıyla gösterme.
- Görev tarihçesini saklama.
- Görevin neden iptal edildiğini kaydetme.
- Görevle ilgili kanıt veya bağlantı ekleme.

Bu özellikler çok kullanıcılı sürümde gerçek kullanıcı kimlikleriyle çalışmalı. Tek kullanıcılı demo için karmaşık yorum ve bildirim altyapısı geliştirmek öncelikli değil.

## 6. Etkinlik ve organizasyon yönetimi

Etkinlik yönetimi, görev modülünü tamamlayan bir katman olmalı. Bir etkinliğin tüm işleri tek bir görev listesinde kaybolmamalı.

### 6.1. Etkinlik kayıtları — P1

Her etkinlikte şu alanlar bulunabilir:

- Etkinlik adı ve açıklaması.
- Etkinlik türü: seminer, eğitim, yarışma, gezi, toplantı, sosyal etkinlik vb.
- Planlanan tarih ve saat.
- Mekân veya çevrim içi bağlantı.
- Etkinlik sorumlusu.
- İlgili birimler.
- Etkinlik durumu: fikir, planlanıyor, onay bekliyor, kesinleşti, gerçekleşti, iptal edildi.
- Etkinlik hedefleri.
- Beklenen katılımcı sayısı.
- Konuşmacılar veya iş birlikleri.
- Bütçe tahmini ve gerçekleşen giderler.
- Hazırlık görevleri.
- Riskler ve bekleyen kararlar.
- Etkinlik sonrası değerlendirme.

Etkinlik tarihi yalnızca mesajda konuşulmuşsa “önerilen tarih” olarak tutulmalı. Kesinleşmiş etkinlik tarihiyle aynı alanda, durum ayrımı olmadan gösterilmemeli.

### 6.2. Etkinlik hazırlık kontrol listeleri — P1

Etkinlik türüne göre tekrar kullanılabilir kontrol listeleri oluşturulabilir.

Örneğin bir seminer için:

- Konuşmacı kesinleştirildi.
- Tarih ve mekân onaylandı.
- Teknik ihtiyaçlar belirlendi.
- Afiş hazırlandı.
- Duyuru yayımlandı.
- Katılımcı kayıtları kontrol edildi.
- Sunum ve ekipman test edildi.
- Etkinlik sonrası değerlendirme tamamlandı.

Bunlar hazır şablonlardır; her etkinlikte tüm maddeler zorunlu olmamalı. Kulüp kendi şablonlarını oluşturup düzenleyebilmeli.

### 6.3. Etkinlik takvimi — P1

- Aylık ve haftalık görünüm.
- Etkinliklerin yanında son tarihi yaklaşan görevleri gösterme.
- Çakışan etkinlikleri işaretleme.
- Etkinlik hazırlık aşamasındaki kritik tarihleri gösterme.
- Tarihi kesinleşmemiş etkinlikleri ayrı bölümde tutma.
- Kullanıcının takvim verisini dışa aktarabilmesi.

Takvimde çakışma bulunması otomatik olarak bir etkinliğin yanlış olduğu anlamına gelmez; sistem uyarı verir, kararı kullanıcıya bırakır.

### 6.4. Etkinlik sonrası raporlama — P2

- Planlanan ve gerçekleşen katılımcı sayısı.
- Tamamlanan ve tamamlanamayan görevler.
- Planlanan ve gerçekleşen bütçe.
- Karşılaşılan sorunlar.
- Katılımcı geri bildirimleri.
- Bir sonraki etkinlik için öğrenilen dersler.

Bu veriler ancak gerçekten kaydedildiyse rapora girmeli. Eksik değerler yapay zekâ tarafından doldurulmamalı.

7. Birimler arası iş birliği ve iletişim karmaşasını çözme
Bu modül, KulüpRadar'ın temel kullanım amacını güçlendirebilir.
7.1. Birimler arası görevler — P1
- Bir görevin birden fazla birimle ilişkilendirilmesi.
- Ana sorumlu birimin belirlenmesi.
- Her birimin kendi alt sorumluluğunun kaydedilmesi.
- Ortak görevlerin birim panellerinde görüntülenmesi.
- Aynı görevin kopyalanması yerine tek kayıttan izlenmesi.
- Birimlerden biri işini tamamlamadığında engelin görünür olması.
- Görevde birim değişikliğinin geçmişinin tutulması.
7.2. Bekleyen yanıtlar ve iş devri — P1
- Birimin başka bir birimden beklediği işlerin listelenmesi.
- Sorumluluğu devredilen görevler.
- Yanıt veya onay bekleyen kayıtlar.
- Birimler arası bağımlılıkların gösterilmesi.
- Uzun süre güncellenmeyen görevlerin belirlenmesi.
- Devredilen işin kabul edilip edilmediğinin izlenmesi.
Sistemin “İletişim birimi gecikiyor” gibi suçlayıcı ifadeler üretmesi yerine, “Afiş yayımlama görevi, sponsorluk biriminden logo onayı bekliyor” gibi somut ve kanıta dayalı açıklamalar sunması daha doğru olur.
7.3. Kulüp içi duyuru ve mesajlaşma — P2
İleride şu özellikler eklenebilir:
- Kulüp içi duyuru alanı.
- Birim duyuruları.
- Etkinlik duyuruları.
- Okundu bilgisi.
- Duyurunun ilgili görev veya etkinliğe bağlanması.
- Basit yorumlar ve tartışma dizileri.
Ancak bu özellikler, WhatsApp'ın yerine geçecek tam bir mesajlaşma sistemi kurmayı gerektirebilir. Yarışma için geliştirilen ilk sürümde öncelik verilmemeli. Kulüp platformunun daha geniş kapsamlı sürümünde ayrıca değerlendirilmesi daha mantıklı.

8. Ana kontrol paneli
Kontrol paneli yalnızca süslü grafiklerden oluşmamalı. Kullanıcının açtığında ne yapması gerektiğini anlamasını sağlamalı.
8.1. Önerilen panel bileşenleri — P0/P1
ÖRNEK PANEL TASARIMI — TEMSİLÎ
Görevler
Aktif ve bekleyen işler


Yaklaşan işler
Son tarihi yaklaşan görevler


Açık sorular
Yanıt veya karar bekleyen konular


AI incelemesi
Onay bekleyen çıkarımlar




Bugün ilgilenilmesi gerekenler
- Gecikmiş görevler
- Atanmamış görevler
- Birim onayı bekleyen işler
- Tarihi çelişkili kayıtlar
- Sonuçlandırılmamış kararlar
  
  Son içe aktarımlar
  Dosya adı, analiz durumu, mesaj sayısı ve incelemeye hazır kayıt sayısı.

8.2. Panel davranışları
- Kartlara tıklanınca ilgili filtrelenmiş listeye gitme.
- Gösterilen sayının hangi kayıtları kapsadığını açıklama.
- Aktif ve arşivlenmiş kayıtları ayrı değerlendirme.
- Henüz onaylanmamış AI önerilerini gerçek görev sayısından ayırma.
- Veri yoksa sıfır değerleri gerçek durumla karıştırmama.
- Analiz sürerken ilerleme ve hata durumunu gösterme.
- Paneldeki bilgileri görev, birim ve etkinlik sayfalarıyla tutarlı tutma.
Bir görev hem gecikmiş hem de yüksek öncelikli olabilir. Dolayısıyla kontrol panelinde yer alan kartlar birbirini dışlayan kategoriler olmak zorunda değildir; toplamların neden örtüşebildiği açıkça anlaşılmalı.

9. Arama, filtreleme ve kayıt ilişkileri
9.1. Evrensel arama — P1
İlerleyen sürümde tek arama alanı üzerinden şunlar bulunabilmeli:
- Görevler.
- Kararlar.
- Açık sorular.
- Etkinlikler.
- Birimler.
- İçe aktarımlar.
- Kaynak mesajlar.
Arama sonuçlarında kayıt türü, ilgili birim, tarih ve durum gösterilmeli. Kullanıcı kaynağa veya ilgili göreve doğrudan gidebilmeli.
9.2. Filtreler
- Tarih aralığı.
- Birim.
- Sorumlu.
- Durum.
- Öncelik.
- Etkinlik.
- Kaynak dosya.
- Yapay zekâ tarafından önerilen veya kullanıcı tarafından oluşturulan kayıt.
- Onay bekleyen veya onaylanmış kayıt.
- Eksik bilgi içeren kayıt.
9.3. Yinelenen kayıt ve çelişki tespiti — P1
- Aynı görev gibi görünen kayıtları bulma.
- Birbiriyle çelişen etkinlik tarihlerini belirleme.
- Farklı mesajlarda farklı sorumluların belirtilmesini işaretleme.
- Eski kararın daha sonra değiştirilmiş olabileceğini gösterme.
- Kullanıcıya kayıtları birleştirme veya ayrı tutma seçeneği sunma.
- Birleştirme sırasında kaynak mesajların tamamını koruma.
Benzer iki cümle her zaman aynı görevi anlatmaz. Otomatik birleştirme yerine kullanıcıya öneri sunulmalı.

10. Raporlar ve dışa aktarma
10.1. Temel raporlar — P1
- Aktif görevler.
- Tamamlanan görevler.
- Gecikmiş görevler.
- Sorumlusu atanmamış görevler.
- Birim bazında görev dağılımı.
- Açık kararlar ve sorular.
- Etkinlik hazırlık durumu.
- Belirli bir konuşma dosyasından çıkarılan kayıtlar.
- Yapay zekâ tarafından önerilen fakat henüz onaylanmayan kayıtlar.
10.2. Dışa aktarma
- Görevleri CSV olarak dışa aktarma.
- Kararları ve açık soruları CSV veya JSON olarak dışa aktarma.
- Analiz özetini Markdown biçiminde kaydetme.
- Kaynak mesaj bağlantılarını ve kanıt metinlerini uygun biçimde koruma.
- Rapor tarih aralığını ve filtreleri belirtme.
- İstenmeyen kişisel bilgilerin rapora eklenmesini engelleyen seçenekler sunma.
PDF raporu, Excel çıktısı ve gelişmiş görselleştirmeler eklenebilir; ancak temel kayıtların doğru tutulmasından daha önemli değiller.

11. Gizlilik, güvenlik ve güvenilirlik
Bu uygulama özel kulüp konuşmalarını işlediği için gizlilik bir eklenti değil, ürünün temel tasarım ilkesi olmalı.
11.1. Yerel çalışma ve veri kontrolü — P0
- Konuşmalar varsayılan olarak kullanıcının cihazında işlenmeli.
- Uzak API'ye veri gönderimi varsayılan akışta bulunmamalı.
- Modelin yerel olup olmadığı ve hangi modelin kullanıldığı açıkça gösterilmeli.
- Hata günlüklerine özel konuşma içerikleri yazılmamalı.
- Kullanıcı içe aktarım dosyalarını ve oluşturulan kayıtları silebilmeli.
- Silme işleminin hangi verileri kapsadığı açıklanmalı.
- Verilerin uygulama veritabanında nerede tutulduğu belgelenmeli.
- Yedekleme ve dışa aktarma davranışları açıkça belirtilmeli.
Yerel model kullanmak tek başına tüm güvenlik sorunlarını çözmez. Dosya yükleme, veri tabanı, uygulama günlükleri, bağımlılıklar ve dışa aktarılan raporlar da güvenli ele alınmalı.
11.2. Hassas veri ve kötü amaçlı içerik
- Mesajların içinde bulunan komut benzeri metinler model talimatı olarak körü körüne kabul edilmemeli.
- Konuşma içeriği güvenilmeyen veri olarak ele alınmalı.
- Dosya içeriği çalıştırılmamalı.
- Beklenmeyen dosya türleri reddedilmeli.
- Büyük dosyalara karşı bellek ve işlem sınırları uygulanmalı.
- Yapay zekâdan gelen yapılandırılmış çıktı şema doğrulamasından geçirilmeli.
- Özel mesajların gereksiz yere dışa aktarılmasını azaltacak kontroller bulunmalı.
- Geliştirme ve test ortamlarında gerçek kişisel veriler yerine sentetik örnekler kullanılmalı.
11.3. Denetlenebilirlik
- Bir kaydın hangi mesajlardan çıkarıldığı gösterilmeli.
- Kullanıcının yaptığı değişiklikler gerektiğinde izlenebilmeli.
- AI önerisinin kabul, ret veya düzenleme durumu tutulmalı.
- Karar değişiklikleri kaydedilmeli.
- Silme ve saklama politikaları belgelenmeli.
- Yapay zekâ çıktısı ile kullanıcının son onayı ayırt edilmeli.
11.4. Hukuki ve etik tasarım
- Uygulamanın hangi verileri işlediği açıkça anlatılmalı.
- Kullanıcılara kendi yerel veri işleme süreçleri hakkında bilgi verilmeli.
- Veri saklama süresi ve silme davranışı tanımlanmalı.
- Kişisel verilerin paylaşılmasına ve dışa aktarılmasına ilişkin riskler açıklanmalı.
- Kulüp konuşmalarının içe aktarılması için gerekli izin ve yetkiler konusunda kullanıcı bilgilendirilmeli.
- Uygulama hukuki uyumluluk konusunda garanti vermemeli; kullanım koşulları ve ilgili mevzuat için uygun inceleme yapılmalı.

12. Kullanıcı deneyimi ve erişilebilirlik
12.1. İlk kullanım akışı — P0
Yeni kullanıcı uygulamayı açtığında şu soruların cevabını hemen bulmalı:
1. Uygulama ne yapıyor?
2. Hangi dosyayı yüklemeliyim?
3. Verilerim nereye gönderiliyor?
4. Analiz başladı mı?
5. Sonuçları nereden kontrol edeceğim?
6. Yapay zekâ bir hata yaparsa bunu nasıl düzelteceğim?
İlk kullanımda örnek bir sentetik konuşma dosyasıyla uygulamayı deneyebilme seçeneği yararlı olur.
12.2. Hata ve işlem durumları
- Dosya yükleniyor.
- Dosya doğrulanıyor.
- Mesajlar ayrıştırılıyor.
- Yapay zekâ analiz ediyor.
- Sonuçlar doğrulanıyor.
- İnceleme bekleniyor.
- Analiz tamamlandı.
- Kısmi hata oluştu.
- Model bulunamadı.
- İşlem iptal edildi.
Her durumda kullanıcıya ne olduğu, ne yapabileceği ve verilerin korunup korunmadığı açıklanmalı. Teknik hata mesajları geliştirici için kaydedilebilir; kullanıcıya ise anlaşılır bir açıklama sunulmalı.
12.3. Arayüz ve erişilebilirlik
- Masaüstü ve dar ekranlarda kullanılabilir düzen.
- Klavye ile temel işlemleri yapabilme.
- Görünür odak göstergeleri.
- Okunabilir metin boyutları ve yeterli kontrast.
- Durumu yalnızca renkle anlatmama.
- Form alanları için açık etiketler.
- Hata mesajlarını ilgili alanla ilişkilendirme.
- Yükleme ve analiz durumlarını erişilebilir biçimde bildirme.
- Boş ekranlar için yönlendirici açıklamalar.
- Uzun mesajları taşma yaratmadan görüntüleme.
- Türkçe karakterlerin tüm ekranlarda doğru gösterilmesi.
İngilizce arayüz, çoklu dil ve özelleştirilebilir tema ileride eklenebilir. Ancak ilk sürümün Türkçe arayüzünün tutarlı olması daha önemli.





13. Yapay zekânın ileri seviye özellikleri
Bunlar ürünü zenginleştirebilir, ancak temel analiz ve kanıt sistemi güvenilir olmadan eklenmemeli.
13.1. Konuşma özeti — P1
- Konuşmanın kısa özeti.
- Konuşulan ana konular.
- Kesinleşen kararlar.
- Henüz karara bağlanmayan konular.
- Yeni ortaya çıkan görevler.
- Birimler arası bağımlılıklar.
- Sonraki adımlar.
Özet, orijinal konuşmanın yerine geçmemeli. Önemli maddeler kaynak mesajlara bağlanmalı.
13.2. Konuşma içindeki değişiklikleri tespit etme — P2
Aynı grup için farklı tarihlerde alınmış dışa aktarımlar olduğunda:
- Yeni mesajları eski içe aktarımla karşılaştırma.
- Daha önceki bir görevin güncellenip güncellenmediğini belirleme.
- Tarih veya sorumlu değişikliklerini işaretleme.
- Yeni kararları önceki kararlarla ilişkilendirme.
- Aynı mesajların tekrar işlenmesini önleme.
Bu özellik yalnızca dosyaların aynı konuşmaya ait olduğu güvenilir biçimde belirlenebiliyorsa çalışmalı. İki farklı WhatsApp grubunun mesajlarını benzer içerik nedeniyle birleştirmemeli.
13.3. Doğal dille arama — P2
Kullanıcı şu tür sorular sorabilir:
- “Yaklaşan etkinliklerin afişleriyle ilgili görevleri göster.”
- “Sorumlusu belli olmayan işler hangileri?”
- “Sponsorluk için hangi konular hâlâ açık?”
- “Geçen hafta hangi kararlar alınmış?”
- “Etkinlik tarihinin değiştiğini gösteren mesajlar var mı?”
Yanıtlar yalnızca uygulamada bulunan verilere dayanmalı; kaynak bulunamıyorsa “kayıtlarda bulamadım” demeli. Sistem yalnızca anahtar kelimelerden hareketle hayalî bir karar oluşturmamalı.
13.4. Akıllı iş yükü analizi — P2
- Üyelerin aktif görev sayısını gösterme.
- Bir kişide aşırı iş birikmesini tespit etme.
- Birimler arasındaki iş dağılımını gösterme.
- Atanmamış görevleri belirleme.
- Aynı kişiye bağlı kritik işlerin birikmesini işaretleme.
- Görev ataması için olası öneriler sunma.
İş yükü analizi, bir kişinin performansını kesin biçimde ölçen veya kişileri sıralayan bir sistem olarak sunulmamalı. Görev sayısı, işin zorluğunu ve kişinin müsaitliğini tek başına açıklamaz.
13.5. Kişiselleştirilebilir iş akışları — P2
- Görev şablonları.
- Etkinlik şablonları.
- Birim bazında özel alanlar.
- İsteğe bağlı onay adımları.
- Kulübün kendi görev durumlarını tanımlaması.
- Özel rapor filtreleri.
- İçe aktarımlar için kayıt kuralları.
Bu yapı esnek olmalı ama sınırsız yapılandırma ilk sürümde karmaşıklığı artırabilir. Önce ortak ve anlaşılır bir varsayılan iş akışı sunulmalı.

14. Teknik mimari ve veri modelinin mantığı
Burada amaç belirli bir teknoloji yığınına körü körüne bağlanmak değil, özelliklerin birbiriyle doğru çalışmasını sağlamak.
14.1. Önerilen mimari
Kullanıcı arayüzü
Dosya yükleme · Panel · Görevler · Kararlar · İnceleme ekranı

Uygulama servisleri
İçe aktarım · İş akışı · Doğrulama · Yetkilendirme · Dışa aktarma

Ayrıştırıcı
Kaynak mesajlar


Yerel AI servisi
Aday kayıtlar



Veri katmanı
İçe aktarımlar · Mesajlar · Görevler · Kararlar · Etkinlikler · Kanıtlar · Geçmiş


Bu şema mantıksal bir öneridir; mevcut kod tabanının yapısı incelenmeden teknolojilerin veya klasörlerin kesin olarak böyle olması gerektiğini söylemek doğru olmaz.
14.2. Temel veri varlıkları
Varlık	Görevi
Workspace	Kulübün veya çalışma alanının kimliği
Unit	Birim ve alt birim yapısı
Member	Kullanıcı veya kulüp üyesi
Import	Kaynak dosya ve işleme durumu
Message	Ayrıştırılmış orijinal mesaj
Task	Görev kaydı
Decision	Karar ve karar geçmişi
Question	Açık soru veya takip konusu
Event	Etkinlik kaydı
Evidence	Yapay zekâ çıktısını destekleyen kaynaklar
AnalysisRun	Model, analiz durumu ve hata bilgileri
AuditEntry	Önemli değişikliklerin geçmişi
Bunlara ileride yorumlar, görev bağımlılıkları, dosyalar, bütçe kalemleri ve raporlar eklenebilir.
14.3. Veri ilişkileri
- Bir çalışma alanında birden fazla birim olabilir.
- Bir içe aktarım birçok mesaj içerebilir.
- Bir mesaj birden fazla analiz önerisini destekleyebilir.
- Bir görev birden fazla kaynak mesajla ilişkilendirilebilir.
- Bir karar birden fazla görevin ortaya çıkmasına neden olabilir.
- Bir etkinliğin birçok görevi olabilir.
- Bir görev birden fazla birimle ilişkili olabilir.
- Aynı mesajdan görev, karar veya açık soru önerileri çıkarılabilir.
- Bir AI analizi birden fazla aday kayıt üretebilir.
En kritik veri tasarımı kararı: Kanıt mesajlarını görev tablosuna yalnızca bir metin olarak kopyalamak yerine ayrı ve ilişkilendirilebilir biçimde tutmak. Böylece bir görev düzenlense veya birleştirilse bile kaynak bilgisi kaybolmaz.
14.4. Durumların birbirinden ayrılması
En az üç ayrı kavram olmalı:
1. Analiz durumu: İşlem sürüyor mu, tamamlandı mı, hata mı oluştu?
2. İnceleme durumu: AI önerisi bekliyor mu, onaylandı mı, reddedildi mi?
3. İş kaydı durumu: Görev yapılacak mı, devam mı ediyor, tamamlandı mı?
Bunları tek bir status alanına sıkıştırmak ileride ciddi hatalara yol açabilir.

15. Test ve doğrulama gereksinimleri
Bir özelliğin eklenmiş olması, doğru çalıştığı anlamına gelmez. Her modül için ölçülebilir kabul kriterleri tanımlanmalı.
15.1. Ayrıştırıcı testleri — P0
- Farklı tarih ve saat biçimleri.
- Çok satırlı mesajlar.
- Türkçe karakterler.
- Boş dosya.
- Bozuk kodlama.
- Sistem mesajları.
- Medya yer tutucuları.
- Birden fazla dosya.
- Çok büyük dosyalar.
- Hatalı satırlar.
- Aynı dosyanın tekrar yüklenmesi.
15.2. AI testleri — P0
Sentetik bir test veri setinde en azından şu durumlar bulunmalı:
- Açıkça belirtilmiş bir görev.
- Sorumlusu belli olmayan görev.
- Belirsiz tarih.
- Kesinleşmemiş öneri.
- Alınmış karar.
- Sonradan değiştirilmiş karar.
- Cevaplanmamış soru.
- Tamamlanmış geçmiş görev.
- Şaka veya alakasız mesaj.
- Birbiriyle çelişen iki mesaj.
- Aynı görevin farklı ifadelerle tekrarlanması.
- Modelin bozuk veya eksik JSON üretmesi.
Sonuçlar insan tarafından etiketlenmiş beklenen çıktılarla karşılaştırılmalı. Modelin gerçekten ne kadar doğru çalıştığı ölçülmeden başarı iddiasında bulunulmamalı.
15.3. Uçtan uca test — P0
Şu akış gerçek bir uygulama testi olarak çalışmalı:
1. Kullanıcı örnek bir .txt dosyası seçer.
2. Dosya doğrulanır.
3. Mesajlar doğru ayrıştırılır.
4. Yerel modelden yapılandırılmış çıktı alınır.
5. Çıktı şeması doğrulanır.
6. Aday görev ve kararlar oluşturulur.
7. Kaynak mesajlar görüntülenir.
8. Kullanıcı bir öneriyi düzenleyip onaylar.
9. Onaylanan görev görev listesinde görünür.
10. Kullanıcı görevin durumunu değiştirir.
11. Sayfa yenilendiğinde kayıt korunur.
12. Görev dışa aktarıldığında kaynak bilgileri uygun şekilde korunur.
Bu akışın tamamı çalışmıyorsa yalnızca ekran görüntüsüne bakarak ürünün hazır olduğu söylenmemeli.
15.4. Güvenlik ve dayanıklılık testleri
- Geçersiz dosya yükleme.
- Beklenmeyen model yanıtı.
- Model servisi kapalıyken çalışma.
- Analizin ortasında iptal.
- Veri tabanı hatası.
- Yinelenen kayıt.
- Eksik alanlar.
- Özel metinlerin günlük dosyalarına sızması.
- Veri silme işleminin gerçekten uygulanması.
- Dışa aktarma dosyasında beklenmeyen içerik.
15.5. Kalite göstergeleri
İlerleyen aşamada şu ölçümler tutulabilir:
- Ayrıştırılan mesaj oranı.
- Doğru görev çıkarma oranı.
- Yanlış görev oluşturma oranı.
- Sorumlu tespitinde doğruluk.
- Tarih çıkarımında doğruluk.
- Kanıtı bulunabilen AI önerilerinin oranı.
- Kullanıcının kabul, düzeltme ve ret oranları.
- Analiz süresi ve hata oranı.
Özellikle yanlış pozitifler önemlidir. Çok sayıda görev çıkarıp bunların çoğunu kullanıcıya sildirtmek, iyi bir AI sistemi anlamına gelmez.





16. Geliştirme öncelikleri: Ne gerçekten ilk sürümde olmalı?
Özellikleri ne kadar geniş düşünürsek düşünelim, mevcut yarışma teslimine kadar hepsini geliştirmeye çalışmak doğru olmaz. Aşağıdaki kapsam, ürünün temel değerini göstermek için daha mantıklı.
Özellik öncelik listesi
Bir seviyeyi seçerek o kapsamdaki maddeleri görüntüleyebilirsin.

Tüm özellikler

P0 — Teslim için temel

P1 — Sonraki geliştirmeler

P2 — İleri seviye


Dosya içe aktarma ve ayrıştırma
P0

WhatsApp .txt dosyası yükleme


Mesajları doğru ayırma ve sıralama


Hatalı satırları raporlama


İçe aktarım durumunu gösterme




AI analiz ve inceleme
P0

Görev, karar ve açık soru çıkarma


Yerel model bağlantısı


Yapılandırılmış çıktı doğrulama


Kaynak mesajı gösterme


Öneriyi onaylama, düzenleme ve reddetme




Görev yönetimi
P0

Onaylanan görevleri listeleme


Görev durumu değiştirme


Sorumlu ve tarih bilgilerini düzenleme


Veriyi kalıcı saklama




Kalite ve teslim
P0

Uçtan uca test


Model kapalıyken hata yönetimi


README ve kurulum talimatları


Açık kaynak lisansı


Demo ve teslim materyalleri




Organizasyon özellikleri
P1

Birimler ve üyeler


Etkinlik yönetimi


Takvim


Birimler arası görevler


Açık soru takibi




Raporlama ve arama
P1

Görev filtreleri


Karar geçmişi


CSV/JSON dışa aktarma


Gelişmiş arama




Gelişmiş AI
P2

Doğal dille sorgulama


Konuşma geçmişlerini karşılaştırma


İş yükü analizi


Özelleştirilebilir iş akışları





17. Uygulamanın doğru uygulanması için değişmez kurallar
Bunları doğrudan yazılım geliştirme gereksinimi olarak kullanmanı öneririm:
1. Kaynak olmadan kesin AI kaydı oluşturulmayacak. Kaynak mesaj bulunamıyorsa çıkarım incelenmek üzere işaretlenecek.
2. AI önerisi otomatik olarak onaylanmayacak. İnsan onayı gerektiren kayıtlar ayrı tutulacak.
3. Belirsiz bilgi uydurulmayacak. Bilinmeyen sorumlu, tarih, birim veya etkinlik boş bırakılabilecek.
4. Mesaj geçmişi ile güncel durum ayrılacak. Eski bir tarih veya görev bilgisi güncel durum gibi sunulmayacak.
5. Kullanıcı düzeltmeleri korunacak. Sonraki analizler kullanıcının onayladığı kayıtları kontrolsüz biçimde ezmeyecek.
6. Yinelenen kayıtlar denetlenecek. Aynı görev tekrar tekrar oluşturulmayacak; belirsiz durumlarda otomatik birleştirme yapılmayacak.
7. Her işlemde hata yönetimi bulunacak. Dosya, model veya veri tabanı hatası uygulamayı kontrolsüz biçimde çökertmeyecek.
8. Veri gizliliği varsayılan olarak korunacak. Özel konuşmalar izinsiz uzak servislere gönderilmeyecek.
9. Arayüzde görünen her işlev çalışacak. Çalışmayan buton, sahte istatistik veya yalnızca görsel amaçlı kontrol bırakılmayacak.
10. Test edilmeyen özellik hazır ilan edilmeyecek. Gerçek test sonucu, bilinen eksikler ve doğrulanamayan durumlar açıkça raporlanacak.
11. Mevcut proje yapısı korunarak geliştirilecek. Kod tabanı incelenmeden gereksiz teknoloji değişimi veya baştan yazım yapılmayacak.
12. Özellikler birbirleriyle tutarlı çalışacak. Görev, karar, etkinlik, birim ve kanıt kayıtları aynı veriyi farklı yerlerde çelişkili göstermeyecek.
18. Benim nihai ürün önerim
KulüpRadar'ın güçlü tarafı, “yapay zekâ sohbeti” olması değil, dağınık konuşmaları kanıtlarıyla birlikte düzenlenebilir ve takip edilebilir organizasyon kayıtlarına dönüştürmesi olmalı.
Bu nedenle geliştirme sırasını şu şekilde belirlerdim:
- Önce: İçe aktarım, ayrıştırıcı, yerel AI, kaynak kanıtları ve onaylı görev akışı.
- Sonra: Kararlar, açık sorular, etkinlik ve birim bağlantıları.
- Daha sonra: Çok kullanıcılı yapı, yetkilendirme, gelişmiş raporlar ve doğal dille arama.
- En son: Bildirimler, kulüp içi mesajlaşma, gelişmiş iş akışları ve büyük platform entegrasyonları.
Bu yaklaşım hem yarışma için gösterilebilir bir ürün ortaya çıkarır hem de ileride daha büyük kulüp yönetim platformuna dönüştürülebilecek sağlam bir temel kurar.
Bir sonraki teknik adım olarak bu özellik kataloğunu mevcut kod tabanına göre uygulanabilir gereksinimlere dönüştürmek gerekir: her özellik için veri alanları, kullanıcı akışı, bağımlılıklar, kabul kriterleri, test senaryoları ve öncelik tanımlanmalı.