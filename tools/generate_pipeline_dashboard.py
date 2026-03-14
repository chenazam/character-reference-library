import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHAR_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
OUTPUT = ROOT / "docs/pipeline/progress.md"

STAGES = [
    "face_anchor",
    "hair_sheet",
    "anatomy_sheet",
    "body_anchor",
    "proportion_grid",
    "muscle_tension",
    "silhouette_sheet",
    "turnaround_sheet",
    "expression_sheet",
    "hand_sheet",
    "gallery_image",
    "ucs_core",
    "signature_outfit",
    "design_language",
    "wardrobe",
    "pose_sheet",
    "motion_anchor",
    "height_scale",
    "interaction_anchor",
    "scene_anchor",
    "dynamic_pose",
    "final_ucs",
]


def load_metadata(character_dir):
    path = character_dir / "00_PROFILE" / "metadata.yaml"

    if not path.exists():
        return None

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def progress_bar(percent):
    total = 20
    filled = int(total * percent)
    return "█" * filled + "░" * (total - filled)


def main():
    lines = []

    lines.append("# Pipeline Progress")
    lines.append("")
    lines.append("Overview of character reference completion.")
    lines.append("")

    lines.append("## Overall Progress")
    lines.append("")

    for char_dir in sorted(CHAR_ROOT.iterdir()):
        if not char_dir.is_dir():
            continue

        metadata = load_metadata(char_dir)
        if not metadata:
            continue

        status = metadata.get("pipeline_status", {})

        completed = sum(1 for s in STAGES if status.get(s) == "complete")
        percent = completed / len(STAGES)

        name = metadata.get("name", char_dir.name)

        lines.append(f"### {name}")
        lines.append("")
        lines.append(f'<div class="pipeline-bar"><div style="width:{round(percent * 100)}%"></div></div>')
        lines.append(f"{round(percent * 100)}%")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Stage Completion")
    lines.append("")

    header = "| Character | " + " | ".join(STAGES) + " |"
    sep = "|---" * (len(STAGES) + 1) + "|"

    lines.append(header)
    lines.append(sep)

    for char_dir in sorted(CHAR_ROOT.iterdir()):
        if not char_dir.is_dir():
            continue

        metadata = load_metadata(char_dir)
        if not metadata:
            continue

        status = metadata.get("pipeline_status", {})
        name = metadata.get("name", char_dir.name)

        row = [name]

        for stage in STAGES:
            state = status.get(stage)

            if state == "complete":
                row.append('<span class="stage-complete">✓</span>')
            elif state == "partial":
                row.append('<span class="stage-partial">~</span>')
            else:
                row.append('<span class="stage-missing">✗</span>')

        lines.append("| " + " | ".join(row) + " |")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print("Pipeline dashboard generated")


if __name__ == "__main__":
    main()
