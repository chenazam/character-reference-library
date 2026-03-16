#!/usr/bin/env python3
"""
Generate a metadata-driven character height comparison page.

This generator:
- compares two characters by height and build metadata
- renders a markdown page
- includes optional paired asset comparison sections when matching assets exist
- includes fallback available-reference sections for unmatched assets
- updates MkDocs comparison nav automatically after generation
"""

import argparse
import pathlib
import subprocess
import sys

try:
    from tools.library_index import build_library_index
except ModuleNotFoundError:
    from library_index import build_library_index

try:
    from tools.site_paths import image_url_from_record
except ModuleNotFoundError:
    from site_paths import image_url_from_record


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "comparisons"
NAV_SCRIPT = ROOT / "tools" / "generate_nav_comparisons.py"

COMPARISON_ASSET_TYPES = [
    ("Body Anchor", "body_anchor"),
    ("Anatomy Sheet", "anatomy_sheet"),
    ("Silhouette Sheet", "silhouette_sheet"),
]


def load_library():
    return build_library_index()


def get_character_record(library: dict, slug: str) -> dict:
    for record in library.values():
        metadata = record.get("metadata") or {}
        if metadata.get("slug") == slug:
            return record
    raise ValueError(f"Could not find character with slug: {slug}")


def get_metadata(record: dict) -> dict:
    metadata = record.get("metadata") or {}
    if not metadata:
        raise ValueError(f"No metadata found for record: {record}")
    return metadata


def get_nested(data: dict, *keys, default=""):
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def cm_to_inches(cm: float) -> float:
    return cm / 2.54


def format_inches_as_feet_and_inches(total_inches: float) -> str:
    rounded = round(total_inches)
    feet = rounded // 12
    inches = rounded % 12
    return f"{feet}'{inches}\""


def prettify_value(value: str) -> str:
    if not value:
        return ""
    return str(value).replace("_", " ").title()


def format_list_as_phrase(values) -> str:
    if not values:
        return ""
    if isinstance(values, str):
        return values.replace("_", " ")
    cleaned = [str(v).replace("_", " ") for v in values if v]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"


def height_difference_summary(height_a: int, height_b: int) -> tuple[int, str]:
    diff_cm = abs(height_a - height_b)
    diff_label = format_inches_as_feet_and_inches(cm_to_inches(diff_cm))
    return diff_cm, diff_label


def ratio_summary(height_a: int, height_b: int) -> tuple[float, str]:
    taller = max(height_a, height_b)
    shorter = min(height_a, height_b)
    ratio = taller / shorter
    pct = (ratio - 1.0) * 100
    return ratio, f"{pct:.1f}%"


def difference_category(diff_cm: int) -> str:
    if diff_cm < 10:
        return "subtle"
    if diff_cm < 20:
        return "noticeable"
    if diff_cm < 30:
        return "dramatic"
    return "extreme"


def canonical_slug_pair(slug_a: str, slug_b: str) -> tuple[str, str]:
    return tuple(sorted([slug_a, slug_b]))


def comparison_page_docs_path(slug_a: str, slug_b: str) -> pathlib.Path:
    canon_a, canon_b = canonical_slug_pair(slug_a, slug_b)
    return OUTPUT_DIR / f"{canon_a}-vs-{canon_b}.md"


def make_image_link(record: dict, filename: str, page_docs_path: pathlib.Path) -> str:
    return image_url_from_record(record, filename, from_page_docs_path=page_docs_path)


def get_reference_links(record: dict, metadata: dict, page_docs_path: pathlib.Path) -> dict:
    refs = metadata.get("reference_files", {})
    return {
        "body_anchor": make_image_link(record, refs.get("body_anchor", ""), page_docs_path),
        "anatomy_sheet": make_image_link(record, refs.get("anatomy_sheet", ""), page_docs_path),
        "silhouette_sheet": make_image_link(record, refs.get("silhouette_sheet", ""), page_docs_path),
        "silhouette_front": make_image_link(record, refs.get("silhouette_front", ""), page_docs_path),
    }


def build_optional_section(
    title: str,
    char_a_name: str,
    char_a_link: str,
    char_b_name: str,
    char_b_link: str,
) -> str:
    if not char_a_link or not char_b_link:
        return ""

    return f"""## {title}

<div class="comparison-grid comparison-grid-2">
  <div class="comparison-item">
    <div class="comparison-label">{char_a_name}</div>
    <img src="{char_a_link}" alt="{char_a_name} {title}">
  </div>
  <div class="comparison-item">
    <div class="comparison-label">{char_b_name}</div>
    <img src="{char_b_link}" alt="{char_b_name} {title}">
  </div>
</div>

"""


