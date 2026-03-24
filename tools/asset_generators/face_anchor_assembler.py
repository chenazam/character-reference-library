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
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
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

# Face-aware normalization defaults
DEFAULT_FACE_TOP_MARGIN_PCT = 0.04
DEFAULT_FACE_CHIN_PCT = 0.62
DEFAULT_FACE_MASK_THRESHOLD = 18.0
DEFAULT_HEAD_UPPER_PORTION = 0.60
DEFAULT_MIN_MASK_COVERAGE = 0.005

VERSION_PATTERN = re.compile(r"_v(\d+)", re.IGNORECASE)



@dataclass
class CropResult:
    image: Image.Image
    method: str
    crop_box: Tuple[int, int, int, int]
    subject_box: Optional[Tuple[int, int, int, int]] = None
    head_box: Optional[Tuple[int, int, int, int]] = None


# -----------------------------
# Utilities
# -----------------------------

def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))


def extract_version(path: Path) -> int:
    m = VERSION_PATTERN.search(path.stem)
    if not m:
        return 0
    return int(m.group(1))


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


def find_latest_view_file(face_dir: Path, character_name: str, view: str) -> Optional[Path]:
    character_slug, _ = normalize_character_name(character_name)
    stem = f"{character_slug}_{view}_face"

    candidates: list[Path] = []
    for file in face_dir.glob(f"{stem}*.png"):
        match = re.match(rf"^{re.escape(stem)}(?:_(v\d+))?\.png$", file.name)
        if match:
            candidates.append(file)

    if not candidates:
        return None

    return max(candidates, key=extract_version)


def find_latest_inputs(face_dir: Path, character_name: str) -> dict[str, Path]:
    result = {
        "front": find_latest_view_file(face_dir, character_name, "front"),
        "profile": find_latest_view_file(face_dir, character_name, "profile"),
        "three_quarter": find_latest_view_file(face_dir, character_name, "three_quarter"),
    }

    missing = [key for key, path in result.items() if path is None]
    if missing:
        raise FileNotFoundError(
            f"Could not find latest files for views: {', '.join(missing)} in {face_dir}"
        )

    return result  # type: ignore[return-value]


def next_face_anchor_version(face_dir: Path, character_name: str) -> str:
    character_slug, _ = normalize_character_name(character_name)
    prefix = f"{character_slug}_face_anchor"

    existing = []
    for file in face_dir.glob(f"{prefix}*.png"):
        match = re.match(rf"^{re.escape(prefix)}(?:_(v\d+))?\.png$", file.name)
        if match:
            existing.append(extract_version(file))

    next_version = (max(existing) + 1) if existing else 1
    return f"v{next_version}"


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



def sample_background_color(img: Image.Image, patch_size: int = 24) -> np.ndarray:
    arr = np.asarray(img).astype(np.float32)
    h, w, _ = arr.shape

    patches = [
        arr[0:patch_size, 0:patch_size],
        arr[0:patch_size, max(0, w - patch_size):w],
        arr[max(0, h - patch_size):h, 0:patch_size],
        arr[max(0, h - patch_size):h, max(0, w - patch_size):w],
    ]
    stacked = np.concatenate([p.reshape(-1, 3) for p in patches], axis=0)
    return np.median(stacked, axis=0)


def build_foreground_mask(
    img: Image.Image,
    threshold: float = DEFAULT_FACE_MASK_THRESHOLD,
) -> np.ndarray:
    arr = np.asarray(img).astype(np.float32)
    bg = sample_background_color(img)

    diff = np.sqrt(np.sum((arr - bg) ** 2, axis=2))
    mask = diff > threshold

    # Light cleanup without extra dependencies:
    # remove isolated specks via simple neighborhood count
    padded = np.pad(mask.astype(np.uint8), 1, mode="constant", constant_values=0)
    neighbor_sum = (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2] + padded[1:-1, 1:-1] + padded[1:-1, 2:] +
        padded[2:, :-2] + padded[2:, 1:-1] + padded[2:, 2:]
    )
    mask = neighbor_sum >= 3

    return mask


