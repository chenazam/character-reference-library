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

This version does NOT use MediaPipe. It performs deterministic cropping while
always preserving the target panel aspect ratio (3:4). Tightening now zooms in
by cropping BOTH width and height proportionally, instead of squishing the image.

New in this version:
- per-view horizontal bias defaults
- automatic profile direction detection using filename + image analysis
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat


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

# Per-view crop defaults
DEFAULT_FRONT_H_BIAS = 0.50
DEFAULT_THREE_QUARTER_H_BIAS = 0.50
DEFAULT_PROFILE_BACKHEAD_BIAS = 0.66  # more room in front of the face


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
    raw = name.strip()
    if not raw:
        raise ValueError("Character name must not be empty.")
    return raw.lower(), raw.upper()


def find_project_root(start_path: Path) -> Optional[Path]:
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
# Direction detection
# -----------------------------

def infer_profile_direction_from_name(path: Path) -> Optional[str]:
    """
    Returns 'left', 'right', or None.
    """
    name = path.stem.lower()

    left_markers = [
        "_left_profile", "_profile_left", "_profile_l", "_left",
    ]
    right_markers = [
        "_right_profile", "_profile_right", "_profile_r", "_right",
    ]

    if any(marker in name for marker in left_markers):
        return "left"
    if any(marker in name for marker in right_markers):
        return "right"
    return None


