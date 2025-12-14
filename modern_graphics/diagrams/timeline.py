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
    """Generate a timeline diagram"""
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
            flex-direction: {'column' if orientation == 'vertical' else 'row'};
            align-items: {'center' if orientation == 'vertical' else 'center'};
            gap: 24px;
            width: 100%;
            max-width: 1000px;
        }}
        
        .timeline-item {{
            display: flex;
            flex-direction: {'column' if orientation == 'vertical' else 'row'};
            align-items: center;
            gap: 24px;
            flex: {'none' if orientation == 'vertical' else '1'};
            width: {'100%' if orientation == 'vertical' else 'auto'};
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
            flex: 1;
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
            {'width: 2px; height: 40px;' if orientation == 'vertical' else 'width: 60px; height: 2px;'}
            background: {'linear-gradient(180deg, #007AFF 0%, #007AFF 100%)' if orientation == 'vertical' else 'linear-gradient(90deg, #007AFF 0%, #007AFF 100%)'};
            opacity: 0.4;
            flex-shrink: 0;
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
