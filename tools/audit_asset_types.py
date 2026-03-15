import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

ASSET_TYPES = {
    # 01_IDENTITY
    "gallery-image": {
        "label": "01 Identity – Gallery Image",
        "patterns": ["gallery", "hero", "thumbnail", "portrait"],
        "folders": ["01_IDENTITY"],
    },
    "face-anchor": {
        "label": "01 Identity – Face Anchor Sheet",
        "patterns": ["face_anchor", "face_anchor_sheet"],
        "folders": ["01_IDENTITY"],
    },
    "face-front": {
        "label": "01 Identity – Face Front",
        "patterns": ["front_face", "face_front"],
        "folders": ["01_IDENTITY"],
    },
    "face-three-quarter": {
        "label": "01 Identity – Face Three-Quarter",
        "patterns": ["three_quarter_face", "face_three_quarter", "face_3q"],
        "folders": ["01_IDENTITY"],
    },
    "face-profile": {
        "label": "01 Identity – Face Profile",
        "patterns": ["profile_face", "face_profile", "side_face"],
        "folders": ["01_IDENTITY"],
    },
    "hair-sheet": {
        "label": "01 Identity – Hair Sheet",
        "patterns": ["hair_sheet"],
        "folders": ["01_IDENTITY"],
    },
    "expression-sheet": {
        "label": "01 Identity – Expression Sheet",
        "patterns": ["expression_sheet"],
        "folders": ["01_IDENTITY"],
    },
    "hand-sheet": {
        "label": "01 Identity – Hand Sheet",
        "patterns": ["hand_sheet"],
        "folders": ["01_IDENTITY"],
    },

    # 02_BODY
    "anatomy-sheet": {
        "label": "02 Body – Anatomy Sheet",
        "patterns": ["anatomy_sheet"],
        "folders": ["02_BODY"],
    },
    "anatomy-front": {
        "label": "02 Body – Anatomy Front",
        "patterns": ["anatomy_front"],
        "folders": ["02_BODY"],
    },
    "anatomy-side": {
        "label": "02 Body – Anatomy Side",
        "patterns": ["anatomy_side"],
        "folders": ["02_BODY"],
    },
    "anatomy-back": {
        "label": "02 Body – Anatomy Back",
        "patterns": ["anatomy_back"],
        "folders": ["02_BODY"],
    },
    "anatomy-glutes": {
        "label": "02 Body – Glute Reference",
        "patterns": ["glute_reference", "anatomy_glutes", "glute_anchor", "glute_sheet"],
        "folders": ["02_BODY"],
    },
    "body-anchor": {
        "label": "02 Body – Body Anchor Sheet",
        "patterns": ["body_anchor"],
        "folders": ["02_BODY"],
    },
    "proportion-grid": {
        "label": "02 Body – Proportion Grid",
        "patterns": ["proportion_grid", "body_proportions_grid"],
        "folders": ["02_BODY"],
    },
    "muscle-tension": {
        "label": "02 Body – Muscle Tension Sheet",
        "patterns": ["muscle_tension"],
        "folders": ["02_BODY"],
    },
    "silhouette-sheet": {
        "label": "02 Body – Silhouette Sheet",
        "patterns": ["silhouette_sheet", "silhouette"],
        "folders": ["02_BODY"],
    },
    "turnaround-sheet": {
        "label": "02 Body – Turnaround Sheet",
        "patterns": ["turnaround_sheet", "turnaround"],
        "folders": ["02_BODY"],
    },
    "height-scale": {
        "label": "02 Body – Height Scale Sheet",
        "patterns": ["height_scale", "scale_sheet"],
        "folders": ["02_BODY"],
    },

    # 03_UCS
    "ucs-sheet": {
        "label": "03 UCS – Ultimate Character Sheet",
        "patterns": ["ultimate_character_sheet", "final_ucs", "ucs"],
        "folders": ["03_UCS"],
    },
    "ucs-face-front": {
        "label": "03 UCS – Face Front",
        "patterns": ["ucs_face_front"],
        "folders": ["03_UCS"],
    },
    "ucs-face-three-quarter": {
        "label": "03 UCS – Face Three-Quarter",
        "patterns": ["ucs_face_three_quarter"],
        "folders": ["03_UCS"],
    },
    "ucs-face-profile": {
        "label": "03 UCS – Face Profile",
        "patterns": ["ucs_face_profile"],
        "folders": ["03_UCS"],
    },
    "ucs-expression": {
        "label": "03 UCS – Expression",
        "patterns": ["ucs_expression"],
        "folders": ["03_UCS"],
    },
    "ucs-body-front": {
        "label": "03 UCS – Body Front",
        "patterns": ["ucs_body_front"],
        "folders": ["03_UCS"],
    },
    "ucs-body-side": {
        "label": "03 UCS – Body Side",
        "patterns": ["ucs_body_side"],
        "folders": ["03_UCS"],
    },
    "ucs-silhouette": {
        "label": "03 UCS – Silhouette",
        "patterns": ["ucs_silhouette"],
        "folders": ["03_UCS"],
    },
    "ucs-dynamic-pose": {
        "label": "03 UCS – Dynamic Pose",
        "patterns": ["ucs_dynamic_pose", "dynamic_pose"],
        "folders": ["03_UCS"],
    },

    # 04_STYLE
    "signature-outfit": {
        "label": "04 Style – Signature Outfit Sheet",
        "patterns": ["signature_outfit", "outfit_signature"],
        "folders": ["04_STYLE"],
    },
    "design-language": {
        "label": "04 Style – Design Language Sheet",
        "patterns": ["design_language"],
        "folders": ["04_STYLE"],
    },
    "outfit-sheet": {
        "label": "04 Style – Outfit Sheet",
        "patterns": ["outfit_sheet"],
        "folders": ["04_STYLE"],
    },
    "wardrobe-sheet": {
        "label": "04 Style – Wardrobe Sheet",
        "patterns": ["wardrobe", "wardrobe_master"],
        "folders": ["04_STYLE"],
    },

    # 05_MOTION
    "pose-sheet": {
        "label": "05 Motion – Pose Sheet",
        "patterns": ["pose_sheet"],
        "folders": ["05_MOTION"],
    },
    "motion-anchor": {
        "label": "05 Motion – Motion Anchor Sheet",
        "patterns": ["motion_anchor", "motion_sheet"],
        "folders": ["05_MOTION"],
    },
    "interaction-anchor": {
        "label": "05 Motion – Interaction Anchor Sheet",
        "patterns": ["interaction_anchor"],
        "folders": ["05_MOTION"],
    },

    # 06_SCENES
    "scene-anchor": {
        "label": "06 Scenes – Scene Anchor Sheet",
        "patterns": ["scene_anchor", "scene_sheet", "lifestyle_scene_anchor"],
        "folders": ["06_SCENES"],
    },
    "prop-sheet": {
        "label": "06 Scenes – Prop Sheet",
        "patterns": ["prop_sheet"],
        "folders": ["06_SCENES"],
    },
}

