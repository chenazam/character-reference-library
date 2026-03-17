#!/usr/bin/env python3

import pathlib
import yaml

try:
    from tools.height_utils import (
        SILHOUETTE_ARCHETYPES,
        fallback_proportion_archetype,
        build_character_placeholder,
    )
except ModuleNotFoundError:
    from height_utils import (
        SILHOUETTE_ARCHETYPES,
        fallback_proportion_archetype,
        build_character_placeholder,
    )

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHARACTERS_ROOT = ROOT / "docs" / "assets" / "library" / "10_CHARACTERS"
OUTPUT_ROOT = ROOT / "docs" / "archetypes"


ARCHETYPE_DESCRIPTIONS = {
    "slender_refined": "A narrow, elegant, lightly built silhouette with delicate proportions and gentle taper.",
    "slender_tall": "A vertically elongated, slender silhouette with long lines and minimal mass.",
    "compact_light": "A smaller, lighter, compact silhouette with grounded proportions and modest width.",
    "athletic_balanced": "A proportional athletic silhouette with moderate shoulder width and balanced lower body.",
    "athletic_leg_dominant": "An athletic silhouette with stronger lower-body emphasis, especially thighs, hips, and glutes.",
    "broad_athletic": "A broad-shouldered athletic silhouette with visible strength but controlled taper.",
    "broad_upper_dominant": "A strongly upper-body-dominant silhouette with wide shoulders and a pronounced V-shape.",
    "heavy_muscular": "A thick, dense, muscular silhouette with heavy overall mass and reduced taper.",
    "massive_upper_dominant": "An extremely large upper-body-dominant silhouette with overwhelming shoulder and torso presence.",
    "soft_curvy": "A softer silhouette with fuller hips, gentler transitions, and a more rounded lower-body read.",
}


def load_all_characters() -> list[dict]:
    characters = []

    for char_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not char_dir.is_dir():
            continue

        metadata_file = char_dir / "00_PROFILE" / "metadata.yaml"
        if not metadata_file.exists():
            continue

        with metadata_file.open("r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f) or {}

        if not isinstance(metadata, dict):
            continue

        characters.append(metadata)

    return characters


def prettify_archetype(name: str) -> str:
    return name.replace("_", " ").title()


def build_character_table(archetype: str, characters: list[dict]) -> str:
    if not characters:
        return "_No characters currently mapped to this archetype._\n"

    lines = [
        "| Character | Build | Anchor | Emphasis |",
        "|---|---|---|---|",
    ]

    for c in sorted(characters, key=lambda x: x.get("name", "")):
        name = c.get("name", c.get("slug", "Unknown"))

        build = get_nested(c, "physical", "build_category", default="-")
        anchor = get_nested(c, "physical", "silhouette_anchor", default="-")
        emphasis = get_nested(c, "physical", "silhouette_emphasis", default="-")

        lines.append(f"| {name} | {build} | {anchor} | {emphasis} |")

    return "\n".join(lines) + "\n"


def build_archetype_preview(archetype: str) -> str:
    placeholder = build_character_placeholder(archetype, 100.0)
    return f"""<div class="height-lineup height-lineup--archetype-doc">
  <div class="height-lineup__baseline" aria-hidden="true"></div>
  <div class="height-lineup__figure">
    <div class="height-lineup__stage">
      {placeholder}
    </div>
  </div>
</div>
"""


def build_archetype_page(archetype: str, characters: list[dict]) -> str:
    title = prettify_archetype(archetype)
    description = ARCHETYPE_DESCRIPTIONS.get(archetype, "")

    preview = build_archetype_preview(archetype)

    lines = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        f"# {title}",
        "",
        preview,
        "",
    ]

    if description:
        lines.extend([description, ""])

    lines.extend([
        "## Characters",
        "",
    ])
    
    lines.append(build_character_table(archetype, characters))

    lines.append("")
    return "\n".join(lines)


def build_index_page(groups: dict[str, list[str]]) -> str:
    lines = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        "# Silhouette Archetypes",
        "",
        "These pages document the fallback silhouette archetypes used when a character does not yet have a `silhouette_front` asset.",
        "",
        "## Archetypes",
        "",
    ]

    for archetype in SILHOUETTE_ARCHETYPES:
        title = prettify_archetype(archetype)
        count = len(groups.get(archetype, []))
        lines.append(f"- [{title}]({archetype}.md) — {count} character(s)")

    lines.append("")
    return "\n".join(lines)


def main():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    characters = load_all_characters()

    groups = {archetype: [] for archetype in SILHOUETTE_ARCHETYPES}
    
    for metadata in characters:
        archetype = fallback_proportion_archetype(metadata)
        groups.setdefault(archetype, []).append(metadata)
    
    for archetype in SILHOUETTE_ARCHETYPES:
        page = build_archetype_page(archetype, groups.get(archetype, []))
        out_file = OUTPUT_ROOT / f"{archetype}.md"
        out_file.write_text(page, encoding="utf-8")
        print(f"Generated archetype page: {out_file}")

    index_page = build_index_page(groups)
    index_file = OUTPUT_ROOT / "index.md"
    index_file.write_text(index_page, encoding="utf-8")
    print(f"Generated archetype index: {index_file}")


if __name__ == "__main__":
    main()
