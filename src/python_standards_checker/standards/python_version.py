import re
from python_standards_checker.utils import is_version_supported
from python_standards_checker.repositories import BaseRepository

from .base import BaseStandard


class PythonVersionStandard(BaseStandard):
    """Python version standard."""

    code = "PY001"
    category = "Version"
    standard = ">=3.9"
    severity = "CRITICAL"
    description = "Python version MUST be at least 3.9"
    recommendation = "Update your project's Python version requirement to at least 3.9"
    standard_type = "version"

    @classmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check Python version requirement."""
        files = repository.get_files()
        python_version = None

        # Check setup.py
        if "setup.py" in files:
            content = repository.read_file_content("setup.py").decode()
            match = re.search(r'python_requires="(>=3\.\d+)"', str(content))
            if match:
                python_version = match.group(1)

        # Check Dockerfile
        if "Dockerfile" in files and not python_version:
            content = repository.read_file_content("Dockerfile").decode()
            match = re.search(r"python:(3\.\d+)", str(content))
            if match:
                python_version = match.group(1)

        return {
            "meets_standard": python_version and is_version_supported(python_version),
            "value": python_version,
        }
