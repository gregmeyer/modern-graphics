"""Color scheme generator for consistent theming across all graphics types.

Allows teams to define brand colors and fonts once and have them automatically
applied to hero slides, slide cards, and other diagram types.

Example:
    >>> from modern_graphics.color_scheme import create_custom_scheme
    >>> scheme = create_custom_scheme(
    ...     name="My Brand",
    ...     primary="#8B5CF6",
    ...     google_font_name="Roboto",
    ...     font_style="sans-serif"
    ... )
    >>> html = scheme.apply_to_html(generated_html)
"""

from typing import Dict, Optional, List
from dataclasses import dataclass, field


@dataclass
class ColorScheme:
    """Defines a complete color scheme for graphics theming
    
    Includes colors, fonts (Google Fonts), and styling preferences
    for consistent theming across all graphics types.
    """
    
    name: str
    description: str = ""
    
    # Font configuration
    font_family: str = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    google_font_name: Optional[str] = None  # e.g., "Inter", "Lora", "Roboto"
    google_font_weights: str = "400;500;600;700"  # Font weights to load
    font_style: str = "sans-serif"  # "sans-serif", "serif", or "monospace"
    
    # Primary colors
    primary: str = "#2563eb"  # Main brand color
    secondary: str = "#64748b"  # Secondary/accent
    accent: str = "#1e40af"  # Highlight color
    
    # Text colors
    text_primary: str = "#1e293b"
    text_secondary: str = "#475569"
    text_tertiary: str = "#64748b"
    text_on_dark: str = "#f1f5f9"
    
    # Background colors
    bg_primary: str = "#ffffff"
    bg_secondary: str = "#f8fafc"
    bg_tertiary: str = "#f1f5f9"
    bg_dark: str = "#1e293b"
    
    # Border/divider colors
    border_light: str = "#e2e8f0"
    border_medium: str = "#cbd5e1"
    border_dark: str = "#94a3b8"
    
    # Status colors (optional - defaults to primary if not set)
    success: Optional[str] = None
    warning: Optional[str] = None
    error: Optional[str] = None
    info: Optional[str] = None
    
    # SVG color replacements (for hero slides, icons, etc.)
    svg_primary: Optional[str] = None  # Replaces purple/violet in SVGs
    svg_secondary: Optional[str] = None
    svg_accent: Optional[str] = None
    
    def __post_init__(self):
        """Set defaults for optional colors and fonts"""
        if self.success is None:
            self.success = self.primary
        if self.warning is None:
            self.warning = self.accent
        if self.error is None:
            self.error = self.accent
        if self.info is None:
            self.info = self.secondary
        
        # SVG colors default to primary/secondary/accent
        if self.svg_primary is None:
            self.svg_primary = self.primary
        if self.svg_secondary is None:
            self.svg_secondary = self.secondary
        if self.svg_accent is None:
            self.svg_accent = self.accent
        
        # Build font family if Google Font is specified
        if self.google_font_name:
            self.font_family = f"'{self.google_font_name}', {self._get_font_fallback()}"
    
    def _get_font_fallback(self) -> str:
        """Get appropriate font fallback based on font style"""
        if self.font_style == "serif":
            return "Georgia, 'Times New Roman', serif"
        elif self.font_style == "monospace":
            return "'Courier New', Courier, monospace"
        else:
            return "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    
    def get_google_fonts_link(self) -> Optional[str]:
        """Generate Google Fonts link tag if using Google Font"""
        if not self.google_font_name:
            return None
        
        # Convert weights string to format Google Fonts expects
        # Input: "400;600;700" -> Output: "wght@400;600;700"
        weights = self.google_font_weights.replace(';', ';')
        if not weights.startswith('wght@'):
            weights = f"wght@{weights}"
        
        font_name_encoded = self.google_font_name.replace(' ', '+')
        return f"<link href='https://fonts.googleapis.com/css2?family={font_name_encoded}:{weights}&display=swap' rel='stylesheet'>"
    
    def get_css_overrides(self) -> str:
        """Generate CSS overrides for all graphics types"""
        return f"""
        /* Color Scheme: {self.name} */
        
        /* Base styles */
        body {{
            font-family: {self.font_family};
            color: {self.text_primary};
            background: {self.bg_secondary};
        }}
        
        /* Apply font to all text elements */
        .hero, .hero-header, .headline, .subhead, .eyebrow,
        .stat, .stat span, .stat strong,
        .tile, .tile-label,
        .flow-node, .flow-node .node-label,
        .ribbon-panel, .ribbon-label,
        .panel, .panel-title, .panel ul,
        .slide-card, .card-title, .card-tagline, .card-subtext, .card-feature,
        .cta {{
            font-family: {self.font_family};
        }}
        
        /* Hero Slides */
        .hero {{
            background: linear-gradient(135deg, {self.bg_primary} 0%, {self.bg_secondary} 100%);
            border-color: {self.border_light};
        }}
        
        .hero-dark {{
            background: linear-gradient(145deg, {self.bg_dark}, {self._darken(self.bg_dark, 10)});
            color: {self.text_on_dark};
        }}
        
        .hero .halo {{
            background: radial-gradient(circle at 30% 25%, {self._with_alpha(self.primary, 0.15)}, transparent 55%);
        }}
        
        .hero-dark .halo {{
            background: radial-gradient(circle at 40% 20%, {self._with_alpha(self.primary, 0.25)}, transparent 60%);
        }}
        
        .eyebrow {{
            color: {self.text_tertiary};
        }}
        
        .hero-dark .eyebrow {{
            color: {self._lighten(self.text_on_dark, 20)};
        }}
        
        .headline {{
            color: {self.text_primary};
        }}
        
        .hero-dark .headline {{
            color: {self.text_on_dark};
        }}
        
        .subhead {{
            color: {self.text_secondary};
        }}
        
        .hero-dark .subhead {{
            color: {self._lighten(self.text_on_dark, 10)};
        }}
        
        /* Stats */
        .stat {{
            background: {self.bg_primary};
            border-color: {self.border_light};
        }}
        
        .hero-dark .stat {{
            background: {self._with_alpha(self.bg_primary, 0.1)};
            border-color: {self.border_medium};
        }}
        
        .stat span {{
            color: {self.text_tertiary};
        }}
        
        .hero-dark .stat span {{
            color: {self._lighten(self.text_on_dark, 20)};
        }}
        
        .stat strong {{
            color: {self.primary};
        }}
        
        .hero-dark .stat strong {{
            color: {self._lighten(self.primary, 20)};
        }}
        
        /* Tiles and highlights */
        .hero-body li {{
            background: {self.bg_primary};
            border-color: {self.border_light};
            color: {self.text_primary};
        }}
        
        .hero-dark .hero-body li {{
            background: {self._with_alpha(self.bg_primary, 0.1)};
            border-color: {self.border_medium};
            color: {self.text_on_dark};
        }}
        
        .tile {{
            background: {self.bg_primary};
            border-color: {self.border_medium};
            color: {self.text_primary};
        }}
        
        .hero-dark .tile {{
            background: {self._with_alpha(self.bg_primary, 0.1)};
            border-color: {self.border_medium};
            color: {self.text_on_dark};
        }}
        
        .tile-label {{
            color: {self.text_primary};
        }}
        
        .hero-dark .tile-label {{
            color: {self.text_on_dark};
        }}
        
        .tile::after {{
            background: linear-gradient(90deg, {self._with_alpha(self.primary, 0.15)}, {self._with_alpha(self.primary, 0.05)});
        }}
        
        /* Flowchart elements */
        .flow-node {{
            background: {self.bg_primary};
            border-color: {self.border_medium};
        }}
        
        .hero-dark .flow-node {{
            background: {self._with_alpha(self.bg_primary, 0.1)};
            border-color: {self.border_medium};
        }}
        
        .flow-node .node-label {{
            color: {self.text_primary};
        }}
        
        .hero-dark .flow-node .node-label {{
            color: {self.text_on_dark};
        }}
        
        .flow-svg path {{
            stroke: {self._with_alpha(self.primary, 0.3)};
        }}
        
        .hero-dark .flow-svg path {{
            stroke: {self._with_alpha(self.primary, 0.4)};
        }}
        
        /* Ribbon panels */
        .ribbon-panel {{
            background: {self.bg_primary};
            border-color: {self.border_medium};
            color: {self.text_primary};
        }}
        
        .hero-dark .ribbon-panel {{
            background: {self._with_alpha(self.bg_primary, 0.1)};
            border-color: {self.border_medium};
            color: {self.text_on_dark};
        }}
        
        /* CTA */
        .cta {{
            color: {self.primary};
        }}
        
        .hero-dark .cta {{
            color: {self._lighten(self.primary, 20)};
        }}
        
        /* Triptych panels */
        .panel {{
            background: linear-gradient(180deg, {self.bg_primary}, {self.bg_secondary});
            border-color: {self.border_light};
        }}
        
        .panel:nth-child(2) {{
            background: linear-gradient(180deg, {self.bg_secondary}, {self.bg_tertiary});
            border-color: {self.border_medium};
        }}
        
        .panel-title {{
            color: {self.text_primary};
        }}
        
        .panel ul {{
            color: {self.text_secondary};
        }}
        
        .panel ul li::before {{
            background: {self.primary};
        }}
        
        /* Slide Cards */
        .slide-card {{
            background: linear-gradient(135deg, {self.bg_primary} 0%, {self.bg_secondary} 100%);
            border-color: {self.border_light};
        }}
        
        .card-title {{
            color: {self.text_primary};
        }}
        
        .card-tagline {{
            color: {self.text_secondary};
        }}
        
        .card-subtext {{
            color: {self.text_tertiary};
        }}
        
        .card-feature {{
            color: {self.text_primary};
        }}
        
        .card-badge {{
            background: {self._with_alpha(self.bg_primary, 0.95)};
            color: {self.text_primary};
            border-color: {self.border_light};
        }}
        
        .card-mockup {{
            background: {self._with_alpha(self.bg_primary, 0.6)};
            border-color: {self.border_light};
        }}
        
        /* Comparison Diagram */
        .comparison .column-title {{
            color: {self.text_primary} !important;
        }}
        
        /* Left column - use error/red color scheme */
        .comparison .column.left .step {{
            background: linear-gradient(135deg, {self._with_alpha(self.error or self.primary, 0.15)} 0%, {self._with_alpha(self.error or self.primary, 0.05)} 100%) !important;
            color: {self.text_primary} !important;
        }}
        
        .comparison .column.left .outcome {{
            background: linear-gradient(135deg, {self._with_alpha(self.error or self.primary, 0.2)} 0%, {self._with_alpha(self.error or self.primary, 0.1)} 100%) !important;
            color: {self.error or self.primary} !important;
        }}
        
        /* Right column - use success/accent color scheme */
        .comparison .column.right .step {{
            background: linear-gradient(135deg, {self._with_alpha(self.success or self.accent, 0.15)} 0%, {self._with_alpha(self.success or self.accent, 0.05)} 100%) !important;
            color: {self.text_primary} !important;
        }}
        
        .comparison .column.right .outcome {{
            background: linear-gradient(135deg, {self._with_alpha(self.success or self.accent, 0.2)} 0%, {self._with_alpha(self.success or self.accent, 0.1)} 100%) !important;
            color: {self.success or self.accent} !important;
        }}
        
        .comparison .vs {{
            color: {self.text_tertiary} !important;
        }}
        
        /* Timeline Diagram */
        .timeline-container .title {{
            color: {self.text_primary} !important;
        }}
        
        /* Timeline line */
        .timeline::before {{
            background: linear-gradient(90deg, {self.primary} 0%, {self.primary} 100%) !important;
            opacity: 0.3 !important;
        }}
        
        /* Event markers on timeline - use theme primary, but allow per-event colors */
        .event-marker {{
            border-color: {self.bg_primary} !important;
        }}
        
        /* Event cards - allow per-event colors from template */
        .timeline .event-card {{
            color: {self.text_primary} !important;
        }}
        
        .timeline .event-card::after {{
            border-top-color: {self.bg_primary} !important;
        }}
        
        /* Override arrow color to match card background */
        .timeline .event-card.blue::after {{
            border-top-color: {self._with_alpha(self.primary, 0.15).replace('rgba(', '').replace(')', '').split(',')[0] if 'rgba' in str(self._with_alpha(self.primary, 0.15)) else self.bg_primary} !important;
        }}
        
        .timeline .event-date {{
            color: {self.text_tertiary} !important;
        }}
        
        .timeline .event-title {{
            color: {self.text_primary} !important;
        }}
        
        .timeline .event-description {{
            color: {self.text_tertiary} !important;
        }}
        
        /* Legacy timeline support */
        .timeline .event {{
            background: linear-gradient(135deg, {self.bg_primary} 0%, {self.bg_secondary} 100%) !important;
            color: {self.text_primary} !important;
        }}
        
        .timeline .event-text {{
            color: {self.text_primary} !important;
        }}
        
        .timeline-line {{
            background: {self.primary} !important;
            opacity: 0.4 !important;
        }}
        
        /* Grid Diagram */
        .container .title {{
            color: {self.text_primary} !important;
        }}
        
        .tests-grid .test {{
            background: linear-gradient(135deg, {self._with_alpha(self.primary, 0.1)} 0%, {self._with_alpha(self.primary, 0.05)} 100%) !important;
            color: {self.text_primary} !important;
        }}
        
        .tests-grid .test-number {{
            color: {self.primary} !important;
        }}
        
        .convergence .arrow {{
            color: {self.primary} !important;
        }}
        
        .convergence .goal {{
            color: {self.text_primary} !important;
        }}
        
        .convergence .outcome {{
            color: {self.success or self.accent} !important;
            background: linear-gradient(135deg, {self._with_alpha(self.success or self.accent, 0.1)} 0%, {self._with_alpha(self.success or self.accent, 0.05)} 100%) !important;
        }}
        
        /* Flywheel Diagram */
        .flywheel-container .title {{
            color: {self.text_primary};
        }}
        
        .flywheel-svg text {{
            font-family: {self.font_family};
            fill: {self.text_primary};
        }}
        
        .flywheel-svg circle[fill="#1D1D1F"] {{
            fill: {self.text_primary};
        }}
        
        .flywheel-svg text[fill="#FFFFFF"] {{
            fill: {self.text_on_dark};
        }}
        
        .flywheel-svg path[stroke="#C7C7CC"] {{
            stroke: {self.border_medium};
        }}
        
        .flywheel-svg path[fill="#8E8E93"] {{
            fill: {self.text_tertiary};
        }}
        """
    
    def get_svg_color_replacements(self) -> Dict[str, str]:
        """Get color replacements for SVG elements and common hardcoded colors"""
        return {
            # Purple/violet colors commonly used in default theme
            "#7C3AED": self.svg_primary,  # Purple-600
            "#A78BFA": self.svg_primary,  # Purple-400
            "#C084FC": self.svg_primary,  # Purple-400
            "#8243B5": self.primary,
            "#AF52DE": self.accent,
            "#DCD2FF": self.svg_secondary,
            "#E4D7FF": self.svg_secondary,
            "#F3E5F5": self.svg_secondary,
            "#CABAF6": self.svg_accent,
            "#DDD6FE": self.svg_accent,
            "#E0D0FF": self.svg_accent,
            "#141416": self.bg_dark or self.text_primary,
            # Common hardcoded colors in diagrams (for SVG elements and inline styles)
            "#007AFF": self.primary,  # Blue used in timeline, grid
            "#0B64D0": self.primary,
            "#1B7A4E": self.secondary,
            "#1D1D1F": self.text_primary,  # Dark text
            "#8E8E93": self.text_tertiary,  # Gray text
            "#C7C7CC": self.border_medium,  # Light gray borders
            "#34C759": self.success or self.accent,  # Green success color
            "#FF3B30": self.error or self.primary,  # Red error color
            "#F5F5F7": self.bg_secondary,  # Light grey background (comparison, timeline)
            "#EBF5FF": self.bg_secondary,  # Light blue background (grid) - overridden by CSS
            "#E3F2FD": self.bg_secondary,  # Light blue background variant (grid) - overridden by CSS
            "#F0F9F4": self.bg_secondary,  # Light green background - overridden by CSS
            "#E8F5E9": self.bg_secondary,  # Light green background variant - overridden by CSS
            # RGB values
            "rgba(124,58,237": f"rgba({self._hex_to_rgb(self.svg_primary)}",
            "rgba(167,139,250": f"rgba({self._hex_to_rgb(self.svg_primary)}",
            "rgba(192,132,252": f"rgba({self._hex_to_rgb(self.svg_primary)}",
        }
    
    def apply_to_html(self, html: str) -> str:
        """Apply color scheme to HTML by injecting CSS, fonts, and replacing SVG colors"""
        # Inject Google Fonts link if needed
        font_link = self.get_google_fonts_link()
        if font_link:
            # Insert before </head> or before first <style>
            if '</head>' in html:
                html = html.replace('</head>', f'    {font_link}\n</head>', 1)
            elif '<style>' in html:
                html = html.replace('<style>', f'{font_link}\n    <style>', 1)
        
        # Inject CSS
        css_overrides = self.get_css_overrides()
        html = html.replace('</style>', f'{css_overrides}\n    </style>', 1)
        
        # Replace SVG colors
        replacements = self.get_svg_color_replacements()
        for old_color, new_color in replacements.items():
            html = html.replace(old_color, new_color)
        
        return html
    
    def _with_alpha(self, color: str, alpha: float) -> str:
        """Convert hex color to rgba with specified alpha"""
        rgb = self._hex_to_rgb(color)
        return f"rgba({rgb}, {alpha})"
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB string"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r}, {g}, {b}"
    
    def _darken(self, hex_color: str, percent: int) -> str:
        """Darken a hex color by percent"""
        rgb = self._hex_to_rgb(hex_color).split(', ')
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        factor = 1 - (percent / 100)
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _lighten(self, hex_color: str, percent: int) -> str:
        """Lighten a hex color by percent"""
        rgb = self._hex_to_rgb(hex_color).split(', ')
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        factor = 1 + (percent / 100)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"


