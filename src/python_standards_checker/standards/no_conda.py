from python_standards_checker.constants import CONDA_FILES
from python_standards_checker.repositories import BaseRepository

from .base import BaseStandard


class NoCondaStandard(BaseStandard):
    """No Conda standard."""

    code = "PY004"
    category = "Dependency Management"
    standard = False
    severity = "CRITICAL"
    description = "Project MUST NOT use conda"
    recommendation = "Remove conda dependencies and use uv, poetry, or pip instead"
    standard_type = "dependency"

    @classmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check if project uses conda."""
        files = repository.get_files()
        has_conda_file = any(
            file.endswith(".yml") or file.endswith(".yaml") for file in files
        )
        return {
            "meets_standard": not has_conda_file,
            "value": (
                "no conda file found" if not has_conda_file else "conda file found"
            ),
        }

    @classmethod
    def _check_conda_usage(cls, repository: BaseRepository) -> bool:
        """Check for conda usage in various files."""
        files = repository.get_files()

        # Check for conda-related files
        for file in files:
            if (
                any(file.endswith(ext) for ext in CONDA_FILES)
                or "conda" in file.lower()
            ):
                return True

        # Check for conda in .gitlab-ci.yml
        ci_files = [".gitlab-ci.yml", ".gitlab-ci.yaml"]
        for ci_file in ci_files:
            if ci_file in files:
                content = repository.read_file_content(ci_file).decode()
                if content and "conda" in content.lower():
                    return True

        # Check shell scripts for conda commands
        for file in files:
            if file.endswith(".sh"):
                try:
                    content = repository.read_file_content(file).decode()
                    if content and "conda" in content.lower():
                        return True
                except Exception as e:
                    print(f"Error checking file {file}: {str(e)}")
                    continue

        return False
