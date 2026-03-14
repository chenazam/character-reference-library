# Reference Attachment Guide

This page defines which reference sheets should be attached when generating new images in the character pipeline.

Attaching the correct references significantly improves:

- character consistency
- anatomical stability
- clothing continuity
- pose realism
- identity preservation

The goal is **not to attach every available reference**, but to attach the **most relevant references** for the task.

---

# Reference Categories

References fall into three categories.

## Required Inputs

These references are necessary to generate the asset reliably.

They define core identity or structural constraints.

---

## Optional Inputs

These references may improve results but are not strictly necessary.

Attach them when:

- identity drift occurs
- the generator struggles with proportions
- more guidance is beneficial

---

## Avoid by Default

These references should normally **not be attached**, because they can:

- introduce conflicting information
- overload the prompt
- bias the generator toward unrelated visual elements

Only attach them if they are explicitly needed.

---

# Identity Anchor Hierarchy

The following sheets act as identity anchors for the character.

They should override conflicting information from later assets.

1. **Face Anchor (1D)** — authoritative for facial structure
2. **Body Anchor (4)** — authoritative for body proportions
3. **UCS Core (12H)** — authoritative for consolidated character identity
4. **Signature Outfit (13)** — authoritative for clothing identity

If identity drift occurs, prioritize earlier anchors.

---

# Pipeline Reference Attachments

## Quick Reference Map

| Step                | Main purpose                    | Best primary references |
| ------------------- | ------------------------------- | ----------------------- |
| 4 Body Anchor       | stable body identity            | 1D, 2, 3E               |
| 8 Turnaround        | canonical full-body reference   | 4, 7, 1D                |
| 9 Expression Sheet  | expressive facial identity      | 1D, 2                   |
| 10 Hand Sheet       | hand anatomy/style              | 3E, 4                   |
| 11 Gallery Image    | early presentation image        | 1D, 2, 7, 8, 9          |
| 12H UCS Core        | consolidated character identity | 12A–12G                 |
| 13 Signature Outfit | canonical clothing identity     | 12H, 8                  |
| 16 Pose Sheet       | clothed body language           | 13, 8                   |
| 22 Final UCS        | enriched final character sheet  | 12H, 21                 |

---

## Dependency Backbone

```text
1D Face Anchor
  ↓
2 Hair Sheet
  ↓
3E Anatomy Sheet
  ↓
4 Body Anchor
  ├─ 5 Proportion Grid
  ├─ 6 Muscle Tension
  └─ 7 Silhouette
        ↓
        8 Turnaround
          ├─ 9 Expression Sheet
          ├─ 10 Hand Sheet
          ├─ 11 Gallery Image
          └─ 12A–12G UCS Panels
                   ↓
                  12H UCS Core
                    ↓
                   13 Signature Outfit
                    ↓
             14 Design Language / 15 Wardrobes
                    ↓
         16 Pose / 17 Motion / 18 Scale / 19 Interaction / 20 Scenes
                    ↓
              21 Dynamic Pose Panel
                    ↓
                22 Final UCS
```

---

# STAGE 1 — Face Identity

## 1A Front Face

Required inputs

- face source references (if available)

Optional inputs

- none

Avoid by default

- other character sheets

---

## 1B 3/4 Face

Required inputs

- 1A Front Face

Optional inputs

- face source references

Avoid by default

- anatomy sheets
- UCS panels

---

## 1C Profile Face

Required inputs

- 1A Front Face
- 1B 3/4 Face

Optional inputs

- face source references

Avoid by default

- body references

---

## 1D Face Anchor

Required inputs

- 1A Front Face
- 1B 3/4 Face
- 1C Profile Face

Optional inputs

- none

Avoid by default

- UCS sheets
- style sheets

---

# STAGE 2 — Hair Identity

## 2 Hair Sheet

Required inputs

- 1D Face Anchor

Optional inputs

- hair reference photos

Avoid by default

- anatomy sheets
- UCS sheets

---

# STAGE 3 — Physique Anchoring

## 3A Anatomy Front

Required inputs

- 1D Face Anchor
- 2 Hair Sheet

Optional inputs

- body reference images

Avoid by default

- UCS sheets
- outfit references

---

## 3B Anatomy Side

Required inputs

- 3A Anatomy Front
- 1D Face Anchor

Optional inputs

- body references

Avoid by default

- UCS sheets

---

## 3C Anatomy Back

Required inputs

- 3A Anatomy Front
- 3B Anatomy Side

Optional inputs

- body references

Avoid by default

- UCS sheets

---

## 3D Anatomy Glutes (optional)

Required inputs

- 3A Anatomy Front
- 3B Anatomy Side
- 3C Anatomy Back

Optional inputs

- athletic reference photos

Avoid by default

- UCS sheets

---

## 3E Anatomy Sheet

Required inputs

- 3A Anatomy Front
- 3B Anatomy Side
- 3C Anatomy Back

Optional inputs

- 3D Anatomy Glutes

Avoid by default

- clothing references

---

# STAGE 4 — Structural Anchors

## 4 Body Anchor

Required inputs

- 1D Face Anchor
- 2 Hair Sheet
- 3E Anatomy Sheet

Optional inputs

- 3D Anatomy Glutes

Avoid by default

- UCS sheets
- outfit references

---

## 5 Proportion Grid

Required inputs

- 4 Body Anchor
- 3E Anatomy Sheet

Optional inputs

- none

