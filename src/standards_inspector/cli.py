import argparse
import json
import os
import sys
from typing import Dict, Union

from .constants import (
    CHECKMARK,
    CROSS,
    WARNING,
    GREEN,
    RED,
    ORANGE,
    RESET,
    FORMAT_JSON,
    FORMAT_CHECKLIST,
    SEVERITY_CRITICAL,
    STANDARD_CODES,
)
from .repositories import BaseRepository, GitLabRepository, LocalRepository
from .standards import (
    PythonVersionStandard,
    ProjectSpecStandard,
    MakefileStandard,
    NoCondaStandard,
    LockFileStandard,
)

# List of all standards
STANDARDS = [
    PythonVersionStandard,
    ProjectSpecStandard,
    MakefileStandard,
    NoCondaStandard,
    LockFileStandard,
]


class StandardsInspector:
    """A class to check standards in repositories.

    This class provides methods to check various Python coding standards in a specified repository.
    It supports both GitLab repositories and local directories.
    It supports formatting the results as a checklist or JSON.

    Attributes:
        repository: The repository instance (GitLab or Local)
    """

    def __init__(self, repository: BaseRepository):
        """Initialize the StandardsInspector with a repository instance.

        Args:
            repository: Repository instance to check standards against
        """
        self.repository = repository

    def format_checklist(self, standards_results: Dict[str, Dict]) -> str:
        """Format standards as a checklist with colored checkmarks/crosses."""
        output = ""
        for code, result in standards_results.items():
            if result["meets_standard"]:
                emoji = CHECKMARK
                color = GREEN
            else:
                emoji = WARNING
                color = ORANGE
                if result["severity"] == SEVERITY_CRITICAL:
                    emoji = CROSS
                    color = RED

            output += f"[{color}{emoji}{RESET}] [{code}] {result['description']}\n"
            if not result["meets_standard"]:
                output += f"    - Got: {result.get('value', 'not found')}\n"
                output += f"    - Suggestion: {result['recommendation']}\n"
        return output

    def format_json(self, standards_results: Dict[str, Dict]) -> str:
        """Format standards as JSON."""
        return json.dumps(standards_results, indent=2)

    def check_standards(
        self,
        output_format: str = FORMAT_CHECKLIST,
        standards: list | None = None,
    ) -> Union[Dict, str]:
        """Check Python standards in a repository and return results in specified format."""
        if not standards:
            standards = STANDARDS

        results = {}
        for std in standards:
            result = {**std.get_info()}
            result.update(std.check(self.repository))
            results[std.code] = result

        if output_format == FORMAT_JSON:
            return self.format_json(results)
        return self.format_checklist(results)


def main():
    """Main function to parse arguments and run checks."""
    parser = argparse.ArgumentParser(
        description="Check Python standards in repositories"
    )
    parser.add_argument(
        "--source",
        choices=["gitlab", "local"],
        required=True,
        help="Source type (gitlab or local)",
    )

    # Project ID is only required for GitLab
    gitlab_group = parser.add_argument_group("GitLab options")
    gitlab_group.add_argument(
        "--project-id",
        dest="project_id",
        help="GitLab project ID or URL (required if source=gitlab)",
    )
    gitlab_group.add_argument(
        "--token",
        dest="private_token",
        help="GitLab private token (can also use GITLAB_TOKEN env var)",
    )
    gitlab_group.add_argument(
        "--url",
        dest="gitlab_url",
        help="GitLab instance URL (defaults to https://gitlab.com)",
    )

    # Local specific argument
    local_group = parser.add_argument_group("Local options")
    local_group.add_argument(
        "--directory",
        dest="directory_path",
        help="Path to local directory to check (required if source=local)",
    )

    parser.add_argument(
        "--include",
        dest="include",
        nargs="+",
        choices=STANDARD_CODES,
        help="Include specific standards to check (comma-separated list)",
    )
    parser.add_argument(
        "--exclude",
        dest="exclude",
        nargs="+",
        choices=STANDARD_CODES,
        help="Exclude specific standards from check (comma-separated list)",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=[FORMAT_JSON, FORMAT_CHECKLIST],
        default=FORMAT_CHECKLIST,
        help="Output format (json or checklist)",
    )
    args = parser.parse_args()

    if args.include:
        invalid_codes = [code for code in args.include if code not in STANDARD_CODES]
        if invalid_codes:
            print(f"Error: Invalid standard codes: {', '.join(invalid_codes)}")
            sys.exit(1)

    if args.exclude:
        invalid_codes = [code for code in args.exclude if code not in STANDARD_CODES]
        if invalid_codes:
            print(f"Error: Invalid standard codes: {', '.join(invalid_codes)}")
            sys.exit(1)

    # Filter standards based on include/exclude options
    filtered_standards = STANDARDS.copy()
    if args.include:
        filtered_standards = [std for std in STANDARDS if std.code in args.include]
    elif args.exclude:
        filtered_standards = [std for std in STANDARDS if std.code not in args.exclude]

    # Create repository based on source type
    try:
        repository = None
        if args.source == "gitlab":
            if not args.project_id:
                raise ValueError("Project ID is required for GitLab source")

            if not args.private_token:
                args.private_token = os.getenv("GITLAB_TOKEN")
                if not args.private_token:
                    raise ValueError("GitLab token is required")

            gitlab_url = args.gitlab_url or os.getenv(
                "GITLAB_URL", "https://gitlab.com"
            )
            repository = GitLabRepository(
                gitlab_url, args.private_token, args.project_id
            )

        elif args.source == "local":
            if not args.directory_path:
                raise ValueError("Directory path is required for local source")
            repository = LocalRepository(args.directory_path)

        # Create checker with repository
        checker = StandardsInspector(repository)

        results = checker.check_standards(
            standards=filtered_standards, output_format=args.output_format
        )
        print(results)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
