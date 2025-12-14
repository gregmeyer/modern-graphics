"""Editorial-style story slide generator - engaging one-page website design"""

import json
import math
from typing import Optional, Dict, List
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from ..env_config import get_openai_key


def generate_editorial_story_slide(
    generator: BaseGenerator,
    prompt: str,
    model: str = "gpt-4-turbo-preview",
    use_unified: bool = False
) -> str:
    """Generate an editorial-style, engaging story slide from a prompt
    
    Creates a one-page website-like design that captivates viewers through:
    - Dynamic typography and scale
    - Asymmetric, flowing layouts
    - Visual hierarchy and rhythm
    - Creative use of whitespace
    - Overlapping elements
    - Editorial design principles
    
    Args:
        generator: BaseGenerator instance
        prompt: Detailed prompt describing the story/data visualization
        model: OpenAI model to use
        use_unified: If True, use unified generator with visualization hero (default: False, keeps editorial style)
    """
    # Optionally delegate to unified generator
    if use_unified:
        try:
            from .unified_story_slide import generate_unified_story_slide
            return generate_unified_story_slide(generator, prompt, model)
        except Exception as e:
            # Fallback to editorial if unified fails
            print(f"Unified generator failed, using editorial: {e}")
    api_key = get_openai_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    try:
        import openai
    except ImportError:
        raise ImportError("openai package required")
    
    client = openai.OpenAI(api_key=api_key)
    
    # Ask AI to understand the essence and design an editorial layout
    system_prompt = """You are an editorial designer creating a captivating one-page story visualization.

Your job is to understand the ESSENCE and EMOTION of the story and design a visually engaging layout that:
- Captivates viewers immediately (think magazine cover, not dashboard)
- Uses dynamic typography with dramatic scale changes
- Creates visual flow and rhythm (elements guide the eye)
- Feels like editorial design - asymmetric, flowing, unexpected
- Combines data visualization with narrative elements creatively
- Uses whitespace strategically (not cramped blocks)
- Creates visual interest through scale, positioning, overlap
- Uses modern design techniques: glassmorphism, floating elements, subtle animations, depth

Design principles (think Apple keynote, modern web design, not PowerPoint):
- Massive headlines (96-120px) with strategic word emphasis
- Asymmetric layouts that feel natural, not grid-based
- Creative use of whitespace (let elements breathe)
- Visual elements that support the narrative (not just display data)
- Data visualizations integrated naturally into the flow
- Overlapping elements for depth and interest
- Color used strategically for emphasis (not everywhere)
- Typography hierarchy that guides the eye
- Glassmorphism effects (backdrop blur, translucent cards)
- Floating metric cards with subtle animations
- Rich shadows and depth for visual interest
- Smooth transitions and hover states (even if static)

SPECIAL: If the prompt requests a COMBO CHART or DUAL-AXIS visualization:
- Set visualization_type to "combo"
- Provide both primary_visualization AND secondary_visualization
- primary_visualization: {type: "line|area", data_points: [...], name: "...", color: "..."}
- secondary_visualization: {type: "bars|spikes", data_points: [...], name: "...", color: "..."}
- Both should share the same time axis (x values)

Return JSON with:
- headline: Bold, impactful headline (the hook - make it dramatic)
- subheadline: Supporting narrative text (conversational, not corporate)
- design_essence: The core visual concept/feeling (e.g., "urgent growth", "quiet transformation")
- color_scheme: "dark" (dark background, light text), "light" (light background, dark text), or "gradient" (colorful gradient)
- layout_style: "hero_focused" (massive headline + integrated chart), "split_screen" (visual/narrative split), "flowing_narrative" (elements flow down), "data_hero" (chart is hero), or "editorial_spread" (magazine style)
- visualization_type: "single" or "combo" (for dual-axis combo charts)
- primary_visualization: {type: "line|bar|area", data_points: [...], style: "minimal|bold|integrated", name: "...", color: "..."}
- secondary_visualization: {type: "bars|spikes", data_points: [...], name: "...", color: "..."} - ONLY if visualization_type is "combo"
- key_metrics: [{label: "...", value: "...", emphasis: "high|medium|low"}] - 2-3 max, make them count
- narrative_elements: [{type: "quote|stat|insight", content: "...", position: "..."}] - 1-2 max
- visual_accent: Primary accent color (hex code) - choose based on story emotion
- typography_scale: "dramatic" (very large) or "moderate" (large but readable)
- composition_notes: How elements should flow and interact visually"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Design an editorial story slide for:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.9,  # Higher creativity
        max_tokens=2000
    )
    
    design = json.loads(response.choices[0].message.content)
    
    # Generate editorial slide based on AI design
    return _build_editorial_slide(generator, design)


def _build_editorial_slide(generator: BaseGenerator, design: Dict) -> str:
    """Build editorial-style slide from AI design"""
    
    headline = design.get("headline", "Story")
    subheadline = design.get("subheadline", "")
    layout_style = design.get("layout_style", "hero_focused")
    design_essence = design.get("design_essence", "")
    color_scheme = design.get("color_scheme", "light")
    
    # Get visual elements
    visualization_type = design.get("visualization_type", "single")
    primary_viz = design.get("primary_visualization", {})
    secondary_viz = design.get("secondary_visualization", {})
    key_metrics = design.get("key_metrics", [])
    narrative_elements = design.get("narrative_elements", [])
    visual_accent = design.get("visual_accent", "#667eea")
    typography_scale = design.get("typography_scale", "dramatic")
    
    # Generate visualization
    if visualization_type == "combo" and secondary_viz:
        # Combo chart: dual-axis
        from .creative_story_slide import _generate_combo_chart
        primary_data = primary_viz.get("data_points", [])
        secondary_data = secondary_viz.get("data_points", [])
        primary_style = primary_viz.get("type", "line")  # line or area
        secondary_style = secondary_viz.get("type", "bars")  # bars or spikes
        primary_color = primary_viz.get("color", None)
        secondary_color = secondary_viz.get("color", None)
        visualization_svg = _generate_combo_chart(
            primary_data, secondary_data, generator.template,
            primary_style, secondary_style, primary_color, secondary_color
        )
    else:
        # Single chart
        viz_type = primary_viz.get("type", "line")
        data_points = primary_viz.get("data_points", [])
        viz_style = primary_viz.get("style", "integrated")
        visualization_svg = _generate_editorial_chart(viz_type, data_points, viz_style, generator.template, visual_accent)
    
    # Build based on layout style
    if layout_style == "hero_focused":
        return _build_hero_focused_editorial(generator, headline, subheadline, visualization_svg, key_metrics, narrative_elements, visual_accent, typography_scale, color_scheme)
    elif layout_style == "split_screen":
        return _build_split_screen_editorial(generator, headline, subheadline, visualization_svg, key_metrics, narrative_elements, visual_accent, typography_scale, color_scheme)
    elif layout_style == "flowing_narrative":
        return _build_flowing_narrative_editorial(generator, headline, subheadline, visualization_svg, key_metrics, narrative_elements, visual_accent, typography_scale, color_scheme)
    elif layout_style == "data_hero":
        return _build_data_hero_editorial(generator, headline, subheadline, visualization_svg, key_metrics, narrative_elements, visual_accent, typography_scale, color_scheme)
    else:  # editorial_spread
        return _build_editorial_spread(generator, headline, subheadline, visualization_svg, key_metrics, narrative_elements, visual_accent, typography_scale, color_scheme)


def _get_color_scheme(color_scheme: str, accent_color: str) -> Dict[str, str]:
    """Get color scheme based on design choice"""
    if color_scheme == "dark":
        return {
            "bg": "linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)",
            "text_primary": "#f8fafc",
            "text_secondary": "#cbd5e1",
            "card_bg": "rgba(255, 255, 255, 0.95)",
            "card_bg_alt": "rgba(255, 255, 255, 0.1)",
            "card_border": "rgba(255, 255, 255, 0.2)",
            "shadow": "rgba(0, 0, 0, 0.3)"
        }
    elif color_scheme == "gradient":
        return {
            "bg": f"linear-gradient(135deg, {accent_color}15 0%, #f8fafc 50%, {accent_color}08 100%)",
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "card_bg": "rgba(255, 255, 255, 0.95)",
            "card_bg_alt": f"rgba(255, 255, 255, 0.9)",
            "card_border": f"rgba({accent_color}, 0.2)",
            "shadow": "rgba(0, 0, 0, 0.15)"
        }
    else:  # light
        return {
            "bg": "#f8fafc",
            "text_primary": "#0f172a",
            "text_secondary": "#475569",
            "card_bg": "#ffffff",
            "card_bg_alt": "#f1f5f9",
            "card_border": "#e2e8f0",
            "shadow": "rgba(0, 0, 0, 0.1)"
        }


def _build_hero_focused_editorial(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    narrative_elements: List[Dict],
    accent_color: str,
    typography_scale: str,
    color_scheme: str = "light"
) -> str:
    """Hero-focused editorial: Massive headline, integrated visuals"""
    
    colors = _get_color_scheme(color_scheme, accent_color)
    headline_size = "120px" if typography_scale == "dramatic" else "96px"
    
    # Build metrics as floating elements
    metrics_html = ""
    if metrics:
        metrics_html = '<div class="floating-metrics">'
        for i, metric in enumerate(metrics[:3]):
            emphasis = metric.get("emphasis", "medium")
            size = "large" if emphasis == "high" else "medium"
            metrics_html += f"""
            <div class="floating-metric {size}" style="--delay: {i * 0.1}s">
                <div class="metric-value">{metric.get('value', '')}</div>
                <div class="metric-label">{metric.get('label', '')}</div>
            </div>"""
        metrics_html += '</div>'
    
    # Build narrative elements
    narrative_html = ""
    for elem in narrative_elements[:2]:
        elem_type = elem.get("type", "insight")
        content = elem.get("content", "")
        if elem_type == "quote":
            narrative_html += f'<div class="narrative-quote">{content}</div>'
        elif elem_type == "stat":
            narrative_html += f'<div class="narrative-stat">{content}</div>'
        else:
            narrative_html += f'<div class="narrative-insight">{content}</div>'
    
    css_content = f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            padding: 0 !important;
            margin: 0;
            background: {colors['bg']};
            font-family: {generator.template.font_family};
            overflow-x: hidden;
            color: {colors['text_primary']};
        }}
        
        .editorial-slide {{
            width: 100%;
            min-height: 100vh;
            background: {colors['bg']};
            position: relative;
        }}
        
        .hero-section {{
            position: relative;
            padding: 140px 100px 100px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(102, 126, 234, 0.05) 100%);
            overflow: hidden;
        }}
        
        .hero-section::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 1000px;
            height: 1000px;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.25) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            animation: pulse 8s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.3; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.1); }}
        }}
        
        .headline-container {{
            position: relative;
            z-index: 2;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .headline {{
            font-size: {headline_size};
            font-weight: 900;
            line-height: 0.95;
            letter-spacing: -0.05em;
            color: {colors['text_primary']};
            margin-bottom: 40px;
            text-transform: none;
            position: relative;
            text-shadow: {'0 2px 20px rgba(0, 0, 0, 0.3)' if color_scheme == 'dark' else 'none'};
        }}
        
        .headline .accent-word {{
            color: {accent_color};
            position: relative;
            display: inline-block;
            transform: scale(1.05);
            background: linear-gradient(135deg, {accent_color} 0%, {accent_color}dd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .headline .accent-word::after {{
            content: '';
            position: absolute;
            bottom: 0.1em;
            left: -0.05em;
            right: -0.05em;
            height: 0.25em;
            background: linear-gradient(135deg, {accent_color}40 0%, {accent_color}20 100%);
            border-radius: 4px;
            z-index: -1;
            transform: skewX(-12deg);
            filter: blur(8px);
        }}
        
        .headline .large-word {{
            font-size: 1.25em;
            font-weight: 900;
            display: inline-block;
        }}
        
        .subheadline {{
            font-size: 32px;
            font-weight: 500;
            line-height: 1.5;
            color: {colors['text_secondary']};
            max-width: 1000px;
            margin-bottom: 60px;
            text-shadow: {'0 1px 10px rgba(0, 0, 0, 0.2)' if color_scheme == 'dark' else 'none'};
        }}
        
        .visual-section {{
            position: relative;
            padding: 0 100px 80px;
            margin-top: -40px;
        }}
        
        .chart-container {{
            background: {colors['card_bg']};
            {'backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);' if color_scheme != 'light' else ''}
            border-radius: 32px;
            padding: 80px 60px;
            box-shadow: 0 24px 64px {colors['shadow']}, 0 8px 24px {colors['shadow']};
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            transform: translateY(-20px);
            border: 1px solid {colors['card_border']};
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .chart-container:hover {{
            transform: translateY(-24px);
            box-shadow: 0 32px 80px {colors['shadow']}, 0 12px 32px {colors['shadow']};
        }}
        
        .chart-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, {accent_color} 0%, {accent_color}cc 50%, transparent 100%);
            border-radius: 32px 32px 0 0;
        }}
        
        .chart-container svg {{
            width: 100%;
            height: auto;
            max-width: 1200px;
            margin: 0 auto;
            display: block;
        }}
        
        {metrics_html and '''
        .floating-metrics {{
            position: absolute;
            top: 200px;
            right: 100px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            z-index: 10;
        }}
        
        .floating-metric {{
            background: {colors['card_bg']};
            {'backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);' if color_scheme != 'light' else ''}
            border-radius: 24px;
            padding: 28px 36px;
            box-shadow: 0 16px 40px {colors['shadow']}, 0 8px 16px {colors['shadow']};
            border: 1px solid {colors['card_border']};
            animation: float 4s ease-in-out infinite;
            animation-delay: var(--delay, 0s);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .floating-metric:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 20px 48px {colors['shadow']}, 0 12px 24px {colors['shadow']};
        }}
        
        .floating-metric.large {{
            transform: scale(1.08);
            border-color: {accent_color}66;
            background: {colors['card_bg']};
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-12px); }}
        }}
        
        .metric-value {{
            font-size: 52px;
            font-weight: 900;
            color: {colors['text_primary']};
            line-height: 1;
            margin-bottom: 10px;
            {'text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);' if color_scheme == 'light' else ''}
        }}
        
        .floating-metric.large .metric-value {{
            font-size: 72px;
            background: linear-gradient(135deg, {accent_color} 0%, {accent_color}dd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .metric-label {{
            font-size: 13px;
            font-weight: 700;
            color: {colors['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }}
        ''' or ''}
        
        {narrative_html and '''
        .narrative-section {{
            padding: 80px 100px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .narrative-quote {{
            font-size: 36px;
            font-weight: 600;
            line-height: 1.5;
            color: #f8fafc;
            font-style: italic;
            padding: 48px;
            border-left: 6px solid #667eea;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            margin-bottom: 40px;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }}
        
        .narrative-stat {{
            font-size: 84px;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 50px 0;
            line-height: 1;
            text-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }}
        
        .narrative-insight {{
            font-size: 24px;
            font-weight: 500;
            line-height: 1.7;
            color: #cbd5e1;
            padding: 40px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
            color: #0f172a;
        }}
        ''' or ''}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="editorial-slide">
        <div class="hero-section">
            <div class="headline-container">
                <div class="headline">{_add_accent_to_headline(headline, accent_color)}</div>
                {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
            </div>
            {metrics_html}
        </div>
        
        <div class="visual-section">
            <div class="chart-container">
                {visualization_svg}
            </div>
        </div>
        
        {f'<div class="narrative-section">{narrative_html}</div>' if narrative_html else ''}
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_split_screen_editorial(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    narrative_elements: List[Dict],
    accent_color: str,
    typography_scale: str,
    color_scheme: str = "light"
) -> str:
    """Split-screen editorial: Visual on one side, narrative on other"""
    
    headline_size = "96px" if typography_scale == "dramatic" else "72px"
    
    css_content = f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .editorial-slide {{
            width: 100%;
            min-height: 100vh;
            display: grid;
            grid-template-columns: 1fr 1fr;
        }}
        
        .narrative-panel {{
            padding: 120px 80px;
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }}
        
        .narrative-panel::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: linear-gradient(180deg, {accent_color} 0%, {accent_color}80 100%);
        }}
        
        .headline {{
            font-size: {headline_size};
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: #1D1D1F;
            margin-bottom: 32px;
        }}
        
        .subheadline {{
            font-size: 28px;
            font-weight: 500;
            line-height: 1.5;
            color: #6C757D;
            margin-bottom: 60px;
        }}
        
        .visual-panel {{
            background: linear-gradient(135deg, {accent_color}10 0%, {accent_color}05 100%);
            padding: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        
        .visual-panel svg {{
            width: 100%;
            height: auto;
            max-width: 800px;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="editorial-slide">
        <div class="narrative-panel">
            <div class="headline">{headline}</div>
            {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        <div class="visual-panel">
            {visualization_svg}
        </div>
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_flowing_narrative_editorial(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    narrative_elements: List[Dict],
    accent_color: str,
    typography_scale: str,
    color_scheme: str = "light"
) -> str:
    """Flowing narrative: Elements flow down the page like editorial"""
    
    headline_size = "108px" if typography_scale == "dramatic" else "84px"
    
    css_content = f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .editorial-slide {{
            width: 100%;
            min-height: 100vh;
            max-width: 1600px;
            margin: 0 auto;
            padding: 0;
        }}
        
        .hero-zone {{
            padding: 140px 100px 100px;
            background: linear-gradient(135deg, {accent_color}08 0%, transparent 100%);
            position: relative;
        }}
        
        .headline {{
            font-size: {headline_size};
            font-weight: 900;
            line-height: 0.95;
            letter-spacing: -0.05em;
            color: #1D1D1F;
            margin-bottom: 40px;
            max-width: 1200px;
        }}
        
        .subheadline {{
            font-size: 32px;
            font-weight: 500;
            line-height: 1.5;
            color: #6C757D;
            max-width: 900px;
        }}
        
        .content-flow {{
            padding: 0 100px 100px;
        }}
        
        .chart-section {{
            margin: 80px 0;
            padding: 60px;
            background: #FFFFFF;
            border-radius: 24px;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.06);
            position: relative;
            overflow: hidden;
        }}
        
        .chart-section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, {accent_color} 0%, {accent_color}80 100%);
        }}
        
        .chart-section svg {{
            width: 100%;
            height: auto;
            max-width: 1000px;
            margin: 0 auto;
            display: block;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="editorial-slide">
        <div class="hero-zone">
            <div class="headline">{headline}</div>
            {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="content-flow">
            <div class="chart-section">
                {visualization_svg}
            </div>
        </div>
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_data_hero_editorial(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    narrative_elements: List[Dict],
    accent_color: str,
    typography_scale: str,
    color_scheme: str = "light"
) -> str:
    """Data hero: Chart is the hero, everything supports it"""
    
    headline_size = "84px" if typography_scale == "dramatic" else "64px"
    
    css_content = f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .editorial-slide {{
            width: 100%;
            min-height: 100vh;
            background: {generator.template.background_color};
        }}
        
        .hero-header {{
            padding: 80px 100px 40px;
            text-align: center;
        }}
        
        .headline {{
            font-size: {headline_size};
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: #1D1D1F;
            margin-bottom: 24px;
        }}
        
        .subheadline {{
            font-size: 28px;
            font-weight: 500;
            color: #6C757D;
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .chart-hero {{
            padding: 0 100px 100px;
            position: relative;
        }}
        
        .chart-hero-container {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            border-radius: 40px;
            padding: 100px 80px;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .chart-hero-container::after {{
            content: '';
            position: absolute;
            top: -200px;
            right: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, {accent_color}15 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }}
        
        .chart-hero-container svg {{
            width: 100%;
            height: auto;
            max-width: 1400px;
            margin: 0 auto;
            display: block;
            position: relative;
            z-index: 1;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="editorial-slide">
        <div class="hero-header">
            <div class="headline">{headline}</div>
            {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="chart-hero">
            <div class="chart-hero-container">
                {visualization_svg}
            </div>
        </div>
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_editorial_spread(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    narrative_elements: List[Dict],
    accent_color: str,
    typography_scale: str,
    color_scheme: str = "light"
) -> str:
    """Editorial spread: Magazine-style layout"""
    return _build_hero_focused_editorial(generator, headline, subheadline, visualization_svg, metrics, narrative_elements, accent_color, typography_scale, color_scheme)


def _add_accent_to_headline(headline: str, accent_color: str) -> str:
    """Add visual accent to headline words - make it dramatic"""
    words = headline.split()
    if len(words) > 1:
        # Accent first word and make it larger
        words[0] = f'<span class="accent-word large-word">{words[0]}</span>'
        # Also accent last significant word if it's impactful
        if len(words) > 3:
            last_word = words[-1].rstrip('.,!?')
            if len(last_word) > 4:  # Only if it's substantial
                words[-1] = words[-1].replace(last_word, f'<span class="accent-word">{last_word}</span>')
    return ' '.join(words)


def _generate_editorial_chart(
    viz_type: str,
    data_points: List[Dict],
    style: str,
    template,
    accent_color: str
) -> str:
    """Generate chart with editorial styling"""
    from .creative_story_slide import _generate_line_chart, _generate_bar_chart, _generate_area_chart
    
    if not data_points:
        if viz_type == "line":
            data_points = [
                {"x": "2020", "y": 20},
                {"x": "2021", "y": 28},
                {"x": "2022", "y": 35},
                {"x": "2023", "y": 42},
            ]
        elif viz_type == "bar":
            data_points = [
                {"label": "Q1", "value": 45},
                {"label": "Q2", "value": 58},
                {"label": "Q3", "value": 52},
                {"label": "Q4", "value": 68},
            ]
    
    # Use accent color instead of template colors for editorial style
    if style == "bold":
        # Override template colors with accent
        original_get_gradient = template.get_gradient
        template.get_gradient = lambda key: (accent_color, accent_color + "CC")
    
    if viz_type == "line":
        chart = _generate_line_chart(data_points, template)
    elif viz_type == "bar":
        chart = _generate_bar_chart(data_points, template)
    elif viz_type == "area":
        chart = _generate_area_chart(data_points, template)
    else:
        chart = _generate_line_chart(data_points, template)
    
    # Restore template method
    if style == "bold":
        template.get_gradient = original_get_gradient
    
    return chart
