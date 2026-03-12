# Controlled Vocabulary

This page defines standardized values used in character metadata.

The purpose of this vocabulary is to keep character descriptions consistent across:

- metadata files
- summary pages
- prompt blocks
- gallery pages
- future automation

Use these values whenever possible instead of inventing new terms for each character.

---

# Build Categories

Use these values for `physical.build_category`.

| Value               | Description                                                      |
| ------------------- | ---------------------------------------------------------------- |
| `soft_slender`      | slender frame with soft musculature and refined proportions      |
| `narrow_slender`    | slender build with a narrow frame and delicate body structure    |
| `elongated_slender` | slender build with visibly long limbs and elongated proportions  |
| `light_athletic`    | lightly toned body with visible fitness but little bulk          |
| `runner_build`      | athletic build with lower-body emphasis and lean overall mass    |
| `balanced_athletic` | proportional athletic build with moderate tone and balanced mass |
| `athletic_muscular` | clearly defined muscular physique without extreme bulk           |
| `heavy_muscular`    | thick muscular body with strong mass and visible density         |
| `power_build`       | very broad and powerful build with heavy upper-body presence     |
| `broad_heavy`       | broad frame with substantial overall body mass                   |
| `thick_set`         | dense body build with strong torso mass and compact power        |
| `large_frame`       | naturally large skeletal frame regardless of muscle level        |

---

# Shoulder Profiles

Use these values for `physical.shoulder_profile`.

| Value                | Description                             |
| -------------------- | --------------------------------------- |
| `narrow_shoulders`   | visibly narrow shoulder width           |
| `moderate_shoulders` | balanced shoulder width                 |
| `broad_shoulders`    | visibly wide shoulder width             |
| `heavy_shoulders`    | thick, mass-heavy shoulder construction |

---

# Torso Profiles

Use these values for `physical.torso_profile`.

| Value            | Description                              |
| ---------------- | ---------------------------------------- |
| `slim_torso`     | narrow torso with low bulk               |
| `soft_torso`     | lightly built torso with soft definition |
| `athletic_torso` | toned torso with visible definition      |
| `broad_torso`    | wide torso with strong width             |
| `thick_torso`    | dense, heavy torso mass                  |

---

# Limb Profiles

Use these values for `physical.limb_profile`.

| Value            | Description                          |
| ---------------- | ------------------------------------ |
| `delicate_limbs` | slim, fine-boned limb structure      |
| `slender_limbs`  | narrow limbs with understated mass   |
| `long_limbs`     | visibly elongated limbs              |
| `athletic_limbs` | toned limbs with moderate definition |
| `thick_limbs`    | limbs with strong width and density  |

---

# Posture Profiles

Use these values for `physical.posture_profile`.

| Value                | Description                                |
| -------------------- | ------------------------------------------ |
| `upright_controlled` | straight, composed posture with control    |
| `relaxed_neutral`    | natural, relaxed standing posture          |
| `grounded_stable`    | heavy, planted posture with strong balance |
| `soft_reserved`      | slightly inward, gentle posture            |
| `confident_open`     | open posture with visible confidence       |

---

# Face Shapes

Use these values for `face.face_shape`.

| Value            | Description                                  |
| ---------------- | -------------------------------------------- |
| `oval`           | balanced oval face shape                     |
| `long_oval`      | elongated oval face                          |
| `heart_shaped`   | wider upper face tapering to a narrower chin |
| `square`         | strong, angular shape with straight edges    |
| `narrow_angular` | slim face with defined planes and angularity |
| `soft_round`     | rounded shape with softer structure          |

---

# Jawline Types

Use these values for `face.jawline`.

| Value             | Description                              |
| ----------------- | ---------------------------------------- |
| `soft_jawline`    | gentle jaw structure with low angularity |
| `defined_jawline` | clearly structured but not overly sharp  |
| `sharp_jawline`   | visibly angular and pronounced           |
| `broad_jawline`   | wide jaw structure with strong base      |

