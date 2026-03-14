import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHAR_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
OUTPUT = ROOT / "docs/pipeline/generation_queue.md"


PIPELINE_ORDER = [
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

        missing = [
            stage for stage in PIPELINE_ORDER
            if status.get(stage) != "complete"
        ]

        if not missing:
            continue

        lines.append(f"## {char_dir.name}")
        lines.append("")
        lines.append(f"- next: {missing[0]}")
        lines.append("")

    OUTPUT.write_text("\n".join(lines))

    print("Generation queue updated")


if __name__ == "__main__":
    main()
