"""Convenience functions for Modern Graphics Generator"""

from typing import List, Dict, Optional, Any
from pathlib import Path

from .models import Attribution
from .generator import ModernGraphicsGenerator
from .diagrams.modern_hero import generate_modern_hero as _modern_hero, generate_modern_hero_triptych as _modern_hero_triptych

def generate_flywheel_diagram(
    title: str,
    elements: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate flywheel diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_flywheel_diagram(elements, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_cycle_diagram(
    title: str,
    steps: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate cycle diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_cycle_diagram(steps, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_comparison_diagram(
    title: str,
    left_column: Dict[str, any],
    right_column: Dict[str, any],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate comparison diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_comparison_diagram(left_column, right_column, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_grid_diagram(
    title: str,
    items: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate grid diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_grid_diagram(items, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_timeline_diagram(
    title: str,
    events: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate timeline diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_timeline_diagram(events, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_pyramid_diagram(
    title: str,
    layers: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate pyramid diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_pyramid_diagram(layers, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_before_after_diagram(
    title: str,
    before_items: List[str],
    after_items: List[str],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate before/after diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_before_after_diagram(before_items, after_items, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_funnel_diagram(
    title: str,
    stages: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate funnel diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_funnel_diagram(stages, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_slide_card_diagram(
    title: str,
    cards: List[Dict[str, any]],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate slide card diagram"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_slide_card_diagram(cards, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_slide_card_comparison(
    title: str,
    left_card: Dict[str, any],
    right_card: Dict[str, any],
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    **kwargs
) -> str:
    """Convenience function to generate slide card comparison"""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_slide_card_comparison(left_card, right_card, **kwargs)
    if output_path:
        generator.save(html, output_path)
    return html


def generate_story_slide(
    title: str,
    what_changed: str,
    time_period: str,
    what_it_means: str,
    insight: Optional[str] = None,
    evolution_data: Optional[List[Dict[str, str]]] = None,
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
    top_tile_only: bool = False,
    hero_use_svg_js: bool = False,
    hero_variant: str = "auto",
    story_cards: Optional[List[Dict[str, Any]]] = None,
    hero_canvas_cards: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Convenience function to generate story-driven slide"""
    from .diagrams.story_slide import generate_story_slide as _generate
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _generate(
        generator,
        title=title,
        what_changed=what_changed,
        time_period=time_period,
        what_it_means=what_it_means,
        insight=insight,
        evolution_data=evolution_data,
        top_tile_only=top_tile_only,
        hero_use_svg_js=hero_use_svg_js,
        hero_variant=hero_variant,
        story_cards=story_cards,
        hero_canvas_cards=hero_canvas_cards
    )
    if output_path:
        generator.save(html, output_path)
    return html


def generate_modern_hero(
    title: str,
    headline: str,
    subheadline: Optional[str] = None,
    eyebrow: Optional[str] = None,
    highlights: Optional[List[str]] = None,
    highlight_tiles: Optional[List[Dict[str, str]]] = None,
    flow_nodes: Optional[List[Dict[str, Any]]] = None,
    flow_connections: Optional[List[Dict[str, str]]] = None,
    freeform_canvas: Optional[str] = None,
    stats: Optional[List[Dict[str, str]]] = None,
    cta: Optional[str] = None,
    background_variant: str = "light",
    visual_description: Optional[str] = None,
    headline_align: str = "left",
    subheadline_align: Optional[str] = None,
    graphic_position: str = "center",
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function for the open modern hero layout."""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _modern_hero(
        generator,
        headline=headline,
        subheadline=subheadline,
        eyebrow=eyebrow,
        highlights=highlights,
        highlight_tiles=highlight_tiles,
        flow_nodes=flow_nodes,
        flow_connections=flow_connections,
        freeform_canvas=freeform_canvas,
        stats=stats,
        cta=cta,
        background_variant=background_variant,
        visual_description=visual_description,
        headline_align=headline_align,
        subheadline_align=subheadline_align,
        graphic_position=graphic_position,
    )
    if output_path:
        generator.save(html, output_path)
    return html


def generate_modern_hero_triptych(
    title: str,
    headline: str,
    subheadline: Optional[str],
    columns: List[Dict[str, any]],
    stats: Optional[List[Dict[str, str]]] = None,
    eyebrow: Optional[str] = None,
    headline_align: str = "left",
    subheadline_align: Optional[str] = None,
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function for the triptych hero layout."""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _modern_hero_triptych(
        generator,
        headline=headline,
        subheadline=subheadline,
        columns=columns,
        stats=stats,
        eyebrow=eyebrow,
        headline_align=headline_align,
        subheadline_align=subheadline_align,
    )
    if output_path:
        generator.save(html, output_path)
    return html
