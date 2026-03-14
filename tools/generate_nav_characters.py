import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

MKDOCS_FILE = ROOT / "mkdocs.yml"
CHARACTER_PAGES = ROOT / "docs/characters"
CHARACTER_ASSETS = ROOT / "docs/assets/library/10_CHARACTERS"


def load_metadata_for_slug(slug: str) -> dict:
    candidates = [
        CHARACTER_ASSETS / slug / "00_PROFILE" / "metadata.yaml",
        CHARACTER_ASSETS / slug.upper() / "00_PROFILE" / "metadata.yaml",
        CHARACTER_ASSETS / slug.capitalize() / "00_PROFILE" / "metadata.yaml",
    ]

    for metadata_file in candidates:
        if not metadata_file.exists():
            continue

        try:
            with metadata_file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print(f"Warning: failed to read {metadata_file}: {e}")
            return {}

    return {}


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


def should_include_in_nav(slug: str) -> bool:
    metadata = load_metadata_for_slug(slug)
    site_visibility = metadata.get("site_visibility", {})

    if not isinstance(site_visibility, dict):
        return True

    return parse_bool(site_visibility.get("include_in_nav"), True)


def display_name_for_slug(slug: str) -> str:
    metadata = load_metadata_for_slug(slug)
    return metadata.get("name", slug.replace("_", " ").title())


def build_character_entries() -> list[dict]:
    entries = [{"Overview": "characters/overview.md"},
               {"Character Index": "characters/index.md"}]

    pages = sorted(
        p for p in CHARACTER_PAGES.glob("*.md")
        if p.name not in {"index.md", "overview.md", "templates.md", "character-page-template.md"}
    )

    for page in pages:
        slug = page.stem

        if not should_include_in_nav(slug):
            print(f"Skipping {slug} (include_in_nav: false)")
            continue

        name = display_name_for_slug(slug)
        entries.append({name: f"characters/{slug}.md"})

    # Keep your manual/static pages at the end
    template_page = CHARACTER_PAGES / "character-page-template.md"
    if template_page.exists():
        entries.append({"Character Page Template": "characters/character-page-template.md"})

    return entries


def find_nav_section(nav_list: list, key: str):
    for item in nav_list:
        if isinstance(item, dict) and key in item:
            return item[key]
    return None


def main():
    if not MKDOCS_FILE.exists():
        raise FileNotFoundError(f"mkdocs.yml not found: {MKDOCS_FILE}")

    with MKDOCS_FILE.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav")
    if not isinstance(nav, list):
        raise RuntimeError("mkdocs.yml does not contain a valid 'nav' list")

    browse_library = find_nav_section(nav, "Browse Library")
    if not isinstance(browse_library, list):
        raise RuntimeError("Could not find 'Browse Library' section in mkdocs.yml")

    characters = find_nav_section(browse_library, "Characters")
    if not isinstance(characters, list):
        raise RuntimeError("Could not find 'Characters' section under 'Browse Library' in mkdocs.yml")

    new_entries = build_character_entries()

    # Replace contents of the Characters section in place
    characters.clear()
    characters.extend(new_entries)

    with MKDOCS_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False, allow_unicode=True)

    print("Updated Characters nav in mkdocs.yml")
    for entry in new_entries:
        print(entry)


if __name__ == "__main__":
    main()