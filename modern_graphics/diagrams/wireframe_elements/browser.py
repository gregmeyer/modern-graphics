"""Browser chrome and window SVG element builders."""

from typing import Optional
from .config import WireframeConfig


def render_browser_chrome(
    config: WireframeConfig,
    x: int = 20,
    y: int = 20,
    width: Optional[int] = None,
    url: str = "app.example.com/dashboard"
) -> str:
    """Render browser chrome with traffic lights and URL bar.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position  
        width: Width (defaults to config.width - 2*padding)
        url: URL to display in address bar
        
    Returns:
        SVG group element string
    """
    w = width or (config.width - 2 * config.padding)
    c = config.colors
    chrome_h = config.chrome_height
    r = config.corner_radius
    
    return f"""
  <g class="browser-chrome">
    <!-- Chrome background with rounded top -->
    <rect x="{x}" y="{y}" width="{w}" height="{chrome_h}" rx="{r}" fill="url(#browserGrad)"/>
    <rect x="{x}" y="{y + chrome_h - r}" width="{w}" height="{r}" fill="url(#browserGrad)"/>
    <line x1="{x}" y1="{y + chrome_h}" x2="{x + w}" y2="{y + chrome_h}" stroke="{c.chrome_border}" stroke-width="1"/>
    
    <!-- Traffic lights -->
    <circle cx="{x + 28}" cy="{y + chrome_h // 2}" r="6" fill="{c.traffic_light}"/>
    <circle cx="{x + 48}" cy="{y + chrome_h // 2}" r="6" fill="{c.traffic_light}"/>
    <circle cx="{x + 68}" cy="{y + chrome_h // 2}" r="6" fill="{c.traffic_light}"/>
    
    <!-- URL bar -->
    <rect x="{x + 110}" y="{y + 10}" width="{min(240, w - 150)}" height="{chrome_h - 20}" rx="6" fill="{c.surface_primary}" stroke="{c.chrome_border}"/>
    <text x="{x + 126}" y="{y + chrome_h // 2 + 4}" font-family="{config.font_family}" font-size="{config.font_size_label}" fill="{c.text_tertiary}">{url}</text>
  </g>
    """


def render_browser_window(
    config: WireframeConfig,
    x: int = 20,
    y: int = 20,
    width: Optional[int] = None,
    height: Optional[int] = None,
    url: str = "app.example.com/dashboard",
    content_bg: Optional[str] = None
) -> str:
    """Render complete browser window frame.
    
    Args:
        config: Wireframe configuration
        x: X position
        y: Y position
        width: Width (defaults to config.width - 2*padding)
        height: Height (defaults to config.height - 2*padding - 100)
        url: URL to display
        content_bg: Background color for content area (defaults to surface_secondary)
        
    Returns:
        SVG group element string with browser frame
    """
    w = width or (config.width - 2 * config.padding)
    h = height or (config.height - 2 * config.padding - 100)
    c = config.colors
    chrome_h = config.chrome_height
    r = config.corner_radius
    bg = content_bg or c.surface_secondary
    
    chrome = render_browser_chrome(config, x, y, w, url)
    
    return f"""
  <g class="browser-window" filter="url(#cardShadow)">
    <!-- Window background -->
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c.surface_primary}"/>
    
    {chrome}
    
    <!-- Content area -->
    <rect x="{x}" y="{y + chrome_h}" width="{w}" height="{h - chrome_h}" fill="{bg}"/>
    
    <!-- Bottom rounded corners mask -->
    <rect x="{x}" y="{y + h - r}" width="{w}" height="{r}" rx="{r}" fill="{bg}"/>
  </g>
    """