# Predefined color schemes
CORPORATE_SCHEME = ColorScheme(
    name="Corporate",
    description="Professional blue and gray theme for corporate presentations",
    google_font_name="Lora",
    google_font_weights="400;600;700",
    font_style="serif",
    primary="#2563eb",
    secondary="#64748b",
    accent="#1e40af",
    text_primary="#1e293b",
    text_secondary="#475569",
    text_tertiary="#64748b",
    text_on_dark="#f1f5f9",
    bg_primary="#ffffff",
    bg_secondary="#f8fafc",
    bg_tertiary="#f1f5f9",
    bg_dark="#1e293b",
    border_light="#e2e8f0",
    border_medium="#cbd5e1",
    border_dark="#94a3b8",
)

DARK_SCHEME = ColorScheme(
    name="Dark",
    description="Dark theme with bright accents",
    google_font_name="Inter",
    google_font_weights="400;500;600;700",
    font_style="sans-serif",
    primary="#60a5fa",
    secondary="#94a3b8",
    accent="#3b82f6",
    text_primary="#f1f5f9",
    text_secondary="#cbd5e1",
    text_tertiary="#94a3b8",
    text_on_dark="#f1f5f9",
    bg_primary="#1e293b",
    bg_secondary="#0f172a",
    bg_tertiary="#1e293b",
    bg_dark="#0f172a",
    border_light="#334155",
    border_medium="#475569",
    border_dark="#64748b",
)

