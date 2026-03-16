#!/usr/bin/env python3

import argparse
import pathlib
import sys
import yaml

try:
    from tools.site_paths import image_url_from_record
except ModuleNotFoundError:
    from site_paths import image_url_from_record


ROOT = pathlib.Path(__file__).resolve().parents[1]
LIBRARY_ROOT = ROOT / "docs" / "assets" / "library" / "10_CHARACTERS"
OUTPUT_ROOT = ROOT / "docs" / "comparisons" / "lineups"

CHART_HEIGHT_PX = 460


def get_nested(d, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default


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


def fallback_archetype(meta: dict) -> str:
    anchor = get_nested(meta, "physical", "silhouette_anchor", default="")
    build = get_nested(meta, "physical", "build_category", default="")
    keywords = get_nested(meta, "physical", "silhouette_keywords", default=[]) or []

    if anchor in {"power_frame"}:
        return "massive"

    if anchor in {"power_athlete"}:
        return "broad"

    if anchor in {"runner_silhouette"}:
        return "athletic"

    if anchor in {"elongated_slender", "glute_slender"}:
        return "slender"

    if build in {"power_build", "heavy_muscular", "broad_heavy", "thick_set", "large_frame"}:
        return "massive"

    if build in {"athletic_muscular"}:
        return "broad"

    if build in {"balanced_athletic", "runner_build", "lower_athletic", "light_athletic"}:
        return "athletic"

    if build in {"soft_slender", "narrow_slender", "elongated_slender"}:
        return "slender"

    if "heavy_set" in keywords or "imposing" in keywords:
        return "massive"

    if "broad" in keywords or "upper_dominant" in keywords:
        return "broad"

    if "agile" in keywords or "leg_dominant" in keywords:
        return "athletic"

    return "slender"


def find_asset(meta: dict, key: str, page_docs_path: pathlib.Path) -> str:
    refs = meta.get("reference_files", {})
    filename = refs.get(key, "")
    if not filename:
        return ""

    record = {"dir": str(meta["_dir"])}
    return image_url_from_record(record, filename, from_page_docs_path=page_docs_path)


def build_chart(characters: list[dict], page_docs_path: pathlib.Path) -> str:
    reference_height = 180
    reference_imperial = "5'11\""

    max_height = max(max(c["physical"]["height_cm"] for c in characters), reference_height)

    def pct(h: int) -> float:
        return (h / max_height) * 100

    def tick_px(cm: int) -> float:
        return (cm / max_height) * CHART_HEIGHT_PX

    tick_step = 10
    tick_start = (max_height // tick_step) * tick_step

    ticks = []
    for t in range(tick_start, 0, -tick_step):
        ticks.append(
            f'<div class="height-lineup__tick" style="bottom: {tick_px(t):.2f}px;">'
            f'<span class="height-lineup__tick-label">{t} cm</span></div>'
        )

    reference_figure = (
        f'<div class="height-lineup__placeholder '
        f'height-lineup__placeholder--athletic '
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

    for c in characters:
        name = c["name"]
        height = c["physical"]["height_cm"]
        imperial = c["physical"]["height_imperial"]

        silhouette = find_asset(c, "silhouette_front", page_docs_path)
        archetype = fallback_archetype(c)

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

    return f"""
<div class="height-lineup height-lineup--multi">

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

    chart = build_chart(characters, output_file)

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
