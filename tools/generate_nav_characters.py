import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTER_PAGES = ROOT / "docs/characters"


def main():

    lines = []

    lines.append("- Characters:")
    lines.append("    - Character Index: characters/index.md")

    pages = sorted(
        p for p in CHARACTER_PAGES.glob("*.md")
        if p.name not in {"index.md", "templates.md"}
    )

    for page in pages:

        name = page.stem.replace("_", " ").title()
        slug = page.stem

        lines.append(f"    - {name}: characters/{slug}.md")

    print("\n".join(lines))


if __name__ == "__main__":
    main()