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


PLACEHOLDER_PATTERN = re.compile(r"\[([A-Z0-9_]+)\]")


def read_text(path: pathlib.Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def strip_code_fence(text: str) -> str:
    """
    If a block file is mostly documentation + one fenced code block,
    return the fenced block content. Otherwise return the original text.
    """
    fence_pattern = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)
    matches = fence_pattern.findall(text)
    if len(matches) == 1:
        return matches[0].strip()
    return text.strip()


def normalize_placeholder_name(filename: str) -> str:
    """
    Convert filenames like:
      global-style-block.md -> GLOBAL_STYLE_BLOCK
      reference-sheet-block-stack.md -> REFERENCE_SHEET_BLOCK_STACK
    """
    stem = pathlib.Path(filename).stem
    return stem.upper().replace("-", "_")


def load_master_blocks() -> Dict[str, str]:
    """
    Load all .md files in 00_MASTER_BLOCKS and convert filenames to placeholder keys.
    Example:
      global-style-block.md -> GLOBAL_STYLE_BLOCK
    """
    blocks: Dict[str, str] = {}

    for path in sorted(MASTER_BLOCKS_ROOT.glob("*.md")):
        key = normalize_placeholder_name(path.name)
        value = strip_code_fence(read_text(path))
        blocks[key] = value

    return blocks


def parse_prompt_blocks_md(text: str) -> Dict[str, str]:
    """
    Parse sections from prompt_blocks.md.

    Example:
      ## Face Block
      ...
    becomes:
      FACE_BLOCK -> body text

    The parser assumes each block is introduced by a level-2 heading.
    """
    sections: Dict[str, str] = {}

    pattern = re.compile(
        r"^##\s+(.+?)\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    for match in pattern.finditer(text):
        raw_title = match.group(1).strip()
        raw_body = match.group(2).strip()

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
    """
    Load prompt_blocks.md from the given character and parse its ## sections.
    """
    prompt_blocks_path = (
        CHARACTERS_ROOT / character_folder / "00_PROFILE" / "prompt_blocks.md"
    )
    text = read_text(prompt_blocks_path)
    return parse_prompt_blocks_md(text)


def resolve_placeholders(text: str, values: Dict[str, str], max_passes: int = 20) -> str:
    """
    Recursively resolve placeholders like [GLOBAL_STYLE_BLOCK].

    Multiple passes are used so that block stacks can expand into other blocks.
    """
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
    found = sorted(set(PLACEHOLDER_PATTERN.findall(text)))
    return found


def build_prompt(template_path: pathlib.Path, character_folder: str) -> str:
    template_text = read_text(template_path).strip()

    master_blocks = load_master_blocks()
    character_blocks = load_character_blocks(character_folder)

    values: Dict[str, str] = {}
    values.update(master_blocks)
    values.update(character_blocks)

    resolved = resolve_placeholders(template_text, values)

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
        required=True,
        help=(
            "Path to template file, relative to repo root. "
            "Example: docs/assets/library/50_PROMPT_TEMPLATES/01_FACE_ANCHORS/face-anchor-sheet.md"
        ),
    )
    parser.add_argument(
        "--character",
        required=True,
        help="Character folder name, e.g. LUCIEN",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path, relative to repo root. Example: build/lucien-face-anchor.txt",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    template_path = ROOT / args.template
    output_path = ROOT / args.output

    try:
        final_prompt = build_prompt(template_path=template_path, character_folder=args.character)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_prompt, encoding="utf-8")

    print(f"Built prompt: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())