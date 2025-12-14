"""Creative story slide generator - flexible layouts based on prompts"""

from typing import Optional, Dict, List
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def generate_creative_story_slide(
    generator: BaseGenerator,
    title: Optional[str] = None,
    headline: Optional[str] = None,
    subheadline: Optional[str] = None,
    prompt: Optional[str] = None,
    story_elements: Optional[List[Dict[str, str]]] = None,
    visualization_type: str = "line",  # line, bar, area, comparison
    data_points: Optional[List[Dict]] = None,
    annotations: Optional[List[str]] = None,
    insight: Optional[str] = None,
    time_range: Optional[str] = None,
    data_source: Optional[str] = None,
    custom_prompt_context: Optional[str] = None,
    use_unified: bool = True
) -> str:
    """Generate a creative, flexible story slide based on detailed prompt
    
    Supports both prompt-based (new) and parameter-based (legacy) approaches.
    If prompt is provided, uses unified generator. Otherwise uses legacy parameters.
    
    Args:
        generator: BaseGenerator instance
        prompt: Optional prompt describing the story (preferred, uses unified generator)
        title: Main slide title (legacy parameter)
        headline: Hero headline (legacy parameter)
        subheadline: Optional subheadline (legacy parameter)
        story_elements: List of story elements with 'label' and 'value'
        visualization_type: Type of visualization (line, bar, area, comparison)
        data_points: Optional data points for visualization
        annotations: List of annotation texts
        insight: Key insight text
        time_range: Time range covered
        data_source: Data source attribution
        custom_prompt_context: Additional context from prompt
        use_unified: If True and prompt provided, use unified generator (default: True)
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
    if not headline:
        headline = title
    
    # Generate visualization SVG based on type
    visualization_svg = _generate_visualization_svg(
        visualization_type,
        data_points or [],
        generator.template
    )
    
    # Build story elements HTML
    story_elements_html = ""
    if story_elements:
        story_elements_html = '<div class="story-elements">'
        for i, elem in enumerate(story_elements[:3]):  # Max 3 elements
            story_elements_html += f"""
            <div class="story-element">
                <div class="story-label">{elem.get('label', '')}</div>
                <div class="story-value">{elem.get('value', '')}</div>
            </div>"""
        story_elements_html += '</div>'
    
    # Build annotations HTML
    annotations_html = ""
    if annotations:
        annotations_html = '<div class="annotations">'
        for annotation in annotations[:2]:  # Max 2 annotations
            annotations_html += f'<div class="annotation">{annotation}</div>'
        annotations_html += '</div>'
    
    # Build footer
    footer_html = ""
    if time_range or data_source:
        footer_html = '<div class="slide-footer">'
        if time_range:
            footer_html += f'<span class="time-range">{time_range}</span>'
        if data_source:
            footer_html += f'<span class="data-source">{data_source}</span>'
        footer_html += '</div>'
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: {generator.template.background_color};
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: {generator.template.font_family};
        }}
        
        .creative-slide-container {{
            max-width: 1800px;
            width: 100%;
            background: #FFFFFF;
            border-radius: 0;
            padding: 0;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.15), 0 16px 32px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 80px 100px 60px;
            color: #FFFFFF;
            text-align: center;
        }}
        
        .slide-title {{
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            opacity: 0.9;
            margin-bottom: 24px;
        }}
        
        .hero-headline {{
            font-size: 64px;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: 20px;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .hero-subheadline {{
            font-size: 28px;
            font-weight: 500;
            line-height: 1.4;
            opacity: 0.95;
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .content-section {{
            padding: 80px 100px;
            background: #FFFFFF;
        }}
        
        .visualization-container {{
            margin: 60px 0;
            background: #F8F9FA;
            border-radius: 16px;
            padding: 60px;
            min-height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .visualization-container svg {{
            width: 100%;
            height: auto;
            max-width: 1000px;
        }}
        
        .story-elements {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin: 60px 0;
        }}
        
        .story-element {{
            text-align: center;
            padding: 40px 30px;
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            border-radius: 16px;
            border: 2px solid #E9ECEF;
        }}
        
        .story-label {{
            font-size: 14px;
            font-weight: 600;
            color: #6C757D;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 16px;
        }}
        
        .story-value {{
            font-size: 32px;
            font-weight: 700;
            color: #212529;
            line-height: 1.2;
        }}
        
        .annotations {{
            display: flex;
            gap: 30px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}
        
        .annotation {{
            flex: 1;
            min-width: 300px;
            padding: 24px;
            background: #FFF9E6;
            border-left: 4px solid #FFC107;
            border-radius: 8px;
            font-size: 16px;
            line-height: 1.6;
            color: #212529;
        }}
        
        .annotation:first-child {{
            background: #E3F2FD;
            border-left-color: #2196F3;
        }}
        
        .insight-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 100px;
            color: #FFFFFF;
            text-align: center;
        }}
        
        .insight-label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .insight-text {{
            font-size: 36px;
            font-weight: 600;
            line-height: 1.4;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .slide-footer {{
            padding: 30px 100px;
            background: #F8F9FA;
            border-top: 1px solid #E9ECEF;
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: #6C757D;
        }}
        
        .time-range {{
            font-weight: 600;
        }}
        
        .data-source {{
            font-style: italic;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="creative-slide-container">
        <div class="hero-section">
            <div class="slide-title">{title}</div>
            <div class="hero-headline">{headline}</div>
            {f'<div class="hero-subheadline">{subheadline}</div>' if subheadline else ''}
        </div>
        
        <div class="content-section">
            {story_elements_html}
            
            <div class="visualization-container">
                {visualization_svg}
            </div>
            
            {annotations_html}
        </div>
        
        {f'<div class="insight-section"><div class="insight-label">Key Insight</div><div class="insight-text">{insight}</div></div>' if insight else ''}
        
        {footer_html}
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)


def _generate_visualization_svg(
    viz_type: str,
    data_points: List[Dict],
    template
) -> str:
    """Generate SVG visualization based on type"""
    
    if not data_points:
        # Generate sample data if none provided
        if viz_type == "line":
            data_points = [
                {"x": "2020", "y": 20},
                {"x": "2021", "y": 25},
                {"x": "2022", "y": 30},
                {"x": "2023", "y": 35},
            ]
        elif viz_type == "bar":
            data_points = [
                {"label": "Q1", "value": 45},
                {"label": "Q2", "value": 52},
                {"label": "Q3", "value": 48},
                {"label": "Q4", "value": 60},
            ]
    
    if viz_type == "line":
        return _generate_line_chart(data_points, template)
    elif viz_type == "bar":
        return _generate_bar_chart(data_points, template)
    elif viz_type == "area":
        return _generate_area_chart(data_points, template)
    else:
        return _generate_line_chart(data_points, template)


def _generate_line_chart(data_points: List[Dict], template) -> str:
    """Generate line chart SVG"""
    width = 800
    height = 400
    padding = 60
    
    # Extract values
    values = [d.get("y", d.get("value", 0)) for d in data_points]
    labels = [d.get("x", d.get("label", "")) for d in data_points]
    
    max_val = max(values) if values else 100
    min_val = min(values) if values else 0
    range_val = max_val - min_val if max_val > min_val else max_val
    
    chart_width = width - 2 * padding
    chart_height = height - 2 * padding
    
    # Generate path
    points = []
    for i, val in enumerate(values):
        x = padding + (i / (len(values) - 1) if len(values) > 1 else 0) * chart_width
        y = padding + chart_height - ((val - min_val) / range_val if range_val > 0 else 0) * chart_height
        points.append(f"{x},{y}")
    
    path_d = f"M {points[0]}"
    for point in points[1:]:
        path_d += f" L {point}"
    
    # Get gradient colors
    grad_start, grad_end = template.get_gradient("blue")
    
    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:{grad_start};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grad_end};stop-opacity:1" />
            </linearGradient>
        </defs>
        
        <!-- Grid lines -->
        {_generate_grid_lines(width, height, padding, 5)}
        
        <!-- Data line -->
        <path d="{path_d}" fill="none" stroke="url(#lineGrad)" stroke-width="4" stroke-linecap="round"/>
        
        <!-- Data points -->
        {''.join([f'<circle cx="{points[i].split(",")[0]}" cy="{points[i].split(",")[1]}" r="6" fill="{grad_start}" stroke="#FFFFFF" stroke-width="2"/>' for i in range(len(points))])}
        
        <!-- Labels -->
        {''.join([f'<text x="{points[i].split(",")[0]}" y="{height - padding + 30}" font-size="14" fill="#6C757D" text-anchor="middle">{labels[i]}</text>' for i in range(len(labels))])}
        
        <!-- Y-axis label -->
        <text x="20" y="{height // 2}" font-size="14" fill="#6C757D" text-anchor="middle" transform="rotate(-90 20 {height // 2})">Value</text>
    </svg>"""
    
    return svg


