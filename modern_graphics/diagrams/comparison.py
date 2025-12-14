"""Comparison diagram generator"""

from typing import Dict
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def generate_comparison_diagram(
    generator: BaseGenerator,
    left_column: Dict[str, any],
    right_column: Dict[str, any],
    vs_text: str = "vs"
) -> str:
    """Generate a comparison diagram (two columns with steps)"""
    def generate_column_html(column_data: Dict, column_class: str) -> str:
        title = column_data['title']
        steps = column_data['steps']
        html = f'        <div class="column {column_class}">\n            <div class="column-title">{title}</div>\n'
        
        for step in steps:
            step_text = step if isinstance(step, str) else step.get('text', step)
            html += f'            <div class="step">{step_text}</div>\n'
        
        outcome = column_data.get('outcome')
        if outcome:
            html += f'            <div class="outcome">{outcome}</div>\n'
        
        html += '        </div>'
        return html
    
    left_class = left_column.get('class', 'left')
    right_class = right_column.get('class', 'right')
    
    css_content = f"""
        .comparison {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 48px;
            align-items: start;
            max-width: 1000px;
            width: 100%;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            max-width: 1000px;
            width: 100%;
        }}
        
        .column {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        
        .column-title {{
            font-size: 21px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}
        
        .step {{
            background: linear-gradient(135deg, #F5F5F7 0%, #F5F5F7 100%);
            border: none;
            border-radius: 14px;
            padding: 20px 24px;
            font-size: 16px;
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.01em;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
        }}
        
        .outcome {{
            margin-top: 16px;
            font-size: 17px;
            font-weight: 600;
            color: #1D1D1F;
            padding: 16px 24px;
            border-radius: 14px;
            background: linear-gradient(135deg, #F5F5F7 0%, #F5F5F7 100%);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
        }}
        
        .vs {{
            font-size: 18px;
            font-weight: 600;
            color: #8E8E93;
            align-self: center;
            padding: 0 16px;
        }}
        
        .column.{left_class} .outcome {{
            color: #FF3B30;
        }}
        
        .column.{right_class} .outcome {{
            color: #34C759;
        }}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top}px;
            font-size: 12px;
            font-weight: 500;
            color: #C7C7CC;
            letter-spacing: -0.01em;
            text-align: right;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="wrapper">
    <div class="comparison">
{generate_column_html(left_column, left_class)}
        
        <div class="vs">{vs_text}</div>
        
{generate_column_html(right_column, right_class)}
    </div>
    {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
