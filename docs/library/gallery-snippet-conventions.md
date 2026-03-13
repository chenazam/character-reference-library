# Gallery Snippet Conventions

This page defines the standard used for gallery snippet files in the character reference library.

Gallery snippets are used to keep character pages short, consistent, and easier to maintain.

They contain the HTML for thumbnail galleries and are included into character pages using `pymdownx.snippets`.

---

## Purpose

Use gallery snippets when a character page needs to display one or more reference images in a reusable gallery block.

This keeps:

- character pages shorter
- gallery markup centralized
- updates easier when image filenames or versions change
- section structure consistent across characters

---

## Snippet Location

All gallery snippets should be stored in:

```text
docs/snippets/galleries/
```

Example:

```text
docs/snippets/galleries/lucien-face.md
docs/snippets/galleries/lucien-body.md
docs/snippets/galleries/lucien-anatomy.md
```

---

## Include Syntax

Character pages include gallery snippets using this syntax:

```markdown
--8<-- "snippets/galleries/lucien-face.md"
```

This works because `mkdocs.yml` configures `pymdownx.snippets` with:

```yaml
pymdownx.snippets:
  base_path:
    - docs
```

---

## Naming Convention

Gallery snippet filenames should use this structure:

```text
[character-slug]-[section-name].md
```

Examples:

```text
lucien-core-identity.md
lucien-face.md
lucien-hair.md
lucien-anatomy.md
lucien-body.md
lucien-expression-gesture.md
```

Use lowercase kebab-case for the full filename.

---

## Standard Section Names

Use these section names wherever possible.

### Core sections

```text
core-identity
face
hair
anatomy
body
expression-gesture
```

### Advanced sections

```text
ucs
signature-outfit
design-language
wardrobe
poses
motion
scale
scenes
props
```

These names should match the logical page sections, not necessarily the raw folder names.

---

## What Belongs in a Snippet

A gallery snippet should contain only the gallery HTML block.

Example:

```html
<div class="character-gallery">
  <a
    href="/assets/library/10_CHARACTERS/LUCIEN/01_FACE/lucien_face_anchor_v1.png"
    target="_blank"
  >
    <img
      src="/assets/library/10_CHARACTERS/LUCIEN/01_FACE/lucien_face_anchor_v1.png"
      alt="Lucien face anchor"
    />
  </a>
</div>
```

A snippet should not contain:

- page headings
- explanatory paragraphs
- markdown lists
- horizontal rules
- unrelated notes

The snippet should only contain the visual gallery markup.

---

## Authoring Rules

### 1. Use only HTML inside gallery snippets

Gallery snippets should contain only:

- `<div>`
- `<a>`
- `<img>`

Do not mix markdown headings or markdown formatting into the snippet file.

This keeps rendering stable inside MkDocs.

---

### 2. Use the shared gallery wrapper

Every gallery snippet should use:

```html
<div class="character-gallery"></div>
```

This ensures the shared CSS applies consistently.

---

### 3. Use `/assets/...` paths, not `/docs/assets/...`

Correct:

```text
/assets/library/10_CHARACTERS/LUCIEN/01_FACE/lucien_face_anchor_v1.png
```

Incorrect:

```text
/docs/assets/library/10_CHARACTERS/LUCIEN/01_FACE/lucien_face_anchor_v1.png
```

MkDocs serves the contents of `docs/` at the site root, so runtime asset paths must begin with `/assets/`.

---

### 4. Always include descriptive `alt` text

Every image must include useful `alt` text.

Good:

```text
alt="Lucien face anchor"
alt="Lucien anatomy front"
alt="Lucien expression sheet"
```

Avoid vague values like:

```text
alt="image"
alt="reference"
```

---

### 5. Keep one snippet per page section

Each major character page section should normally have its own snippet file.

Example:

- `lucien-face.md`
- `lucien-anatomy.md`
- `lucien-body.md`

Do not combine unrelated sections into one large snippet unless there is a clear reason.

---

### 6. Update snippets when image versions change

If an asset changes from:

```text
lucien_face_anchor_v1.png
```

to:

```text
lucien_face_anchor_v2.png
```

update the snippet file so the character page continues to point to the newest intended version.

This is one of the main maintenance benefits of using snippets.

---

## Character Page Responsibilities

The character page should contain:

- headings
- short descriptive section text
- include lines for the gallery snippets
- prompting notes
- navigation

The character page should not contain large repeated image blocks directly unless there is a strong reason.

Example:

```markdown
## Face References

These references define facial identity, angle consistency, and portrait fidelity.

--8<-- "snippets/galleries/lucien-face.md"
```

---

## Recommended Character Page Pattern

Use this structure for character pages where available:

```text
Overview
Quick Navigation
Core Identity
Face References
Hair References
Anatomy
Body / Proportions
Expression and Gesture
Advanced Reference Sets
Prompting Notes
```

Not every character needs every section immediately, but the naming and layout should remain as consistent as possible.

---

## Example Snippet Set

A typical character with current core coverage may have:

```text
docs/snippets/galleries/
  lucien-core-identity.md
  lucien-face.md
  lucien-hair.md
  lucien-anatomy.md
  lucien-body.md
  lucien-expression-gesture.md
```

As the library expands, additional snippets may be added:

```text
lucien-ucs.md
lucien-signature-outfit.md
lucien-design-language.md
lucien-wardrobe.md
lucien-poses.md
lucien-motion.md
lucien-scale.md
lucien-scenes.md
lucien-props.md
```

---

## Summary

Gallery snippets are the standard way to render reference galleries in character pages.

Use them to keep pages:

- clean
- modular
- maintainable
- visually consistent

When in doubt:

- keep headings in the character page
- keep gallery HTML in the snippet
- keep asset paths rooted at `/assets/`
- keep filenames predictable
