import re
from abc import ABC, abstractmethod
from typing import Optional, Union, Dict
import pytoml

from python_standards_checker.repositories import BaseRepository


class BaseStandard(ABC):
    """Base class for all Python standards."""

    # Static attributes that must be defined by subclasses
    code: str = ""
    category: str = ""
    standard: Union[str, bool] = ""
    severity: str = ""
    description: str = ""
    recommendation: str = ""
    standard_type: str = ""

    @classmethod
    def get_info(cls) -> Dict:
        """Get standard information as a dictionary.

        Returns:
            dict: Dictionary containing standard information with keys:
                - code: str
                - category: str
                - standard: str
                - severity: str
                - description: str
                - recommendation: str
                - standard_type: str
        """
        return {
            "code": cls.code,
            "category": cls.category,
            "standard": cls.standard,
            "severity": cls.severity,
            "description": cls.description,
            "recommendation": cls.recommendation,
            "standard_type": cls.standard_type,
        }

    @classmethod
    @abstractmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check if the standard is met.

        Args:
            repository: Repository instance

        Returns:
            dict: Dictionary containing check result with keys:
                - meets_standard: bool
                - value: str (if applicable)
        """
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    def get_python_version(cls, repository: BaseRepository) -> Optional[str]:
        """Detect Python version from various files.

        Args:
            repository: Repository instance

        Returns:
            Python version string if found, None otherwise
        """
        files = repository.get_files()

        # Check pyproject.toml first
        if "pyproject.toml" in files:
            content = repository.read_file_content("pyproject.toml").decode()
            toml_data = pytoml.loads(content)
            if "project" in toml_data and "requires-python" in toml_data["project"]:
                return toml_data["project"]["requires-python"]

        # Check setup.py
        if "setup.py" in files:
            content = repository.read_file_content("setup.py").decode()
            match = re.search(r'python_requires="(>=3\.\d+)"', str(content))
            if match:
                return match.group(1)

        # Check Dockerfile
        if "Dockerfile" in files:
            content = repository.read_file_content("Dockerfile").decode()
            match = re.search(r"python:(3\.\d+)", str(content))
            if match:
                return match.group(1)
        return None
