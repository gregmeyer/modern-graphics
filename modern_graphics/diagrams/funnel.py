"""Funnel diagram generator"""

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


def _get_stage_gradient(generator: BaseGenerator, color_key: str) -> str:
    template = _get_template(generator)
    start, end = template.get_gradient(color_key or "blue")
    return f"linear-gradient(135deg, {start}, {end})", template.get_shadow(color_key or "blue")


def generate_funnel_diagram(
    generator: BaseGenerator,
    stages: List[Dict[str, Any]],
    show_percentages: bool = False
) -> str:
    """Generate a modern funnel diagram"""
    if not stages:
        stages = [
            {"text": "Awareness", "value": 1000, "color": "blue"},
            {"text": "Consideration", "value": 520, "color": "green"},
            {"text": "Trial", "value": 260, "color": "purple"},
            {"text": "Purchase", "value": 130, "color": "orange"}
        ]
    
    max_value = max(stage.get("value", 0) for stage in stages) or 1
    min_width = 45
    max_width = 92
    step = (max_width - min_width) / max(len(stages) - 1, 1)
    template = _get_template(generator)
    dark_theme = _is_dark_theme(template)
    primary_text = "#F8FAFC" if dark_theme else "#0F172A"
    secondary_text = "rgba(248,250,252,0.75)" if dark_theme else "#6B7280"
        
    stage_html = []
    for idx, stage in enumerate(stages):
        color_key = stage.get("color", "blue")
        gradient, shadow = _get_stage_gradient(generator, color_key)
        value = stage.get("value", 0)
        pct = (value / max_value) * 100
        width_pct = max_width - (idx * step)
        value_label = f"{pct:.0f}%" if show_percentages else f"{value:,}"
        stage_html.append(f"""
            <div class="funnel-stage" style="width: {width_pct}%; background: {gradient}; box-shadow: {shadow}; border: 1px solid rgba(0,0,0,0.08);">
                <div class="stage-info">
                    <div class="stage-label">{stage.get("text", "Stage")}</div>
                    <div class="stage-value">{value_label}</div>
                </div>
            </div>
        """)
    
    conversion = (stages[-1].get("value", 0) / stages[0].get("value", 1)) * 100
    css_content = f"""
        body {{
            font-family: {template.font_family}, -apple-system, BlinkMacSystemFont, sans-serif;
            background: #F5F5F7;
            margin: 0;
            padding: 60px 20px;
            display: flex;
            justify-content: center;
        }}
        
        .funnel-wrapper {{
            max-width: 900px;
            width: 100%;
            background: #FFFFFF;
            border-radius: 32px;
            padding: 48px 60px 60px;
            box-shadow: 0 30px 70px rgba(15, 23, 42, 0.12);
        }}
        
        .funnel-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 32px;
        }}
        
        .funnel-title {{
            font-size: 28px;
            font-weight: 700;
            color: {primary_text};
            letter-spacing: -0.02em;
        }}
        
        .funnel-metric {{
            text-align: right;
        }}
        
        .funnel-metric .label {{
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.1em;
            color: {secondary_text};
            font-weight: 600;
        }}
        
        .funnel-metric .value {{
            font-size: 26px;
            font-weight: 700;
            color: {primary_text};
        }}
        
        .funnel-stages {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 18px;
        }}
        
        .funnel-stage {{
            position: relative;
            padding: 18px 28px;
            border-radius: 18px;
            clip-path: polygon(6% 0%, 94% 0%, 100% 100%, 0% 100%);
            color: {primary_text};
        }}
        
        .stage-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
        }}
        
        .stage-label {{
            font-size: 18px;
            letter-spacing: -0.01em;
            color: {primary_text};
        }}
        
        .stage-value {{
            font-size: 20px;
            font-weight: 700;
            color: {primary_text};
        }}
        
        .funnel-notes {{
            margin-top: 24px;
            font-size: 14px;
            color: {secondary_text};
            line-height: 1.5;
        }}
        
        {template.attribution_styles}
    """
    
    html_content = f"""
    <div class="funnel-wrapper">
        <div class="funnel-header">
            <div class="funnel-title">{generator.title}</div>
            <div class="funnel-metric">
                <div class="label">Overall Conversion</div>
                <div class="value">{conversion:.1f}%</div>
            </div>
        </div>
        <div class="funnel-stages">
            {''.join(stage_html)}
        </div>
        <div class="funnel-notes">
            {generator._generate_attribution_html()}
        </div>
    </div>
    """
    
    return generator._wrap_html(html_content, css_content)
