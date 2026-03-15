import pathlib
import re
import yaml
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"
SNIPPETS_ROOT = ROOT / "docs/snippets/comparisons"

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

CHARACTER_ORDER = [
    "blake",
    "daimon",
    "danny",
    "dennis",
    "hudson",
    "jasper",
    "jonah",
    "luca",
    "lucien",
    "tommy",
]


def load_metadata(character_dir: pathlib.Path) -> dict:
    metadata_file = character_dir / "00_PROFILE" / "metadata.yaml"
    if not metadata_file.exists():
        return {}

    try:
        with metadata_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def include_character_in_comparisons(character_dir: pathlib.Path) -> bool:
    metadata = load_metadata(character_dir)
    site_visibility = metadata.get("site_visibility", {})

    # default to True so older characters without the field still appear
    return site_visibility.get("list_in_character_index", True)


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
        if not include_character_in_comparisons(character_dir):
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
    return path.relative_to(CHARACTERS_ROOT).parts[0].lower()


def site_root_url(target_under_docs: pathlib.Path) -> str:
    return "/" + target_under_docs.relative_to(DOCS_ROOT).as_posix()


VERSION_PATTERN = re.compile(r"_v(\d+)$", re.IGNORECASE)


def extract_version(path: pathlib.Path) -> int:
    match = VERSION_PATTERN.search(path.stem)
    if not match:
        return -1
    return int(match.group(1))


def canonical_bonus(path: pathlib.Path) -> int:
    stem = path.stem.lower()
    return 1 if "_rear" not in stem and "_alt" not in stem and "_crop" not in stem else 0


def choose_best_image(paths: list[pathlib.Path]) -> pathlib.Path:
    return sorted(
        paths,
        key=lambda p: (
            -canonical_bonus(p),
            -extract_version(p),  # highest version wins
            len(p.stem),
            p.stem.lower(),
        ),
    )[0]


def character_sort_key(name: str) -> tuple[int, str]:
    lowered = name.lower()
    if lowered in CHARACTER_ORDER:
        return (0, CHARACTER_ORDER.index(lowered))
    return (1, lowered)


def titleize_character(name: str) -> str:
    return name.capitalize()


def build_character_page_link(character_slug: str) -> str:
    return f"/characters/{character_slug}/"


def build_asset_snippet(asset_key: str, paths_by_character: dict[str, list[pathlib.Path]]) -> str:
    lines = []
    lines.append('<div class="comparison-grid">')
    lines.append("")

    for character in sorted(paths_by_character.keys(), key=character_sort_key):
        best_image = choose_best_image(paths_by_character[character])
        image_rel = site_root_url(best_image)
        char_page_rel = build_character_page_link(character)
        display_name = titleize_character(character)

        lines.append('  <div class="comparison-card">')
        lines.append(f'    <h3><a href="{char_page_rel}">{display_name}</a></h3>')
        lines.append(f'    <a href="{image_rel}" target="_blank">')
        lines.append(f'      <img src="{image_rel}" alt="{display_name} {asset_key}">')
        lines.append("    </a>")
        lines.append("  </div>")
        lines.append("")

    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    SNIPPETS_ROOT.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, dict[str, list[pathlib.Path]]] = {
        key: defaultdict(list) for key in ASSET_TYPES
    }

    for path in collect_images():
        matches = classify_path(path)
        if not matches:
            continue

        character = character_name_from_path(path)
        for asset_key in matches:
            grouped[asset_key][character].append(path)

    generated = 0

    for asset_key, config in ASSET_TYPES.items():
        paths_by_character = grouped.get(asset_key, {})
        if not paths_by_character:
            continue

        snippet = build_asset_snippet(asset_key, paths_by_character)
        out_path = SNIPPETS_ROOT / f"{asset_key}.md"
        out_path.write_text(snippet, encoding="utf-8")
        generated += 1
        print(f"Generated {out_path.relative_to(ROOT)} ({config['label']})")

    print(f"\nGenerated {generated} comparison snippets.")


if __name__ == "__main__":
    main()
