"""Step 02b: an individual's T1w MRI, registered into the atlas space and defaced, as an extra slice contrast.

    uv run atlas-subject path/to/t1w.nii.gz --id me
    uv run atlas-subject path/to/patient-cd.zip --id me      # or the DICOM folder itself

The atlas is a template: every mesh, label volume and slice lives on the MNI152NLin2009cAsym 1 mm grid. A
personal scan therefore does not change the atlas -- it is carried INTO that frame, where the meshes and the
label overlays already line up, and becomes one more entry in the contrast menu next to T1 and T2.

What happens to the scan:
  0. DICOM (a folder, or the zip a hospital hands out) is converted with dcm2niix, every series, and the one
     that looks most like a whole-head 3D T1 is taken (`--series` overrides; the table is printed).
  1. N4 bias-field correction.
  2. rigid + affine + SyN registration onto raw/mni_t1w/tpl-MNI152NLin2009cAsym_res-01_T1w.nii.gz (antspyx,
     the pipeline's [subject] extra). The metric is confined to the template's brain mask dilated by FIXED_MASK_MM,
     so the face, the neck and the scanner table never steer the fit. Affine alone leaves the gyri several
     millimetres off the parcels; the deformable stage is what makes the cortical labels sit on this person's
     sulci. Both stages' similarity to the template is measured and recorded.
  3. resampling onto the atlas grid with the forward transforms (linear interpolation).
  4. DEFACING, in MNI space, with one fixed shear plane computed from the template's own brain mask: the facet
     of the (sagittally projected, dilated) mask's convex hull that removes the most head, so it cannot cut
     brain and takes the eyes, nose and mouth. The plane is the same for every subject, which is exactly the
     point: whether a face survives is decided once, on the template, and verified in qa/subjects/<id>/.
  5. windowing like the template (0 .. the 99.5th percentile inside the brain mask) to uint8, gzip, sidecar.

Outputs
  public/data/volumes/subject-<id>.u8.bin     the volume, x-fastest uint8, gzipped (like t1w.u8.bin)
  public/data/volumes/subject-<id>.json       the manifest entry: grid, window, source, licence, how it was
                                              registered and defaced (atlas-manifest picks every subject-*.json up)
  pipeline/work/subjects/<id>/                the ANTs transforms (forward and inverse) and the N4 image
  pipeline/raw/subject_<id>/SOURCE.json       the run record NOTICE points at for a `generated` source
  pipeline/qa/subjects/<id>/*.png             before/after: sagittal midline, the skin surface seen from the
                                              front, an axial slice through the orbits -- look before releasing

The source id `subject_<id>` must exist in config/sources.yaml (group `subjects`, `generated: true`, a licence
that may be redistributed) -- that is where the name, the consent statement and the licence live, and it is
what NOTICE, the manifest's source table and the About panel print. The scan itself stays out of the
repository: raw/ and public/data/ are ignored, and the tree guard refuses .nii files.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import nibabel as nib
from scipy import ndimage
from scipy.spatial import ConvexHull

from .download import load_sources
from .paths import QA, RAW, VOLUMES, WORK
from .spaces import GRID_AFFINE, GRID_SHAPE, load_ras, robust_window, to_uint8
from .volumes import MASK, T1

FIXED_MASK_MM = 12     # the registration metric sees the brain plus this much margin
DEFACE_MARGIN_MM = 6   # the shear plane stays at least this far outside the brain mask
FACE_Y_MM, FACE_Z_MM = 20.0, 10.0   # "the face" for choosing the plane: head anterior to y and below z (MNI mm)
MIN_ANTERIOR = 0.45    # the plane's outward normal must have at least this much anterior component (about 27 deg)
HEAD_PERCENTILE = 40   # voxels above this percentile of the template's non-zero intensities count as head
# Normalised mutual information with the template inside the brain mask after SyN, (H(a)+H(b))/H(a,b) over 48
# bins: 1.0 means the two say nothing about each other, and it does not care whether the scan's contrast matches
# the template's or is even inverted, which Pearson does (Pearson is still recorded, for information). Measured on
# four open T1s and Colin27 the fit that is right by eye lands at 1.08-1.11; the same scan shifted 4 mm gives
# 1.04, 8 mm 1.02, flipped front-to-back 1.01; a paediatric scan with flat contrast that visibly did not converge
# gave 1.02, and a QA phantom 1.01. The gate sits in the gap; the renders in qa/subjects/<id>/ remain the check.
MIN_SIMILARITY = 1.05  # below this the run fails
WARN_SIMILARITY = 1.07 # below this it says so
# The full antsRegistrationSyN.sh "s" recipe (rigid, affine, SyN with cross-correlation, proper multi-resolution
# schedules), not antspyx's quick "SyN" shortcut: on a paediatric scan with flat grey/white contrast the shortcut
# settled at NMI 1.018 (visibly off), the recipe at 1.082 -- at the price of 5-10 minutes instead of 40 s.
DEFAULT_TRANSFORM = "antsRegistrationSyN[s]"


def key_of(subject_id: str) -> str:
    return f"subject-{subject_id}"


def source_of(subject_id: str) -> str:
    return f"subject_{subject_id}"


# ---------------------------------------------------------------- the defacing plane
def deface_plane(mask: np.ndarray, head: np.ndarray) -> dict:
    """The shear plane, as a*y + b*z + c > 0 in MNI mm (independent of x). `mask` is the template brain mask
    and `head` the template's head voxels, both on the atlas grid.

    Every edge of the convex hull of the mask's sagittal projection is a line with the whole brain on one side,
    so cutting along one can never remove brain. Of the edges that face forward and down, the one that takes the
    most head voxels is the face."""
    dil = ndimage.binary_dilation(mask, iterations=DEFACE_MARGIN_MM)
    proj = dil.any(axis=0)                               # (y, z) index space
    jj, kk = np.nonzero(proj)
    pts = np.stack([jj + GRID_AFFINE[1, 3], kk + GRID_AFFINE[2, 3]], axis=1).astype(float)   # mm
    hull = ConvexHull(pts)
    y_mm = np.arange(GRID_SHAPE[1]) + GRID_AFFINE[1, 3]
    z_mm = np.arange(GRID_SHAPE[2]) + GRID_AFFINE[2, 3]
    head_yz = head.sum(axis=0)                           # head voxels per (y, z) column, summed over x
    # only the face counts: head in front of and below the brain. Scoring the whole head lets the neck win
    # and picks a near-horizontal plane that leaves the eyes in (measured: 0.41*y - 0.91*z, orbits intact).
    head_yz = head_yz * ((y_mm[:, None] > FACE_Y_MM) & (z_mm[None, :] < FACE_Z_MM))
    best = None
    for a, b, c in hull.equations:                       # a*y + b*z + c <= 0 inside the hull
        if not (a >= MIN_ANTERIOR and b < 0):            # outward normal must point anterior enough, and inferior
            continue
        outside = (a * y_mm[:, None] + b * z_mm[None, :] + c) > 0
        removed = int(head_yz[outside].sum())
        if best is None or removed > best["voxels_removed"]:
            best = {"a": float(a), "b": float(b), "c": float(c), "voxels_removed": removed}
    if best is None:
        raise SystemExit("deface: no anterior-inferior facet on the brain-mask hull (is the mask empty?)")
    return best


def face_mask(plane: dict) -> np.ndarray:
    """Boolean (x, y, z) on the atlas grid: True where the plane removes voxels."""
    y_mm = np.arange(GRID_SHAPE[1]) + GRID_AFFINE[1, 3]
    z_mm = np.arange(GRID_SHAPE[2]) + GRID_AFFINE[2, 3]
    yz = (plane["a"] * y_mm[:, None] + plane["b"] * z_mm[None, :] + plane["c"]) > 0
    return np.broadcast_to(yz[None, :, :], GRID_SHAPE)


# ---------------------------------------------------------------- DICOM -> NIfTI
T1_WORDS = re.compile(r"t1|mprage|mp-rage|mp2rage|spgr|fspgr|bravo|tfl|3d", re.I)
NOT_T1_WORDS = re.compile(r"t2|flair|dwi|dti|adc|trace|swi|tof|angio|pd|bold|fmri|asl|perf|localizer|localiser|scout|survey|"
                          r"calib|smartbrain|aahead|mip|derived", re.I)


def series_score(shape: tuple, zooms: tuple, desc: str, acq: str) -> tuple[int, str]:
    """How much a converted series looks like the whole-head 3D T1 the registration wants; the reason is printed."""
    why = []
    if len(shape) != 3 or min(shape) < 48:
        return -9, "not a 3D whole-head volume"
    if max(zooms) > 2.5:
        return -9, f"slices {max(zooms):.1f} mm apart"
    s = 0
    if T1_WORDS.search(desc): s += 2; why.append("named like a T1")
    if NOT_T1_WORDS.search(desc): s -= 3; why.append("named like something else")
    if max(zooms) / max(min(zooms), 1e-3) <= 1.6: s += 1; why.append("near-isotropic")
    if acq.upper() == "3D": s += 1; why.append("3D acquisition")
    return s, ", ".join(why) or "no clue in the name"


def to_nifti(scan: Path, work: Path, series: str | None) -> tuple[Path, dict]:
    """A NIfTI from whatever the person has: a NIfTI already, a folder of DICOM files, or the .zip a hospital
    hands out. DICOM goes through dcm2niix (BSD-2-Clause, the `subject` extra); every series is converted into
    work/subjects/<id>/nifti/ and the one that looks most like a whole-head 3D T1 is taken -- `--series` picks
    by series number instead. Nothing here ships: the converted files stay in work/."""
    if scan.suffix == ".nii" or scan.name.endswith(".nii.gz"):
        return scan, {"format": "nifti"}
    src = scan
    if scan.suffix.lower() == ".zip":
        src = work / "dicom"
        shutil.rmtree(src, ignore_errors=True)
        shutil.unpack_archive(str(scan), str(src))
    if not src.is_dir():
        sys.exit(f"{scan}: expected a NIfTI (.nii/.nii.gz), a folder of DICOM files, or a .zip of one")
    try:
        import dcm2niix  # noqa: PLC0415
    except ImportError:
        sys.exit("reading DICOM needs dcm2niix: `uv sync --extra subject`")
    out = work / "nifti"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    # -ba y: no names or dates in the sidecars; -z y: gzip; %s_%d: series number then description
    r = subprocess.run([str(dcm2niix.bin_path), "-z", "y", "-b", "y", "-ba", "y", "-f", "%s_%d", "-o", str(out), str(src)],
                       capture_output=True, text=True)
    (work / "dcm2niix.log").write_text(r.stdout + r.stderr)
    rows = []
    for nii in sorted(out.glob("*.nii.gz")):
        side = nii.with_name(nii.name[:-7] + ".json")
        meta = json.loads(side.read_text()) if side.exists() else {}
        img = nib.load(str(nii))
        shape = tuple(int(v) for v in img.shape); zooms = tuple(float(v) for v in img.header.get_zooms()[:len(shape)])
        desc = str(meta.get("SeriesDescription") or meta.get("ProtocolName") or nii.name)
        num = str(meta.get("SeriesNumber", nii.name.split("_")[0]))
        score, why = series_score(shape, zooms, desc, str(meta.get("MRAcquisitionType", "")))
        rows.append({"file": nii, "series": num, "description": desc, "shape": shape, "zooms": zooms, "score": score, "why": why})
    if not rows:
        sys.exit(f"dcm2niix found no image series in {src} (see {work / 'dcm2niix.log'})")
    if series is not None:
        pick = next((x for x in rows if x["series"] == str(series)), None)
        if pick is None:
            sys.exit(f"--series {series}: no such series; available: {', '.join(x['series'] for x in rows)}")
    else:
        pick = max(rows, key=lambda x: (x["score"], int(np.prod(x["shape"]))))
    print(f"  {len(rows)} series converted with dcm2niix {r.stdout.split('version')[1].split()[0] if 'version' in r.stdout else ''}:")
    for x in rows:
        mark = "->" if x is pick else "  "
        print(f"   {mark} series {x['series']:>4}  {x['description'][:40]:<40} {'x'.join(map(str, x['shape'])):>14}  "
              f"{'x'.join(f'{z:.2g}' for z in x['zooms']):>14} mm  {x['why']}")
    if series is None and pick["score"] < 1:
        sys.exit("none of these looks like a whole-head 3D T1; pick one with --series <number>")
    return pick["file"], {"format": "dicom", "series": pick["series"], "description": pick["description"], "seriesFound": len(rows)}


# ---------------------------------------------------------------- registration
def register(t1: Path, subject_id: str, transform: str, reuse: bool) -> tuple[np.ndarray, np.ndarray, dict]:
    """Returns (warped, affine_only, info): the subject on the atlas grid after the full transform and after the
    linear stages alone, both float32 (x, y, z), plus the run record."""
    try:
        import ants  # noqa: PLC0415
    except ImportError:
        sys.exit("atlas-subject needs antspyx: `uv sync --extra warp` (the pipeline's [warp] extra)")
    work = WORK / "subjects" / subject_id
    work.mkdir(parents=True, exist_ok=True)
    fixed = ants.image_read(str(T1))
    fixed_mask = ants.image_read(str(MASK))
    fixed_mask = ants.iMath(fixed_mask, "MD", FIXED_MASK_MM)     # morphological dilation, mm == voxels here
    src = load_ras(t1)
    info = {"input": {"file": str(t1), "shape": list(src.shape), "spacing": [round(float(z), 3) for z in src.header.get_zooms()[:3]]}}
    # files rather than in-memory conversion: the nibabel<->ants helpers have been renamed across antspyx releases
    n4_path = work / "n4.nii.gz"
    if reuse and n4_path.exists():
        moving = ants.image_read(str(n4_path))
    else:
        ras_path = work / "input_ras.nii.gz"
        nib.save(src, str(ras_path))
        moving = ants.n4_bias_field_correction(ants.image_read(str(ras_path)))
        ants.image_write(moving, str(n4_path))
    fwd = sorted(work.glob("fwd_*")); inv = sorted(work.glob("inv_*"))
    if reuse and fwd and inv:
        fwdtransforms = [str(p) for p in fwd]; invtransforms = [str(p) for p in inv]
        print(f"  reusing transforms in {work}")
    else:
        for p in fwd + inv:
            p.unlink()
        print(f"  {transform} registration onto the MNI T1w (metric inside the brain mask + {FIXED_MASK_MM} mm) ...")
        reg = ants.registration(fixed=fixed, moving=moving, type_of_transform=transform, mask=fixed_mask, random_seed=1)
        # antspyx writes its transforms into a temp dir; keep them (forward: warp then affine; inverse: affine then warp)
        fwdtransforms, invtransforms = [], []
        for i, p in enumerate(reg["fwdtransforms"]):
            dst = work / f"fwd_{i}{''.join(Path(p).suffixes)}"; shutil.copyfile(p, dst); fwdtransforms.append(str(dst))
        for i, p in enumerate(reg["invtransforms"]):
            dst = work / f"inv_{i}{''.join(Path(p).suffixes)}"; shutil.copyfile(p, dst); invtransforms.append(str(dst))
    warped = ants.apply_transforms(fixed=fixed, moving=moving, transformlist=fwdtransforms, interpolator="linear")
    linear = [p for p in fwdtransforms if p.endswith(".mat")]
    affine_only = ants.apply_transforms(fixed=fixed, moving=moving, transformlist=linear, interpolator="linear")

    def on_grid(img) -> np.ndarray:
        tmp = work / "_on_grid.nii.gz"
        ants.image_write(img, str(tmp))
        nb = nib.as_closest_canonical(nib.load(str(tmp)))
        assert nb.shape == GRID_SHAPE, nb.shape
        assert np.allclose(nb.affine, GRID_AFFINE, atol=1e-3), nb.affine
        arr = np.asanyarray(nb.dataobj).astype(np.float32)
        tmp.unlink()
        return arr

    info.update({"tool": f"antspyx {ants.__version__}", "transform": transform, "fixed": T1.name,
                 "fixed_mask": f"{MASK.name} dilated {FIXED_MASK_MM} mm", "transforms": [str(Path(p).name) for p in fwdtransforms]})
    return on_grid(warped), on_grid(affine_only), info


def similarity(a: np.ndarray, b: np.ndarray, mask: np.ndarray, bins: int = 48) -> float:
    """Normalised mutual information inside the mask (see MIN_SIMILARITY) -- the number that says whether the
    fit worked, whatever the scan's contrast. Each image is scaled to its 0.5-99.5 percentile range first."""
    def scaled(v: np.ndarray) -> np.ndarray:
        lo, hi = np.percentile(v, [0.5, 99.5])
        return np.clip((v - lo) / max(hi - lo, 1e-6), 0, 1)
    h, _, _ = np.histogram2d(scaled(a[mask].astype(np.float64)), scaled(b[mask].astype(np.float64)), bins=bins, range=[[0, 1], [0, 1]])
    p = h / h.sum()
    ent = lambda q: float(-(q[q > 0] * np.log(q[q > 0])).sum())  # noqa: E731
    return (ent(p.sum(1)) + ent(p.sum(0))) / ent(p)