def edge_energy_half(gray: Image.Image, left_half: bool) -> float:
    """
    Estimate how much edge detail exists in one half of the image.
    The face side usually has stronger edge energy than the blank background side.
    """
    w, h = gray.size
    box = (0, 0, w // 2, h) if left_half else (w // 2, 0, w, h)
    region = gray.crop(box)
    region = ImageOps.autocontrast(region)
    edges = region.filter(ImageFilter.FIND_EDGES)  # type: ignore[name-defined]
    stat = ImageStat.Stat(edges)
    return float(stat.mean[0])


def infer_profile_direction_from_pixels(img: Image.Image) -> str:
    """
    Returns:
      'left'  -> subject facing left
      'right' -> subject facing right

    Heuristic:
    - Compute edge energy in left/right halves.
    - The half containing the facial silhouette tends to have more structure.
    """
    gray = ImageOps.grayscale(img)
    left_energy = edge_energy_half(gray, left_half=True)
    right_energy = edge_energy_half(gray, left_half=False)

    return "left" if left_energy >= right_energy else "right"


def detect_profile_direction(path: Path, img: Image.Image) -> str:
    """
    First trust explicit filename markers if present, otherwise infer from image.
    """
    from_name = infer_profile_direction_from_name(path)
    if from_name is not None:
        return from_name
    return infer_profile_direction_from_pixels(img)


def profile_horizontal_bias_for_direction(direction: str) -> float:
    """
    Bias points toward the back of the head so the face gets more room in front.

    - facing left: subject occupies left side, so shift crop to the right
    - facing right: subject occupies right side, so shift crop to the left
    """
    if direction == "left":
        return DEFAULT_PROFILE_BACKHEAD_BIAS
    if direction == "right":
        return 1.0 - DEFAULT_PROFILE_BACKHEAD_BIAS
    return 0.50


# -----------------------------
# Cropping
# -----------------------------
from PIL import ImageFilter


def crop_to_ratio(
    img: Image.Image,
    target_ratio: float = TARGET_PANEL_RATIO,
    vertical_bias: float = 0.30,
    tighten: float = 1.0,
    horizontal_bias: float = 0.50,
) -> CropResult:
    """
    Deterministic crop that ALWAYS preserves the target aspect ratio.

    Strategy:
    1. Start from the largest possible 3:4 crop in the source image.
    2. Apply 'tighten' as a proportional zoom, reducing BOTH width and height.
    3. Position the crop with vertical_bias and horizontal_bias.
    """
    w, h = img.size

    source_ratio = w / h
    if source_ratio < target_ratio:
        max_crop_w = w
        max_crop_h = int(round(max_crop_w / target_ratio))
        method_base = "max-from-width"
    else:
        max_crop_h = h
        max_crop_w = int(round(max_crop_h * target_ratio))
        method_base = "max-from-height"

    max_crop_w = min(max_crop_w, w)
    max_crop_h = min(max_crop_h, h)

    crop_w = max(1, int(round(max_crop_w * tighten)))
    crop_h = max(1, int(round(max_crop_h * tighten)))

    crop_h = min(crop_h, h)
    crop_w = int(round(crop_h * target_ratio))
    if crop_w > w:
        crop_w = w
        crop_h = int(round(crop_w / target_ratio))

    extra_w = w - crop_w
    extra_h = h - crop_h

    left = int(round(extra_w * horizontal_bias))
    top = int(round(extra_h * vertical_bias))

    left = clamp(left, 0, w - crop_w)
    top = clamp(top, 0, h - crop_h)

    box = (left, top, left + crop_w, top + crop_h)
    method = f"{method_base}-tight" if tighten < 0.999 else method_base
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

    parser.add_argument("--character", required=True, help="Character name, e.g. CONNOR or connor")
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
        default=0.25,
        help="Top-bias for crop placement. 0.25-0.35 is a useful range.",
    )
    parser.add_argument(
        "--front-horizontal-bias",
        type=float,
        default=DEFAULT_FRONT_H_BIAS,
        help="Horizontal bias for front crop. Default keeps it centered.",
    )
    parser.add_argument(
        "--three-quarter-horizontal-bias",
        type=float,
        default=DEFAULT_THREE_QUARTER_H_BIAS,
        help="Horizontal bias for three-quarter crop. Default keeps it centered.",
    )
    parser.add_argument(
        "--profile-horizontal-bias",
        type=float,
        default=None,
        help=(
            "Optional explicit horizontal bias for profile crop. "
            "If omitted, profile direction is auto-detected and bias is applied toward the back of the head."
        ),
    )
    parser.add_argument(
        "--tighten",
        type=float,
        default=0.88,
        help="Proportional zoom while preserving 3:4 ratio. 0.88 is a good starting point.",
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


def validate_bias(name: str, value: float) -> None:
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0")


def validate_tighten(tighten: float) -> None:
    if not (0.80 <= tighten <= 1.00):
        raise ValueError("tighten must be between 0.80 and 1.00")


def main() -> int:
    args = parse_args()

    try:
        validate_panel_ratio(args.panel_width, args.panel_height)
        validate_bias("vertical-bias", args.vertical_bias)
        validate_bias("front-horizontal-bias", args.front_horizontal_bias)
        validate_bias("three-quarter-horizontal-bias", args.three_quarter_horizontal_bias)
        if args.profile_horizontal_bias is not None:
            validate_bias("profile-horizontal-bias", args.profile_horizontal_bias)
        validate_tighten(args.tighten)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.face_dir is not None:
        face_dir = args.face_dir.resolve()
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

    profile_direction = detect_profile_direction(profile_path, profile_img)
    profile_horizontal_bias = (
        args.profile_horizontal_bias
        if args.profile_horizontal_bias is not None
        else profile_horizontal_bias_for_direction(profile_direction)
    )

    front_crop = crop_to_ratio(
        front_img,
        vertical_bias=args.vertical_bias,
        horizontal_bias=args.front_horizontal_bias,
        tighten=args.tighten,
    )
    profile_crop = crop_to_ratio(
        profile_img,
        vertical_bias=args.vertical_bias,
        horizontal_bias=profile_horizontal_bias,
        tighten=args.tighten,
    )
    three_quarter_crop = crop_to_ratio(
        three_quarter_img,
        vertical_bias=args.vertical_bias,
        horizontal_bias=args.three_quarter_horizontal_bias,
        tighten=args.tighten,
    )

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
    print(f"Front horizontal bias: {args.front_horizontal_bias}")
    print(f"Profile direction: {profile_direction}")
    print(f"Profile horizontal bias: {profile_horizontal_bias}")
    print(f"Three-quarter horizontal bias: {args.three_quarter_horizontal_bias}")
    print(f"Tighten: {args.tighten}")
    print(f"Profile crop method: {profile_crop.method}, box={profile_crop.crop_box}")
    print(f"Front crop method: {front_crop.method}, box={front_crop.crop_box}")
    print(f"Three-quarter crop method: {three_quarter_crop.method}, box={three_quarter_crop.crop_box}")

    if args.debug_dir is not None:
        print(f"Saved debug crops in: {debug_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
