#!/usr/bin/env python3
"""
Face Anchor Assembler

Assembles a face anchor sheet from three generated portrait images using the
project's directory conventions.

Default project conventions:
- Script location:
    [ROOT]/tools/asset_generators/face_anchor_assembler.py
- Source directory:
    [ROOT]/docs/assets/library/10_CHARACTERS/[CHARACTER_NAME]/01_IDENTITY/face
- Input filenames:
    [character_name]_front_face_[VERSION].png
    [character_name]_profile_face_[VERSION].png
    [character_name]_three_quarter_face_[VERSION].png
- Output filename:
    [character_name]_face_anchor_[VERSION].png

This version does NOT use MediaPipe. It performs deterministic width-preserving
vertical crops from 2:3 to 3:4 with configurable upward bias and optional
tightening to reduce visible shoulder/chest mass.

Install:
    python -m pip install --upgrade Pillow
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


# -----------------------------
# Configuration
# -----------------------------

TARGET_PANEL_RATIO = 3 / 4  # width / height

DEFAULT_PANEL_WIDTH = 900
DEFAULT_PANEL_HEIGHT = 1200

DEFAULT_BG = (245, 245, 245)
DEFAULT_TEXT = (60, 60, 60)

LEFT_RIGHT_MARGIN_PX = 180
TOP_MARGIN_PX = 90
BOTTOM_MARGIN_PX = 120
GUTTER_PX = 120
LABEL_BAND_PX = 120
LABEL_GAP_PX = 30

CHAR_ROOT_RELATIVE = Path("docs/assets/library/10_CHARACTERS")


@dataclass
class CropResult:
    image: Image.Image
    method: str
    crop_box: Tuple[int, int, int, int]


# -----------------------------
# Utilities
# -----------------------------

def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def save_debug_image(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def normalize_character_name(name: str) -> tuple[str, str]:
    """
    Returns:
        character_slug: lowercase filename prefix, e.g. 'connor'
        character_dir: uppercase directory name, e.g. 'CONNOR'
    """
    raw = name.strip()
    if not raw:
        raise ValueError("Character name must not be empty.")
    return raw.lower(), raw.upper()


def find_project_root(start_path: Path) -> Optional[Path]:
    """
    Walk upward from start_path and look for the repository root by checking for
    the character library folder.
    """
    current = start_path.resolve()
    if current.is_file():
        current = current.parent

    for candidate in [current, *current.parents]:
        if (candidate / CHAR_ROOT_RELATIVE).exists():
            return candidate
    return None


def resolve_face_dir(project_root: Path, character_name: str) -> Path:
    _, character_dir = normalize_character_name(character_name)
    return project_root / CHAR_ROOT_RELATIVE / character_dir / "01_IDENTITY" / "face"


def build_expected_paths(face_dir: Path, character_name: str, version: str) -> dict[str, Path]:
    character_slug, _ = normalize_character_name(character_name)
    version_suffix = f"_{version}" if version else ""

    return {
        "front": face_dir / f"{character_slug}_front_face{version_suffix}.png",
        "profile": face_dir / f"{character_slug}_profile_face{version_suffix}.png",
        "three_quarter": face_dir / f"{character_slug}_three_quarter_face{version_suffix}.png",
        "output": face_dir / f"{character_slug}_face_anchor{version_suffix}.png",
    }


def choose_latest_version(face_dir: Path, character_name: str) -> Optional[str]:
    """
    Find the latest version where all three required inputs exist.
    Supports:
      - *_v1.png, *_v2.png ...
      - files with no version suffix
    """
    character_slug, _ = normalize_character_name(character_name)
    required_stems = [
        f"{character_slug}_front_face",
        f"{character_slug}_profile_face",
        f"{character_slug}_three_quarter_face",
    ]

    candidates: set[str] = set()

    for stem in required_stems:
        for file in face_dir.glob(f"{stem}*.png"):
            match = re.match(rf"^{re.escape(stem)}(?:_(v\d+))?\.png$", file.name)
            if match:
                candidates.add(match.group(1) or "")

    def version_key(v: str) -> tuple[int, str]:
        if not v:
            return (0, "")
        m = re.match(r"v(\d+)$", v)
        if m:
            return (int(m.group(1)), v)
        return (-1, v)

    for version in sorted(candidates, key=version_key, reverse=True):
        paths = build_expected_paths(face_dir, character_name, version)
        if all(paths[key].exists() for key in ("front", "profile", "three_quarter")):
            return version

    return None


# -----------------------------
# Cropping
# -----------------------------

def crop_to_ratio(
    img: Image.Image,
    target_ratio: float = TARGET_PANEL_RATIO,
    vertical_bias: float = 0.30,
    tighten: float = 1.0,
) -> CropResult:
    """
    Deterministic portrait crop:
    - Preserve full width when possible
    - Crop height down from 2:3 to 3:4
    - Optionally tighten the crop to reduce visible shoulders/chest mass
    - Bias slightly upward so the result keeps a bit more room below than above

    vertical_bias meaning:
    - 0.00 => crop starts at very top
    - 0.50 => centered crop
    - 0.25-0.35 => useful range

    tighten meaning:
    - 1.00 => standard 3:4 crop from source width
    - 0.88 => tighter crop before resize, usually better for face anchors
    - 0.80-1.00 => safe range
    """
    w, h = img.size

    base_crop_h = int(round(w / target_ratio))
    crop_h = int(round(base_crop_h * tighten))
    crop_h = max(1, crop_h)

    if crop_h > h:
        crop_w = int(round(h * target_ratio))
        crop_w = min(crop_w, w)
        left = (w - crop_w) // 2
        box = (left, 0, left + crop_w, h)
        return CropResult(img.crop(box), "fallback-width", box)

    extra_h = h - crop_h
    top = int(round(extra_h * vertical_bias))
    top = clamp(top, 0, h - crop_h)

    box = (0, top, w, top + crop_h)
    method = "fallback-height-tight" if tighten < 0.999 else "fallback-height"
    return CropResult(img.crop(box), method, box)


def fit_panel(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    return img.resize(size, Image.Resampling.LANCZOS)


# -----------------------------
# Sheet assembly
# -----------------------------

def load_font(size: int) -> ImageFont.ImageFont:
    font_candidates = [
        "arial.ttf",
        "Arial.ttf",
        "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in font_candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def assemble_sheet(
    profile_panel: Image.Image,
    front_panel: Image.Image,
    three_quarter_panel: Image.Image,
    output_path: Path,
    panel_size: Tuple[int, int] = (DEFAULT_PANEL_WIDTH, DEFAULT_PANEL_HEIGHT),
    bg_color: Tuple[int, int, int] = DEFAULT_BG,
    text_color: Tuple[int, int, int] = DEFAULT_TEXT,
) -> None:
    panel_w, panel_h = panel_size

    canvas_w = LEFT_RIGHT_MARGIN_PX * 2 + panel_w * 3 + GUTTER_PX * 2
    canvas_h = TOP_MARGIN_PX + panel_h + LABEL_GAP_PX + LABEL_BAND_PX + BOTTOM_MARGIN_PX

    canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(canvas)

    x0 = LEFT_RIGHT_MARGIN_PX
    x1 = x0 + panel_w + GUTTER_PX
    x2 = x1 + panel_w + GUTTER_PX
    y_img = TOP_MARGIN_PX

    panels = [
        (profile_panel, x0, "PROFILE"),
        (front_panel, x1, "FRONT"),
        (three_quarter_panel, x2, "3/4"),
    ]

    for panel_img, x, _ in panels:
        canvas.paste(panel_img, (x, y_img))

    font = load_font(size=46)
    label_y_top = y_img + panel_h + LABEL_GAP_PX

    for _panel_img, x, label in panels:
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = x + (panel_w - text_w) // 2
        text_y = label_y_top + (LABEL_BAND_PX - text_h) // 2 - 4
        draw.text((text_x, text_y), label, fill=text_color, font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


# -----------------------------
# CLI
# -----------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a Face Anchor Sheet using the project's character asset conventions."
    )

    parser.add_argument(
        "--character",
        required=True,
        help="Character name, e.g. CONNOR or connor",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Version suffix such as v1 or v2. If omitted, the latest complete set is used.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Optional explicit project root. If omitted, the script auto-detects it.",
    )
    parser.add_argument(
        "--face-dir",
        type=Path,
        default=None,
        help="Optional explicit face directory. Overrides project-root + character resolution.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional explicit output path. Defaults to the character face directory.",
    )
    parser.add_argument(
        "--panel-width",
        type=int,
        default=DEFAULT_PANEL_WIDTH,
        help="Final width of each 3:4 panel in pixels.",
    )
    parser.add_argument(
        "--panel-height",
        type=int,
        default=DEFAULT_PANEL_HEIGHT,
        help="Final height of each 3:4 panel in pixels.",
    )
    parser.add_argument(
        "--vertical-bias",
        type=float,
        default=0.30,
        help="Top-bias for width-preserving vertical crop. 0.25-0.35 is a useful range.",
    )
    parser.add_argument(
        "--tighten",
        type=float,
        default=1.0,
        help="Tighten the crop before resize. 0.88 is a good starting point.",
    )
    parser.add_argument(
        "--debug-dir",
        type=Path,
        default=None,
        help="Optional directory to save cropped intermediate panels.",
    )
    return parser.parse_args()


def validate_panel_ratio(panel_width: int, panel_height: int) -> None:
    ratio = panel_width / panel_height
    if abs(ratio - TARGET_PANEL_RATIO) > 1e-6:
        raise ValueError(
            f"Panel size must be 3:4. Got {panel_width}:{panel_height} "
            f"(ratio={ratio:.4f}, expected {TARGET_PANEL_RATIO:.4f})."
        )


def validate_vertical_bias(vertical_bias: float) -> None:
    if not (0.0 <= vertical_bias <= 0.5):
        raise ValueError("vertical-bias must be between 0.0 and 0.5")


def validate_tighten(tighten: float) -> None:
    if not (0.80 <= tighten <= 1.00):
        raise ValueError("tighten must be between 0.80 and 1.00")


def main() -> int:
    args = parse_args()

    try:
        validate_panel_ratio(args.panel_width, args.panel_height)
        validate_vertical_bias(args.vertical_bias)
        validate_tighten(args.tighten)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.face_dir is not None:
        face_dir = args.face_dir.resolve()
        project_root = None
    else:
        if args.project_root is not None:
            project_root = args.project_root.resolve()
        else:
            project_root = find_project_root(Path(__file__))
            if project_root is None:
                print(
                    "Error: Could not auto-detect project root. Use --project-root or --face-dir.",
                    file=sys.stderr,
                )
                return 1

        face_dir = resolve_face_dir(project_root, args.character)

    if not face_dir.exists():
        print(f"Error: face directory not found: {face_dir}", file=sys.stderr)
        return 1

    version = args.version
    if version is None:
        version = choose_latest_version(face_dir, args.character)
        if version is None:
            print(
                f"Error: Could not find a complete front/profile/three-quarter set in {face_dir}",
                file=sys.stderr,
            )
            return 1

    paths = build_expected_paths(face_dir, args.character, version)

    front_path = paths["front"]
    profile_path = paths["profile"]
    three_quarter_path = paths["three_quarter"]
    output_path = args.output.resolve() if args.output else paths["output"]

    for required_path in [front_path, profile_path, three_quarter_path]:
        if not required_path.exists():
            print(f"Error: file not found: {required_path}", file=sys.stderr)
            return 1

    front_img = load_image(front_path)
    profile_img = load_image(profile_path)
    three_quarter_img = load_image(three_quarter_path)

    front_crop = crop_to_ratio(front_img, vertical_bias=args.vertical_bias, tighten=args.tighten)
    profile_crop = crop_to_ratio(profile_img, vertical_bias=args.vertical_bias, tighten=args.tighten)
    three_quarter_crop = crop_to_ratio(three_quarter_img, vertical_bias=args.vertical_bias, tighten=args.tighten)

    panel_size = (args.panel_width, args.panel_height)
    front_panel = fit_panel(front_crop.image, panel_size)
    profile_panel = fit_panel(profile_crop.image, panel_size)
    three_quarter_panel = fit_panel(three_quarter_crop.image, panel_size)

    if args.debug_dir is not None:
        debug_dir = args.debug_dir.resolve()
        save_debug_image(profile_crop.image, debug_dir / "profile_cropped.png")
        save_debug_image(front_crop.image, debug_dir / "front_cropped.png")
        save_debug_image(three_quarter_crop.image, debug_dir / "three_quarter_cropped.png")

    assemble_sheet(
        profile_panel=profile_panel,
        front_panel=front_panel,
        three_quarter_panel=three_quarter_panel,
        output_path=output_path,
        panel_size=panel_size,
    )

    print("Done.")
    print(f"Character: {args.character}")
    print(f"Face directory: {face_dir}")
    print(f"Version: {version if version else '(no suffix)'}")
    print(f"Front input: {front_path}")
    print(f"Profile input: {profile_path}")
    print(f"Three-quarter input: {three_quarter_path}")
    print(f"Output: {output_path}")
    print(f"Vertical bias: {args.vertical_bias}")
    print(f"Tighten: {args.tighten}")
    print(f"Profile crop method: {profile_crop.method}, box={profile_crop.crop_box}")
    print(f"Front crop method: {front_crop.method}, box={front_crop.crop_box}")
    print(f"Three-quarter crop method: {three_quarter_crop.method}, box={three_quarter_crop.crop_box}")

    if args.debug_dir is not None:
        print(f"Saved debug crops in: {debug_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
