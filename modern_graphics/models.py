"""Data models for Modern Graphics Generator"""

from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class Attribution:
    """Attribution bug configuration"""
    copyright: str = "© Greg Meyer 2025 • gregmeyer.com"
    context: Optional[str] = None
    position: Literal["bottom-right", "bottom-center", "below-element"] = "bottom-right"
    margin_top: int = 20
    
    # Styling options
    font_size: str = "12px"
    font_color: str = "#8E8E93"
    font_weight: str = "400"
    background_color: Optional[str] = None  # None = transparent
    opacity: float = 0.8
    padding: str = "8px 12px"
    border_radius: str = "6px"
    show: bool = True  # Set to False to hide attribution completely


@dataclass
class StepStyle:
    """Style configuration for a step/box"""
    background_color: Optional[str] = None
    background_gradient: Optional[tuple] = None
    shadow_color: Optional[str] = None
    text_color: str = "#1D1D1F"
