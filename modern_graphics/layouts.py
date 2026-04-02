"""Layout strategy registry for Phase 2 architecture.

This module introduces a strategy-style dispatch layer so layouts can be
registered and rendered through a consistent interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Set

from .base import BaseGenerator


RenderFn = Callable[..., str]


@dataclass
class LayoutStrategy:
    """Single layout strategy contract."""

    layout_type: str
    render_fn: RenderFn
    required_args: Set[str] = field(default_factory=set)
    description: str = ""
    example_command: str = ""
    keywords: List[str] = field(default_factory=list)

    def validate(self, kwargs: Dict[str, object]) -> None:
        missing = sorted(arg for arg in self.required_args if kwargs.get(arg) in (None, ""))
        if missing:
            missing_str = ", ".join(missing)
            raise ValueError(
                f"Missing required args for layout '{self.layout_type}': {missing_str}"
            )

    def render(self, generator: BaseGenerator, **kwargs: object) -> str:
        self.validate(kwargs)
        return self.render_fn(generator, **kwargs)


class LayoutStrategyRegistry:
    """Registry for layout strategies."""

    def __init__(self) -> None:
        self._strategies: Dict[str, LayoutStrategy] = {}

    def register(self, strategy: LayoutStrategy) -> None:
        key = strategy.layout_type.strip().lower()
        self._strategies[key] = strategy

    def get(self, layout_type: str) -> Optional[LayoutStrategy]:
        return self._strategies.get(layout_type.strip().lower())

    def list_types(self) -> List[str]:
        return sorted(self._strategies.keys())

    def render(self, layout_type: str, generator: BaseGenerator, **kwargs: object) -> str:
        strategy = self.get(layout_type)
        if strategy is None:
            available = ", ".join(self.list_types())
            raise ValueError(
                f"Unknown layout strategy '{layout_type}'. Available: {available}"
            )
        return strategy.render(generator, **kwargs)


def _build_default_registry() -> LayoutStrategyRegistry:
    # Import lazily so strategy scaffolding does not create heavy import loops.
    from .diagrams.insight import (
        generate_insight_card,
        generate_insight_story,
        generate_key_insight,
    )
    from .diagrams.modern_hero import generate_modern_hero, generate_modern_hero_triptych
    from .diagrams.story_slide import generate_story_slide
    from .diagrams.equation import generate_equation

    def _render_comparison(generator: BaseGenerator, **kwargs: object) -> str:
        return generator.generate_comparison_diagram(
            left_column=kwargs["left_column"],
            right_column=kwargs["right_column"],
            vs_text=str(kwargs.get("vs_text", "vs")),
            color_scheme=kwargs.get("color_scheme"),
        )

    def _render_timeline(generator: BaseGenerator, **kwargs: object) -> str:
        return generator.generate_timeline_diagram(
            events=kwargs["events"],
            orientation=str(kwargs.get("orientation", "horizontal")),
            color_scheme=kwargs.get("color_scheme"),
        )

    def _render_funnel(generator: BaseGenerator, **kwargs: object) -> str:
        return generator.generate_funnel_diagram(
            stages=kwargs["stages"],
            show_percentages=bool(kwargs.get("show_percentages", False)),
            color_scheme=kwargs.get("color_scheme"),
        )

    def _render_grid(generator: BaseGenerator, **kwargs: object) -> str:
        return generator.generate_grid_diagram(
            items=kwargs["items"],
            columns=int(kwargs.get("columns", 5)),
            convergence=kwargs.get("convergence"),
            color_scheme=kwargs.get("color_scheme"),
        )

    def _render_story(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_story_slide(
            generator,
            title=kwargs.get("title"),
            what_changed=kwargs.get("what_changed"),
            time_period=kwargs.get("time_period"),
            what_it_means=kwargs.get("what_it_means"),
            insight=kwargs.get("insight"),
        )

    registry = LayoutStrategyRegistry()
    registry.register(
        LayoutStrategy(
            layout_type="hero",
            render_fn=generate_modern_hero,
            required_args={"headline"},
            description="Bold opener with headline, subheadline, and optional highlights",
            example_command='modern-graphics create --layout hero --headline "Execution scales" --output hero.html',
            keywords=["hero", "opener", "headline", "banner", "title slide", "cover slide", "opening slide"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="hero-triptych",
            render_fn=generate_modern_hero_triptych,
            required_args={"headline", "columns"},
            description="Three-column hero with headline and panels",
            example_command='modern-graphics create --layout hero-triptych --headline "Three pillars" --columns "A,B,C" --output triptych.html',
            keywords=["triptych", "three column", "three-column", "triple"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="insight-story",
            render_fn=generate_insight_story,
            required_args={"headline", "insight_text"},
            description="Before/after narrative with insight callout",
            example_command='modern-graphics create --layout insight-story --headline "When shipping gets easy" --insight-text "Use checklist gates" --output insight-story.html',
            keywords=["insight story", "before after insight", "before/after insight"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="key-insight",
            render_fn=generate_key_insight,
            required_args={"text"},
            description="Standalone pull quote or key takeaway",
            example_command='modern-graphics create --layout key-insight --text "Key takeaway" --output insight.html',
            keywords=["quote", "insight", "key point", "pullquote", "pull quote", "takeaway", "one thing"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="insight-card",
            render_fn=generate_insight_card,
            required_args={"text", "svg_content"},
            description="Insight text paired with an SVG visual panel",
            example_command='modern-graphics create --layout insight-card --text "Key takeaway" --output insight-card.html',
            keywords=["insight card", "insight with image", "insight with svg", "card with visual"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="comparison",
            render_fn=_render_comparison,
            required_args={"left_column", "right_column"},
            description="Side-by-side comparison of two approaches",
            example_command='modern-graphics create --layout comparison --left "Before:Manual:Slow" --right "After:Agentic:Faster" --output comparison.html',
            keywords=["compare", "vs", "versus", "before and after", "tradeoff", "trade-off", "pros cons", "side by side", "side-by-side"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="timeline",
            render_fn=_render_timeline,
            required_args={"events"},
            description="Chronological sequence of events or milestones",
            example_command='modern-graphics create --layout timeline --events "Q1|Baseline,Q2|Adoption" --output timeline.html',
            keywords=["timeline", "chronolog", "milestones", "roadmap", "events over time"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="funnel",
            render_fn=_render_funnel,
            required_args={"stages"},
            description="Conversion funnel with stages and values",
            example_command='modern-graphics create --layout funnel --stages "Visit,Trial,Paid" --values "100,40,12" --output funnel.html',
            keywords=["funnel", "conversion", "pipeline", "drop-off", "dropoff", "stages of"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="grid",
            render_fn=_render_grid,
            required_args={"items"},
            description="Numbered item grid with optional convergence goal",
            example_command='modern-graphics create --layout grid --items "A,B,C" --columns 3 --output grid.html',
            keywords=["list", "grid", "items", "options", "priorities", "top ", "checklist", "inventory"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="story",
            render_fn=_render_story,
            required_args=set(),
            description="Narrative block: what changed, over what period, why it matters",
            example_command='modern-graphics create --layout story --what-changed "Execution accelerated" --output story.html',
            keywords=["story", "narrative", "what changed", "transformation", "journey", "evolution"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="equation",
            render_fn=generate_equation,
            required_args={"equation"},
            description="Mathematical-style equation as visual centerpiece",
            example_command='modern-graphics create --layout equation --equation "Satisfaction = Perception - Expectation" --output equation.html',
            keywords=["equation", "formula", "math", "equals", "expression"],
        )
    )
    return registry


DEFAULT_LAYOUT_REGISTRY = _build_default_registry()


def list_layout_strategies() -> List[str]:
    return DEFAULT_LAYOUT_REGISTRY.list_types()


def register_layout_strategy(strategy: LayoutStrategy) -> None:
    DEFAULT_LAYOUT_REGISTRY.register(strategy)


def render_layout(
    layout_type: str,
    generator: BaseGenerator,
    **kwargs: object,
) -> str:
    return DEFAULT_LAYOUT_REGISTRY.render(layout_type, generator, **kwargs)
