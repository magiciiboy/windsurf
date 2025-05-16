import os
import json
import pytest
from gitlab_checker import GitLabChecker

@pytest.fixture
def gitlab_checker():
    """Create a GitLabChecker instance using test environment variables."""
    token = os.getenv("GITLAB_TEST_TOKEN") or os.getenv("GITLAB_TOKEN")
    url = os.getenv("GITLAB_TEST_URL") or os.getenv("GITLAB_URL", "https://gitlab.com")
    if not token:
        pytest.skip("GITLAB_TEST_TOKEN or GITLAB_TOKEN environment variable not set")
    return GitLabChecker(gitlab_url=url, private_token=token)

@pytest.fixture
def test_project_id():
    """Get test project ID from environment variables."""
    return os.getenv("GITLAB_TEST_PROJECT_ID") or os.getenv("GITLAB_PROJECT_ID")

def test_check_standards(gitlab_checker, test_project_id):
    """Test checking standards on a test project."""
    if not test_project_id:
        pytest.skip("GITLAB_TEST_PROJECT_ID or GITLAB_PROJECT_ID environment variable not set")
    
    try:
        standards = gitlab_checker.check_standards(test_project_id)
        assert isinstance(standards, dict)
        assert "python_version" in standards
        assert "pyproject_toml" in standards
        
        python_version = standards["python_version"]
        assert isinstance(python_version, dict)
        assert "standard" in python_version
        assert "meets_standard" in python_version
        assert "detected_version" in python_version
        
        # Test various Python version specifications
        version_specifications = [
            (">=3.9", True),
            (">3.9", True),
            ("~=3.9", True),
            ("~=3.10", True),
            ("~=3.8", False),
            ("<3.9", False),
            ("<=3.9", False),
            ("==3.9", True),
            ("!=3.8", True),
            ("^3.9", True),
            (">=3.10", True),
            (">=3.8", False)
        ]
        
        for spec, expected in version_specifications:
            python_version["detected_version"] = spec
            # Use the public function for testing
            meets_standard = checker.is_version_supported(spec)
            assert meets_standard == expected
        
        pyproject_toml = standards["pyproject_toml"]
        assert isinstance(pyproject_toml, dict)
        assert "standard" in pyproject_toml
        assert "meets_standard" in pyproject_toml
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")

def test_get_repository_files(gitlab_checker, test_project_id):
    """Test getting repository files."""
    if not test_project_id:
        pytest.skip("GITLAB_TEST_PROJECT_ID or GITLAB_PROJECT_ID environment variable not set")
    
    try:
        files = gitlab_checker.get_repository_files(test_project_id)
        assert isinstance(files, list)
        assert len(files) > 0
    except Exception as e:
        pytest.fail(f"Unexpected error: {str(e)}")
