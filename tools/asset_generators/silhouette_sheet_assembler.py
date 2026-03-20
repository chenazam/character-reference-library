#!/usr/bin/env python3
"""
Silhouette Sheet Assembler v1

Builds a 4-panel silhouette sheet from:
- front
- side
- back
- three_quarter_back

Versioning rules:
- If --version is provided:
    * require that exact version for all panels
    * output sheet uses that same version
- If --version is omitted:
    * resolve highest available version per panel individually
    * output sheet uses next available sheet version

Input dir:
    docs/assets/library/10_CHARACTERS/[CHARACTER]/02_BODY/structure

Output dir:
    docs/assets/library/10_CHARACTERS/[CHARACTER]/02_BODY/structure
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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

DEFAULT_THRESHOLD = 10.0  # silhouette mask threshold can be lower

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


@dataclass(frozen=True)
class ResolvedPanel:
    panel: str
    path: Path
    version: str  # e.g. "v2"


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


def resolve_structure_dir(project_root: Path, character_name: str) -> Path:
    _, character_dir = normalize_character_name(character_name)
    return project_root / CHAR_ROOT_RELATIVE / character_dir / "02_BODY" / "structure"


def parse_version(version: str | None) -> str:
    if not version:
        return ""
    version = version.strip()
    if not version:
        return ""
    if not version.lower().startswith("v"):
        version = f"v{version}"
    return version.lower()


def version_key(version: str) -> Tuple[int, str]:
    if not version:
        return (0, "")
    m = re.fullmatch(r"v(\d+)", version, re.IGNORECASE)
    if m:
        return (int(m.group(1)), version.lower())
    return (-1, version.lower())


def extract_version_from_stem(stem: str) -> str:
    m = re.search(r"_v(\d+)$", stem, re.IGNORECASE)
    return f"v{m.group(1)}" if m else ""


def build_panel_filename(slug: str, panel: str, version: str) -> str:
    suffix = f"_{version}" if version else ""
    return f"{slug}_silhouette_{panel}{suffix}.png"


def build_sheet_filename(slug: str, version: str) -> str:
    suffix = f"_{version}" if version else ""
    return f"{slug}_silhouette_sheet{suffix}.png"


def find_latest_panel(structure_dir: Path, slug: str, panel: str) -> Optional[ResolvedPanel]:
    pattern = f"{slug}_silhouette_{panel}*.png"
    matches: List[ResolvedPanel] = []

    expected_stem = f"{slug}_silhouette_{panel}"
    for path in structure_dir.glob(pattern):
        stem = path.stem.lower()

        # Explicitly ignore normalized (and any future derived variants)
        if "_normalized" in stem:
            continue

        m = re.fullmatch(
            rf"{re.escape(expected_stem)}(?:_(v\d+))?",
            path.stem,
            re.IGNORECASE,
        )
        if not m:
            continue

        version = m.group(1) or ""
        matches.append(ResolvedPanel(panel=panel, path=path, version=version))

    if not matches:
        return None

    return max(matches, key=lambda x: version_key(x.version))


def resolve_panels(
    structure_dir: Path,
    character: str,
    forced_version: str,
) -> Dict[str, ResolvedPanel]:
    slug, _ = normalize_character_name(character)
    resolved: Dict[str, ResolvedPanel] = {}

    for panel in PANELS:
        if forced_version:
            path = structure_dir / build_panel_filename(slug, panel, forced_version)
            if not path.exists():
                raise FileNotFoundError(f"Missing required panel: {path}")
            resolved[panel] = ResolvedPanel(panel=panel, path=path, version=forced_version)
        else:
            latest = find_latest_panel(structure_dir, slug, panel)
            if latest is None:
                raise FileNotFoundError(
                    f"Could not find any silhouette panel for '{panel}' in {structure_dir}"
                )
            resolved[panel] = latest

    return resolved


def choose_next_sheet_version(structure_dir: Path, character: str) -> str:
    slug, _ = normalize_character_name(character)
    pattern = f"{slug}_silhouette_sheet*.png"
    versions = []

    expected_stem = f"{slug}_silhouette_sheet"
    for path in structure_dir.glob(pattern):
        m = re.fullmatch(rf"{re.escape(expected_stem)}(?:_(v\d+))?", path.stem, re.IGNORECASE)
        if not m:
            continue
        version = m.group(1) or ""
        versions.append(version)

    if not versions:
        return "v1"

    highest = max(versions, key=version_key)
    if not highest:
        return "v1"

    n = version_key(highest)[0]
    return f"v{n + 1}"


def estimate_bg(img: Image.Image, s: int = 24) -> np.ndarray:
    w, h = img.size
    s = min(s, w, h)

    corners = [
        img.crop((0, 0, s, s)),
        img.crop((w - s, 0, w, s)),
        img.crop((0, h - s, s, h)),
        img.crop((w - s, h - s, w, h)),
    ]
    vals = []
    for c in corners:
        arr = np.asarray(c, dtype=np.float32).reshape(-1, 3)
        vals.append(arr.mean(axis=0))
    return np.mean(vals, axis=0)


def normalize_bg(img: Image.Image, target: Tuple[int, int, int] = DEFAULT_BG) -> Image.Image:
    bg = estimate_bg(img)
    arr = np.asarray(img, dtype=np.float32)
    dist = np.sqrt(((arr - bg) ** 2).sum(axis=2))

    alpha = np.clip((dist - 8) / (28 - 8), 0, 1)[..., None]
    result = np.array(target, dtype=np.float32) * (1 - alpha) + arr * alpha
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
        raise ValueError("Mask appears empty; could not find foreground bounds.")
    return Bounds(xs.min(), ys.min(), xs.max(), ys.max())


def resize(img: Image.Image, scale: float) -> Image.Image:
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
    return min(
        DEFAULT_TARGET_HEIGHT,
        *[DEFAULT_MAX_WIDTH * (b.height / b.width) for b in bounds_list],
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

    figure_area = DEFAULT_TARGET_HEIGHT + 60
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

def render(processed: Dict[str, Processed], output: Path) -> Image.Image:
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

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return canvas


# ---------------- MAIN ----------------

def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("--character", type=str)
    parser.add_argument("--dir", type=Path, help="Override structure directory")
    parser.add_argument("--version", type=str, help="Force exact version for all panels")

    args = parser.parse_args()

    try:
        forced_version = parse_version(args.version)

        if args.dir:
            structure_dir = args.dir.resolve()
            if not args.character:
                raise ValueError("--character required when using --dir")
            character = args.character

        elif args.character:
            project_root = find_project_root(Path(__file__))
            if project_root is None:
                raise ValueError("Could not detect project root")
            structure_dir = resolve_structure_dir(project_root, args.character)
            character = args.character

        else:
            raise ValueError("Provide either --character or --dir")

        if not structure_dir.exists():
            raise FileNotFoundError(structure_dir)

        resolved = resolve_panels(
            structure_dir=structure_dir,
            character=character,
            forced_version=forced_version,
        )

        print("Resolved inputs:")
        for panel in PANELS:
            rp = resolved[panel]
            version_label = rp.version if rp.version else "(no suffix)"
            print(f"  {panel:<18} -> {rp.path.name} [{version_label}]")

        data = {}
        for key in PANELS:
            img, bounds = process_panel(resolved[key].path)
            data[key] = (img, bounds)

        shared_h = compute_shared_height([b for _, b in data.values()])
        _, _, centers, baseline = compute_layout(len(PANELS))

        processed = {}
        for i, key in enumerate(PANELS):
            img, bounds = data[key]
            scale = shared_h / bounds.height
            resized = resize(img, scale)
            px, py = place(bounds, scale, centers[i], baseline)
            processed[key] = Processed(img, bounds, scale, resized, px, py)

        slug, _ = normalize_character_name(character)
        if forced_version:
            output_version = forced_version
        else:
            output_version = choose_next_sheet_version(structure_dir, character)

        out = structure_dir / build_sheet_filename(slug, output_version)
        render(processed, out)

        print("Writing output:")
        print(f"  silhouette_sheet     -> {out.name} [{output_version}]")
        print(f"Saved: {out}")
        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())