import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCAFFOLD = ROOT / "scaffolding" / "characters"
CHARACTER_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"


def create_character(name):

    folder_name = name.upper()
    slug = name.lower()

    target = CHARACTER_ROOT / folder_name

    if target.exists():
        print(f"Character already exists: {folder_name}")
        return

    print(f"\nCreating character: {folder_name}")

    shutil.copytree(SCAFFOLD, target)

    print("Folder structure created")

    profile = target / "00_PROFILE"

    metadata = profile / "metadata.yaml"
    summary = profile / "character_summary.md"
    prompt_blocks = profile / "prompt_blocks.md"

    if metadata.exists():
        text = metadata.read_text()
        text = text.replace("[CHARACTER_NAME]", folder_name)
        metadata.write_text(text)

    if summary.exists():
        text = summary.read_text()
        text = text.replace("[CHARACTER_NAME]", folder_name)
        summary.write_text(text)

    if prompt_blocks.exists():
        text = prompt_blocks.read_text()
        text = text.replace("[CHARACTER_NAME]", folder_name)
        prompt_blocks.write_text(text)

    print("Profile templates initialized")

    print("\nUpdating generated pages...")

    subprocess.run([sys.executable, "tools/generate_character_pages.py"])
    subprocess.run([sys.executable, "tools/generate_character_index.py"])
    subprocess.run([sys.executable, "tools/generate_nav_characters.py"])

    print("\nCharacter creation complete.\n")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        required=True,
        help="Character name (e.g. luca → folder LUCA)"
    )

    args = parser.parse_args()

    create_character(args.name)


if __name__ == "__main__":
    main()
