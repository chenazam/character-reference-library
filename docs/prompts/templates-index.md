# Prompt Template Library

This section provides direct access to the prompt templates used throughout the character reference pipeline.

These templates are designed to be:

- browsable in the MkDocs frontend
- reusable across multiple characters
- consistent in structure and terminology
- optimized for AI image generation workflows

Templates are grouped by **asset family** so they align with the character folder structure and the major reference types used throughout the pipeline.

This makes it easier to browse templates in the same way character assets are organized.

---

## Pipeline Overview

Template groups correspond to the major asset families used in the pipeline:

1. Identity → face, hair, expressions, hands, gallery image
2. Body → anatomy and structural body references
3. UCS → canonical character sheets
4. Style → clothing and design language
5. Motion → poses and interaction references
6. Scenes → lifestyle and environment usage

---

## Template Groups

### Identity

Templates used to establish and extend core character identity.

Includes templates for early identity references such as:

- face identity views
- hair sheet
- expression sheet
- hand sheet
- gallery image

- [Identity Templates](templates/identity.md)

### Body

Templates used to define anatomy, structure, silhouette, turnaround, and scale.

Includes:

- anatomy views and anatomy sheet
- body anchor
- proportion grid
- muscle tension
- silhouette
- turnaround
- height scale

- [Body Templates](templates/body.md)

### UCS

Templates used to generate UCS panels and assemble the UCS reference sheets.

Includes:

- UCS core panels
- UCS core assembly
- dynamic pose panel
- final UCS assembly

- [UCS Templates](templates/ucs.md)

### Style

Templates used to define signature outfit, design language, wardrobe variants, and wardrobe master assembly.

- [Style Templates](templates/style.md)

### Motion

Templates used for pose, motion, and interaction-oriented character usage.

- [Motion Templates](templates/motion.md)

### Scenes

Templates used for lifestyle scene anchors and scene-oriented character application.

- [Scene Templates](templates/scenes.md)

---

## How Templates Are Built

Prompt templates in this library are built from three layers:

1. **Master prompt blocks**  
   Reusable blocks such as style, layout, lighting, camera, and identity preservation.

2. **Character prompt blocks**  
   Character-specific descriptions stored in each character’s profile.

3. **Pipeline prompt templates**  
   Stage-specific prompt templates used to generate reference sheets.

For more detail, see:

- [Prompt System Overview](overview.md)
- [Master Blocks](master-blocks.md)
- [Prompt Recipes](prompt-recipes.md)
- [Reference Attachments](reference-attachments.md)

---

## Usage Notes

These frontend pages are intended for browsing and copying templates.

The underlying source files remain stored in:

```text
docs/assets/library/50_PROMPT_TEMPLATES/
```

The frontend pages expose them in a more readable and structured form.

Because the templates already store their prompt bodies inside fenced code blocks, they can be copied directly from the frontend using the MkDocs code-copy button.

---

## Recommended Workflow

A typical workflow is:

1. choose the relevant pipeline stage
2. open the matching template page
3. copy the template
4. inject the relevant character blocks
5. attach the correct reference sheets

This allows the same template to be reused across many characters without duplicating prompt files.
