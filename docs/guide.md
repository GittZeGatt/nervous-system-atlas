# User guide

Everything the atlas can do, for someone who has it running (see the [README](../README.md) for that).
Türkçe: [Kullanım kılavuzu](guide.tr.md).

## Sections, tracts and territories

Every slice is the same MRI the meshes are registered to, so a structure can be read on the section and in
three dimensions at once. Click the slice to select what is under the cursor, or click a structure to move the
slices to it.

| | |
|---|---|
| ![Axial T1 through the internal capsule at z = 16 mm, the caudate and thalamus drawn over the slice and the left internal capsule outlined, its content panel open on the right](screenshots/axial-capsule.webp) | ![Coronal T1 at the hippocampal body, the lateral ventricles in blue and the hippocampi and amygdalae in pink over the slice, the left hippocampus outlined](screenshots/coronal-temporal.webp) |
| **Axial, through the internal capsule.** The label overlay paints the deep grey nuclei on the MRI; the selected structure is outlined. | **Coronal, at the hippocampus.** The temporal horn, the hippocampi and the amygdalae on the section that shows them. |
| ![Near-midline sagittal T1 with the left hemisphere peeled away, showing the corpus callosum, the lateral ventricle, the brainstem and the cerebellum painted on the section](screenshots/sagittal-midline.webp) | ![The left arcuate fasciculus arching over a sagittal T1 at x = -30 mm, with the tract atlas painted faintly on the slice and the tract tree open on the left](screenshots/tracts.webp) |
| **Sagittal, hemisected.** Peel mode hides everything on one side of the plane, so you look at the cut surface with the MRI behind it. | **Tracts.** Sixty white-matter bundles from the HCP1065 atlas, in 3D and painted on the slice. |
| ![Axial T1 tinted with the arterial territories, anterior cerebral in orange, middle cerebral in pink, posterior cerebral in blue, with the arteries in 3D](screenshots/territories.webp) | ![The sagittal slice continuing below the foramen magnum into the cord MRI, the cervical cord segment outlined in orange and the thoracic segment in green](screenshots/cord-mri.webp) |
| **Arterial territories.** The territory tint answers "which vessel would do this?" on the section itself. | **The cord.** Below the foramen magnum the slices continue into a cord MRI reformatted along the atlas's own cord, with the spinal levels painted. |

## Features

- **One coordinate frame.** Meshes, T1/T2 volumes, label volumes and the cord MRI are all MNI152NLin2009cAsym RAS mm.
- **Tree, search and selection.** Tri-state checkboxes per system and subsystem, an all-structures master switch, Alt-click to solo a group, and a search over structures, pathways and syndromes (`>` for syndromes only).
- **3D view.** Orbit, pan and zoom toward the cursor; click a mesh or the MRI slice to select, double-click to frame it; eight camera presets on keys `1`–`8`. Physically based materials with an anatomical palette, and a **Quality** switch for ambient occlusion, soft shadows and anti-aliasing.
- **Slices.** Axial, coronal and sagittal with T1/T2, peel modes, arterial-territory tint, label outlines and an "all labels" paint; the cord MRI switches itself on as soon as a slice reaches the foramen magnum, names the spinal level under the cursor and lets you click one to select that cord segment.
- **Syndrome mode.** `#/syndrome/<id>` dims the scene, highlights the involved structures, places the lesion marker and steps through the deficits; **Mirror** moves the lesion to the other side.
- **Your own MRI.** A personal T1 scan can be registered into the atlas space and shown on the slices next to the template's T1/T2, with every mesh and label already lined up on it — see [Adding your own MRI](#adding-your-own-mri). Defaced before it ships, always.
- **Two languages.** English and Turkish, switched with the **TR / EN** button or `L`, kept in the URL so a link opens in the language it was copied in.
- **Everything addressable.** `#/structure/<id>`, `#/pathway/<id>`, `#/syndrome/<id>?step=n&side=l`, `#/topic/<id>`, `#/glossary`, `#/quiz`, `#/about`. Press `?` for the shortcuts.
- **Share view.** The toolbar's **Share view** copies a link that reproduces the scene exactly — camera, visible structures, slices, peels, contrast, open panel — where a plain link carries only the route and the slice positions.
- **Quiz that remembers.** Answers stay in your browser across reloads; filter the vignettes by type or difficulty, or review only the ones you missed.

## Keyboard shortcuts

Press `?` in the app for this list.

| Key | Does |
|---|---|
| `1`–`8` | camera presets: lateral (L), lateral (R), anterior, posterior, superior, inferior, medial (L), medial (R) |
| `a` / `c` / `s` | toggle the axial / coronal / sagittal slice |
| `↑` / `↓` | move the last touched slice by 1 mm |
| `t` | cycle the contrast: T1 / T2 / your own scan |
| `p` | peel at the last slice toggled with `a` / `c` / `s` (each slider also has a peel menu) |
| `[` / `]` | toggle the left / right panel |
| `f` | search |
| `A`–`E` | answer the open quiz vignette; `←` / `→` move between vignettes |
| `L` | switch language (English / Türkçe) |
| `Esc` | clear the selection / leave a syndrome |
| `Shift+S` | screenshot of the 3D view |
| `Shift`+click | select without moving the slices |
| `Alt`+click a system or group in the tree | show only that group |
| double-click | frame the clicked structure; on empty space, re-centre on the brain |

