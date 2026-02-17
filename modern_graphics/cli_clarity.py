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
    "key-insight",
    "insight-card",
    "insight-story",
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


@dataclass(frozen=True)
class CreateDefaults:
    density: DensityMode = "clarity"
    theme: str = "corporate"
    crop_mode: Literal["none", "safe", "tight"] = "safe"
    padding_mode: Literal["none", "minimal", "comfortable"] = "minimal"


CREATE_DEFAULTS = CreateDefaults()


def normalize_density(value: str) -> DensityMode:
    value = (value or CREATE_DEFAULTS.density).strip().lower()
    if value not in {"clarity", "balanced", "dense"}:
        return CREATE_DEFAULTS.density
    return value  # type: ignore[return-value]
