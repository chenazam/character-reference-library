# Character Asset Pipeline Matrix

## Column systems

### For **source assets (prompt-generated)**

| Column      | Meaning                                  |
| ----------- | ---------------------------------------- |
| Face        | Uses face identity block                 |
| Body        | Uses body identity block                 |
| Hair        | Uses hair identity block                 |
| Style       | Uses style/aesthetic block               |
| Outfit      | Uses outfit block                        |
| Guardrails  | Uses identity guardrails                 |
| Strict View | Requires explicit view/orientation block |
| Layout      | Requires prompt-level layout constraints |
| Pair Logic  | Requires pair composition logic          |
| Scene Logic | Requires narrative/staging logic         |

---

### For **derived sheets (script-assembled)**

| Column        | Meaning                         |
| ------------- | ------------------------------- |
| Source Assets | Required input images           |
| Assembly Spec | Template / composition logic    |
| Labels        | Text/labels required            |
| Layout Rules  | Panel arrangement rules         |
| Normalization | Scale/background/crop alignment |

---

---

# A. Face identity assets

## Source assets

| Asset Type                      | Family | Output | Face |  Body | Hair | Style |   Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes                 |
| ------------------------------- | ------ | ------ | ---: | ----: | ---: | ----: | -------: | ---------: | ----------: | -----: | ---: | ----: | --------------------- |
| Front face reference            | Face   | source |  yes |    no |  yes |    no |       no |        yes |         yes |  light |   no |    no | Canonical face anchor |
| Side face reference             | Face   | source |  yes |    no |  yes |    no |       no |        yes |         yes |  light |   no |    no | Profile definition    |
| Three-quarter face reference    | Face   | source |  yes |    no |  yes |    no |       no |        yes |         yes |  light |   no |    no | Bridge view           |
| Neutral portrait identity image | Face   | source |  yes | light |  yes | light | optional |        yes |         yes |  light |   no |    no | Slightly more natural |

---

## Derived sheets

| Asset Type                        | Family          | Output  | Source Assets             | Assembly Spec       | Labels | Layout Rules      | Normalization       | Notes                     |
| --------------------------------- | --------------- | ------- | ------------------------- | ------------------- | ------ | ----------------- | ------------------- | ------------------------- |
| Face anchor sheet                 | Face            | derived | front, 3Q, side face refs | face sheet template | yes    | fixed panel order | crop + scale match  | Core identity sheet       |
| Expression-neutral close-up sheet | Face            | derived | multiple close-up refs    | close-up grid       | yes    | aligned grid      | crop normalization  | Optional                  |
| Expression sheet                  | Pose/Expression | derived | expression panels         | expression grid     | yes    | ordered grid      | scale normalization | Identity under expression |

---

# B. Body structure / anatomy assets

## Source assets

| Asset Type                         | Family     | Output |  Face | Body | Hair | Style | Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes               |
| ---------------------------------- | ---------- | ------ | ----: | ---: | ---: | ----: | -----: | ---------: | ----------: | -----: | ---: | ----: | ------------------- |
| Front anatomy reference            | Body       | source | light |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Core proportions    |
| Side anatomy reference             | Body       | source | light |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Profile depth       |
| Back anatomy reference             | Body       | source |    no |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Posterior structure |
| Three-quarter body anchor          | Body       | source | light |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Volume bridge       |
| Front silhouette reference         | Silhouette | source |    no |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Outline read        |
| Side silhouette reference          | Silhouette | source |    no |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Optional            |
| Back silhouette reference          | Silhouette | source |    no |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Optional            |
| Three-quarter silhouette reference | Silhouette | source |    no |  yes |  yes |    no |     no |        yes |         yes |  light |   no |    no | Optional            |

---

## Derived sheets

| Asset Type                | Family     | Output  | Source Assets                 | Assembly Spec       | Labels   | Layout Rules    | Normalization            | Notes             |
| ------------------------- | ---------- | ------- | ----------------------------- | ------------------- | -------- | --------------- | ------------------------ | ----------------- |
| Full body anchor sheet    | Body       | derived | front, side, back, 3Q anatomy | body sheet template | yes      | fixed layout    | scale + background unify | Master body sheet |
| Proportion grid reference | Body       | derived | front anatomy                 | grid overlay        | optional | exact alignment | canvas normalization     | Technical asset   |
| Silhouette sheet          | Silhouette | derived | silhouette refs               | silhouette template | yes      | uniform sizing  | background normalization | Outline library   |

---

# B2. Specialized anatomy assets

## Source assets

