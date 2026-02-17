#!/usr/bin/env python3
"""
CLI for Modern Graphics Generator

Usage:
    modern-graphics cycle --title "My Cycle" --steps "Step1,Step2,Step3" --output output.html
    modern-graphics comparison --title "Comparison" --left "Left Title:Step1,Step2" --right "Right Title:Step1,Step2" --output output.html
    modern-graphics grid --title "Grid" --items "Item1,Item2,Item3" --output output.html
    modern-graphics flywheel --title "Flywheel" --elements "Element1,Element2,Element3" --output output.html
    modern-graphics timeline --title "Timeline" --events "2024|Event1,2025|Event2" --output output.html
    modern-graphics pyramid --title "Pyramid" --layers "Layer1,Layer2,Layer3" --output output.html
    modern-graphics before-after --title "Transformation" --before "Item1,Item2" --after "Item3,Item4" --output output.html
    modern-graphics funnel --title "Funnel" --stages "Stage1,Stage2,Stage3" --values "100,80,50" --output output.html
    
    # Insight graphics
    modern-graphics key-insight --text "The key insight text" --label "Key Insight" --output insight.png --png
    modern-graphics insight-card --text "Insight text" --svg-file wireframe.svg --output card.png --png
    modern-graphics insight-story --headline "Main Headline" --before-svg before.svg --after-svg after.svg --output story.png --png
    
    # SVG wireframe generation
    modern-graphics wireframe-svg --type before --output before.svg
    modern-graphics wireframe-svg --type after --output after.svg
    modern-graphics wireframe-svg --type chat-panel --output chat.svg

    # Scene-spec wireframe (preset or JSON spec)
    modern-graphics wireframe-scene --preset before --output before.svg
    modern-graphics wireframe-scene --preset after --theme apple --png --output after.png
    modern-graphics wireframe-scene --spec my_scene.json --output scene.svg

    # Mermaid: render Mermaid diagram to SVG or PNG (requires mermaid-cli)
    modern-graphics mermaid --input diagram.mmd --output diagram.svg
    modern-graphics mermaid --input - --output diagram.svg   # read Mermaid from stdin
    modern-graphics mermaid --input diagram.mmd --output diagram.png --png
    modern-graphics insight-card --text "Insight" --mermaid-file diagram.mmd --output card.html
    modern-graphics modern-hero --title "Doc" --headline "Headline" --mermaid-file diagram.mmd --output hero.html

    # Graphic ideas: "I need some ideas" — interactive interview, stores prompt version
    modern-graphics ideas
    modern-graphics ideas --name launch-graphic --save-dir ./my_prompts
    modern-graphics ideas --no-save

    # Append a note to a prompt file (Notes / changes)
    modern-graphics prompt-note path/to/prompt.md "Use Material icon for rocket"
    echo "Next: align arrows" | modern-graphics prompt-note path/to/prompt.md --no-date

    # From prompt file: generate a story slide from prompt markdown
    modern-graphics from-prompt-file path/to/prompt.md --output prompt-story.html
    modern-graphics from-prompt-file path/to/prompt.md --output prompt-story.png --png
"""

import argparse
import json
import sys
import textwrap
from pathlib import Path
from typing import Optional

