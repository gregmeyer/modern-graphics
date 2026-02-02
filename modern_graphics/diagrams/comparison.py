"""Comparison diagram generator - Modern redesign with theming support"""

from typing import Dict, Optional, TYPE_CHECKING
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from .theme_utils import extract_theme_colors, generate_css_variables, inject_google_fonts, with_alpha

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def generate_comparison_diagram(
    generator: BaseGenerator,
    left_column: Dict[str, any],
    right_column: Dict[str, any],
    vs_text: str = "vs",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a modern comparison diagram (two columns with steps).
    
    Args:
        generator: BaseGenerator instance
        left_column: Dict with 'title', 'steps', optional 'outcome', 'class'
        right_column: Dict with 'title', 'steps', optional 'outcome', 'class'
        vs_text: Text between columns (default: "vs")
        color_scheme: Optional ColorScheme for theming
        
    Returns:
        HTML string
    """
    # Extract theme colors
    theme = extract_theme_colors(color_scheme)
    
    def generate_column_html(column_data: Dict, column_class: str, is_positive: bool) -> str:
        title = column_data['title']
        steps = column_data['steps']
        icon = "✕" if not is_positive else "✓"
        
        html = f'''        <div class="column {column_class}">
            <div class="column-header">
                <div class="column-icon">{icon}</div>
                <div class="column-title">{title}</div>
            </div>
            <div class="steps-container">
'''
        
        for i, step in enumerate(steps):
            step_text = step if isinstance(step, str) else step.get('text', step)
            html += f'                <div class="step"><span class="step-bullet">•</span>{step_text}</div>\n'
        
        html += '            </div>\n'
        
        outcome = column_data.get('outcome')
        if outcome:
            html += f'            <div class="outcome">{outcome}</div>\n'
        
        html += '        </div>'
        return html
    
    left_class = left_column.get('class', 'left')
    right_class = right_column.get('class', 'right')
    
    # Generate shadow based on theme
    shadow = "0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.04)"
    if theme.is_dark:
        shadow = "0 4px 24px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.2)"
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        .comparison {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 32px;
            align-items: stretch;
            max-width: 1000px;
            width: 100%;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 1000px;
            width: 100%;
            padding: 40px;
        }}
        
        .title {{
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 700;
            color: var(--text-1);
            margin-bottom: 32px;
            letter-spacing: -0.03em;
            text-align: center;
        }}
        
        .column {{
            display: flex;
            flex-direction: column;
            background: var(--bg-card);
            border: {theme.card_border};
            border-radius: 20px;
            padding: 28px;
            box-shadow: {shadow};
            position: relative;
            overflow: hidden;
        }}
        
        .column::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
        }}
        
        .column.{left_class}::before {{
            background: linear-gradient(90deg, var(--error), {with_alpha(theme.error, 0.6)});
        }}
        
        .column.{right_class}::before {{
            background: linear-gradient(90deg, var(--success), {with_alpha(theme.success, 0.6)});
        }}
        
        .column-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid {with_alpha(theme.text_tertiary, 0.2)};
        }}
        
        .column-icon {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 700;
        }}
        
        .column.{left_class} .column-icon {{
            background: {with_alpha(theme.error, 0.15)};
            color: var(--error);
        }}
        
        .column.{right_class} .column-icon {{
            background: {with_alpha(theme.success, 0.15)};
            color: var(--success);
        }}
        
        .column-title {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.02em;
        }}
        
        .steps-container {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            flex: 1;
        }}
        
        .step {{
            font-family: var(--font-body);
            font-size: 15px;
            font-weight: 500;
            color: var(--text-2);
            letter-spacing: -0.01em;
            line-height: 1.5;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }}
        
        .step-bullet {{
            color: var(--text-3);
            font-size: 12px;
            line-height: 1.8;
        }}
        
        .outcome {{
            margin-top: 20px;
            padding: 16px 20px;
            border-radius: 12px;
            font-family: var(--font-body);
            font-size: 16px;
            font-weight: 600;
            letter-spacing: -0.01em;
        }}
        
        .column.{left_class} .outcome {{
            background: {with_alpha(theme.error, 0.1)};
            color: var(--error);
        }}
        
        .column.{right_class} .outcome {{
            background: {with_alpha(theme.success, 0.1)};
            color: var(--success);
        }}
        
        .vs {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .vs-circle {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--bg-card);
            border: 2px solid {with_alpha(theme.text_tertiary, 0.2)};
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 700;
            color: var(--text-3);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top}px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-3);
            letter-spacing: -0.01em;
            text-align: right;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="wrapper">
    <div class="title">{generator.title}</div>
    <div class="comparison">
{generate_column_html(left_column, left_class, False)}
        
        <div class="vs">
            <div class="vs-circle">{vs_text}</div>
        </div>
        
{generate_column_html(right_column, right_class, True)}
    </div>
    {generator._generate_attribution_html()}
    </div>
        """
    
    html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(html, theme)
