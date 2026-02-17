"""Reference extension strategies for Phase 2 architecture.

These examples are intentionally small and intended for copy/adapt workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .layouts import LayoutStrategy, register_layout_strategy


@dataclass(frozen=True)
class CalloutPayload:
    """Example payload model for custom callout strategy."""

    headline: str
    detail: str

    def __post_init__(self) -> None:
        if not self.headline.strip():
            raise ValueError("headline is required")
        if not self.detail.strip():
            raise ValueError("detail is required")

    def to_strategy_kwargs(self) -> Dict[str, Any]:
        return {"headline": self.headline, "detail": self.detail}


def _render_callout(generator, **kwargs: object) -> str:
    headline = str(kwargs["headline"])
    detail = str(kwargs["detail"])
    html = f"""
    <div style="padding:40px;font-family:Inter,system-ui,sans-serif;">
      <div style="font-size:32px;font-weight:700;line-height:1.1;">{headline}</div>
      <div style="margin-top:12px;font-size:18px;line-height:1.4;color:#475569;">{detail}</div>
    </div>
    """
    return generator._wrap_html(html, "")


def register_example_callout_strategy() -> None:
    """Register a tiny sample extension strategy."""
    register_layout_strategy(
        LayoutStrategy(
            layout_type="callout-example",
            render_fn=_render_callout,
            required_args={"headline", "detail"},
        )
    )

