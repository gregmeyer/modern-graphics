"""Premium stacked card layout with hero illustrations + detail panel."""

from __future__ import annotations

from html import escape
from textwrap import dedent
from typing import Any, Dict, List, Sequence

from ..base import BaseGenerator

DEFAULT_CARD_SIZE = 1100
DEFAULT_FONT = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
DEFAULT_PALETTE = {
    "frame_bg": "linear-gradient(145deg, #040910, #0b1d33)",
    "frame_border": "rgba(148,163,184,0.45)",
    "panel_bg": "linear-gradient(135deg, rgba(2,9,22,0.95), rgba(7,19,37,0.9))",
    "panel_border": "rgba(59,130,246,0.35)",
    "accent": "#38bdf8",
    "accent_soft": "rgba(56,189,248,0.32)",
    "accent_glow": "rgba(56,189,248,0.65)",
    "pill_bg": "rgba(8,18,36,0.75)",
    "pill_border": "rgba(56,189,248,0.35)",
    "grid_color": "rgba(56,189,248,0.08)",
    "background": "#01050f",
}


def _merge_palette(palette: Dict[str, str]) -> Dict[str, str]:
    merged = DEFAULT_PALETTE.copy()
    merged.update(palette or {})
    return merged


def _format_coord(value: float) -> str:
    numeric = float(value)
    if numeric.is_integer():
        return str(int(numeric))
    return f"{numeric:.2f}".rstrip("0").rstrip(".")


def _svg_multiline_text(
    lines: Sequence[str],
    *,
    x: float,
    y: float,
    css_class: str,
    anchor: str = "middle",
    line_height: int = 18,
) -> str:
    if not lines:
        return ""
    safe_lines = [escape(line) for line in lines]
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    text = [
        f'<text x="{_format_coord(x)}" y="{_format_coord(y)}"{anchor_attr} '
        f'class="{css_class}">'
    ]
    for idx, line in enumerate(safe_lines):
        if idx == 0:
            text.append(line)
        else:
            text.append(f'<tspan x="{_format_coord(x)}" dy="{line_height}">{line}</tspan>')
    text.append("</text>")
    return "".join(text)


def _timeline_svg(hero: Dict[str, Any], palette: Dict[str, str], base_id: str) -> str:
    steps = hero.get("steps", [])
    width, height = 720, 360
    left, right = 90, width - 90
    if len(steps) <= 1:
        positions = [width / 2.0]
    else:
        spacing = (right - left) / (len(steps) - 1)
        positions = [left + idx * spacing for idx in range(len(steps))]

    node_markup = []
    for idx, step in enumerate(steps):
        x = positions[idx]
        label_text = _svg_multiline_text([step.get("label", "")], x=x, y=110, css_class="timeline-label")
        detail_text = _svg_multiline_text(step.get("lines", []), x=x, y=270, css_class="timeline-detail")
        node_markup.append(
            dedent(
                f"""
                <g>
                    <circle cx="{_format_coord(x)}" cy="210" r="46" fill="rgba(2,11,27,0.8)"
                            stroke="{palette['panel_border']}" stroke-width="2" />
                    <circle cx="{_format_coord(x)}" cy="210" r="32" fill="{palette['accent_soft']}" />
                    <circle cx="{_format_coord(x)}" cy="210" r="16" fill="{palette['accent']}"
                            filter="url(#glow-{base_id})" />
                    {label_text}
                    {detail_text}
                </g>
                """
            )
        )

    grid_lines = "\n".join(
        f'<line x1="60" y1="{80 + offset}" x2="660" y2="{80 + offset}" '
        f'stroke="{palette["grid_color"]}" stroke-width="1" />'
        for offset in (0, 60, 120)
    )
    return dedent(
        f"""
        <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img"
             aria-label="{escape(hero.get('badge', 'Hero timeline'))}">
            <defs>
                <linearGradient id="timeline-bg-{base_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="rgba(4,18,40,0.85)"/>
                    <stop offset="100%" stop-color="rgba(6,26,50,0.7)"/>
                </linearGradient>
                <filter id="glow-{base_id}" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <style>
                .timeline-label {{ font-size: 20px; font-weight: 600; fill: {palette.get('text_secondary', '#e2e8f0')}; font-family: {DEFAULT_FONT}; }}
                .timeline-detail {{ font-size: 14px; fill: {palette.get('text_subtle', '#94a3b8')}; font-family: {DEFAULT_FONT}; }}
            </style>
            <rect x="0" y="0" width="{width}" height="{height}" rx="32"
                  fill="url(#timeline-bg-{base_id})" />
            <g opacity="0.25">{grid_lines}</g>
            <path d="M{_format_coord(positions[0])} 210 L{_format_coord(positions[-1])} 210"
                  stroke="{palette['accent']}" stroke-width="8"
                  stroke-linecap="round" opacity="0.4" />
            {''.join(node_markup)}
        </svg>
        """
    )


