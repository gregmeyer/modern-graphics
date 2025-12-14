"""Intelligent story slide generator - AI-driven composition using visual primitives"""

import json
from typing import Optional, Dict, List
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from ..env_config import get_openai_key


def generate_intelligent_story_slide(
    generator: BaseGenerator,
    prompt: str,
    model: str = "gpt-4-turbo-preview",
    temperature: float = 0.5,
    use_unified: bool = True
) -> str:
    """Generate an intelligent, data-driven story slide from a prompt
    
    Uses AI to understand the essence and create an engaging design.
    Delegates to unified_story_slide for visualization-hero layouts.
    
    Args:
        generator: BaseGenerator instance
        prompt: Detailed prompt describing the story/data visualization
        model: OpenAI model to use
        temperature: Sampling temperature (0.0-2.0). Higher = more creative. Default: 0.5
        use_unified: If True, use unified generator (default: True)
    """
    # Use unified generator for visualization-hero layouts
    if use_unified:
        try:
            from .unified_story_slide import generate_unified_story_slide
            return generate_unified_story_slide(generator, prompt, model, temperature)
        except Exception as e:
            # Fallback to editorial if unified fails
            print(f"Unified generator failed, using editorial: {e}")
    
    # Fallback to editorial slide generator
    from .editorial_story_slide import generate_editorial_story_slide
    return generate_editorial_story_slide(generator, prompt, model)


def _build_slide_from_design(generator: BaseGenerator, design: Dict) -> str:
    """Build slide HTML from AI design specification"""
    
    headline = design.get("headline", "Data Story")
    subheadline = design.get("subheadline", "")
    layout_type = design.get("layout_type", "data_focused")
    
    # Generate primary visualization
    primary_viz = design.get("primary_visualization", {})
    viz_type = primary_viz.get("type", "line")
    data_points = primary_viz.get("data_points", [])
    visualization_svg = _generate_smart_chart(viz_type, data_points, generator.template)
    
    # Build story metrics
    story_metrics = design.get("story_metrics", [])
    metrics_html = _build_metrics_grid(story_metrics, generator.template)
    
    # Build timeline if present
    timeline_events = design.get("timeline_events", [])
    timeline_html = _build_timeline_section(timeline_events, generator.template) if timeline_events else ""
    
    # Build comparison if present
    comparison = design.get("comparison")
    comparison_html = _build_comparison_section(comparison, generator.template) if comparison else ""
    
    # Build annotations
    annotations = design.get("annotations", [])
    annotations_html = _build_annotations(annotations)
    
    insight = design.get("insight", "")
    
    # Choose layout based on layout_type
    if layout_type == "data_focused":
        return _build_data_focused_layout(
            generator, headline, subheadline, visualization_svg,
            metrics_html, annotations_html, insight
        )
    elif layout_type == "narrative_focused":
        return _build_narrative_focused_layout(
            generator, headline, subheadline, visualization_svg,
            timeline_html, metrics_html, annotations_html, insight
        )
    elif layout_type == "comparison_focused":
        return _build_comparison_focused_layout(
            generator, headline, subheadline, comparison_html,
            visualization_svg, annotations_html, insight
        )
    else:  # process_focused or default
        return _build_process_focused_layout(
            generator, headline, subheadline, visualization_svg,
            metrics_html, annotations_html, insight
        )


