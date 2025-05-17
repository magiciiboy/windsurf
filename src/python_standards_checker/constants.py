# ANSI color codes for terminal output
CHECKMARK = "\u2713"  # ✓
CROSS = "\u2717"  # ✗
WARNING = "\u26a0"  # ⚠
GREEN = "\033[92m"
RED = "\033[91m"
ORANGE = "\033[33m"
RESET = "\033[0m"

# Output formats
FORMAT_JSON = "json"
FORMAT_CHECKLIST = "checklist"

# Severity levels
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_RECOMMENDATION = "RECOMMENDATION"

# Standards with severity, categories, codes, and descriptions
STANDARDS = {
    "python_version": {
        "code": "PY001",
        "category": "Version",
        "standard": ">=3.9",
        "severity": SEVERITY_CRITICAL,
        "description": "Python version MUST be at least 3.9",
        "recommendation": "Update your project's Python version requirement to at least 3.9",
        "standard_type": "version",
    },
    "pyproject_toml": {
        "code": "PY002",
        "category": "Project Structure",
        "standard": True,
        "severity": SEVERITY_RECOMMENDATION,
        "description": "Project SHOULD have a pyproject.toml specification",
        "recommendation": "Create a pyproject.toml file to specify project metadata and dependencies",
        "standard_type": "file",
    },
    "makefile": {
        "code": "PY003",
        "category": "Project Structure",
        "standard": True,
        "severity": SEVERITY_RECOMMENDATION,
        "description": "Project SHOULD have Makefile at root level",
        "recommendation": "Create a Makefile at the root of your project to define build and automation targets",
        "standard_type": "file",
    },
    "no_conda": {
        "code": "PY004",
        "category": "Dependency Management",
        "standard": False,
        "severity": SEVERITY_CRITICAL,
        "description": "Project MUST NOT use conda",
        "recommendation": "Remove conda dependencies and use uv, poetry, or pip instead",
        "standard_type": "dependency",
    },
    "lock_file": {
        "code": "PY005",
        "category": "Dependency Management",
        "standard": True,
        "severity": SEVERITY_RECOMMENDATION,
        "description": "Project SHOULD have a lock file (poetry.lock, pip-tools requirements.in, requirements.txt)",
        "recommendation": "Create a lock file to ensure consistent dependency versions across environments",
        "standard_type": "file",
    },
}

# Standard categories
STANDARD_CATEGORIES = {
    "Version": "Version-related standards",
    "Project Structure": "Project structure and organization standards",
    "Dependency Management": "Dependency management standards",
}

# Standard codes
STANDARD_CODES = {
    "PY001": "python_version",
    "PY002": "pyproject_toml",
    "PY003": "makefile",
    "PY004": "no_conda",
    "PY005": "lock_file",
}

# Standard categories
STANDARD_CATEGORIES = {
    "Version": "Version-related standards",
    "Project Structure": "Project structure and organization standards",
    "Dependency Management": "Dependency management standards",
}

# Lock files to check
LOCK_FILES = ["requirements.txt", "poetry.lock", "requirements.in"]  # pip-tools

# Conda-related files
CONDA_FILES = ["environment.yml", ".condarc", "*.conda", "*.yml", "*.yaml"]

# GitLab CI files
CI_FILES = [".gitlab-ci.yml", ".gitlab-ci.yaml"]

# Lock files to check
LOCK_FILES = ["requirements.txt", "poetry.lock", "requirements.in"]  # pip-tools

# Conda-related files
CONDA_FILES = ["environment.yml", ".condarc", "*.conda", "*.yml", "*.yaml"]

# GitLab CI files
CI_FILES = [".gitlab-ci.yml", ".gitlab-ci.yaml"]
