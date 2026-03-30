"""Grid diagram generator - Material Design inspired"""

from typing import List, Dict, Optional, TYPE_CHECKING
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from .theme_utils import extract_theme_colors, generate_css_variables, inject_google_fonts, with_alpha

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def generate_grid_diagram(
    generator: BaseGenerator,
    items: List[Dict[str, any]],
    columns: int = 5,
    convergence: Optional[Dict[str, str]] = None,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a grid diagram (Material Design: elevated cards, 8dp spacing, typography scale).
    
    Args:
        generator: BaseGenerator instance
        items: List of item dicts with 'text' and optional 'number'
        columns: Number of columns in grid
        convergence: Optional dict with 'goal' and 'outcome' for convergence section
        color_scheme: Optional ColorScheme for theming
        
    Returns:
        HTML string
    """
    theme = extract_theme_colors(color_scheme)
    use_pretext = getattr(generator, "use_pretext", False)
    display_font = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    body_font = display_font
    if color_scheme is not None:
        display_font = (
            getattr(color_scheme, "font_family_display", None)
            or getattr(color_scheme, "font_family", display_font)
        )
        body_font = (
            getattr(color_scheme, "font_family_body", None)
            or getattr(color_scheme, "font_family", body_font)
        )
    if use_pretext:
        from ..pretext_renderer import pretext_slot
    
    items_html = []
    for item in items:
        number = item.get("number")
        text = item["text"]
        if use_pretext:
            item_text_html = pretext_slot(
                text=text,
                font=f"16px {body_font}",
                max_width=130,
                line_height=1.5,
                css_class="md-subtitle1",
                text_anchor="middle",
            )
        else:
            item_text_html = f'<div class="md-subtitle1">{text}</div>'
        if number:
            items_html.append(f"""
            <div class="md-card">
                <div class="md-card-badge" aria-hidden="true">{number}</div>
                <div class="md-card-content">
                    {item_text_html}
                </div>
            </div>""")
        else:
            items_html.append(f"""
            <div class="md-card">
                <div class="md-card-content">
                    {item_text_html}
                </div>
            </div>""")
    
    convergence_html = ""
    if convergence:
        goal = convergence.get("goal", "")
        outcome = convergence.get("outcome", "")
        convergence_html = f"""
        <div class="md-convergence">
            <div class="md-divider" role="separator"></div>
            <div class="md-convergence-goal">{goal}</div>
            <div class="md-convergence-arrow" aria-hidden="true">↓</div>
            <div class="md-convergence-outcome">{outcome}</div>
        </div>"""
    
    # Material elevation 1dp (cards), 2dp (outcome)
    elevation_1 = "0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)"
    elevation_2 = "0 2px 6px rgba(0, 0, 0, 0.16), 0 1px 3px rgba(0, 0, 0, 0.12)"
    if theme.is_dark:
        elevation_1 = "0 2px 6px rgba(0, 0, 0, 0.3), 0 1px 3px rgba(0, 0, 0, 0.2)"
        elevation_2 = "0 4px 12px rgba(0, 0, 0, 0.35), 0 2px 6px rgba(0, 0, 0, 0.2)"
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .container {{
            max-width: 900px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 0 24px;
        }}
        
        .md-headline {{
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            color: var(--text-1);
            margin-bottom: 32px;
            text-align: center;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .md-grid {{
            display: grid;
            grid-template-columns: repeat({columns}, 1fr);
            gap: 16px;
            margin-bottom: 32px;
            width: 100%;
        }}
        
        .md-card {{
            background: var(--bg-card);
            border: {theme.card_border};
            border-radius: 8px;
            padding: 16px;
            min-height: 72px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: {elevation_1};
            transition: box-shadow 0.2s ease;
        }}
        
        .md-card:focus-within {{
            box-shadow: {elevation_2};
        }}
        
        .md-card-badge {{
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
            margin-bottom: 12px;
            flex-shrink: 0;
        }}
        
        .md-card-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .md-subtitle1 {{
            font-family: var(--font-body);
            font-size: 16px;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: 0.01em;
            line-height: 1.5;
        }}
        
        .md-convergence {{
            text-align: center;
            margin: 24px 0 32px;
            width: 100%;
            max-width: 480px;
        }}
        
        .md-divider {{
            height: 1px;
            background: {with_alpha(theme.text_tertiary, 0.24)};
            margin: 0 0 24px;
        }}
        
        .md-convergence-goal {{
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 500;
            color: var(--text-2);
            letter-spacing: 0.02em;
            line-height: 1.43;
            margin-bottom: 16px;
        }}
        
        .md-convergence-arrow {{
            color: var(--accent);
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        
        .md-convergence-outcome {{
            font-family: var(--font-body);
            font-size: 16px;
            font-weight: 600;
            color: var(--success);
            letter-spacing: 0.01em;
            padding: 16px 24px;
            background: {with_alpha(theme.success, 0.12)};
            border-radius: 8px;
            display: inline-block;
            box-shadow: {elevation_1};
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
    if use_pretext:
        headline_html = pretext_slot(
            text=generator.title,
            font=f"24px {display_font}",
            max_width=860,
            line_height=1.2,
            css_class="md-headline",
            text_anchor="middle",
        )
    else:
        headline_html = f'<div class="md-headline">{generator.title}</div>'
    
    html_content = f"""
    <div class="wrapper">
        <div class="container">
            {headline_html}
            <div class="md-grid">
{''.join(items_html)}
            </div>{convergence_html}
            {generator._generate_attribution_html()}
        </div>
    </div>
    """
    
    html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(html, theme)
