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
    def check(cls, gl: 'gitlab.Gitlab', project_id: str) -> dict:
        """Check for lock file."""
        has_lock_file = cls._check_lock_file(gl, project_id)
        return {
            "meets_standard": has_lock_file,
            "detected_version": "present" if has_lock_file else "not found"
        }

    @classmethod
    def _check_lock_file(cls, gl: 'gitlab.Gitlab', project_id: str) -> bool:
        """Check if project has a lock file (requirements.txt, poetry.lock, or pip-tools requirements.in)."""
        files = cls.get_repository_files(gl, project_id)
        
        # Check for common lock files
        lock_files = [
            "requirements.txt",
            "poetry.lock",
            "requirements.in"  # pip-tools
        ]
        
        return any(file in files for file in lock_files)
