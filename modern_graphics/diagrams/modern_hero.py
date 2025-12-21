"""Modern hero slide layouts (open + triptych)."""

from __future__ import annotations

from html import escape
from typing import List, Dict, Optional, Any

from .base import BaseGenerator


def _render_svg_icon(kind: Optional[str], size: int = 64) -> str:
    """Return a lightweight SVG icon for hero panels."""
    if kind == "manual":
        return f"""<svg viewBox=\"0 0 64 64\" width=\"{size}\" height=\"{size}\" aria-hidden=\"true\"><rect x=\"10\" y=\"14\" width=\"44\" height=\"34\" rx=\"6\" fill=\"rgba(235,235,241,0.8)\" stroke=\"#D1D5DB\" stroke-width=\"1.5\"/><line x1=\"18\" y1=\"24\" x2=\"46\" y2=\"24\" stroke=\"#C084FC\" stroke-width=\"2\"/><line x1=\"18\" y1=\"32\" x2=\"40\" y2=\"32\" stroke=\"#C4B5FD\" stroke-width=\"1.5\"/><line x1=\"18\" y1=\"40\" x2=\"32\" y2=\"40\" stroke=\"#C4B5FD\" stroke-width=\"1.5\"/></svg>"""
    if kind == "templates":
        return f"""<svg viewBox=\"0 0 64 64\" width=\"{size}\" height=\"{size}\" aria-hidden=\"true\"><rect x=\"8\" y=\"12\" width=\"48\" height=\"40\" rx=\"12\" fill=\"#F4F2FF\" stroke=\"#C7B6F7\" stroke-width=\"1.2\"/><rect x=\"16\" y=\"20\" width=\"12\" height=\"8\" rx=\"4\" fill=\"#DCD2FF\"/><rect x=\"34\" y=\"20\" width=\"12\" height=\"8\" rx=\"4\" fill=\"#CABAF6\"/><rect x=\"16\" y=\"32\" width=\"12\" height=\"8\" rx=\"4\" fill=\"#ECE7FF\"/><rect x=\"34\" y=\"32\" width=\"12\" height=\"8\" rx=\"4\" fill=\"#F4E8FF\"/></svg>"""
    if kind == "generated":
        return f"""<svg viewBox=\"0 0 64 64\" width=\"{size}\" height=\"{size}\" aria-hidden=\"true\"><rect x=\"12\" y=\"14\" width=\"40\" height=\"36\" rx=\"12\" fill=\"rgba(235,235,241,0.85)\" stroke=\"#D1D5DB\" stroke-width=\"1.5\"/><path d=\"M18 36 L28 26 L36 34 L46 24\" stroke=\"#BFA7F4\" stroke-width=\"2\" fill=\"none\"/><circle cx=\"46\" cy=\"24\" r=\"4\" fill=\"#A78BFA\"/><line x1=\"18\" y1=\"40\" x2=\"44\" y2=\"40\" stroke=\"#C4B5FD\" stroke-width=\"2\"/></svg>"""
    if kind == "warning":
        return f"""<svg viewBox=\"0 0 64 64\" width=\"{size}\" height=\"{size}\" aria-hidden=\"true\"><polygon points=\"32,8 58,54 6,54\" fill=\"rgba(244,114,182,0.18)\" stroke=\"#F472B6\" stroke-width=\"2\"/><line x1=\"32\" y1=\"22\" x2=\"32\" y2=\"38\" stroke=\"#F472B6\" stroke-width=\"3\"/><circle cx=\"32\" cy=\"46\" r=\"3\" fill=\"#F472B6\"/></svg>"""
    if kind == "search":
        return f"""<svg viewBox=\"0 0 64 64\" width=\"{size}\" height=\"{size}\" aria-hidden=\"true\"><circle cx=\"28\" cy=\"28\" r=\"16\" fill=\"rgba(99,102,241,0.12)\" stroke=\"#6366F1\" stroke-width=\"2\"/><line x1=\"40\" y1=\"40\" x2=\"54\" y2=\"54\" stroke=\"#6366F1\" stroke-width=\"3\" stroke-linecap=\"round\"/></svg>"""
    return f"""<svg viewBox=\"0 0 64 64\" width=\"{size}\" height=\"{size}\" aria-hidden=\"true\"><circle cx=\"32\" cy=\"32\" r=\"24\" fill=\"rgba(235,235,241,0.7)\" stroke=\"#DCD7F9\"/></svg>"""