def _generate_bar_chart(data_points: List[Dict], template) -> str:
    """Generate bar chart SVG"""
    width = 800
    height = 400
    padding = 60
    
    values = [d.get("value", d.get("y", 0)) for d in data_points]
    labels = [d.get("label", d.get("x", "")) for d in data_points]
    
    max_val = max(values) if values else 100
    chart_width = width - 2 * padding
    chart_height = height - 2 * padding
    bar_width = chart_width / len(values) * 0.6
    bar_spacing = chart_width / len(values) * 0.4
    
    grad_start, grad_end = template.get_gradient("blue")
    
    bars = []
    for i, val in enumerate(values):
        bar_height = (val / max_val) * chart_height if max_val > 0 else 0
        x = padding + i * (bar_width + bar_spacing) + bar_spacing / 2
        y = padding + chart_height - bar_height
        
        bars.append(f'''
            <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" 
                  fill="url(#barGrad)" rx="4"/>
            <text x="{x + bar_width/2}" y="{y - 10}" font-size="14" font-weight="600" 
                  fill="#212529" text-anchor="middle">{val}</text>
            <text x="{x + bar_width/2}" y="{height - padding + 30}" font-size="14" 
                  fill="#6C757D" text-anchor="middle">{labels[i]}</text>
        ''')
    
    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grad_start};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{grad_end};stop-opacity:1" />
            </linearGradient>
        </defs>
        
        {_generate_grid_lines(width, height, padding, 5)}
        
        {''.join(bars)}
    </svg>"""
    
    return svg


def _generate_area_chart(data_points: List[Dict], template) -> str:
    """Generate area chart SVG"""
    width = 800
    height = 400
    padding = 60
    
    values = [d.get("y", d.get("value", 0)) for d in data_points]
    labels = [d.get("x", d.get("label", "")) for d in data_points]
    
    max_val = max(values) if values else 100
    min_val = min(values) if values else 0
    range_val = max_val - min_val if max_val > min_val else max_val
    
    chart_width = width - 2 * padding
    chart_height = height - 2 * padding
    
    points = []
    for i, val in enumerate(values):
        x = padding + (i / (len(values) - 1) if len(values) > 1 else 0) * chart_width
        y = padding + chart_height - ((val - min_val) / range_val if range_val > 0 else 0) * chart_height
        points.append((x, y))
    
    # Create area path
    area_path = f"M {points[0][0]},{padding + chart_height}"
    for x, y in points:
        area_path += f" L {x},{y}"
    area_path += f" L {points[-1][0]},{padding + chart_height} Z"
    
    # Line path
    line_path = f"M {points[0][0]},{points[0][1]}"
    for x, y in points[1:]:
        line_path += f" L {x},{y}"
    
    grad_start, grad_end = template.get_gradient("blue")
    
    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{grad_start};stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:{grad_end};stop-opacity:0.1" />
            </linearGradient>
        </defs>
        
        {_generate_grid_lines(width, height, padding, 5)}
        
        <path d="{area_path}" fill="url(#areaGrad)"/>
        <path d="{line_path}" fill="none" stroke="{grad_start}" stroke-width="3" stroke-linecap="round"/>
        
        {''.join([f'<circle cx="{x}" cy="{y}" r="5" fill="{grad_start}" stroke="#FFFFFF" stroke-width="2"/>' for x, y in points])}
        
        {''.join([f'<text x="{points[i][0]}" y="{height - padding + 30}" font-size="14" fill="#6C757D" text-anchor="middle">{labels[i]}</text>' for i in range(len(labels))])}
    </svg>"""
    
    return svg


