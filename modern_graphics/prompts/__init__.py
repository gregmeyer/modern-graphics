"""Prompt library for AI-assisted template and diagram creation"""

from .template_prompts import (
    TEMPLATE_INTERVIEW_SYSTEM_PROMPT,
    TEMPLATE_INTERVIEW_USER_PROMPT,
    TEMPLATE_GENERATION_PROMPT,
    parse_template_response,
)
from .graphic_prompt_template import (
    GRAPHIC_PROMPT_QUESTIONS,
    PROMPT_CHECKLIST_ITEMS,
    EXAMPLE_ANSWERS_PBJ,
    EXAMPLE_PROMPT_PBJ,
    build_graphic_prompt,
)

__all__ = [
    'TEMPLATE_INTERVIEW_SYSTEM_PROMPT',
    'TEMPLATE_INTERVIEW_USER_PROMPT',
    'TEMPLATE_GENERATION_PROMPT',
    'parse_template_response',
    'GRAPHIC_PROMPT_QUESTIONS',
    'PROMPT_CHECKLIST_ITEMS',
    'EXAMPLE_ANSWERS_PBJ',
    'EXAMPLE_PROMPT_PBJ',
    'build_graphic_prompt',
]
