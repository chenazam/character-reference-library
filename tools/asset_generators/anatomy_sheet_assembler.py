#!/usr/bin/env python3
"""
Anatomy Sheet Assembler

Assembles a 3-panel anatomy sheet from individual FRONT / SIDE / BACK full-body
panel images using strict measurement-first normalization.

Design goals:
- identical baseline across panels
- identical normalized figure height across panels
- no non-uniform scaling
- no aesthetic per-view bias
- no cropping of the body
- strict technical layout

Default output spec:
- canvas: 1800 x 1200
- sheet ratio: 3:2
- panels: FRONT | SIDE | BACK
- panel zones: 500 x 930 figure areas
- shared baseline: y = 990
- target figure height: 880 px
- max figure width inside panel: 450 px

Requirements:
    python -m pip install --upgrade Pillow numpy
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


DEFAULT_CANVAS_WIDTH = 1800
DEFAULT_CANVAS_HEIGHT = 1200

DEFAULT_MARGIN_LEFT = 90
DEFAULT_MARGIN_RIGHT = 90
DEFAULT_MARGIN_TOP = 60
DEFAULT_MARGIN_BOTTOM = 120

DEFAULT_GUTTER = 60
DEFAULT_LABEL_GAP = 20
DEFAULT_LABEL_BAND = 70

DEFAULT_PANEL_WIDTH = 500
DEFAULT_FIGURE_AREA_HEIGHT = 930
DEFAULT_BASELINE_Y = 990

DEFAULT_TARGET_HEIGHT = 880
DEFAULT_MAX_FIGURE_WIDTH = 450

DEFAULT_THRESHOLD = 28.0

DEFAULT_BG = (244, 244, 244)
DEFAULT_TEXT = (90, 90, 90)

DEFAULT_OUTPUT = Path("anatomy_sheet.png")

BASE_LIBRARY_PATH = Path("/docs/assets/library/10_CHARACTERS")


@dataclass
class FigureBounds:
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
class ProcessedFigure:
    source_path: Path
    original_image: Image.Image
    bounds: FigureBounds
    scale: float
    resized_image: Image.Image
    paste_x: int
    paste_y: int


@dataclass
class LayoutSpec:
    canvas_width: int = DEFAULT_CANVAS_WIDTH
    canvas_height: int = DEFAULT_CANVAS_HEIGHT
    margin_left: int = DEFAULT_MARGIN_LEFT
    margin_right: int = DEFAULT_MARGIN_RIGHT
    margin_top: int = DEFAULT_MARGIN_TOP
    margin_bottom: int = DEFAULT_MARGIN_BOTTOM
    gutter: int = DEFAULT_GUTTER
    label_gap: int = DEFAULT_LABEL_GAP
    label_band: int = DEFAULT_LABEL_BAND
    panel_width: int = DEFAULT_PANEL_WIDTH
    figure_area_height: int = DEFAULT_FIGURE_AREA_HEIGHT
    baseline_y: int = DEFAULT_BASELINE_Y
    target_height: int = DEFAULT_TARGET_HEIGHT
    max_figure_width: int = DEFAULT_MAX_FIGURE_WIDTH

    @property
    def panel_centers(self) -> Tuple[int, int, int]:
        x0 = self.margin_left
        x1 = x0 + self.panel_width + self.gutter
        x2 = x1 + self.panel_width + self.gutter
        return (
            x0 + self.panel_width // 2,
            x1 + self.panel_width // 2,
            x2 + self.panel_width // 2,
        )

    @property
    def panel_lefts(self) -> Tuple[int, int, int]:
        x0 = self.margin_left
        x1 = x0 + self.panel_width + self.gutter
        x2 = x1 + self.panel_width + self.gutter
        return x0, x1, x2


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def save_image(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def validate_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    

def resolve_character_paths(character: str) -> tuple[Path, Path, Path]:
    char = character.upper()

    base = BASE_LIBRARY_PATH / char / "02_BODY" / "anatomy"

    front = base / "anatomy_front.png"
    side  = base / "anatomy_side.png"
    back  = base / "anatomy_back.png"

    for p in (front, side, back):
        if not p.exists():
            raise FileNotFoundError(f"Missing anatomy panel: {p}")

    return front, side, back


def average_rgb(values: Iterable[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    arr = np.array(list(values), dtype=np.float32)
    mean = arr.mean(axis=0)
    return float(mean[0]), float(mean[1]), float(mean[2])


def estimate_background_color(img: Image.Image, sample_size: int = 24) -> Tuple[float, float, float]:
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
        mean = arr.mean(axis=0)
        samples.append((float(mean[0]), float(mean[1]), float(mean[2])))

    return average_rgb(samples)


def make_foreground_mask(img: Image.Image, threshold: float = DEFAULT_THRESHOLD) -> Image.Image:
    bg = estimate_background_color(img)
    arr = np.asarray(img, dtype=np.float32)
    bg_arr = np.array(bg, dtype=np.float32)

    diff = arr - bg_arr
    dist = np.sqrt(np.sum(diff * diff, axis=2))

    mask = (dist > threshold).astype(np.uint8) * 255
    mask_img = Image.fromarray(mask, mode="L")
    mask_img = mask_img.filter(ImageFilter.MedianFilter(size=3))
    mask_img = mask_img.point(lambda p: 255 if p >= 128 else 0, mode="L")
    return mask_img


def find_figure_bounds(mask: Image.Image) -> FigureBounds:
    arr = np.asarray(mask, dtype=np.uint8)
    ys, xs = np.where(arr > 0)
    if len(xs) == 0 or len(ys) == 0:
        raise ValueError("Could not detect foreground figure in image.")

    return FigureBounds(
        x_min=int(xs.min()),
        y_min=int(ys.min()),
        x_max=int(xs.max()),
        y_max=int(ys.max()),
    )


def compute_scale(bounds: FigureBounds, layout: LayoutSpec) -> float:
    scale_height_limited = layout.target_height / bounds.height
    scale_width_limited = layout.max_figure_width / bounds.width
    return min(scale_height_limited, scale_width_limited)


def resize_image(img: Image.Image, scale: float) -> Image.Image:
    w, h = img.size
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)


def place_figure(
    bounds: FigureBounds,
    scale: float,
    panel_center_x: int,
    baseline_y: int,
) -> Tuple[int, int]:
    figure_center_x = ((bounds.x_min + bounds.x_max) / 2.0) * scale
    resized_baseline = bounds.y_max * scale

    paste_x = int(round(panel_center_x - figure_center_x))
    paste_y = int(round(baseline_y - resized_baseline))
    return paste_x, paste_y


def process_panel(
    source_path: Path,
    panel_center_x: int,
    layout: LayoutSpec,
    threshold: float,
) -> Tuple[ProcessedFigure, Image.Image]:
    img = load_image(source_path)
    mask = make_foreground_mask(img, threshold=threshold)
    bounds = find_figure_bounds(mask)
    scale = compute_scale(bounds, layout)
    resized = resize_image(img, scale)
    paste_x, paste_y = place_figure(bounds, scale, panel_center_x, layout.baseline_y)

    processed = ProcessedFigure(
        source_path=source_path,
        original_image=img,
        bounds=bounds,
        scale=scale,
        resized_image=resized,
        paste_x=paste_x,
        paste_y=paste_y,
    )
    return processed, mask


def validate_layout(layout: LayoutSpec) -> None:
    expected_width = (
        layout.margin_left
        + layout.panel_width
        + layout.gutter
        + layout.panel_width
        + layout.gutter
        + layout.panel_width
        + layout.margin_right
    )
    if expected_width != layout.canvas_width:
        raise ValueError(
            f"Canvas width mismatch: expected {expected_width} from margins/panels/gutters, got {layout.canvas_width}."
        )

    expected_figure_area_height = (
        layout.canvas_height
        - layout.margin_top
        - layout.margin_bottom
        - layout.label_gap
        - layout.label_band
    )
    if expected_figure_area_height != layout.figure_area_height:
        raise ValueError(
            f"Figure area height mismatch: expected {expected_figure_area_height}, got {layout.figure_area_height}."
        )

    expected_baseline = layout.margin_top + layout.figure_area_height
    if expected_baseline != layout.baseline_y:
        raise ValueError(
            f"Baseline mismatch: expected {expected_baseline}, got {layout.baseline_y}."
        )

    if layout.max_figure_width > layout.panel_width:
        raise ValueError("max_figure_width must be <= panel_width.")
    if layout.target_height > layout.figure_area_height:
        raise ValueError("target_height must be <= figure_area_height.")


def validate_processed_figure(processed: ProcessedFigure, layout: LayoutSpec) -> None:
    scaled_width = processed.bounds.width * processed.scale
    if scaled_width > layout.max_figure_width + 1:
        raise ValueError(
            f"Scaled figure width exceeds max allowed width for {processed.source_path.name}: "
            f"{scaled_width:.2f} > {layout.max_figure_width}"
        )

    scaled_top = processed.bounds.y_min * processed.scale + processed.paste_y
    top_clearance = scaled_top - layout.margin_top
    if top_clearance < 10:
        raise ValueError(
            f"Top clearance too small for {processed.source_path.name}: {top_clearance:.2f}px"
        )


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


def render_sheet(
    front: ProcessedFigure,
    side: ProcessedFigure,
    back: ProcessedFigure,
    layout: LayoutSpec,
    output_path: Path,
    background: Tuple[int, int, int] = DEFAULT_BG,
    text_color: Tuple[int, int, int] = DEFAULT_TEXT,
) -> Image.Image:
    canvas = Image.new("RGB", (layout.canvas_width, layout.canvas_height), background)

    for pf in (front, side, back):
        canvas.paste(pf.resized_image, (pf.paste_x, pf.paste_y))

    draw = ImageDraw.Draw(canvas)
    font = load_font(size=46)

    labels = ["FRONT", "SIDE", "BACK"]
    panel_lefts = layout.panel_lefts
    label_top = layout.margin_top + layout.figure_area_height + layout.label_gap

    for panel_left, label in zip(panel_lefts, labels):
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = panel_left + (layout.panel_width - text_w) // 2
        text_y = label_top + (layout.label_band - text_h) // 2 - 4
        draw.text((text_x, text_y), label, fill=text_color, font=font)

    save_image(canvas, output_path)
    return canvas


def save_debug_mask(mask: Image.Image, path: Path) -> None:
    save_image(mask, path)


def save_debug_bounded_source(img: Image.Image, bounds: FigureBounds, path: Path) -> None:
    debug = img.copy()
    draw = ImageDraw.Draw(debug)
    draw.rectangle((bounds.x_min, bounds.y_min, bounds.x_max, bounds.y_max), outline=(255, 0, 0), width=3)
    save_image(debug, path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a strict anatomy sheet from front/side/back full-body images."
    )
    parser.add_argument("--front", type=Path, required=True, help="Path to front panel image")
    parser.add_argument("--side", type=Path, required=True, help="Path to side panel image")
    parser.add_argument("--back", type=Path, required=True, help="Path to back panel image")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output anatomy sheet path")
    parser.add_argument("--debug-dir", type=Path, default=None, help="Optional debug output directory")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Foreground threshold")
    parser.add_argument("--character", type=str, help="Character name")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.character:
            front_path, side_path, back_path = resolve_character_paths(args.character)
        else:
            if not (args.front and args.side and args.back):
                raise ValueError("Either --character OR all of --front/--side/--back must be provided.")
            front_path, side_path, back_path = args.front, args.side, args.back

        for p in (front_path, side_path, back_path):
            validate_exists(p)

        layout = LayoutSpec()
        validate_layout(layout)

        front_pf, front_mask = process_panel(args.front, layout.panel_centers[0], layout, args.threshold)
        side_pf, side_mask = process_panel(args.side, layout.panel_centers[1], layout, args.threshold)
        back_pf, back_mask = process_panel(args.back, layout.panel_centers[2], layout, args.threshold)

        for pf in (front_pf, side_pf, back_pf):
            validate_processed_figure(pf, layout)

        render_sheet(front_pf, side_pf, back_pf, layout, args.output)

        print("Done.")
        print(f"Output: {args.output}")
        print(f"Threshold: {args.threshold}")
        for label, pf in (("FRONT", front_pf), ("SIDE", side_pf), ("BACK", back_pf)):
            print(
                f"{label}: bounds=({pf.bounds.x_min}, {pf.bounds.y_min}, {pf.bounds.x_max}, {pf.bounds.y_max}), "
                f"scale={pf.scale:.6f}, paste=({pf.paste_x}, {pf.paste_y})"
            )

        if args.debug_dir is not None:
            debug_dir = args.debug_dir.resolve()
            save_debug_mask(front_mask, debug_dir / "front_mask.png")
            save_debug_mask(side_mask, debug_dir / "side_mask.png")
            save_debug_mask(back_mask, debug_dir / "back_mask.png")
            save_debug_bounded_source(front_pf.original_image, front_pf.bounds, debug_dir / "front_bounds.png")
            save_debug_bounded_source(side_pf.original_image, side_pf.bounds, debug_dir / "side_bounds.png")
            save_debug_bounded_source(back_pf.original_image, back_pf.bounds, debug_dir / "back_bounds.png")
            print(f"Saved debug files in: {debug_dir}")

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
