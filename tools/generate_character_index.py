import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
OUTPUT_FILE = ROOT / "docs/characters/index.md"


def find_thumbnail(character_dir):

    gallery_dir = character_dir / "20_THUMBNAIL"

    if gallery_dir.exists():
        for f in gallery_dir.iterdir():
            if "gallery" in f.name:
                return f

    face_dir = character_dir / "01_FACE"

    if face_dir.exists():
        for f in face_dir.iterdir():
            if "face_anchor" in f.name:
                return f

    return None


def main():

    lines = []

    lines.append("# Characters")
    lines.append("")
    lines.append("Browse characters in the reference library.")
    lines.append("")
    lines.append('<div class="character-index-grid">')
    lines.append("")

    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):

        if not character_dir.is_dir():
            continue

        name = character_dir.name
        slug = name.lower()

        face = find_thumbnail(character_dir)

        if face:
            rel = face.relative_to(ROOT / "docs").as_posix()
            rel = "/" + rel
        else:
            rel = ""

        lines.append(f'<a class="character-card" href="../characters/{slug}/">')
        lines.append("")

        if rel:
            lines.append(f'  <img src="{rel}" alt="{name}">')

        lines.append(f"  <h3>{name}</h3>")
        lines.append("")
        lines.append("</a>")
        lines.append("")

    lines.append("</div>")
    lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()