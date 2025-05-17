from abc import ABC, abstractmethod
from typing import List


class BaseRepository(ABC):
    """Base class for repository implementations."""

    @abstractmethod
    def get_files(self) -> List[str]:
        """Get list of files in the repository.

        Returns:
            List[str]: List of file paths in the repository
        """
        raise NotImplementedError

    @abstractmethod
    def read_file_content(self, file_path: str) -> bytes:
        """Read content of a file.

        Args:
            file_path (str): Path to the file

        Returns:
            bytes: Content of the file
        """
        raise NotImplementedError
