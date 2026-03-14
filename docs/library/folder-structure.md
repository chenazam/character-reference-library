# Reference Library Folder Structure

The reference library is stored inside:

```
docs/assets/library/
```

This folder contains **all generated assets, reference images, and prompt templates** used in the character generation pipeline.

Unlike many documentation projects, this system intentionally stores the full asset library directly inside `docs/assets/` so that all files are immediately accessible through the MkDocs site.

Documentation explaining how the system works lives in:

```
docs/
```

The `docs/assets/library/` folder stores the **actual reference images and generation resources**.

---

# Top-Level Library Structure

```
docs/assets/library/

10_CHARACTERS
20_CHARACTER_PAIRS
30_CHARACTER_GROUPS
40_ENVIRONMENTS
50_PROMPT_TEMPLATES
60_INSPIRATION
```

---

# 10_CHARACTERS

Contains the full reference pipeline for each individual character.

Each character receives its own folder with all reference sheets generated through the pipeline.

Example:

```
10_CHARACTERS/
├── LUCIEN/
├── RAGNAR/
└── JONAH/
```

Each character folder contains anatomy references, style sheets, pose sheets, and other generated resources.

---

# 20_CHARACTER_PAIRS

Contains resources for **two-character relationships**.

This includes reference sheets used when two characters frequently appear together.

Typical contents:

- height comparison sheets
- interaction anchors
- couple pose sheets
- scene anchors involving both characters

Example:

```
20_CHARACTER_PAIRS/
├── LUCIEN__RAGNAR/
└── JASPER__BLAKE/
```

---

# 30_CHARACTER_GROUPS

Contains resources for **groups of three or more characters**.

Useful for teams, families, ensembles, or story casts.

Typical contents:

- group lineup sheets
- group pose sheets
- interaction scenes
- group scene anchors

Example:

```
30_CHARACTER_GROUPS/
├── WITCH_COVEN/
└── GYM_CREW/
```

---

# 40_ENVIRONMENTS

Contains reference sheets for **locations and environments** where characters appear.

These act as scene anchors to keep locations visually consistent.

Typical environment sheets include:

- room layouts
- lighting references
- architectural details
- environmental mood references

Example environments:

```
40_ENVIRONMENTS/

LUCIEN_APARTMENT/
RITUAL_CHAMBER/
GYM_INTERIOR/
CITY_STREET/
```

Environment anchors are often attached to prompts when generating **scene images**.

---

# 50_PROMPT_TEMPLATES

Contains reusable prompt templates used throughout the pipeline.

Templates are organized by generation stage.

Example:

```
50_PROMPT_TEMPLATES/

00_MASTER_BLOCKS
01_FACE_ANCHORS
03_ANATOMY
11_UCS
```

Each template should include reusable placeholder blocks such as:

```
[CHARACTER BLOCK]
[GLOBAL STYLE BLOCK]
```

These allow prompts to be reused across multiple characters.

---

# 60_INSPIRATION

Contains reference images used as **design inspiration**.

These are not generated assets, but visual references that influence character design.

Examples include:

- fashion references
- architecture references
- lighting references
- pose inspiration
- color palette inspiration

Example structure:

```
60_INSPIRATION/

FASHION/
LIGHTING/
POSES/
COLOR_PALETTES/
ARCHITECTURE/
```

These images are sometimes attached to prompts to guide visual style.

---

# Character Folder Structure

Each character folder contains the complete reference pipeline for that character.

Example:

```
10_CHARACTERS/
└── LUCIEN/
```

Inside each character folder:

