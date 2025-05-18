from typing import List
from functools import lru_cache

from gitlab import Gitlab
from gitlab.v4.objects import Project
from gitlab.exceptions import GitlabGetError

from .base import BaseRepository


class GitLabRepository(BaseRepository):
    """GitLab repository implementation."""

    gl: Gitlab
    project: Project

    def __init__(self, gitlab_url: str, private_token: str, project_id: str):
        """Initialize GitLab repository.

        Args:
            gitlab_url (str): URL of the GitLab instance
            private_token (str): GitLab private token
            project_id (str): GitLab project ID
        """
        self.gl = Gitlab(gitlab_url, private_token=private_token)
        self.project_id = project_id
        self.test_connection()

    def test_connection(self) -> None:
        """Test connection to the GitLab project.

        Raises:
            ValueError: If project initialization fails
        """
        if self.gl:
            self.gl.auth()

            try:
                self.project = self.gl.projects.get(self.project_id)
                print(f"Successfully connected to project: {self.project.name}")
            except GitlabGetError as e:
                raise ValueError(
                    f"Failed to access project ID {self.project_id}: {str(e)}"
                ) from e

    @lru_cache(maxsize=128)
    def read_file_content(self, file_path: str) -> bytes:
        """Read content of a file from GitLab repository.

        Args:
            file_path (str): Path to the file

        Returns:
            bytes: Content of the file

        Raises:
            ValueError: If project is not initialized
        """
        if not self.project or not self.gl:
            raise ValueError(
                "Repository not initialized. Call test_connection() first."
            )

        try:
            return self.project.files.get(file_path=file_path, ref="main").decode()
        except Exception as e:
            raise ValueError(f"Failed to read file {file_path}: {str(e)}") from e

    @lru_cache(maxsize=1)
    def get_files(self) -> List[str]:
        """Get list of files in the GitLab repository.

        Returns:
            List[str]: List of file paths in the repository

        Raises:
            ValueError: If project is not initialized
        """
        if not self.gl or not self.project:
            raise ValueError(
                "Repository not initialized. Call test_connection() first."
            )
        try:
            self.gl.auth()
            return [
                file["path"]
                for file in self.gl.projects.get(self.project_id).repository_tree(
                    all=True
                )
            ]
        except Exception as e:
            raise ValueError(f"Failed to get repository files: {str(e)}") from e

    def clear_cache(self) -> None:
        """Clear the cache for file operations."""
        self.get_files.cache_clear()
        self.read_file_content.cache_clear()
