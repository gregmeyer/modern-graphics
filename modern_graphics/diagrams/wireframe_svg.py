"""Pure SVG wireframe generators for embedding in other graphics.

These functions return SVG strings (not HTML) that can be embedded
in heroes, insight cards, or other compositions.
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


@dataclass
class WireframeSVGConfig:
    """Configuration for SVG wireframe generation."""
    width: int = 400
    height: int = 300
    corner_radius: int = 16
    accent_color: str = "#0071e3"
    success_color: str = "#34c759"
    error_color: str = "#ff3b30"
    text_primary: str = "#1d1d1f"
    text_secondary: str = "#6e6e73"
    text_tertiary: str = "#86868b"
    surface_1: str = "#ffffff"
    surface_2: str = "#f5f5f7"
    surface_3: str = "#e8e8ed"
    border_color: str = "#e8e8ed"
    font_family: str = "Inter, -apple-system, sans-serif"
    # Browser chrome colors (traffic light dots)
    chrome_dot_color: str = "#d2d2d7"
    # For dark themes, use accent colors for chrome dots
    chrome_dot_red: Optional[str] = None
    chrome_dot_yellow: Optional[str] = None
    chrome_dot_green: Optional[str] = None
    # Button colors (for proper contrast)
    button_bg: Optional[str] = None      # Button background (defaults to text_primary or accent)
    button_text: Optional[str] = None    # Button text (defaults to white or contrasting)
    
    @classmethod
    def from_color_scheme(cls, scheme: "ColorScheme", **kwargs) -> "WireframeSVGConfig":
        """Create config from a ColorScheme."""
        # Detect if dark theme based on background color
        bg = scheme.bg_primary.lstrip('#')
        is_dark = sum(int(bg[i:i+2], 16) for i in (0, 2, 4)) < 384
        
        if is_dark:
            # Use accent colors for traffic lights on dark themes
            chrome_dot_red = scheme.error or "#ff5f56"
            chrome_dot_yellow = scheme.warning or "#ffbd2e"
            chrome_dot_green = scheme.success or "#27c93f"
            # Use accent/primary for buttons on dark themes
            button_bg = scheme.primary
            button_text = "#000000" if _is_light_color(scheme.primary) else "#ffffff"
        else:
            chrome_dot_red = None
            chrome_dot_yellow = None
            chrome_dot_green = None
            button_bg = None  # Will default to text_primary
            button_text = None  # Will default to white
        
        return cls(
            accent_color=scheme.primary,
            success_color=scheme.success or "#34c759",
            error_color=scheme.error or "#ff3b30",
            font_family=scheme.font_family,
            chrome_dot_red=chrome_dot_red,
            chrome_dot_yellow=chrome_dot_yellow,
            chrome_dot_green=chrome_dot_green,
            button_bg=button_bg,
            button_text=button_text,
            **kwargs
        )


def _is_light_color(hex_color: str) -> bool:
    """Check if a color is light (for contrast calculations)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # Using relative luminance formula
    luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    return luminance > 128


def _get_defs(config: WireframeSVGConfig) -> str:
    """Generate common SVG defs (filters, gradients)."""
    return f"""
    <defs>
        <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="6" stdDeviation="12" flood-opacity="0.1"/>
        </filter>
        <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.06"/>
        </filter>
        <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{config.accent_color}"/>
            <stop offset="100%" stop-color="{config.accent_color}"/>
        </linearGradient>
        <linearGradient id="successGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{config.success_color}"/>
            <stop offset="100%" stop-color="{config.success_color}"/>
        </linearGradient>
    </defs>
    """


