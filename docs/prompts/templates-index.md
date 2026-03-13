# Prompt Template Library

This section provides direct access to the prompt templates used throughout the character reference pipeline.

These templates are designed to be:

- browsable in the MkDocs frontend
- reusable across multiple characters
- consistent in structure and terminology
- optimized for AI image generation workflows

Templates are grouped by pipeline stage so they can be browsed in the same order the reference library is typically built.

---

## Template Groups

### Facial Identity

Templates used to establish facial identity and neutral face references.

- [Face Templates](templates/face.md)

### Hair and Anatomy

Templates used to define hairstyle identity and anatomical construction.

- [Hair and Anatomy Templates](templates/anatomy.md)

### Body Structure

Templates used to define full-body proportions, musculature, silhouette, and turnaround references.

- [Body Structure Templates](templates/body.md)

### Ultimate Character Sheet

Templates used to build UCS panel prompts and assembly guidance.

- [UCS Templates](templates/ucs.md)

### Outfit and Design

Templates used to define signature outfits, wardrobe variants, and design language references.

- [Outfit and Design Templates](templates/outfits.md)

### Motion and Scenes

Templates used for poses, motion references, interactions, scale, and scene-based character usage.

- [Motion and Scene Templates](templates/scenes.md)

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
