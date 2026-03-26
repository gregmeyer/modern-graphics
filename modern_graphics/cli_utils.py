"""Shared helpers and constants for CLI command handlers."""

import sys
import textwrap
from pathlib import Path
from typing import Optional

from .color_scheme import get_scheme, ColorScheme
from .diagrams.wireframe_svg import (
    WireframeSVGConfig,
)


LEGACY_COMMAND_ALIASES = {
    "slide-comparison": "slide-compare",
    "from-prompt": "from-prompt-file",
    "key_insight": "key-insight",
    "insight_card": "insight-card",
    "insight_story": "insight-story",
    "before_after": "before-after",
}

LEGACY_CREATE_HINTS = {
    "cycle": 'modern-graphics create --layout story --what-changed "System shifts" --output graphic.html',
    "comparison": 'modern-graphics create --layout comparison --left "Before:Manual:Slow" --right "After:Agentic:Faster" --output graphic.html',
    "grid": 'modern-graphics create --layout grid --items "A,B,C" --columns 3 --output graphic.html',
    "timeline": 'modern-graphics create --layout timeline --events "Q1|Baseline,Q2|Adoption" --output graphic.html',
    "funnel": 'modern-graphics create --layout funnel --stages "Visit,Trial,Paid" --values "100,40,12" --output graphic.html',
    "story-slide": 'modern-graphics create --layout story --what-changed "Execution changed" --time-period "this quarter" --what-it-means "Judgment quality now differentiates" --output graphic.html',
    "key-insight": 'modern-graphics create --layout key-insight --text "Key takeaway" --output insight.html',
    "insight-card": 'modern-graphics create --layout insight-card --text "Key takeaway" --output insight-card.html',
    "insight-story": 'modern-graphics create --layout insight-story --headline "When shipping gets easy" --insight-text "Use checklist gates" --output insight-story.html',
}

CREATE_EXAMPLES = {
    "hero": 'modern-graphics create --layout hero --headline "Execution scales" --output hero.html',
    "insight": 'modern-graphics create --layout insight --text "Key takeaway" --output insight.html',
    "key-insight": 'modern-graphics create --layout key-insight --text "Key takeaway" --output insight.html',
    "insight-card": 'modern-graphics create --layout insight-card --text "Key takeaway" --output insight-card.html',
    "insight-story": 'modern-graphics create --layout insight-story --headline "When shipping gets easy" --insight-text "Use checklist gates" --output insight-story.html',
    "comparison": 'modern-graphics create --layout comparison --left "Before:Manual:Slow" --right "After:Agentic:Faster" --output comparison.html',
    "story": 'modern-graphics create --layout story --what-changed "Execution accelerated" --output story.html',
    "timeline": 'modern-graphics create --layout timeline --events "Q1|Baseline,Q2|Adoption" --output timeline.html',
    "funnel": 'modern-graphics create --layout funnel --stages "Visit,Trial,Paid" --values "100,40,12" --output funnel.html',
    "grid": 'modern-graphics create --layout grid --items "A,B,C" --columns 3 --output grid.html',
}


def _adapt_legacy_command_aliases(argv: list[str]) -> tuple[list[str], Optional[str]]:
    """Map known legacy command aliases to canonical commands."""
    if len(argv) < 2:
        return argv, None

    command = argv[1]
    canonical = LEGACY_COMMAND_ALIASES.get(command)
    if not canonical:
        return argv, None

    adapted = list(argv)
    adapted[1] = canonical
    warning = (
        f"Deprecation warning: `{command}` is deprecated; use `{canonical}` instead. "
        "See docs/MIGRATION.md for canonical create workflows."
    )
    return adapted, warning


def _emit_legacy_command_warning(command: str) -> None:
    hint = LEGACY_CREATE_HINTS.get(command)
    if not hint:
        return
    print(
        f"Deprecation warning: `{command}` remains supported but is now considered legacy. "
        "Prefer `create` for new workflows.",
        file=sys.stderr,
    )
    print(f"Migration hint: {hint}", file=sys.stderr)


def _emit_create_error(layout: str, message: str) -> int:
    print(f"Error: {message}")
    example = CREATE_EXAMPLES.get(layout)
    if example:
        print(f"Hint: try `{example}`")
    return 1