WARM_SCHEME = ColorScheme(
    name="Warm",
    description="Warm, friendly theme with orange and amber tones",
    google_font_name="Merriweather",
    google_font_weights="400;700;900",
    font_style="serif",
    primary="#f59e0b",
    secondary="#d97706",
    accent="#ea580c",
    text_primary="#1c1917",
    text_secondary="#44403c",
    text_tertiary="#78716c",
    text_on_dark="#fef3c7",
    bg_primary="#fffbeb",
    bg_secondary="#fef3c7",
    bg_tertiary="#fde68a",
    bg_dark="#78350f",
    border_light="#fde68a",
    border_medium="#fcd34d",
    border_dark="#f59e0b",
)

GREEN_SCHEME = ColorScheme(
    name="Green",
    description="Nature-inspired green theme",
    google_font_name="Open Sans",
    google_font_weights="400;600;700",
    font_style="sans-serif",
    primary="#10b981",
    secondary="#34d399",
    accent="#059669",
    text_primary="#064e3b",
    text_secondary="#047857",
    text_tertiary="#059669",
    text_on_dark="#d1fae5",
    bg_primary="#ecfdf5",
    bg_secondary="#d1fae5",
    bg_tertiary="#a7f3d0",
    bg_dark="#065f46",
    border_light="#a7f3d0",
    border_medium="#6ee7b7",
    border_dark="#34d399",
)


