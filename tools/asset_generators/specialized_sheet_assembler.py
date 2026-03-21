#!/usr/bin/env python3
"""
specialized_sheet_assembler.py

Assemble specialized anatomy renders into a labeled sheet.

Default conventions:
- Input folder:
  docs/assets/library/10_CHARACTERS/{CHARACTER}/02_BODY/anatomy/specialized
- Output folder:
  same as input
- Source filename:
  {character}_anatomy_{asset}_{view}_v{n}.png
- Output filename:
  {character}_{asset}_sheet_v{n}.png

Version behavior:
- If --version is omitted, the script selects the highest available version
  for each requested view independently.
- The output sheet version is always the next available sheet version,
  unless --output-version is explicitly provided.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from PIL import Image, ImageColor, ImageDraw, ImageFont


VIEW_LABELS = {
    "front": "FRONT",
    "back": "BACK",
    "side": "SIDE",
    "three_quarter": "3/4",
    "three_quarter_back": "3/4",
    "three_quarter_front": "3/4",
}

VALID_RATIOS = {"1:1", "3:4", "4:5", "2:3"}

PRESETS = {
    "glutes": {
        "views": ["back", "side", "three_quarter"],
        "panel_ratio": "3:4",
        "labels": "on",
    },
    "upper_body": {
        "views": ["front", "side", "back"],
        "panel_ratio": "3:4",
        "labels": "on",
    },
    "torso": {
        "views": ["front", "side", "three_quarter"],
        "panel_ratio": "3:4",
        "labels": "on",
    },
    "legs": {
        "views": ["front", "side", "back"],
        "panel_ratio": "2:3",
        "labels": "on",
    },
    "arms": {
        "views": ["front", "side"],
        "panel_ratio": "3:4",
        "labels": "on",
    },
}


@dataclass(frozen=True)
class Config:
    character: str
    asset: str
    views: List[str]
    ratio_text: str
    target_ratio: float
    panel_width: int
    panel_height: int
    gap: int
    outer_margin: int
    label_space: int
    background: Tuple[int, int, int]
    labels: bool
    input_dir: Path
    output_dir: Path
    forced_input_version: int | None
    forced_output_version: int | None
    force: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble specialized anatomy source renders into a labeled sheet."
    )
    parser.add_argument("--character", required=True, help="Character slug/folder name, e.g. jasper")
    parser.add_argument("--asset", required=True, help="Specialized asset family, e.g. glutes")
    parser.add_argument(
        "--views",
        nargs="+",
        help="Ordered list of views, e.g. back side three_quarter",
    )
    parser.add_argument(
        "--panel-ratio",
        help="Panel aspect ratio, e.g. 3:4",
    )
    parser.add_argument(
        "--input-dir",
        help="Override canonical input directory",
    )
    parser.add_argument(
        "--output-dir",
        help="Override canonical output directory",
    )
    parser.add_argument(
        "--labels",
        choices=("on", "off"),
        help="Whether to render labels under panels (default: on)",
    )
    parser.add_argument(
        "--background",
        default="#e9e9e9",
        help="Sheet background color (default: #e9e9e9)",
    )
    parser.add_argument(
        "--gap",
        type=int,
        default=48,
        help="Gap between panels in pixels (default: 48)",
    )
    parser.add_argument(
        "--outer-margin",
        type=int,
        default=64,
        help="Outer sheet margin in pixels (default: 64)",
    )
    parser.add_argument(
        "--label-space",
        type=int,
        default=72,
        help="Reserved label area height in pixels (default: 72)",
    )
    parser.add_argument(
        "--panel-width",
        type=int,
        default=800,
        help="Panel width in pixels (default: 800)",
    )
    parser.add_argument(
        "--version",
        type=int,
        help="Force a specific input version for all requested views",
    )
    parser.add_argument(
        "--output-version",
        type=int,
        help="Force a specific output sheet version",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting an explicitly requested output version",
    )
    parser.add_argument(
        "--preset",
        choices=tuple(PRESETS.keys()),
        help="Optional sheet preset, e.g. glutes",
    )
    return parser.parse_args()


def canonical_specialized_dir(character: str) -> Path:
    return Path("docs/assets/library/10_CHARACTERS") / character / "02_BODY" / "anatomy" / "specialized"


def parse_ratio(text: str) -> float:
    if text not in VALID_RATIOS:
        raise ValueError(
            f"Unsupported panel ratio '{text}'. Supported values: {', '.join(sorted(VALID_RATIOS))}"
        )
    w_text, h_text = text.split(":")
    w = int(w_text)
    h = int(h_text)
    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid panel ratio '{text}'")
    return w / h


def build_config(args: argparse.Namespace) -> Config:
    character = args.character.strip()
    asset = args.asset.strip()

    if not character:
        raise ValueError("--character must not be empty")
    if not asset:
        raise ValueError("--asset must not be empty")

    preset_data = PRESETS.get(args.preset, {})

    views = [v.strip() for v in (args.views or preset_data.get("views", []))]
    if not views:
        raise ValueError("No views provided. Use --views or --preset.")

    ratio_text = args.panel_ratio or preset_data.get("panel_ratio")
    if not ratio_text:
        raise ValueError("No panel ratio provided. Use --panel-ratio or --preset.")
    target_ratio = parse_ratio(ratio_text)

    labels_value = args.labels
    if labels_value is None:
        labels_value = preset_data.get("labels", "on")

    panel_width = int(args.panel_width)
    if panel_width <= 0:
        raise ValueError("--panel-width must be > 0")
    panel_height = int(round(panel_width / target_ratio))

    background = ImageColor.getrgb(args.background)

    input_dir = Path(args.input_dir) if args.input_dir else canonical_specialized_dir(character)
    output_dir = Path(args.output_dir) if args.output_dir else canonical_specialized_dir(character)

    return Config(
        character=character,
        asset=asset,
        views=views,
        ratio_text=ratio_text,
        target_ratio=target_ratio,
        panel_width=panel_width,
        panel_height=panel_height,
        gap=int(args.gap),
        outer_margin=int(args.outer_margin),
        label_space=int(args.label_space),
        background=background,
        labels=(labels_value == "on"),
        input_dir=input_dir,
        output_dir=output_dir,
        forced_input_version=args.version,
        forced_output_version=args.output_version,
        force=bool(args.force),
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def source_filename_pattern(character: str, asset: str, view: str) -> re.Pattern[str]:
    escaped_character = re.escape(character)
    escaped_asset = re.escape(asset)
    escaped_view = re.escape(view)
    return re.compile(
        rf"^{escaped_character}_anatomy_{escaped_asset}_{escaped_view}_v(?P<version>\d+)\.png$",
        re.IGNORECASE,
    )


def output_filename_pattern(character: str, asset: str) -> re.Pattern[str]:
    escaped_character = re.escape(character)
    escaped_asset = re.escape(asset)
    return re.compile(
        rf"^{escaped_character}_{escaped_asset}_sheet_v(?P<version>\d+)\.png$",
        re.IGNORECASE,
    )


def find_view_input(config: Config, view: str) -> Tuple[Path, int]:
    pattern = source_filename_pattern(config.character, config.asset, view)
    candidates: List[Tuple[int, Path]] = []

    if not config.input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {config.input_dir}")

    for path in config.input_dir.glob("*.png"):
        match = pattern.match(path.name)
        if not match:
            continue
        version = int(match.group("version"))
        candidates.append((version, path))

    if not candidates:
        raise FileNotFoundError(
            f"No source image found for view '{view}' in {config.input_dir} "
            f"matching pattern '{config.character}_anatomy_{config.asset}_{view}_v#.png'"
        )

    candidates.sort(key=lambda item: item[0])

    if config.forced_input_version is not None:
        for version, path in candidates:
            if version == config.forced_input_version:
                return path, version
        raise FileNotFoundError(
            f"Requested --version {config.forced_input_version} not found for view '{view}' in {config.input_dir}"
        )

    return candidates[-1][1], candidates[-1][0]


def find_latest_inputs(config: Config) -> Dict[str, Tuple[Path, int]]:
    return {view: find_view_input(config, view) for view in config.views}


def get_next_output_version(config: Config) -> int:
    ensure_dir(config.output_dir)

    if config.forced_output_version is not None:
        output_path = config.output_dir / f"{config.character}_{config.asset}_sheet_v{config.forced_output_version}.png"
        if output_path.exists() and not config.force:
            raise FileExistsError(
                f"Output already exists: {output_path}. Use --force to overwrite it."
            )
        return config.forced_output_version

    pattern = output_filename_pattern(config.character, config.asset)
    highest = 0
    for path in config.output_dir.glob("*.png"):
        match = pattern.match(path.name)
        if not match:
            continue
        highest = max(highest, int(match.group("version")))
    return highest + 1


def center_crop_to_ratio(image: Image.Image, target_ratio: float) -> Image.Image:
    width, height = image.size
    current_ratio = width / height

    if math.isclose(current_ratio, target_ratio, rel_tol=1e-9, abs_tol=1e-9):
        return image.copy()

    if current_ratio > target_ratio:
        new_width = int(round(height * target_ratio))
        left = max(0, (width - new_width) // 2)
        right = left + new_width
        box = (left, 0, right, height)
    else:
        new_height = int(round(width / target_ratio))
        top = max(0, (height - new_height) // 2)
        bottom = top + new_height
        box = (0, top, width, bottom)

    return image.crop(box)


def load_and_process_panel(path: Path, config: Config) -> Image.Image:
    with Image.open(path) as img:
        img = img.convert("RGB")
        cropped = center_crop_to_ratio(img, config.target_ratio)
        resized = cropped.resize((config.panel_width, config.panel_height), Image.Resampling.LANCZOS)
        return resized


def compute_layout(panel_count: int) -> Tuple[int, int]:
    if panel_count <= 0:
        raise ValueError("panel_count must be > 0")
    if panel_count == 1:
        return 1, 1
    if panel_count == 2:
        return 1, 2
    if panel_count == 3:
        return 1, 3
    if panel_count == 4:
        return 2, 2
    raise ValueError("V1 supports 1 to 4 panels only")


def load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=size)
    except Exception:
        return ImageFont.load_default()


def view_label(view: str) -> str:
    return VIEW_LABELS.get(view, view.replace("_", " ").upper())


def render_sheet(panels: Sequence[Tuple[str, Image.Image]], config: Config) -> Image.Image:
    rows, cols = compute_layout(len(panels))
    panel_area_width = cols * config.panel_width + (cols - 1) * config.gap
    panel_area_height = rows * config.panel_height + (rows - 1) * config.gap
    label_block_height = config.label_space if config.labels else 0

    canvas_width = panel_area_width + 2 * config.outer_margin
    canvas_height = panel_area_height + rows * label_block_height + 2 * config.outer_margin

    sheet = Image.new("RGB", (canvas_width, canvas_height), config.background)
    draw = ImageDraw.Draw(sheet)
    font = load_font(size=28)

    top = config.outer_margin
    left = config.outer_margin

    for index, (view, panel) in enumerate(panels):
        row = index // cols
        col = index % cols

        x = left + col * (config.panel_width + config.gap)
        y = top + row * (config.panel_height + config.gap + label_block_height)

        sheet.paste(panel, (x, y))

        if config.labels:
            label = view_label(view)
            bbox = draw.textbbox((0, 0), label, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            tx = x + (config.panel_width - text_w) / 2
            ty = y + config.panel_height + (config.label_space - text_h) / 2
            draw.text((tx, ty), label, fill=(80, 80, 80), font=font)

    return sheet


def resolve_output_path(config: Config, version: int) -> Path:
    return config.output_dir / f"{config.character}_{config.asset}_sheet_v{version}.png"


def print_summary(
    config: Config,
    selected_inputs: Dict[str, Tuple[Path, int]],
    output_path: Path,
) -> None:
    print("Specialized sheet assembly")
    print(f"  Character      : {config.character}")
    print(f"  Asset          : {config.asset}")
    print(f"  Views          : {', '.join(config.views)}")
    print(f"  Panel ratio    : {config.ratio_text} ({config.panel_width}x{config.panel_height})")
    print(f"  Input dir      : {config.input_dir}")
    print(f"  Output dir     : {config.output_dir}")
    print(f"  Labels         : {'on' if config.labels else 'off'}")
    print("  Selected inputs:")
    for view in config.views:
        path, version = selected_inputs[view]
        print(f"    - {view:<14} v{version:<3} {path.name}")
    print(f"  Output         : {output_path}")


def main() -> int:
    try:
        args = parse_args()
        config = build_config(args)
        ensure_dir(config.output_dir)

        selected_inputs = find_latest_inputs(config)
        version = get_next_output_version(config)
        output_path = resolve_output_path(config, version)

        panels = [(view, load_and_process_panel(selected_inputs[view][0], config)) for view in config.views]
        sheet = render_sheet(panels, config)

        if output_path.exists() and not config.force:
            raise FileExistsError(
                f"Refusing to overwrite existing file: {output_path}. Use --force if that is intentional."
            )

        sheet.save(output_path)
        print_summary(config, selected_inputs, output_path)
        print("Done.")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
