from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # pip install pyyaml
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: PyYAML. Install with: pip install pyyaml"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY_ROOT = ROOT / "docs" / "assets" / "library"

PROMPTS_DIRNAME = "50_PROMPT_TEMPLATES"
CHARACTERS_DIRNAME = "10_CHARACTERS"
MASTER_BLOCKS_DIRNAME = "00_MASTER_BLOCKS"
RECIPES_DIRNAME = "00_PROMPT_RECIPES"

WHITESPACE_RE = re.compile(r"[ \t]+")
BLANKS_RE = re.compile(r"\n{3,}")


class PromptBuildError(RuntimeError):
    pass


def read_text(path: Path) -> str:
    if not path.exists():
        raise PromptBuildError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def normalize_for_model(text: str) -> str:
    replacements = {
        "\u2022": "- ",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u00b0": " degrees",
        "\u2192": "->",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = WHITESPACE_RE.sub(" ", text)
    text = BLANKS_RE.sub("\n\n", text)
    return text.strip()


def strip_code_fence(text: str) -> str:
    match = re.fullmatch(r"\s*```(?:\w+)?\n(.*?)\n?```\s*", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise PromptBuildError(f"Missing recipe file: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PromptBuildError(f"Recipe must be a YAML mapping: {path}")
    return data


def render_string(template: str, variables: dict[str, str]) -> str:
    try:
        return template.format(**variables)
    except KeyError as exc:
        missing = exc.args[0]
        raise PromptBuildError(
            f"Missing variable '{missing}' while rendering: {template}"
        ) from exc


class PromptBuilderV2:
    def __init__(self, library_root: Path) -> None:
        self.library_root = library_root.resolve()
        self.prompts_root = self.library_root / PROMPTS_DIRNAME
        self.blocks_root = self.prompts_root / MASTER_BLOCKS_DIRNAME
        self.recipes_root = self.prompts_root / RECIPES_DIRNAME
        self.characters_root = self.library_root / CHARACTERS_DIRNAME

    def recipe_path(self, recipe_ref: str) -> Path:
        recipe_path = self.recipes_root / recipe_ref
        if recipe_path.suffix.lower() != ".yaml":
            recipe_path = recipe_path.with_suffix(".yaml")
        return recipe_path

    def resolve_include_path(self, include_ref: str, variables: dict[str, str]) -> Path:
        rendered = render_string(include_ref, variables)
        rendered_path = Path(rendered)

        if rendered.startswith("blocks/"):
            relative = rendered_path.relative_to("blocks")
            return self.blocks_root / relative

        if rendered.startswith("characters/"):
            # shorthand:
            # characters/{character_id}/body.md
            # -> 10_CHARACTERS/{character_id}/00_PROFILE/blocks/body.md
            parts = rendered_path.parts
            if len(parts) < 3:
                raise PromptBuildError(
                    f"Character include must be at least characters/<id>/<file>: {rendered}"
                )
            _, character_id, *rest = parts
            return self.characters_root / character_id / "00_PROFILE" / "blocks" / Path(*rest)

        raise PromptBuildError(
            f"Unsupported include prefix in '{include_ref}'. "
            "Use 'blocks/...' or 'characters/...'."
        )

    def load_block(self, include_ref: str, variables: dict[str, str]) -> str:
        path = self.resolve_include_path(include_ref, variables)
        raw = strip_code_fence(read_text(path))
        return render_string(raw, variables)

    def load_block_optional(self, include_ref: str, variables: dict[str, str]) -> str | None:
        path = self.resolve_include_path(include_ref, variables)
        if not path.exists():
            return None
        raw = strip_code_fence(read_text(path))
        return render_string(raw, variables)

    def build_prompt(
        self,
        recipe_ref: str,
        variables: dict[str, str],
        enabled_conditionals: set[str] | None = None,
    ) -> str:
        enabled_conditionals = enabled_conditionals or set()
        recipe = load_yaml(self.recipe_path(recipe_ref))

        include_items = recipe.get("include", [])
        if not isinstance(include_items, list):
            raise PromptBuildError(f"'include' must be a list in recipe: {recipe_ref}")

        optional_items = recipe.get("optional", [])
        if optional_items and not isinstance(optional_items, list):
            raise PromptBuildError(f"'optional' must be a list in recipe: {recipe_ref}")

        pieces: list[str] = []

        for item in include_items:
            if not isinstance(item, str):
                raise PromptBuildError(
                    f"All recipe include entries must be strings: {recipe_ref}"
                )
            pieces.append(self.load_block(item, variables))

        for item in optional_items:
            if not isinstance(item, str):
                raise PromptBuildError(
                    f"All recipe optional entries must be strings: {recipe_ref}"
                )
            loaded = self.load_block_optional(item, variables)
            if loaded and loaded.strip():
                pieces.append(loaded)

        conditional_map = recipe.get("conditional", {})
        if conditional_map:
            if not isinstance(conditional_map, dict):
                raise PromptBuildError(
                    f"'conditional' must be a mapping in recipe: {recipe_ref}"
                )

            for condition_name, conditional_items in conditional_map.items():
                if condition_name not in enabled_conditionals:
                    continue

                if not isinstance(conditional_items, list):
                    raise PromptBuildError(
                        f"Conditional '{condition_name}' must map to a list in recipe: {recipe_ref}"
                    )

                for item in conditional_items:
                    if not isinstance(item, str):
                        raise PromptBuildError(
                            f"Conditional include entries must be strings: {recipe_ref}"
                        )
                    pieces.append(self.load_block(item, variables))

        final_text = "\n\n".join(piece.strip() for piece in pieces if piece.strip())
        return normalize_for_model(final_text)

    def recipe_debug_info(self, recipe_ref: str, variables: dict[str, str]) -> dict[str, Any]:
        recipe = load_yaml(self.recipe_path(recipe_ref))
        resolved: dict[str, Any] = {
            "recipe": recipe_ref,
            "name": recipe.get("name"),
            "includes": [],
            "optional": [],
            "conditional": {},
        }

        for item in recipe.get("include", []):
            resolved["includes"].append(str(self.resolve_include_path(item, variables)))

        for item in recipe.get("optional", []):
            resolved["optional"].append(str(self.resolve_include_path(item, variables)))

        conditional_map = recipe.get("conditional", {})
        for condition_name, conditional_items in conditional_map.items():
            resolved["conditional"][condition_name] = [
                str(self.resolve_include_path(item, variables)) for item in conditional_items
            ]

        return resolved


def parse_kv_pairs(items: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    if not items:
        return result

    for item in items:
        if "=" not in item:
            raise PromptBuildError(f"Expected KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def copy_to_clipboard(text: str) -> None:
    try:
        import subprocess

        subprocess.run(["clip"], input=text, text=True, check=True)
    except Exception as exc:
        raise PromptBuildError(f"Clipboard copy failed: {exc}") from exc


def build_default_variables(args: argparse.Namespace) -> dict[str, str]:
    variables = parse_kv_pairs(args.var)

    if args.character:
        variables.setdefault("character_id", args.character)

    if args.region:
        variables.setdefault("region", args.region)

    if getattr(args, "outfit", None):
        variables.setdefault("outfit_id", args.outfit)

    if getattr(args, "character_a", None):
        variables.setdefault("character_a", args.character_a)

    if getattr(args, "character_b", None):
        variables.setdefault("character_b", args.character_b)

    if getattr(args, "scene_description", None):
        variables.setdefault("scene_description", args.scene_description)

    return variables


def main() -> None:
    parser = argparse.ArgumentParser(description="Build prompt from recipe + modular blocks")

    parser.add_argument(
        "--recipe",
        required=True,
        help="Recipe path relative to 00_PROMPT_RECIPES, e.g. reference/anatomy_side.yaml",
    )
    parser.add_argument(
        "--character",
        help="Character folder name / id used for characters/{character_id}/...",
    )
    parser.add_argument("--character-a", help="First character id")
    parser.add_argument("--character-b", help="Second character id")
    parser.add_argument("--scene-description", help="Freeform scene description")
    parser.add_argument(
        "--region",
        help="Optional specialized anatomy region, e.g. glutes",
    )
    parser.add_argument(
        "--var",
        action="append",
        help="Additional template variable as KEY=VALUE. Can be repeated.",
    )
    parser.add_argument(
        "--outfit",
        help="Outfit id used for characters/{character_id}/outfits/{outfit_id}.md",
    )
    parser.add_argument(
        "--enable",
        action="append",
        default=[],
        help="Enable a conditional section, e.g. --enable references_attached",
    )
    parser.add_argument(
        "--library-root",
        type=Path,
        default=DEFAULT_LIBRARY_ROOT,
        help="Override library root. Defaults to [ROOT]/docs/assets/library",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write final prompt to this file",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print final prompt to stdout",
    )
    parser.add_argument(
        "--json-debug",
        action="store_true",
        help="Print resolved recipe/block paths as JSON",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Do not copy final prompt to clipboard",
    )

    args = parser.parse_args()

    try:
        builder = PromptBuilderV2(args.library_root)
        variables = build_default_variables(args)
        enabled_conditionals = set(args.enable)

        if args.json_debug:
            debug_payload = builder.recipe_debug_info(args.recipe, variables)
            print(json.dumps(debug_payload, indent=2))
            return

        final_prompt = builder.build_prompt(
            recipe_ref=args.recipe,
            variables=variables,
            enabled_conditionals=enabled_conditionals,
        )

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(final_prompt, encoding="utf-8")

        if args.stdout:
            print(final_prompt)

        if not args.no_clipboard:
            copy_to_clipboard(final_prompt)

    except PromptBuildError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # last-resort guardrail
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()