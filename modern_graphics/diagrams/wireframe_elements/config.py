"""Configuration classes for wireframe diagrams.

Provides WireframeConfig and WireframeColors that can be derived
from a ColorScheme or used standalone with sensible defaults.
"""

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ...color_scheme import ColorScheme


@dataclass
class WireframeColors:
    """Color palette for wireframe elements.
    
    Can be created from a ColorScheme or used with defaults.
    """
    # Chrome/browser colors
    chrome_bg: str = "#f5f5f7"
    chrome_border: str = "#e8e8ed"
    traffic_light: str = "#d2d2d7"
    
    # Surface colors
    surface_primary: str = "#ffffff"
    surface_secondary: str = "#f5f5f7"
    surface_tertiary: str = "#fafafa"
    
    # Text colors
    text_primary: str = "#1d1d1f"
    text_secondary: str = "#6e6e73"
    text_tertiary: str = "#86868b"
    text_placeholder: str = "#86868b"
    
    # Border colors
    border_light: str = "#e8e8ed"
    border_medium: str = "#d2d2d7"
    
    # Accent colors
    accent_blue: str = "#0071e3"
    accent_green: str = "#34c759"
    accent_red: str = "#ff3b30"
    
    # Skeleton/placeholder colors
    skeleton_primary: str = "#e8e8ed"
    skeleton_secondary: str = "#f5f5f7"
    
    # Shadow colors (for filter definitions)
    shadow_color: str = "rgba(0,0,0,0.08)"
    shadow_color_medium: str = "rgba(0,0,0,0.12)"
    shadow_color_heavy: str = "rgba(0,0,0,0.15)"
    
    @classmethod
    def from_color_scheme(cls, scheme: "ColorScheme") -> "WireframeColors":
        """Create WireframeColors from a ColorScheme instance."""
        return cls(
            chrome_bg=scheme.bg_secondary,
            chrome_border=scheme.border_light,
            traffic_light=scheme.border_medium,
            surface_primary=scheme.bg_primary,
            surface_secondary=scheme.bg_secondary,
            surface_tertiary=scheme.bg_tertiary,
            text_primary=scheme.text_primary,
            text_secondary=scheme.text_secondary,
            text_tertiary=scheme.text_tertiary,
            text_placeholder=scheme.text_tertiary,
            border_light=scheme.border_light,
            border_medium=scheme.border_medium,
            accent_blue=scheme.primary,
            accent_green=scheme.success or "#34c759",
            accent_red=scheme.error or "#ff3b30",
            skeleton_primary=scheme.border_light,
            skeleton_secondary=scheme.bg_secondary,
        )


# Predefined color palettes
APPLE_COLORS = WireframeColors(
    chrome_bg="#f5f5f7",
    chrome_border="#e8e8ed",
    traffic_light="#d2d2d7",
    surface_primary="#ffffff",
    surface_secondary="#f5f5f7",
    surface_tertiary="#fafafa",
    text_primary="#1d1d1f",
    text_secondary="#6e6e73",
    text_tertiary="#86868b",
    text_placeholder="#86868b",
    border_light="#e8e8ed",
    border_medium="#d2d2d7",
    accent_blue="#0071e3",
    accent_green="#34c759",
    accent_red="#ff3b30",
    skeleton_primary="#e8e8ed",
    skeleton_secondary="#f5f5f7",
)

MATERIAL_COLORS = WireframeColors(
    chrome_bg="#fafafa",
    chrome_border="#e0e0e0",
    traffic_light="#bdbdbd",
    surface_primary="#ffffff",
    surface_secondary="#fafafa",
    surface_tertiary="#f5f5f5",
    text_primary="#212121",
    text_secondary="#757575",
    text_tertiary="#9e9e9e",
    text_placeholder="#9e9e9e",
    border_light="#e0e0e0",
    border_medium="#bdbdbd",
    accent_blue="#1976d2",
    accent_green="#4caf50",
    accent_red="#f44336",
    skeleton_primary="#e0e0e0",
    skeleton_secondary="#f5f5f5",
)


@dataclass
class WireframeConfig:
    """Configuration for wireframe rendering.
    
    Controls dimensions, styling, and color palette.
    """
    # Dimensions
    width: int = 600
    height: int = 520
    
    # Browser chrome settings
    chrome_height: int = 40
    corner_radius: int = 20
    
    # Spacing
    padding: int = 20
    gap: int = 16
    
    # Typography
    font_family: str = "Inter, SF Pro Display, -apple-system, sans-serif"
    font_size_label: int = 9
    font_size_title: int = 12
    font_size_body: int = 10
    
    # Style variant
    style: str = "apple"  # "apple", "material", "minimal"
    
    # Colors
    colors: WireframeColors = field(default_factory=lambda: APPLE_COLORS)
    
    @classmethod
    def from_color_scheme(
        cls,
        scheme: "ColorScheme",
        width: int = 600,
        height: int = 520,
        style: str = "apple"
    ) -> "WireframeConfig":
        """Create WireframeConfig from a ColorScheme instance."""
        colors = WireframeColors.from_color_scheme(scheme)
        font_family = scheme.font_family
        
        return cls(
            width=width,
            height=height,
            style=style,
            colors=colors,
            font_family=font_family,
        )
    
    def get_filter_defs(self) -> str:
        """Generate SVG filter definitions for shadows."""
        return f"""
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.08"/>
    </filter>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="20" flood-opacity="0.12"/>
    </filter>
    <filter id="modalShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="20" stdDeviation="30" flood-opacity="0.2"/>
    </filter>
    <linearGradient id="browserGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{self.colors.surface_tertiary}"/>
      <stop offset="100%" stop-color="{self.colors.chrome_bg}"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{self.colors.accent_blue}"/>
      <stop offset="100%" stop-color="{self._darken_color(self.colors.accent_blue, 10)}"/>
    </linearGradient>
        """
    
    def _darken_color(self, hex_color: str, percent: int) -> str:
        """Darken a hex color by percent."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        factor = 1 - (percent / 100)
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
