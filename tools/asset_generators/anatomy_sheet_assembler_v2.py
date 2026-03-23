#!/usr/bin/env python3
"""
Anatomy / Body Anchor Sheet Assembler v2

Supports N panels (default: front / side / back / three_quarter)

Design goals:
- identical baseline across panels
- identical normalized figure height across panels
- no per-view scaling bias
- panel-agnostic layout
- background normalization preserved
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ---------------- CONFIG ----------------

PANELS = ["front", "side", "back", "three_quarter_back"]

LABEL_MAP = {
    "front": "FRONT",
    "side": "SIDE",
    "back": "BACK",
    "three_quarter_back": "3/4",
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
    def width(self): return self.x_max - self.x_min + 1

    @property
    def height(self): return self.y_max - self.y_min + 1


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


def next_output_version(anatomy_dir: Path, character: str) -> str:
    slug, _ = normalize_character_name(character)
    candidates = list(anatomy_dir.glob(f"{slug}_body_anchor_v*.png"))

    max_n = 0
    for path in candidates:
        m = re.match(rf"^{re.escape(slug)}_body_anchor_v(\d+)\.png$", path.name)
        if m:
            max_n = max(max_n, int(m.group(1)))

    return f"v{max_n + 1}"


def find_project_root(start_path: Path) -> Optional[Path]:
    current = start_path.resolve()
    if current.is_file():
        current = current.parent

    for candidate in [current, *current.parents]:
        if (candidate / CHAR_ROOT_RELATIVE).exists():
            return candidate
    return None


def resolve_anatomy_dir(project_root: Path, character_name: str) -> Path:
    _, character_dir = normalize_character_name(character_name)
    return project_root / CHAR_ROOT_RELATIVE / character_dir / "02_BODY" / "anatomy"


def resolve_structure_dir(project_root: Path, character_name: str) -> Path:
    _, character_dir = normalize_character_name(character_name)
    return project_root / CHAR_ROOT_RELATIVE / character_dir / "02_BODY" / "structure"


def build_paths(anatomy_dir: Path, character: str, version: str):
    slug, _ = normalize_character_name(character)
    suffix = f"_{version}" if version else ""

    return {
        p: anatomy_dir / f"{slug}_anatomy_{p}{suffix}.png"
        for p in PANELS
    }


def choose_latest_paths(anatomy_dir: Path, character: str) -> Dict[str, Path]:
    slug, _ = normalize_character_name(character)
    resolved: Dict[str, Path] = {}

    def version_key(path: Path):
        m = re.match(rf"^{re.escape(slug)}_anatomy_[a-z_]+(?:_(v\d+))?\.png$", path.name)
        if not m:
            return (-1, "")
        version = m.group(1) or ""
        if not version:
            return (0, "")
        vm = re.match(r"v(\d+)", version)
        return (int(vm.group(1)) if vm else -1, version)

    for panel in PANELS:
        candidates = list(anatomy_dir.glob(f"{slug}_anatomy_{panel}*.png"))
        candidates = [
            p for p in candidates
            if re.match(rf"^{re.escape(slug)}_anatomy_{re.escape(panel)}(?:_(v\d+))?\.png$", p.name)
        ]
        if not candidates:
            raise FileNotFoundError(
                f"Could not find any versions for panel '{panel}' in {anatomy_dir}"
            )
        candidates.sort(key=version_key)
        resolved[panel] = candidates[-1]

    return resolved

    def key(v):
        if not v:
            return (0, "")
        m = re.match(r"v(\d+)", v)
        return (int(m.group(1)) if m else -1, v)

    for v in sorted(versions, key=key, reverse=True):
        paths = build_paths(anatomy_dir, character, v)
        if all(p.exists() for p in paths.values()):
            return v

    return None


def estimate_bg(img: Image.Image, s=24):
    w, h = img.size
    corners = [
        img.crop((0, 0, s, s)),
        img.crop((w-s, 0, w, s)),
        img.crop((0, h-s, s, h)),
        img.crop((w-s, h-s, w, h)),
    ]
    vals = []
    for c in corners:
        arr = np.asarray(c, dtype=np.float32).reshape(-1, 3)
        vals.append(arr.mean(axis=0))
    return np.mean(vals, axis=0)


def normalize_bg(img: Image.Image, target=DEFAULT_BG):
    bg = estimate_bg(img)
    arr = np.asarray(img, dtype=np.float32)
    dist = np.sqrt(((arr - bg) ** 2).sum(axis=2))

    alpha = np.clip((dist - 16) / (40 - 16), 0, 1)[..., None]
    result = target * (1 - alpha) + arr * alpha
    return Image.fromarray(result.astype(np.uint8))


def mask_fg(img: Image.Image, threshold=DEFAULT_THRESHOLD):
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
    return Bounds(xs.min(), ys.min(), xs.max(), ys.max())


def resize(img, scale):
    w, h = img.size
    return img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)


# ---------------- CORE ----------------

def process_panel(path: Path) -> Tuple[Image.Image, Bounds]:
    img = load_image(path)
    img = normalize_bg(img)
    mask = mask_fg(img)
    bounds = find_bounds(mask)
    return img, bounds


def compute_shared_height(bounds_list: List[Bounds]) -> float:
    return min(DEFAULT_TARGET_HEIGHT, *[
        DEFAULT_MAX_WIDTH * (b.height / b.width)
        for b in bounds_list
    ])


def place(bounds: Bounds, scale: float, center_x: int, baseline: int):
    cx = ((bounds.x_min + bounds.x_max) / 2) * scale
    by = bounds.y_max * scale
    return int(center_x - cx), int(baseline - by)


# ---------------- LAYOUT ----------------

def compute_layout(panel_count: int):
    width = (
        DEFAULT_MARGIN_LEFT +
        panel_count * DEFAULT_PANEL_WIDTH +
        (panel_count - 1) * DEFAULT_GUTTER +
        DEFAULT_MARGIN_RIGHT
    )

    figure_area = DEFAULT_TARGET_HEIGHT + 60
    height = (
        DEFAULT_MARGIN_TOP +
        figure_area +
        DEFAULT_LABEL_GAP +
        DEFAULT_LABEL_BAND +
        DEFAULT_MARGIN_BOTTOM
    )

    centers = []
    x = DEFAULT_MARGIN_LEFT
    for _ in range(panel_count):
        centers.append(x + DEFAULT_PANEL_WIDTH // 2)
        x += DEFAULT_PANEL_WIDTH + DEFAULT_GUTTER

    baseline = DEFAULT_MARGIN_TOP + figure_area

    return width, height, centers, baseline


# ---------------- RENDER ----------------

def render(processed: Dict[str, Processed], output: Path):
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

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--character", type=str)
    parser.add_argument("--dir", type=Path)
    parser.add_argument("--version", type=str)

    args = parser.parse_args()

    if args.dir:
        anatomy_dir = args.dir.resolve()
        if not args.character:
            raise ValueError("--character required when using --dir")
        character = args.character

    elif args.character:
        project_root = find_project_root(Path(__file__))
        if project_root is None:
            raise ValueError("Could not detect project root")

        anatomy_dir = resolve_anatomy_dir(project_root, args.character)
        character = args.character

        structure_dir = resolve_structure_dir(project_root, character)
        structure_dir.mkdir(parents=True, exist_ok=True)

    else:
        raise ValueError("Provide either --character or --dir")

    if not anatomy_dir.exists():
        raise FileNotFoundError(anatomy_dir)

    version = args.version

    if version is None:
        paths = choose_latest_paths(anatomy_dir, character)
    else:
        paths = build_paths(anatomy_dir, character, version)
        for p in paths.values():
            if not p.exists():
                raise FileNotFoundError(p)

    data = {}
    for key in PANELS:
        img, bounds = process_panel(paths[key])
        data[key] = (img, bounds)

    shared_h = compute_shared_height([b for _, b in data.values()])

    width, height, centers, baseline = compute_layout(len(PANELS))

    processed = {}
    for i, key in enumerate(PANELS):
        img, bounds = data[key]
        scale = shared_h / bounds.height
        resized = resize(img, scale)
        px, py = place(bounds, scale, centers[i], baseline)

        processed[key] = Processed(img, bounds, scale, resized, px, py)

    slug, _ = normalize_character_name(character)

    output_version = version if version is not None else next_output_version(structure_dir, character)
    out = structure_dir / f"{slug}_body_anchor_{output_version}.png"
    render(processed, out)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()