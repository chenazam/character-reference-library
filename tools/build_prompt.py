from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Dict, List


ROOT = pathlib.Path(__file__).resolve().parents[1]

TEMPLATES_ROOT = ROOT / "docs" / "assets" / "library" / "50_PROMPT_TEMPLATES"
MASTER_BLOCKS_ROOT = TEMPLATES_ROOT / "00_MASTER_BLOCKS"
CHARACTERS_ROOT = ROOT / "docs" / "assets" / "library" / "10_CHARACTERS"

BUILD_ROOT = ROOT / "build"

PLACEHOLDER_PATTERN = re.compile(r"\[([A-Z0-9_]+)\]")


TEMPLATE_ALIASES = {
    # Identity
    "face-front": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/front-face-reference.md",
    "front-face": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/front-face-reference.md",

    "face-three-quarter": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/three-quarter-face-reference.md",
    "three-quarter-face": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/three-quarter-face-reference.md",

    "face-profile": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/profile-face-reference.md",
    "profile-face": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/profile-face-reference.md",

    "face-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/face-anchor-sheet.md",

    "hair-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/hair-reference-sheet.md",

    "expression-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/expression-sheet.md",
    "expressions": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/expression-sheet.md",

    "hand-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/hand-reference-sheet.md",
    "hands": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/hand-reference-sheet.md",

    "gallery-image": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/gallery-image.md",
    "thumbnail": "docs/assets/library/50_PROMPT_TEMPLATES/01_IDENTITY/gallery-image.md",

    # Body
    "anatomy-front": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/anatomy-front.md",
    "anatomy-side": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/anatomy-side.md",
    "anatomy-back": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/anatomy-back.md",
    "anatomy-glutes": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/anatomy-glutes.md",
    "anatomy-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/anatomy-sheet.md",

    "body-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/body-anchor-sheet.md",

    "proportion-grid": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/body-proportions-grid.md",
    "body-proportions-grid": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/body-proportions-grid.md",

    "muscle-tension": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/muscle-tension-sheet.md",
    "muscle-tension-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/muscle-tension-sheet.md",

    "silhouette": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/silhouette-sheet.md",
    "silhouette-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/silhouette-sheet.md",

    "turnaround": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/turnaround-sheet.md",
    "turnaround-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/turnaround-sheet.md",

    "height-scale": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/height-scale-sheet.md",
    "height-scale-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_BODY/height-scale-sheet.md",

    # UCS
    "ucs-face-front": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-face-front.md",
    "ucs-front-face": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-face-front.md",

    "ucs-face-three-quarter": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-face-three-quarter.md",
    "ucs-three-quarter-face": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-face-three-quarter.md",

    "ucs-face-profile": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-face-profile.md",
    "ucs-profile-face": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-face-profile.md",

    "ucs-expression": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-expression.md",
    "ucs-expression-panel": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-expression.md",

    "ucs-body-front": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-body-front.md",
    "ucs-body-front-panel": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-body-front.md",

    "ucs-body-side": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-body-side.md",
    "ucs-body-side-panel": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-body-side.md",

    "ucs-silhouette": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-silhouette.md",
    "ucs-silhouette-panel": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-silhouette.md",

    "ucs-dynamic-pose": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-dynamic-pose.md",
    "dynamic-pose": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-dynamic-pose.md",

    "ucs-assembly-notes": "docs/assets/library/50_PROMPT_TEMPLATES/03_UCS/ucs-assembly-notes.md",

    # Style
    "signature-outfit": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/signature-outfit-sheet.md",
    "signature-outfit-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/signature-outfit-sheet.md",

    "design-language": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/design-language-sheet.md",
    "design-language-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/design-language-sheet.md",

    "outfit-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/outfit-sheet.md",
    "outfit": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/outfit-sheet.md",

    "wardrobe-master": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/wardrobe-master-sheet.md",
    "wardrobe-master-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/04_STYLE/wardrobe-master-sheet.md",

    # Motion
    "pose-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/05_MOTION/pose-sheet.md",

    "motion-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/05_MOTION/motion-anchor-sheet.md",
    "motion-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/05_MOTION/motion-anchor-sheet.md",
    "motion-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/05_MOTION/motion-anchor-sheet.md",

    "interaction-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/05_MOTION/interaction-anchor-sheet.md",
    "interaction-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/05_MOTION/interaction-anchor-sheet.md",

    # Scenes
    "scene-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/06_SCENES/lifestyle-scene-anchor-sheet.md",
    "lifestyle-scene-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/06_SCENES/lifestyle-scene-anchor-sheet.md",
    "lifestyle-scene-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/06_SCENES/lifestyle-scene-anchor-sheet.md",
}



def read_text(path: pathlib.Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def strip_code_fence(text: str) -> str:
    fence_pattern = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)
    matches = fence_pattern.findall(text)
    if matches:
        return matches[-1].strip()
    return text.strip()


def normalize_placeholder_name(filename: str) -> str:
    stem = pathlib.Path(filename).stem
    return stem.upper().replace("-", "_")


