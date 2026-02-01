"""Chat panel SVG element builders."""

from typing import Optional, List, Dict, Any
from .config import WireframeConfig
from .cards import render_inline_preview_card


def render_chat_message(
    config: WireframeConfig,
    x: int,
    y: int,
    text: str,
    is_user: bool = False,
    max_width: int = 165
) -> str:
    """Render a chat message bubble.
    
    Args:
        config: Wireframe configuration
        x: X position (left edge for system, right edge for user)
        y: Y position
        text: Message text
        is_user: Whether this is a user message (blue) or system (gray)
        max_width: Maximum bubble width
        
    Returns:
        SVG group element
    """
    c = config.colors
    
    # Estimate text width (rough approximation)
    text_width = min(len(text) * 5.5, max_width - 20)
    bubble_width = text_width + 24
    bubble_height = 28
    r = 14
    
    if is_user:
        # User message - right aligned, blue
        bubble_x = x - bubble_width
        fill = "url(#accentGrad)"
        text_fill = "white"
        border_radius = f"rx=\"{r}\" ry=\"{r}\""
    else:
        # System message - left aligned, gray
        bubble_x = x
        fill = c.surface_secondary
        text_fill = c.text_secondary
        border_radius = f"rx=\"{r}\" ry=\"{r}\""
    
    return f"""
  <g class="chat-message">
    <rect x="{bubble_x}" y="{y}" width="{bubble_width}" height="{bubble_height}" {border_radius} fill="{fill}"/>
    <text x="{bubble_x + 12}" y="{y + 18}" font-family="{config.font_family}" font-size="{config.font_size_label}" font-weight="500" fill="{text_fill}">{text}</text>
  </g>
    """


def render_action_buttons(
    config: WireframeConfig,
    x: int,
    y: int,
    buttons: List[Dict[str, Any]]
) -> str:
    """Render action buttons (primary and secondary styles).
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        buttons: List of button dicts with 'text' and optional 'primary' bool
        
    Returns:
        SVG group element
    """
    c = config.colors
    elements = []
    current_x = x
    
    for btn in buttons:
        text = btn.get('text', 'Button')
        is_primary = btn.get('primary', False)
        
        # Estimate button width
        btn_width = len(text) * 6 + 24
        btn_height = 26
        r = 13
        
        if is_primary:
            fill = "url(#accentGrad)"
            text_fill = "white"
            stroke = ""
        else:
            fill = c.surface_primary
            text_fill = c.text_primary
            stroke = f'stroke="{c.border_light}"'
        
        elements.append(f"""
    <rect x="{current_x}" y="{y}" width="{btn_width}" height="{btn_height}" rx="{r}" fill="{fill}" {stroke}/>
    <text x="{current_x + btn_width // 2}" y="{y + 17}" font-family="{config.font_family}" font-size="{config.font_size_label}" font-weight="600" fill="{text_fill}" text-anchor="middle">{text}</text>
        """)
        
        current_x += btn_width + 8
    
    return f"""
  <g class="action-buttons">
    {''.join(elements)}
  </g>
    """


def render_quick_actions(
    config: WireframeConfig,
    x: int,
    y: int,
    actions: List[str]
) -> str:
    """Render quick action links with chevron icons.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        actions: List of action text strings
        
    Returns:
        SVG group element
    """
    c = config.colors
    elements = []
    current_y = y
    
    # Label
    elements.append(f"""
    <text x="{x}" y="{current_y}" font-family="{config.font_family}" font-size="8" font-weight="600" fill="{c.text_tertiary}" letter-spacing="0.5">QUICK ACTIONS</text>
    """)
    current_y += 16
    
    for action in actions:
        elements.append(f"""
    <g fill="{c.accent_blue}">
      <polygon points="{x},{current_y - 4} {x + 5},{current_y} {x},{current_y + 4}"/>
      <text x="{x + 11}" y="{current_y + 3}" font-family="{config.font_family}" font-size="{config.font_size_label}" font-weight="500">{action}</text>
    </g>
        """)
        current_y += 18
    
    return f"""
  <g class="quick-actions">
    {''.join(elements)}
  </g>
    """


