#!/usr/bin/env python3
"""
Specialized / Outfit Sheet Assembler v1

Assembles a 3-panel outfit sheet:
- side
- front
- back

Supports outfit roots:
- signature
- wardrobes

Design goals:
- identical baseline across panels
- identical normalized figure height across panels
- no per-view scaling bias
- clean panel layout
- background normalization preserved
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ---------------- CONFIG ----------------

PANELS = ["side", "front", "back"]

LABEL_MAP = {
    "side": "SIDE",
    "front": "FRONT",
    "back": "BACK",
}

DEFAULT_BG = (244, 244, 244)
DEFAULT_TEXT = (90, 90, 90)

DEFAULT_PANEL_WIDTH = 500
DEFAULT_GUTTER = 60
DEFAULT_MARGIN_LEFT = 80
DEFAULT_MARGIN_RIGHT = 80
DEFAULT_MARGIN_TOP = 60
DEFAULT_MARGIN_BOTTOM = 120

DEFAULT_LABEL_BAND = 80
DEFAULT_LABEL_GAP = 20

DEFAULT_TARGET_HEIGHT = 900
DEFAULT_MAX_WIDTH = 460

DEFAULT_THRESHOLD = 28.0

CHAR_ROOT_RELATIVE = Path("docs/assets/library/10_CHARACTERS")


# ---------------- DATA STRUCTURES ----------------

@dataclass
class Bounds:
    x_min: int
    y_min: int
    x_max: int
    y_max: int

    @property
    def width(self) -> int:
        return self.x_max - self.x_min + 1

    @property
    def height(self) -> int:
        return self.y_max - self.y_min + 1


@dataclass
class Processed:
    image: Image.Image
    bounds: Bounds
    scale: float
    resized: Image.Image
    paste_x: int
    paste_y: int


# ---------------- UTILS ----------------

def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


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


def resolve_outfit_dir(project_root: Path, character_name: str, category: str) -> Path:
    _, character_dir = normalize_character_name(character_name)

    if category not in {"signature", "wardrobes"}:
        raise ValueError("category must be 'signature' or 'wardrobes'")

    return (
        project_root
        / CHAR_ROOT_RELATIVE
        / character_dir
        / "04_STYLE"
        / category
    )


def build_paths(outfit_dir: Path, character: str, outfit: str, version: str = "") -> Dict[str, Path]:
    slug, _ = normalize_character_name(character)
    outfit_slug = outfit.strip().lower()
    suffix = f"_{version}" if version else ""

    return {
        panel: outfit_dir / f"{slug}_{outfit_slug}_{panel}{suffix}.png"
        for panel in PANELS
    }


def choose_latest_version(outfit_dir: Path, character: str, outfit: str) -> Optional[str]:
    slug, _ = normalize_character_name(character)
    outfit_slug = outfit.strip().lower()

    stems = [f"{slug}_{outfit_slug}_{panel}" for panel in PANELS]
    versions = set()

    for stem in stems:
        for file in outfit_dir.glob(f"{stem}*.png"):
            m = re.match(rf"^{re.escape(stem)}(?:_(v\d+))?\.png$", file.name)
            if m:
                versions.add(m.group(1) or "")

    def key(v: str):
        if not v:
            return (0, "")
        m = re.match(r"v(\d+)", v)
        return (int(m.group(1)) if m else -1, v)

    for v in sorted(versions, key=key, reverse=True):
        paths = build_paths(outfit_dir, character, outfit, v)
        if all(path.exists() for path in paths.values()):
            return v

    return None


def estimate_bg(img: Image.Image, s: int = 24) -> np.ndarray:
    w, h = img.size
    corners = [
        img.crop((0, 0, s, s)),
        img.crop((w - s, 0, w, s)),
        img.crop((0, h - s, s, h)),
        img.crop((w - s, h - s, w, h)),
    ]
    vals = []
    for corner in corners:
        arr = np.asarray(corner, dtype=np.float32).reshape(-1, 3)
        vals.append(arr.mean(axis=0))
    return np.mean(vals, axis=0)


def normalize_bg(img: Image.Image, target: Tuple[int, int, int] = DEFAULT_BG) -> Image.Image:
    bg = estimate_bg(img)
    arr = np.asarray(img, dtype=np.float32)
    dist = np.sqrt(((arr - bg) ** 2).sum(axis=2))

    alpha = np.clip((dist - 16) / (40 - 16), 0, 1)[..., None]
    target_arr = np.array(target, dtype=np.float32)
    result = target_arr * (1 - alpha) + arr * alpha
    return Image.fromarray(result.astype(np.uint8))


def mask_fg(img: Image.Image, threshold: float = DEFAULT_THRESHOLD) -> Image.Image:
    bg = estimate_bg(img)
    arr = np.asarray(img, dtype=np.float32)
    dist = np.sqrt(((arr - bg) ** 2).sum(axis=2))
    mask = (dist > threshold).astype(np.uint8) * 255
    m = Image.fromarray(mask)
    m = m.filter(ImageFilter.MedianFilter(3))
    return m


def find_bounds(mask: Image.Image) -> Bounds:
    arr = np.asarray(mask)
    ys, xs = np.where(arr > 0)
    if len(xs) == 0 or len(ys) == 0:
        raise ValueError("Could not detect figure bounds from mask.")
    return Bounds(xs.min(), ys.min(), xs.max(), ys.max())


def resize(img: Image.Image, scale: float) -> Image.Image:
    w, h = img.size
    return img.resize(
        (int(w * scale), int(h * scale)),
        Image.Resampling.LANCZOS,
    )


# ---------------- CORE ----------------

def process_panel(path: Path) -> Tuple[Image.Image, Bounds]:
    img = load_image(path)
    img = normalize_bg(img)
    mask = mask_fg(img)
    bounds = find_bounds(mask)
    return img, bounds


def compute_shared_height(bounds_list: List[Bounds]) -> float:
    return min(
        DEFAULT_TARGET_HEIGHT,
        *[
            DEFAULT_MAX_WIDTH * (b.height / b.width)
            for b in bounds_list
        ],
    )


def place(bounds: Bounds, scale: float, center_x: int, baseline: int) -> Tuple[int, int]:
    cx = ((bounds.x_min + bounds.x_max) / 2) * scale
    by = bounds.y_max * scale
    return int(center_x - cx), int(baseline - by)


# ---------------- LAYOUT ----------------

def compute_layout(panel_count: int) -> Tuple[int, int, List[int], int]:
    width = (
        DEFAULT_MARGIN_LEFT
        + panel_count * DEFAULT_PANEL_WIDTH
        + (panel_count - 1) * DEFAULT_GUTTER
        + DEFAULT_MARGIN_RIGHT
    )

    figure_area = DEFAULT_TARGET_HEIGHT + 100
    height = (
        DEFAULT_MARGIN_TOP
        + figure_area
        + DEFAULT_LABEL_GAP
        + DEFAULT_LABEL_BAND
        + DEFAULT_MARGIN_BOTTOM
    )

    centers = []
    x = DEFAULT_MARGIN_LEFT
    for _ in range(panel_count):
        centers.append(x + DEFAULT_PANEL_WIDTH // 2)
        x += DEFAULT_PANEL_WIDTH + DEFAULT_GUTTER

    baseline = DEFAULT_MARGIN_TOP + figure_area
    return width, height, centers, baseline


# ---------------- RENDER ----------------

def render(
    processed: Dict[str, Processed],
    output: Path,
) -> Image.Image:
    panel_count = len(processed)
    width, height, centers, baseline = compute_layout(panel_count)

    canvas = Image.new("RGB", (width, height), DEFAULT_BG)

    for i, key in enumerate(PANELS):
        pf = processed[key]
        canvas.paste(pf.resized, (pf.paste_x, pf.paste_y))

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    label_y = baseline + DEFAULT_LABEL_GAP

    for i, key in enumerate(PANELS):
        label = LABEL_MAP[key]
        text_w = draw.textlength(label, font=font)
        x = centers[i] - text_w / 2
        draw.text((x, label_y), label, fill=DEFAULT_TEXT, font=font)

    canvas.save(output)
    return canvas


# ---------------- MAIN ----------------

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--character", type=str, required=True)
    parser.add_argument("--outfit", type=str, required=True)
    parser.add_argument(
        "--category",
        type=str,
        choices=["signature", "wardrobes"],
        required=True,
        help="Whether the outfit lives in 04_STYLE/signature or 04_STYLE/wardrobes",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        help="Optional direct path to outfit directory. Overrides auto-resolution.",
    )
    parser.add_argument(
        "--version",
        type=str,
        help="Optional version suffix, e.g. v1. If omitted, the latest complete set is used.",
    )

    args = parser.parse_args()

    character = args.character
    outfit = args.outfit

    if args.dir:
        outfit_dir = args.dir.resolve()
    else:
        project_root = find_project_root(Path(__file__))
        if project_root is None:
            raise ValueError("Could not detect project root.")
        outfit_dir = resolve_outfit_dir(project_root, character, args.category)

    if not outfit_dir.exists():
        raise FileNotFoundError(outfit_dir)

    version = args.version
    if version is None:
        version = choose_latest_version(outfit_dir, character, outfit)
        if version is None:
            raise ValueError("Could not find a complete panel set for this outfit.")

    paths = build_paths(outfit_dir, character, outfit, version)

    for path in paths.values():
        if not path.exists():
            raise FileNotFoundError(path)

    data: Dict[str, Tuple[Image.Image, Bounds]] = {}
    for key in PANELS:
        img, bounds = process_panel(paths[key])
        data[key] = (img, bounds)

    shared_h = compute_shared_height([bounds for _, bounds in data.values()])
    _, _, centers, baseline = compute_layout(len(PANELS))

    processed: Dict[str, Processed] = {}
    for i, key in enumerate(PANELS):
        img, bounds = data[key]
        scale = shared_h / bounds.height
        resized = resize(img, scale)
        paste_x, paste_y = place(bounds, scale, centers[i], baseline)

        processed[key] = Processed(
            image=img,
            bounds=bounds,
            scale=scale,
            resized=resized,
            paste_x=paste_x,
            paste_y=paste_y,
        )

    slug, _ = normalize_character_name(character)
    outfit_slug = outfit.strip().lower()
    suffix = f"_{version}" if version else ""
    output_path = outfit_dir / f"{slug}_{outfit_slug}_sheet{suffix}.png"

    render(processed, output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()