import gitlab
from .base import BaseStandard


class ProjectSpecStandard(BaseStandard):
    """Project specification standard."""

    code = "PY002"
    category = "Project Structure"
    standard = True
    severity = "RECOMMENDATION"
    description = "Project SHOULD have a project specification"
    recommendation = "Create a project specification file to specify project metadata and dependencies"
    standard_type = "file"

    @classmethod
    def check(cls, gl: "gitlab.Gitlab", project_id: str) -> dict:
        """Check for project specification file."""
        has_project_spec = cls._check_project_spec(gl, project_id)
        return {
            "meets_standard": has_project_spec,
            "value": "present" if has_project_spec else "not found",
        }

    @classmethod
    def _check_project_spec(cls, gl: "gitlab.Gitlab", project_id: str) -> bool:
        """Check if project has a valid pyproject.toml file."""
        files = cls.get_repository_files(gl, project_id)
        return "pyproject.toml" in files
