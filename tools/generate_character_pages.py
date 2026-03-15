import pathlib
import re
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

RESERVED_PAGES = {
    "index.md",
    "overview.md",
    "templates.md",
    "character-page-template.md",
}


def fix_common_mojibake(text: str) -> str:
    return (
        text.replace("â€™", "'")
            .replace("â€“", "–")
            .replace("â€œ", '"')
            .replace("â€\x9d", '"')
    )


def deep_fix_strings(value):
    if isinstance(value, str):
        return fix_common_mojibake(value)
    if isinstance(value, list):
        return [deep_fix_strings(item) for item in value]
    if isinstance(value, dict):
        return {k: deep_fix_strings(v) for k, v in value.items()}
    return value


def load_metadata(character_dir: pathlib.Path) -> dict:
    metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"

    if not metadata_file.exists():
        return {}

    try:
        with metadata_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                return {}
            return deep_fix_strings(data)
    except Exception as e:
        print(f"Warning: failed to read {metadata_file}: {e}")
        return {}


def load_character_summary(character_dir: pathlib.Path) -> str:
    summary_file = character_dir / "00_PROFILE" / "character_summary.md"
    if not summary_file.exists():
        return ""
    try:
        text = summary_file.read_text(encoding="utf-8")
        return fix_common_mojibake(text)
    except Exception as e:
        print(f"Warning: failed to read {summary_file}: {e}")
        return ""


def parse_markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    pattern = re.compile(r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)

    for match in pattern.finditer(text):
        title = match.group(1).strip()
        body = match.group(2).strip()
        sections[title] = body

    return sections


def clean_md_text(text: str) -> str:
    text = re.sub(r"(?m)^Use this block.*$", "", text).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_first_paragraph(text: str) -> str:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return parts[0] if parts else ""


def human_join(items: list[str]) -> str:
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def build_overview(metadata: dict, summary_sections: dict[str, str]) -> str:
    name = metadata.get("name", "This character")

    core = metadata.get("core_identity", {})
    physical = metadata.get("physical", {})
    face = metadata.get("face", {})
    style = metadata.get("style", {})
    expression = metadata.get("expression", {})
    movement = metadata.get("movement", {})

    short_summary = (core.get("short_summary") or "").strip()
    height_cm = physical.get("height_cm")
    height_imp = physical.get("height_imperial")
    build_notes = (physical.get("build_notes") or "").strip()
    notes = (metadata.get("notes") or "").strip()

    face_desc = []
    if face.get("face_shape"):
        face_desc.append(str(face["face_shape"]).replace("_", " "))
    if face.get("jawline"):
        face_desc.append(str(face["jawline"]).replace("_", " "))
    if face.get("hair_description"):
        face_desc.append(str(face["hair_description"]))
    if face.get("eye_description"):
        face_desc.append(str(face["eye_description"]))

    visual_full = clean_md_text(summary_sections.get("Visual Identity (Full Prompt Version)", ""))
    personality = clean_md_text(summary_sections.get("Personality Snapshot", ""))

    identity_para = []
    if short_summary:
        if height_cm and height_imp:
            identity_para.append(f"{name} is {height_cm} cm ({height_imp}) tall. {short_summary}")
        else:
            identity_para.append(f"{name} is {short_summary[0].lower() + short_summary[1:]}" if short_summary else "")
    elif visual_full:
        identity_para.append(extract_first_paragraph(visual_full))
    elif build_notes:
        identity_para.append(build_notes)

    if build_notes and build_notes not in " ".join(identity_para):
        identity_para.append(build_notes)

    if face_desc:
        identity_para.append(f"He is characterized by a {'; '.join(face_desc)}.")

    style_para = ""
    primary_aesthetic = str(style.get("primary_aesthetic", "")).replace("_", " ").strip()
    secondary = style.get("secondary_aesthetic") or []
    materials = style.get("materials") or []
    colors = style.get("primary_colors") or []

    if primary_aesthetic or secondary or materials or colors:
        style_para = (
            f"His style is defined by {primary_aesthetic}"
            if primary_aesthetic
            else "His style is visually consistent"
        )
        extras = []
        if secondary:
            extras.append(f"secondary influences from {human_join([str(s).replace('_', ' ') for s in secondary])}")
        if materials:
            extras.append(f"materials such as {human_join([str(m) for m in materials])}")
        if colors:
            extras.append(f"a palette built around {human_join([str(c).replace('_', ' ') for c in colors])}")
        if extras:
            style_para += ", with " + ", ".join(extras)
        style_para += "."

    presence_para_parts = []
    movement_style = str(movement.get("movement_style", "")).replace("_", " ").strip()
    gesture_style = str(movement.get("gesture_style", "")).replace("_", " ").strip()
    spatial_presence = str(movement.get("spatial_presence", "")).replace("_", " ").strip()

    if movement_style or gesture_style or spatial_presence:
        presence_para_parts.append(
            f"He moves with {movement_style or 'controlled movement'}, uses {gesture_style or 'controlled'} gestures, and projects a {spatial_presence or 'steady presence'}."
        )

    if expression.get("default_expression") or expression.get("smile_type") or expression.get("emotional_tone"):
        expr_bits = []
        if expression.get("default_expression"):
            expr_bits.append(str(expression["default_expression"]).replace("_", " "))
        if expression.get("smile_type"):
            expr_bits.append(str(expression["smile_type"]).replace("_", " "))
        if expression.get("emotional_tone"):
            expr_bits.append(str(expression["emotional_tone"]).replace("_", " "))
        presence_para_parts.append(f"His expression profile reads as {human_join(expr_bits)}.")

    if personality:
        presence_para_parts.append(extract_first_paragraph(personality))
    elif notes:
        presence_para_parts.append(notes)

    paragraphs = [
        " ".join(identity_para).strip(),
        style_para.strip(),
        " ".join(presence_para_parts).strip(),
    ]

    paragraphs = [p for p in paragraphs if p]
    return "\n\n".join(paragraphs)


def build_character_page(character: str, character_dir: pathlib.Path) -> str:
    metadata = load_metadata(character_dir)
    summary_text = load_character_summary(character_dir)
    summary_sections = parse_markdown_sections(summary_text)

    name = metadata.get("name", character_dir.name)
    overview = build_overview(metadata, summary_sections)

    lines = []

    lines.append(f"# {name}")
    lines.append("")

    hero_snippet_path = SNIPPETS_ROOT / character / "hero.md"
    if hero_snippet_path.exists():
        lines.append(f'--8<-- "snippets/galleries/{character}/hero.md"')
        lines.append("")

    lines.append("## Overview")
    lines.append("")
    lines.append(overview or f"{name} is a character in the reference library.")
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

        if page_path.stem not in valid_slugs:
            page_path.unlink()
            print(f"Removed stale page {page_path.relative_to(ROOT)}")


def main() -> None:
    PAGES_ROOT.mkdir(parents=True, exist_ok=True)

    valid_slugs = current_character_slugs()
    cleanup_stale_generated_pages(valid_slugs)

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
