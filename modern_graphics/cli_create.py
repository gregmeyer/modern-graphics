"""Handler for the 'create' command."""

import textwrap
from pathlib import Path

from . import ModernGraphicsGenerator, Attribution
from .color_scheme import get_scheme
from .cli_clarity import normalize_density, CREATE_DEFAULTS
from .export_policy import ExportPolicy
from .export_presets import get_export_preset
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
from .diagrams.wireframe_svg import (
    generate_before_wireframe_svg,
    generate_after_wireframe_svg,
)
from .cli_utils import (
    CREATE_EXAMPLES,
    _emit_create_error,
    parse_column,
    parse_timeline_events,
    parse_funnel_stages,
    parse_items,
    parse_highlights_arg,
    parse_stats_arg,
    shape_story_fields_for_density,
    shape_timeline_events_for_density,
    shape_grid_for_density,
    get_wireframe_config_from_theme,
)


def _build_hero_payload(args, density, color_scheme):
    """Build payload for the hero layout."""
    highlights = parse_highlights_arg(getattr(args, "highlights", None))
    if density == "clarity" and highlights:
        highlights = highlights[:3]
    try:
        return HeroPayload(
            headline=args.headline or "Execution scales. Judgment stays scarce.",
            subheadline=getattr(args, "subheadline", None),
            eyebrow=getattr(args, "eyebrow", None),
            highlights=highlights,
            background_variant="light",
            color_scheme=color_scheme,
        ).to_strategy_kwargs()
    except ValueError as exc:
        return _emit_create_error(args.layout, str(exc))


def _build_key_insight_payload(args, density, color_scheme):
    """Build payload for the key-insight layout."""
    if not getattr(args, "text", None):
        return _emit_create_error(args.layout, "--text is required for this layout")
    key_variant = getattr(args, "variant", None) or ("bold" if density != "dense" else "default")
    try:
        return KeyInsightPayload(
            text=args.text,
            label=getattr(args, "label", "Key Insight"),
            variant=key_variant,
            icon=getattr(args, "icon", "lightning"),
            color_scheme=color_scheme,
        ).to_strategy_kwargs()
    except ValueError as exc:
        return _emit_create_error(args.layout, str(exc))


