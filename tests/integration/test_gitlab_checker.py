import os
import json
import pytest
from src.gitlab_checker import GitLabChecker

# Add your test GitLab project ID here
TEST_PROJECT_ID = "your-test-project-id"

@pytest.fixture
def gitlab_checker():
    """Create a GitLabChecker instance using test environment variables."""
    token = os.getenv("GITLAB_TEST_TOKEN")
    url = os.getenv("GITLAB_TEST_URL", "https://gitlab.com")
    if not token:
        pytest.skip("GITLAB_TEST_TOKEN environment variable not set")
    return GitLabChecker(gitlab_url=url, private_token=token)

def test_check_standards(gitlab_checker):
    """Test checking standards on a test project."""
    try:
        standards = gitlab_checker.check_standards(TEST_PROJECT_ID)
        assert isinstance(standards, dict)
        assert "python_version" in standards
        assert "pyproject_toml" in standards
        
        python_version = standards["python_version"]
        assert isinstance(python_version, dict)
        assert "standard" in python_version
        assert "meets_standard" in python_version
        assert "detected_version" in python_version
        
        pyproject_toml = standards["pyproject_toml"]
        assert isinstance(pyproject_toml, dict)
        assert "standard" in pyproject_toml
        assert "meets_standard" in pyproject_toml
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")

def test_get_repository_files(gitlab_checker):
    """Test getting repository files."""
    try:
        files = gitlab_checker.get_repository_files(TEST_PROJECT_ID)
        assert isinstance(files, list)
        assert len(files) > 0
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")