def generate_chat_panel_svg(
    config: Optional[WireframeSVGConfig] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    inline_card: Optional[Dict[str, Any]] = None,
    action_buttons: Optional[List[str]] = None,
    success_toast: Optional[Dict[str, str]] = None,
    header_title: str = "Help",
    show_status_dot: bool = True,
) -> str:
    """Generate a chat panel wireframe as pure SVG.
    
    Args:
        config: SVG configuration
        messages: List of message dicts with 'role' ('user'/'assistant') and 'text'
        inline_card: Dict with 'title', 'subtitle', 'progress' (0-100), 'status'
        action_buttons: List of button labels
        success_toast: Dict with 'title' and optional 'subtitle'
        header_title: Chat panel header title
        show_status_dot: Show green status dot in header
        
    Returns:
        SVG string
    """
    config = config or WireframeSVGConfig()
    w, h = config.width, config.height
    
    elements = [_get_defs(config)]
    
    # Background
    elements.append(f'''
        <rect x="0" y="0" width="{w}" height="{h}" fill="{config.surface_2}" rx="{config.corner_radius}"/>
    ''')
    
    # Chat panel container
    panel_margin = 16
    panel_w = w - panel_margin * 2
    panel_h = h - panel_margin * 2
    elements.append(f'''
        <rect x="{panel_margin}" y="{panel_margin}" width="{panel_w}" height="{panel_h}" 
              rx="{config.corner_radius - 2}" fill="{config.surface_1}" filter="url(#cardShadow)"/>
    ''')
    
    # Header
    header_h = 40
    elements.append(f'''
        <text x="{panel_margin + 16}" y="{panel_margin + 26}" 
              font-family="{config.font_family}" font-size="13" font-weight="600" 
              fill="{config.text_primary}">{header_title}</text>
    ''')
    if show_status_dot:
        elements.append(f'''
            <circle cx="{w - panel_margin - 20}" cy="{panel_margin + 20}" r="4" fill="{config.success_color}"/>
        ''')
    elements.append(f'''
        <line x1="{panel_margin}" y1="{panel_margin + header_h}" 
              x2="{w - panel_margin}" y2="{panel_margin + header_h}" 
              stroke="{config.border_color}" stroke-width="1"/>
    ''')
    
    # Messages
    y_offset = panel_margin + header_h + 16
    messages = messages or [
        {"role": "user", "text": "I need help"},
        {"role": "assistant", "text": "I can help with that."}
    ]
    
    for msg in messages:
        if msg["role"] == "user":
            text_w = min(len(msg["text"]) * 7, panel_w - 60)
            elements.append(f'''
                <rect x="{w - panel_margin - 16 - text_w}" y="{y_offset}" 
                      width="{text_w}" height="28" rx="14" fill="url(#accentGrad)"/>
                <text x="{w - panel_margin - 16 - text_w + 14}" y="{y_offset + 18}" 
                      font-family="{config.font_family}" font-size="11" fill="white">{msg["text"][:30]}</text>
            ''')
        else:
            text_w = min(len(msg["text"]) * 6.5, panel_w - 60)
            elements.append(f'''
                <rect x="{panel_margin + 16}" y="{y_offset}" 
                      width="{text_w}" height="24" rx="12" fill="{config.surface_2}"/>
                <text x="{panel_margin + 28}" y="{y_offset + 16}" 
                      font-family="{config.font_family}" font-size="10" fill="{config.text_secondary}">{msg["text"][:40]}</text>
            ''')
        y_offset += 36
    
    # Inline card
    if inline_card:
        card_y = y_offset + 8
        card_h = 70
        card_w = panel_w - 40
        elements.append(f'''
            <rect x="{panel_margin + 20}" y="{card_y}" width="{card_w}" height="{card_h}" 
                  rx="12" fill="{config.surface_1}" stroke="{config.border_color}" filter="url(#softShadow)"/>
            <text x="{panel_margin + 36}" y="{card_y + 22}" 
                  font-family="{config.font_family}" font-size="11" font-weight="600" 
                  fill="{config.text_primary}">{inline_card.get("title", "Plan")}</text>
        ''')
        
        if inline_card.get("status"):
            status_w = 56
            elements.append(f'''
                <rect x="{panel_margin + 20 + card_w - status_w - 12}" y="{card_y + 10}" 
                      width="{status_w}" height="20" rx="10" fill="rgba(52,199,89,0.12)"/>
                <text x="{panel_margin + 20 + card_w - status_w}" y="{card_y + 24}" 
                      font-family="{config.font_family}" font-size="9" font-weight="600" 
                      fill="{config.success_color}">{inline_card.get("status", "Active")}</text>
            ''')
        
        if inline_card.get("subtitle"):
            elements.append(f'''
                <text x="{panel_margin + 36}" y="{card_y + 40}" 
                      font-family="{config.font_family}" font-size="11" fill="{config.text_primary}">
                    {inline_card.get("subtitle", "")}
                </text>
            ''')
        
        if inline_card.get("progress") is not None:
            progress = inline_card.get("progress", 75)
            bar_w = card_w - 32
            elements.append(f'''
                <rect x="{panel_margin + 36}" y="{card_y + 50}" width="{bar_w}" height="5" rx="2.5" fill="{config.surface_3}"/>
                <rect x="{panel_margin + 36}" y="{card_y + 50}" width="{bar_w * progress / 100}" height="5" rx="2.5" fill="url(#accentGrad)"/>
            ''')
        
        y_offset = card_y + card_h + 12
    
    # Action buttons
    if action_buttons:
        btn_x = panel_margin + 20
        for i, label in enumerate(action_buttons[:2]):
            btn_w = 72
            if i == 0:
                elements.append(f'''
                    <rect x="{btn_x}" y="{y_offset}" width="{btn_w}" height="28" rx="14" fill="url(#accentGrad)"/>
                    <text x="{btn_x + 12}" y="{y_offset + 18}" 
                          font-family="{config.font_family}" font-size="11" font-weight="600" fill="white">{label}</text>
                ''')
            else:
                elements.append(f'''
                    <rect x="{btn_x}" y="{y_offset}" width="{btn_w}" height="28" rx="14" 
                          fill="{config.surface_1}" stroke="{config.border_color}"/>
                    <text x="{btn_x + 14}" y="{y_offset + 18}" 
                          font-family="{config.font_family}" font-size="11" fill="{config.text_secondary}">{label}</text>
                ''')
            btn_x += btn_w + 10
    
    # Success toast
    if success_toast:
        toast_w = 160
        toast_h = 44
        toast_x = panel_margin + 20
        toast_y = h - panel_margin - toast_h - 16
        elements.append(f'''
            <rect x="{toast_x}" y="{toast_y}" width="{toast_w}" height="{toast_h}" 
                  rx="12" fill="{config.surface_1}" filter="url(#cardShadow)"/>
            <circle cx="{toast_x + 22}" cy="{toast_y + toast_h/2}" r="14" fill="rgba(52,199,89,0.1)"/>
            <path d="M{toast_x + 16} {toast_y + toast_h/2} L{toast_x + 20} {toast_y + toast_h/2 + 4} L{toast_x + 28} {toast_y + toast_h/2 - 4}" 
                  stroke="{config.success_color}" stroke-width="2" fill="none" stroke-linecap="round"/>
            <text x="{toast_x + 44}" y="{toast_y + 18}" 
                  font-family="{config.font_family}" font-size="10" font-weight="600" 
                  fill="{config.text_primary}">{success_toast.get("title", "Done")}</text>
        ''')
        if success_toast.get("subtitle"):
            elements.append(f'''
                <text x="{toast_x + 44}" y="{toast_y + 32}" 
                      font-family="{config.font_family}" font-size="9" fill="{config.text_tertiary}">
                    {success_toast.get("subtitle", "")}
                </text>
            ''')
    
    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        {"".join(elements)}
    </svg>'''


def generate_modal_form_svg(
    config: Optional[WireframeSVGConfig] = None,
    title: str = "Support Request",
    fields: Optional[List[str]] = None,
    submit_label: str = "Submit",
    show_overlay: bool = True,
) -> str:
    """Generate a modal form wireframe as pure SVG.
    
    Args:
        config: SVG configuration
        title: Modal title
        fields: List of field labels
        submit_label: Submit button text
        show_overlay: Show dimmed overlay behind modal
        
    Returns:
        SVG string
    """
    config = config or WireframeSVGConfig()
    w, h = config.width, config.height
    
    elements = [_get_defs(config)]
    
    # Browser chrome background
    elements.append(f'''
        <rect x="0" y="0" width="{w}" height="{h}" fill="{config.surface_1}" rx="{config.corner_radius}"/>
        <rect x="0" y="0" width="{w}" height="32" rx="{config.corner_radius}" fill="{config.surface_2}"/>
        <rect x="0" y="16" width="{w}" height="16" fill="{config.surface_2}"/>
    ''')
    
    # Traffic lights
    elements.append(f'''
        <circle cx="18" cy="16" r="5" fill="#d2d2d7"/>
        <circle cx="34" cy="16" r="5" fill="#d2d2d7"/>
        <circle cx="50" cy="16" r="5" fill="#d2d2d7"/>
    ''')
    
    # URL bar
    elements.append(f'''
        <rect x="70" y="8" width="120" height="16" rx="4" fill="{config.surface_1}" stroke="{config.border_color}"/>
    ''')
    
    # Content area
    elements.append(f'''
        <rect x="0" y="32" width="{w}" height="{h - 32}" fill="{config.surface_2}"/>
    ''')
    
    # Overlay
    if show_overlay:
        elements.append(f'''
            <rect x="0" y="32" width="{w}" height="{h - 32}" fill="rgba(29,29,31,0.25)"/>
        ''')
    
    # Modal
    modal_w = min(280, w - 60)
    modal_h = 160
    modal_x = (w - modal_w) / 2
    modal_y = (h - modal_h) / 2 + 16
    
    elements.append(f'''
        <rect x="{modal_x}" y="{modal_y}" width="{modal_w}" height="{modal_h}" 
              rx="16" fill="{config.surface_1}" filter="url(#cardShadow)"/>
        <rect x="{modal_x}" y="{modal_y}" width="{modal_w}" height="36" rx="16" fill="{config.surface_2}"/>
        <rect x="{modal_x}" y="{modal_y + 20}" width="{modal_w}" height="16" fill="{config.surface_2}"/>
        <text x="{modal_x + 20}" y="{modal_y + 24}" 
              font-family="{config.font_family}" font-size="12" font-weight="600" 
              fill="{config.text_primary}">{title}</text>
    ''')
    
    # Fields
    fields = fields or ["Email", "Description"]
    field_y = modal_y + 52
    for field in fields[:3]:
        elements.append(f'''
            <text x="{modal_x + 20}" y="{field_y}" 
                  font-family="{config.font_family}" font-size="9" fill="{config.text_tertiary}">{field}</text>
            <rect x="{modal_x + 20}" y="{field_y + 4}" width="{modal_w - 40}" height="24" 
                  rx="6" fill="{config.surface_2}" stroke="{config.border_color}"/>
        ''')
        field_y += 40
    
    # Submit button
    btn_y = modal_y + modal_h - 44
    btn_bg = config.button_bg or config.text_primary
    btn_text = config.button_text or "white"
    elements.append(f'''
        <rect x="{modal_x + 20}" y="{btn_y}" width="{modal_w - 40}" height="32" 
              rx="8" fill="{btn_bg}"/>
        <text x="{modal_x + modal_w/2}" y="{btn_y + 21}" text-anchor="middle"
              font-family="{config.font_family}" font-size="12" font-weight="600" fill="{btn_text}">{submit_label}</text>
    ''')
    
    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        {"".join(elements)}
    </svg>'''


