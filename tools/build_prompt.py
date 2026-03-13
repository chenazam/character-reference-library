from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Dict


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = ROOT / "docs" / "assets" / "library" / "50_PROMPT_TEMPLATES"
MASTER_BLOCKS_ROOT = TEMPLATES_ROOT / "00_MASTER_BLOCKS"
CHARACTERS_ROOT = ROOT / "docs" / "assets" / "library" / "10_CHARACTERS"
BUILD_ROOT = ROOT / "build"

PLACEHOLDER_PATTERN = re.compile(r"\[([A-Z0-9_]+)\]")

TEMPLATE_ALIASES = {
    # 01_FACE_ANCHORS
    "face-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/face-anchor-sheet.md",
    "face-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/face-anchor-sheet.md",
    "front-face-reference": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/front-face-reference.md",
    "face-front": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/front-face-reference.md",
    "three-quarter-face-reference": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/three-quarter-face-reference.md",
    "face-three-quarter": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/three-quarter-face-reference.md",
    "profile-face-reference": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/profile-face-reference.md",
    "face-profile": "docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/profile-face-reference.md",

    # 02_HAIR
    "hair-reference-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_HAIR/hair-reference-sheet.md",
    "hair-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/02_HAIR/hair-reference-sheet.md",

    # 03_ANATOMY
    "anatomy-front": "docs/assets/library/50_PROMPT_TEMPLATES/03_ANATOMY/anatomy-front.md",
    "anatomy-side": "docs/assets/library/50_PROMPT_TEMPLATES/03_ANATOMY/anatomy-side.md",
    "anatomy-back": "docs/assets/library/50_PROMPT_TEMPLATES/03_ANATOMY/anatomy-back.md",
    "anatomy-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/03_ANATOMY/anatomy-sheet.md",

    # 04_PROPORTIONS
    "body-proportions-grid": "docs/assets/library/50_PROMPT_TEMPLATES/04_PROPORTIONS/body-proportions-grid.md",
    "proportions-grid": "docs/assets/library/50_PROMPT_TEMPLATES/04_PROPORTIONS/body-proportions-grid.md",

    # 05_MUSCLE
    "muscle-tension-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/05_MUSCLE/muscle-tension-sheet.md",
    "muscle-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/05_MUSCLE/muscle-tension-sheet.md",

    # 06_BODY
    "body-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/06_BODY/body-anchor-sheet.md",
    "body-anchor": "docs/assets/library/50_PROMPT_TEMPLATES/06_BODY/body-anchor-sheet.md",

    # 07_SILHOUETTE
    "silhouette-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/07_SILHOUETTE/silhouette-sheet.md",
    "silhouette": "docs/assets/library/50_PROMPT_TEMPLATES/07_SILHOUETTE/silhouette-sheet.md",

    # 08_TURNAROUND
    "turnaround-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/08_TURNAROUND/turnaround-sheet.md",
    "turnaround": "docs/assets/library/50_PROMPT_TEMPLATES/08_TURNAROUND/turnaround-sheet.md",

    # 09_EXPRESSIONS
    "expression-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/09_EXPRESSIONS/expression-sheet.md",
    "expressions": "docs/assets/library/50_PROMPT_TEMPLATES/09_EXPRESSIONS/expression-sheet.md",

    # 10_HANDS
    "hand-reference-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/10_HANDS/hand-reference-sheet.md",
    "hand-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/10_HANDS/hand-reference-sheet.md",

    # 11_UCS
    "ucs-face-front": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-face-front.md",
    "ucs-face-three-quarter": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-face-three-quarter.md",
    "ucs-face-profile": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-face-profile.md",
    "ucs-body-front": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-body-front.md",
    "ucs-body-side": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-body-side.md",
    "ucs-silhouette": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-silhouette.md",
    "ucs-expression": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-expression.md",
    "ucs-dynamic-pose": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-dynamic-pose.md",
    "ucs-assembly-notes": "docs/assets/library/50_PROMPT_TEMPLATES/11_UCS/ucs-assembly-notes.md",

    # 12_SIGNATURE_OUTFIT
    "signature-outfit-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/12_SIGNATURE_OUTFIT/signature-outfit-sheet.md",
    "signature-outfit": "docs/assets/library/50_PROMPT_TEMPLATES/12_SIGNATURE_OUTFIT/signature-outfit-sheet.md",

    # 13_DESIGN_LANGUAGE
    "design-language-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/13_DESIGN_LANGUAGE/design-language-sheet.md",
    "design-language": "docs/assets/library/50_PROMPT_TEMPLATES/13_DESIGN_LANGUAGE/design-language-sheet.md",

    # 14_WARDROBE
    "outfit-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/14_WARDROBE/outfit-sheet.md",
    "wardrobe-master-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/14_WARDROBE/wardrobe-master-sheet.md",
    "wardrobe-master": "docs/assets/library/50_PROMPT_TEMPLATES/14_WARDROBE/wardrobe-master-sheet.md",

    # 15_POSES
    "pose-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/15_POSES/pose-sheet.md",
    "pose": "docs/assets/library/50_PROMPT_TEMPLATES/15_POSES/pose-sheet.md",

    # 16_MOTION
    "motion-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/16_MOTION/motion-anchor-sheet.md",
    "motion-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/16_MOTION/motion-anchor-sheet.md",

    # 17_SCALE
    "height-scale-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/17_SCALE/height-scale-sheet.md",
    "height-scale": "docs/assets/library/50_PROMPT_TEMPLATES/17_SCALE/height-scale-sheet.md",

    # 18_INTERACTIONS
    "interaction-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/18_INTERACTIONS/interaction-anchor-sheet.md",
    "interaction-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/18_INTERACTIONS/interaction-anchor-sheet.md",

    # 19_SCENES
    "lifestyle-scene-anchor-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/19_SCENES/lifestyle-scene-anchor-sheet.md",
    "scene-sheet": "docs/assets/library/50_PROMPT_TEMPLATES/19_SCENES/lifestyle-scene-anchor-sheet.md",
}


