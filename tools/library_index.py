import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

ASSET_FAMILIES = [
    "00_SOURCE_REFERENCES",
    "00_PROFILE",
    "01_IDENTITY",
    "02_BODY",
    "03_UCS",
    "04_STYLE",
    "05_MOTION",
    "06_SCENES",
    "07_EXPORTS",
]


def load_metadata(character_dir: pathlib.Path) -> dict:
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


def collect_images(folder: pathlib.Path) -> list[pathlib.Path]:
    if not folder.exists():
        return []

    return sorted(
        p for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def character_slug(character_dir: pathlib.Path, metadata: dict | None = None) -> str:
    if metadata is None:
        metadata = load_metadata(character_dir)

    return metadata.get("slug", character_dir.name.lower())


def character_display_name(character_dir: pathlib.Path, metadata: dict | None = None) -> str:
    if metadata is None:
        metadata = load_metadata(character_dir)

    return metadata.get("name", character_dir.name)


def build_character_record(character_dir: pathlib.Path) -> dict:
    metadata = load_metadata(character_dir)

    family_dirs = {}
    family_images = {}
    all_images = []

    for family in ASSET_FAMILIES:
        family_dir = character_dir / family
        family_dirs[family] = family_dir
        images = collect_images(family_dir)
        family_images[family] = images
        all_images.extend(images)

    all_images = sorted(all_images)

    return {
        "dir": character_dir,
        "key": character_dir.name,
        "slug": character_slug(character_dir, metadata),
        "name": character_display_name(character_dir, metadata),
        "metadata": metadata,
        "families": family_dirs,
        "family_images": family_images,
        "images": all_images,
        "image_names": [p.name.lower() for p in all_images],
    }


def build_library_index() -> dict[str, dict]:
    library = {}

    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not character_dir.is_dir():
            continue

        record = build_character_record(character_dir)
        library[character_dir.name] = record

    return library


def iter_character_records():
    library = build_library_index()
    for key in sorted(library):
        yield library[key]
