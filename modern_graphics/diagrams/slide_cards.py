"""Slide card diagram generators – Material Design inspired.

Uses elevation (shadow) instead of borders, 8dp grid, Material type scale,
and surface-first card styling with optional accent tint.

Cards can embed a wireframe by setting wireframe or svg_type on the card dict:
  - "before" | "after" | "chat-panel" | "modal-form"
"""

from typing import List, Dict, Optional, Any, TYPE_CHECKING
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from ..svg_generator import generate_slide_mockup
from .theme_utils import (
    extract_theme_colors,
    generate_css_variables,
    inject_google_fonts,
    with_alpha,
)
from .wireframe_svg import (
    WireframeSVGConfig,
    generate_before_wireframe_svg,
    generate_after_wireframe_svg,
    generate_chat_panel_svg,
    generate_modal_form_svg,
)

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme

# Wireframe size when embedded in slide card mockup area
WIREFRAME_CARD_WIDTH = 360
WIREFRAME_CARD_HEIGHT = 200


def _wireframe_svg_for_card(
    wireframe_type: str,
    color_scheme: Optional["ColorScheme"],
    generator: BaseGenerator,
) -> str:
    """Return SVG string for the given wireframe type, themed if color_scheme provided."""
    if color_scheme:
        config = WireframeSVGConfig.from_color_scheme(
            color_scheme, width=WIREFRAME_CARD_WIDTH, height=WIREFRAME_CARD_HEIGHT
        )
    else:
        config = WireframeSVGConfig(width=WIREFRAME_CARD_WIDTH, height=WIREFRAME_CARD_HEIGHT)
    if wireframe_type == "before":
        return generate_before_wireframe_svg(config)
    if wireframe_type == "after":
        return generate_after_wireframe_svg(config)
    if wireframe_type == "chat-panel":
        return generate_chat_panel_svg(config)
    if wireframe_type == "modal-form":
        return generate_modal_form_svg(config)
    return generate_slide_mockup("", "gray")  # fallback

# Material elevation shadows (dp): 1 = resting card, 2 = raised, 4 = hover
MD_ELEVATION_1 = "0 1px 3px 0 rgba(0, 0, 0, 0.12), 0 1px 2px 0 rgba(0, 0, 0, 0.24)"
MD_ELEVATION_2 = (
    "0 3px 4px -2px rgba(0, 0, 0, 0.2), "
    "0 2px 2px 0 rgba(0, 0, 0, 0.14), "
    "0 1px 5px 0 rgba(0, 0, 0, 0.12)"
)
MD_ELEVATION_4 = (
    "0 6px 10px -2px rgba(0, 0, 0, 0.2), "
    "0 3px 4px -2px rgba(0, 0, 0, 0.14), "
    "0 1px 8px 0 rgba(0, 0, 0, 0.12)"
)

ACCENT_MAP = {
    "blue": {"accent": "#0B64D0", "tint": "rgba(11, 100, 208, 0.08)"},
    "green": {"accent": "#1B7A4E", "tint": "rgba(27, 122, 78, 0.08)"},
    "purple": {"accent": "#8243B5", "tint": "rgba(130, 67, 181, 0.08)"},
    "gray": {"accent": "#3A3A3C", "tint": "rgba(58, 58, 60, 0.06)"},
}