---

# Primary Aesthetic Tags

Use these values for `style.primary_aesthetic` or `core_identity.aesthetic_tags`.

| Value           | Description                                        |
| --------------- | -------------------------------------------------- |
| `occult`        | ritual, arcane, symbolic, mystical design language |
| `gothic`        | dark, moody, dramatic, ornate visual styling       |
| `scholarly`     | intellectual, academic, bookish, refined styling   |
| `royal`         | noble, aristocratic, elevated styling              |
| `luxury`        | polished, expensive, high-end fashion language     |
| `athletic`      | sport-influenced or activewear-informed styling    |
| `military`      | uniformed, structured, disciplined style language  |
| `streetwear`    | modern casual urban styling                        |
| `domestic_soft` | cozy, warm, home-oriented styling                  |
| `romantic`      | soft, elegant, intimate styling                    |

---

# Materials

Use these values for `style.materials`.

| Value           | Description                                   |
| --------------- | --------------------------------------------- |
| `wool`          | matte, soft woven fabric                      |
| `velvet`        | rich soft pile fabric with subtle sheen       |
| `linen`         | light natural woven material                  |
| `cotton`        | basic soft everyday fabric                    |
| `leather`       | structured leather material                   |
| `antique_metal` | aged metal, jewelry, clasps, symbolic objects |
| `silk`          | smooth elegant fabric with soft sheen         |

---

# Expression Defaults

Use these values for `expression.default_expression`.

| Value                | Description                                |
| -------------------- | ------------------------------------------ |
| `calm_reserved`      | composed and restrained neutral expression |
| `soft_neutral`       | gentle, open neutral expression            |
| `serious_controlled` | focused and emotionally contained          |
| `confident_neutral`  | self-assured neutral expression            |
| `watchful_distant`   | observant and slightly emotionally removed |

---

# Smile Types

Use these values for `expression.smile_type`.

| Value              | Description                           |
| ------------------ | ------------------------------------- |
| `subtle_smile`     | understated, restrained smile         |
| `warm_smile`       | gentle open smile                     |
| `playful_smile`    | teasing, lively smile                 |
| `rare_broad_smile` | broad smile that appears infrequently |

---

# Emotional Tone

Use these values for `expression.emotional_tone`.

| Value        | Description                                      |
| ------------ | ------------------------------------------------ |
| `controlled` | emotions feel measured and contained             |
| `open_warm`  | emotions read easily and warmly                  |
| `guarded`    | emotional presentation feels partially protected |
| `intense`    | emotions read strongly and directly              |
| `gentle`     | emotional presentation feels soft and mild       |

---

# Movement Styles

Use these values for `movement.movement_style`.

| Value                | Description                         |
| -------------------- | ----------------------------------- |
| `deliberate_precise` | careful, intentional movement       |
| `fluid_graceful`     | smooth, elegant movement            |
| `relaxed_natural`    | easy, ordinary movement             |
| `grounded_powerful`  | strong, planted movement            |
| `restless_quick`     | quick, energetic, shifting movement |

---

# Gesture Styles

Use these values for `movement.gesture_style`.

| Value             | Description                      |
| ----------------- | -------------------------------- |
| `restrained`      | minimal, controlled gestures     |
| `expressive`      | clear visible hand/body gestures |
| `precise`         | sharp, intentional gestures      |
| `soft_gentle`     | mild, low-force gestures         |
| `broad_confident` | larger, open, confident gestures |

---

# Body Language Types

Use these values for `movement.body_language`.

| Value              | Description                                   |
| ------------------ | --------------------------------------------- |
| `calm_composed`    | physically controlled and poised              |
| `guarded_reserved` | slightly closed or protected body language    |
| `open_confident`   | accessible, confident, expanded body language |
| `soft_withdrawn`   | quiet, inward, gentle physical presentation   |
| `intense_focused`  | strong concentration and directed physicality |
