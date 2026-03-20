#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY_ROOT = ROOT / "docs" / "assets" / "library"
CHARACTERS_DIRNAME = "10_CHARACTERS"
CHAR_ROOT_RELATIVE = Path("docs/assets/library/10_CHARACTERS")

ANATOMY_SUBDIR = Path("02_BODY") / "anatomy"
STRUCTURE_SUBDIR = Path("02_BODY") / "structure"

DEFAULT_FG_THRESHOLD = 28.0
DEFAULT_BG_THRESHOLD_LOW = 16.0
DEFAULT_BG_THRESHOLD_HIGH = 40.0

ASSET_KEYS = ["front", "side", "back", "three_quarter_back"]

VERSION_RE = re.compile(r"_v(\d+)$", re.IGNORECASE)


class SilhouetteError(RuntimeError):
    pass


@dataclass(frozen=True)
class ResolvedAsset:
    asset_key: str
    input_path: Path
    output_path: Path
    source_version: str


def normalize_character_name(name: str) -> tuple[str, str]:
    raw = name.strip()
    if not raw:
        raise SilhouetteError("Character name must not be empty.")
    return raw.lower(), raw.upper()


def find_project_root(start_path: Path) -> Optional[Path]:
    current = start_path.resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / CHAR_ROOT_RELATIVE).exists():
            return candidate
    return None


def resolve_character_dirs(library_root: Path, character_name: str) -> tuple[Path, Path]:
    _, character_dir = normalize_character_name(character_name)
    char_root = library_root / CHARACTERS_DIRNAME / character_dir
    anatomy_dir = char_root / ANATOMY_SUBDIR
    structure_dir = char_root / STRUCTURE_SUBDIR
    return anatomy_dir, structure_dir


def parse_version_str(version: str | None) -> str:
    if not version:
        return ""
    version = version.strip()
    if not version:
        return ""
    if not version.lower().startswith("v"):
        version = f"v{version}"
    return version.lower()


def extract_version(path: Path) -> str:
    m = VERSION_RE.search(path.stem)
    return f"v{m.group(1)}" if m else ""


def version_sort_key(version: str) -> tuple[int, str]:
    if not version:
        return (0, "")
    m = re.fullmatch(r"v(\d+)", version, re.IGNORECASE)
    if m:
        return (int(m.group(1)), version.lower())
    return (-1, version.lower())


def anatomy_filename(slug: str, asset_key: str, version: str) -> str:
    suffix = f"_{version}" if version else ""
    return f"{slug}_anatomy_{asset_key}{suffix}.png"


def silhouette_filename(slug: str, asset_key: str, version: str) -> str:
    suffix = f"_{version}" if version else ""
    return f"{slug}_silhouette_{asset_key}{suffix}.png"


def find_latest_asset_file(anatomy_dir: Path, slug: str, asset_key: str) -> Optional[Path]:
    pattern = f"{slug}_anatomy_{asset_key}*.png"
    candidates = []
    for path in anatomy_dir.glob(pattern):
        stem_expected = f"{slug}_anatomy_{asset_key}"
        m = re.fullmatch(rf"{re.escape(stem_expected)}(?:_(v\d+))?", path.stem, re.IGNORECASE)
        if m:
            candidates.append(path)
    if not candidates:
        return None
    return max(candidates, key=lambda p: version_sort_key(extract_version(p)))


def resolve_assets(
    anatomy_dir: Path,
    structure_dir: Path,
    character_name: str,
    version: str,
    asset_keys: Iterable[str],
) -> list[ResolvedAsset]:
    slug, _ = normalize_character_name(character_name)
    resolved: list[ResolvedAsset] = []

    for asset_key in asset_keys:
        if version:
            input_path = anatomy_dir / anatomy_filename(slug, asset_key, version)
            if not input_path.exists():
                raise SilhouetteError(
                    f"Missing required anatomy asset for {asset_key}: {input_path}"
                )
            source_version = version
        else:
            input_path = find_latest_asset_file(anatomy_dir, slug, asset_key)
            if input_path is None:
                raise SilhouetteError(
                    f"Could not find any anatomy asset for {asset_key} in {anatomy_dir}"
                )
            source_version = extract_version(input_path)

        output_path = structure_dir / silhouette_filename(slug, asset_key, source_version)
        resolved.append(
            ResolvedAsset(
                asset_key=asset_key,
                input_path=input_path,
                output_path=output_path,
                source_version=source_version,
            )
        )

    return resolved


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise SilhouetteError(f"Invalid hex color: {value}")
    try:
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError as exc:
        raise SilhouetteError(f"Invalid hex color: {value}") from exc


