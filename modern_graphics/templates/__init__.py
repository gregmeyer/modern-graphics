"""Template system for Modern Graphics"""

from typing import Dict
from .base import StyleTemplate
from .default import DEFAULT_TEMPLATE
from .builder import TemplateBuilder

# Registry of available templates
TEMPLATE_REGISTRY: Dict[str, StyleTemplate] = {
    "default": DEFAULT_TEMPLATE,
}


def register_template(template: StyleTemplate):
    """Register a custom template"""
    TEMPLATE_REGISTRY[template.name] = template


def get_template(name: str = "default") -> StyleTemplate:
    """Get template by name, defaults to 'default'"""
    return TEMPLATE_REGISTRY.get(name, DEFAULT_TEMPLATE)


__all__ = [
    'StyleTemplate',
    'DEFAULT_TEMPLATE',
    'TEMPLATE_REGISTRY',
    'register_template',
    'get_template',
    'TemplateBuilder',
]
