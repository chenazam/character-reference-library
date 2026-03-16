import pathlib

def get_nested(data: dict, *keys, default=""):
    cur = data
    for key in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
        if cur is None:
            return default
    return cur


def fallback_proportion_archetype(meta: dict) -> str:
    anchor = get_nested(meta, "physical", "silhouette_anchor", default="")
    emphasis = get_nested(meta, "physical", "silhouette_emphasis", default="")
    build = get_nested(meta, "physical", "build_category", default="")
    keywords = set(get_nested(meta, "physical", "silhouette_keywords", default=[]) or [])

    # Normalize values to strings
    anchor = str(anchor or "").strip()
    emphasis = str(emphasis or "").strip()
    build = str(build or "").strip()
    keywords = {str(k).strip() for k in keywords if str(k).strip()}

    # Strong direct anchor mappings
    if anchor == "power_frame":
        return "massive_upper_dominant"

    if anchor == "power_athlete":
        if emphasis in {"balanced", "overall"}:
            return "broad_balanced"
        return "broad_upper_dominant"

    if anchor == "runner_silhouette":
        if "compact" in keywords:
            return "compact_athletic"
        return "athletic_leg_dominant"

    if anchor == "elongated_slender":
        if emphasis in {"soft", "lower_curve", "glutes", "hips"}:
            return "slender_soft"
        return "slender_tall"

    if anchor == "glute_slender":
        return "slender_soft"

    # Build-category defaults
    archetype = None

    if build in {"soft_slender"}:
        archetype = "slender_soft"
    elif build in {"narrow_slender", "elongated_slender"}:
        archetype = "slender_tall"
    elif build in {"balanced_athletic", "light_athletic"}:
        archetype = "athletic_balanced"
    elif build in {"runner_build", "lower_athletic"}:
        archetype = "athletic_leg_dominant"
    elif build in {"compact_athletic"}:
        archetype = "compact_athletic"
    elif build in {"athletic_muscular"}:
        archetype = "broad_balanced"
    elif build in {"power_build", "heavy_muscular", "broad_heavy", "thick_set", "large_frame"}:
        archetype = "massive_balanced"

    # Keyword refinements
    if "compact" in keywords and archetype in {"athletic_balanced", "athletic_leg_dominant", None}:
        archetype = "compact_athletic"

    if "leg_dominant" in keywords and archetype in {"athletic_balanced", "broad_balanced", None}:
        archetype = "athletic_leg_dominant"

    if "upper_dominant" in keywords:
        if archetype in {"massive_balanced", None}:
            archetype = "massive_upper_dominant"
        elif archetype in {"broad_balanced", "athletic_balanced", None}:
            archetype = "broad_upper_dominant"

    if keywords & {"curvy", "soft", "glute_dominant", "hip_dominant"}:
        if archetype in {"slender_tall", "slender_soft", None}:
            archetype = "slender_soft"
        else:
            archetype = "soft_curvy"

    if keywords & {"imposing", "massive", "heavy_set"}:
        if emphasis in {"upper_body", "shoulders", "chest"} or "upper_dominant" in keywords:
            archetype = "massive_upper_dominant"
        else:
            archetype = "massive_balanced"

    if "broad" in keywords and archetype in {"athletic_balanced", None}:
        archetype = "broad_balanced"

    if "agile" in keywords and archetype is None:
        archetype = "athletic_balanced"

    # Emphasis refinements
    if emphasis in {"upper_body", "shoulders", "chest"}:
        if archetype in {"massive_balanced"}:
            archetype = "massive_upper_dominant"
        elif archetype in {"broad_balanced", "athletic_balanced", None}:
            archetype = "broad_upper_dominant"

    elif emphasis in {"legs", "lower_body"}:
        if archetype in {"athletic_balanced", "compact_athletic", None}:
            archetype = "athletic_leg_dominant"

    elif emphasis in {"glutes", "hips", "lower_curve", "soft"}:
        if archetype in {"slender_tall", "slender_soft", None}:
            archetype = "slender_soft"
        elif archetype not in {"massive_upper_dominant", "broad_upper_dominant"}:
            archetype = "soft_curvy"

    elif emphasis in {"balanced", "overall"}:
        if archetype == "broad_upper_dominant":
            archetype = "broad_balanced"
        elif archetype == "massive_upper_dominant":
            archetype = "massive_balanced"

    # Final fallback
    if archetype is None:
        return "slender_tall"

    return archetype


def height_percent(height: int, max_height: int) -> float:
    if max_height <= 0:
        return 0
    return (height / max_height) * 100


def tick_px(cm: int, max_height: int, chart_height_px: int) -> float:
    return (cm / max_height) * chart_height_px