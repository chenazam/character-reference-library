import argparse
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCAFFOLD = ROOT / "scaffolding" / "characters"
CHARACTER_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"


def create_character(name):

    name = name.upper()

    target = CHARACTER_ROOT / name

    if target.exists():
        print(f"Character already exists: {name}")
        return

    print(f"Creating character: {name}")

    shutil.copytree(SCAFFOLD, target)

    print("Folder structure created")

    profile = target / "00_PROFILE"

    metadata = profile / "metadata.yaml"
    summary = profile / "character_summary.md"
    prompt_blocks = profile / "prompt_blocks.md"

    if metadata.exists():
        text = metadata.read_text()
        text = text.replace("[CHARACTER_NAME]", name)
        metadata.write_text(text)

    if summary.exists():
        text = summary.read_text()
        text = text.replace("[CHARACTER_NAME]", name)
        summary.write_text(text)

    if prompt_blocks.exists():
        text = prompt_blocks.read_text()
        text = text.replace("[CHARACTER_NAME]", name)
        prompt_blocks.write_text(text)

    print("Profile templates initialized")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--name", required=True)

    args = parser.parse_args()

    create_character(args.name)


if __name__ == "__main__":
    main()

import subprocess
import sys

subprocess.run([sys.executable, "tools/generate_character_pages.py"])
subprocess.run([sys.executable, "tools/generate_character_index.py"])