import argparse
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

GROUP_SCAFFOLD = ROOT / "scaffolding" / "groups"
GROUP_ROOT = ROOT / "docs/assets/library/30_GROUPS"


def create_group(name):

    name = name.upper()

    target = GROUP_ROOT / name

    if target.exists():
        print(f"Group already exists: {name}")
        return

    print(f"Creating group: {name}")

    shutil.copytree(GROUP_SCAFFOLD, target)

    profile = target / "00_PROFILE"

    for file in profile.glob("*.md"):
        text = file.read_text()
        text = text.replace("[GROUP_NAME]", name)
        file.write_text(text)

    print("Group scaffold created")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--name", required=True)

    args = parser.parse_args()

    create_group(args.name)


if __name__ == "__main__":
    main()