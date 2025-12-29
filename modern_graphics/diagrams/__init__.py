"""Diagram generators for Modern Graphics"""

from typing import Dict, Type
from .base import DiagramGenerator
from .cycle import generate_cycle_diagram, CycleDiagramGenerator
from .comparison import generate_comparison_diagram
from .grid import generate_grid_diagram
from .flywheel import generate_flywheel_diagram
from .timeline import generate_timeline_diagram
from .pyramid import generate_pyramid_diagram
from .before_after import generate_before_after_diagram
from .funnel import generate_funnel_diagram
from .slide_cards import generate_slide_card_diagram, generate_slide_card_comparison
from .premium_card import generate_premium_card
from .story_slide import generate_story_slide
from .creative_story_slide import generate_combo_chart
from .unified_story_slide import generate_unified_story_slide
from .wireframe import generate_wireframe_diagram, generate_wireframe_comparison
from .insight import generate_insight_story, generate_key_insight, generate_insight_card
from .wireframe_svg import (
    WireframeSVGConfig,
    generate_chat_panel_svg,
    generate_modal_form_svg,
    generate_ticket_flow_svg,
    generate_before_wireframe_svg,
    generate_after_wireframe_svg,
)
from .wireframe_scene import (
    render_scene,
    list_element_types,
    list_presets,
    SCENE_PRESETS,
    ELEMENT_REGISTRY,
    compute_flow_layout,
    build_flow_elements,
    build_postit_flow_elements,
)
from .transaction_icons_svg import render_transaction_svg
from .mermaid_svg import mermaid_to_svg
from .radar import generate_radar_diagram, RadarDiagramGenerator

# Registry of diagram types
DIAGRAM_REGISTRY: Dict[str, Type[DiagramGenerator]] = {
    "cycle": CycleDiagramGenerator,
    "radar": RadarDiagramGenerator,
    # TODO: Add other diagram generators as classes are created
}

def register_diagram(name: str, diagram_class: Type[DiagramGenerator]):
    """Register a custom diagram type"""
    DIAGRAM_REGISTRY[name] = diagram_class

def get_diagram_generator(name: str) -> Type[DiagramGenerator]:
    """Get diagram generator class by name"""
    return DIAGRAM_REGISTRY.get(name)

__all__ = [
    'DiagramGenerator',
    'DIAGRAM_REGISTRY',
    'register_diagram',
    'get_diagram_generator',
    'generate_cycle_diagram',
    'CycleDiagramGenerator',
    'generate_comparison_diagram',
    'generate_grid_diagram',
    'generate_flywheel_diagram',
    'generate_timeline_diagram',
    'generate_pyramid_diagram',
    'generate_before_after_diagram',
    'generate_funnel_diagram',
    'generate_slide_card_diagram',
    'generate_slide_card_comparison',
    'generate_premium_card',
    'generate_story_slide',
    'generate_combo_chart',
    'generate_unified_story_slide',
    'generate_wireframe_diagram',
    'generate_wireframe_comparison',
    'generate_insight_story',
    'generate_key_insight',
    'generate_insight_card',
    'generate_radar_diagram',
    'RadarDiagramGenerator',
    # SVG wireframe generators
    'WireframeSVGConfig',
    'generate_chat_panel_svg',
    'generate_modal_form_svg',
    'generate_ticket_flow_svg',
    'generate_before_wireframe_svg',
    'generate_after_wireframe_svg',
    # Scene-spec wireframe
    'render_scene',
    'list_element_types',
    'list_presets',
    'SCENE_PRESETS',
    'ELEMENT_REGISTRY',
    'compute_flow_layout',
    'build_flow_elements',
    'build_postit_flow_elements',
    'render_transaction_svg',
    'mermaid_to_svg',
]
