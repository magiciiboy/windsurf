from .base import BaseStandard
from typing import Optional


class Makefile(BaseStandard):
    """Makefile standard."""
    code = "PY003"
    category = "Project Structure"
    standard = True
    severity = "RECOMMENDATION"
    description = "Project SHOULD have Makefile at root level"
    recommendation = "Create a Makefile at the root of your project to define build and automation targets"
    standard_type = "file"

    @classmethod
    def check(cls, project_id: str, checker: 'GitLabChecker') ->dict:
        """Check for Makefile."""
        has_makefile = checker._check_makefile(project_id)
        return {
            "meets_standard": has_makefile,
            "detected_version": "present" if has_makefile else "not found"
        }
