from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any
from dataclasses import dataclass



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
PAIRS_DIRNAME = "20_CHARACTER_PAIRS"
MASTER_BLOCKS_DIRNAME = "00_MASTER_BLOCKS"
RECIPES_DIRNAME = "00_PROMPT_RECIPES"

WHITESPACE_RE = re.compile(r"[ \t]+")
BLANKS_RE = re.compile(r"\n{3,}")


@dataclass
class DebugEvent:
    status: str   # LOAD, MISS, FAIL, SKIP
    label: str
    path: str | None = None
    detail: str | None = None


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


def resolve_latest_ucs(characters_root: Path, character: str) -> Path | None:
    base = characters_root / character
    if not base.exists():
        return None

    files = list(base.glob("*ucs*_v*.png"))
    if not files:
        return None

    def extract_version(p: Path):
        match = re.search(r"_v(\d+)", p.name)
        return int(match.group(1)) if match else -1

    return max(files, key=extract_version)


def resolve_latest_face_anchor(characters_root: Path, character: str) -> Path | None:
    base = characters_root / character / "01_IDENTITY" / "face"
    if not base.exists():
        return None

    files = list(base.glob("*face_anchor*_v*.png"))
    if not files:
        return None

    def extract_version(p: Path):
        match = re.search(r"_v(\d+)", p.name)
        return int(match.group(1)) if match else -1

    return max(files, key=extract_version)


def resolve_latest_height_sheet(pairs_root: Path, pair_id: str) -> Path | None:
    base = pairs_root / pair_id
    if not base.exists():
        return None

    files = list(base.glob("*height_comparison_v*.png"))
    if not files:
        return None

    def extract_version(p: Path):
        match = re.search(r"_v(\d+)", p.name)
        return int(match.group(1)) if match else -1

    return max(files, key=extract_version)


def stage_inputs(
    root: Path,
    characters_root: Path,
    pairs_root: Path,
    variables: dict[str, str],
    prompt_text: str,
):
    staging_dir = root / "tmp" / "prompt_inputs"

    # Clean folder
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    # Characters
    for key in ["character_id", "character_a", "character_b"]:
        char = variables.get(key)
        if not char:
            continue

        ucs = resolve_latest_ucs(characters_root, char)
        if ucs:
            shutil.copy2(ucs, staging_dir / ucs.name)
            print(f"[STAGE] Copied UCS: {ucs.name}")
        else:
            print(f"[STAGE] Missing UCS for {char}")

        face_anchor = resolve_latest_face_anchor(characters_root, char)
        if face_anchor:
            shutil.copy2(face_anchor, staging_dir / face_anchor.name)
            print(f"[STAGE] Copied face anchor: {face_anchor.name}")
        else:
            print(f"[STAGE] Missing face anchor for {char}")

    # Pair
    pair_id = variables.get("pair_id")
    if pair_id:
        sheet = resolve_latest_height_sheet(pairs_root, pair_id)
        if sheet:
            shutil.copy2(sheet, staging_dir / sheet.name)
            print(f"[STAGE] Copied height sheet: {sheet.name}")
        else:
            print(f"[STAGE] Missing height sheet for {pair_id}")

    # Prompt file
    (staging_dir / "00_prompt.txt").write_text(prompt_text, encoding="utf-8")

    print(f"[STAGE] Ready: {staging_dir}")


