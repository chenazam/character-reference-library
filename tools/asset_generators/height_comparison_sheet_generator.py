#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional, Tuple

import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--left-character", required=True)
    parser.add_argument("--right-character", required=True)
    parser.add_argument("--left-height-cm", type=float)
    parser.add_argument("--right-height-cm", type=float)
    parser.add_argument("--output")

    parser.add_argument("--canvas-width", type=int, default=2200)
    parser.add_argument("--canvas-height", type=int, default=1800)
    parser.add_argument("--background", default="#f3f3f3")
    parser.add_argument("--top-padding", type=int, default=120)
    parser.add_argument("--bottom-padding", type=int, default=180)
    parser.add_argument("--side-padding", type=int, default=140)
    parser.add_argument("--character-gap", type=int, default=220)

    parser.add_argument("--background-threshold", type=int, default=18)
    parser.add_argument("--bbox-pad-x", type=int, default=16)
    parser.add_argument("--bbox-pad-top", type=int, default=16)
    parser.add_argument("--bbox-pad-bottom", type=int, default=28)
    parser.add_argument("--min-row-coverage", type=float, default=0.015)

    parser.add_argument("--show-debug", action="store_true")
    return parser.parse_args()


# ------------------------------------------------------------
# PATH RESOLUTION
# ------------------------------------------------------------

def resolve_anatomy_front(character: str) -> Path:
    char_slug = character.lower()
    base_path = character_root(character) / "02_BODY/anatomy"

    if not base_path.exists():
        raise FileNotFoundError(f"Anatomy path not found: {base_path}")

    pattern = re.compile(rf"{re.escape(char_slug)}_anatomy_front_v(\d+)\.png$")

    best_version = -1
    best_file = None
    for file in base_path.glob(f"{char_slug}_anatomy_front_v*.png"):
        match = pattern.match(file.name)
        if match:
            version = int(match.group(1))
            if version > best_version:
                best_version = version
                best_file = file

    if not best_file:
        raise FileNotFoundError(f"No anatomy front image found for {character}")

    print(f"[RESOLVED] {character}: {best_file.name}")
    return best_file


def character_root(character: str) -> Path:
    return ROOT / "docs/assets/library/10_CHARACTERS" / character


def canonical_pair_folder_name(character_a: str, character_b: str) -> str:
    ordered = sorted([character_a.upper(), character_b.upper()])
    return f"{ordered[0]}_{ordered[1]}"


def resolve_pair_output_path(left_character: str, right_character: str, explicit_output: Optional[str]) -> Path:
    if explicit_output:
        return Path(explicit_output)

    pair_folder = ROOT / "docs/assets/library/20_CHARACTER_PAIRS" / canonical_pair_folder_name(left_character, right_character)
    pair_folder.mkdir(parents=True, exist_ok=True)

    left_slug = left_character.lower()
    right_slug = right_character.lower()
    pattern = re.compile(rf"{re.escape(left_slug)}_{re.escape(right_slug)}_height_comparison_v([0-9]+)[.]png$")

    best_version = 0
    for file in pair_folder.glob(f"{left_slug}_{right_slug}_height_comparison_v*.png"):
        match = pattern.match(file.name)
        if match:
            version = int(match.group(1))
            if version > best_version:
                best_version = version

    next_version = best_version + 1
    return pair_folder / f"{left_slug}_{right_slug}_height_comparison_v{next_version}.png"


def resolve_metadata_path(character: str) -> Path:
    return character_root(character) / "00_PROFILE" / "metadata.yaml"


def load_height_from_metadata(character: str) -> Optional[float]:
    metadata_path = resolve_metadata_path(character)
    if not metadata_path.exists():
        print(f"[HEIGHT] {character}: metadata.yaml not found, falling back to CLI height if provided")
        return None

    try:
        with metadata_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"[HEIGHT] {character}: failed to read metadata.yaml ({exc}), falling back to CLI height if provided")
        return None

    raw_height = None
    if isinstance(data, dict):
        physical = data.get("physical")
        if isinstance(physical, dict):
            raw_height = physical.get("height_cm")

    if raw_height is None:
        print(f"[HEIGHT] {character}: physical.height_cm missing in metadata.yaml, falling back to CLI height if provided")
        return None

    try:
        height = float(raw_height)
    except (TypeError, ValueError):
        print(f"[HEIGHT] {character}: invalid physical.height_cm={raw_height!r}, falling back to CLI height if provided")
        return None

    if height <= 0:
        print(f"[HEIGHT] {character}: non-positive physical.height_cm={height}, falling back to CLI height if provided")
        return None

    print(f"[HEIGHT] {character}: loaded {height} cm from metadata.yaml")
    return height


