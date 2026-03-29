import html
import pathlib
import re
import yaml

try:
    from tools.site_paths import site_root_url
except ModuleNotFoundError:
    from site_paths import site_root_url

try:
    from tools.height_utils import (
        get_nested,
        fallback_proportion_archetype,
        get_reference_silhouette_link,
        make_root_image_link,
        build_reference_placeholder,
        build_character_placeholder,
        build_silhouette_img,
    )
except ModuleNotFoundError:
    from height_utils import (
        get_nested,
        fallback_proportion_archetype,
        get_reference_silhouette_link,
        make_root_image_link,
        build_reference_placeholder,
        build_character_placeholder,
        build_silhouette_img,
    )

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"
PAGES_ROOT = ROOT / "docs/characters"
REFERENCE_SILHOUETTE = ROOT / "docs" / "assets" / "reference" / "reference_male_average_180cm_front_v1.png"

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


def resolve_latest_normalized_silhouette_front(character_dir: pathlib.Path) -> str:
    structure_dir = character_dir / "02_BODY" / "structure"
    if not structure_dir.exists():
        return ""

    slug = character_dir.name.lower()
    pattern = f"{slug}_silhouette_front*_normalized.png"

    best_path = None
    best_version = -1

    for path in structure_dir.glob(pattern):
        m = re.fullmatch(
            rf"{re.escape(slug)}_silhouette_front(?:_v(\d+))?_normalized",
            path.stem,
            re.IGNORECASE,
        )
        if not m:
            continue

        version = int(m.group(1)) if m.group(1) else 0
        if version > best_version:
            best_version = version
            best_path = path

    if not best_path:
        return ""

    return make_root_image_link(character_dir, best_path.name)


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