Avoid by default

- UCS sheets

---

## 6 Muscle Tension

Required inputs

- 4 Body Anchor
- 3E Anatomy Sheet

Optional inputs

- athletic reference images

Avoid by default

- UCS sheets

---

## 7 Silhouette

Required inputs

- 4 Body Anchor
- 3E Anatomy Sheet

Optional inputs

- 5 Proportion Grid

Avoid by default

- outfit sheets
- UCS sheets

---

## 8 Turnaround

Required inputs

- 4 Body Anchor
- 7 Silhouette
- 1D Face Anchor

Optional inputs

- 3E Anatomy Sheet

Avoid by default

- outfit sheets

---

# STAGE 5 — Identity Extensions

## 9 Expression Sheet

Required inputs

- 1D Face Anchor
- 2 Hair Sheet

Optional inputs

- 8 Turnaround

Avoid by default

- UCS sheets

---

## 10 Hand Sheet

Required inputs

- 3E Anatomy Sheet
- 4 Body Anchor

Optional inputs

- 8 Turnaround

Avoid by default

- UCS sheets

---

## 11 Gallery Image

Required inputs

- 1D Face Anchor
- 2 Hair Sheet
- 7 Silhouette
- 8 Turnaround
- 9 Expression Sheet

Optional inputs

- 4 Body Anchor

Avoid by default

- UCS sheets
- wardrobe sheets

---

# STAGE 6 — UCS Core Generation

## 12A UCS Front Face Panel

Required inputs

- 1D Face Anchor
- 2 Hair Sheet

Optional inputs

- 9 Expression Sheet

Avoid by default

- body sheets

---

## 12B UCS 3/4 Face Panel

Required inputs

- 12A UCS Front Face Panel
- 1D Face Anchor

Optional inputs

- 2 Hair Sheet

Avoid by default

- body sheets

---

## 12C UCS Profile Face Panel

Required inputs

- 12A UCS Front Face Panel
- 12B UCS 3/4 Face Panel
- 1D Face Anchor

Optional inputs

- 2 Hair Sheet

Avoid by default

- body sheets

---

## 12D UCS Body Front Panel

Required inputs

- 4 Body Anchor
- 8 Turnaround

Optional inputs

- 3E Anatomy Sheet

Avoid by default

- outfit sheets

---

## 12E UCS Body Side Panel

Required inputs

- 4 Body Anchor
- 8 Turnaround

Optional inputs

- 3E Anatomy Sheet

Avoid by default

- outfit sheets

---

## 12F UCS Silhouette Panel

Required inputs

- 4 Body Anchor
- 7 Silhouette

Optional inputs

- none

Avoid by default

- outfit sheets

---

## 12G UCS Expression Panel

Required inputs

- 1D Face Anchor
- 9 Expression Sheet

Optional inputs

- 2 Hair Sheet

Avoid by default

- body sheets

---

## 12H UCS Core Assembly

Required inputs

- 12A–12G panels

Optional inputs

- none

Avoid by default

- dynamic pose panels

---

# STAGE 7 — Style Anchoring

## 13 Signature Outfit

Required inputs

- 12H UCS Core
- 8 Turnaround

Optional inputs

- 4 Body Anchor

Avoid by default

- wardrobe sheets

---

## 14 Design Language Sheet

Required inputs

- 13 Signature Outfit
- 7 Silhouette
- 8 Turnaround

Optional inputs

- style reference images

Avoid by default

- UCS panels

---

## 15 Additional Wardrobes

Required inputs

- 13 Signature Outfit
- 8 Turnaround

Optional inputs

- 14 Design Language Sheet

Avoid by default

- UCS sheets

---

# STAGE 8 — Motion & Character Use

## 16 Pose Sheet

Required inputs

- 13 Signature Outfit
- 8 Turnaround

Optional inputs

- 4 Body Anchor
- 6 Muscle Tension

Avoid by default

- UCS sheets

---

## 17 Motion Anchor

Required inputs

- 16 Pose Sheet
- 4 Body Anchor

Optional inputs

- 6 Muscle Tension

Avoid by default

- UCS sheets

---

## 18 Height Scale Sheet

Required inputs

- 8 Turnaround

Optional inputs

- 4 Body Anchor
- 5 Proportion Grid

Avoid by default

- UCS sheets

---

## 19 Interaction Anchor

Required inputs

- 13 Signature Outfit
- 16 Pose Sheet

Optional inputs

- 10 Hand Sheet

Avoid by default

- UCS sheets

---

## 20 Lifestyle Scene Anchor

Required inputs

- 13 Signature Outfit
- 16 Pose Sheet
- 19 Interaction Anchor

Optional inputs

- environment reference images

Avoid by default

- UCS sheets

---

# STAGE 9 — Final UCS

## 21 UCS Dynamic Pose Panel

Required inputs

- 4 Body Anchor
- 13 Signature Outfit
- 16 Pose Sheet

Optional inputs

- 6 Muscle Tension

Avoid by default

- UCS Core

---

## 22 Final UCS Assembly

Required inputs

- 12H UCS Core
- 21 Dynamic Pose Panel

Optional inputs

- none

Avoid by default

- additional panels

---

# Reference Priority

If the number of references must be limited, prioritize them in this order:

1. Face Anchor (1D)
2. UCS Core (12H)
3. Body Anchor (4)
4. Signature Outfit (13)
5. task-specific references

This priority order preserves character identity and structural consistency.
