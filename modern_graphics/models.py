"""Data models for Modern Graphics Generator"""

from dataclasses import dataclass
from datetime import date
from typing import Optional, Literal


@dataclass
class Attribution:
    """Attribution label configuration.
    
    If copyright is set, it is used as-is. Otherwise the line is built from
    person + current year + website (e.g. "© Jane 2026 • example.com").
    """
    person: str = "Greg Meyer"
    website: str = "gregmeyer.com"
    copyright: Optional[str] = None  # If set, used as-is; else built from person + year + website
    context: Optional[str] = None
    position: Literal["bottom-right", "bottom-center", "below-element"] = "bottom-right"
    margin_top: int = 20
    
    # Styling options (pill label)
    font_size: str = "11px"
    font_color: str = "#8E8E93"
    font_weight: str = "500"
    background_color: Optional[str] = None  # None = use default pill background
    opacity: float = 1.0
    padding: str = "6px 12px"
    border_radius: str = "20px"
    show: bool = True  # Set to False to hide attribution completely


@dataclass
class StepStyle:
    """Style configuration for a step/box"""
    background_color: Optional[str] = None
    background_gradient: Optional[tuple] = None
    shadow_color: Optional[str] = None
    text_color: str = "#1D1D1F"
