"""Timeline diagram generator"""

from typing import List, Dict
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from ..utils import generate_step_style


def generate_timeline_diagram(
    generator: BaseGenerator,
    events: List[Dict[str, any]],
    orientation: str = "horizontal"
) -> str:
    """Generate a timeline diagram with a continuous line and event markers"""
    if orientation != "horizontal":
        # For vertical, keep simpler layout for now
        return _generate_vertical_timeline(generator, events)
    
    events_html = []
    events_css = []
    
    for i, event in enumerate(events):
        event_id = f'event-{i}'
        date = event.get('date', '')
        text = event.get('text', event.get('title', ''))
        description = event.get('description', '')
        color = event.get('color', 'gray')
        event_class = event.get('class', event_id.replace(' ', '-').lower())
        
        # Get color from template
        step_style = event.get('style')
        css = generate_step_style(step_style, color, template=generator.template)
        
        # Get marker color from template gradient (use first color)
        grad_start, grad_end = generator.template.get_gradient(color)
        marker_color = grad_start
        
        # Extract background color for arrow
        bg_color = grad_start  # Use gradient start for arrow
        
        events_css.append(f"""
        .event-marker.{event_class} {{ 
            background: {marker_color};
        }}
        .event-card.{event_class} {{
            {css}
        }}
        .event-card.{event_class}::after {{
            border-top-color: {bg_color};
        }}""")
        
        # Position cards above the line, alternating slightly for visual interest
        card_position = "above" if i % 2 == 0 else "above"  # Keep all above for consistency
        
        events_html.append(f"""
            <div class="timeline-event">
                <div class="event-card {event_class} {card_position}">
                    <div class="event-date">{date}</div>
                    <div class="event-title">{text}</div>
                    {f'<div class="event-description">{description}</div>' if description else ''}
                </div>
                <div class="event-marker {event_class}"></div>
            </div>""")
    
    css_content = f"""
        .timeline-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            position: relative;
            width: 100%;
            max-width: 1200px;
            padding: 40px 20px;
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
            margin-bottom: 20px;
            letter-spacing: -0.02em;
            line-height: 1.2;
            text-align: center;
        }}
        
        .timeline {{
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            width: 100%;
            padding: 0 20px;
            margin: 140px 0 40px 0;
        }}
        
        /* Continuous horizontal line */
        .timeline::before {{
            content: '';
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 3px;
            background: linear-gradient(90deg, #007AFF 0%, #007AFF 100%);
            opacity: 0.3;
            z-index: 1;
        }}
        
        .timeline-event {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            z-index: 2;
        }}
        
        .event-marker {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #007AFF;
            border: 3px solid #ffffff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            position: absolute;
            bottom: -8px;
            z-index: 3;
        }}
        
        .event-card {{
            background: #F5F5F7;
            border: none;
            border-radius: 14px;
            padding: 16px 20px;
            font-size: 15px;
            font-weight: 600;
            color: #1D1D1F;
            min-width: 200px;
            max-width: 220px;
            text-align: center;
            letter-spacing: -0.01em;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1), 0 4px 16px rgba(0, 0, 0, 0.05);
            margin-bottom: 40px;
            position: relative;
        }}
        
        .event-card.above {{
            margin-bottom: 40px;
        }}
        
        .event-card::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 8px solid;
            border-top-color: inherit;
        }}
        
        {''.join(events_css)}
        
        .event-date {{
            font-size: 12px;
            font-weight: 600;
            color: #8E8E93;
            margin-bottom: 6px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        
        .event-title {{
            font-size: 16px;
            font-weight: 700;
            color: #1D1D1F;
            letter-spacing: -0.01em;
            line-height: 1.3;
            margin-bottom: 4px;
        }}
        
        .event-description {{
            font-size: 13px;
            font-weight: 500;
            color: #8E8E93;
            letter-spacing: -0.01em;
            line-height: 1.4;
            margin-top: 6px;
        }}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top}px;
            font-size: 12px;
            font-weight: 500;
            color: #C7C7CC;
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
        <div class="title">{generator.title}</div>
        <div class="timeline">
{''.join(events_html)}
        </div>
    </div>
    {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _generate_vertical_timeline(generator: BaseGenerator, events: List[Dict[str, any]]) -> str:
    """Generate a vertical timeline (fallback for vertical orientation)"""
    events_html = []
    events_css = []
    
    for i, event in enumerate(events):
        event_id = f'event-{i}'
        date = event.get('date', '')
        text = event.get('text', '')
        color = event.get('color', 'gray')
        event_class = event.get('class', event_id.replace(' ', '-').lower())
        
        step_style = event.get('style')
        css = generate_step_style(step_style, color, template=generator.template)
        events_css.append(f"""
        .event.{event_class} {{ 
            {css}
        }}""")
        
        events_html.append(f"""
            <div class="timeline-item">
                <div class="event {event_class}">
                    <div class="event-date">{date}</div>
                    <div class="event-text">{text}</div>
                </div>
                {f'<div class="timeline-line"></div>' if i < len(events) - 1 else ''}
            </div>""")
    
    css_content = f"""
        .timeline-container {{
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
        
        .timeline {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
            width: 100%;
            max-width: 1000px;
        }}
        
        .timeline-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
            width: 100%;
        }}
        
        .event {{
            background: #F5F5F7;
            border: none;
            border-radius: 14px;
            padding: 20px 24px;
            font-size: 16px;
            font-weight: 600;
            color: #1D1D1F;
            min-width: 180px;
            text-align: center;
            letter-spacing: -0.01em;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
        }}
        {''.join(events_css)}
        
        .event-date {{
            font-size: 14px;
            font-weight: 500;
            color: #8E8E93;
            margin-bottom: 8px;
            letter-spacing: -0.01em;
        }}
        
        .event-text {{
            font-size: 16px;
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.01em;
        }}
        
        .timeline-line {{
            width: 2px;
            height: 40px;
            background: linear-gradient(180deg, #007AFF 0%, #007AFF 100%);
            opacity: 0.4;
        }}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top}px;
            font-size: 12px;
            font-weight: 500;
            color: #C7C7CC;
            letter-spacing: -0.01em;
            text-align: right;
            width: 100%;
            max-width: 1000px;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="wrapper">
    <div class="timeline-container">
        <div class="title">{generator.title}</div>
        <div class="timeline">
{''.join(events_html)}
        </div>
    </div>
    {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
