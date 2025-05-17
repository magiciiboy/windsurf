from .base import BaseStandard
from typing import Optional


class PythonVersion(BaseStandard):
    """Python version standard."""
    code = "PY001"
    category = "Version"
    standard = ">=3.9"
    severity = "CRITICAL"
    description = "Python version MUST be at least 3.9"
    recommendation = "Update your project's Python version requirement to at least 3.9"
    standard_type = "version"

    @classmethod
    def check(cls, gl: 'gitlab.Gitlab', project_id: str) -> dict:
        """Check Python version requirement."""
        python_version = cls.get_python_version(gl, project_id)
        return {
            "meets_standard": python_version and cls.is_version_supported(python_version),
            "detected_version": python_version
        }
