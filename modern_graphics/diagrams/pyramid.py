"""Pyramid diagram generator"""

from typing import List, Dict, Any
from ..base import BaseGenerator


def _get_template(generator: BaseGenerator):
    return getattr(generator, "template", generator.template)


def _hex_to_rgb(color: str):
    color = color.lstrip('#')
    if len(color) == 3:
        color = ''.join(ch * 2 for ch in color)
    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))


def _calculate_luminance(color: str) -> float:
    r, g, b = [v / 255 for v in _hex_to_rgb(color)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _is_dark_theme(template) -> bool:
    bg = getattr(template, "background_color", "#FFFFFF")
    return _calculate_luminance(bg) < 0.5


def _layer_gradient(generator: BaseGenerator, color_key: str) -> str:
    template = _get_template(generator)
    start, end = template.get_gradient(color_key or "blue")
    return f"linear-gradient(135deg, {start}, {end})", template.get_shadow(color_key or "blue")


def generate_pyramid_diagram(
    generator: BaseGenerator,
    layers: List[Dict[str, Any]],
    orientation: str = "up"
) -> str:
    """Generate a layered pyramid diagram"""
    if not layers:
        layers = [
            {"text": "Vision", "color": "purple"},
            {"text": "Strategy", "color": "blue"},
            {"text": "Execution", "color": "green"},
            {"text": "Impact", "color": "orange"}
        ]
    
    template = _get_template(generator)
    dark_theme = _is_dark_theme(template)
    primary_text = "#F8FAFC" if dark_theme else "#0F172A"
    secondary_text = "rgba(248,250,252,0.75)" if dark_theme else "#6B7280"
    layer_count = len(layers)
    min_width = 40
    max_width = 92
    step = (max_width - min_width) / max(layer_count - 1, 1)
    
    html_layers = []
    for idx, layer in enumerate(layers):
        color_key = layer.get("color", "blue")
        gradient, shadow = _layer_gradient(generator, color_key)
        width_index = idx if orientation == "up" else (layer_count - 1 - idx)
        width_pct = min_width + (width_index * step)
        html_layers.append(f"""
            <div class="pyramid-layer orientation-{orientation}" style="width: {width_pct}%; background: {gradient}; box-shadow: {shadow}; border: 1px solid rgba(0,0,0,0.08);">
                <div class="layer-label">{layer.get("text", "Layer")}</div>
            </div>
        """)
    
    css_content = f"""
        body {{
            font-family: {template.font_family}, -apple-system, BlinkMacSystemFont, sans-serif;
            background: #F5F5F7;
            padding: 60px 20px;
            margin: 0;
            display: flex;
            justify-content: center;
        }}
        
        .pyramid-wrapper {{
            width: 100%;
            max-width: 900px;
            background: #FFFFFF;
            border-radius: 32px;
            padding: 48px 60px 60px;
            box-shadow: 0 30px 70px rgba(15, 23, 42, 0.12);
        }}
        
        .pyramid-header {{
            text-align: center;
            margin-bottom: 32px;
        }}
        
        .pyramid-title {{
            font-size: 28px;
            font-weight: 700;
            color: {primary_text};
            letter-spacing: -0.02em;
        }}
        
        .pyramid-subtitle {{
            font-size: 15px;
            color: {secondary_text};
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
            color: {primary_text};
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
            color: {secondary_text};
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
    
    return generator._wrap_html(html_content, css_content)
