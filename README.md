# Clinical Neuroanatomy Atlas

**English** · [Türkçe](#klinik-nöroanatomi-atlası)

A browser-based 3D atlas of clinical neuroanatomy: 585 meshes, synchronised MRI slices, arterial territories, traced pathways, a lesion mode that shows you what a syndrome does and why, plus clinical topics, a glossary and a quiz. Everything lives in one coordinate frame — MNI152NLin2009cAsym RAS millimetres — so the surfaces, the T1/T2 slices and the label overlays line up exactly, and below the foramen magnum the slices continue into a spinal cord MRI reformatted along the atlas's own cord. Every entry cites open-access sources that anyone can read for free. It runs locally, from static files, with no server and no account.

**[Open the live demo →](https://aycibatuhan.github.io/nervous-system-atlas/)**  — the same public edition, nothing to install.

> **Not for clinical use.** This is an educational reference. Its structures are group-average templates and a registered specimen, not any patient's anatomy; its syndrome, imaging and management text is a teaching summary written from the cited sources and may be incomplete, out of date or wrong. Nothing in it is medical advice, and it must not be used to diagnose, treat or make decisions about a patient. Clinical decisions belong to qualified clinicians using current guidelines and the patient's own findings and imaging.

![The atlas on first paint: the cortical surface and the vessels in the 3D view, the structure tree on the left, the slice controls along the foot of the window](docs/screenshots/overview.webp)

## Quick start

[Node.js](https://nodejs.org) 22 or newer, then three lines:

```bash
git clone https://github.com/aycibatuhan/nervous-system-atlas.git
cd nervous-system-atlas
npm start
```

`npm start` installs the dependencies, fetches the atlas data (49 MB, verified against a checksum pinned in the
repository) and serves the app at <http://localhost:5173>. From then on it simply starts. `npm run build` writes
a copy into `dist/` that any static web server can host.

## What it looks like

| | |
|---|---|
| ![An axial T1 slice with the deep grey nuclei painted on it and the putamen outlined in orange, its content panel open on the right](docs/screenshots/slices-mri.webp) | ![The lateral medullary syndrome in lesion mode: the scene dimmed to the involved structures, the lesion marker on the left medulla, and the deficit table stepping through the signs](docs/screenshots/syndrome-wallenberg.webp) |
| **Slices and 3D in one frame.** Click the MRI to select a structure, or a structure to move the slices. | **Lesion mode.** A syndrome dims the scene to what it involves and steps through its deficits. |
| ![The lateral corticospinal tract with its neuron chain, decussation and numbered course in the right-hand panel](docs/screenshots/pathway.webp) | ![The cranial nerves seen from below with the arteries, the trigeminal nerve selected and its course, nuclei and branches listed](docs/screenshots/cranial-nerves.webp) |
| **Pathways.** Neuron chain, where it crosses, and every station as a clickable waypoint. | **Cranial nerves.** Nuclei, course, branches, reflexes, bedside tests and localising signs. |
| ![A clinical vignette asking where the lesion is, with five answer options](docs/screenshots/quiz.webp) | ![The same syndrome page in Turkish, with Latin structure names and the machine-assisted translation notice along the foot of the view](docs/screenshots/turkish-syndrome.webp) |
| **Quiz.** 60 original vignettes; answering spotlights the structures in 3D. | **Turkish.** The whole interface and all the clinical prose, structures named in Latin. |

## What is in it

| Kind | Count | Notes |
|---|---|---|
| Structures | 379 | deep cerebral veins, cord segments, lobes and gyri, hippocampal subfields, basal forebrain, thalamic and hypothalamic nuclei, brainstem nuclei, cerebellar lobules, white-matter tracts, arterial territories, ventricles, meninges, arteries, peripheral and cutaneous nerves, autonomic |
| Cranial nerves | 12 | nuclei, course, branches, reflexes, bedside tests, localising signs |
| Pathways | 25 | neuron chain, decussation, clickable waypoints, lesion effects by level |
| Syndromes | 125 | localisation, deficits with substrates, crossing logic, imaging, mimics, management pearls |
| Topics | 19 | development, CSF and the blood–brain barrier, neurotransmitters, sleep and EEG, epilepsy, headache, dementia, movement disorders, neuromuscular patterns, paediatric syndromes, localisation, imaging, stroke, infection, tumours, leukodystrophies, nerve injury, cortical layers, coma |
| Glossary | 205 | |
| Quiz | 60 | original vignettes; the answer spotlights the structures in 3D |
| Meshes | 585 public / 655 private | MNI atlases remeshed from label masks, the VENAT venous atlas, BodyParts3D and Z-Anatomy geometry registered by landmarks, and meshes constructed here from geometry no atlas provides (12 in both editions, 40 in the public one); 36 MB at full detail, about 3.5 MB on first paint |
| Citations | 2384 | to 657 open-access sources, across all 824 entries |

## Going further

| | |
|---|---|
| [User guide](docs/guide.md) | every feature — slices and peel modes, lesion mode, pathways, the cord MRI, links that reproduce a view, keyboard shortcuts, the quiz, the Turkish edition, showing your own MRI — and what the atlas deliberately leaves out |
| [Contributing](CONTRIBUTING.md) | working on the code, the content and the translations; `npm run check` runs every check in one go |
| [Building the data](docs/pipeline.md) | regenerating the meshes and volumes from the source atlases with `npm run data:build` instead of downloading them, and [the two editions](docs/editions.md) the pipeline can produce |
| [Changelog](CHANGELOG.md) | what changed in each version |

## Licences

| What | Licence | File |
|---|---|---|
| Code (`src/`, `scripts/`, `pipeline/`, `tools/`, `blender/`) | Apache License 2.0 | [LICENSE](LICENSE) |
| Authored content (`content/`) | CC BY-SA 4.0 | [content/LICENSE](content/LICENSE) |
| Generated data (`public/data/`) | CC BY-SA 4.0 | written by the pipeline into `public/data/LICENSE` |

The meshes and volumes are derivatives of the third-party datasets credited in [NOTICE](NOTICE) and in the app's
**About** panel, each under its own licence. To cite the atlas: Ayci B. *Clinical Neuroanatomy Atlas*, v1.0.2,
2026 — and cite the source datasets themselves when you use the meshes. The details are in the
[user guide](docs/guide.md#licences-and-attribution).

## Contributing, security and contact

Pull requests are welcome — read [CONTRIBUTING.md](CONTRIBUTING.md) first, especially the two-branch layout and what must never be committed. Licence, redistribution or data-integrity concerns go to the address in [SECURITY.md](SECURITY.md) rather than a public issue. Clinically wrong or dangerous content is an ordinary issue, and a welcome one.

---

<a id="klinik-nöroanatomi-atlası"></a>

# Klinik Nöroanatomi Atlası

*(This is the Turkish version of the document above. [Back to English](#clinical-neuroanatomy-atlas).)*

Tarayıcıda çalışan üç boyutlu bir klinik nöroanatomi atlası: 585 mesh, eşzamanlı MR kesitleri, arter sulama alanları, izlenebilir yolaklar, bir sendromun neyi nasıl bozduğunu gösteren lezyon kipi, klinik konular, bir sözlük ve vaka soruları. Her şey tek bir koordinat çerçevesindedir (MNI152NLin2009cAsym RAS milimetre), bu yüzden yüzeyler, T1/T2 kesitleri ve etiket kaplamaları tam olarak çakışır; foramen magnumun altında kesitler, atlasın kendi omuriliği boyunca yeniden biçimlenmiş bir spinal kord MR'ına devam eder. Her kayıt, herkesin ücretsiz okuyabileceği açık erişimli kaynaklara atıf verir. Uygulama yerelde, statik dosyalardan çalışır; sunucu da hesap da gerektirmez.

**[Canlı demoyu açın →](https://aycibatuhan.github.io/nervous-system-atlas/)**  — aynı genel sürüm, hiçbir kurulum gerekmez.

> **Klinik kullanım için değildir.** Bu atlas eğitim amaçlı bir başvuru kaynağıdır. İçindeki yapılar grup ortalaması şablonlar ve kayıtlanmış bir örnektir, hiçbir hastanın kendi anatomisi değildir; sendrom, görüntüleme ve tedavi metinleri ise belirtilen kaynaklardan yazılmış öğretim özetleridir ve eksik, güncelliğini yitirmiş ya da yanlış olabilir. Buradaki hiçbir bilgi tıbbi tavsiye değildir; hastaya tanı koymak, tedavi vermek ya da hastayla ilgili karar almak için kullanmayın. Bu kararlar, güncel kılavuzları ve hastanın kendi bulgularını ve görüntülerini kullanan yetkin hekimlere aittir.

![Atlasın açılış görünümü: üç boyutlu pencerede korteks yüzeyi ve damarlar, solda yapı ağacı, altta kesit denetimleri](docs/screenshots/overview.webp)

## Hızlı başlangıç

[Node.js](https://nodejs.org) 22 ya da üstü, sonra üç satır:

```bash
git clone https://github.com/aycibatuhan/nervous-system-atlas.git
cd nervous-system-atlas
npm start
```

`npm start` bağımlılıkları kurar, atlas verisini indirir (49 MB; depoda sabitlenmiş bir özetle doğrulanır) ve
uygulamayı <http://localhost:5173> adresinde açar. Sonraki çalıştırmalarda yalnızca başlatır. `npm run build`,
`dist/` içine herhangi bir statik web sunucusunun barındırabileceği bir kopya yazar.

## Nasıl görünüyor

| | |
|---|---|
| ![Derin gri çekirdeklerin boyandığı aksiyal T1 kesiti, putamen turuncu konturla işaretli, sağda içerik paneli açık](docs/screenshots/slices-mri.webp) | ![Lezyon kipinde lateral medüller sendrom: sahne yalnızca tutulan yapılara indirgenmiş, sol medullada lezyon işareti, defisit tablosu bulguları tek tek geziyor](docs/screenshots/syndrome-wallenberg.webp) |
| **Kesit ve üç boyut aynı çerçevede.** MR'a tıklayarak yapıyı seçin ya da bir yapıya tıklayarak kesitleri oraya taşıyın. | **Lezyon kipi.** Sendrom, sahneyi tuttuğu yapılara indirger ve defisitleri sırayla gösterir. |
| ![Tractus corticospinalis lateralis'in nöron zinciri, çaprazlaşması ve numaralı seyri sağ panelde](docs/screenshots/pathway.webp) | ![Alttan bakışta kranial sinirler ve arterler; nervus trigeminus seçili, seyri, çekirdekleri ve dalları listeleniyor](docs/screenshots/cranial-nerves.webp) |
| **Yolaklar.** Nöron zinciri, nerede çaprazlaştığı ve her durağı tıklanabilir bir ara nokta olarak. | **Kranial sinirler.** Çekirdekler, seyir, dallar, refleksler, yatak başı testler ve lokalize edici bulgular. |
| ![Lezyonun yerini soran bir klinik vaka, beş seçenekle](docs/screenshots/quiz.webp) | ![Aynı sendrom sayfası Türkçe: Latince yapı adları ve makine destekli çeviri uyarısı](docs/screenshots/turkish-syndrome.webp) |
| **Vaka soruları.** 60 özgün vaka; yanıtlayınca ilgili yapılar üç boyutta öne çıkar. | **Türkçe.** Arayüzün tamamı ve bütün klinik metinler, yapı adları Latince. |

## İçindekiler

| Tür | Sayı | Not |
|---|---|---|
| Yapılar | 379 | derin serebral venler, kord segmentleri, loblar ve giruslar, hippokampal alt alanlar, bazal ön beyin, talamik ve hipotalamik çekirdekler, beyin sapı çekirdekleri, serebellar lobüller, ak madde traktusları, arter sulama alanları, ventriküller, meninksler, arterler, periferik ve kutanöz sinirler, otonom yapılar |
| Kranial sinirler | 12 | çekirdekler, seyir, dallar, refleksler, yatak başı testler, lokalize edici bulgular |
| Yolaklar | 25 | nöron zinciri, çaprazlaşma, tıklanabilir ara noktalar, düzeye göre lezyon etkileri |
| Sendromlar | 125 | lokalizasyon, anatomik zeminiyle defisitler, taraf mantığı, görüntüleme, ayırıcı tanılar, tedavi incileri |
| Konular | 19 | gelişim, BOS ve kan-beyin bariyeri, nörotransmitterler, uyku ve EEG, epilepsi, baş ağrısı, demans, hareket bozuklukları, nöromusküler desenler, pediatrik sendromlar, lokalizasyon, görüntüleme, inme, enfeksiyon, tümörler, lökodistrofiler, sinir hasarı, kortikal katmanlar, koma |
| Sözlük | 205 | |
| Vaka soruları | 60 | özgün vakalar; yanıt, ilgili yapıları üç boyutta öne çıkarır |
| Mesh | 585 açık / 655 özel | etiket maskelerinden yeniden meshlenen MNI atlasları, VENAT venöz atlası, işaret noktalarıyla kayıtlanan BodyParts3D ve Z-Anatomy geometrisi ve hiçbir atlasın vermediği, burada kurulan meshler (iki sürümde de 12, açık sürümde 40); tam ayrıntıda 36 MB, ilk boyamada yaklaşık 3,5 MB |
| Atıflar | 2384 | 824 kaydın tamamında, 657 açık erişimli kaynağa |

## Daha fazlası

| | |
|---|---|
| [Kullanım kılavuzu](docs/guide.tr.md) | her özellik — kesitler ve soyma kipleri, lezyon kipi, yolaklar, kord MR'ı, bir görünümü aynen kuran bağlantılar, klavye kısayolları, vaka soruları, Türkçe sürüm, kendi MR'ınızı göstermek — ve atlasın bilerek dışarıda bıraktıkları |
| [Katkı](CONTRIBUTING.md) | kod, içerik ve çeviriler üzerinde çalışmak; `npm run check` bütün denetimleri tek seferde koşturur |
| [Veriyi üretmek](docs/pipeline.md) | meshleri ve hacimleri indirmek yerine `npm run data:build` ile kaynak atlaslardan yeniden üretmek ve işlem hattının üretebildiği [iki sürüm](docs/editions.md) |
| [Değişiklik günlüğü](CHANGELOG.md) | her sürümde ne değişti |

## Lisanslar

| Ne | Lisans | Dosya |
|---|---|---|
| Kod (`src/`, `scripts/`, `pipeline/`, `tools/`, `blender/`) | Apache License 2.0 | [LICENSE](LICENSE) |
| Yazılmış içerik (`content/`) | CC BY-SA 4.0 | [content/LICENSE](content/LICENSE) |
| Üretilen veri (`public/data/`) | CC BY-SA 4.0 | işlem hattının yazdığı `public/data/LICENSE` |

Meshler ve hacimler, [NOTICE](NOTICE) dosyasında ve uygulamanın **Hakkında** panelinde adı geçen üçüncü taraf
veri kümelerinin, her biri kendi lisansı altında, türevleridir. Atıf için: Ayci B. *Clinical Neuroanatomy
Atlas*, v1.0.2, 2026 — meshleri kullanırken kaynak veri kümelerine de atıf verin. Ayrıntılar
[kullanım kılavuzunda](docs/guide.tr.md#lisanslar-ve-atıf).

## Katkı, güvenlik ve iletişim

Katkılar beklenir; önce [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını, özellikle iki dallı düzeni ve `main` dalına asla konmaması gerekenleri okuyun. Lisans, yeniden dağıtım ya da veri bütünlüğüyle ilgili endişeler için genel bir issue yerine [SECURITY.md](SECURITY.md) içindeki adrese yazın. Klinik olarak yanlış ya da tehlikeli içerik ise sıradan bir issue konusudur ve bildirilmesi memnuniyetle karşılanır.
