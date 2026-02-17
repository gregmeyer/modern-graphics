"""Phase 1 CLI clarity scaffolding.

This module defines the future clarity-first command surface and can be wired
into the main CLI behind a feature flag.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LayoutType = Literal[
    "hero",
    "insight",
    "story",
    "comparison",
    "timeline",
    "funnel",
    "grid",
    "pyramid",
]
DensityMode = Literal["clarity", "balanced", "dense"]


@dataclass(frozen=True)
class CreateCommand:
    layout: LayoutType
    density: DensityMode = "clarity"
    theme: str = "corporate"
    output: str = "output.png"


def normalize_density(value: str) -> DensityMode:
    value = (value or "clarity").strip().lower()
    if value not in {"clarity", "balanced", "dense"}:
        return "clarity"
    return value  # type: ignore[return-value]
