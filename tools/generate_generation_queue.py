import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHAR_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
OUTPUT = ROOT / "docs/pipeline/generation_queue.md"


def load_metadata(character_dir):

    path = character_dir / "00_PROFILE/metadata.yaml"

    if not path.exists():
        return None

    return yaml.safe_load(path.read_text())


def main():

    lines = []

    lines.append("# Generation Queue")
    lines.append("")
    lines.append("Reference assets that still need to be generated.")
    lines.append("")

    for char_dir in sorted(CHAR_ROOT.iterdir()):

        if not char_dir.is_dir():
            continue

        metadata = load_metadata(char_dir)

        if not metadata:
            continue

        status = metadata.get("pipeline_status", {})

        missing = [k for k,v in status.items() if v != "complete"]

        if not missing:
            continue

        lines.append(f"## {char_dir.name}")
        lines.append("")

        for stage in missing:

            lines.append(f"- {stage}")

        lines.append("")

    OUTPUT.write_text("\n".join(lines))

    print("Generation queue updated")


if __name__ == "__main__":
    main()