Thumbnail standardization constraint:

This asset must follow a strictly standardized presentation across all characters.

Image type:

- tight headshot only
- framed like an ID photo or profile avatar

Not allowed:

- portrait composition
- half-body framing
- chest-up framing

Final image behavior (CRITICAL):

- the generated image itself is the final output
- there must be no outer canvas, frame, or padding
- the subject must not be placed inside a larger background area

Prohibited:

- do not embed the image inside a larger canvas
- do not create margins, borders, or framing space around the subject
- do not simulate a layout, card, or presentation sheet

Requirement:

- the edges of the image must correspond directly to the intended crop
- what is generated must already be tightly framed

Framing (CRITICAL):

- tight head-and-shoulders crop
- head occupies ~75–85% of frame height
- only minimal shoulders visible

Aspect ratio behavior (CRITICAL):

- the composition must be natively built for a 3:2 landscape frame
- the subject must fill the full width of the frame
- no empty side margins or padding
- no square or 1:1 composition inside a wider canvas

Prohibited:

- do not render a square image and place it on a wider background
- do not leave empty space on the left or right side of the subject
- do not center a narrow composition within a wide frame

Composition requirement:

- the head and shoulders must extend naturally toward both horizontal edges
- the framing must feel intentionally composed for a wide format, not adapted from a square crop

Hard constraints:

- crop must end at or above the clavicle line
- no visible pectoral forms
- no visible torso mass
- abs must never be visible

Surface treatment constraints:

- no soft fading, vignetting, or gradient masking on the subject
- the subject must remain fully opaque and clearly defined
- no blur or fade applied to the torso or lower frame area
- edges of the subject must remain crisp and consistent

Prohibited:

- no atmospheric fade into the background
- no soft blending of the subject into the background
- no partial transparency or visual de-emphasis techniques

Failure condition:

- if the image reads as a chest-up portrait, it is incorrect

Camera:

- three-quarter view (mandatory)
- eye-level perspective

Expression:

- neutral to slightly relaxed
- no exaggerated emotion

Clothing:

- shirtless only
- no accessories

Consistency:

- identical framing, lighting, and background across all thumbnails

Priority:

- immediate facial recognition
- strict visual consistency
