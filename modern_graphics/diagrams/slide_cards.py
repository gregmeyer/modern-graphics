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
    arrow_text: str = "→",
    style: str = "default"
) -> str:
    """Generate a horizontal slide card diagram showing transformation/evolution
    
    Args:
        generator: BaseGenerator instance
        cards: List of card dictionaries. Each card can have:
            - title: Card title
            - tagline: Card tagline
            - subtext: Card subtext
            - color: Color key ('blue', 'green', 'purple', 'gray')
            - features: List of feature strings
            - badge: Badge text
            - custom_mockup: Optional custom SVG or SVG.js code for mockup
        arrow_text: Text to display between cards
        style: Layout style - 'default' (vertical cards) or 'lower_third' (horizontal bar style)
    
    Args:
        generator: BaseGenerator instance
        cards: List of card dictionaries. Each card can have:
            - title: Card title
            - tagline: Card tagline
            - subtext: Card subtext
            - color: Color key ('blue', 'green', 'purple', 'gray')
            - features: List of feature strings
            - badge: Badge text
            - custom_mockup: Optional custom SVG or SVG.js code for mockup
        arrow_text: Text to display between cards
    """
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
        custom_mockup = card.get('custom_mockup', None)
        
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
        
        # Generate SVG mockup - use custom if provided, otherwise default
        if custom_mockup:
            if generator.use_svg_js and not custom_mockup.strip().startswith('<'):
                # SVG.js code - wrap in script tag
                mockup_id = f'mockup-{card_id}'
                # Adjust SVG size based on style: landscape for lower_third, portrait for default
                if style == "lower_third":
                    svg_width, svg_height = 400, 200  # Landscape for lower third
                else:
                    svg_width, svg_height = 240, 140  # Portrait for default
                svg_mockup = f'<div id="{mockup_id}" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;"></div><script>(function(){{const draw = SVG().addTo("#{mockup_id}").size({svg_width}, {svg_height});{custom_mockup}}})();</script>'
            else:
                # Raw SVG string
                svg_mockup = custom_mockup
        else:
            svg_mockup = generate_slide_mockup(title, color_key)
        
        # Generate HTML for this card
        badge_html = f'<div class="card-badge">{badge}</div>' if badge else ''
        
        features_html = ''
        if features:
            features_html = '<div class="card-features">'
            for feature in features:
                features_html += f'<div class="card-feature">{feature}</div>'
            features_html += '</div>'
        
        # Lower third style: graphic on top 2/3, text on bottom 1/3
        if style == "lower_third":
            cards_html.append(f"""
            <div class="slide-card slide-card-lower-third {card_id}">
                {badge_html}
                <div class="card-mockup">{svg_mockup}</div>
                <div class="card-text-content">
                    <div class="card-title">{title}</div>
                    <div class="card-tagline">{tagline}</div>
                    <div class="card-subtext">{subtext}</div>
                    {features_html}
                </div>
            </div>""")
        else:
            # Default style: vertical layout
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
            position: relative;
        }}
        
        .card-mockup > div {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            position: relative;
        }}
        
        .card-mockup svg {{
            width: 100%;
            height: 100%;
            display: block;
            margin: 0 auto;
            max-width: 100%;
            max-height: 100%;
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
        
        /* Lower third style: graphic top 2/3, text bottom 1/3 */
        .slide-card-lower-third {{
            padding: 0 !important;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            min-width: 320px;
            max-width: 400px;
        }}
        
        .slide-card-lower-third .card-mockup {{
            width: 100%;
            height: 0;
            padding-bottom: 66.67%; /* 2/3 aspect ratio */
            margin-bottom: 0;
            flex-shrink: 0;
            border-radius: 16px 16px 0 0;
            position: relative;
            overflow: hidden;
        }}
        
        .slide-card-lower-third .card-mockup > div {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-card-lower-third .card-mockup svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}
        
        .slide-card-lower-third .card-text-content {{
            padding: 20px 24px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex: 1;
            min-height: 33.33%; /* Bottom 1/3 */
        }}
        
        .slide-card-lower-third .card-title {{
            font-size: 20px;
            margin-bottom: 4px;
        }}
        
        .slide-card-lower-third .card-tagline {{
            font-size: 16px;
            margin-bottom: 6px;
        }}
        
        .slide-card-lower-third .card-subtext {{
            font-size: 13px;
            margin-bottom: 10px;
        }}
        
        .slide-card-lower-third .card-features {{
            gap: 4px;
        }}
        
        .slide-card-lower-third .card-feature {{
            font-size: 12px;
        }}
        
        .slide-card-lower-third .card-badge {{
            top: 12px;
            right: 12px;
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
    """Generate a side-by-side slide card comparison
    
    Args:
        generator: BaseGenerator instance
        left_card: Left card dictionary (same structure as cards in generate_slide_card_diagram)
        right_card: Right card dictionary (same structure as cards in generate_slide_card_diagram)
        vs_text: Text to display between cards
    """
    
    def generate_card_html(card: Dict[str, any], card_class: str) -> str:
        title = card.get('title', '')
        tagline = card.get('tagline', '')
        color_key = card.get('color', 'gray')
        features = card.get('features', [])
        badge = card.get('badge', '')
        custom_mockup = card.get('custom_mockup', None)
        
        palette = ACCENT_MAP.get(color_key, ACCENT_MAP['gray'])
        
        # Generate SVG mockup - use custom if provided, otherwise default
        if custom_mockup:
            if generator.use_svg_js and not custom_mockup.strip().startswith('<'):
                # SVG.js code - wrap in script tag
                mockup_id = f'mockup-{card_class}'
                svg_mockup = f'<div id="{mockup_id}" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;"></div><script>(function(){{const draw = SVG().addTo("#{mockup_id}").size(240, 140);{custom_mockup}}})();</script>'
            else:
                # Raw SVG string
                svg_mockup = custom_mockup
        else:
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
        
        .slide-card .card-mockup > div {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-card .card-mockup svg {{
            width: 100%;
            height: 100%;
            display: block;
            margin: 0 auto;
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