def _isolation_svg(hero: Dict[str, Any], palette: Dict[str, str], base_id: str) -> str:
    zones = hero.get("zones", [])
    width, height = 720, 360
    zone_height, top_offset = 78, 60
    fill_palette = ["rgba(12,18,40,0.85)", "rgba(10,14,34,0.8)", "rgba(8,12,30,0.75)"]
    zone_markup: List[str] = []

    for idx, zone in enumerate(zones):
        y = top_offset + idx * (zone_height + 14)
        fill_color = fill_palette[idx % len(fill_palette)]
        icon_x = 160
        icon_y = y + zone_height / 2
        label = _svg_multiline_text([zone.get("label", "")], x=210, y=y + 32, css_class="zone-label", anchor="start")
        detail = _svg_multiline_text(zone.get("lines", []), x=210, y=y + 52, css_class="zone-detail", anchor="start")
        zone_markup.append(
            dedent(
                f"""
                <g>
                    <rect x="120" y="{_format_coord(y)}" width="520" height="{zone_height}" rx="26"
                          fill="{fill_color}" stroke="{palette['panel_border']}" stroke-opacity="0.5"/>
                    <g>
                        <circle cx="{_format_coord(icon_x)}" cy="{_format_coord(icon_y)}" r="22"
                                fill="{palette['accent_soft']}" stroke="{palette['panel_border']}" />
                        <rect x="{_format_coord(icon_x - 12)}" y="{_format_coord(icon_y - 2)}"
                              width="24" height="20" rx="6" fill="{palette['accent']}" opacity="0.8"/>
                        <path d="M {_format_coord(icon_x - 8)} {_format_coord(icon_y - 4)} v-10 a10 10 0 0 1 20 0 v10"
                              stroke="#0f172a" stroke-width="2" fill="none"/>
                    </g>
                    {label}
                    {detail}
                </g>
                """
            )
        )

    grid_lines = "\n".join(
        f'<line x1="{150 + idx * 140}" y1="40" x2="{150 + idx * 140}" y2="320" '
        f'stroke="{palette["grid_color"]}" stroke-dasharray="6 10" />'
        for idx in range(3)
    )
    return dedent(
        f"""
        <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img"
             aria-label="{escape(hero.get('badge', 'Hero isolation diagram'))}">
            <defs>
                <linearGradient id="isolation-bg-{base_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="rgba(20,5,38,0.9)"/>
                    <stop offset="100%" stop-color="rgba(8,2,20,0.85)"/>
                </linearGradient>
            </defs>
            <style>
                .zone-label {{ font-size: 18px; font-weight: 600; fill: {palette.get('text_primary', '#f8fafc')}; font-family: {DEFAULT_FONT}; }}
                .zone-detail {{ font-size: 14px; fill: {palette.get('text_muted', '#cbd5e1')}; font-family: {DEFAULT_FONT}; }}
            </style>
            <rect x="0" y="0" width="{width}" height="{height}" rx="32"
                  fill="url(#isolation-bg-{base_id})" />
            <g opacity="0.3">{grid_lines}</g>
            {''.join(zone_markup)}
        </svg>
        """
    )


