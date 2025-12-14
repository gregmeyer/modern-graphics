"""Flywheel diagram generator"""

import math
from typing import List, Dict, Optional
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def generate_flywheel_diagram(
    generator: BaseGenerator,
    elements: List[Dict[str, any]],
    center_label: Optional[str] = None,
    radius: int = 200
) -> str:
    """Generate a flywheel diagram (spoke-style radiating from center)"""
    num_elements = len(elements)
    angle_step = 360 / num_elements
    center_radius = 60
    viewbox_size = radius * 2 + 200
    center_x = 0
    center_y = 0
    outer_radius = radius
    inner_radius = center_radius + 20
    
    svg_elements = []
    
    color_map = {
        'blue': '#4285F4',
        'green': '#34A853', 
        'orange': '#FBBC05',
        'purple': '#EA4335',
        'red': '#EA4335',
        'gray': '#36454F'
    }
    
    if center_label:
        svg_elements.append(f'''
                <circle cx="{center_x}" cy="{center_y}" r="{center_radius}" fill="#36454F"/>
                <text x="{center_x}" y="{center_y + 5}" font-family="Inter, -apple-system, sans-serif" font-size="20" font-weight="600" fill="#FFFFFF" text-anchor="middle" dominant-baseline="middle">{center_label}</text>
            ''')
    
    segment_info = []
    for i, element in enumerate(elements):
        color_key = element.get('color', 'gray')
        color = color_map.get(color_key, '#36454F')
        
        start_angle_deg = i * angle_step - 90
        end_angle_deg = (i + 1) * angle_step - 90
        
        start_angle_rad = math.radians(start_angle_deg)
        end_angle_rad = math.radians(end_angle_deg)
        
        outer_start_x = center_x + outer_radius * math.cos(start_angle_rad)
        outer_start_y = center_y + outer_radius * math.sin(start_angle_rad)
        outer_end_x = center_x + outer_radius * math.cos(end_angle_rad)
        outer_end_y = center_y + outer_radius * math.sin(end_angle_rad)
        
        inner_start_x = center_x + inner_radius * math.cos(start_angle_rad)
        inner_start_y = center_y + inner_radius * math.sin(start_angle_rad)
        inner_end_x = center_x + inner_radius * math.cos(end_angle_rad)
        inner_end_y = center_y + inner_radius * math.sin(end_angle_rad)
        
        large_arc = 1 if angle_step > 180 else 0
        
        svg_elements.append(f'''
                <path d="M {outer_start_x} {outer_start_y} 
                         A {outer_radius} {outer_radius} 0 0 {large_arc} {outer_end_x} {outer_end_y}
                         L {inner_end_x} {inner_end_y}
                         A {inner_radius} {inner_radius} 0 0 {large_arc} {inner_start_x} {inner_start_y}
                         Z" fill="{color}"/>
            ''')
        
        mid_angle_deg = (start_angle_deg + end_angle_deg) / 2
        mid_angle_rad = math.radians(mid_angle_deg)
        label_radius = (inner_radius + outer_radius) / 2
        label_x = center_x + label_radius * math.cos(mid_angle_rad)
        label_y = center_y + label_radius * math.sin(mid_angle_rad)
        
        text_color = '#FFFFFF' if color_key in ['blue', 'green', 'purple', 'red', 'gray'] else '#333333'
        
        svg_elements.append(f'''
                <text x="{label_x}" y="{label_y}" font-family="Inter, -apple-system, sans-serif" font-size="16" font-weight="500" fill="{text_color}" text-anchor="middle" dominant-baseline="middle">{element['text']}</text>
            ''')
        
        segment_info.append({
            'start_angle': start_angle_deg,
            'end_angle': end_angle_deg,
            'mid_angle': mid_angle_deg,
            'outer_start_x': outer_start_x,
            'outer_start_y': outer_start_y,
            'outer_end_x': outer_end_x,
            'outer_end_y': outer_end_y
        })
    
    arrow_radius = outer_radius + 40
    control_radius = arrow_radius + 30
    
    for i, seg in enumerate(segment_info):
        next_i = (i + 1) % len(segment_info)
        next_seg = segment_info[next_i]
        
        start_angle_deg = seg['mid_angle']
        end_angle_deg = next_seg['mid_angle']
        
        extended_end_deg = end_angle_deg
        if extended_end_deg <= start_angle_deg:
            extended_end_deg += 360
        angle_span = extended_end_deg - start_angle_deg
        
        start_angle_rad = math.radians(start_angle_deg)
        end_angle_rad = math.radians(end_angle_deg)
        start_x = center_x + arrow_radius * math.cos(start_angle_rad)
        start_y = center_y + arrow_radius * math.sin(start_angle_rad)
        end_x = center_x + arrow_radius * math.cos(end_angle_rad)
        end_y = center_y + arrow_radius * math.sin(end_angle_rad)
        
        cp1_angle_rad = math.radians(start_angle_deg + angle_span * 0.35)
        cp2_angle_rad = math.radians(start_angle_deg + angle_span * 0.65)
        cp1_x = center_x + control_radius * math.cos(cp1_angle_rad)
        cp1_y = center_y + control_radius * math.sin(cp1_angle_rad)
        cp2_x = center_x + control_radius * math.cos(cp2_angle_rad)
        cp2_y = center_y + control_radius * math.sin(cp2_angle_rad)
        
        svg_elements.append(f'''
                <path d="M {start_x} {start_y} C {cp1_x} {cp1_y}, {cp2_x} {cp2_y}, {end_x} {end_y}" 
                      fill="none" stroke="#8E8E93" stroke-width="14" stroke-linecap="round" marker-end="url(#arrowhead)"/>
            ''')
    
    css_content = f"""
        .flywheel-container {{
            position: relative;
            width: {viewbox_size}px;
            height: {viewbox_size}px;
            margin: 60px auto;
        }}
        
        .flywheel-svg {{
            width: 100%;
            height: 100%;
            pointer-events: none;
        }}
        
        .title {{
            font-size: 24px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 32px;
            text-align: center;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top + 40}px;
            font-size: 12px;
            font-weight: 500;
            color: #C7C7CC;
            letter-spacing: -0.01em;
            text-align: right;
            width: 100%;
            max-width: {viewbox_size}px;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    html_content = f"""
    <div class="wrapper">
        <div class="title">{generator.title}</div>
        <div class="flywheel-container">
            <svg class="flywheel-svg" viewBox="-{viewbox_size//2} -{viewbox_size//2} {viewbox_size} {viewbox_size}" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <marker id="arrowhead" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">
                        <path d="M0 0 L12 6 L0 12 Z" fill="#8E8E93"/>
                    </marker>
                </defs>
                {''.join(svg_elements)}
            </svg>
        </div>
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
