"""Slide card diagram generators"""

from typing import List, Dict
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from ..svg_generator import generate_slide_mockup


ACCENT_MAP = {
    'blue': {
        'grad_start': '#EBF5FF',
        'grad_end': '#E3F2FD',
        'accent': '#0B64D0',
        'border': 'rgba(11, 100, 208, 0.18)',
        'shadow': 'rgba(11, 100, 208, 0.22)',
    },
    'green': {
        'grad_start': '#F0F9F4',
        'grad_end': '#E8F5E9',
        'accent': '#1B7A4E',
        'border': 'rgba(27, 122, 78, 0.18)',
        'shadow': 'rgba(27, 122, 78, 0.20)',
    },
    'purple': {
        'grad_start': '#F9F0FF',
        'grad_end': '#F3E5F5',
        'accent': '#8243B5',
        'border': 'rgba(130, 67, 181, 0.18)',
        'shadow': 'rgba(130, 67, 181, 0.22)',
    },
    'gray': {
        'grad_start': '#F5F5F7',
        'grad_end': '#F5F5F7',
        'accent': '#3A3A3C',
        'border': 'rgba(58, 58, 60, 0.12)',
        'shadow': 'rgba(58, 58, 60, 0.12)',
    }
}


def generate_slide_card_diagram(
    generator: BaseGenerator,
    cards: List[Dict[str, any]],
    arrow_text: str = "→"
) -> str:
    """Generate a horizontal slide card diagram showing transformation/evolution"""
    cards_html = []
    cards_css = []
    
    for i, card in enumerate(cards):
        card_id = f'card-{i}'
        title = card.get('title', '')
        tagline = card.get('tagline', '')
        subtext = card.get('subtext', '')
        color_key = card.get('color', 'gray')
        features = card.get('features', [])
        badge = card.get('badge', '')
        
        palette = ACCENT_MAP.get(color_key, ACCENT_MAP['gray'])
        
        # Generate CSS for this card
        cards_css.append(f"""
        .slide-card.{card_id} {{
            background: linear-gradient(135deg, {palette['grad_start']} 0%, {palette['grad_end']} 100%);
            border: 1px solid {palette['border']};
            box-shadow: 0 24px 48px {palette['shadow']}, 0 8px 16px rgba(0, 0, 0, 0.08);
        }}
        
        .slide-card.{card_id} .card-title {{
            color: {palette['accent']};
        }}
        
        .slide-card.{card_id} .card-tagline {{
            color: {palette['accent']};
        }}""")
        
        # Generate SVG mockup based on card type
        svg_mockup = generate_slide_mockup(title, color_key)
        
        # Generate HTML for this card
        badge_html = f'<div class="card-badge">{badge}</div>' if badge else ''
        
        features_html = ''
        if features:
            features_html = '<div class="card-features">'
            for feature in features:
                features_html += f'<div class="card-feature">{feature}</div>'
            features_html += '</div>'
        
        cards_html.append(f"""
            <div class="slide-card {card_id}">
                {badge_html}
                <div class="card-title">{title}</div>
                <div class="card-tagline">{tagline}</div>
                <div class="card-mockup">{svg_mockup}</div>
                <div class="card-subtext">{subtext}</div>
                {features_html}
            </div>""")
        
        # Add arrow if not last card
        if i < len(cards) - 1:
            cards_html.append(f'            <div class="card-arrow">{arrow_text}</div>')
    
    css_content = f"""
        body {{
            padding: 40px 20px !important;
        }}
        
        .slide-cards-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            position: relative;
            width: 100%;
            max-width: 100%;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 100%;
        }}
        
        .title {{
            font-size: 28px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .slide-cards-row {{
            display: flex;
            align-items: center;
            gap: 32px;
            flex-wrap: nowrap;
            justify-content: center;
            width: fit-content;
            max-width: 100%;
        }}
        
        .slide-card {{
            background: #F5F5F7;
            border: none;
            border-radius: 16px;
            padding: 32px 40px;
            min-width: 280px;
            max-width: 320px;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .slide-card:hover {{
            transform: translateY(-4px);
        }}
        
        .card-badge {{
            position: absolute;
            top: 16px;
            right: 16px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.01em;
        }}
        
        .card-title {{
            font-size: 24px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .card-tagline {{
            font-size: 18px;
            font-weight: 600;
            color: #1D1D1F;
            margin-bottom: 20px;
            letter-spacing: -0.01em;
        }}
        
        .card-mockup {{
            width: 100%;
            height: 140px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .card-mockup svg {{
            width: 100%;
            height: 100%;
        }}
        
        .card-subtext {{
            font-size: 14px;
            font-weight: 400;
            color: #86868B;
            margin-bottom: 20px;
            line-height: 1.5;
            letter-spacing: -0.01em;
        }}
        
        .card-features {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .card-feature {{
            font-size: 14px;
            font-weight: 500;
            color: #1D1D1F;
            letter-spacing: -0.01em;
        }}
        
        .card-arrow {{
            color: #007AFF;
            font-size: 32px;
            font-weight: 600;
            opacity: 0.6;
            flex-shrink: 0;
        }}
        
        {''.join(cards_css)}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="wrapper">
    <div class="slide-cards-container">
        <div class="title">{generator.title}</div>
        <div class="slide-cards-row">
{''.join(cards_html)}
        </div>
    </div>
    {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def generate_slide_card_comparison(
    generator: BaseGenerator,
    left_card: Dict[str, any],
    right_card: Dict[str, any],
    vs_text: str = "→"
) -> str:
    """Generate a side-by-side slide card comparison"""
    
    def generate_card_html(card: Dict[str, any], card_class: str) -> str:
        title = card.get('title', '')
        tagline = card.get('tagline', '')
        color_key = card.get('color', 'gray')
        features = card.get('features', [])
        badge = card.get('badge', '')
        
        palette = ACCENT_MAP.get(color_key, ACCENT_MAP['gray'])
        
        # Generate SVG mockup
        svg_mockup = generate_slide_mockup(title, color_key)
        
        badge_html = f'<div class="card-badge">{badge}</div>' if badge else ''
        
        features_html = ''
        if features:
            features_html = '<div class="card-features">'
            for feature in features:
                features_html += f'<div class="card-feature">{feature}</div>'
            features_html += '</div>'
        
        return f"""
            <div class="slide-card {card_class}" style="background: linear-gradient(135deg, {palette['grad_start']} 0%, {palette['grad_end']} 100%); border: 1px solid {palette['border']}; box-shadow: 0 24px 48px {palette['shadow']}, 0 8px 16px rgba(0, 0, 0, 0.08);">
                {badge_html}
                <div class="card-title" style="color: {palette['accent']};">{title}</div>
                <div class="card-tagline" style="color: {palette['accent']};">{tagline}</div>
                <div class="card-mockup">{svg_mockup}</div>
                {features_html}
            </div>"""
    
    css_content = f"""
        body {{
            padding: 40px 20px !important;
        }}
        
        .slide-comparison-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            position: relative;
            width: fit-content;
            max-width: 100%;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: fit-content;
            max-width: 100%;
        }}
        
        .title {{
            font-size: 28px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .slide-comparison-row {{
            display: flex;
            align-items: center;
            gap: 40px;
            flex-wrap: nowrap;
            justify-content: center;
            width: fit-content;
            max-width: 100%;
        }}
        
        .slide-card {{
            background: #F5F5F7;
            border: none;
            border-radius: 16px;
            padding: 40px 48px;
            min-width: 320px;
            max-width: 380px;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .slide-card:hover {{
            transform: translateY(-4px);
        }}
        
        .card-badge {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.01em;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }}
        
        .card-title {{
            font-size: 26px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .card-tagline {{
            font-size: 20px;
            font-weight: 600;
            color: #1D1D1F;
            margin-bottom: 20px;
            letter-spacing: -0.01em;
        }}
        
        .slide-card .card-mockup {{
            width: 100%;
            height: 160px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .slide-card .card-mockup svg {{
            width: 100%;
            height: 100%;
        }}
        
        .card-features {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .card-feature {{
            font-size: 15px;
            font-weight: 500;
            color: #1D1D1F;
            letter-spacing: -0.01em;
            line-height: 1.4;
        }}
        
        .card-vs {{
            color: #007AFF;
            font-size: 36px;
            font-weight: 600;
            opacity: 0.7;
            flex-shrink: 0;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="wrapper">
    <div class="slide-comparison-container">
        <div class="title">{generator.title}</div>
        <div class="slide-comparison-row">
{generate_card_html(left_card, 'left-card')}
            <div class="card-vs">{vs_text}</div>
{generate_card_html(right_card, 'right-card')}
        </div>
    </div>
    {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
