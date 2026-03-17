#!/usr/bin/env python3

import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
LINEUPS_DIR = ROOT / "docs" / "comparisons" / "lineups"
GENERATOR = ROOT / "tools" / "generate_height_lineup.py"


def parse_lineup_filename(path: pathlib.Path) -> list[str]:
    """
    Convert a filename like:
        danny-hudson-jonah-luca-lineup.md
    into:
        ["danny", "hudson", "jonah", "luca"]
    """
    stem = path.stem

    if not stem.endswith("-lineup"):
        raise ValueError(f"Not a lineup filename: {path.name}")

    slug_part = stem[:-len("-lineup")]

    if not slug_part:
        raise ValueError(f"No slugs found in lineup filename: {path.name}")

    slugs = [part for part in slug_part.split("-") if part]
    if not slugs:
        raise ValueError(f"No valid slugs parsed from: {path.name}")

    return slugs


def refresh_lineup(path: pathlib.Path) -> bool:
    try:
        slugs = parse_lineup_filename(path)
    except ValueError as e:
        print(f"Skipping {path.name}: {e}")
        return False

    cmd = [sys.executable, str(GENERATOR), *slugs]

    print(f"Refreshing lineup: {path.name} -> {' '.join(slugs)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR refreshing {path.name}")
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        return False

    if result.stdout:
        print(result.stdout.strip())

    return True


def main():
    if not LINEUPS_DIR.exists():
        print(f"No lineup directory found: {LINEUPS_DIR}")
        return

    if not GENERATOR.exists():
        print(f"Lineup generator not found: {GENERATOR}")
        sys.exit(1)

    lineup_files = sorted(
        p for p in LINEUPS_DIR.glob("*.md")
        if p.name != "index.md"
    )

    if not lineup_files:
        print("No lineup pages found to refresh.")
        return

    success_count = 0
    fail_count = 0

    for lineup_file in lineup_files:
        ok = refresh_lineup(lineup_file)
        if ok:
            success_count += 1
        else:
            fail_count += 1

    print("")
    print(f"Refreshed lineups: {success_count}")
    print(f"Failed lineups: {fail_count}")

    if fail_count:
        sys.exit(1)


if __name__ == "__main__":
    main()