def _window_svg(hero: Dict[str, Any], palette: Dict[str, str], base_id: str) -> str:
    windows = hero.get("windows", [])
    width, height = 720, 360
    left, right = 110, width - 110
    if len(windows) <= 1:
        centers = [width / 2.0]
    else:
        spacing = (right - left) / (len(windows) - 1)
        centers = [left + idx * spacing for idx in range(len(windows))]

    tile_width, tile_height = 170, 120
    gate_markup: List[str] = []
    for idx, window in enumerate(windows):
        center = centers[idx]
        x = center - tile_width / 2
        y = 110
        label = _svg_multiline_text([window.get("label", "")], x=x + 20, y=y + 32, css_class="window-label", anchor="start")
        detail = _svg_multiline_text(window.get("lines", []), x=x + 20, y=y + 52, css_class="window-detail", anchor="start")
        gate_markup.append(
            dedent(
                f"""
                <g>
                    <rect x="{_format_coord(x)}" y="{y}" width="{tile_width}" height="{tile_height}" rx="28"
                          fill="rgba(10,10,10,0.45)" stroke="{palette['panel_border']}" />
                    {label}
                    {detail}
                </g>
                """
            )
        )

    path = "M60 260 C 200 120, 360 120, 520 260 S 700 380, 660 220"
    pulses = "\n".join(
        f'<circle cx="{_format_coord(center)}" cy="{210 if idx % 2 == 0 else 260}" '
        f'r="10" fill="{palette["accent"]}" />'
        for idx, center in enumerate(centers)
    )
    return dedent(
        f"""
        <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img"
             aria-label="{escape(hero.get('badge', 'Hero control window'))}">
            <defs>
                <linearGradient id="window-bg-{base_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="rgba(30,15,5,0.9)"/>
                    <stop offset="100%" stop-color="rgba(10,4,1,0.85)"/>
                </linearGradient>
            </defs>
            <style>
                .window-label {{ font-size: 17px; font-weight: 600; fill: {palette.get('text_primary', '#f8fafc')}; font-family: {DEFAULT_FONT}; }}
                .window-detail {{ font-size: 13px; fill: {palette.get('text_muted', '#f1f5f9')}; opacity: 0.85; font-family: {DEFAULT_FONT}; }}
            </style>
            <rect x="0" y="0" width="{width}" height="{height}" rx="32"
                  fill="url(#window-bg-{base_id})" />
            <path d="{path}" stroke="{palette['accent']}" stroke-width="6" fill="none" opacity="0.6" />
            <path d="{path}" stroke="{palette['accent_soft']}" stroke-width="24" fill="none" opacity="0.15" />
            {pulses}
            {''.join(gate_markup)}
        </svg>
        """
    )


HERO_BUILDERS = {
    "timeline": _timeline_svg,
    "isolation": _isolation_svg,
    "window": _window_svg,
}


def _build_hero_svg(hero: Dict[str, Any], palette: Dict[str, str], card_id: str) -> str:
    hero_type = hero.get("type", "timeline")
    builder = HERO_BUILDERS.get(hero_type)
    if not builder:
        raise ValueError(f"Unknown premium card hero type: {hero_type}")
    return builder(hero, palette, card_id)