def estimate_background_color(img: Image.Image, sample_size: int = 24) -> tuple[float, float, float]:
    w, h = img.size
    s = min(sample_size, max(1, w // 4), max(1, h // 4))
    corners = [
        img.crop((0, 0, s, s)),
        img.crop((w - s, 0, w, s)),
        img.crop((0, h - s, s, h)),
        img.crop((w - s, h - s, w, h)),
    ]
    samples = []
    for c in corners:
        arr = np.asarray(c, dtype=np.float32).reshape(-1, 3)
        samples.append(arr.mean(axis=0))
    avg = np.mean(np.stack(samples, axis=0), axis=0)
    return float(avg[0]), float(avg[1]), float(avg[2])


def normalize_background(
    img: Image.Image,
    target_bg: tuple[int, int, int],
    threshold_low: float,
    threshold_high: float,
) -> Image.Image:
    if threshold_high <= threshold_low:
        raise SilhouetteError("bg-threshold-high must be greater than bg-threshold-low")

    src_bg = estimate_background_color(img)
    arr = np.asarray(img, dtype=np.float32)
    bg_arr = np.array(src_bg, dtype=np.float32)
    target_arr = np.array(target_bg, dtype=np.float32)

    diff = arr - bg_arr
    dist = np.sqrt(np.sum(diff * diff, axis=2))

    alpha = np.clip((dist - threshold_low) / (threshold_high - threshold_low), 0.0, 1.0)
    alpha = alpha[..., None]

    blended = target_arr * (1.0 - alpha) + arr * alpha
    blended = np.clip(blended, 0, 255).astype(np.uint8)
    return Image.fromarray(blended, mode="RGB")


def build_mask(img: Image.Image, threshold: float) -> Image.Image:
    bg = estimate_background_color(img)
    arr = np.asarray(img, dtype=np.float32)
    bg_arr = np.array(bg, dtype=np.float32)
    dist = np.sqrt(np.sum((arr - bg_arr) ** 2, axis=2))

    mask = (dist > threshold).astype(np.uint8) * 255
    mask_img = Image.fromarray(mask, mode="L")

    # Base cleanup: remove speckle and anti-aliased edge noise
    mask_img = mask_img.filter(ImageFilter.MedianFilter(size=3))
    mask_img = mask_img.filter(ImageFilter.MinFilter(size=3))
    mask_img = mask_img.filter(ImageFilter.MaxFilter(size=3))
    mask_img = mask_img.point(lambda p: 255 if p >= 128 else 0, mode="L")

    # Refined bottom-edge cleanup:
    # keep the true silhouette boundary, remove stray pixels below it,
    # and lightly smooth the bottom edge without thickening the feet.
    mask_arr = np.asarray(mask_img, dtype=np.uint8).copy()
    h, w = mask_arr.shape

    for x in range(w):
        ys = np.where(mask_arr[:, x] > 0)[0]
        if len(ys) == 0:
            continue

        bottom = ys.max()

        # Remove anything below the detected silhouette in this column.
        if bottom + 1 < h:
            mask_arr[bottom + 1 :, x] = 0

    # Light vertical-only closing to smooth tiny jagged base artifacts
    # without widening the silhouette horizontally.
    padded = np.pad(mask_arr, ((1, 1), (0, 0)), mode="constant", constant_values=0)
    vertical_sum = (
        (padded[:-2, :] > 0).astype(np.uint8)
        + (padded[1:-1, :] > 0).astype(np.uint8)
        + (padded[2:, :] > 0).astype(np.uint8)
    )
    mask_arr = np.where(vertical_sum >= 2, 255, 0).astype(np.uint8)

    return Image.fromarray(mask_arr, mode="L")

def create_silhouette_image(
    input_path: Path,
    threshold: float,
    normalize_bg_enabled: bool,
    bg_threshold_low: float,
    bg_threshold_high: float,
    subject_rgb: tuple[int, int, int],
    background_rgb: tuple[int, int, int],
) -> tuple[Image.Image, Image.Image, Image.Image]:
    original = Image.open(input_path).convert("RGB")
    working = (
        normalize_background(original, background_rgb, bg_threshold_low, bg_threshold_high)
        if normalize_bg_enabled
        else original.copy()
    )
    mask = build_mask(working, threshold)

    mask_arr = np.asarray(mask, dtype=np.uint8) > 0
    result = np.zeros((working.height, working.width, 3), dtype=np.uint8)
    result[:, :] = background_rgb
    result[mask_arr] = subject_rgb

    silhouette = Image.fromarray(result, mode="RGB")
    return original, working, silhouette


def save_image(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate silhouette assets from anatomy references."
    )
    parser.add_argument("--character", type=str, help="Character id/folder name, e.g. jasper")
    parser.add_argument(
        "--library-root",
        type=Path,
        default=None,
        help="Override library root. Defaults to auto-detected [ROOT]/docs/assets/library",
    )
    parser.add_argument(
        "--anatomy-dir",
        type=Path,
        default=None,
        help="Override anatomy input directory",
    )
    parser.add_argument(
        "--structure-dir",
        type=Path,
        default=None,
        help="Override silhouette output directory",
    )
    parser.add_argument(
        "--version",
        type=str,
        default=None,
        help="Exact version to use for all input assets, e.g. v2. If omitted, highest version is resolved per asset.",
    )
    parser.add_argument(
        "--asset",
        action="append",
        choices=ASSET_KEYS,
        default=None,
        help="Restrict generation to one or more specific assets. Can be repeated.",
    )
    parser.add_argument(
        "--bg-threshold",
        type=float,
        default=DEFAULT_FG_THRESHOLD,
        help="Foreground threshold after background normalization (default: 28)",
    )
    parser.add_argument(
        "--normalize-background",
        action="store_true",
        default=True,
        help="Normalize source backgrounds before masking (default: on)",
    )
    parser.add_argument(
        "--no-normalize-background",
        action="store_false",
        dest="normalize_background",
    )
    parser.add_argument(
        "--bg-threshold-low",
        type=float,
        default=DEFAULT_BG_THRESHOLD_LOW,
        help="Distance below which pixels are treated as definite background (default: 16)",
    )
    parser.add_argument(
        "--bg-threshold-high",
        type=float,
        default=DEFAULT_BG_THRESHOLD_HIGH,
        help="Distance above which pixels are treated as definite foreground (default: 40)",
    )
    parser.add_argument(
        "--fill-subject",
        type=str,
        default="#000000",
        help="Silhouette color as hex (default: #000000)",
    )
    parser.add_argument(
        "--fill-background",
        type=str,
        default="#FFFFFF",
        help="Background color as hex (default: #FFFFFF)",
    )
    parser.add_argument(
        "--debug-dir",
        type=Path,
        default=None,
        help="Optional directory for normalized intermediates",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if not args.character and not args.anatomy_dir:
            raise SilhouetteError("Provide --character or --anatomy-dir.")

        version = parse_version_str(args.version)
        requested_assets = args.asset or ASSET_KEYS
        subject_rgb = hex_to_rgb(args.fill_subject)
        background_rgb = hex_to_rgb(args.fill_background)

        if args.library_root is not None:
            library_root = args.library_root.resolve()
        else:
            project_root = find_project_root(Path(__file__))
            if project_root is None:
                raise SilhouetteError(
                    "Could not auto-detect project root. Use --library-root or provide explicit directories."
                )
            library_root = (project_root / "docs" / "assets" / "library").resolve()

        if args.anatomy_dir is not None:
            anatomy_dir = args.anatomy_dir.resolve()
            if args.structure_dir is not None:
                structure_dir = args.structure_dir.resolve()
            else:
                structure_dir = anatomy_dir.parent / "structure"
            if not args.character:
                raise SilhouetteError("--character is required when using --anatomy-dir.")
            character = args.character
        else:
            character = args.character
            anatomy_dir, structure_dir = resolve_character_dirs(library_root, character)
            if args.structure_dir is not None:
                structure_dir = args.structure_dir.resolve()

        if not anatomy_dir.exists():
            raise SilhouetteError(f"Anatomy directory not found: {anatomy_dir}")
        structure_dir.mkdir(parents=True, exist_ok=True)

        resolved_assets = resolve_assets(
            anatomy_dir=anatomy_dir,
            structure_dir=structure_dir,
            character_name=character,
            version=version,
            asset_keys=requested_assets,
        )

        print("Resolved inputs:")
        for ra in resolved_assets:
            version_label = ra.source_version if ra.source_version else "(no suffix)"
            print(f"  {ra.asset_key:<18} -> {ra.input_path.name} [{version_label}]")

        print("Writing outputs:")
        for ra in resolved_assets:
            version_label = ra.source_version if ra.source_version else "(no suffix)"
            print(f"  {ra.asset_key:<18} -> {ra.output_path.name} [{version_label}]")

        for ra in resolved_assets:
            original, working, silhouette = create_silhouette_image(
                input_path=ra.input_path,
                threshold=args.bg_threshold,
                normalize_bg_enabled=args.normalize_background,
                bg_threshold_low=args.bg_threshold_low,
                bg_threshold_high=args.bg_threshold_high,
                subject_rgb=subject_rgb,
                background_rgb=background_rgb,
            )
            save_image(silhouette, ra.output_path)

            if args.debug_dir is not None:
                debug_dir = args.debug_dir.resolve() / normalize_character_name(character)[0]
                debug_dir.mkdir(parents=True, exist_ok=True)
                stem = ra.output_path.stem
                save_image(original, debug_dir / f"{stem}_source.png")
                save_image(working, debug_dir / f"{stem}_normalized.png")
                save_image(silhouette, debug_dir / f"{stem}_silhouette.png")

        print("Done.")
        print(f"Anatomy dir:   {anatomy_dir}")
        print(f"Structure dir: {structure_dir}")
        print(f"Foreground threshold: {args.bg_threshold}")
        print(f"Background normalization: {args.normalize_background}")
        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())