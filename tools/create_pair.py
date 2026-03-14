import argparse
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

PAIR_SCAFFOLD = ROOT / "scaffolding" / "pairs"
PAIR_ROOT = ROOT / "docs/assets/library/20_PAIRS"


def create_pair(name):

    name = name.upper()

    target = PAIR_ROOT / name

    if target.exists():
        print(f"Pair already exists: {name}")
        return

    print(f"Creating pair: {name}")

    shutil.copytree(PAIR_SCAFFOLD, target)

    profile = target / "00_PROFILE"

    for file in profile.glob("*.md"):
        text = file.read_text()
        text = text.replace("[PAIR_NAME]", name)
        file.write_text(text)

    print("Pair scaffold created")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--name", required=True)

    args = parser.parse_args()

    create_pair(args.name)


if __name__ == "__main__":
    main()