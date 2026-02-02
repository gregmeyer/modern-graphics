"""Timeline diagram generator - Material Design inspired"""

from typing import List, Dict, Optional, Any, TYPE_CHECKING
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from .theme_utils import extract_theme_colors, generate_css_variables, inject_google_fonts, with_alpha

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def _event_marker_color(color_key: str, generator: BaseGenerator, theme: Any) -> str:
    """Resolve step/marker color from template or theme accent."""
    template = getattr(generator, "template", None)
    if template and hasattr(template, "get_gradient"):
        try:
            start, _ = template.get_gradient(color_key)
            return start
        except Exception:
            pass
    return theme.accent


def generate_timeline_diagram(
    generator: BaseGenerator,
    events: List[Dict[str, any]],
    orientation: str = "horizontal",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a timeline diagram (Material Design inspired).
    
    Args:
        generator: BaseGenerator instance
        events: List of event dicts with 'date', 'text'/'title', optional 'description', 'color'
        orientation: 'horizontal' or 'vertical'
        color_scheme: Optional ColorScheme for theming
        
    Returns:
        HTML string
    """
    if orientation != "horizontal":
        return _generate_vertical_timeline(generator, events, color_scheme)
    
    theme = extract_theme_colors(color_scheme)
    
    # Material elevation 2dp (card)
    shadow = "0 2px 6px rgba(0, 0, 0, 0.16), 0 1px 3px rgba(0, 0, 0, 0.12)"
    if theme.is_dark:
        shadow = "0 4px 12px rgba(0, 0, 0, 0.35), 0 2px 6px rgba(0, 0, 0, 0.2)"
    
    events_html = []
    events_css = []
    
    for i, event in enumerate(events):
        event_id = f"event-{i}"
        date = event.get("date", "")
        text = event.get("text", event.get("title", ""))
        description = event.get("description", "")
        color = event.get("color", "gray")
        event_class = event.get("class", event_id.replace(" ", "-").lower())
        marker_color = _event_marker_color(color, generator, theme)
        
        events_css.append(f"""
        .timeline-step-indicator.{event_class} {{
            background: {marker_color};
            border-color: var(--bg-card);
        }}
        .timeline-step-indicator.{event_class} .step-num {{
            color: white;
        }}""")
        
        desc_html = f'<div class="md-body2">{description}</div>' if description else ""
        events_html.append(f"""
            <div class="timeline-step">
                <div class="timeline-step-content">
                    <div class="md-overline">{date}</div>
                    <div class="md-subtitle1">{text}</div>
                    {desc_html}
                </div>
                <div class="timeline-step-indicator {event_class}">
                    <span class="step-num">{i + 1}</span>
                </div>
            </div>""")
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        .timeline-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 1200px;
            padding: 40px 24px;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .md-headline {{
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin-bottom: 32px;
            text-align: center;
        }}
        
        .timeline-track {{
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            width: 100%;
            position: relative;
        }}
        
        .timeline-track::before {{
            content: '';
            position: absolute;
            left: 24px;
            right: 24px;
            bottom: 12px;
            height: 2px;
            background: {with_alpha(theme.text_tertiary, 0.24)};
            pointer-events: none;
        }}
        
        .timeline-step {{
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            position: relative;
            z-index: 1;
        }}
        
        .timeline-step-content {{
            background: var(--bg-card);
            border: {theme.card_border};
            border-radius: 8px;
            padding: 16px 20px;
            min-width: 160px;
            max-width: 240px;
            text-align: center;
            box-shadow: {shadow};
            margin-bottom: 24px;
        }}
        
        .md-overline {{
            font-family: var(--font-body);
            font-size: 12px;
            font-weight: 500;
            color: var(--text-3);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        
        .md-subtitle1 {{
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: 0.01em;
            line-height: 1.4;
        }}
        
        .md-body2 {{
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 400;
            color: var(--text-2);
            letter-spacing: 0.02em;
            line-height: 1.43;
            margin-top: 8px;
        }}
        
        .timeline-step-indicator {{
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 2px solid var(--bg-card);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        }}
        
        .step-num {{
            font-family: var(--font-display);
            font-size: 12px;
            font-weight: 700;
        }}
        
        {''.join(events_css)}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top}px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-3);
            letter-spacing: -0.01em;
            text-align: right;
            width: 100%;
            max-width: 1200px;
        }}
        
        {ATTRIBUTION_STYLES}
    """
    
    html_content = f"""
    <div class="wrapper">
    <div class="timeline-container">
        <div class="md-headline">{generator.title}</div>
        <div class="timeline-track">
{''.join(events_html)}
        </div>
    </div>
    {generator._generate_attribution_html()}
    </div>
    """
    
    html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(html, theme)


def _generate_vertical_timeline(
    generator: BaseGenerator,
    events: List[Dict[str, any]],
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a vertical timeline (Material Design: central line, alternating content, chips)."""
    theme = extract_theme_colors(color_scheme)
    
    shadow = "0 2px 6px rgba(0, 0, 0, 0.16), 0 1px 3px rgba(0, 0, 0, 0.12)"
    if theme.is_dark:
        shadow = "0 4px 12px rgba(0, 0, 0, 0.35), 0 2px 6px rgba(0, 0, 0, 0.2)"
    
    events_html = []
    events_css = []
    
    for i, event in enumerate(events):
        event_id = f"event-{i}"
        date = event.get("date", "")
        text = event.get("text", event.get("title", ""))
        description = event.get("description", "")
        color = event.get("color", "gray")
        event_class = event.get("class", event_id.replace(" ", "-").lower())
        marker_color = _event_marker_color(color, generator, theme)
        side = "left" if i % 2 == 0 else "right"
        
        events_css.append(f"""
        .vt-dot.{event_class} {{
            background: {marker_color};
            border-color: var(--bg-card);
        }}""")
        
        desc_html = f'<div class="md-body2">{description}</div>' if description else ""
        events_html.append(f"""
            <div class="vt-item vt-{side}">
                <div class="vt-content">
                    <div class="vt-chip">{date}</div>
                    <div class="md-subtitle1">{text}</div>
                    {desc_html}
                </div>
                <div class="vt-dot {event_class}" aria-hidden="true"></div>
            </div>""")
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        .timeline-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 720px;
            padding: 40px 24px;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .md-headline {{
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            color: var(--text-1);
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin-bottom: 32px;
            text-align: center;
        }}
        
        .timeline {{
            position: relative;
            width: 100%;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background: {with_alpha(theme.text_tertiary, 0.24)};
            transform: translateX(-50%);
        }}
        
        .vt-item {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: start;
            gap: 0 20px;
            position: relative;
            margin-bottom: 8px;
        }}
        
        .vt-item.vt-left .vt-content {{ grid-column: 1; }}
        .vt-item.vt-right .vt-content {{ grid-column: 3; }}
        
        .vt-content {{
            background: var(--bg-card);
            border: {theme.card_border};
            border-radius: 8px;
            padding: 16px 20px;
            box-shadow: {shadow};
        }}
        
        .vt-chip {{
            display: inline-block;
            font-family: var(--font-body);
            font-size: 12px;
            font-weight: 500;
            color: var(--text-3);
            letter-spacing: 0.04em;
            background: {with_alpha(theme.text_tertiary, 0.12)};
            padding: 4px 10px;
            border-radius: 16px;
            margin-bottom: 10px;
        }}
        
        .vt-content .md-subtitle1 {{
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 600;
            color: var(--text-1);
            letter-spacing: 0.01em;
            line-height: 1.4;
        }}
        
        .vt-content .md-body2 {{
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 400;
            color: var(--text-2);
            letter-spacing: 0.02em;
            line-height: 1.43;
            margin-top: 8px;
        }}
        
        .vt-dot {{
            grid-column: 2;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 2px solid var(--bg-card);
            justify-self: center;
            position: relative;
            z-index: 1;
            margin-top: 20px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
        }}
        
        {''.join(events_css)}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top}px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-3);
            letter-spacing: -0.01em;
            text-align: right;
            width: 100%;
            max-width: 720px;
        }}
        
        {ATTRIBUTION_STYLES}
    """
    
    html_content = f"""
    <div class="wrapper">
    <div class="timeline-container">
        <div class="md-headline">{generator.title}</div>
        <div class="timeline">
{''.join(events_html)}
        </div>
    </div>
    {generator._generate_attribution_html()}
    </div>
    """
    
    html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(html, theme)