```text
[CHARACTER_NAME]/
├── 00_SOURCE_REFERENCES/
│   ├── face/
│   │   ├── actor_reference_01.jpg
│   │   ├── facial_structure_example.jpg
│   │   └── notes.md
│   ├── hair/
│   │   ├── hairstyle_reference_01.jpg
│   │   └── notes.md
│   ├── body/
│   │   ├── physique_reference.jpg
│   │   └── notes.md
│   ├── clothing/
│   │   ├── jacket_reference.jpg
│   │   ├── outfit_style_reference.jpg
│   │   └── notes.md
│   ├── poses/
│   │   ├── running_pose.jpg
│   │   ├── relaxed_pose_reference.jpg
│   │   └── notes.md
│   ├── scenes/
│   │   ├── cozy_lifestyle_reference.jpg
│   │   └── notes.md
│   └── misc/
│   └── notes.md
├── 00_PROFILE/
│   ├── metadata.yaml
│   ├── character_summary.md
│   ├── prompt_blocks.md
│   ├── identity_guardrails.md
│   └── notes.md
├── 01_IDENTITY/
│   ├── face/
│   │   ├── 1A_front_face.png
│   │   ├── 1B_three_quarter_face.png
│   │   ├── 1C_profile_face.png
│   │   ├── 1D_face_anchor_sheet.png
│   │   └── notes.md
│   ├── hair/
│   │   ├── 2_hair_sheet.png
│   │   └── notes.md
│   ├── expression/
│   │   ├── 9_expression_sheet.png
│   │   └── notes.md
│   ├── hands/
│   │   ├── 10_hand_sheet.png
│   │   └── notes.md
│   └── gallery/
│       ├── 11_gallery_image.png
│       └── notes.md
├── 02_BODY/
│   ├── anatomy/
│   │   ├── 3A_anatomy_front.png
│   │   ├── 3B_anatomy_side.png
│   │   ├── 3C_anatomy_back.png
│   │   ├── 3D_anatomy_glutes.png
│   │   ├── 3E_anatomy_sheet.png
│   │   └── notes.md
│   ├── structure/
│   │   ├── 4_body_anchor.png
│   │   ├── 5_proportion_grid.png
│   │   ├── 6_muscle_tension.png
│   │   ├── 7_silhouette.png
│   │   ├── 8_turnaround.png
│   │   └── notes.md
│   ├── scale/
│   │   ├── 18_height_scale_sheet.png
│   │   └── notes.md
│   └── notes.md
├── 03_UCS/
│   ├── core_panels/
│   │   ├── 12A_ucs_front_face_panel.png
│   │   ├── 12B_ucs_three_quarter_face_panel.png
│   │   ├── 12C_ucs_profile_face_panel.png
│   │   ├── 12D_ucs_body_front_panel.png
│   │   ├── 12E_ucs_body_side_panel.png
│   │   ├── 12F_ucs_silhouette_panel.png
│   │   ├── 12G_ucs_expression_panel.png
│   │   └── notes.md
│   ├── core/
│   │   ├── 12H_ucs_core_assembly.png
│   │   └── notes.md
│   ├── extended/
│   │   ├── 21_ucs_dynamic_pose_panel.png
│   │   ├── 22_final_ucs_assembly.png
│   │   └── notes.md
│   ├── assembly_notes.md
│   └── notes.md
├── 04_STYLE/
│   ├── signature/
│   │   ├── 13_signature_outfit.png
│   │   └── notes.md
│   ├── design_language/
│   │   ├── 14_design_language_sheet.png
│   │   └── notes.md
│   ├── wardrobes/
│   │   ├── 15A_outfit_01.png
│   │   ├── 15B_outfit_02.png
│   │   ├── 15C_outfit_03.png
│   │   ├── 15D_outfit_04.png
│   │   ├── 15E_outfit_05.png
│   │   ├── 15F_wardrobe_master_sheet.png
│   │   └── notes.md
│   └── notes.md
├── 05_MOTION/
│   ├── poses/
│   │   ├── 16_pose_sheet.png
│   │   └── notes.md
│   ├── motion/
│   │   ├── 17_motion_anchor_sheet.png
│   │   └── notes.md
│   ├── interaction/
│   │   ├── 19_interaction_anchor_sheet.png
│   │   └── notes.md
│   └── notes.md
├── 06_SCENES/
│   ├── lifestyle/
│   │   ├── 20_lifestyle_scene_anchor_sheet.png
│   │   └── notes.md
│   └── notes.md
└── 07_EXPORTS/
    ├── thumbnails/
    │   └── .gitkeep
    ├── sheets/
    │   └── .gitkeep
    ├── web/
    │   └── .gitkeep
    ├── print/
    │   └── .gitkeep
    └── notes.md
```

---

## Folder Purpose Notes

### `07_SOURCE_REFERENCES/`

Original source images used during character creation.

Use for:

- face inspiration photos
- clothing inspiration
- hairstyle references
- pose references

---

### `00_PROFILE/`

Core character metadata and reference documents.

Use for:

- metadata
- character summary
- prompt blocks
- identity guardrails
- character-specific notes

This folder should remain highly stable.

---

### `01_IDENTITY/`

Face-first and early identity assets.

Use for:

- face identity views
- face anchor
- hair sheet
- expression sheet
- hand sheet
- gallery image

This groups all the “who is this character?” assets that are not primarily body-structural.

---

### `02_BODY/`

Anatomy, structural body references, and scale.

Use for:

- anatomy views and anatomy sheet
- body anchor
- proportion grid
- muscle tension
- silhouette
- turnaround
- height/scale sheet

This is the main body-reference family.

---

### `03_UCS/`

All UCS-related panels and assemblies.

Use for:

- UCS core panels
- UCS core assembly
- dynamic pose panel
- final UCS assembly
- assembly notes

This makes the UCS Core / Final UCS split explicit.

---

### `04_STYLE/`

Clothing and style-definition assets.

Use for:

- signature outfit
- design language
- wardrobe variations
- wardrobe master sheet

This is the style / costume family.

---

### `05_MOTION/`

Pose, movement, and interaction assets.

Use for:

- pose sheet
- motion anchor
- interaction anchor

This is the body-language / applied-character-use family.

---

### `06_SCENES/`

Scene-oriented character-use assets.

Use for:

- lifestyle scene anchor sheet
- future scene-oriented expansions

This keeps scene-use separate from motion references.

---

### `07_EXPORTS/`

Derived outputs intended for presentation or publishing rather than generation.

Use for:

- thumbnails
- web-ready exports
- print-ready exports
- assembled output sheets

This separates reference-source assets from delivery artifacts.
