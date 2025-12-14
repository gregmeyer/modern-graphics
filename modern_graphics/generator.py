"""Generator class for Modern Graphics"""

from typing import List, Dict, Optional
from pathlib import Path

from .models import Attribution, StepStyle
from .base import BaseGenerator
from .diagrams import (
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
    DIAGRAM_REGISTRY,
    get_diagram_generator,
)


class ModernGraphicsGenerator(BaseGenerator):
    """Generator for modern HTML/CSS graphics"""
    
    def generate_diagram(self, diagram_type: str, **kwargs) -> str:
        """Generate diagram by type name using registry
        
        Args:
            diagram_type: Name of diagram type (e.g., 'cycle', 'comparison')
            **kwargs: Diagram-specific parameters
            
        Returns:
            HTML string for the diagram
            
        Raises:
            ValueError: If diagram type is unknown or input is invalid
        """
        diagram_class = get_diagram_generator(diagram_type)
        if not diagram_class:
            raise ValueError(f"Unknown diagram type: {diagram_type}. Available types: {list(DIAGRAM_REGISTRY.keys())}")
        
        diagram_gen = diagram_class()
        if not diagram_gen.validate_input(**kwargs):
            raise ValueError(f"Invalid input for {diagram_type} diagram")
        
        return diagram_gen.generate(self, **kwargs)
    
    def _generate_step_style(
        self,
        style: Optional[StepStyle] = None,
        color_key: Optional[str] = None
    ) -> str:
        """Generate CSS for a step/box - delegates to utils module"""
        from .utils import generate_step_style
        return generate_step_style(style, color_key, template=self.template)
    
    def generate_cycle_diagram(
        self,
        steps: List[Dict[str, any]],
        arrow_text: str = "→",
        cycle_end_text: Optional[str] = None,
        attribution_on_last: bool = True
    ) -> str:
        """Generate a cycle/flow diagram"""
        from .diagrams.cycle import generate_cycle_diagram as _generate
        return _generate(self, steps, arrow_text, cycle_end_text, attribution_on_last)
    
    def generate_comparison_diagram(
        self,
        left_column: Dict[str, any],
        right_column: Dict[str, any],
        vs_text: str = "vs"
    ) -> str:
        """Generate a comparison diagram"""
        from .diagrams.comparison import generate_comparison_diagram as _generate
        return _generate(self, left_column, right_column, vs_text)
    
    def generate_grid_diagram(
        self,
        items: List[Dict[str, any]],
        columns: int = 5,
        convergence: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a grid diagram"""
        from .diagrams.grid import generate_grid_diagram as _generate
        return _generate(self, items, columns, convergence)
    
    def generate_flywheel_diagram(
        self,
        elements: List[Dict[str, any]],
        center_label: Optional[str] = None,
        radius: int = 200
    ) -> str:
        """Generate a flywheel diagram"""
        from .diagrams.flywheel import generate_flywheel_diagram as _generate
        return _generate(self, elements, center_label, radius)
    
    def generate_timeline_diagram(
        self,
        events: List[Dict[str, any]],
        orientation: str = "horizontal"
    ) -> str:
        """Generate a timeline diagram"""
        from .diagrams.timeline import generate_timeline_diagram as _generate
        return _generate(self, events, orientation)
    
    def generate_pyramid_diagram(
        self,
        layers: List[Dict[str, any]],
        orientation: str = "up"
    ) -> str:
        """Generate a pyramid diagram"""
        from .diagrams.pyramid import generate_pyramid_diagram as _generate
        return _generate(self, layers, orientation)
    
    def generate_before_after_diagram(
        self,
        before_items: List[str],
        after_items: List[str],
        transition_text: str = "→"
    ) -> str:
        """Generate a before/after diagram"""
        from .diagrams.before_after import generate_before_after_diagram as _generate
        return _generate(self, before_items, after_items, transition_text)
    
    def generate_funnel_diagram(
        self,
        stages: List[Dict[str, any]],
        show_percentages: bool = False
    ) -> str:
        """Generate a funnel diagram"""
        from .diagrams.funnel import generate_funnel_diagram as _generate
        return _generate(self, stages, show_percentages)
    
    def generate_slide_card_diagram(
        self,
        cards: List[Dict[str, any]],
        arrow_text: str = "→"
    ) -> str:
        """Generate a horizontal slide card diagram"""
        return generate_slide_card_diagram(self, cards, arrow_text)
    
    def generate_slide_card_comparison(
        self,
        left_card: Dict[str, any],
        right_card: Dict[str, any],
        vs_text: str = "→"
    ) -> str:
        """Generate a side-by-side slide card comparison"""
        return generate_slide_card_comparison(self, left_card, right_card, vs_text)
    
    def generate_story_slide(
        self,
        title: str,
        what_changed: str,
        time_period: str,
        what_it_means: str,
        insight: Optional[str] = None,
        evolution_data: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Generate a story-driven slide"""
        from .diagrams.story_slide import generate_story_slide as _generate
        return _generate(
            self,
            title=title,
            what_changed=what_changed,
            time_period=time_period,
            what_it_means=what_it_means,
            insight=insight,
            evolution_data=evolution_data
        )
