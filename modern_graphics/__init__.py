"""
Modern Graphics Generator - Generate elegant HTML/CSS graphics

This module provides utilities to generate modern HTML/CSS graphics
with clean design, consistent styling, and professional output.
"""

from .models import Attribution, StepStyle
from .constants import MODERN_COLORS, APPLE_COLORS, BASE_STYLES, ATTRIBUTION_STYLES
from .generator import ModernGraphicsGenerator
from .templates import StyleTemplate, DEFAULT_TEMPLATE, register_template, get_template, TEMPLATE_REGISTRY
from .templates.builder import TemplateBuilder
from .diagrams import DiagramGenerator, DIAGRAM_REGISTRY, register_diagram, get_diagram_generator
from .env_config import get_openai_key, get_braintrust_key, load_env_file
from .template_interview import interview_for_template, quick_template_from_description
from .eval import log_template_creation_eval, log_interview_eval
from .config import Config, get_config, braintrust_enabled, set_braintrust_enabled
from .convenience import (
    generate_cycle_diagram,
    generate_comparison_diagram,
    generate_grid_diagram,
    generate_flywheel_diagram,
    generate_timeline_diagram,
    generate_pyramid_diagram,
    generate_before_after_diagram,
    generate_funnel_diagram,
    generate_slide_card_diagram,
    generate_slide_card_comparison,
    generate_story_slide,
)

__all__ = [
    # Models
    'Attribution',
    'StepStyle',
    # Constants (backward compatibility)
    'MODERN_COLORS',
    'APPLE_COLORS',
    'BASE_STYLES',
    'ATTRIBUTION_STYLES',
    # Generator
    'ModernGraphicsGenerator',
    # Templates
    'StyleTemplate',
    'DEFAULT_TEMPLATE',
    'TEMPLATE_REGISTRY',
    'register_template',
    'get_template',
    'TemplateBuilder',
    # Diagrams
    'DiagramGenerator',
    'DIAGRAM_REGISTRY',
    'register_diagram',
    'get_diagram_generator',
    # Environment config
    'get_openai_key',
    'load_env_file',
    # AI-assisted template creation
    'interview_for_template',
    'quick_template_from_description',
    # Evaluation
    'get_braintrust_key',
    'log_template_creation_eval',
    'log_interview_eval',
    # Configuration
    'Config',
    'get_config',
    'braintrust_enabled',
    'set_braintrust_enabled',
    # Convenience functions
    'generate_cycle_diagram',
    'generate_comparison_diagram',
    'generate_grid_diagram',
    'generate_flywheel_diagram',
    'generate_timeline_diagram',
    'generate_pyramid_diagram',
    'generate_before_after_diagram',
    'generate_funnel_diagram',
    'generate_slide_card_diagram',
    'generate_slide_card_comparison',
    'generate_story_slide',
]

# Version
__version__ = "0.1.0"
