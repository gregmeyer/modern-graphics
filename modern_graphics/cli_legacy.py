"""Handlers for all legacy diagram commands."""

import json
import sys
import textwrap
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
    generate_chat_panel_svg,
    generate_modal_form_svg,
    generate_ticket_flow_svg,
    generate_before_wireframe_svg,
    generate_after_wireframe_svg,
)
from .diagrams.wireframe_scene import render_scene, SCENE_PRESETS
from .diagrams.wireframe_elements.config import WireframeConfig
from .diagrams.mermaid_svg import mermaid_to_svg
from .color_scheme import get_scheme
from .cli_clarity import normalize_density, CREATE_DEFAULTS
from .cli_utils import (
    _emit_legacy_command_warning,
    parse_steps,
    parse_column,
    parse_items,
    parse_flywheel_elements,
    parse_timeline_events,
    parse_pyramid_layers,
    parse_funnel_stages,
    parse_highlights_arg,
    parse_stats_arg,
    shape_story_fields_for_density,
    shape_timeline_events_for_density,
    shape_grid_for_density,
    get_wireframe_config_from_theme,
    wrap_svg_for_png_export,
)


def handle_legacy_command(args) -> int:
    """Handle all legacy diagram commands."""
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
