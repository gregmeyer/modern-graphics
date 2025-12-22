"""Story-driven slide generator - Compelling Apple-style hero slide"""

import html
import json
import textwrap
from typing import Optional, Dict, List, Tuple, Any
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(ch * 2 for ch in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _calculate_luminance(hex_color: str) -> float:
    r, g, b = [v / 255 for v in _hex_to_rgb(hex_color)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _determine_hero_variant(requested_variant: str, template) -> str:
    variant = (requested_variant or "auto").lower()
    if variant in ("light", "dark"):
        return variant
    template_bg = getattr(template, 'background_color', '#FFFFFF')
    luminance = _calculate_luminance(template_bg)
    # Use dark hero on brighter templates for contrast, light hero otherwise
    return "dark" if luminance > 0.65 else "light"


def _shorten_text(text: Optional[str], width: int) -> str:
    if not text:
        return ""
    return textwrap.shorten(text.strip(), width, placeholder="...")


def _build_static_mini_tile(width: int, height: int, palette: Dict[str, str], data: Dict[str, str]) -> str:
    safe_headline = html.escape((data.get('tile_headline') or data.get('headline') or '')[:36])
    safe_subline = html.escape((data.get('subline') or '')[:48])
    safe_pill = html.escape((data.get('pill') or '')[:24])
    safe_metric = html.escape((data.get('metric') or '')[:48])
    
    padding_x = 48
    column_gap = 32
    metric_column_width = 240
    chart_width = max(220, width - (padding_x * 2) - metric_column_width - column_gap)
    chart_start_x = padding_x
    chart_end_x = chart_start_x + chart_width
    metric_rect_width = metric_column_width
    metric_rect_x = width - padding_x - metric_rect_width
    metric_text_x = metric_rect_x + (metric_rect_width / 2)
    pill_rect_width = min(240, chart_width)
    pill_rect_x = padding_x
    pill_text_x = pill_rect_x + pill_rect_width / 2
    
    values = data.get('chart') or [70, 95, 65, 110]
    chart_top = 220
    chart_bottom_margin = 80
    chart_base_y = height - chart_bottom_margin
    chart_height = max(120, chart_base_y - chart_top)
    step = chart_width / max(len(values) - 1, 1)
    
    points = []
    for idx, value in enumerate(values):
        clamped = max(40, min(160, value))
        x = chart_start_x + idx * step
        y = chart_base_y - (clamped / 160) * chart_height
        points.append((x, y))
    
    area_path = []
    if points:
        area_path.append(f"M {points[0][0]} {chart_base_y}")
        area_path.append(f"L {points[0][0]} {points[0][1]}")
        for px, py in points[1:]:
            area_path.append(f"L {px} {py}")
        area_path.append(f"L {points[-1][0]} {chart_base_y} Z")
    area_path_str = ' '.join(area_path) if area_path else ''
    
    line_path = []
    if points:
        line_path.append(f"M {points[0][0]} {points[0][1]}")
        for px, py in points[1:]:
            line_path.append(f"L {px} {py}")
    line_path_str = ' '.join(line_path) if line_path else ''
    
    circles_svg = '\n'.join(
        f'<circle cx="{px}" cy="{py}" r="4" fill="{palette["accent_primary"]}" opacity="0.8"/>'
        for px, py in points
    )
    
    def wrap_text(text: str, limit: int = 32) -> list:
        words = text.split()
        if not words:
            return ['']
        lines = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) > limit and current:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines[:2]
    
    metric_lines = wrap_text(safe_metric, 22)
    metric_tspans = []
    for idx, line in enumerate(metric_lines):
        dy = "0" if idx == 0 else "1.2em"
        metric_tspans.append(f'<tspan x="{metric_text_x}" dy="{dy}">{line}</tspan>')
    metric_text_svg = ''.join(metric_tspans)
    
    metric_rect_height = 120
    metric_rect_y = max(chart_top, chart_top + (chart_height - metric_rect_height) / 2)
    metric_text_y = metric_rect_y + (metric_rect_height / 2) - 6
    
    return f"""
            <svg class="hero-mini-tile-svg" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Story insight tile">
                <rect x="0" y="0" width="{width}" height="{height}" rx="28" fill="{palette['background']}" stroke="{palette['border']}" stroke-width="2"/>
                <text x="{padding_x}" y="96" font-family="Inter, -apple-system, sans-serif" font-size="24" font-weight="700" fill="{palette['text_primary']}">{safe_headline}</text>
                <text x="{padding_x}" y="136" font-family="Inter, -apple-system, sans-serif" font-size="14" font-weight="500" fill="{palette['text_secondary']}" opacity="0.9">{safe_subline}</text>
                <rect x="{pill_rect_x}" y="164" width="{pill_rect_width}" height="36" rx="18" fill="{palette['metric_bg']}"/>
                <text x="{pill_text_x}" y="187" font-family="Inter, -apple-system, sans-serif" font-size="13" font-weight="600" fill="{palette['text_primary']}" text-anchor="middle">{safe_pill}</text>
                <line x1="{chart_start_x}" y1="{chart_base_y}" x2="{chart_end_x}" y2="{chart_base_y}" stroke="{palette['border']}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
                {f'<path d="{area_path_str}" fill="{palette["metric_bg"]}" opacity="0.6"/>' if area_path_str else ''}
                {f'<path d="{line_path_str}" stroke="{palette["accent_primary"]}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' if line_path_str else ''}
                {circles_svg}
                <rect x="{metric_rect_x}" y="{metric_rect_y}" width="{metric_rect_width}" height="{metric_rect_height}" rx="32" fill="{palette['metric_bg']}" opacity="0.95" stroke="{palette['border']}" stroke-width="1.5"/>
                <text x="{metric_text_x}" y="{metric_text_y}" font-family="Inter, -apple-system, sans-serif" font-size="15" font-weight="600" fill="{palette['metric_text']}" text-anchor="middle" dominant-baseline="middle">
                    {metric_text_svg}
                </text>
            </svg>
        """


def _generate_hero_content_with_prompt(
    what_changed: str,
    time_period: str,
    what_it_means: str,
    title: str,
    hero_prompt: Optional[str] = None
) -> Tuple[str, str]:
    """
    Generate hero headline and subheadline using OpenAI prompt
    
    Args:
        what_changed: What changed (the change)
        time_period: Over what time period
        what_it_means: What it means (the meaning/implication)
        title: Main slide title
        hero_prompt: Optional custom prompt. If None, uses default prompt.
        
    Returns:
        Tuple of (headline, subheadline)
    """
    try:
        from ..env_config import get_openai_key
        api_key = get_openai_key()
        if not api_key:
            # Fallback to default if no API key
            return title, "Start Building Stories"
        
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        # Default prompt if none provided
        if hero_prompt is None:
            hero_prompt = """Create a compelling hero headline and subheadline for a story-driven slide.

The story is about:
- What Changed: {what_changed}
- Time Period: {time_period}
- What It Means: {what_it_means}
- Title: {title}

Generate:
1. A powerful, concise headline (5-8 words max, impactful, forward-looking)
2. A compelling subheadline (8-15 words, explains the transformation or opportunity)

Format as JSON:
{{"headline": "...", "subheadline": "..."}}

Make it inspiring, modern, and focused on the transformation or opportunity.""".format(
                what_changed=what_changed,
                time_period=time_period,
                what_it_means=what_it_means,
                title=title
            )
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert at creating compelling, modern hero headlines for presentations. Always respond with valid JSON."},
                {"role": "user", "content": hero_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=200
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        headline = result.get("headline", title)
        subheadline = result.get("subheadline", "Start Building Stories")
        
        return headline, subheadline
        
    except Exception as e:
        # Fallback to defaults on any error
        return title, "Start Building Stories"


def generate_story_slide(
    generator: BaseGenerator,
    title: Optional[str] = None,
    what_changed: Optional[str] = None,
    time_period: Optional[str] = None,
    what_it_means: Optional[str] = None,
    prompt: Optional[str] = None,
    insight: Optional[str] = None,
    evolution_data: Optional[List[Dict[str, str]]] = None,
    hero_headline: Optional[str] = None,
    hero_subheadline: Optional[str] = None,
    hero_prompt: Optional[str] = None,
    use_ai_hero: bool = True,
    use_unified: bool = True,
    top_tile_only: bool = False,
    hero_use_svg_js: bool = False,
    hero_variant: str = "auto",
    story_cards: Optional[List[Dict[str, Any]]] = None,
    hero_canvas_cards: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Generate a compelling story-driven hero slide
    
    Supports both prompt-based (new) and parameter-based (legacy) approaches.
    If prompt is provided, uses unified generator. Otherwise uses legacy parameters.
    
    Args:
        generator: BaseGenerator instance
        prompt: Optional prompt describing the story (preferred, uses unified generator)
        title: Main slide title (legacy parameter)
        what_changed: What changed (the change) (legacy parameter)
        time_period: Over what time period (legacy parameter)
        what_it_means: What it means (the meaning/implication) (legacy parameter)
        insight: Optional key insight/takeaway
        evolution_data: Optional list of evolution stages
        hero_headline: Optional custom hero headline (overrides AI generation)
        hero_subheadline: Optional custom hero subheadline (overrides AI generation)
        hero_prompt: Optional custom prompt for AI hero generation
        use_ai_hero: If True, use AI to generate hero content (default: True)
        use_unified: If True and prompt provided, use unified generator (default: True)
        top_tile_only: If True, render only the hero tile (hide framework/insight tiles)
        hero_use_svg_js: Retained for backward compatibility (static SVG used by default)
        hero_variant: "auto", "light", or "dark" to control hero styling
        story_cards: Optional list of card modules to render beneath the hero (defaults to insight tiles)
        hero_canvas_cards: Optional list of compact card modules rendered inside the hero canvas
    """
    # If prompt provided, use unified generator
    if prompt and use_unified:
        try:
            from .unified_story_slide import generate_unified_story_slide
            return generate_unified_story_slide(generator, prompt)
        except Exception as e:
            # Fallback to legacy if unified fails
            print(f"Unified generator failed, using legacy: {e}")
    
    # Legacy parameter-based approach
    if not title:
        title = "Data Story"
    if not what_changed:
        what_changed = "Data transformation"
    if not time_period:
        time_period = "Recent period"
    if not what_it_means:
        what_it_means = "Significant change"
    
    if insight is None:
        insight = "What changed, over what time period, and what does it mean? This is the basic insight you're building when you tell a story about data."
    
    if evolution_data is None:
        evolution_data = [
            {'era': '2010s', 'label': 'Manual Slides', 'icon': '📊'},
            {'era': '2020s', 'label': 'Automated Slides', 'icon': '⚡'},
            {'era': '2024+', 'label': 'Story-Driven', 'icon': '✨'}
        ]
    
    # Generate hero content - default to AI if available
    if hero_headline and hero_subheadline:
        # Use provided custom content
        final_headline = hero_headline
        final_subheadline = hero_subheadline
    elif use_ai_hero:
        # Generate with AI prompt (default behavior)
        try:
            final_headline, final_subheadline = _generate_hero_content_with_prompt(
                what_changed, time_period, what_it_means, title, hero_prompt
            )
        except Exception:
            # Fallback if AI fails
            final_headline = title
            final_subheadline = "Start Building Stories"
    else:
        # Use defaults
        final_headline = title
        final_subheadline = "Start Building Stories"
    
    # Hero visual: Forward-looking story-driven transformation
    # Shows: Manual pain → Story input → Dynamic AI-generated output
    hero_visual = """<svg viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg">
        <!-- Left: The Tension - Manual slide building with last-minute change -->
        <g opacity="0.75">
            <!-- Person working on slide -->
            <circle cx="100" cy="140" r="20" fill="rgba(255,255,255,0.4)" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
            <rect x="90" y="160" width="20" height="35" rx="10" fill="rgba(255,255,255,0.4)" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
            
            <!-- Slide being edited manually -->
            <rect x="50" y="220" width="100" height="70" rx="6" fill="rgba(255,255,255,0.2)" stroke="rgba(255,255,255,0.6)" stroke-width="2.5"/>
            <!-- Content lines -->
            <line x1="60" y1="235" x2="140" y2="235" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <line x1="60" y1="250" x2="120" y2="250" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <rect x="65" y="260" width="40" height="20" rx="3" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
            
            <!-- Last-minute change indicator (red alert) -->
            <circle cx="160" cy="180" r="18" fill="rgba(255,59,48,0.4)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5"/>
            <text x="160" y="188" font-family="-apple-system" font-size="20" font-weight="700" fill="rgba(255,255,255,0.95)" text-anchor="middle">!</text>
            <!-- Stress lines -->
            <path d="M 145 165 L 150 160 M 175 165 L 170 160 M 145 195 L 150 200 M 175 195 L 170 200" stroke="rgba(255,255,255,0.7)" stroke-width="2" stroke-linecap="round"/>
            
            <!-- Manual tools scattered -->
            <rect x="30" y="120" width="12" height="25" rx="2" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5" transform="rotate(-30 36 132)"/>
            <rect x="170" y="110" width="15" height="15" rx="2" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
        </g>
        
        <!-- Transformation arrow -->
        <path d="M 220 255 L 320 255" stroke="rgba(255,255,255,0.9)" stroke-width="10" stroke-linecap="round"/>
        <path d="M 310 245 L 320 255 L 310 265" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        
        <!-- Center: Your Story (the input) - Forward-looking, aspirational -->
        <g opacity="0.95">
            <!-- Story container (modern, fluid) -->
            <path d="M 340 100 Q 380 80 450 100 Q 480 120 450 140 Q 480 160 450 180 Q 480 200 450 220 Q 420 240 380 220 Q 340 200 360 180 Q 340 160 360 140 Q 340 120 360 100 Z" 
                  fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.9)" stroke-width="3.5"/>
            
            <!-- Story elements (narrative flow) -->
            <path d="M 370 120 Q 400 110 430 120" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round"/>
            <path d="M 375 150 Q 400 145 425 150" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round"/>
            <path d="M 370 180 Q 400 175 430 180" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round"/>
            
            <!-- Story points -->
            <circle cx="370" cy="120" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="400" cy="110" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="430" cy="120" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="400" cy="150" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="400" cy="180" r="4" fill="rgba(255,255,255,0.9)"/>
            
            <!-- AI assistance indicator (subtle, modern) -->
            <circle cx="420" cy="100" r="5" fill="rgba(255,255,255,0.9)"/>
            <circle cx="425" cy="105" r="3" fill="rgba(255,255,255,0.7)"/>
            <circle cx="415" cy="105" r="3" fill="rgba(255,255,255,0.7)"/>
            <!-- Iteration/update symbol -->
            <path d="M 380 200 Q 400 195 420 200" stroke="rgba(52,199,89,0.8)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-dasharray="3,3"/>
        </g>
        
        <!-- Arrow: Story generates slides -->
        <path d="M 500 255 L 600 255" stroke="rgba(255,255,255,0.9)" stroke-width="10" stroke-linecap="round"/>
        <path d="M 590 245 L 600 255 L 590 265" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        
        <!-- Right: Dynamic Output - Slides generated from story -->
        <g opacity="0.95">
            <!-- Slides flowing out (dynamic, varied) -->
            <rect x="650" y="100" width="80" height="60" rx="6" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" transform="rotate(-8 690 130)"/>
            <rect x="670" y="180" width="80" height="60" rx="6" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5"/>
            <rect x="650" y="260" width="80" height="60" rx="6" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" transform="rotate(8 690 290)"/>
            
            <!-- Dynamic content (varied, showing AI generation) -->
            <!-- Slide 1: Chart/data -->
            <rect x="665" y="115" width="60" height="6" rx="3" fill="rgba(255,255,255,0.7)"/>
            <rect x="665" y="125" width="50" height="6" rx="3" fill="rgba(255,255,255,0.6)"/>
            <rect x="670" y="135" width="20" height="15" rx="2" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1"/>
            <rect x="695" y="140" width="20" height="10" rx="2" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1"/>
            
            <!-- Slide 2: Text/story -->
            <rect x="685" y="195" width="60" height="6" rx="3" fill="rgba(255,255,255,0.7)"/>
            <rect x="685" y="205" width="55" height="6" rx="3" fill="rgba(255,255,255,0.6)"/>
            <rect x="685" y="215" width="45" height="6" rx="3" fill="rgba(255,255,255,0.5)"/>
            <rect x="685" y="225" width="50" height="6" rx="3" fill="rgba(255,255,255,0.5)"/>
            
            <!-- Slide 3: Visual/infographic -->
            <rect x="665" y="275" width="60" height="6" rx="3" fill="rgba(255,255,255,0.7)"/>
            <circle cx="680" cy="295" r="8" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
            <circle cx="700" cy="295" r="8" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
            <circle cx="720" cy="295" r="8" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
            
            <!-- Flow lines showing generation from story -->
            <path d="M 500 255 Q 550 200 650 130" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" fill="none" stroke-dasharray="5,5" opacity="0.7"/>
            <path d="M 500 255 Q 575 255 670 210" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" fill="none" stroke-dasharray="5,5" opacity="0.7"/>
            <path d="M 500 255 Q 550 310 650 290" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" fill="none" stroke-dasharray="5,5" opacity="0.7"/>
            
            <!-- Update/iteration indicator (showing dynamic nature) -->
            <circle cx="750" cy="120" r="12" fill="rgba(52,199,89,0.4)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5"/>
            <path d="M 745 120 L 750 128 L 755 115" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
        
        <!-- Labels - Emotionally resonant, not corporate -->
        <text x="100" y="310" font-family="-apple-system" font-size="20" font-weight="600" fill="rgba(255,255,255,0.85)" text-anchor="middle">The Tension</text>
        <text x="100" y="330" font-family="-apple-system" font-size="15" font-weight="500" fill="rgba(255,255,255,0.65)" text-anchor="middle">Perfect slides, last-minute changes</text>
        
        <text x="400" y="85" font-family="-apple-system" font-size="22" font-weight="700" fill="rgba(255,255,255,0.95)" text-anchor="middle">Your Story</text>
        <text x="400" y="105" font-family="-apple-system" font-size="15" font-weight="500" fill="rgba(255,255,255,0.75)" text-anchor="middle">Narrative + AI assistance</text>
        
        <text x="700" y="310" font-family="-apple-system" font-size="20" font-weight="600" fill="rgba(255,255,255,0.85)" text-anchor="middle">Dynamic Output</text>
        <text x="700" y="330" font-family="-apple-system" font-size="15" font-weight="500" fill="rgba(255,255,255,0.65)" text-anchor="middle">Slides that evolve with your story</text>
    </svg>"""

    # Generate evolution timeline HTML
    evolution_html = ''
    for i, stage in enumerate(evolution_data):
        is_last = i == len(evolution_data) - 1
        evolution_html += f"""
            <div class="evolution-stage">
                <div class="evolution-icon">{stage.get('icon', '•')}</div>
                <div class="evolution-era">{stage['era']}</div>
                <div class="evolution-label">{stage['label']}</div>
            </div>"""
        if not is_last:
            evolution_html += '<div class="evolution-arrow">→</div>'
    
    # Generate SVG icons for story elements - avoiding clichés, forward-looking
    what_changed_icon = """<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Transformation: Input/Output flip -->
        <rect x="15" y="20" width="20" height="15" rx="2" fill="#007AFF" opacity="0.2" stroke="#007AFF" stroke-width="2"/>
        <rect x="15" y="40" width="20" height="15" rx="2" fill="#007AFF" opacity="0.2" stroke="#007AFF" stroke-width="2"/>
        <path d="M 45 27 L 55 27" stroke="#8243B5" stroke-width="3" stroke-linecap="round"/>
        <path d="M 50 22 L 55 27 L 50 32" stroke="#8243B5" stroke-width="3" fill="none" stroke-linecap="round"/>
        <!-- Output (story arc) -->
        <path d="M 60 20 Q 70 15 75 20 Q 70 25 60 30" stroke="#8243B5" stroke-width="3.5" fill="rgba(130,67,181,0.15)" stroke-linecap="round"/>
        <path d="M 60 40 Q 70 35 75 40 Q 70 45 60 50" stroke="#8243B5" stroke-width="3.5" fill="rgba(130,67,181,0.15)" stroke-linecap="round"/>
    </svg>"""
    
    time_period_icon = """<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Modern timeline indicator -->
        <line x1="20" y1="40" x2="60" y2="40" stroke="#8E8E93" stroke-width="3" stroke-linecap="round"/>
        <circle cx="20" cy="40" r="5" fill="#8E8E93"/>
        <circle cx="40" cy="40" r="5" fill="#8E8E93"/>
        <circle cx="60" cy="40" r="8" fill="#8243B5" stroke="#8243B5" stroke-width="2"/>
        <circle cx="60" cy="40" r="4" fill="#FFFFFF"/>
        <!-- 2024 label -->
        <text x="60" y="65" font-family="-apple-system" font-size="13" font-weight="700" fill="#8243B5" text-anchor="middle">2024</text>
    </svg>"""
    
    what_it_means_icon = """<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Forward-looking: Focus shift visualization -->
        <rect x="20" y="25" width="25" height="18" rx="3" fill="#8E8E93" opacity="0.2" stroke="#8E8E93" stroke-width="2"/>
        <path d="M 50 34 L 60 34" stroke="#8243B5" stroke-width="3" stroke-linecap="round"/>
        <path d="M 55 29 L 60 34 L 55 39" stroke="#8243B5" stroke-width="3" fill="none" stroke-linecap="round"/>
        <!-- Narrative focus (story arc) -->
        <path d="M 60 20 Q 70 15 75 25 Q 70 35 60 40 Q 65 30 60 20" stroke="#8243B5" stroke-width="3.5" fill="rgba(130,67,181,0.2)" stroke-linecap="round"/>
        <!-- Forward arrow -->
        <path d="M 65 45 L 70 50 L 65 55" stroke="#1B7A4E" stroke-width="3" fill="none" stroke-linecap="round"/>
    </svg>"""

    template = getattr(generator, 'template', generator.template)
    resolved_hero_variant = _determine_hero_variant(hero_variant, template)
    hero_grad_start, hero_grad_end = template.get_gradient('purple')
    accent_start, accent_end = template.get_gradient('blue')
    
    if resolved_hero_variant == "dark":
        body_background = f"linear-gradient(135deg, {hero_grad_start} 0%, {hero_grad_end} 100%)"
        hero_section_background = f"linear-gradient(145deg, {hero_grad_start}, {hero_grad_end})"
        hero_border_color = "rgba(255, 255, 255, 0.15)"
        hero_text_primary = "#FFFFFF"
        hero_text_secondary = "rgba(255, 255, 255, 0.85)"
        tile_card_bg = "#141416"
        tile_card_border = "rgba(255, 255, 255, 0.2)"
        tile_text_primary = "#FFFFFF"
        tile_text_secondary = "rgba(255, 255, 255, 0.65)"
        tile_pill_bg = "rgba(255, 255, 255, 0.12)"
        tile_pill_text = "#FFFFFF"
        metric_bg = "rgba(255, 255, 255, 0.12)"
        metric_text = "#FFFFFF"
        tile_wrapper_tint = f"linear-gradient(135deg, {hero_grad_start}33, {hero_grad_end}55)"
        tile_card_shadow = "0 20px 40px rgba(0, 0, 0, 0.45)"
        hero_box_shadow = "0 28px 60px rgba(0, 0, 0, 0.45)"
    else:
        body_background = getattr(template, 'background_color', '#F5F5F5')
        hero_section_background = "#FFFFFF"
        hero_border_color = "rgba(0, 0, 0, 0.06)"
        hero_text_primary = "#1D1D1F"
        hero_text_secondary = "#4A4A4A"
        tile_card_bg = "#FFFFFF"
        tile_card_border = "rgba(0, 0, 0, 0.06)"
        tile_text_primary = "#111111"
        tile_text_secondary = "rgba(0, 0, 0, 0.55)"
        tile_pill_bg = "rgba(0, 0, 0, 0.05)"
        tile_pill_text = "#1D1D1F"
        metric_bg = "rgba(0, 0, 0, 0.04)"
        metric_text = "#1D1D1F"
        tile_wrapper_tint = f"linear-gradient(135deg, {hero_grad_start}1A, {hero_grad_end}33)"
        tile_card_shadow = "0 12px 30px rgba(0, 0, 0, 0.12)"
        hero_box_shadow = "0 24px 48px rgba(0, 0, 0, 0.12)"
    
    chart_seed = sum(ord(c) for c in (what_changed or "story"))
    chart_values = [60 + ((chart_seed + i * 11) % 50) for i in range(4)]
    hero_svg_data = {
        "tile_headline": _shorten_text(what_changed or final_headline, 40),
        "headline": final_headline or "",
        "subline": _shorten_text(final_subheadline or what_it_means, 55),
        "pill": _shorten_text(time_period, 24),
        "metric": _shorten_text(what_it_means, 44),
        "chart": chart_values
    }
    tile_palette = {
        "background": tile_card_bg,
        "border": tile_card_border,
        "text_primary": tile_text_primary,
        "text_secondary": tile_text_secondary,
        "pill_bg": tile_pill_bg,
        "pill_text": tile_pill_text,
        "accent_primary": accent_start,
        "accent_secondary": accent_end,
        "chart_fill": accent_end,
        "metric_bg": metric_bg,
        "metric_text": metric_text
    }
    cards_data = story_cards if story_cards is not None else _default_story_cards(
        what_changed,
        time_period,
        what_it_means,
        what_changed_icon,
        time_period_icon,
        what_it_means_icon
    )
    canvas_cards_html = ""
    if hero_canvas_cards:
        canvas_cards_html = f"""
                <div class="hero-mockup-cards">
                    {''.join(_render_story_card_module(card, variant="compact") for card in hero_canvas_cards)}
                </div>
        """
    hero_mockup_inner = f"""
            <div class="hero-mockup-wrapper">
                {_build_static_mini_tile(640, 400, tile_palette, hero_svg_data)}
                {canvas_cards_html}
            </div>
        """
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {body_background};
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .story-slide-container {{
            max-width: 1800px;
            width: 100%;
            background: #FFFFFF;
            border-radius: 0;
            padding: 0;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.12), 0 16px 32px rgba(0, 0, 0, 0.08);
            position: relative;
            overflow: hidden;
        }}
        
        .story-slide-container.top-tile-only {{
            max-width: 1200px;
            border-radius: 32px;
            padding: 40px 32px 48px;
            box-shadow: 0 24px 48px rgba(0, 0, 0, 0.12);
        }}
        
        .story-slide-container.top-tile-only .hero-section {{
            margin: 0 auto;
        }}
        
        .hero-section {{
            position: relative;
            background: {hero_section_background};
            border: 1px solid {hero_border_color};
            border-radius: 24px;
            padding: 60px 80px;
            margin: 40px auto;
            max-width: 1000px;
            box-shadow: {hero_box_shadow};
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            overflow: visible;
        }}
        
        .hero-section .hero-headline,
        .hero-section .hero-subheadline {{
            position: relative;
            z-index: 2;
        }}
        
        .hero-headline {{
            font-size: 56px;
            font-weight: 700;
            color: {hero_text_primary};
            margin-bottom: 16px;
            letter-spacing: -0.04em;
            line-height: 1.1;
            position: relative;
        }}
        
        .hero-subheadline {{
            font-size: 24px;
            font-weight: 600;
            color: {hero_text_secondary};
            letter-spacing: -0.02em;
            line-height: 1.3;
            margin-bottom: 40px;
            opacity: 0.9;
            position: relative;
        }}
        
        .hero-visual {{
            margin-top: 48px;
            width: 100%;
            display: flex;
            justify-content: center;
            position: relative;
        }}
        
        .hero-slide-mockup {{
            width: 100%;
            max-width: 720px;
            padding: 24px;
            border-radius: 28px;
            background: {tile_wrapper_tint};
            box-shadow: {tile_card_shadow};
            position: relative;
        }}
        
        .hero-mockup-wrapper {{
            position: relative;
        }}
        
        .hero-mini-tile-svg {{
            width: 100%;
            max-width: 640px;
            display: block;
            margin: 0 auto;
            filter: drop-shadow(0 35px 50px rgba(0,0,0,0.15));
        }}
        
        .hero-mockup-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin-top: 28px;
        }}
        
        .story-card {{
            border-radius: 24px;
            padding: 24px;
            background: {tile_card_bg};
            border: 1px solid {tile_card_border};
            box-shadow: 0 16px 30px rgba(0, 0, 0, 0.08);
        }}
        
        .story-card--compact {{
            padding: 18px;
            border-radius: 20px;
        }}
        
        .story-card-label {{
            font-size: 14px;
            font-weight: 600;
            color: {tile_text_secondary};
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}
        
        .story-card-value {{
            font-size: 20px;
            font-weight: 700;
            color: {tile_text_primary};
            line-height: 1.4;
        }}
        
        .story-framework-section {{
            background: {body_background};
            padding: 80px 80px 0;
        }}
        
        .story-framework {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 28px;
            margin-bottom: 40px;
        }}
        
        .story-card-icon {{
            font-size: 18px;
            width: 44px;
            height: 44px;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.65);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 18px;
        }}
        
        .story-card-title {{
            font-size: 20px;
            font-weight: 700;
            color: #111111;
        }}
        
        .story-card-subtitle {{
            font-size: 13px;
            font-weight: 500;
            color: rgba(17, 24, 39, 0.65);
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}
        
        .story-card-funnel {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 8px;
        }}
        
        .story-card-funnel-stage {{
            background: rgba(255, 255, 255, 0.18);
            border-radius: 14px;
            padding: 10px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            color: #F8FAFC;
            backdrop-filter: saturate(120%);
        }}
        
        .story-card--funnel {{
            background: linear-gradient(135deg, #0F172A, #1F2937);
            color: #F8FAFC;
        }}
        
        .story-card--pyramid {{
            background: linear-gradient(135deg, #111827, #1f2933);
            color: #F8FAFC;
        }}
        
        .story-card-pyramid {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 12px;
        }}
        
        .story-card-pyramid-layer {{
            align-self: center;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 8px 14px;
            text-align: center;
            font-weight: 600;
            font-size: 13px;
        }}
        
        .evolution-section {{
            padding: 60px 100px;
            background: linear-gradient(135deg, #F5F5F7 0%, #F5F5F7 100%);
        }}
        
        .evolution-timeline {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 32px;
            flex-wrap: wrap;
        }}
        
        .evolution-stage {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            min-width: 140px;
        }}
        
        .evolution-icon {{
            font-size: 48px;
            line-height: 1;
        }}
        
        .evolution-era {{
            font-size: 20px;
            font-weight: 700;
            color: #8243B5;
            letter-spacing: -0.02em;
        }}
        
        .evolution-label {{
            font-size: 16px;
            font-weight: 500;
            color: #8E8E93;
            text-align: center;
        }}
        
        .evolution-arrow {{
            color: #8243B5;
            font-size: 36px;
            font-weight: 600;
            opacity: 0.6;
        }}
        
        .insight-section {{
            background: linear-gradient(135deg, #AF52DE 0%, #8243B5 100%);
            padding: 80px 100px;
            position: relative;
            overflow: hidden;
        }}
        
        .insight-section::before {{
            content: '';
            position: absolute;
            top: -40%;
            right: -5%;
            width: 500px;
            height: 500px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
        }}
        
        .insight-label {{
            font-size: 13px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 24px;
            text-align: center;
        }}
        
        .insight-text {{
            font-size: 42px;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.03em;
            line-height: 1.4;
            text-align: center;
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    container_classes = "story-slide-container"
    if top_tile_only:
        container_classes += " top-tile-only"
    
    hero_section_html = f"""
        <div class="hero-section">
            <div class="hero-headline">{final_headline}</div>
            <div class="hero-subheadline">{final_subheadline}</div>
            <div class="hero-visual">
                <div class="hero-slide-mockup">
                    {hero_mockup_inner}
                </div>
            </div>
        </div>"""
    
    framework_section_html = ""
    insight_section_html = ""
    if not top_tile_only:
        cards_html = '\n'.join(_render_story_card_module(card, variant="default") for card in cards_data)
        framework_section_html = f"""
        <div class="story-framework-section">
            <div class="story-framework">
{cards_html}
            </div>
            
            <div class="evolution-section">
                <div class="evolution-timeline">
{evolution_html}
                </div>
            </div>
        </div>"""
        insight_section_html = f"""
        <div class="insight-section">
            <div class="insight-label">The Core Insight</div>
            <div class="insight-text">{insight}</div>
        </div>"""
    html_content = f"""
    <div class="{container_classes}">
{hero_section_html}
{framework_section_html}
{insight_section_html}
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


    
def _default_story_cards(
    what_changed: str,
    time_period: str,
    what_it_means: str,
    what_changed_icon: str,
    time_period_icon: str,
    what_it_means_icon: str
) -> List[Dict[str, Any]]:
    return [
        {
            "type": "insight",
            "label": "What Changed",
            "value": what_changed,
            "icon": what_changed_icon,
            "background": "linear-gradient(135deg, #EBF5FF 0%, #E3F2FD 100%)",
            "border_color": "rgba(11, 100, 208, 0.2)"
        },
        {
            "type": "insight",
            "label": "Time Period",
            "value": time_period,
            "icon": time_period_icon,
            "background": "linear-gradient(135deg, #F5F5F7 0%, #F5F5F7 100%)",
            "border_color": "rgba(58, 58, 60, 0.15)"
        },
        {
            "type": "insight",
            "label": "What It Means",
            "value": what_it_means,
            "icon": what_it_means_icon,
            "background": "linear-gradient(135deg, #F0F9F4 0%, #E8F5E9 100%)",
            "border_color": "rgba(27, 122, 78, 0.2)"
        }
    ]


def _render_story_card_module(
    module: Dict[str, Any],
    variant: str = "default"
) -> str:
    module_type = module.get("type", "insight")
    if module_type == "funnel":
        return _render_funnel_card(module, variant)
    if module_type == "pyramid":
        return _render_pyramid_card(module, variant)
    return _render_insight_card(module, variant)


def _render_insight_card(module: Dict[str, Any], variant: str) -> str:
    background = module.get("background", "#FFFFFF")
    border_color = module.get("border_color", "rgba(0, 0, 0, 0.06)")
    icon_html = f'<div class="story-card-icon">{module.get("icon", "")}</div>' if module.get("icon") else ""
    value = module.get("value", "")
    label = module.get("label", "")
    return f"""
        <div class="story-card story-card--insight story-card--{variant}" style="background:{background}; border: 2px solid {border_color};">
            {icon_html}
            <div class="story-card-label">{label}</div>
            <div class="story-card-value">{value}</div>
        </div>
    """


def _render_funnel_card(module: Dict[str, Any], variant: str) -> str:
    stages = module.get("stages") or [
        {"label": "Awareness", "value": 1500},
        {"label": "Consideration", "value": 780},
        {"label": "Decision", "value": 340},
        {"label": "Won", "value": 180}
    ]
    max_value = max(stage.get("value", 0) for stage in stages) or 1
    min_width = 40
    max_width = 92
    step = (max_width - min_width) / max(len(stages) - 1, 1)
    stage_rows = []
    for idx, stage in enumerate(stages):
        width_pct = max_width - idx * step
        pct = (stage.get("value", 0) / max_value) * 100
        stage_rows.append(f"""
            <div class="story-card-funnel-stage" style="width:{width_pct}%">
                <span>{stage.get("label")}</span>
                <strong>{pct:.0f}%</strong>
            </div>
        """)
    title = module.get("title", "Conversion Funnel")
    subtitle = module.get("subtitle", "Drop-off per stage")
    return f"""
        <div class="story-card story-card--funnel story-card--{variant}">
            <div class="story-card-title">{title}</div>
            <div class="story-card-subtitle">{subtitle}</div>
            <div class="story-card-funnel">
                {''.join(stage_rows)}
            </div>
        </div>
    """


def _render_pyramid_card(module: Dict[str, Any], variant: str) -> str:
    layers = module.get("layers") or [
        {"label": "Vision"},
        {"label": "Strategy"},
        {"label": "Execution"},
        {"label": "Impact"}
    ]
    max_width = 95
    min_width = 55
    step = (max_width - min_width) / max(len(layers) - 1, 1)
    rows = []
    for idx, layer in enumerate(layers):
        width_pct = max_width - idx * step
        rows.append(f"""
            <div class="story-card-pyramid-layer" style="width:{width_pct}%">
                <span>{layer.get("label")}</span>
            </div>
        """)
    title = module.get("title", "Priority Stack")
    subtitle = module.get("subtitle", "Top initiatives")
    return f"""
        <div class="story-card story-card--pyramid story-card--{variant}">
            <div class="story-card-title">{title}</div>
            <div class="story-card-subtitle">{subtitle}</div>
            <div class="story-card-pyramid">
                {''.join(rows)}
            </div>
        </div>
    """