def pearson(a: np.ndarray, b: np.ndarray, mask: np.ndarray) -> float:
    """Recorded alongside: it reads as 'how T1-like is this scan', not as 'did the fit work'."""
    return float(np.corrcoef(a[mask].astype(np.float64), b[mask].astype(np.float64))[0, 1])


# ---------------------------------------------------------------- QA renders
def qa_renders(subject_id: str, before: np.ndarray, after: np.ndarray, template: np.ndarray, mask_ref: np.ndarray) -> list[str]:
    import matplotlib  # noqa: PLC0415
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt  # noqa: PLC0415
    out = QA / "subjects" / subject_id
    out.mkdir(parents=True, exist_ok=True)
    x0 = int(-GRID_AFFINE[0, 3]); z_orbit = int(-25 - GRID_AFFINE[2, 3])

    def skin_from_front(v: np.ndarray) -> np.ndarray:
        """Depth of the first head voxel along -y for every (x, z), lit from the front: a face, if one is there.
        Air is not zero in a real scan, so the head is what is brighter than a tenth of the brain's median, in
        one piece (the largest connected component) and with the speckle opened away."""
        if not (v > 0).any():
            return np.zeros((GRID_SHAPE[2], GRID_SHAPE[0]))
        head = v > 0.1 * np.median(v[mask_ref])
        head = ndimage.binary_opening(head, iterations=2)
        lab, n = ndimage.label(head)
        if n > 1:
            head = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
        j = np.argmax(head[:, ::-1, :], axis=1)          # first anterior head voxel, index from the front
        depth = np.where(head.any(axis=1), GRID_SHAPE[1] - 1 - j, np.nan).astype(float)
        gx, gz = np.gradient(np.nan_to_num(depth, nan=np.nanmin(depth) if np.isfinite(depth).any() else 0))
        shade = 1.0 / np.sqrt(1 + gx ** 2 + gz ** 2)      # a headlight: flat-on skin bright, grazing skin dark
        return np.where(np.isfinite(depth), shade, 0).T

    panels = [
        ("sagittal-midline", lambda v: v[x0].T, "sagittal x = 0 mm"),
        ("skin-front", skin_from_front, "skin surface seen from the front"),
        ("axial-orbits", lambda v: v[:, :, z_orbit].T, "axial z = -25 mm (orbits)"),
    ]
    files = []
    for name, cut, title in panels:
        fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
        for ax, (vol, lbl) in zip(axes, ((before, "registered, before defacing"), (after, "shipped (defaced)"), (template, "MNI template"))):
            img = cut(vol)
            ax.imshow(img, cmap="gray", origin="lower", vmin=0, vmax=np.percentile(img[img > 0], 99.5) if (img > 0).any() else 1)
            ax.set_title(lbl, fontsize=9); ax.axis("off")
        fig.suptitle(f"{key_of(subject_id)} -- {title}", fontsize=10)
        fig.tight_layout()
        p = out / f"{name}.png"; fig.savefig(p, dpi=110); plt.close(fig)
        files.append(str(p))
    return files


