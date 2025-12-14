"""Utility functions for Modern Graphics generators"""

from typing import Optional
from .models import StepStyle
from .templates import StyleTemplate, DEFAULT_TEMPLATE


def generate_step_style(
    style: Optional[StepStyle] = None,
    color_key: Optional[str] = None,
    template: Optional[StyleTemplate] = None
) -> str:
    """Generate CSS for a step/box using template colors"""
    template = template or DEFAULT_TEMPLATE
    
    if style and style.background_gradient:
        grad_start, grad_end = style.background_gradient
        bg = f"linear-gradient(135deg, {grad_start} 0%, {grad_end} 100%)"
    elif color_key:
        grad_start, grad_end = template.get_gradient(color_key)
        bg = f"linear-gradient(135deg, {grad_start} 0%, {grad_end} 100%)"
    else:
        grad_start, grad_end = template.get_gradient('gray')
        bg = f"linear-gradient(135deg, {grad_start} 0%, {grad_end} 100%)"
    
    if style and style.shadow_color:
        shadow = style.shadow_color
    elif color_key:
        shadow = template.get_shadow(color_key)
    else:
        shadow = template.get_shadow('gray')
    
    return f"""
            background: {bg};
            box-shadow: 0 2px 8px {shadow}, 0 8px 24px {shadow.replace('0.12', '0.08') if '0.12' in shadow else shadow};
        """
