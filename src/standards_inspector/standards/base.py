import re
from abc import ABC, abstractmethod
from typing import Optional, Union, Dict
from functools import lru_cache

import pytoml
from packaging import version as semver

from standards_inspector.utils import get_min_version
from standards_inspector.repositories import BaseRepository
from standards_inspector.constants import (
    PYTHON_REQUIRES_REGEX,
    PYTHON_COMMAND_REGEX,
    PYTHON_REGEX,
)


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
    @lru_cache(maxsize=1)
    def get_python_version(cls, repository: BaseRepository) -> Optional[str]:
        """Detect Python version from various files.

        Args:
            repository: Repository instance

        Returns:
            Python version string if found, None otherwise
        """

        min_runtime_version = cls.get_python_min_runtime_version(repository)
        min_spec_version = cls.get_python_min_spec_version(repository)

        if min_runtime_version and min_spec_version:
            return min(min_runtime_version, min_spec_version)

        if min_runtime_version:
            return min_runtime_version

        if min_spec_version:
            return min_spec_version

        return None

    @classmethod
    @lru_cache(maxsize=1)
    def get_python_min_spec_version(cls, repository: BaseRepository) -> Optional[str]:
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
                return get_min_version(toml_data["project"]["requires-python"])

        # Check setup.py
        if "setup.py" in files:
            content = repository.read_file_content("setup.py").decode()
            match = re.search(PYTHON_REQUIRES_REGEX, str(content))
            if match:
                return get_min_version(match.group("version"))

        return None

    @classmethod
    @lru_cache(maxsize=1)
    def get_python_min_runtime_version(
        cls, repository: BaseRepository
    ) -> Optional[str]:
        """Detect Python version from various files.

        Args:
            repository: Repository instance

        Returns:
            Python version string if found, None otherwise
        """
        files = repository.get_files()
        possible_versions = []

        # Check Dockerfile
        if "Dockerfile" in files:
            content = repository.read_file_content("Dockerfile").decode()
            match = re.search(PYTHON_REGEX, str(content))
            if match:
                possible_versions.append(get_min_version(match.group("version")))

        # Check shell scripts for conda commands
        for file in files:
            if file.endswith(".sh"):
                try:
                    content = repository.read_file_content(file).decode()
                    match = re.search(PYTHON_COMMAND_REGEX, str(content))
                    if match:
                        possible_versions.append(
                            get_min_version(match.group("version"))
                        )
                except Exception as e:
                    print(f"Error checking file {file}: {str(e)}")
                    continue

        # Sorted possible versions by semver, get the lowest version
        if possible_versions:
            versions: list[str] = list(filter(None, possible_versions))
            return sorted(versions, key=semver.parse)[0]

        return None