class PromptBuilderV2:
    def __init__(self, library_root: Path) -> None:
        self.library_root = library_root.resolve()
        self.prompts_root = self.library_root / PROMPTS_DIRNAME
        self.blocks_root = self.prompts_root / MASTER_BLOCKS_DIRNAME
        self.recipes_root = self.prompts_root / RECIPES_DIRNAME
        self.characters_root = self.library_root / CHARACTERS_DIRNAME
        self.pairs_root = self.library_root / PAIRS_DIRNAME
        self.debug_events: list[DebugEvent] = []


    def _record_event(self, status: str, label: str, path: Path | None = None, detail: str | None = None) -> None:
        self.debug_events.append(
            DebugEvent(
                status=status,
                label=label,
                path=str(path) if path else None,
                detail=detail,
            )
        )

    def _scoped_label_for_include(
        self, include_ref: str, variables: dict[str, str]
    ) -> tuple[str | None, str]:
        # Avoid hard failure on unresolved optional placeholders
        try:
            rendered = render_string(include_ref, variables)
        except PromptBuildError:
            rendered = include_ref

        char_a = variables.get("character_a", "A")
        char_b = variables.get("character_b", "B")

        # Character-specific outfit blocks
        if include_ref.startswith("characters/{character_a}/outfits/"):
            return ("A", f"Character A ({char_a}) - Outfit")

        if include_ref.startswith("characters/{character_b}/outfits/"):
            return ("B", f"Character B ({char_b}) - Outfit")

        # Character-specific wardrobe modes
        if include_ref.startswith("blocks/scene/wardrobe_modes/"):
            if "{mode_a_id}" in include_ref:
                return ("A", f"Character A ({char_a}) - Wardrobe mode")
            if "{mode_b_id}" in include_ref:
                return ("B", f"Character B ({char_b}) - Wardrobe mode")
            return (None, "Wardrobe mode")

        # Intensity
        if include_ref.startswith("blocks/scene/intensity/"):
            if "{intensity_a_id}" in include_ref:
                return ("A", f"Character A ({char_a}) - Intensity")
            if "{intensity_b_id}" in include_ref:
                return ("B", f"Character B ({char_b}) - Intensity")
            return (None, "Scene intensity")

        # Scenarios
        if rendered.startswith("blocks/scene/scenarios/") or rendered.startswith(
            f"pairs/{variables.get('pair_id', '')}/scenarios/"
        ):
            scenario = variables.get("scenario_id", "unknown")
            return (None, f"Scenario ({scenario})")

        # Environment context
        if include_ref.startswith("blocks/global/context/environment/"):
            if "{environment_a_id}" in include_ref:
                return ("A", f"Character A ({char_a}) - Environment context")
            if "{environment_b_id}" in include_ref:
                return ("B", f"Character B ({char_b}) - Environment context")
            return (None, "Environment context")

        return (None, rendered)

    def _wrap_scoped_block(self, include_ref: str, content: str, variables: dict[str, str]) -> str:
        _, label = self._scoped_label_for_include(include_ref, variables)
        return f"Apply the following only to {label}:\n{content.strip()}"

    def resolve_variable_values(self, variables: dict[str, str]) -> dict[str, str]:
        resolved: dict[str, str] = {}

        for key, value in variables.items():
            if value.startswith("blocks/") or value.startswith("characters/"):
                raw = self.load_block(value, variables)
                resolved[key] = raw
            else:
                resolved[key] = value

        return resolved

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

        if rendered.startswith("pairs/"):
            # shorthand:
            # pairs/{pair_id}/pair_core.md
            # -> 20_PAIRS/{pair_id}/pair_core.md
            parts = rendered_path.parts
            if len(parts) < 3:
                raise PromptBuildError(
                    f"Pair include must be at least pairs/<id>/<file>: {rendered}"
                )
            _, pair_id, *rest = parts
            return self.pairs_root / pair_id / Path(*rest)

        raise PromptBuildError(
            f"Unsupported include prefix in '{include_ref}'. "
            "Use 'blocks/...' or 'characters/...'."
        )

    def load_block(self, include_ref: str, variables: dict[str, str]) -> str:
        path = self.resolve_include_path(include_ref, variables)
        raw = strip_code_fence(read_text(path))
        return render_string(raw, variables)

    def load_block_optional_with_status(self, include_ref: str, variables: dict[str, str]) -> tuple[str | None, str, Path | None, str | None]:
        try:
            path = self.resolve_include_path(include_ref, variables)
        except PromptBuildError as exc:
            return None, "fail", None, str(exc)

        if not path.exists():
            return None, "miss", path, "file not found"

        raw = strip_code_fence(read_text(path))

        try:
            rendered = render_string(raw, variables)
            if not rendered.strip():
                return None, "skip", path, "rendered empty"
            return rendered, "load", path, None
        except PromptBuildError as exc:
            return None, "fail", path, str(exc)

    def build_prompt(
        self,
        recipe_ref: str,
        variables: dict[str, str],
        enabled_conditionals: set[str] | None = None,
        debug_blocks: bool = False,
    ) -> str:
        enabled_conditionals = enabled_conditionals or set()
        variables = self.resolve_variable_values(variables)
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
            content = self.load_block(item, variables)

            if debug_blocks:
                path = self.resolve_include_path(item, variables)
                relative = path.relative_to(self.library_root)
                header = f"\n--- BLOCK: {relative.as_posix()} ---\n"
                pieces.append(header + content)
            else:
                pieces.append(content)

        for item in optional_items:
            if not isinstance(item, str):
                raise PromptBuildError(
                    f"All recipe optional entries must be strings: {recipe_ref}"
                )

            loaded, status, path, detail = self.load_block_optional_with_status(item, variables)

            label = self._scoped_label_for_include(item, variables)[1]

            if status == "load" and loaded:
                wrapped = self._wrap_scoped_block(item, loaded, variables)

                if debug_blocks:
                    relative = path.relative_to(self.library_root) if path else None
                    header = f"\n--- BLOCK: {relative.as_posix()} ---\n" if relative else "\n--- BLOCK: <unknown> ---\n"
                    pieces.append(header + wrapped)
                else:
                    pieces.append(wrapped)

                self._record_event("LOAD", label, path)
            elif status == "miss":
                self._record_event("MISS", label, path, detail)
            elif status == "fail":
                self._record_event("FAIL", label, path, detail)
            else:
                self._record_event("SKIP", label, path, detail)

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
                    content = self.load_block(item, variables)

                    if debug_blocks:
                        path = self.resolve_include_path(item, variables)
                        relative = path.relative_to(self.library_root)
                        header = f"\n--- BLOCK: {relative.as_posix()} ---\n"
                        pieces.append(header + content)
                    else:
                        pieces.append(content)

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
        variables.setdefault("outfit_a_id", args.outfit)
        variables.setdefault("outfit_b_id", args.outfit)

    if getattr(args, "outfit_a", None):
        variables.setdefault("outfit_a_id", args.outfit_a)

    if getattr(args, "outfit_b", None):
        variables.setdefault("outfit_b_id", args.outfit_b)

    if getattr(args, "mode", None):
        variables.setdefault("mode_id", args.mode)
        variables.setdefault("mode_a_id", args.mode)
        variables.setdefault("mode_b_id", args.mode)

    if getattr(args, "mode_a", None):
        variables.setdefault("mode_a_id", args.mode_a)

    if getattr(args, "mode_b", None):
        variables.setdefault("mode_b_id", args.mode_b)

    if getattr(args, "environment", None):
        variables.setdefault("environment_id", args.environment)
        variables.setdefault("environment_a_id", args.environment)
        variables.setdefault("environment_b_id", args.environment)

    if getattr(args, "environment_a", None):
        variables.setdefault("environment_a_id", args.environment_a)

    if getattr(args, "environment_b", None):
        variables.setdefault("environment_b_id", args.environment_b)

    if getattr(args, "scene_block", None):
        variables.setdefault("scene_block", args.scene_block)

    if getattr(args, "character_a", None):
        variables.setdefault("character_a", args.character_a)

    if getattr(args, "character_b", None):
        variables.setdefault("character_b", args.character_b)

    if getattr(args, "pair", None):
        variables.setdefault("pair_id", args.pair)

    if getattr(args, "scenario", None):
        variables.setdefault("scenario_id", args.scenario)

    if getattr(args, "intensity", None):
        variables.setdefault("intensity_id", args.intensity)    

    if getattr(args, "scene_description", None):
        variables.setdefault("scene_description", args.scene_description)

    if getattr(args, "trigger", None):
        variables.setdefault("trigger_id", args.trigger)

    return variables


