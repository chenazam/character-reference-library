import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTER_PAGES = ROOT / "docs/characters"
CHARACTER_ASSETS = ROOT / "docs/assets/library/10_CHARACTERS"


def load_metadata_for_slug(slug: str) -> dict:
    metadata_file = CHARACTER_ASSETS / slug.upper() / "metadata.yaml"

    if not metadata_file.exists():
        # Fallback: try lowercase folder name if your structure ever changes
        metadata_file = CHARACTER_ASSETS / slug / "metadata.yaml"

    if not metadata_file.exists():
        return {}

    try:
        with metadata_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"Warning: failed to read {metadata_file}: {e}")
        return {}


def should_include_in_nav(slug: str) -> bool:
    metadata = load_metadata_for_slug(slug)
    site_visibility = metadata.get("site_visibility", {})

    if not isinstance(site_visibility, dict):
        return True

    return site_visibility.get("include_in_nav", True)


def main():
    lines = []

    lines.append("- Characters:")
    lines.append("    - Character Index: characters/index.md")

    pages = sorted(
        p for p in CHARACTER_PAGES.glob("*.md")
        if p.name not in {"index.md", "templates.md"}
    )

    for page in pages:
        slug = page.stem

        if not should_include_in_nav(slug):
            print(f"Skipping {slug} (include_in_nav: false)")
            continue

        name = page.stem.replace("_", " ").title()
        lines.append(f"    - {name}: characters/{slug}.md")

    print("\n".join(lines))


if __name__ == "__main__":
    main()