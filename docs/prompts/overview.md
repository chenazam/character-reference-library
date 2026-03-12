# Prompt System Overview

This project uses a modular prompt system designed to reduce character drift
when generating images with AI models.

The system is composed of three layers:

1. master prompt blocks
2. prompt recipes
3. pipeline prompt templates

Prompt blocks contain reusable text fragments.

Prompt recipes explain how to combine blocks for different tasks.

Pipeline templates are full prompts used to generate specific reference sheets.
