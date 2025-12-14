"""Flywheel diagram generator"""

import math
from typing import List, Dict, Optional
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def generate_flywheel_diagram(
    generator: BaseGenerator,
    elements: List[Dict[str, any]],
    center_label: Optional[str] = None,
    radius: int = 220
) -> str:
    """Generate a flywheel diagram (circular flow with elements arranged in a circle)"""
    num_elements = len(elements)
    angle_step = 360 / num_elements
    center_radius = 80 if center_label else 0
    viewbox_size = radius * 2 + 400
    center_x = viewbox_size // 2
    center_y = viewbox_size // 2
    element_radius = radius
    element_size = 140  # Size of each element box
    
    svg_elements = []
    
    # Use template colors instead of hardcoded colors
    def get_color_from_template(color_key: str) -> str:
        """Get color from template or fallback to default"""
        color_def = generator.template.get_color(color_key)
        # Extract a solid color from gradient (use first gradient color)
        gradient = color_def.get("gradient", ("#8E8E93", "#8E8E93"))
        if isinstance(gradient, tuple) and len(gradient) > 0:
            return gradient[0]
        return '#8E8E93'
    
    # Center circle if label provided
    if center_label:
        svg_elements.append(f'''
                <circle cx="{center_x}" cy="{center_y}" r="{center_radius}" fill="#1D1D1F" opacity="0.95"/>
                <circle cx="{center_x}" cy="{center_y}" r="{center_radius}" fill="none" stroke="#E5E5EA" stroke-width="2" opacity="0.5"/>
                <text x="{center_x}" y="{center_y + 7}" font-family="Inter, -apple-system, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle" dominant-baseline="middle" letter-spacing="-0.01em">{center_label}</text>
            ''')
    
    # Calculate element positions in circle
    element_positions = []
    for i, element in enumerate(elements):
        angle_deg = i * angle_step - 90  # Start at top
        angle_rad = math.radians(angle_deg)
        
        # Position of element center
        element_x = center_x + element_radius * math.cos(angle_rad)
        element_y = center_y + element_radius * math.sin(angle_rad)
        
        element_positions.append({
            'x': element_x,
            'y': element_y,
            'angle': angle_deg,
            'element': element
        })
    
    # Draw arrows between elements (circular flow - clockwise)
    # For clockwise flow: arrow exits from right side of source node, enters left side of target node
    arrow_offset = 8  # Small offset to ensure arrow is just outside the box edge
    for i, pos in enumerate(element_positions):
        next_i = (i + 1) % len(element_positions)
        next_pos = element_positions[next_i]
        
        # Calculate angles for arrow connection points
        start_angle_rad = math.radians(pos['angle'])
        end_angle_rad = math.radians(next_pos['angle'])
        
        # For clockwise flow, we need to find the right side of source and left side of target
        # Right side of source: angle + 90 degrees (clockwise from outward direction)
        # Left side of target: angle - 90 degrees (counter-clockwise from outward direction)
        half_box = element_size // 2
        
        # Arrow starts from RIGHT side of current element (clockwise direction)
        # Right side angle = element_angle + 90 degrees
        right_side_angle_rad = start_angle_rad + math.radians(90)
        arrow_start_x = pos['x'] + (half_box + arrow_offset) * math.cos(right_side_angle_rad)
        arrow_start_y = pos['y'] + (half_box + arrow_offset) * math.sin(right_side_angle_rad)
        
        # Arrow ends at LEFT side of next element (clockwise direction)
        # Left side angle = element_angle - 90 degrees
        left_side_angle_rad = end_angle_rad - math.radians(90)
        arrow_end_x = next_pos['x'] + (half_box + arrow_offset) * math.cos(left_side_angle_rad)
        arrow_end_y = next_pos['y'] + (half_box + arrow_offset) * math.sin(left_side_angle_rad)
        
        # Calculate control points for clockwise arc (45° arc)
        # The arc should curve outward (away from center) in a clockwise direction
        # Use a 45-degree offset from the midpoint for smooth clockwise arc
        angle_diff = next_pos['angle'] - pos['angle']
        # Normalize angle difference to [-180, 180]
        if angle_diff < -180:
            angle_diff += 360
        elif angle_diff > 180:
            angle_diff -= 360
        
        # Mid angle for the arc (between the two element angles)
        mid_angle_deg = pos['angle'] + angle_diff / 2
        # Add 45 degrees for clockwise arc (curving outward)
        arc_angle_deg = mid_angle_deg + 45
        arc_angle_rad = math.radians(arc_angle_deg)
        
        # Control point should be further out from center to create clockwise arc
        # For clockwise, the control point should be at a larger radius
        control_radius = element_radius + 80
        
        cp1_x = center_x + control_radius * math.cos(arc_angle_rad)
        cp1_y = center_y + control_radius * math.sin(arc_angle_rad)
        
        # Use quadratic Bezier for smooth clockwise arc
        svg_elements.append(f'''
                <path d="M {arrow_start_x} {arrow_start_y} Q {cp1_x} {cp1_y}, {arrow_end_x} {arrow_end_y}" 
                      fill="none" stroke="#C7C7CC" stroke-width="4" stroke-linecap="round" 
                      marker-end="url(#arrowhead)" opacity="0.8"/>
            ''')
    
    # Create gradients for all colors used (using template colors)
    gradient_defs = []
    used_colors = set()
    for pos in element_positions:
        color_key = pos['element'].get('color', 'gray')
        if color_key not in used_colors:
            used_colors.add(color_key)
            # Get gradient colors from template
            grad_start, grad_end = generator.template.get_gradient(color_key)
            gradient_id = f"gradient-{color_key}"
            gradient_defs.append(f'''
                    <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:{grad_start};stop-opacity:0.25" />
                        <stop offset="100%" style="stop-color:{grad_end};stop-opacity:0.1" />
                    </linearGradient>
                ''')
    
    # Draw element boxes with improved styling (using template colors)
    for pos in element_positions:
        element = pos['element']
        color_key = element.get('color', 'gray')
        # Get color from template gradient
        grad_start, grad_end = generator.template.get_gradient(color_key)
        color = grad_start  # Use first gradient color for stroke
        gradient_id = f"gradient-{color_key}"
        
        # Element box with better styling
        box_x = pos['x'] - element_size // 2
        box_y = pos['y'] - element_size // 2
        
        svg_elements.append(f'''
                <rect x="{box_x}" y="{box_y}" width="{element_size}" height="{element_size}" 
                      rx="16" fill="url(#{gradient_id})" stroke="{color}" stroke-width="3"/>
                <text x="{pos['x']}" y="{pos['y'] + 6}" font-family="Inter, -apple-system, sans-serif" 
                      font-size="18" font-weight="700" fill="#1D1D1F" 
                      text-anchor="middle" dominant-baseline="middle" letter-spacing="-0.01em">{element['text']}</text>
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
            <svg class="flywheel-svg" viewBox="0 0 {viewbox_size} {viewbox_size}" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <marker id="arrowhead" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">
                        <path d="M0 0 L12 6 L0 12 Z" fill="#8E8E93" opacity="0.8"/>
                    </marker>
                    {''.join(gradient_defs)}
                </defs>
                {''.join(svg_elements)}
            </svg>
        </div>
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
