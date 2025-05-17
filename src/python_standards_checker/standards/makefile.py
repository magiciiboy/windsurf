import gitlab
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
    def check(cls, gl: "gitlab.Gitlab", project_id: str) -> dict:
        """Check for Makefile."""
        has_makefile = cls._check_makefile(gl, project_id)
        return {
            "meets_standard": has_makefile,
            "value": "present" if has_makefile else "not found",
        }

    @classmethod
    def _check_makefile(cls, gl: "gitlab.Gitlab", project_id: str) -> bool:
        """Check if project has a Makefile at root level."""
        files = cls.get_repository_files(gl, project_id)
        return "Makefile" in files
