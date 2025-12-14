"""Prompt library for AI-assisted template and diagram creation"""

from .template_prompts import (
    TEMPLATE_INTERVIEW_SYSTEM_PROMPT,
    TEMPLATE_INTERVIEW_USER_PROMPT,
    TEMPLATE_GENERATION_PROMPT,
    parse_template_response,
)

__all__ = [
    'TEMPLATE_INTERVIEW_SYSTEM_PROMPT',
    'TEMPLATE_INTERVIEW_USER_PROMPT',
    'TEMPLATE_GENERATION_PROMPT',
    'parse_template_response',
]
