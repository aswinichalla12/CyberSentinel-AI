"""
setup_project.py
Creates the complete CyberSentinel AI folder structure.
Safe to run more than once: it never deletes or overwrites existing files.

Run from the project root:
    python setup_project.py
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

# Folders to create
DIRECTORIES = [
    "app",
    "cybersentinel",
    "scripts",
    "knowledge_base",
    "data/raw",
    "data/processed",
    "models",
    "reports/figures",
    "tests",
    "extensions/audio_deepfake",
    "docs",
]

# Folders that must be importable Python packages
PACKAGE_DIRECTORIES = [
    "cybersentinel",
    "scripts",
    "tests",
]

GITIGNORE_CONTENT = """\
# Virtual environment
venv/
.venv/

# Python cache
__pycache__/
*.pyc
*.egg-info/

# Secrets (never commit these)
.env
.streamlit/secrets.toml

# Raw data and user history (privacy + size)
data/raw/
data/history.db
data/*.db

# Large model files (keep small ones only if you choose to)
models/transformer/
*.pt
*.bin
*.safetensors

# Notebook and editor files
.ipynb_checkpoints/
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
"""

PYPROJECT_CONTENT = """\
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "cybersentinel"
version = "0.1.0"
description = "CyberSentinel AI: Explainable Multimodal Scam Detection and Threat Investigation Platform"
requires-python = ">=3.10,<3.13"

[tool.setuptools.packages.find]
include = ["cybersentinel*"]
"""


def create_directories() -> None:
    for relative in DIRECTORIES:
        path = PROJECT_ROOT / relative
        if path.exists():
            print(f"[exists ] {relative}")
        else:
            path.mkdir(parents=True, exist_ok=True)
            print(f"[created] {relative}")


def create_package_markers() -> None:
    for relative in PACKAGE_DIRECTORIES:
        init_file = PROJECT_ROOT / relative / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""CyberSentinel AI package."""\n', encoding="utf-8")
            print(f"[created] {relative}/__init__.py")


def write_if_missing(filename: str, content: str) -> None:
    target = PROJECT_ROOT / filename
    if target.exists():
        print(f"[exists ] {filename}")
    else:
        target.write_text(content, encoding="utf-8")
        print(f"[created] {filename}")


def create_placeholder_readmes() -> None:
    notes = {
        "data/raw": "Downloaded datasets go here. Never edit raw files.\n",
        "data/processed": "Cleaned train/validation/test files go here.\n",
        "knowledge_base": "Trusted cybersecurity reference notes for the RAG assistant.\n",
        "extensions/audio_deepfake": "Optional audio deepfake detection extension.\n",
    }
    for relative, text in notes.items():
        target = PROJECT_ROOT / relative / "README.txt"
        if not target.exists():
            target.write_text(text, encoding="utf-8")


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}\n")
    create_directories()
    create_package_markers()
    write_if_missing(".gitignore", GITIGNORE_CONTENT)
    write_if_missing("pyproject.toml", PYPROJECT_CONTENT)
    create_placeholder_readmes()
    print("\nDone. Next: create cybersentinel/config.py (see Step 1, File 2).")


if __name__ == "__main__":
    main()