def main() -> None:
    parser = argparse.ArgumentParser(description="Build prompt from recipe + modular blocks")

    parser.add_argument(
        "--recipe",
        required=True,
        help="Recipe path relative to 00_PROMPT_RECIPES, e.g. reference/anatomy_side.yaml",
    )
    parser.add_argument("--scene-block", help="Scene block include ref, e.g. blocks/scene/descriptions/scene_neutral_presence.md")
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
    parser.add_argument(
        "--debug-blocks",
        action="store_true",
        help="Inject block filenames into prompt for debugging",
    )
    parser.add_argument(
        "--pair", 
        help="Pair id"
    )
    parser.add_argument(
        "--scenario", 
        help="Scenario id, e.g. grounding_hip_pull"
    )
    parser.add_argument(
        "--intensity", 
        help="Intensity id, e.g. level_3_charged"
    )
    parser.add_argument(
        "--intensity-a", 
        help="Intensity id for character A"
    )
    parser.add_argument(
        "--intensity-b", 
        help="Intensity id for character B"
    )
    parser.add_argument(
        "--outfit-a", 
        help="Outfit id for character A"
    )
    parser.add_argument(
        "--outfit-b", 
        help="Outfit id for character B"
    )
    parser.add_argument(
        "--mode", 
        help="Wardrobe mode id for single-character scene"
    )
    parser.add_argument(
        "--mode-a", 
        help="Wardrobe mode id for character A"
    )
    parser.add_argument(
        "--mode-b", 
        help="Wardrobe mode id for character B"
    )
    parser.add_argument(
        "--environment",
        help="Environment context id for single-character scene or shared pair scene, e.g. semi_private"
    )
    parser.add_argument(
        "--environment-a",
        help="Environment context id for character A"
    )
    parser.add_argument(
        "--environment-b",
        help="Environment context id for character B"
    )
    parser.add_argument(
        "--trigger",
        help="Trigger id for scene or pair interaction, e.g. attention_lock"
    )
    parser.add_argument(
        "--stage-inputs",
        action="store_true",
        help="Copy required input assets (UCS, pair height sheets) into staging folder",
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
            debug_blocks=args.debug_blocks,
        )

        if args.stage_inputs:
            stage_inputs(
                root=ROOT,
                characters_root=builder.characters_root,
                pairs_root=builder.pairs_root,
                variables=variables,
                prompt_text=final_prompt,
            )

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(final_prompt, encoding="utf-8")

        if args.debug_blocks and builder.debug_events:
            print("\n\n=== DEBUG BLOCK STATUS ===", file=sys.stderr)
            for event in builder.debug_events:
                msg = f"[{event.status}] {event.label}"
                if event.path:
                    msg += f" -> {event.path}"
                if event.detail:
                    msg += f" ({event.detail})"
                print(msg, file=sys.stderr)

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