from . import (
    ModernGraphicsGenerator,
    Attribution,
    generate_cycle_diagram,
    generate_comparison_diagram,
    generate_grid_diagram,
    generate_flywheel_diagram,
    generate_timeline_diagram,
    generate_pyramid_diagram,
    generate_before_after_diagram,
    generate_funnel_diagram,
    generate_slide_card_diagram,
    generate_slide_card_comparison,
    generate_story_slide,
    create_story_slide_from_prompt,
    generate_modern_hero,
    generate_modern_hero_triptych,
    generate_premium_card,
)
from .diagrams.insight import (
    generate_key_insight,
    generate_insight_card,
    generate_insight_story,
)
from .diagrams.wireframe_svg import (
    WireframeSVGConfig,
    generate_chat_panel_svg,
    generate_modal_form_svg,
    generate_ticket_flow_svg,
    generate_before_wireframe_svg,
    generate_after_wireframe_svg,
)
from .diagrams.wireframe_scene import render_scene, list_presets, SCENE_PRESETS
from .diagrams.wireframe_elements.config import WireframeConfig
from .diagrams.mermaid_svg import mermaid_to_svg
from .color_scheme import get_scheme, list_schemes, ColorScheme
from .cli_clarity import normalize_density, CREATE_DEFAULTS
from .export_policy import ExportPolicy
from .export_presets import list_export_presets, get_export_preset
from .layout_models import (
    HeroPayload,
    ComparisonPayload,
    TimelinePayload,
    FunnelPayload,
    GridPayload,
    KeyInsightPayload,
    InsightCardPayload,
    InsightStoryPayload,
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


def _emit_create_error(layout: str, message: str) -> int:
    print(f"Error: {message}")
    example = CREATE_EXAMPLES.get(layout)
    if example:
        print(f"Hint: try `{example}`")
    return 1


def main():
    parser = argparse.ArgumentParser(description='Generate modern HTML/CSS graphics')
    parser.add_argument('--person', default='Greg Meyer', help='Attribution person name (default: Greg Meyer)')
    parser.add_argument('--website', default='gregmeyer.com', help='Attribution website (default: gregmeyer.com)')
    subparsers = parser.add_subparsers(dest='command', help='Diagram type')

    # Clarity-first create scaffold
    create_parser = subparsers.add_parser(
        'create',
        help='Unified clarity-first creation surface',
        epilog=(
            "Examples:\n"
            "  modern-graphics create --layout hero --headline \"Execution scales\" --output hero.html\n"
            "  modern-graphics create --layout comparison --left \"Before:Manual:Slow\" --right \"After:Agentic:Faster\" --output cmp.html\n"
            "  modern-graphics create --layout insight-card --text \"Key point\" --output card.html"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    create_core = create_parser.add_argument_group('core')
    create_layout = create_parser.add_argument_group('layout-specific')
    create_expert = create_parser.add_argument_group('expert')

    create_core.add_argument('--layout', required=True, choices=['hero', 'insight', 'key-insight', 'insight-card', 'insight-story', 'comparison', 'story', 'timeline', 'funnel', 'grid'], help='Layout family to generate')
    create_core.add_argument('--output', required=True, help='Output HTML/PNG path')
    create_core.add_argument('--title', default='Modern Graphic', help='Graphic title scope')
    create_core.add_argument('--theme', choices=list_schemes(), default=CREATE_DEFAULTS.theme, help=f'Color theme (default: {CREATE_DEFAULTS.theme})')

    create_layout.add_argument('--headline', help='Headline (hero/story/insight-story)')
    create_layout.add_argument('--subheadline', help='Subheadline (hero/story/insight-story)')
    create_layout.add_argument('--eyebrow', help='Eyebrow/tagline')
    create_layout.add_argument('--highlights', help='Comma-separated highlights (hero)')
    create_layout.add_argument('--text', help='Insight text (key-insight/insight-card)')
    create_layout.add_argument('--label', default='Key Insight', help='Insight label (key-insight/insight-card/insight-story)')
    create_layout.add_argument('--variant', default='bold', help='Insight variant (key-insight: default|minimal|bold|quote, insight-card: default|bold)')
    create_layout.add_argument('--icon', default='lightning', help='Insight icon (lightning|lightbulb|quote|star|none)')
    create_layout.add_argument('--svg-file', help='Path to SVG file (insight-card or insight-story panels)')
    create_layout.add_argument('--svg-label', help='SVG label (insight-card)')
    create_layout.add_argument('--svg-layout', default='side-by-side', choices=['side-by-side', 'stacked'], help='Insight card layout (default: side-by-side)')
    create_layout.add_argument('--svg-position', default='right', choices=['left', 'right'], help='Insight card SVG position (default: right)')
    create_layout.add_argument('--before-svg', help='Path to before SVG (insight-story)')
    create_layout.add_argument('--after-svg', help='Path to after SVG (insight-story)')
    create_layout.add_argument('--insight-text', help='Insight story key insight text')
    create_layout.add_argument('--before-label', default='Before', help='Insight story before label')
    create_layout.add_argument('--after-label', default='After', help='Insight story after label')
    create_layout.add_argument('--left', help='Left column payload for comparison: \"Title:Step1,Step2:Outcome\"')
    create_layout.add_argument('--right', help='Right column payload for comparison: \"Title:Step1,Step2:Outcome\"')
    create_layout.add_argument('--events', help='Timeline events: \"Date|Event,Date|Event\"')
    create_layout.add_argument('--orientation', choices=['horizontal', 'vertical'], default='horizontal', help='Timeline orientation (default: horizontal)')
    create_layout.add_argument('--stages', help='Funnel stages: \"Stage1,Stage2,Stage3\"')
    create_layout.add_argument('--values', help='Funnel values: \"100,70,30\"')
    create_layout.add_argument('--percentages', action='store_true', help='Show funnel percentages')
    create_layout.add_argument('--items', help='Grid items: \"Item1,Item2,Item3\"')
    create_layout.add_argument('--columns', type=int, default=5, help='Grid column count (default: 5)')
    create_layout.add_argument('--goal', help='Grid convergence goal (optional)')
    create_layout.add_argument('--outcome', help='Grid convergence outcome (optional)')
    create_layout.add_argument('--what-changed', help='Story field: what changed')
    create_layout.add_argument('--time-period', help='Story field: over what period')
    create_layout.add_argument('--what-it-means', help='Story field: why it matters')

    create_expert.add_argument('--density', default=CREATE_DEFAULTS.density, choices=['clarity', 'balanced', 'dense'], help=f'Density mode (default: {CREATE_DEFAULTS.density})')
    create_expert.add_argument('--png', action='store_true', help='Export as PNG')
    create_expert.add_argument('--export-preset', choices=list_export_presets(), help='Channel preset for PNG export (linkedin|x|substack-hero)')
    create_expert.add_argument('--crop-mode', choices=['none', 'safe', 'tight'], default=CREATE_DEFAULTS.crop_mode, help=f'PNG crop mode (default: {CREATE_DEFAULTS.crop_mode})')
    create_expert.add_argument('--padding-mode', choices=['none', 'minimal', 'comfortable'], default=CREATE_DEFAULTS.padding_mode, help=f'PNG padding mode (default: {CREATE_DEFAULTS.padding_mode})')

    # Cycle diagram
    cycle_parser = subparsers.add_parser('cycle', help='Generate cycle diagram')
    cycle_parser.add_argument('--title', required=True, help='Diagram title')
    cycle_parser.add_argument('--steps', required=True, help='Comma-separated list of steps')
    cycle_parser.add_argument('--arrow', default='→', help='Arrow text (default: →)')
    cycle_parser.add_argument('--cycle-end', help='Text to display after cycle (e.g., "(repeat)")')
    cycle_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    cycle_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    cycle_parser.add_argument('--context', help='Optional context line for attribution')
    cycle_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    cycle_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    cycle_parser.add_argument('--no-loop', action='store_true', help='Hide the loop-back (↻) indicator after the last step')
    
    # Comparison diagram
    comp_parser = subparsers.add_parser('comparison', help='Generate comparison diagram')
    comp_parser.add_argument('--title', required=True, help='Diagram title')
    comp_parser.add_argument('--left', required=True, help='Left column: "Title:Step1,Step2:Outcome"')
    comp_parser.add_argument('--right', required=True, help='Right column: "Title:Step1,Step2:Outcome"')
    comp_parser.add_argument('--vs', default='vs', help='VS text (default: vs)')
    comp_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    comp_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    comp_parser.add_argument('--context', help='Optional context line for attribution')
    comp_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    comp_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    
    # Grid diagram
    grid_parser = subparsers.add_parser('grid', help='Generate grid diagram')
    grid_parser.add_argument('--title', required=True, help='Diagram title')
    grid_parser.add_argument('--items', required=True, help='Comma-separated list of items')
    grid_parser.add_argument('--columns', type=int, default=5, help='Number of columns (default: 5)')
    grid_parser.add_argument('--goal', help='Goal text for convergence section')
    grid_parser.add_argument('--outcome', help='Outcome text for convergence section')
    grid_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    grid_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    grid_parser.add_argument('--context', help='Optional context line for attribution')
    grid_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    grid_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    grid_parser.add_argument('--density', choices=['clarity', 'balanced', 'dense'], default=CREATE_DEFAULTS.density, help=f'Density mode (default: {CREATE_DEFAULTS.density})')
    
    # Flywheel diagram
    flywheel_parser = subparsers.add_parser('flywheel', help='Generate flywheel diagram')
    flywheel_parser.add_argument('--title', required=True, help='Diagram title')
    flywheel_parser.add_argument('--elements', required=True, help='Comma-separated list of elements')
    flywheel_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    flywheel_parser.add_argument('--center', help='Optional center label')
    flywheel_parser.add_argument('--radius', type=int, default=200, help='Circle radius in pixels (default: 200)')
    flywheel_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    flywheel_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    flywheel_parser.add_argument('--context', help='Optional context line for attribution')
    flywheel_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    flywheel_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    
    # Timeline diagram
    timeline_parser = subparsers.add_parser('timeline', help='Generate timeline diagram')
    timeline_parser.add_argument('--title', required=True, help='Diagram title')
    timeline_parser.add_argument('--events', required=True, help='Comma-separated list of events in format "Date|Text" or "Date:Text"')
    timeline_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    timeline_parser.add_argument('--orientation', choices=['horizontal', 'vertical'], default='horizontal', help='Timeline orientation (default: horizontal)')
    timeline_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    timeline_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    timeline_parser.add_argument('--context', help='Optional context line for attribution')
    timeline_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    timeline_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    timeline_parser.add_argument('--density', choices=['clarity', 'balanced', 'dense'], default=CREATE_DEFAULTS.density, help=f'Density mode (default: {CREATE_DEFAULTS.density})')

    # Pyramid diagram
    pyramid_parser = subparsers.add_parser('pyramid', help='Generate pyramid diagram')
    pyramid_parser.add_argument('--title', required=True, help='Diagram title')
    pyramid_parser.add_argument('--layers', required=True, help='Comma-separated list of layers (top to bottom)')
    pyramid_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    pyramid_parser.add_argument('--orientation', choices=['up', 'down'], default='up', help='Pyramid orientation - up (pointing up) or down (pointing down) (default: up)')
    pyramid_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    pyramid_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    pyramid_parser.add_argument('--context', help='Optional context line for attribution')
    pyramid_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    pyramid_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Before/After diagram
    before_after_parser = subparsers.add_parser('before-after', help='Generate before/after diagram')
    before_after_parser.add_argument('--title', required=True, help='Diagram title')
    before_after_parser.add_argument('--before', required=True, help='Comma-separated list of "before" items')
    before_after_parser.add_argument('--after', required=True, help='Comma-separated list of "after" items')
    before_after_parser.add_argument('--transition', default='→', help='Transition text between states (default: →)')
    before_after_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    before_after_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    before_after_parser.add_argument('--context', help='Optional context line for attribution')
    before_after_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Funnel diagram
    funnel_parser = subparsers.add_parser('funnel', help='Generate funnel diagram')
    funnel_parser.add_argument('--title', required=True, help='Diagram title')
    funnel_parser.add_argument('--stages', required=True, help='Comma-separated list of stage names')
    funnel_parser.add_argument('--values', help='Comma-separated list of numeric values for each stage')
    funnel_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    funnel_parser.add_argument('--percentages', action='store_true', help='Display percentages instead of values')
    funnel_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    funnel_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    funnel_parser.add_argument('--context', help='Optional context line for attribution')
    funnel_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    funnel_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Slide card diagram
    slide_cards_parser = subparsers.add_parser('slide-cards', help='Generate slide card diagram (horizontal transformation)')
    slide_cards_parser.add_argument('--title', required=True, help='Diagram title')
    slide_cards_parser.add_argument('--cards', required=True, help='JSON string with cards array: [{"title":"...","tagline":"...","subtext":"...","filename":"...","color":"blue|green|purple|gray","features":["..."],"badge":"..."}]')
    slide_cards_parser.add_argument('--arrow', default='→', help='Arrow text between cards (default: →)')
    slide_cards_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    slide_cards_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    slide_cards_parser.add_argument('--context', help='Optional context line for attribution')
    slide_cards_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    slide_cards_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Slide card comparison
    slide_compare_parser = subparsers.add_parser('slide-compare', help='Generate slide card comparison (side-by-side)')
    slide_compare_parser.add_argument('--title', required=True, help='Diagram title')
    slide_compare_parser.add_argument('--left', required=True, help='JSON string with left card: {"title":"...","tagline":"...","color":"...","features":["..."],"badge":"..."}')
    slide_compare_parser.add_argument('--right', required=True, help='JSON string with right card: {"title":"...","tagline":"...","color":"...","features":["..."],"badge":"..."}')
    slide_compare_parser.add_argument('--vs', default='→', help='VS text between cards (default: →)')
    slide_compare_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    slide_compare_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    slide_compare_parser.add_argument('--context', help='Optional context line for attribution')
    slide_compare_parser.add_argument('--theme', help='Theme name (apple, corporate, dark, warm, green, arcade, nike)')
    slide_compare_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Premium stacked card
    premium_card_parser = subparsers.add_parser('premium-card', help='Generate stacked premium card (hero + detail panels)')
    premium_card_parser.add_argument('--title', required=True, help='Document title / default card headline')
    premium_card_parser.add_argument('--config', required=True, help='Path to JSON file or raw JSON describing the card payload')
    premium_card_parser.add_argument('--size', type=int, default=1100, help='Square canvas size in pixels (default: 1100)')
    premium_card_parser.add_argument('--top-only', action='store_true', help='Render only the top/hero panel')
    premium_card_parser.add_argument('--bottom-only', action='store_true', help='Render only the bottom/detail panel')
    premium_card_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    premium_card_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    premium_card_parser.add_argument('--context', help='Optional context line for attribution')
    premium_card_parser.add_argument('--png', action='store_true', help='Export as PNG')
    
    # Story-driven slide
    story_slide_parser = subparsers.add_parser('story-slide', help='Generate compelling story-driven slide (What changed, time period, what it means)')
    story_slide_parser.add_argument('--title', required=True, help='Slide title')
    story_slide_parser.add_argument('--what-changed', required=True, help='What changed (the change)')
    story_slide_parser.add_argument('--time-period', required=True, help='Over what time period')
    story_slide_parser.add_argument('--what-it-means', required=True, help='What it means (the meaning/implication)')
    story_slide_parser.add_argument('--insight', help='Optional key insight/takeaway')
    story_slide_parser.add_argument('--evolution-data', help='JSON array of evolution stages: [{"era":"2010s","label":"Manual Slides","icon":"📊"}]')
    story_slide_parser.add_argument('--top-tile-only', action='store_true', help='Render only the hero/top tile')
    story_slide_parser.add_argument('--hero-variant', choices=['auto', 'light', 'dark'], default='auto', help='Force hero panel variant (default: auto)')
    story_slide_parser.add_argument('--hero-svg-js', action='store_true', help='Render hero mockup using SVG.js')
    story_slide_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    story_slide_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    story_slide_parser.add_argument('--context', help='Optional context line for attribution')
    story_slide_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML')
    story_slide_parser.add_argument('--density', choices=['clarity', 'balanced', 'dense'], default=CREATE_DEFAULTS.density, help=f'Density mode (default: {CREATE_DEFAULTS.density})')

    # Modern hero (open)
    modern_hero_parser = subparsers.add_parser('modern-hero', help='Generate modern open hero layout')
    modern_hero_parser.add_argument('--title', required=True, help='Document title scope')
    modern_hero_parser.add_argument('--headline', required=True, help='Hero headline')
    modern_hero_parser.add_argument('--subheadline', help='Supporting line')
    modern_hero_parser.add_argument('--eyebrow', help='Eyebrow/tagline')
    modern_hero_parser.add_argument('--highlights', help='Comma-separated highlight list')
    modern_hero_parser.add_argument('--highlight-tiles', help='JSON array of tile objects ({"label": "...", "icon": "manual"})')
    modern_hero_parser.add_argument('--flow-nodes', help='JSON array describing flow nodes for a freeform layout')
    modern_hero_parser.add_argument('--flow-connections', help='Optional JSON array of {\"from\":\"id\",\"to\":\"id\"} connections')
    modern_hero_parser.add_argument('--freeform-canvas', help='Raw HTML/SVG snippet to inject into the hero body')
    modern_hero_parser.add_argument('--mermaid-file', help='Path to Mermaid .mmd file; render to SVG and inject into hero body (requires mermaid-cli)')
    modern_hero_parser.add_argument('--mermaid-font', help='Font family for the Mermaid diagram (e.g. Roboto, "Georgia, serif")')
    modern_hero_parser.add_argument('--theme', choices=list_schemes(), help=f'Color theme for hero and Mermaid diagram: {", ".join(list_schemes())}')
    modern_hero_parser.add_argument('--stats', help='Comma-separated stats in Label:Value format')
    modern_hero_parser.add_argument('--cta', help='CTA copy')
    modern_hero_parser.add_argument('--visual-description', help='Optional freeform description (keywords like "curved arrow" or "glassmorphism")')
    modern_hero_parser.add_argument('--background', default='light', choices=['light', 'dark'], help='Background variant (default: light)')
    modern_hero_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    modern_hero_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    modern_hero_parser.add_argument('--context', help='Optional context line for attribution')
    modern_hero_parser.add_argument('--png', action='store_true', help='Export as PNG')

    # Modern hero triptych
    modern_triptych_parser = subparsers.add_parser('modern-hero-triptych', help='Generate modern hero triptych layout')
    modern_triptych_parser.add_argument('--title', required=True, help='Document title scope')
    modern_triptych_parser.add_argument('--headline', required=True, help='Hero headline')
    modern_triptych_parser.add_argument('--subheadline', help='Supporting line')
    modern_triptych_parser.add_argument('--columns', required=True, help='JSON array describing the three columns (title, items[], optional icon)')
    modern_triptych_parser.add_argument('--stats', help='Comma-separated stats in Label:Value format')
    modern_triptych_parser.add_argument('--eyebrow', help='Eyebrow/tagline')
    modern_triptych_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    modern_triptych_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    modern_triptych_parser.add_argument('--context', help='Optional context line for attribution')
    modern_triptych_parser.add_argument('--png', action='store_true', help='Export as PNG')
    
    # Modern hero from prompt (JSON)
    hero_prompt_parser = subparsers.add_parser('modern-hero-prompt', help='Generate modern hero layout from JSON prompt file')
    hero_prompt_parser.add_argument('--title', default='Modern Hero Prompt', help='Document title scope')
    hero_prompt_parser.add_argument('--prompt-file', required=True, help='Path to JSON prompt describing the hero (layout, headline, stats, etc.)')
    hero_prompt_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    hero_prompt_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    hero_prompt_parser.add_argument('--context', help='Optional context line for attribution')
    hero_prompt_parser.add_argument('--png', action='store_true', help='Export as PNG')
    
    # =========================================================================
    # Insight Graphics
    # =========================================================================
    
    # Key Insight (standalone pull quote)
    key_insight_parser = subparsers.add_parser('key-insight', help='Generate standalone key insight / pull quote')
    key_insight_parser.add_argument('--title', default='Key Insight', help='Document title')
    key_insight_parser.add_argument('--text', required=True, help='The insight text (supports HTML: <strong>, <em>, <span class="highlight">)')
    key_insight_parser.add_argument('--label', default='Key Insight', help='Label above the insight (default: Key Insight)')
    key_insight_parser.add_argument('--eyebrow', help='Optional eyebrow text above label')
    key_insight_parser.add_argument('--context', help='Optional context text below insight (e.g., source attribution)')
    key_insight_parser.add_argument('--variant', default='default', choices=['default', 'minimal', 'bold', 'quote'], help='Style variant (default: default)')
    key_insight_parser.add_argument('--icon', default='lightning', choices=['lightning', 'lightbulb', 'quote', 'star', 'none'], help='Icon type (default: lightning)')
    key_insight_parser.add_argument('--accent-color', default='#0071e3', help='Accent color (default: #0071e3)')
    key_insight_parser.add_argument('--theme', choices=list_schemes(), help=f'Color theme: {", ".join(list_schemes())}')
    key_insight_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    key_insight_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    key_insight_parser.add_argument('--png', action='store_true', help='Export as PNG')
    key_insight_parser.add_argument('--square', action='store_true', help='Export PNG as square (use with --png)')
    key_insight_parser.add_argument('--size', type=int, default=800, help='Side length in pixels for square export (default: 800). Used with --square.')
    key_insight_parser.add_argument('--padding', type=int, default=10, help='PNG padding in pixels (default: 10 for inline use)')
    
    # Insight Card (insight + SVG illustration)
    insight_card_parser = subparsers.add_parser('insight-card', help='Generate insight card with SVG illustration')
    insight_card_parser.add_argument('--title', default='Insight Card', help='Document title')
    insight_card_parser.add_argument('--text', required=True, help='The insight text (supports HTML)')
    insight_card_parser.add_argument('--svg-file', help='Path to SVG file to embed')
    insight_card_parser.add_argument('--svg-type', choices=['before', 'after', 'chat-panel', 'modal-form'], help='Generate SVG wireframe of this type instead of using --svg-file')
    insight_card_parser.add_argument('--mermaid-file', help='Path to Mermaid .mmd file; render to SVG and use as illustration (requires mermaid-cli)')
    insight_card_parser.add_argument('--mermaid-font', help='Font family for the Mermaid diagram (e.g. Roboto, "Georgia, serif")')
    insight_card_parser.add_argument('--label', default='Key Insight', help='Label above the insight')
    insight_card_parser.add_argument('--svg-label', help='Label above the SVG')
    insight_card_parser.add_argument('--eyebrow', help='Optional eyebrow text')
    insight_card_parser.add_argument('--context', help='Optional context text below insight')
    insight_card_parser.add_argument('--layout', default='side-by-side', choices=['side-by-side', 'stacked'], help='Layout style (default: side-by-side)')
    insight_card_parser.add_argument('--svg-position', default='right', choices=['left', 'right'], help='SVG position for side-by-side (default: right)')
    insight_card_parser.add_argument('--variant', default='bold', choices=['default', 'bold'], help='Insight style variant (default: bold)')
    insight_card_parser.add_argument('--icon', default='lightning', choices=['lightning', 'lightbulb', 'quote', 'star', 'none'], help='Icon type (default: lightning)')
    insight_card_parser.add_argument('--accent-color', default='#0071e3', help='Accent color (default: #0071e3)')
    insight_card_parser.add_argument('--theme', choices=list_schemes(), help=f'Color theme: {", ".join(list_schemes())}')
    insight_card_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    insight_card_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    insight_card_parser.add_argument('--png', action='store_true', help='Export as PNG')
    insight_card_parser.add_argument('--square', action='store_true', help='Export PNG as square (use with --png)')
    insight_card_parser.add_argument('--size', type=int, default=800, help='Side length in pixels for square export (default: 800). Used with --square.')
    insight_card_parser.add_argument('--padding', type=int, default=10, help='PNG padding in pixels (default: 10)')
    
    # Insight Story (full graphic with before/after + insight + stats)
    insight_story_parser = subparsers.add_parser('insight-story', help='Generate full insight story with before/after comparison')
    insight_story_parser.add_argument('--title', default='Insight Story', help='Document title')
    insight_story_parser.add_argument('--headline', required=True, help='Main headline')
    insight_story_parser.add_argument('--subtitle', help='Subtitle text')
    insight_story_parser.add_argument('--eyebrow', help='Eyebrow text above headline')
    insight_story_parser.add_argument('--before-svg', help='Path to "before" SVG file (or use --generate-wireframes)')
    insight_story_parser.add_argument('--before-label', default='Before', help='Label for before panel')
    insight_story_parser.add_argument('--before-status', help='Status text for before panel (prefix with - for negative, + for positive)')
    insight_story_parser.add_argument('--after-svg', help='Path to "after" SVG file (or use --generate-wireframes)')
    insight_story_parser.add_argument('--after-label', default='After', help='Label for after panel')
    insight_story_parser.add_argument('--after-status', help='Status text for after panel')
    insight_story_parser.add_argument('--generate-wireframes', action='store_true', help='Auto-generate before/after wireframe SVGs')
    insight_story_parser.add_argument('--shift-from', help='Left side of shift badge (e.g., "Tickets")')
    insight_story_parser.add_argument('--shift-to', help='Right side of shift badge (e.g., "Control")')
    insight_story_parser.add_argument('--shift-badge', help='Additional badge text')
    insight_story_parser.add_argument('--insight-text', help='Key insight text (supports HTML)')
    insight_story_parser.add_argument('--insight-label', default='Key Insight', help='Label above insight')
    insight_story_parser.add_argument('--stats', help='Comma-separated stats in Label:Value format')
    insight_story_parser.add_argument('--accent-color', default='#0071e3', help='Accent color')
    insight_story_parser.add_argument('--theme', choices=list_schemes(), help=f'Color theme: {", ".join(list_schemes())}')
    insight_story_parser.add_argument('--output', required=True, help='Output HTML/PNG path')
    insight_story_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    insight_story_parser.add_argument('--png', action='store_true', help='Export as PNG')
    insight_story_parser.add_argument('--padding', type=int, default=10, help='PNG padding in pixels (default: 10)')
    
    # =========================================================================
    # SVG Wireframe Generation
    # =========================================================================
    
    wireframe_svg_parser = subparsers.add_parser('wireframe-svg', help='Generate pure SVG wireframes')
    wireframe_svg_parser.add_argument('--type', required=True, choices=['before', 'after', 'chat-panel', 'modal-form', 'ticket-flow'], help='Wireframe type')
    wireframe_svg_parser.add_argument('--width', type=int, default=400, help='SVG width (default: 400)')
    wireframe_svg_parser.add_argument('--height', type=int, default=300, help='SVG height (default: 300)')
    wireframe_svg_parser.add_argument('--accent-color', default='#0071e3', help='Accent color (default: #0071e3)')
    wireframe_svg_parser.add_argument('--theme', choices=list_schemes(), help=f'Color theme: {", ".join(list_schemes())}')
    wireframe_svg_parser.add_argument('--output', required=True, help='Output SVG/PNG path')
    wireframe_svg_parser.add_argument('--copyright', default=None, help='Override attribution line (default: © --person YEAR • --website)')
    wireframe_svg_parser.add_argument('--png', action='store_true', help='Export as PNG instead of SVG')
    wireframe_svg_parser.add_argument('--padding', type=int, default=10, help='PNG padding in pixels (default: 10)')
    # Chat panel specific options
    wireframe_svg_parser.add_argument('--messages', help='JSON array of messages: [{"role":"user","text":"..."},{"role":"assistant","text":"..."}]')
    wireframe_svg_parser.add_argument('--inline-card', help='JSON object for inline card: {"title":"...","status":"...","progress":75}')
    wireframe_svg_parser.add_argument('--action-buttons', help='Comma-separated button labels')
    wireframe_svg_parser.add_argument('--success-toast', help='JSON object: {"title":"...","subtitle":"..."}')
    # Modal form specific options
    wireframe_svg_parser.add_argument('--modal-title', default='Support Request', help='Modal title')
    wireframe_svg_parser.add_argument('--fields', help='Comma-separated field labels')
    wireframe_svg_parser.add_argument('--submit-label', default='Submit', help='Submit button text')

    # Scene-spec wireframe: preset or custom JSON spec
    wireframe_scene_parser = subparsers.add_parser('wireframe-scene', help='Render wireframe from scene preset or JSON spec')
    wireframe_scene_parser.add_argument('--preset', choices=list_presets(), help='Preset name (e.g. before, after)')
    wireframe_scene_parser.add_argument('--spec', help='Path to JSON file with width, height, elements')
    wireframe_scene_parser.add_argument('--theme', choices=list_schemes(), help=f'Color theme: {", ".join(list_schemes())}')
    wireframe_scene_parser.add_argument('--output', required=True, help='Output SVG/PNG path')
    wireframe_scene_parser.add_argument('--png', action='store_true', help='Export as PNG instead of SVG')
    wireframe_scene_parser.add_argument('--padding', type=int, default=10, help='PNG padding in pixels (default: 10)')

    # Mermaid: render Mermaid source to SVG (or PNG)
    mermaid_parser = subparsers.add_parser('mermaid', help='Render Mermaid diagram to SVG or PNG')
    mermaid_parser.add_argument('--input', required=True, help='Path to .mmd file, or "-" to read Mermaid from stdin')
    mermaid_parser.add_argument('--output', required=True, help='Output SVG or PNG path')
    mermaid_parser.add_argument('--theme', choices=list_schemes(), help=f'Apply color theme to diagram: {", ".join(list_schemes())}')
    mermaid_parser.add_argument('--font', help='Font family for the diagram (e.g. Roboto, "Georgia, serif"). Overrides theme font when --theme is set.')
    mermaid_parser.add_argument('--width', type=int, help='SVG width (passed to mermaid-cli)')
    mermaid_parser.add_argument('--height', type=int, help='SVG height (passed to mermaid-cli)')
    mermaid_parser.add_argument('--png', action='store_true', help='Export as PNG instead of SVG')
    mermaid_parser.add_argument('--padding', type=int, default=10, help='PNG padding in pixels (default: 10)')

    # Graphic ideas interview: "I need some ideas" → prompts you, stores prompt version
    ideas_parser = subparsers.add_parser(
        'ideas',
        help='Run graphic ideas interview; prompt collects format, subject, theme, etc., and saves a prompt version',
    )
    ideas_parser.add_argument(
        '--save-dir',
        type=Path,
        default=None,
        help='Directory to save prompt version (default: ./prompt_versions or MODERN_GRAPHICS_PROMPTS_DIR)',
    )
    ideas_parser.add_argument(
        '--name',
        type=str,
        default=None,
        help='Name for the saved file (e.g. launch-graphic); default is timestamp',
    )
    ideas_parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save to file; only print the built prompt',
    )

    # From prompt file: generate a story slide from markdown prompt text
    from_prompt_parser = subparsers.add_parser(
        'from-prompt-file',
        help='Generate a story slide from prompt markdown text',
    )
    from_prompt_parser.add_argument(
        'prompt_file',
        type=Path,
        help='Path to prompt markdown file',
    )
    from_prompt_parser.add_argument(
        '--title',
        default='Prompt Story',
        help='Document title (default: Prompt Story)',
    )
    from_prompt_parser.add_argument(
        '--model',
        default='gpt-4-turbo-preview',
        help='OpenAI model for extraction/composition (default: gpt-4-turbo-preview)',
    )
    from_prompt_parser.add_argument(
        '--theme',
        choices=list_schemes(),
        help=f'Optional color theme for output: {", ".join(list_schemes())}',
    )
    from_prompt_parser.add_argument(
        '--output',
        required=True,
        help='Output HTML/PNG path',
    )
    from_prompt_parser.add_argument(
        '--png',
        action='store_true',
        help='Export as PNG instead of HTML',
    )

    # Append a note to a prompt file (Notes / changes)
    prompt_note_parser = subparsers.add_parser(
        'prompt-note',
        help='Append a note to a prompt markdown file (Notes / changes section)',
    )
    prompt_note_parser.add_argument(
        'prompt_file',
        type=Path,
        help='Path to prompt .md file to update',
    )
    prompt_note_parser.add_argument(
        'note',
        type=str,
        nargs='?',
        default=None,
        help='Note text to append (e.g. "Use Material icon for rocket"). If omitted, read from stdin.',
    )
    prompt_note_parser.add_argument(
        '--date',
        action='store_true',
        default=True,
        help='Prepend today\'s date to the note (default: True)',
    )
    prompt_note_parser.add_argument(
        '--no-date',
        action='store_true',
        help='Do not prepend a date to the note',
    )
    
    adapted_argv, alias_warning = _adapt_legacy_command_aliases(list(sys.argv))
    args = parser.parse_args(adapted_argv[1:])
    
    if not args.command:
        parser.print_help()
        return 1

    if alias_warning:
        print(alias_warning, file=sys.stderr)

    if args.command == 'ideas':
        from .graphic_ideas_interview import run_graphic_ideas_interview
        run_graphic_ideas_interview(
            save_dir=getattr(args, 'save_dir', None),
            prompt_name=getattr(args, 'name', None),
            skip_save=getattr(args, 'no_save', False),
        )
        return 0

    if args.command == 'prompt-note':
        from datetime import date
        prompt_path = Path(getattr(args, 'prompt_file')).resolve()
        if not prompt_path.exists():
            print(f"Error: prompt file not found: {prompt_path}")
            return 1
        note = getattr(args, 'note', None)
        if note is None or note.strip() == "":
            note = sys.stdin.read().strip()
        if not note:
            print("Error: no note provided (pass as argument or via stdin)")
            return 1
        add_date = not getattr(args, 'no_date', False)
        if add_date:
            note = f"- **{date.today().isoformat()}:** {note}"
        else:
            note = f"- {note}"
        content = prompt_path.read_text(encoding='utf-8')
        section = "## Notes / changes"
        if section in content:
            content = content.rstrip() + "\n" + note + "\n"
        else:
            content = content.rstrip() + "\n\n---\n\n" + section + "\n\n" + note + "\n"
        prompt_path.write_text(content, encoding='utf-8')
        print(f"Appended note to: {prompt_path}")
        return 0

    if args.command == 'from-prompt-file':
        prompt_path = Path(args.prompt_file).resolve()
        if not prompt_path.exists():
            print(f"Error: prompt file not found: {prompt_path}")
            return 1

        prompt_text = prompt_path.read_text(encoding='utf-8').strip()
        if not prompt_text:
            print(f"Error: prompt file is empty: {prompt_path}")
            return 1

        output_path = Path(args.output)
        if args.png and output_path.suffix != '.png':
            output_path = output_path.with_suffix('.png')

        attribution = Attribution(
            person=getattr(args, 'person', 'Greg Meyer'),
            website=getattr(args, 'website', 'gregmeyer.com'),
        )
        generator = ModernGraphicsGenerator(args.title, attribution=attribution)
        html = create_story_slide_from_prompt(generator, prompt_text, model=args.model)

        theme = getattr(args, 'theme', None)
        if theme:
            html = get_scheme(theme).apply_to_html(html)

        if args.png:
            generator.export_to_png(html, output_path, padding=10)
            print(f"Generated from-prompt-file PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated from-prompt-file HTML: {output_path}")
        return 0

    if args.command == 'create':
        output_path = Path(args.output)
        attribution = Attribution(
            person=getattr(args, 'person', 'Greg Meyer'),
            website=getattr(args, 'website', 'gregmeyer.com'),
        )
        if getattr(args, 'png', False) and output_path.suffix != '.png':
            output_path = output_path.with_suffix('.png')

        generator = ModernGraphicsGenerator(
            getattr(args, 'title', 'Modern Graphic'),
            attribution=attribution,
        )
        density = normalize_density(getattr(args, "density", "clarity"))
        color_scheme = get_scheme(getattr(args, 'theme', None)) if getattr(args, 'theme', None) else None

        layout_type = args.layout
        if layout_type == "insight":
            layout_type = "key-insight"

        payload = {}
        if args.layout == "hero":
            highlights = parse_highlights_arg(getattr(args, "highlights", None))
            if density == "clarity" and highlights:
                highlights = highlights[:3]
            try:
                payload = HeroPayload(
                    headline=args.headline or "Execution scales. Judgment stays scarce.",
                    subheadline=getattr(args, "subheadline", None),
                    eyebrow=getattr(args, "eyebrow", None),
                    highlights=highlights,
                    background_variant="light",
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout in {"insight", "key-insight"}:
            if not getattr(args, "text", None):
                return _emit_create_error(args.layout, "--text is required for this layout")
            key_variant = getattr(args, "variant", None) or ("bold" if density != "dense" else "default")
            try:
                payload = KeyInsightPayload(
                    text=args.text,
                    label=getattr(args, "label", "Key Insight"),
                    variant=key_variant,
                    icon=getattr(args, "icon", "lightning"),
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout == "insight-card":
            if not getattr(args, "text", None):
                return _emit_create_error(args.layout, "--text is required for this layout")
            svg_content = None
            if getattr(args, "svg_file", None):
                svg_path = Path(args.svg_file)
                if not svg_path.exists():
                    return _emit_create_error(args.layout, f"SVG file not found: {svg_path}")
                svg_content = svg_path.read_text(encoding="utf-8")
            else:
                cfg = get_wireframe_config_from_theme(getattr(args, "theme", None), width=360, height=260)
                svg_content = generate_after_wireframe_svg(cfg)
            card_variant = getattr(args, "variant", None) or ("bold" if density != "dense" else "default")
            try:
                payload = InsightCardPayload(
                    text=args.text,
                    svg_content=svg_content,
                    label=getattr(args, "label", "Key Insight"),
                    svg_label=getattr(args, "svg_label", None),
                    layout=getattr(args, "svg_layout", "side-by-side"),
                    svg_position=getattr(args, "svg_position", "right"),
                    variant=card_variant,
                    icon=getattr(args, "icon", "lightning"),
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout == "insight-story":
            before_svg = None
            after_svg = None
            if getattr(args, "before_svg", None):
                before_path = Path(args.before_svg)
                if not before_path.exists():
                    return _emit_create_error(args.layout, f"before SVG file not found: {before_path}")
                before_svg = before_path.read_text(encoding="utf-8")
            if getattr(args, "after_svg", None):
                after_path = Path(args.after_svg)
                if not after_path.exists():
                    return _emit_create_error(args.layout, f"after SVG file not found: {after_path}")
                after_svg = after_path.read_text(encoding="utf-8")
            if before_svg is None or after_svg is None:
                cfg = get_wireframe_config_from_theme(getattr(args, "theme", None), width=360, height=260)
                before_svg = before_svg or generate_before_wireframe_svg(cfg)
                after_svg = after_svg or generate_after_wireframe_svg(cfg)
            try:
                payload = InsightStoryPayload(
                    headline=args.headline or "Execution scales. Judgment does not.",
                    insight_text=getattr(args, "insight_text", None) or args.text or "Use explicit gates to decide what ships.",
                    before_svg=before_svg,
                    after_svg=after_svg,
                    subtitle=getattr(args, "subheadline", None),
                    eyebrow=getattr(args, "eyebrow", None),
                    before_label=getattr(args, "before_label", "Before"),
                    after_label=getattr(args, "after_label", "After"),
                    insight_label=getattr(args, "label", "Key Insight"),
                    stats=parse_stats_arg(getattr(args, "stats", None)),
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout == "comparison":
            if not getattr(args, "left", None) or not getattr(args, "right", None):
                return _emit_create_error(args.layout, "--left and --right are required for this layout")
            try:
                payload = ComparisonPayload(
                    left_column=parse_column(args.left),
                    right_column=parse_column(args.right),
                    vs_text="vs",
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout == "story":
            story_what_changed, story_time_period, story_what_it_means = shape_story_fields_for_density(
                getattr(args, "what_changed", None) or "Execution capacity increased",
                getattr(args, "time_period", None) or "this quarter",
                getattr(args, "what_it_means", None) or "Decision quality now drives outcomes",
                density,
            )
            payload = {
                "title": args.title,
                "what_changed": story_what_changed,
                "time_period": story_time_period,
                "what_it_means": story_what_it_means,
                "insight": getattr(args, "headline", None),
            }
        elif args.layout == "timeline":
            if not getattr(args, "events", None):
                return _emit_create_error(args.layout, "--events is required for this layout")
            try:
                timeline_events = shape_timeline_events_for_density(
                    parse_timeline_events(args.events),
                    density,
                )
                payload = TimelinePayload(
                    events=timeline_events,
                    orientation=getattr(args, "orientation", "horizontal"),
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout == "funnel":
            if not getattr(args, "stages", None):
                return _emit_create_error(args.layout, "--stages is required for this layout")
            try:
                payload = FunnelPayload(
                    stages=parse_funnel_stages(args.stages, getattr(args, "values", None)),
                    show_percentages=bool(getattr(args, "percentages", False)),
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        elif args.layout == "grid":
            if not getattr(args, "items", None):
                return _emit_create_error(args.layout, "--items is required for this layout")
            grid_items, grid_columns = shape_grid_for_density(
                parse_items(args.items),
                getattr(args, "columns", 5),
                density,
            )
            convergence = None
            if getattr(args, "goal", None) or getattr(args, "outcome", None):
                convergence = {
                    "goal": textwrap.shorten(getattr(args, "goal", None) or "", width=44, placeholder="..."),
                    "outcome": textwrap.shorten(getattr(args, "outcome", None) or "", width=44, placeholder="..."),
                }
            try:
                payload = GridPayload(
                    items=grid_items,
                    columns=grid_columns,
                    convergence=convergence,
                    color_scheme=color_scheme,
                ).to_strategy_kwargs()
            except ValueError as exc:
                return _emit_create_error(args.layout, str(exc))
        else:
            return _emit_create_error(args.layout, f"unsupported layout '{args.layout}'")

        try:
            html = generator.generate_layout(layout_type, **payload)
        except ValueError as exc:
            return _emit_create_error(args.layout, str(exc))

        if color_scheme is not None and args.layout in {"story"}:
            html = color_scheme.apply_to_html(html)

        if getattr(args, 'png', False):
            preset = get_export_preset(getattr(args, "export_preset", None))
            if preset is not None:
                policy = ExportPolicy(crop_mode=preset.crop_mode, padding_mode=preset.padding_mode)
                generator.export_to_png(
                    html,
                    output_path,
                    viewport_width=preset.viewport_width,
                    viewport_height=preset.viewport_height,
                    device_scale_factor=preset.device_scale_factor,
                    padding=policy.resolve_padding(),
                    crop_mode=policy.crop_mode,
                )
                print(f"Applied export preset '{preset.name}' ({preset.viewport_width}x{preset.viewport_height})")
            else:
                policy = ExportPolicy(
                    crop_mode=getattr(args, "crop_mode", "safe"),
                    padding_mode=getattr(args, "padding_mode", "minimal"),
                )
                generator.export_to_png(
                    html,
                    output_path,
                    padding=policy.resolve_padding(),
                    crop_mode=policy.crop_mode,
                )
            print(f"Generated create/{args.layout} PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated create/{args.layout}: {output_path}")
        return 0

    _emit_legacy_command_warning(args.command)
    
    output_path = Path(args.output)
    
    # Handle wireframe-svg, wireframe-scene, mermaid specially (no generator until PNG)
    if args.command in ('wireframe-svg', 'wireframe-scene', 'mermaid'):
        # SVG generation doesn't need attribution or generator until --png
        pass
    else:
        attribution = Attribution(
            person=getattr(args, 'person', 'Greg Meyer'),
            website=getattr(args, 'website', 'gregmeyer.com'),
            copyright=args.copyright,
            context=getattr(args, 'context', None),
        )
        
        # If PNG export requested, ensure output path has .png extension
        if getattr(args, 'png', False):
            if output_path.suffix != '.png':
                output_path = output_path.with_suffix('.png')
        
        generator = ModernGraphicsGenerator(getattr(args, 'title', 'Untitled'), attribution)
    
    if args.command == 'cycle':
        steps = parse_steps(args.steps)
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        html = generate_cycle_diagram(
            title=args.title,
            steps=steps,
            arrow_text=args.arrow,
            cycle_end_text=getattr(args, 'cycle_end', None),
            attribution=attribution,
            attribution_on_last=True,
            color_scheme=color_scheme,
            show_loop_indicator=not getattr(args, 'no_loop', False),
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated cycle diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated cycle diagram: {output_path}")
    
    elif args.command == 'comparison':
        left_column = parse_column(args.left)
        right_column = parse_column(args.right)
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        html = generate_comparison_diagram(
            title=args.title,
            left_column=left_column,
            right_column=right_column,
            vs_text=args.vs,
            attribution=attribution,
            color_scheme=color_scheme,
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated comparison diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated comparison diagram: {output_path}")
    
    elif args.command == 'grid':
        density = normalize_density(getattr(args, "density", CREATE_DEFAULTS.density))
        items, grid_columns = shape_grid_for_density(parse_items(args.items), args.columns, density)
        convergence = None
        if args.goal or args.outcome:
            convergence = {
                'goal': textwrap.shorten(args.goal or '', width=44, placeholder='...') if density == "clarity" else (args.goal or ''),
                'outcome': textwrap.shorten(args.outcome or '', width=44, placeholder='...') if density == "clarity" else (args.outcome or '')
            }
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        html = generate_grid_diagram(
            title=args.title,
            items=items,
            columns=grid_columns,
            convergence=convergence,
            attribution=attribution,
            color_scheme=color_scheme,
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated grid diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated grid diagram: {output_path}")
    
    elif args.command == 'flywheel':
        elements = parse_flywheel_elements(args.elements, args.colors)
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        html = generate_flywheel_diagram(
            title=args.title,
            elements=elements,
            center_label=getattr(args, 'center', None),
            radius=args.radius,
            attribution=attribution,
            color_scheme=color_scheme,
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated flywheel diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated flywheel diagram: {output_path}")
    
    elif args.command == 'timeline':
        density = normalize_density(getattr(args, "density", CREATE_DEFAULTS.density))
        events = shape_timeline_events_for_density(
            parse_timeline_events(args.events, getattr(args, 'colors', None)),
            density,
        )
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        html = generate_timeline_diagram(
            title=args.title,
            events=events,
            orientation=getattr(args, 'orientation', 'horizontal'),
            attribution=attribution,
            color_scheme=color_scheme,
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated timeline diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated timeline diagram: {output_path}")
    
    elif args.command == 'pyramid':
        layers = parse_pyramid_layers(args.layers, getattr(args, 'colors', None))
        color_scheme = get_scheme(args.theme) if getattr(args, 'theme', None) else None
        html = generate_pyramid_diagram(
            title=args.title,
            layers=layers,
            orientation=getattr(args, 'orientation', 'up'),
            attribution=attribution,
            color_scheme=color_scheme
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated pyramid diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated pyramid diagram: {output_path}")
    
    elif args.command == 'before-after':
        before_items = [item.strip() for item in args.before.split(',')]
        after_items = [item.strip() for item in args.after.split(',')]
        
        html = generate_before_after_diagram(
            title=args.title,
            before_items=before_items,
            after_items=after_items,
            transition_text=getattr(args, 'transition', '→'),
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated before/after diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated before/after diagram: {output_path}")
    
    elif args.command == 'funnel':
        stages = parse_funnel_stages(
            args.stages,
            getattr(args, 'values', None),
            getattr(args, 'colors', None)
        )
        color_scheme = get_scheme(args.theme) if getattr(args, 'theme', None) else None
        html = generate_funnel_diagram(
            title=args.title,
            stages=stages,
            show_percentages=getattr(args, 'percentages', False),
            attribution=attribution,
            color_scheme=color_scheme
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated funnel diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated funnel diagram: {output_path}")
    
    elif args.command == 'slide-cards':
        cards = json.loads(args.cards)
        color_scheme = get_scheme(args.theme) if getattr(args, 'theme', None) else None
        html = generate_slide_card_diagram(
            title=args.title,
            cards=cards,
            arrow_text=getattr(args, 'arrow', '→'),
            attribution=attribution,
            color_scheme=color_scheme
        )
        if getattr(args, 'png', False):
            # Use wider viewport for horizontal card layouts
            num_cards = len(cards)
            viewport_width = max(4000, num_cards * 1400)  # At least 1400px per card
            viewport_height = 1600
            generator.export_to_png(html, output_path, viewport_width=viewport_width, viewport_height=viewport_height, padding=60)
            print(f"Generated slide card diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated slide card diagram: {output_path}")
    
    elif args.command == 'slide-compare':
        left_card = json.loads(args.left)
        right_card = json.loads(args.right)
        color_scheme = get_scheme(args.theme) if getattr(args, 'theme', None) else None
        html = generate_slide_card_comparison(
            title=args.title,
            left_card=left_card,
            right_card=right_card,
            vs_text=getattr(args, 'vs', '→'),
            attribution=attribution,
            color_scheme=color_scheme
        )
        if getattr(args, 'png', False):
            # Use wider viewport for side-by-side comparison
            viewport_width = 2800
            viewport_height = 1600
            generator.export_to_png(html, output_path, viewport_width=viewport_width, viewport_height=viewport_height, padding=60)
            print(f"Generated slide card comparison PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated slide card comparison: {output_path}")
    
    elif args.command == 'premium-card':
        config_source = args.config
        config_path = Path(config_source)
        if config_path.exists():
            config_raw = config_path.read_text(encoding='utf-8')
        else:
            config_raw = config_source
        try:
            card_config = json.loads(config_raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON for --config: {exc}")
        if getattr(args, 'top_only', False) and getattr(args, 'bottom_only', False):
            raise SystemExit("Cannot combine --top-only and --bottom-only. Choose a single panel or leave both enabled.")
        show_top = not getattr(args, 'bottom_only', False)
        show_bottom = not getattr(args, 'top_only', False)
        title_text = card_config.get('title') or args.title
        html = generate_premium_card(
            title=title_text,
            tagline=card_config.get('tagline', ''),
            subtext=card_config.get('subtext', ''),
            eyebrow=card_config.get('eyebrow', ''),
            features=card_config.get('features', []),
            hero=card_config.get('hero', {}),
            palette=card_config.get('palette', {}),
            canvas_size=getattr(args, 'size', 1100),
            show_top_panel=show_top,
            show_bottom_panel=show_bottom,
            attribution=attribution
        )
        if getattr(args, 'png', False):
            viewport = getattr(args, 'size', 1100)
            generator.export_to_png(
                html,
                output_path,
                viewport_width=viewport,
                viewport_height=viewport,
                padding=0
            )
            print(f"Generated premium card PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated premium card: {output_path}")
    
    elif args.command == 'modern-hero':
        highlights = parse_highlights_arg(getattr(args, 'highlights', None))
        highlight_tiles = None
        if getattr(args, 'highlight_tiles', None):
            try:
                highlight_tiles = json.loads(args.highlight_tiles)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON for --highlight-tiles: {exc}")
        flow_nodes = None
        if getattr(args, 'flow_nodes', None):
            try:
                flow_nodes = json.loads(args.flow_nodes)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON for --flow-nodes: {exc}")
        flow_connections = None
        if getattr(args, 'flow_connections', None):
            try:
                flow_connections = json.loads(args.flow_connections)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON for --flow-connections: {exc}")
        freeform_canvas = getattr(args, 'freeform_canvas', None)
        if getattr(args, 'mermaid_file', None):
            mermaid_path = Path(args.mermaid_file)
            if not mermaid_path.exists():
                raise SystemExit(f"Mermaid file not found: {mermaid_path}")
            hero_mermaid_scheme = get_scheme(getattr(args, 'theme', None)) if getattr(args, 'theme', None) else None
            try:
                freeform_canvas = mermaid_to_svg(
                    mermaid_path.read_text(encoding="utf-8"),
                    color_scheme=hero_mermaid_scheme,
                    font_family=getattr(args, 'mermaid_font', None),
                )
            except RuntimeError as e:
                raise SystemExit(str(e))
        stats = parse_stats_arg(getattr(args, 'stats', None))
        html = generate_modern_hero(
            title=args.title,
            headline=args.headline,
            subheadline=getattr(args, 'subheadline', None),
            eyebrow=getattr(args, 'eyebrow', None),
            highlights=highlights,
            highlight_tiles=highlight_tiles,
            flow_nodes=flow_nodes,
            flow_connections=flow_connections,
            freeform_canvas=freeform_canvas,
            stats=stats,
            cta=getattr(args, 'cta', None),
            background_variant=getattr(args, 'background', 'light'),
            visual_description=getattr(args, 'visual_description', None),
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path, viewport_width=1700, viewport_height=1100, padding=30)
            print(f"Generated modern hero PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated modern hero: {output_path}")

    elif args.command == 'modern-hero-triptych':
        stats = parse_stats_arg(getattr(args, 'stats', None))
        try:
            columns = json.loads(args.columns)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON for --columns: {exc}")
        html = generate_modern_hero_triptych(
            title=args.title,
            headline=args.headline,
            subheadline=getattr(args, 'subheadline', None),
            columns=columns,
            stats=stats,
            eyebrow=getattr(args, 'eyebrow', None),
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path, viewport_width=1700, viewport_height=1100, padding=30)
            print(f"Generated modern hero triptych PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated modern hero triptych: {output_path}")

    elif args.command == 'modern-hero-prompt':
        prompt_path = Path(args.prompt_file)
        try:
            prompt_data = json.loads(prompt_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON prompt file: {exc}")
        layout = prompt_data.get('layout', 'open')
        stats = prompt_data.get('stats')
        eyebrow = prompt_data.get('eyebrow')
        headline = prompt_data.get('headline') or "Modern Hero"
        subheadline = prompt_data.get('subheadline')
        visual_description = prompt_data.get('visual_description')
        if layout == 'triptych':
            columns = prompt_data.get('columns')
            if not columns:
                raise SystemExit("Triptych layout requires 'columns' array in prompt JSON.")
            html = generate_modern_hero_triptych(
                title=prompt_data.get('title', args.prompt_file),
                headline=headline,
                subheadline=subheadline,
                columns=columns,
                stats=stats,
                eyebrow=eyebrow,
                attribution=attribution
            )
        else:
            html = generate_modern_hero(
                title=prompt_data.get('title', args.prompt_file),
                headline=headline,
                subheadline=subheadline,
                eyebrow=eyebrow,
                highlights=prompt_data.get('highlights'),
                highlight_tiles=prompt_data.get('highlight_tiles'),
                flow_nodes=prompt_data.get('flow_nodes'),
                flow_connections=prompt_data.get('flow_connections'),
                freeform_canvas=prompt_data.get('freeform_canvas'),
                stats=stats,
                cta=prompt_data.get('cta'),
                background_variant=prompt_data.get('background', 'light'),
                visual_description=visual_description,
                attribution=attribution
            )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path, viewport_width=1700, viewport_height=1100, padding=30)
            print(f"Generated modern hero from prompt PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated modern hero from prompt: {output_path}")

    elif args.command == 'story-slide':
        evolution_data = None
        density = normalize_density(getattr(args, "density", CREATE_DEFAULTS.density))
        
        if getattr(args, 'evolution_data', None):
            evolution_data = json.loads(args.evolution_data)
        
        what_changed, time_period, what_it_means = shape_story_fields_for_density(
            args.what_changed,
            args.time_period,
            args.what_it_means,
            density,
        )

        html = generate_story_slide(
            title=args.title,
            what_changed=what_changed,
            time_period=time_period,
            what_it_means=what_it_means,
            insight=getattr(args, 'insight', None),
            evolution_data=evolution_data,
            attribution=attribution,
            top_tile_only=getattr(args, 'top_tile_only', False),
            hero_use_svg_js=getattr(args, 'hero_svg_js', False),
            hero_variant=getattr(args, 'hero_variant', 'auto')
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path, viewport_width=2400, viewport_height=1800, padding=40)
            print(f"Generated story-driven slide PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated story-driven slide: {output_path}")
    
    # =========================================================================
    # Insight Graphics Commands
    # =========================================================================
    
    elif args.command == 'key-insight':
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        
        html = generate_key_insight(
            generator,
            text=args.text,
            label=getattr(args, 'label', 'Key Insight'),
            eyebrow=getattr(args, 'eyebrow', None),
            context=getattr(args, 'context', None),
            variant=getattr(args, 'variant', 'default'),
            icon=getattr(args, 'icon', 'lightning'),
            accent_color=getattr(args, 'accent_color', '#0071e3'),
            color_scheme=color_scheme,
        )
        padding = getattr(args, 'padding', 10)
        if getattr(args, 'png', False):
            size = getattr(args, 'size', 800)
            if getattr(args, 'square', False):
                generator.export_to_png(html, output_path, viewport_width=size, viewport_height=size, padding=padding)
            else:
                generator.export_to_png(html, output_path, viewport_width=900, viewport_height=400, padding=padding)
            print(f"Generated key insight PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated key insight: {output_path}")
    
    elif args.command == 'insight-card':
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        
        # Get SVG content
        svg_content = None
        if getattr(args, 'mermaid_file', None):
            mermaid_path = Path(args.mermaid_file)
            if not mermaid_path.exists():
                raise SystemExit(f"Mermaid file not found: {mermaid_path}")
            mermaid_source = mermaid_path.read_text(encoding="utf-8")
            mermaid_scheme = get_scheme(getattr(args, 'theme', None)) if getattr(args, 'theme', None) else None
            try:
                svg_content = mermaid_to_svg(
                    mermaid_source,
                    color_scheme=mermaid_scheme,
                    font_family=getattr(args, 'mermaid_font', None),
                )
            except RuntimeError as e:
                raise SystemExit(str(e))
        elif getattr(args, 'svg_file', None):
            svg_path = Path(args.svg_file)
            if not svg_path.exists():
                raise SystemExit(f"SVG file not found: {svg_path}")
            svg_content = svg_path.read_text()
        elif getattr(args, 'svg_type', None):
            # Use themed config if theme specified
            config = get_wireframe_config_from_theme(
                getattr(args, 'theme', None),
                width=360,
                height=280,
                accent_color=getattr(args, 'accent_color', '#0071e3'),
            )
            if args.svg_type == 'before':
                svg_content = generate_before_wireframe_svg(config)
            elif args.svg_type == 'after':
                svg_content = generate_after_wireframe_svg(config)
            elif args.svg_type == 'chat-panel':
                svg_content = generate_chat_panel_svg(config)
            elif args.svg_type == 'modal-form':
                svg_content = generate_modal_form_svg(config)
        else:
            raise SystemExit("One of --svg-file, --svg-type, or --mermaid-file is required")
        
        html = generate_insight_card(
            generator,
            text=args.text,
            svg_content=svg_content,
            label=getattr(args, 'label', 'Key Insight'),
            svg_label=getattr(args, 'svg_label', None),
            eyebrow=getattr(args, 'eyebrow', None),
            context=getattr(args, 'context', None),
            layout=getattr(args, 'layout', 'side-by-side'),
            svg_position=getattr(args, 'svg_position', 'right'),
            variant=getattr(args, 'variant', 'bold'),
            icon=getattr(args, 'icon', 'lightning'),
            accent_color=getattr(args, 'accent_color', '#0071e3'),
            color_scheme=color_scheme,
        )
        padding = getattr(args, 'padding', 10)
        if getattr(args, 'png', False):
            size = getattr(args, 'size', 800)
            if getattr(args, 'square', False):
                generator.export_to_png(html, output_path, viewport_width=size, viewport_height=size, padding=padding)
            else:
                generator.export_to_png(html, output_path, viewport_width=960, viewport_height=400, padding=padding)
            print(f"Generated insight card PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated insight card: {output_path}")
    
    elif args.command == 'insight-story':
        # Get color scheme if theme specified
        color_scheme = None
        if getattr(args, 'theme', None):
            color_scheme = get_scheme(args.theme)
        
        # Get before/after SVGs
        before_svg = None
        after_svg = None
        
        if getattr(args, 'generate_wireframes', False):
            # Use themed config if theme specified
            config = get_wireframe_config_from_theme(
                getattr(args, 'theme', None),
                width=360,
                height=280,
                accent_color=getattr(args, 'accent_color', '#0071e3'),
            )
            before_svg = generate_before_wireframe_svg(config)
            after_svg = generate_after_wireframe_svg(config)
        else:
            if getattr(args, 'before_svg', None):
                before_path = Path(args.before_svg)
                if before_path.exists():
                    before_svg = before_path.read_text()
            if getattr(args, 'after_svg', None):
                after_path = Path(args.after_svg)
                if after_path.exists():
                    after_svg = after_path.read_text()
        
        # Parse status strings
        before_status = None
        if getattr(args, 'before_status', None):
            status_text = args.before_status
            if status_text.startswith('-'):
                before_status = {'type': 'negative', 'text': status_text[1:].strip()}
            elif status_text.startswith('+'):
                before_status = {'type': 'positive', 'text': status_text[1:].strip()}
            else:
                before_status = {'type': 'neutral', 'text': status_text}
        
        after_status = None
        if getattr(args, 'after_status', None):
            status_text = args.after_status
            if status_text.startswith('-'):
                after_status = {'type': 'negative', 'text': status_text[1:].strip()}
            elif status_text.startswith('+'):
                after_status = {'type': 'positive', 'text': status_text[1:].strip()}
            else:
                after_status = {'type': 'neutral', 'text': status_text}
        
        stats = parse_stats_arg(getattr(args, 'stats', None))
        
        html = generate_insight_story(
            generator,
            headline=args.headline,
            subtitle=getattr(args, 'subtitle', None),
            eyebrow=getattr(args, 'eyebrow', None),
            before_svg=before_svg,
            before_label=getattr(args, 'before_label', 'Before'),
            before_status=before_status,
            after_svg=after_svg,
            after_label=getattr(args, 'after_label', 'After'),
            after_status=after_status,
            shift_from=getattr(args, 'shift_from', None),
            shift_to=getattr(args, 'shift_to', None),
            shift_badge=getattr(args, 'shift_badge', None),
            insight_text=getattr(args, 'insight_text', ''),
            insight_label=getattr(args, 'insight_label', 'Key Insight'),
            stats=stats,
            accent_color=getattr(args, 'accent_color', '#0071e3'),
            color_scheme=color_scheme,
        )
        padding = getattr(args, 'padding', 10)
        # Determine viewport size based on content
        has_svgs = before_svg or after_svg
        viewport_height = 1100 if has_svgs else 500
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path, viewport_width=1400, viewport_height=viewport_height, padding=padding)
            print(f"Generated insight story PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated insight story: {output_path}")
    
    # =========================================================================
    # SVG Wireframe Generation
    # =========================================================================
    
    elif args.command == 'wireframe-svg':
        # Get color scheme if theme specified
        theme_name = getattr(args, 'theme', None)
        color_scheme = get_scheme(theme_name) if theme_name else None
        
        # Create config from theme or defaults
        config = get_wireframe_config_from_theme(
            theme_name,
            width=getattr(args, 'width', 400),
            height=getattr(args, 'height', 300),
            accent_color=getattr(args, 'accent_color', '#0071e3'),
        )
        
        wireframe_type = args.type
        svg_content = None
        
        if wireframe_type == 'before':
            svg_content = generate_before_wireframe_svg(config)
        
        elif wireframe_type == 'after':
            svg_content = generate_after_wireframe_svg(config)
        
        elif wireframe_type == 'chat-panel':
            messages = None
            if getattr(args, 'messages', None):
                try:
                    messages = json.loads(args.messages)
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"Invalid JSON for --messages: {exc}")
            
            inline_card = None
            if getattr(args, 'inline_card', None):
                try:
                    inline_card = json.loads(args.inline_card)
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"Invalid JSON for --inline-card: {exc}")
            
            action_buttons = None
            if getattr(args, 'action_buttons', None):
                action_buttons = [b.strip() for b in args.action_buttons.split(',')]
            
            success_toast = None
            if getattr(args, 'success_toast', None):
                try:
                    success_toast = json.loads(args.success_toast)
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"Invalid JSON for --success-toast: {exc}")
            
            svg_content = generate_chat_panel_svg(
                config=config,
                messages=messages,
                inline_card=inline_card,
                action_buttons=action_buttons,
                success_toast=success_toast,
            )
        
        elif wireframe_type == 'modal-form':
            fields = None
            if getattr(args, 'fields', None):
                fields = [f.strip() for f in args.fields.split(',')]
            
            svg_content = generate_modal_form_svg(
                config=config,
                title=getattr(args, 'modal_title', 'Support Request'),
                fields=fields,
                submit_label=getattr(args, 'submit_label', 'Submit'),
            )
        
        elif wireframe_type == 'ticket-flow':
            svg_content = generate_ticket_flow_svg(config)
        
        # Export as PNG or save as SVG
        if getattr(args, 'png', False):
            # Need generator for PNG export
            attribution = Attribution(
                copyright=args.copyright,
                context=getattr(args, 'context', None)
            )
            generator = ModernGraphicsGenerator(f"Wireframe {wireframe_type}", attribution)
            
            # Wrap SVG in HTML for proper rendering
            width = getattr(args, 'width', 400)
            height = getattr(args, 'height', 300)
            html = wrap_svg_for_png_export(svg_content, color_scheme, width, height)
            
            padding = getattr(args, 'padding', 10)
            if output_path.suffix != '.png':
                output_path = output_path.with_suffix('.png')
            generator.export_to_png(html, output_path, viewport_width=width + 40, viewport_height=height + 40, padding=padding)
            print(f"Generated wireframe PNG: {output_path}")
        else:
            # Save SVG
            output_path.write_text(svg_content)
            print(f"Generated wireframe SVG: {output_path}")

    elif args.command == 'wireframe-scene':
        preset = getattr(args, 'preset', None)
        spec_path = getattr(args, 'spec', None)
        if not preset and not spec_path:
            raise SystemExit("wireframe-scene requires either --preset or --spec")
        if preset and spec_path:
            raise SystemExit("wireframe-scene: use either --preset or --spec, not both")

        theme_name = getattr(args, 'theme', None)
        scheme = get_scheme(theme_name) if theme_name else None
        default_width = 600
        default_height = 520

        if preset:
            spec = SCENE_PRESETS[preset]
        else:
            with open(spec_path, encoding="utf-8") as f:
                spec = json.load(f)
            if not isinstance(spec, dict) or "elements" not in spec:
                raise SystemExit("wireframe-scene --spec: JSON must be an object with 'width', 'height', and 'elements'")

        scene_width = spec.get("width", default_width)
        scene_height = spec.get("height", default_height)
        config = WireframeConfig.from_color_scheme(scheme, width=scene_width, height=scene_height) if scheme else WireframeConfig(width=scene_width, height=scene_height)

        svg_content = render_scene(spec, config)

        if getattr(args, 'png', False):
            attribution = Attribution(
                copyright=getattr(args, 'copyright', None),
                context=getattr(args, 'context', None),
            )
            generator = ModernGraphicsGenerator("Wireframe scene", attribution)
            html = wrap_svg_for_png_export(svg_content, scheme, scene_width, scene_height)
            if output_path.suffix != '.png':
                output_path = output_path.with_suffix('.png')
            padding = getattr(args, 'padding', 10)
            generator.export_to_png(html, output_path, viewport_width=scene_width + 40, viewport_height=scene_height + 40, padding=padding)
            print(f"Generated wireframe scene PNG: {output_path}")
        else:
            output_path.write_text(svg_content)
            print(f"Generated wireframe scene SVG: {output_path}")

    elif args.command == 'mermaid':
        import re
        inp = getattr(args, 'input', None)
        if inp == '-':
            mermaid_source = sys.stdin.read()
        else:
            mermaid_path = Path(inp)
            if not mermaid_path.exists():
                raise SystemExit(f"Input file not found: {mermaid_path}")
            mermaid_source = mermaid_path.read_text(encoding="utf-8")
        mermaid_theme_scheme = get_scheme(getattr(args, 'theme', None)) if getattr(args, 'theme', None) else None
        try:
            svg_content = mermaid_to_svg(
                mermaid_source,
                width=getattr(args, 'width', None),
                height=getattr(args, 'height', None),
                color_scheme=mermaid_theme_scheme,
                font_family=getattr(args, 'font', None),
            )
        except RuntimeError as e:
            raise SystemExit(str(e))
        if getattr(args, 'png', False):
            m = re.search(r'viewBox="[^"]*\s+([\d.]+)\s+([\d.]+)"', svg_content)
            vw = int(float(m.group(1))) if m else 800
            vh = int(float(m.group(2))) if m else 600
            attribution = Attribution(
                copyright=getattr(args, 'copyright', None),
                context=getattr(args, 'context', None),
            )
            generator = ModernGraphicsGenerator("Mermaid diagram", attribution)
            html = wrap_svg_for_png_export(svg_content, None, vw, vh)
            if output_path.suffix != '.png':
                output_path = output_path.with_suffix('.png')
            padding = getattr(args, 'padding', 10)
            generator.export_to_png(html, output_path, viewport_width=vw + 40, viewport_height=vh + 40, padding=padding)
            print(f"Generated Mermaid PNG: {output_path}")
        else:
            output_path.write_text(svg_content)
            print(f"Generated Mermaid SVG: {output_path}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
