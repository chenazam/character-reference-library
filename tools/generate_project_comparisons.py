#!/usr/bin/env python3
"""
Generate missing height comparison pages for characters that share the same project.

This script:
- reads character metadata from the library index
- groups characters by project
- generates missing comparison pages for all unique pairs within each project
- skips pages that already exist
- does not update comparison nav itself; the pipeline should run
  generate_nav_comparisons.py --refresh-pages afterward
"""

import pathlib
import subprocess
import sys
from collections import defaultdict

try:
    from tools.library_index import build_library_index
except ModuleNotFoundError:
    from library_index import build_library_index


ROOT = pathlib.Path(__file__).resolve().parents[1]
COMPARISON_DIR = ROOT / "docs" / "comparisons"
HEIGHT_GENERATOR = ROOT / "tools" / "generate_height_comparison.py"


def canonical_slug_pair(slug_a: str, slug_b: str) -> tuple[str, str]:
    return tuple(sorted([slug_a, slug_b]))


def comparison_path_for(slug_a: str, slug_b: str) -> pathlib.Path:
    canon_a, canon_b = canonical_slug_pair(slug_a, slug_b)
    return COMPARISON_DIR / f"{canon_a}-vs-{canon_b}.md"


def load_project_groups() -> dict[str, list[dict]]:
    library = build_library_index()
    groups: dict[str, list[dict]] = defaultdict(list)

    for record in library.values():
        metadata = record.get("metadata") or {}
        slug = metadata.get("slug")
        project = metadata.get("project")

        if not slug or not project:
            continue

        groups[project].append(record)

    return groups


def eligible_slug(record: dict) -> str | None:
    metadata = record.get("metadata") or {}

    if metadata.get("exclude_from_comparisons", False):
        return None

    slug = metadata.get("slug")
    if not slug:
        return None

    return slug


def generate_missing_comparison(slug_a: str, slug_b: str) -> bool:
    if not HEIGHT_GENERATOR.exists():
        raise FileNotFoundError(f"Height comparison generator not found: {HEIGHT_GENERATOR}")

    output_path = comparison_path_for(slug_a, slug_b)
    if output_path.exists():
        return False

    result = subprocess.run(
        [sys.executable, str(HEIGHT_GENERATOR), slug_a, slug_b, "--no-nav-update"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Warning: failed to generate comparison for {slug_a} vs {slug_b}")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return False

    if result.stdout.strip():
        print(result.stdout.strip())

    return True


def main():
    COMPARISON_DIR.mkdir(parents=True, exist_ok=True)

    project_groups = load_project_groups()
    generated_count = 0
    skipped_existing = 0
    skipped_small_groups = 0

    print("\n===== GENERATING PROJECT COMPARISONS =====\n")

    for project, records in sorted(project_groups.items()):
        eligible_records = []
        for r in records:
            slug = eligible_slug(r)
            if slug:
                eligible_records.append(r)
            else:
                name = (r.get("metadata") or {}).get("name", "unknown")
                print(f"Skipping {name} (exclude_from_comparisons=true)")

        eligible_records.sort(key=lambda r: (r.get("metadata") or {}).get("slug", ""))

        if len(eligible_records) < 2:
            skipped_small_groups += 1
            continue

        print(f"\n--- Project: {project} ({len(eligible_records)} character(s)) ---")

        for i in range(len(eligible_records)):
            for j in range(i + 1, len(eligible_records)):
                slug_a = eligible_slug(eligible_records[i])
                slug_b = eligible_slug(eligible_records[j])

                if not slug_a or not slug_b:
                    continue

                output_path = comparison_path_for(slug_a, slug_b)
                if output_path.exists():
                    skipped_existing += 1
                    print(f"Skipping existing: {output_path.name}")
                    continue

                created = generate_missing_comparison(slug_a, slug_b)
                if created:
                    generated_count += 1

    print("\n===== PROJECT COMPARISON GENERATION COMPLETE =====")
    print(f"Generated new comparison pages: {generated_count}")
    print(f"Skipped existing comparison pages: {skipped_existing}")
    print(f"Projects with fewer than 2 eligible characters: {skipped_small_groups}\n")


if __name__ == "__main__":
    main()