def parse_steps(steps_str: str) -> list:
    """Parse steps string into list of step dicts"""
    steps = []
    colors = ['green', 'blue', 'orange', 'purple', 'red']
    for i, step_text in enumerate(steps_str.split(',')):
        steps.append({
            'text': step_text.strip(),
            'color': colors[i % len(colors)]
        })
    return steps


def parse_column(column_str: str) -> dict:
    """Parse column string like 'Title:Step1,Step2:Outcome'"""
    parts = column_str.split(':')
    title = parts[0]
    steps = parts[1].split(',') if len(parts) > 1 else []
    outcome = parts[2] if len(parts) > 2 else None

    return {
        'title': title,
        'steps': steps,
        'outcome': outcome
    }


def parse_items(items_str: str) -> list:
    """Parse items string into list of item dicts"""
    items = []
    for i, item_text in enumerate(items_str.split(','), 1):
        items.append({
            'number': str(i),
            'text': item_text.strip()
        })
    return items


def parse_flywheel_elements(elements_str: str, colors_str: str = None) -> list:
    """Parse flywheel elements string into list of element dicts"""
    elements = []
    element_texts = elements_str.split(',')
    colors = colors_str.split(',') if colors_str else []

    for i, text in enumerate(element_texts):
        color = colors[i].strip() if i < len(colors) else 'gray'
        elements.append({
            'text': text.strip(),
            'color': color
        })
    return elements


def parse_timeline_events(events_str: str, colors_str: str = None) -> list:
    """Parse timeline events string into list of event dicts

    Format: "Date1|Text1,Date2|Text2" or "Date1:Text1,Date2:Text2"
    """
    events = []
    event_texts = events_str.split(',')
    colors = colors_str.split(',') if colors_str else []

    for i, event_text in enumerate(event_texts):
        # Support both | and : as separators
        if '|' in event_text:
            parts = event_text.split('|', 1)
        elif ':' in event_text:
            parts = event_text.split(':', 1)
        else:
            parts = ['', event_text]

        date = parts[0].strip() if len(parts) > 0 else ''
        text = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        color = colors[i].strip() if i < len(colors) else 'gray'

        events.append({
            'date': date,
            'text': text,
            'color': color
        })
    return events


def parse_pyramid_layers(layers_str: str, colors_str: str = None) -> list:
    """Parse pyramid layers string into list of layer dicts"""
    layers = []
    layer_texts = layers_str.split(',')
    colors = colors_str.split(',') if colors_str else []

    for i, text in enumerate(layer_texts):
        color = colors[i].strip() if i < len(colors) else 'gray'
        layers.append({
            'text': text.strip(),
            'color': color
        })
    return layers


def parse_funnel_stages(stages_str: str, values_str: str = None, colors_str: str = None) -> list:
    """Parse funnel stages string into list of stage dicts

    Format: "Stage1,Stage2" with optional values "100,80,50"
    """
    stages = []
    stage_texts = stages_str.split(',')
    values = values_str.split(',') if values_str else []
    colors = colors_str.split(',') if colors_str else []

    for i, text in enumerate(stage_texts):
        value = int(values[i].strip()) if i < len(values) else 100 - (i * 10)
        color = colors[i].strip() if i < len(colors) else 'blue'
        stages.append({
            'text': text.strip(),
            'value': value,
            'color': color
        })
    return stages


def parse_highlights_arg(highlights_str: Optional[str]) -> Optional[list]:
    """Parse comma-separated highlight string into list."""
    if not highlights_str:
        return None
    return [item.strip() for item in highlights_str.split(',') if item.strip()]


def parse_stats_arg(stats_str: Optional[str]) -> Optional[list]:
    """Parse comma-separated stats in Label:Value format."""
    if not stats_str:
        return None
    stats = []
    for chunk in stats_str.split(','):
        if not chunk.strip():
            continue
        if ':' in chunk:
            label, value = chunk.split(':', 1)
        else:
            label, value = chunk, ''
        stats.append({'label': label.strip(), 'value': value.strip()})
    return stats


