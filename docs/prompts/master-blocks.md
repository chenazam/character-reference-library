# Master Prompt Blocks

These files define reusable prompt fragments used across the character generation pipeline.

Templates reference these blocks using placeholder names.

## Canonical Placeholder Reference

| Placeholder                       | Block File                       |
| --------------------------------- | -------------------------------- |
| `[CHARACTER_BLOCK]`               | character-block-template.md      |
| `[GLOBAL_STYLE_BLOCK]`            | global-style-block.md            |
| `[IDENTITY_PRESERVATION_BLOCK]`   | identity-preservation-block.md   |
| `[LAYOUT_BLOCK]`                  | layout-block.md                  |
| `[LABELS_BLOCK]`                  | labels-block.md                  |
| `[CAMERA_BLOCK]`                  | camera-block.md                  |
| `[LIGHTING_BLOCK]`                | lighting-block.md                |
| `[BACKGROUND_BLOCK]`              | background-block.md              |
| `[REFERENCE_SHEET_BLOCK_STACK]`   | reference-sheet-block-stack.md   |
| `[REFERENCE_PANEL_BLOCK_STACK]`   | reference-panel-block-stack.md   |
| `[SCENE_BLOCK_STACK]`             | scene-block-stack.md             |
| `[SQUARE_REFERENCE_FORMAT_BLOCK]` | square-reference-format-block.md |
| `[PORTRAIT_SHEET_FORMAT_BLOCK]`   | portrait-sheet-format-block.md   |
| `[LANDSCAPE_SHEET_FORMAT_BLOCK]`  | landscape-sheet-format-block.md  |

Do not duplicate these blocks in templates.  
Templates should reference them instead.

---

## Block Placeholder Names

Prompt templates reference reusable blocks using standardized placeholders.

These placeholders correspond to files stored in:

```text
assets/library/50_PROMPT_TEMPLATES/00_MASTER_BLOCKS/
```

Templates should always use these canonical placeholder names.

| Placeholder                       | Block File                       |
| --------------------------------- | -------------------------------- |
| `[CHARACTER_BLOCK]`               | character-block-template.md      |
| `[GLOBAL_STYLE_BLOCK]`            | global-style-block.md            |
| `[IDENTITY_PRESERVATION_BLOCK]`   | identity-preservation-block.md   |
| `[LAYOUT_BLOCK]`                  | layout-block.md                  |
| `[LABELS_BLOCK]`                  | labels-block.md                  |
| `[CAMERA_BLOCK]`                  | camera-block.md                  |
| `[LIGHTING_BLOCK]`                | lighting-block.md                |
| `[BACKGROUND_BLOCK]`              | background-block.md              |
| `[REFERENCE_FIDELITY_BLOCK]`      | reference-fidelity-block.md      |
| `[REFERENCE_SHEET_BLOCK_STACK]`   | reference-sheet-block-stack.md   |
| `[REFERENCE_PANEL_BLOCK_STACK]`   | reference-panel-block-stack.md   |
| `[SCENE_BLOCK_STACK]`             | scene-block-stack.md             |
| `[SQUARE_REFERENCE_FORMAT_BLOCK]` | square-reference-format-block.md |
| `[PORTRAIT_SHEET_FORMAT_BLOCK]`   | portrait-sheet-format-block.md   |
| `[LANDSCAPE_SHEET_FORMAT_BLOCK]`  | landscape-sheet-format-block.md  |

When writing prompt templates:

- always reference the canonical placeholder names
- avoid inventing new block names
- reuse the existing master blocks whenever possible
- use block stacks when a template consistently uses the same combination of blocks
- use format blocks to standardize aspect-ratio families across the library

This ensures prompt templates remain consistent across the pipeline.

---

## Character Block Template

This block is replaced with the character-specific description.

```text
Character:

Lucien is a slender man of average height (170 cm / 5'7") with refined facial features and a calm, slightly mysterious presence. His aesthetic is occult and scholarly with subtle gothic influences.
```

---

## Global Style Block

Use this block in most reference prompts.

```text
Style:
clean professional character design reference sheet

Rendering:
high detail illustration
consistent anatomy

Lighting:
neutral studio lighting

Background:
pure white

Camera:
orthographic reference camera
no dramatic perspective

Color:
natural realistic colors

Linework:
clean professional design lines
```

---

## Identity Preservation Block

Use this in prompts where identity drift may occur.

```text
Important constraints:

• preserve exact facial identity
• maintain body proportions
• maintain hairstyle consistency
• ensure all panels clearly depict the same character
```

---

## Layout Block

Use this block when generating multi-panel reference sheets.

```text
Layout:
professional animation reference sheet layout
even spacing
clean grid alignment

Important:
no panel cropping
no overlapping panels
all panels fully visible
```

---

## Labels Block

Standard label style for reference sheets.

```text
Labels:
small clean sans-serif labels
dark gray text
centered under panels
```

---

## Camera Block

Ensures consistent orthographic views.

```text
Camera:
orthographic reference camera
eye-level perspective
no dramatic perspective distortion
```

---

## Lighting Block

Standard lighting used in most reference prompts.

```text
Lighting:
neutral studio lighting
soft even illumination
no dramatic shadows
no directional spotlighting
consistent lighting across panels
```

---

## Background Block

Standard background used in most sheet and panel prompts.

```text
Background:
pure white
```

---

## Reference Fidelity Block

Use this block when prompts rely on previously generated character references.

```text
Reference fidelity:

The attached reference images define the canonical appearance of the character.

Strictly preserve:

• facial identity
• hairstyle
• body proportions
• silhouette
• age and facial maturity
• recognizable facial features

The generated image must clearly depict the same character as the references.

Do not reinterpret or redesign the character.
Do not change facial structure or body proportions.
```

---

## Reference Sheet Block Stack

Use this block stack for multi-panel reference sheets.

```text
[GLOBAL_STYLE_BLOCK]

[IDENTITY_PRESERVATION_BLOCK]

[LAYOUT_BLOCK]

[LABELS_BLOCK]

[CAMERA_BLOCK]

[LIGHTING_BLOCK]

[BACKGROUND_BLOCK]
```

---

## Reference Panel Block Stack

Use this block stack for single-panel reference images and UCS panel prompts.

```text
[GLOBAL_STYLE_BLOCK]

[IDENTITY_PRESERVATION_BLOCK]

[CAMERA_BLOCK]

[LIGHTING_BLOCK]

[BACKGROUND_BLOCK]
```

---

## Scene Block Stack

Use this block stack for scenes, interactions, and environment-driven prompts.

```text
[GLOBAL_STYLE_BLOCK]

[IDENTITY_PRESERVATION_BLOCK]

[CAMERA_BLOCK]

[LIGHTING_BLOCK]
```

---

## Square Reference Format Block

Use this block for square single-panel references.

```text
Output format:
square reference canvas
consistent square aspect ratio
subject centered
clean margins
intended for uniform gallery display
```

---

## Portrait Sheet Format Block

Use this block for portrait-oriented multi-panel sheets.

```text
Output format:
portrait-oriented reference sheet
consistent portrait aspect ratio across this sheet type
clean outer margins
all panels fully visible
intended for uniform library browsing
```

---

## Landscape Sheet Format Block

Use this block for landscape-oriented multi-panel sheets.

```text
Output format:
landscape-oriented reference sheet
consistent landscape aspect ratio across this sheet type
clean outer margins
all panels fully visible
intended for uniform library browsing
```
