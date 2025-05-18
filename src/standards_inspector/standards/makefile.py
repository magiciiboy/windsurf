from standards_inspector.repositories import BaseRepository

from .base import BaseStandard


class MakefileStandard(BaseStandard):
    """Makefile standard."""

    code = "PY003"
    category = "Project Structure"
    standard = True
    severity = "RECOMMENDATION"
    description = "Project SHOULD have Makefile at root level"
    recommendation = "Create a Makefile at the root of your project to define build and automation targets"
    standard_type = "file"

    @classmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check if project has a Makefile."""
        files = repository.get_files()
        return {
            "meets_standard": "Makefile" in files,
            "value": "Makefile" if "Makefile" in files else "not found",
        }

    @classmethod
    def _check_makefile(cls, repository: BaseRepository) -> bool:
        """Check if project has a Makefile at root level."""
        files = repository.get_files()
        return "Makefile" in files
