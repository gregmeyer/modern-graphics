"""Named export presets for channel-specific output workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal

CropMode = Literal["none", "safe", "tight"]
PaddingMode = Literal["none", "minimal", "comfortable"]


@dataclass(frozen=True)
class ExportPreset:
    name: str
    viewport_width: int
    viewport_height: int
    device_scale_factor: int
    crop_mode: CropMode
    padding_mode: PaddingMode
    description: str


EXPORT_PRESETS: Dict[str, ExportPreset] = {
    "linkedin": ExportPreset(
        name="linkedin",
        viewport_width=1200,
        viewport_height=627,
        device_scale_factor=1,
        crop_mode="none",
        padding_mode="none",
        description="LinkedIn feed image (1200x627)",
    ),
    "x": ExportPreset(
        name="x",
        viewport_width=1600,
        viewport_height=900,
        device_scale_factor=1,
        crop_mode="none",
        padding_mode="none",
        description="X/Twitter landscape image (1600x900)",
    ),
    "substack-hero": ExportPreset(
        name="substack-hero",
        viewport_width=1400,
        viewport_height=700,
        device_scale_factor=1,
        crop_mode="none",
        padding_mode="none",
        description="Substack hero image (1400x700)",
    ),
}


def list_export_presets() -> list[str]:
    return sorted(EXPORT_PRESETS.keys())


def get_export_preset(name: str | None) -> ExportPreset | None:
    if not name:
        return None
    return EXPORT_PRESETS.get(name)