NORMALIZED_SCENE_PATTERNS = {
    "scene_anchor",
    "scene_sheet",
    "lifestyle_scene_anchor",
    "interaction_anchor",
    "prop_sheet",
}

IGNORED_FOLDER_NAMES = {
    "00_source_references",
}


def is_image(path: pathlib.Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS


def rel_parts_lower(path: pathlib.Path) -> list[str]:
    rel = path.relative_to(CHARACTERS_ROOT)
    return [part.lower() for part in rel.parts]


def filename_lower(path: pathlib.Path) -> str:
    return path.stem.lower()


def should_consider_file(path: pathlib.Path) -> bool:
    parts = rel_parts_lower(path)
    name = filename_lower(path)

    if any(folder in parts for folder in IGNORED_FOLDER_NAMES):
        return False

    if "06_scenes" in parts:
        return any(pattern in name for pattern in NORMALIZED_SCENE_PATTERNS)

    return True


def collect_images() -> list[pathlib.Path]:
    images = []
    for character_dir in sorted(CHARACTERS_ROOT.iterdir()):
        if not character_dir.is_dir():
            continue
        for path in character_dir.rglob("*"):
            if is_image(path) and should_consider_file(path):
                images.append(path)
    return sorted(images)


def folder_matches(path: pathlib.Path, allowed_folders: list[str]) -> bool:
    parts = rel_parts_lower(path)
    return any(folder.lower() in parts for folder in allowed_folders)


def asset_matches(path: pathlib.Path, config: dict) -> bool:
    name = filename_lower(path)
    if not folder_matches(path, config["folders"]):
        return False
    return any(pattern.lower() in name for pattern in config["patterns"])


def classify_path(path: pathlib.Path) -> list[str]:
    matches = []
    for asset_key, config in ASSET_TYPES.items():
        if asset_matches(path, config):
            matches.append(asset_key)
    return matches


def character_name_from_path(path: pathlib.Path) -> str:
    return path.relative_to(CHARACTERS_ROOT).parts[0]


def print_grouped_report(grouped: dict[str, list[pathlib.Path]]) -> None:
    print("\n===== ASSET TYPE COVERAGE =====\n")
    for asset_key, config in ASSET_TYPES.items():
        paths = grouped.get(asset_key, [])
        characters = sorted({character_name_from_path(p) for p in paths})
        print(f"{asset_key:<22} | {config['label']}")
        print(f"  matches    : {len(paths)}")
        print(f"  characters : {', '.join(characters) if characters else '-'}")
        if paths:
            for p in paths:
                print(f"    - {p.relative_to(ROOT)}")
        print("")


def print_unmatched(unmatched: list[pathlib.Path]) -> None:
    print("\n===== UNMATCHED FILES =====\n")
    if not unmatched:
        print("None\n")
        return
    for p in unmatched:
        print(f"- {p.relative_to(ROOT)}")
    print("")


def print_multi_matched(multi: dict[pathlib.Path, list[str]]) -> None:
    print("\n===== MULTI-MATCHED FILES =====\n")
    if not multi:
        print("None\n")
        return
    for path, keys in multi.items():
        print(f"- {path.relative_to(ROOT)}")
        print(f"  matched: {', '.join(keys)}")
    print("")


def print_summary(grouped: dict[str, list[pathlib.Path]], unmatched: list[pathlib.Path], multi: dict[pathlib.Path, list[str]], total_images: int) -> None:
    populated = sum(1 for key in ASSET_TYPES if grouped.get(key))
    total = sum(len(v) for v in grouped.values())
    print("\n===== SUMMARY =====\n")
    print(f"Considered image files : {total_images}")
    print(f"Defined asset types    : {len(ASSET_TYPES)}")
    print(f"Populated asset types  : {populated}")
    print(f"Matched files          : {total}")
    print(f"Unmatched files        : {len(unmatched)}")
    print(f"Multi-matched files    : {len(multi)}")
    print("")


def main() -> None:
    images = collect_images()

    grouped: dict[str, list[pathlib.Path]] = defaultdict(list)
    unmatched: list[pathlib.Path] = []
    multi: dict[pathlib.Path, list[str]] = {}

    for path in images:
        matches = classify_path(path)

        if not matches:
            unmatched.append(path)
            continue

        if len(matches) > 1:
            multi[path] = matches

        for key in matches:
            grouped[key].append(path)

    print_summary(grouped, unmatched, multi, total_images=len(images))
    print_grouped_report(grouped)
    print_unmatched(unmatched)
    print_multi_matched(multi)


if __name__ == "__main__":
    main()
