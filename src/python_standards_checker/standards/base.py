from abc import ABC, abstractmethod
from typing import Dict, Optional
from packaging import version


class BaseStandard(ABC):
    """Base class for all Python standards."""
    
    # Static attributes that must be defined by subclasses
    code: str = ""
    category: str = ""
    standard: str = ""
    severity: str = ""
    description: str = ""
    recommendation: str = ""
    standard_type: str = ""

    @classmethod
    @abstractmethod
    def check(cls, project_id: str, checker: 'GitLabChecker') -> dict:
        """Check if the standard is met.
        
        Args:
            project_id: GitLab project ID
            checker: GitLabChecker instance
            
        Returns:
            Dict containing:
            - meets_standard: bool
            - detected_version: str (if applicable)
        """
        pass

    @classmethod
    def is_version_supported(cls, version_spec: str) -> bool:
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
