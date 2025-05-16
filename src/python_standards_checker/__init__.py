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
WARNING = "\u26A0"   # ⚠
GREEN = "\033[92m"
RED = "\033[91m"
ORANGE = "\033[33m"
RESET = "\033[0m"

# Output formats
FORMAT_JSON = "json"
FORMAT_CHECKLIST = "checklist"

# Severity levels
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_RECOMMENDATION = "RECOMMENDATION"

# Standards with severity and descriptions
STANDARDS = {
    "python_version": {
        "standard": ">=3.9",
        "severity": SEVERITY_CRITICAL,
        "description": "Python version must be at least 3.9",
        "recommendation": "Update your project's Python version requirement to at least 3.9",
        "standard_type": "version"
    },
    "pyproject_toml": {
        "standard": True,
        "severity": SEVERITY_RECOMMENDATION,
        "description": "Project should have a pyproject.toml specification",
        "recommendation": "Create a pyproject.toml file to specify project metadata and dependencies",
        "standard_type": "file"
    }
}

class GitLabChecker:
    def __init__(self, gitlab_url: Optional[str] = None, private_token: Optional[str] = None):
        self.gitlab_url = gitlab_url or os.getenv("GITLAB_URL", "https://gitlab.com")
        self.gl = gitlab.Gitlab(self.gitlab_url, private_token=private_token)

    def format_checklist(self, standards: Dict[str, Dict]) -> str:
        """Format standards as a checklist with colored checkmarks/crosses."""
        output = []
        
        for std_name, std_data in standards.items():
            # Get standard info from STANDARDS dictionary
            std_info = STANDARDS[std_name]
            
            # Format the check mark with appropriate color and symbol
            if std_data["meets_standard"]:
                check = f"{GREEN}{CHECKMARK}{RESET}"
            else:
                if std_info["severity"] == SEVERITY_CRITICAL:
                    check = f"{RED}{CROSS}{RESET}"
                else:  # RECOMMENDATION
                    check = f"{ORANGE}{WARNING}{RESET}"
            
            # Format the standard line
            output.append(f"[{check}] {std_info['description']}")
            
            # Add recommendation if standard is not met
            if not std_data["meets_standard"]:
                output.append(f"  • {std_info['recommendation']}")
        
        return "\n".join(output)

    def _format_check(self, meets_standard: bool, severity: str) -> str:
        """Format a single check with colored checkmark/cross."""
        if meets_standard:
            return f"{GREEN}{CHECKMARK}{RESET}"
        if severity == SEVERITY_CRITICAL:
            return f"{RED}{CROSS}{RESET}"
        return f"{ORANGE}{WARNING}{RESET}"

    def check_standards(self, project_id: str, output_format: str = FORMAT_JSON) -> Union[Dict, str]:
        """Check Python standards in a GitLab project and return results in specified format."""
        python_version = self.get_python_version(project_id)
        pyproject_toml = self._check_pyproject_toml(project_id)
        
        # Get standard info from STANDARDS dictionary
        python_std = STANDARDS["python_version"]
        toml_std = STANDARDS["pyproject_toml"]
        
        standards = {
            "python_version": {
                "standard": python_std["standard"],
                "severity": python_std["severity"],
                "description": python_std["description"],
                "recommendation": python_std["recommendation"],
                "meets_standard": python_version and self.is_version_supported(python_version),
                "detected_version": python_version
            },
            "pyproject_toml": {
                "standard": toml_std["standard"],
                "severity": toml_std["severity"],
                "description": toml_std["description"],
                "recommendation": toml_std["recommendation"],
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
