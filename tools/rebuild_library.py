import subprocess
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCRIPTS = [
    "tools/update_pipeline_status.py",
    "tools/validate_library.py",
    "tools/generate_gallery_snippets.py",
    "tools/generate_character_pages.py",
    "tools/generate_character_index.py",
    "tools/generate_nav_characters.py",
    "tools/generate_pipeline_dashboard.py",
    "tools/generate_generation_queue.py",
]


def run_command(command, label, allow_failure=False):
    print(f"\n\n========== {label} ==========\n")
    result = subprocess.run(command, cwd=ROOT)

    if result.returncode != 0 and not allow_failure:
        sys.exit(result.returncode)

    return result.returncode


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
    )
    return bool(result.stdout.strip())


def commit_generated_changes():
    if not has_git_changes():
        print("\nNo generated changes to commit.\n")
        return

    run_command(["git", "add", "-A"], "Staging generated changes")

    # Commit all generated updates before build/deploy.
    # If commit fails for any real reason, stop the pipeline.
    run_command(
        ["git", "commit", "-m", "Auto-update generated reference library"],
        "Committing generated changes",
    )


def main():
    # Deploy by default; use --no-deploy for local-only builds.
    deploy = "--no-deploy" not in sys.argv

    print("\n===== REBUILDING REFERENCE LIBRARY =====\n")

    for script in SCRIPTS:
        run_python(script)

    commit_generated_changes()

    run_mkdocs_build()

    if deploy:
        run_mkdocs_gh_deploy()

    print("\n===== BUILD COMPLETE =====\n")


if __name__ == "__main__":
    main()
