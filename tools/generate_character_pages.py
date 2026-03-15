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

print("USING UPDATED generate_character_pages.py")
print(__file__)


# --- text cleanup helpers --------------------------------

def fix_common_mojibake(text: str) -> str:
    return (
        text.replace("â€™", "'")
            .replace("â€“", "–")
            .replace("â€œ", '"')
            .replace("â€", '"')
    )


# --- metadata loading ------------------------------------

def load_metadata(character_dir: pathlib.Path) -> dict:
    metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"

    if not metadata_file.exists():
        return {}

    try:
        with metadata_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

            # clean string fields
            for k, v in data.items():
                if isinstance(v, str):
                    data[k] = fix_common_mojibake(v)

            return data if isinstance(data, dict) else {}
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

    short_summary = core.get("short_summary", "")
    height_cm = physical.get("height_cm")
    height_imp = physical.get("height_imperial")
    build_notes = (physical.get("build_notes") or "").strip()
    notes = (metadata.get("notes") or "").strip()

    face_desc = []
    if face.get("face_shape"):
        face_desc.append(face["face_shape"].replace("_", " "))
    if face.get("jawline"):
        face_desc.append(face["jawline"].replace("_", " "))
    if face.get("hair_description"):
        face_desc.append(face["hair_description"])
    if face.get("eye_description"):
        face_desc.append(face["eye_description"])

    style_parts = []
    if style.get("primary_aesthetic"):
        style_parts.append(style["primary_aesthetic"].replace("_", " "))
    if style.get("secondary_aesthetic"):
        style_parts.append(human_join([s.replace("_", " ") for s in style["secondary_aesthetic"]]))
    if style.get("materials"):
        style_parts.append(f"materials such as {human_join(style['materials'])}")
    if style.get("primary_colors"):
        style_parts.append(f"colors such as {human_join([c.replace('_', ' ') for c in style['primary_colors']])}")

    movement_parts = []
    if movement.get("movement_style"):
        movement_parts.append(movement["movement_style"].replace("_", " "))
    if movement.get("gesture_style"):
        movement_parts.append(movement["gesture_style"].replace("_", " "))
    if movement.get("spatial_presence"):
        movement_parts.append(movement["spatial_presence"].replace("_", " "))

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
        identity_para.append(
            f"He is characterized by a {'; '.join(face_desc)}."
        )

    style_para = ""
    if style_parts:
        style_para = (
            f"His style is defined by {style.get('primary_aesthetic', '').replace('_', ' ')}"
            if style.get("primary_aesthetic")
            else "His style is visually consistent"
        )
        extras = []
        if style.get("secondary_aesthetic"):
            extras.append(f"secondary influences from {human_join([s.replace('_', ' ') for s in style['secondary_aesthetic']])}")
        if style.get("materials"):
            extras.append(f"materials such as {human_join(style['materials'])}")
        if style.get("primary_colors"):
            extras.append(f"a palette built around {human_join([c.replace('_', ' ') for c in style['primary_colors']])}")
        if extras:
            style_para += ", with " + ", ".join(extras)
        style_para += "."

    presence_para_parts = []
    if movement_parts:
        presence_para_parts.append(
            f"He moves with {movement.get('movement_style', '').replace('_', ' ')}, uses {movement.get('gesture_style', '').replace('_', ' ') if movement.get('gesture_style') else 'controlled'} gestures, and projects a {movement.get('spatial_presence', '').replace('_', ' ')}."
        )
    if expression.get("default_expression") or expression.get("smile_type") or expression.get("emotional_tone"):
        expr_bits = []
        if expression.get("default_expression"):
            expr_bits.append(expression["default_expression"].replace("_", " "))
        if expression.get("smile_type"):
            expr_bits.append(expression["smile_type"].replace("_", " "))
        if expression.get("emotional_tone"):
            expr_bits.append(expression["emotional_tone"].replace("_", " "))
        presence_para_parts.append(
            f"His expression profile reads as {human_join(expr_bits)}."
        )
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
    print(f"{character}: overview length = {len(overview)}")
    print(repr(overview[:200]))


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
