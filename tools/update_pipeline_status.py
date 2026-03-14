import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"

PIPELINE_MAP = {
    "01_FACE": "face_anchor",
    "02_HAIR": "hair_sheet",
    "03_ANATOMY": "anatomy_sheet",
    "04_PROPORTIONS": "proportion_grid",
    "05_MUSCLE": "muscle_tension",
    "06_BODY": "body_anchor",
    "07_SILHOUETTE": "silhouette_sheet",
    "08_TURNAROUND": "turnaround_sheet",
    "09_EXPRESSIONS": "expression_sheet",
    "10_HANDS": "hand_sheet",
    "11_UCS": "ucs",
    "12_SIGNATURE_OUTFIT": "signature_outfit",
    "13_DESIGN_LANGUAGE": "design_language",
    "14_WARDROBE": "wardrobe",
    "15_POSES": "pose_sheet",
    "16_MOTION": "motion_sheet",
    "17_SCALE": "scale_sheet",
    "18_SCENES": "scene_anchors",
    "19_PROPS": "prop_sheet",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def stage_status(stage_dir):

    if not stage_dir.exists():
        return "not_started"

    images = [
        f for f in stage_dir.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if not images:
        return "not_started"

    if len(images) == 1:
        return "partial"

    return "complete"


def main():

    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):

        if not character_dir.is_dir():
            continue

        metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"

        if not metadata_file.exists():
            continue

        data = yaml.safe_load(metadata_file.read_text())

        if "pipeline_status" not in data:
            data["pipeline_status"] = {}

        for folder, key in PIPELINE_MAP.items():

            stage_dir = character_dir / folder

            status = stage_status(stage_dir)

            data["pipeline_status"][key] = status

        metadata_file.write_text(
            yaml.dump(data, sort_keys=False),
            encoding="utf-8",
        )

        print(f"Updated pipeline status for {character_dir.name}")


if __name__ == "__main__":
    main()