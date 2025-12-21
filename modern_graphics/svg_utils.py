"""SVG.js integration utilities for Modern Graphics Generator"""

from typing import Optional, List, Dict, Any


def generate_svg_container(container_id: str, width: int, height: int, style: Optional[str] = None) -> str:
    """
    Generate HTML container for SVG.js.
    
    Args:
        container_id: Unique ID for the container element
        width: Container width in pixels
        height: Container height in pixels
        style: Optional additional CSS styles
    
    Returns:
        HTML string with div container
    """
    style_attr = f' style="{style}"' if style else ''
    return f'<div id="{container_id}" style="width: {width}px; height: {height}px;"{style_attr}></div>'


def generate_svg_init_script(
    container_id: str,
    width: int,
    height: int,
    custom_script: Optional[str] = None,
    global_var_name: str = "draw"
) -> str:
    """
    Generate SVG.js initialization script.
    
    Args:
        container_id: ID of the container element
        width: SVG width in pixels
        height: SVG height in pixels
        custom_script: Optional JavaScript code to execute after initialization
        global_var_name: Name of global variable to store SVG instance (default: 'draw')
    
    Returns:
        JavaScript code string wrapped in <script> tags
    """
    custom_code = f"\n        {custom_script}" if custom_script else ""
    
    return f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const {global_var_name} = SVG().addTo('#{container_id}').size({width}, {height});
        window.{global_var_name} = {global_var_name}; // Make available globally{custom_code}
    }});
    </script>
    """


def create_svg_circle(x: float, y: float, radius: float, fill: str, stroke: Optional[str] = None, stroke_width: Optional[float] = None) -> str:
    """
    Generate SVG.js code to create a circle.
    
    Args:
        x: X coordinate of center
        y: Y coordinate of center
        radius: Circle radius
        fill: Fill color
        stroke: Optional stroke color
        stroke_width: Optional stroke width
    
    Returns:
        JavaScript code string to create circle
    """
    code = f'draw.circle({radius}).move({x - radius}, {y - radius}).fill("{fill}")'
    if stroke:
        code += f'.stroke({{color: "{stroke}"'
        if stroke_width:
            code += f', width: {stroke_width}'
        code += '})'
    return code


def create_svg_rect(x: float, y: float, width: float, height: float, fill: str, rx: Optional[float] = None, stroke: Optional[str] = None) -> str:
    """
    Generate SVG.js code to create a rectangle.
    
    Args:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Rectangle width
        height: Rectangle height
        fill: Fill color
        rx: Optional border radius for rounded corners
        stroke: Optional stroke color
    
    Returns:
        JavaScript code string to create rectangle
    """
    code = f'draw.rect({width}, {height}).move({x}, {y}).fill("{fill}")'
    if rx:
        code += f'.radius({rx})'
    if stroke:
        code += f'.stroke({{color: "{stroke}"}})'
    return code


def create_svg_line(x1: float, y1: float, x2: float, y2: float, stroke: str, stroke_width: float = 2) -> str:
    """
    Generate SVG.js code to create a line.
    
    Args:
        x1: X coordinate of start point
        y1: Y coordinate of start point
        x2: X coordinate of end point
        y2: Y coordinate of end point
        stroke: Stroke color
        stroke_width: Stroke width
    
    Returns:
        JavaScript code string to create line
    """
    return f'draw.line({x1}, {y1}, {x2}, {y2}).stroke({{color: "{stroke}", width: {stroke_width}}})'


def create_svg_path(path_data: str, fill: Optional[str] = None, stroke: Optional[str] = None, stroke_width: Optional[float] = None) -> str:
    """
    Generate SVG.js code to create a path.
    
    Args:
        path_data: SVG path data string (e.g., "M 10 10 L 20 20")
        fill: Optional fill color
        stroke: Optional stroke color
        stroke_width: Optional stroke width
    
    Returns:
        JavaScript code string to create path
    """
    code = f'draw.path("{path_data}")'
    if fill:
        code += f'.fill("{fill}")'
    if stroke:
        stroke_attr = f'{{color: "{stroke}"'
        if stroke_width:
            stroke_attr += f', width: {stroke_width}'
        stroke_attr += '}'
        code += f'.stroke({stroke_attr})'
    return code


def create_svg_text(x: float, y: float, text: str, font_size: Optional[int] = None, fill: Optional[str] = None, font_family: Optional[str] = None) -> str:
    """
    Generate SVG.js code to create text.
    
    Args:
        x: X coordinate
        y: Y coordinate
        text: Text content
        font_size: Optional font size in pixels
        fill: Optional text color
        font_family: Optional font family
    
    Returns:
        JavaScript code string to create text
    """
    # Escape quotes in text
    escaped_text = text.replace('"', '\\"').replace("'", "\\'")
    code = f'draw.text("{escaped_text}").move({x}, {y})'
    if font_size:
        code += f'.font({{size: {font_size}}}'
        if font_family:
            code += f', family: "{font_family}"'
        code += ')'
    elif font_family:
        code += f'.font({{family: "{font_family}"}})'
    if fill:
        code += f'.fill("{fill}")'
    return code


def create_svg_group(elements: List[str], transform: Optional[str] = None) -> str:
    """
    Generate SVG.js code to create a group containing multiple elements.
    
    Args:
        elements: List of JavaScript code strings for SVG elements
        transform: Optional transform string (e.g., "translate(10, 20)")
    
    Returns:
        JavaScript code string to create group
    """
    code = 'const group = draw.group()'
    if transform:
        code += f'.transform({transform})'
    for element_code in elements:
        # Extract the element creation part (everything after 'draw.')
        if 'draw.' in element_code:
            element_part = element_code.split('draw.', 1)[1]
            code += f'\n    group.{element_part}'
        else:
            code += f'\n    {element_code}'
    return code


def generate_svg_js_cdn_script() -> str:
    """
    Generate script tag to include SVG.js from CDN.
    
    Returns:
        HTML script tag string
    """
    return '<script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js@3.2.0"></script>'


def generate_complete_svg_example(container_id: str, width: int, height: int, elements: List[str]) -> str:
    """
    Generate complete HTML/JavaScript example with SVG.js.
    
    Args:
        container_id: ID for the container
        width: SVG width
        height: SVG height
        elements: List of JavaScript code strings for SVG elements
    
    Returns:
        Complete HTML string with container and initialization script
    """
    container = generate_svg_container(container_id, width, height)
    elements_code = '\n        '.join(elements)
    script = generate_svg_init_script(container_id, width, height, elements_code)
    return f"{container}\n{script}"
