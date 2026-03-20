#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import pathlib
import re
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

REFERENCE_HEIGHT_CM = 180
REFERENCE_HEIGHT_IMPERIAL = "5'11\""


def resolve_latest_normalized_silhouette_front(character_dir: pathlib.Path) -> str:
    structure_dir = character_dir / "02_BODY" / "structure"
    if not structure_dir.exists():
        return ""

    slug = character_dir.name.lower()
    pattern = f"{slug}_silhouette_front*_normalized.png"

    best_path = None
    best_version = -1

    for path in structure_dir.glob(pattern):
        m = re.fullmatch(
            rf"{re.escape(slug)}_silhouette_front(?:_v(\d+))?_normalized",
            path.stem,
            re.IGNORECASE,
        )
        if not m:
            continue

        version = int(m.group(1)) if m.group(1) else 0
        if version > best_version:
            best_version = version
            best_path = path

    if not best_path:
        return ""

    return make_root_image_link(character_dir, best_path.name)


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


def cm_to_inches(cm: float) -> float:
    return cm / 2.54


def cm_to_feet_inches(cm: float) -> str:
    rounded = round(cm_to_inches(cm))
    feet = rounded // 12
    inches = rounded % 12
    return f"{feet}'{inches}\""


def build_ticks(min_cm: int, max_cm: int, step: int = 10) -> str:
    tick_start = (max_cm // step) * step
    ticks = []

    for tick_cm in range(tick_start, min_cm, -step):
        bottom_pct = (tick_cm / max_cm) * 100
        ticks.append(
            f'<div class="height-lineup__tick" style="bottom: {bottom_pct:.4f}%;">'
            f'<span class="height-lineup__tick-label">{tick_cm} cm</span>'
            f"</div>"
        )

    return "".join(ticks)


def build_chart(characters: list[dict]) -> str:
    reference_silhouette = get_reference_silhouette_link()

    character_silhouettes = [
        resolve_latest_normalized_silhouette_front(c["_dir"])
        for c in characters
    ]

    heights_cm = [int(get_nested(c, "physical", "height_cm", default=0) or 0) for c in characters]
    names = [str(c.get("name", c.get("slug", "Unknown"))) for c in characters]
    feet_inches = [cm_to_feet_inches(h) for h in heights_cm]

    max_height = max([REFERENCE_HEIGHT_CM, *heights_cm])
    if max_height <= 0:
        return ""

    def pct(height: int) -> float:
        return (height / max_height) * 100

    use_real_character_silhouettes = all(bool(s) for s in character_silhouettes)
    use_real_reference = bool(use_real_character_silhouettes and reference_silhouette)

    if use_real_reference:
        reference_figure = build_silhouette_img(
            reference_silhouette,
            "Reference silhouette",
            pct(REFERENCE_HEIGHT_CM),
            reference=True,
        )
    else:
        reference_figure = build_reference_placeholder(pct(REFERENCE_HEIGHT_CM))

    figures = [
        f"""
<div class="height-lineup__figure">
  <div class="height-lineup__stage">
    {reference_figure}
  </div>
  <div class="height-lineup__label">Reference</div>
  <div class="height-lineup__meta">{REFERENCE_HEIGHT_CM} cm / {REFERENCE_HEIGHT_IMPERIAL}</div>
</div>
"""
    ]

    for character, silhouette, name, height_cm, imperial in zip(
        characters,
        character_silhouettes,
        names,
        feet_inches,
    ):
        archetype = fallback_proportion_archetype(character)

        if use_real_character_silhouettes:
            body = build_silhouette_img(
                silhouette,
                f"{name} silhouette",
                pct(height_cm),
            )
        else:
            body = build_character_placeholder(archetype, pct(height_cm), character)

        figures.append(
            f"""
<div class="height-lineup__figure">
  <div class="height-lineup__stage">
    {body}
  </div>
  <div class="height-lineup__label">{html.escape(name)}</div>
  <div class="height-lineup__meta">{height_cm} cm / {imperial}</div>
</div>
"""
        )

    lineup_count = len(characters) + 1

    return f"""
<div class="height-lineup__scroll">
  <div class="height-lineup height-lineup--multi" style="--lineup-count:{lineup_count};">
    <div class="height-lineup__ticks" aria-hidden="true">
      {build_ticks(0, max_height)}
    </div>

    <div class="height-lineup__baseline" aria-hidden="true"></div>
    <div class="height-lineup__spacer" aria-hidden="true"></div>

    {''.join(figures)}
  </div>
</div>
"""


def generate_lineup(slugs: list[str]) -> pathlib.Path:
    characters = [load_character(s) for s in slugs]
    characters.sort(
        key=lambda c: int(get_nested(c, "physical", "height_cm", default=0) or 0),
        reverse=True,
    )

    title = "Height Lineup — " + ", ".join(c.get("name", c.get("slug", "Unknown")) for c in characters)

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a multi-character height lineup page.")
    parser.add_argument("slugs", nargs="+", help="Character slugs to include")
    args = parser.parse_args()

    try:
        output_file = generate_lineup(args.slugs)
        print(f"Generated lineup page: {output_file}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()