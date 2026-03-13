# Pair Templates

This page explains how to create and organize **character pairs** in the reference library.

Character pairs represent **two characters that frequently appear together** and have a recognizable visual relationship.

Examples:

- romantic pairs
- rivals
- siblings
- mentor/student
- teammates

Pairs focus on **visual dynamics between characters**, not just their individual identities.

---

# Pair Folder Structure

Pairs are stored in:

```
docs/assets/library/20_CHARACTER_PAIRS/
```

Each pair has its own folder.

Example:

```
20_CHARACTER_PAIRS/
  BLAKE_JASPER/
```

Inside that folder the structure is:

```
BLAKE_JASPER/
  00_PROFILE/
  01_SCALE/
  02_DYNAMICS/
  03_WARDROBE/
  04_SCENES/

  IDENTITY_PACK/
  SOURCE_REFERENCES/
```

Unlike individual characters, pair folders focus on **relationship assets** rather than individual anatomy or wardrobe.

---

# Pair Pipeline Overview

The pair pipeline focuses on the **visual relationship between two characters**.

Typical stages include:

| Stage    | Purpose                                     |
| -------- | ------------------------------------------- |
| Profile  | Define the pair identity and dynamics       |
| Scale    | Establish height and build relationships    |
| Dynamics | Capture body language and interaction style |
| Wardrobe | Explore coordinated or contrasting outfits  |
| Scenes   | Anchor the pair in shared environments      |

---

# 00_PROFILE

The profile folder defines the **identity of the pair itself**.

```
00_PROFILE/
  metadata.yaml
  pair_summary.md
  prompt_blocks.md
  identity_guardrails.md
```

---

## metadata.yaml

Structured metadata describing the pair.

Contains:

- member characters
- dynamic keywords
- style relationship
- height relationship
- visual contrast notes

Used for:

- library indexing
- prompt generation
- documentation.

---

## pair_summary.md

Human-readable overview of the pair.

Includes:

- core identity description
- dynamic summary
- height and scale relationship
- styling relationship
- identity preservation notes.

This document explains **how the pair should visually read together**.

---

## prompt_blocks.md

Reusable prompt fragments describing the pair.

Typical blocks include:

- pair character block
- extended identity block
- scale block
- dynamic block
- style relationship block

These blocks can be copied directly into prompts.

---

## identity_guardrails.md

Defines **non-negotiable visual rules** for the pair.

This file prevents identity drift when generating images.

Typical sections include:

- core pair locks
- scale guardrails
- identity guardrails
- dynamic guardrails
- style guardrails
- known generator drift risks
- reference hierarchy

Guardrails are used when reviewing generated images or troubleshooting identity problems.

---

# 01_SCALE

Scale sheets define **relative physical relationships**.

Examples:

```
blake_jasper_height_comparison_v1.png
blake_jasper_scale_sheet_v1.png
```

These sheets establish:

- height differences
- build contrast
- silhouette relationships.

---

# 02_DYNAMICS

Dynamic sheets capture **how the characters interact visually**.

Examples:

```
blake_jasper_interaction_anchor_v1.png
blake_jasper_dynamic_pose_sheet_v1.png
blake_jasper_body_language_sheet_v1.png
```

These sheets define:

- posture dynamics
- interaction tone
- body language relationships.

---

# 03_WARDROBE

Pair wardrobe sheets explore **coordinated styling**.

Examples:

```
blake_jasper_shared_style_sheet_v1.png
blake_jasper_outfit_coordination_v1.png
```

These sheets show how characters:

- complement each other stylistically
- contrast visually while remaining cohesive.

---

# 04_SCENES

Scene anchors show the pair interacting in **shared environments**.

Examples:

```
blake_jasper_lifestyle_scene_anchor_v1.png
blake_jasper_environment_interaction_v1.png
```

These sheets help stabilize:

- scene composition
- interaction dynamics
- spatial relationships.

---

# Identity Pack

```
IDENTITY_PACK/
```

This folder stores curated assets used to stabilize generation:

- face anchors
- body anchors
- pair interaction anchors
- scale references.

These are the most important references when generating pair scenes.

---

# Source References

```
SOURCE_REFERENCES/
```

Stores external references and legacy assets.

Examples:

```
SOURCE_REFERENCES/
  inspiration/
  legacy_pipeline/
  raw/
```

These assets may not follow the pipeline layout but remain valuable references.

---

# Naming Conventions

Pair folders use **uppercase member names separated by underscores**.

Example:

```
BLAKE_JASPER
```

File naming convention:

```
blake_jasper_height_comparison_v1.png
blake_jasper_interaction_anchor_v1.png
blake_jasper_scene_anchor_v1.png
```

---

# Creating a New Pair

1. Copy the pair scaffolding folder:

```
scaffolding/pair/
```

2. Rename it:

```
PAIR_NAME
```

3. Place it inside:

```
docs/assets/library/20_CHARACTER_PAIRS/
```

4. Fill in:

- metadata.yaml
- pair_summary.md
- prompt_blocks.md
- identity_guardrails.md

5. Generate pair reference sheets.

---

# Relationship to Character Assets

Pair assets do **not replace individual character references**.

Instead they complement them.

Pair prompts should attach:

1. pair interaction anchors
2. pair scale sheets
3. individual character face anchors
4. individual body anchors

This preserves both:

- individual character identity
- pair dynamics.
