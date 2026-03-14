# 1D Face Anchor

Required inputs

- 1A Front Face
- 1B 3/4 Face
- 1C Profile Face

Optional inputs

- none

Avoid by default

- UCS sheets
- style sheets

```
Create a face anchor sheet used to lock the character's facial identity for the reference pipeline.

Character:
[CHARACTER_BLOCK]

Panels:
front neutral face
three-quarter neutral face
full side profile

Focus:
consistent facial identity across views
stable facial proportions
hairline consistency
recognizable nose, jaw, eye, and brow structure
consistent age and facial maturity

Output requirements:
clean professional facial reference sheet
all panels depict the same character
neutral expression in all panels
consistent framing and camera distance
head fully visible in each panel
no dramatic perspective distortion
no stylization drift between panels

Use:
[REFERENCE_SHEET_BLOCK_STACK]
[PORTRAIT_SHEET_FORMAT_BLOCK]
```
