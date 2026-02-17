"""Phase 1 export policy defaults.

Defines deterministic padding and crop modes for reusable graphics outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CropMode = Literal["none", "safe", "tight"]
PaddingMode = Literal["none", "minimal", "comfortable"]


@dataclass(frozen=True)
class ExportPolicy:
    crop_mode: CropMode = "safe"
    padding_mode: PaddingMode = "minimal"

    def resolve_padding(self) -> int:
        if self.padding_mode == "none":
            return 0
        if self.padding_mode == "comfortable":
            return 20
        return 8


DEFAULT_EXPORT_POLICY = ExportPolicy()
