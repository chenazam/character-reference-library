# Characters Overview

The `library/10_CHARACTERS/` directory contains the full reference pipeline for each individual character.

Each character folder stores:

- conceptual profile information
- generated reference sheets
- style anchors
- motion and scene references
- source references used to build the character

This structure is designed so that each character can be rebuilt, maintained, and reused consistently across many AI image generations.

---

## Character Folder Philosophy

Each character is treated as a self-contained reference package.

A complete character folder should contain:

1. **Profile data**  
   Human-readable and machine-readable information about the character.

2. **Identity anchors**  
   Face, anatomy, body, and UCS references that define the character visually.

3. **Style anchors**  
   Signature outfit, design language, and wardrobe sheets.

4. **Motion and scene anchors**  
   Pose sheets, motion sheets, interaction references, and scene anchors.

5. **Source references**  
   Original inspiration or source images used to build the character.

---

## Character Folder Structure

A typical character folder contains the following subfolders:

- `00_PROFILE`
- `01_FACE`
- `02_HAIR`
- `03_ANATOMY`
- `04_PROPORTIONS`
- `05_MUSCLE`
- `06_BODY`
- `07_SILHOUETTE`
- `08_TURNAROUND`
- `09_EXPRESSIONS`
- `10_HANDS`
- `11_UCS`
- `12_SIGNATURE_OUTFIT`
- `13_DESIGN_LANGUAGE`
- `14_WARDROBE`
- `15_POSES`
- `16_MOTION`
- `17_SCALE`
- `18_SCENES`
- `19_PROPS`
- `IDENTITY_PACK`
- `SOURCE_REFERENCES`

See the library folder structure documentation for a more detailed explanation of each folder.

---

## The Most Important Character Files

The most important files for a character are usually:

- Face Anchor Sheet
- Anatomy Sheet
- Body Anchor Sheet
- Ultimate Character Sheet
- Signature Outfit Sheet

Together, these form the character’s core identity pack.

---

## The Profile Folder

The `00_PROFILE` folder contains the conceptual definition of the character.

Typical files include:

- `metadata.yaml` — structured character metadata
- `character_summary.md` — human-readable overview
- `prompt_blocks.md` — reusable character-specific prompt fragments

These files define the character in text form before or alongside the image-based references.

---

## Character Lifecycle

A new character is usually created in this order:

1. Create the character folder structure
2. Fill out the `00_PROFILE` files
3. Generate face identity references
4. Generate anatomy and body structure anchors
5. Generate the Ultimate Character Sheet
6. Introduce style through the signature outfit and design language sheets
7. Expand into poses, wardrobe, motion, and scene use

---

## Goal

The goal of the character system is to make each character:

- easy to understand
- easy to regenerate
- easy to use in prompts
- resistant to visual drift
