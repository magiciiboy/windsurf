from python_standards_checker.utils import is_version_supported
from python_standards_checker.repositories import BaseRepository

from .base import BaseStandard


class PythonVersionStandard(BaseStandard):
    """Python version standard."""

    code = "PY001"
    category = "Version"
    standard = "3.9"
    severity = "CRITICAL"
    description = "Python version MUST be at least 3.9"
    recommendation = "Update your project's Python version requirement to at least 3.9"
    standard_type = "version"

    @classmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check Python version requirement."""
        python_version = cls.get_python_version(repository)

        return {
            "meets_standard": python_version
            and is_version_supported(python_version, cls.standard),
            "value": python_version,
        }
