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
import sys
from pathlib import Path

from . import ModernGraphicsGenerator, Attribution
from .color_scheme import get_scheme, list_schemes
from .cli_clarity import CREATE_DEFAULTS
from .export_presets import list_export_presets
from .diagrams.wireframe_scene import list_presets
from .cli_utils import (
    _adapt_legacy_command_aliases,
    # Re-export for backwards compatibility with tests
    LEGACY_CREATE_HINTS,
    shape_story_fields_for_density,
    shape_timeline_events_for_density,
    shape_grid_for_density,
    CREATE_EXAMPLES,
    parse_column,
    parse_timeline_events,
    parse_funnel_stages,
    parse_items,
    parse_highlights_arg,
)
from .cli_build import handle_themes, handle_build, handle_retheme
from .cli_create import handle_create
from .cli_legacy import handle_legacy_command


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

    create_core.add_argument('--layout', choices=['hero', 'insight', 'key-insight', 'insight-card', 'insight-story', 'comparison', 'story', 'timeline', 'funnel', 'grid'], help='Layout family to generate (omit to get a suggestion)')
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

    # Themes browser
    subparsers.add_parser('themes', help='List available color themes with descriptions')

    # Interactive build
    build_parser = subparsers.add_parser('build', help='Interactive graphic builder — guided layout, theme, and content selection')
    build_parser.add_argument('--output', default=None, help='Output path (default: ./output/<layout>.html)')

    # Retheme existing graphic
    retheme_parser = subparsers.add_parser('retheme', help='Apply a different theme to an existing HTML graphic')
    retheme_parser.add_argument('input', help='Path to existing HTML graphic')
    retheme_parser.add_argument('--theme', required=True, help='New theme name')
    retheme_parser.add_argument('--output', help='Output path (default: overwrites input)')
    retheme_parser.add_argument('--png', action='store_true', help='Also export as PNG')

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

    # ── Short inline handlers ──────────────────────────────────────

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
        from . import create_story_slide_from_prompt
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

        # Detect layout from prompt file format field
        detected_layout = None
        from .suggest import suggest_layout
        for line in prompt_text.splitlines():
            if line.lower().startswith("## format") or line.lower().startswith("**format"):
                # Next non-empty line has the format
                idx = prompt_text.splitlines().index(line)
                remaining = prompt_text.splitlines()[idx + 1:]
                for next_line in remaining:
                    stripped = next_line.strip().strip("*").strip()
                    if stripped:
                        result = suggest_layout(stripped)
                        if result.confidence > 0.1:
                            detected_layout = result.layout
                            print(f"Detected layout from prompt: {detected_layout} (from: {stripped})")
                        break
                break

        if detected_layout and detected_layout != "story":
            print(f"Routing to layout '{detected_layout}' instead of default story slide.")
            print(f"Tip: use 'modern-graphics create --layout {detected_layout} ...' for full control.")

        # Always fall back to story slide generation (the only AI-powered path)
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

    # ── Dispatched handlers ────────────────────────────────────────

    if args.command == 'themes':
        return handle_themes(args)

    if args.command == 'build':
        return handle_build(args)

    if args.command == 'retheme':
        return handle_retheme(args)

    if args.command == 'create':
        return handle_create(args)

    # Legacy commands
    return handle_legacy_command(args)


if __name__ == '__main__':
    import sys
    sys.exit(main())