def generate_ticket_flow_svg(
    config: Optional[WireframeSVGConfig] = None,
    statuses: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Generate a ticket status flow wireframe as pure SVG.
    
    Args:
        config: SVG configuration
        statuses: List of status dicts with 'label' and 'state' ('done', 'active', 'pending')
        
    Returns:
        SVG string
    """
    config = config or WireframeSVGConfig()
    w, h = config.width, 80
    
    elements = [_get_defs(config)]
    
    # Background card
    elements.append(f'''
        <rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{config.surface_1}" filter="url(#cardShadow)"/>
    ''')
    
    statuses = statuses or [
        {"label": "Open", "state": "done"},
        {"label": "In Progress", "state": "active"},
        {"label": "Resolved", "state": "pending"},
    ]
    
    # Label
    elements.append(f'''
        <text x="20" y="24" font-family="{config.font_family}" font-size="9" font-weight="600" 
              fill="{config.text_tertiary}" letter-spacing="0.05em">TICKET STATUS</text>
    ''')
    
    # Status pills
    pill_x = 20
    pill_y = 38
    for status in statuses:
        state = status.get("state", "pending")
        label = status.get("label", "")
        pill_w = len(label) * 7 + 24
        
        if state == "done":
            fill = config.surface_3
            text_color = config.text_secondary
        elif state == "active":
            fill = f"rgba({_hex_to_rgb(config.accent_color)}, 0.15)"
            text_color = config.accent_color
        else:
            fill = config.surface_2
            text_color = config.text_tertiary
        
        elements.append(f'''
            <rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="26" rx="13" fill="{fill}"/>
            <text x="{pill_x + 12}" y="{pill_y + 17}" 
                  font-family="{config.font_family}" font-size="10" font-weight="600" 
                  fill="{text_color}">{label}</text>
        ''')
        
        pill_x += pill_w + 12
    
    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        {"".join(elements)}
    </svg>'''


def generate_before_wireframe_svg(
    config: Optional[WireframeSVGConfig] = None,
    show_modal: bool = True,
    show_ticket_status: bool = True,
) -> str:
    """Generate a complete 'before' wireframe (modal form + ticket flow).
    
    Args:
        config: SVG configuration
        show_modal: Include the modal form
        show_ticket_status: Include the ticket status bar
        
    Returns:
        SVG string
    """
    config = config or WireframeSVGConfig(width=400, height=320)
    w, h = config.width, config.height
    
    elements = [_get_defs(config)]
    
    # Browser chrome dot colors
    dot_red = config.chrome_dot_red or config.chrome_dot_color
    dot_yellow = config.chrome_dot_yellow or config.chrome_dot_color
    dot_green = config.chrome_dot_green or config.chrome_dot_color
    
    # Browser frame
    elements.append(f'''
        <rect x="0" y="0" width="{w}" height="{h}" fill="{config.surface_1}" rx="{config.corner_radius}"/>
        <rect x="0" y="0" width="{w}" height="32" rx="{config.corner_radius}" fill="{config.surface_2}"/>
        <rect x="0" y="16" width="{w}" height="16" fill="{config.surface_2}"/>
        <circle cx="18" cy="16" r="5" fill="{dot_red}"/>
        <circle cx="34" cy="16" r="5" fill="{dot_yellow}"/>
        <circle cx="50" cy="16" r="5" fill="{dot_green}"/>
        <rect x="70" y="8" width="120" height="16" rx="4" fill="{config.surface_1}" stroke="{config.border_color}"/>
    ''')
    
    # Content area with background page content
    overlay_color = "rgba(29,29,31,0.4)" if config.surface_1.lower() in ["#ffffff", "#fff", "white"] else f"rgba(0,0,0,0.5)"
    elements.append(f'''
        <rect x="0" y="32" width="{w}" height="{h - 32}" fill="{config.surface_2}"/>
    ''')
    
    # Background page content (visible behind overlay)
    elements.append(f'''
        <rect x="16" y="48" width="{w - 32}" height="40" rx="8" fill="{config.surface_1}" stroke="{config.border_color}"/>
        <text x="28" y="72" font-family="{config.font_family}" font-size="11" font-weight="600" fill="{config.text_primary}">My Account</text>
        <rect x="16" y="100" width="{w - 32}" height="100" rx="8" fill="{config.surface_1}" stroke="{config.border_color}"/>
        <text x="28" y="122" font-family="{config.font_family}" font-size="10" font-weight="600" fill="{config.text_primary}">Subscription</text>
        <rect x="28" y="132" width="140" height="8" rx="4" fill="{config.surface_3}"/>
        <rect x="28" y="148" width="100" height="8" rx="4" fill="{config.surface_3}"/>
        <rect x="28" y="164" width="120" height="8" rx="4" fill="{config.surface_3}"/>
    ''')
    
    # Overlay (dims the background when modal is open)
    elements.append(f'''
        <rect x="0" y="32" width="{w}" height="{h - 32 - 60}" fill="{overlay_color}"/>
    ''')
    
    # Modal
    if show_modal:
        modal_w = 220
        modal_h = 150
        modal_x = (w - modal_w) / 2
        modal_y = 55
        
        elements.append(f'''
            <rect x="{modal_x}" y="{modal_y}" width="{modal_w}" height="{modal_h}" 
                  rx="14" fill="{config.surface_1}" stroke="{config.border_color}" filter="url(#cardShadow)"/>
            <rect x="{modal_x}" y="{modal_y}" width="{modal_w}" height="32" rx="14" fill="{config.surface_2}"/>
            <rect x="{modal_x}" y="{modal_y + 18}" width="{modal_w}" height="14" fill="{config.surface_2}"/>
            <text x="{modal_x + 16}" y="{modal_y + 22}" 
                  font-family="{config.font_family}" font-size="11" font-weight="600" 
                  fill="{config.text_primary}">Support Request</text>
            <text x="{modal_x + 16}" y="{modal_y + 42}" 
                  font-family="{config.font_family}" font-size="8" font-weight="600" 
                  fill="{config.text_tertiary}">Subject</text>
            <rect x="{modal_x + 16}" y="{modal_y + 46}" width="{modal_w - 32}" height="22" 
                  rx="5" fill="{config.surface_2}" stroke="{config.border_color}"/>
            <text x="{modal_x + 24}" y="{modal_y + 61}" 
                  font-family="{config.font_family}" font-size="9" fill="{config.text_tertiary}">Billing issue...</text>
            <text x="{modal_x + 16}" y="{modal_y + 78}" 
                  font-family="{config.font_family}" font-size="8" font-weight="600" 
                  fill="{config.text_tertiary}">Description</text>
            <rect x="{modal_x + 16}" y="{modal_y + 82}" width="{modal_w - 32}" height="22" 
                  rx="5" fill="{config.surface_2}" stroke="{config.border_color}"/>
            <text x="{modal_x + 24}" y="{modal_y + 97}" 
                  font-family="{config.font_family}" font-size="9" fill="{config.text_tertiary}">Please describe...</text>
            <rect x="{modal_x + 16}" y="{modal_y + 112}" width="{modal_w - 32}" height="22" 
                  rx="6" fill="{config.button_bg or config.text_primary}"/>
            <text x="{modal_x + modal_w/2}" y="{modal_y + 127}" text-anchor="middle"
                  font-family="{config.font_family}" font-size="10" font-weight="600" fill="{config.button_text or 'white'}">Submit Ticket</text>
        ''')
    
    # Ticket status
    if show_ticket_status:
        status_y = h - 52
        elements.append(f'''
            <rect x="40" y="{status_y}" width="{w - 80}" height="44" rx="12" fill="{config.surface_1}" stroke="{config.border_color}" filter="url(#softShadow)"/>
            <text x="56" y="{status_y + 14}" font-family="{config.font_family}" font-size="8" font-weight="600" 
                  fill="{config.text_tertiary}" letter-spacing="0.05em">TICKET STATUS</text>
            <rect x="56" y="{status_y + 22}" width="44" height="16" rx="8" fill="{config.surface_3}" stroke="{config.border_color}"/>
            <text x="66" y="{status_y + 33}" font-family="{config.font_family}" font-size="8" font-weight="600" fill="{config.text_secondary}">Open</text>
            <rect x="108" y="{status_y + 22}" width="60" height="16" rx="8" fill="rgba({_hex_to_rgb(config.accent_color)}, 0.25)"/>
            <text x="114" y="{status_y + 33}" font-family="{config.font_family}" font-size="8" font-weight="600" fill="{config.accent_color}">Pending</text>
            <rect x="176" y="{status_y + 22}" width="52" height="16" rx="8" fill="{config.surface_2}" stroke="{config.border_color}"/>
            <text x="182" y="{status_y + 33}" font-family="{config.font_family}" font-size="8" font-weight="600" fill="{config.text_tertiary}">Closed</text>
        ''')
    
    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        {"".join(elements)}
    </svg>'''


def generate_after_wireframe_svg(
    config: Optional[WireframeSVGConfig] = None,
    show_chat_panel: bool = True,
    show_inline_card: bool = True,
    show_success_toast: bool = True,
) -> str:
    """Generate a complete 'after' wireframe (app with chat panel).
    
    Args:
        config: SVG configuration
        show_chat_panel: Include the chat panel
        show_inline_card: Include the inline action card in chat
        show_success_toast: Include the success toast
        
    Returns:
        SVG string
    """
    config = config or WireframeSVGConfig(width=400, height=320)
    w, h = config.width, config.height
    
    elements = [_get_defs(config)]
    
    # Browser chrome dot colors
    dot_red = config.chrome_dot_red or config.chrome_dot_color
    dot_yellow = config.chrome_dot_yellow or config.chrome_dot_color
    dot_green = config.chrome_dot_green or config.chrome_dot_color
    
    # Browser frame
    elements.append(f'''
        <rect x="0" y="0" width="{w}" height="{h}" fill="{config.surface_1}" rx="{config.corner_radius}"/>
        <rect x="0" y="0" width="{w}" height="32" rx="{config.corner_radius}" fill="{config.surface_2}"/>
        <rect x="0" y="16" width="{w}" height="16" fill="{config.surface_2}"/>
        <circle cx="18" cy="16" r="5" fill="{dot_red}"/>
        <circle cx="34" cy="16" r="5" fill="{dot_yellow}"/>
        <circle cx="50" cy="16" r="5" fill="{dot_green}"/>
        <rect x="70" y="8" width="120" height="16" rx="4" fill="{config.surface_1}" stroke="{config.border_color}"/>
    ''')
    
    # Main content area
    main_w = w - 160
    elements.append(f'''
        <rect x="0" y="32" width="{main_w}" height="{h - 32}" fill="{config.surface_2}"/>
        <rect x="16" y="48" width="{main_w - 32}" height="48" rx="10" fill="{config.surface_1}" stroke="{config.border_color}" filter="url(#softShadow)"/>
        <text x="28" y="68" font-family="{config.font_family}" font-size="10" font-weight="600" fill="{config.text_primary}">Dashboard</text>
        <rect x="28" y="76" width="80" height="8" rx="4" fill="{config.surface_3}"/>
        <rect x="16" y="108" width="{main_w - 32}" height="72" rx="10" fill="{config.surface_1}" stroke="{config.border_color}" filter="url(#softShadow)"/>
        <text x="28" y="128" font-family="{config.font_family}" font-size="10" font-weight="600" fill="{config.text_primary}">Recent Activity</text>
        <rect x="28" y="136" width="120" height="6" rx="3" fill="{config.surface_3}"/>
        <rect x="28" y="148" width="100" height="6" rx="3" fill="{config.surface_3}"/>
        <rect x="28" y="160" width="90" height="6" rx="3" fill="{config.surface_3}"/>
    ''')
    
    # Chat panel
    if show_chat_panel:
        chat_x = main_w
        chat_w = 160
        elements.append(f'''
            <rect x="{chat_x}" y="32" width="{chat_w}" height="{h - 32}" fill="{config.surface_1}"/>
            <line x1="{chat_x}" y1="32" x2="{chat_x}" y2="{h}" stroke="{config.border_color}"/>
            <text x="{chat_x + 16}" y="54" font-family="{config.font_family}" font-size="12" font-weight="600" 
                  fill="{config.text_primary}">Help</text>
            <circle cx="{w - 20}" cy="48" r="4" fill="{config.success_color}"/>
            <line x1="{chat_x}" y1="68" x2="{w}" y2="68" stroke="{config.border_color}"/>
        ''')
        
        # User message
        elements.append(f'''
            <rect x="{chat_x + 50}" y="80" width="96" height="24" rx="12" fill="url(#accentGrad)"/>
            <text x="{chat_x + 62}" y="96" font-family="{config.font_family}" font-size="10" fill="white">Update my card</text>
        ''')
        
        # Assistant message
        elements.append(f'''
            <rect x="{chat_x + 12}" y="112" width="100" height="20" rx="10" fill="{config.surface_2}"/>
            <text x="{chat_x + 22}" y="126" font-family="{config.font_family}" font-size="9" 
                  fill="{config.text_secondary}">Here's your plan:</text>
        ''')
        
        # Inline card
        if show_inline_card:
            card_y = 140
            # Get success color RGB for transparent background
            success_rgb = _hex_to_rgb(config.success_color)
            elements.append(f'''
                <rect x="{chat_x + 12}" y="{card_y}" width="136" height="60" rx="10" 
                      fill="{config.surface_1}" stroke="{config.border_color}" filter="url(#softShadow)"/>
                <text x="{chat_x + 22}" y="{card_y + 18}" font-family="{config.font_family}" font-size="10" 
                      font-weight="600" fill="{config.text_primary}">Pro Plan</text>
                <rect x="{chat_x + 100}" y="{card_y + 8}" width="40" height="16" rx="8" fill="rgba({success_rgb}, 0.2)"/>
                <text x="{chat_x + 108}" y="{card_y + 20}" font-family="{config.font_family}" font-size="8" 
                      font-weight="600" fill="{config.success_color}">Active</text>
                <rect x="{chat_x + 22}" y="{card_y + 30}" width="116" height="5" rx="2.5" fill="{config.surface_3}"/>
                <rect x="{chat_x + 22}" y="{card_y + 30}" width="87" height="5" rx="2.5" fill="url(#accentGrad)"/>
                <text x="{chat_x + 22}" y="{card_y + 52}" font-family="{config.font_family}" font-size="8" 
                      fill="{config.text_tertiary}">18 days remaining</text>
            ''')
        
        # Action buttons
        elements.append(f'''
            <rect x="{chat_x + 12}" y="210" width="64" height="24" rx="12" fill="url(#accentGrad)"/>
            <text x="{chat_x + 24}" y="226" font-family="{config.font_family}" font-size="10" 
                  font-weight="600" fill="white">Update</text>
            <rect x="{chat_x + 84}" y="210" width="56" height="24" rx="12" fill="{config.surface_1}" stroke="{config.border_color}"/>
            <text x="{chat_x + 96}" y="226" font-family="{config.font_family}" font-size="10" 
                  fill="{config.text_secondary}">Cancel</text>
        ''')
    
    # Success toast
    if show_success_toast:
        toast_x = 16
        toast_y = h - 60
        elements.append(f'''
            <rect x="{toast_x}" y="{toast_y}" width="156" height="44" rx="12" fill="{config.surface_1}" filter="url(#cardShadow)"/>
            <circle cx="{toast_x + 24}" cy="{toast_y + 22}" r="14" fill="rgba(52,199,89,0.1)"/>
            <path d="M{toast_x + 18} {toast_y + 22} L{toast_x + 22} {toast_y + 26} L{toast_x + 30} {toast_y + 18}" 
                  stroke="{config.success_color}" stroke-width="2" fill="none" stroke-linecap="round"/>
            <text x="{toast_x + 46}" y="{toast_y + 18}" font-family="{config.font_family}" font-size="10" 
                  font-weight="600" fill="{config.text_primary}">Card updated</text>
            <text x="{toast_x + 46}" y="{toast_y + 32}" font-family="{config.font_family}" font-size="9" 
                  fill="{config.text_tertiary}">Action completed</text>
        ''')
    
    return f'''<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        {"".join(elements)}
    </svg>'''


def _hex_to_rgb(hex_color: str) -> str:
    """Convert hex color to RGB string for rgba()."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r}, {g}, {b}"
