"""Form and modal SVG element builders."""

from typing import Optional, List, Dict
from .config import WireframeConfig


def render_form_field(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    label: str,
    height: int = 32,
    is_textarea: bool = False,
    placeholder_lines: int = 1
) -> str:
    """Render a form field with label.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of field
        label: Field label
        height: Height of input (larger for textarea)
        is_textarea: Whether this is a multi-line textarea
        placeholder_lines: Number of placeholder lines for textarea
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 8
    label_height = 16
    
    field_height = height if not is_textarea else height
    
    elements = [f"""
    <text x="{x}" y="{y + 10}" font-family="{config.font_family}" font-size="{config.font_size_body}" font-weight="500" fill="{c.text_secondary}">{label}</text>
    <rect x="{x}" y="{y + label_height}" width="{width}" height="{field_height}" rx="{r}" fill="{c.surface_secondary}" stroke="{c.border_light}"/>
    """]
    
    # Placeholder content
    if is_textarea:
        line_y = y + label_height + 13
        widths = [1.0, 0.8, 0.6][:placeholder_lines]
        for w in widths:
            elements.append(f"""
    <rect x="{x + 13}" y="{line_y}" width="{int((width - 26) * w)}" height="6" rx="3" fill="{c.skeleton_primary}"/>
            """)
            line_y += 12
    else:
        elements.append(f"""
    <rect x="{x + 13}" y="{y + label_height + (field_height - 8) // 2}" width="{int(width * 0.4)}" height="8" rx="4" fill="{c.skeleton_primary}"/>
        """)
    
    return f"""
  <g class="form-field">
    {''.join(elements)}
  </g>
    """


def render_submit_button(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    text: str = "Submit",
    height: int = 32
) -> str:
    """Render a submit button.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of button
        text: Button text
        height: Height of button
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 8
    
    return f"""
  <g class="submit-button">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.text_primary}"/>
    <text x="{x + width // 2}" y="{y + height // 2 + 5}" font-family="{config.font_family}" font-size="11" font-weight="600" fill="white" text-anchor="middle">{text}</text>
  </g>
    """


def render_modal(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    height: int,
    title: str = "Modal Title",
    fields: Optional[List[Dict[str, str]]] = None,
    submit_text: str = "Submit"
) -> str:
    """Render a modal dialog with form fields.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of modal
        height: Height of modal
        title: Modal title
        fields: List of field dicts with 'label' and optional 'textarea' bool
        submit_text: Text for submit button
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 20
    header_height = 48
    padding = 25
    
    elements = []
    
    # Modal container
    elements.append(f"""
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_primary}"/>
    """)
    
    # Header
    elements.append(f"""
    <rect x="{x}" y="{y}" width="{width}" height="{header_height}" rx="{r}" fill="{c.surface_secondary}"/>
    <rect x="{x}" y="{y + header_height - r}" width="{width}" height="{r}" fill="{c.surface_secondary}"/>
    <line x1="{x}" y1="{y + header_height}" x2="{x + width}" y2="{y + header_height}" stroke="{c.border_light}" stroke-width="1"/>
    <text x="{x + padding}" y="{y + 30}" font-family="{config.font_family}" font-size="{config.font_size_title}" font-weight="600" fill="{c.text_primary}">{title}</text>
    
    <!-- Close button -->
    <circle cx="{x + width - 30}" cy="{y + header_height // 2}" r="12" fill="{c.skeleton_primary}"/>
    <text x="{x + width - 30}" y="{y + header_height // 2 + 4}" font-family="{config.font_family}" font-size="12" fill="{c.text_tertiary}" text-anchor="middle">×</text>
    """)
    
    # Form fields
    content_y = y + header_height + padding
    field_width = width - 2 * padding
    
    if fields:
        for field in fields:
            label = field.get('label', 'Field')
            is_textarea = field.get('textarea', False)
            field_height = 50 if is_textarea else 32
            
            elements.append(render_form_field(
                config,
                x + padding,
                content_y,
                field_width,
                label,
                height=field_height,
                is_textarea=is_textarea,
                placeholder_lines=3 if is_textarea else 1
            ))
            
            content_y += field_height + 24
    
    # Submit button
    button_y = y + height - padding - 32
    elements.append(render_submit_button(
        config,
        x + padding,
        button_y,
        field_width,
        submit_text
    ))
    
    return f"""
  <g class="modal" filter="url(#modalShadow)">
    {''.join(elements)}
  </g>
    """


def render_modal_overlay(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    height: int,
    opacity: float = 0.25
) -> str:
    """Render modal backdrop overlay.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of overlay
        height: Height of overlay
        opacity: Opacity of overlay
        
    Returns:
        SVG rect element
    """
    c = config.colors
    
    return f"""
  <rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{c.text_primary}" opacity="{opacity}"/>
    """
