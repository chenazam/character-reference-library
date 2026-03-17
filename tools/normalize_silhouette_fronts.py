from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


def find_nontransparent_bbox(img: Image.Image, alpha_threshold: int = 1) -> Optional[Tuple[int, int, int, int]]:
    """
    Return bounding box of non-transparent pixels as (left, top, right, bottom),
    where right/bottom are exclusive, matching Pillow crop semantics.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    alpha = img.getchannel("A")
    bbox = alpha.point(lambda a: 255 if a >= alpha_threshold else 0).getbbox()
    return bbox


def normalize_silhouette(
    input_path: Path,
    output_path: Path,
    left_pad: int,
    right_pad: int,
    top_pad: int,
    bottom_pad: int,
    alpha_threshold: int = 1,
    overwrite: bool = False,
) -> bool:
    if output_path.exists() and not overwrite:
        print(f"Skipping existing: {output_path}")
        return False

    img = Image.open(input_path).convert("RGBA")
    bbox = find_nontransparent_bbox(img, alpha_threshold=alpha_threshold)

    if bbox is None:
        print(f"Skipping empty/fully transparent image: {input_path}")
        return False

    left, top, right, bottom = bbox
    cropped = img.crop((left, top, right, bottom))

    silhouette_w = right - left
    silhouette_h = bottom - top

    out_w = silhouette_w + left_pad + right_pad
    out_h = silhouette_h + top_pad + bottom_pad

    out = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    out.paste(cropped, (left_pad, top_pad))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(output_path)

    print(
        f"Normalized: {input_path.name} -> {output_path.name} | "
        f"silhouette={silhouette_w}x{silhouette_h}, canvas={out_w}x{out_h}"
    )
    return True


def collect_pngs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]

    return sorted(
        p for p in input_path.rglob("*.png")
        if p.is_file()
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize silhouette PNG margins while preserving true silhouette size."
    )
    parser.add_argument("input", help="Input PNG file or directory")
    parser.add_argument(
        "--output-dir",
        help="Directory to write normalized PNGs into. "
             "If omitted and input is a file, writes next to input with _normalized suffix. "
             "If omitted and input is a directory, writes to <input>/normalized.",
    )
    parser.add_argument("--left-pad", type=int, default=55, help="Left padding in px (default: 55)")
    parser.add_argument("--right-pad", type=int, default=55, help="Right padding in px (default: 55)")
    parser.add_argument("--top-pad", type=int, default=20, help="Top padding in px (default: 20)")
    parser.add_argument("--bottom-pad", type=int, default=0, help="Bottom padding in px (default: 0)")
    parser.add_argument(
        "--alpha-threshold",
        type=int,
        default=1,
        help="Minimum alpha value treated as non-transparent (default: 1)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files",
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        raise SystemExit(f"Input does not exist: {input_path}")

    files = collect_pngs(input_path)
    if not files:
        raise SystemExit("No PNG files found.")

    if args.output_dir:
        output_root = Path(args.output_dir)
    else:
        output_root = (
            input_path.parent if input_path.is_file()
            else input_path / "normalized"
        )

    count = 0
    for src in files:
        if input_path.is_file():
            dst = output_root / f"{src.stem}_normalized.png"
        else:
            rel = src.relative_to(input_path)
            dst = output_root / rel

        changed = normalize_silhouette(
            input_path=src,
            output_path=dst,
            left_pad=args.left_pad,
            right_pad=args.right_pad,
            top_pad=args.top_pad,
            bottom_pad=args.bottom_pad,
            alpha_threshold=args.alpha_threshold,
            overwrite=args.overwrite,
        )
        if changed:
            count += 1

    print(f"\nDone. Wrote {count} normalized file(s).")


if __name__ == "__main__":
    main()