def create_custom_scheme(
    name: str,
    primary: str,
    secondary: Optional[str] = None,
    accent: Optional[str] = None,
    google_font_name: Optional[str] = None,
    font_style: str = "sans-serif",
    description: str = "",
    **kwargs
) -> ColorScheme:
    """Create a custom color scheme from primary color
    
    Args:
        name: Scheme name
        primary: Primary brand color (hex)
        secondary: Secondary color (defaults to gray if not provided)
        accent: Accent color (defaults to darker primary if not provided)
        google_font_name: Google Font name (e.g., "Roboto", "Lora", "Inter")
        font_style: "sans-serif", "serif", or "monospace"
        description: Optional description
        **kwargs: Additional color overrides
    
    Returns:
        ColorScheme instance
    
    Example:
        >>> scheme = create_custom_scheme(
        ...     name="My Brand",
        ...     primary="#8B5CF6",
        ...     google_font_name="Roboto",
        ...     font_style="sans-serif"
        ... )
    """
    # Auto-generate secondary and accent if not provided
    if secondary is None:
        # Use a neutral gray
        secondary = "#64748b"
    
    if accent is None:
        # Darken primary by 20%
        scheme = ColorScheme(name="temp", primary=primary)
        accent = scheme._darken(primary, 20)
    
    return ColorScheme(
        name=name,
        description=description,
        primary=primary,
        secondary=secondary,
        accent=accent,
        google_font_name=google_font_name,
        font_style=font_style,
        **kwargs
    )


# Registry of available schemes
SCHEME_REGISTRY: Dict[str, ColorScheme] = {
    "corporate": CORPORATE_SCHEME,
    "dark": DARK_SCHEME,
    "warm": WARM_SCHEME,
    "green": GREEN_SCHEME,
}


def get_scheme(name: str) -> Optional[ColorScheme]:
    """Get a color scheme by name"""
    return SCHEME_REGISTRY.get(name.lower())


def register_scheme(scheme: ColorScheme):
    """Register a custom color scheme"""
    SCHEME_REGISTRY[scheme.name.lower()] = scheme


def list_schemes() -> List[str]:
    """List all available color scheme names"""
    return list(SCHEME_REGISTRY.keys())
