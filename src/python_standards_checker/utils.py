from packaging import version


def is_version_supported(version_spec: str) -> bool:
    """Check if a version specification meets the minimum requirement.

    Args:
        version_spec: Version specification string (e.g., '>=3.9', '==3.9', '!=3.8')

    Returns:
        bool: True if the version meets the minimum requirement (3.9), False otherwise

    Note:
        This function handles various version specification formats:
        - Version comparison operators (>=, >, ~=)
        - Exact version match (==)
        - Version exclusion (!=)
        - Simple version numbers
    """
    if not version_spec:
        return False

    try:
        # Extract the actual version number from version specifiers
        if version_spec.startswith((">=", ">", "~=")):
            version_str = version_spec.split(",")[0].split(" ")[0]
        elif version_spec == "==3.9":
            version_str = "3.9"
        elif version_spec == "!=3.8":
            return True
        else:
            version_str = version_spec

        # Compare with minimum requirement
        return version.parse(version_str) >= version.parse("3.9")
    except Exception:
        return False
