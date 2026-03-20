# 🧭 Prompt Optimization Goals (v2 Spec)

This becomes our **reference contract**.
Every template and block should satisfy these.

---

## 🔴 1. Cross-Asset Consistency (Global)

**Goal**

> The same asset type must look structurally identical across all characters.

**Includes**

- identical layout
- identical panel structure
- identical camera setup
- identical output format
- identical labeling rules

**Implication**

- prompts must define structure explicitly, not implicitly
- no “creative interpretation” of layout by the model

---

## 🔴 2. Intra-Asset Consistency (Per Asset)

**Goal**

> All panels/views within a single asset must be internally consistent.

**Includes**

- same proportions across panels
- same character identity
- same scale and camera distance
- no drift between views

---

## 🔴 3. Normalization & Pipeline Compatibility

**Goal**

> Assets must be directly usable in downstream pipeline steps without manual correction.

**Includes**

- consistent framing
- predictable margins
- consistent scale
- alignment with:
  - normalization scripts
  - comparison charts
  - asset ingestion steps

**Example**

- silhouette_front → must be crop-consistent for height charts
- face reference → must be clean enough for reuse

---

## 🔴 4. Character Fidelity (Non-Negotiable)

**Goal**

> The character must remain visually identical across all assets.

**Includes**

- face structure
- body proportions
- silhouette read
- defining traits

**Implication**

- prompts must emphasize:
  - “same character”
  - “consistent identity”
  - “no reinterpretation”

---

## 🔴 5. Purpose-Driven Asset Design

**Goal**

> Each asset must be optimized for its role in the pipeline.

**Examples**

- face reference → clean, reusable input
- silhouette → readable at small size
- anatomy sheet → structural clarity, not stylization
- body anchor → stable proportions, not dynamic posing

This is critical and often overlooked.

---

## 🟠 6. Layout & Format Determinism

**Goal**

> Output structure must be deterministic.

**Includes**

- panel count fixed
- panel arrangement fixed
- spacing predictable
- no random cropping

**Implication**

- prompts must define:
  - grid structure
  - spacing
  - framing rules
  - camera consistency

---

## 🟠 7. ChatGPT Optimization

**Goal**

> Prompts must be structured for **maximum reliability with ChatGPT image generation**.

**Includes**

- clear hierarchy:
  1. subject
  2. task
  3. structure
  4. constraints

- avoid:
  - redundancy
  - conflicting instructions
  - overly poetic phrasing

---

## 🟠 8. Filter Safety (Critical for Stability)

**Goal**

> Minimize risk of refusals or degraded outputs.

**Includes**

- neutral anatomical language
- avoid:
  - sexualized phrasing
  - ambiguous wording

- prefer:
  - “body proportions”
  - “anatomical structure”
  - “silhouette”

**Especially important for**

- anatomy sheets
- body descriptions
- glute/hip emphasis

---

## 🟡 9. Readability & Clarity of Output

**Goal**

> Assets must be readable at:

- small sizes
- comparison contexts
- documentation contexts

**Includes**

- strong silhouette readability
- clean shapes
- no visual noise

---

## 🟡 10. Minimal Redundancy in Prompts

**Goal**

> Prompts should be as short as possible while remaining precise.

**Why**

- redundancy reduces reliability
- conflicting phrasing introduces noise

---

## 🟡 11. Controlled Variance

**Goal**

> Allow variation where useful, eliminate it where harmful.

**Examples**

- ❌ layout → no variance
- ❌ proportions → no variance
- ✅ micro texture → acceptable
- ✅ minor rendering variation → acceptable

---

## 🔴 12. AI-Optimal Output Design

**Goal**

> Asset format, layout, and structure must be optimized for how ChatGPT actually generates images — not based on human preference.

**Implications**

- Fewer panels = more reliable
- Symmetry = more stable
- Consistent camera = critical
- Overly complex layouts = degrade output
- “Clean, simple, repeated structure” > “fancy layout”

This will strongly influence what we change.

---

# 🧠 Meta Principle

All prompts should follow:

```text
Identity → Purpose → Structure → Constraints → Output Rules
```

NOT:

```text
Mixed instructions → repeated constraints → unclear priorities
```

---

# ✅ Acceptance Criteria (Practical)

A prompt is “good” if:

- you can generate 5 characters with it and:
  - they all look structurally identical
  - only the character changes

- the output requires:
  - zero manual correction

- it does not:
  - trigger filters
  - produce layout drift

- it works reliably across multiple generations
