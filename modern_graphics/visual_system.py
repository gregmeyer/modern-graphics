"""Phase 1 visual system token contract.

This module defines semantic design tokens used by clarity-first layouts.
Templates should consume semantic roles instead of hard-coded style values.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List


@dataclass(frozen=True)
class TypographyScale:
    display: int = 56
    h1: int = 42
    h2: int = 32
    h3: int = 24
    body_l: int = 20
    body: int = 17
    caption: int = 13
    micro: int = 11


@dataclass(frozen=True)
class SpacingScale:
    xxs: int = 4
    xs: int = 8
    sm: int = 12
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48


@dataclass(frozen=True)
class VisualSystemTokens:
    typography: TypographyScale = TypographyScale()
    spacing: SpacingScale = SpacingScale()
    radius: Dict[str, int] = None
    border: Dict[str, int] = None
    elevation: Dict[str, str] = None

    def __post_init__(self):
        # dataclass frozen workaround
        if self.radius is None:
            object.__setattr__(self, "radius", {"sm": 8, "md": 12, "lg": 18, "xl": 24})
        if self.border is None:
            object.__setattr__(self, "border", {"thin": 1, "medium": 2, "thick": 3})
        if self.elevation is None:
            object.__setattr__(
                self,
                "elevation",
                {
                    "none": "none",
                    "subtle": "0 1px 3px rgba(15, 23, 42, 0.08)",
                    "soft": "0 6px 18px rgba(15, 23, 42, 0.08)",
                    "strong": "0 12px 32px rgba(15, 23, 42, 0.16)",
                },
            )


CLARITY_TOKENS = VisualSystemTokens()


def token_lint(style_values: List[str]) -> List[str]:
    """Return lint errors for ad-hoc style values.

    This initial scaffold expects style values to be token references,
    e.g. `token.spacing.md` instead of arbitrary literals like `17px`.
    """
    errors: List[str] = []
    for value in style_values:
        if "token." not in value:
            errors.append(f"Non-token style value: {value}")
    return errors


HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_VALUE_RE = re.compile(r"\b\d+(?:\.\d+)?px\b")


def scan_files_for_ad_hoc_literals(paths: List[Path]) -> Dict[str, List[str]]:
    """Scan files and report ad-hoc style literals.

    This is intentionally broad in Phase 1 to establish baseline debt.
    Later phases can narrow this with exemptions and token-aware parsing.
    """
    findings: Dict[str, List[str]] = {}
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        issues: List[str] = []
        for match in HEX_COLOR_RE.finditer(text):
            issues.append(f"hex:{match.group(0)}")
        for match in PX_VALUE_RE.finditer(text):
            issues.append(f"px:{match.group(0)}")
        if issues:
            findings[str(path)] = issues
    return findings
