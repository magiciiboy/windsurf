import argparse
import json
import os
import re
from typing import Dict, List, Optional
import gitlab
from gitlab.v4.objects import Project
import pytoml
from packaging import version

class GitLabChecker:
    def __init__(self, gitlab_url: Optional[str] = None, private_token: Optional[str] = None):
        self.gitlab_url = gitlab_url or os.getenv("GITLAB_URL", "https://gitlab.com")
        self.gl = gitlab.Gitlab(self.gitlab_url, private_token=private_token)

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

        # Check shell scripts
        for file in files:
            if file.endswith(".sh"):
                content = self.gl.projects.get(project_id).files.get(
                    file_path=file, ref="main"
                ).decode()
                match = re.search(r'python(3\.\d+)', content)
                if match:
                    return match.group(1)

        return None

    def is_version_supported(self, version_spec: str) -> bool:
        """Check if a version specification meets the minimum requirement."""
        # Extract version number from specifiers like ~=3.12, >=3.9, etc.
        match = re.search(r'[~>=<]*([0-9]+\.[0-9]+)', version_spec)
        if not match:
            return False
            
        version_number = match.group(1)
        try:
            return version.parse(version_number) >= version.parse("3.9")
        except:
            return False

    def check_standards(self, project_id: str) -> Dict:
        """Check repository against defined standards."""
        files = self.get_repository_files(project_id)
        python_version = self.get_python_version(project_id)
        
        standards = {
            "python_version": {
                "standard": ">=3.9",
                "meets_standard": python_version and self.is_version_supported(python_version),
                "detected_version": python_version
            },
            "pyproject_toml": {
                "standard": "required",
                "meets_standard": "pyproject.toml" in files
            }
        }
        
        return standards

def main():
    parser = argparse.ArgumentParser(description="Check GitLab repository against Python standards")
    parser.add_argument("project_id", help="GitLab project ID or URL")
    parser.add_argument("--token", help="GitLab private token")
    parser.add_argument("--url", help="GitLab instance URL")
    
    args = parser.parse_args()

    # Get token from environment variable if not provided as argument
    token = args.token or os.getenv("GITLAB_TOKEN")
    url = args.url or os.getenv("GITLAB_URL")
    
    if not token:
        print("Error: GitLab token is required. Please provide it via --token or GITLAB_TOKEN environment variable.")
        return

    checker = GitLabChecker(gitlab_url=url, private_token=token)
    
    try:
        standards = checker.check_standards(args.project_id)
        print(json.dumps(standards, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