def resolve_height(character: str, cli_height: Optional[float]) -> float:
    metadata_height = load_height_from_metadata(character)
    if metadata_height is not None:
        return metadata_height

    if cli_height is not None and cli_height > 0:
        print(f"[HEIGHT] {character}: using CLI override/fallback {cli_height} cm")
        return cli_height

    raise ValueError(
        f"No usable height found for {character}. Add height_cm to metadata.yaml or pass a positive CLI height."
    )


# ------------------------------------------------------------
# IMAGE / MASK HELPERS
# ------------------------------------------------------------

def create_mask(img: Image.Image, threshold: int = 245) -> Image.Image:
    """
    Build a foreground mask by comparing each pixel to the sampled background
    color from the image corners instead of using a naive near-white cutoff.
    This is much more reliable for pale gray backgrounds like #f3f3f3.
    """
    rgb = img.convert("RGB")
    w, h = rgb.size

    corners = [
        rgb.getpixel((0, 0)),
        rgb.getpixel((w - 1, 0)),
        rgb.getpixel((0, h - 1)),
        rgb.getpixel((w - 1, h - 1)),
    ]
    bg_r = round(sum(c[0] for c in corners) / 4)
    bg_g = round(sum(c[1] for c in corners) / 4)
    bg_b = round(sum(c[2] for c in corners) / 4)

    mask = Image.new("L", (w, h), 0)

    for y in range(h):
        for x in range(w):
            r, g, b = rgb.getpixel((x, y))
            dist = abs(r - bg_r) + abs(g - bg_g) + abs(b - bg_b)
            if dist >= threshold:
                mask.putpixel((x, y), 255)

    mask = mask.filter(ImageFilter.MedianFilter(3))
    mask = mask.filter(ImageFilter.MaxFilter(3))
    return mask


def expand_bbox(
    bbox: Tuple[int, int, int, int],
    image_size: Tuple[int, int],
    pad_x: int,
    pad_top: int,
    pad_bottom: int,
) -> Tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    w, h = image_size

    return (
        max(0, left - pad_x),
        max(0, top - pad_top),
        min(w, right + pad_x),
        min(h, bottom + pad_bottom),
    )


def row_coverage(mask: Image.Image, y: int, left: int, right: int) -> float:
    count = 0
    for x in range(left, right):
        if mask.getpixel((x, y)) > 0:
            count += 1
    return count / max(1, (right - left))


def get_bbox(mask: Image.Image) -> Tuple[int, int, int, int]:
    bbox = mask.getbbox()
    if not bbox:
        raise ValueError("No subject detected")
    return bbox


def detect_head_feet(mask: Image.Image, bbox: Tuple[int, int, int, int], min_row_coverage: float) -> Tuple[int, int]:
    left, top, right, bottom = bbox

    head = None
    for y in range(top, bottom):
        if row_coverage(mask, y, left, right) >= min_row_coverage:
            head = y
            break
    if head is None:
        raise ValueError("Could not detect head line")

    foot = None
    for y in range(bottom - 1, top - 1, -1):
        if row_coverage(mask, y, left, right) >= min_row_coverage:
            foot = y
            break
    if foot is None:
        raise ValueError("Could not detect foot line")

    return head, foot


