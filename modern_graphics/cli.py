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
"""

import argparse
import json
from pathlib import Path

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
)


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


def main():
    parser = argparse.ArgumentParser(description='Generate modern HTML/CSS graphics')
    subparsers = parser.add_subparsers(dest='command', help='Diagram type')
    
    # Cycle diagram
    cycle_parser = subparsers.add_parser('cycle', help='Generate cycle diagram')
    cycle_parser.add_argument('--title', required=True, help='Diagram title')
    cycle_parser.add_argument('--steps', required=True, help='Comma-separated list of steps')
    cycle_parser.add_argument('--arrow', default='→', help='Arrow text (default: →)')
    cycle_parser.add_argument('--cycle-end', help='Text to display after cycle (e.g., "(repeat)")')
    cycle_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    cycle_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    cycle_parser.add_argument('--context', help='Optional context line for attribution')
    cycle_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Comparison diagram
    comp_parser = subparsers.add_parser('comparison', help='Generate comparison diagram')
    comp_parser.add_argument('--title', required=True, help='Diagram title')
    comp_parser.add_argument('--left', required=True, help='Left column: "Title:Step1,Step2:Outcome"')
    comp_parser.add_argument('--right', required=True, help='Right column: "Title:Step1,Step2:Outcome"')
    comp_parser.add_argument('--vs', default='vs', help='VS text (default: vs)')
    comp_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    comp_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    comp_parser.add_argument('--context', help='Optional context line for attribution')
    comp_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Grid diagram
    grid_parser = subparsers.add_parser('grid', help='Generate grid diagram')
    grid_parser.add_argument('--title', required=True, help='Diagram title')
    grid_parser.add_argument('--items', required=True, help='Comma-separated list of items')
    grid_parser.add_argument('--columns', type=int, default=5, help='Number of columns (default: 5)')
    grid_parser.add_argument('--goal', help='Goal text for convergence section')
    grid_parser.add_argument('--outcome', help='Outcome text for convergence section')
    grid_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    grid_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    grid_parser.add_argument('--context', help='Optional context line for attribution')
    grid_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Flywheel diagram
    flywheel_parser = subparsers.add_parser('flywheel', help='Generate flywheel diagram')
    flywheel_parser.add_argument('--title', required=True, help='Diagram title')
    flywheel_parser.add_argument('--elements', required=True, help='Comma-separated list of elements')
    flywheel_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    flywheel_parser.add_argument('--center', help='Optional center label')
    flywheel_parser.add_argument('--radius', type=int, default=200, help='Circle radius in pixels (default: 200)')
    flywheel_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    flywheel_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    flywheel_parser.add_argument('--context', help='Optional context line for attribution')
    flywheel_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Timeline diagram
    timeline_parser = subparsers.add_parser('timeline', help='Generate timeline diagram')
    timeline_parser.add_argument('--title', required=True, help='Diagram title')
    timeline_parser.add_argument('--events', required=True, help='Comma-separated list of events in format "Date|Text" or "Date:Text"')
    timeline_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    timeline_parser.add_argument('--orientation', choices=['horizontal', 'vertical'], default='horizontal', help='Timeline orientation (default: horizontal)')
    timeline_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    timeline_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    timeline_parser.add_argument('--context', help='Optional context line for attribution')
    timeline_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Pyramid diagram
    pyramid_parser = subparsers.add_parser('pyramid', help='Generate pyramid diagram')
    pyramid_parser.add_argument('--title', required=True, help='Diagram title')
    pyramid_parser.add_argument('--layers', required=True, help='Comma-separated list of layers (top to bottom)')
    pyramid_parser.add_argument('--colors', help='Comma-separated list of colors (blue,green,orange,purple,red,gray)')
    pyramid_parser.add_argument('--orientation', choices=['up', 'down'], default='up', help='Pyramid orientation - up (pointing up) or down (pointing down) (default: up)')
    pyramid_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    pyramid_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    pyramid_parser.add_argument('--context', help='Optional context line for attribution')
    pyramid_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Before/After diagram
    before_after_parser = subparsers.add_parser('before-after', help='Generate before/after diagram')
    before_after_parser.add_argument('--title', required=True, help='Diagram title')
    before_after_parser.add_argument('--before', required=True, help='Comma-separated list of "before" items')
    before_after_parser.add_argument('--after', required=True, help='Comma-separated list of "after" items')
    before_after_parser.add_argument('--transition', default='→', help='Transition text between states (default: →)')
    before_after_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    before_after_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
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
    funnel_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    funnel_parser.add_argument('--context', help='Optional context line for attribution')
    funnel_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Slide card diagram
    slide_cards_parser = subparsers.add_parser('slide-cards', help='Generate slide card diagram (horizontal transformation)')
    slide_cards_parser.add_argument('--title', required=True, help='Diagram title')
    slide_cards_parser.add_argument('--cards', required=True, help='JSON string with cards array: [{"title":"...","tagline":"...","subtext":"...","filename":"...","color":"blue|green|purple|gray","features":["..."],"badge":"..."}]')
    slide_cards_parser.add_argument('--arrow', default='→', help='Arrow text between cards (default: →)')
    slide_cards_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    slide_cards_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    slide_cards_parser.add_argument('--context', help='Optional context line for attribution')
    slide_cards_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Slide card comparison
    slide_compare_parser = subparsers.add_parser('slide-compare', help='Generate slide card comparison (side-by-side)')
    slide_compare_parser.add_argument('--title', required=True, help='Diagram title')
    slide_compare_parser.add_argument('--left', required=True, help='JSON string with left card: {"title":"...","tagline":"...","color":"...","features":["..."],"badge":"..."}')
    slide_compare_parser.add_argument('--right', required=True, help='JSON string with right card: {"title":"...","tagline":"...","color":"...","features":["..."],"badge":"..."}')
    slide_compare_parser.add_argument('--vs', default='→', help='VS text between cards (default: →)')
    slide_compare_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    slide_compare_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    slide_compare_parser.add_argument('--context', help='Optional context line for attribution')
    slide_compare_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML (high-resolution, tight cropping)')
    
    # Story-driven slide
    story_slide_parser = subparsers.add_parser('story-slide', help='Generate compelling story-driven slide (What changed, time period, what it means)')
    story_slide_parser.add_argument('--title', required=True, help='Slide title')
    story_slide_parser.add_argument('--what-changed', required=True, help='What changed (the change)')
    story_slide_parser.add_argument('--time-period', required=True, help='Over what time period')
    story_slide_parser.add_argument('--what-it-means', required=True, help='What it means (the meaning/implication)')
    story_slide_parser.add_argument('--insight', help='Optional key insight/takeaway')
    story_slide_parser.add_argument('--evolution-data', help='JSON array of evolution stages: [{"era":"2010s","label":"Manual Slides","icon":"📊"}]')
    story_slide_parser.add_argument('--output', required=True, help='Output HTML file path (or PNG if --png is set)')
    story_slide_parser.add_argument('--copyright', default='© Greg Meyer 2025 • gregmeyer.com', help='Copyright text')
    story_slide_parser.add_argument('--context', help='Optional context line for attribution')
    story_slide_parser.add_argument('--png', action='store_true', help='Export as PNG instead of HTML')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    attribution = Attribution(
        copyright=args.copyright,
        context=getattr(args, 'context', None)
    )
    
    output_path = Path(args.output)
    
    # If PNG export requested, ensure output path has .png extension
    if getattr(args, 'png', False):
        if output_path.suffix != '.png':
            output_path = output_path.with_suffix('.png')
    
    generator = ModernGraphicsGenerator(args.title, attribution)
    
    if args.command == 'cycle':
        steps = parse_steps(args.steps)
        html = generate_cycle_diagram(
            title=args.title,
            steps=steps,
            arrow_text=args.arrow,
            cycle_end_text=getattr(args, 'cycle_end', None),
            attribution=attribution,
            attribution_on_last=True
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
        html = generate_comparison_diagram(
            title=args.title,
            left_column=left_column,
            right_column=right_column,
            vs_text=args.vs,
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated comparison diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated comparison diagram: {output_path}")
    
    elif args.command == 'grid':
        items = parse_items(args.items)
        convergence = None
        if args.goal or args.outcome:
            convergence = {
                'goal': args.goal or '',
                'outcome': args.outcome or ''
            }
        html = generate_grid_diagram(
            title=args.title,
            items=items,
            columns=args.columns,
            convergence=convergence,
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated grid diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated grid diagram: {output_path}")
    
    elif args.command == 'flywheel':
        elements = parse_flywheel_elements(args.elements, args.colors)
        
        html = generate_flywheel_diagram(
            title=args.title,
            elements=elements,
            center_label=getattr(args, 'center', None),
            radius=args.radius,
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated flywheel diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated flywheel diagram: {output_path}")
    
    elif args.command == 'timeline':
        events = parse_timeline_events(args.events, getattr(args, 'colors', None))
        
        html = generate_timeline_diagram(
            title=args.title,
            events=events,
            orientation=getattr(args, 'orientation', 'horizontal'),
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated timeline diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated timeline diagram: {output_path}")
    
    elif args.command == 'pyramid':
        layers = parse_pyramid_layers(args.layers, getattr(args, 'colors', None))
        
        html = generate_pyramid_diagram(
            title=args.title,
            layers=layers,
            orientation=getattr(args, 'orientation', 'up'),
            attribution=attribution
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
        
        html = generate_funnel_diagram(
            title=args.title,
            stages=stages,
            show_percentages=getattr(args, 'percentages', False),
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path)
            print(f"Generated funnel diagram PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated funnel diagram: {output_path}")
    
    elif args.command == 'slide-cards':
        cards = json.loads(args.cards)
        
        html = generate_slide_card_diagram(
            title=args.title,
            cards=cards,
            arrow_text=getattr(args, 'arrow', '→'),
            attribution=attribution
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
        
        html = generate_slide_card_comparison(
            title=args.title,
            left_card=left_card,
            right_card=right_card,
            vs_text=getattr(args, 'vs', '→'),
            attribution=attribution
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
    
    elif args.command == 'story-slide':
        evolution_data = None
        
        if getattr(args, 'evolution_data', None):
            evolution_data = json.loads(args.evolution_data)
        
        html = generate_story_slide(
            title=args.title,
            what_changed=args.what_changed,
            time_period=args.time_period,
            what_it_means=args.what_it_means,
            insight=getattr(args, 'insight', None),
            evolution_data=evolution_data,
            attribution=attribution
        )
        if getattr(args, 'png', False):
            generator.export_to_png(html, output_path, viewport_width=2400, viewport_height=1800, padding=40)
            print(f"Generated story-driven slide PNG: {output_path}")
        else:
            generator.save(html, output_path)
            print(f"Generated story-driven slide: {output_path}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