def generate_slide_card_diagram(
    generator: BaseGenerator,
    cards: List[Dict[str, any]],
    arrow_text: str = "→",
    style: str = "default",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a horizontal slide card diagram showing transformation/evolution.

    Each card can have:
        title, tagline, subtext, color ('blue'|'green'|'purple'|'gray'),
        features (list), badge.
    Mockup per card: set custom_mockup (SVG string or SVG.js code), or set
        wireframe / svg_type to 'before'|'after'|'chat-panel'|'modal-form'
        to embed that wireframe (themed if color_scheme provided).
    """
    theme = extract_theme_colors(color_scheme)
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
        custom_mockup = card.get("custom_mockup", None)
        wireframe_type = card.get("wireframe") or card.get("svg_type")

        palette = ACCENT_MAP.get(color_key, ACCENT_MAP["gray"])
        # Material: surface + subtle tint, 4px left accent bar, elevation
        cards_css.append(f"""
        .slide-card.{card_id} {{
            background: var(--bg-card);
            box-shadow: {MD_ELEVATION_1};
            border-left: 4px solid {palette['accent']};
        }}
        .slide-card.{card_id} .card-title {{
            color: var(--text-1);
        }}
        .slide-card.{card_id} .card-tagline {{
            color: var(--text-2);
        }}
        .slide-card.{card_id} .card-mockup {{
            background: {palette['tint']};
        }}""")

        # Generate SVG mockup: custom_mockup > wireframe type > default
        if custom_mockup:
            if generator.use_svg_js and not custom_mockup.strip().startswith("<"):
                mockup_id = f"mockup-{card_id}"
                if style == "lower_third":
                    svg_width, svg_height = 400, 200
                else:
                    svg_width, svg_height = 240, 140
                svg_mockup = f'<div id="{mockup_id}" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;"></div><script>(function(){{const draw = SVG().addTo("#{mockup_id}").size({svg_width}, {svg_height});{custom_mockup}}})();</script>'
            else:
                svg_mockup = custom_mockup
        elif wireframe_type and str(wireframe_type).lower() in ("before", "after", "chat-panel", "modal-form"):
            svg_mockup = _wireframe_svg_for_card(
                str(wireframe_type).lower(), color_scheme, generator
            )
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
    
    # Material: 8dp grid (24, 32), elevation, type scale
    md_card_shadow_hover = MD_ELEVATION_4 if not theme.is_dark else "0 8px 16px -4px rgba(0,0,0,0.35), 0 4px 8px -2px rgba(0,0,0,0.2)"
    css_content = f"""
        {generate_css_variables(theme)}
        
        body {{
            padding: 32px 24px !important;
            background: var(--bg-page);
        }}
        
        .slide-cards-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 32px;
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
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 500;
            color: var(--text-1);
            margin-bottom: 16px;
            letter-spacing: 0;
            line-height: 1.35;
        }}
        
        .slide-cards-row {{
            display: flex;
            align-items: center;
            gap: 24px;
            flex-wrap: nowrap;
            justify-content: center;
            width: fit-content;
            max-width: 100%;
        }}
        
        .slide-card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 24px;
            min-width: 280px;
            max-width: 320px;
            position: relative;
            transition: box-shadow 0.2s ease;
        }}
        
        .slide-card:hover {{
            box-shadow: {md_card_shadow_hover};
        }}
        
        .card-badge {{
            position: absolute;
            top: 16px;
            right: 16px;
            background: {with_alpha(theme.text_tertiary, 0.12)};
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-2);
            letter-spacing: 0.04em;
        }}
        
        .card-title {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 500;
            color: var(--text-1);
            margin-bottom: 8px;
            letter-spacing: 0;
            line-height: 1.35;
        }}
        
        .card-tagline {{
            font-family: var(--font-body);
            font-size: 16px;
            font-weight: 500;
            color: var(--text-2);
            margin-bottom: 16px;
            letter-spacing: 0.015em;
            line-height: 1.5;
        }}
        
        .card-mockup {{
            width: 100%;
            height: 140px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
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
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 400;
            color: var(--text-2);
            margin-bottom: 16px;
            line-height: 1.5;
            letter-spacing: 0.025em;
        }}
        
        .card-features {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .card-feature {{
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 400;
            color: var(--text-1);
            letter-spacing: 0.025em;
            line-height: 1.43;
        }}
        
        .card-arrow {{
            color: var(--text-3);
            font-size: 24px;
            font-weight: 500;
            opacity: 0.7;
            flex-shrink: 0;
        }}
        
        /* Lower third: graphic top 2/3, text bottom 1/3 */
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
            padding-bottom: 66.67%;
            margin-bottom: 0;
            flex-shrink: 0;
            border-radius: 12px 12px 0 0;
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
            padding: 16px 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
            min-height: 33.33%;
        }}
        
        .slide-card-lower-third .card-title {{
            font-size: 20px;
            margin-bottom: 0;
        }}
        
        .slide-card-lower-third .card-tagline {{
            font-size: 16px;
            margin-bottom: 0;
        }}
        
        .slide-card-lower-third .card-subtext {{
            font-size: 13px;
            margin-bottom: 8px;
        }}
        
        .slide-card-lower-third .card-features {{
            gap: 8px;
        }}
        
        .slide-card-lower-third .card-feature {{
            font-size: 13px;
        }}
        
        .slide-card-lower-third .card-badge {{
            top: 16px;
            right: 16px;
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
    
    full_html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(full_html, theme)


def generate_slide_card_comparison(
    generator: BaseGenerator,
    left_card: Dict[str, any],
    right_card: Dict[str, any],
    vs_text: str = "→",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a side-by-side slide card comparison
    
    Args:
        generator: BaseGenerator instance
        left_card: Left card dictionary (same structure as cards in generate_slide_card_diagram)
        right_card: Right card dictionary (same structure as cards in generate_slide_card_diagram)
        vs_text: Text to display between cards
        color_scheme: Optional ColorScheme for theming
    """
    theme = extract_theme_colors(color_scheme)
    
    def generate_card_html(card: Dict[str, any], card_class: str) -> str:
        title = card.get("title", "")
        tagline = card.get("tagline", "")
        color_key = card.get("color", "gray")
        features = card.get("features", [])
        badge = card.get("badge", "")
        custom_mockup = card.get("custom_mockup", None)
        wireframe_type = card.get("wireframe") or card.get("svg_type")

        palette = ACCENT_MAP.get(color_key, ACCENT_MAP["gray"])

        if custom_mockup:
            if generator.use_svg_js and not custom_mockup.strip().startswith("<"):
                mockup_id = f"mockup-{card_class}"
                svg_mockup = f'<div id="{mockup_id}" style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;"></div><script>(function(){{const draw = SVG().addTo("#{mockup_id}").size(240, 140);{custom_mockup}}})();</script>'
            else:
                svg_mockup = custom_mockup
        elif wireframe_type and str(wireframe_type).lower() in ("before", "after", "chat-panel", "modal-form"):
            svg_mockup = _wireframe_svg_for_card(
                str(wireframe_type).lower(), color_scheme, generator
            )
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
            <div class="slide-card {card_class}" style="border-left: 4px solid {palette['accent']};">
                {badge_html}
                <div class="card-title">{title}</div>
                <div class="card-tagline">{tagline}</div>
                <div class="card-mockup" style="background: {palette['tint']};">{svg_mockup}</div>
                {features_html}
            </div>"""
    
    md_compare_shadow = MD_ELEVATION_1
    md_compare_shadow_hover = MD_ELEVATION_4 if not theme.is_dark else "0 8px 16px -4px rgba(0,0,0,0.35), 0 4px 8px -2px rgba(0,0,0,0.2)"
    css_content = f"""
        {generate_css_variables(theme)}
        
        body {{
            padding: 32px 24px !important;
            background: var(--bg-page);
        }}
        
        .slide-comparison-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 32px;
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
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 500;
            color: var(--text-1);
            margin-bottom: 16px;
            letter-spacing: 0;
            line-height: 1.35;
        }}
        
        .slide-comparison-row {{
            display: flex;
            align-items: center;
            gap: 24px;
            flex-wrap: nowrap;
            justify-content: center;
            width: fit-content;
            max-width: 100%;
        }}
        
        .slide-card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 24px 32px;
            min-width: 320px;
            max-width: 380px;
            position: relative;
            box-shadow: {md_compare_shadow};
            transition: box-shadow 0.2s ease;
        }}
        
        .slide-card:hover {{
            box-shadow: {md_compare_shadow_hover};
        }}
        
        .card-badge {{
            position: absolute;
            top: 16px;
            right: 16px;
            background: {with_alpha(theme.text_tertiary, 0.12)};
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-2);
            letter-spacing: 0.04em;
        }}
        
        .card-title {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 500;
            color: var(--text-1);
            margin-bottom: 8px;
            letter-spacing: 0;
            line-height: 1.35;
        }}
        
        .card-tagline {{
            font-family: var(--font-body);
            font-size: 16px;
            font-weight: 500;
            color: var(--text-2);
            margin-bottom: 16px;
            letter-spacing: 0.015em;
            line-height: 1.5;
        }}
        
        .slide-card .card-mockup {{
            width: 100%;
            height: 160px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
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
            gap: 8px;
        }}
        
        .card-feature {{
            font-family: var(--font-body);
            font-size: 14px;
            font-weight: 400;
            color: var(--text-1);
            letter-spacing: 0.025em;
            line-height: 1.43;
        }}
        
        .card-vs {{
            color: var(--text-3);
            font-size: 24px;
            font-weight: 500;
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
    
    full_html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(full_html, theme)
