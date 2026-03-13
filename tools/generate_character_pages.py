import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"
PAGES_ROOT = ROOT / "docs/characters"


STAGES = {
    "face": "Face References",
    "hair": "Hair References",
    "anatomy": "Anatomy",
    "proportions": "Body / Proportions",
    "muscle": "Body / Proportions",
    "body": "Body / Proportions",
    "silhouette": "Body / Proportions",
    "turnaround": "Body / Proportions",
    "expressions": "Expression and Gesture",
    "hands": "Expression and Gesture",
    "ucs": "Advanced Reference Sets",
    "signature-outfit": "Advanced Reference Sets",
    "design-language": "Advanced Reference Sets",
    "wardrobe": "Advanced Reference Sets",
    "poses": "Advanced Reference Sets",
    "motion": "Advanced Reference Sets",
    "scale": "Advanced Reference Sets",
    "scenes": "Advanced Reference Sets",
    "props": "Advanced Reference Sets",
}


def snippet_line(character, stage):

    snippet_path = SNIPPETS_ROOT / character / f"{stage}.md"

    if snippet_path.exists():
        return f'--8<-- "snippets/galleries/{character}/{stage}.md"'
    else:
        return f'<!-- snippet missing: snippets/galleries/{character}/{stage}.md -->'


def build_character_page(character):

    name = character.upper()

    lines = []

    lines.append(f"# {name}")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"{name} is a character in the reference library.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Core identity
    lines.append("## Core Identity")
    lines.append("")
    lines.append(snippet_line(character, "core-identity"))
    lines.append("")
    lines.append("---")
    lines.append("")

    current_section = None

    for stage, section in STAGES.items():

        if section != current_section:
            lines.append(f"## {section}")
            lines.append("")
            current_section = section

        lines.append(snippet_line(character, stage))
        lines.append("")

    return "\n".join(lines)


def main():

    PAGES_ROOT.mkdir(parents=True, exist_ok=True)

    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):

        if not character_dir.is_dir():
            continue

        character = character_dir.name.lower()

        page_path = PAGES_ROOT / f"{character}.md"

        page_content = build_character_page(character)

        page_path.write_text(page_content, encoding="utf-8")

        print(f"Generated {page_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()