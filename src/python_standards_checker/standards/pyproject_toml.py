from .base import BaseStandard
from typing import Optional


class PyprojectToml(BaseStandard):
    """pyproject.toml standard."""
    code = "PY002"
    category = "Project Structure"
    standard = True
    severity = "RECOMMENDATION"
    description = "Project SHOULD have a pyproject.toml specification"
    recommendation = "Create a pyproject.toml file to specify project metadata and dependencies"
    standard_type = "file"

    @classmethod
    def check(cls, project_id: str, checker: 'GitLabChecker') -> dict:
        """Check for pyproject.toml file."""
        has_pyproject_toml = checker._check_pyproject_toml(project_id)
        return {
            "meets_standard": has_pyproject_toml,
            "detected_version": "present" if has_pyproject_toml else "not found"
        }
