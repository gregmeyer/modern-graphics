"""Typed payload models for strategy-based layout rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class HeroPayload:
    headline: str
    subheadline: Optional[str] = None
    eyebrow: Optional[str] = None
    highlights: Optional[List[str]] = None
    background_variant: str = "light"
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.headline or not self.headline.strip():
            raise ValueError("headline is required")
        if self.background_variant not in {"light", "dark"}:
            raise ValueError("background_variant must be 'light' or 'dark'")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "headline": self.headline,
            "subheadline": self.subheadline,
            "eyebrow": self.eyebrow,
            "highlights": self.highlights,
            "background_variant": self.background_variant,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class ComparisonPayload:
    left_column: Dict[str, Any]
    right_column: Dict[str, Any]
    vs_text: str = "vs"
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        for side, column in (("left_column", self.left_column), ("right_column", self.right_column)):
            if not isinstance(column, dict):
                raise ValueError(f"{side} must be an object")
            if not column.get("title"):
                raise ValueError(f"{side}.title is required")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "left_column": self.left_column,
            "right_column": self.right_column,
            "vs_text": self.vs_text,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class TimelinePayload:
    events: List[Dict[str, Any]]
    orientation: str = "horizontal"
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.events:
            raise ValueError("events must contain at least one event")
        if self.orientation not in {"horizontal", "vertical"}:
            raise ValueError("orientation must be 'horizontal' or 'vertical'")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "events": self.events,
            "orientation": self.orientation,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class FunnelPayload:
    stages: List[Dict[str, Any]]
    show_percentages: bool = False
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.stages:
            raise ValueError("stages must contain at least one stage")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "stages": self.stages,
            "show_percentages": self.show_percentages,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class GridPayload:
    items: List[Dict[str, Any]]
    columns: int = 5
    convergence: Optional[Dict[str, str]] = None
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("items must contain at least one item")
        if self.columns < 1:
            raise ValueError("columns must be >= 1")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "items": self.items,
            "columns": self.columns,
            "convergence": self.convergence,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class KeyInsightPayload:
    text: str
    label: str = "Key Insight"
    variant: str = "bold"
    icon: str = "lightning"
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("text is required")
        if self.variant not in {"default", "minimal", "bold", "quote"}:
            raise ValueError("variant must be one of: default, minimal, bold, quote")
        if self.icon not in {"lightning", "lightbulb", "quote", "star", "none"}:
            raise ValueError("icon must be one of: lightning, lightbulb, quote, star, none")
        if len(self.label) > 60:
            raise ValueError("label must be 60 characters or fewer")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "label": self.label,
            "variant": self.variant,
            "icon": self.icon,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class InsightCardPayload:
    text: str
    svg_content: str
    label: str = "Key Insight"
    svg_label: Optional[str] = None
    layout: str = "side-by-side"
    svg_position: str = "right"
    variant: str = "bold"
    icon: str = "lightning"
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError("text is required")
        if "<svg" not in self.svg_content:
            raise ValueError("svg_content must contain an <svg> element")
        if self.layout not in {"side-by-side", "stacked"}:
            raise ValueError("layout must be 'side-by-side' or 'stacked'")
        if self.svg_position not in {"left", "right"}:
            raise ValueError("svg_position must be 'left' or 'right'")
        if self.variant not in {"default", "bold"}:
            raise ValueError("variant must be 'default' or 'bold'")
        if self.icon not in {"lightning", "lightbulb", "quote", "star", "none"}:
            raise ValueError("icon must be one of: lightning, lightbulb, quote, star, none")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "svg_content": self.svg_content,
            "label": self.label,
            "svg_label": self.svg_label,
            "layout": self.layout,
            "svg_position": self.svg_position,
            "variant": self.variant,
            "icon": self.icon,
            "color_scheme": self.color_scheme,
        }


@dataclass(frozen=True)
class InsightStoryPayload:
    headline: str
    insight_text: str
    before_svg: Optional[str] = None
    after_svg: Optional[str] = None
    subtitle: Optional[str] = None
    eyebrow: Optional[str] = None
    before_label: str = "Before"
    after_label: str = "After"
    insight_label: str = "Key Insight"
    stats: Optional[List[Dict[str, str]]] = None
    color_scheme: Optional[Any] = None

    def __post_init__(self) -> None:
        if not self.headline or not self.headline.strip():
            raise ValueError("headline is required")
        if not self.insight_text or not self.insight_text.strip():
            raise ValueError("insight_text is required")
        if self.before_svg and "<svg" not in self.before_svg:
            raise ValueError("before_svg must contain an <svg> element")
        if self.after_svg and "<svg" not in self.after_svg:
            raise ValueError("after_svg must contain an <svg> element")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {
            "headline": self.headline,
            "insight_text": self.insight_text,
            "before_svg": self.before_svg,
            "after_svg": self.after_svg,
            "subtitle": self.subtitle,
            "eyebrow": self.eyebrow,
            "before_label": self.before_label,
            "after_label": self.after_label,
            "insight_label": self.insight_label,
            "stats": self.stats,
            "color_scheme": self.color_scheme,
        }
