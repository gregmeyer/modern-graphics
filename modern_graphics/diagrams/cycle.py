"""Cycle diagram generator"""

from typing import List, Dict, Optional
from ..base import BaseGenerator
from .base import DiagramGenerator
from ..utils import generate_step_style


def generate_cycle_diagram(
    generator: BaseGenerator,
    steps: List[Dict[str, any]],
    arrow_text: str = "→",
    cycle_end_text: Optional[str] = None,
    attribution_on_last: bool = True
) -> str:
    """Generate a cycle/flow diagram"""
    html_steps = []
    css_steps = []
    
    for i, step in enumerate(steps):
        step_id = step.get('id', f'step-{i}')
        step_text = step['text']
        step_color = step.get('color', 'gray')
        step_class = step.get('class', step_id.replace(' ', '-').lower())
        
        # Generate CSS for this step
        step_style = step.get('style')
        css = generate_step_style(step_style, step_color, template=generator.template)
        css_steps.append(f"""
        .step.{step_class} {{ 
            {css}
        }}""")
        
        # Check if this is the last step and we need attribution
        if i == len(steps) - 1 and attribution_on_last:
            html_steps.append(f"""
            <div class="share-wrapper">
                <div class="step {step_class}">{step_text}</div>
                {generator._generate_attribution_html()}
            </div>""")
        else:
            html_steps.append(f'            <div class="step {step_class}">{step_text}</div>')
        
        # Add arrow if not last step
        if i < len(steps) - 1:
            html_steps.append(f'            <div class="arrow">{arrow_text}</div>')
    
    css_content = f"""
        .cycle-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 32px;
            position: relative;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .title {{
            font-size: 24px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .cycle {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .share-wrapper {{
            position: relative;
            display: inline-block;
        }}
        
        .share-wrapper .attribution {{
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: {generator.attribution.margin_top}px;
            width: auto;
        }}
        
        .step {{
            background: #F5F5F7;
            border: none;
            border-radius: 14px;
            padding: 24px 32px;
            font-size: 18px;
            font-weight: 600;
            color: #1D1D1F;
            min-width: 160px;
            text-align: center;
            letter-spacing: -0.01em;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        {''.join(css_steps)}
        
        .arrow {{
            color: #007AFF;
            font-size: 28px;
            font-weight: 600;
            opacity: 0.6;
        }}
        
        .cycle-end {{
            color: #8E8E93;
            font-size: 15px;
            font-weight: 500;
            margin-top: 8px;
            letter-spacing: -0.01em;
        }}
        
        {generator.template.attribution_styles}
        """
    
    cycle_end_html = f'\n        <div class="cycle-end">{cycle_end_text}</div>' if cycle_end_text else ''
    
    html_content = f"""
    <div class="wrapper">
    <div class="cycle-container">
        <div class="title">{generator.title}</div>
        <div class="cycle">
{''.join(html_steps)}
        </div>{cycle_end_html}
    </div>
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


class CycleDiagramGenerator(DiagramGenerator):
    """Cycle diagram generator class"""
    
    def generate(self, generator: BaseGenerator, steps: List[Dict[str, any]], arrow_text: str = "→", cycle_end_text: Optional[str] = None, attribution_on_last: bool = True, **kwargs) -> str:
        """Generate a cycle/flow diagram"""
        return generate_cycle_diagram(generator, steps, arrow_text, cycle_end_text, attribution_on_last)
    
    def validate_input(self, steps: List[Dict[str, any]], **kwargs) -> bool:
        """Validate cycle diagram input"""
        if not steps or not isinstance(steps, list):
            return False
        if not all(isinstance(step, dict) and 'text' in step for step in steps):
            return False
        return True
