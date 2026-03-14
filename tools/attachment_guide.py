import argparse
import pathlib
import fnmatch

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHARACTERS_ROOT = ROOT / "docs/assets/library/10_CHARACTERS"


ATTACHMENT_RULES = {

    "face-anchor": [
        "*front_face*",
        "*three_quarter_face*",
        "*profile_face*",
    ],

    "gallery-image": [
        "*face_anchor*",
        "*body_anchor*",
        "*silhouette*",
        "*turnaround*",
        "*expression_sheet*",
    ],

    "anatomy-front": [
        "*face_anchor*",
        "*hair_sheet*",
    ],

    "anatomy-side": [
        "*anatomy_front*",
    ],

    "anatomy-back": [
        "*anatomy_front*",
        "*anatomy_side*",
    ],

    "expression-sheet": [
        "*face_anchor*",
        "*hair_sheet*",
    ],

    "pose-sheet": [
        "*signature_outfit*",
        "*turnaround*",
    ],

    "scene-sheet": [
        "*signature_outfit*",
        "*pose_sheet*",
        "*interaction_anchor*",
    ],
}


def find_files(character, pattern):

    base = CHARACTERS_ROOT / character

    matches = []

    for p in base.rglob("*"):
        if fnmatch.fnmatch(p.name.lower(), pattern.lower()):
            matches.append(p)

    return matches


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
