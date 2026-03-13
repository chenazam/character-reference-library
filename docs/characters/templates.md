# Character Templates

This page explains how to create a new character using the project’s folder and file templates.

The goal is to ensure that all characters follow the same structure, follow the same reference pipeline, and remain easy to browse inside the MkDocs library.

---

## Character Page Layout

Character pages in the MkDocs site serve as **visual reference hubs** for browsing a character’s generated sheets.

These pages are separate from the character asset folders and are located in:

```text
docs/characters/
```

Example:

```text
docs/characters/lucien.md
```

Each character page aggregates thumbnail previews of the character’s reference sheets and links to the full-size images stored in:

```text
docs/assets/library/10_CHARACTERS/
```

A reusable template for these pages is provided here:

```text
docs/characters/character-page-template.md
```

When creating a new character page:

1. Copy the template.
2. Rename it to the character name.
3. Replace placeholder paths.
4. Add thumbnails for the character’s available sheets.

These pages are optimized for **visual browsing and prompt construction**, rather than for pipeline documentation.

---

## Creating a New Character

To create a new character:

1. Copy the character template folder.
2. Rename the folder to the character’s name.
3. Fill out the files in `00_PROFILE`.
4. Begin generating the reference sheets following the pipeline.

Example asset folder:

```text
docs/assets/library/10_CHARACTERS/LUCIEN
```

---

## Character Folder Template

Every character asset folder follows the same structure.

```text
CHARACTER_NAME/

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

Each folder corresponds to a stage in the character generation pipeline.

---

## The Profile Folder

The `00_PROFILE` folder contains the conceptual definition of the character.

```text
00_PROFILE/

metadata.yaml
character_summary.md
prompt_blocks.md
```

These files define the character before reference sheets are generated.

---

## `metadata.yaml` Template

```yaml
name: [CHARACTER_NAME]
slug: [character_slug]

height_cm: [HEIGHT_CM]
height_imperial: '[HEIGHT_IMPERIAL]'

build_category: [build_type]

tags:
  - [style_tag]
  - [archetype]

style_keywords:
  - [style_word]
  - [style_word]

signature_accessories:
  - [item]

reference_files:
  face_anchor: ''
  anatomy_sheet: ''
  body_anchor: ''
  ultimate_character_sheet: ''
  signature_outfit_sheet: ''
```

This file stores structured metadata for the character.

---

## `character_summary.md` Template

This file contains a human-readable overview of the character.

Example structure:

```markdown
# Character Summary — [CHARACTER_NAME]

## Core Identity

Name: [CHARACTER_NAME]

Height: [HEIGHT_CM] cm ([HEIGHT_IMPERIAL])

Build Type: [lean / athletic / muscular / heavyset / etc.]

Age Appearance: [approximate age range]

Gender Presentation: [optional]

---

## Visual Identity (Short Prompt Version)

Use this block when a prompt needs a **short character description**.

[CHARACTER_NAME] is a [height + build description] with [key facial features].
Their aesthetic is [style description].

---

## Visual Identity (Full Prompt Version)

Use this block when a prompt needs a **complete character description**.

[CHARACTER_NAME] is [height description] with [body description].

Key features:

- face shape: [description]
- jawline: [description]
- eyes: [description]
- hair: [description]
- skin tone: [description]

Body proportions:

- shoulder width: [description]
- torso shape: [description]
- limb proportions: [description]
- posture: [description]

Overall silhouette:

[describe the recognizable shape of the character]

---

## Style Identity

Aesthetic keywords:

- [style keyword]
- [style keyword]
- [style keyword]

Typical clothing elements:

- [element]
- [element]
- [element]

Typical materials:

- [material]
- [material]

Typical colors:

Primary colors:

- [color]
- [color]

Accent colors:

- [color]

---

## Accessories

Recurring items that often appear with the character:

- [item]
- [item]
- [item]

---

## Body Language

Posture:

[description]

Movement style:

[description]

Gesture style:

[description]

---

## Expression Profile

Default expression:

[description]

Typical smile:

[description]

Emotional range:

[description]

---

## Personality Snapshot

Short personality description used for scene prompts.

[description]

---

## Identity Preservation Rules

These traits should **never drift in generated images**.

Always preserve:

- height range
- body proportions
- facial structure
- hairstyle silhouette
- core aesthetic

Avoid:

- [common drift issue]
- [common drift issue]

---

## Core Reference Sheets

These sheets define the character’s visual identity.

- Face Anchor Sheet
- Anatomy Sheet
- Body Anchor Sheet
- Ultimate Character Sheet
- Signature Outfit Sheet

These should be attached whenever possible.

---

## Identity Pack

