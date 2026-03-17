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


def fallback_proportion_archetype(meta: dict) -> str:
    height_cm = get_nested(meta, "physical", "height_cm", default=0)
    build = get_nested(meta, "physical", "build_category", default="")
    anchor = get_nested(meta, "physical", "silhouette_anchor", default="")
    emphasis = get_nested(meta, "physical", "silhouette_emphasis", default="")
    keywords = set(get_nested(meta, "physical", "silhouette_keywords", default=[]) or [])

    anchor = str(anchor or "").strip()
    emphasis = str(emphasis or "").strip()
    build = str(build or "").strip()
    keywords = {str(k).strip() for k in keywords if str(k).strip()}

    
        # --- MUSCULAR / HEAVY TYPES (REFINED) ---

    if build in {"heavy_muscular"}:
        # Distinguish Danny vs Ragnar
        if height_cm and height_cm >= 195:
            return "massive_upper_dominant"   # Ragnar-tier
        return "heavy_muscular"               # Danny-tier


    if build in {"power_build", "broad_heavy", "thick_set", "large_frame"}:
        # Use silhouette emphasis if available
        emphasis = meta.get("silhouette_emphasis", "")

        if emphasis == "upper_body":
            return "massive_upper_dominant"

        return "massive_balanced"


    if build in {"athletic_muscular"}:
        # Split Hudson vs Daimon
        emphasis = meta.get("silhouette_emphasis", "")

        if emphasis == "upper_body":
            return "broad_upper_dominant"     # Daimon

        return "broad_athletic"               # Hudson

    if anchor == "power_athlete":
        if emphasis in {"balanced", "overall"}:
            return "broad_athletic"
        return "broad_upper_dominant"
    
    if build in {"compact_athletic"}:
        if emphasis in {"legs", "lower_body"} or "leg_dominant" in keywords:
            return "athletic_leg_dominant"    # Jasper
        return "compact_light"                # Luca
    
    if anchor == "elongated_slender":
        if emphasis in {"soft", "lower_curve", "glutes", "hips"}:
            return "slender_refined"
        return "slender_tall"
    
    if anchor == "glute_slender":
        return "slender_refined"

    if anchor in {"hip_dominant_soft", "soft_curvy"}:
        return "soft_curvy"

    archetype = None

    if build in {"soft_slender"}:
        archetype = "slender_refined"
    elif build in {"soft_heavy"}:
        archetype = "soft_curvy"
    elif build in {"narrow_slender", "elongated_slender"}:
        archetype = "slender_tall"
    elif build in {"balanced_athletic", "light_athletic"}:
        archetype = "athletic_balanced"
    elif build in {"runner_build", "lower_athletic"}:
        archetype = "athletic_leg_dominant"
    elif build in {"compact_athletic"}:
        if emphasis in {"legs", "lower_body"} or "leg_dominant" in keywords:
            return "athletic_leg_dominant"
        return "compact_light"

    if "compact" in keywords and archetype in {"athletic_balanced", "athletic_leg_dominant", None}:
        archetype = "compact_light"
    
    if "leg_dominant" in keywords and archetype in {"athletic_balanced", "broad_athletic", None}:
        archetype = "athletic_leg_dominant"
    
    if "upper_dominant" in keywords:
        if archetype in {"heavy_muscular", None}:
            archetype = "massive_upper_dominant"
        elif archetype in {"broad_athletic", "athletic_balanced", None}:
            archetype = "broad_upper_dominant"
    
    if keywords & {"curvy", "soft", "glute_dominant", "hip_dominant"}:
        if emphasis in {"glutes", "hips", "lower_curve", "soft"}:
            archetype = "soft_curvy"
        elif archetype in {"slender_tall", "slender_refined", None}:
            archetype = "slender_refined"
        else:
            archetype = "soft_curvy"
    
    if keywords & {"imposing", "massive", "heavy_set"}:
        if build == "soft_heavy" or anchor in {"hip_dominant_soft", "soft_curvy"}:
            archetype = "soft_curvy"
        elif emphasis in {"upper_body", "shoulders", "chest"} or "upper_dominant" in keywords:
            archetype = "massive_upper_dominant"
        else:
            archetype = "heavy_muscular"
    
    if "broad" in keywords and archetype in {"athletic_balanced", None}:
        archetype = "broad_athletic"

    if "agile" in keywords and archetype is None:
        archetype = "athletic_balanced"

    if emphasis in {"upper_body", "shoulders", "chest"}:
        if archetype in {"heavy_muscular"}:
            archetype = "massive_upper_dominant"
        elif archetype in {"broad_athletic", "athletic_balanced", None}:
            archetype = "broad_upper_dominant"
    
    elif emphasis in {"legs", "lower_body"}:
        if archetype in {"athletic_balanced", "compact_light", None}:
            archetype = "athletic_leg_dominant"
    
    elif emphasis in {"glutes", "hips", "lower_curve", "soft"}:
        if archetype not in {"massive_upper_dominant", "broad_upper_dominant"}:
            archetype = "soft_curvy"
    
    elif emphasis in {"balanced", "overall"}:
        if archetype == "broad_upper_dominant":
            archetype = "broad_athletic"
        elif archetype == "massive_upper_dominant":
            archetype = "heavy_muscular"
    
    if archetype is None:
        return "slender_tall"

    return archetype


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
