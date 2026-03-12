# Library Folder Structure

The `library/` directory contains all generated assets, references, and prompt templates used in the character pipeline.

Documentation explaining how to use these assets lives in `docs/`.  
The `library/` folder itself stores the **actual files used for generation**.

---

# Top-Level Library Structure

```
library/

10_CHARACTERS
20_CHARACTER_PAIRS
30_CHARACTER_GROUPS
40_ENVIRONMENTS
50_PROMPT_TEMPLATES
60_INSPIRATION
```

## 10_CHARACTERS

Contains the full reference pipeline for each individual character.

Each character receives its own folder with all reference sheets generated through the pipeline.

Example:

```
10_CHARACTERS/
LUCIEN/
RAGNAR/
JONAH/
```

Each character folder contains anatomy references, style sheets, pose sheets, and other generated resources.

---

## 20_CHARACTER_PAIRS

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
LUCIEN__RAGNAR/
JASPER__BLAKE/
```

---

## 30_CHARACTER_GROUPS

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
WITCH_COVEN/
GYM_CREW/
```

---

## 40_ENVIRONMENTS

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

## 50_PROMPT_TEMPLATES

Contains reusable prompt templates used throughout the pipeline.

Templates are organized by generation stage.

Example:

```
50_PROMPT_TEMPLATES/

FACE/
ANATOMY/
BODY/
UCS/
WARDROBE/
POSE/
SCENE/
```

Each template should include placeholders such as:

```
[CHARACTER BLOCK]
[GLOBAL STYLE BLOCK]
```

These allow prompts to be reused across multiple characters.

---

## 60_INSPIRATION

Contains reference images used as **design inspiration**.

These are not generated assets, but visual references that influence character design.

Examples:

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

```
00_PROFILE
01_FACE
02_HAIR
03_ANATOMY
04_PROPORTIONS
05_MUSCLE
06_BODY
07_SILHOUETTE
08_TURNAROUND
09_EXPRESSIONS
10_HANDS
11_UCS
12_SIGNATURE_OUTFIT
13_DESIGN_LANGUAGE
14_WARDROBE
15_POSES
16_MOTION
17_SCALE
18_SCENES
19_PROPS

IDENTITY_PACK
SOURCE_REFERENCES
```

---

# Character Folder Explanations

## 00_PROFILE

Contains descriptive information about the character.

Typical files:

```
metadata.yaml
character_summary.md
prompt_blocks.md
prompt_recipes.md
```

These files define the character concept and reusable prompt components.

---

## 01_FACE

Contains all face identity references.

Examples:

```
face_front.png
face_34.png
face_profile.png
face_anchor_sheet.png
```

These images establish the character’s facial identity.

---

## 02_HAIR

Hair structure references.

Examples:

```
hair_reference_sheet.png
```

Used to prevent hairstyle drift.

---

## 03_ANATOMY

Bare-torso anatomy references used to define physique and proportions.

Examples:

```
anatomy_front.png
anatomy_side.png
anatomy_back.png
anatomy_sheet.png
```

---

## 04_PROPORTIONS

Contains body proportion grid sheets.

Used to anchor limb lengths and body ratios.

---

## 05_MUSCLE

Contains muscle tension references.

Shows how musculature appears when relaxed vs engaged.

---

## 06_BODY

Contains the **body anchor sheet**, which introduces neutral clothing.

This becomes the main body reference used for most later prompts.

---

## 07_SILHOUETTE

Contains silhouette references used to stabilize character shape.

---

## 08_TURNAROUND

Contains the multi-angle turnaround sheet used to define how the character looks from different angles.

---

## 09_EXPRESSIONS

Contains the character’s expression sheet.

Defines emotional range while preserving facial structure.

---

## 10_HANDS

Contains hand reference sheets used to stabilize finger proportions and gestures.

---

## 11_UCS

Contains the Ultimate Character Sheet and its individual panels.

This is the master identity reference for the character.

---

## 12_SIGNATURE_OUTFIT

Contains the character’s canonical outfit reference.

This sheet defines the character’s primary visual style.

---

## 13_DESIGN_LANGUAGE

Contains sheets that define materials, accessories, color palette, and stylistic motifs.

These help maintain consistent aesthetic across outfits and scenes.

---

## 14_WARDROBE

Contains additional outfit sheets for the character.

Examples:

- casual outfit
- work outfit
- formal outfit
- relaxed home outfit

---

## 15_POSES

Contains pose sheets used to demonstrate body language and movement.

---

## 16_MOTION

Contains motion anchor sheets.

These stabilize movement such as walking, running, turning, and reaching.

---

## 17_SCALE

Contains height comparison sheets and scale references.

Used when characters appear together.

---

## 18_SCENES

Contains scene anchors involving the character.

Examples:

- domestic scene
- workplace scene
- social interaction
- action scene

---

## 19_PROPS

Contains prop interaction references.

Examples include the character handling:

- phones
- books
- weapons
- tools
- bags

---

## IDENTITY_PACK

Contains the small set of core identity references most commonly attached to prompts.

Typical contents:

```
face_anchor_sheet.png
anatomy_sheet.png
body_anchor_sheet.png
ultimate_character_sheet.png
signature_outfit_sheet.png
```

---

## SOURCE_REFERENCES

Contains original source images used during character creation.

Examples:

- face inspiration photos
- clothing inspiration
- hairstyle references
- pose references
