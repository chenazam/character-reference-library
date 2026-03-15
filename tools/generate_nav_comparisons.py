#!/usr/bin/env python3
"""
Generate the Comparison Pages navigation section in mkdocs.yml.

This script scans docs/comparisons for markdown pages and rewrites the
'Comparison Pages' subsection under 'Browse Library' in mkdocs.yml.
"""

import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

MKDOCS_FILE = ROOT / "mkdocs.yml"
COMPARISON_PAGES = ROOT / "docs" / "comparisons"

# Optional static pages that should appear first if they exist
STATIC_COMPARISON_PAGES = {
    "assets.md": "Asset Comparison",
    "index.md": "Index",
    "templates.md": "Templates",
}


def display_name_for_slug(slug: str) -> str:
    parts = slug.replace("_", "-").split("-vs-")
    if len(parts) == 2:
        left = parts[0].replace("-", " ").title()
        right = parts[1].replace("-", " ").title()
        return f"{left} vs {right}"
    return slug.replace("-", " ").replace("_", " ").title()


def build_comparison_entries() -> list[dict]:
    entries = []

    # Static pages first
    for filename, title in STATIC_COMPARISON_PAGES.items():
        page = COMPARISON_PAGES / filename
        if page.exists():
            entries.append({title: f"comparisons/{filename}"})

    # Then generated comparison pages
    pages = [
        p for p in COMPARISON_PAGES.glob("*.md")
        if p.name not in STATIC_COMPARISON_PAGES
    ]

    pages.sort(key=lambda p: display_name_for_slug(p.stem))

    for page in pages:
        entries.append({display_name_for_slug(page.stem): f"comparisons/{page.name}"})

    return entries


def find_nav_section(nav_list: list, key: str):
    for item in nav_list:
        if isinstance(item, dict) and key in item:
            return item[key]
    return None


def main():
    if not MKDOCS_FILE.exists():
        raise FileNotFoundError(f"mkdocs.yml not found: {MKDOCS_FILE}")

    if not COMPARISON_PAGES.exists():
        raise FileNotFoundError(f"Comparison pages folder not found: {COMPARISON_PAGES}")

    with MKDOCS_FILE.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav")
    if not isinstance(nav, list):
        raise RuntimeError("mkdocs.yml does not contain a valid 'nav' list")

    browse_library = find_nav_section(nav, "Browse Library")
    if not isinstance(browse_library, list):
        raise RuntimeError("Could not find 'Browse Library' section in mkdocs.yml")

    comparison_pages = find_nav_section(browse_library, "Comparison Pages")
    if not isinstance(comparison_pages, list):
        raise RuntimeError(
            "Could not find 'Comparison Pages' section under 'Browse Library' in mkdocs.yml"
        )

    new_entries = build_comparison_entries()

    comparison_pages.clear()
    comparison_pages.extend(new_entries)

    with MKDOCS_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False, allow_unicode=True)

    print("Updated Comparison Pages nav in mkdocs.yml")
    for entry in new_entries:
        print(entry)


if __name__ == "__main__":
    main()
