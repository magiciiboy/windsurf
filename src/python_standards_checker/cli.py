import argparse
import json
import os
import sys
from typing import Dict, Optional, Union
import gitlab
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
from .standards import STANDARDS


class GitLabChecker:
    """A class to check Python standards in GitLab projects.

    This class provides methods to authenticate with a GitLab instance and
    check various Python coding standards in a specified GitLab project.
    It supports formatting the results as a checklist or JSON.

    Attributes:
        gitlab_url: The URL of the GitLab instance.
        gl: The GitLab API client instance.
    """

    def __init__(
        self, gitlab_url: Optional[str] = None, private_token: Optional[str] = None
    ):
        """Initialize GitLab API client.

        Args:
            gitlab_url: URL of the GitLab instance
            private_token: GitLab private token for authentication

        Raises:
            ValueError: If token is not provided and not found in environment
            ValueError: If GitLab URL is invalid
        """
        if not private_token:
            private_token = os.getenv("GITLAB_TOKEN")
            if not private_token:
                raise ValueError(
                    "GitLab token is required. Please provide it via --private-token \n"
                    "or GITLAB_TOKEN environment variable."
                )

        self.gitlab_url = gitlab_url or os.getenv("GITLAB_URL", "https://gitlab.com")
        if not self.gitlab_url or not self.gitlab_url.startswith("https://"):
            raise ValueError(
                f"Invalid GitLab URL: {self.gitlab_url}. Must be a full URL starting with https://"
            )

        self.gl = gitlab.Gitlab(self.gitlab_url, private_token=private_token)

        # Test connection
        try:
            self.gl.auth()
        except gitlab.exceptions.GitlabAuthenticationError as e:
            raise ValueError("Invalid GitLab token. Authentication failed.") from e
        except Exception as e:
            raise ValueError(f"Failed to connect to GitLab: {str(e)}") from e

    def format_checklist(self, standards_results: Dict[str, Dict]) -> str:
        """Format standards as a checklist with colored checkmarks/crosses."""
        output = []

        for _, std in standards_results.items():
            # Format the check mark with appropriate color and symbol
            if std["meets_standard"]:
                check = f"{GREEN}{CHECKMARK}{RESET}"
            else:
                if std["severity"] == SEVERITY_CRITICAL:
                    check = f"{RED}{CROSS}{RESET}"
                else:  # RECOMMENDATION
                    check = f"{ORANGE}{WARNING}{RESET}"

            # Format the standard line
            output.append(f"[{check}] [{std['code']}] {std['description']}")

            # Add recommendation if standard is not met
            if not std["meets_standard"]:
                output.append(f"    - Got: {std['value']}")
                output.append(f"    - Suggestion: {std['recommendation']}")

        return "\n".join(output)

    def format_json(self, standards_results: Dict[str, Dict]) -> str:
        """Format standards as JSON."""
        return json.dumps(standards_results, indent=2)

    def check_standards(
        self,
        project_id: str,
        output_format: str = FORMAT_CHECKLIST,
        standards: list | None = None,
    ) -> Union[Dict, str]:
        """Check Python standards in a GitLab project and return results in specified format."""
        if not standards:
            standards = STANDARDS

        results = {}
        for std in standards:
            result = std.check(self.gl, project_id)
            result = {**result, **std.get_info()}
            results[std.code] = result

        if output_format == FORMAT_JSON:
            return self.format_json(results)
        return self.format_checklist(results)


def main():
    """Main function to handle command-line arguments and run checks."""
    parser = argparse.ArgumentParser(
        description="Check Python standards in GitLab projects"
    )
    parser.add_argument("project_id", help="GitLab project ID")
    parser.add_argument("--gitlab-url", help="GitLab URL (default: https://gitlab.com)")
    parser.add_argument("--private-token", help="GitLab private token")
    parser.add_argument(
        "--format",
        choices=[FORMAT_JSON, FORMAT_CHECKLIST],
        default=FORMAT_CHECKLIST,
        help="Output format (default: checklist)",
    )
    parser.add_argument(
        "--include", nargs="*", help="Include specific standards by code (e.g., PY001)"
    )
    parser.add_argument(
        "--exclude", nargs="*", help="Exclude specific standards by code (e.g., PY001)"
    )

    args = parser.parse_args()

    # Validate project ID
    try:
        project_id = int(args.project_id)
    except ValueError:
        print(f"Error: Project ID must be a number, got '{args.project_id}'")
        sys.exit(1)

    # Validate included/excluded standards
    if args.include and args.exclude:
        print("Error: Cannot use --include and --exclude together")
        sys.exit(1)

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

    # Create checker and run checks
    try:
        checker = GitLabChecker(
            gitlab_url=args.gitlab_url, private_token=args.private_token
        )

        # Test project access before running checks
        try:
            project = checker.gl.projects.get(project_id)
            print(f"Successfully connected to project: {project.name}")
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Error: Failed to access project ID {project_id}: {str(e)}")
            sys.exit(1)

        results = checker.check_standards(project_id, args.format, filtered_standards)
        print(results)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