def _build_insight_card_payload(args, density, color_scheme):
    """Build payload for the insight-card layout."""
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
        return InsightCardPayload(
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


def _build_insight_story_payload(args, density, color_scheme):
    """Build payload for the insight-story layout."""
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
        return InsightStoryPayload(
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


def _build_comparison_payload(args, density, color_scheme):
    """Build payload for the comparison layout."""
    if not getattr(args, "left", None) or not getattr(args, "right", None):
        return _emit_create_error(args.layout, "--left and --right are required for this layout")
    try:
        return ComparisonPayload(
            left_column=parse_column(args.left),
            right_column=parse_column(args.right),
            vs_text="vs",
            color_scheme=color_scheme,
        ).to_strategy_kwargs()
    except ValueError as exc:
        return _emit_create_error(args.layout, str(exc))


def _build_story_payload(args, density, color_scheme):
    """Build payload for the story layout."""
    story_what_changed, story_time_period, story_what_it_means = shape_story_fields_for_density(
        getattr(args, "what_changed", None) or "Execution capacity increased",
        getattr(args, "time_period", None) or "this quarter",
        getattr(args, "what_it_means", None) or "Decision quality now drives outcomes",
        density,
    )
    return {
        "title": args.title,
        "what_changed": story_what_changed,
        "time_period": story_time_period,
        "what_it_means": story_what_it_means,
        "insight": getattr(args, "headline", None),
    }


def _build_timeline_payload(args, density, color_scheme):
    """Build payload for the timeline layout."""
    if not getattr(args, "events", None):
        return _emit_create_error(args.layout, "--events is required for this layout")
    try:
        timeline_events = shape_timeline_events_for_density(
            parse_timeline_events(args.events),
            density,
        )
        return TimelinePayload(
            events=timeline_events,
            orientation=getattr(args, "orientation", "horizontal"),
            color_scheme=color_scheme,
        ).to_strategy_kwargs()
    except ValueError as exc:
        return _emit_create_error(args.layout, str(exc))


def _build_funnel_payload(args, density, color_scheme):
    """Build payload for the funnel layout."""
    if not getattr(args, "stages", None):
        return _emit_create_error(args.layout, "--stages is required for this layout")
    try:
        return FunnelPayload(
            stages=parse_funnel_stages(args.stages, getattr(args, "values", None)),
            show_percentages=bool(getattr(args, "percentages", False)),
            color_scheme=color_scheme,
        ).to_strategy_kwargs()
    except ValueError as exc:
        return _emit_create_error(args.layout, str(exc))


def _build_grid_payload(args, density, color_scheme):
    """Build payload for the grid layout."""
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
        return GridPayload(
            items=grid_items,
            columns=grid_columns,
            convergence=convergence,
            color_scheme=color_scheme,
        ).to_strategy_kwargs()
    except ValueError as exc:
        return _emit_create_error(args.layout, str(exc))


# ---------------------------------------------------------------------------
# Payload builder registry
# ---------------------------------------------------------------------------

def _build_equation_payload(args, density, color_scheme):
    """Build payload for the equation layout."""
    if not getattr(args, "equation", None):
        return _emit_create_error(args.layout, "--equation is required for this layout")
    payload = {
        "equation": args.equation,
        "label": getattr(args, "eq_label", None),
        "footnote": getattr(args, "footnote", None),
        "size": getattr(args, "eq_size", "large"),
    }
    if color_scheme is not None:
        payload["color_scheme"] = color_scheme
    return payload


PAYLOAD_BUILDERS = {
    "hero": _build_hero_payload,
    "key-insight": _build_key_insight_payload,
    "insight-card": _build_insight_card_payload,
    "insight-story": _build_insight_story_payload,
    "comparison": _build_comparison_payload,
    "story": _build_story_payload,
    "timeline": _build_timeline_payload,
    "funnel": _build_funnel_payload,
    "grid": _build_grid_payload,
    "equation": _build_equation_payload,
}
PAYLOAD_BUILDERS["insight"] = PAYLOAD_BUILDERS["key-insight"]

# Control args excluded from generic fallback payload
_CONTROL_ARGS = frozenset({
    "command", "output", "layout", "theme", "density", "png",
    "export_preset", "crop_mode", "padding_mode", "title", "person", "website",
})


def handle_create(args) -> int:
    """Handle the 'create' command."""
    if not getattr(args, 'layout', None):
        import sys as _sys
        from .suggest import suggest_layout_top_n, LAYOUT_DESCRIPTIONS
        if _sys.stdin.isatty():
            try:
                desc = input("What do you want to show? ")
            except (EOFError, KeyboardInterrupt):
                print("")
                return 0
            results = suggest_layout_top_n(desc, n=3)
            best = results[0]
            print(f"\nSuggested layout: {best.layout} (confidence: {best.confidence})")
            print(f"  {LAYOUT_DESCRIPTIONS.get(best.layout, '')}")
            print(f"\nTry:\n  {best.example_command}")
            if len(results) > 1:
                print("\nAlternatives:")
                for alt in results[1:]:
                    print(f"  {alt.layout} — {LAYOUT_DESCRIPTIONS.get(alt.layout, '')} (matched: {alt.reason})")
            try:
                confirm = input("\nRun the suggested command? [Y/n] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("")
                return 0
            if confirm in ("", "y", "yes"):
                args.layout = best.layout
            else:
                print("\nAvailable layouts:")
                for lt, desc_text in sorted(LAYOUT_DESCRIPTIONS.items()):
                    print(f"  {lt:18s} {desc_text}")
                return 0
        else:
            print("Error: --layout is required in non-interactive mode.")
            print("Use: modern-graphics create --layout <layout> --output <path>")
            print("Run 'modern-graphics create --help' to see available layouts.")
            return 1
    output_path = Path(args.output)
    attribution = Attribution(
        person=getattr(args, 'person', 'Greg Meyer'),
        website=getattr(args, 'website', 'gregmeyer.com'),
    )
    if getattr(args, 'png', False) and output_path.suffix != '.png':
        output_path = output_path.with_suffix('.png')

    use_pretext = getattr(args, 'text_render', 'css') == 'pretext'
    generator = ModernGraphicsGenerator(
        getattr(args, 'title', 'Modern Graphic'),
        attribution=attribution,
        use_pretext=use_pretext,
    )
    density = normalize_density(getattr(args, "density", "clarity"))
    color_scheme = get_scheme(getattr(args, 'theme', None)) if getattr(args, 'theme', None) else None

    layout_type = args.layout
    if layout_type == "insight":
        layout_type = "key-insight"

    builder = PAYLOAD_BUILDERS.get(args.layout)
    if builder is not None:
        payload = builder(args, density, color_scheme)
        # Builder returns an int error code on validation failure
        if isinstance(payload, int):
            return payload
    else:
        # Generic fallback: pass all non-control args as kwargs
        payload = {
            k: v for k, v in vars(args).items()
            if k not in _CONTROL_ARGS and v is not None
        }

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
