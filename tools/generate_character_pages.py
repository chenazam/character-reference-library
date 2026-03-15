import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"
PAGES_ROOT = ROOT / "docs/characters"

SECTIONS = [
    ("Identity", "identity"),
    ("Body", "body"),
    ("UCS", "ucs"),
    ("Style", "style"),
    ("Motion", "motion"),
    ("Scenes", "scenes"),
]

# Files in docs/characters that are documentation/manual files, not generated character pages
RESERVED_PAGES = {
    "index.md",
    "overview.md",
    "templates.md",
    "character-page-template.md",
}


def load_metadata(character_dir: pathlib.Path) -> dict:
    metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"

    if not metadata_file.exists():
        return {}

    try:
        with metadata_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"Warning: failed to read {metadata_file}: {e}")
        return {}


def build_character_page(character: str, character_dir: pathlib.Path) -> str:
    metadata = load_metadata(character_dir)
    name = metadata.get("name", character_dir.name)

    lines = []

    lines.append(f"# {name}")
    lines.append("")

    hero_snippet_path = SNIPPETS_ROOT / character / "hero.md"
    if hero_snippet_path.exists():
        lines.append(f'--8<-- "snippets/galleries/{character}/hero.md"')
        lines.append("")

    lines.append("## Overview")
    lines.append("")
    lines.append(f"{name} is a character in the reference library.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for section_title, section_slug in SECTIONS:
        snippet_path = SNIPPETS_ROOT / character / f"{section_slug}.md"
        if not snippet_path.exists():
            continue

        lines.append(f"## {section_title}")
        lines.append("")
        lines.append(f'--8<-- "snippets/galleries/{character}/{section_slug}.md"')
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)



def current_character_slugs() -> set[str]:
    slugs = set()
    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if character_dir.is_dir():
            slugs.add(character_dir.name.lower())
    return slugs


def cleanup_stale_generated_pages(valid_slugs: set[str]) -> None:
    for page_path in PAGES_ROOT.glob("*.md"):
        if page_path.name in RESERVED_PAGES:
            continue

        # page stem is the slug, e.g. docs/characters/blake.md -> "blake"
        if page_path.stem not in valid_slugs:
            page_path.unlink()
            print(f"Removed stale page {page_path.relative_to(ROOT)}")


def main():
    PAGES_ROOT.mkdir(parents=True, exist_ok=True)

    valid_slugs = current_character_slugs()

    # First remove stale generated pages for deleted characters
    cleanup_stale_generated_pages(valid_slugs)

    # Then regenerate current character pages
    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not character_dir.is_dir():
            continue

        character = character_dir.name.lower()
        page_path = PAGES_ROOT / f"{character}.md"

        page_content = build_character_page(character, character_dir)
        page_path.write_text(page_content, encoding="utf-8")

        print(f"Generated {page_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