def cutout_with_alpha(img: Image.Image, mask: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    alpha = mask.filter(ImageFilter.GaussianBlur(1.2))
    rgba.putalpha(alpha)
    return rgba


def prepare(image_path: Path, args) -> Tuple[Image.Image, int, int]:
    img = Image.open(image_path).convert("RGBA")
    mask = create_mask(img, threshold=args.background_threshold)

    raw_bbox = get_bbox(mask)
    bbox = expand_bbox(
        raw_bbox,
        img.size,
        pad_x=args.bbox_pad_x,
        pad_top=args.bbox_pad_top,
        pad_bottom=args.bbox_pad_bottom,
    )

    head, foot = detect_head_feet(mask, bbox, args.min_row_coverage)
    rgba = cutout_with_alpha(img, mask)
    cut = rgba.crop(bbox)

    if args.show_debug:
        debug = img.convert("RGB")
        draw = ImageDraw.Draw(debug)
        draw.rectangle(bbox, outline="red", width=3)
        draw.line((bbox[0], head, bbox[2], head), fill="blue", width=3)
        draw.line((bbox[0], foot, bbox[2], foot), fill="green", width=3)
        debug_path = image_path.with_name(image_path.stem + "_height_debug.png")
        debug.save(debug_path)
        print(f"[DEBUG] saved {debug_path.name}")

    return cut, head - bbox[1], foot - bbox[1]


# ------------------------------------------------------------
# BUILD
# ------------------------------------------------------------

def resize_subject(img: Image.Image, head: int, foot: int, target_height_px: int) -> Tuple[Image.Image, int, int]:
    body_px = foot - head
    if body_px <= 0:
        raise ValueError("Invalid detected body height")

    scale = target_height_px / body_px
    new_w = max(1, round(img.width * scale))
    new_h = max(1, round(img.height * scale))
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return img, round(head * scale), round(foot * scale)


def load_font(size: int):
    for candidate in [
        "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def build(left_char, right_char, left_h, right_h, args):
    left_path = resolve_anatomy_front(left_char)
    right_path = resolve_anatomy_front(right_char)

    left_img, l_head, l_foot = prepare(left_path, args)
    right_img, r_head, r_foot = prepare(right_path, args)

    W, H = args.canvas_width, args.canvas_height
    baseline = H - args.bottom_padding
    available_height = H - args.top_padding - args.bottom_padding

    # Shared px/cm so both characters fit the same real-world scale.
    px_per_cm = available_height / max(left_h, right_h)
    left_target_height_px = round(left_h * px_per_cm)
    right_target_height_px = round(right_h * px_per_cm)

    left_img, l_head, l_foot = resize_subject(left_img, l_head, l_foot, left_target_height_px)
    right_img, r_head, r_foot = resize_subject(right_img, r_head, r_foot, right_target_height_px)

    # If combined width is too large, shrink both equally while preserving relative scale.
    usable_width = W - 2 * args.side_padding
    combined_width = left_img.width + right_img.width + args.character_gap
    if combined_width > usable_width:
        s = usable_width / combined_width
        left_img = left_img.resize((round(left_img.width * s), round(left_img.height * s)), Image.Resampling.LANCZOS)
        right_img = right_img.resize((round(right_img.width * s), round(right_img.height * s)), Image.Resampling.LANCZOS)
        l_head, l_foot = round(l_head * s), round(l_foot * s)
        r_head, r_foot = round(r_head * s), round(r_foot * s)

    canvas = Image.new("RGBA", (W, H), args.background)

    group_width = left_img.width + args.character_gap + right_img.width
    start_x = (W - group_width) // 2
    lx = start_x
    rx = lx + left_img.width + args.character_gap

    ly = baseline - l_foot
    ry = baseline - r_foot

    canvas.alpha_composite(left_img, (lx, ly))
    canvas.alpha_composite(right_img, (rx, ry))

    draw = ImageDraw.Draw(canvas)
    font = load_font(24)
    draw.text((lx + left_img.width // 2, baseline + 28), f"{left_char} ({int(left_h)} cm)", anchor="ma", fill="#444", font=font)
    draw.text((rx + right_img.width // 2, baseline + 28), f"{right_char} ({int(right_h)} cm)", anchor="ma", fill="#444", font=font)

    return canvas.convert("RGB")


# ------------------------------------------------------------
# ENTRY
# ------------------------------------------------------------

def main():
    args = parse_args()
    left_height_cm = resolve_height(args.left_character, args.left_height_cm)
    right_height_cm = resolve_height(args.right_character, args.right_height_cm)

    sheet = build(args.left_character, args.right_character, left_height_cm, right_height_cm, args)

    out = resolve_pair_output_path(args.left_character, args.right_character, args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"Saved -> {out}")


if __name__ == "__main__":
    main()
