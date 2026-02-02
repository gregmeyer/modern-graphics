"""Flywheel diagram generator - Material Design: track circle, numbered nodes, flat cards"""

import html as html_module
import math
from typing import List, Dict, Optional, TYPE_CHECKING
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES
from .theme_utils import (
    extract_theme_colors,
    generate_css_variables,
    inject_google_fonts,
    with_alpha,
)

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def generate_flywheel_diagram(
    generator: BaseGenerator,
    elements: List[Dict[str, any]],
    center_label: Optional[str] = None,
    radius: int = 180,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Generate a Material Design flywheel: track circle, numbered nodes, flat cards on rays.
    
    Static SVG only; no JavaScript. Renders reliably for PNG export.
    
    Args:
        generator: BaseGenerator instance
        elements: List of element dicts with 'text' and optional 'color'
        center_label: Optional label for center circle
        radius: Radius of the track circle (distance from center to nodes)
        color_scheme: Optional ColorScheme for theming
        
    Returns:
        HTML string
    """
    theme = extract_theme_colors(color_scheme)
    
    elements = list(elements) if elements else [{"text": "Step 1", "color": "blue"}]
    num_elements = len(elements)
    angle_step = 360 / num_elements
    
    # Layout: center, track radius, node size, card distance from center
    cx = 320.0
    cy = 320.0
    track_r = float(min(radius, 200))
    node_r = 14.0
    card_center_r = track_r + 88.0
    card_w = 180.0
    card_h = 52.0
    view_size = 640
    # Ensure viewbox fits cards (card center at card_center_r, card extends card_w/2)
    margin = card_center_r + card_w / 2 + 24
    if margin * 2 > view_size:
        view_size = int(margin * 2)
        cx = view_size / 2
        cy = view_size / 2
    
    # Node positions on track
    nodes = []
    for i in range(num_elements):
        angle_deg = i * angle_step - 90
        angle_rad = math.radians(angle_deg)
        nx = cx + track_r * math.cos(angle_rad)
        ny = cy + track_r * math.sin(angle_rad)
        nodes.append({
            "x": nx, "y": ny, "angle": angle_deg, "angle_rad": angle_rad,
            "element": elements[i],
        })
    
    # Card positions (further out on same ray)
    def card_center_and_rect(node: dict) -> dict:
        ar = node["angle_rad"]
        ccx = cx + card_center_r * math.cos(ar)
        ccy = cy + card_center_r * math.sin(ar)
        rx = ccx - card_w / 2
        ry = ccy - card_h / 2
        return {"cx": ccx, "cy": ccy, "rx": rx, "ry": ry, "width": card_w, "height": card_h}
    
    cards = [card_center_and_rect(n) for n in nodes]
    
    # Connector: from node edge to card center (along ray)
    def connector_path(node: dict, card: dict) -> str:
        ar = node["angle_rad"]
        n_ex = node["x"] + node_r * math.cos(ar)
        n_ey = node["y"] + node_r * math.sin(ar)
        ccx, ccy = card["cx"], card["cy"]
        return f"M {n_ex:.1f} {n_ey:.1f} L {ccx:.1f} {ccy:.1f}"
    
    # Arrows along track: clockwise flow (Amazon-style). SVG arc sweep=1 = positive angle = clockwise in screen coords (y down).
    arrow_paths = []
    for i in range(num_elements):
        j = (i + 1) % num_elements
        n1, n2 = nodes[i], nodes[j]
        a1, a2 = n1["angle_rad"], n2["angle_rad"]
        x1 = cx + track_r * math.cos(a1)
        y1 = cy + track_r * math.sin(a1)
        x2 = cx + track_r * math.cos(a2)
        y2 = cy + track_r * math.sin(a2)
        sweep = 1  # clockwise (top → right → bottom → left → top)
        arrow_paths.append({
            "d": f"M {x1:.1f} {y1:.1f} A {track_r:.1f} {track_r:.1f} 0 0 {sweep} {x2:.1f} {y2:.1f}",
            "end_x": x2, "end_y": y2,
            "angle": n2["angle_rad"],
        })
    
    # Arrowhead at end of arc: point in direction of travel (clockwise, Amazon-style).
    # Screen coords: y down. Radius angle θ from center (0=right, 90°=bottom). CW tangent at θ = (sin θ, -cos θ) => angle = θ + 90°.
    def arrowhead_polygon(ax: float, ay: float, angle_rad: float) -> str:
        tangent = angle_rad + math.radians(90)  # CW tangent
        tip_len = 14
        half_w = 6
        tx = ax + tip_len * math.cos(tangent)
        ty = ay + tip_len * math.sin(tangent)
        perp_x = -math.sin(tangent)
        perp_y = math.cos(tangent)
        lx = ax - half_w * math.cos(tangent) + half_w * perp_x
        ly = ay - half_w * math.sin(tangent) + half_w * perp_y
        rx = ax - half_w * math.cos(tangent) - half_w * perp_x
        ry = ay - half_w * math.sin(tangent) - half_w * perp_y
        return f"{tx:.1f},{ty:.1f} {lx:.1f},{ly:.1f} {rx:.1f},{ry:.1f}"
    
    track_color = with_alpha(theme.text_tertiary, 0.24)
    connector_color = with_alpha(theme.text_tertiary, 0.45)  # visible in PNG export
    arrow_color = theme.accent
    node_fill = theme.accent
    node_text_color = theme.bg_primary if theme.is_dark else "#FFFFFF"
    card_fill = theme.card_bg
    card_stroke = with_alpha(theme.text_tertiary, 0.24)
    card_text_color = theme.text_primary
    
    # Center circle (optional)
    center_svg = ""
    if center_label:
        center_r = 44.0
        safe_center = html_module.escape(center_label)
        center_bg = theme.text_primary if theme.is_dark else "#1D1D1F"
        center_text_fill = theme.bg_primary if theme.is_dark else "#FFFFFF"
        center_svg = f"""
        <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{center_r}" fill="{center_bg}" stroke="{with_alpha(theme.accent, 0.4)}" stroke-width="1.5"/>
        <text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" dominant-baseline="middle" fill="{center_text_fill}" font-family="{theme.font_family_display}" font-size="14" font-weight="700">{safe_center}</text>"""
    
    # Build SVG (arrows drawn last so they sit on top and are always visible)
    parts = []
    parts.append(f'<svg class="flywheel-svg" viewBox="0 0 {view_size:.0f} {view_size:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Flywheel diagram">')
    
    # Track circle
    parts.append(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{track_r:.1f}" fill="none" stroke="{track_color}" stroke-width="2"/>')
    
    # Center
    if center_svg:
        parts.append("  <g class=\"flywheel-center\">")
        parts.append(center_svg.strip())
        parts.append("  </g>")
    
    # Cards (flat, 8px radius, Material surface)
    parts.append('  <g class="flywheel-cards">')
    for node, card in zip(nodes, cards):
        safe_text = html_module.escape(node["element"]["text"])
        parts.append(f'    <rect x="{card["rx"]:.1f}" y="{card["ry"]:.1f}" width="{card["width"]:.0f}" height="{card["height"]:.0f}" rx="8" fill="{card_fill}" stroke="{card_stroke}" stroke-width="1"/>')
        parts.append(f'    <text x="{card["cx"]:.1f}" y="{card["cy"]:.1f}" text-anchor="middle" dominant-baseline="middle" fill="{card_text_color}" font-family="{theme.font_family_body}" font-size="15" font-weight="600">{safe_text}</text>')
    parts.append("  </g>")
    
    # Nodes (numbered circles)
    parts.append('  <g class="flywheel-nodes">')
    for i, node in enumerate(nodes):
        parts.append(f'    <circle cx="{node["x"]:.1f}" cy="{node["y"]:.1f}" r="{node_r}" fill="{node_fill}"/>')
        parts.append(f'    <text x="{node["x"]:.1f}" y="{node["y"]:.1f}" text-anchor="middle" dominant-baseline="middle" fill="{node_text_color}" font-family="{theme.font_family_display}" font-size="13" font-weight="700">{i + 1}</text>')
    parts.append("  </g>")
    
    # Secondary arcs: connectors from each node to its card (on top so they show in PNG)
    parts.append('  <g class="flywheel-connectors">')
    for node, card in zip(nodes, cards):
        parts.append(f'    <path d="{connector_path(node, card)}" fill="none" stroke="{connector_color}" stroke-width="2" stroke-linecap="round"/>')
    parts.append("  </g>")
    
    # Arrows along track (on top so directional arrows are always visible in browser)
    parts.append('  <g class="flywheel-arrows">')
    for arr in arrow_paths:
        parts.append(f'    <path d="{arr["d"]}" fill="none" stroke="{arrow_color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append(f'    <polygon points="{arrowhead_polygon(arr["end_x"], arr["end_y"], arr["angle"])}" fill="{arrow_color}"/>')
    parts.append("  </g>")
    
    parts.append("</svg>")
    svg_content = "\n".join(parts)
    
    css_content = f"""
        {generate_css_variables(theme)}
        
        .flywheel-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }}
        
        .flywheel-container {{
            position: relative;
            width: 100%;
            max-width: min({view_size:.0f}px, 100%);
            margin: 40px auto;
        }}
        
        .flywheel-svg {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .title {{
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            color: var(--text-1);
            margin-bottom: 32px;
            text-align: center;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .attribution {{
            margin-top: {generator.attribution.margin_top + 24}px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-3);
            letter-spacing: -0.01em;
            text-align: right;
            width: 100%;
            max-width: {view_size:.0f}px;
        }}
        
        {ATTRIBUTION_STYLES}
    """
    
    html_content = f"""
    <div class="flywheel-wrapper">
        <div class="title">{generator.title}</div>
        <div class="flywheel-container">
            {svg_content}
        </div>
        {generator._generate_attribution_html()}
    </div>
    """
    
    full_html = generator._wrap_html(html_content, css_content)
    return inject_google_fonts(full_html, theme)