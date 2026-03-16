#!/usr/bin/env python3

import argparse
import pathlib
import sys
import yaml

try:
    from tools.site_paths import site_root_url
except ModuleNotFoundError:
    from site_paths import site_root_url


try:
    from tools.height_utils import (
        get_nested,
        fallback_proportion_archetype,
        get_reference_silhouette_link,
        make_root_image_link,
        build_reference_placeholder,
        build_character_placeholder,
        build_silhouette_img,
    )
except ModuleNotFoundError:
    from height_utils import (
        get_nested,
        fallback_proportion_archetype,
        get_reference_silhouette_link,
        make_root_image_link,
        build_reference_placeholder,
        build_character_placeholder,
        build_silhouette_img,
    )



ROOT = pathlib.Path(__file__).resolve().parents[1]
LIBRARY_ROOT = ROOT / "docs" / "assets" / "library" / "10_CHARACTERS"
OUTPUT_ROOT = ROOT / "docs" / "comparisons" / "lineups"

NORMAL_CHART_HEIGHT_PX = 460
COMPACT_CHART_HEIGHT_PX = 360
COMPACT_THRESHOLD = 4
REFERENCE_SILHOUETTE = ROOT / "docs" / "assets" / "reference" / "reference_male_average_180cm_front_v1.png"


def get_nested(d, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default


def get_reference_silhouette_link() -> str:
    if not REFERENCE_SILHOUETTE.exists():
        return ""
    try:
        return site_root_url(REFERENCE_SILHOUETTE)
    except Exception:
        return ""


def load_character(slug: str) -> dict:
    if not LIBRARY_ROOT.exists():
        raise FileNotFoundError(f"Library root not found: {LIBRARY_ROOT}")

    for char_dir in LIBRARY_ROOT.iterdir():
        if not char_dir.is_dir():
            continue

        meta_file = char_dir / "00_PROFILE" / "metadata.yaml"
        if not meta_file.exists():
            continue

        meta = yaml.safe_load(meta_file.read_text(encoding="utf-8")) or {}
        if meta.get("slug") == slug:
            meta["_dir"] = char_dir
            return meta

    raise ValueError(f"Character not found for slug: {slug}")


def find_asset(meta: dict, key: str) -> str:
    refs = meta.get("reference_files", {})
    filename = refs.get(key, "")
    if not filename:
        return ""

    character_dir = pathlib.Path(meta["_dir"])
    matches = [p for p in character_dir.rglob(filename) if p.is_file()]
    if not matches:
        return ""

    matches.sort()
    try:
        return site_root_url(matches[0])
    except Exception:
        return ""


def build_chart(characters: list[dict]) -> str:
    reference_height = 180
    reference_imperial = "5'11\""

    compact_mode = len(characters) >= COMPACT_THRESHOLD
    chart_height_px = COMPACT_CHART_HEIGHT_PX if compact_mode else NORMAL_CHART_HEIGHT_PX
    reference_silhouette = get_reference_silhouette_link()

    max_height = max(max(c["physical"]["height_cm"] for c in characters), reference_height)

    def pct(h: int) -> float:
        return (h / max_height) * 100

    def tick_px(cm: int) -> float:
        return (cm / max_height) * chart_height_px

    tick_step = 10
    tick_start = (max_height // tick_step) * tick_step

    ticks = []
    for t in range(tick_start, 0, -tick_step):
        ticks.append(
            f'<div class="height-lineup__tick" style="bottom: {tick_px(t):.2f}px;">'
            f'<span class="height-lineup__tick-label">{t} cm</span></div>'
        )

    character_silhouettes = [
        find_asset(c, "silhouette_front")
        for c in characters
    ]
    use_real_character_silhouettes = all(bool(s) for s in character_silhouettes)
    use_real_reference = bool(use_real_character_silhouettes and reference_silhouette)

    if use_real_reference:
        reference_figure = (
            f'<img class="height-lineup__silhouette height-lineup__silhouette--reference" '
            f'src="{reference_silhouette}" '
            f'alt="Reference silhouette" '
            f'style="height: {pct(reference_height):.2f}%;">'
        )
    else:
        reference_figure = (
            f'<div class="height-lineup__placeholder '
            f'height-lineup__placeholder--athletic_balanced '
            f'height-lineup__placeholder--reference" '
            f'style="height: {pct(reference_height):.2f}%"></div>'
        )

    figures = [
        f"""
<div class="height-lineup__figure">
  <div class="height-lineup__stage">
    {reference_figure}
  </div>
  <div class="height-lineup__label">Reference</div>
  <div class="height-lineup__meta">{reference_height} cm / {reference_imperial}</div>
</div>
"""
    ]

    for c, silhouette in zip(characters, character_silhouettes):
        name = c["name"]
        height = c["physical"]["height_cm"]
        imperial = c["physical"]["height_imperial"]
        archetype = fallback_proportion_archetype(meta)
        
        print(f"[archetype] {meta['name']} → {archetype}")
        
        print(f"[archetype] {meta['name']} → {archetype}")

        if silhouette:
            body = (
                f'<img class="height-lineup__silhouette" '
                f'src="{silhouette}" '
                f'alt="{name} silhouette" '
                f'style="height: {pct(height):.2f}%;">'
            )
        else:
            body = (
                f'<div class="height-lineup__placeholder '
                f'height-lineup__placeholder--{archetype}" '
                f'style="height: {pct(height):.2f}%"></div>'
            )

        figures.append(
            f"""
<div class="height-lineup__figure">
  <div class="height-lineup__stage">
    {body}
  </div>
  <div class="height-lineup__label">{name}</div>
  <div class="height-lineup__meta">{height} cm / {imperial}</div>
</div>
"""
        )

    lineup_classes = "height-lineup height-lineup--multi"
    if compact_mode:
        lineup_classes += " height-lineup--compact"

    return f"""
<div class="{lineup_classes}">

  <div class="height-lineup__ticks" aria-hidden="true">
    {"".join(ticks)}
  </div>

  <div class="height-lineup__baseline" aria-hidden="true"></div>
  <div class="height-lineup__spacer" aria-hidden="true"></div>

  {"".join(figures)}

</div>
"""


def generate_lineup(slugs: list[str]) -> pathlib.Path:
    characters = [load_character(s) for s in slugs]
    characters.sort(key=lambda c: c["physical"]["height_cm"], reverse=True)

    title = "Height Lineup — " + ", ".join(c["name"] for c in characters)

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    filename = "-".join(sorted(slugs)) + "-lineup.md"
    output_file = OUTPUT_ROOT / filename

    chart = build_chart(characters)

    markdown = f"""---
hide:
  - toc
---

# {title}

{chart}
"""

    output_file.write_text(markdown, encoding="utf-8")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="Generate a multi-character height lineup page.")
    parser.add_argument("slugs", nargs="+", help="Character slugs to include")
    args = parser.parse_args()

    try:
        output_file = generate_lineup(args.slugs)
        print(f"Generated lineup page: {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
