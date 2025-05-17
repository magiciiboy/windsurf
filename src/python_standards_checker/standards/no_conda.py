from .base import BaseStandard
from typing import Optional


class NoConda(BaseStandard):
    """No Conda standard."""
    code = "PY004"
    category = "Dependency Management"
    standard = False
    severity = "CRITICAL"
    description = "Project MUST NOT use conda"
    recommendation = "Remove conda dependencies and use uv, poetry, or pip instead"
    standard_type = "dependency"

    @classmethod
    def check(cls, project_id: str, checker: 'GitLabChecker') -> dict:
        """Check for conda usage."""
        uses_conda = checker._check_conda_usage(project_id)
        return {
            "meets_standard": not uses_conda,
            "detected_version": "not found" if not uses_conda else "found conda usage"
        }
