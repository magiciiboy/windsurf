from .base import BaseStandard
from .python_version import PythonVersion
from .project_spec import ProjectSpec
from .makefile import Makefile
from .no_conda import NoConda
from .lock_file import LockFile

# List of all standards
STANDARDS = [
    PythonVersion,
    ProjectSpec,
    Makefile,
    NoConda,
    LockFile
]

__all__ = [
    "BaseStandard",
    "PythonVersion",
    "ProjectSpec",
    "Makefile",
    "NoConda",
    "LockFile",
    "STANDARDS"
]