def generate_premium_card(
    generator: BaseGenerator,
    *,
    title: str,
    tagline: str,
    subtext: str,
    eyebrow: str,
    features: List[str],
    hero: Dict[str, Any],
    palette: Dict[str, str],
    canvas_size: int = DEFAULT_CARD_SIZE,
    show_top_panel: bool = True,
    show_bottom_panel: bool = True,
) -> str:
    """Render a stacked premium card with hero illustration + detail panel.

    Args:
        generator: Base generator for wrapping styles.
        title: Card headline.
        tagline: Supporting line under the headline.
        subtext: Body copy.
        eyebrow: Small top label in the bottom panel.
        features: Bullet/pill list rendered below the copy.
        hero: Dict describing the hero section (type + data + pills).
        palette: Dict overriding styling tokens from DEFAULT_PALETTE.
        canvas_size: Square stage size (px) for the render (default 1100).
        show_top_panel: When False, omit the hero canvas.
        show_bottom_panel: When False, omit the body card.
    """
    if not show_top_panel and not show_bottom_panel:
        raise ValueError("At least one of top or bottom panel must be enabled.")

    palette_config = _merge_palette(palette or {})
    text_primary = palette_config.get("text_primary", "#f8fafc")
    text_secondary = palette_config.get("text_secondary", "#e2e8f0")
    text_muted = palette_config.get("text_muted", "#cbd5e1")
    badge_bg = palette_config.get("badge_bg", "rgba(2,6,23,0.6)")
    hero_visual_bg = palette_config.get("hero_visual_bg", "rgba(2,6,23,0.55)")
    hero_visual_border = palette_config.get("hero_visual_border", "rgba(148,163,184,0.18)")
    card_body_bg = palette_config.get("card_body_bg", "rgba(4,12,30,0.65)")
    feature_bg = palette_config.get("feature_bg", "rgba(2,6,23,0.65)")
    panel_shadow = palette_config.get("panel_shadow", "inset 0 0 60px rgba(0,0,0,0.45)")
    font_family = palette_config.get("font_family", DEFAULT_FONT)
    stage_size = max(canvas_size, 800)
    card_width = stage_size - 100
    card_classes: List[str] = ["ops-card"]
    hero_section = ""

    if show_top_panel:
        if not hero:
            raise ValueError("Hero configuration is required when show_top_panel is True.")
        hero_svg = _build_hero_svg(hero, palette_config, card_id=hero.get("id", "premium-card"))
        pills_html = "".join(
            f'<div class="hero-pill"><span>{escape(pill.get("label", ""))}</span>'
            f"<p>{escape(pill.get('detail', ''))}</p></div>"
            for pill in hero.get("pills", [])
        )
        caption_html = (
            f'<span class="hero-caption">{escape(hero.get("caption", ""))}</span>'
            if hero.get("caption")
            else ""
        )
        hero_section = dedent(
            f"""
            <div class="card-hero">
                <div class="hero-header">
                    <span class="hero-badge">{escape(hero.get('badge', 'Hero panel'))}</span>
                    {caption_html}
                </div>
                <div class="hero-content">
                    <div class="hero-visual">
                        {hero_svg}
                    </div>
                    <div class="hero-pills">{pills_html}</div>
                </div>
            </div>
            """
        )
    else:
        card_classes.append("bottom-only")

    body_section = ""
    if show_bottom_panel:
        features_html = "".join(
            f"<li><span></span>{escape(feature)}</li>"
            for feature in (features or [])
        )
        body_section = dedent(
            f"""
            <div class="card-body">
                <div class="eyebrow">{escape(eyebrow)}</div>
                <h1>{escape(title)}</h1>
                <div class="tagline">{escape(tagline)}</div>
                <p class="subtext">{escape(subtext)}</p>
                <ul class="feature-list">
                    {features_html}
                </ul>
            </div>
            """
        )
    else:
        card_classes.append("top-only")

    card_html = f'<div class="{" ".join(card_classes)}">{hero_section}{body_section}</div>'
    stage_html = dedent(
        f"""
        <div class="premium-card-stage" style="width:{stage_size}px;">
            {card_html}
        </div>
        {generator._generate_attribution_html()}
        """
    )

    styles = dedent(
        f"""
        :root {{
            --ops-font: {font_family};
            --accent: {palette_config['accent']};
            --accent-soft: {palette_config['accent_soft']};
            --accent-glow: {palette_config['accent_glow']};
            --frame-bg: {palette_config['frame_bg']};
            --frame-border: {palette_config['frame_border']};
            --panel-bg: {palette_config['panel_bg']};
            --panel-border: {palette_config['panel_border']};
            --pill-bg: {palette_config['pill_bg']};
            --pill-border: {palette_config['pill_border']};
            --grid-color: {palette_config['grid_color']};
            --canvas-bg: {palette_config.get('background', '#01050f')};
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--ops-font);
            color: {text_primary};
            background: var(--canvas-bg);
        }}

        .premium-card-stage {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            height: auto;
            background: var(--canvas-bg);
        }}

        .ops-card {{
            width: {card_width}px;
            min-height: {card_width}px;
            height: auto;
            background: var(--frame-bg);
            border: 1px solid var(--frame-border);
            border-radius: 48px;
            padding: 48px;
            box-shadow: 0 55px 160px rgba(1,5,15,0.85);
            display: flex;
            flex-direction: column;
            gap: 32px;
            position: relative;
            overflow: hidden;
        }}

        .ops-card::before {{
            content: "";
            position: absolute;
            inset: 24px;
            border-radius: 40px;
            background: radial-gradient(circle at 20% 20%, var(--accent-soft), transparent 60%);
            opacity: 0.65;
            filter: blur(8px);
            z-index: 0;
        }}

        .ops-card > * {{
            position: relative;
            z-index: 1;
        }}

        .ops-card.top-only,
        .ops-card.bottom-only {{
            min-height: auto;
        }}

        .card-hero {{
            background: var(--panel-bg);
            border-radius: 32px;
            border: 1px solid var(--panel-border);
            padding: 32px;
            display: flex;
            flex-direction: column;
            gap: 18px;
            box-shadow: {panel_shadow};
        }}

        .hero-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .hero-badge {{
            font-size: 13px;
            letter-spacing: 0.4em;
            text-transform: uppercase;
            color: {text_secondary};
            padding: 6px 22px;
            border-radius: 999px;
            border: 1px solid var(--panel-border);
            background: {badge_bg};
        }}

        .hero-caption {{
            font-size: 14px;
            color: {text_muted};
            letter-spacing: 0.08em;
        }}

        .hero-content {{
            display: flex;
            gap: 28px;
            align-items: stretch;
        }}

        .hero-visual {{
            flex: 1.15;
            border-radius: 28px;
            overflow: hidden;
            border: 1px solid {hero_visual_border};
            background: {hero_visual_bg};
            padding: 16px;
        }}

        .hero-visual svg {{
            width: 100%;
            height: 100%;
            display: block;
            border-radius: 20px;
        }}

        .hero-pills {{
            flex: 0.85;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .hero-pill {{
            background: var(--pill-bg);
            border-radius: 22px;
            border: 1px solid var(--pill-border);
            padding: 18px 22px;
            box-shadow: inset 0 0 40px rgba(0,0,0,0.25);
        }}

        .hero-pill span {{
            font-size: 12px;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--accent);
            display: block;
            margin-bottom: 6px;
        }}

        .hero-pill p {{
            margin: 0;
            font-size: 17px;
            line-height: 1.4;
        }}

        .card-body {{
            background: {card_body_bg};
            border-radius: 32px;
            padding: 32px;
            border: 1px solid rgba(148,163,184,0.25);
        }}

        .card-body .eyebrow {{
            font-size: 12px;
            letter-spacing: 0.5em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 16px;
        }}

        .card-body h1 {{
            font-size: 42px;
            margin: 0 0 12px;
            letter-spacing: -0.02em;
        }}

        .card-body .tagline {{
            font-size: 22px;
            margin: 0 0 16px;
            color: {text_secondary};
        }}

        .card-body .subtext {{
            font-size: 18px;
            margin: 0 0 20px;
            color: {text_muted};
            line-height: 1.5;
        }}

        .feature-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .feature-list li {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 18px;
            background: {feature_bg};
            border-radius: 18px;
            padding: 14px 18px;
            border: 1px solid rgba(148,163,184,0.25);
        }}

        .feature-list li span {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent);
            display: inline-flex;
        }}

        .ops-card.no-top-panel .card-body {{
            margin-top: auto;
        }}

        .ops-card.no-bottom-panel .card-hero {{
            margin-bottom: auto;
        }}
        """
    )

    return generator._wrap_html(stage_html, styles)
