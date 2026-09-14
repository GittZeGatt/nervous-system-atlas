# Kullanım kılavuzu

Atlasın yapabildiği her şey, onu çalıştırmış biri için (çalıştırmak için [README](../README.md#klinik-nöroanatomi-atlası)).
English: [User guide](guide.md).

## Kesitler, traktuslar ve sulama alanları

Her kesit, meshlerin kayıtlandığı MR'ın kendisidir; böylece bir yapı hem kesitte hem üç boyutta aynı anda okunur. Kesite tıklayınca imlecin altındaki yapı seçilir, bir yapıya tıklayınca kesitler ona taşınır.

| | |
|---|---|
| ![z = 16 mm'de capsula interna düzeyinden aksiyal T1; nucleus caudatus ve thalamus kesitin üzerinde, sol capsula interna konturlu](screenshots/axial-capsule.webp) | ![Hippocampus gövdesi düzeyinde koronal T1; yan ventriküller mavi, hippocampus ve amygdala pembe, sol hippocampus konturlu](screenshots/coronal-temporal.webp) |
| **Aksiyal, capsula interna düzeyi.** Etiket kaplaması derin gri çekirdekleri MR'ın üzerine boyar; seçili yapı konturlanır. | **Koronal, hippocampus düzeyi.** Cornu temporale, hippocampus ve amygdala, onları gösteren kesitte. |
| ![Orta hatta yakın sagital T1; sol yarım küre soyulmuş, corpus callosum, yan ventrikül, beyin sapı ve serebellum kesit üzerinde boyanmış](screenshots/sagittal-midline.webp) | ![x = -30 mm'de sagital T1 üzerinde kavis çizen sol fasciculus arcuatus; traktus atlası kesite soluk boyanmış, solda traktus ağacı açık](screenshots/tracts.webp) |
| **Sagital, hemiseksiyon.** Soyma kipi düzlemin bir yanındaki her şeyi gizler; kesit yüzeyine arkadaki MR ile birlikte bakarsınız. | **Traktuslar.** HCP1065 atlasından altmış ak madde demeti, üç boyutta ve kesitin üzerinde boyalı. |
| ![Arter sulama alanlarıyla renklendirilmiş aksiyal T1: arteria cerebri anterior turuncu, media pembe, posterior mavi; arterler üç boyutta](screenshots/territories.webp) | ![Sagital kesit foramen magnumun altında spinal kord MR'ına devam ediyor; servikal segment turuncu konturlu, torakal segment yeşil](screenshots/cord-mri.webp) |
| **Sulama alanları.** "Hangi damar bunu yapardı?" sorusunu kesitin kendisinde yanıtlar. | **Omurilik.** Foramen magnumun altında kesitler, atlasın kendi kordonu boyunca yeniden biçimlenmiş bir kord MR'ına devam eder; spinal düzeyler boyanmıştır. |

## Özellikler

- **Tek koordinat çerçevesi.** Meshler, T1/T2 hacimleri, etiket hacimleri ve kord MR'ı hep MNI152NLin2009cAsym RAS mm'dir.
- **Ağaç, arama ve seçim.** Her sistem ve alt sistem için üç durumlu kutular, tüm yapıları açıp kapatan ana anahtar, bir grubu yalnız bırakmak için Alt+tıklama ve yapılar, yolaklar ve sendromlar üzerinde arama (`>` yalnızca sendromlar için).
- **Üç boyutlu görünüm.** Döndürme, kaydırma ve imlece doğru yakınlaşma; bir meshe ya da MR kesitine tıklayarak seçme, çift tıklayarak çerçeveleme; `1`–`8` tuşlarında sekiz kamera ön ayarı. Anatomik paletli fiziksel tabanlı malzemeler ve ortam okluzyonu, yumuşak gölge ve kenar yumuşatma için bir **Kalite** düğmesi.
- **Kesitler.** T1/T2 ile aksiyal, koronal ve sagital; soyma kipleri, sulama alanı renklendirmesi, etiket konturları ve "tüm etiketler" boyaması. Bir kesit foramen magnuma indiği anda kord MR'ı kendiliğinden açılır, imlecin altındaki spinal düzeyi adlandırır ve düzeye tıklayınca o kord segmentini seçer.
- **Lezyon kipi.** `#/syndrome/<id>` sahneyi karartır, tutulan yapıları öne çıkarır, lezyon işaretini yerleştirir ve defisitleri sırayla gezer; **Yansıt** lezyonu diğer tarafa taşır.
- **İki dil.** Araç çubuğundaki **TR / EN** düğmesi ya da `L` ile İngilizce ve Türkçe. Seçim adres çubuğunda tutulur, böylece bir bağlantı kopyalandığı dilde açılır.
- **Her şeyin adresi var.** `#/structure/<id>`, `#/pathway/<id>`, `#/syndrome/<id>?step=n&side=l`, `#/topic/<id>`, `#/glossary`, `#/quiz`, `#/about`. Kısayollar için `?` tuşuna basın.
- **Görünümü paylaş.** Araç çubuğundaki **Görünümü paylaş**, sahneyi aynen kuran bir bağlantı kopyalar: kamera, görünen yapılar, kesitler, soyma, kontrast, açık panel. Sıradan bir bağlantı yalnızca rotayı ve kesit konumlarını taşır.
- **Hatırlayan vaka soruları.** Yanıtlar tarayıcınızda kalır, yenilemede kaybolmaz; soruları türe ya da zorluğa göre süzün ya da yalnızca yanlışlarınızı gözden geçirin.

## Klavye kısayolları

Uygulamada `?` tuşu bu listeyi açar.

| Tuş | İşlev |
|---|---|
| `1`–`8` | kamera açıları: lateral (sol), lateral (sağ), anterior, posterior, superior, inferior, medial (sol), medial (sağ) |
| `a` / `c` / `s` | aksiyal / koronal / sagital kesiti aç-kapat |
| `↑` / `↓` | son kullanılan kesiti 1 mm kaydır |
| `t` | kontrastı değiştir: T1 / T2 / kendi MR'ınız |
| `p` | `a` / `c` / `s` ile en son açılan kesitten soy (her kaydırıcının kendi soyma menüsü de var) |
| `[` / `]` | sol / sağ paneli aç-kapat |
| `f` | ara |
| `A`–`E` | açık vaka sorusunu yanıtla; `←` / `→` sorular arasında geçer |
| `L` | dili değiştir (English / Türkçe) |
| `Esc` | seçimi temizle / sendromdan çık |
| `Shift+S` | 3B görünümün ekran görüntüsü |
| `Shift`+tıklama | kesitleri oynatmadan seç |
| `Alt`+ağaçta bir sisteme ya da gruba tıklama | yalnızca o grubu göster |
| çift tıklama | tıklanan yapıyı çerçevele; boşlukta beyni ortala |

## Bağlantılar ve görünümü paylaşmak

Her rota bir bağlantıdır: `#/structure/<id>`, `#/pathway/<id>`, `#/syndrome/<id>?step=n&side=l`,
`#/topic/<id>`, `#/glossary`, `#/quiz`, `#/about`. Sıradan bir bağlantı kesit konumlarını (`ax`, `cor`,
`sag`), varsayılan dışı bir kontrastı (`c=t2w`, `c=subject-<id>`) ve varsayılan dışı dili (`lang=tr`) de taşır;
adres çubuğu her zaman aşağı yukarı gördüğünüz şeye bir bağlantıdır.

Araç çubuğundaki **Görünümü paylaş**, sahneyi *aynen* bağlantıya yazar ve kopyalar: kamera konumu ve hedefi,
görünen sistemler ve yapı bazındaki istisnalar, hangi kesitlerin açık olduğu, soyma, sabitleme, kontrast ve
açık panel. Sıradan bağlantılar kısa kalır; uzun biçim yalnızca istendiğinde yazılır.

## Kendi MR'ınızı eklemek

Atlas bir şablondur ve içindeki her şey — meshler, etiket hacimleri, kesitler — tek bir MNI152NLin2009cAsym
ızgarası üzerindedir. Kişisel bir tarama bu yüzden atlasın kendisine *uyarlandığı* bir şey değildir; yapıların
zaten hizalı olduğu bu çerçevenin *içine taşınır* ve kontrast menüsünde T1 ile T2'nin yanında belirir:

```bash
cd pipeline && uv sync --extra subject && cd ..                     # kayıt için antspyx, DICOM için dcm2niix
uv run --project pipeline atlas-subject hasta-cd.zip --id ben
```

Elinizde ne varsa onu verin: hastanenin verdiği zip ya da klasör (DICOM — her seri
[dcm2niix](https://github.com/rordenlab/dcm2niix) ile dönüştürülür, tüm başı kapsayan 3B T1'e benzeyen seri
alınır, tablo yazdırılır, `--series N` ile seçim değiştirilir) ya da bir NIfTI. Ardından N4 bias düzeltmesi,
atlasın kendi MNI T1w'sine rijit + afin + **SyN** kaydı (tam `antsRegistrationSyN` tarifi, beş ile on dakika;
yalnızca afin kayıt girusları parsellerden milimetrelerce uzakta bırakır, kortikal etiketleri *sizin*
sulkuslarınıza oturtan deforme edilebilir aşamadır), atlas ızgarasına yeniden örnekleme ve beyne asla
dokunamayan, şablonun beyin maskesinden türetilmiş bir düzlemle **yüz silme** yapılır. Paylaşmadan önce
`pipeline/qa/subjects/ben/` klasörüne, özellikle önden görülen cilt yüzeyi `skin-front.png` dosyasına bakın.
Hacim, `pipeline/config/sources.yaml` içinde bir `subject_ben` kaydı ister (lisansı ve kimin taraması olduğunu
söyleyen bir satır); üç denetim de yüzü silinmemiş, kaynağı belirtilmemiş ya da yeniden dağıtılamayan bir
tarama hacmini reddeder. Taramanın kendisi depoya asla girmez. Paylaşılan bağlantı seçimi taşır:
`#/slice?c=subject-ben&ax=-2`.

## İki sürüm

Atlas aynı ağaçtan iki kez derlenir.

**Açık sürüm** yeniden dağıtılabilen sürümdür (kod Apache-2.0, veri ve içerik CC BY-SA 4.0) ve her yerde varsayılandır: `npm run dev` onu sunar, `npm run build` onu `dist/` içine derler ve `scripts/check-public.ts` yayımlanmadan önce bu derlemeyi denetler. **Özel sürüm** buna ek olarak, lisansı ticari olmayan kullanımla sınırlı ya da türev dosyaların aktarılmasını yasaklayan dört veri kümesini içerir; bu yüzden onu derleyen makineden hiç çıkmaz: `npm run dev:private`, `npm run build:private`.

| Veri kümesi | Lisans | Neden yayımlanamaz | Açık sürümdeki karşılığı |
|---|---|---|---|
| Harvard-Oxford (FSL) | `FSL-NC` | inceleme bekliyor — FSL, Ağustos 2025'te CC BY-SA 4.0'a geçirdi | CerebrA/DKT kortikal parselleri (CC0) |
| Diedrichsen serebellum atlası | `CC-BY-ND` | türev çalışmalar dağıtılamaz | kendi şablonumuzun FastSurfer CerebNet bölütlemesi (CC BY-SA 4.0) |
| Brainstem Navigator 7 T çekirdekleri | `BrainstemNavigator-NC-ND` | türev dosyalar kurum dışına çıkamaz | Dahl locus coeruleus meta-maskesi (CC BY 4.0) ve yayımlanmış hacimlerden kurulan işaret noktası tabanlı belirteçler |
| PAM50 kord şablonu | `PAM50-unlicensed` | deposunda hiçbir lisans yok | burada spine-generic ve Fudan tüm-omurga verisinden birleştirilen bir kord MR'ı (CC BY 4.0) |

Hiçbir şey adına göre ayıklanmaz: bir veri kümesi, lisans kaydında `nc: true` ya da `no_redistribution: true` taşıyorsa açık sürümden çıkar. Bu dördü `restricted` indirme grubundadır; `atlas-download` onları yalnızca `private` dalında ya da `ATLAS_ALLOW_RESTRICTED=1` ile indirir, böylece bu dalın düz bir klonu paylaşamayacağı veriyi üretemez. Sonuçta açık sürüm özel sürümden 202 mesh eksiktir ve yerine 132 karşılık koyar: 592'ye karşı 662.

Karşılıkların hiçbiri birebir kopya değildir; her birinin gerekçesi [İki sürüm](editions.md) içindedir.

## İçerik ve kaynaklar

**Sözlük dışındaki her kayıt yalnızca açık erişimli kaynaklara atıf verir**: NCBI Bookshelf üzerindeki StatPearls bölümleri, PubMed Central'daki makaleler, açık lisanslı başvuru sayfaları. Yayımlanan atlasın hiçbir yerinde basılı ders kitabına ya da ödeme duvarı ardındaki bir makaleye atıf yoktur. Bugün bu, **657 kaynak üzerinden 2384 atıf** demektir ve her atıf, canlı bölümden okunarak geldiği bölümü adlandırır.

Bir kaynakça kaydındaki `verified: true` yalnızca bir araç tarafından, canlı kaynak üstverisinden yazılır; elle asla. Bilinmeyen bir kaynağa atıf derlemeyi durdurur; `npm run citations:check` ise bozuk bir atıfta, doğrulanmamış bir kayıtta ya da hiçbir yerden atıf almayan bir kayıtta hata verir. Şemalar, yazım araçları ve kurallar için [İçerik ve kaynaklar](content.md).

## Türkçe sürüm

Arayüz İngilizce ve Türkçedir (`src/i18n/en.ts` ve `src/i18n/tr.ts`, 293 dizge; Türkçe tablo İngilizcesine göre tiplenmiştir, bu yüzden eksik bir anahtar tip denetimini düşürür). Türkçe kipte yapılar, kranial sinirler ve yolaklar Türk tıp eğitiminin adlandırdığı gibi, FIPAT'ın *Terminologia Neuroanatomica* ve *Terminologia Anatomica 2* listelerinden gelen Latince terimleriyle adlandırılır; İngilizce ad ikinci satırda kalır.

824 kaydın klinik metinlerinin tamamı da çevrilmiştir. Çeviriler `content/i18n/tr/` altında, üretildikleri İngilizce metnin özetine (hash) sabitlenmiş kaplamalar olarak durur; böylece İngilizce metin değiştiğinde çeviri sessizce yanlış kalmak yerine "eskimiş" olarak işaretlenir.

![Atlas Türkçe kipte: yapı ağacı ve panel, yapıları Latince adlarıyla, altında İngilizce adıyla gösteriyor; arayüz Türkçe ve üç boyutlu pencerenin altında makine destekli çeviri uyarısı](screenshots/turkish.webp)

> **Türkçe klinik metinler makine destekli çeviridir ve uzman incelemesi sürmektedir.** Makineyle ve terminoloji açısından denetlenmiştir; bir Türk nöroloğun incelemesinden ise henüz geçmemiştir. İki metin ayrıldığında İngilizce metin esastır. Uygulama bunu Türkçe kipte söyler; çevirisi eksik ya da eskimiş bir kayıt ise *English* etiketi taşır.

Terminoloji tablosunu, kaplama biçimini ve araçları [Türkçe sürüm](turkish-edition.md) anlatır.

## Veriyi kendiniz üretmek

`npm start` ile inen sürüm paketi üretilmiş bir çıktıdır; `npm run data:build` aynısını kaynak atlaslardan
yeniden üretir (birkaç GB indirme, uzun bir koşu, [uv](https://docs.astral.sh/uv/) gerekir). Buna yalnızca
meshlerin ya da hacimlerin nasıl yapıldığını değiştirmek için gerek duyarsınız; adımları ve isteğe bağlı ekleri
[Veriyi üretmek](pipeline.md) (İngilizce), tam sürümün kısıtlı veri kümelerini [İki sürüm](editions.md) anlatır.

## Lisanslar ve atıf

| Ne | Lisans | Dosya |
|---|---|---|
| Kod (`src/`, `scripts/`, `pipeline/`, `tools/`, `blender/`) | Apache License 2.0 | [LICENSE](../LICENSE) |
| Yazılmış içerik (`content/`) | CC BY-SA 4.0 | [content/LICENSE](../content/LICENSE) |
| Üretilen veri (`public/data/`) | CC BY-SA 4.0 | işlem hattının yazdığı `public/data/LICENSE` |

Meshler ve hacimler, [NOTICE](../NOTICE) dosyasında listelenen üçüncü taraf veri kümelerinin, kendi lisansları altında kullanılan **türevleridir**; yapılan değişiklikler: MNI152NLin2009cAsym uzayına kayıtlama, etiket maskelerinin işaretli mesafe alanı üzerinden yeniden meshlenmesi, yumuşatma, sınıf başına üçgen bütçesine indirgeme, komşu parsellerin kaynaştırılması, yeniden etiketleme ve renklendirme ve hiçbir kaynak atlasın vermediği meshlerin kurulması. Her kaynak lisansı, kendisinden türetilene CC BY-SA 4.0 ile birlikte uygulanmaya devam eder.

`NOTICE` üretilir, elle düzenlenmez; her veri kümesi için atıf, lisans ve indirme adresleriyle bir blok içerir ve `npm run notice -- --check` dosya eskidiyse hata verir. Lisans metinlerinin tamamı veriyle birlikte `public/data/licenses/` altında gider. Uygulamada **Hakkında** (ya da `#/about`), yüklü derlemedeki her kaynağı lisansı, atfı ve tam metin bağlantısıyla listeler.

**Nasıl atıf verilir:** Ayci B. *Clinical Neuroanatomy Atlas*, v1.0.2, 2026. Kod Apache 2.0, veri ve içerik CC BY-SA 4.0; `NOTICE` içindeki veri kümelerinden türetilmiştir. Meshleri kullanırken kaynak veri kümelerine, metin için `content/bibliography/` altındaki açık erişimli kaynaklara da atıf verin.

## Bilinen sınırlar

- **Türkçe klinik metinler bir hekim tarafından incelenmemiştir** (yukarıya bakın). Esas metin İngilizcedir.
- **Atlas bir şablondur, bir hasta değil.** Grup ortalaması parselasyonlar ve kayıtlanmış tek bir örnek; içindeki hiçbir şey bir bireyin ölçümü değildir.
- **Açık sürümün beyin sapı çekirdekleri konum belirteçleridir**, bölütleme değil: yayımlanmış hacim kadar elipsoidler, açık işaret noktalarına göre yerleştirilmiştir; çünkü kopyalanabilecek açık lisanslı bir 7 T çekirdek atlası yoktur. Panelde ve `manifest.derived` içinde nasıl kuruldukları açıkça yazılıdır.
- **Bazı yapıların iki sürümde de meshi yoktur.** Vena thalamostriata venöz atlasta vena cerebri interna'dan ayrılamıyor; birkaç kayıt benzer nedenlerle yalnızca metindir.
- **On iki mesh bölütlenmemiş, kurulmuştur** (nervus phrenicus, kord segment blokları, truncus lumbosacralis, dördüncü ventrikülün pleksus koroideusu) ve göründükleri her yerde şematik olarak işaretlenmiştir.
- **Genel nöron ve glia biyolojisi** yalnızca bir konuya değdiği ölçüde işlenmiştir (transmitterler, sinir hasarı, kortikal katmanlar).
- **Masaüstü penceresi için tasarlanmıştır.** 1100 pikselin altında paneller daralır, 900 pikselin altında ise 3B görünümün üzerine yerleşir ve kapalı başlar; böylece tablette ya da yarım genişlikte pencerede kullanılabilir kalır. Yine de tasarımın dayandığı düzen üç sütunludur ve telefonda elde edilen şey, telefona özgü bir arayüz değil, çalışan bir 3B görünümdür.

## Yol haritası

- Çevrilmiş metinlerin bir Türk nörolog tarafından kayıt kayıt incelenmesi.
- PAM50 şablonu için bir lisans. `pipeline/raw/pam50/LICENSE_REQUEST_DRAFT.txt` yazarlara gönderilmemiş bir istek taslağıdır; lisans belirtirlerse özel kord MR'ı, ölçülmüş kord segmentleri ve PAM50 ile kesilen filum terminale de açık sürümde yer alabilir ve iki sürüm arasındaki fark o kadar azalır.
- Periferik sinir sisteminin daha geniş kapsanması: bugünkü kapsam klinik olarak yük taşıyan sinirlerdir, eksiksiz bir periferik atlas değil.
- Masaüstü düzeninin küçülmesi yerine, telefonlar için tasarlanmış bir düzen.