| Asset Type                                    | Family | Output | Face | Body | Hair | Style | Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes                             |
| --------------------------------------------- | ------ | ------ | ---: | ---: | ---: | ----: | -----: | ---------: | ----------: | -----: | ---: | ----: | --------------------------------- |
| Specialized anatomy close-up (single view)    | Body   | source |   no |  yes |   no |    no |     no |        yes |         yes |  light |   no |    no | e.g. glutes, chest, thighs        |
| Specialized anatomy close-up (multi-view set) | Body   | source |   no |  yes |   no |    no |     no |        yes |         yes |  light |   no |    no | front / side / 3Q / back variants |

---

## Derived sheets

| Asset Type                          | Family | Output  | Source Assets       | Assembly Spec          | Labels | Layout Rules  | Normalization              | Notes                         |
| ----------------------------------- | ------ | ------- | ------------------- | ---------------------- | ------ | ------------- | -------------------------- | ----------------------------- |
| Specialized anatomy reference sheet | Body   | derived | multi-view closeups | anatomy-sheet template | yes    | ordered views | scale + crop normalization | e.g. glute sheet, chest sheet |

---

# C. Clothing / wardrobe assets

## Source assets

| Asset Type             | Family   | Output |  Face | Body | Hair | Style | Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes |
| ---------------------- | -------- | ------ | ----: | ---: | ---: | ----: | -----: | ---------: | ----------: | -----: | ---: | ----: | ----- |
| Front outfit reference | Clothing | source | light |  yes |  yes | light |    yes |        yes |         yes |  light |   no |    no |       |
| Side outfit reference  | Clothing | source |    no |  yes |  yes | light |    yes |        yes |         yes |  light |   no |    no |       |
| Back outfit reference  | Clothing | source |    no |  yes |  yes | light |    yes |        yes |         yes |  light |   no |    no |       |

---

## Derived sheets

| Asset Type              | Family   | Output  | Source Assets               | Assembly Spec       | Labels   | Layout Rules      | Normalization            | Notes               |
| ----------------------- | -------- | ------- | --------------------------- | ------------------- | -------- | ----------------- | ------------------------ | ------------------- |
| Outfit turnaround sheet | Clothing | derived | front/side/back outfit refs | turnaround template | yes      | ordered views     | body scale normalization | Core clothing asset |
| Alternate outfit sheet  | Clothing | derived | alt outfit refs             | same template       | yes      | consistent layout | normalization            |                     |
| Garment detail sheet    | Clothing | derived | detail panels               | detail layout       | yes      | modular grid      | crop normalization       |                     |
| Footwear reference      | Clothing | derived | footwear panels             | detail layout       | optional | grid              | crop normalization       |                     |
| Accessory reference     | Clothing | derived | accessory panels            | detail layout       | optional | grid              | crop normalization       |                     |
| Uniform reference sheet | Clothing | derived | uniform refs                | uniform template    | yes      | strict layout     | normalization            |                     |

---

# D. Gallery / library assets

## Source assets

| Asset Type                 | Family  | Output | Face |  Body | Hair | Style |   Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes |
| -------------------------- | ------- | ------ | ---: | ----: | ---: | ----: | -------: | ---------: | ----------: | -----: | ---: | ----: | ----- |
| Gallery portrait           | Gallery | source |  yes | light |  yes |   yes | optional |        yes |         yes |    yes |   no |    no |       |
| Gallery full-body portrait | Gallery | source |  yes |   yes |  yes |   yes |      yes |        yes |         yes |    yes |   no |    no |       |
| Catalog thumbnail image    | Gallery | source |  yes |    no |  yes |   yes | optional |        yes |         yes |    yes |   no |    no |       |

---

## Derived sheets

| Asset Type              | Family  | Output  | Source Assets             | Assembly Spec     | Labels | Layout Rules      | Normalization             | Notes |
| ----------------------- | ------- | ------- | ------------------------- | ----------------- | ------ | ----------------- | ------------------------- | ----- |
| Character library card  | Gallery | derived | gallery images + metadata | card template     | yes    | fixed layout      | framing normalization     |       |
| Identity overview sheet | Gallery | derived | face + body + gallery     | overview template | yes    | structured layout | multi-asset normalization |       |

---

# E. Pose / expression support assets

## Source assets

| Asset Type            | Family | Output |  Face | Body | Hair | Style |   Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes |
| --------------------- | ------ | ------ | ----: | ---: | ---: | ----: | -------: | ---------: | ----------: | -----: | ---: | ----: | ----- |
| Pose anchor reference | Pose   | source | light |  yes |  yes | light | optional |        yes |         yes |  light |   no | light |       |

---

## Derived sheets

