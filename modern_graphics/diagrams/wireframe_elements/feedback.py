"""Feedback and status SVG element builders."""

from typing import Optional, List, Literal
from .config import WireframeConfig


def render_success_toast(
    config: WireframeConfig,
    x: int,
    y: int,
    title: str = "Success",
    subtitle: Optional[str] = None,
    width: int = 260,
    height: int = 56
) -> str:
    """Render a success toast notification.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        title: Toast title
        subtitle: Optional subtitle
        width: Width of toast
        height: Height of toast
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 14
    icon_r = 18
    
    # Checkmark path
    check_path = f"M{x + 24} {y + height // 2} L{x + 30} {y + height // 2 + 6} L{x + 42} {y + height // 2 - 6}"
    
    subtitle_el = ""
    if subtitle:
        subtitle_el = f"""
    <text x="{x + 60}" y="{y + height // 2 + 12}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}">{subtitle}</text>
        """
        title_y = y + height // 2 - 4
    else:
        title_y = y + height // 2 + 4
    
    return f"""
  <g class="success-toast" filter="url(#cardShadow)">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_primary}"/>
    
    <!-- Success icon -->
    <circle cx="{x + 32}" cy="{y + height // 2}" r="{icon_r}" fill="rgba(52, 199, 89, 0.1)"/>
    <path d="{check_path}" stroke="{c.accent_green}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Text -->
    <text x="{x + 60}" y="{title_y}" font-family="{config.font_family}" font-size="11" font-weight="600" fill="{c.text_primary}">{title}</text>
    {subtitle_el}
  </g>
    """


def render_error_toast(
    config: WireframeConfig,
    x: int,
    y: int,
    title: str = "Error",
    subtitle: Optional[str] = None,
    width: int = 260,
    height: int = 56
) -> str:
    """Render an error toast notification.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        title: Toast title
        subtitle: Optional subtitle
        width: Width of toast
        height: Height of toast
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = 14
    icon_r = 18
    
    subtitle_el = ""
    if subtitle:
        subtitle_el = f"""
    <text x="{x + 60}" y="{y + height // 2 + 12}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}">{subtitle}</text>
        """
        title_y = y + height // 2 - 4
    else:
        title_y = y + height // 2 + 4
    
    return f"""
  <g class="error-toast" filter="url(#cardShadow)">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_primary}"/>
    
    <!-- Error icon -->
    <circle cx="{x + 32}" cy="{y + height // 2}" r="{icon_r}" fill="rgba(255, 59, 48, 0.1)"/>
    <line x1="{x + 24}" y1="{y + height // 2 - 8}" x2="{x + 40}" y2="{y + height // 2 + 8}" stroke="{c.accent_red}" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="{x + 40}" y1="{y + height // 2 - 8}" x2="{x + 24}" y2="{y + height // 2 + 8}" stroke="{c.accent_red}" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Text -->
    <text x="{x + 60}" y="{title_y}" font-family="{config.font_family}" font-size="11" font-weight="600" fill="{c.text_primary}">{title}</text>
    {subtitle_el}
  </g>
    """


def render_status_pill(
    config: WireframeConfig,
    x: int,
    y: int,
    text: str,
    status: Literal["positive", "negative", "neutral", "active"] = "neutral",
    icon: bool = True
) -> str:
    """Render a status pill/badge.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        text: Status text
        status: Status type (affects color)
        icon: Whether to show status icon
        
    Returns:
        SVG group element
    """
    c = config.colors
    
    # Color mapping
    color_map = {
        "positive": (c.accent_green, f"rgba(52, 199, 89, 0.08)", f"rgba(52, 199, 89, 0.15)"),
        "negative": (c.accent_red, f"rgba(255, 59, 48, 0.08)", f"rgba(255, 59, 48, 0.15)"),
        "neutral": (c.text_tertiary, c.surface_secondary, c.border_light),
        "active": (c.accent_blue, f"rgba(0, 113, 227, 0.08)", f"rgba(0, 113, 227, 0.15)"),
    }
    
    text_color, bg_color, border_color = color_map.get(status, color_map["neutral"])
    
    # Estimate pill width
    icon_width = 24 if icon else 0
    text_width = len(text) * 6
    pill_width = text_width + icon_width + 24
    pill_height = 28
    r = pill_height // 2
    
    icon_el = ""
    if icon:
        icon_x = x + 12
        icon_y = y + pill_height // 2
        if status == "positive":
            icon_el = f"""
    <circle cx="{icon_x + 7}" cy="{icon_y}" r="7" stroke="{text_color}" stroke-width="1.5" fill="none"/>
    <path d="M{icon_x + 4} {icon_y} L{icon_x + 7} {icon_y + 3} L{icon_x + 11} {icon_y - 3}" stroke="{text_color}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            """
        elif status == "negative":
            icon_el = f"""
    <circle cx="{icon_x + 7}" cy="{icon_y}" r="7" stroke="{text_color}" stroke-width="1.5" fill="none"/>
    <line x1="{icon_x + 7}" y1="{icon_y - 3}" x2="{icon_x + 7}" y2="{icon_y + 1}" stroke="{text_color}" stroke-width="1.5" stroke-linecap="round"/>
    <circle cx="{icon_x + 7}" cy="{icon_y + 4}" r="0.5" fill="{text_color}"/>
            """
        elif status == "active":
            icon_el = f"""
    <circle cx="{icon_x + 7}" cy="{icon_y}" r="4" fill="{text_color}"/>
            """
    
    text_x = x + (icon_width + 12 if icon else 12)
    
    return f"""
  <g class="status-pill">
    <rect x="{x}" y="{y}" width="{pill_width}" height="{pill_height}" rx="{r}" fill="{bg_color}" stroke="{border_color}"/>
    {icon_el}
    <text x="{text_x}" y="{y + pill_height // 2 + 4}" font-family="{config.font_family}" font-size="13" font-weight="600" fill="{text_color}">{text}</text>
  </g>
    """


