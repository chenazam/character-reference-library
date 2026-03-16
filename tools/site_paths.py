#!/usr/bin/env python3

from __future__ import annotations

import os
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
SITE_ROOT = ROOT / "site"


def as_path(value) -> pathlib.Path:
    return value if isinstance(value, pathlib.Path) else pathlib.Path(value)


def ensure_under_docs(path) -> pathlib.Path:
    """
    Return an absolute path and verify that it lives under docs/.
    """
    p = as_path(path).resolve()
    try:
        p.relative_to(DOCS_ROOT.resolve())
    except ValueError as e:
        raise ValueError(f"Path is not under docs/: {p}") from e
    return p


def docs_relative(path) -> pathlib.Path:
    """
    Convert an absolute docs file path to a path relative to docs/.

    Example:
        docs/assets/x.png -> assets/x.png
    """
    p = ensure_under_docs(path)
    return p.relative_to(DOCS_ROOT.resolve())


def site_root_url(path) -> str:
    """
    Convert a docs file path into a site-root URL.

    Example:
        docs/assets/x.png -> /assets/x.png
    """
    rel = docs_relative(path)
    return "/" + rel.as_posix()


def site_output_path(path) -> pathlib.Path:
    """
    Convert a docs file path into the equivalent built-site file path.

    Example:
        docs/assets/x.png -> site/assets/x.png
    """
    rel = docs_relative(path)
    return SITE_ROOT / rel


def page_build_dir(page_docs_path) -> pathlib.Path:
    """
    Return the built output directory for a markdown page under MkDocs.

    Examples:
        docs/index.md -> site/
        docs/comparisons/assets.md -> site/comparisons/assets/
        docs/comparisons/index.md -> site/comparisons/
    """
    page_path = ensure_under_docs(page_docs_path)

    if page_path.suffix.lower() != ".md":
        raise ValueError(f"Expected a markdown page under docs/: {page_path}")

    rel = docs_relative(page_path)

    if page_path.name == "index.md":
        return SITE_ROOT / rel.parent

    return SITE_ROOT / rel.with_suffix("")


def asset_relative_url(asset_docs_path, from_page_docs_path) -> str:
    """
    Build a URL to an asset file relative to the final built page location.

    Example:
        asset_docs_path = docs/assets/library/x.png
        from_page_docs_path = docs/comparisons/assets.md
        -> ../../assets/library/x.png
    """
    target = site_output_path(asset_docs_path)
    base = page_build_dir(from_page_docs_path)
    rel = os.path.relpath(target, base)
    return pathlib.Path(rel).as_posix()


def page_relative_url(target_page_docs_path, from_page_docs_path) -> str:
    """
    Build a URL to another markdown page relative to the final built page location.

    Example:
        target_page_docs_path = docs/characters/lucien.md
        from_page_docs_path = docs/comparisons/assets.md
        -> ../../characters/lucien/
    """
    target = page_build_dir(target_page_docs_path)
    base = page_build_dir(from_page_docs_path)
    rel = pathlib.Path(os.path.relpath(target, base)).as_posix()

    if rel == ".":
        return "./"

    return rel.rstrip("/") + "/"


def find_named_file(root, filename: str) -> pathlib.Path | None:
    """
    Recursively search for a filename under a root folder.
    Returns the first stable sorted match, or None.
    """
    root_path = as_path(root)
    matches = [p for p in root_path.rglob(filename) if p.is_file()]
    if not matches:
        return None
    matches.sort()
    return matches[0]


def image_url_from_record(record: dict, filename: str, from_page_docs_path=None) -> str:
    """
    Resolve a reference filename from a library record into a URL.

    If from_page_docs_path is omitted, returns a site-root URL.
    If from_page_docs_path is provided, returns a URL relative to the final built page.
    """
    if not filename:
        return ""

    character_dir = as_path(record["dir"])
    candidate = find_named_file(character_dir, filename)
    if candidate is None:
        return ""

    try:
        if from_page_docs_path is None:
            return site_root_url(candidate)
        return asset_relative_url(candidate, from_page_docs_path)
    except ValueError:
        return ""
