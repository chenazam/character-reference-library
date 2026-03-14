import argparse
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"

ATTACHMENT_RULES = {

    "face-anchor": [
        "01_FACE/*front*",
        "01_FACE/*three_quarter*",
        "01_FACE/*profile*",
    ],

    "gallery-image": [
        "01_FACE/*face_anchor*",
        "06_BODY/*body_anchor*",
        "07_SILHOUETTE/*",
        "08_TURNAROUND/*",
    ],

    "anatomy-front": [
        "01_FACE/*face_anchor*",
        "06_BODY/*body_anchor*",
        "07_SILHOUETTE/*",
    ],

    "anatomy-side": [
        "01_FACE/*face_anchor*",
        "06_BODY/*body_anchor*",
        "07_SILHOUETTE/*",
    ],

    "turnaround": [
        "01_FACE/*face_anchor*",
        "06_BODY/*body_anchor*",
        "07_SILHOUETTE/*",
    ],

    "expression-sheet": [
        "01_FACE/*face_anchor*",
    ],

    "pose-sheet": [
        "06_BODY/*body_anchor*",
        "07_SILHOUETTE/*",
        "08_TURNAROUND/*",
    ],

    "scene-sheet": [
        "01_FACE/*face_anchor*",
        "06_BODY/*body_anchor*",
        "08_TURNAROUND/*",
    ],
}


def find_files(character, pattern):

    base = CHARACTERS_ROOT / character

    return list(base.glob(pattern))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--character", required=True)
    parser.add_argument("--template", required=True)

    args = parser.parse_args()

    character = args.character.upper()
    template = args.template

    if template not in ATTACHMENT_RULES:
        print("No attachment rule for template")
        return

    print(f"\nReference attachments for {character} / {template}:\n")

    for pattern in ATTACHMENT_RULES[template]:

        files = find_files(character, pattern)

        for f in files:
            rel = f.relative_to(ROOT)
            print(rel)


if __name__ == "__main__":
    main()