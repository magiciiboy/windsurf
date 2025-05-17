from .base import BaseStandard
from .python_version import PythonVersion
from .pyproject_toml import PyprojectToml
from .makefile import Makefile
from .no_conda import NoConda
from .lock_file import LockFile

# List of all standards
STANDARDS = [
    PythonVersion,
    PyprojectToml,
    Makefile,
    NoConda,
    LockFile
]

__all__ = [
    "BaseStandard",
    "PythonVersion",
    "PyprojectToml",
    "Makefile",
    "NoConda",
    "LockFile",
    "STANDARDS"
]
