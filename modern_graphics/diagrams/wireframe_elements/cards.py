"""Content card and skeleton SVG element builders."""

from typing import Optional, List
from .config import WireframeConfig


def render_skeleton_lines(
    config: WireframeConfig,
    x: int,
    y: int,
    widths: List[float],
    line_height: int = 8,
    gap: int = 10
) -> str:
    """Render skeleton placeholder lines.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        widths: List of line widths as percentages (0-1) or absolute pixels (>1)
        line_height: Height of each line
        gap: Gap between lines
        
    Returns:
        SVG group with skeleton lines
    """
    c = config.colors
    lines = []
    current_y = y
    
    for width in widths:
        # If width > 1, treat as absolute pixels, otherwise as percentage of 200px
        w = width if width > 1 else int(width * 200)
        lines.append(
            f'<rect x="{x}" y="{current_y}" width="{w}" height="{line_height}" rx="{line_height // 2}" fill="{c.skeleton_secondary}"/>'
        )
        current_y += line_height + gap
    
    return f"""
  <g class="skeleton-lines">
    {''.join(lines)}
  </g>
    """


def render_app_header(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    height: int = 45
) -> str:
    """Render app header bar with logo and nav placeholders.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of header
        height: Height of header
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 12  # Border radius
    
    return f"""
  <g class="app-header" filter="url(#softShadow)">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_primary}"/>
    
    <!-- Logo placeholder -->
    <rect x="{x + 15}" y="{y + (height - 24) // 2}" width="24" height="24" rx="6" fill="{c.skeleton_primary}"/>
    <rect x="{x + 47}" y="{y + (height - 8) // 2}" width="70" height="8" rx="4" fill="{c.skeleton_primary}"/>
    
    <!-- Nav items (right side) -->
    <rect x="{x + width - 100}" y="{y + (height - 8) // 2}" width="50" height="8" rx="4" fill="{c.skeleton_primary}"/>
    <circle cx="{x + width - 25}" cy="{y + height // 2}" r="10" fill="{c.skeleton_primary}"/>
  </g>
    """


def render_content_card(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    height: int,
    line_widths: Optional[List[float]] = None,
    show_divider: bool = False,
    opacity: float = 1.0
) -> str:
    """Render content placeholder card with skeleton lines.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of card
        height: Height of card
        line_widths: Optional list of line widths (defaults to standard pattern)
        show_divider: Whether to show a divider line
        opacity: Opacity of the card (for dimming effect)
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 12  # Border radius
    padding = 20
    
    # Default line pattern
    if line_widths is None:
        line_widths = [0.8, 1.0, 0.9, 0.6]
    
    lines = render_skeleton_lines(
        config,
        x + padding,
        y + padding,
        line_widths,
        line_height=8,
        gap=10
    )
    
    divider = ""
    extra_lines = ""
    if show_divider:
        divider_y = y + height - 45
        divider = f'<line x1="{x + padding}" y1="{divider_y}" x2="{x + width - padding}" y2="{divider_y}" stroke="{c.skeleton_secondary}" stroke-width="1"/>'
        extra_lines = render_skeleton_lines(
            config,
            x + padding,
            divider_y + 12,
            [0.5, 0.7],
            line_height=8,
            gap=8
        )
    
    opacity_attr = f'opacity="{opacity}"' if opacity < 1.0 else ""
    
    return f"""
  <g class="content-card" filter="url(#softShadow)" {opacity_attr}>
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_primary}"/>
    {lines}
    {divider}
    {extra_lines}
  </g>
    """


def render_inline_preview_card(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int = 175,
    height: int = 85,
    title: str = "Pro Plan",
    subtitle: str = "$29/mo",
    detail: str = "Visa •••• 4242",
    progress: float = 0.75,
    footer: str = "Renews Dec 15"
) -> str:
    """Render inline preview card (e.g., for billing info in chat).
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of card
        height: Height of card
        title: Card title
        subtitle: Subtitle (e.g., price)
        detail: Detail line
        progress: Progress bar value (0-1)
        footer: Footer text
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 12
    padding = 16
    
    progress_width = int((width - 2 * padding - 20) * progress)
    
    return f"""
  <g class="inline-card" filter="url(#softShadow)">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_tertiary}" stroke="{c.border_light}"/>
    
    <!-- Title row -->
    <text x="{x + padding}" y="{y + 20}" font-family="{config.font_family}" font-size="{config.font_size_body}" font-weight="600" fill="{c.text_primary}">{title}</text>
    <text x="{x + width - padding}" y="{y + 20}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}" text-anchor="end">{subtitle}</text>
    
    <!-- Detail -->
    <text x="{x + padding}" y="{y + 38}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_secondary}">{detail}</text>
    
    <!-- Progress bar -->
    <rect x="{x + padding}" y="{y + 49}" width="{width - 2 * padding - 10}" height="6" rx="3" fill="{c.skeleton_primary}"/>
    <rect x="{x + padding}" y="{y + 49}" width="{progress_width}" height="6" rx="3" fill="url(#accentGrad)"/>
    
    <!-- Footer -->
    <text x="{x + padding}" y="{y + 71}" font-family="{config.font_family}" font-size="8" fill="{c.text_tertiary}">{footer}</text>
  </g>
    """
