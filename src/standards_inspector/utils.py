import re
from typing import Optional
from packaging import version


def is_version_supported(version_spec: str, min_version: str) -> bool:
    """Check if a version specification meets the minimum requirement.

    Args:
        version_spec: Version specification string (e.g., '3.9' or '3.11')
        min_version: Minimum version string (e.g., '3.9')

    Returns:
        bool: True if the version meets the minimum requirement (3.9), False otherwise

    Note:
        This function handles various version specification formats:
        - Version comparison operators (>=, >, ~=)
        - Exact version match (==)
        - Version exclusion (!=)
        - Simple version numbers
    """
    if not version_spec or not min_version:
        raise ValueError("Version specification and minimum version must be provided")

    return version.parse(version_spec) >= version.parse(min_version)


def get_min_version(version: str) -> Optional[str]:
    """Get the minimum version from a version specification."""
    if not version:
        raise ValueError("Version specification must be provided")

    # If there is no sign < or ! in the version spec,
    # extract the version major and minor number only without signs ~=, ==, >=, >
    # For example, from ~=3.9 extract 3.9
    if "<" not in version and "!" not in version:
        v = re.search(r"(\d+(\.\d+)?)", version)
        if v:
            return v.group(1)
    return None
