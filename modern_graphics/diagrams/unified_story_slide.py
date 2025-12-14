"""Unified story slide generator - prompt-driven with visualization heroes"""

import json
from typing import Optional, Dict, List
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from ..env_config import get_openai_key


def generate_unified_story_slide(
    generator: BaseGenerator,
    prompt: str,
    model: str = "gpt-4-turbo-preview",
    temperature: float = 0.5
) -> str:
    """Generate a unified story slide from a prompt with visualization as hero
    
    This is the core unified generator that:
    - Accepts a prompt describing the story/data
    - Uses AI to interpret the prompt and design the layout
    - Makes visualization (single or combo) the dominant hero element
    - Supports both single and combo visualizations
    
    Args:
        generator: BaseGenerator instance
        prompt: Detailed prompt describing the story/data visualization
        model: OpenAI model to use
        temperature: Sampling temperature (0.0-2.0). Higher = more creative/random.
                     Lower = more deterministic/focused. Default: 0.5
    """
    api_key = get_openai_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    try:
        import openai
    except ImportError:
        raise ImportError("openai package required")
    
    client = openai.OpenAI(api_key=api_key)
    
    # System prompt for unified story slide generation
    system_prompt = """You are a visualization designer creating story-driven slides where VISUALIZATIONS ARE THE HERO.

Your job is to:
1. Understand the essence of the story from the prompt
2. Determine if this needs a SINGLE chart or COMBO chart (dual-axis)
3. Design a layout where the visualization is the dominant, hero element
4. Position supporting elements (headline, metrics, annotations) around/over the visualization

VISUALIZATION HERO PRINCIPLES:
- Charts are large, dominant, and visually striking
- Headlines and text support the visualization, not compete with it
- Metrics and annotations are positioned strategically around the chart
- The visualization tells the story visually
- Layout guides the eye through: headline → visualization → insights

COMBO CHART DETECTION:
- Use combo charts when the prompt mentions:
  * Two different metrics/measures over the same time period
  * Dual-axis comparisons (e.g., "temperature vs precipitation", "revenue vs users")
  * Correlations between different data types
  * "Combined", "dual", "two metrics", "correlation" keywords

Return JSON with:
- headline: Bold headline (supports the visualization story)
- subheadline: Supporting narrative text
- visualization_type: "single" or "combo"
- primary_visualization: {type: "line|bar|area", data_points: [...], name: "...", color: "..."}
- secondary_visualization: {type: "bars|spikes", data_points: [...], name: "...", color: "..."} - ONLY if visualization_type is "combo"
- layout_style: "hero_center" (chart centered, text around), "hero_fullwidth" (chart spans full width), "hero_overlay" (text overlays chart), "hero_split" (chart left, narrative right)
- key_metrics: [{label: "...", value: "...", position: "top-left|top-right|bottom-left|bottom-right"}] - 2-4 max
- annotations: [{text: "...", position: "..."}] - 1-3 max, positioned around chart
- insight: Key takeaway text
- visual_accent: Primary accent color (hex)
- chart_emphasis: "high" (very large) or "medium" (large but balanced)"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Design a visualization-hero story slide for:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=temperature,
        max_tokens=2000
    )
    
    design = json.loads(response.choices[0].message.content)
    
    # Store model and temperature in design for tracking
    design["_metadata"] = {
        "model": model,
        "temperature": temperature
    }
    
    # Generate visualization hero slide
    return _build_visualization_hero_slide(generator, design)


def _build_visualization_hero_slide(generator: BaseGenerator, design: Dict) -> str:
    """Build visualization hero slide from AI design"""
    
    headline = design.get("headline", "Data Story")
    subheadline = design.get("subheadline", "")
    layout_style = design.get("layout_style", "hero_center")
    visualization_type = design.get("visualization_type", "single")
    
    # Get visual elements
    primary_viz = design.get("primary_visualization", {})
    secondary_viz = design.get("secondary_visualization", {})
    key_metrics = design.get("key_metrics", [])
    annotations = design.get("annotations", [])
    insight = design.get("insight", "")
    visual_accent = design.get("visual_accent", "#667eea")
    chart_emphasis = design.get("chart_emphasis", "high")
    
    # Generate visualization
    if visualization_type == "combo" and secondary_viz:
        # Combo chart: dual-axis
        from .creative_story_slide import _generate_combo_chart
        primary_data = primary_viz.get("data_points", [])
        secondary_data = secondary_viz.get("data_points", [])
        primary_style = primary_viz.get("type", "line")
        secondary_style = secondary_viz.get("type", "bars")
        primary_color = primary_viz.get("color", None)
        secondary_color = secondary_viz.get("color", None)
        primary_name = primary_viz.get("name", "Primary")
        secondary_name = secondary_viz.get("name", "Secondary")
        visualization_svg = _generate_combo_chart(
            primary_data, secondary_data, generator.template,
            primary_style, secondary_style, primary_color, secondary_color,
            primary_name, secondary_name
        )
    else:
        # Single chart
        viz_type = primary_viz.get("type", "line")
        data_points = primary_viz.get("data_points", [])
        from .creative_story_slide import _generate_line_chart, _generate_bar_chart, _generate_area_chart
        if viz_type == "line":
            visualization_svg = _generate_line_chart(data_points, generator.template)
        elif viz_type == "bar":
            visualization_svg = _generate_bar_chart(data_points, generator.template)
        elif viz_type == "area":
            visualization_svg = _generate_area_chart(data_points, generator.template)
        else:
            visualization_svg = _generate_line_chart(data_points, generator.template)
    
    # Build based on layout style
    if layout_style == "hero_center":
        return _build_hero_center_layout(generator, headline, subheadline, visualization_svg, key_metrics, annotations, insight, visual_accent, chart_emphasis)
    elif layout_style == "hero_fullwidth":
        return _build_hero_fullwidth_layout(generator, headline, subheadline, visualization_svg, key_metrics, annotations, insight, visual_accent, chart_emphasis)
    elif layout_style == "hero_overlay":
        return _build_hero_overlay_layout(generator, headline, subheadline, visualization_svg, key_metrics, annotations, insight, visual_accent, chart_emphasis)
    else:  # hero_split
        return _build_hero_split_layout(generator, headline, subheadline, visualization_svg, key_metrics, annotations, insight, visual_accent, chart_emphasis)


def _build_hero_center_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    annotations: List[Dict],
    insight: str,
    accent_color: str,
    chart_emphasis: str
) -> str:
    """Hero center: Chart centered, text and metrics positioned around it"""
    
    chart_size = "1400px" if chart_emphasis == "high" else "1200px"
    
    # Build metrics HTML
    metrics_html = ""
    if metrics:
        metrics_html = '<div class="hero-metrics">'
        for metric in metrics[:4]:
            position = metric.get("position", "top-left")
            label = metric.get("label", "")
            value = metric.get("value", "")
            metrics_html += f"""
            <div class="hero-metric {position}">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>"""
        metrics_html += '</div>'
    
    # Build annotations HTML
    annotations_html = ""
    if annotations:
        annotations_html = '<div class="hero-annotations">'
        for ann in annotations[:3]:
            text = ann.get("text", "")
            position = ann.get("position", "bottom-left")
            annotations_html += f'<div class="hero-annotation {position}">{text}</div>'
        annotations_html += '</div>'
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .hero-slide-container {{
            width: 100%;
            min-height: 100vh;
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            padding: 60px 100px;
        }}
        
        .hero-header {{
            text-align: center;
            margin-bottom: 60px;
        }}
        
        .hero-headline {{
            font-size: 72px;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: #1D1D1F;
            margin-bottom: 20px;
        }}
        
        .hero-subheadline {{
            font-size: 28px;
            font-weight: 500;
            color: #6C757D;
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .visualization-hero {{
            position: relative;
            background: #FFFFFF;
            border-radius: 32px;
            padding: 80px;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.1);
            margin: 0 auto;
            max-width: {chart_size};
            border: 1px solid #E9ECEF;
        }}
        
        .visualization-hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, {accent_color} 0%, {accent_color}cc 100%);
            border-radius: 32px 32px 0 0;
        }}
        
        .visualization-hero svg {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        {metrics_html and '''
        .hero-metrics {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: none;
        }
        
        .hero-metric {
            position: absolute;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 20px 24px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(0, 0, 0, 0.05);
            min-width: 160px;
        }
        
        .hero-metric.top-left {
            top: 40px;
            left: 40px;
        }
        
        .hero-metric.top-right {
            top: 40px;
            right: 40px;
        }
        
        .hero-metric.bottom-left {
            bottom: 40px;
            left: 40px;
        }
        
        .hero-metric.bottom-right {
            bottom: 40px;
            right: 40px;
        }
        
        .metric-label {
            font-size: 12px;
            font-weight: 600;
            color: #6C757D;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #1D1D1F;
            line-height: 1;
        }
        ''' or ''}
        
        {annotations_html and '''
        .hero-annotations {
            margin-top: 40px;
            display: flex;
            gap: 24px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .hero-annotation {
            background: #FFF9E6;
            border-left: 4px solid #FFC107;
            border-radius: 12px;
            padding: 20px 24px;
            font-size: 16px;
            line-height: 1.6;
            color: #212529;
            max-width: 400px;
        }
        
        .hero-annotation.highlight {
            background: #E3F2FD;
            border-left-color: #2196F3;
        }
        ''' or ''}
        
        {insight and '''
        .hero-insight {
            margin-top: 60px;
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 24px;
            color: #FFFFFF;
        }
        
        .hero-insight-text {
            font-size: 32px;
            font-weight: 600;
            line-height: 1.4;
            max-width: 1200px;
            margin: 0 auto;
        }
        ''' or ''}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="hero-slide-container">
        <div class="hero-header">
            <div class="hero-headline">{headline}</div>
            {f'<div class="hero-subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="visualization-hero">
            {metrics_html}
            {visualization_svg}
        </div>
        
        {annotations_html}
        
        {f'<div class="hero-insight"><div class="hero-insight-text">{insight}</div></div>' if insight else ''}
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_hero_fullwidth_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    annotations: List[Dict],
    insight: str,
    accent_color: str,
    chart_emphasis: str
) -> str:
    """Hero fullwidth: Chart spans full width, headline above"""
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .hero-slide-container {{
            width: 100%;
            min-height: 100vh;
            background: #FFFFFF;
        }}
        
        .hero-header {{
            padding: 80px 100px 40px;
            text-align: center;
        }}
        
        .hero-headline {{
            font-size: 84px;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: #1D1D1F;
            margin-bottom: 24px;
        }}
        
        .hero-subheadline {{
            font-size: 32px;
            font-weight: 500;
            color: #6C757D;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .visualization-hero {{
            padding: 0 100px 80px;
        }}
        
        .visualization-hero svg {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="hero-slide-container">
        <div class="hero-header">
            <div class="hero-headline">{headline}</div>
            {f'<div class="hero-subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="visualization-hero">
            {visualization_svg}
        </div>
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_hero_overlay_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    annotations: List[Dict],
    insight: str,
    accent_color: str,
    chart_emphasis: str
) -> str:
    """Hero overlay: Text overlays the chart"""
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .hero-slide-container {{
            width: 100%;
            min-height: 100vh;
            position: relative;
        }}
        
        .visualization-hero {{
            width: 100%;
            padding: 0;
            position: relative;
        }}
        
        .visualization-hero svg {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .overlay-content {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 100px;
            pointer-events: none;
        }}
        
        .hero-headline {{
            font-size: 96px;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: #FFFFFF;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            margin-bottom: 24px;
            text-align: center;
        }}
        
        .hero-subheadline {{
            font-size: 32px;
            font-weight: 500;
            color: #FFFFFF;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            text-align: center;
            max-width: 1000px;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="hero-slide-container">
        <div class="visualization-hero">
            {visualization_svg}
            <div class="overlay-content">
                <div class="hero-headline">{headline}</div>
                {f'<div class="hero-subheadline">{subheadline}</div>' if subheadline else ''}
            </div>
        </div>
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_hero_split_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics: List[Dict],
    annotations: List[Dict],
    insight: str,
    accent_color: str,
    chart_emphasis: str
) -> str:
    """Hero split: Chart on left, narrative on right"""
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .hero-slide-container {{
            width: 100%;
            min-height: 100vh;
            display: grid;
            grid-template-columns: 1.2fr 1fr;
        }}
        
        .visualization-panel {{
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            padding: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .visualization-panel svg {{
            width: 100%;
            height: auto;
            max-width: 1000px;
        }}
        
        .narrative-panel {{
            padding: 100px 80px;
            background: #FFFFFF;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .hero-headline {{
            font-size: 64px;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -0.04em;
            color: #1D1D1F;
            margin-bottom: 24px;
        }}
        
        .hero-subheadline {{
            font-size: 28px;
            font-weight: 500;
            color: #6C757D;
            line-height: 1.5;
            margin-bottom: 40px;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="hero-slide-container">
        <div class="visualization-panel">
            {visualization_svg}
        </div>
        <div class="narrative-panel">
            <div class="hero-headline">{headline}</div>
            {f'<div class="hero-subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
