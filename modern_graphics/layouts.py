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
    from .diagrams.cohort_chart import generate_cohort_chart
    from .diagrams.charts import (
        generate_line_chart,
        generate_stacked_area_chart,
        generate_bar_chart,
        generate_grouped_bar_chart,
        generate_stacked_bar_chart,
        generate_grouped_stacked_bar_chart,
        generate_horizontal_bar_chart,
        generate_pie_chart,
        generate_donut_chart,
        generate_sankey_chart,
    )

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
    def _chart_kwargs(kwargs: Dict[str, object], *keys: str) -> Dict[str, object]:
        return {k: kwargs[k] for k in keys if k in kwargs and kwargs[k] is not None}

    def _render_line_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_line_chart(
            generator,
            labels=kwargs["labels"],
            series=kwargs["series"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "show_legend", "color_scheme"),
        )

    def _render_stacked_area_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_stacked_area_chart(
            generator,
            labels=kwargs["labels"],
            series=kwargs["series"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "show_legend", "color_scheme"),
        )

    def _render_bar_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_bar_chart(
            generator,
            labels=kwargs["labels"],
            values=kwargs["values"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "color_scheme"),
        )

    def _render_grouped_bar_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_grouped_bar_chart(
            generator,
            labels=kwargs["labels"],
            series=kwargs["series"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "show_legend", "color_scheme"),
        )

    def _render_stacked_bar_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_stacked_bar_chart(
            generator,
            labels=kwargs["labels"],
            series=kwargs["series"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "show_legend", "color_scheme"),
        )

    def _render_grouped_stacked_bar_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_grouped_stacked_bar_chart(
            generator,
            labels=kwargs["labels"],
            series=kwargs["series"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "show_legend", "color_scheme"),
        )

    def _render_horizontal_bar_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_horizontal_bar_chart(
            generator,
            labels=kwargs["labels"],
            values=kwargs["values"],
            **_chart_kwargs(kwargs, "title", "subtitle", "x_axis_label", "y_axis_label", "color_scheme"),
        )

    def _render_pie_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_pie_chart(
            generator,
            labels=kwargs["labels"],
            values=kwargs["values"],
            **_chart_kwargs(kwargs, "title", "subtitle", "show_legend", "color_scheme"),
        )

    def _render_donut_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_donut_chart(
            generator,
            labels=kwargs["labels"],
            values=kwargs["values"],
            **_chart_kwargs(kwargs, "title", "subtitle", "show_legend", "color_scheme"),
        )

    def _render_cohort_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_cohort_chart(
            generator,
            cohorts=kwargs["cohorts"],
            **_chart_kwargs(kwargs, "period_labels", "title", "subtitle", "date_label", "size_label", "color_scheme"),
        )

    def _render_sankey_chart(generator: BaseGenerator, **kwargs: object) -> str:
        return generate_sankey_chart(
            generator,
            links=kwargs["links"],
            **_chart_kwargs(kwargs, "nodes", "title", "subtitle", "color_scheme"),
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
    registry.register(
        LayoutStrategy(
            layout_type="line-chart",
            render_fn=_render_line_chart,
            required_args={"labels", "series"},
            description="Line chart with one or more series over a shared x-axis (Chart.js)",
            example_command='modern-graphics create --layout line-chart --labels "Q1,Q2,Q3,Q4" --series \'[{"name":"2024","values":[10,14,18,22]}]\' --output line.png',
            keywords=["line chart", "trend", "over time", "time series", "growth"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="stacked-area-chart",
            render_fn=_render_stacked_area_chart,
            required_args={"labels", "series"},
            description="Stacked area chart showing composition over time (Chart.js)",
            example_command='modern-graphics create --layout stacked-area-chart --labels "2024,2025,2026" --series \'[{"name":"A","values":[10,20,30]}]\' --output stacked-area.png',
            keywords=["stacked area", "area chart", "composition over time", "cohort revenue"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="bar-chart",
            render_fn=_render_bar_chart,
            required_args={"labels", "values"},
            description="Single-series vertical bar chart (Chart.js)",
            example_command='modern-graphics create --layout bar-chart --labels "A,B,C" --values "10,20,15" --output bar.png',
            keywords=["bar chart", "bar graph", "column chart", "vertical bars"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="grouped-bar-chart",
            render_fn=_render_grouped_bar_chart,
            required_args={"labels", "series"},
            description="Grouped (multi-series) vertical bar chart (Chart.js)",
            example_command='modern-graphics create --layout grouped-bar-chart --labels "Q1,Q2" --series \'[{"name":"A","values":[10,12]},{"name":"B","values":[8,14]}]\' --output grouped.png',
            keywords=["grouped bar", "clustered bar", "multi series bar", "side by side bars"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="stacked-bar-chart",
            render_fn=_render_stacked_bar_chart,
            required_args={"labels", "series"},
            description="Stacked bar chart — one bar per x label, each a stack of series (Chart.js)",
            example_command='modern-graphics create --layout stacked-bar-chart --labels "Q1,Q2,Q3" --series \'[{"name":"A","values":[10,12,14]},{"name":"B","values":[5,7,9]}]\' --output stacked-bar.png',
            keywords=["stacked bar", "stacked column", "composition over time bar"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="grouped-stacked-bar-chart",
            render_fn=_render_grouped_stacked_bar_chart,
            required_args={"labels", "series"},
            description="Grouped stacked bar chart (bars side-by-side per x label, each a stack)",
            example_command='modern-graphics create --layout grouped-stacked-bar-chart --labels "Q1,Q2" --series \'[{"name":"A","stack":"2024","values":[10,12]},{"name":"B","stack":"2024","values":[5,7]},{"name":"A","stack":"2025","values":[15,17]},{"name":"B","stack":"2025","values":[8,10]}]\' --output gsb.png',
            keywords=["grouped stacked bar", "stacked grouped bar", "side by side stacked bar", "stack comparison"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="horizontal-bar-chart",
            render_fn=_render_horizontal_bar_chart,
            required_args={"labels", "values"},
            description="Horizontal bar chart for ranked categorical data (Chart.js)",
            example_command='modern-graphics create --layout horizontal-bar-chart --labels "A,B,C" --values "10,20,15" --output hbar.png',
            keywords=["horizontal bar", "ranking", "ranked list", "bar chart horizontal"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="pie-chart",
            render_fn=_render_pie_chart,
            required_args={"labels", "values"},
            description="Pie chart showing parts-of-a-whole (Chart.js)",
            example_command='modern-graphics create --layout pie-chart --labels "Mobile,Web,API" --values "55,30,15" --output pie.png',
            keywords=["pie chart", "share", "composition", "parts of whole"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="donut-chart",
            render_fn=_render_donut_chart,
            required_args={"labels", "values"},
            description="Donut chart (pie with a hollow center) for share/composition (Chart.js)",
            example_command='modern-graphics create --layout donut-chart --labels "Mobile,Web,API" --values "55,30,15" --output donut.png',
            keywords=["donut chart", "doughnut chart", "share", "composition"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="cohort-chart",
            render_fn=_render_cohort_chart,
            required_args={"cohorts"},
            description="Cohort retention heatmap (Mixpanel-style): rows = cohorts, columns = period offsets",
            example_command='modern-graphics create --layout cohort-chart --cohorts \'[{"date":"Sep 17","size":7262,"values":[95.6,33.5,31.3]}]\' --output cohort.png',
            keywords=["cohort", "retention", "heatmap", "mixpanel", "amplitude", "retained"],
        )
    )
    registry.register(
        LayoutStrategy(
            layout_type="sankey-chart",
            render_fn=_render_sankey_chart,
            required_args={"links"},
            description="Sankey flow diagram (Chart.js + chartjs-chart-sankey plugin)",
            example_command='modern-graphics create --layout sankey-chart --links \'[{"from":"Visit","to":"Trial","value":40}]\' --output sankey.png',
            keywords=["sankey", "flow diagram", "flows", "allocation", "attribution"],
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
