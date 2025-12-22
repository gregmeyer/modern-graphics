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
    """Generate a flywheel diagram (circular flow with elements arranged in a circle) using SVG.js
    
    Requires generator.use_svg_js = True for proper rendering.
    """
    if not generator.use_svg_js:
        # Fallback: enable SVG.js for flywheel diagrams
        generator.use_svg_js = True
    num_elements = len(elements)
    angle_step = 360 / num_elements
    center_radius = 70 if center_label else 0
    viewbox_size = radius * 2 + 450  # More padding for elegant spacing
    center_x = viewbox_size // 2
    center_y = viewbox_size // 2
    element_radius = radius
    element_size = 150  # Optimal size for readability and elegance
    
    # Get template colors for elements
    def get_color_from_template(color_key: str) -> tuple:
        """Get gradient colors from template"""
        grad_start, grad_end = generator.template.get_gradient(color_key)
        return grad_start, grad_end
    
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
    
    # Calculate arrow positions for all connections - elegant curved arrows
    arrow_offset = 12  # Increased offset for cleaner look
    arrows_data = []
    for i, pos in enumerate(element_positions):
        next_i = (i + 1) % len(element_positions)
        next_pos = element_positions[next_i]
        
        start_angle_rad = math.radians(pos['angle'])
        end_angle_rad = math.radians(next_pos['angle'])
        half_box = element_size // 2
        
        # Arrow start (right side of current element, slightly outward)
        right_side_angle_rad = start_angle_rad + math.radians(90)
        arrow_start_x = pos['x'] + (half_box + arrow_offset) * math.cos(right_side_angle_rad)
        arrow_start_y = pos['y'] + (half_box + arrow_offset) * math.sin(right_side_angle_rad)
        
        # Arrow end (left side of next element, slightly outward)
        left_side_angle_rad = end_angle_rad - math.radians(90)
        arrow_end_x = next_pos['x'] + (half_box + arrow_offset) * math.cos(left_side_angle_rad)
        arrow_end_y = next_pos['y'] + (half_box + arrow_offset) * math.sin(left_side_angle_rad)
        
        # Calculate smooth arc using cubic bezier for more elegant curves
        # Use two control points for smoother flow
        angle_diff = next_pos['angle'] - pos['angle']
        if angle_diff < -180:
            angle_diff += 360
        elif angle_diff > 180:
            angle_diff -= 360
        
        # First control point - curves outward smoothly
        mid_angle_deg = pos['angle'] + angle_diff / 3
        arc_angle_deg_1 = mid_angle_deg + 50  # Outward curve
        arc_angle_rad_1 = math.radians(arc_angle_deg_1)
        control_radius_1 = element_radius + 90  # Smooth outward curve
        
        # Second control point - continues the smooth curve
        mid_angle_deg_2 = pos['angle'] + (angle_diff * 2 / 3)
        arc_angle_deg_2 = mid_angle_deg_2 + 50
        arc_angle_rad_2 = math.radians(arc_angle_deg_2)
        control_radius_2 = element_radius + 90
        
        cp1_x = center_x + control_radius_1 * math.cos(arc_angle_rad_1)
        cp1_y = center_y + control_radius_1 * math.sin(arc_angle_rad_1)
        cp2_x = center_x + control_radius_2 * math.cos(arc_angle_rad_2)
        cp2_y = center_y + control_radius_2 * math.sin(arc_angle_rad_2)
        
        # Calculate arrowhead direction (tangent to curve at end point)
        # Use the direction from cp2 to end point
        dx = arrow_end_x - cp2_x
        dy = arrow_end_y - cp2_y
        arrow_length = math.sqrt(dx*dx + dy*dy)
        if arrow_length > 0:
            arrow_dir_x = dx / arrow_length
            arrow_dir_y = dy / arrow_length
        else:
            arrow_dir_x = 1
            arrow_dir_y = 0
        
        # Arrowhead size
        arrowhead_size = 12
        arrowhead_width = 8
        
        # Calculate arrowhead triangle points
        # Perpendicular to arrow direction
        perp_x = -arrow_dir_y
        perp_y = arrow_dir_x
        
        arrowhead_tip_x = arrow_end_x
        arrowhead_tip_y = arrow_end_y
        arrowhead_left_x = arrow_end_x - arrowhead_size * arrow_dir_x + arrowhead_width * perp_x
        arrowhead_left_y = arrow_end_y - arrowhead_size * arrow_dir_y + arrowhead_width * perp_y
        arrowhead_right_x = arrow_end_x - arrowhead_size * arrow_dir_x - arrowhead_width * perp_x
        arrowhead_right_y = arrow_end_y - arrowhead_size * arrow_dir_y - arrowhead_width * perp_y
        
        arrows_data.append({
            'start_x': arrow_start_x,
            'start_y': arrow_start_y,
            'end_x': arrow_end_x,
            'end_y': arrow_end_y,
            'cp1_x': cp1_x,
            'cp1_y': cp1_y,
            'cp2_x': cp2_x,
            'cp2_y': cp2_y,
            'arrowhead_tip_x': arrowhead_tip_x,
            'arrowhead_tip_y': arrowhead_tip_y,
            'arrowhead_left_x': arrowhead_left_x,
            'arrowhead_left_y': arrowhead_left_y,
            'arrowhead_right_x': arrowhead_right_x,
            'arrowhead_right_y': arrowhead_right_y
        })
    
    # Get colors for arrows (use primary color from template)
    arrow_color = "#C7C7CC"  # Default, will be overridden by CSS if theme applied
    
    # Generate SVG.js code
    svg_js_parts = []
    
    # Draw arrows with arrowheads directly drawn at the end
    svg_js_parts.append("""
        // Draw all arrows with smooth cubic bezier curves and visible arrowheads
        arrows.forEach(function(arrow, i) {
            // Draw the curved path
            const path = draw.path(`M ${arrow.start_x} ${arrow.start_y} C ${arrow.cp1_x} ${arrow.cp1_y}, ${arrow.cp2_x} ${arrow.cp2_y}, ${arrow.end_x} ${arrow.end_y}`)
                .stroke({color: arrowColor, width: 3})
                .fill('none')
                .opacity(0.6);
            
            // Draw arrowhead triangle directly at the end
            const arrowhead = draw.path(`M ${arrow.arrowhead_tip_x} ${arrow.arrowhead_tip_y} L ${arrow.arrowhead_left_x} ${arrow.arrowhead_left_y} L ${arrow.arrowhead_right_x} ${arrow.arrowhead_right_y} Z`)
                .fill(arrowColor)
                .opacity(0.8);
        });
    """)
    
    # Draw center circle if label provided
    if center_label:
        svg_js_parts.append(f"""
            // Center circle
            const centerCircle = draw.circle({center_radius * 2})
                .move({center_x - center_radius}, {center_y - center_radius})
                .fill('#1D1D1F')
                .opacity(0.95);
            
            const centerCircleBorder = draw.circle({center_radius * 2})
                .move({center_x - center_radius}, {center_y - center_radius})
                .fill('none')
                .stroke({{color: '#E5E5EA', width: 2}})
                .opacity(0.5);
            
            const centerText = draw.text('{center_label}')
                .move({center_x}, {center_y})
                .font({{family: 'Inter, -apple-system, sans-serif', size: 20, weight: 'bold'}})
                .fill('#FFFFFF')
                .attr({{'text-anchor': 'middle', 'dominant-baseline': 'middle'}})
                .attr('letter-spacing', '-0.01em');
        """)
    
    # Draw element boxes with gradients
    for i, pos in enumerate(element_positions):
        element = pos['element']
        color_key = element.get('color', 'gray')
        grad_start, grad_end = get_color_from_template(color_key)
        
        box_x = pos['x'] - element_size // 2
        box_y = pos['y'] - element_size // 2
        
        # Escape text for JavaScript
        element_text = element['text'].replace("'", "\\'").replace('"', '\\"')
        
        svg_js_parts.append(f"""
            // Gradient for element {i}
            const grad{i} = draw.gradient('linear', function(add) {{
                add.stop(0, '{grad_start}').opacity(0.3);
                add.stop(1, '{grad_end}').opacity(0.15);
            }});
            
            // Element box {i} - elegant rounded rectangle
            const box{i} = draw.rect({element_size}, {element_size})
                .move({box_x}, {box_y})
                .radius(18)
                .fill(grad{i})
                .stroke({{color: '{grad_start}', width: 2}})
                .opacity(0.98);
            
            // Element text {i} - refined typography
            const text{i} = draw.text('{element_text}')
                .move({pos['x']}, {pos['y']})
                .font({{family: 'Inter, -apple-system, sans-serif', size: 19, weight: 'bold'}})
                .fill('#1D1D1F')
                .attr({{'text-anchor': 'middle', 'dominant-baseline': 'middle'}})
                .attr('letter-spacing', '-0.02em');
        """)
    
    svg_js_code = '\n'.join(svg_js_parts)
    
    # Generate container and script
    container_id = "flywheel-svg-container"
    container_html = f'<div id="{container_id}" style="width: {viewbox_size}px; height: {viewbox_size}px; margin: 0 auto;"></div>'
    
    # Create the SVG.js initialization script with arrow data
    arrows_json = str(arrows_data).replace("'", '"')
    
    script_html = f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const draw = SVG().addTo('#{container_id}').size({viewbox_size}, {viewbox_size});
        
        // Arrow data
        const arrows = {arrows_json};
        const arrowColor = '{arrow_color}';
        
        {svg_js_code}
    }});
    </script>
    """
    
    css_content = f"""
        .flywheel-container {{
            position: relative;
            width: {viewbox_size}px;
            height: {viewbox_size}px;
            margin: 60px auto;
        }}
        
        #{container_id} {{
            width: 100%;
            height: 100%;
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
            {container_html}
            {script_html}
        </div>
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
