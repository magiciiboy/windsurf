import gitlab
from python_standards_checker.constants import CONDA_FILES
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
    def check(cls, gl: "gitlab.Gitlab", project_id: str) -> dict:
        """Check for conda usage."""
        uses_conda = cls._check_conda_usage(gl, project_id)
        return {
            "meets_standard": not uses_conda,
            "value": "not found" if not uses_conda else "found conda usage",
        }

    @classmethod
    def _check_conda_usage(cls, gl: "gitlab.Gitlab", project_id: str) -> bool:
        """Check for conda usage in various files."""
        files = cls.get_repository_files(gl, project_id)

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
                content = (
                    gl.projects.get(project_id)
                    .files.get(file_path=ci_file, ref="main")
                    .decode()
                )
                if content and b"conda" in content.lower():
                    return True

        # Check shell scripts for conda commands
        for file in files:
            if file.endswith(".sh"):
                try:
                    content = (
                        gl.projects.get(project_id)
                        .files.get(file_path=file, ref="main")
                        .decode()
                    )
                    if content and b"conda" in content.lower():
                        return True
                except Exception as e:
                    print(f"Error checking file {file}: {str(e)}")
                    continue

        return False
