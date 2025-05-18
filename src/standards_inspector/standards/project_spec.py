from standards_inspector.repositories import BaseRepository

from .base import BaseStandard


class ProjectSpecStandard(BaseStandard):
    """Project specification standard."""

    code = "PY002"
    category = "Project Structure"
    standard = True
    severity = "CRITICAL"
    description = "Project MUST have a project specification"
    recommendation = "Create a project specification file to specify project metadata and dependencies"
    standard_type = "file"

    @classmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check if project has a project specification."""
        files = repository.get_files()
        return {
            "meets_standard": "pyproject.toml" in files,
            "value": "pyproject.toml" if "pyproject.toml" in files else "not found",
        }

    @classmethod
    def _check_project_spec(cls, repository: BaseRepository) -> bool:
        """Check if project has a valid pyproject.toml file."""
        files = repository.get_files()
        return "pyproject.toml" in files
