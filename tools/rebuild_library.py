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


def run_command(command, label):
    print(f"\n\n========== {label} ==========\n")
    result = subprocess.run(command, cwd=ROOT)

    if result.returncode != 0:
        sys.exit(result.returncode)


def run_python(script):
    run_command([sys.executable, script], f"Running {script}")


def run_mkdocs_build():
    run_command([sys.executable, "-m", "mkdocs", "build"], "Running mkdocs build")


def run_mkdocs_gh_deploy():
    run_command(
        [sys.executable, "-m", "mkdocs", "gh-deploy", "--clean"],
        "Running mkdocs gh-deploy",
    )


def main():
    args = set(sys.argv[1:])

    # Default behavior: rebuild + deploy.
    # Use --no-deploy when a local-only build is desired.
    deploy = True
    if "--no-deploy" in args:
        deploy = False
    elif "--deploy" in args:
        deploy = True

    print("\n===== REBUILDING REFERENCE LIBRARY =====\n")

    for script in SCRIPTS:
        run_python(script)

    run_mkdocs_build()

    if deploy:
        run_mkdocs_gh_deploy()

    print("\n===== BUILD COMPLETE =====\n")


if __name__ == "__main__":
    main()
