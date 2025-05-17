import re
from abc import ABC, abstractmethod
from typing import Optional, List, Union
from functools import lru_cache

import gitlab
import pytoml


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
    def get_info(cls) -> dict:
        """Get standard information as a dictionary.

        Returns:
            dict: Dictionary containing standard metadata:
                - code: Standard code
                - category: Standard category
                - standard: Standard status (True/False)
                - severity: Standard severity level
                - description: Standard description
                - recommendation: Standard recommendation
                - standard_type: Standard type
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
    def check(cls, gl: "gitlab.Gitlab", project_id: str) -> dict:
        """Check if the standard is met.

        Args:
            gl: GitLab API client instance
            project_id: GitLab project ID

        Returns:
            Dict containing:
            - meets_standard: bool
            - value: str (if applicable)
        """
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    @lru_cache(maxsize=128)
    def get_repository_files(cls, gl: "gitlab.Gitlab", project_id: str) -> List[str]:
        """Get list of files from GitLab repository.

        Args:
            gl: GitLab API client instance
            project_id: GitLab project ID

        Returns:
            List of file names in the repository

        Note:
            This method uses LRU caching to avoid redundant API calls when multiple
            standards check the same files. The cache size is set to 128 projects.
        """
        project = gl.projects.get(project_id)
        items = project.repository_tree(all=True, recursive=True)
        return [item["name"] for item in items]

    @classmethod
    def get_python_version(cls, gl: "gitlab.Gitlab", project_id: str) -> Optional[str]:
        """Detect Python version from various files.

        Args:
            gl: GitLab API client instance
            project_id: GitLab project ID

        Returns:
            Python version string if found, None otherwise
        """
        files = cls.get_repository_files(gl, project_id)

        # Check pyproject.toml first
        if "pyproject.toml" in files:
            content = (
                gl.projects.get(project_id)
                .files.get(file_path="pyproject.toml", ref="main")
                .decode()
            )
            toml_data = pytoml.loads(content)
            if "project" in toml_data and "requires-python" in toml_data["project"]:
                return toml_data["project"]["requires-python"]

        # Check setup.py
        if "setup.py" in files:
            content = (
                gl.projects.get(project_id)
                .files.get(file_path="setup.py", ref="main")
                .decode()
            )
            match = re.search(r'python_requires="(>=3\.\d+)"', str(content))
            if match:
                return match.group(1)

        # Check Dockerfile
        if "Dockerfile" in files:
            content = (
                gl.projects.get(project_id)
                .files.get(file_path="Dockerfile", ref="main")
                .decode()
            )
            match = re.search(r"python:(3\.\d+)", str(content))
            if match:
                return match.group(1)
        return None
