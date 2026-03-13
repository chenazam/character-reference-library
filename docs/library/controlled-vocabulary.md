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
| `lower_athletic`    | athletic build with noticeable lower-body dominance              |
| `balanced_athletic` | proportional athletic build with moderate tone and balanced mass |
| `athletic_muscular` | clearly defined muscular physique without extreme bulk           |
| `heavy_muscular`    | thick muscular body with strong mass and visible density         |
| `power_build`       | very broad and powerful build with heavy upper-body presence     |
| `broad_heavy`       | broad frame with substantial overall body mass                   |
| `thick_set`         | dense body build with strong torso mass and compact power        |
| `large_frame`       | naturally large skeletal frame regardless of muscle level        |

---

# Silhouette Anchor

Use these values for `physical.silhouette_anchor`.

| Value               | Description                                                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `runner_silhouette` | lean athletic silhouette with strong lower-body emphasis and light upper-body mass                                           |
| `power_athlete`     | broad, muscular athletic silhouette with dominant shoulders and chest                                                        |
| `elongated_slender` | slender silhouette defined by long limbs and extended vertical proportions                                                   |
| `power_frame`       | extremely broad, dense, muscular silhouette defined by heavy upper-body mass                                                 |
| `glute_slender`     | slender silhouette where the lower body is visually defined by rounded glutes relative to a narrow waist and slim upper body |

---

# Silhouette Keywords

Use these values for `physical.silhouette_keywords`.

| Value          | Description                                                                          |
| -------------- | ------------------------------------------------------------------------------------ |
| compact        | tight, condensed body proportions                                                    |
| tall           | visually tall vertical silhouette                                                    |
| broad          | wide shoulder silhouette                                                             |
| imposing       | large presence with strong physical scale                                            |
| agile          | light, athletic movement-oriented silhouette                                         |
| leg_dominant   | lower body visually emphasized                                                       |
| upper_dominant | upper body visually emphasized                                                       |
| glute_emphasis | silhouette visually defined by prominent rounded glutes relative to waist and thighs |
| heavy_set      | dense mass-focused silhouette                                                        |

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

# Body Fat Ranges

Use these values for `physical.body_fat_range`.

| Value        | Description                |
| ------------ | -------------------------- |
| lean         | visible definition         |
| athletic     | clearly trained physique   |
| soft_average | healthy but untrained body |
| soft_heavy   | noticeable softness        |

---

# Height Visual Categories

Use these values for `physical.height_visual_category`.

| Value      | Description                                                                                                                |
| ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| `short`    | visibly below average height; character reads clearly shorter than most others (approx. under ~170 cm / 5'7")              |
| `medium`   | average or typical height; character reads neither short nor tall in most scenes (approx. ~170–180 cm / 5'7"–5'11")        |
| `tall`     | clearly above average height; character reads noticeably taller than many others (approx. ~180–190 cm / 5'11"–6'3")        |
| `imposing` | extremely tall or physically dominant height presence; character towers over others visually (approx. over ~190 cm / 6'3") |

---

# Body Softness Distributions

Use these values for `physical.body_softness_distribution`.

| Value               | Description                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------- |
| `balanced`          | body softness distributed evenly across torso and limbs                                         |
| `lower_body`        | softness concentrated in hips, glutes, and thighs rather than stomach or chest                  |
| `torso`             | softness concentrated in stomach and waist area                                                 |
| `upper_body`        | softness concentrated in chest, shoulders, and arms                                             |
| `glute_dominant`    | softness concentrated specifically in glutes and hips, creating a rounded lower-body silhouette |
| `firm_all`          | musculature appears firm and defined across the entire body with minimal softness               |
| `soft_lower_body`   | lower body appears slightly softer or fuller compared to upper body                             |
| `soft_upper_body`   | upper body carries slightly more softness than the lower body                                   |
| `balanced_softness` | moderate softness distributed evenly without strong regional emphasis                           |

---

# Frame Proportions

Use these values for `physical.frame_proportion`.

| Value                 | Description                                                                 |
| --------------------- | --------------------------------------------------------------------------- |
| `balanced_frame`      | shoulders, hips, and limbs appear proportionally balanced                   |
| `shoulder_dominant`   | shoulders noticeably wider than hips, upper body visually emphasized        |
| `hip_dominant`        | hips slightly wider relative to shoulders, lower body visually emphasized   |
| `elongated_frame`     | long limbs and extended proportions create a tall visual frame              |
| `compact_frame`       | shorter limbs and condensed proportions create a compact silhouette         |
| `leg_dominant`        | lower body visually dominates the silhouette due to strong thighs or glutes |
| `upper_body_dominant` | shoulders, chest, and arms visually dominate the body structure             |

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

| Value                | Description                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------- |
| `occult`             | ritual, arcane, symbolic, mystical design language                                                |
| `gothic`             | dark, moody, dramatic, ornate visual styling                                                      |
| `scholarly`          | intellectual, academic, bookish, refined styling                                                  |
| `royal`              | noble, aristocratic, elevated styling                                                             |
| `luxury`             | polished, expensive, high-end fashion language                                                    |
| `athletic`           | sport-influenced or activewear-informed styling                                                   |
| `athletic_luxury`    | high-end athletic lifestyle aesthetic                                                             |
| `military`           | uniformed, structured, disciplined style language                                                 |
| `streetwear`         | modern casual urban styling                                                                       |
| `domestic_soft`      | cozy, warm, home-oriented styling                                                                 |
| `romantic`           | soft, elegant, intimate styling                                                                   |
| `playful_athletic`   | sporty, expressive, bold, flirtatious styling                                                     |
| `exhibitionist`      | styling that intentionally shows body or skin                                                     |
| `rugged_utilitarian` | practical, durable clothing emphasizing toughness, function, and intimidation rather than fashion |

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
| `mesh`          | lightweight open-weave fabric                 |

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

# Spatial Presence

Use these values for `movement.spatial_presence`.

| Value                | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| `compact_presence`   | occupies little physical space; posture and stance are contained or inward   |
| `neutral_presence`   | occupies a typical amount of space with relaxed balanced posture             |
| `expansive_presence` | posture and stance naturally spread outward; character visually fills space  |
| `dominant_presence`  | strong physical presence with wide stance and commanding spatial footprint   |
| `grounded`           | stable, planted presence that feels physically heavy and anchored            |
| `expansive`          | character naturally opens their posture and spreads into surrounding space   |
| `energetic`          | presence defined by movement, shifting weight, and dynamic physical activity |

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

---

# TODO — Pair Metadata Vocabulary

Future pair-level aesthetic tags to consider:

- dangerous_romance — intimate dynamic defined by tension between softness and danger
- protective_intimacy — visual dynamic where one character physically protects or dominates space around a partner
