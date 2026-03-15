import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHARACTER_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"


def run_step(script_name: str) -> None:
    print(f"\n========== Running {script_name} ==========", flush=True)
    subprocess.run([sys.executable, f"tools/{script_name}"], check=True, cwd=ROOT)
    print(f"========== Finished {script_name} ==========", flush=True)


def delete_character(name, force=False):
    folder_name = name.upper()
    target = CHARACTER_ROOT / folder_name

    if not target.exists():
        print(f"Character does not exist: {folder_name}")
        return

    print(f"\nPreparing to delete character: {folder_name}", flush=True)
    print(f"Target folder: {target}", flush=True)

    if not force:
        confirm = input(f'Type "{folder_name}" to confirm deletion: ').strip()
        if confirm != folder_name:
            print("Deletion cancelled.")
            return

    shutil.rmtree(target)
    print("Character folder deleted", flush=True)

    run_step("generate_character_pages.py")
    run_step("generate_character_index.py")
    run_step("generate_nav_characters.py")

    print("\nCharacter deletion complete.\n", flush=True)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--name",
        required=True,
        help="Character name (e.g. luca -> folder LUCA)"
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
