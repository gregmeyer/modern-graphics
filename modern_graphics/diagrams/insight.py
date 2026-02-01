"""Insight diagram generators for storytelling graphics.

Provides two main functions:
- generate_insight_story: Full insight graphic with visual comparison and key insight
- generate_key_insight: Standalone pull quote / key insight graphic
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING
from html import escape

if TYPE_CHECKING:
    from ..base import BaseGenerator
    from ..color_scheme import ColorScheme


def generate_insight_story(
    generator: "BaseGenerator",
    headline: str,
    subtitle: Optional[str] = None,
    eyebrow: Optional[str] = None,
    # Before/After panels
    before_svg: Optional[str] = None,
    before_label: str = "Before",
    before_status: Optional[Dict[str, str]] = None,
    after_svg: Optional[str] = None,
    after_label: str = "After",
    after_status: Optional[Dict[str, str]] = None,
    # Shift indicators
    shift_from: Optional[str] = None,
    shift_to: Optional[str] = None,
    shift_badge: Optional[str] = None,
    # Key insight
    insight_text: str = "",
    insight_label: str = "Key Insight",
    # Footer stats
    stats: Optional[List[Dict[str, str]]] = None,
    # Styling
    accent_color: str = "#0071e3",
    success_color: str = "#34c759",
    error_color: str = "#ff3b30",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a full insight story graphic with visual comparison.
    
    Args:
        generator: BaseGenerator instance
        headline: Main headline
        subtitle: Subtitle text
        eyebrow: Eyebrow text above headline
        before_svg: SVG content for "before" panel
        before_label: Label for before panel
        before_status: Status dict with 'type' and 'text' for before panel
        after_svg: SVG content for "after" panel
        after_label: Label for after panel
        after_status: Status dict with 'type' and 'text' for after panel
        shift_from: Left side of shift badge (e.g., "Tickets")
        shift_to: Right side of shift badge (e.g., "Control")
        shift_badge: Additional badge text (e.g., "User-owned inbox")
        insight_text: The key insight text (supports HTML for bold/highlight)
        insight_label: Label above insight text
        stats: List of stat dicts with 'label' and 'value' keys
        accent_color: Primary accent color
        success_color: Success/positive color
        error_color: Error/negative color
        color_scheme: Optional ColorScheme to derive colors from
        
    Returns:
        HTML string
    """
    # Apply color scheme if provided
    if color_scheme:
        accent_color = color_scheme.primary
        success_color = color_scheme.success or success_color
        error_color = color_scheme.error or error_color
        font_family = color_scheme.font_family
        font_family_display = getattr(color_scheme, 'font_family_display', font_family)
        font_family_body = getattr(color_scheme, 'font_family_body', font_family)
    else:
        font_family = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
        font_family_display = font_family
        font_family_body = font_family
    
    # Build shift indicator HTML
    shift_html = ""
    if shift_from and shift_to:
        shift_html += f"""
        <div class="shift-badge">
            <span>{escape(shift_from)}</span>
            <span class="arrow">→</span>
            <span>{escape(shift_to)}</span>
        </div>
        """
    if shift_badge:
        shift_html += f"""
        <div class="shift-badge positive">{escape(shift_badge)}</div>
        """
    
    if shift_html:
        shift_html = f"""
        <div class="shift-indicator">
            {shift_html}
        </div>
        """
    
    # Build before panel
    before_panel = ""
    if before_svg:
        before_status_html = _render_panel_status(before_status, "negative") if before_status else ""
        before_panel = f"""
        <div class="showcase-panel before">
            <div class="panel-label before">
                <div class="dot"></div>
                <span>{escape(before_label)}</span>
            </div>
            <div class="panel-svg">
                {before_svg}
            </div>
            {before_status_html}
        </div>
        """
    
    # Build after panel
    after_panel = ""
    if after_svg:
        after_status_html = _render_panel_status(after_status, "positive") if after_status else ""
        after_panel = f"""
        <div class="showcase-panel after">
            <div class="panel-label after">
                <div class="dot"></div>
                <span>{escape(after_label)}</span>
            </div>
            <div class="panel-svg">
                {after_svg}
            </div>
            {after_status_html}
        </div>
        """
    
    # Build visual showcase
    showcase_html = ""
    if before_panel or after_panel:
        showcase_html = f"""
        <div class="visual-showcase">
            {before_panel}
            {after_panel}
        </div>
        """
    
    # Build key insight
    insight_html = ""
    if insight_text:
        insight_html = f"""
        <div class="key-insight">
            <div class="insight-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            </div>
            <div class="insight-label">{escape(insight_label)}</div>
            <p class="insight-text">{insight_text}</p>
        </div>
        """
    
    # Build footer stats
    stats_html = ""
    if stats:
        stat_items = "".join(
            f"""
            <div class="stat">
                <div class="stat-label">{escape(stat.get('label', ''))}</div>
                <div class="stat-value">{escape(stat.get('value', ''))}</div>
            </div>
            """
            for stat in stats
        )
        stats_html = f"""
        <div class="footer-stats">
            {stat_items}
        </div>
        """
    
    html_content = f"""
    <div class="insight-card">
        <div class="card-inner">
            <div class="header">
                <div class="header-text">
                    {f'<div class="eyebrow">{escape(eyebrow)}</div>' if eyebrow else ''}
                    <h1>{escape(headline)}</h1>
                    {f'<p class="subtitle">{escape(subtitle)}</p>' if subtitle else ''}
                </div>
                {shift_html}
            </div>
            
            {showcase_html}
            {insight_html}
            {stats_html}
        </div>
    </div>
    """
    
    css_content = f"""
        :root {{
            --font: {font_family};
            --font-display: {font_family_display};
            --font-body: {font_family_body};
            --accent: {accent_color};
            --accent-soft: {_with_alpha(accent_color, 0.15)};
            --accent-glow: {_with_alpha(accent_color, 0.4)};
            --success: {success_color};
            --success-soft: {_with_alpha(success_color, 0.15)};
            --error: {error_color};
            --surface-1: #ffffff;
            --surface-2: #f5f5f7;
            --surface-3: #e8e8ed;
            --text-1: #1d1d1f;
            --text-2: #6e6e73;
            --text-3: #86868b;
            --border: rgba(0, 0, 0, 0.06);
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: var(--font);
            background: linear-gradient(180deg, #f5f5f7 0%, #e8e8ed 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 60px;
            -webkit-font-smoothing: antialiased;
        }}
        
        .insight-card {{
            width: 1200px;
            background: var(--surface-1);
            border-radius: 40px;
            box-shadow: 0 0 0 1px var(--border), 0 40px 120px rgba(0,0,0,0.12), 0 20px 60px rgba(0,0,0,0.08);
            overflow: hidden;
            position: relative;
        }}
        
        .insight-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 6px;
            background: linear-gradient(90deg, var(--accent), #5856d6, var(--success));
        }}
        
        .card-inner {{ padding: 56px; }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 40px;
        }}
        
        .header-text {{ flex: 1; max-width: 600px; }}
        
        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-display);
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 16px;
        }}
        
        .eyebrow::before {{
            content: '';
            width: 24px;
            height: 2px;
            background: var(--accent);
            border-radius: 1px;
        }}
        
        h1 {{
            font-family: var(--font-display);
            font-size: 48px;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1.1;
            color: var(--text-1);
            margin-bottom: 16px;
        }}
        
        .subtitle {{
            font-family: var(--font-body);
            font-size: 20px;
            font-weight: 400;
            color: var(--text-2);
            line-height: 1.5;
            letter-spacing: -0.01em;
        }}
        
        .shift-indicator {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 12px;
        }}
        
        .shift-badge {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 20px;
            background: var(--surface-2);
            border-radius: 100px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-2);
        }}
        
        .shift-badge .arrow {{ color: var(--accent); font-size: 18px; }}
        .shift-badge.positive {{ background: var(--success-soft); color: var(--success); }}
        
        .visual-showcase {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 40px;
        }}
        
        .showcase-panel {{
            background: var(--surface-2);
            border-radius: 24px;
            padding: 24px;
            position: relative;
            overflow: hidden;
        }}
        
        .showcase-panel::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
        }}
        
        .showcase-panel.before::before {{ background: var(--text-3); }}
        .showcase-panel.after::before {{ background: var(--success); }}
        
        .panel-label {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 16px;
        }}
        
        .panel-label .dot {{ width: 8px; height: 8px; border-radius: 50%; }}
        .panel-label.before .dot {{ background: var(--text-3); }}
        .panel-label.after .dot {{ background: var(--success); }}
        
        .panel-label span {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text-2);
            letter-spacing: -0.01em;
        }}
        
        .panel-svg {{
            background: var(--surface-1);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        }}
        
        .panel-svg svg {{ width: 100%; height: auto; display: block; }}
        
        .panel-status {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 16px;
            padding: 10px 16px;
            border-radius: 100px;
            font-size: 13px;
            font-weight: 600;
        }}
        
        .panel-status.negative {{ background: {_with_alpha(error_color, 0.08)}; color: var(--error); }}
        .panel-status.positive {{ background: var(--success-soft); color: var(--success); }}
        .panel-status svg {{ width: 16px; height: 16px; }}
        
        .key-insight {{
            background: linear-gradient(135deg, var(--surface-2) 0%, {_with_alpha(accent_color, 0.04)} 100%);
            border-radius: 24px;
            padding: 32px;
            border-left: 4px solid var(--accent);
            position: relative;
        }}
        
        .insight-icon {{
            position: absolute;
            top: -16px;
            left: 32px;
            width: 40px;
            height: 40px;
            background: var(--accent);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px var(--accent-glow);
        }}
        
        .insight-icon svg {{ width: 20px; height: 20px; color: white; }}
        
        .insight-label {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 12px;
            margin-top: 8px;
        }}
        
        .insight-text {{
            font-family: var(--font-body);
            font-size: 22px;
            font-weight: 500;
            letter-spacing: -0.02em;
            line-height: 1.5;
            color: var(--text-1);
        }}
        
        .insight-text strong {{ font-weight: 700; }}
        .insight-text .highlight {{ color: var(--accent); font-weight: 600; }}
        
        .footer-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 32px;
            padding-top: 32px;
            border-top: 1px solid var(--border);
        }}
        
        .stat {{ text-align: center; padding: 20px; }}
        
        .stat-label {{
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-3);
            margin-bottom: 8px;
        }}
        
        .stat-value {{
            font-size: 15px;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: -0.01em;
        }}
    """
    
    # Build Google Fonts link
    google_fonts_link = ""
    if color_scheme:
        fonts_link = color_scheme.get_google_fonts_link()
        if fonts_link:
            google_fonts_link = fonts_link
    
    html = generator._wrap_html(html_content, css_content)
    if google_fonts_link and '</head>' in html:
        html = html.replace('</head>', f'    {google_fonts_link}\n</head>')
    
    return html


