import argparse
import json
import os
import re
from typing import Dict, List, Optional, Union
import gitlab
from gitlab.v4.objects import Project
import pytoml
from packaging import version
from .constants import (
    CHECKMARK, CROSS, WARNING, GREEN, RED, ORANGE, RESET,
    FORMAT_JSON, FORMAT_CHECKLIST,
    SEVERITY_CRITICAL,
    STANDARDS, STANDARD_CODES
)

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
                output.append(f"    - Suggestion: {std_info['recommendation']}")
        
        return "\n".join(output)

    def _format_check(self, meets_standard: bool, severity: str) -> str:
        """Format a single check with colored checkmark/cross."""
        if meets_standard:
            return f"{GREEN}{CHECKMARK}{RESET}"
        if severity == SEVERITY_CRITICAL:
            return f"{RED}{CROSS}{RESET}"
        return f"{ORANGE}{WARNING}{RESET}"

    def check_standards(self, project_id: str, output_format: str = FORMAT_JSON, standards: Dict[str, Dict] = None) -> Union[Dict, str]:
        """Check Python standards in a GitLab project and return results in specified format."""
        if standards is None:
            standards = STANDARDS

        python_version = self.get_python_version(project_id)
        pyproject_toml = self._check_pyproject_toml(project_id)
        has_makefile = self._check_makefile(project_id)
        uses_conda = self._check_conda_usage(project_id)
        has_lock_file = self._check_lock_file(project_id)
        
        results = {}
        for std_name, std in standards.items():
            if std_name == "python_version":
                results[std_name] = {
                    "code": std["code"],
                    "category": std["category"],
                    "standard": std["standard"],
                    "severity": std["severity"],
                    "description": std["description"],
                    "recommendation": std["recommendation"],
                    "meets_standard": python_version and self.is_version_supported(python_version),
                    "detected_version": python_version
                }
            elif std_name == "pyproject_toml":
                results[std_name] = {
                    "code": std["code"],
                    "category": std["category"],
                    "standard": std["standard"],
                    "severity": std["severity"],
                    "description": std["description"],
                    "recommendation": std["recommendation"],
                    "meets_standard": pyproject_toml,
                    "detected_version": "present" if pyproject_toml else "not found"
                }
            elif std_name == "makefile":
                results[std_name] = {
                    "code": std["code"],
                    "category": std["category"],
                    "standard": std["standard"],
                    "severity": std["severity"],
                    "description": std["description"],
                    "recommendation": std["recommendation"],
                    "meets_standard": has_makefile,
                    "detected_version": "present" if has_makefile else "not found"
                }
            elif std_name == "no_conda":
                results[std_name] = {
                    "code": std["code"],
                    "category": std["category"],
                    "standard": std["standard"],
                    "severity": std["severity"],
                    "description": std["description"],
                    "recommendation": std["recommendation"],
                    "meets_standard": not uses_conda,
                    "detected_version": "not found" if not uses_conda else "found conda usage"
                }
            elif std_name == "lock_file":
                results[std_name] = {
                    "code": std["code"],
                    "category": std["category"],
                    "standard": std["standard"],
                    "severity": std["severity"],
                    "description": std["description"],
                    "recommendation": std["recommendation"],
                    "meets_standard": has_lock_file,
                    "detected_version": "present" if has_lock_file else "not found"
                }
        
        if output_format == FORMAT_CHECKLIST:
            return self.format_checklist(results)
        return results

    def _check_lock_file(self, project_id: str) -> bool:
        """Check if project has a lock file (requirements.txt, poetry.lock, or pip-tools requirements.in)."""
        files = self.get_repository_files(project_id)
        
        # Check for common lock files
        lock_files = [
            "requirements.txt",
            "poetry.lock",
            "requirements.in"  # pip-tools
        ]
        
        return any(file in files for file in lock_files)

    def _check_makefile(self, project_id: str) -> bool:
        """Check if project has a Makefile at root level."""
        files = self.get_repository_files(project_id)
        return "Makefile" in files

    def _check_conda_usage(self, project_id: str) -> bool:
        """Check for conda usage in various files."""
        files = self.get_repository_files(project_id)
        
        # Check for conda-related files
        conda_files = [
            "environment.yml",
            ".condarc",
            "*.conda",
            "*.yml",
            "*.yaml"
        ]
        
        # Check for conda in filenames
        for file in files:
            if any(file.endswith(ext) for ext in conda_files) or "conda" in file.lower():
                return True
        
        # Check for conda in .gitlab-ci.yml
        ci_files = [".gitlab-ci.yml", ".gitlab-ci.yaml"]
        for ci_file in ci_files:
            if ci_file in files:
                content = self.gl.projects.get(project_id).files.get(
                    file_path=ci_file, ref="main"
                ).decode()
                if content and b"conda" in content.lower():
                    return True
        
        # Check shell scripts for conda commands
        for file in files:
            if file.endswith(".sh"):
                try:
                    content = self.gl.projects.get(project_id).files.get(
                        file_path=file, ref="main"
                    ).decode()
                    if content and b"conda" in content.lower():
                        return True
                except Exception:
                    continue
        
        return False

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
    parser.add_argument('--include', nargs='*', help='List of standard codes to include (e.g., PY001 PY002)')
    parser.add_argument('--exclude', nargs='*', help='List of standard codes to exclude (e.g., PY003 PY004)')
    parser.add_argument('--list-standards', action='store_true', help='List all available standards and their codes')
    args = parser.parse_args()

    # Get token from environment variable if not provided as argument
    token = args.token or os.getenv("GITLAB_TOKEN")
    url = args.url or os.getenv("GITLAB_URL")
    
    if not token:
        print("Error: GitLab token is required. Please provide it via --token or GITLAB_TOKEN environment variable.")
        return

    # Handle list-standards option
    if args.list_standards:
        print("Available Standards:")
        for code, std_name in STANDARD_CODES.items():
            std = STANDARDS[std_name]
            print(f"\nCode: {code}")
            print(f"Category: {std['category']}")
            print(f"Severity: {std['severity']}")
            print(f"Description: {std['description']}")
        return

    # Filter standards based on include/exclude options
    filtered_standards = STANDARDS.copy()
    if args.include:
        filtered_standards = {std_name: std for std_name, std in STANDARDS.items() 
                            if std['code'] in args.include}
    elif args.exclude:
        filtered_standards = {std_name: std for std_name, std in STANDARDS.items() 
                            if std['code'] not in args.exclude}

    # Create checker and run checks
    checker = GitLabChecker(gitlab_url=url, private_token=token)
    results = checker.check_standards(args.project_id, output_format=args.format, standards=filtered_standards)
    
    if args.format == FORMAT_JSON:
        print(json.dumps(results, indent=2))
    else:
        print(results)