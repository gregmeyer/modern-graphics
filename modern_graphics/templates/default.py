"""Default template - modern, clean style"""

from .base import StyleTemplate
from ..constants import MODERN_COLORS, BASE_STYLES, ATTRIBUTION_STYLES

DEFAULT_TEMPLATE = StyleTemplate(
    name="default",
    colors=MODERN_COLORS,
    base_styles=BASE_STYLES,
    attribution_styles=ATTRIBUTION_STYLES,
    font_family="'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    background_color="#FFFFFF"
)