| Asset Type                    | Family | Output  | Source Assets     | Assembly Spec   | Labels | Layout Rules       | Normalization       | Notes |
| ----------------------------- | ------ | ------- | ----------------- | --------------- | ------ | ------------------ | ------------------- | ----- |
| Pose sheet                    | Pose   | derived | pose panels       | pose grid       | yes    | ordered layout     | scale normalization |       |
| Gesture sheet                 | Pose   | derived | gesture panels    | grid            | yes    | consistent spacing | normalization       |       |
| Hand reference sheet          | Pose   | derived | hand panels       | close-up layout | yes    | technical grid     | crop normalization  |       |
| Expression sheet              | Pose   | derived | expression panels | grid            | yes    | aligned layout     | normalization       |       |
| Emotional body language sheet | Pose   | derived | emotional poses   | grid            | yes    | grouped layout     | normalization       |       |
| Hair movement reference       | Pose   | derived | hair panels       | grid            | yes    | consistent framing | normalization       |       |

---

# F. Pair / relationship assets

## Source assets

| Asset Type         | Family       | Output | Face | Body | Hair | Style |   Outfit | Guardrails | Strict View | Layout | Pair | Scene | Notes |
| ------------------ | ------------ | ------ | ---: | ---: | ---: | ----: | -------: | ---------: | ----------: | -----: | ---: | ----: | ----- |
| Pair gallery asset | Pair/Gallery | source |  yes |  yes |  yes |   yes | optional |        yes |         yes |    yes |  yes | light |       |

---

## Derived sheets

| Asset Type                   | Family | Output         | Source Assets         | Assembly Spec         | Labels   | Layout Rules          | Normalization       | Notes             |
| ---------------------------- | ------ | -------------- | --------------------- | --------------------- | -------- | --------------------- | ------------------- | ----------------- |
| Height comparison sheet      | Pair   | derived        | body refs/silhouettes | comparison template   | yes      | shared baseline       | scale normalization |                   |
| Couple standing reference    | Pair   | derived/hybrid | pair refs             | pair template         | optional | aligned layout        | normalization       | could be prompted |
| Interaction pose anchor      | Pair   | derived/hybrid | interaction panels    | grid template         | optional | comparable panels     | normalization       |                   |
| Pair outfit comparison sheet | Pair   | derived        | outfit refs           | side-by-side template | yes      | structured comparison | normalization       |                   |
| Scale and contact sheet      | Pair   | derived        | pair pose refs        | technical template    | yes      | fixed layout          | exact normalization |                   |

---

# G. Scene / downstream outputs (all source)

| Asset Type                | Family | Output | Face | Body | Hair | Style |   Outfit | Guardrails | Strict View | Layout |     Pair | Scene | Notes |
| ------------------------- | ------ | ------ | ---: | ---: | ---: | ----: | -------: | ---------: | ----------: | -----: | -------: | ----: | ----- |
| Single-character scene    | Scene  | source |  yes |  yes |  yes |   yes | optional |        yes |          no |     no |       no |   yes |       |
| Outfit scene              | Scene  | source |  yes |  yes |  yes |   yes |      yes |        yes |          no |     no |       no |   yes |       |
| Pair scene                | Scene  | source |  yes |  yes |  yes |   yes | optional |        yes |          no |     no |      yes |   yes |       |
| Pair outfit scene         | Scene  | source |  yes |  yes |  yes |   yes |      yes |        yes |          no |     no |      yes |   yes |       |
| Group scene               | Scene  | source |  yes |  yes |  yes |   yes | optional |        yes |          no |     no |      yes |   yes |       |
| Emotional narrative scene | Scene  | source |  yes |  yes |  yes |   yes | optional |        yes |          no |     no | optional |   yes |       |

---

# Key structural takeaway (now explicit)

The matrix now clearly shows:

## 1. Two fundamentally different pipelines

### A. Prompt pipeline (source assets)

- driven by blocks
- identity + instruction + context
- sensitive to wording and structure

### B. Assembly pipeline (derived sheets)

- driven by scripts
- deterministic
- depends on:
  - source assets
  - layout templates
  - normalization rules

---

## 2. Clean separation of responsibilities

### Prompt system handles:

- identity fidelity
- anatomy correctness
- clothing design
- pose correctness
- scene composition

### Script system handles:

- layout consistency
- panel alignment
- scaling
- labeling
- visual standardization

---

## 3. Why this matters for the next step

This revised matrix gives us exactly what we need to build the blueprint:

- which assets require **block composition**
- which assets require **assembly specs**
- where identity blocks are actually used
- where they should NOT be used

---

# Next step

Now we can move cleanly into:

👉 **Concrete pipeline block blueprint**

That will include:

- exact block taxonomy
- inheritance order
- asset assembly recipes (per asset type)
- YAML-style schema for implementation

And most importantly:

- how to plug this into your existing pipeline without breaking it

Whenever you're ready, we move to that.
