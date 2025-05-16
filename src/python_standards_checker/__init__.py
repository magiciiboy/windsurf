import argparse
import json
import os
import re
from typing import Dict, List, Optional, Union
import gitlab
from gitlab.v4.objects import Project
import pytoml
from packaging import version

# ANSI color codes for terminal output
CHECKMARK = "\u2713"  # ✓
CROSS = "\u2717"     # ✗
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Output formats
FORMAT_JSON = "json"
FORMAT_CHECKLIST = "checklist"

# Standards
PYTHON_VERSION_STANDARD = ">=3.9"
PYPROJECT_TOML_STANDARD = True

class GitLabChecker:
    def __init__(self, gitlab_url: Optional[str] = None, private_token: Optional[str] = None):
        self.gitlab_url = gitlab_url or os.getenv("GITLAB_URL", "https://gitlab.com")
        self.gl = gitlab.Gitlab(self.gitlab_url, private_token=private_token)

    def format_checklist(self, standards: Dict[str, Dict]) -> str:
        """Format standards as a checklist with colored checkmarks/crosses."""
        output = []
        
        # Format Python version check
        python_version = standards["python_version"]
        version_check = self._format_check(python_version["meets_standard"])
        output.append(f"Python version {python_version['detected_version'] or 'not found'} {version_check}")
        
        # Format pyproject.toml check
        pyproject = standards["pyproject_toml"]
        pyproject_check = self._format_check(pyproject["meets_standard"])
        output.append(f"pyproject.toml specification {pyproject_check}")
        
        return "\n".join(output)

    def _format_check(self, meets_standard: bool) -> str:
        """Format a single check with colored checkmark/cross."""
        if meets_standard:
            return f"{GREEN}{CHECKMARK}{RESET}"
        return f"{RED}{CROSS}{RESET}"

    def check_standards(self, project_id: str, output_format: str = FORMAT_JSON) -> Union[Dict, str]:
        """Check Python standards in a GitLab project and return results in specified format."""
        python_version = self.get_python_version(project_id)
        pyproject_toml = self._check_pyproject_toml(project_id)
        
        standards = {
            "python_version": {
                "standard": PYTHON_VERSION_STANDARD,
                "meets_standard": python_version and self.is_version_supported(python_version),
                "detected_version": python_version
            },
            "pyproject_toml": {
                "standard": PYPROJECT_TOML_STANDARD,
                "meets_standard": pyproject_toml,
                "detected_version": "present" if pyproject_toml else "not found"
            }
        }
        
        if output_format == FORMAT_CHECKLIST:
            return self.format_checklist(standards)
        return standards

    def _check_pyproject_toml(self, project_id: str) -> bool:
        """Check if project has a valid pyproject.toml file."""
        files = self.get_repository_files(project_id)
        return "pyproject.toml" in files

    def get_repository_files(self, project_id: str) -> List[str]:
        """Get list of files from GitLab repository."""
        project = self.gl.projects.get(project_id)
        items = project.repository_tree(all=True, recursive=True)
        return [item['name'] for item in items]

    def get_python_version(self, project_id: str) -> Optional[str]:
        """Detect Python version from various files."""
        files = self.get_repository_files(project_id)
        
        # Check pyproject.toml first
        if "pyproject.toml" in files:
            content = self.gl.projects.get(project_id).files.get(
                file_path="pyproject.toml", ref="main"
            ).decode()
            toml_data = pytoml.loads(content)
            if "project" in toml_data and "requires-python" in toml_data["project"]:
                return toml_data["project"]["requires-python"]

        # Check setup.py
        if "setup.py" in files:
            content = self.gl.projects.get(project_id).files.get(
                file_path="setup.py", ref="main"
            ).decode()
            match = re.search(r'python_requires="(>=3\.\d+)', content)
            if match:
                return match.group(1)

        # Check Dockerfile
        if "Dockerfile" in files:
            content = self.gl.projects.get(project_id).files.get(
                file_path="Dockerfile", ref="main"
            ).decode()
            match = re.search(r'python:(3\.\d+)', content)
            if match:
                return match.group(1)
        return None

    def is_version_supported(self, version_spec: str) -> bool:
        """Check if a version specification meets the minimum requirement."""
        if not version_spec:
            return False
        
        try:
            # Extract the actual version number from version specifiers
            if version_spec.startswith(('>=', '>', '~=')):
                version_str = version_spec.split(',')[0].split(' ')[0]
            elif version_spec == '==3.9':
                version_str = '3.9'
            elif version_spec == '!=3.8':
                return True
            else:
                version_str = version_spec
            
            # Compare with minimum requirement
            return version.parse(version_str) >= version.parse('3.9')
        except Exception:
            return False

def main():
    parser = argparse.ArgumentParser(description='Check Python standards in GitLab repositories.')
    parser.add_argument('project_id', help='GitLab project ID')
    parser.add_argument('--token', help='GitLab private token')
    parser.add_argument('--url', help='GitLab instance URL')
    parser.add_argument('--format', choices=[FORMAT_JSON, FORMAT_CHECKLIST], default=FORMAT_CHECKLIST,
                       help='Output format (json or checklist)')
    args = parser.parse_args()

    # Get token from environment variable if not provided as argument
    token = args.token or os.getenv("GITLAB_TOKEN")
    url = args.url or os.getenv("GITLAB_URL")
    
    if not token:
        print("Error: GitLab token is required. Please provide it via --token or GITLAB_TOKEN environment variable.")
        return

    checker = GitLabChecker(gitlab_url=url, private_token=token)
    result = checker.check_standards(args.project_id, args.format)
    
    if args.format == FORMAT_JSON:
        print(json.dumps(result, indent=2))
    else:
        print(result)

if __name__ == "__main__":
    main()
