# Face Anchor Sheet — v2

Create a clean, structured face anchor reference sheet for a character design pipeline.

This asset is used to lock the character’s facial identity across multiple angles.  
The result must be highly consistent, neutral, and optimized for reuse in downstream generation.

---

## Character

<INSERT CHARACTER DESCRIPTION HERE>

---

## Reference Input

Use the provided references with the following priority:

1. Front view → primary identity anchor
2. Side view → profile accuracy
3. Three-quarter view → supporting reference only

If conflicts occur, prioritize:
front > side > three-quarter

These references collectively define the canonical appearance of the character.

Strictly preserve across all views:

- facial structure (bone structure, proportions)
- eye shape, spacing, and alignment
- nose shape and projection
- mouth shape and proportions
- jawline and chin structure
- cheekbone structure
- hairstyle, hairline, and volume
- overall likeness and identity

Do NOT reinterpret, redesign, or average the face across views.

Each reference represents the same individual from a different angle and must remain consistent.

---

## Identity Preservation (CRITICAL)

- all views must depict the exact same person
- the provided references define the canonical facial identity

- do not reinterpret, idealize, or average facial features across views
- do not generate a new or modified version of the face

- preserve consistently across all views:
  - eye shape, size, and spacing
  - nose shape and projection
  - jawline shape and chin structure
  - cheekbone structure
  - overall facial proportions

- each view must be a consistent representation of the same head from different angles

- prioritize identity consistency over stylistic or photographic variation
- the result should be clearly recognizable as the same individual in all panels

---

## Panel Assignment (STRICT)

The output MUST contain exactly three panels arranged horizontally:

LEFT PANEL:

- front view
- perfectly forward-facing
- both eyes symmetrical

CENTER PANEL:

- side profile
- exact 90° profile
- only one eye visible

RIGHT PANEL:

- three-quarter view (~45°)
- both eyes visible
- far eye partially occluded

Do NOT change the order.
Do NOT merge or duplicate views.
Each panel must represent a clearly distinct angle.

---

## Angle Separation (CRITICAL)

The three-quarter view MUST NOT approach a full profile.

- clear visibility of both eyes is required
- the nose must NOT align with the facial outline
- the far cheek must remain visible

The side view MUST remain a strict 90° profile.

These two views must be visually distinct and not interchangeable.

---

## View Consistency (CRITICAL)

- each panel must directly reflect the provided reference views
- do not reinterpret, redraw, or modify the face in any panel
- do not generate a new version of the face

- the task is to arrange consistent views of the same head, not to re-render or improve them

- preserve the exact facial structure and appearance from the input references in each corresponding view

---

## Layout Constraints

- wide horizontal canvas (landscape orientation)
- three evenly spaced vertical panels
- equal panel width
- consistent head size across panels

Do NOT:

- stack panels vertically
- crop panels unevenly
- output a single image instead of a 3-panel sheet

---

## Panels

Include exactly three panels:

1. Front view (perfectly front-facing)
2. Side view (true 90° profile)
3. Three-quarter view (approximately 45° rotation)

---

## Expression

- neutral expression
- relaxed face
- closed mouth
- no exaggerated emotion

---

## Pose & Framing

- head and upper neck visible
- minimal shoulder inclusion (do not include full torso)
- consistent scale across all panels
- all heads aligned to the same vertical height
- all panels centered and evenly spaced

---

## Camera & Perspective

- orthographic or near-orthographic look (avoid strong perspective distortion)
- consistent focal length across all panels
- no lens distortion

---

## Lighting

- soft, neutral studio lighting
- even illumination across the face
- no dramatic shadows
- no directional mood lighting

---

## Style

- semi-realistic rendering
- clean and controlled
- minimal stylization
- avoid painterly exaggeration
- avoid hyper-photographic noise

The result should sit between:
photographic realism and clean illustration

---

## Background

- plain light neutral background
- no gradients or textures

---

## Layout

- horizontal three-panel layout
- evenly spaced panels
- no overlap between panels

---

## Labels

Include small, clean labels beneath each panel:

- "Front View"
- "Side View"
- "Three-Quarter View"

Typography:

- simple sans-serif
- neutral styling
- no decorative fonts

---

## Restrictions

Do NOT include:

- character name
- borders or frames
- additional design elements
- clothing details beyond minimal neckline
- accessories (unless essential to identity)

---

## Output Requirements

- single unified image
- three clearly separated panels
- consistent proportions across all views
- high clarity and readability
- identity must match the input reference exactly
