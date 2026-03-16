import argparse
import pathlib
import yaml

from site_paths import site_root_url

LIBRARY_ROOT = pathlib.Path("assets/library/10_CHARACTERS")
OUTPUT_ROOT = pathlib.Path("docs/comparisons/lineups")

CHART_HEIGHT_PX = 460

reference_height = 180
reference_imperial = "5'11\""


def load_character(slug: str) -> dict:
    for char_dir in LIBRARY_ROOT.iterdir():
        meta_file = char_dir / "metadata.yaml"
        if not meta_file.exists():
            continue

        meta = yaml.safe_load(meta_file.read_text())
        if meta.get("slug") == slug:
            meta["_dir"] = char_dir
            return meta

    raise ValueError(f"Character not found for slug: {slug}")


def get_nested(d, *keys, default=None):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
    return cur if cur is not None else default


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

    if build in {"power_build", "heavy_muscular", "broad_heavy", "large_frame"}:
        return "massive"

    if build in {"athletic_muscular"}:
        return "broad"

    if build in {"balanced_athletic", "runner_build", "light_athletic"}:
        return "athletic"

    if build in {"soft_slender", "narrow_slender"}:
        return "slender"

    if "heavy_set" in keywords or "imposing" in keywords:
        return "massive"

    if "broad" in keywords:
        return "broad"

    if "agile" in keywords or "leg_dominant" in keywords:
        return "athletic"

    return "slender"


def find_asset(meta: dict, key: str) -> str:
    refs = meta.get("reference_files", {})
    filename = refs.get(key)

    if not filename:
        return ""

    char_dir = meta["_dir"]
    matches = list(char_dir.rglob(filename))
    if not matches:
        return ""

    return site_root_url(matches[0])


def build_chart(characters: list) -> str:
    max_height = max(max(c["height_cm"] for c in characters), 180)

    def pct(h):
        return (h / max_height) * 100

    def tick_px(cm):
        return (cm / max_height) * CHART_HEIGHT_PX

    tick_step = 10
    tick_start = (max_height // tick_step) * tick_step

    ticks = []
    for t in range(tick_start, 0, -tick_step):
        ticks.append(
            f'<div class="height-lineup__tick" style="bottom:{tick_px(t):.2f}px;">'
            f'<span class="height-lineup__tick-label">{t} cm</span></div>'
        )

    reference_figure = (
    f'<div class="height-lineup__placeholder '
    f'height-lineup__placeholder--athletic '
    f'height-lineup__placeholder--reference" '
    f'style="height:{pct(reference_height):.2f}%"></div>'
)

    figures = [
        f"""
    <div class="height-lineup__figure height-lineup__figure--ref">
      <div class="height-lineup__stage">
        {reference_figure}
      </div>
      <div class="height-lineup__label">Reference</div>
      <div class="height-lineup__meta">{reference_height} cm / {reference_imperial}</div>
    </div>
    """
    ]

    for i, c in enumerate(characters):
        name = c["name"]
        height = c["height_cm"]
        imperial = c["height_imperial"]

        silhouette = find_asset(c, "silhouette_front")
        archetype = fallback_archetype(c)

        if silhouette:
            body = (
                f'<img class="height-lineup__silhouette" '
                f'src="{silhouette}" '
                f'alt="{name} silhouette" '
                f'style="height:{pct(height):.2f}%;">'
            )
        else:
            body = (
                f'<div class="height-lineup__placeholder '
                f'height-lineup__placeholder--{archetype}" '
                f'style="height:{pct(height):.2f}%"></div>'
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

  <div class="height-lineup__ticks">
    {"".join(ticks)}
  </div>

  <div class="height-lineup__baseline"></div>

  {"".join(figures)}

</div>
"""


def generate_lineup(slugs: list):
    characters = [load_character(s) for s in slugs]

    characters.sort(key=lambda c: c["height_cm"], reverse=True)

    title = "Height Lineup — " + ", ".join(c["name"] for c in characters)

    chart = build_chart(characters)

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    filename = "-".join(sorted(slugs)) + "-lineup.md"
    output_file = OUTPUT_ROOT / filename

    markdown = f"""---
hide:
  - toc
---

# {title}

{chart}
"""

    output_file.write_text(markdown, encoding="utf-8")

    print("Generated lineup page:", output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slugs", nargs="+")
    args = parser.parse_args()

    generate_lineup(args.slugs)


if __name__ == "__main__":
    main()
