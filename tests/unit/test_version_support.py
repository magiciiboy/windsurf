import pytest
from python_standards_checker.utils import is_version_supported

@pytest.mark.parametrize(
    "version_spec, expected",
    [
        # Version specifiers that should be supported
        (">=3.9", True),
        (">3.9", True),
        ("~=3.9", True),
        ("~=3.10", True),
        ("^3.9", True),
        (">=3.10", True),
        ("==3.9", True),
        ("!=3.8", True),
        ("~=3.12", True),
        ("3.9", True),  # Just the version number
        
        # Version specifiers that should not be supported
        ("~=3.8", False),
        ("<3.9", False),
        ("<=3.9", False),
        ("==3.8", False),
        (">=3.8", False),
        ("<3.8", False),
        ("<=3.8", False),
        ("!=3.9", False),
        ("3.8", False),  # Just the version number
        
        # Invalid version specifiers
        ("invalid", False),
        ("python3.9", False),
        ("", False),
        (None, False)
    ]
)
def test_is_version_supported(version_spec, expected):
    """Test the is_version_supported function with various version specifications."""
    result = is_version_supported(version_spec)
    assert result == expected, f"Expected {expected} for version spec: {version_spec}"
