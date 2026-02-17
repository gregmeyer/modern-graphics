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
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="hero-triptych",
            render_fn=generate_modern_hero_triptych,
            required_args={"headline", "columns"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="insight-story",
            render_fn=generate_insight_story,
            required_args={"headline", "insight_text"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="key-insight",
            render_fn=generate_key_insight,
            required_args={"text"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="insight-card",
            render_fn=generate_insight_card,
            required_args={"text", "svg_content"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="comparison",
            render_fn=_render_comparison,
            required_args={"left_column", "right_column"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="timeline",
            render_fn=_render_timeline,
            required_args={"events"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="funnel",
            render_fn=_render_funnel,
            required_args={"stages"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="grid",
            render_fn=_render_grid,
            required_args={"items"},
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="story",
            render_fn=_render_story,
            required_args=set(),
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
