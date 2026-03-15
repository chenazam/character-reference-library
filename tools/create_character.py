import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCAFFOLD = ROOT / "scaffolding" / "characters"
CHARACTER_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"


def display_name_from_input(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("Character name cannot be empty.")
    return name[0].upper() + name[1:].lower()


def create_character(name: str) -> None:
    display_name = display_name_from_input(name)
    folder_name = display_name.upper()
    slug = display_name.lower()

    target = CHARACTER_ROOT / folder_name

    if target.exists():
        print(f"Character already exists: {folder_name}")
        return

    print(f"\nCreating character: {display_name} ({folder_name})")

    shutil.copytree(SCAFFOLD, target)

    print("Folder structure created")

    profile = target / "00_PROFILE"

    metadata = profile / "metadata.yaml"
    summary = profile / "character_summary.md"
    prompt_blocks = profile / "prompt_blocks.md"

    replacements = {
        "[CHARACTER_NAME]": display_name,
        "[CHARACTER_SLUG]": slug,
        "[CHARACTER_FOLDER]": folder_name,
    }

    for path in [metadata, summary, prompt_blocks]:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for placeholder, value in replacements.items():
                text = text.replace(placeholder, value)
            path.write_text(text, encoding="utf-8")

    print("Profile templates initialized")

    print("\nUpdating generated pages...")

    subprocess.run([sys.executable, "tools/generate_character_pages.py"], cwd=ROOT)
    subprocess.run([sys.executable, "tools/generate_character_index.py"], cwd=ROOT)
    subprocess.run([sys.executable, "tools/generate_nav_characters.py"], cwd=ROOT)

    print("\nCharacter creation complete.\n")


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        required=True,
        help="Character name (e.g. ragnar -> folder RAGNAR, display name Ragnar)",
    )

    args = parser.parse_args()

    create_character(args.name)


if __name__ == "__main__":
    main()
