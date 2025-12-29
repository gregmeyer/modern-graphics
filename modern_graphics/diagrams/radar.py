"""Radar diagram generator for support signal mapping and similar visualizations"""

import math
from typing import List, Dict, Optional
from ..base import BaseGenerator
from .base import DiagramGenerator


def generate_radar_diagram(
    generator: BaseGenerator,
    signals: List[Dict[str, any]],
    center_label: str = "Support Radar",
    viewbox_width: int = 1200,
    viewbox_height: int = 700,
    radar_radius: int = 250,
    show_sweep: bool = True,
    show_circles: bool = True,
) -> str:
    """Generate a radar diagram with signals positioned around a center point.
    
    Args:
        generator: BaseGenerator instance with template and attribution
        center_label: Label for the center radar dish
        signals: List of signal dictionaries with:
            - label: Signal text
            - axiom: Axiom identifier or name
            - failure_type: Type of failure discovered
            - covers: What it covers (optional)
            - position: Dict with 'angle' (degrees) or 'x', 'y' (0-1 normalized)
            - color: Color key (blue, purple, green, orange, gray)
        viewbox_width: SVG viewBox width
        viewbox_height: SVG viewBox height
        radar_radius: Radius of the outer radar circle
        show_sweep: Whether to show animated radar sweep
        show_circles: Whether to show concentric radar circles
        
    Returns:
        HTML string for the radar diagram
    """
    center_x = viewbox_width // 2
    center_y = viewbox_height // 2
    
    # Generate SVG content
    svg_parts = []
    
    # SVG definitions
    svg_parts.append("""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
        <defs>
            <radialGradient id="radarGradient" cx="50%" cy="50%">
                <stop offset="0%" stop-color="#0A84FF" stop-opacity="0.15"/>
                <stop offset="50%" stop-color="#0A84FF" stop-opacity="0.08"/>
                <stop offset="100%" stop-color="#0A84FF" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="sweepGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#0A84FF" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#0A84FF" stop-opacity="0"/>
            </linearGradient>
            <filter id="glow">
                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            <filter id="cardShadow">
                <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
                <feOffset dx="0" dy="2" result="offsetblur"/>
                <feComponentTransfer>
                    <feFuncA type="linear" slope="0.3"/>
                </feComponentTransfer>
                <feMerge>
                    <feMergeNode/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>""".format(width=viewbox_width, height=viewbox_height))
    
    # Color mapping
    color_map = {
        "blue": "#0A84FF",
        "purple": "#8B5CF6",
        "green": "#34C759",
        "orange": "#FF9500",
        "gray": "#6B7280",
    }
    
    # Radar circles
    if show_circles:
        for r in [radar_radius, int(radar_radius * 0.72), int(radar_radius * 0.44)]:
            svg_parts.append(
                f'<circle cx="{center_x}" cy="{center_y}" r="{r}" fill="none" stroke="#D6DAE0" stroke-width="2" opacity="0.4"/>'
            )
    
    # Radar sweep (animated)
    if show_sweep:
        sweep_path = f'M {center_x} {center_y} L {center_x} {center_y - radar_radius} A {radar_radius} {radar_radius} 0 0 1 {center_x + int(radar_radius * 0.707)} {center_y - int(radar_radius * 0.707)} Z'
        svg_parts.append(
            f'<path d="{sweep_path}" fill="url(#sweepGradient)" opacity="0.3">'
            f'<animateTransform attributeName="transform" type="rotate" values="0 {center_x} {center_y};360 {center_x} {center_y}" dur="8s" repeatCount="indefinite"/>'
            f'</path>'
        )
    
    # Center radar dish
    svg_parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="70" fill="url(#radarGradient)" stroke="#0A84FF" stroke-width="3" filter="url(#glow)"/>')
    svg_parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="35" fill="#0A84FF" opacity="0.2"/>')
    svg_parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="18" fill="#0A84FF"/>')
    
    # Center label
    label_lines = center_label.split('\n')
    for i, line in enumerate(label_lines):
        y_offset = center_y + 35 + (i * 15)
        svg_parts.append(
            f'<text x="{center_x}" y="{y_offset}" text-anchor="middle" font-family="Roboto, sans-serif" font-size="12" font-weight="600" fill="#0A84FF" opacity="0.8">{line}</text>'
        )
    
    # Process signals
    for i, signal in enumerate(signals):
        color_key = signal.get('color', 'blue')
        color = color_map.get(color_key, color_map['blue'])
        
        # Calculate position
        distance = radar_radius * 0.85  # Position signals at 85% of radius
        
        if 'angle' in signal:
            # Position by angle (degrees, 0 = top, clockwise)
            angle_rad = math.radians(signal['angle'] - 90)
            x = center_x + distance * math.cos(angle_rad)
            y = center_y + distance * math.sin(angle_rad)
        elif 'position' in signal:
            pos = signal['position']
            if 'x' in pos and 'y' in pos:
                # Normalized coordinates (0-1)
                x = pos['x'] * viewbox_width
                y = pos['y'] * viewbox_height
            elif 'angle' in pos:
                angle_rad = math.radians(pos['angle'] - 90)
                distance = radar_radius * 0.85
                x = center_x + distance * math.cos(angle_rad)
                y = center_y + distance * math.sin(angle_rad)
        else:
            # Default: distribute evenly around circle
            angle = (i * 360 / len(signals)) - 90
            angle_rad = math.radians(angle)
            distance = radar_radius * 0.85
            x = center_x + distance * math.cos(angle_rad)
            y = center_y + distance * math.sin(angle_rad)
        
        # Signal blip
        svg_parts.append(
            f'<circle cx="{int(x)}" cy="{int(y)}" r="12" fill="{color}" filter="url(#glow)" opacity="0.9">'
            f'<animate attributeName="opacity" values="0.3;1;0.3" dur="{2 + i * 0.2}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
        
        # Connection line
        svg_parts.append(
            f'<line x1="{center_x}" y1="{center_y}" x2="{int(x)}" y2="{int(y)}" stroke="{color}" stroke-width="2" stroke-dasharray="4 4" opacity="0.3"/>'
        )
        
        # Annotation card
        card_width = 240
        card_height = 75 if signal.get('covers') else 60
        
        # Position card based on signal position
        if x > center_x:
            card_x = int(x) + 20
            text_anchor = "start"
        else:
            card_x = int(x) - card_width - 20
            text_anchor = "end"
        
        if y < center_y:
            card_y = int(y) - 10
        else:
            card_y = int(y) + 10
        
        # Ensure card stays within bounds
        card_x = max(10, min(card_x, viewbox_width - card_width - 10))
        card_y = max(10, min(card_y, viewbox_height - card_height - 10))
        
        svg_parts.append(
            f'<rect x="{card_x}" y="{card_y}" width="{card_width}" height="{card_height}" rx="8" fill="#FFFFFF" stroke="{color}" stroke-width="2" filter="url(#cardShadow)" opacity="0.95"/>'
        )
        
        # Card content
        axiom_text = signal.get('axiom', f'Axiom {i+1}')
        detects_text = signal.get('detects', signal.get('label', ''))
        discovers_text = signal.get('discovers', signal.get('failure_type', ''))
        covers_text = signal.get('covers', '')
        
        text_x = card_x + card_width // 2
        
        svg_parts.append(
            f'<text x="{text_x}" y="{card_y + 22}" text-anchor="middle" font-family="Roboto, sans-serif" font-size="13" font-weight="700" fill="{color}">{axiom_text}</text>'
        )
        svg_parts.append(
            f'<text x="{text_x}" y="{card_y + 38}" text-anchor="middle" font-family="Roboto, sans-serif" font-size="11" fill="#4B5563">Detects: {detects_text}</text>'
        )
        svg_parts.append(
            f'<text x="{text_x}" y="{card_y + 52}" text-anchor="middle" font-family="Roboto, sans-serif" font-size="11" fill="#4B5563">Discovers: {discovers_text}</text>'
        )
        if covers_text:
            svg_parts.append(
                f'<text x="{text_x}" y="{card_y + 66}" text-anchor="middle" font-family="Roboto, sans-serif" font-size="10" fill="#6B7280" font-style="italic">Covers: {covers_text}</text>'
            )
    
    svg_parts.append("</svg>")
    
    svg_content = "\n        ".join(svg_parts)
    
    html_content = f"""
    <div class="radar-wrapper">
        <div class="radar-container">
            {svg_content}
        </div>
    </div>
    {generator._generate_attribution_html()}
    """
    
    css_content = """
        body {
            margin: 0;
            padding: 60px 40px;
            background: #FFFFFF;
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .radar-wrapper {
            max-width: 1600px;
            margin: 0 auto;
        }
        .radar-container {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    """
    
    return generator._wrap_html(html_content, css_content)


class RadarDiagramGenerator(DiagramGenerator):
    """Generator class for radar diagrams"""
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters"""
        required = ['signals']
        return all(key in kwargs for key in required) and isinstance(kwargs.get('signals'), list)
    
    def generate(self, generator: BaseGenerator, **kwargs) -> str:
        """Generate radar diagram"""
        return generate_radar_diagram(generator, **kwargs)
