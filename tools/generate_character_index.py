import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
OUTPUT_FILE = ROOT / "docs/characters/index.md"


def find_thumbnail(character_dir):
    identity_dir = character_dir / "01_IDENTITY"

    if not identity_dir.exists():
        return None

    images = [
        p for p in identity_dir.rglob("*")
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]


    # Priority 1 — gallery image
    for f in images:
        name = f.name.lower()
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and "gallery" in name:
            return f

    # Priority 2 — face anchor
    for f in images:
        name = f.name.lower()
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and "face_anchor" in name:
            return f

    # Priority 3 — front face
    for f in images:
        name = f.name.lower()
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and "front" in name:
            return f

    return None



def load_metadata(character_dir):
    metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"

    if not metadata_file.exists():
        print(f"No metadata found for {character_dir.name}: {metadata_file}")
        return {}, metadata_file

    try:
        with metadata_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if isinstance(data, dict):
                return data, metadata_file
            print(f"Metadata is not a dict for {character_dir.name}: {metadata_file}")
            return {}, metadata_file
    except Exception as e:
        print(f"Warning: failed to read {metadata_file}: {e}")
        return {}, metadata_file


def parse_bool(value, default=True):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1", "on"}:
            return True
        if normalized in {"false", "no", "0", "off"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return default


def should_list_in_character_index(character_dir):
    metadata, metadata_file = load_metadata(character_dir)
    site_visibility = metadata.get("site_visibility", {})

    if not isinstance(site_visibility, dict):
        print(f"{character_dir.name}: no valid site_visibility in {metadata_file}, defaulting to True")
        return True

    raw_value = site_visibility.get("list_in_character_index", True)
    resolved = parse_bool(raw_value, True)

    print(
        f"{character_dir.name}: list_in_character_index={raw_value!r} "
        f"-> {resolved} (from {metadata_file})"
    )

    return resolved


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

        if not should_list_in_character_index(character_dir):
            print(f"Skipping {character_dir.name} (list_in_character_index: false)")
            continue

        metadata, _ = load_metadata(character_dir)
        name = metadata.get("name", character_dir.name)
        slug = metadata.get("slug", character_dir.name.lower())

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