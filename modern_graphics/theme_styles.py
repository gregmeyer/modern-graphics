"""Theme-aware style resolver for layout rendering.

Provides resolved CSS values based on ColorScheme properties, allowing
layouts to use theme-driven values instead of hardcoding shadows,
border-radius, and spacing.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .color_scheme import BORDER_RADIUS_PRESETS, SHADOW_PRESETS


DEFAULT_STYLES = {
    "radius_sm": "8px",
    "radius_md": "16px",
    "radius_lg": "24px",
    "radius_xl": "32px",
    "radius_pill": "999px",
    "shadow_container": "0 8px 32px rgba(0,0,0,0.1), 0 2px 8px rgba(0,0,0,0.06)",
    "shadow_card": "0 4px 16px rgba(0,0,0,0.08)",
    "heading_scale": 1.0,
    "spacing_scale": 1.0,
}


def resolve_styles(scheme: Optional[Any] = None) -> Dict[str, Any]:
    """Resolve theme properties into CSS-ready values.

    Args:
        scheme: ColorScheme instance, or None for defaults.

    Returns:
        Dict with resolved radius, shadow, and scale values.
    """
    if scheme is None:
        return dict(DEFAULT_STYLES)

    border_style = getattr(scheme, "border_style", "soft")
    shadow_depth = getattr(scheme, "shadow_depth", "medium")

    radii = BORDER_RADIUS_PRESETS.get(border_style, BORDER_RADIUS_PRESETS["soft"])
    shadows = SHADOW_PRESETS.get(shadow_depth, SHADOW_PRESETS["medium"])

    return {
        "radius_sm": radii["sm"],
        "radius_md": radii["md"],
        "radius_lg": radii["lg"],
        "radius_xl": radii["xl"],
        "radius_pill": radii["pill"],
        "shadow_container": shadows["container"],
        "shadow_card": shadows["card"],
        "heading_scale": getattr(scheme, "heading_scale", 1.0),
        "spacing_scale": getattr(scheme, "spacing_scale", 1.0),
    }
