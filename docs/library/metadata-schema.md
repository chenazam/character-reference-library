# Metadata Schema

This page defines the standard structure for character `metadata.yaml` files.

The goal of the metadata system is to make character information:

- consistent
- searchable
- useful for prompt construction
- useful for future automation

---

# Top-Level Fields

## `name`

Character display name.

Example:

Lucien

---

## `slug`

Lowercase identifier used in filenames and automation.

Example:

lucien

---

## `status`

Current status of the character.

Recommended values:

- active
- draft
- archived

---

## `project`

Optional project or setting label.

Example:

Occult City

---

# `core_identity`

Stores the character’s most important identity descriptors.

## `short_summary`

One-sentence identity summary.

## `role_archetype`

Narrative or design archetypes.

Examples:

- scholar
- protector
- athlete
- rival
- aristocrat

## `aesthetic_tags`

Primary aesthetic descriptors.

Examples:

- gothic
- athletic
- streetwear
- scholarly
- occult

---

# `physical`

Stores detailed body and silhouette identity.

## Height

### `height_cm`

Height in centimeters.

### `height_imperial`

Height in feet and inches.

### `height_visual_category`

Relative visual category used for scale comparison.

Examples:

- short
- average
- tall
- very_tall

---

## Body Construction

### `build_category`

Primary body-type classification.

See controlled vocabulary.

Examples:

- runner_build
- athletic_muscular
- slender
- heavyset

### `frame_proportion`

Describes the dominant body mass distribution.

Examples:

- leg_dominant
- upper_body_dominant
- balanced_frame

### `body_fat_range`

Approximate body-fat presentation.

Examples:

- very_lean
- athletic_lean
- athletic_average
- soft_average

### `body_softness_distribution`

Where softness or firmness appears on the body.

Examples:

- firm_all
- soft_lower_body
- soft_upper_body

---

## Structural Profiles

### `build_notes`

Natural-language description of the body.

### `shoulder_profile`

Descriptor for shoulder width or shape.

Examples:

- narrow_shoulders
- moderate_shoulders
- broad_shoulders

### `torso_profile`

Descriptor for torso construction.

Examples:

- slender_torso
- athletic_torso
- thick_torso

### `limb_profile`

Descriptor for limbs.

Examples:

- long_limbs
- athletic_limbs
- thick_limbs

### `posture_profile`

General posture type.

Examples:

- relaxed_neutral
- confident_open
- upright_formal

---

### `silhouette_anchor`

Primary silhouette classification used for identity anchoring.

This value captures the character's most recognizable body structure.

Examples:

- runner_silhouette
- power_athlete
- elongated_slender

---

## `silhouette_keywords`

Keywords describing the overall body silhouette.

Examples:

- compact
- broad
- slender
- leg_dominant
- imposing

---

# `face`

Stores facial identity.

## `face_shape`

General face shape.

Examples:

- oval
- square
- heart

## `jawline`

Jawline structure.

Examples:

- defined_jawline
- soft_jawline
- sharp_jawline

## `eye_description`

Short natural-language description.

## `hair_description`

Short hairstyle description.

## `skin_description`

Short skin description.

## `distinctive_features`

List of notable visual traits.

Examples:

- freckles
- strong jawline
- expressive eyes

---

## `hair_color`

Controlled vocabulary for hair color.

Examples:

- dark_brown
- black
- blonde
- light_brown_dark_blonde

---

# `style`

Stores design-language and wardrobe information.

## `primary_aesthetic`

Primary design aesthetic.

Examples:

- athletic
- athletic_luxury
- gothic
- scholarly
- exhibitionist

## `secondary_aesthetic`

Supporting aesthetics.

## `materials`

Common clothing materials.

Examples:

- cotton
- wool
- mesh
- linen

## `primary_colors`

Main color palette.

## `accent_colors`

Accent palette.

## `recurring_accessories`

Recurring wardrobe items.

---

# `expression`

Stores emotional presentation.

## `default_expression`

Neutral resting expression.

## `smile_type`

Typical smile.

## `emotional_tone`

General emotional read.

Examples:

- open_warm
- controlled
- reserved
- playful

---

# `movement`

Stores motion and body-language identity.

## `movement_style`

Overall movement pattern.

Examples:

- restless_quick
- grounded_powerful
- graceful

## `gesture_style`

How the character gestures.

## `body_language`

General body language.

## `spatial_presence`

How the character occupies space.

Examples:

- expansive
- grounded
- compact
- energetic

---

# `identity_rules`

Stores anti-drift rules.

## `preserve`

Traits that must remain stable.

## `avoid`

Common generation failures to prevent.

---

# `reference_files`

Stores filenames for core reference sheets.

These form the character’s **identity pack**.

---

# `pipeline_status`

Tracks completion of the reference pipeline.

Used for workflow tracking and automation.

---

# `notes`

Optional freeform notes.

---

# `last_updated`

Date of the last metadata update.