def build_available_references_section(name_a: str, refs_a: dict, name_b: str, refs_b: dict) -> str:
    def item(label: str, link: str, char_name: str) -> str:
        if not link:
            return ""
        return f"""
  <div class="comparison-item">
    <div class="comparison-label">{char_name} — {label}</div>
    <img src="{link}" alt="{char_name} {label}">
  </div>"""

    items = []

    for label, key in COMPARISON_ASSET_TYPES:
        a_link = refs_a.get(key, "")
        b_link = refs_b.get(key, "")

        if a_link and b_link:
            continue

        if a_link:
            items.append(item(label, a_link, name_a))
        if b_link:
            items.append(item(label, b_link, name_b))

    if not items:
        return ""

    return (
        "## Available References\n\n"
        "<div class=\"comparison-grid comparison-grid-2\">\n"
        + "".join(items)
        + "\n</div>\n\n"
    )


def build_height_chart_section(
    name_a: str,
    height_a: int,
    imperial_a: str,
    silhouette_front_a: str,
    name_b: str,
    height_b: int,
    imperial_b: str,
    silhouette_front_b: str,
) -> str:
    max_height = max(height_a, height_b)
    if max_height <= 0:
        return ""

    def pct(height: int) -> float:
        return (height / max_height) * 100

    a_pct = pct(height_a)
    b_pct = pct(height_b)

    use_silhouettes = bool(silhouette_front_a and silhouette_front_b)

    if use_silhouettes:
        figure_a = (
            f'<img class="height-lineup__silhouette" '
            f'src="{silhouette_front_a}" '
            f'alt="{name_a} silhouette front" '
            f'style="height: {a_pct:.2f}%;">'
        )
        figure_b = (
            f'<img class="height-lineup__silhouette" '
            f'src="{silhouette_front_b}" '
            f'alt="{name_b} silhouette front" '
            f'style="height: {b_pct:.2f}%;">'
        )
    else:
        figure_a = f'<div class="height-lineup__placeholder" style="height: {a_pct:.2f}%"></div>'
        figure_b = f'<div class="height-lineup__placeholder" style="height: {b_pct:.2f}%"></div>'

    return f"""## Visual Height Chart

<div class="height-lineup">
  <div class="height-lineup__figure">
    <div class="height-lineup__stage">
      {figure_a}
    </div>
    <div class="height-lineup__label">{name_a}</div>
    <div class="height-lineup__meta">{height_a} cm / {imperial_a}</div>
  </div>

  <div class="height-lineup__figure">
    <div class="height-lineup__stage">
      {figure_b}
    </div>
    <div class="height-lineup__label">{name_b}</div>
    <div class="height-lineup__meta">{height_b} cm / {imperial_b}</div>
  </div>
</div>

"""


def build_difference_badges(meta_a: dict, meta_b: dict, diff_category: str) -> str:
    build_a = prettify_value(get_nested(meta_a, "physical", "build_category", default=""))
    build_b = prettify_value(get_nested(meta_b, "physical", "build_category", default=""))

    silhouette_a = prettify_value(get_nested(meta_a, "physical", "silhouette_anchor", default=""))
    silhouette_b = prettify_value(get_nested(meta_b, "physical", "silhouette_anchor", default=""))

    return f"""<div class="comparison-badges">
  <div class="comparison-badge">
    <div class="comparison-badge__label">Height Contrast</div>
    <div class="comparison-badge__value">{prettify_value(diff_category)}</div>
  </div>
  <div class="comparison-badge">
    <div class="comparison-badge__label">Build Contrast</div>
    <div class="comparison-badge__value">{build_a} vs {build_b}</div>
  </div>
  <div class="comparison-badge">
    <div class="comparison-badge__label">Silhouette Contrast</div>
    <div class="comparison-badge__value">{silhouette_a} vs {silhouette_b}</div>
  </div>
</div>

"""