The **core reference pack** for prompts:

1. Face Anchor Sheet
2. Anatomy Sheet
3. Ultimate Character Sheet
4. Signature Outfit Sheet

---

## Prompt Identity Block

This block is designed to be **copied directly into prompts**.

[CHARACTER_NAME] is a [height + build] character with [distinctive facial features] and [visual style].
Their aesthetic includes [style keywords], [typical clothing elements], and [accessories].
Maintain consistent facial identity, body proportions, and style across all views.
```

This file acts as a condensed character reference.

---

## `prompt_blocks.md` Template

This file contains reusable prompt fragments that describe the character.

Example structure:

```markdown
# Prompt Blocks — [CHARACTER_NAME]

This file contains reusable prompt fragments describing the character.
Each block can be copied into prompts depending on the generation task.

---

## Identity Block (Short)

Use for:

- quick prompts
- scene prompts
- interaction prompts

[CHARACTER_NAME] is a [height + build description] with [distinctive facial features].
Their aesthetic is [style keywords] with [typical clothing elements].

---

## Identity Block (Extended)

Use for:

- character setup
- detailed prompts
- new chat initialization

[CHARACTER_NAME] is [height description] with [body description].

Key facial traits:

- face shape: [description]
- jawline: [description]
- eyes: [description]
- hair: [description]
- skin tone: [description]

Body proportions:

- shoulder width: [description]
- torso shape: [description]
- limb proportions: [description]
- posture: [description]

Overall silhouette:

[describe the character's recognizable body shape]

---

## Face Block

Use for:

- face anchor prompts
- portrait prompts
- expression sheets

Facial description:

- face shape: [description]
- jawline: [description]
- cheekbones: [description]
- eye shape: [description]
- eyebrow style: [description]
- hairstyle framing the face: [description]

Maintain consistent facial proportions and identity.

---

## Body Block

Use for:

- anatomy prompts
- body anchor prompts
- pose prompts
- scale prompts

[CHARACTER_NAME] is [height description] with a [build description].

Body proportions:

- shoulders: [description]
- torso: [description]
- waist: [description]
- hips: [description]
- limbs: [description]

Posture:

[describe typical posture]

Overall silhouette should read as:

[describe the character's recognizable shape]

---

## Style Block

Use for:

- wardrobe prompts
- outfit generation
- scene prompts

Aesthetic keywords:

- [style keyword]
- [style keyword]
- [style keyword]

Typical clothing elements:

- [element]
- [element]
- [element]

Typical materials:

- [material]
- [material]

Typical color palette:

Primary:

- [color]
- [color]

Accent:

- [color]

---

## Movement Block

Use for:

- pose sheets
- motion anchors
- dynamic scenes

Movement style:

[describe how the character moves]

Posture tendencies:

[describe typical stance]

Gesture style:

[describe how the character uses their hands or body]

---

## Expression Block

Use for:

- expression sheets
- portraits
- interaction scenes

Default expression:

[description]

Typical smile:

[description]

Emotional range:

[description]

Avoid exaggerated or cartoonish expressions unless explicitly requested.

---

## Wardrobe Description Block

Use for:

- outfit sheets
- wardrobe generation
- style prompts

Clothing should reflect:

[aesthetic description]

Common elements:

- [element]
- [element]
- [element]

Accessories may include:

- [item]
- [item]

Avoid styles that conflict with the character’s core aesthetic.

---

## Anti-Drift Rules

These traits must remain consistent across generated images.

Always preserve:

- height and body proportions
- facial structure and identity
- hairstyle silhouette
- core aesthetic style

Avoid:

- [common drift issue]
- [common drift issue]

---

## Short Prompt Description

Copy this block directly into short prompts.

[CHARACTER_NAME] is a [height + build] character with [distinctive facial features].
Their style combines [style keywords] with [typical clothing elements].

---

## Full Prompt Description

Copy this block into prompts that require a full character description.

[CHARACTER_NAME] is [height description] with [body description] and [facial description].
Their aesthetic includes [style keywords], [typical clothing elements], and [accessories].
Maintain consistent facial identity, body proportions, and style across all views.
```

These blocks are combined with prompt templates when generating images.

---

## Minimum Character Setup

Before starting image generation, each character should have:

- a character folder
- completed `metadata.yaml`
- completed `character_summary.md`
- initial `prompt_blocks.md`

Once these are complete, the image generation pipeline can begin.

---

## Recommended Workflow

1. Create character folder.
2. Fill profile files.
3. Generate face anchors.
4. Generate anatomy sheets.
5. Generate body anchors.
6. Generate UCS.
7. Introduce style with signature outfit.
8. Expand into wardrobe, poses, and scenes.
