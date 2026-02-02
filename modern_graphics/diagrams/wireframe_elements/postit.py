"""Post-it / sticky note wireframe element: tilted shape with folded corner and shadow.

Use as a scene element via ELEMENT_REGISTRY (type "postit"). Composable in a flow
with other postits and optional "connector" elements.
"""

import math
from typing import List, Optional, Tuple

from .config import WireframeConfig


# Default sticky-note colors when not overridden by props
_DEFAULT_FILL = "#fff59d"
_DEFAULT_BORDER = "#d4a84b"
_DEFAULT_FOLD = "#f5e6a3"
_DEFAULT_TEXT = "#5d4037"
_DEFAULT_SHADOW = "rgba(0,0,0,0.12)"


def render_postit_at(
    config: WireframeConfig,
    x: float,
    y: float,
    width: int = 140,
    height: int = 100,
    label: str = "Note",
    rotation_deg: float = -3,
    fill: Optional[str] = None,
    border: Optional[str] = None,
    fold_color: Optional[str] = None,
    text_color: Optional[str] = None,
) -> str:
    """Render a single post-it (tilted rect with folded corner and shadow) at (x, y).

    Returns an SVG <g> fragment for scene composition. Uses config.colors for
    text if text_color not provided; fill/border/fold default to sticky yellow/tan.
    """
    fill = fill or _DEFAULT_FILL
    border = border or _DEFAULT_BORDER
    fold_color = fold_color or _DEFAULT_FOLD
    text_color = text_color or getattr(config.colors, "text_primary", _DEFAULT_TEXT)

    cx = width / 2
    cy = height / 2
    rx = 6
    fold_size = 14

    # Fold triangle: clips top-right corner (drawn first so body can overlap edge)
    fold_path = (
        f"M {width - fold_size} 0 "
        f"L {width} 0 L {width} {fold_size} Z"
    )

    # Body: rounded rect (full rect then we describe the fold cut)
    # Simple approach: one rect with large rx, then overlay fold triangle
    body_rect = f'<rect x="0" y="0" width="{width}" height="{height}" rx="{rx}" ry="{rx}" fill="{fill}" stroke="{border}" stroke-width="1"/>'

    # Fold triangle (darker/lighter to suggest fold)
    fold_tri = f'<path d="{fold_path}" fill="{fold_color}" stroke="{border}" stroke-width="1"/>'

    # Shadow: offset drop shadow via filter (use inline filter id that scene provides, or define one)
    # Scene's get_filter_defs has softShadow, cardShadow. Use cardShadow for post-it lift.
    shadow_filter = 'filter="url(#cardShadow)"'
    g_open = f'<g class="postit" transform="translate({x},{y}) rotate({rotation_deg},{cx},{cy})" {shadow_filter}>'
    # Text: centered, with padding so it doesn't hit the fold
    font = config.font_family
    pad = 12
    text_x = width / 2
    text_y = height / 2
    # Single or multi-line label
    lines = [t.strip() for t in label.replace("\\n", "\n").split("\n") if t.strip()]
    if not lines:
        lines = ["Note"]
    font_size = min(14, max(10, 100 // len(lines)))
    line_height = font_size + 4
    total_h = (len(lines) - 1) * line_height
    start_y = text_y - total_h / 2 + font_size * 0.35

    text_parts = []
    for i, line in enumerate(lines):
        dy = start_y + i * line_height
        text_parts.append(
            f'<text x="{text_x}" y="{dy}" font-family="{font}" font-size="{font_size}" '
            f'fill="{text_color}" text-anchor="middle">{line}</text>'
        )
    text_svg = "\n    ".join(text_parts)

    return f"""
  {g_open}
    {body_rect}
    {fold_tri}
    {text_svg}
  </g>"""


def render_connector_at(
    config: WireframeConfig,
    x: float,
    y: float,
    to_x: float,
    to_y: float,
    stroke: Optional[str] = None,
    stroke_width: float = 2,
    arrow_size: float = 8,
    waypoints: Optional[List[Tuple[float, float]]] = None,
) -> str:
    """Render an arrow connector from (x, y) to (to_x, to_y) for flow diagrams.

    If waypoints is provided, the path goes start -> waypoint[0] -> ... -> end
    (Mermaid-style orthogonal/step routing). Otherwise a single straight line.
    Returns an SVG <g> fragment.
    """
    stroke = stroke or getattr(config.colors, "border_medium", "#d2d2d7")

    if waypoints:
        pts: List[Tuple[float, float]] = [(x, y)] + list(waypoints) + [(to_x, to_y)]
        seg_start_x, seg_start_y = pts[-2][0], pts[-2][1]
    else:
        seg_start_x, seg_start_y = x, y

    dx = to_x - seg_start_x
    dy = to_y - seg_start_y
    angle = math.atan2(dy, dx)
    shorten = arrow_size * 1.2
    end_x = to_x - shorten * math.cos(angle)
    end_y = to_y - shorten * math.sin(angle)

    ax1 = to_x - arrow_size * math.cos(angle - 0.4)
    ay1 = to_y - arrow_size * math.sin(angle - 0.4)
    ax2 = to_x - arrow_size * math.cos(angle + 0.4)
    ay2 = to_y - arrow_size * math.sin(angle + 0.4)
    head = f'<path d="M {to_x} {to_y} L {ax1} {ay1} L {ax2} {ay2} Z" fill="{stroke}" stroke="none"/>'

    if waypoints:
        path_pts = [(x, y)] + list(waypoints) + [(end_x, end_y)]
        d = "M " + " L ".join(f"{px} {py}" for px, py in path_pts)
        line = f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        line = f'<line x1="{x}" y1="{y}" x2="{end_x}" y2="{end_y}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"/>'

    return f"""
  <g class="connector">
    {line}
    {head}
  </g>"""