def _render_list(items: Optional[List[str]]) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{item}</li>" for item in items)
    return f"<ul>{lis}</ul>"


def _render_stats(stats: Optional[List[Dict[str, str]]]) -> str:
    if not stats:
        return ""
    stat_html = "".join(
        f"<div class='stat'><span>{stat.get('label', '')}</span><strong>{stat.get('value', '')}</strong></div>"
        for stat in stats
    )
    return f"<div class='stats'>{stat_html}</div>"

def _render_tile_flow(tiles: Optional[List[Dict[str, str]]]) -> str:
    if not tiles:
        return ""
    cards = []
    for tile in tiles:
        icon_svg = _render_svg_icon(tile.get("icon"), size=52)
        cards.append(
            f"""
            <div class="tile">
                <div class="tile-icon">{icon_svg}</div>
                <div class="tile-label">{tile.get('label', '')}</div>
            </div>
            """
        )
    return f"<div class='tile-flow'>{''.join(cards)}</div>"


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 360


def _extract_panel_data(
    highlights: Optional[List[str]],
    highlight_tiles: Optional[List[Dict[str, str]]],
) -> List[Dict[str, str]]:
    """Derive up to three panel labels/icons from existing inputs."""
    panels: List[Dict[str, str]] = []
    if highlight_tiles:
        for tile in highlight_tiles:
            panels.append({"label": tile.get("label", ""), "icon": tile.get("icon")})
    elif highlights:
        for text in highlights:
            panels.append({"label": text, "icon": None})
    if not panels:
        panels = [
            {"label": "Orchestration", "icon": "manual"},
            {"label": "Observability", "icon": "generated"},
            {"label": "Memory", "icon": "templates"},
        ]
    return panels[:3]


def _render_ribbon_collage(panels: List[Dict[str, str]]) -> str:
    """Render a flowing ribbon collage with translucent panels."""
    panel_html = []
    for idx, panel in enumerate(panels[:3]):
        left = 22 + idx * 28
        top = 38 + ((idx % 2) * 10)
        icon_svg = _render_svg_icon(panel.get("icon"), size=40)
        panel_html.append(
            f"""
            <div class="ribbon-panel" style="left:{left}%; top:{top}%;">
                <div class="ribbon-icon">{icon_svg}</div>
                <div class="ribbon-label">{escape(panel.get('label', ''))}</div>
            </div>
            """
        )
    return f"""
        <div class="ribbon-area">
            <svg class="ribbon-svg" viewBox="0 0 1200 320" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="ribbonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFCF6B" />
                        <stop offset="50%" stop-color="#FF9D5C" />
                        <stop offset="100%" stop-color="#FF5F5F" />
                    </linearGradient>
                </defs>
                <path d="M-20 180 C 200 120, 420 240, 640 180 S 1000 80, 1220 200"
                      stroke="url(#ribbonGrad)" stroke-width="90" fill="none" stroke-linecap="round" opacity="0.8"/>
                <path d="M-20 170 C 200 110, 420 260, 640 190 S 1000 100, 1220 180"
                      stroke="rgba(255,255,255,0.45)" stroke-width="2" fill="none" stroke-dasharray="30 14"/>
                <circle cx="160" cy="120" r="6" class="ribbon-glyph"/>
                <circle cx="520" cy="220" r="8" class="ribbon-glyph"/>
                <circle cx="920" cy="150" r="5" class="ribbon-glyph"/>
            </svg>
            <div class="ribbon-panels">
                {''.join(panel_html)}
            </div>
        </div>
    """