def build_comparison_summary(
    meta_a: dict,
    meta_b: dict,
    diff_cm: int,
    diff_category: str,
    taller_name: str,
    shorter_name: str,
    refs_a: dict,
    refs_b: dict,
) -> str:
    name_a = meta_a["name"]
    name_b = meta_b["name"]

    build_a = prettify_value(get_nested(meta_a, "physical", "build_category", default=""))
    build_b = prettify_value(get_nested(meta_b, "physical", "build_category", default=""))

    anchor_a = prettify_value(get_nested(meta_a, "physical", "silhouette_anchor", default=""))
    anchor_b = prettify_value(get_nested(meta_b, "physical", "silhouette_anchor", default=""))

    emphasis_a = prettify_value(get_nested(meta_a, "physical", "silhouette_emphasis", default=""))
    emphasis_b = prettify_value(get_nested(meta_b, "physical", "silhouette_emphasis", default=""))

    keywords_a = format_list_as_phrase(get_nested(meta_a, "physical", "silhouette_keywords", default=[]))
    keywords_b = format_list_as_phrase(get_nested(meta_b, "physical", "silhouette_keywords", default=[]))

    aesthetic_a = prettify_value(get_nested(meta_a, "style", "primary_aesthetic", default=""))
    aesthetic_b = prettify_value(get_nested(meta_b, "style", "primary_aesthetic", default=""))

    movement_a = prettify_value(get_nested(meta_a, "movement", "movement_style", default=""))
    movement_b = prettify_value(get_nested(meta_b, "movement", "movement_style", default=""))

    body_language_a = prettify_value(get_nested(meta_a, "movement", "body_language", default=""))
    body_language_b = prettify_value(get_nested(meta_b, "movement", "body_language", default=""))

    expression_a = prettify_value(get_nested(meta_a, "expression", "default_expression", default=""))
    expression_b = prettify_value(get_nested(meta_b, "expression", "default_expression", default=""))

    emotional_tone_a = prettify_value(get_nested(meta_a, "expression", "emotional_tone", default=""))
    emotional_tone_b = prettify_value(get_nested(meta_b, "expression", "emotional_tone", default=""))

    sentences = []

    sentences.append(
        f"**{name_a}** and **{name_b}** show a **{prettify_value(diff_category)} height contrast**, "
        f"with **{taller_name}** standing **{diff_cm} cm** taller than **{shorter_name}**."
    )

    if build_a and build_b:
        sentences.append(
            f"In terms of build, **{name_a}** reads as **{build_a}**, while **{name_b}** reads as **{build_b}**."
        )

    silhouettes_exist = bool(refs_a.get("silhouette_sheet") and refs_b.get("silhouette_sheet"))
    if silhouettes_exist and anchor_a and anchor_b:
        silhouette_sentence = (
            f"Their silhouettes reinforce this contrast: "
            f"**{name_a}** has a **{anchor_a} silhouette"
        )

        if emphasis_a:
            silhouette_sentence += f" with **{emphasis_a} emphasis**"
        if keywords_a:
            silhouette_sentence += f", characterized by {keywords_a}"

        silhouette_sentence += ", while "

        silhouette_sentence += f"**{name_b}** presents a **{anchor_b} silhouette"
        if emphasis_b:
            silhouette_sentence += f" with **{emphasis_b} emphasis**"
        if keywords_b:
            silhouette_sentence += f", characterized by {keywords_b}"

        silhouette_sentence += "."
        sentences.append(silhouette_sentence)

    if aesthetic_a and aesthetic_b and aesthetic_a != aesthetic_b:
        sentences.append(
            f"Their design language also differs strongly: **{name_a}** is rooted in a **{aesthetic_a}** aesthetic, "
            f"while **{name_b}** is defined more by **{aesthetic_b}** styling."
        )

    if movement_a and movement_b and movement_a != movement_b:
        sentences.append(
            f"In motion, **{name_a}** reads as **{movement_a}**, whereas **{name_b}** feels more **{movement_b}**."
        )

    if body_language_a and body_language_b and body_language_a != body_language_b:
        sentences.append(
            f"Their body language pushes this contrast further: **{name_a}** appears **{body_language_a}**, "
            f"while **{name_b}** appears **{body_language_b}**."
        )

    if expression_a and expression_b and expression_a != expression_b:
        sentences.append(
            f"Facially, **{name_a}** tends toward a **{expression_a}** expression, while **{name_b}** reads as more **{expression_b}**."
        )

    if emotional_tone_a and emotional_tone_b and emotional_tone_a != emotional_tone_b:
        sentences.append(
            f"Their emotional presentation also differs: **{name_a}** feels **{emotional_tone_a}**, while **{name_b}** feels **{emotional_tone_b}**."
        )

    return "## Comparison Summary\n\n" + "\n\n".join(sentences) + "\n\n"