def render_progress_bar(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    progress: float,
    height: int = 6,
    show_label: bool = False
) -> str:
    """Render a progress bar.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Total width
        progress: Progress value (0-1)
        height: Bar height
        show_label: Whether to show percentage label
        
    Returns:
        SVG group element
    """
    c = config.colors
    r = height // 2
    progress_width = int(width * max(0, min(1, progress)))
    
    label_el = ""
    if show_label:
        label_el = f"""
    <text x="{x + width + 10}" y="{y + height // 2 + 4}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}">{int(progress * 100)}%</text>
        """
    
    return f"""
  <g class="progress-bar">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.skeleton_primary}"/>
    <rect x="{x}" y="{y}" width="{progress_width}" height="{height}" rx="{r}" fill="url(#accentGrad)"/>
    {label_el}
  </g>
    """


def render_ticket_status_flow(
    config: WireframeConfig,
    x: int,
    y: int,
    statuses: Optional[List[str]] = None,
    active_index: int = 1,
    ticket_id: str = "#48291",
    estimated_time: str = "24-48 hours"
) -> str:
    """Render a ticket status flow (Open → In Progress → Resolved).
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        statuses: List of status labels (defaults to Open, In Progress, Resolved)
        active_index: Index of active status (0-based)
        ticket_id: Ticket ID to display
        estimated_time: Estimated response time
        
    Returns:
        SVG group element
    """
    c = config.colors
    
    if statuses is None:
        statuses = ["Open", "In Progress", "Resolved"]
    
    elements = []
    
    # Label
    elements.append(f"""
    <text x="{x}" y="{y}" font-family="{config.font_family}" font-size="9" font-weight="600" fill="{c.text_tertiary}" letter-spacing="1">TICKET STATUS</text>
    """)
    
    # Status pills
    pill_y = y + 15
    current_x = x
    
    for i, status in enumerate(statuses):
        pill_width = len(status) * 7 + 20
        pill_height = 24
        r = 12
        
        if i < active_index:
            # Completed
            fill = c.skeleton_primary
            text_color = c.text_secondary
        elif i == active_index:
            # Active
            fill = f"rgba(0, 113, 227, 0.1)"
            text_color = c.accent_blue
            stroke = f'stroke="rgba(0, 113, 227, 0.2)"'
        else:
            # Pending
            fill = c.surface_secondary
            text_color = c.text_tertiary
            stroke = ""
        
        stroke = stroke if i == active_index else ""
        
        elements.append(f"""
    <rect x="{current_x}" y="{pill_y}" width="{pill_width}" height="{pill_height}" rx="{r}" fill="{fill}" {stroke}/>
    <text x="{current_x + pill_width // 2}" y="{pill_y + pill_height // 2 + 4}" font-family="{config.font_family}" font-size="{config.font_size_label}" font-weight="600" fill="{text_color}" text-anchor="middle">{status}</text>
        """)
        
        current_x += pill_width + 5
        
        # Connector line
        if i < len(statuses) - 1:
            elements.append(f"""
    <line x1="{current_x}" y1="{pill_y + pill_height // 2}" x2="{current_x + 20}" y2="{pill_y + pill_height // 2}" stroke="{c.border_medium}" stroke-width="2"/>
            """)
            current_x += 25
    
    # Ticket info
    elements.append(f"""
    <text x="{x}" y="{pill_y + 45}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}">Ticket {ticket_id} • Estimated response: {estimated_time}</text>
    """)
    
    return f"""
  <g class="ticket-status">
    {''.join(elements)}
  </g>
    """
