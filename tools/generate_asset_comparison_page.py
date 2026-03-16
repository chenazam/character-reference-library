import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
SNIPPETS_ROOT = DOCS_ROOT / "snippets" / "comparisons"
COMPARISONS_ROOT = DOCS_ROOT / "comparisons"

ASSET_TYPES = {
    "gallery-image": "01 Identity – Gallery Image",
    "face-anchor": "01 Identity – Face Anchor Sheet",
    "face-front": "01 Identity – Face Front",
    "face-three-quarter": "01 Identity – Face Three-Quarter",
    "face-profile": "01 Identity – Face Profile",
    "hair-sheet": "01 Identity – Hair Sheet",
    "expression-sheet": "01 Identity – Expression Sheet",
    "hand-sheet": "01 Identity – Hand Sheet",
    "anatomy-sheet": "02 Body – Anatomy Sheet",
    "anatomy-front": "02 Body – Anatomy Front",
    "anatomy-side": "02 Body – Anatomy Side",
    "anatomy-back": "02 Body – Anatomy Back",
    "anatomy-glutes": "02 Body – Glute Reference",
    "body-anchor": "02 Body – Body Anchor Sheet",
    "proportion-grid": "02 Body – Proportion Grid",
    "muscle-tension": "02 Body – Muscle Tension Sheet",
    "silhouette-sheet": "02 Body – Silhouette Sheet",
    "turnaround-sheet": "02 Body – Turnaround Sheet",
    "height-scale": "02 Body – Height Scale Sheet",
    "ucs-sheet": "03 UCS – Ultimate Character Sheet",
    "ucs-face-front": "03 UCS – Face Front",
    "ucs-face-three-quarter": "03 UCS – Face Three-Quarter",
    "ucs-face-profile": "03 UCS – Face Profile",
    "ucs-expression": "03 UCS – Expression",
    "ucs-body-front": "03 UCS – Body Front",
    "ucs-body-side": "03 UCS – Body Side",
    "ucs-silhouette": "03 UCS – Silhouette",
    "ucs-dynamic-pose": "03 UCS – Dynamic Pose",
    "signature-outfit": "04 Style – Signature Outfit Sheet",
    "design-language": "04 Style – Design Language Sheet",
    "outfit-sheet": "04 Style – Outfit Sheet",
    "wardrobe-sheet": "04 Style – Wardrobe Sheet",
    "pose-sheet": "05 Motion – Pose Sheet",
    "motion-anchor": "05 Motion – Motion Anchor Sheet",
    "interaction-anchor": "05 Motion – Interaction Anchor Sheet",
    "scene-anchor": "06 Scenes – Scene Anchor Sheet",
    "prop-sheet": "06 Scenes – Prop Sheet",
}


def populated_asset_keys() -> list[str]:
    keys = []
    for asset_key in ASSET_TYPES:
        snippet_path = SNIPPETS_ROOT / f"{asset_key}.md"
        if snippet_path.exists():
            keys.append(asset_key)
    return keys


def build_page(asset_keys: list[str]) -> str:
    if not asset_keys:
        body = [
            "# Asset Comparisons",
            "",
            "No comparison snippets have been generated yet.",
            "",
            "Run `tools/generate_asset_comparison_snippets.py` first.",
            "",
        ]
        return "\n".join(body)

    lines = []
    lines.append("# Asset Comparisons")
    lines.append("")
    lines.append("Compare one asset type across all characters. Use the selector to switch between generated comparison grids.")
    lines.append("")
    lines.append('<div class="comparison-controls">')
    lines.append('  <label for="asset-type-select"><strong>Asset type:</strong></label>')
    lines.append('  <select id="asset-type-select">')
    for asset_key in asset_keys:
        label = ASSET_TYPES[asset_key]
        lines.append(f'    <option value="{asset_key}">{label}</option>')
    lines.append("  </select>")
    lines.append("</div>")
    lines.append("")

    for index, asset_key in enumerate(asset_keys):
        label = ASSET_TYPES[asset_key]
        hidden_attr = "" if index == 0 else ' hidden="hidden"'
        lines.append(f'<section class="comparison-section" data-asset-type="{asset_key}"{hidden_attr}>')
        lines.append(f"<h2>{label}</h2>")
        lines.append("")
        lines.append(f'--8<-- "snippets/comparisons/{asset_key}.md"')
        lines.append("")
        lines.append("</section>")
        lines.append("")

    lines.append("<script>")
    lines.append("document.addEventListener('DOMContentLoaded', function () {")
    lines.append("  const select = document.getElementById('asset-type-select');")
    lines.append("  const sections = Array.from(document.querySelectorAll('.comparison-section'));")
    lines.append("")
    lines.append("  function showAssetType(assetType) {")
    lines.append("    sections.forEach((section) => {")
    lines.append("      const isMatch = section.dataset.assetType === assetType;")
    lines.append("      if (isMatch) {")
    lines.append("        section.removeAttribute('hidden');")
    lines.append("      } else {")
    lines.append("        section.setAttribute('hidden', 'hidden');")
    lines.append("      }")
    lines.append("    });")
    lines.append("  }")
    lines.append("")
    lines.append("  if (select) {")
    lines.append("    showAssetType(select.value);")
    lines.append("    select.addEventListener('change', function () {")
    lines.append("      showAssetType(select.value);")
    lines.append("    });")
    lines.append("  }")
    lines.append("});")
    lines.append("</script>")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    COMPARISONS_ROOT.mkdir(parents=True, exist_ok=True)

    asset_keys = populated_asset_keys()
    page = build_page(asset_keys)

    out_path = COMPARISONS_ROOT / "assets.md"
    out_path.write_text(page, encoding="utf-8")

    print(f"Generated {out_path.relative_to(ROOT)}")
    print(f"Included {len(asset_keys)} populated asset types.")


if __name__ == "__main__":
    main()
