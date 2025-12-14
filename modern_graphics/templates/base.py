"""Base template class for styling graphics"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class StyleTemplate:
    """Base template for styling graphics"""
    name: str
    colors: Dict[str, Dict[str, any]]  # Color palette: {"blue": {"gradient": (...), "shadow": "..."}}
    base_styles: str  # Base CSS styles
    attribution_styles: str  # Attribution CSS styles
    font_family: str  # Font stack
    background_color: str  # Default background color
    
    def get_color(self, color_key: str) -> Dict[str, any]:
        """Get color definition by key, fallback to gray"""
        return self.colors.get(color_key, self.colors.get('gray', {}))
    
    def get_gradient(self, color_key: str) -> tuple:
        """Get gradient tuple for a color"""
        color = self.get_color(color_key)
        return color.get("gradient", ("#F5F5F7", "#F5F5F7"))
    
    def get_shadow(self, color_key: str) -> str:
        """Get shadow color for a color"""
        color = self.get_color(color_key)
        return color.get("shadow", "rgba(0, 0, 0, 0.08)")
