import fnmatch
import pathlib
import re
import yaml

try:
    from tools.library_index import build_library_index
except ModuleNotFoundError:
    from library_index import build_library_index


ROOT = pathlib.Path(__file__).resolve().parents[1]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

# These are the single-file reference assets we want to auto-resolve into metadata.reference_files
REFERENCE_RULES = {
    "face_anchor": ["*face_anchor*"],
    "anatomy_sheet": ["*anatomy_sheet*"],
    "body_anchor": ["*body_anchor*"],
    "silhouette_sheet": ["*silhouette_sheet*", "*silhouette*"],
    "turnaround_sheet": ["*turnaround_sheet*", "*turnaround*"],
    "ultimate_character_sheet": ["*ultimate_character_sheet*", "*final_ucs*", "*ucs*"],
    "signature_outfit_sheet": ["*signature_outfit*"],
}

# These are the pipeline status checks. Some map directly to reference files, others are broader.
PIPELINE_RULES = {
    "face_anchor": ["*face_anchor*"],
    "hair_sheet": ["*hair_sheet*"],
    "anatomy_sheet": ["*anatomy_sheet*"],
    "body_anchor": ["*body_anchor*"],
    "proportion_grid": ["*proportion_grid*"],
    "muscle_tension": ["*muscle_tension*"],
    "silhouette_sheet": ["*silhouette_sheet*", "*silhouette*"],
    "turnaround_sheet": ["*turnaround_sheet*", "*turnaround*"],
    "expression_sheet": ["*expression_sheet*"],
    "hand_sheet": ["*hand_sheet*"],
    "gallery_image": ["*gallery*"],
    "ucs": ["*ultimate_character_sheet*", "*final_ucs*", "*ucs*"],
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
    "motion_sheet": ["*motion_anchor*", "*motion_sheet*"],
    "scale_sheet": ["*height_scale*", "*height_lineup*", "*scale_sheet*"],
    "scene_anchors": ["*scene_anchor*", "*lifestyle_scene*"],
    "prop_sheet": ["*prop_sheet*"],
}

# Map reference_files keys to the corresponding pipeline_status keys
REFERENCE_TO_STATUS_KEY = {
    "face_anchor": "face_anchor",
    "anatomy_sheet": "anatomy_sheet",
    "body_anchor": "body_anchor",
    "silhouette_sheet": "silhouette_sheet",
    "turnaround_sheet": "turnaround_sheet",
    "ultimate_character_sheet": "ucs",
    "signature_outfit_sheet": "signature_outfit",
}


def pattern_matches_any_file(pattern: str, filenames: list[str]) -> bool:
    pattern = pattern.lower()
    return any(fnmatch.fnmatch(name.lower(), pattern) for name in filenames)


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


def extract_version(filename: str) -> int:
    """
    Supports names like:
    lucien_face_anchor_v1.png
    lucien_face_anchor_sheet_v12.png
    """
    match = re.search(r"_v(\d+)(?:\.[^.]+)?$", filename.lower())
    return int(match.group(1)) if match else -1


def find_best_match(patterns: list[str], filenames: list[str]) -> str:
    matches = []
    for name in filenames:
        lower_name = name.lower()
        if pathlib.Path(lower_name).suffix not in IMAGE_EXTENSIONS:
            continue
        if any(fnmatch.fnmatch(lower_name, pattern.lower()) for pattern in patterns):
            matches.append(name)

    if not matches:
        return ""

    # Prefer highest explicit version, then fall back to alphabetical for stability
    matches.sort(key=lambda n: (extract_version(n), n.lower()), reverse=True)
    return matches[0]


def ensure_metadata_sections(metadata: dict) -> None:
    metadata.setdefault("reference_files", {})
    metadata.setdefault("pipeline_status", {})


def update_reference_files(metadata: dict, filenames: list[str]) -> None:
    for ref_key, patterns in REFERENCE_RULES.items():
        best_match = find_best_match(patterns, filenames)
        metadata["reference_files"][ref_key] = best_match


def update_pipeline_status(metadata: dict, filenames: list[str]) -> None:
    # First: derive status from file patterns for all pipeline assets
    for status_key, patterns in PIPELINE_RULES.items():
        metadata["pipeline_status"][status_key] = evaluate_status(patterns, filenames)

    # Second: for the single-file reference assets, force complete/not_started based on reference_files
    # This keeps reference_files and pipeline_status in sync.
    for ref_key, status_key in REFERENCE_TO_STATUS_KEY.items():
        has_file = bool(metadata.get("reference_files", {}).get(ref_key, ""))
        metadata["pipeline_status"][status_key] = "complete" if has_file else "not_started"


def main():
    library = build_library_index()

    for _, record in sorted(library.items()):
        character_dir = record["dir"]
        metadata = record["metadata"] or {}
        filenames = record["image_names"]

        metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"
        if not metadata_file.exists():
            continue

        ensure_metadata_sections(metadata)
        update_reference_files(metadata, filenames)
        update_pipeline_status(metadata, filenames)

        metadata_file.write_text(
            yaml.dump(metadata, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

        print(f"Updated metadata for {character_dir.name}")


if __name__ == "__main__":
    main()
