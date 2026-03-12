# Metadata Schema

This page defines the standard structure for character `metadata.yaml` files.

The goal of the metadata system is to make character information:

- consistent
- searchable
- useful for prompt construction
- useful for future automation

---

## Top-Level Fields

### `name`

Character display name.

Example:

`Lucien`

---

### `slug`

Lowercase identifier used in filenames and automation.

Example:

`lucien`

---

### `status`

Current status of the character.

Recommended values:

- `active`
- `draft`
- `archived`

---

### `project`

Optional project or setting label.

Example:

`Occult City`

---

## `core_identity`

Stores the character’s most important high-level identity tags.

### `short_summary`

One-sentence summary of the character.

### `role_archetype`

Narrative or design archetypes.

Examples:

- scholar
- rival
- protector
- aristocrat

### `aesthetic_tags`

Main aesthetic descriptors.

Examples:

- occult
- gothic
- scholarly
- royal

---

## `physical`

Stores body and silhouette information.

### `height_cm`

Height in centimeters.

### `height_imperial`

Height in feet and inches.

### `build_category`

Controlled vocabulary field describing body type.

See the controlled vocabulary page.

### `build_notes`

Short natural-language expansion of the build.

### `shoulder_profile`

Short descriptor for shoulder width / shape.

### `torso_profile`

Short descriptor for torso construction.

### `limb_profile`

Short descriptor for limb length / thickness.

### `posture_profile`

Short descriptor for posture.

### `silhouette_keywords`

Short tags describing the overall silhouette.

Examples:

- slender
- long-limbed
- compact
- broad

---

## `face`

Stores facial identity information.

### `face_shape`

General face shape.

### `jawline`

Jawline description.

### `eye_description`

Short eye description.

### `hair_description`

Short hairstyle description.

### `skin_description`

Short skin description.

### `distinctive_features`

List of notable facial identity markers.

---

## `style`

Stores style and design-language information.

### `primary_aesthetic`

Main aesthetic label.

### `secondary_aesthetic`

Supporting aesthetics.

### `materials`

Common clothing/material descriptors.

### `primary_colors`

Main palette colors.

### `accent_colors`

Accent colors.

### `recurring_accessories`

Accessories or objects that recur often.

---

## `expression`

Stores emotional presentation defaults.

### `default_expression`

Typical resting expression.

### `smile_type`

Typical smile description.

### `emotional_tone`

General emotional read.

---

## `movement`

Stores movement and body-language information.

### `movement_style`

How the character moves overall.

### `gesture_style`

How the character uses hands / gestures.

### `body_language`

General physical demeanor.

---

## `identity_rules`

Stores anti-drift rules.

### `preserve`

Traits that should remain stable.

### `avoid`

Common failure modes to avoid.

---

## `reference_files`

Stores the filenames of the character’s most important anchor sheets.

These files form the character’s core identity pack.

---

## `pipeline_status`

Tracks which parts of the reference pipeline are complete.

This is useful for workflow management and future automation.

---

## `notes`

Optional freeform notes.

---

## `last_updated`

Date of last metadata update.
