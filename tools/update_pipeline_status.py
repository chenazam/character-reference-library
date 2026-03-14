import fnmatch
import pathlib
import yaml

try:
    from tools.library_index import build_library_index
except ModuleNotFoundError:
    from library_index import build_library_index




ROOT = pathlib.Path(__file__).resolve().parents[1]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

PIPELINE_RULES = {
    "face_anchor": ["*face_anchor*"],
    "hair_sheet": ["*hair_sheet*"],
    "anatomy_sheet": ["*anatomy_sheet*"],
    "body_anchor": ["*body_anchor*"],
    "proportion_grid": ["*proportion_grid*"],
    "muscle_tension": ["*muscle_tension*"],
    "silhouette_sheet": ["*silhouette*"],
    "turnaround_sheet": ["*turnaround*"],
    "expression_sheet": ["*expression_sheet*"],
    "hand_sheet": ["*hand_sheet*"],
    "gallery_image": ["*gallery*"],
    "ucs_core": ["*ucs_core*"],
    "signature_outfit": ["*signature_outfit*"],
    "design_language": ["*design_language*"],
    "wardrobe": [
        "*wardrobe_master*",
        "*outfit_01*",
        "*outfit_02*",
        "*outfit_03*",
        "*outfit_04*",
        "*outfit_05*",
    ],
    "pose_sheet": ["*pose_sheet*"],
    "motion_anchor": ["*motion_anchor*"],
    "height_scale": ["*height_scale*", "*height_lineup*", "*scale_sheet*"],
    "interaction_anchor": ["*interaction_anchor*"],
    "scene_anchor": ["*scene_anchor*", "*lifestyle_scene*"],
    "dynamic_pose": ["*dynamic_pose*"],
    "final_ucs": ["*final_ucs*"],
}


def pattern_matches_any_file(pattern: str, filenames: list[str]) -> bool:
    pattern = pattern.lower()
    return any(fnmatch.fnmatch(name, pattern) for name in filenames)


def evaluate_status(patterns: list[str], filenames: list[str]) -> str:
    if not filenames:
        return "not_started"

    matched = sum(
        1 for pattern in patterns
        if pattern_matches_any_file(pattern, filenames)
    )

    if matched == 0:
        return "not_started"
    if matched < len(patterns):
        return "partial"
    return "complete"


def main():
    library = build_library_index()

    for _, record in sorted(library.items()):
        character_dir = record["dir"]
        metadata = record["metadata"] or {}
        filenames = record["image_names"]

        metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"
        if not metadata_file.exists():
            continue

        if "pipeline_status" not in metadata:
            metadata["pipeline_status"] = {}

        for status_key, patterns in PIPELINE_RULES.items():
            metadata["pipeline_status"][status_key] = evaluate_status(patterns, filenames)

        metadata_file.write_text(
            yaml.dump(metadata, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

        print(f"Updated pipeline status for {character_dir.name}")


if __name__ == "__main__":
    main()