def generate_key_insight(
    generator: "BaseGenerator",
    text: str,
    label: str = "Key Insight",
    eyebrow: Optional[str] = None,
    context: Optional[str] = None,
    # Styling
    accent_color: str = "#0071e3",
    variant: str = "default",  # "default", "minimal", "bold", "quote"
    icon: str = "lightning",  # "lightning", "lightbulb", "quote", "star", "none"
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a standalone key insight / pull quote graphic.
    
    Args:
        generator: BaseGenerator instance
        text: The insight text (supports HTML for bold/highlight)
        label: Label above the insight
        eyebrow: Optional eyebrow text above label
        context: Optional context text below the insight
        accent_color: Primary accent color
        variant: Style variant - "default", "minimal", "bold", "quote"
        icon: Icon type - "lightning", "lightbulb", "quote", "star", "none"
        color_scheme: Optional ColorScheme to derive colors from
        
    Returns:
        HTML string
    """
    # Apply color scheme if provided
    is_arcade = False
    effects = {}
    if color_scheme:
        accent_color = color_scheme.primary
        font_family = color_scheme.font_family
        font_family_display = getattr(color_scheme, 'font_family_display', font_family)
        font_family_body = getattr(color_scheme, 'font_family_body', font_family)
        effects = getattr(color_scheme, 'effects', {}) or {}
        # Only treat as arcade if explicitly named "arcade" (not just because it has glow)
        is_arcade = color_scheme.name.lower() == "arcade"
        
        # Get colors from scheme
        bg_primary = color_scheme.bg_primary
        bg_secondary = color_scheme.bg_secondary
        text_primary = color_scheme.text_primary
        text_secondary = color_scheme.text_secondary
        text_tertiary = color_scheme.text_tertiary
        glow_color = getattr(color_scheme, 'glow_color', accent_color)
        accent_secondary = color_scheme.accent
        success_color = color_scheme.success
    else:
        font_family = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
        font_family_display = font_family
        font_family_body = font_family
        bg_primary = "#ffffff"
        bg_secondary = "#f5f5f7"
        text_primary = "#1d1d1f"
        text_secondary = "#6e6e73"
        text_tertiary = "#86868b"
        glow_color = accent_color
        accent_secondary = accent_color
        success_color = "#34c759"
    
    # Get icon SVG
    icon_svg = _get_insight_icon(icon)
    icon_html = f"""
        <div class="insight-icon">
            {icon_svg}
        </div>
    """ if icon != "none" else ""
    
    # Build eyebrow HTML
    eyebrow_html = f'<div class="eyebrow">{escape(eyebrow)}</div>' if eyebrow else ""
    
    # Build context HTML
    context_html = f'<div class="context">{escape(context)}</div>' if context else ""
    
    # Scanlines overlay for arcade theme
    scanlines_html = '<div class="scanlines"></div>' if effects.get('scanlines') else ""
    
    html_content = f"""
    <div class="key-insight-card {variant}">
        {scanlines_html}
        {icon_html}
        <div class="content">
            {eyebrow_html}
            <div class="label">{escape(label)}</div>
            <p class="text">{text}</p>
            {context_html}
        </div>
    </div>
    """
    
    # Get variant-specific styles
    variant_styles = _get_variant_styles(variant, accent_color)
    
    # Check if this is a dark theme (for contrast handling)
    is_dark_theme = False
    if color_scheme:
        # Check luminance of bg_primary to determine if dark
        bg_hex = bg_primary.lstrip('#')
        if len(bg_hex) == 6:
            r, g, b = int(bg_hex[0:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            is_dark_theme = luminance < 0.5
    
    # Dark theme styles (non-arcade) - ensure card has solid background
    dark_theme_styles = ""
    if is_dark_theme and not is_arcade:
        dark_theme_styles = f"""
        /* Dark Theme Overrides */
        .key-insight-card {{
            background: {bg_primary};
            border: 2px solid {accent_color};
        }}
        .key-insight-card.bold {{
            background: {bg_primary};
            border: 2px solid {accent_color};
        }}
        .key-insight-card.minimal {{
            background: {bg_primary};
            border-left: 4px solid {accent_color};
            border-radius: 8px;
        }}
        """
    
    # Arcade-specific styles
    arcade_styles = ""
    if is_arcade:
        arcade_styles = f"""
        /* Arcade Theme Overrides */
        body {{
            background: {bg_secondary};
        }}
        
        .key-insight-card {{
            background: {bg_primary};
            border: 4px solid {accent_color};
            border-radius: 0;
            box-shadow: 
                0 0 30px {_with_alpha(glow_color, 0.4)},
                inset 0 0 60px {_with_alpha(glow_color, 0.05)};
        }}
        
        /* Pixel corner accents */
        .key-insight-card::before {{
            content: '';
            position: absolute;
            top: -4px; left: -4px; right: -4px; bottom: -4px;
            background: 
                linear-gradient(90deg, {accent_secondary} 8px, transparent 8px),
                linear-gradient(180deg, {accent_secondary} 8px, transparent 8px),
                linear-gradient(90deg, transparent calc(100% - 8px), {accent_secondary} calc(100% - 8px)),
                linear-gradient(180deg, transparent calc(100% - 8px), {accent_secondary} calc(100% - 8px));
            background-size: 100% 4px, 4px 100%, 100% 4px, 4px 100%;
            background-position: 0 0, 0 0, 0 100%, 100% 0;
            background-repeat: no-repeat;
            pointer-events: none;
        }}
        
        .insight-icon {{
            background: linear-gradient(135deg, {accent_secondary}, {accent_color});
            border-radius: 0;
            box-shadow: 0 0 20px {_with_alpha(accent_secondary, 0.6)};
        }}
        
        .label {{
            font-family: {font_family_display};
            font-size: 10px;
            letter-spacing: 2px;
            color: {success_color};
            text-shadow: 0 0 10px {_with_alpha(success_color, 0.6)};
        }}
        
        .text {{
            font-family: {font_family_body};
            font-size: 32px;
            color: {text_primary};
            text-shadow: 0 0 10px {_with_alpha(glow_color, 0.3)};
        }}
        
        .text .highlight {{
            color: {accent_color};
            text-shadow: 0 0 20px {_with_alpha(accent_color, 0.6)};
        }}
        
        .text em {{
            font-style: normal;
            color: {accent_secondary};
            text-shadow: 0 0 20px {_with_alpha(accent_secondary, 0.6)};
        }}
        
        .eyebrow {{
            font-family: {font_family_display};
            font-size: 8px;
            color: {text_tertiary};
        }}
        
        .context {{
            font-family: {font_family_display};
            font-size: 10px;
            color: {success_color};
            text-shadow: 0 0 10px {_with_alpha(success_color, 0.4)};
        }}
        
        /* Scanlines */
        .scanlines {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 0, 0, 0.1) 2px,
                rgba(0, 0, 0, 0.1) 4px
            );
            pointer-events: none;
            z-index: 10;
        }}
        """
    
    # Build Google Fonts link
    google_fonts_link = ""
    if color_scheme:
        fonts_link = color_scheme.get_google_fonts_link()
        if fonts_link:
            google_fonts_link = fonts_link
    
    css_content = f"""
        :root {{
            --font: {font_family};
            --font-display: {font_family_display};
            --font-body: {font_family_body};
            --accent: {accent_color};
            --accent-soft: {_with_alpha(accent_color, 0.1)};
            --accent-glow: {_with_alpha(glow_color, 0.3)};
            --surface-1: {bg_primary};
            --surface-2: {bg_secondary};
            --text-1: {text_primary};
            --text-2: {text_secondary};
            --text-3: {text_tertiary};
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: var(--font);
            background: var(--surface-2);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
            -webkit-font-smoothing: antialiased;
        }}
        
        .key-insight-card {{
            max-width: 800px;
            background: var(--surface-1);
            border-radius: 32px;
            padding: 48px 56px;
            position: relative;
            box-shadow: 0 0 0 1px rgba(0,0,0,0.04), 0 20px 60px rgba(0,0,0,0.1);
        }}
        
        .insight-icon {{
            position: absolute;
            top: -20px;
            left: 48px;
            width: 48px;
            height: 48px;
            background: var(--accent);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 24px var(--accent-glow);
        }}
        
        .insight-icon svg {{
            width: 24px;
            height: 24px;
            color: white;
        }}
        
        .content {{ padding-top: 8px; position: relative; z-index: 1; }}
        
        .eyebrow {{
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-3);
            margin-bottom: 8px;
        }}
        
        .label {{
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 16px;
        }}
        
        .text {{
            font-size: 28px;
            font-weight: 500;
            letter-spacing: -0.02em;
            line-height: 1.45;
            color: var(--text-1);
        }}
        
        .text strong {{ font-weight: 700; }}
        .text .highlight {{ color: var(--accent); font-weight: 600; }}
        .text em {{ font-style: italic; }}
        
        .context {{
            margin-top: 20px;
            font-size: 14px;
            color: var(--text-3);
            font-weight: 500;
        }}
        
        {variant_styles}
        {dark_theme_styles}
        {arcade_styles}
    """
    
    # Inject Google Fonts if needed
    html = generator._wrap_html(html_content, css_content)
    if google_fonts_link and '</head>' in html:
        html = html.replace('</head>', f'    {google_fonts_link}\n</head>')
    
    return html


# ============================================================================
# Private helper functions
# ============================================================================

def _with_alpha(hex_color: str, alpha: float) -> str:
    """Convert hex color to rgba with specified alpha."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def _render_panel_status(status: Dict[str, str], default_type: str = "neutral") -> str:
    """Render panel status HTML."""
    status_type = status.get('type', default_type)
    status_text = status.get('text', '')
    
    icon = _get_status_icon(status_type)
    
    return f"""
    <div class="panel-status {status_type}">
        {icon}
        <span>{escape(status_text)}</span>
    </div>
    """