def render_chat_input(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    placeholder: str = "Type a message..."
) -> str:
    """Render chat input field.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of input
        placeholder: Placeholder text
        
    Returns:
        SVG group element
    """
    c = config.colors
    height = 28
    r = 8
    
    return f"""
  <g class="chat-input">
    <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{r}" fill="{c.surface_secondary}"/>
    <text x="{x + 15}" y="{y + 18}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_placeholder}">{placeholder}</text>
  </g>
    """


def render_chat_panel(
    config: WireframeConfig,
    x: int,
    y: int,
    width: int,
    height: int,
    messages: Optional[List[Dict[str, Any]]] = None,
    inline_card: Optional[Dict[str, Any]] = None,
    action_buttons: Optional[List[Dict[str, Any]]] = None,
    quick_actions: Optional[List[str]] = None,
    header_title: str = "Help",
    show_active_status: bool = True
) -> str:
    """Render complete chat panel with messages, cards, and actions.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width of panel
        height: Height of panel
        messages: List of message dicts with 'text' and 'is_user' keys
        inline_card: Optional inline card config dict
        action_buttons: Optional list of button configs
        quick_actions: Optional list of quick action strings
        header_title: Panel header title
        show_active_status: Whether to show active indicator
        
    Returns:
        SVG group element
    """
    c = config.colors
    padding = 16
    header_height = 44
    input_height = 44
    
    elements = []
    
    # Panel background
    elements.append(f"""
    <rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{c.surface_primary}"/>
    <line x1="{x}" y1="{y}" x2="{x}" y2="{y + height}" stroke="{c.border_light}" stroke-width="1"/>
    """)
    
    # Header
    elements.append(f"""
    <text x="{x + padding}" y="{y + 28}" font-family="{config.font_family}" font-size="13" font-weight="600" fill="{c.text_primary}">{header_title}</text>
    """)
    
    if show_active_status:
        elements.append(f"""
    <circle cx="{x + width - 35}" cy="{y + 22}" r="4" fill="{c.accent_green}"/>
    <text x="{x + width - 25}" y="{y + 26}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}">Active</text>
        """)
    
    elements.append(f"""
    <line x1="{x}" y1="{y + header_height}" x2="{x + width}" y2="{y + header_height}" stroke="{c.border_light}" stroke-width="1"/>
    """)
    
    # Messages area
    content_y = y + header_height + padding
    
    if messages:
        for msg in messages:
            is_user = msg.get('is_user', False)
            text = msg.get('text', '')
            msg_x = x + width - padding if is_user else x + padding
            elements.append(render_chat_message(config, msg_x, content_y, text, is_user))
            content_y += 40
    
    # Inline card
    if inline_card:
        elements.append(render_inline_preview_card(
            config,
            x + padding,
            content_y,
            width=width - 2 * padding - 10,
            **inline_card
        ))
        content_y += 95
    
    # Action buttons
    if action_buttons:
        elements.append(render_action_buttons(config, x + padding, content_y, action_buttons))
        content_y += 38
    
    # Quick actions
    if quick_actions:
        elements.append(render_quick_actions(config, x + padding, content_y, quick_actions))
    
    # Input area
    input_y = y + height - input_height
    elements.append(f"""
    <line x1="{x}" y1="{input_y}" x2="{x + width}" y2="{input_y}" stroke="{c.border_light}" stroke-width="1"/>
    """)
    elements.append(render_chat_input(config, x + padding, input_y + 8, width - 2 * padding))
    
    return f"""
  <g class="chat-panel">
    {''.join(elements)}
  </g>
    """


# Alias for backwards compatibility
def render_inline_card(
    config: WireframeConfig,
    x: int,
    y: int,
    **kwargs
) -> str:
    """Alias for render_inline_preview_card."""
    return render_inline_preview_card(config, x, y, **kwargs)
