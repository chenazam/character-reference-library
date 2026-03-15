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


def generate_hero_image(image: pathlib.Path, character_slug: str):
    rel = page_relative_url(character_slug, image)

    lines = []
    lines.append('<div class="character-hero">')
    lines.append(f'  <a href="{rel}" target="_blank">')
    lines.append(f'    <img src="{rel}" alt="">')
    lines.append("  </a>")
    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def is_gallery_image(path: pathlib.Path) -> bool:
    parts_lower = [p.lower() for p in path.parts]
    name_lower = path.name.lower()
    stem_lower = path.stem.lower()

    return (
        "01_gallery" in parts_lower
        or "gallery" in stem_lower
        or "thumbnail" in stem_lower
    )


def collect_images(folder):
    images = []
    for p in folder.rglob("*"):
        if p.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(p)
    return sorted(images)


def split_identity_images(images):
    gallery_images = [img for img in images if is_gallery_image(img)]
    regular_images = [img for img in images if not is_gallery_image(img)]
    return regular_images, gallery_images


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

            if family_folder == "01_IDENTITY":
                identity_images, hero_images = split_identity_images(images)

                if identity_images:
                    snippet_path = character_snippet_dir / f"{family_name}.md"
                    gallery = generate_gallery(identity_images, character)
                    snippet_path.write_text(gallery, encoding="utf-8")
                    print(f"  Generated {snippet_path.relative_to(ROOT)}")
                else:
                    print(f"  Skipping {family_folder} identity gallery (no non-gallery images)")

                if hero_images:
                    hero_path = character_snippet_dir / "hero.md"
                    hero = generate_hero_image(hero_images[0], character)
                    hero_path.write_text(hero, encoding="utf-8")
                    print(f"  Generated {hero_path.relative_to(ROOT)}")
                else:
                    print(f"  No hero image found for {character_dir.name}")

                continue

            snippet_path = character_snippet_dir / f"{family_name}.md"
            gallery = generate_gallery(images, character)
            snippet_path.write_text(gallery, encoding="utf-8")

            print(f"  Generated {snippet_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
