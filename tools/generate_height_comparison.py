#!/usr/bin/env python3

import argparse
import math
import pathlib
import yaml

try:
    from tools.library_index import build_library_index
except ModuleNotFoundError:
    from library_index import build_library_index


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "docs" / "characters" / "comparisons"


def load_library():
    return build_library_index()


def get_character_record(library: dict, slug: str) -> dict:
    for _, record in library.items():
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


def height_difference_summary(height_a: int, height_b: int) -> tuple[int, float, str]:
    diff_cm = abs(height_a - height_b)
    diff_in = cm_to_inches(diff_cm)
    diff_label = format_inches_as_feet_and_inches(diff_in)
    return diff_cm, diff_in, diff_label


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


def make_image_link(record: dict, filename: str) -> str:
    if not filename:
        return ""
    character_dir = pathlib.Path(record["dir"])
    candidate = character_dir / filename
    if candidate.exists():
        rel = candidate.relative_to(ROOT / "docs")
        return f"/{rel.as_posix()}"
    return ""


def get_reference_links(record: dict, metadata: dict) -> dict:
    refs = metadata.get("reference_files", {})
    return {
        "body_anchor": make_image_link(record, refs.get("body_anchor", "")),
        "anatomy_sheet": make_image_link(record, refs.get("anatomy_sheet", "")),
        "silhouette_sheet": make_image_link(record, refs.get("silhouette_sheet", "")),
    }


def build_identity_summary(metadata: dict) -> str:
    build_category = get_nested(metadata, "physical", "build_category", default="")
    silhouette_anchor = get_nested(metadata, "physical", "silhouette_anchor", default="")
    silhouette_emphasis = get_nested(metadata, "physical", "silhouette_emphasis", default="")
    silhouette_keywords = get_nested(metadata, "physical", "silhouette_keywords", default=[]) or []

    parts = []
    if build_category:
        parts.append(build_category)
    if silhouette_anchor:
        parts.append(silhouette_anchor)
    if silhouette_emphasis:
        parts.append(f"{silhouette_emphasis}-emphasis")
    if silhouette_keywords:
        parts.append(", ".join(silhouette_keywords))

    return " | ".join(parts) if parts else "No additional build metadata available."


def build_optional_section(title: str, char_a_name: str, char_a_link: str, char_b_name: str, char_b_link: str) -> str:
    if not char_a_link or not char_b_link:
        return ""

    return f"""## {title}

**{char_a_name}**  
![{char_a_name} {title}]({char_a_link})

**{char_b_name}**  
![{char_b_name} {title}]({char_b_link})

"""


def build_markdown(meta_a: dict, meta_b: dict, record_a: dict, record_b: dict) -> str:
    name_a = meta_a["name"]
    name_b = meta_b["name"]

    height_a = int(get_nested(meta_a, "physical", "height_cm", default=0))
    height_b = int(get_nested(meta_b, "physical", "height_cm", default=0))

    imperial_a = get_nested(meta_a, "physical", "height_imperial", default="")
    imperial_b = get_nested(meta_b, "physical", "height_imperial", default="")

    diff_cm, diff_in, diff_label = height_difference_summary(height_a, height_b)
    _, pct_label = ratio_summary(height_a, height_b)
    diff_category = difference_category(diff_cm)

    taller_name = name_a if height_a > height_b else name_b
    shorter_name = name_b if height_a > height_b else name_a

    summary_a = build_identity_summary(meta_a)
    summary_b = build_identity_summary(meta_b)

    refs_a = get_reference_links(record_a, meta_a)
    refs_b = get_reference_links(record_b, meta_b)

    body_section = build_optional_section("Body Anchor Comparison", name_a, refs_a["body_anchor"], name_b, refs_b["body_anchor"])
    anatomy_section = build_optional_section("Anatomy Sheet Comparison", name_a, refs_a["anatomy_sheet"], name_b, refs_b["anatomy_sheet"])
    silhouette_section = build_optional_section("Silhouette Comparison", name_a, refs_a["silhouette_sheet"], name_b, refs_b["silhouette_sheet"])

    return f"""# {name_a} vs {name_b}

## Height Comparison

- **{name_a}:** {height_a} cm / {imperial_a}
- **{name_b}:** {height_b} cm / {imperial_b}
- **Difference:** {diff_cm} cm / {diff_label}
- **Category:** {diff_category}
- **Relative scale:** {taller_name} is approximately {pct_label} taller than {shorter_name}

## Physical Contrast

### {name_a}
{summary_a}

### {name_b}
{summary_b}

{body_section}{anatomy_section}{silhouette_section}"""
    

def write_output(slug_a: str, slug_b: str, markdown: str) -> pathlib.Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slug_a}-vs-{slug_b}.md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(description="Generate a simple metadata-driven height comparison page.")
    parser.add_argument("slug_a", help="Slug of the first character")
    parser.add_argument("slug_b", help="Slug of the second character")
    return parser.parse_args()


def main():
    args = parse_args()
    library = load_library()

    record_a = get_character_record(library, args.slug_a)
    record_b = get_character_record(library, args.slug_b)

    meta_a = get_metadata(record_a)
    meta_b = get_metadata(record_b)

    markdown = build_markdown(meta_a, meta_b, record_a, record_b)
    output_path = write_output(args.slug_a, args.slug_b, markdown)

    print(f"Generated comparison page: {output_path}")


if __name__ == "__main__":
    main()