def resolve_template_path(template_arg: str) -> pathlib.Path:
    if template_arg in TEMPLATE_ALIASES:
        return ROOT / TEMPLATE_ALIASES[template_arg]
    return ROOT / template_arg


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("_", "-")
    value = re.sub(r"[^a-z0-9\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def derive_output_path(character_names: List[str], template_name: str):
    char_slug = "-".join(slugify(c) for c in character_names)
    template_slug = slugify(template_name)
    filename = f"{char_slug}-{template_slug}.txt"
    return BUILD_ROOT / filename


def load_master_blocks() -> Dict[str, str]:
    blocks: Dict[str, str] = {}

    for path in MASTER_BLOCKS_ROOT.glob("*.md"):
        key = normalize_placeholder_name(path.name)
        blocks[key] = strip_code_fence(read_text(path))

    return blocks


def parse_prompt_blocks_md(text: str) -> Dict[str, str]:
    sections: Dict[str, str] = {}

    pattern = re.compile(
        r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    for match in pattern.finditer(text):
        raw_title = match.group(1).strip()
        raw_body = match.group(2).strip()

        raw_body = re.sub(
            r"Use for:\s*(?:\n|\r\n)?(?:\s*-\s.+(?:\n|\r\n)?)+",
            "",
            raw_body,
            flags=re.IGNORECASE,
        ).strip()

        key = (
            raw_title.upper()
            .replace("&", "AND")
            .replace("/", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
        )

        key = re.sub(r"\s+", "_", key)
        key = re.sub(r"_+", "_", key).strip("_")

        sections[key] = raw_body

    return sections


def load_character_blocks(character_folder: str) -> Dict[str, str]:
    prompt_blocks_path = (
        CHARACTERS_ROOT / character_folder / "00_PROFILE" / "prompt_blocks.md"
    )
    text = read_text(prompt_blocks_path)
    return parse_prompt_blocks_md(text)


def load_multiple_character_blocks(character_names: List[str]) -> Dict[str, str]:
    combined_blocks: Dict[str, str] = {}

    character_blocks = []

    for name in character_names:
        blocks = load_character_blocks(name)

        if "CHARACTER_BLOCK" not in blocks:
            raise ValueError(f"{name} missing CHARACTER_BLOCK")

        character_blocks.append(blocks["CHARACTER_BLOCK"])

    combined_blocks["CHARACTER_BLOCKS"] = "\n\n".join(character_blocks)

    return combined_blocks


def resolve_placeholders(text: str, values: Dict[str, str]) -> str:
    result = text

    for _ in range(20):
        changed = False

        def replacer(match):
            nonlocal changed
            key = match.group(1)

            if key in values:
                changed = True
                return values[key]

            return match.group(0)

        result = PLACEHOLDER_PATTERN.sub(replacer, result)

        if not changed:
            break

    return result


def clean_final_prompt(text: str) -> str:
    cleaned = re.sub(r"\n{3,}", "\n\n", text)
    return cleaned.strip()


def build_prompt(
    template_path,
    character_folder=None,
    character_list=None,
    params=None,
):

    template_text = strip_code_fence(read_text(template_path))

    master_blocks = load_master_blocks()

    values: Dict[str, str] = {}
    values.update(master_blocks)

    if character_folder:
        values.update(load_character_blocks(character_folder))

    if character_list:
        values.update(load_multiple_character_blocks(character_list))

    if params:
        values.update(params)

    resolved = resolve_placeholders(template_text, values)

    return clean_final_prompt(resolved)


def parse_params(param_args):
    params = {}

    if not param_args:
        return params

    for item in param_args:
        key, value = item.split("=", 1)
        params[key.strip().upper()] = value.strip()

    return params


def main():

    parser = argparse.ArgumentParser(
        description="Build prompt from template + blocks"
    )

    parser.add_argument("--template")

    parser.add_argument("--character")
    parser.add_argument("--characters", nargs="+")

    parser.add_argument("--output")

    parser.add_argument("--stdout", action="store_true")

    parser.add_argument("--param", action="append")

    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available template aliases and exit",
    )

    args = parser.parse_args()

    if args.list_templates:
        print("Available template aliases:\n")

        for alias, path in sorted(TEMPLATE_ALIASES.items()):
            print(f"{alias:<20} -> {path}")

        sys.exit(0)

    if not args.template:
        print("Error: Provide --template", file=sys.stderr)
        sys.exit(1)

    if not args.character and not args.characters:
        print("Error: Provide --character or --characters", file=sys.stderr)
        sys.exit(1)

    template_path = resolve_template_path(args.template)

    params = parse_params(args.param)

    character_list = []

    if args.character:
        character_list.append(args.character)

    if args.characters:
        character_list.extend(args.characters)

    final_prompt = build_prompt(
        template_path=template_path,
        character_folder=args.character,
        character_list=args.characters,
        params=params,
    )

    if args.stdout:
        print(final_prompt)

    if not args.stdout or args.output:

        output_path = (
            ROOT / args.output
            if args.output
            else derive_output_path(character_list, args.template)
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(final_prompt, encoding="utf-8")

        print(f"Built prompt: {output_path}")


if __name__ == "__main__":
    main()