def shape_story_fields_for_density(
    what_changed: str,
    time_period: str,
    what_it_means: str,
    density: str,
) -> tuple[str, str, str]:
    """Apply density-specific shaping to story text fields."""
    if density != "clarity":
        return what_changed, time_period, what_it_means
    return (
        textwrap.shorten(what_changed, width=56, placeholder="..."),
        textwrap.shorten(time_period, width=32, placeholder="..."),
        textwrap.shorten(what_it_means, width=64, placeholder="..."),
    )


def shape_timeline_events_for_density(events: list, density: str) -> list:
    """Apply density-specific shaping to timeline events."""
    if density != "clarity":
        return events
    shaped = []
    for event in events[:4]:
        item = dict(event)
        item["text"] = textwrap.shorten(str(item.get("text", "")), width=42, placeholder="...")
        if item.get("description"):
            item["description"] = textwrap.shorten(str(item["description"]), width=72, placeholder="...")
        shaped.append(item)
    return shaped


def shape_grid_for_density(items: list, columns: int, density: str) -> tuple[list, int]:
    """Apply density-specific shaping to grid items and column count."""
    if density != "clarity":
        return items, columns
    shaped_items = []
    for item in items[:6]:
        shaped_items.append(
            {
                "number": item.get("number"),
                "text": textwrap.shorten(str(item.get("text", "")), width=34, placeholder="..."),
            }
        )
    return shaped_items, min(columns, 3)


def get_wireframe_config_from_theme(theme_name: Optional[str], width: int = 400, height: int = 300, accent_color: str = "#0071e3") -> WireframeSVGConfig:
    """Create WireframeSVGConfig from theme name or defaults."""
    if theme_name:
        scheme = get_scheme(theme_name)
        if scheme:
            # Detect dark theme
            bg = scheme.bg_primary.lstrip('#')
            is_dark = sum(int(bg[i:i+2], 16) for i in (0, 2, 4)) < 384

            return WireframeSVGConfig(
                width=width,
                height=height,
                accent_color=scheme.primary,
                success_color=scheme.success or "#34c759",
                error_color=scheme.error or "#ff3b30",
                text_primary=scheme.text_primary,
                text_secondary=scheme.text_secondary,
                text_tertiary=scheme.text_tertiary,
                surface_1=scheme.bg_primary,
                surface_2=scheme.bg_secondary,
                surface_3=scheme.bg_tertiary,
                border_color=scheme.border_medium if is_dark else scheme.border_light,
                font_family=scheme.font_family_body or scheme.font_family,
                chrome_dot_red=scheme.error if is_dark else None,
                chrome_dot_yellow=scheme.warning if is_dark else None,
                chrome_dot_green=scheme.success if is_dark else None,
            )

    return WireframeSVGConfig(
        width=width,
        height=height,
        accent_color=accent_color,
    )


def wrap_svg_for_png_export(svg: str, scheme: Optional[ColorScheme], width: int, height: int, white_bg: bool = True) -> str:
    """Wrap SVG in HTML for PNG export with proper styling.

    Args:
        svg: SVG content
        scheme: Optional color scheme for fonts/effects
        width: SVG width
        height: SVG height
        white_bg: Use white background for easy drop-in (default True)
    """
    # Use white background by default for easy drop-in to documents
    bg_color = "#ffffff" if white_bg else (scheme.bg_secondary if scheme else "#f5f5f7")

    # Get Google Fonts link if theme uses custom fonts
    fonts_link = ""
    if scheme:
        fonts_link = scheme.get_google_fonts_link() or ""

    # Add glow effect for themes with glow enabled
    glow_css = ""
    if scheme and scheme.effects and scheme.effects.get('glow'):
        glow_css = f"filter: drop-shadow(0 0 20px {scheme.glow_color or scheme.primary}40);"

    return f"""<!DOCTYPE html>
<html>
<head>
    {fonts_link}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            background: {bg_color};
            width: {width + 40}px;
            height: {height + 40}px;
        }}
        body {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        svg {{
            display: block;
            width: {width}px;
            height: {height}px;
            {glow_css}
        }}
    </style>
</head>
<body>
    {svg}
</body>
</html>"""
