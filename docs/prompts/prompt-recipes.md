# Prompt Recipes

This page explains how prompts are constructed using the modular prompt system.

Prompts are built from three components:

1. **Master Blocks**  
   Global prompt fragments used across all characters.

2. **Character Prompt Blocks**  
   Character-specific descriptions stored in each character’s `prompt_blocks.md`.

3. **Prompt Templates**  
   Pipeline templates stored in `library/50_PROMPT_TEMPLATES/`.

---

# Basic Prompt Structure

Most prompts follow this structure:

Character block

- task description
- style block
- layout block
- identity preservation rules

Example structure:

```
Character:
[CHARACTER_BLOCK]

Task description:
[WHAT SHOULD BE GENERATED]

[GLOBAL STYLE BLOCK]

[LAYOUT BLOCK]

[IDENTITY PRESERVATION BLOCK]
```

---

# Common Prompt Recipes

## Face Reference Generation

Use blocks:

• Face Block  
• Identity Block (Short)  
• Anti-Drift Rules

Attach references:

• source face reference
• existing face anchors (if available)

---

## Anatomy Generation

Use blocks:

• Body Block  
• Movement Block  
• Anti-Drift Rules

Attach references:

• Face Anchor Sheet  
• Hair Sheet

---

## Body Anchor Generation

Use blocks:

• Body Block  
• Style Block  
• Anti-Drift Rules

Attach references:

• Anatomy Sheet  
• Face Anchor Sheet

---

## Signature Outfit Generation

Use blocks:

• Identity Block (Extended)  
• Style Block  
• Wardrobe Block  
• Anti-Drift Rules

Attach references:

• Ultimate Character Sheet  
• Body Anchor Sheet  
• Turnaround Sheet

---

## Pose Sheet Generation

Use blocks:

• Body Block  
• Movement Block  
• Style Block  
• Anti-Drift Rules

Attach references:

• Ultimate Character Sheet  
• Signature Outfit Sheet

---

## Scene Generation

Use blocks:

• Identity Block (Short)  
• Style Block  
• Expression Block  
• Anti-Drift Rules

Attach references:

• Ultimate Character Sheet  
• Signature Outfit Sheet  
• scene-specific references

---

# General Prompt Guidelines

When constructing prompts:

• keep descriptions structured  
• use bullet lists for physical traits  
• avoid overly long paragraphs  
• explicitly preserve identity traits  
• attach reference sheets whenever possible

This system helps reduce character drift and improves consistency across generations.
