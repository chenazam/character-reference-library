import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"

ASSET_FAMILIES = {
    "01_IDENTITY": "identity",
    "02_BODY": "body",
    "03_UCS": "ucs",
    "04_STYLE": "style",
    "05_MOTION": "motion",
    "06_SCENES": "scenes",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def page_relative_url(character_slug: str, target_under_docs: pathlib.Path) -> str:
    """
    Compute a URL relative to the rendered character page location.

    Character pages live at:
        docs/characters/<slug>.md

    With MkDocs default directory_urls: true, they render to:
        /characters/<slug>/

    So paths inside included snippets must be relative to the virtual page
    directory "characters/<slug>/", not to the snippet file location and not
    to docs/characters/.
    """
    target_virtual = pathlib.PurePosixPath(target_under_docs.relative_to(DOCS_ROOT).as_posix())
    page_virtual_dir = pathlib.PurePosixPath("characters") / character_slug
    rel = os.path.relpath(str(target_virtual), start=str(page_virtual_dir))
    return pathlib.PurePosixPath(rel).as_posix()


def generate_gallery(images, character_slug: str):
    lines = []
    lines.append('<div class="character-gallery">')
    lines.append("")

    for img in images:
        rel = page_relative_url(character_slug, img)
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
            gallery = generate_gallery(images, character)
            snippet_path.write_text(gallery, encoding="utf-8")

            print(f"  Generated {snippet_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
