"""Generator class for Modern Graphics"""

from typing import List, Dict, Optional, Any
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
    generate_radar_diagram,
    DIAGRAM_REGISTRY,
    get_diagram_generator,
)
from .diagrams.modern_hero import generate_modern_hero, generate_modern_hero_triptych


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
        attribution_on_last: bool = True,
        color_scheme: Optional["ColorScheme"] = None,
        show_loop_indicator: bool = True,
    ) -> str:
        """Generate a cycle/flow diagram"""
        from .diagrams.cycle import generate_cycle_diagram as _generate
        return _generate(
            self, steps, arrow_text, cycle_end_text, attribution_on_last, color_scheme, show_loop_indicator
        )
    
    def generate_comparison_diagram(
        self,
        left_column: Dict[str, any],
        right_column: Dict[str, any],
        vs_text: str = "vs",
        color_scheme: Optional["ColorScheme"] = None
    ) -> str:
        """Generate a comparison diagram"""
        from .diagrams.comparison import generate_comparison_diagram as _generate
        return _generate(self, left_column, right_column, vs_text, color_scheme)
    
    def generate_grid_diagram(
        self,
        items: List[Dict[str, any]],
        columns: int = 5,
        convergence: Optional[Dict[str, str]] = None,
        color_scheme: Optional["ColorScheme"] = None
    ) -> str:
        """Generate a grid diagram"""
        from .diagrams.grid import generate_grid_diagram as _generate
        return _generate(self, items, columns, convergence, color_scheme)
    
    def generate_flywheel_diagram(
        self,
        elements: List[Dict[str, any]],
        center_label: Optional[str] = None,
        radius: int = 200,
        color_scheme: Optional["ColorScheme"] = None
    ) -> str:
        """Generate a flywheel diagram"""
        from .diagrams.flywheel import generate_flywheel_diagram as _generate
        return _generate(self, elements, center_label, radius, color_scheme)
    
    def generate_timeline_diagram(
        self,
        events: List[Dict[str, any]],
        orientation: str = "horizontal",
        color_scheme: Optional["ColorScheme"] = None
    ) -> str:
        """Generate a timeline diagram"""
        from .diagrams.timeline import generate_timeline_diagram as _generate
        return _generate(self, events, orientation, color_scheme)
    
    def generate_pyramid_diagram(
        self,
        layers: List[Dict[str, any]],
        orientation: str = "up",
        color_scheme: Optional["ColorScheme"] = None,
    ) -> str:
        """Generate a pyramid diagram"""
        from .diagrams.pyramid import generate_pyramid_diagram as _generate
        return _generate(self, layers, orientation, color_scheme)
    
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
        show_percentages: bool = False,
        color_scheme: Optional["ColorScheme"] = None,
    ) -> str:
        """Generate a funnel diagram"""
        from .diagrams.funnel import generate_funnel_diagram as _generate
        return _generate(self, stages, show_percentages, color_scheme)
    
    def generate_radar_diagram(
        self,
        signals: List[Dict[str, any]],
        center_label: str = "Support Radar",
        viewbox_width: int = 1200,
        viewbox_height: int = 700,
        radar_radius: int = 250,
        show_sweep: bool = True,
        show_circles: bool = True,
    ) -> str:
        """Generate a radar diagram with signals positioned around a center point.
        
        Args:
            center_label: Label for the center radar dish
            signals: List of signal dictionaries with:
                - label: Signal text
                - axiom: Axiom identifier or name
                - detects: What signal it detects
                - discovers: Type of failure discovered
                - covers: What it covers (optional)
                - position: Dict with 'angle' (degrees) or 'x', 'y' (0-1 normalized)
                - color: Color key (blue, purple, green, orange, gray)
            viewbox_width: SVG viewBox width
            viewbox_height: SVG viewBox height
            radar_radius: Radius of the outer radar circle
            show_sweep: Whether to show animated radar sweep
            show_circles: Whether to show concentric radar circles
        """
        return generate_radar_diagram(
            self,
            signals=signals,
            center_label=center_label,
            viewbox_width=viewbox_width,
            viewbox_height=viewbox_height,
            radar_radius=radar_radius,
            show_sweep=show_sweep,
            show_circles=show_circles,
        )
    
    def generate_slide_card_diagram(
        self,
        cards: List[Dict[str, any]],
        arrow_text: str = "→",
        style: str = "default",
        color_scheme: Optional["ColorScheme"] = None,
    ) -> str:
        """Generate a horizontal slide card diagram
        
        Args:
            cards: List of card dictionaries
            arrow_text: Text to display between cards
            style: Layout style - 'default' (vertical cards) or 'lower_third' (horizontal bar style)
            color_scheme: Optional ColorScheme for theming
        """
        return generate_slide_card_diagram(self, cards, arrow_text, style, color_scheme)
    
    def generate_slide_card_comparison(
        self,
        left_card: Dict[str, any],
        right_card: Dict[str, any],
        vs_text: str = "→",
        color_scheme: Optional["ColorScheme"] = None,
    ) -> str:
        """Generate a side-by-side slide card comparison"""
        return generate_slide_card_comparison(self, left_card, right_card, vs_text, color_scheme)

    def generate_premium_card(
        self,
        *,
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
    ) -> str:
        """Generate a stacked premium card with hero + body panels."""
        from .diagrams.premium_card import generate_premium_card as _generate

        return _generate(
            self,
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

    def generate_modern_hero(
        self,
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
        color_scheme: Optional["ColorScheme"] = None,
        insight_callout: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate the open modern hero layout."""
        return generate_modern_hero(
            self,
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
            color_scheme=color_scheme,
            insight_callout=insight_callout,
        )

    def generate_modern_hero_triptych(
        self,
        headline: str,
        subheadline: Optional[str],
        columns: List[Dict[str, any]],
        stats: Optional[List[Dict[str, str]]] = None,
        eyebrow: Optional[str] = None,
        headline_align: str = "left",
        subheadline_align: Optional[str] = None,
    ) -> str:
        """Generate the triptych hero layout (manual → templates → outputs)."""
        return generate_modern_hero_triptych(
            self,
            headline=headline,
            subheadline=subheadline,
            columns=columns,
            stats=stats,
            eyebrow=eyebrow,
            headline_align=headline_align,
            subheadline_align=subheadline_align,
        )
    
    def generate_story_slide(
        self,
        title: Optional[str] = None,
        what_changed: Optional[str] = None,
        time_period: Optional[str] = None,
        what_it_means: Optional[str] = None,
        prompt: Optional[str] = None,
        insight: Optional[str] = None,
        evolution_data: Optional[List[Dict[str, str]]] = None,
        hero_headline: Optional[str] = None,
        hero_subheadline: Optional[str] = None,
        hero_prompt: Optional[str] = None,
        use_ai_hero: bool = True,
        use_unified: bool = True,
        top_tile_only: bool = False,
        hero_use_svg_js: bool = False,
        hero_variant: str = "auto"
    ) -> str:
        """Generate a story-driven slide
        
        Supports both prompt-based (new) and parameter-based (legacy) approaches.
        If prompt is provided, uses unified generator. Otherwise uses legacy parameters.
        
        Args:
            prompt: Optional prompt describing the story (preferred, uses unified generator)
            title: Main slide title (legacy parameter)
            what_changed: What changed (the change) (legacy parameter)
            time_period: Over what time period (legacy parameter)
            what_it_means: What it means (the meaning/implication) (legacy parameter)
            insight: Optional key insight/takeaway
            evolution_data: Optional list of evolution stages
            hero_headline: Optional custom hero headline (overrides AI generation)
            hero_subheadline: Optional custom hero subheadline (overrides AI generation)
            hero_prompt: Optional custom prompt for AI hero generation
            use_ai_hero: If True, use AI to generate hero content (default: True)
            use_unified: If True and prompt provided, use unified generator (default: True)
            top_tile_only: If True, render only the top hero tile
            hero_use_svg_js: Retained for backward compatibility (static tile by default)
            hero_variant: "auto", "light", or "dark" to control hero styling
        """
        from .diagrams.story_slide import generate_story_slide as _generate
        return _generate(
            self,
            title=title,
            what_changed=what_changed,
            time_period=time_period,
            what_it_means=what_it_means,
            prompt=prompt,
            insight=insight,
            evolution_data=evolution_data,
            hero_headline=hero_headline,
            hero_subheadline=hero_subheadline,
            hero_prompt=hero_prompt,
            use_ai_hero=use_ai_hero,
            use_unified=use_unified,
            top_tile_only=top_tile_only,
            hero_use_svg_js=hero_use_svg_js,
            hero_variant=hero_variant
        )
    
    def generate_creative_story_slide(
        self,
        title: str,
        headline: str,
        subheadline: Optional[str] = None,
        story_elements: Optional[List[Dict[str, str]]] = None,
        visualization_type: str = "line",
        data_points: Optional[List[Dict]] = None,
        annotations: Optional[List[str]] = None,
        insight: Optional[str] = None,
        time_range: Optional[str] = None,
        data_source: Optional[str] = None
    ) -> str:
        """Generate a creative, flexible story slide
        
        Args:
            title: Main slide title/category
            headline: Hero headline (main insight)
            subheadline: Optional subheadline
            story_elements: List of key metrics with 'label' and 'value'
            visualization_type: Type of chart (line, bar, area, comparison)
            data_points: Optional data points for visualization
            annotations: List of annotation texts explaining the change
            insight: Key insight text
            time_range: Time range covered
            data_source: Data source attribution
        """
        from .diagrams.creative_story_slide import generate_creative_story_slide as _generate
        return _generate(
            self,
            title=title,
            headline=headline,
            subheadline=subheadline,
            story_elements=story_elements,
            visualization_type=visualization_type,
            data_points=data_points,
            annotations=annotations,
            insight=insight,
            time_range=time_range,
            data_source=data_source
        )
    
    def generate_intelligent_story_slide(
        self,
        prompt: str,
        model: str = "gpt-4-turbo-preview"
    ) -> str:
        """Generate an intelligent, data-driven story slide from a prompt
        
        Uses AI to determine the best visual composition by combining:
        - Data visualizations (charts)
        - Story elements (key metrics)
        - Visual primitives (timelines, comparisons, cycles)
        - Narrative structure
        
        Args:
            prompt: Detailed prompt describing the story/data visualization
            model: OpenAI model to use
        """
        from .diagrams.intelligent_story_slide import generate_intelligent_story_slide as _generate
        return _generate(self, prompt, model)
