"""Pyramid diagram generator"""

from typing import List, Dict, Any, Optional, TYPE_CHECKING, Tuple
from ..base import BaseGenerator
from .theme_utils import (
    extract_theme_colors,
    generate_css_variables,
    inject_google_fonts,
    with_alpha,
)

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def _get_template(generator: BaseGenerator):
    return getattr(generator, "template", generator.template)


def _layer_gradient(
    generator: BaseGenerator, color_key: str, theme: Any
) -> Tuple[str, str]:
    """Return (gradient_css, shadow_css). Use template gradient when available, else theme accent."""
    template = _get_template(generator)
    color_key = color_key or "blue"
    try:
        if template and hasattr(template, "get_gradient"):
            start, end = template.get_gradient(color_key)
            gradient = f"linear-gradient(135deg, {start}, {end})"
        else:
            gradient = f"linear-gradient(135deg, {theme.accent}, {theme.accent})"
    except Exception:
        gradient = f"linear-gradient(135deg, {theme.accent}, {theme.accent})"
    try:
        if template and hasattr(template, "get_shadow"):
            shadow = template.get_shadow(color_key)
        else:
            shadow = f"0 4px 12px {with_alpha(theme.accent, 0.2)}"
    except Exception:
        shadow = f"0 4px 12px {with_alpha(theme.accent, 0.2)}"
    return gradient, shadow


def generate_pyramid_diagram(
    generator: BaseGenerator,
    layers: List[Dict[str, Any]],
    orientation: str = "up",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a layered pyramid diagram"""
    if not layers:
        layers = [
            {"text": "Vision", "color": "purple"},
            {"text": "Strategy", "color": "blue"},
            {"text": "Execution", "color": "green"},
            {"text": "Impact", "color": "orange"}
        ]
    
    theme = extract_theme_colors(color_scheme)
    template = _get_template(generator)
    layer_count = len(layers)
    min_width = 40
    max_width = 92
    step = (max_width - min_width) / max(layer_count - 1, 1)
    
    html_layers = []
    for idx, layer in enumerate(layers):
        color_key = layer.get("color", "blue")
        gradient, shadow = _layer_gradient(generator, color_key, theme)
        width_index = idx if orientation == "up" else (layer_count - 1 - idx)
        width_pct = min_width + (width_index * step)
        border_color = with_alpha(theme.text_tertiary, 0.2)
        html_layers.append(f"""
            <div class="pyramid-layer orientation-{orientation}" style="width: {width_pct}%; background: {gradient}; box-shadow: {shadow}; border: 1px solid {border_color};">
                <div class="layer-label">{layer.get("text", "Layer")}</div>
            </div>
        """)
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        body {{
            font-family: var(--font-body);
            background: var(--bg-page);
            padding: 60px 20px;
            margin: 0;
            display: flex;
            justify-content: center;
        }}
        
        .pyramid-wrapper {{
            width: 100%;
            max-width: 900px;
            background: var(--bg-card);
            border-radius: 32px;
            padding: 48px 60px 60px;
            box-shadow: 0 30px 70px {with_alpha(theme.text_primary, 0.12)};
        }}
        
        .pyramid-header {{
            text-align: center;
            margin-bottom: 32px;
        }}
        
        .pyramid-title {{
            font-size: 28px;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.02em;
        }}
        
        .pyramid-subtitle {{
            font-size: 15px;
            color: var(--text-2);
            margin-top: 6px;
        }}
        
        .pyramid-layers {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 14px;
        }}
        
        .pyramid-layer {{
            height: 72px;
            border-radius: 20px;
            clip-path: polygon(10% 0%, 90% 0%, 100% 100%, 0% 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-1);
            font-weight: 600;
            letter-spacing: -0.01em;
            font-size: 17px;
            text-transform: capitalize;
        }}
        
        .pyramid-layer.orientation-down {{
            clip-path: polygon(0% 0%, 100% 0%, 90% 100%, 10% 100%);
        }}
        
        .pyramid-footer {{
            margin-top: 28px;
            font-size: 13px;
            color: var(--text-2);
            text-align: center;
        }}
        
        {template.attribution_styles}
    """
    
    orientation_text = "Ascending priorities" if orientation == "up" else "Inverted stack"
    html_content = f"""
    <div class="pyramid-wrapper">
        <div class="pyramid-header">
            <div class="pyramid-title">{generator.title}</div>
            <div class="pyramid-subtitle">{orientation_text}</div>
        </div>
        <div class="pyramid-layers">
            {''.join(html_layers)}
        </div>
        <div class="pyramid-footer">
            {generator._generate_attribution_html()}
        </div>
    </div>
    """
    
    full_html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(full_html, theme)
