import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
CHARACTER_PAGES_ROOT = ROOT / "docs/characters"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"

EXPECTED_PROFILE_FILES = {
    "character_summary.md",
    "identity_guardrails.md",
    "metadata.yaml",
    "prompt_blocks.md",
}

EXPECTED_FOLDERS = [
    "00_PROFILE",
    "00_SOURCE_REFERENCES",
    "01_IDENTITY",
    "02_BODY",
    "03_UCS",
    "04_STYLE",
    "05_MOTION",
    "06_SCENES",
]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def validate_character(character_dir: pathlib.Path):
    name = character_dir.name
    issues = []

    # Check folder structure
    for folder in EXPECTED_FOLDERS:
        if not (character_dir / folder).exists():
            issues.append(f"Missing folder: {folder}")

    # Check profile files
    profile_dir = character_dir / "00_PROFILE"
    if profile_dir.exists():
        existing = {p.name for p in profile_dir.iterdir() if p.is_file()}
        for filename in EXPECTED_PROFILE_FILES:
            if filename not in existing:
                issues.append(f"Missing profile file: 00_PROFILE/{filename}")

    # Check asset-family folders for images (warning only)
    for folder in EXPECTED_FOLDERS:
        if folder in {"00_PROFILE", "00_SOURCE_REFERENCES"}:
            continue

        asset_dir = character_dir / folder
        if not asset_dir.exists():
            continue

        images = [
            p for p in asset_dir.rglob("*")
            if p.suffix.lower() in IMAGE_EXTENSIONS
        ]

        if not images:
            issues.append(f"No images found in asset folder: {folder}")

    # Check generated character page
    page_path = CHARACTER_PAGES_ROOT / f"{name.lower()}.md"
    if not page_path.exists():
        issues.append(f"Missing generated page: docs/characters/{name.lower()}.md")

    # Check snippet folder
    snippet_dir = SNIPPETS_ROOT / name.lower()
    if not snippet_dir.exists():
        issues.append(f"Missing snippet folder: docs/snippets/galleries/{name.lower()}")

    return issues


def main():
    any_issues = False

    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not character_dir.is_dir():
            continue

        issues = validate_character(character_dir)

        if issues:
            any_issues = True
            print(f"\n[{character_dir.name}]")
            for issue in issues:
                print(f"  - {issue}")

    if not any_issues:
        print("Library validation passed: no issues found.")


if __name__ == "__main__":
    main()
