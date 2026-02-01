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


def generate_premium_card(
    title: str,
    tagline: str,
    subtext: str,
    eyebrow: str,
    features: List[str],
    hero: Dict[str, Any],
    palette: Dict[str, str],
    canvas_size: int = 1100,
    show_top_panel: bool = True,
    show_bottom_panel: bool = True,
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience helper to render the stacked premium card layout."""
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = generator.generate_premium_card(
        title=title,
        tagline=tagline,
        subtext=subtext,
        eyebrow=eyebrow,
        features=features,
        hero=hero,
        palette=palette,
        canvas_size=canvas_size,
        show_top_panel=show_top_panel,
        show_bottom_panel=show_bottom_panel,
    )
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


def generate_wireframe_diagram(
    title: str,
    variant: str = "chat-panel",
    diagram_title: Optional[str] = None,
    subtitle: Optional[str] = None,
    eyebrow: Optional[str] = None,
    chat_messages: Optional[List[Dict[str, Any]]] = None,
    chat_inline_card: Optional[Dict[str, Any]] = None,
    chat_action_buttons: Optional[List[Dict[str, Any]]] = None,
    chat_quick_actions: Optional[List[str]] = None,
    modal_title: str = "Submit Support Request",
    modal_fields: Optional[List[Dict[str, str]]] = None,
    modal_submit_text: str = "Submit Request",
    success_toast: Optional[Dict[str, str]] = None,
    status: Optional[Dict[str, str]] = None,
    ticket_status: Optional[Dict[str, Any]] = None,
    width: int = 600,
    height: int = 520,
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function to generate wireframe diagram.
    
    Args:
        title: Generator title
        variant: Wireframe variant - "chat-panel", "modal-form", "dashboard"
        diagram_title: Title displayed above wireframe
        subtitle: Subtitle text
        eyebrow: Eyebrow text
        chat_messages: Chat messages for chat-panel variant
        chat_inline_card: Inline card config for chat-panel
        chat_action_buttons: Action buttons for chat-panel
        chat_quick_actions: Quick actions for chat-panel
        modal_title: Modal title for modal-form variant
        modal_fields: Form fields for modal-form
        modal_submit_text: Submit button text
        success_toast: Success toast config
        status: Status pill config
        ticket_status: Ticket status flow config
        width: SVG width
        height: SVG height
        output_path: Optional path to save HTML
        attribution: Attribution config
        
    Returns:
        HTML string
    """
    from .diagrams.wireframe import generate_wireframe_diagram as _generate
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _generate(
        generator,
        variant=variant,
        title=diagram_title,
        subtitle=subtitle,
        eyebrow=eyebrow,
        chat_messages=chat_messages,
        chat_inline_card=chat_inline_card,
        chat_action_buttons=chat_action_buttons,
        chat_quick_actions=chat_quick_actions,
        modal_title=modal_title,
        modal_fields=modal_fields,
        modal_submit_text=modal_submit_text,
        success_toast=success_toast,
        status=status,
        ticket_status=ticket_status,
        width=width,
        height=height,
    )
    if output_path:
        generator.save(html, output_path)
    return html


def generate_wireframe_comparison(
    title: str,
    before: Dict[str, Any],
    after: Dict[str, Any],
    headline: Optional[str] = None,
    subheadline: Optional[str] = None,
    eyebrow: Optional[str] = None,
    insight: Optional[str] = None,
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function to generate before/after wireframe comparison.
    
    Args:
        title: Generator title
        before: Config dict for "before" wireframe
        after: Config dict for "after" wireframe
        headline: Main headline
        subheadline: Subtitle
        eyebrow: Eyebrow text
        insight: Key insight text for bottom card
        output_path: Optional path to save HTML
        attribution: Attribution config
        
    Returns:
        HTML string
    """
    from .diagrams.wireframe import generate_wireframe_comparison as _generate
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _generate(
        generator,
        before=before,
        after=after,
        headline=headline,
        subheadline=subheadline,
        eyebrow=eyebrow,
        insight=insight,
    )
    if output_path:
        generator.save(html, output_path)
    return html


def generate_insight_story(
    title: str,
    headline: str,
    subtitle: Optional[str] = None,
    eyebrow: Optional[str] = None,
    before_svg: Optional[str] = None,
    before_label: str = "Before",
    before_status: Optional[Dict[str, str]] = None,
    after_svg: Optional[str] = None,
    after_label: str = "After",
    after_status: Optional[Dict[str, str]] = None,
    shift_from: Optional[str] = None,
    shift_to: Optional[str] = None,
    shift_badge: Optional[str] = None,
    insight_text: str = "",
    insight_label: str = "Key Insight",
    stats: Optional[List[Dict[str, str]]] = None,
    accent_color: str = "#0071e3",
    success_color: str = "#34c759",
    error_color: str = "#ff3b30",
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function to generate an insight story graphic.
    
    A full insight graphic with visual comparison panels (before/after SVGs),
    key insight callout, and footer stats.
    
    Args:
        title: Generator title
        headline: Main headline
        subtitle: Subtitle text
        eyebrow: Eyebrow text above headline
        before_svg: SVG content for "before" panel
        before_label: Label for before panel
        before_status: Status dict with 'type' and 'text'
        after_svg: SVG content for "after" panel
        after_label: Label for after panel
        after_status: Status dict with 'type' and 'text'
        shift_from: Left side of shift badge
        shift_to: Right side of shift badge
        shift_badge: Additional badge text
        insight_text: The key insight text (supports HTML)
        insight_label: Label above insight text
        stats: List of stat dicts with 'label' and 'value'
        accent_color: Primary accent color
        success_color: Success/positive color
        error_color: Error/negative color
        output_path: Optional path to save HTML
        attribution: Attribution config
        
    Returns:
        HTML string
    """
    from .diagrams.insight import generate_insight_story as _generate
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _generate(
        generator,
        headline=headline,
        subtitle=subtitle,
        eyebrow=eyebrow,
        before_svg=before_svg,
        before_label=before_label,
        before_status=before_status,
        after_svg=after_svg,
        after_label=after_label,
        after_status=after_status,
        shift_from=shift_from,
        shift_to=shift_to,
        shift_badge=shift_badge,
        insight_text=insight_text,
        insight_label=insight_label,
        stats=stats,
        accent_color=accent_color,
        success_color=success_color,
        error_color=error_color,
    )
    if output_path:
        generator.save(html, output_path)
    return html


def generate_key_insight(
    title: str,
    text: str,
    label: str = "Key Insight",
    eyebrow: Optional[str] = None,
    context: Optional[str] = None,
    accent_color: str = "#0071e3",
    variant: str = "default",
    icon: str = "lightning",
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function to generate a standalone key insight / pull quote.
    
    Args:
        title: Generator title
        text: The insight text (supports HTML for bold/highlight)
        label: Label above the insight
        eyebrow: Optional eyebrow text above label
        context: Optional context text below the insight
        accent_color: Primary accent color
        variant: Style variant - "default", "minimal", "bold", "quote"
        icon: Icon type - "lightning", "lightbulb", "quote", "star", "none"
        output_path: Optional path to save HTML
        attribution: Attribution config
        
    Returns:
        HTML string
    """
    from .diagrams.insight import generate_key_insight as _generate
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _generate(
        generator,
        text=text,
        label=label,
        eyebrow=eyebrow,
        context=context,
        accent_color=accent_color,
        variant=variant,
        icon=icon,
    )
    if output_path:
        generator.save(html, output_path)
    return html


def generate_insight_card(
    title: str,
    text: str,
    svg_content: str,
    label: str = "Key Insight",
    svg_label: Optional[str] = None,
    eyebrow: Optional[str] = None,
    context: Optional[str] = None,
    layout: str = "side-by-side",
    svg_position: str = "right",
    accent_color: str = "#0071e3",
    variant: str = "bold",
    icon: str = "lightning",
    output_path: Optional[Path] = None,
    attribution: Optional[Attribution] = None,
) -> str:
    """Convenience function to generate an insight card with SVG illustration.
    
    Combines a key insight (pull quote) with an illustrative SVG in a
    compact card format suitable for inline use.
    
    Args:
        title: Generator title
        text: The insight text (supports HTML for bold/highlight)
        svg_content: SVG string to display
        label: Label above the insight
        svg_label: Optional label above the SVG
        eyebrow: Optional eyebrow text
        context: Optional context text below insight
        layout: "side-by-side" or "stacked"
        svg_position: "left" or "right" for side-by-side layout
        accent_color: Primary accent color
        variant: Style variant - "default" or "bold"
        icon: Icon type - "lightning", "lightbulb", "quote", "star", "none"
        output_path: Optional path to save HTML
        attribution: Attribution config
        
    Returns:
        HTML string
    """
    from .diagrams.insight import generate_insight_card as _generate
    generator = ModernGraphicsGenerator(title, attribution=attribution)
    html = _generate(
        generator,
        text=text,
        svg_content=svg_content,
        label=label,
        svg_label=svg_label,
        eyebrow=eyebrow,
        context=context,
        layout=layout,
        svg_position=svg_position,
        accent_color=accent_color,
        variant=variant,
        icon=icon,
    )
    if output_path:
        generator.save(html, output_path)
    return html