def read_text(path: pathlib.Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def strip_code_fence(text: str) -> str:
    """
    Return the content of the last fenced code block if present.
    Otherwise return the stripped text.
    """
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


def print_available_aliases() -> None:
    print("Available template aliases:")
    for alias in sorted(TEMPLATE_ALIASES):
        print(f"  {alias} -> {TEMPLATE_ALIASES[alias]}")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("_", "-")
    value = re.sub(r"[^a-z0-9\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def derive_template_output_name(template_arg: str, template_path: pathlib.Path) -> str:
    """
    Prefer the alias the user passed in. If they passed a path, use the file stem.
    """
    if template_arg in TEMPLATE_ALIASES:
        return slugify(template_arg)
    return slugify(template_path.stem)


def derive_output_path(
    output_arg: str | None,
    character_arg: str,
    template_arg: str,
    template_path: pathlib.Path,
) -> pathlib.Path:
    """
    If --output is provided, use it.
    Otherwise auto-generate:
      build/[character]-[template].txt
    """
    if output_arg:
        return ROOT / output_arg

    character_slug = slugify(character_arg)
    template_slug = derive_template_output_name(template_arg, template_path)
    filename = f"{character_slug}-{template_slug}.txt"
    return BUILD_ROOT / filename


def load_master_blocks() -> Dict[str, str]:
    blocks: Dict[str, str] = {}

    for path in sorted(MASTER_BLOCKS_ROOT.glob("*.md")):
        key = normalize_placeholder_name(path.name)
        value = strip_code_fence(read_text(path))
        blocks[key] = value

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
            .replace("'", "")
            .replace('"', "")
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


def parse_params(param_args: list[str] | None) -> Dict[str, str]:
    params: Dict[str, str] = {}

    if not param_args:
        return params

    for item in param_args:
        if "=" not in item:
            raise ValueError(
                f"Invalid --param value '{item}'. Expected KEY=VALUE format."
            )

        key, value = item.split("=", 1)
        key = key.strip().upper()
        value = value.strip()

        if not key:
            raise ValueError(f"Invalid --param value '{item}'. Empty key.")

        if not re.fullmatch(r"[A-Z0-9_]+", key):
            raise ValueError(
                f"Invalid parameter key '{key}'. Use uppercase letters, numbers, and underscores only."
            )

        params[key] = value

    return params


def resolve_placeholders(text: str, values: Dict[str, str], max_passes: int = 20) -> str:
    result = text

    for _ in range(max_passes):
        changed = False

        def replacer(match: re.Match[str]) -> str:
            nonlocal changed
            key = match.group(1)
            if key in values:
                changed = True
                return values[key]
            return match.group(0)

        new_result = PLACEHOLDER_PATTERN.sub(replacer, result)
        result = new_result

        if not changed:
            break

    return result


def find_unresolved_placeholders(text: str) -> list[str]:
    return sorted(set(PLACEHOLDER_PATTERN.findall(text)))


def clean_final_prompt(text: str) -> str:
    cleaned = text
    cleaned = re.sub(r"^\s*Use:\s*$\n?", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def build_prompt(
    template_path: pathlib.Path,
    character_folder: str,
    params: Dict[str, str] | None = None,
) -> str:
    template_text = strip_code_fence(read_text(template_path))

    master_blocks = load_master_blocks()
    character_blocks = load_character_blocks(character_folder)
    runtime_params = params or {}

    values: Dict[str, str] = {}
    values.update(master_blocks)
    values.update(character_blocks)
    values.update(runtime_params)

    resolved = resolve_placeholders(template_text, values)
    resolved = clean_final_prompt(resolved)

    unresolved = find_unresolved_placeholders(resolved)
    if unresolved:
        unresolved_display = ", ".join(unresolved)
        raise ValueError(
            "Unresolved placeholders remain in the built prompt: "
            f"{unresolved_display}"
        )

    return resolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a final prompt from a template + master blocks + character blocks."
    )
    parser.add_argument(
        "--template",
        help=(
            "Template alias or repo-relative path. "
            "Example alias: face-front "
            "Example path: docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/front-face-reference.md"
        ),
    )
    parser.add_argument(
        "--character",
        help="Character folder name, e.g. LUCIEN",
    )
    parser.add_argument(
        "--output",
        help=(
            "Optional output file path, relative to repo root. "
            "If omitted, output is auto-generated as build/[character]-[template].txt"
        ),
    )
    parser.add_argument(
        "--param",
        action="append",
        help=(
            "Optional placeholder parameter in KEY=VALUE format. "
            "Can be repeated. Example: --param OUTFIT_CONCEPT='winter casual outfit'"
        ),
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the generated prompt to stdout. If used without --output, no file is written.",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available template aliases and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_templates:
        print_available_aliases()
        return 0

    if not args.template or not args.character:
        print(
            "Error: --template and --character are required unless --list-templates is used.",
            file=sys.stderr,
        )
        return 1

    try:
        params = parse_params(args.param)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    template_path = resolve_template_path(args.template)

    try:
        final_prompt = build_prompt(
            template_path=template_path,
            character_folder=args.character,
            params=params,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.stdout:
        print(final_prompt)
        if args.output:
            output_path = ROOT / args.output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(final_prompt, encoding="utf-8")
            print(f"\nBuilt prompt: {output_path}", file=sys.stderr)
        return 0

    output_path = derive_output_path(
        output_arg=args.output,
        character_arg=args.character,
        template_arg=args.template,
        template_path=template_path,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_prompt, encoding="utf-8")

    print(f"Built prompt: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())