def generate_combo_chart(
    generator: BaseGenerator,
    primary_data: List[Dict],
    secondary_data: List[Dict],
    primary_style: str = "line",  # "line" or "area"
    secondary_style: str = "bars",  # "bars" or "spikes"
    primary_color: str = None,
    secondary_color: str = None,
    primary_name: str = "Primary",
    secondary_name: str = "Secondary"
) -> str:
    """Generate a standalone combo chart diagram
    
    Args:
        generator: BaseGenerator instance
        primary_data: List of {x, y} for primary axis (left)
        secondary_data: List of {x, y} for secondary axis (right)
        primary_style: "line" or "area"
        secondary_style: "bars" or "spikes"
        primary_color: Override color for primary series
        secondary_color: Override color for secondary series
        primary_name: Label for primary series
        secondary_name: Label for secondary series
    """
    svg = _generate_combo_chart(
        primary_data, secondary_data, generator.template,
        primary_style, secondary_style, primary_color, secondary_color,
        primary_name, secondary_name
    )
    return generator._wrap_html(f'<div class="combo-chart-container">{svg}</div>', "")


def _generate_combo_chart(
    primary_data: List[Dict],
    secondary_data: List[Dict],
    template,
    primary_style: str = "line",  # "line" or "area"
    secondary_style: str = "bars",  # "bars" or "spikes"
    primary_color: str = None,
    secondary_color: str = None,
    primary_name: str = "Primary",
    secondary_name: str = "Secondary"
) -> str:
    """Generate dual-axis combo chart SVG
    
    Args:
        primary_data: List of {x, y} for primary axis (left)
        secondary_data: List of {x, y} for secondary axis (right)
        template: Style template
        primary_style: "line" or "area"
        secondary_style: "bars" or "spikes"
        primary_color: Override color for primary series
        secondary_color: Override color for secondary series
    """
    width = 1000
    height = 500
    padding = 80
    right_padding = 100  # Extra space for right axis
    
    # Extract primary values and convert to float
    primary_values = [float(d.get("y", d.get("value", 0))) for d in primary_data]
    primary_labels = [d.get("x", d.get("label", "")) for d in primary_data]
    
    # Extract secondary values and convert to float
    secondary_values = [float(d.get("y", d.get("value", 0))) for d in secondary_data]
    secondary_labels = [d.get("x", d.get("label", "")) for d in secondary_data]
    
    # Ensure same number of points
    if len(primary_data) != len(secondary_data):
        min_len = min(len(primary_data), len(secondary_data))
        primary_values = primary_values[:min_len]
        primary_labels = primary_labels[:min_len]
        secondary_values = secondary_values[:min_len]
        secondary_labels = secondary_labels[:min_len]
    
    # Calculate ranges
    primary_max = max(primary_values) if primary_values else 100
    primary_min = min(primary_values) if primary_values else 0
    primary_range = primary_max - primary_min if primary_max > primary_min else primary_max
    
    secondary_max = max(secondary_values) if secondary_values else 100
    secondary_min = min(secondary_values) if secondary_values else 0
    secondary_range = secondary_max - secondary_min if secondary_max > secondary_min else secondary_max
    
    chart_width = width - padding - right_padding
    chart_height = height - 2 * padding
    
    # Colors
    if primary_color:
        prim_start, prim_end = primary_color, primary_color + "CC"
    else:
        prim_start, prim_end = template.get_gradient("blue")
    
    if secondary_color:
        sec_start, sec_end = secondary_color, secondary_color + "CC"
    else:
        sec_start, sec_end = template.get_gradient("red")
    
    # Primary axis (left) - line or area
    primary_points = []
    for i, val in enumerate(primary_values):
        x = padding + (i / (len(primary_values) - 1) if len(primary_values) > 1 else 0) * chart_width
        y = padding + chart_height - ((val - primary_min) / primary_range if primary_range > 0 else 0) * chart_height
        primary_points.append((x, y))
    
    # Secondary axis (right) - bars or spikes
    secondary_points = []
    for i, val in enumerate(secondary_values):
        x = padding + (i / (len(secondary_values) - 1) if len(secondary_values) > 1 else 0) * chart_width
        # Scale to right axis (invert: higher values at top)
        y = padding + chart_height - ((val - secondary_min) / secondary_range if secondary_range > 0 else 0) * chart_height
        secondary_points.append((x, y, val))
    
    # Build SVG
    svg_parts = []
    
    # Primary line/area path
    if primary_style == "area":
        area_path = f"M {primary_points[0][0]},{padding + chart_height}"
        for x, y in primary_points:
            area_path += f" L {x},{y}"
        area_path += f" L {primary_points[-1][0]},{padding + chart_height} Z"
        svg_parts.append(f'<path d="{area_path}" fill="url(#primaryGrad)" opacity="0.3"/>')
    
    line_path = f"M {primary_points[0][0]},{primary_points[0][1]}"
    for x, y in primary_points[1:]:
        line_path += f" L {x},{y}"
    svg_parts.append(f'<path d="{line_path}" fill="none" stroke="{prim_start}" stroke-width="4" stroke-linecap="round"/>')
    
    # Primary data points
    for x, y in primary_points:
        svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{prim_start}" stroke="#FFFFFF" stroke-width="2"/>')
    
    # Secondary bars/spikes
    bar_width = chart_width / len(secondary_points) * 0.4
    bar_spacing = chart_width / len(secondary_points) * 0.6
    
    for i, (x, y, val) in enumerate(secondary_points):
        if secondary_style == "bars":
            bar_height = (val - secondary_min) / secondary_range * chart_height if secondary_range > 0 else 0
            bar_y = padding + chart_height - bar_height
            svg_parts.append(f'<rect x="{x - bar_width/2}" y="{bar_y}" width="{bar_width}" height="{bar_height}" fill="{sec_start}" opacity="0.7" rx="2"/>')
        else:  # spikes
            spike_height = (val - secondary_min) / secondary_range * chart_height if secondary_range > 0 else 0
            spike_y = padding + chart_height - spike_height
            svg_parts.append(f'<line x1="{x}" y1="{padding + chart_height}" x2="{x}" y2="{spike_y}" stroke="{sec_start}" stroke-width="3" stroke-linecap="round"/>')
            svg_parts.append(f'<circle cx="{x}" cy="{spike_y}" r="4" fill="{sec_start}"/>')
    
    # Grid lines (for primary axis)
    grid_lines = []
    for i in range(6):
        y = padding + (i / 5) * chart_height
        grid_lines.append(f'<line x1="{padding}" y1="{y}" x2="{width - right_padding}" y2="{y}" stroke="#E9ECEF" stroke-width="1" opacity="0.4"/>')
    
    # Labels
    label_elements = []
    for i in range(len(primary_labels)):
        x = primary_points[i][0]
        label_elements.append(f'<text x="{x}" y="{height - padding + 25}" font-size="13" fill="#6C757D" text-anchor="middle">{primary_labels[i]}</text>')
    
    # Y-axis labels
    # Left axis (primary)
    for i in range(6):
        y_val = primary_min + (i / 5) * primary_range
        y_pos = padding + (1 - i / 5) * chart_height
        label_elements.append(f'<text x="{padding - 15}" y="{y_pos + 5}" font-size="12" fill="#6C757D" text-anchor="end">{y_val:.1f}</text>')
    
    # Right axis (secondary)
    for i in range(6):
        y_val = secondary_min + (i / 5) * secondary_range
        y_pos = padding + (1 - i / 5) * chart_height
        label_elements.append(f'<text x="{width - right_padding + 15}" y="{y_pos + 5}" font-size="12" fill="#DC2626" text-anchor="start" font-weight="600">{y_val:.1f}</text>')
    
    # Axis lines
    axis_lines = [
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{padding + chart_height}" stroke="#6C757D" stroke-width="2"/>',  # Left
        f'<line x1="{width - right_padding}" y1="{padding}" x2="{width - right_padding}" y2="{padding + chart_height}" stroke="#DC2626" stroke-width="2"/>',  # Right
        f'<line x1="{padding}" y1="{padding + chart_height}" x2="{width - right_padding}" y2="{padding + chart_height}" stroke="#6C757D" stroke-width="2"/>',  # Bottom
    ]
    
    svg = f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{prim_start};stop-opacity:0.4" />
                <stop offset="100%" style="stop-color:{prim_end};stop-opacity:0.1" />
            </linearGradient>
        </defs>
        
        {''.join(grid_lines)}
        {''.join(axis_lines)}
        {''.join(svg_parts)}
        {''.join(label_elements)}
        
        <!-- Legend -->
        <g transform="translate({width - 200}, {padding - 30})">
            <line x1="0" y1="0" x2="30" y2="0" stroke="{prim_start}" stroke-width="3"/>
            <text x="35" y="5" font-size="13" fill="#6C757D">{primary_name}</text>
            <line x1="0" y1="20" x2="30" y2="20" stroke="{sec_start}" stroke-width="3"/>
            <text x="35" y="25" font-size="13" fill="#DC2626">{secondary_name}</text>
        </g>
    </svg>"""
    
    return svg


def _generate_grid_lines(width: int, height: int, padding: int, num_lines: int) -> str:
    """Generate grid lines for charts"""
    chart_height = height - 2 * padding
    lines = []
    
    for i in range(num_lines + 1):
        y = padding + (i / num_lines) * chart_height
        lines.append(f'<line x1="{padding}" y1="{y}" x2="{width - padding}" y2="{y}" stroke="#E9ECEF" stroke-width="1" opacity="0.5"/>')
    
    return '\n        '.join(lines)