# ---------------------------------------------------------------- main
def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scan", type=Path, help="the subject's T1-weighted scan: a NIfTI, a folder of DICOM files, or the .zip a hospital hands out")
    ap.add_argument("--id", required=True, help="short id: the volume becomes subject-<id>, its source subject_<id>")
    ap.add_argument("--series", help="DICOM only: the series number to use instead of the one that looks most like a 3D T1")
    ap.add_argument("--transform", default=DEFAULT_TRANSFORM,
                    help=f"antspyx type_of_transform. {DEFAULT_TRANSFORM} (default) is the full antsRegistrationSyN.sh recipe, 5-10 min; "
                         "SyN is the quick one (40 s) and can miss on a scan with flat contrast; Affine shows what the deformable stage adds")
    ap.add_argument("--reuse", action="store_true", help="reuse the transforms already in work/subjects/<id>/")
    ap.add_argument("--no-deface", action="store_true", help="skip defacing (local use only: check-public refuses an undefaced subject volume)")
    a = ap.parse_args(argv)
    if not a.scan.exists():
        sys.exit(f"{a.scan}: no such file or folder")
    if not T1.exists() or not MASK.exists():
        sys.exit("the MNI template is missing: run atlas-download first")
    sid = a.id
    if not sid.replace("-", "").isalnum() or not sid.islower():
        sys.exit("--id must be lower-case letters, digits and dashes")
    cfg = load_sources()
    src = next((s for s in cfg["sources"] if s["id"] == source_of(sid)), None)
    if src is None:
        sys.exit(f"config/sources.yaml has no entry `{source_of(sid)}` -- add one (group: subjects, generated: true, "
                 "a redistributable licence, and a citation that says whose scan it is and that they consented)")
    lic = cfg["licenses"].get(src["license"], {})
    if lic.get("nc") or lic.get("no_redistribution"):
        sys.exit(f"{source_of(sid)}: licence {src['license']} is restricted; a subject volume must be redistributable")

    template = np.asanyarray(load_ras(T1).dataobj).astype(np.float32)
    mask = np.asanyarray(load_ras(MASK).dataobj) > 0
    work = WORK / "subjects" / sid
    work.mkdir(parents=True, exist_ok=True)
    t1w, origin = to_nifti(a.scan, work, a.series)
    warped, affine_only, info = register(t1w, sid, a.transform, a.reuse)
    info["input"] = {**origin, **info["input"], "given": str(a.scan)}
    sim = {"affine": round(similarity(template, affine_only, mask), 4), "deformable": round(similarity(template, warped, mask), 4)}
    info["similarity"] = sim
    info["pearson"] = {"affine": round(pearson(template, affine_only, mask), 4), "deformable": round(pearson(template, warped, mask), 4)}
    print(f"  normalised mutual information with the template inside the brain mask: affine {sim['affine']:.3f} -> "
          f"{a.transform} {sim["deformable"]:.3f}  (Pearson {info['pearson']['affine']:.2f} -> {info['pearson']["deformable"]:.2f})")
    if sim["deformable"] < MIN_SIMILARITY:
        # the renders are exactly what is needed to see what went wrong, so write them before giving up
        renders = qa_renders(sid, affine_only, warped, template, mask)
        sys.exit(f"registration failed the {MIN_SIMILARITY} similarity gate -- look at {', '.join(renders)} "
                 "(left: after the affine, middle: after the deformable stage) and at the input's orientation")
    if sim["deformable"] < WARN_SIMILARITY:
        print(f"  WARNING: similarity under {WARN_SIMILARITY}; check the renders before trusting the overlay")

    before = warped.copy()
    if a.no_deface:
        defaced = None
    else:
        head = template > np.percentile(template[template > 0], HEAD_PERCENTILE)
        plane = deface_plane(mask, head)
        cut = face_mask(plane)
        removed = int(((warped > 0) & cut).sum())
        warped[cut] = 0
        assert not (mask & cut).any(), "the shear plane cuts the brain mask"
        defaced = {"method": "shear plane in MNI space: the forward-facing facet of the convex hull of the template brain mask "
                             f"(dilated {DEFACE_MARGIN_MM} mm) that removes the most head; a*y + b*z + c > 0 is zeroed",
                   "plane_mm": {k: round(plane[k], 5) for k in ("a", "b", "c")}, "voxels_removed": removed}
        print(f"  defaced: {removed} voxels behind the plane {plane['a']:.3f}*y {plane['b']:+.3f}*z {plane['c']:+.1f} > 0")
    renders = qa_renders(sid, before, warped if defaced else before, template, mask)

    lo, hi = robust_window(warped, mask)
    u8 = to_uint8(warped, 0.0, hi)
    raw = np.ascontiguousarray(u8).tobytes(order="F")
    key = key_of(sid)
    path = VOLUMES / f"{key}.u8.bin"
    with gzip.open(path, "wb", compresslevel=6) as f:
        f.write(raw)
    meta = {
        "key": key, "kind": "subject", "name": src.get("name", key), "source": src["id"], "license": src["license"],
        "file": f"volumes/{path.name}", "dtype": "uint8", "shape": list(GRID_SHAPE),
        "bytes_raw": len(raw), "bytes_gz": path.stat().st_size, "sha256": hashlib.sha256(raw).hexdigest(),
        "window": 255, "level": 127, "source_window": [0.0, round(float(hi), 3)],
        "registration": info, "defaced": defaced,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "qa": renders,
    }
    (VOLUMES / f"{key}.json").write_text(json.dumps(meta, indent=1))
    rec = RAW / src["id"]
    rec.mkdir(parents=True, exist_ok=True)
    (rec / "SOURCE.json").write_text(json.dumps({
        "what": "an individual's T1w MRI, registered into MNI152NLin2009cAsym and defaced by atlas-subject",
        "command": " ".join(["atlas-subject"] + (argv if argv is not None else sys.argv[1:])),
        "tool": info["tool"], "transform": info["transform"], "similarity": sim, "defaced": defaced is not None,
        "generated": meta["generated"]}, indent=1))
    print(f"wrote {path} ({meta['bytes_gz']/1e6:.2f} MB gz), {VOLUMES / (key + '.json')}")
    print(f"QA renders: {', '.join(renders)}")
    if not defaced:
        print("  NOT DEFACED: this volume must not be released (check-public will refuse it)")
    # keep the work dir tidy for `git status` readers: the transforms are the only large thing there
    subprocess.run(["du", "-sh", str(WORK / "subjects" / sid)], check=False)


if __name__ == "__main__":
    main()