def build_markdown(
    meta_a: dict,
    meta_b: dict,
    record_a: dict,
    record_b: dict,
    page_docs_path: pathlib.Path,
) -> str:
    name_a = meta_a["name"]
    name_b = meta_b["name"]

    height_a = int(get_nested(meta_a, "physical", "height_cm", default=0))
    height_b = int(get_nested(meta_b, "physical", "height_cm", default=0))

    imperial_a = get_nested(meta_a, "physical", "height_imperial", default="")
    imperial_b = get_nested(meta_b, "physical", "height_imperial", default="")

    diff_cm, diff_label = height_difference_summary(height_a, height_b)
    _, pct_label = ratio_summary(height_a, height_b)
    diff_category = difference_category(diff_cm)

    taller_name = name_a if height_a > height_b else name_b
    shorter_name = name_b if height_a > height_b else name_a

    refs_a = get_reference_links(record_a, meta_a, page_docs_path)
    refs_b = get_reference_links(record_b, meta_b, page_docs_path)

    difference_badges_section = build_difference_badges(meta_a, meta_b, diff_category)

    height_chart_section = build_height_chart_section(
        name_a,
        height_a,
        imperial_a,
        refs_a.get("silhouette_front", ""),
        name_b,
        height_b,
        imperial_b,
        refs_b.get("silhouette_front", ""),
    )

    comparison_summary_section = build_comparison_summary(
        meta_a,
        meta_b,
        diff_cm,
        diff_category,
        taller_name,
        shorter_name,
        refs_a,
        refs_b,
    )

    body_section = build_optional_section(
        "Body Anchor Comparison",
        name_a, refs_a["body_anchor"],
        name_b, refs_b["body_anchor"],
    )
    anatomy_section = build_optional_section(
        "Anatomy Sheet Comparison",
        name_a, refs_a["anatomy_sheet"],
        name_b, refs_b["anatomy_sheet"],
    )
    silhouette_section = build_optional_section(
        "Silhouette Sheet Comparison",
        name_a, refs_a["silhouette_sheet"],
        name_b, refs_b["silhouette_sheet"],
    )
    available_references_section = build_available_references_section(
        name_a, refs_a, name_b, refs_b
    )

    return f"""# {name_a} vs {name_b}

## Height Comparison

- **{name_a}:** {height_a} cm / {imperial_a}
- **{name_b}:** {height_b} cm / {imperial_b}
- **Difference:** {diff_cm} cm / {diff_label}
- **Category:** {diff_category}
- **Relative scale:** {taller_name} is approximately {pct_label} taller than {shorter_name}

{difference_badges_section}{height_chart_section}{comparison_summary_section}{body_section}{anatomy_section}{silhouette_section}{available_references_section}"""


def write_output(page_docs_path: pathlib.Path, markdown: str) -> pathlib.Path:
    page_docs_path.parent.mkdir(parents=True, exist_ok=True)
    page_docs_path.write_text(markdown, encoding="utf-8")
    return page_docs_path


def update_comparison_nav() -> None:
    if not NAV_SCRIPT.exists():
        print(f"Warning: comparison nav script not found: {NAV_SCRIPT}")
        return

    result = subprocess.run(
        [sys.executable, str(NAV_SCRIPT)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Warning: failed to update comparison nav.")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return

    if result.stdout:
        print(result.stdout.strip())


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a metadata-driven height comparison page."
    )
    parser.add_argument("slug_a", help="Slug of the first character")
    parser.add_argument("slug_b", help="Slug of the second character")
    parser.add_argument(
        "--no-nav-update",
        action="store_true",
        help="Do not update comparison nav after generating the page.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    library = load_library()

    canon_a, canon_b = canonical_slug_pair(args.slug_a, args.slug_b)
    if (args.slug_a, args.slug_b) != (canon_a, canon_b):
        print(f"Note: using canonical comparison filename order: {canon_a}-vs-{canon_b}.md")

    record_a = get_character_record(library, args.slug_a)
    record_b = get_character_record(library, args.slug_b)

    meta_a = get_metadata(record_a)
    meta_b = get_metadata(record_b)

    page_docs_path = comparison_page_docs_path(args.slug_a, args.slug_b)
    markdown = build_markdown(meta_a, meta_b, record_a, record_b, page_docs_path)
    output_path = write_output(page_docs_path, markdown)

    print(f"Generated comparison page: {output_path}")
    if not args.no_nav_update:
        update_comparison_nav()


if __name__ == "__main__":
    main()
