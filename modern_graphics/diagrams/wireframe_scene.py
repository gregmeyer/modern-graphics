"""Scene-spec wireframe renderer: compose wireframe elements from a declarative spec.

Spec format:
    {
        "width": 800,
        "height": 520,
        "elements": [
            { "type": "browser_window", "x": 0, "y": 0, "width": 800, "height": 520, "props": { "url": "app.example.com" } },
            { "type": "modal", "x": 260, "y": 120, "width": 280, "height": 320, "props": { "title": "Support Request", "fields": [{"label": "Subject"}, {"label": "Description", "textarea": true}] } }
        ]
    }

Element types and props (see ELEMENT_REGISTRY and adapter docstrings):
    browser_window, browser_chrome, modal, modal_overlay, chat_panel, content_card,
    app_header, success_toast, status_pill, ticket_status_flow, skeleton_lines,
    transaction (credit-card-style transaction with icons + merchant, amount, date),
    postit (tilted sticky note with folded corner; props: label, rotation_deg, fill, border),
    connector (arrow from x,y to props to_x, to_y; for flow diagrams).

Post-it flow layouts: use build_postit_flow_elements(labels, layout, width, height)
with layout one of "linear", "zigzag", "vertical", "arc", "outline", "orgchart",
"fishbone", "mindmap". For outline pass optional outline_levels; for orgchart/fishbone/
mindmap pass structure= (dict). Presets: postit_flow, postit_flow_zigzag, postit_flow_vertical,
postit_flow_arc, postit_flow_outline, postit_flow_orgchart, postit_flow_fishbone, postit_flow_mindmap.

Using other element types: call compute_flow_layout(...) to get {"nodes": [...], "connectors": [...]}
(position/dimension data only), then build scene elements with any ELEMENT_REGISTRY type via
build_flow_elements(..., node_type="content_card", node_props_fn=lambda n: {"title": n["label"]}).
"""

import math
from typing import Any, Callable, Dict, List, Optional, Union

from .wireframe_elements.config import WireframeConfig
from .wireframe_elements.browser import render_browser_chrome, render_browser_window
from .wireframe_elements.forms import render_modal, render_modal_overlay
from .wireframe_elements.chat import render_chat_panel
from .wireframe_elements.cards import render_content_card, render_app_header, render_skeleton_lines
from .wireframe_elements.feedback import (
    render_success_toast,
    render_status_pill,
    render_ticket_status_flow,
)
from .transaction_icons_svg import render_transaction_at
from .wireframe_elements.postit import render_postit_at, render_connector_at


def _el(config: WireframeConfig, element: Dict[str, Any], **defaults: Any) -> str:
    """Call builder with element x, y, width, height, and merged props."""
    x = element.get("x", 0)
    y = element.get("y", 0)
    width = element.get("width")
    height = element.get("height")
    props = dict(element.get("props", {}), **defaults)
    if width is not None:
        props.setdefault("width", width)
    if height is not None:
        props.setdefault("height", height)
    return x, y, props


