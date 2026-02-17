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
from .graphic_ideas_interview import run_graphic_ideas_interview
from .prompt_to_story import generate_story_from_prompt, create_story_slide_from_prompt
from .diagrams.intelligent_story_slide import generate_intelligent_story_slide
from .diagrams.editorial_story_slide import generate_editorial_story_slide
from .diagrams.unified_story_slide import generate_unified_story_slide
from .diagrams.creative_story_slide import generate_combo_chart
from .prompt_to_diagram import (
    DEFAULT_DIAGRAM_PROMPTS,
    generate_cycle_diagram_from_prompt,
    generate_comparison_diagram_from_prompt,
    generate_timeline_diagram_from_prompt,
    generate_grid_diagram_from_prompt,
    generate_flywheel_diagram_from_prompt,
    generate_slide_cards_from_prompt,
    generate_slide_card_comparison_from_prompt,
)
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
    generate_modern_hero,
    generate_modern_hero_triptych,
    generate_premium_card,
)
from .color_scheme import (
    ColorScheme,
    CORPORATE_SCHEME,
    DARK_SCHEME,
    WARM_SCHEME,
    GREEN_SCHEME,
    create_custom_scheme,
    get_scheme,
    register_scheme,
    list_schemes,
    SCHEME_REGISTRY,
)
from .scheme_from_prompt import (
    generate_scheme_from_prompt,
    load_scheme_from_json,
)
from .svg_decision_helper import should_use_svg_js, get_recommendation_reason
from .svg_utils import (
    generate_svg_container,
    generate_svg_init_script,
    create_svg_circle,
    create_svg_rect,
    create_svg_line,
    create_svg_path,
    create_svg_text,
    create_svg_group,
    generate_svg_js_cdn_script,
    generate_complete_svg_example,
)
from .illustration_review import review_illustration, generate_with_review
from .illustration_validator import IllustrationValidator
from .design_review_agent import DesignReviewAgent
from .svg_element_parser import SVGElementParser
from .visual_system import VisualSystemTokens, TypographyScale, SpacingScale, CLARITY_TOKENS, token_lint
from .critique_gates import GateResult, CritiqueReport, run_clarity_gates
from .export_policy import ExportPolicy, DEFAULT_EXPORT_POLICY
from .cli_clarity import CreateCommand, normalize_density

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
    'run_graphic_ideas_interview',
    # Prompt-to-story generation
    'generate_story_from_prompt',
    'create_story_slide_from_prompt',
    'generate_intelligent_story_slide',
    'generate_editorial_story_slide',
    'generate_unified_story_slide',
    'generate_combo_chart',
    # Prompt-to-diagram generation
    'DEFAULT_DIAGRAM_PROMPTS',
    'generate_cycle_diagram_from_prompt',
    'generate_comparison_diagram_from_prompt',
    'generate_timeline_diagram_from_prompt',
    'generate_grid_diagram_from_prompt',
    'generate_flywheel_diagram_from_prompt',
    'generate_slide_cards_from_prompt',
    'generate_slide_card_comparison_from_prompt',
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
    'generate_modern_hero',
    'generate_modern_hero_triptych',
    'generate_premium_card',
    # SVG.js utilities
    'should_use_svg_js',
    'get_recommendation_reason',
    'generate_svg_container',
    'generate_svg_init_script',
    'create_svg_circle',
    'create_svg_rect',
    'create_svg_line',
    'create_svg_path',
    'create_svg_text',
    'create_svg_group',
    'generate_svg_js_cdn_script',
    'generate_complete_svg_example',
    # Illustration review system
    'review_illustration',
    'generate_with_review',
    'IllustrationValidator',
    'DesignReviewAgent',
    'SVGElementParser',
    # Color schemes
    'ColorScheme',
    'CORPORATE_SCHEME',
    'DARK_SCHEME',
    'WARM_SCHEME',
    'GREEN_SCHEME',
    'create_custom_scheme',
    'get_scheme',
    'register_scheme',
    'list_schemes',
    'SCHEME_REGISTRY',
    # Scheme from prompt
    'generate_scheme_from_prompt',
    'load_scheme_from_json',
    # Overhaul phase 1 scaffolding
    'VisualSystemTokens',
    'TypographyScale',
    'SpacingScale',
    'CLARITY_TOKENS',
    'token_lint',
    'GateResult',
    'CritiqueReport',
    'run_clarity_gates',
    'ExportPolicy',
    'DEFAULT_EXPORT_POLICY',
    'CreateCommand',
    'normalize_density',
]

# Version
__version__ = "0.1.0"
