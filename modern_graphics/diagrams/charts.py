"""Chart.js-powered data chart layouts.

Renders line, bar, grouped bar, horizontal bar, pie, donut, and sankey charts.
Chart.js (and the sankey plugin) is vendored in ``modern_graphics/assets/vendor``
and inlined into the HTML so PNG export works offline.

All layouts emit ``<canvas data-mg-chart>`` and set ``window.__chartReady = true``
in Chart.js's ``animation.onComplete`` hook; ``export.py`` waits on that flag
before taking the screenshot.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING

from ..base import BaseGenerator
from .theme_utils import (
    ThemeColors,
    extract_theme_colors,
    generate_css_variables,
    inject_google_fonts,
    with_alpha,
)

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


_VENDOR_DIR = Path(__file__).resolve().parent.parent / "assets" / "vendor"


def _load_vendor_script(filename: str) -> str:
    path = _VENDOR_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Vendored script not found: {path}. "
            "Re-run the vendor step in modern_graphics/assets/vendor/README.md."
        )
    return path.read_text(encoding="utf-8")


def _hex_to_rgb(color: str) -> Optional[tuple]:
    c = color.lstrip("#")
    if len(c) != 6:
        return None
    try:
        return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    except ValueError:
        return None


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02x}{:02x}{:02x}".format(max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def _rotate_hue(color: str, degrees: float) -> str:
    """Rotate a hex color's hue by degrees on the HSL wheel."""
    import colorsys

    rgb = _hex_to_rgb(color)
    if rgb is None:
        return color
    r, g, b = (v / 255.0 for v in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + degrees / 360.0) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return _rgb_to_hex(int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def _build_palette(theme: ThemeColors, color_scheme: Optional["ColorScheme"], n: int) -> List[str]:
    """Return a list of N distinct but harmonious hex colors."""
    seeds: List[str] = [theme.accent]
    if color_scheme is not None:
        for attr in ("secondary", "accent"):
            val = getattr(color_scheme, attr, None)
            if isinstance(val, str) and val and val not in seeds:
                seeds.append(val)
    # Rotate hues from the primary seed to fill out the palette.
    rotations = [30, -30, 60, -60, 90, -90, 120, -120, 150, -150, 180]
    for deg in rotations:
        if len(seeds) >= n:
            break
        rotated = _rotate_hue(seeds[0], deg)
        if rotated not in seeds:
            seeds.append(rotated)
    # Pad by cycling if still short.
    while len(seeds) < n:
        seeds.append(seeds[len(seeds) % max(1, len(seeds))])
    return seeds[:n]


def _common_options(
    theme: ThemeColors,
    *,
    show_legend: bool = True,
    legend_position: str = "top",
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    show_scales: bool = True,
    index_axis: str = "x",
) -> Dict[str, Any]:
    axis_text = theme.text_secondary
    grid_color = with_alpha(theme.text_primary, 0.08)
    opts: Dict[str, Any] = {
        "responsive": True,
        "maintainAspectRatio": False,
        "plugins": {
            "legend": {
                "display": show_legend,
                "position": legend_position,
                "labels": {
                    "color": theme.text_primary,
                    "font": {"family": theme.font_family, "size": 14},
                    "boxWidth": 18,
                    "padding": 16,
                },
            },
            "tooltip": {
                "enabled": False,  # PNG export is static; tooltips add no value.
            },
        },
    }
    if show_scales:
        make_axis = lambda title: {
            "ticks": {"color": axis_text, "font": {"family": theme.font_family, "size": 12}},
            "grid": {"color": grid_color, "drawBorder": False},
            "title": (
                {
                    "display": bool(title),
                    "text": title or "",
                    "color": theme.text_secondary,
                    "font": {"family": theme.font_family, "size": 13, "weight": "600"},
                }
                if title
                else {"display": False}
            ),
        }
        opts["scales"] = {
            "x": make_axis(x_axis_label),
            "y": make_axis(y_axis_label),
        }
        opts["indexAxis"] = index_axis
    return opts


def _wrap_chart(
    generator: BaseGenerator,
    *,
    theme: ThemeColors,
    color_scheme: Optional["ColorScheme"],
    chart_type: str,
    config: Dict[str, Any],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    canvas_height: int = 720,
    canvas_width: int = 1280,
    include_sankey_plugin: bool = False,
) -> str:
    """Build the full HTML document for a chart."""
    chart_js = _load_vendor_script("chart.umd.min.js")
    plugin_script = ""
    if include_sankey_plugin:
        plugin_script = (
            "<script>"
            + _load_vendor_script("chartjs-chart-sankey.min.js")
            + "</script>"
        )

    config_with_hooks = dict(config)
    options = dict(config.get("options", {}))
    # The real ready signal: fires once the chart has painted.
    animation_js = "__MG_ANIMATION_COMPLETE__"
    options["animation"] = animation_js  # placeholder, replaced after JSON serialize
    config_with_hooks["options"] = options

    config_json = json.dumps(config_with_hooks, ensure_ascii=False)
    config_json = config_json.replace(
        f'"{animation_js}"',
        "{duration: 0, onComplete: function() { window.__chartReady = true; }}",
    )

    css_vars = generate_css_variables(theme)
    title_html = ""
    if title:
        title_html += f'<h1 class="chart-title">{escape(title)}</h1>'
    if subtitle:
        title_html += f'<p class="chart-subtitle">{escape(subtitle)}</p>'

    content = f"""
    <div class="chart-wrapper" data-mg-crop-root>
      {title_html}
      <div class="chart-canvas-box" style="width:{canvas_width}px;height:{canvas_height}px;">
        <canvas id="mg-chart" data-mg-chart></canvas>
      </div>
    </div>
    <script>
    {chart_js}
    </script>
    {plugin_script}
    <script>
    window.__chartReady = false;
    (function() {{
      const ctx = document.getElementById('mg-chart').getContext('2d');
      const config = {config_json};
      new Chart(ctx, config);
      // Fallback: mark ready after 3s even if animation hook is skipped.
      setTimeout(function() {{ window.__chartReady = true; }}, 3000);
    }})();
    </script>
    """

    css = f"""
    {css_vars}
    body {{
      background: var(--bg-page);
      padding: 48px;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .chart-wrapper {{
      background: var(--bg-card);
      border-radius: 20px;
      padding: 40px 48px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 12px 40px rgba(0,0,0,0.06);
    }}
    .chart-title {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-1);
      margin-bottom: 4px;
    }}
    .chart-subtitle {{
      font-family: var(--font-body);
      font-size: 16px;
      color: var(--text-2);
      margin-bottom: 24px;
    }}
    .chart-canvas-box {{
      position: relative;
    }}
    """

    html = generator._wrap_html(content, css)
    html = inject_google_fonts(html, theme)
    return html


def _resolve_series_colors(
    series: List[Dict[str, Any]], palette: List[str]
) -> List[str]:
    return [s.get("color") or palette[i % len(palette)] for i, s in enumerate(series)]


# ---------------------------------------------------------------------------
# Line chart
# ---------------------------------------------------------------------------

def generate_line_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    series: Sequence[Dict[str, Any]],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    theme = extract_theme_colors(color_scheme)
    series_list = list(series)
    palette = _build_palette(theme, color_scheme, max(1, len(series_list)))
    colors = _resolve_series_colors(series_list, palette)

    datasets = []
    for s, c in zip(series_list, colors):
        datasets.append({
            "label": s.get("name", ""),
            "data": list(s.get("values", [])),
            "borderColor": c,
            "backgroundColor": with_alpha(c, 0.15),
            "borderWidth": 3,
            "pointRadius": 4,
            "pointBackgroundColor": c,
            "tension": 0.35,
            "fill": False,
        })

    config = {
        "type": "line",
        "data": {"labels": list(labels), "datasets": datasets},
        "options": _common_options(
            theme,
            show_legend=show_legend and len(series_list) > 1,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
        ),
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="line", config=config,
        title=title, subtitle=subtitle,
    )


# ---------------------------------------------------------------------------
# Stacked area chart
# ---------------------------------------------------------------------------

def generate_stacked_area_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    series: Sequence[Dict[str, Any]],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    theme = extract_theme_colors(color_scheme)
    series_list = list(series)
    palette = _build_palette(theme, color_scheme, max(1, len(series_list)))
    colors = _resolve_series_colors(series_list, palette)

    datasets = []
    for s, c in zip(series_list, colors):
        datasets.append({
            "label": s.get("name", ""),
            "data": list(s.get("values", [])),
            "borderColor": c,
            "backgroundColor": with_alpha(c, 0.55),
            "borderWidth": 1,
            "pointRadius": 0,
            "tension": 0.35,
            "fill": True,
        })

    options = _common_options(
        theme,
        show_legend=show_legend,
        legend_position="bottom",
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
    )
    options["scales"]["y"]["stacked"] = True
    options["scales"]["x"]["stacked"] = True

    config = {
        "type": "line",
        "data": {"labels": list(labels), "datasets": datasets},
        "options": options,
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="line", config=config,
        title=title, subtitle=subtitle,
    )


# ---------------------------------------------------------------------------
# Bar chart (single series, vertical)
# ---------------------------------------------------------------------------

def generate_bar_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    values: Sequence[float],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    theme = extract_theme_colors(color_scheme)
    palette = _build_palette(theme, color_scheme, len(labels))
    config = {
        "type": "bar",
        "data": {
            "labels": list(labels),
            "datasets": [{
                "data": list(values),
                "backgroundColor": palette,
                "borderRadius": 8,
                "borderSkipped": False,
            }],
        },
        "options": _common_options(
            theme,
            show_legend=False,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
        ),
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="bar", config=config,
        title=title, subtitle=subtitle,
    )


# ---------------------------------------------------------------------------
# Grouped bar chart (multi-series, vertical)
# ---------------------------------------------------------------------------

def generate_grouped_bar_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    series: Sequence[Dict[str, Any]],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    theme = extract_theme_colors(color_scheme)
    series_list = list(series)
    palette = _build_palette(theme, color_scheme, max(1, len(series_list)))
    colors = _resolve_series_colors(series_list, palette)

    datasets = [
        {
            "label": s.get("name", ""),
            "data": list(s.get("values", [])),
            "backgroundColor": c,
            "borderRadius": 6,
            "borderSkipped": False,
        }
        for s, c in zip(series_list, colors)
    ]

    config = {
        "type": "bar",
        "data": {"labels": list(labels), "datasets": datasets},
        "options": _common_options(
            theme,
            show_legend=show_legend,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
        ),
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="bar", config=config,
        title=title, subtitle=subtitle,
    )


# ---------------------------------------------------------------------------
# Stacked bar chart (single stack per x label)
# ---------------------------------------------------------------------------

def generate_stacked_bar_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    series: Sequence[Dict[str, Any]],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """One stacked bar per x label; each series is a layer in every stack."""
    theme = extract_theme_colors(color_scheme)
    series_list = list(series)
    palette = _build_palette(theme, color_scheme, max(1, len(series_list)))
    colors = _resolve_series_colors(series_list, palette)

    datasets = [
        {
            "label": s.get("name", ""),
            "data": list(s.get("values", [])),
            "backgroundColor": c,
            "borderRadius": 4,
            "borderSkipped": False,
        }
        for s, c in zip(series_list, colors)
    ]

    options = _common_options(
        theme,
        show_legend=show_legend,
        legend_position="bottom",
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
    )
    options["scales"]["x"]["stacked"] = True
    options["scales"]["y"]["stacked"] = True

    config = {
        "type": "bar",
        "data": {"labels": list(labels), "datasets": datasets},
        "options": options,
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="bar", config=config,
        title=title, subtitle=subtitle,
    )


# ---------------------------------------------------------------------------
# Grouped stacked bar chart
# ---------------------------------------------------------------------------

def generate_grouped_stacked_bar_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    series: Sequence[Dict[str, Any]],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Bars grouped side-by-side per x label, each bar being a stack.

    Each series must include a ``stack`` key — series sharing the same
    ``stack`` are drawn on top of each other; different stacks sit
    side-by-side within each x label.

    Example series::

        [
          {"name": "Product A", "stack": "2024", "values": [10, 12, 14]},
          {"name": "Product B", "stack": "2024", "values": [5, 7, 9]},
          {"name": "Product A", "stack": "2025", "values": [15, 17, 20]},
          {"name": "Product B", "stack": "2025", "values": [8, 10, 12]},
        ]
    """
    theme = extract_theme_colors(color_scheme)
    series_list = list(series)
    # Color by unique series name so the legend reads cleanly.
    unique_names: List[str] = []
    for s in series_list:
        name = s.get("name", "")
        if name not in unique_names:
            unique_names.append(name)
    palette = _build_palette(theme, color_scheme, max(1, len(unique_names)))
    color_by_name = {n: palette[i] for i, n in enumerate(unique_names)}

    datasets = []
    seen_names = set()
    for s in series_list:
        name = s.get("name", "")
        stack = str(s.get("stack", "default"))
        color = s.get("color") or color_by_name.get(name, theme.accent)
        show_in_legend = name not in seen_names
        seen_names.add(name)
        datasets.append({
            "label": name,
            "stack": stack,
            "data": list(s.get("values", [])),
            "backgroundColor": color,
            "borderRadius": 4,
            "borderSkipped": False,
            "borderWidth": 0,
            # Hide duplicate legend entries for the same product across stacks.
            **({"hidden": False} if show_in_legend else {}),
        })

    options = _common_options(
        theme,
        show_legend=show_legend,
        legend_position="bottom",
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
    )
    options["scales"]["x"]["stacked"] = True
    options["scales"]["y"]["stacked"] = True
    # De-duplicate legend entries (chart.js emits one per dataset otherwise).
    options["plugins"]["legend"]["labels"]["generateLabels"] = "__MG_LEGEND_DEDUP__"

    config = {
        "type": "bar",
        "data": {"labels": list(labels), "datasets": datasets},
        "options": options,
    }
    html = _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="bar", config=config,
        title=title, subtitle=subtitle,
    )
    # Inject a generateLabels fn that returns one entry per unique dataset label.
    dedup_fn = (
        "function(chart) { var seen = {}; var out = []; "
        "chart.data.datasets.forEach(function(ds, i) { "
        "  if (seen[ds.label]) return; seen[ds.label] = true; "
        "  out.push({ text: ds.label, fillStyle: ds.backgroundColor, "
        "    strokeStyle: ds.backgroundColor, lineWidth: 0, hidden: false, "
        "    datasetIndex: i }); "
        "}); return out; }"
    )
    html = html.replace('"__MG_LEGEND_DEDUP__"', dedup_fn)
    return html


# ---------------------------------------------------------------------------
# Horizontal bar chart
# ---------------------------------------------------------------------------

def generate_horizontal_bar_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    values: Sequence[float],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    x_axis_label: Optional[str] = None,
    y_axis_label: Optional[str] = None,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    theme = extract_theme_colors(color_scheme)
    palette = _build_palette(theme, color_scheme, len(labels))
    config = {
        "type": "bar",
        "data": {
            "labels": list(labels),
            "datasets": [{
                "data": list(values),
                "backgroundColor": palette,
                "borderRadius": 8,
                "borderSkipped": False,
            }],
        },
        "options": _common_options(
            theme,
            show_legend=False,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            index_axis="y",
        ),
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="bar", config=config,
        title=title, subtitle=subtitle,
    )


# ---------------------------------------------------------------------------
# Pie chart
# ---------------------------------------------------------------------------

def _pie_or_donut(
    generator: BaseGenerator,
    labels: Sequence[str],
    values: Sequence[float],
    *,
    cutout: str,
    title: Optional[str],
    subtitle: Optional[str],
    show_legend: bool,
    color_scheme: Optional["ColorScheme"],
) -> str:
    theme = extract_theme_colors(color_scheme)
    palette = _build_palette(theme, color_scheme, len(labels))
    config = {
        "type": "doughnut",
        "data": {
            "labels": list(labels),
            "datasets": [{
                "data": list(values),
                "backgroundColor": palette,
                "borderColor": theme.card_bg,
                "borderWidth": 3,
            }],
        },
        "options": {
            **_common_options(theme, show_legend=show_legend, legend_position="right", show_scales=False),
            "cutout": cutout,
        },
    }
    return _wrap_chart(
        generator, theme=theme, color_scheme=color_scheme,
        chart_type="doughnut", config=config,
        title=title, subtitle=subtitle,
        canvas_height=600, canvas_width=900,
    )


def generate_pie_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    values: Sequence[float],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    return _pie_or_donut(
        generator, labels, values,
        cutout="0%",
        title=title, subtitle=subtitle,
        show_legend=show_legend,
        color_scheme=color_scheme,
    )


def generate_donut_chart(
    generator: BaseGenerator,
    labels: Sequence[str],
    values: Sequence[float],
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    show_legend: bool = True,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    return _pie_or_donut(
        generator, labels, values,
        cutout="62%",
        title=title, subtitle=subtitle,
        show_legend=show_legend,
        color_scheme=color_scheme,
    )


# ---------------------------------------------------------------------------
# Sankey chart
# ---------------------------------------------------------------------------

def generate_sankey_chart(
    generator: BaseGenerator,
    links: Sequence[Dict[str, Any]],
    nodes: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Render a sankey diagram.

    Args:
        links: list of {"from": str, "to": str, "value": number}
        nodes: optional explicit node list (otherwise derived from links)
    """
    theme = extract_theme_colors(color_scheme)
    link_list = [
        {"from": l["from"], "to": l["to"], "flow": float(l["value"])}
        for l in links
    ]

    node_names: List[str] = list(nodes) if nodes else []
    if not node_names:
        seen = []
        for l in link_list:
            for k in ("from", "to"):
                if l[k] not in seen:
                    seen.append(l[k])
        node_names = seen

    palette = _build_palette(theme, color_scheme, len(node_names))
    colors_map = {name: palette[i] for i, name in enumerate(node_names)}

    config = {
        "type": "sankey",
        "data": {
            "datasets": [{
                "label": "",
                "data": link_list,
                "colorFrom": "__MG_COLOR_FROM__",
                "colorTo": "__MG_COLOR_TO__",
                "colorMode": "gradient",
                "borderWidth": 0,
            }],
        },
        "options": {
            **_common_options(theme, show_legend=False, show_scales=False),
        },
    }

    # Inject colorFrom/colorTo as JS functions (not JSON-serializable).
    config_json = json.dumps(config, ensure_ascii=False)
    colors_js = json.dumps(colors_map, ensure_ascii=False)
    color_fn_from = f"function(c){{ var m={colors_js}; return m[c.dataset.data[c.dataIndex].from] || '{theme.accent}'; }}"
    color_fn_to = f"function(c){{ var m={colors_js}; return m[c.dataset.data[c.dataIndex].to] || '{theme.accent}'; }}"
    config_json = config_json.replace('"__MG_COLOR_FROM__"', color_fn_from)
    config_json = config_json.replace('"__MG_COLOR_TO__"', color_fn_to)

    # Also replace the "labels" dict with the plugin's expected form: node -> display name.
    # (Plugin accepts `labels` as {id: displayName}; here display name == id.)
    # That's already correct in our structure — no-op.

    # Build the chart inline (reuses _wrap_chart's structure but with pre-serialized config).
    chart_js = _load_vendor_script("chart.umd.min.js")
    plugin_js = _load_vendor_script("chartjs-chart-sankey.min.js")
    css_vars = generate_css_variables(theme)
    title_html = ""
    if title:
        title_html += f'<h1 class="chart-title">{escape(title)}</h1>'
    if subtitle:
        title_html += f'<p class="chart-subtitle">{escape(subtitle)}</p>'

    # Inject animation hook into the options object. We pre-serialized config,
    # so patch the JSON string: insert an onComplete hook before the closing
    # brace of the top-level "options" object.
    hook = '"animation":{"duration":0,"onComplete":function(){window.__chartReady=true;}}'
    # Find "options":{ and insert our hook as the first key.
    needle = '"options":{'
    if needle in config_json:
        config_json = config_json.replace(needle, needle + hook + ",", 1)

    content = f"""
    <div class="chart-wrapper" data-mg-crop-root>
      {title_html}
      <div class="chart-canvas-box" style="width:1280px;height:720px;">
        <canvas id="mg-chart" data-mg-chart></canvas>
      </div>
    </div>
    <script>{chart_js}</script>
    <script>{plugin_js}</script>
    <script>
    window.__chartReady = false;
    (function() {{
      const ctx = document.getElementById('mg-chart').getContext('2d');
      const config = {config_json};
      new Chart(ctx, config);
      setTimeout(function() {{ window.__chartReady = true; }}, 3000);
    }})();
    </script>
    """

    css = f"""
    {css_vars}
    body {{
      background: var(--bg-page);
      padding: 48px;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .chart-wrapper {{
      background: var(--bg-card);
      border-radius: 20px;
      padding: 40px 48px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 12px 40px rgba(0,0,0,0.06);
    }}
    .chart-title {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-1);
      margin-bottom: 4px;
    }}
    .chart-subtitle {{
      font-family: var(--font-body);
      font-size: 16px;
      color: var(--text-2);
      margin-bottom: 24px;
    }}
    .chart-canvas-box {{
      position: relative;
    }}
    """

    html = generator._wrap_html(content, css)
    html = inject_google_fonts(html, theme)
    return html