def _adapt_browser_window(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width")
    h = p.get("height")
    return render_browser_window(
        config, x=x, y=y, width=w, height=h,
        url=p.get("url", "app.example.com"),
        content_bg=p.get("content_bg"),
    )


def _adapt_browser_chrome(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width")
    return render_browser_chrome(config, x=x, y=y, width=w, url=p.get("url", "app.example.com"))


def _adapt_modal(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width", 280)
    h = p.get("height", 320)
    return render_modal(
        config, x=x, y=y, width=w, height=h,
        title=p.get("title", "Modal Title"),
        fields=p.get("fields"),
        submit_text=p.get("submit_text", "Submit"),
    )


def _adapt_modal_overlay(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width")
    h = p.get("height")
    if w is None or h is None:
        return ""
    return render_modal_overlay(config, x=x, y=y, width=w, height=h, opacity=p.get("opacity", 0.25))


def _adapt_chat_panel(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width", 320)
    h = p.get("height", 400)
    return render_chat_panel(
        config, x=x, y=y, width=w, height=h,
        messages=p.get("messages"),
        inline_card=p.get("inline_card"),
        action_buttons=p.get("action_buttons"),
        quick_actions=p.get("quick_actions"),
        header_title=p.get("header_title", "Help"),
        show_active_status=p.get("show_active_status", True),
    )


def _adapt_content_card(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width", 200)
    h = p.get("height", 120)
    return render_content_card(
        config, x=x, y=y, width=w, height=h,
        line_widths=p.get("line_widths"),
        show_divider=p.get("show_divider", False),
        opacity=p.get("opacity", 1.0),
    )


def _adapt_app_header(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width", 400)
    h = p.get("height", 45)
    return render_app_header(config, x=x, y=y, width=w, height=h)


def _adapt_success_toast(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    return render_success_toast(
        config, x=x, y=y,
        title=p.get("title", "Success"),
        subtitle=p.get("subtitle"),
        width=p.get("width", 260),
        height=p.get("height", 56),
    )


def _adapt_status_pill(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    return render_status_pill(
        config, x=x, y=y,
        text=p.get("text", "Status"),
        status=p.get("status", "neutral"),
        icon=p.get("icon", True),
    )


def _adapt_ticket_status_flow(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    return render_ticket_status_flow(
        config, x=x, y=y,
        statuses=p.get("statuses"),
        active_index=p.get("active_index", 1),
        ticket_id=p.get("ticket_id", "#48291"),
        estimated_time=p.get("estimated_time", "24-48 hours"),
    )


def _adapt_skeleton_lines(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    return render_skeleton_lines(
        config, x=x, y=y,
        widths=p.get("widths", [0.9, 0.7, 0.5]),
        line_height=p.get("line_height", 8),
        gap=p.get("gap", 10),
    )


def _adapt_transaction(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width", 360)
    h = p.get("height", 200)
    c = config.colors
    return render_transaction_at(
        x=x,
        y=y,
        width=w,
        height=h,
        merchant=p.get("merchant", "Coffee Shop"),
        amount=p.get("amount", "$4.50"),
        date=p.get("date", "Today"),
        accent=c.accent_blue,
        text_primary=c.text_primary,
        text_secondary=c.text_secondary,
        surface=c.surface_secondary,
        border=c.border_light,
    )


def _adapt_postit(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    w = p.get("width", 140)
    h = p.get("height", 100)
    c = config.colors
    return render_postit_at(
        config,
        x=x,
        y=y,
        width=w,
        height=h,
        label=p.get("label", "Note"),
        rotation_deg=p.get("rotation_deg", -3),
        fill=p.get("fill", c.surface_secondary),
        border=p.get("border", c.border_medium),
        fold_color=p.get("fold_color", c.surface_tertiary),
        text_color=p.get("text_color", c.text_primary),
    )


def _adapt_connector(config: WireframeConfig, element: Dict[str, Any]) -> str:
    x, y, p = _el(config, element)
    to_x = p.get("to_x", x + 60)
    to_y = p.get("to_y", y)
    waypoints = p.get("waypoints")
    return render_connector_at(
        config,
        x=x,
        y=y,
        to_x=to_x,
        to_y=to_y,
        stroke=p.get("stroke"),
        stroke_width=p.get("stroke_width", 2),
        arrow_size=p.get("arrow_size", 8),
        waypoints=waypoints,
    )


ELEMENT_REGISTRY: Dict[str, Callable[[WireframeConfig, Dict[str, Any]], str]] = {
    "browser_window": _adapt_browser_window,
    "browser_chrome": _adapt_browser_chrome,
    "modal": _adapt_modal,
    "modal_overlay": _adapt_modal_overlay,
    "chat_panel": _adapt_chat_panel,
    "content_card": _adapt_content_card,
    "app_header": _adapt_app_header,
    "success_toast": _adapt_success_toast,
    "status_pill": _adapt_status_pill,
    "ticket_status_flow": _adapt_ticket_status_flow,
    "skeleton_lines": _adapt_skeleton_lines,
    "transaction": _adapt_transaction,
    "postit": _adapt_postit,
    "connector": _adapt_connector,
}


def compute_flow_layout(
    labels: Optional[List[str]] = None,
    layout: str = "linear",
    width: int = 1100,
    height: int = 280,
    node_width: int = 120,
    node_height: int = 88,
    gap: int = 24,
    outline_levels: Optional[List[int]] = None,
    structure: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compute flow layout only: node positions/dimensions and connector segments.

    Returns {"nodes": [...], "connectors": [...]}. Each node has x, y, width, height,
    label, rotation_deg. Each connector has from_x, from_y, to_x, to_y, waypoints.
    Use with build_flow_elements(node_type=..., node_props_fn=...) to get scene
    elements for any ELEMENT_REGISTRY type (postit, content_card, etc.).
    Same parameters as build_postit_flow_elements.
    """
    return _compute_flow_layout(
        labels=labels,
        layout=layout,
        width=width,
        height=height,
        node_width=node_width,
        node_height=node_height,
        gap=gap,
        outline_levels=outline_levels,
        structure=structure,
    )


def build_flow_elements(
    labels: Optional[List[str]] = None,
    layout: str = "linear",
    width: int = 1100,
    height: int = 280,
    node_width: int = 120,
    node_height: int = 88,
    gap: int = 24,
    outline_levels: Optional[List[int]] = None,
    structure: Optional[Dict[str, Any]] = None,
    node_type: str = "postit",
    node_props_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    connector_type: str = "connector",
) -> List[Dict[str, Any]]:
    """Build flow elements using any registered node type (postit, content_card, etc.).

    Layout is computed the same as compute_flow_layout; nodes are emitted as
    node_type with props from node_props_fn(node). If node_props_fn is None and
    node_type is "postit", defaults to {"label": node["label"], "rotation_deg": ...}.
    Connectors are always connector_type (default "connector"). Returns list of
    element dicts (nodes first, then connectors) for use in a scene spec.
    """
    layout_data = compute_flow_layout(
        labels=labels,
        layout=layout,
        width=width,
        height=height,
        node_width=node_width,
        node_height=node_height,
        gap=gap,
        outline_levels=outline_levels,
        structure=structure,
    )
    nodes = layout_data["nodes"]
    connectors = layout_data["connectors"]
    if node_props_fn is None and node_type == "postit":
        node_props_fn = lambda n: {"label": n["label"], "rotation_deg": n.get("rotation_deg", 0)}
    if node_props_fn is None:
        node_props_fn = lambda n: {}
    elements: List[Dict[str, Any]] = []
    for n in nodes:
        elements.append({
            "type": node_type,
            "x": round(n["x"]),
            "y": round(n["y"]),
            "width": n["width"],
            "height": n["height"],
            "props": node_props_fn(n),
        })
    for c in connectors:
        conn_props: Dict[str, Any] = {"to_x": round(c["to_x"]), "to_y": round(c["to_y"])}
        if c.get("waypoints") is not None:
            conn_props["waypoints"] = c["waypoints"]
        elements.append({
            "type": connector_type,
            "x": round(c["from_x"]),
            "y": round(c["from_y"]),
            "props": conn_props,
        })
    return elements


def build_postit_flow_elements(
    labels: Optional[List[str]] = None,
    layout: str = "linear",
    width: int = 1100,
    height: int = 280,
    node_width: int = 120,
    node_height: int = 88,
    gap: int = 24,
    outline_levels: Optional[List[int]] = None,
    structure: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build postit + connector elements for a flow.

    For linear/zigzag/vertical/arc: pass labels (list of strings).
    For outline: pass labels and optional outline_levels (list of int, same length).
    For orgchart/fishbone/mindmap: pass structure (dict) and omit labels.

    Layouts:
        linear: Left-to-right, slight y stagger.
        zigzag: Left-to-right with nodes alternating top/bottom row.
        vertical: Stack top-to-bottom.
        arc: Nodes along bottom arc of an ellipse.
        outline: Hierarchical indented list (levels 0,1,2...).
        orgchart: Tree; structure = {label, children: [{label, children: [...]}, ...]}.
        fishbone: Spine + ribs; structure = {theme: str, causes_top: [str], causes_bottom: [str]}.
        mindmap: Center + branches; structure = {center: str, branches: [str]}.
    """
    return build_flow_elements(
        labels=labels,
        layout=layout,
        width=width,
        height=height,
        node_width=node_width,
        node_height=node_height,
        gap=gap,
        outline_levels=outline_levels,
        structure=structure,
        node_type="postit",
        node_props_fn=lambda n: {"label": n["label"], "rotation_deg": n.get("rotation_deg", 0)},
    )


def _compute_flow_layout(
    labels: Optional[List[str]] = None,
    layout: str = "linear",
    width: int = 1100,
    height: int = 280,
    node_width: int = 120,
    node_height: int = 88,
    gap: int = 24,
    outline_levels: Optional[List[int]] = None,
    structure: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Internal: return {"nodes": [...], "connectors": [...]} with layout data only."""
    nodes: List[Dict[str, Any]] = []
    connectors: List[Dict[str, Any]] = []
    pad = 20
    cx = node_width / 2
    cy = node_height / 2

    if layout in ("orgchart", "fishbone", "mindmap") and structure:
        nodes, connectors = _build_structured_layout_data(
            layout, structure, width, height, node_width, node_height, pad, gap, cx, cy
        )
        return {"nodes": nodes, "connectors": connectors}
    if labels is None:
        labels = []
    n = len(labels)
    if n == 0 and layout not in ("outline", "orgchart", "fishbone", "mindmap"):
        return {"nodes": [], "connectors": []}

    if layout == "linear":
        step = (width - 2 * pad - node_width) / max(n - 1, 1)
        for i, label in enumerate(labels):
            x = pad + i * step
            y = 50 + (8 if i % 2 == 0 else -8) * (i % 3)
            rot = -2 if i % 2 == 0 else 2
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": rot})
            if i < n - 1:
                from_x = x + node_width + gap // 2
                from_y = y + cy
                nx = pad + (i + 1) * step
                ny = 50 + (8 if (i + 1) % 2 == 0 else -8) * ((i + 1) % 3)
                to_x = nx + cx - gap // 2
                to_y = ny + cy
                connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
    elif layout == "zigzag":
        row_y_top = 30
        row_y_bottom = height - 30 - node_height
        step = (width - 2 * pad - node_width) / max(n - 1, 1)
        for i, label in enumerate(labels):
            x = pad + i * step
            y = row_y_top if i % 2 == 0 else row_y_bottom
            rot = -3 if i % 2 == 0 else 3
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": rot})
            if i < n - 1:
                from_x = x + node_width + gap // 2
                from_y = y + cy
                nx = pad + (i + 1) * step
                next_y = row_y_top if (i + 1) % 2 == 0 else row_y_bottom
                to_x = nx + cx - gap // 2
                to_y = next_y + cy
                connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
    elif layout == "vertical":
        step_y = (height - 2 * pad - node_height) / max(n - 1, 1)
        center_x = (width - node_width) / 2
        for i, label in enumerate(labels):
            x = center_x + (10 if i % 2 == 0 else -10)
            y = pad + i * step_y
            rot = 1 if i % 2 == 0 else -1
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": rot})
            if i < n - 1:
                from_x = x + cx
                from_y = y + node_height + gap // 2
                next_x = center_x + (10 if (i + 1) % 2 == 0 else -10)
                to_x = next_x + cx
                to_y = pad + (i + 1) * step_y - gap // 2
                connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
    elif layout == "arc":
        radius_x = (width - 2 * pad - node_width) / 2
        radius_y = (height - node_height) * 0.45
        center_x = width / 2 - cx
        center_y = height - 40 - node_height / 2
        positions: List[tuple] = []
        for i in range(n):
            t = i / max(n - 1, 1)
            angle = math.pi * 0.95 * (1 - t)
            x = center_x + radius_x * math.cos(angle) - cx
            y = center_y - radius_y * math.sin(angle) - cy
            positions.append((x, y))
        for i, label in enumerate(labels):
            x, y = positions[i]
            rot = -4 + (i % 3) * 3
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": rot})
            if i < n - 1:
                from_x = x + node_width * 0.85
                from_y = y + cy
                nx, ny = positions[i + 1]
                to_x = nx + node_width * 0.15
                to_y = ny + cy
                connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
    elif layout == "outline":
        levels = outline_levels if outline_levels is not None and len(outline_levels) == n else [0] * n
        indent_per_level = 48
        row_h = node_height + gap
        y = pad
        prev_x: Optional[float] = None
        prev_y: Optional[float] = None
        for i, label in enumerate(labels):
            lev = min(levels[i], 4)
            x = pad + lev * indent_per_level
            rot = -1 if i % 2 == 0 else 1
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": rot})
            if prev_x is not None and prev_y is not None:
                from_x = prev_x + cx
                from_y = prev_y + node_height
                to_x = x + cx
                to_y = y
                connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
            prev_x, prev_y = x, y
            y += row_h
    else:
        step = (width - 2 * pad - node_width) / max(n - 1, 1)
        for i, label in enumerate(labels):
            x = pad + i * step
            y = 50
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": -2})
            if i < n - 1:
                from_x = x + node_width + gap // 2
                from_y = y + cy
                to_x = pad + (i + 1) * step + cx - gap // 2
                to_y = y + cy
                connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
    return {"nodes": nodes, "connectors": connectors}


def _build_structured_layout_data(
    layout: str,
    structure: Dict[str, Any],
    width: int,
    height: int,
    node_width: int,
    node_height: int,
    pad: int,
    gap: int,
    cx: float,
    cy: float,
) -> tuple:
    """Return (nodes, connectors) for orgchart, fishbone, or mindmap."""
    nodes: List[Dict[str, Any]] = []
    connectors: List[Dict[str, Any]] = []

    if layout == "orgchart":
        row_h = node_height + gap
        flat: List[tuple] = []

        def collect(node: Dict, d: int, parent_ii: int) -> None:
            ii = len(flat)
            flat.append((node.get("label", "?"), d, parent_ii))
            for c in node.get("children", []):
                collect(c, d + 1, ii)
        collect(structure, 0, -1)
        by_depth: Dict[int, List[int]] = {}
        for i, (_, d, _) in enumerate(flat):
            by_depth.setdefault(d, []).append(i)
        positions: List[tuple] = [(-1.0, -1.0)] * len(flat)
        for depth in sorted(by_depth.keys()):
            indices = by_depth[depth]
            y = pad + depth * row_h
            nn = len(indices)
            for k, ii in enumerate(indices):
                x = pad + k * (width - 2 * pad - node_width) / max(nn - 1, 1)
                positions[ii] = (x, y)
        for i, (label, _, _) in enumerate(flat):
            x, y = positions[i]
            nodes.append({"x": x, "y": y, "width": node_width, "height": node_height, "label": label, "rotation_deg": -1})
        for i, (_, _, parent_ii) in enumerate(flat):
            if parent_ii < 0:
                continue
            child_x, child_y = positions[i]
            px, py = positions[parent_ii]
            from_x = px + cx
            from_y = py + node_height + gap // 2
            to_x = child_x + cx
            to_y = child_y - gap // 2
            connectors.append({"from_x": from_x, "from_y": from_y, "to_x": to_x, "to_y": to_y})
        return (nodes, connectors)

    if layout == "fishbone":
        theme = structure.get("theme", "Effect")
        causes_top = structure.get("causes_top", [])
        causes_bottom = structure.get("causes_bottom", [])
        spine_y = height / 2
        theme_x = width - pad - node_width
        nodes.append({
            "x": theme_x, "y": spine_y - node_height / 2,
            "width": node_width, "height": node_height, "label": theme, "rotation_deg": 0,
        })
        rib_len = 120
        for i, cause in enumerate(causes_top):
            t = (i + 1) / (len(causes_top) + 1)
            spine_x = pad + node_width + t * (width - 2 * pad - 2 * node_width)
            angle = -0.55
            ex = spine_x + rib_len * math.cos(angle)
            ey = spine_y - 50 - rib_len * math.sin(angle)
            to_x = ex + cx
            to_y = ey + node_height
            connectors.append({"from_x": spine_x, "from_y": spine_y, "to_x": to_x, "to_y": to_y})
            nodes.append({"x": ex, "y": ey, "width": node_width, "height": node_height, "label": cause, "rotation_deg": 2})
        for i, cause in enumerate(causes_bottom):
            t = (i + 1) / (len(causes_bottom) + 1)
            spine_x = pad + node_width + t * (width - 2 * pad - 2 * node_width)
            angle = 0.55
            ex = spine_x + rib_len * math.cos(angle)
            ey = spine_y + 50 + rib_len * math.sin(angle)
            to_x = ex + cx
            to_y = ey
            connectors.append({"from_x": spine_x, "from_y": spine_y, "to_x": to_x, "to_y": to_y})
            nodes.append({"x": ex, "y": ey, "width": node_width, "height": node_height, "label": cause, "rotation_deg": -2})
        return (nodes, connectors)

    if layout == "mindmap":
        center_label = structure.get("center", "Topic")
        branches = structure.get("branches", [])
        center_x = width / 2 - cx
        center_y = height / 2 - cy
        nodes.append({
            "x": center_x, "y": center_y,
            "width": node_width, "height": node_height, "label": center_label, "rotation_deg": 0,
        })
        nb = len(branches)
        radius = min(width, height) * 0.32
        for i, label in enumerate(branches):
            angle = 2 * math.pi * i / nb - math.pi / 2
            bx = center_x + cx + radius * math.cos(angle)
            by = center_y + cy + radius * math.sin(angle)
            to_x = center_x + cx + (radius - node_width * 0.6) * math.cos(angle)
            to_y = center_y + cy + (radius - node_width * 0.6) * math.sin(angle)
            connectors.append({
                "from_x": center_x + cx, "from_y": center_y + cy,
                "to_x": to_x, "to_y": to_y,
            })
            nodes.append({"x": bx - cx, "y": by - cy, "width": node_width, "height": node_height, "label": label, "rotation_deg": 0})
        return (nodes, connectors)

    return (nodes, connectors)


# Named scene presets: same content as custom spec (width, height, elements).
SCENE_PRESETS: Dict[str, Dict[str, Any]] = {
    "before": {
        "width": 400,
        "height": 360,
        "elements": [
            {"type": "browser_window", "x": 0, "y": 0, "width": 400, "height": 360, "props": {"url": "support.example.com"}},
            {"type": "modal_overlay", "x": 0, "y": 32, "width": 400, "height": 328, "props": {"opacity": 0.4}},
            {"type": "modal", "x": 90, "y": 80, "width": 220, "height": 200, "props": {"title": "Support Request", "fields": [{"label": "Subject"}, {"label": "Description", "textarea": True}], "submit_text": "Submit Ticket"}},
            {"type": "ticket_status_flow", "x": 40, "y": 308, "props": {"active_index": 1, "statuses": ["Open", "Pending", "Closed"]}},
        ],
    },
    "after": {
        "width": 400,
        "height": 360,
        "elements": [
            {"type": "browser_window", "x": 0, "y": 0, "width": 400, "height": 360, "props": {"url": "app.example.com"}},
            {"type": "chat_panel", "x": 240, "y": 32, "width": 160, "height": 328, "props": {"header_title": "Help", "messages": [{"text": "How can I help?", "is_user": False}, {"text": "Billing question", "is_user": True}], "inline_card": {"title": "Pro Plan", "subtitle": "$29/mo"}}},
            {"type": "success_toast", "x": 70, "y": 280, "props": {"title": "Message sent", "subtitle": "We'll reply soon"}},
        ],
    },
    "postit_flow": {
        "width": 1100,
        "height": 200,
        "elements": build_postit_flow_elements(
            ["Get bread", "Add spread", "Add fillings", "Add toppings", "Cut in half", "Plate", "Serve"],
            layout="linear",
            width=1100,
            height=200,
        ),
    },
    "postit_flow_zigzag": {
        "width": 1100,
        "height": 220,
        "elements": build_postit_flow_elements(
            ["Get bread", "Add spread", "Add fillings", "Add toppings", "Cut in half", "Plate", "Serve"],
            layout="zigzag",
            width=1100,
            height=220,
        ),
    },
    "postit_flow_vertical": {
        "width": 220,
        "height": 720,
        "elements": build_postit_flow_elements(
            ["Get bread", "Add spread", "Add fillings", "Add toppings", "Cut in half", "Plate", "Serve"],
            layout="vertical",
            width=220,
            height=720,
        ),
    },
    "postit_flow_arc": {
        "width": 1100,
        "height": 280,
        "elements": build_postit_flow_elements(
            ["Get bread", "Add spread", "Add fillings", "Add toppings", "Cut in half", "Plate", "Serve"],
            layout="arc",
            width=1100,
            height=280,
        ),
    },
    "postit_flow_outline": {
        "width": 520,
        "height": 1160,
        "elements": build_postit_flow_elements(
            labels=[
                "Q4 Product Launch",
                "Goals",
                "Revenue target",
                "Market share",
                "Tactics",
                "Campaign A",
                "Campaign B",
                "Risks",
                "Timeline",
                "Budget",
            ],
            layout="outline",
            width=520,
            height=1160,
            outline_levels=[0, 1, 2, 2, 1, 2, 2, 1, 2, 2],
        ),
    },
    "postit_flow_orgchart": {
        "width": 720,
        "height": 400,
        "elements": build_postit_flow_elements(
            labels=None,
            layout="orgchart",
            width=720,
            height=400,
            structure={
                "label": "CEO",
                "children": [
                    {
                        "label": "CTO",
                        "children": [{"label": "Engineering"}, {"label": "Product"}],
                    },
                    {
                        "label": "CFO",
                        "children": [{"label": "Finance"}, {"label": "Legal"}],
                    },
                    {
                        "label": "COO",
                        "children": [{"label": "Operations"}, {"label": "HR"}],
                    },
                ],
            },
        ),
    },
    "postit_flow_fishbone": {
        "width": 1000,
        "height": 340,
        "elements": build_postit_flow_elements(
            labels=None,
            layout="fishbone",
            width=1000,
            height=340,
            structure={
                "theme": "Defects",
                "causes_top": ["Training", "Equipment", "Procedure"],
                "causes_bottom": ["Material", "Measurement", "Environment"],
            },
        ),
    },
    "postit_flow_mindmap": {
        "width": 700,
        "height": 440,
        "elements": build_postit_flow_elements(
            labels=None,
            layout="mindmap",
            width=700,
            height=440,
            structure={
                "center": "Product Launch",
                "branches": ["Marketing", "Sales", "Support", "Legal", "Operations"],
            },
        ),
    },
}


def render_scene(
    spec: Union[Dict[str, Any], str],
    config: WireframeConfig,
) -> str:
    """Render a wireframe scene from a spec or preset name.

    Args:
        spec: Either a preset name (e.g. "before", "after") or a dict with
            width, height, and elements (list of { type, x, y, width?, height?, props? }).
        config: WireframeConfig for colors, fonts, and filter defs.

    Returns:
        Full SVG string with viewBox and defs.
    """
    if isinstance(spec, str):
        if spec not in SCENE_PRESETS:
            raise ValueError(f"Unknown scene preset: {spec}. Known: {list(SCENE_PRESETS)}")
        spec = SCENE_PRESETS[spec]

    width = spec.get("width", 600)
    height = spec.get("height", 520)
    elements_list = spec.get("elements", [])

    parts = []
    for el in elements_list:
        el_type = el.get("type")
        if not el_type:
            continue
        if el_type not in ELEMENT_REGISTRY:
            raise ValueError(f"Unknown element type: {el_type}. Known: {list(ELEMENT_REGISTRY)}")
        adapter = ELEMENT_REGISTRY[el_type]
        parts.append(adapter(config, el))

    defs = config.get_filter_defs()
    content = "\n".join(parts)
    return f"""<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {defs}
  </defs>
  {content}
</svg>"""


def list_element_types() -> List[str]:
    """Return registered element type names."""
    return list(ELEMENT_REGISTRY.keys())


def list_presets() -> List[str]:
    """Return named scene preset names."""
    return list(SCENE_PRESETS.keys())
