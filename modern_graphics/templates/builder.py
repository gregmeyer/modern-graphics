"""Template builder for creating custom style templates"""

from typing import Dict, Optional
from .base import StyleTemplate
from .default import DEFAULT_TEMPLATE


class TemplateBuilder:
    """Builder for creating custom templates"""
    
    def __init__(self, name: str):
        """Initialize template builder
        
        Args:
            name: Unique name for the template
        """
        self.name = name
        self.colors: Dict[str, Dict[str, any]] = {}
        self.base_styles: str = DEFAULT_TEMPLATE.base_styles
        self.attribution_styles: str = DEFAULT_TEMPLATE.attribution_styles
        self.font_family: str = DEFAULT_TEMPLATE.font_family
        self.background_color: str = DEFAULT_TEMPLATE.background_color
    
    def add_color(self, name: str, gradient: tuple, shadow: str) -> 'TemplateBuilder':
        """Add a color to the palette
        
        Args:
            name: Color name (e.g., 'blue', 'green')
            gradient: Tuple of (start_color, end_color) hex codes
            shadow: Shadow color (rgba string)
            
        Returns:
            Self for method chaining
        """
        self.colors[name] = {"gradient": gradient, "shadow": shadow}
        return self
    
    def set_base_styles(self, css: str) -> 'TemplateBuilder':
        """Set base CSS styles
        
        Args:
            css: CSS string for base styles
            
        Returns:
            Self for method chaining
        """
        self.base_styles = css
        return self
    
    def set_attribution_styles(self, css: str) -> 'TemplateBuilder':
        """Set attribution CSS styles
        
        Args:
            css: CSS string for attribution styles
            
        Returns:
            Self for method chaining
        """
        self.attribution_styles = css
        return self
    
    def set_font_family(self, font_stack: str) -> 'TemplateBuilder':
        """Set font family
        
        Args:
            font_stack: CSS font-family value
            
        Returns:
            Self for method chaining
        """
        self.font_family = font_stack
        return self
    
    def set_background_color(self, color: str) -> 'TemplateBuilder':
        """Set default background color
        
        Args:
            color: Hex color code
            
        Returns:
            Self for method chaining
        """
        self.background_color = color
        return self
    
    def copy_from(self, template: StyleTemplate) -> 'TemplateBuilder':
        """Copy settings from an existing template
        
        Args:
            template: Template to copy from
            
        Returns:
            Self for method chaining
        """
        self.colors = template.colors.copy()
        self.base_styles = template.base_styles
        self.attribution_styles = template.attribution_styles
        self.font_family = template.font_family
        self.background_color = template.background_color
        return self
    
    def build(self) -> StyleTemplate:
        """Build the template
        
        Returns:
            StyleTemplate instance
            
        Raises:
            ValueError: If required fields are missing
        """
        if not self.colors:
            # Copy default colors if none specified
            self.colors = DEFAULT_TEMPLATE.colors.copy()
        
        return StyleTemplate(
            name=self.name,
            colors=self.colors,
            base_styles=self.base_styles,
            attribution_styles=self.attribution_styles,
            font_family=self.font_family,
            background_color=self.background_color
        )
