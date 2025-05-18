from python_standards_checker.repositories import BaseRepository

from .base import BaseStandard


class LockFileStandard(BaseStandard):
    """Lock file standard."""

    code = "PY005"
    category = "Dependency Management"
    standard = True
    severity = "RECOMMENDATION"
    description = "Project SHOULD have a lock file"
    recommendation = (
        "Create a lock file to ensure consistent dependency versions across environments. "
        + "Use poetry.lock, pip-tools requirements.in, requirements.txt, or any other lock file format."
    )
    standard_type = "file"

    @classmethod
    def check(cls, repository: BaseRepository) -> dict:
        """Check if project has a lock file."""
        files = repository.get_files()
        return {
            "meets_standard": any(
                file.endswith(".lock") or file == "requirements.txt" for file in files
            ),
            "value": (
                "lock file found"
                if any(
                    file.endswith(".lock") or file == "requirements.txt"
                    for file in files
                )
                else "no lock file found"
            ),
        }
