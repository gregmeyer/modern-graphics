"""Wireframe diagram generator for before/after comparisons and UI mockups.

Provides high-level functions to create Material Design-inspired wireframe
illustrations using composable SVG elements.

Example:
    >>> from modern_graphics import ModernGraphicsGenerator
    >>> generator = ModernGraphicsGenerator("Wireframe Demo")
    >>> html = generator.generate_wireframe_diagram(
    ...     variant="chat-panel",
    ...     title="Inline Chat Support"
    ... )
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING
from html import escape

from .wireframe_elements.config import WireframeConfig, WireframeColors, APPLE_COLORS
from .wireframe_elements.browser import render_browser_window
from .wireframe_elements.cards import render_app_header, render_content_card
from .wireframe_elements.chat import render_chat_panel
from .wireframe_elements.forms import render_modal, render_modal_overlay
from .wireframe_elements.feedback import (
    render_success_toast,
    render_status_pill,
    render_ticket_status_flow
)

if TYPE_CHECKING:
    from ..base import BaseGenerator
    from ..color_scheme import ColorScheme


def generate_wireframe_diagram(
    generator: "BaseGenerator",
    variant: str = "chat-panel",
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    eyebrow: Optional[str] = None,
    config: Optional[WireframeConfig] = None,
    color_scheme: Optional["ColorScheme"] = None,
    # Chat panel options
    chat_messages: Optional[List[Dict[str, Any]]] = None,
    chat_inline_card: Optional[Dict[str, Any]] = None,
    chat_action_buttons: Optional[List[Dict[str, Any]]] = None,
    chat_quick_actions: Optional[List[str]] = None,
    # Modal options
    modal_title: str = "Submit Support Request",
    modal_fields: Optional[List[Dict[str, str]]] = None,
    modal_submit_text: str = "Submit Request",
    # Success toast
    success_toast: Optional[Dict[str, str]] = None,
    # Status
    status: Optional[Dict[str, str]] = None,
    # Ticket status
    ticket_status: Optional[Dict[str, Any]] = None,
    # Layout
    width: int = 600,
    height: int = 520,
) -> str:
    """Generate a wireframe diagram.
    
    Args:
        generator: BaseGenerator instance
        variant: Wireframe variant - "chat-panel", "modal-form", "dashboard"
        title: Diagram title
        subtitle: Diagram subtitle
        eyebrow: Eyebrow text above title
        config: Optional WireframeConfig (created from color_scheme if not provided)
        color_scheme: Optional ColorScheme to derive colors from
        chat_messages: List of chat messages for chat-panel variant
        chat_inline_card: Inline card config for chat-panel
        chat_action_buttons: Action buttons for chat-panel
        chat_quick_actions: Quick action strings for chat-panel
        modal_title: Title for modal-form variant
        modal_fields: Form fields for modal-form variant
        modal_submit_text: Submit button text for modal
        success_toast: Success toast config dict with 'title' and 'subtitle'
        status: Status pill config dict with 'type' and 'text'
        ticket_status: Ticket status flow config
        width: SVG width
        height: SVG height
        
    Returns:
        HTML string with SVG wireframe
    """
    # Create config from color scheme if provided
    if config is None:
        if color_scheme:
            config = WireframeConfig.from_color_scheme(color_scheme, width=width, height=height)
        else:
            config = WireframeConfig(width=width, height=height)
    
    c = config.colors
    
    # Build SVG content based on variant
    if variant == "chat-panel":
        svg_content = _build_chat_panel_wireframe(
            config,
            messages=chat_messages,
            inline_card=chat_inline_card,
            action_buttons=chat_action_buttons,
            quick_actions=chat_quick_actions,
            success_toast=success_toast,
        )
    elif variant == "modal-form":
        svg_content = _build_modal_form_wireframe(
            config,
            modal_title=modal_title,
            modal_fields=modal_fields,
            modal_submit_text=modal_submit_text,
            ticket_status=ticket_status,
        )
    else:
        # Default to basic dashboard
        svg_content = _build_dashboard_wireframe(config)
    
    # Build complete SVG
    svg = f"""