def bbox_from_mask(mask: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return None
    left = int(xs.min())
    right = int(xs.max()) + 1
    top = int(ys.min())
    bottom = int(ys.max()) + 1
    return (left, top, right, bottom)


def estimate_subject_box(mask: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    coverage = float(mask.mean())
    if coverage < DEFAULT_MIN_MASK_COVERAGE:
        return None
    return bbox_from_mask(mask)


def estimate_head_box(
    mask: np.ndarray,
    subject_box: Tuple[int, int, int, int],
    upper_portion: float = DEFAULT_HEAD_UPPER_PORTION,
) -> Optional[Tuple[int, int, int, int]]:
    left, top, right, bottom = subject_box
    subj_h = bottom - top
    if subj_h < 20:
        return None

    upper_bottom = top + int(round(subj_h * upper_portion))
    upper_mask = mask[top:upper_bottom, left:right]

    head_bbox = bbox_from_mask(upper_mask)
    if head_bbox is None:
        return None

    h_left, h_top, h_right, h_bottom = head_bbox
    return (
        left + h_left,
        top + h_top,
        left + h_right,
        top + h_bottom,
    )


def clamp_crop_box(
    left: int,
    top: int,
    crop_w: int,
    crop_h: int,
    img_w: int,
    img_h: int,
) -> Tuple[int, int, int, int]:
    left = clamp(left, 0, img_w - crop_w)
    top = clamp(top, 0, img_h - crop_h)
    return (left, top, left + crop_w, top + crop_h)


def compute_face_normalized_crop(
    img: Image.Image,
    target_ratio: float,
    head_box: Tuple[int, int, int, int],
    subject_box: Tuple[int, int, int, int],
    face_top_margin_pct: float = DEFAULT_FACE_TOP_MARGIN_PCT,
    chin_pct: float = DEFAULT_FACE_CHIN_PCT,
    horizontal_bias: float = 0.50,
    tighten: float = 1.0,
    profile_direction: Optional[str] = None,
) -> Tuple[int, int, int, int]:
    img_w, img_h = img.size
    h_left, h_top, h_right, h_bottom = head_box

    head_w = max(1, h_right - h_left)
    head_h = max(1, h_bottom - h_top)

    # Use head top + chin target to derive crop height
    # head bottom is our practical chin proxy in this no-ML version
    crop_h_from_head = int(
        round(head_h / max(0.05, (chin_pct - face_top_margin_pct)))
    )
    crop_h = min(crop_h_from_head, img_h)
    crop_w = int(round(crop_h * target_ratio))
    if crop_w > img_w:
        crop_w = img_w
        crop_h = int(round(crop_w / target_ratio))

    # Apply tighten after deriving normalized crop size
    crop_w = max(1, int(round(crop_w * tighten)))
    crop_h = max(1, int(round(crop_h * tighten)))

    crop_w = min(crop_w, img_w)
    crop_h = min(crop_h, img_h)

    # Re-enforce ratio
    crop_w = int(round(crop_h * target_ratio))
    if crop_w > img_w:
        crop_w = img_w
        crop_h = int(round(crop_w / target_ratio))

    # Vertical anchoring:
    # place head top at desired margin, using head_box top as hair-top proxy
    top = int(round(h_top - crop_h * face_top_margin_pct))

    # Horizontal anchoring:
    # default: center on head box
    head_cx = 0.5 * (h_left + h_right)

    if profile_direction == "left":
        # face points left; preserve more room in front of the nose
        nose_x = h_left
        backhead_x = h_right
        desired_nose_x = crop_w * 0.30
        desired_backhead_x = crop_w * 0.76
        # blend both anchors a bit
        left_from_nose = int(round(nose_x - desired_nose_x))
        left_from_back = int(round(backhead_x - desired_backhead_x))
        left = int(round(0.35 * left_from_nose + 0.65 * left_from_back))
    elif profile_direction == "right":
        nose_x = h_right
        backhead_x = h_left
        desired_nose_x = crop_w * 0.70
        desired_backhead_x = crop_w * 0.24
        left_from_nose = int(round(nose_x - desired_nose_x))
        left_from_back = int(round(backhead_x - desired_backhead_x))
        left = int(round(0.35 * left_from_nose + 0.65 * left_from_back))
    else:
        # centered around the head box, with optional additional bias
        ideal_left = int(round(head_cx - crop_w / 2))
        extra_w = img_w - crop_w
        bias_left = int(round(extra_w * horizontal_bias))
        left = int(round(0.65 * ideal_left + 0.35 * bias_left))

    return clamp_crop_box(left, top, crop_w, crop_h, img_w, img_h)


def draw_debug_boxes(
    img: Image.Image,
    crop_box: Tuple[int, int, int, int],
    subject_box: Optional[Tuple[int, int, int, int]] = None,
    head_box: Optional[Tuple[int, int, int, int]] = None,
) -> Image.Image:
    debug = img.copy()
    draw = ImageDraw.Draw(debug)

    if subject_box is not None:
        draw.rectangle(subject_box, outline=(0, 180, 255), width=4)

    if head_box is not None:
        draw.rectangle(head_box, outline=(255, 120, 0), width=4)

    draw.rectangle(crop_box, outline=(255, 0, 120), width=5)
    return debug


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


def crop_to_ratio_face_normalized(
    img: Image.Image,
    target_ratio: float = TARGET_PANEL_RATIO,
    vertical_bias: float = 0.30,  # retained for fallback compatibility
    tighten: float = 1.0,
    horizontal_bias: float = 0.50,
    profile_direction: Optional[str] = None,
) -> CropResult:
    """
    Face-aware crop:
    - detect foreground against flat background
    - estimate subject box
    - estimate head box from upper subject region
    - compute 3:4 crop using normalized head anchors

    Falls back to deterministic crop if normalization fails.
    """
    mask = build_foreground_mask(img)
    subject_box = estimate_subject_box(mask)

    if subject_box is None:
        fallback = crop_to_ratio(
            img,
            target_ratio=target_ratio,
            vertical_bias=vertical_bias,
            tighten=tighten,
            horizontal_bias=horizontal_bias,
        )
        fallback.method = f"fallback-no-subject-{fallback.method}"
        return fallback

    head_box = estimate_head_box(mask, subject_box)
    if head_box is None:
        fallback = crop_to_ratio(
            img,
            target_ratio=target_ratio,
            vertical_bias=vertical_bias,
            tighten=tighten,
            horizontal_bias=horizontal_bias,
        )
        fallback.method = f"fallback-no-head-{fallback.method}"
        fallback.subject_box = subject_box
        return fallback

    crop_box = compute_face_normalized_crop(
        img=img,
        target_ratio=target_ratio,
        head_box=head_box,
        subject_box=subject_box,
        horizontal_bias=horizontal_bias,
        tighten=tighten,
        profile_direction=profile_direction,
    )

    cropped = img.crop(crop_box)
    return CropResult(
        image=cropped,
        method="face-normalized",
        crop_box=crop_box,
        subject_box=subject_box,
        head_box=head_box,
    )

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
    parser.add_argument(
        "--no-face-normalize",
        action="store_true",
        help="Disable face-aware normalization and use the legacy deterministic crop.",
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

    if args.version is not None:
        version = args.version
        paths = build_expected_paths(face_dir, args.character, version)
        front_path = paths["front"]
        profile_path = paths["profile"]
        three_quarter_path = paths["three_quarter"]
        output_version = version
    else:
        try:
            latest_inputs = find_latest_inputs(face_dir, args.character)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        front_path = latest_inputs["front"]
        profile_path = latest_inputs["profile"]
        three_quarter_path = latest_inputs["three_quarter"]
        output_version = next_face_anchor_version(face_dir, args.character)

    character_slug, _ = normalize_character_name(args.character)
    default_output = face_dir / f"{character_slug}_face_anchor_{output_version}.png"
    output_path = args.output.resolve() if args.output else default_output

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

    if args.no_face_normalize:
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
    else:
        front_crop = crop_to_ratio_face_normalized(
            front_img,
            vertical_bias=args.vertical_bias,
            horizontal_bias=args.front_horizontal_bias,
            tighten=args.tighten,
            profile_direction=None,
        )
        profile_crop = crop_to_ratio_face_normalized(
            profile_img,
            vertical_bias=args.vertical_bias,
            horizontal_bias=profile_horizontal_bias,
            tighten=args.tighten,
            profile_direction=profile_direction,
        )
        three_quarter_crop = crop_to_ratio_face_normalized(
            three_quarter_img,
            vertical_bias=args.vertical_bias,
            horizontal_bias=args.three_quarter_horizontal_bias,
            tighten=args.tighten,
            profile_direction=None,
        )

    panel_size = (args.panel_width, args.panel_height)
    front_panel = fit_panel(front_crop.image, panel_size)
    profile_panel = fit_panel(profile_crop.image, panel_size)
    three_quarter_panel = fit_panel(three_quarter_crop.image, panel_size)

    if args.debug_dir is not None:
        debug_dir = args.debug_dir.resolve()
        debug_dir.mkdir(parents=True, exist_ok=True)

        save_debug_image(profile_crop.image, debug_dir / "profile_cropped.png")
        save_debug_image(front_crop.image, debug_dir / "front_cropped.png")
        save_debug_image(three_quarter_crop.image, debug_dir / "three_quarter_cropped.png")

        save_debug_image(
            draw_debug_boxes(
                profile_img,
                profile_crop.crop_box,
                subject_box=profile_crop.subject_box,
                head_box=profile_crop.head_box,
            ),
            debug_dir / "profile_debug_boxes.png",
        )
        save_debug_image(
            draw_debug_boxes(
                front_img,
                front_crop.crop_box,
                subject_box=front_crop.subject_box,
                head_box=front_crop.head_box,
            ),
            debug_dir / "front_debug_boxes.png",
        )
        save_debug_image(
            draw_debug_boxes(
                three_quarter_img,
                three_quarter_crop.crop_box,
                subject_box=three_quarter_crop.subject_box,
                head_box=three_quarter_crop.head_box,
            ),
            debug_dir / "three_quarter_debug_boxes.png",
        )

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
    print(f"Output version: {output_version}")
    print(f"Front input version: v{extract_version(front_path)}")
    print(f"Profile input version: v{extract_version(profile_path)}")
    print(f"Three-quarter input version: v{extract_version(three_quarter_path)}")
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
    print(f"Face normalization: {'OFF' if args.no_face_normalize else 'ON'}")
    print(f"Profile subject box: {profile_crop.subject_box}")
    print(f"Profile head box: {profile_crop.head_box}")
    print(f"Front subject box: {front_crop.subject_box}")
    print(f"Front head box: {front_crop.head_box}")
    print(f"Three-quarter subject box: {three_quarter_crop.subject_box}")
    print(f"Three-quarter head box: {three_quarter_crop.head_box}")

    if args.debug_dir is not None:
        print(f"Saved debug crops in: {debug_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
