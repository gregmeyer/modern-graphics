"""Funnel diagram generator"""

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


def _get_stage_gradient(
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


def generate_funnel_diagram(
    generator: BaseGenerator,
    stages: List[Dict[str, Any]],
    show_percentages: bool = False,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a modern funnel diagram"""
    if not stages:
        stages = [
            {"text": "Awareness", "value": 1000, "color": "blue"},
            {"text": "Consideration", "value": 520, "color": "green"},
            {"text": "Trial", "value": 260, "color": "purple"},
            {"text": "Purchase", "value": 130, "color": "orange"}
        ]
    
    theme = extract_theme_colors(color_scheme)
    max_value = max(stage.get("value", 0) for stage in stages) or 1
    min_width = 45
    max_width = 92
    step = (max_width - min_width) / max(len(stages) - 1, 1)
        
    stage_html = []
    for idx, stage in enumerate(stages):
        color_key = stage.get("color", "blue")
        gradient, shadow = _get_stage_gradient(generator, color_key, theme)
        value = stage.get("value", 0)
        pct = (value / max_value) * 100
        width_pct = max_width - (idx * step)
        value_label = f"{pct:.0f}%" if show_percentages else f"{value:,}"
        border_color = with_alpha(theme.text_tertiary, 0.2)
        stage_html.append(f"""
            <div class="funnel-stage" style="width: {width_pct}%; background: {gradient}; box-shadow: {shadow}; border: 1px solid {border_color};">
                <div class="stage-info">
                    <div class="stage-label">{stage.get("text", "Stage")}</div>
                    <div class="stage-value">{value_label}</div>
                </div>
            </div>
        """)
    
    conversion = (stages[-1].get("value", 0) / stages[0].get("value", 1)) * 100
    template = _get_template(generator)
    css_content = f"""
        {generate_css_variables(theme)}
        
        body {{
            font-family: var(--font-body);
            background: var(--bg-page);
            margin: 0;
            padding: 60px 20px;
            display: flex;
            justify-content: center;
        }}
        
        .funnel-wrapper {{
            max-width: 900px;
            width: 100%;
            background: var(--bg-card);
            border-radius: 32px;
            padding: 48px 60px 60px;
            box-shadow: 0 30px 70px {with_alpha(theme.text_primary, 0.12)};
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
            color: var(--text-1);
            letter-spacing: -0.02em;
        }}
        
        .funnel-metric {{
            text-align: right;
        }}
        
        .funnel-metric .label {{
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.1em;
            color: var(--text-2);
            font-weight: 600;
        }}
        
        .funnel-metric .value {{
            font-size: 26px;
            font-weight: 700;
            color: var(--text-1);
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
            color: var(--text-1);
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
            color: var(--text-1);
        }}
        
        .stage-value {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-1);
        }}
        
        .funnel-notes {{
            margin-top: 24px;
            font-size: 14px;
            color: var(--text-2);
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
    
    full_html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(full_html, theme)