## Links and sharing a view

Every route is a hash: `#/structure/<id>`, `#/pathway/<id>`, `#/syndrome/<id>?step=n&side=l`, `#/topic/<id>`,
`#/glossary`, `#/quiz`, `#/about`. A plain link also carries the slice positions (`ax`, `cor`, `sag`), a
non-default contrast (`c=t2w`, `c=subject-<id>`) and a non-default language (`lang=tr`), so the address bar is
always a link to roughly what you see.

**Share view** in the toolbar writes the *exact* scene into the link and copies it: camera position and
target, the visible systems and per-structure overrides, which slices are on, the peels, the pin, the contrast
and the open panel. Ordinary links stay short; the long form is only written when you ask for it.

## Adding your own MRI

The atlas is a template, and everything in it — meshes, label volumes, slices — lives on one MNI152NLin2009cAsym
grid. A personal scan is therefore not something the atlas adapts *to*; it is carried *into* that frame, where the
structures already line up, and appears in the contrast menu next to T1 and T2:

```bash
cd pipeline && uv sync --extra subject && cd ..                     # antspyx for the registration, dcm2niix for DICOM
uv run --project pipeline atlas-subject path/to/patient-cd.zip --id me
```

Give it what you have: the zip or folder a hospital hands out (DICOM — every series is converted with
[dcm2niix](https://github.com/rordenlab/dcm2niix), the one that looks like a whole-head 3D T1 is taken, the
table is printed, `--series N` overrides), or a NIfTI. It then does N4 bias correction, rigid + affine + **SyN** registration onto the atlas's own MNI T1w — the full `antsRegistrationSyN` recipe, five to ten minutes (affine alone
leaves the gyri millimetres off the parcels; the deformable stage is what puts the cortical labels on *your*
sulci), a resample onto the atlas grid, and **defacing** with a plane derived from the template's brain mask
that cannot cut brain. Look at `pipeline/qa/subjects/me/` — especially `skin-front.png`, the skin surface seen
from the front — before you share anything. The volume needs a `subject_me` entry in
`pipeline/config/sources.yaml` (its licence and a line saying whose scan it is), and the three guards refuse a
subject volume that is undefaced, unattributed or not redistributable. The scan itself never enters the
repository. A shared link carries the choice: `#/slice?c=subject-me&ax=-2`.

## The two editions

The atlas is built twice from the same tree.

The **public edition** is what may be redistributed — Apache-2.0 code, CC BY-SA 4.0 data and content — and it is the default everywhere: `npm run dev` serves it, `npm run build` builds it into `dist/`, and `scripts/check-public.ts` gates that build before you can publish it. The **private edition** additionally contains four datasets whose licence is non-commercial or forbids passing derived files on, so it never leaves the machine that built it: `npm run dev:private`, `npm run build:private`.

| Dataset | Licence | Why it cannot ship | Replaced in the public edition by |
|---|---|---|---|
| Harvard-Oxford (FSL) | `FSL-NC` | held back pending review — FSL relicensed it to CC BY-SA 4.0 in Aug 2025 | CerebrA/DKT cortical parcels (CC0) |
| Diedrichsen cerebellar atlas | `CC-BY-ND` | no derivatives may be distributed | a FastSurfer CerebNet segmentation of our own template (CC BY-SA 4.0) |
| Brainstem Navigator 7 T nuclei | `BrainstemNavigator-NC-ND` | derived files may not leave the organisation | the Dahl locus coeruleus meta-mask (CC BY 4.0) and landmark-anchored markers built from published volumes |
| PAM50 cord template | `PAM50-unlicensed` | the repository ships no licence at all | a cord MRI composed here from spine-generic and Fudan whole-spine data (CC BY 4.0) |

Nothing is special-cased by name: a dataset leaves the public edition when its licence record carries `nc: true` or `no_redistribution: true`. Those four sit in the `restricted` download group, which `atlas-download` fetches only on the `private` branch or with `ATLAS_ALLOW_RESTRICTED=1`, so a plain clone of this branch cannot build data it may not share. That leaves the public edition 202 meshes short of the private one and puts 132 replacements back, for 592 against 662.

The substitutions are worth reading about — none of them is a like-for-like copy, and the reasoning for each is in [The two editions](editions.md).

## Content and citations

**Every non-glossary entry cites open-access sources only**: StatPearls chapters on the NCBI Bookshelf, articles in PubMed Central, openly licensed reference pages. No printed textbook is cited anywhere in the shipped atlas, and no paywalled article. Today that is **2384 citations over 657 sources**, and a citation names the section it came from, read from the live chapter.