def _normalize_ratio(value, dimension):
    if value is None:
        return None
    try:
        if isinstance(value, str):
            raw = value.strip()
            if raw.endswith("%"):
                return max(0.0, min(1.0, float(raw[:-1]) / 100.0))
            value = float(raw)
        else:
            value = float(value)
    except (ValueError, TypeError):
        return None
    if value > 1.5:
        value = value / float(dimension)
    return max(0.0, min(1.0, value))


def _prepare_flow_nodes(flow_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not flow_nodes:
        return []
    processed = []
    total = len(flow_nodes)
    for idx, node in enumerate(flow_nodes):
        node_id = node.get("id") or f"node{idx}"
        position = node.get("position") or node.get("pos") or {}
        x = _normalize_ratio(position.get("x"), CANVAS_WIDTH)
        y = _normalize_ratio(position.get("y"), CANVAS_HEIGHT)
        orbit = (node.get("orbit") or "").lower()
        if x is None:
            if total == 1:
                x = 0.5
            else:
                span = 0.82
                x = 0.09 + span * (idx / max(total - 1, 1))
        if y is None:
            if orbit == "top":
                y = 0.32
            elif orbit == "bottom":
                y = 0.68
            elif orbit == "mid" or orbit == "center":
                y = 0.5
            else:
                y = 0.38 if idx % 2 == 0 else 0.62
        processed.append(
            {
                "id": node_id,
                "label": node.get("label", ""),
                "icon": node.get("icon"),
                "size": node.get("size", "medium"),
                "x": max(0.03, min(0.97, x)),
                "y": max(0.18, min(0.82, y)),
            }
        )
    return processed


def _render_flowchart(flow_nodes, connections=None):
    if not flow_nodes:
        return ""
    nodes = _prepare_flow_nodes(flow_nodes)
    node_lookup = {node["id"]: node for node in nodes}
    if not connections:
        connections = []
        for idx in range(len(nodes) - 1):
            connections.append({"from": nodes[idx]["id"], "to": nodes[idx + 1]["id"]})

    path_html = []
    for conn in connections:
        source = node_lookup.get(conn.get("from"))
        target = node_lookup.get(conn.get("to"))
        if not source or not target:
            continue
        sx = source["x"] * CANVAS_WIDTH
        sy = source["y"] * CANVAS_HEIGHT
        tx = target["x"] * CANVAS_WIDTH
        ty = target["y"] * CANVAS_HEIGHT
        ctrl_dx = (tx - sx) * 0.4
        path = (
            f"M {sx:.2f} {sy:.2f} "
            f"C {sx + ctrl_dx:.2f} {sy - 40:.2f}, "
            f"{tx - ctrl_dx:.2f} {ty + 40:.2f}, "
            f"{tx:.2f} {ty:.2f}"
        )
        path_html.append(f"<path d=\"{path}\" />")

    node_cards = []
    for node in nodes:
        icon_svg = _render_svg_icon(node.get("icon"), size=48)
        node_cards.append(
            f"""
            <div class="flow-node flow-size-{node.get('size', 'medium')}" style="left:{node['x']*100:.2f}%; top:{node['y']*100:.2f}%;">
                <div class="node-icon">{icon_svg}</div>
                <div class="node-label">{escape(node.get('label', ''))}</div>
            </div>
            """
        )

    svg = f"""
        <svg class="flow-svg" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" preserveAspectRatio="none">
            <defs>
                <linearGradient id="flowStroke" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="rgba(149,114,255,0.3)"/>
                    <stop offset="65%" stop-color="rgba(149,114,255,0.15)"/>
                    <stop offset="100%" stop-color="rgba(149,114,255,0.05)"/>
                </linearGradient>
                <marker id="flowArrow" markerWidth="12" markerHeight="12" refX="11" refY="5.5" orient="auto">
                    <path d="M1,1 L11,5.5 L1,10" fill="rgba(149,114,255,0.45)"/>
                </marker>
            </defs>
            {''.join(path_html)}
        </svg>
    """
    return f"""
        <div class="flowchart-area">
            {svg}
            <div class="flow-nodes">
                {''.join(node_cards)}
            </div>
        </div>
    """


def generate_modern_hero(
    generator: BaseGenerator,
    headline: str,
    subheadline: Optional[str] = None,
    eyebrow: Optional[str] = None,
    highlights: Optional[List[str]] = None,
    highlight_tiles: Optional[List[Dict[str, str]]] = None,
    flow_nodes: Optional[List[Dict[str, Any]]] = None,
    flow_connections: Optional[List[Dict[str, str]]] = None,
    freeform_canvas: Optional[str] = None,
    stats: Optional[List[Dict[str, str]]] = None,
    cta: Optional[str] = None,
    background_variant: str = "light",
    visual_description: Optional[str] = None,
) -> str:
    """Produce an open hero layout with generous whitespace."""
    background_class = "hero-light" if background_variant == "light" else "hero-dark"
    visual_desc = (visual_description or "").lower()
    curved_flow = "hero-flow-curved" if "curved arrow" in visual_desc or "curved flow" in visual_desc else ""
    constellation_flow = (
        "hero-flow-constellation"
        if any(keyword in visual_desc for keyword in ["constellation", "floating arc", "open orbit", "s-curve"])
        else ""
    )
    glass_mode = "hero-glass" if "glass" in visual_desc or "glassmorphism" in visual_desc else ""
    warm_palette = (
        "hero-warm"
        if any(keyword in visual_desc for keyword in ["warm", "sunrise", "amber", "gold", "golden", "yellow", "saffron", "scarlet", "red"])
        else ""
    )
    ribbon_collage = any(keyword in visual_desc for keyword in ["ribbon", "collage", "bezier"])
    hero_classes = " ".join(
        cls for cls in [background_class, curved_flow, constellation_flow, glass_mode, warm_palette] if cls
    )
    collage_html = ""
    flowchart_html = ""
    freeform_html = ""
    if freeform_canvas:
        freeform_html = f"<div class='freeform-canvas'>{freeform_canvas}</div>"
    if ribbon_collage and not flow_nodes and not freeform_canvas:
        panel_data = _extract_panel_data(highlights, highlight_tiles)
        collage_html = _render_ribbon_collage(panel_data)
    elif not freeform_canvas:
        flowchart_html = _render_flowchart(flow_nodes, flow_connections)
    highlight_html = ""
    if not flow_nodes and not collage_html and not freeform_canvas:
        highlight_html = (
            _render_tile_flow(highlight_tiles)
            if highlight_tiles
            else _render_list(highlights)
        )
    elif highlights:
        highlight_html = _render_list(highlights)
    stats_html = _render_stats(stats)
    cta_html = f"<div class='cta'>{cta}</div>" if cta else ""
    html = f"""
    <div class="hero {hero_classes}">
        <div class="halo"></div>
        <div class="hero-header">
            {f"<div class='eyebrow'>{eyebrow}</div>" if eyebrow else ''}
            <div class="headline">{headline}</div>
            {f"<div class='subhead'>{subheadline}</div>" if subheadline else ''}
        </div>
        <div class="hero-body">
            {freeform_html}
            {collage_html}
            {flowchart_html}
            {highlight_html}
            {cta_html}
        </div>
        {stats_html}
    </div>
    """
    css = """
        body { background: #f3f4f6; padding: 80px; font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif; }
        .hero { width: 1500px; min-height: 720px; border-radius: 48px; padding: 72px; position: relative; overflow: hidden; color: #1C1D29; box-shadow: 0 35px 140px rgba(15,15,40,0.12), inset 0 1px 0 rgba(255,255,255,0.6); background: #fff; }
        .hero-glass { background: rgba(255,255,255,0.75); backdrop-filter: blur(18px); border: 1px solid rgba(255,255,255,0.4); }
        .hero-dark { background: linear-gradient(145deg, #160b2e, #27123f); color: #f7f5ff; }
        .hero-warm { background: linear-gradient(135deg, #fff8ec, #ffe7c1); color: #2f1a00; }
        .hero .halo { position: absolute; width: 1200px; height: 1200px; top: -320px; left: -240px; background: radial-gradient(circle at 30% 25%, rgba(213,196,255,0.55), transparent 55%); pointer-events: none; }
        .hero-dark .halo { background: radial-gradient(circle at 40% 20%, rgba(120,97,204,0.65), transparent 60%); }
        .hero-warm .halo { background: radial-gradient(circle at 20% 20%, rgba(255,215,141,0.75), rgba(255,247,230,0.3) 45%, transparent 65%); }
        .hero-header { position: relative; z-index: 2; }
        .eyebrow { text-transform: uppercase; letter-spacing: 0.24em; font-size: 13px; color: #7a7f99; margin-bottom: 18px; }
        .hero-dark .eyebrow { color: #c5c1ff; }
        .hero-warm .eyebrow { color: #c4530e; }
        .headline { font-size: 64px; font-weight: 600; letter-spacing: -0.025em; max-width: 900px; }
        .subhead { margin-top: 16px; max-width: 720px; font-size: 24px; color: #414555; }
        .hero-dark .subhead { color: #d4d0ff; }
        .hero-warm .subhead { color: #6e3510; }
        .hero-body { position: relative; z-index: 2; margin-top: 36px; }
        .freeform-canvas { position: relative; width: 100%; margin-bottom: 32px; }
        .hero-dark .freeform-canvas { color: inherit; }
        .freeform-canvas .canvas-chip { background: rgba(255,255,255,0.9); border-radius: 28px; padding: 18px 32px; min-height: 72px; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 18px 50px rgba(15,15,40,0.12); font-weight: 600; letter-spacing: -0.01em; color: #1F1F29; border: 1px solid rgba(0,0,0,0.04); text-align: center; }
        .hero-dark .freeform-canvas .canvas-chip { background: rgba(20,17,30,0.85); border-color: rgba(255,255,255,0.12); color: #F5F2FF; }
        .hero-warm .freeform-canvas .canvas-chip { background: rgba(255,249,239,0.97); border-color: rgba(255,191,120,0.45); color: #4c2000; }
        .ribbon-area { position: relative; width: 100%; height: 320px; margin-bottom: 28px; }
        .hero-dark .ribbon-area { opacity: 0.95; }
        .ribbon-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
        .ribbon-svg path:first-child { filter: drop-shadow(0 20px 50px rgba(255,141,84,0.35)); }
        .ribbon-glyph { fill: rgba(255,255,255,0.8); stroke: rgba(0,0,0,0.04); }
        .hero-dark .ribbon-glyph { fill: rgba(255,255,255,0.35); }
        .ribbon-panels { position: absolute; inset: 0; pointer-events: none; }
        .ribbon-panel { position: absolute; transform: translate(-50%, -50%); background: rgba(255,255,255,0.85); border-radius: 30px; padding: 18px 22px; min-width: 220px; box-shadow: 0 25px 60px rgba(255,138,76,0.25); border: 1px solid rgba(255,255,255,0.4); pointer-events: auto; }
        .hero-dark .ribbon-panel { background: rgba(19,15,33,0.85); border-color: rgba(255,255,255,0.15); color: #f7f5ff; box-shadow: 0 25px 60px rgba(8,8,24,0.65); }
        .hero-warm .ribbon-panel { background: rgba(255,249,239,0.9); border-color: rgba(255,191,120,0.35); color: #3c1d00; }
        .ribbon-icon svg { width: 42px; height: 42px; }
        .ribbon-label { font-size: 18px; font-weight: 600; letter-spacing: -0.01em; margin-top: 10px; }
        .flowchart-area { position: relative; width: 100%; height: 360px; margin-bottom: 32px; }
        .hero-dark .flowchart-area { margin-bottom: 28px; }
        .flowchart-area::after { content: ''; position: absolute; inset: 40px 80px; border-radius: 40% 60% 45% 55%; border: 1px solid rgba(149,114,255,0.08); pointer-events: none; }
        .flow-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
        .flow-svg path { fill: none; stroke: url(#flowStroke); stroke-width: 3; marker-end: url(#flowArrow); }
        .hero-dark .flow-svg path { stroke: rgba(255,255,255,0.3); marker-end: url(#flowArrow); }
        .hero-warm .flow-svg path { stroke: rgba(255,159,64,0.45); }
        .flow-nodes { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
        .flow-node { position: absolute; transform: translate(-50%, -50%); background: rgba(249,248,255,0.92); border-radius: 28px; padding: 18px 22px; border: 1px solid rgba(121,120,148,0.14); box-shadow: 0 25px 60px rgba(54,48,84,0.16); min-width: 200px; max-width: 280px; pointer-events: auto; }
        .hero-dark .flow-node { background: rgba(17,13,35,0.85); border-color: rgba(255,255,255,0.12); box-shadow: 0 25px 70px rgba(4,4,12,0.8); color: #F6F2FF; }
        .hero-warm .flow-node { background: rgba(255,250,236,0.95); border-color: rgba(255,191,120,0.5); box-shadow: 0 25px 70px rgba(255,153,51,0.25); color: #3c1d00; }
        .flow-node .node-icon { margin-bottom: 10px; }
        .flow-node .node-icon svg { width: 44px; height: 44px; }
        .flow-node .node-label { font-size: 18px; font-weight: 600; letter-spacing: -0.01em; color: #1F1F2D; }
        .hero-dark .flow-node .node-label { color: #F5F2FF; }
        .hero-warm .flow-node .node-label { color: #5c2100; }
        .flow-size-small { min-width: 180px; max-width: 210px; }
        .flow-size-large { min-width: 260px; max-width: 320px; padding: 22px 26px; }
        .hero-body ul { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 12px; }
        .hero-body li { background: rgba(121,120,148,0.08); border-radius: 999px; padding: 10px 18px; font-size: 15px; font-weight: 500; color: #3A3B47; }
        .hero-dark .hero-body li { background: rgba(255,255,255,0.08); color: #EEE6FF; }
        .hero-warm .hero-body li { background: rgba(255,196,120,0.22); color: #7b3610; }
        .tile-flow { display: flex; flex-wrap: wrap; gap: 18px; align-items: stretch; margin-top: 8px; position: relative; z-index: 2; }
        .hero-flow-curved .tile-flow { padding: 24px 0; }
        .hero-flow-curved .tile-flow::before { content: ''; position: absolute; width: 75%; height: 200px; top: -10px; left: 12%; border-radius: 60%/70%; border: 2px solid rgba(124,58,237,0.18); border-color: transparent transparent rgba(124,58,237,0.25) rgba(124,58,237,0.1); }
        .hero-flow-curved .tile-flow::after { content: ''; position: absolute; right: 8%; top: 60px; width: 18px; height: 18px; border-left: 2px solid rgba(124,58,237,0.4); border-bottom: 2px solid rgba(124,58,237,0.4); transform: rotate(-45deg); }
        .hero-flow-constellation .tile-flow { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px,1fr)); gap: 32px 42px; justify-items: center; padding: 24px 12px 12px; min-height: 260px; }
        .hero-flow-constellation .tile-flow::before { content: ''; position: absolute; width: 82%; height: 260px; left: 9%; top: 6px; border-radius: 60% 40% 55% 45% / 55% 60% 40% 45%; border: 2px solid rgba(124,58,237,0.14); filter: blur(0.1px); pointer-events: none; }
        .hero-flow-constellation .tile-flow::after { content: ''; position: absolute; width: 120px; height: 120px; right: 12%; bottom: 12px; border: 1.5px dashed rgba(124,58,237,0.25); border-radius: 45% 55% 50% 50%; transform: rotate(12deg); opacity: 0.7; }
        .tile { position: relative; background: rgba(121,120,148,0.08); border: 1px solid rgba(121,120,148,0.15); border-radius: 22px; padding: 16px 18px; min-width: 170px; max-width: 220px; display: flex; flex-direction: column; gap: 8px; }
        .hero-flow-constellation .tile { border-radius: 30px; padding: 20px 22px; min-width: 210px; max-width: 240px; box-shadow: 0 25px 70px rgba(54,48,84,0.08); background: rgba(249,248,255,0.95); border-color: rgba(121,120,148,0.12); }
        .hero-dark.hero-flow-constellation .tile { background: rgba(255,255,255,0.06); box-shadow: 0 20px 60px rgba(4,4,12,0.55); }
        .hero-dark .tile { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15); color: #EEE6FF; }
        .hero-warm .tile { background: rgba(255,250,236,0.92); border-color: rgba(255,191,120,0.4); color: #5c2100; }
        .tile::after { content: ''; position: absolute; top: 50%; right: -36px; width: 42px; height: 2px; background: linear-gradient(90deg, rgba(124,58,237,0.2), rgba(124,58,237,0.05)); }
        .hero-flow-constellation .tile::after { display: none; }
        .hero-flow-constellation .tile::before { content: ''; position: absolute; width: 68px; height: 68px; border-radius: 999px; border: 1px solid rgba(149,114,255,0.15); top: -26px; left: -18px; opacity: 0.6; }
        .hero-flow-constellation .tile:nth-child(odd)::before { border-style: dashed; opacity: 0.35; }
        .tile:last-child::after { display: none; }
        .tile-icon svg { width: 46px; height: 46px; }
        .tile-label { font-size: 15px; font-weight: 600; color: #2D2E36; }
        .hero-dark .tile-label { color: #F5F0FF; }
        .hero-warm .tile-label { color: #5c2100; }
        .cta { margin-top: 24px; display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: #7C3AED; }
        .hero-dark .cta { color: #F5E1FF; }
        .hero-warm .cta { color: #c2410c; }
        .cta::after { content: '→'; font-size: 20px; }
        .stats { margin-top: 48px; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 16px; }
        .stat { background: #f9f8ff; border-radius: 24px; padding: 16px 20px; border: 1px solid rgba(134,114,175,0.12); }
        .hero-dark .stat { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15); color: #F7F2FF; }
        .hero-warm .stat { background: #fff6dd; border-color: rgba(255,191,120,0.45); color: #5b2600; }
        .stat span { font-size: 12px; text-transform: uppercase; letter-spacing: 0.18em; color: #9B9EAF; }
        .hero-dark .stat span { color: #CFC3F4; }
        .hero-warm .stat span { color: #c47a0c; }
        .stat strong { display: block; margin-top: 6px; font-size: 24px; font-weight: 600; letter-spacing: -0.015em; }
        .hero-warm .stat strong { color: #6a2a00; }
    """
    return generator._wrap_html(html, css)


def generate_modern_hero_triptych(
    generator: BaseGenerator,
    headline: str,
    subheadline: Optional[str],
    columns: List[Dict[str, Any]],
    stats: Optional[List[Dict[str, str]]] = None,
    eyebrow: Optional[str] = None,
) -> str:
    """Render the triptych hero layout (manual → templates → generated)."""
    if len(columns) < 3:
        raise ValueError("modern hero triptych requires at least 3 columns")

    column_html = "".join(
        f"""
        <div class='panel'>
            {_render_svg_icon(col.get('icon'))}
            <div class='panel-title'>{col.get('title', '')}</div>
            {_render_list(col.get('items'))}
        </div>
        """
        for col in columns[:3]
    )
    stats_html = _render_stats(stats)
    html = f"""
    <div class='hero hero-triptych'>
        <svg class='soft-orbit' viewBox='0 0 900 900' aria-hidden='true'>
            <circle cx='450' cy='450' r='360' fill='url(#orbitGrad)' />
            <circle cx='450' cy='450' r='310' fill='none' stroke='rgba(120,118,141,0.12)' stroke-width='1.2' />
            <circle cx='450' cy='450' r='370' fill='none' stroke='rgba(120,118,141,0.07)' stroke-width='1' />
            <circle cx='170' cy='170' r='5' fill='#E0D0FF' />
            <circle cx='720' cy='260' r='5' fill='#CABAF6' />
            <circle cx='700' cy='640' r='4' fill='#DDD6FE' />
        </svg>
        <svg class='defs' width='0' height='0'><defs><radialGradient id='orbitGrad' r='0.7'><stop offset='0' stop-color='#E4D7FF' stop-opacity='0.85'/><stop offset='0.5' stop-color='#D5C8FA' stop-opacity='0.35'/><stop offset='1' stop-color='rgba(255,255,255,0)'/></radialGradient></defs></svg>
        <div class='hero-header'>
            {f"<div class='eyebrow'>{eyebrow}</div>" if eyebrow else ''}
            <div class='headline'>{headline}</div>
            {f"<div class='subhead'>{subheadline}</div>" if subheadline else ''}
        </div>
        <div class='panels'>
            {column_html}
        </div>
        {stats_html}
    </div>
    """
    css = """
        body { background: #f5f6fb; padding: 80px; font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif; }
        .hero-triptych { width: 1500px; min-height: 860px; border-radius: 48px; background: #ffffff; padding: 72px; position: relative; overflow: hidden; color: #1F1F2B; box-shadow: 0 35px 140px rgba(15,15,40,0.12), inset 0 1px 0 rgba(255,255,255,0.6); }
        .soft-orbit { position: absolute; width: 1200px; height: 1200px; top: -240px; right: -220px; pointer-events: none; }
        .hero-header { position: relative; z-index: 2; margin-bottom: 48px; }
        .eyebrow { text-transform: uppercase; letter-spacing: 0.2em; font-size: 13px; color: #8A8FA2; margin-bottom: 14px; }
        .headline { font-size: 60px; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 18px; }
        .subhead { max-width: 780px; font-size: 22px; color: #4B4E5F; }
        .panels { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 24px; position: relative; z-index: 2; }
        .panel { border-radius: 32px; padding: 32px; background: linear-gradient(180deg, #fcfcff, #f5f2fb); border: 1px solid rgba(21,24,36,0.06); box-shadow: 0 20px 60px rgba(44,44,76,0.08); min-height: 320px; display: flex; flex-direction: column; gap: 18px; }
        .panel:nth-child(2) { background: linear-gradient(180deg, #f7f2ff, #ece6ff); border-color: rgba(134,114,175,0.18); }
        .icon { width: 64px; height: 64px; }
        .panel-title { font-size: 20px; font-weight: 600; letter-spacing: -0.01em; color: #2D2E36; }
        .panel ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; font-size: 16px; color: #4B4E5F; }
        .panel ul li::before { content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #A78BFA; margin-right: 12px; position: relative; top: -1px; }
        .stats { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 18px; margin-top: 48px; position: relative; z-index: 2; }
        .stats .stat { background: #f9f8ff; border-radius: 24px; padding: 18px 24px; border: 1px solid rgba(134,114,175,0.12); }
        .stat span { font-size: 12px; text-transform: uppercase; letter-spacing: 0.2em; color: #9D9FB5; }
        .stat strong { display: block; margin-top: 6px; font-size: 22px; font-weight: 600; letter-spacing: -0.01em; color: #2C2F3C; }
    """
    return generator._wrap_html(html, css)
