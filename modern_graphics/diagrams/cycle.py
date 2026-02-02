"""Cycle diagram generator - Modern redesign with theming support"""

from typing import List, Dict, Optional, Any, TYPE_CHECKING
from ..base import BaseGenerator
from .base import DiagramGenerator
from .theme_utils import extract_theme_colors, generate_css_variables, inject_google_fonts, with_alpha

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def _step_accent_gradient(
    step_color: str,
    generator: BaseGenerator,
    theme: Any,
) -> tuple:
    """Resolve gradient (start, end) for step accent bar and number. Uses template if available."""
    template = getattr(generator, "template", None)
    if template and hasattr(template, "get_gradient"):
        try:
            return template.get_gradient(step_color)
        except Exception:
            pass
    return (theme.accent, theme.accent)


def generate_cycle_diagram(
    generator: BaseGenerator,
    steps: List[Dict[str, any]],
    arrow_text: str = "→",
    cycle_end_text: Optional[str] = None,
    attribution_on_last: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
    show_loop_indicator: bool = True,
) -> str:
    """Generate a modern cycle/flow diagram.
    
    Args:
        generator: BaseGenerator instance
        steps: List of step dicts with 'text' and optional 'color', 'class', 'description'
        arrow_text: Text/symbol for arrows between steps
        cycle_end_text: Optional text below the cycle (e.g. "and repeat")
        attribution_on_last: Whether to show attribution on last step
        color_scheme: Optional ColorScheme for theming
        show_loop_indicator: If True, show a loop-back (↻) after the last step
        
    Returns:
        HTML string
    """
    theme = extract_theme_colors(color_scheme)
    
    html_steps = []
    css_steps = []
    
    default_colors = ["blue", "green", "orange", "purple", "red"]
    
    for i, step in enumerate(steps):
        step_id = step.get("id", f"step-{i}")
        step_text = step["text"]
        step_color = step.get("color", default_colors[i % len(default_colors)])
        step_class = step.get("class", step_id.replace(" ", "-").lower())
        description = step.get("description")
        
        grad_start, grad_end = _step_accent_gradient(step_color, generator, theme)
        
        css_steps.append(f"""
        .step.{step_class}::before {{
            background: linear-gradient(135deg, {grad_start}, {grad_end});
        }}
        .step.{step_class} .step-number {{
            background: linear-gradient(135deg, {grad_start}, {grad_end});
            color: white;
        }}""")
        
        desc_html = ""
        if description:
            desc_html = f'\n                <div class="step-description">{description}</div>'
        
        step_html = f"""
            <div class="step {step_class}">
                <div class="step-number">{i + 1}</div>
                <div class="step-text">{step_text}</div>{desc_html}
            </div>"""
        
        if i == len(steps) - 1 and attribution_on_last:
            html_steps.append(f"""
            <div class="share-wrapper">
                {step_html}
                {generator._generate_attribution_html()}
            </div>""")
        else:
            html_steps.append(step_html)
        
        if i < len(steps) - 1:
            html_steps.append(f'            <div class="arrow"><span>{arrow_text}</span></div>')
    
    # Loop-back indicator after last step
    if show_loop_indicator and len(steps) > 1:
        loop_label = cycle_end_text or "repeat"
        html_steps.append(f"""
            <div class="loop-indicator" aria-label="cycle repeats">
                <span class="loop-icon">↻</span>
                <span class="loop-text">{loop_label}</span>
            </div>""")
    
    # Generate shadow based on theme
    shadow = "0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.04)"
    if theme.is_dark:
        shadow = "0 4px 24px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.2)"
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        .cycle-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            position: relative;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            padding: 40px;
        }}
        
        .title {{
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 700;
            color: var(--text-1);
            margin-bottom: 12px;
            letter-spacing: -0.03em;
            line-height: 1.2;
            text-align: center;
        }}
        
        .cycle {{
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            justify-content: center;
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
            background: var(--bg-card);
            border: {theme.card_border};
            border-radius: 16px;
            padding: 24px 28px;
            min-width: 160px;
            max-width: 200px;
            text-align: center;
            box-shadow: {shadow};
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .step::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--accent);
        }}
        
        .step:hover {{
            transform: translateY(-4px);
        }}
        
        .step-number {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--accent);
            color: white;
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
        }}
        
        .step-text {{
            font-family: var(--font-body);
            font-size: 16px;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: -0.01em;
            line-height: 1.4;
        }}
        
        .step-description {{
            font-family: var(--font-body);
            font-size: 13px;
            font-weight: 500;
            color: var(--text-2);
            letter-spacing: -0.01em;
            line-height: 1.4;
            margin-top: 8px;
        }}
        
        {''.join(css_steps)}
        
        .loop-indicator {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 18px;
            background: {with_alpha(theme.accent, 0.1)};
            border: 1px dashed {with_alpha(theme.accent, 0.4)};
            border-radius: 24px;
            margin-left: 8px;
        }}
        
        .loop-icon {{
            font-size: 20px;
            color: var(--accent);
            line-height: 1;
        }}
        
        .loop-text {{
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 600;
            color: var(--text-2);
            letter-spacing: -0.01em;
        }}
        
        .arrow {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
        }}
        
        .arrow span {{
            color: var(--accent);
            font-size: 24px;
            font-weight: 600;
            opacity: 0.6;
            transition: opacity 0.2s ease;
        }}
        
        .cycle:hover .arrow span {{
            opacity: 1;
        }}
        
        .cycle-end {{
            color: var(--text-3);
            font-family: var(--font-body);
            font-size: 15px;
            font-weight: 500;
            margin-top: 16px;
            letter-spacing: -0.01em;
            padding: 8px 16px;
            background: {with_alpha(theme.accent, 0.08)};
            border-radius: 20px;
        }}
        
        {generator.template.attribution_styles}
        """
    
    # Optional line below cycle (only when loop indicator is off to avoid duplicate label)
    cycle_end_html = ""
    if cycle_end_text and not show_loop_indicator:
        cycle_end_html = f'\n        <div class="cycle-end">{cycle_end_text}</div>'
    
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
    
    html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(html, theme)


class CycleDiagramGenerator(DiagramGenerator):
    """Cycle diagram generator class"""

    def generate(
        self,
        generator: BaseGenerator,
        steps: List[Dict[str, any]],
        arrow_text: str = "→",
        cycle_end_text: Optional[str] = None,
        attribution_on_last: bool = True,
        color_scheme: Optional["ColorScheme"] = None,
        show_loop_indicator: bool = True,
        **kwargs,
    ) -> str:
        """Generate a cycle/flow diagram."""
        return generate_cycle_diagram(
            generator,
            steps,
            arrow_text,
            cycle_end_text,
            attribution_on_last,
            color_scheme,
            show_loop_indicator,
        )
    
    def validate_input(self, steps: List[Dict[str, any]], **kwargs) -> bool:
        """Validate cycle diagram input"""
        if not steps or not isinstance(steps, list):
            return False
        if not all(isinstance(step, dict) and 'text' in step for step in steps):
            return False
        return True