def build_height_context_section(record: dict, metadata: dict) -> str:
    height_cm = get_nested(metadata, "physical", "height_cm", default=0)
    height_imperial = get_nested(metadata, "physical", "height_imperial", default="")
    if not isinstance(height_cm, (int, float)):
        height_cm = 0
    if not height_cm:
        return ""

    reference_height = 180
    reference_imperial = "5'11\""
    print(f"[HEIGHT DEBUG] {record['dir']} -> {height_cm} ({type(height_cm)})")
    max_height = max(height_cm, reference_height)

    def pct(height: int) -> float:
        return (height / max_height) * 100

    char_name = metadata.get("name", "Character")
    archetype = fallback_proportion_archetype(metadata)

    silhouette_front = resolve_latest_normalized_silhouette_front(pathlib.Path(record["dir"]))

    reference_silhouette = get_reference_silhouette_link()

    if silhouette_front and reference_silhouette:
        reference_figure = build_silhouette_img(
            reference_silhouette,
            "Reference silhouette",
            pct(reference_height),
            reference=True,
        )
    else:
        reference_figure = build_reference_placeholder(
            pct(reference_height)
        )

    if silhouette_front:
        character_figure = build_silhouette_img(
            silhouette_front,
            f"{char_name} silhouette front",
            pct(height_cm),
        )
    else:
        character_figure = build_character_placeholder(
            archetype,
            pct(height_cm),
            metadata
        )

    return f"""## Height Context

<div class="height-lineup height-lineup--character-context">
  <div class="height-lineup__baseline" aria-hidden="true"></div>

  <div class="height-lineup__figure height-lineup__figure--ref">
    <div class="height-lineup__stage">
      {reference_figure}
    </div>
    <div class="height-lineup__label">Reference</div>
    <div class="height-lineup__meta">{reference_height} cm / {reference_imperial}</div>
  </div>

  <div class="height-lineup__figure height-lineup__figure--a">
    <div class="height-lineup__stage">
      {character_figure}
    </div>
    <div class="height-lineup__label">{char_name}</div>
    <div class="height-lineup__meta">{height_cm} cm / {height_imperial}</div>
  </div>
</div>

"""


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
    items = [str(i).strip() for i in items if str(i).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def labelize(value: str) -> str:
    return str(value).replace("_", " ").strip()


def add_stat(stats: list[tuple[str, str]], label: str, value) -> None:
    if value is None:
        return
    if isinstance(value, list):
        rendered = human_join([labelize(v) for v in value])
    else:
        rendered = labelize(value)
    if rendered:
        stats.append((label, rendered))


def build_overview_paragraph(metadata: dict, summary_sections: dict[str, str]) -> str:
    overview_text = clean_md_text(summary_sections.get("Overview Paragraph", ""))
    overview_para = extract_first_paragraph(overview_text)
    if overview_para:
        extra_paras = [p.strip() for p in overview_text.split("\n\n")[1:] if p.strip()]
        if extra_paras:
            return "\n\n".join([overview_para] + extra_paras)
        return overview_para

    core = metadata.get("core_identity", {})
    physical = metadata.get("physical", {})
    face = metadata.get("face", {})
    style = metadata.get("style", {})
    movement = metadata.get("movement", {})

    visual_full = clean_md_text(summary_sections.get("Visual Identity (Full Prompt Version)", ""))
    personality = clean_md_text(summary_sections.get("Personality Snapshot", ""))

    visual_para = extract_first_paragraph(visual_full)
    personality_para = extract_first_paragraph(personality)

    if visual_para:
        paragraph = visual_para
        if personality_para and personality_para not in paragraph:
            paragraph += " " + personality_para
        return paragraph

    short_summary = (core.get("short_summary") or "").strip()
    build_notes = (physical.get("build_notes") or "").strip()
    primary_aesthetic = labelize(style.get("primary_aesthetic", ""))
    movement_style = labelize(movement.get("movement_style", ""))
    spatial_presence = labelize(movement.get("spatial_presence", ""))

    bits = []
    if short_summary:
        bits.append(short_summary)
    elif build_notes:
        bits.append(build_notes)

    face_bits = []
    if face.get("face_shape"):
        face_bits.append(labelize(face["face_shape"]))
    if face.get("jawline"):
        face_bits.append(labelize(face["jawline"]))
    if face.get("hair_description"):
        face_bits.append(str(face["hair_description"]).strip())
    if face.get("eye_description"):
        face_bits.append(str(face["eye_description"]).strip())

    if face_bits:
        bits.append(f"He is characterized by a {'; '.join(face_bits)}.")

    if primary_aesthetic:
        style_sentence = f"His style centers on {primary_aesthetic}"
        secondary = style.get("secondary_aesthetic") or []
        if secondary:
            style_sentence += f", with influences from {human_join([labelize(s) for s in secondary])}"
        style_sentence += "."
        bits.append(style_sentence)

    if movement_style or spatial_presence:
        move_sentence = f"He moves with {movement_style or 'controlled movement'}"
        if spatial_presence:
            move_sentence += f" and projects a {spatial_presence}"
        move_sentence += "."
        bits.append(move_sentence)

    return " ".join(bit.strip() for bit in bits if bit.strip()) or "Overview unavailable."


def build_stats(metadata: dict) -> list[tuple[str, str]]:
    core = metadata.get("core_identity", {})
    physical = metadata.get("physical", {})
    face = metadata.get("face", {})
    style = metadata.get("style", {})
    expression = metadata.get("expression", {})
    movement = metadata.get("movement", {})

    stats: list[tuple[str, str]] = []

    height_cm = physical.get("height_cm")
    height_imp = physical.get("height_imperial")
    if height_cm and height_imp:
        stats.append(("Height", f"{height_cm} cm / {height_imp}"))
    elif height_cm:
        stats.append(("Height", f"{height_cm} cm"))
    elif height_imp:
        stats.append(("Height", str(height_imp)))

    add_stat(stats, "Build", core.get("body_type") or physical.get("build_category"))
    add_stat(stats, "Silhouette", core.get("silhouette") or physical.get("frame_proportion"))
    add_stat(stats, "Face", [face.get("face_shape"), face.get("jawline")])
    add_stat(stats, "Hair", face.get("hair_description"))
    add_stat(stats, "Eyes", face.get("eye_description"))
    add_stat(stats, "Style", [style.get("primary_aesthetic")] + list(style.get("secondary_aesthetic") or []))
    add_stat(stats, "Palette", style.get("primary_colors"))
    add_stat(stats, "Materials", style.get("materials"))
    add_stat(stats, "Expression", [expression.get("default_expression"), expression.get("emotional_tone")])
    add_stat(stats, "Movement", movement.get("movement_style"))
    add_stat(stats, "Presence", movement.get("spatial_presence"))

    return [(label, value) for label, value in stats if value]


def build_overview_block(metadata: dict, summary_sections: dict[str, str]) -> str:
    paragraph = build_overview_paragraph(metadata, summary_sections)
    stats = build_stats(metadata)

    lines = ['<div class="character-overview-text">', ""]

    if paragraph:
        for para in [p.strip() for p in paragraph.split("\n\n") if p.strip()]:
            lines.append(f"<p>{html.escape(para)}</p>")
            lines.append("")

    if stats:
        lines.append('<div class="character-stats">')
        lines.append("<ul>")
        for label, value in stats:
            lines.append(f"  <li><strong>{html.escape(label)}:</strong> {html.escape(value)}</li>")
        lines.append("</ul>")
        lines.append("</div>")
        lines.append("")

    lines.append("</div>")
    return "\n".join(lines)


def build_character_page(character: str, character_dir: pathlib.Path) -> str:
    metadata = load_metadata(character_dir)
    summary_text = load_character_summary(character_dir)
    summary_sections = parse_markdown_sections(summary_text)
    record = {"dir": str(character_dir)}
    height_context_section = build_height_context_section(record, metadata)

    name = metadata.get("name", character_dir.name)
    overview_block = build_overview_block(metadata, summary_sections)

    lines = []

    lines.append(f"# {name}")
    lines.append("")
    lines.append('<div class="character-header">')
    lines.append("")

    hero_snippet_path = SNIPPETS_ROOT / character / "hero.md"
    if hero_snippet_path.exists():
        lines.append(f'--8<-- "snippets/galleries/{character}/hero.md"')
        lines.append("")

        lines.append(overview_block)
        lines.append("")

        lines.append("</div>")
        lines.append("")

        if height_context_section:
            lines.append("---")
            lines.append("")
            lines.append(height_context_section)
            lines.append("")
            lines.append("---")
            lines.append("")
        else:
            lines.append("---")
            lines.append("")

    gallery_sections = []
    for section_title, section_slug in SECTIONS:
        snippet_path = SNIPPETS_ROOT / character / f"{section_slug}.md"
        if snippet_path.exists():
            gallery_sections.append((section_title, section_slug))

    if gallery_sections:
        lines.append('<div class="gallery-version-toggle" role="group" aria-label="Asset version display">')
        lines.append('  <label class="gallery-version-toggle__label">')
        lines.append('    <input class="gallery-version-toggle__input" type="checkbox" id="show-all-versions-toggle">')
        lines.append('    <span>Show all versions</span>')
        lines.append('  </label>')
        lines.append('</div>')
        lines.append("")

    for section_title, section_slug in gallery_sections:
        lines.append(f"## {section_title}")
        lines.append("")
        lines.append(f'--8<-- "snippets/galleries/{character}/{section_slug}.md"')
        lines.append("")
        lines.append("---")
        lines.append("")

    if gallery_sections:
        lines.append("<script>")
        lines.append("document.addEventListener('DOMContentLoaded', function () {")
        lines.append("  var toggle = document.getElementById('show-all-versions-toggle');")
        lines.append("  if (!toggle) return;")
        lines.append("  var root = document.documentElement;")
        lines.append("  var storageKey = 'character-gallery-version-mode';")
        lines.append("  try {")
        lines.append("    if (window.localStorage && localStorage.getItem(storageKey) === 'all') {")
        lines.append("      toggle.checked = true;")
        lines.append("    }")
        lines.append("  } catch (error) {}")
        lines.append("")
        lines.append("  function applyMode() {")
        lines.append("    var mode = toggle.checked ? 'all' : 'latest';")
        lines.append("    root.setAttribute('data-gallery-versions', mode);")
        lines.append("    try {")
        lines.append("      if (window.localStorage) {")
        lines.append("        localStorage.setItem(storageKey, mode);")
        lines.append("      }")
        lines.append("    } catch (error) {}")
        lines.append("  }")
        lines.append("")
        lines.append("  toggle.addEventListener('change', applyMode);")
        lines.append("  applyMode();")
        lines.append("});")
        lines.append("</script>")
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
