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


def load_metadata(character_dir):
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


def snippet_line(character, section_slug):
    snippet_path = SNIPPETS_ROOT / character / f"{section_slug}.md"

    if snippet_path.exists():
        return f'--8<-- "snippets/galleries/{character}/{section_slug}.md"'
    return f'<!-- snippet missing: snippets/galleries/{character}/{section_slug}.md -->'


def build_character_page(character, character_dir):
    metadata = load_metadata(character_dir)
    name = metadata.get("name", character_dir.name)

    lines = []

    lines.append(f"# {name}")
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


def main():
    PAGES_ROOT.mkdir(parents=True, exist_ok=True)

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
