# Prompt Template Normalization Checklist

This checklist ensures that all prompt templates in the library use the correct master blocks and format blocks.

The goal is to maintain:

- consistent prompt structure
- stable output formats
- predictable image aspect ratios
- reusable block stacks

When reviewing a template:

1. Replace duplicated blocks with the correct block stack.
2. Ensure exactly one format block is used when appropriate.
3. Remove redundant or outdated block placeholders.
4. Verify the template uses the canonical placeholder names.

---

# General Rules

### Single-panel references

Use:

```
[REFERENCE_PANEL_BLOCK_STACK]
```

Add a format block if needed:

```
[SQUARE_REFERENCE_FORMAT_BLOCK]
```

or

```
[PORTRAIT_SHEET_FORMAT_BLOCK]
```

---

### Multi-panel reference sheets

Use:

```
[REFERENCE_SHEET_BLOCK_STACK]
```

Add one format block:

```
[PORTRAIT_SHEET_FORMAT_BLOCK]
```

or

```
[LANDSCAPE_SHEET_FORMAT_BLOCK]
```

---

### Scene or environment prompts

Use:

```
[SCENE_BLOCK_STACK]
```

Format blocks are usually **not required**.

---

# Template Review Checklist

---

# 01_FACE_ANCHORS

### face-anchor-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`
- [ ] Does NOT manually list individual style/layout blocks

---

### front-face-reference.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`
- [ ] No layout or label blocks

---

### three-quarter-face-reference.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`

---

### profile-face-reference.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`

---

# 02_HAIR

### hair-reference-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 03_ANATOMY

### anatomy-front.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### anatomy-side.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### anatomy-back.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### anatomy-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 04_PROPORTIONS

### body-proportions-grid.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 05_MUSCLE

### muscle-tension-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 06_BODY

### body-anchor-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 07_SILHOUETTE

### silhouette-sheet.md

- [ ] Uses layout and label blocks
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`
- [ ] Does NOT rely on the full style block stack

Recommended block set:

```
[LAYOUT_BLOCK]
[LABELS_BLOCK]
[CAMERA_BLOCK]
[LIGHTING_BLOCK]
[BACKGROUND_BLOCK]
[PORTRAIT_SHEET_FORMAT_BLOCK]
```

---

# 08_TURNAROUND

### turnaround-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[LANDSCAPE_SHEET_FORMAT_BLOCK]`

---

# 09_EXPRESSIONS

### expression-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 10_HANDS

### hand-reference-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 11_UCS

### ucs-face-front.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`

---

### ucs-face-three-quarter.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`

---

### ucs-face-profile.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`

---

### ucs-body-front.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### ucs-body-side.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### ucs-silhouette.md

- [ ] Uses camera, lighting, and background blocks
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### ucs-expression.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[SQUARE_REFERENCE_FORMAT_BLOCK]`

---

### ucs-dynamic-pose.md

- [ ] Uses `[REFERENCE_PANEL_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### ucs-assembly-notes.md

- [ ] No prompt blocks used
- [ ] Pure documentation

---

# 12_SIGNATURE_OUTFIT

### signature-outfit-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 13_DESIGN_LANGUAGE

### design-language-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 14_WARDROBE

### outfit-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

### wardrobe-master-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[LANDSCAPE_SHEET_FORMAT_BLOCK]`

---

# 15_POSES

### pose-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 16_MOTION

### motion-anchor-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[LANDSCAPE_SHEET_FORMAT_BLOCK]`

---

# 17_SCALE

### height-scale-sheet.md

- [ ] Uses `[REFERENCE_SHEET_BLOCK_STACK]`
- [ ] Uses `[PORTRAIT_SHEET_FORMAT_BLOCK]`

---

# 18_INTERACTIONS

### interaction-anchor-sheet.md

- [ ] Uses `[SCENE_BLOCK_STACK]`

Optional:

- [ ] Uses `[LANDSCAPE_SHEET_FORMAT_BLOCK]`

---

# 19_SCENES

### lifestyle-scene-anchor-sheet.md

- [ ] Uses `[SCENE_BLOCK_STACK]`
- [ ] No sheet layout blocks
