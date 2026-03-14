import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"
CHARACTER_PAGES = ROOT / "docs/characters"

ASSET_FAMILIES = {
    "01_IDENTITY": "identity",
    "02_BODY": "body",
    "03_UCS": "ucs",
    "04_STYLE": "style",
    "05_MOTION": "motion",
    "06_SCENES": "scenes",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def docs_rel_url(from_markdown_file: pathlib.Path, target_under_docs: pathlib.Path) -> str:
    rel = os.path.relpath(target_under_docs, start=from_markdown_file.parent)
    return pathlib.PurePosixPath(rel).as_posix()


def generate_gallery(images, snippet_path: pathlib.Path, character_slug: str):
    lines = []
    lines.append('<div class="character-gallery">')
    lines.append("")

    character_page = CHARACTER_PAGES / f"{character_slug}.md"

    for img in images:
        rel = docs_rel_url(character_page, img)

        lines.append(f'  <a href="{rel}" target="_blank">')
        lines.append(f'    <img src="{rel}" alt="">')
        lines.append("  </a>")
        lines.append("")

    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


def collect_images(folder):
    images = []
    for p in folder.rglob("*"):
        if p.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(p)
    return sorted(images)


def main():
    SNIPPETS_ROOT.mkdir(parents=True, exist_ok=True)

    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not character_dir.is_dir():
            continue

        character = character_dir.name.lower()
        character_snippet_dir = SNIPPETS_ROOT / character
        character_snippet_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nProcessing {character_dir.name}")

        for family_folder, family_name in ASSET_FAMILIES.items():
            family_path = character_dir / family_folder

            if not family_path.exists():
                continue

            images = collect_images(family_path)

            if not images:
                print(f"  Skipping {family_folder} (no images)")
                continue

            snippet_path = character_snippet_dir / f"{family_name}.md"

            gallery = generate_gallery(images, snippet_path, character)
            snippet_path.write_text(gallery, encoding="utf-8")

            print(f"  Generated {snippet_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
