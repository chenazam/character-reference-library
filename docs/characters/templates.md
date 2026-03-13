# Character Templates

This page explains how to create and organize **individual characters** in the reference library.

Character folders represent the **core unit of the library**. Each character stores their profile information, generated reference sheets, identity packs, and source references.

The purpose of the character template system is to ensure that all characters:

- follow the same folder structure
- use the same profile file schema
- move through the same reference pipeline
- remain easy to browse in the MkDocs frontend

---

# Character Page Layout

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

A reusable page template is provided here:

```text
docs/characters/character-page-template.md
```

When creating a new character page:

1. copy the template
2. rename it to the character name
3. replace placeholder paths
4. add gallery snippets or thumbnails for the character’s available sheets

These pages are optimized for **visual browsing and prompt construction**, rather than for template storage.

---

# Character Folder Structure

Characters are stored in:

```text
docs/assets/library/10_CHARACTERS/
```

Each character has its own folder.

Example:

```text
10_CHARACTERS/
  LUCIEN/
```

Inside that folder the structure is:

```text
LUCIEN/
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

Each numbered folder corresponds to a stage in the character generation pipeline.

---

# Creating a New Character

To create a new character:

1. copy the character scaffolding folder:

```text
scaffolding/character/
```

2. rename it to the character name
3. place it inside:

```text
docs/assets/library/10_CHARACTERS/
```

4. fill out the files in `00_PROFILE`
5. begin generating the character’s reference sheets following the pipeline

This is preferred over copying an existing character folder and deleting old assets.

---

# 00_PROFILE

The `00_PROFILE` folder contains the **conceptual definition of the character**.

```text
00_PROFILE/
  metadata.yaml
  character_summary.md
  prompt_blocks.md
  identity_guardrails.md
```

These files define the character before reference sheets are generated.

---

## metadata.yaml

Structured metadata describing the character.

Typical contents include:

- core identity summary
- physical information
- facial information
- style information
- expression and movement traits
- identity rules
- reference file links
- pipeline progress

This file is used for:

- structured character data
- indexing
- future automation
- library maintenance

The canonical template lives in:

```text
scaffolding/character/00_PROFILE/metadata.yaml
```

---

## character_summary.md

Human-readable overview of the character.

This file typically includes:

- core identity
- short and full visual identity descriptions
- silhouette summary
- style identity
- body language
- expression profile
- identity preservation rules
- core reference sheets

This file acts as a **condensed character reference document**.

The canonical template lives in:

```text
scaffolding/character/00_PROFILE/character_summary.md
```

---

## prompt_blocks.md

Reusable prompt fragments describing the character.

Typical blocks include:

- Character Block
- Identity Block (Short)
- Identity Block (Extended)
- Face Block
- Body Block
- Style Block
- Movement Block
- Expression Block
- Wardrobe Description Block
- Anti-Drift Rules
- Short Prompt Description
- Full Prompt Description

These blocks are used when building prompts for reference generation and later scenes.

The canonical template lives in:

```text
scaffolding/character/00_PROFILE/prompt_blocks.md
```

---

## identity_guardrails.md

Defines **non-negotiable identity constraints** for the character.

This file is used when:

- generating new reference sheets
- creating outfits or scenes
- troubleshooting generator drift
- reviewing whether an image still reads as the same character

Typical contents include:

- core identity locks
- silhouette guardrails
- facial guardrails
- style guardrails
- expression guardrails
- movement guardrails
- known generator drift risks
- reference hierarchy
- identity test checklist

This file should be concise but clear. Some characters may need only a short version, while others benefit from more detailed guardrails.

The canonical template lives in:

```text
scaffolding/character/00_PROFILE/identity_guardrails.md
```

---

# Identity Pack

```text
IDENTITY_PACK/
```

This folder stores the **most important identity-stabilizing references** for the character.

Examples:

- face anchors
- body anchors
- turnaround sheets
- signature outfit references

These are the assets most likely to be attached during prompt generation.

---

# Source References

```text
SOURCE_REFERENCES/
```

This folder stores external references and non-canonical source material.

Examples:

```text
SOURCE_REFERENCES/
  legacy_pipeline/
  inspiration/
  raw/
```

This may include:

- cropped legacy images
- older pipeline outputs
- inspiration images
- raw generation outputs

These assets do not need to follow the current sheet layout to remain useful.

---

# Character Pipeline Overview

The individual character pipeline focuses on defining the character’s **own identity and structure**.

Typical stages include:

| Stage                           | Purpose                                    |
| ------------------------------- | ------------------------------------------ |
| Face                            | establish facial identity                  |
| Hair                            | define hairstyle consistency               |
| Anatomy                         | define body construction                   |
| Body / Silhouette / Turnaround  | stabilize full-body identity               |
| Expression / Hands              | define expressive range                    |
| UCS                             | consolidate identity into one master sheet |
| Outfit / Design Language        | define style and wardrobe                  |
| Poses / Motion / Scale / Scenes | expand character usage                     |

---

# Minimum Character Setup

Before starting image generation, each character should have:

- a character folder created from scaffolding
- completed `metadata.yaml`
- completed `character_summary.md`
- completed `prompt_blocks.md`
- an initial `identity_guardrails.md`

Once these are in place, the visual reference pipeline can begin.

---

# Recommended Workflow

1. create the character folder from scaffolding
2. fill in `00_PROFILE`
3. generate face references
4. generate anatomy references
5. generate body identity sheets
6. generate UCS
7. generate signature outfit and design language
8. expand into wardrobe, poses, motion, scale, scenes, and props

---

# Relationship to Other Template Pages

This page documents **individual character templates**.

Related pages:

- `docs/pairs/templates.md` for character pairs
- `docs/groups/templates.md` for groups
- `docs/prompts/templates-index.md` for prompt template browsing

Character templates define the **individual unit** of the library. Pairs and groups define **relationship-focused units** built on top of those individual characters.
