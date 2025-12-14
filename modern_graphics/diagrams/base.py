"""Base class for diagram generators"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..base import BaseGenerator


class DiagramGenerator(ABC):
    """Base class for diagram generators"""
    
    @abstractmethod
    def generate(self, generator: BaseGenerator, **kwargs) -> str:
        """Generate diagram HTML
        
        Args:
            generator: BaseGenerator instance with template and attribution
            **kwargs: Diagram-specific parameters
            
        Returns:
            HTML string for the diagram
        """
        pass
    
    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters
        
        Args:
            **kwargs: Diagram-specific parameters
            
        Returns:
            True if input is valid, False otherwise
        """
        pass
