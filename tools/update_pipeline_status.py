import fnmatch
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"

PIPELINE_RULES = {
    "01_FACE": {
        "status_key": "face_anchor",
        "required_patterns": [
            "*face_anchor*",
            "*front_face*",
            "*three_quarter_face*",
            "*profile_face*",
        ],
    },
    "02_HAIR": {
        "status_key": "hair_sheet",
        "required_patterns": [
            "*hair_sheet*",
        ],
    },
    "03_ANATOMY": {
        "status_key": "anatomy_sheet",
        "required_patterns": [
            "*anatomy_front*",
            "*anatomy_side*",
            "*anatomy_back*",
            "*anatomy_sheet*",
        ],
    },
    "04_PROPORTIONS": {
        "status_key": "proportion_grid",
        "required_patterns": [
            "*proportion_grid*",
        ],
    },
    "05_MUSCLE": {
        "status_key": "muscle_tension",
        "required_patterns": [
            "*muscle_tension*",
        ],
    },
    "06_BODY": {
        "status_key": "body_anchor",
        "required_patterns": [
            "*body_anchor*",
        ],
    },
    "07_SILHOUETTE": {
        "status_key": "silhouette_sheet",
        "required_patterns": [
            "*silhouette*",
        ],
    },
    "08_TURNAROUND": {
        "status_key": "turnaround_sheet",
        "required_patterns": [
            "*turnaround*",
        ],
    },
    "09_EXPRESSIONS": {
        "status_key": "expression_sheet",
        "required_patterns": [
            "*expression_sheet*",
        ],
    },
    "10_HANDS": {
        "status_key": "hand_sheet",
        "required_patterns": [
            "*hand_sheet*",
        ],
    },
    "11_UCS": {
        "status_key": "ucs",
        "required_patterns": [
            "*ucs*",
        ],
    },
    "12_SIGNATURE_OUTFIT": {
        "status_key": "signature_outfit",
        "required_patterns": [
            "*signature_outfit*",
        ],
    },
    "13_DESIGN_LANGUAGE": {
        "status_key": "design_language",
        "required_patterns": [
            "*design_language*",
        ],
    },
    "14_WARDROBE": {
        "status_key": "wardrobe",
        "required_patterns": [
            "*activity_outfit*",
            "*casual_outfit*",
            "*formal_outfit*",
            "*home_outfit*",
            "*work_outfit*",
        ],
    },
    "15_POSES": {
        "status_key": "pose_sheet",
        "required_patterns": [
            "*pose_sheet*",
        ],
    },
    "16_MOTION": {
        "status_key": "motion_sheet",
        "required_patterns": [
            "*motion_anchor*",
        ],
    },
    "17_SCALE": {
        "status_key": "scale_sheet",
        "required_patterns": [
            "*height_scale*",
            "*height_lineup*",
            "*scale_sheet*",
        ],
        "match_mode": "any",
    },
    "18_SCENES": {
        "status_key": "scene_anchors",
        "required_patterns": [
            "*scene_anchor*",
            "*lifestyle_scene*",
        ],
        "match_mode": "any",
    },
    "19_PROPS": {
        "status_key": "prop_sheet",
        "required_patterns": [
            "*prop_sheet*",
        ],
    },
    "20_GALLERY": {
        "status_key": "gallery_image",
        "required_patterns": [
            "*gallery*",
        ],
    },
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def get_image_names(stage_dir: pathlib.Path) -> list[str]:
    if not stage_dir.exists():
        return []

    return [
        p.name.lower()
        for p in stage_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]


def pattern_matches_any_file(pattern: str, filenames: list[str]) -> bool:
    pattern = pattern.lower()
    return any(fnmatch.fnmatch(name, pattern) for name in filenames)


def stage_status(stage_dir: pathlib.Path, rule: dict) -> str:
    filenames = get_image_names(stage_dir)
    if not filenames:
        return "not_started"

    patterns = rule["required_patterns"]
    match_mode = rule.get("match_mode", "all")

    matched_count = sum(
        1 for pattern in patterns
        if pattern_matches_any_file(pattern, filenames)
    )

    if match_mode == "any":
        return "complete" if matched_count > 0 else "not_started"

    if matched_count == 0:
        return "not_started"
    if matched_count < len(patterns):
        return "partial"
    return "complete"


def main():
    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not character_dir.is_dir():
            continue

        metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"
        if not metadata_file.exists():
            continue

        data = yaml.safe_load(metadata_file.read_text(encoding="utf-8")) or {}

        if "pipeline_status" not in data:
            data["pipeline_status"] = {}

        for folder, rule in PIPELINE_RULES.items():
            status_key = rule["status_key"]
            stage_dir = character_dir / folder
            data["pipeline_status"][status_key] = stage_status(stage_dir, rule)

        metadata_file.write_text(
            yaml.dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

        print(f"Updated pipeline status for {character_dir.name}")


if __name__ == "__main__":
    main()