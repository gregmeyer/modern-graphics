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
from .story_slide import generate_story_slide

# Registry of diagram types
DIAGRAM_REGISTRY: Dict[str, Type[DiagramGenerator]] = {
    "cycle": CycleDiagramGenerator,
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
    'generate_story_slide',
]
