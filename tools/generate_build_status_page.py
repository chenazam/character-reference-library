#!/usr/bin/env python3

from __future__ import annotations

import pathlib
import subprocess
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "docs" / "build-status.md"


def run_git_command(args: list[str]) -> str:
    result = subprocess.run(
        ["git"] + args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def safe_git_command(args: list[str], fallback: str = "unknown") -> str:
    try:
        return run_git_command(args)
    except Exception:
        return fallback


def working_tree_dirty() -> bool:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def build_status_markdown() -> str:
    now_local = datetime.now().astimezone()
    now_utc = datetime.now(timezone.utc)

    branch = safe_git_command(["branch", "--show-current"])
    commit = safe_git_command(["rev-parse", "--short", "HEAD"])
    commit_full = safe_git_command(["rev-parse", "HEAD"])
    dirty = "yes" if working_tree_dirty() else "no"

    lines = [
        "# Build Status",
        "",
        "This page is regenerated during the library rebuild pipeline.",
        "",
        "## Current Build",
        "",
        f"- **Local build time:** {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        f"- **UTC build time:** {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- **Git branch:** `{branch}`",
        f"- **Git commit (short):** `{commit}`",
        f"- **Git commit (full):** `{commit_full}`",
        f"- **Working tree dirty at build time:** `{dirty}`",
        "",
        "## Purpose",
        "",
        "Use this page to verify that the deployed site reflects the latest rebuild and deployment.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(build_status_markdown(), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
