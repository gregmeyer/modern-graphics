"""Wireframe SVG element builders for composable wireframe diagrams.

This module provides reusable SVG fragment builders for creating
Material Design-inspired wireframe illustrations.
"""

from .config import WireframeConfig, WireframeColors, APPLE_COLORS, MATERIAL_COLORS
from .browser import render_browser_chrome, render_browser_window
from .cards import render_content_card, render_app_header, render_skeleton_lines
from .chat import render_chat_panel, render_chat_message, render_inline_card, render_action_buttons
from .forms import render_modal, render_form_field, render_submit_button
from .feedback import render_success_toast, render_status_pill, render_progress_bar

__all__ = [
    # Config
    'WireframeConfig',
    'WireframeColors', 
    'APPLE_COLORS',
    'MATERIAL_COLORS',
    # Browser elements
    'render_browser_chrome',
    'render_browser_window',
    # Card elements
    'render_content_card',
    'render_app_header',
    'render_skeleton_lines',
    # Chat elements
    'render_chat_panel',
    'render_chat_message',
    'render_inline_card',
    'render_action_buttons',
    # Form elements
    'render_modal',
    'render_form_field',
    'render_submit_button',
    # Feedback elements
    'render_success_toast',
    'render_status_pill',
    'render_progress_bar',
]
