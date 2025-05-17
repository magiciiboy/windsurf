from .base import BaseStandard
from typing import Optional


class LockFile(BaseStandard):
    """Lock file standard."""
    code = "PY005"
    category = "Dependency Management"
    standard = True
    severity = "RECOMMENDATION"
    description = "Project SHOULD have a lock file (poetry.lock, pip-tools requirements.in, requirements.txt)"
    recommendation = "Create a lock file to ensure consistent dependency versions across environments"
    standard_type = "file"

    @classmethod
    def check(cls, project_id: str, checker: 'GitLabChecker') -> dict:
        """Check for lock file."""
        has_lock_file = checker._check_lock_file(project_id)
        return {
            "meets_standard": has_lock_file,
            "detected_version": "present" if has_lock_file else "not found"
        }
