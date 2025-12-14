"""Prompts for template creation interviews"""

import json
from typing import Dict, Optional

TEMPLATE_INTERVIEW_SYSTEM_PROMPT = """You are a helpful design assistant that helps users create visual style templates for graphics.

Your goal is to understand the user's design preferences through a friendly conversation and then generate a complete template specification.

Ask questions about:
1. Color preferences (what colors they like, mood/feeling they want)
2. Style (modern, classic, playful, professional, dark, light)
3. Use case (presentations, articles, social media, etc.)
4. Font preferences (if any)
5. Overall aesthetic goals

Keep questions conversational and focused. After gathering enough information, generate a JSON template specification."""

TEMPLATE_INTERVIEW_USER_PROMPT = """I'd like to create a new visual style template for my graphics. Can you help me design it?

Please ask me questions about my preferences, and then generate a template based on my answers."""

TEMPLATE_GENERATION_PROMPT = """Based on our conversation, create a complete template specification in JSON format.

The template should include:
- name: A short, descriptive name (e.g., "dark_professional", "playful_bright")
- colors: Object with color names as keys, each with:
  - gradient: Array of two hex color codes [start, end]
  - shadow: RGBA shadow color string
  Colors should include: blue, green, orange, purple, red, gray (at minimum)
- base_styles: Complete CSS string for base styles (body, containers, etc.)
- attribution_styles: CSS string for attribution/copyright styling
- font_family: CSS font-family value
- background_color: Default background hex color

Return ONLY valid JSON, no markdown formatting, no code blocks. The JSON should have this structure:
{
  "name": "template_name",
  "colors": {
    "blue": {"gradient": ["#hex1", "#hex2"], "shadow": "rgba(...)"},
    ...
  },
  "base_styles": "css string here",
  "attribution_styles": "css string here",
  "font_family": "font stack",
  "background_color": "#hex"
}"""


def parse_template_response(response_text: str) -> Optional[Dict]:
    """Parse OpenAI response into template dictionary
    
    Args:
        response_text: Raw response text from OpenAI
        
    Returns:
        Dictionary with template specification, or None if parsing fails
    """
    # Try to extract JSON from response (might be wrapped in markdown)
    text = response_text.strip()
    
    # Remove markdown code blocks if present
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        start_idx = text.find("{")
        end_idx = text.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            try:
                return json.loads(text[start_idx:end_idx])
            except json.JSONDecodeError:
                pass
        return None
