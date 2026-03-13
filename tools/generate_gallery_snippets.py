import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/galleries"

# pipeline folders we want snippet galleries for
PIPELINE_STAGES = {
    "01_FACE": "face",
    "02_HAIR": "hair",
    "03_ANATOMY": "anatomy",
    "04_PROPORTIONS": "proportions",
    "05_MUSCLE": "muscle",
    "06_BODY": "body",
    "07_SILHOUETTE": "silhouette",
    "08_TURNAROUND": "turnaround",
    "09_EXPRESSIONS": "expressions",
    "10_HANDS": "hands",
    "11_UCS": "ucs",
    "12_SIGNATURE_OUTFIT": "signature-outfit",
    "13_DESIGN_LANGUAGE": "design-language",
    "14_WARDROBE": "wardrobe",
    "15_POSES": "poses",
    "16_MOTION": "motion",
    "17_SCALE": "scale",
    "18_SCENES": "scenes",
    "19_PROPS": "props",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def generate_gallery(images):
    lines = []
    lines.append('<div class="character-gallery">')
    lines.append("")

    for img in images:

        # path relative to docs/
        rel = img.relative_to(ROOT / "docs")

        # convert for use inside docs/characters pages
        rel = "../" + rel.as_posix()

        lines.append(f'  <a href="{rel}" target="_blank">')
        lines.append(f'    <img src="{rel}" alt="">')
        lines.append("  </a>")
        lines.append("")

    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


def main():

    SNIPPETS_ROOT.mkdir(parents=True, exist_ok=True)

    for character_dir in CHARACTERS_ROOT.iterdir():

        if not character_dir.is_dir():
            continue

        character = character_dir.name.lower()

        for stage_folder, stage_name in PIPELINE_STAGES.items():

            stage_path = character_dir / stage_folder

            if not stage_path.exists():
                continue

            images = [
                p for p in sorted(stage_path.iterdir())
                if p.suffix.lower() in IMAGE_EXTENSIONS
            ]

            if not images:
                continue

            snippet_path = SNIPPETS_ROOT / f"{character}-{stage_name}.md"

            gallery = generate_gallery(images)

            snippet_path.write_text(gallery, encoding="utf-8")

            print(f"Generated {snippet_path}")


if __name__ == "__main__":
    main()