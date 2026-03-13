# Master Prompt Blocks

These files define reusable prompt fragments used across the character generation pipeline.

Templates reference these blocks using placeholder names.

| Placeholder                     | Block File                     |
| ------------------------------- | ------------------------------ | --- |
| `[CHARACTER_BLOCK]`             | character-block-template.md    |
| `[GLOBAL_STYLE_BLOCK]`          | global-style-block.md          |
| `[IDENTITY_PRESERVATION_BLOCK]` | identity-preservation-block.md |
| `[LAYOUT_BLOCK]`                | layout-block.md                |
| `[LABELS_BLOCK]`                | labels-block.md                |
| `[CAMERA_BLOCK]`                | camera-block.md                |
| `[LIGHTING_BLOCK]`              | lighting-block.md              |
| `[BACKGROUND_BLOCK]`            | background-block.md            |
| `[REFERENCE_SHEET_BLOCK_STACK]` | reference-sheet-block-stack.md |     |

Do not duplicate these blocks in templates.  
Templates should reference them instead.

---

## Block Placeholder Names

Prompt templates reference reusable blocks using standardized placeholders.

These placeholders correspond to files stored in:

assets/library/50_PROMPT_TEMPLATES/00_MASTER_BLOCKS/

Templates should always use these canonical placeholder names.

| Placeholder                     | Block File                     |
| ------------------------------- | ------------------------------ |
| `[CHARACTER_BLOCK]`             | character-block-template.md    |
| `[GLOBAL_STYLE_BLOCK]`          | global-style-block.md          |
| `[IDENTITY_PRESERVATION_BLOCK]` | identity-preservation-block.md |
| `[LAYOUT_BLOCK]`                | layout-block.md                |
| `[LABELS_BLOCK]`                | labels-block.md                |
| `[CAMERA_BLOCK]`                | camera-block.md                |
| `[LIGHTING_BLOCK]`              | lighting-block.md              |
| `[BACKGROUND_BLOCK]`            | background-block.md            |

When writing prompt templates:

• always reference the canonical placeholder names  
• avoid inventing new block names  
• reuse the existing master blocks whenever possible

This ensures prompt templates remain consistent across the pipeline.

---

## Character Block Template

This block is replaced with the character-specific description.

```
Character:

Lucien is a slender man of average height (170 cm / 5'7") with refined facial features and a calm, slightly mysterious presence. His aesthetic is occult and scholarly with subtle gothic influences.
```

---

## Global Style Block

Use this block in most reference sheet prompts.

```
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

```
Important constraints:

• preserve exact facial identity
• maintain body proportions
• maintain hairstyle consistency
• ensure all panels clearly depict the same character
```

---

## Layout Block

Use this block when generating reference sheets.

```
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

```
Labels:
small clean sans-serif labels
dark gray text
centered under panels
```

---

## Camera Block

Ensures consistent orthographic views.

```
Camera:
orthographic reference camera
eye-level perspective
no dramatic perspective distortion
```

---

## Lighting Block

Standard lighting used in most reference sheets.

```
Lighting:
neutral studio lighting
soft even illumination
no dramatic shadows
no directional spotlighting
consistent lighting across panels
```

---

## Background Block

Standard background used in most sheets.

```
Background:
pure white
```
