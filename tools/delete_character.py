import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHARACTER_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"


def delete_character(name, force=False):
    folder_name = name.upper()
    target = CHARACTER_ROOT / folder_name

    if not target.exists():
        print(f"Character does not exist: {folder_name}")
        return

    print(f"\nPreparing to delete character: {folder_name}")
    print(f"Target folder: {target}")

    if not force:
        confirm = input(
            f'Type "{folder_name}" to confirm deletion: '
        ).strip()

        if confirm != folder_name:
            print("Deletion cancelled.")
            return

    shutil.rmtree(target)
    print("Character folder deleted")

    print("\nUpdating generated pages...")

    subprocess.run([sys.executable, "tools/generate_character_pages.py"], check=True)
    subprocess.run([sys.executable, "tools/generate_character_index.py"], check=True)
    subprocess.run([sys.executable, "tools/generate_nav_characters.py"], check=True)

    print("\nCharacter deletion complete.\n")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        required=True,
        help="Character name (e.g. luca → folder LUCA)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete without confirmation prompt"
    )

    args = parser.parse_args()
    delete_character(args.name, force=args.force)


if __name__ == "__main__":
    main()
