#!/usr/bin/env python3
"""
panel_sheet_assembler.py

Generalized sheet assembler for ordered panel sets such as:
- pose sheets
- expression sheets
- UCS sheets

Design goals:
- versioned input/output
- configurable ordered panel IDs
- preset defaults for pose/expression/UCS
- "contain" fit mode (never crop source images)
- configurable grid, panel ratio, spacing, margins, labels
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from PIL import Image, ImageColor, ImageDraw, ImageFont


VERSION_RE = re.compile(r"_v(\d+)\.png$", re.IGNORECASE)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LIBRARY_ROOT = PROJECT_ROOT / "docs" / "assets" / "library" / "10_CHARACTERS"

DEFAULT_POSE_PANEL_IDS = [
    "balanced",
    "grounded",
    "casual",
    "rotation",
    "mid_step",
    "open_gesture",
]

DEFAULT_EXPRESSION_PANEL_IDS = [
    "neutral",
    "smile",
    "flirty",
    "smirk",
    "determined",
    "skeptical",
    "surprised",
    "vulnerable",
]

POSE_LABELS = {
    "balanced": "BALANCED",
    "grounded": "GROUNDED",
    "casual": "CASUAL",
    "rotation": "ROTATION",
    "mid_step": "MID-STEP",
    "open_gesture": "OPEN GESTURE",
}

EXPRESSION_LABELS = {
    "neutral": "NEUTRAL",
    "smile": "SMILE",
    "flirty": "FLIRTY",
    "smirk": "SMIRK",
    "determined": "DETERMINED",
    "skeptical": "SKEPTICAL",
    "surprised": "SURPRISED",
    "vulnerable": "VULNERABLE",
}

# Relative to character root, without version suffix.
def build_ucs_panels(
    name: str,
    expression_id: str,
    outfit_id: str,
    outfit_label: Optional[str] = None,
) -> List[Tuple[str, str]]:
    if outfit_id == "signature":
        outfit_rel = f"04_STYLE/signature/{name}_outfit_signature_front"
        outfit_panel_label = outfit_label or "SIGNATURE"
    else:
        outfit_rel = f"04_STYLE/wardrobes/{name}_outfit_{outfit_id}_front"
        outfit_panel_label = outfit_label or outfit_id.replace("_", " ").upper()

    return [
        (f"01_IDENTITY/face/{name}_front_face", "FRONT FACE"),
        (f"01_IDENTITY/face/{name}_three_quarter_face", "3/4 FACE"),
        (f"01_IDENTITY/face/{name}_front_face_photoreal", "PHOTOREAL"),
        (f"02_BODY/anatomy/{name}_anatomy_front", "BODY"),
        (outfit_rel, outfit_panel_label),
        (f"01_IDENTITY/expression/{name}_expression_{expression_id}", "EXPRESSION"),
    ]


@dataclass(frozen=True)
class Preset:
    rows: int
    cols: int
    panel_ratio: Tuple[int, int]
    sheet_width: int
    margin: int
    gap: int
    panel_padding: int
    labels: bool
    label_font_size: int
    label_gap: int
    bg_color: str
    panel_bg_color: str
    label_color: str
    source_subdir: Path


PRESETS: Dict[str, Preset] = {
    "pose": Preset(
        rows=2,
        cols=3,
        panel_ratio=(3, 4),
        sheet_width=2400,
        margin=90,
        gap=55,
        panel_padding=26,
        labels=True,
        label_font_size=34,
        label_gap=18,
        bg_color="#efefef",
        panel_bg_color="#f8f8f8",
        label_color="#3a3a3a",
        source_subdir=Path("05_MOTION/poses"),
    ),
    "expression": Preset(
        rows=2,
        cols=4,
        panel_ratio=(4, 5),
        sheet_width=2800,
        margin=100,
        gap=40,
        panel_padding=18,
        labels=True,
        label_font_size=30,
        label_gap=26,
        bg_color="#efefef",
        panel_bg_color="#f8f8f8",
        label_color="#3a3a3a",
        source_subdir=Path("01_IDENTITY/expression"),
    ),
    "ucs": Preset(
        rows=2,
        cols=3,
        panel_ratio=(4, 5),
        sheet_width=2600,
        margin=90,
        gap=45,
        panel_padding=20,
        labels=True,
        label_font_size=30,
        label_gap=18,
        bg_color="#efefef",
        panel_bg_color="#f8f8f8",
        label_color="#3a3a3a",
        source_subdir=Path("."),  # unused for UCS
    ),
}


def resolve_character_dir(library_root: Path, character: str) -> Path:
    target = character.lower()

    for path in library_root.iterdir():
        if path.is_dir() and path.name.lower() == target:
            return path

    raise FileNotFoundError(
        f"Character directory not found for '{character}' in {library_root}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble pose/expression/UCS panel sheets.")

    parser.add_argument("--character", required=True, help="Character name, e.g. jasper")
    parser.add_argument(
        "--sheet-type",
        required=True,
        choices=sorted(PRESETS.keys()),
        help="Sheet preset to use.",
    )
    parser.add_argument(
        "--panel-ids",
        default=None,
        help="Comma-separated ordered panel IDs, e.g. balanced,contrapposto,... Required for pose/expression. Ignored for ucs.",
    )

    parser.add_argument(
        "--library-root",
        default=str(DEFAULT_LIBRARY_ROOT),
        help="Base library root. Default: /docs/assets/library/10_CHARACTERS",
    )
    parser.add_argument(
        "--source-dir",
        default=None,
        help="Optional explicit source directory override.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional explicit output directory override. Defaults to source-dir (or character root for UCS).",
    )
    parser.add_argument(
        "--version",
        type=int,
        default=None,
        help="Optional explicit input version. If omitted, latest version per panel is used.",
    )

    parser.add_argument("--rows", type=int, default=None, help="Override rows.")
    parser.add_argument("--cols", type=int, default=None, help="Override cols.")
    parser.add_argument("--sheet-width", type=int, default=None, help="Sheet width in px.")
    parser.add_argument("--margin", type=int, default=None, help="Outer margin in px.")
    parser.add_argument("--gap", type=int, default=None, help="Gap between panels in px.")
    parser.add_argument(
        "--panel-padding",
        type=int,
        default=None,
        help="Inner padding inside each panel in px.",
    )
    parser.add_argument(
        "--panel-ratio",
        default=None,
        help="Panel ratio as W:H, e.g. 3:4 or 4:5",
    )

    parser.add_argument(
        "--labels",
        dest="labels",
        action="store_true",
        default=None,
        help="Enable labels.",
    )
    parser.add_argument(
        "--no-labels",
        dest="labels",
        action="store_false",
        help="Disable labels.",
    )
    parser.add_argument(
        "--label-font-size",
        type=int,
        default=None,
        help="Label font size in px.",
    )
    parser.add_argument(
        "--label-gap",
        type=int,
        default=None,
        help="Gap between panel and label in px.",
    )
    parser.add_argument(
        "--font-path",
        default=None,
        help="Optional TTF/OTF font path. Falls back to common sans fonts / PIL default.",
    )

    parser.add_argument("--bg-color", default=None, help='Sheet background color, e.g. "#efefef"')
    parser.add_argument(
        "--panel-bg-color",
        default=None,
        help='Panel background color, e.g. "#f8f8f8"',
    )
    parser.add_argument(
        "--label-color",
        default=None,
        help='Label text color, e.g. "#5f5f5f"',
    )

    parser.add_argument(
        "--expression-id",
        help="Expression id for UCS (default: smirk)",
    )

    parser.add_argument(
        "--outfit-id",
        default="signature",
        help="Outfit id for UCS. Default: signature. Non-signature outfits are resolved from 04_STYLE/wardrobes.",
    )
    parser.add_argument(
        "--outfit-label",
        default=None,
        help="Optional custom UCS label for the outfit panel. Defaults to SIGNATURE or the uppercase outfit id.",
    )

    return parser.parse_args()


def parse_ratio(value: Optional[str], fallback: Tuple[int, int]) -> Tuple[int, int]:
    if not value:
        return fallback
    match = re.fullmatch(r"\s*(\d+)\s*:\s*(\d+)\s*", value)
    if not match:
        raise ValueError(f"Invalid ratio '{value}'. Use W:H, e.g. 3:4")
    w, h = int(match.group(1)), int(match.group(2))
    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid ratio '{value}'. Both sides must be > 0.")
    return (w, h)


def normalize_character_name(name: str) -> str:
    return name.strip().lower()


def make_panel_filename(character: str, sheet_type: str, panel_id: str, version: int) -> str:
    return f"{character}_{sheet_type}_{panel_id}_v{version}.png"


def make_panel_glob(character: str, sheet_type: str, panel_id: str) -> str:
    return f"{character}_{sheet_type}_{panel_id}_v*.png"


def make_output_filename(character: str, sheet_type: str, version: int) -> str:
    if sheet_type == "ucs":
        return f"{character}_ucs_v{version}.png"
    return f"{character}_{sheet_type}_sheet_v{version}.png"


def extract_version(path: Path) -> Optional[int]:
    match = VERSION_RE.search(path.name)
    return int(match.group(1)) if match else None


def resolve_source_dir(character_dir: Path, sheet_type: str, source_dir: Optional[str]) -> Path:
    if source_dir:
        return Path(source_dir)
    preset = PRESETS[sheet_type]
    if sheet_type == "ucs":
        return character_dir
    return character_dir / preset.source_subdir


def resolve_output_dir(source_dir: Path, output_dir: Optional[str]) -> Path:
    return Path(output_dir) if output_dir else source_dir


def resolve_panel_file(
    source_dir: Path,
    character: str,
    sheet_type: str,
    panel_id: str,
    explicit_version: Optional[int],
) -> Path:
    if explicit_version is not None:
        path = source_dir / make_panel_filename(character, sheet_type, panel_id, explicit_version)
        if not path.exists():
            raise FileNotFoundError(f"Missing panel file: {path}")
        return path

    candidates = list(source_dir.glob(make_panel_glob(character, sheet_type, panel_id)))
    candidates = [p for p in candidates if extract_version(p) is not None]
    if not candidates:
        raise FileNotFoundError(
            f"No versions found for panel '{panel_id}' in {source_dir} "
            f"(expected pattern: {character}_{sheet_type}_{panel_id}_v*.png)"
        )

    candidates.sort(key=lambda p: extract_version(p) or -1)
    return candidates[-1]


def resolve_latest_version_file(base_path: Path) -> Path:
    parent = base_path.parent
    stem = base_path.name
    candidates = list(parent.glob(f"{stem}_v*.png"))
    candidates = [p for p in candidates if extract_version(p) is not None]

    if not candidates:
        raise FileNotFoundError(f"No versions found for UCS panel base: {base_path}")

    candidates.sort(key=lambda p: extract_version(p) or -1)
    return candidates[-1]


def resolve_ucs_panels(
    character_dir: Path,
    character_name: str,
    expression_id: str,
    outfit_id: str,
    outfit_label: Optional[str],
    explicit_version: Optional[int],
) -> Tuple[List[Path], List[str], List[str]]:
    panel_paths: List[Path] = []
    panel_ids: List[str] = []
    panel_labels: List[str] = []

    ucs_panels = build_ucs_panels(
    name=character_name,
    expression_id=expression_id,
    outfit_id=outfit_id,
    outfit_label=outfit_label,
    )

    for rel_base, label in ucs_panels:
        rel = rel_base.format(name=character_name, expression_id=expression_id)
        base_path = character_dir / rel

        if explicit_version is not None:
            path = Path(f"{base_path}_v{explicit_version}.png")
            if not path.exists():
                raise FileNotFoundError(f"Missing UCS panel file: {path}")
        else:
            path = resolve_latest_version_file(base_path)

        panel_paths.append(path)
        panel_ids.append(base_path.name)
        panel_labels.append(label)

    return panel_paths, panel_ids, panel_labels


def next_output_version(output_dir: Path, character: str, sheet_type: str) -> int:
    if sheet_type == "ucs":
        candidates = list(output_dir.glob(f"{character}_ucs_v*.png"))
    else:
        candidates = list(output_dir.glob(f"{character}_{sheet_type}_sheet_v*.png"))

    versions = [extract_version(p) for p in candidates]
    versions = [v for v in versions if v is not None]
    return (max(versions) + 1) if versions else 1


def get_label(sheet_type: str, panel_id: str) -> str:
    if sheet_type == "pose":
        return POSE_LABELS.get(panel_id, panel_id.replace("_", " ").upper())
    if sheet_type == "expression":
        return EXPRESSION_LABELS.get(panel_id, panel_id.replace("_", " ").upper())
    return panel_id.replace("_", " ").upper()


def load_font(font_path: Optional[str], size: int) -> ImageFont.ImageFont:
    if font_path:
        path = Path(font_path)
        if not path.exists():
            raise FileNotFoundError(f"Font not found: {font_path}")
        return ImageFont.truetype(str(path), size=size)

    fallback_names = [
        "Arial.ttf",
        "Arial Unicode.ttf",
        "Helvetica.ttf",
        "DejaVuSans.ttf",
        "LiberationSans-Regular.ttf",
    ]
    for name in fallback_names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue

    return ImageFont.load_default()


def get_text_height(font: ImageFont.ImageFont) -> int:
    try:
        bbox = font.getbbox("Ag")
        return bbox[3] - bbox[1]
    except Exception:
        return font.size if hasattr(font, "size") else 16


def contain_fit_size(src_size: Tuple[int, int], max_size: Tuple[int, int]) -> Tuple[int, int]:
    src_w, src_h = src_size
    max_w, max_h = max_size
    if src_w <= 0 or src_h <= 0:
        raise ValueError(f"Invalid source size: {src_size}")
    if max_w <= 0 or max_h <= 0:
        raise ValueError(f"Invalid max size: {max_size}")

    scale = min(max_w / src_w, max_h / src_h)
    out_w = max(1, int(round(src_w * scale)))
    out_h = max(1, int(round(src_h * scale)))
    return out_w, out_h


def compute_geometry(
    panel_count: int,
    rows: int,
    cols: int,
    panel_ratio: Tuple[int, int],
    sheet_width: int,
    margin: int,
    gap: int,
    labels: bool,
    label_height: int,
    label_gap: int,
) -> Dict[str, int]:
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be > 0")
    if rows * cols < panel_count:
        raise ValueError(
            f"Grid too small: rows*cols={rows*cols}, but panel_count={panel_count}"
        )

    ratio_w, ratio_h = panel_ratio
    usable_width = sheet_width - 2 * margin - (cols - 1) * gap
    if usable_width <= 0:
        raise ValueError("Sheet width too small for given margin/gap/cols")

    panel_w = usable_width // cols
    panel_h = int(round(panel_w * ratio_h / ratio_w))

    slot_h = panel_h
    if labels:
        slot_h += label_gap + label_height

    sheet_height = 2 * margin + rows * slot_h + (rows - 1) * gap

    return {
        "panel_w": panel_w,
        "panel_h": panel_h,
        "slot_h": slot_h,
        "sheet_w": sheet_width,
        "sheet_h": sheet_height,
    }


def draw_centered_image(
    panel_img: Image.Image,
    src_img: Image.Image,
    panel_padding: int,
) -> None:
    avail_w = panel_img.width - 2 * panel_padding
    avail_h = panel_img.height - 2 * panel_padding
    if avail_w <= 0 or avail_h <= 0:
        raise ValueError("Panel padding too large for panel size")

    fitted_w, fitted_h = contain_fit_size(src_img.size, (avail_w, avail_h))
    resized = src_img.resize((fitted_w, fitted_h), Image.Resampling.LANCZOS)

    offset_x = (panel_img.width - fitted_w) // 2
    offset_y = (panel_img.height - fitted_h) // 2

    if resized.mode in ("RGBA", "LA"):
        panel_img.paste(resized, (offset_x, offset_y), resized)
    else:
        panel_img.paste(resized, (offset_x, offset_y))


def assemble_sheet(
    panel_paths: Sequence[Path],
    panel_ids: Sequence[str],
    panel_labels: Optional[Sequence[str]],
    character: str,
    sheet_type: str,
    output_path: Path,
    rows: int,
    cols: int,
    panel_ratio: Tuple[int, int],
    sheet_width: int,
    margin: int,
    gap: int,
    panel_padding: int,
    labels: bool,
    font: ImageFont.ImageFont,
    label_gap: int,
    bg_color: str,
    panel_bg_color: str,
    label_color: str,
) -> None:
    label_height = get_text_height(font) if labels else 0
    geom = compute_geometry(
        panel_count=len(panel_paths),
        rows=rows,
        cols=cols,
        panel_ratio=panel_ratio,
        sheet_width=sheet_width,
        margin=margin,
        gap=gap,
        labels=labels,
        label_height=label_height,
        label_gap=label_gap,
    )

    bg_rgb = ImageColor.getrgb(bg_color)
    panel_bg_rgb = ImageColor.getrgb(panel_bg_color)
    label_rgb = ImageColor.getrgb(label_color)

    sheet = Image.new("RGB", (geom["sheet_w"], geom["sheet_h"]), bg_rgb)
    draw = ImageDraw.Draw(sheet)

    for index, (panel_path, panel_id) in enumerate(zip(panel_paths, panel_ids)):
        row = index // cols
        col = index % cols

        slot_x = margin + col * (geom["panel_w"] + gap)
        slot_y = margin + row * (geom["slot_h"] + gap)

        panel_rect = (
            slot_x,
            slot_y,
            slot_x + geom["panel_w"],
            slot_y + geom["panel_h"],
        )
        draw.rectangle(panel_rect, fill=panel_bg_rgb)

        panel_img = Image.new("RGB", (geom["panel_w"], geom["panel_h"]), panel_bg_rgb)
        src = Image.open(panel_path).convert("RGBA")
        draw_centered_image(panel_img, src, panel_padding=panel_padding)
        sheet.paste(panel_img, (slot_x, slot_y))

        if labels:
            if panel_labels is not None:
                label_text = panel_labels[index]
            else:
                label_text = get_label(sheet_type, panel_id)

            try:
                bbox = draw.textbbox((0, 0), label_text, font=font)
                text_w = bbox[2] - bbox[0]
            except Exception:
                text_w = int(len(label_text) * label_height * 0.6)

            text_x = slot_x + (geom["panel_w"] - text_w) // 2
            text_y = slot_y + geom["panel_h"] + label_gap
            draw.text((text_x, text_y), label_text, font=font, fill=label_rgb)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=95)
    print(f"Saved sheet: {output_path}")

    print("\nResolved input panels:")
    for i, (panel_id, panel_path) in enumerate(zip(panel_ids, panel_paths)):
        label_info = f" [{panel_labels[i]}]" if panel_labels is not None else ""
        print(f"  {panel_id:<28} -> {panel_path.name}{label_info}")


def main() -> None:
    args = parse_args()

    character = normalize_character_name(args.character)
    sheet_type = args.sheet_type

    preset = PRESETS[sheet_type]

    rows = args.rows if args.rows is not None else preset.rows
    cols = args.cols if args.cols is not None else preset.cols
    panel_ratio = parse_ratio(args.panel_ratio, preset.panel_ratio)
    sheet_width = args.sheet_width if args.sheet_width is not None else preset.sheet_width
    margin = args.margin if args.margin is not None else preset.margin
    gap = args.gap if args.gap is not None else preset.gap
    panel_padding = args.panel_padding if args.panel_padding is not None else preset.panel_padding
    labels = args.labels if args.labels is not None else preset.labels
    base_width = 2000
    scale = sheet_width / base_width

    expression_id = args.expression_id or "smirk"
    outfit_id = args.outfit_id or "signature"
    outfit_label = args.outfit_label

    default_font_size = int(round(preset.label_font_size * scale))
    label_font_size = (
        args.label_font_size if args.label_font_size is not None else default_font_size
    )
    label_gap = args.label_gap if args.label_gap is not None else preset.label_gap
    bg_color = args.bg_color if args.bg_color is not None else preset.bg_color
    panel_bg_color = (
        args.panel_bg_color if args.panel_bg_color is not None else preset.panel_bg_color
    )
    label_color = args.label_color if args.label_color is not None else preset.label_color

    library_root = Path(args.library_root)
    character_dir = resolve_character_dir(library_root, character)

    source_dir = resolve_source_dir(
        character_dir=character_dir,
        sheet_type=sheet_type,
        source_dir=args.source_dir,
    )
    output_dir = resolve_output_dir(source_dir=source_dir, output_dir=args.output_dir)

    if not source_dir.exists():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    if sheet_type == "ucs":
        panel_paths, panel_ids, panel_labels = resolve_ucs_panels(
            character_dir=character_dir,
            character_name=character,
            expression_id=expression_id,
            outfit_id=outfit_id,
            outfit_label=outfit_label,
            explicit_version=args.version,
        )
    else:
            if args.panel_ids:
                panel_ids = [p.strip() for p in args.panel_ids.split(",") if p.strip()]
                if not panel_ids:
                    raise SystemExit("No panel IDs supplied.")
            else:
                if sheet_type == "pose":
                    panel_ids = DEFAULT_POSE_PANEL_IDS
                elif sheet_type == "expression":
                    panel_ids = DEFAULT_EXPRESSION_PANEL_IDS
                else:
                    raise SystemExit("--panel-ids is required for this sheet type.")

            panel_paths = [
                resolve_panel_file(
                    source_dir=source_dir,
                    character=character,
                    sheet_type=sheet_type,
                    panel_id=panel_id,
                    explicit_version=args.version,
                )
                for panel_id in panel_ids
            ]
            panel_labels = None

    output_version = next_output_version(output_dir, character, sheet_type)
    output_path = output_dir / make_output_filename(character, sheet_type, output_version)

    font = load_font(args.font_path, size=label_font_size)

    assemble_sheet(
        panel_paths=panel_paths,
        panel_ids=panel_ids,
        panel_labels=panel_labels,
        character=character,
        sheet_type=sheet_type,
        output_path=output_path,
        rows=rows,
        cols=cols,
        panel_ratio=panel_ratio,
        sheet_width=sheet_width,
        margin=margin,
        gap=gap,
        panel_padding=panel_padding,
        labels=labels,
        font=font,
        label_gap=label_gap,
        bg_color=bg_color,
        panel_bg_color=panel_bg_color,
        label_color=label_color,
    )


if __name__ == "__main__":
    main()