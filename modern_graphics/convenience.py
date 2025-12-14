"""Convenience functions for Modern Graphics Generator"""

from typing import List, Dict, Optional
from pathlib import Path

from .models import Attribution
from .generator import ModernGraphicsGenerator

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
    attribution: Optional[Attribution] = None
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
        evolution_data=evolution_data
    )
    if output_path:
        generator.save(html, output_path)
    return html
