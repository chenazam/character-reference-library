import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCRIPTS = [
    "tools/update_pipeline_status.py",
    "tools/validate_library.py",
    "tools/generate_gallery_snippets.py",
    "tools/generate_character_pages.py",
    "tools/generate_character_index.py",
    "tools/generate_nav_characters.py",
    "tools/generate_asset_comparison_snippets.py",
    "tools/generate_asset_comparison_page.py",
    "tools/generate_pipeline_dashboard.py",
    "tools/generate_generation_queue.py",
]


def run_command(command, label, allow_failure=False, capture_output=False, text=True):
    print(f"\n\n========== {label} ==========\n")
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=capture_output,
        text=text,
    )

    if result.returncode != 0 and not allow_failure:
        if capture_output:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    return result


def run_python(script):
    run_command([sys.executable, script], f"Running {script}")


def run_mkdocs_build():
    run_command([sys.executable, "-m", "mkdocs", "build"], "Running mkdocs build")


def run_mkdocs_gh_deploy():
    run_command(
        [sys.executable, "-m", "mkdocs", "gh-deploy", "--clean"],
        "Running mkdocs gh-deploy",
    )


def has_git_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return bool(result.stdout.strip())


def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    branch = result.stdout.strip()
    if not branch:
        raise RuntimeError("Could not determine current git branch.")
    return branch


def commit_generated_changes(message="Auto-update generated reference library"):
    if not has_git_changes():
        print("\nNo generated changes to commit.\n")
        return False

    run_command(["git", "add", "-A"], "Staging generated changes")
    run_command(
        ["git", "commit", "-m", message],
        "Committing generated changes",
    )
    return True


def push_current_branch():
    branch = get_current_branch()
    run_command(["git", "push", "origin", branch], f"Pushing branch {branch}")


def commit_and_push_if_needed(message="Auto-update generated reference library"):
    changed = commit_generated_changes(message)
    if changed:
        push_current_branch()
    return changed


def main():
    deploy = "--no-deploy" not in sys.argv

    print("\n===== REBUILDING REFERENCE LIBRARY =====\n")

    for script in SCRIPTS:
        run_python(script)

    # Commit/push script-generated source changes first.
    commit_and_push_if_needed("Auto-update generated reference library")

    # Build may itself update tracked files.
    run_mkdocs_build()

    # Commit/push again in case build created or modified tracked files.
    commit_and_push_if_needed("Auto-update generated build artifacts")

    if deploy:
        run_mkdocs_gh_deploy()

    print("\n===== BUILD COMPLETE =====\n")


if __name__ == "__main__":
    main()