def _get_status_icon(status_type: str) -> str:
    """Get SVG icon for status type."""
    if status_type == "positive":
        return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    elif status_type == "negative":
        return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    return '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>'


def _get_insight_icon(icon_type: str) -> str:
    """Get SVG icon for insight card."""
    icons = {
        "lightning": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>',
        "lightbulb": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>',
        "quote": '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/></svg>',
        "star": '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>',
    }
    return icons.get(icon_type, icons["lightning"])


def generate_insight_card(
    generator: "BaseGenerator",
    text: str,
    svg_content: str,
    label: str = "Key Insight",
    svg_label: Optional[str] = None,
    eyebrow: Optional[str] = None,
    context: Optional[str] = None,
    # Layout
    layout: str = "side-by-side",  # "side-by-side" or "stacked"
    svg_position: str = "right",   # "left" or "right" (for side-by-side)
    # Styling
    accent_color: str = "#0071e3",
    variant: str = "bold",  # "default", "bold"
    icon: str = "lightning",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate an insight card combining key insight with illustrative SVG.
    
    Args:
        generator: BaseGenerator instance
        text: The insight text (supports HTML for bold/highlight)
        svg_content: SVG string to display
        label: Label above the insight
        svg_label: Optional label above the SVG
        eyebrow: Optional eyebrow text
        context: Optional context text below insight
        layout: "side-by-side" or "stacked"
        svg_position: "left" or "right" for side-by-side layout
        accent_color: Primary accent color
        variant: Style variant for insight - "default" or "bold"
        icon: Icon type - "lightning", "lightbulb", "quote", "star", "none"
        color_scheme: Optional ColorScheme to derive colors from
        
    Returns:
        HTML string
    """
    # Apply color scheme
    is_arcade = False
    effects = {}
    if color_scheme:
        accent_color = color_scheme.primary
        font_family = color_scheme.font_family
        font_family_display = getattr(color_scheme, 'font_family_display', font_family)
        font_family_body = getattr(color_scheme, 'font_family_body', font_family)
        effects = getattr(color_scheme, 'effects', {}) or {}
        is_arcade = color_scheme.name.lower() == "arcade" or effects.get('glow')
        
        bg_primary = color_scheme.bg_primary
        bg_secondary = color_scheme.bg_secondary
        text_primary = color_scheme.text_primary
        text_secondary = color_scheme.text_secondary
        text_tertiary = color_scheme.text_tertiary
        glow_color = getattr(color_scheme, 'glow_color', accent_color)
        accent_secondary = color_scheme.accent
        success_color = color_scheme.success
    else:
        font_family = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
        font_family_display = font_family
        font_family_body = font_family
        bg_primary = "#ffffff"
        bg_secondary = "#f5f5f7"
        text_primary = "#1d1d1f"
        text_secondary = "#6e6e73"
        text_tertiary = "#86868b"
        glow_color = accent_color
        accent_secondary = accent_color
        success_color = "#34c759"
    
    # Get icon SVG
    icon_svg = _get_insight_icon(icon) if icon != "none" else ""
    icon_html = f"""
        <div class="insight-icon">
            {icon_svg}
        </div>
    """ if icon_svg else ""
    
    # Scanlines for arcade
    scanlines_html = '<div class="scanlines"></div>' if effects.get('scanlines') else ""
    
    # Build insight content
    eyebrow_html = f'<div class="eyebrow">{escape(eyebrow)}</div>' if eyebrow else ""
    context_html = f'<div class="context">{escape(context)}</div>' if context else ""
    
    insight_html = f"""
    <div class="insight-content {variant}">
        {icon_html}
        {eyebrow_html}
        <div class="label">{escape(label)}</div>
        <p class="text">{text}</p>
        {context_html}
    </div>
    """
    
    # Build SVG content
    svg_label_html = f"""
        <div class="svg-label">
            <div class="dot"></div>
            <span>{escape(svg_label)}</span>
        </div>
    """ if svg_label else ""
    
    svg_html = f"""
    <div class="svg-container">
        {svg_label_html}
        <div class="svg-wrapper">
            {svg_content}
        </div>
    </div>
    """
    
    # Arrange based on layout
    if layout == "stacked":
        grid_style = "grid-template-columns: 1fr; gap: 32px;"
        content_order = f"{insight_html}{svg_html}"
    else:
        grid_style = "grid-template-columns: 1fr 1fr; gap: 40px;"
        if svg_position == "left":
            content_order = f"{svg_html}{insight_html}"
        else:
            content_order = f"{insight_html}{svg_html}"
    
    html_content = f"""
    <div class="insight-card" style="{grid_style}">
        {scanlines_html}
        {content_order}
    </div>
    """
    
    # Variant-specific insight styles
    variant_insight_css = ""
    if variant == "bold" and not is_arcade:
        variant_insight_css = f"""
        .insight-content.bold {{
            background: linear-gradient(135deg, {_with_alpha(accent_color, 0.04)} 0%, {_with_alpha(accent_color, 0.1)} 100%);
            border: 2px solid {_with_alpha(accent_color, 0.15)};
        }}
        .insight-content.bold .text {{
            font-size: 22px;
            font-weight: 600;
        }}
        """
    
    # Arcade-specific styles
    arcade_styles = ""
    if is_arcade:
        arcade_styles = f"""
        /* Arcade Theme */
        body {{
            background: {bg_secondary};
        }}
        
        .insight-card {{
            background: {bg_primary};
            border: 4px solid {accent_color};
            border-radius: 0;
            box-shadow: 
                0 0 40px {_with_alpha(glow_color, 0.4)},
                inset 0 0 80px {_with_alpha(glow_color, 0.05)};
            position: relative;
        }}
        
        /* Pixel corners */
        .insight-card::before {{
            content: '';
            position: absolute;
            top: -4px; left: -4px; right: -4px; bottom: -4px;
            background: 
                linear-gradient(90deg, {accent_secondary} 8px, transparent 8px),
                linear-gradient(180deg, {accent_secondary} 8px, transparent 8px),
                linear-gradient(90deg, transparent calc(100% - 8px), {accent_secondary} calc(100% - 8px)),
                linear-gradient(180deg, transparent calc(100% - 8px), {accent_secondary} calc(100% - 8px));
            background-size: 100% 4px, 4px 100%, 100% 4px, 4px 100%;
            background-position: 0 0, 0 0, 0 100%, 100% 0;
            background-repeat: no-repeat;
            pointer-events: none;
        }}
        
        .insight-content {{
            background: {_with_alpha(accent_color, 0.1)};
            border: 2px solid {accent_color};
            border-radius: 0;
        }}
        
        .insight-content.bold {{
            background: {_with_alpha(accent_color, 0.1)};
            border: 2px solid {accent_color};
        }}
        
        .insight-icon {{
            background: linear-gradient(135deg, {accent_secondary}, {accent_color});
            border-radius: 0;
            box-shadow: 0 0 20px {_with_alpha(accent_secondary, 0.6)};
        }}
        
        .label {{
            font-family: {font_family_display};
            font-size: 10px;
            letter-spacing: 2px;
            color: {success_color};
            text-shadow: 0 0 10px {_with_alpha(success_color, 0.6)};
        }}
        
        .text {{
            font-family: {font_family_body};
            font-size: 28px;
            color: {text_primary};
            text-shadow: 0 0 10px {_with_alpha(glow_color, 0.3)};
        }}
        
        .text .highlight {{
            color: {accent_color};
            text-shadow: 0 0 20px {_with_alpha(accent_color, 0.6)};
        }}
        
        .text em {{
            font-style: normal;
            color: {accent_secondary};
            text-shadow: 0 0 20px {_with_alpha(accent_secondary, 0.6)};
        }}
        
        .eyebrow {{
            font-family: {font_family_display};
            font-size: 8px;
            color: {text_tertiary};
        }}
        
        .context {{
            font-family: {font_family_display};
            font-size: 10px;
            color: {success_color};
            text-shadow: 0 0 10px {_with_alpha(success_color, 0.4)};
        }}
        
        .svg-label span {{
            font-family: {font_family_display};
            font-size: 8px;
            color: {text_secondary};
            letter-spacing: 1px;
        }}
        
        .svg-label .dot {{
            background: {accent_color};
            box-shadow: 0 0 10px {accent_color};
            border-radius: 0;
            width: 8px;
            height: 8px;
        }}
        
        .svg-wrapper {{
            border-radius: 0;
            border: 2px solid {accent_color};
            box-shadow: 0 0 20px {_with_alpha(accent_color, 0.3)};
        }}
        
        .scanlines {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 0, 0, 0.1) 2px,
                rgba(0, 0, 0, 0.1) 4px
            );
            pointer-events: none;
            z-index: 10;
        }}
        """
    
    # Google Fonts link
    google_fonts_link = ""
    if color_scheme:
        fonts_link = color_scheme.get_google_fonts_link()
        if fonts_link:
            google_fonts_link = fonts_link
    
    css_content = f"""
        :root {{
            --font: {font_family};
            --font-display: {font_family_display};
            --font-body: {font_family_body};
            --accent: {accent_color};
            --accent-soft: {_with_alpha(accent_color, 0.1)};
            --accent-glow: {_with_alpha(glow_color, 0.35)};
            --surface-1: {bg_primary};
            --surface-2: {bg_secondary};
            --text-1: {text_primary};
            --text-2: {text_secondary};
            --text-3: {text_tertiary};
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: var(--font);
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }}
        
        .insight-card {{
            display: grid;
            align-items: center;
            max-width: 900px;
            background: var(--surface-1);
            border-radius: 32px;
            padding: 40px;
            box-shadow: 0 0 0 1px rgba(0,0,0,0.04), 0 20px 60px rgba(0,0,0,0.1);
            position: relative;
        }}
        
        .insight-content {{
            position: relative;
            padding: 28px 32px;
            border-radius: 24px;
        }}
        
        .insight-content.default {{
            background: var(--surface-2);
        }}
        
        .insight-icon {{
            position: absolute;
            top: -16px;
            left: 28px;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 6px 20px var(--accent-glow);
        }}
        
        .insight-icon svg {{
            width: 20px;
            height: 20px;
            color: white;
        }}
        
        .eyebrow {{
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-3);
            margin-bottom: 6px;
            margin-top: 8px;
        }}
        
        .label {{
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 12px;
        }}
        
        .text {{
            font-size: 20px;
            font-weight: 500;
            letter-spacing: -0.02em;
            line-height: 1.4;
            color: var(--text-1);
        }}
        
        .text strong {{ font-weight: 700; }}
        .text .highlight {{ color: var(--accent); font-weight: 600; }}
        .text em {{ font-style: normal; color: var(--accent); }}
        
        .context {{
            margin-top: 14px;
            font-size: 12px;
            color: var(--text-3);
            font-weight: 500;
        }}
        
        .svg-container {{
            position: relative;
            z-index: 1;
        }}
        
        .svg-label {{
            position: absolute;
            top: -22px;
            left: 0;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .svg-label .dot {{
            width: 6px;
            height: 6px;
            background: var(--accent);
            border-radius: 50%;
        }}
        
        .svg-label span {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-2);
        }}
        
        .svg-wrapper {{
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 12px 40px rgba(0,0,0,0.1);
        }}
        
        .svg-wrapper svg {{
            display: block;
            width: 100%;
            height: auto;
        }}
        
        {variant_insight_css}
        {arcade_styles}
    """
    
    html = generator._wrap_html(html_content, css_content)
    if google_fonts_link and '</head>' in html:
        html = html.replace('</head>', f'    {google_fonts_link}\n</head>')
    
    return html


def _get_variant_styles(variant: str, accent_color: str) -> str:
    """Get CSS overrides for style variant."""
    if variant == "minimal":
        return """
        .key-insight-card.minimal {
            background: transparent;
            box-shadow: none;
            border-left: 3px solid var(--accent);
            border-radius: 0;
            padding: 24px 32px;
        }
        .key-insight-card.minimal .insight-icon {
            display: none;
        }
        .key-insight-card.minimal .content {
            padding-top: 0;
        }
        .key-insight-card.minimal .text {
            font-size: 24px;
        }
        """
    elif variant == "bold":
        return f"""
        .key-insight-card.bold {{
            background: linear-gradient(135deg, {_with_alpha(accent_color, 0.05)} 0%, {_with_alpha(accent_color, 0.12)} 100%);
            border: 2px solid {_with_alpha(accent_color, 0.2)};
        }}
        .key-insight-card.bold .text {{
            font-size: 32px;
            font-weight: 600;
        }}
        """
    elif variant == "quote":
        return """
        .key-insight-card.quote {
            padding-left: 80px;
        }
        .key-insight-card.quote .insight-icon {
            left: 24px;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            box-shadow: none;
        }
        .key-insight-card.quote .insight-icon svg {
            width: 40px;
            height: 40px;
            color: var(--accent);
            opacity: 0.3;
        }
        .key-insight-card.quote .label {
            display: none;
        }
        .key-insight-card.quote .text {
            font-style: italic;
            font-size: 26px;
        }
        """
    return ""
