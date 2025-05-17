import os
from typing import List
from .base import BaseRepository


class LocalRepository(BaseRepository):
    """Local directory repository implementation."""

    def __init__(self, directory_path: str):
        """Initialize local repository.

        Args:
            directory_path (str): Path to the local directory
        """
        self.directory_path = os.path.abspath(directory_path)
        if not os.path.isdir(self.directory_path):
            raise ValueError(f"Directory does not exist: {directory_path}")

    def get_files(self) -> List[str]:
        """Get list of files in the local directory.

        Returns:
            List[str]: List of file paths in the directory
        """
        files = []
        for root, _, filenames in os.walk(self.directory_path):
            for filename in filenames:
                relative_path = os.path.relpath(
                    os.path.join(root, filename), self.directory_path
                )
                files.append(relative_path)
        return files

    def read_file_content(self, file_path: str) -> bytes:
        """Read content of a file from local directory.

        Args:
            file_path (str): Path to the file

        Returns:
            bytes: Content of the file
        """
        absolute_path = os.path.join(self.directory_path, file_path)
        if not os.path.exists(absolute_path):
            raise ValueError(f"File not found: {file_path}")
        with open(absolute_path, "rb") as f:
            return f.read()