def _build_data_focused_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics_html: str,
    annotations_html: str,
    insight: str
) -> str:
    """Data-focused layout: Chart is hero, metrics support"""
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .slide-container {{
            max-width: 1800px;
            width: 100%;
            background: #FFFFFF;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.12);
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 80px 100px 60px;
            color: #FFFFFF;
        }}
        
        .headline {{
            font-size: 72px;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: 16px;
        }}
        
        .subheadline {{
            font-size: 28px;
            font-weight: 500;
            opacity: 0.95;
            line-height: 1.4;
        }}
        
        .content-section {{
            padding: 80px 100px;
        }}
        
        .chart-hero {{
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 24px;
            padding: 60px;
            margin: 40px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        }}
        
        .chart-hero svg {{
            width: 100%;
            height: auto;
            max-width: 1200px;
            margin: 0 auto;
            display: block;
        }}
        
        {metrics_html and '''
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            border-radius: 16px;
            padding: 32px 24px;
            border: 2px solid #E9ECEF;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-label {{
            font-size: 13px;
            font-weight: 600;
            color: #6C757D;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
        }}
        
        .metric-value {{
            font-size: 42px;
            font-weight: 700;
            color: #212529;
            line-height: 1;
            margin-bottom: 8px;
        }}
        
        .metric-change {{
            font-size: 16px;
            font-weight: 600;
            color: #34C759;
        }}
        ''' or ''}
        
        {annotations_html and '''
        .annotations-container {{
            display: flex;
            gap: 24px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}
        
        .annotation-card {{
            flex: 1;
            min-width: 280px;
            padding: 24px;
            background: #FFF9E6;
            border-left: 4px solid #FFC107;
            border-radius: 12px;
            font-size: 16px;
            line-height: 1.6;
        }}
        
        .annotation-card.highlight {{
            background: #E3F2FD;
            border-left-color: #2196F3;
        }}
        ''' or ''}
        
        {insight and '''
        .insight-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 100px;
            color: #FFFFFF;
            text-align: center;
        }}
        
        .insight-text {{
            font-size: 32px;
            font-weight: 600;
            line-height: 1.4;
            max-width: 1200px;
            margin: 0 auto;
        }}
        ''' or ''}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="slide-container">
        <div class="hero-section">
            <div class="headline">{headline}</div>
            {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="content-section">
            <div class="chart-hero">
                {visualization_svg}
            </div>
            
            {metrics_html}
            {annotations_html}
        </div>
        
        {f'<div class="insight-section"><div class="insight-text">{insight}</div></div>' if insight else ''}
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_narrative_focused_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    timeline_html: str,
    metrics_html: str,
    annotations_html: str,
    insight: str
) -> str:
    """Narrative-focused layout: Story flows through timeline and visuals"""
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .slide-container {{
            max-width: 1800px;
            width: 100%;
            background: #FFFFFF;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.12);
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 80px 100px 60px;
            color: #FFFFFF;
        }}
        
        .headline {{
            font-size: 72px;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: 16px;
        }}
        
        .subheadline {{
            font-size: 28px;
            font-weight: 500;
            opacity: 0.95;
            line-height: 1.4;
        }}
        
        .content-section {{
            padding: 80px 100px;
        }}
        
        .story-flow {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            margin: 60px 0;
        }}
        
        .visual-panel {{
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 24px;
            padding: 40px;
        }}
        
        .visual-panel svg {{
            width: 100%;
            height: auto;
        }}
        
        .narrative-panel {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        {timeline_html and '''
        .timeline-section {{
            margin: 40px 0;
        }}
        
        .timeline-item {{
            display: flex;
            gap: 24px;
            margin-bottom: 32px;
            padding-left: 24px;
            border-left: 3px solid #667eea;
        }}
        
        .timeline-date {{
            font-size: 18px;
            font-weight: 700;
            color: #667eea;
            min-width: 120px;
        }}
        
        .timeline-content {{
            flex: 1;
        }}
        
        .timeline-event {{
            font-size: 20px;
            font-weight: 600;
            color: #212529;
            margin-bottom: 8px;
        }}
        
        .timeline-significance {{
            font-size: 16px;
            color: #6C757D;
            line-height: 1.5;
        }}
        ''' or ''}
        
        {metrics_html and '''
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 24px;
            margin: 40px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            border-radius: 12px;
            padding: 24px;
            border: 2px solid #E9ECEF;
            text-align: center;
        }}
        
        .metric-label {{
            font-size: 12px;
            font-weight: 600;
            color: #6C757D;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 8px;
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: 700;
            color: #212529;
            line-height: 1;
        }}
        ''' or ''}
        
        {insight and '''
        .insight-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 100px;
            color: #FFFFFF;
            text-align: center;
        }}
        
        .insight-text {{
            font-size: 32px;
            font-weight: 600;
            line-height: 1.4;
            max-width: 1200px;
            margin: 0 auto;
        }}
        ''' or ''}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="slide-container">
        <div class="hero-section">
            <div class="headline">{headline}</div>
            {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="content-section">
            <div class="story-flow">
                <div class="visual-panel">
                    {visualization_svg}
                </div>
                <div class="narrative-panel">
                    {timeline_html}
                    {metrics_html}
                </div>
            </div>
            
            {annotations_html}
        </div>
        
        {f'<div class="insight-section"><div class="insight-text">{insight}</div></div>' if insight else ''}
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_comparison_focused_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    comparison_html: str,
    visualization_svg: str,
    annotations_html: str,
    insight: str
) -> str:
    """Comparison-focused layout: Before/after or A vs B"""
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            font-family: {generator.template.font_family};
        }}
        
        .slide-container {{
            max-width: 1800px;
            width: 100%;
            background: #FFFFFF;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.12);
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 80px 100px 60px;
            color: #FFFFFF;
            text-align: center;
        }}
        
        .headline {{
            font-size: 72px;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: 16px;
        }}
        
        .subheadline {{
            font-size: 28px;
            font-weight: 500;
            opacity: 0.95;
            line-height: 1.4;
        }}
        
        .content-section {{
            padding: 80px 100px;
        }}
        
        .comparison-container {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 40px;
            align-items: center;
            margin: 60px 0;
        }}
        
        .comparison-side {{
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 24px;
            padding: 60px 40px;
            border: 3px solid #E9ECEF;
        }}
        
        .comparison-side.before {{
            border-color: #FF9500;
        }}
        
        .comparison-side.after {{
            border-color: #34C759;
        }}
        
        .comparison-label {{
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 24px;
            text-align: center;
        }}
        
        .comparison-side.before .comparison-label {{
            color: #FF9500;
        }}
        
        .comparison-side.after .comparison-label {{
            color: #34C759;
        }}
        
        .comparison-title {{
            font-size: 32px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 24px;
            color: #212529;
        }}
        
        .comparison-features {{
            list-style: none;
            padding: 0;
        }}
        
        .comparison-features li {{
            padding: 12px 0;
            font-size: 18px;
            border-bottom: 1px solid #E9ECEF;
        }}
        
        .vs-divider {{
            font-size: 48px;
            font-weight: 700;
            color: #667eea;
        }}
        
        {visualization_svg and '''
        .chart-section {{
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 24px;
            padding: 60px;
            margin: 40px 0;
        }}
        
        .chart-section svg {{
            width: 100%;
            height: auto;
            max-width: 1000px;
            margin: 0 auto;
            display: block;
        }}
        ''' or ''}
        
        {insight and '''
        .insight-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 100px;
            color: #FFFFFF;
            text-align: center;
        }}
        
        .insight-text {{
            font-size: 32px;
            font-weight: 600;
            line-height: 1.4;
            max-width: 1200px;
            margin: 0 auto;
        }}
        ''' or ''}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="slide-container">
        <div class="hero-section">
            <div class="headline">{headline}</div>
            {f'<div class="subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="content-section">
            <div class="comparison-container">
                {comparison_html}
            </div>
            
            {f'<div class="chart-section">{visualization_svg}</div>' if visualization_svg else ''}
            {annotations_html}
        </div>
        
        {f'<div class="insight-section"><div class="insight-text">{insight}</div></div>' if insight else ''}
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _build_process_focused_layout(
    generator: BaseGenerator,
    headline: str,
    subheadline: str,
    visualization_svg: str,
    metrics_html: str,
    annotations_html: str,
    insight: str
) -> str:
    """Process-focused layout: Shows flow/cycle with data"""
    # Similar to data_focused but with process emphasis
    return _build_data_focused_layout(generator, headline, subheadline, visualization_svg, metrics_html, annotations_html, insight)


def _generate_smart_chart(viz_type: str, data_points: List[Dict], template) -> str:
    """Generate chart SVG with smart defaults"""
    from .creative_story_slide import _generate_line_chart, _generate_bar_chart, _generate_area_chart
    
    if not data_points:
        # Generate sample data based on type
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
    
    if viz_type == "line":
        return _generate_line_chart(data_points, template)
    elif viz_type == "bar":
        return _generate_bar_chart(data_points, template)
    elif viz_type == "area":
        return _generate_area_chart(data_points, template)
    else:
        return _generate_line_chart(data_points, template)


def _build_metrics_grid(metrics: List[Dict], template) -> str:
    """Build metrics grid HTML"""
    if not metrics:
        return ""
    
    html = '<div class="metrics-grid">'
    for metric in metrics[:4]:  # Max 4 metrics
        label = metric.get("label", "")
        value = metric.get("value", "")
        change = metric.get("change", "")
        
        change_html = f'<div class="metric-change">{change}</div>' if change else ''
        
        html += f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {change_html}
        </div>"""
    html += '</div>'
    return html


def _build_timeline_section(events: List[Dict], template) -> str:
    """Build timeline section HTML"""
    if not events:
        return ""
    
    html = '<div class="timeline-section">'
    for event in events[:4]:  # Max 4 events
        date = event.get("date", "")
        event_text = event.get("event", "")
        significance = event.get("significance", "")
        
        html += f"""
        <div class="timeline-item">
            <div class="timeline-date">{date}</div>
            <div class="timeline-content">
                <div class="timeline-event">{event_text}</div>
                {f'<div class="timeline-significance">{significance}</div>' if significance else ''}
            </div>
        </div>"""
    html += '</div>'
    return html


def _build_comparison_section(comparison: Dict, template) -> str:
    """Build comparison section HTML"""
    if not comparison:
        return ""
    
    before = comparison.get("before", {})
    after = comparison.get("after", {})
    
    before_title = before.get("title", "Before")
    before_features = before.get("features", [])
    
    after_title = after.get("title", "After")
    after_features = after.get("features", [])
    
    before_list = ''.join([f'<li>{f}</li>' for f in before_features[:5]])
    after_list = ''.join([f'<li>{f}</li>' for f in after_features[:5]])
    
    return f"""
    <div class="comparison-side before">
        <div class="comparison-label">Before</div>
        <div class="comparison-title">{before_title}</div>
        <ul class="comparison-features">{before_list}</ul>
    </div>
    <div class="vs-divider">VS</div>
    <div class="comparison-side after">
        <div class="comparison-label">After</div>
        <div class="comparison-title">{after_title}</div>
        <ul class="comparison-features">{after_list}</ul>
    </div>
    """


def _build_annotations(annotations: List[Dict]) -> str:
    """Build annotations HTML"""
    if not annotations:
        return ""
    
    html = '<div class="annotations-container">'
    for ann in annotations[:3]:  # Max 3 annotations
        text = ann.get("text", "")
        highlight = ann.get("highlight", False)
        class_name = "annotation-card highlight" if highlight else "annotation-card"
        html += f'<div class="{class_name}">{text}</div>'
    html += '</div>'
    return html
