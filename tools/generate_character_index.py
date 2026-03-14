#!/usr/bin/env python3

"""
Generate the character index page.

Fixes:
- Correct relative image paths for mkdocs build
- Use os.path.relpath instead of invalid pathlib.Path.relpath
- Ensure links resolve correctly from docs/characters/index.md
"""

import pathlib
import os
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
CHAR_ROOT = ROOT / "10_CHARACTERS"

OUTPUT_DIR = DOCS_ROOT / "characters"
OUTPUT_FILE = OUTPUT_DIR / "index.md"


def to_output_relative_url(path_under_docs: pathlib.Path) -> str:
    """
    Convert an absolute path under docs/ to a URL relative to the index page.
    """
    rel = path_under_docs.relative_to(DOCS_ROOT)
    rel_path = os.path.relpath(rel, OUTPUT_DIR)
    return pathlib.PurePosixPath(rel_path).as_posix()


def load_metadata(character_dir: pathlib.Path):
    meta_file = character_dir / "00_PROFILE" / "metadata.yaml"
    if not meta_file.exists():
        return None
    with open(meta_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_face_thumbnail(character_slug: str):
    """
    Locate the face anchor thumbnail used on the index page.
    """
    path = DOCS_ROOT / "assets" / "images" / character_slug / "face_anchor.png"
    if path.exists():
        return path
    return None


def generate_index():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cards = []

    for char_dir in sorted(CHAR_ROOT.iterdir()):
        if not char_dir.is_dir():
            continue

        metadata = load_metadata(char_dir)
        if not metadata:
            continue

        slug = metadata.get("slug", char_dir.name.lower())
        name = metadata.get("name", slug.capitalize())

        thumb = find_face_thumbnail(slug)

        img_html = ""
        if thumb:
            img_src = to_output_relative_url(thumb)
            img_html = f'<img src="{img_src}" alt="{name}"/>'

        card = f"""
<a class="character-card" href="../{slug}/">
  {img_html}
  <div class="character-name">{name}</div>
</a>
"""
        cards.append(card.strip())

    content = f"""
# Characters

<div class="character-grid">

{"".join(cards)}

</div>
"""

    OUTPUT_FILE.write_text(content.strip(), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_index()
