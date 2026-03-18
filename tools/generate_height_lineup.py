#!/usr/bin/env python3

import argparse
import pathlib
import sys
import yaml

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
        make_root_image_link(
            c["_dir"],
            get_nested(c, "reference_files", "silhouette_front", default="")
        )
        for c in characters
    ]
    use_real_character_silhouettes = all(bool(s) for s in character_silhouettes)
    use_real_reference = bool(use_real_character_silhouettes and reference_silhouette)

    if use_real_reference:
        reference_figure = build_silhouette_img(
            reference_silhouette,
            "Reference silhouette",
            pct(reference_height),
            reference=True,
        )
    else:
        reference_figure = build_reference_placeholder(pct(reference_height))

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
        archetype = fallback_proportion_archetype(c)

        if use_real_character_silhouettes:
            body = build_silhouette_img(
                silhouette,
                f"{name} silhouette",
                pct(height),
            )
        else:
            body = build_character_placeholder(archetype, pct(height), c)

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
<div class="height-lineup__scroll">
<div class="{lineup_classes}">

  <div class="height-lineup__ticks" aria-hidden="true">
    {"".join(ticks)}
  </div>

  <div class="height-lineup__baseline" aria-hidden="true"></div>
  <div class="height-lineup__spacer" aria-hidden="true"></div>

  {"".join(figures)}

</div>
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
