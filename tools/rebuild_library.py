import subprocess
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

SCRIPTS = [
    "tools/generate_gallery_snippets.py",
    "tools/generate_character_pages.py",
    "tools/generate_character_index.py",
    "tools/generate_pipeline_dashboard.py",
    "tools/update_pipeline_status.py",
    "tools/validate_library.py",
    "tools/generate_generation_queue.py",
]


def run_python(script):
    print(f"\n=== Running {script} ===\n")

    result = subprocess.run(
        [sys.executable, script],
        cwd=ROOT
    )

    if result.returncode != 0:
        sys.exit(result.returncode)


def run_mkdocs_build():
    print("\n=== Running mkdocs build ===\n")

    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build"],
        cwd=ROOT
    )

    if result.returncode != 0:
        sys.exit(result.returncode)


def main():

    print("\n===== REBUILDING REFERENCE LIBRARY =====\n")

    for script in SCRIPTS:
        run_python(script)

    run_mkdocs_build()

    print("\n===== BUILD COMPLETE =====\n")


if __name__ == "__main__":
    main()