"""Grid diagram generator"""

from typing import List, Dict, Optional
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def generate_grid_diagram(
    generator: BaseGenerator,
    items: List[Dict[str, any]],
    columns: int = 5,
    convergence: Optional[Dict[str, str]] = None
) -> str:
    """Generate a grid diagram (like five tests)"""
    items_html = []
    for item in items:
        number = item.get('number')
        text = item['text']
        if number:
            items_html.append(f"""
            <div class="test">
                <div class="test-number">{number}</div>
                <div>{text}</div>
            </div>""")
        else:
            items_html.append(f'            <div class="test">{text}</div>')
    
    convergence_html = ""
    if convergence:
        convergence_html = f"""
        <div class="convergence">
            <div class="arrow">↓</div>
            <div class="goal">{convergence.get('goal', '')}</div>
            <div class="arrow">↓</div>
            <div class="outcome">{convergence.get('outcome', '')}</div>
        </div>"""
    
    css_content = f"""
        .container {{
            max-width: 900px;
            width: 100%;
        }}
        
        .title {{
            font-size: 24px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 32px;
            text-align: center;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .tests-grid {{
            display: grid;
            grid-template-columns: repeat({columns}, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }}
        
        .test {{
            background: linear-gradient(135deg, #EBF5FF 0%, #E3F2FD 100%);
            border: none;
            border-radius: 14px;
            padding: 20px 16px;
            text-align: center;
            font-size: 15px;
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.01em;
            line-height: 1.4;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .test-number {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #007AFF;
            letter-spacing: -0.02em;
        }}
        
        .convergence {{
            text-align: center;
            margin: 32px 0;
        }}
        
        .arrow {{
            color: #007AFF;
            font-size: 24px;
            margin: 12px 0;
            font-weight: 600;
        }}
        
        .goal {{
            font-size: 19px;
            font-weight: 600;
            color: #1D1D1F;
            margin: 16px 0;
            letter-spacing: -0.01em;
        }}
        
        .outcome {{
            font-size: 19px;
            font-weight: 600;
            color: #34C759;
            margin-top: 16px;
            padding: 20px 32px;
            background: linear-gradient(135deg, #F0F9F4 0%, #E8F5E9 100%);
            border-radius: 14px;
            display: inline-block;
            letter-spacing: -0.01em;
            box-shadow: 0 2px 8px rgba(52, 199, 89, 0.12), 0 8px 24px rgba(52, 199, 89, 0.08);
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
    <div class="container">
        <div class="title">{generator.title}</div>
        <div class="tests-grid">
{''.join(items_html)}
        </div>{convergence_html}
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
