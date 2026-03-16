#!/usr/bin/env python3

from __future__ import annotations

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


def image_url_from_record(record: dict, filename: str) -> str:
    """
    Resolve a reference filename from a library record into a site-root URL.
    Returns "" if not found or not under docs/.
    """
    if not filename:
        return ""

    character_dir = as_path(record["dir"])
    candidate = find_named_file(character_dir, filename)
    if candidate is None:
        return ""

    try:
        return site_root_url(candidate)
    except ValueError:
        return ""