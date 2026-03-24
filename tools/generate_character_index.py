import os
import re
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
DOCS_ROOT = ROOT / "docs"
OUTPUT_FILE = ROOT / "docs/characters/index.md"
VERSION_RE = re.compile(r"^(?P<base>.+?)_v(?P<version>\d+)$", re.IGNORECASE)


def docs_rel_url(from_markdown_file: pathlib.Path, target_under_docs: pathlib.Path) -> str:
    rel = os.path.relpath(target_under_docs, start=from_markdown_file.parent)
    return pathlib.PurePosixPath(rel).as_posix()


def split_version(stem: str) -> tuple[str, int]:
    match = VERSION_RE.match(stem)
    if not match:
        return stem, 0
    return match.group("base"), int(match.group("version"))


def find_thumbnail(character_dir):
    identity_dir = character_dir / "01_IDENTITY"

    if not identity_dir.exists():
        return None

    images = [
        p for p in identity_dir.rglob("*")
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ]

    def score(path):
        stem = path.stem.lower()
        base, version = split_version(path.stem)
        base = base.lower()

        if "catalog_thumbnail" in base:
            return (0, -version, stem)
        if "gallery_image" in base:
            return (1, -version, stem)
        if "face_anchor" in base or ("anchor" in base and "face" in base):
            return (2, -version, stem)

        return (9, -version, stem)

    candidates = [p for p in images if score(p)[0] < 9]
    if not candidates:
        return None

    return sorted(candidates, key=score)[0]


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

    lines.append("---")
    lines.append("hide:")
    lines.append("  - toc")
    lines.append("---")
    lines.append("")
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

        rel_img = ""
        if face:
            rel_img = docs_rel_url(OUTPUT_FILE, face)

        # Link relative to docs/characters/index.md -> docs/characters/<slug>.md
        rel_href = f"{slug}/"

        lines.append(f'<a class="character-card" href="{rel_href}">')
        lines.append("")

        if rel_img:
            lines.append(f'  <img src="{rel_img}" alt="{name}">')

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
