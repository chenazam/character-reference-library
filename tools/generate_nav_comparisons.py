#!/usr/bin/env python3
"""
Generate the Comparison Pages navigation section in mkdocs.yml.

Optional:
- refresh all existing generated height comparison pages before updating nav
"""

import argparse
import pathlib
import subprocess
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

MKDOCS_FILE = ROOT / "mkdocs.yml"
COMPARISON_PAGES = ROOT / "docs" / "comparisons"
HEIGHT_GENERATOR = ROOT / "tools" / "generate_height_comparison.py"
LINEUP_GENERATOR = ROOT / "tools" / "generate_height_lineup.py"
LINEUPS_DIR = COMPARISON_PAGES / "lineups"

# Optional static pages that should appear first if they exist
STATIC_COMPARISON_PAGES = {
    "assets.md": "Asset Comparison",
    "index.md": "Index",
    "templates.md": "Templates",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Update comparison nav in mkdocs.yml."
    )
    parser.add_argument(
        "--refresh-pages",
        action="store_true",
        help="Regenerate all existing comparison and lineup pages before updating nav.",
    )
    return parser.parse_args()


def display_name_for_slug(slug: str) -> str:
    parts = slug.replace("_", "-").split("-vs-")
    if len(parts) == 2:
        left = parts[0].replace("-", " ").title()
        right = parts[1].replace("-", " ").title()
        return f"{left} vs {right}"
    return slug.replace("-", " ").replace("_", " ").title()


def comparison_slug_pairs():
    pages = [
        p for p in COMPARISON_PAGES.glob("*.md")
        if p.name not in STATIC_COMPARISON_PAGES
    ]

    for page in pages:
        stem = page.stem.replace("_", "-")
        if "-vs-" not in stem:
            continue
        left, right = stem.split("-vs-", 1)
        if left and right:
            yield left, right, page


def lineup_slug_groups():
    if not LINEUPS_DIR.exists():
        return

    pages = sorted(
        p for p in LINEUPS_DIR.glob("*.md")
        if p.name != "index.md"
    )

    for page in pages:
        stem = page.stem.replace("_", "-")
        if not stem.endswith("-lineup"):
            continue

        slug_part = stem[:-len("-lineup")]
        slugs = [part for part in slug_part.split("-") if part]

        if slugs:
            yield slugs, page


def refresh_existing_comparison_pages():
    if not HEIGHT_GENERATOR.exists():
        raise FileNotFoundError(f"Height comparison generator not found: {HEIGHT_GENERATOR}")

    refreshed = []

    for left, right, page in sorted(comparison_slug_pairs(), key=lambda item: item[2].name):
        result = subprocess.run(
            [sys.executable, str(HEIGHT_GENERATOR), left, right, "--no-nav-update"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"Warning: failed to refresh comparison page for {left} vs {right}")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            continue

        refreshed.append((left, right))
        if result.stdout.strip():
            print(result.stdout.strip())

    return refreshed


def refresh_existing_lineup_pages():
    if not LINEUP_GENERATOR.exists():
        raise FileNotFoundError(f"Height lineup generator not found: {LINEUP_GENERATOR}")

    refreshed = []

    for slugs, page in lineup_slug_groups():
        result = subprocess.run(
            [sys.executable, str(LINEUP_GENERATOR), *slugs],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"Warning: failed to refresh lineup page for {' / '.join(slugs)}")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            continue

        refreshed.append((slugs, page))
        if result.stdout.strip():
            print(result.stdout.strip())

    return refreshed


def build_lineup_entries() -> list[dict]:
    lineups_dir = COMPARISON_PAGES / "lineups"
    if not lineups_dir.exists():
        return []

    pages = sorted(lineups_dir.glob("*.md"), key=lambda p: p.stem)

    entries = []
    for page in pages:
        label = page.stem.replace("-", " ").replace("_", " ").title()
        label = label.replace(" Lineup", "")
        entries.append({label: f"comparisons/lineups/{page.name}"})

    return entries


def build_comparison_entries() -> list[dict]:
    entries = []

    # Static pages first
    for filename, title in STATIC_COMPARISON_PAGES.items():
        page = COMPARISON_PAGES / filename
        if page.exists():
            entries.append({title: f"comparisons/{filename}"})

    # Regular comparison pages
    pages = [
        p for p in COMPARISON_PAGES.glob("*.md")
        if p.name not in STATIC_COMPARISON_PAGES
    ]

    pages.sort(key=lambda p: display_name_for_slug(p.stem))

    for page in pages:
        entries.append({display_name_for_slug(page.stem): f"comparisons/{page.name}"})

    # Lineups subsection
    lineup_entries = build_lineup_entries()
    if lineup_entries:
        entries.append({"Lineups": lineup_entries})

    return entries


def find_nav_section(nav_list: list, key: str):
    for item in nav_list:
        if isinstance(item, dict) and key in item:
            return item[key]
    return None


def update_nav():
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


def main():
    args = parse_args()

    if args.refresh_pages:
        refreshed_comparisons = refresh_existing_comparison_pages()
        print(f"Refreshed {len(refreshed_comparisons)} comparison page(s).")

        refreshed_lineups = refresh_existing_lineup_pages()
        print(f"Refreshed {len(refreshed_lineups)} lineup page(s).")

    update_nav()


if __name__ == "__main__":
    main()