<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" class="wireframe-diagram">
  <defs>
    {config.get_filter_defs()}
  </defs>
  
  {svg_content}
</svg>
    """
    
    # Build HTML wrapper
    title_html = ""
    if title or eyebrow:
        title_html = f"""
    <div class="wireframe-label">
        {f'<div class="eyebrow">{escape(eyebrow)}</div>' if eyebrow else ''}
        {f'<h2>{escape(title)}</h2>' if title else ''}
        {f'<p class="subtitle">{escape(subtitle)}</p>' if subtitle else ''}
    </div>
        """
    
    status_html = ""
    if status:
        status_type = status.get('type', 'neutral')
        status_text = status.get('text', '')
        status_class = f"status-{status_type}"
        icon = _get_status_icon(status_type)
        status_html = f"""
    <div class="wireframe-status {status_class}">
        {icon}
        <span>{escape(status_text)}</span>
    </div>
        """
    
    html_content = f"""
    <div class="wireframe-container">
        {title_html}
        <div class="wireframe-svg">
            {svg}
        </div>
        {status_html}
    </div>
    """
    
    css_content = f"""
        body {{
            background: {c.surface_secondary};
            padding: 60px;
            font-family: {config.font_family};
            -webkit-font-smoothing: antialiased;
        }}
        
        .wireframe-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .wireframe-label {{
            text-align: center;
            margin-bottom: 32px;
        }}
        
        .wireframe-label .eyebrow {{
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {c.text_tertiary};
            margin-bottom: 8px;
        }}
        
        .wireframe-label h2 {{
            font-size: 28px;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: {c.text_primary};
            margin: 0;
        }}
        
        .wireframe-label .subtitle {{
            font-size: 16px;
            color: {c.text_secondary};
            margin: 8px 0 0 0;
        }}
        
        .wireframe-svg {{
            width: {width}px;
        }}
        
        .wireframe-svg svg {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .wireframe-status {{
            margin-top: 32px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            border-radius: 100px;
        }}
        
        .wireframe-status svg {{
            width: 18px;
            height: 18px;
        }}
        
        .wireframe-status span {{
            font-size: 14px;
            font-weight: 600;
            letter-spacing: -0.01em;
        }}
        
        .wireframe-status.status-positive {{
            background: rgba(52, 199, 89, 0.08);
            border: 1px solid rgba(52, 199, 89, 0.15);
        }}
        .wireframe-status.status-positive svg {{ color: {c.accent_green}; }}
        .wireframe-status.status-positive span {{ color: {c.accent_green}; }}
        
        .wireframe-status.status-negative {{
            background: rgba(255, 59, 48, 0.08);
            border: 1px solid rgba(255, 59, 48, 0.15);
        }}
        .wireframe-status.status-negative svg {{ color: {c.accent_red}; }}
        .wireframe-status.status-negative span {{ color: {c.accent_red}; }}
        
        .wireframe-status.status-neutral {{
            background: {c.surface_secondary};
            border: 1px solid {c.border_light};
        }}
        .wireframe-status.status-neutral svg {{ color: {c.text_tertiary}; }}
        .wireframe-status.status-neutral span {{ color: {c.text_secondary}; }}
    """
    
    return generator._wrap_html(html_content, css_content)


def generate_wireframe_comparison(
    generator: "BaseGenerator",
    before: Dict[str, Any],
    after: Dict[str, Any],
    headline: Optional[str] = None,
    subheadline: Optional[str] = None,
    eyebrow: Optional[str] = None,
    insight: Optional[str] = None,
    config: Optional[WireframeConfig] = None,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a before/after wireframe comparison.
    
    Args:
        generator: BaseGenerator instance
        before: Config dict for "before" wireframe with keys:
            - variant: "modal-form", "chat-panel", etc.
            - title: Panel title
            - status: Status dict with 'type' and 'text'
            - (other variant-specific options)
        after: Config dict for "after" wireframe (same structure as before)
        headline: Main headline
        subheadline: Subtitle text
        eyebrow: Eyebrow text
        insight: Key insight text for bottom card
        config: Optional WireframeConfig
        color_scheme: Optional ColorScheme
        
    Returns:
        HTML string with comparison wireframes
    """
    # Create config
    if config is None:
        if color_scheme:
            config = WireframeConfig.from_color_scheme(color_scheme)
        else:
            config = WireframeConfig()
    
    c = config.colors
    
    # Generate before SVG
    before_variant = before.get('variant', 'modal-form')
    before_svg = _build_wireframe_svg(config, before_variant, before)
    
    # Generate after SVG
    after_variant = after.get('variant', 'chat-panel')
    after_svg = _build_wireframe_svg(config, after_variant, after)
    
    # Build comparison HTML
    header_html = ""
    if headline or eyebrow:
        header_html = f"""
    <div class="comparison-header">
        {f'<div class="eyebrow">{escape(eyebrow)}</div>' if eyebrow else ''}
        {f'<h1>{escape(headline)}</h1>' if headline else ''}
        {f'<p>{escape(subheadline)}</p>' if subheadline else ''}
    </div>
        """
    
    before_status = before.get('status', {})
    after_status = after.get('status', {})
    
    insight_html = ""
    if insight:
        insight_html = f"""
    <div class="comparison-insight">
        <div class="insight-card">
            <div class="insight-label">Key Insight</div>
            <p>{insight}</p>
        </div>
    </div>
        """
    
    html_content = f"""
    {header_html}
    
    <div class="comparison-panels">
        <div class="panel">
            <div class="panel-label before">
                <div class="dot"></div>
                <h3>{escape(before.get('title', 'Before'))}</h3>
            </div>
            <div class="wireframe-svg">{before_svg}</div>
            {_render_status_html(before_status, c)}
        </div>
        
        <div class="panel">
            <div class="panel-label after">
                <div class="dot"></div>
                <h3>{escape(after.get('title', 'After'))}</h3>
            </div>
            <div class="wireframe-svg">{after_svg}</div>
            {_render_status_html(after_status, c)}
        </div>
    </div>
    
    {insight_html}
    """
    
    css_content = f"""
        body {{
            background: {c.surface_secondary};
            padding: 60px;
            font-family: {config.font_family};
            -webkit-font-smoothing: antialiased;
        }}
        
        .comparison-header {{
            text-align: center;
            margin-bottom: 48px;
        }}
        
        .comparison-header .eyebrow {{
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: {c.text_tertiary};
            margin-bottom: 12px;
        }}
        
        .comparison-header h1 {{
            font-size: 42px;
            font-weight: 600;
            letter-spacing: -0.025em;
            color: {c.text_primary};
            margin: 0 0 12px 0;
        }}
        
        .comparison-header p {{
            font-size: 18px;
            color: {c.text_secondary};
            margin: 0;
            letter-spacing: -0.01em;
        }}
        
        .comparison-panels {{
            display: flex;
            gap: 40px;
            justify-content: center;
        }}
        
        .panel {{
            flex: 1;
            max-width: 560px;
        }}
        
        .panel-label {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .panel-label .dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        
        .panel-label.before .dot {{ background: {c.text_tertiary}; }}
        .panel-label.after .dot {{ background: {c.accent_blue}; }}
        
        .panel-label h3 {{
            font-size: 15px;
            font-weight: 600;
            color: {c.text_secondary};
            margin: 0;
            letter-spacing: -0.01em;
        }}
        
        .wireframe-svg svg {{
            width: 100%;
            height: auto;
        }}
        
        .status {{
            margin-top: 24px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 18px;
            border-radius: 100px;
        }}
        
        .status svg {{
            width: 16px;
            height: 16px;
        }}
        
        .status span {{
            font-size: 13px;
            font-weight: 600;
            letter-spacing: -0.01em;
        }}
        
        .status.negative {{
            background: rgba(255, 59, 48, 0.08);
            border: 1px solid rgba(255, 59, 48, 0.15);
        }}
        .status.negative svg {{ color: {c.accent_red}; }}
        .status.negative span {{ color: {c.accent_red}; }}
        
        .status.positive {{
            background: rgba(52, 199, 89, 0.08);
            border: 1px solid rgba(52, 199, 89, 0.15);
        }}
        .status.positive svg {{ color: {c.accent_green}; }}
        .status.positive span {{ color: {c.accent_green}; }}
        
        .comparison-insight {{
            margin-top: 48px;
            text-align: center;
        }}
        
        .insight-card {{
            display: inline-block;
            background: {c.surface_primary};
            border-radius: 24px;
            padding: 32px 48px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        }}
        
        .insight-card .insight-label {{
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {c.text_tertiary};
            margin-bottom: 12px;
        }}
        
        .insight-card p {{
            font-size: 17px;
            color: {c.text_primary};
            margin: 0;
            line-height: 1.5;
            letter-spacing: -0.01em;
        }}
    """
    
    return generator._wrap_html(html_content, css_content)


# ============================================================================
# Private helper functions
# ============================================================================

def _build_chat_panel_wireframe(
    config: WireframeConfig,
    messages: Optional[List[Dict]] = None,
    inline_card: Optional[Dict] = None,
    action_buttons: Optional[List[Dict]] = None,
    quick_actions: Optional[List[str]] = None,
    success_toast: Optional[Dict[str, str]] = None,
) -> str:
    """Build SVG content for chat-panel wireframe variant."""
    
    # Default values
    if messages is None:
        messages = [
            {"text": "How do I update billing?", "is_user": True},
            {"text": "I can help with that.", "is_user": False},
        ]
    
    if inline_card is None:
        inline_card = {
            "title": "Pro Plan",
            "subtitle": "$29/mo",
            "detail": "Visa •••• 4242",
            "progress": 0.75,
            "footer": "Renews Dec 15"
        }
    
    if action_buttons is None:
        action_buttons = [
            {"text": "Update Card", "primary": True},
            {"text": "View Invoices", "primary": False},
        ]
    
    if quick_actions is None:
        quick_actions = ["Change billing cycle", "Download receipt"]
    
    elements = []
    
    # Browser window (main content area on left)
    elements.append(render_browser_window(
        config,
        x=20, y=20,
        width=340,
        height=380,
    ))
    
    # App header inside browser
    elements.append(render_app_header(
        config,
        x=35, y=75,
        width=310, height=45
    ))
    
    # Content card inside browser
    elements.append(render_content_card(
        config,
        x=35, y=135,
        width=310, height=120,
        show_divider=True
    ))
    
    # Chat panel on right
    elements.append(render_chat_panel(
        config,
        x=370, y=20,
        width=210, height=380,
        messages=messages,
        inline_card=inline_card,
        action_buttons=action_buttons,
        quick_actions=quick_actions,
    ))
    
    # Success toast (floating)
    if success_toast:
        elements.append(render_success_toast(
            config,
            x=35, y=280,
            title=success_toast.get('title', 'Success'),
            subtitle=success_toast.get('subtitle'),
            width=260
        ))
    
    return '\n'.join(elements)


def _build_modal_form_wireframe(
    config: WireframeConfig,
    modal_title: str = "Submit Support Request",
    modal_fields: Optional[List[Dict]] = None,
    modal_submit_text: str = "Submit Request",
    ticket_status: Optional[Dict] = None,
) -> str:
    """Build SVG content for modal-form wireframe variant."""
    
    if modal_fields is None:
        modal_fields = [
            {"label": "Subject"},
            {"label": "Describe your issue", "textarea": True},
        ]
    
    elements = []
    
    # Browser window
    elements.append(render_browser_window(
        config,
        x=20, y=20,
        width=config.width - 40,
        height=340
    ))
    
    # App header (dimmed)
    elements.append(render_app_header(
        config,
        x=35, y=75,
        width=config.width - 70,
        height=45
    ))
    
    # Content card (dimmed)
    elements.append(render_content_card(
        config,
        x=35, y=135,
        width=config.width - 70,
        height=100,
        opacity=0.5
    ))
    
    # Modal overlay
    elements.append(render_modal_overlay(
        config,
        x=20, y=60,
        width=config.width - 40,
        height=300
    ))
    
    # Modal dialog
    modal_width = 300
    modal_height = 240
    modal_x = (config.width - modal_width) // 2
    modal_y = 85
    
    elements.append(render_modal(
        config,
        x=modal_x, y=modal_y,
        width=modal_width, height=modal_height,
        title=modal_title,
        fields=modal_fields,
        submit_text=modal_submit_text
    ))
    
    # Ticket status flow (below browser)
    if ticket_status is not None:
        elements.append(render_ticket_status_flow(
            config,
            x=100, y=400,
            **ticket_status
        ))
    else:
        elements.append(render_ticket_status_flow(
            config,
            x=100, y=400
        ))
    
    return '\n'.join(elements)


def _build_dashboard_wireframe(config: WireframeConfig) -> str:
    """Build SVG content for basic dashboard wireframe."""
    elements = []
    
    # Browser window
    elements.append(render_browser_window(
        config,
        x=20, y=20,
        width=config.width - 40,
        height=config.height - 40
    ))
    
    # App header
    elements.append(render_app_header(
        config,
        x=35, y=75,
        width=config.width - 70,
        height=45
    ))
    
    # Content cards
    elements.append(render_content_card(
        config,
        x=35, y=135,
        width=config.width - 70,
        height=140,
        show_divider=True
    ))
    
    elements.append(render_content_card(
        config,
        x=35, y=290,
        width=(config.width - 90) // 2,
        height=100
    ))
    
    elements.append(render_content_card(
        config,
        x=35 + (config.width - 90) // 2 + 20, y=290,
        width=(config.width - 90) // 2,
        height=100
    ))
    
    return '\n'.join(elements)


def _build_wireframe_svg(
    config: WireframeConfig,
    variant: str,
    options: Dict[str, Any]
) -> str:
    """Build complete SVG for a wireframe variant."""
    
    if variant == "chat-panel":
        content = _build_chat_panel_wireframe(
            config,
            messages=options.get('chat_messages'),
            inline_card=options.get('chat_inline_card'),
            action_buttons=options.get('chat_action_buttons'),
            quick_actions=options.get('chat_quick_actions'),
            success_toast=options.get('success_toast'),
        )
    elif variant == "modal-form":
        content = _build_modal_form_wireframe(
            config,
            modal_title=options.get('modal_title', 'Submit Support Request'),
            modal_fields=options.get('modal_fields'),
            modal_submit_text=options.get('modal_submit_text', 'Submit Request'),
            ticket_status=options.get('ticket_status'),
        )
    else:
        content = _build_dashboard_wireframe(config)
    
    return f"""
<svg viewBox="0 0 {config.width} {config.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {config.get_filter_defs()}
  </defs>
  {content}
</svg>
    """


def _get_status_icon(status_type: str) -> str:
    """Get SVG icon for status type."""
    if status_type == "positive":
        return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    elif status_type == "negative":
        return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    else:
        return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>'


def _render_status_html(status: Dict[str, str], colors: WireframeColors) -> str:
    """Render status HTML element."""
    if not status:
        return ""
    
    status_type = status.get('type', 'neutral')
    status_text = status.get('text', '')
    icon = _get_status_icon(status_type)
    
    return f"""
    <div class="status {status_type}">
        {icon}
        <span>{escape(status_text)}</span>
    </div>
    """
