"""Theme utilities for diagram generators.

This module provides shared functions for extracting colors, fonts, and styles
from ColorScheme objects, with sensible defaults for unthemed diagrams.
"""

from typing import Optional, Dict, Any, Tuple, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


@dataclass
class ThemeColors:
    """Extracted theme colors with defaults."""
    # Primary colors
    accent: str
    success: str
    error: str
    warning: str
    
    # Text colors
    text_primary: str
    text_secondary: str
    text_tertiary: str
    
    # Background colors
    bg_primary: str
    bg_secondary: str
    bg_tertiary: str
    
    # Computed colors for layouts
    page_bg: str
    card_bg: str
    card_border: str
    
    # Fonts
    font_family: str
    font_family_display: str
    font_family_body: str
    
    # Theme state
    is_dark: bool
    google_fonts_link: str


def extract_theme_colors(color_scheme: Optional["ColorScheme"] = None) -> ThemeColors:
    """Extract colors and fonts from a ColorScheme with defaults.
    
    Args:
        color_scheme: Optional ColorScheme object
        
    Returns:
        ThemeColors dataclass with all extracted values
    """
    if color_scheme:
        accent = color_scheme.primary
        success = color_scheme.success or "#34c759"
        error = color_scheme.error or "#ff3b30"
        warning = color_scheme.warning or "#ff9500"
        
        font_family = color_scheme.font_family
        font_family_display = getattr(color_scheme, 'font_family_display', font_family)
        font_family_body = getattr(color_scheme, 'font_family_body', font_family)
        
        bg_primary = color_scheme.bg_primary
        bg_secondary = color_scheme.bg_secondary
        bg_tertiary = getattr(color_scheme, 'bg_tertiary', bg_secondary)
        
        text_primary = color_scheme.text_primary
        text_secondary = color_scheme.text_secondary
        text_tertiary = color_scheme.text_tertiary
        
        # Check if dark theme
        is_dark = _is_dark_color(bg_primary)
        
        # For dark themes, adjust page/card backgrounds
        if is_dark:
            page_bg = bg_secondary
            card_bg = bg_primary
            card_border = f"1px solid {color_scheme.border_medium}"
        else:
            page_bg = bg_secondary
            card_bg = bg_primary
            card_border = "none"
        
        # Get Google Fonts link
        google_fonts_link = color_scheme.get_google_fonts_link() or ""
    else:
        # Default light theme
        accent = "#007AFF"
        success = "#34c759"
        error = "#ff3b30"
        warning = "#ff9500"
        
        font_family = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
        font_family_display = font_family
        font_family_body = font_family
        
        bg_primary = "#ffffff"
        bg_secondary = "#f5f5f7"
        bg_tertiary = "#e8e8ed"
        
        text_primary = "#1D1D1F"
        text_secondary = "#6e6e73"
        text_tertiary = "#8E8E93"
        
        page_bg = "#f5f5f7"
        card_bg = "#ffffff"
        card_border = "none"
        is_dark = False
        google_fonts_link = ""
    
    return ThemeColors(
        accent=accent,
        success=success,
        error=error,
        warning=warning,
        text_primary=text_primary,
        text_secondary=text_secondary,
        text_tertiary=text_tertiary,
        bg_primary=bg_primary,
        bg_secondary=bg_secondary,
        bg_tertiary=bg_tertiary,
        page_bg=page_bg,
        card_bg=card_bg,
        card_border=card_border,
        font_family=font_family,
        font_family_display=font_family_display,
        font_family_body=font_family_body,
        is_dark=is_dark,
        google_fonts_link=google_fonts_link,
    )


def _is_dark_color(hex_color: str) -> bool:
    """Check if a hex color is dark based on luminance.
    
    Args:
        hex_color: Hex color string (e.g., "#002244")
        
    Returns:
        True if the color is dark (luminance < 0.5)
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return False
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Relative luminance formula
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance < 0.5


def generate_css_variables(theme: ThemeColors) -> str:
    """Generate CSS :root variables from theme colors.
    
    Args:
        theme: ThemeColors dataclass
        
    Returns:
        CSS string with :root variables
    """
    return f"""
        :root {{
            --font: {theme.font_family};
            --font-display: {theme.font_family_display};
            --font-body: {theme.font_family_body};
            --accent: {theme.accent};
            --success: {theme.success};
            --error: {theme.error};
            --warning: {theme.warning};
            --bg-page: {theme.page_bg};
            --bg-card: {theme.card_bg};
            --bg-tertiary: {theme.bg_tertiary};
            --text-1: {theme.text_primary};
            --text-2: {theme.text_secondary};
            --text-3: {theme.text_tertiary};
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: var(--font-body);
            background: var(--bg-page);
            -webkit-font-smoothing: antialiased;
        }}
    """


def generate_base_styles(theme: ThemeColors) -> str:
    """Generate common base styles for diagrams.
    
    Args:
        theme: ThemeColors dataclass
        
    Returns:
        CSS string with base styles
    """
    return f"""
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .title {{
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            color: var(--text-1);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .subtitle {{
            font-family: var(--font-body);
            font-size: 16px;
            color: var(--text-2);
            margin-bottom: 16px;
        }}
    """


def generate_card_styles(theme: ThemeColors, border_radius: str = "14px") -> str:
    """Generate card/step styles for diagrams.
    
    Args:
        theme: ThemeColors dataclass
        border_radius: Border radius for cards
        
    Returns:
        CSS string with card styles
    """
    shadow = "0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04)"
    if theme.is_dark:
        shadow = "0 2px 8px rgba(0, 0, 0, 0.3), 0 8px 24px rgba(0, 0, 0, 0.2)"
    
    return f"""
        .card, .step, .item {{
            background: var(--bg-card);
            border: {theme.card_border};
            border-radius: {border_radius};
            padding: 24px 32px;
            font-family: var(--font-body);
            font-size: 18px;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: -0.01em;
            box-shadow: {shadow};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
    """


def inject_google_fonts(html: str, theme: ThemeColors) -> str:
    """Inject Google Fonts link into HTML head.
    
    Args:
        html: HTML string
        theme: ThemeColors dataclass
        
    Returns:
        HTML string with fonts link injected
    """
    if theme.google_fonts_link and '</head>' in html:
        html = html.replace('</head>', f'    {theme.google_fonts_link}\n</head>')
    return html


def with_alpha(color: str, alpha: float) -> str:
    """Convert hex color to rgba with alpha.
    
    Args:
        color: Hex color string
        alpha: Alpha value (0-1)
        
    Returns:
        rgba() CSS string
    """
    hex_color = color.lstrip('#')
    if len(hex_color) != 6:
        return color
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f"rgba({r}, {g}, {b}, {alpha})"