`verified: true` on a bibliography entry is only ever written by a tool from live source metadata, never by hand. The build fails on an unknown reference, and `npm run citations:check` fails on a malformed citation, an unverified entry or an entry nothing cites. See [Content and citations](content.md) for the schemas, the authoring tools and the rules.

## Turkish edition

The interface exists in English and Turkish (`src/i18n/en.ts` and `src/i18n/tr.ts`, 293 strings, the Turkish table typed against the English one so a missing key fails the typecheck). In Turkish mode structures, cranial nerves and pathways are named the way Turkish medical teaching names them — by their Latin term, from FIPAT's *Terminologia Neuroanatomica* and *Terminologia Anatomica 2* — with the English name as a secondary line.

All 824 entries' clinical prose is translated too, as overlays under `content/i18n/tr/` that pin a hash of the English text they were made from, so an English edit shows up as stale rather than as silently wrong Turkish.

![The atlas in Turkish: the structure tree and panel naming structures by their Latin terms with the English name beneath, the interface in Turkish, and the machine-assisted translation notice along the foot of the 3D view](screenshots/turkish.webp)

> **The Turkish clinical prose is a machine-assisted translation and is still under specialist review.** It has been checked mechanically and for terminology, but not by a Turkish neurologist. Where the two texts differ, the English is the reference. The app says so in Turkish mode, and an entry whose translation is missing or stale carries an *English* tag instead.

[The Turkish edition](turkish-edition.md) covers the terminology table, the overlay format and the tooling.

## Building the data yourself

The release bundle that `npm start` fetches is generated; `npm run data:build` regenerates it from the source
atlases (several GB of downloads, a long run, needs [uv](https://docs.astral.sh/uv/)). You only need this to
change how the meshes or volumes are made — [Building the data](pipeline.md) describes the steps and the
optional extras, and [the two editions](editions.md) covers the restricted datasets of the full edition.

## Licences and attribution

| What | Licence | File |
|---|---|---|
| Code (`src/`, `scripts/`, `pipeline/`, `tools/`, `blender/`) | Apache License 2.0 | [LICENSE](../LICENSE) |
| Authored content (`content/`) | CC BY-SA 4.0 | [content/LICENSE](../content/LICENSE) |
| Generated data (`public/data/`) | CC BY-SA 4.0 | written by the pipeline into `public/data/LICENSE` |

The meshes and volumes are **derivatives** of the third-party datasets listed in [NOTICE](../NOTICE), used under their own licences, with changes: registration into MNI152NLin2009cAsym space, remeshing of the label masks through a signed-distance field, smoothing, decimation to per-class triangle budgets, welding of neighbouring parcels, relabelling and recolouring, and the construction of meshes no source atlas provides. Each source licence keeps applying to what is derived from it, alongside CC BY-SA 4.0.

`NOTICE` is generated, never edited by hand — one block per dataset with its citation, licence and download URLs — and `npm run notice -- --check` fails if it is stale. Verbatim licence texts ship with the data in `public/data/licenses/`. In the app, **About** (or `#/about`) lists every source in the loaded build with its licence, its citation and a link to the full text.

**How to cite:** Ayci B. *Clinical Neuroanatomy Atlas*, v1.0.2, 2026. Code Apache 2.0, data and content CC BY-SA 4.0, derived from the datasets in `NOTICE`. Cite the source datasets themselves when you use the meshes, and the open-access references in `content/bibliography/` for the text.

## Known limitations

- **The Turkish clinical prose has not been reviewed by a clinician** (see above). The English text is the reference.
- **The atlas is a template, not a patient.** Group-average parcellations and one registered specimen; nothing in it is a measurement of an individual.
- **The public edition's brainstem nuclei are location markers**, not delineations: ellipsoids of the published volume placed against open landmarks, because no openly licensed 7 T nucleus atlas exists to copy. They are honest about their own construction in the panel and in `manifest.derived`.
- **Some structures have no mesh in either edition.** The thalamostriate vein is not separable from the internal cerebral vein in the venous atlas, and a handful of entries are text-only for the same kind of reason.
- **Twelve meshes are constructed, not segmented** — the phrenic nerves, cord segment blocks, the lumbosacral trunk, the fourth-ventricle choroid plexus — and are flagged as schematic wherever they appear.
- **General neuron and glial biology is covered only where it touches a topic** (transmitters, nerve injury, cortical layers).
- **Built for a desktop window.** Below 1100px the panels narrow, and below 900px they float over the 3D view and start closed, so the atlas stays usable on a tablet or a half-width window — but the three-column layout is still what it is designed around, and a phone gets a workable 3D view rather than a phone interface.

## Roadmap

- A Turkish neurologist's review of the translated prose, entry by entry.
- A licence for the PAM50 template. `pipeline/raw/pam50/LICENSE_REQUEST_DRAFT.txt` is a drafted, unsent request; if the authors state one, the private cord MRI, the measured cord segments and the PAM50-cut filum could all ship publicly and the two editions would differ by that much less.
- More of the peripheral nervous system: the current coverage is the clinically load-bearing nerves, not a complete peripheral atlas.
- A layout designed for phones, rather than the desktop one degrading gracefully.
