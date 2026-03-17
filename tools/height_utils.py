#!/usr/bin/env python3

from __future__ import annotations

import pathlib

try:
    from tools.site_paths import site_root_url
except ModuleNotFoundError:
    from site_paths import site_root_url


ROOT = pathlib.Path(__file__).resolve().parents[1]
REFERENCE_SILHOUETTE = ROOT / "docs" / "assets" / "reference" / "reference_male_average_180cm_front_v1.png"

SILHOUETTE_ARCHETYPES = {
    "slender_refined",
    "slender_tall",
    "compact_light",
    "athletic_balanced",
    "athletic_leg_dominant",
    "broad_athletic",
    "broad_upper_dominant",
    "heavy_muscular",
    "massive_upper_dominant",
    "soft_curvy",
}


def get_nested(data: dict, *keys, default=""):
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def extract_silhouette_signals(meta: dict) -> dict:
    return {
        "height_cm": get_nested(meta, "physical", "height_cm", default=0),
        "build": get_nested(meta, "physical", "build_category", default=""),
        "anchor": get_nested(meta, "physical", "silhouette_anchor", default=""),
        "emphasis": get_nested(meta, "physical", "silhouette_emphasis", default=""),
        "keywords": set(get_nested(meta, "physical", "silhouette_keywords", default=[]) or []),
    }


def fallback_proportion_archetype(meta: dict) -> str:
    s = extract_silhouette_signals(meta)

    height = s["height_cm"]
    build = s["build"]
    anchor = s["anchor"]
    emphasis = s["emphasis"]
    keywords = s["keywords"]

    # =========================================================
    # 1. SPECIFIC COMBINATION RULES (HIGHEST PRIORITY)
    # =========================================================

    # --- HEAVY MUSCULAR SPLIT (Danny vs Ragnar) ---
    if build == "heavy_muscular":
        if height >= 195:
            return "massive_upper_dominant"
        return "heavy_muscular"

    # --- ATHLETIC MUSCULAR SPLIT (Daimon vs Hudson) ---
    if build == "athletic_muscular":
        if emphasis == "upper_body":
            return "broad_upper_dominant"
        if emphasis in {"shoulders", "upper_frame"}:
            return "broad_athletic"
        return "broad_athletic"

    # --- COMPACT LOWER-BODY SPLIT (Jasper vs Luca) ---
    if build == "compact_athletic":
        if emphasis in {"legs", "lower_body"} or "leg_dominant" in keywords:
            return "athletic_leg_dominant"
        return "compact_light"

    # --- SOFT / CURVY ---
    if build in {"soft_heavy", "soft_curvy"}:
        return "soft_curvy"

    # =========================================================
    # 2. ANCHOR-BASED CLASSIFICATION
    # =========================================================

    if anchor == "runner_silhouette":
        return "athletic_leg_dominant"

    if anchor == "heroic_upper":
        return "broad_upper_dominant"

    if anchor == "balanced_athletic":
        return "athletic_balanced"

    if anchor == "compact_frame":
        return "compact_light"

    if anchor == "slender_frame":
        return "slender_refined"

    # =========================================================
    # 3. BUILD-BASED FALLBACKS
    # =========================================================

    if build in {"runner_build", "lower_athletic"}:
        return "athletic_leg_dominant"

    if build in {"balanced_athletic", "light_athletic"}:
        return "athletic_balanced"

    if build in {"athletic_muscular"}:
        return "broad_athletic"

    if build in {"power_build", "broad_heavy", "thick_set", "large_frame"}:
        if emphasis == "upper_body":
            return "massive_upper_dominant"
        return "heavy_muscular"

    # =========================================================
    # 4. KEYWORD / FINAL REFINEMENT
    # =========================================================

    if "massive" in keywords:
        return "massive_upper_dominant"

    if "broad_shoulders" in keywords:
        return "broad_upper_dominant"

    if "soft" in keywords or "curvy" in keywords:
        return "soft_curvy"

    # =========================================================
    # DEFAULT
    # =========================================================

    return "athletic_balanced"


def make_root_image_link(search_root: str | pathlib.Path, filename: str) -> str:
    if not filename:
        return ""

    root = pathlib.Path(search_root)
    matches = [p for p in root.rglob(filename) if p.is_file()]
    if not matches:
        return ""

    matches.sort()
    try:
        return site_root_url(matches[0])
    except Exception:
        return ""


def get_reference_silhouette_link() -> str:
    if not REFERENCE_SILHOUETTE.exists():
        return ""
    try:
        return site_root_url(REFERENCE_SILHOUETTE)
    except Exception:
        return ""


def build_reference_placeholder(height_pct: float) -> str:
    return (
        f'<div class="height-lineup__placeholder '
        f'height-lineup__placeholder--athletic_balanced '
        f'height-lineup__placeholder--reference" '
        f'style="height: {height_pct:.2f}%"></div>'
    )


def build_character_placeholder(archetype: str, height_pct: float) -> str:
    return (
        f'<div class="height-lineup__placeholder '
        f'height-lineup__placeholder--{archetype}" '
        f'style="height: {height_pct:.2f}%"></div>'
    )


def build_silhouette_img(src: str, alt: str, height_pct: float, reference: bool = False) -> str:
    classes = "height-lineup__silhouette"
    if reference:
        classes += " height-lineup__silhouette--reference"
    return (
        f'<img class="{classes}" '
        f'src="{src}" '
        f'alt="{alt}" '
        f'style="height: {height_pct:.2f}%;">'
    )
