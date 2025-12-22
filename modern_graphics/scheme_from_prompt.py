"""Generate color schemes from natural language prompts

Uses AI to interpret brand descriptions and suggest appropriate colors and fonts,
then saves the scheme as JSON for team reuse.
"""

from pathlib import Path
import json
from typing import Optional, Dict, Any
from .color_scheme import ColorScheme, create_custom_scheme, register_scheme
from .env_config import get_openai_key


def generate_scheme_from_prompt(
    prompt: str,
    output_path: Optional[Path] = None,
    model: str = "gpt-4o-mini"
) -> ColorScheme:
    """Generate a color scheme from a natural language prompt
    
    Args:
        prompt: Description of desired theme (e.g., "professional corporate theme 
                with blue accents and serif font" or "modern tech startup with 
                bright colors and sans-serif")
        output_path: Optional path to save JSON file (auto-generated if None)
        model: OpenAI model to use
    
    Returns:
        ColorScheme instance
    
    Example:
        >>> scheme = generate_scheme_from_prompt(
        ...     "professional corporate theme with navy blue and serif font"
        ... )
        >>> html = scheme.apply_to_html(generated_html)
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "generate_scheme_from_prompt requires openai. "
            "Install with: pip install openai"
        )
    
    api_key = get_openai_key()
    if not api_key:
        raise ValueError(
            "OpenAI API key required. Set OPENAI_API_KEY environment variable."
        )
    
    client = OpenAI(api_key=api_key)
    
    system_prompt = """You are a color scheme and typography expert. Generate a color scheme and font choice based on the user's description.

Return a JSON object with:
- name: Short name for the scheme
- description: Brief description
- google_font_name: Google Font name (e.g., "Inter", "Lora", "Roboto", "Merriweather", "Poppins", "Open Sans")
- font_style: "sans-serif", "serif", or "monospace"
- primary: Primary brand color (hex, e.g., "#2563eb")
- secondary: Secondary/accent color (hex)
- accent: Highlight color (hex)
- text_primary: Main text color (hex)
- text_secondary: Secondary text color (hex)
- text_tertiary: Tertiary text color (hex)
- text_on_dark: Text color for dark backgrounds (hex)
- bg_primary: Primary background (hex, usually white or light)
- bg_secondary: Secondary background (hex, slightly darker)
- bg_tertiary: Tertiary background (hex)
- bg_dark: Dark background color (hex)
- border_light: Light border color (hex)
- border_medium: Medium border color (hex)
- border_dark: Dark border color (hex)

Choose colors that work well together and match the description. For corporate/professional themes, use muted blues and grays. For tech startups, use bright, modern colors. For creative agencies, use vibrant colors.

Choose fonts appropriately:
- Corporate/professional: serif fonts like "Lora", "Merriweather", "Georgia"
- Modern/tech: sans-serif like "Inter", "Roboto", "Poppins", "Open Sans"
- Creative: display fonts or unique sans-serif

Return ONLY valid JSON, no markdown formatting."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    
    # Create the color scheme
    scheme = ColorScheme(
        name=result.get("name", "Custom Scheme"),
        description=result.get("description", prompt),
        google_font_name=result.get("google_font_name"),
        google_font_weights=result.get("google_font_weights", "400;600;700"),
        font_style=result.get("font_style", "sans-serif"),
        primary=result.get("primary", "#2563eb"),
        secondary=result.get("secondary", "#64748b"),
        accent=result.get("accent", "#1e40af"),
        text_primary=result.get("text_primary", "#1e293b"),
        text_secondary=result.get("text_secondary", "#475569"),
        text_tertiary=result.get("text_tertiary", "#64748b"),
        text_on_dark=result.get("text_on_dark", "#f1f5f9"),
        bg_primary=result.get("bg_primary", "#ffffff"),
        bg_secondary=result.get("bg_secondary", "#f8fafc"),
        bg_tertiary=result.get("bg_tertiary", "#f1f5f9"),
        bg_dark=result.get("bg_dark", "#1e293b"),
        border_light=result.get("border_light", "#e2e8f0"),
        border_medium=result.get("border_medium", "#cbd5e1"),
        border_dark=result.get("border_dark", "#94a3b8"),
        svg_primary=result.get("svg_primary"),
        svg_secondary=result.get("svg_secondary"),
        svg_accent=result.get("svg_accent"),
    )
    
    # Register it
    register_scheme(scheme)
    
    # Save to JSON
    if output_path is None:
        schemes_dir = Path("examples/schemes")
        schemes_dir.mkdir(exist_ok=True)
        filename = scheme.name.lower().replace(' ', '_').replace('/', '_') + ".json"
        output_path = schemes_dir / filename
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    scheme_data = {
        "name": scheme.name,
        "description": scheme.description,
        "google_font_name": scheme.google_font_name,
        "google_font_weights": scheme.google_font_weights,
        "font_style": scheme.font_style,
        "font_family": scheme.font_family,
        "primary": scheme.primary,
        "secondary": scheme.secondary,
        "accent": scheme.accent,
        "text_primary": scheme.text_primary,
        "text_secondary": scheme.text_secondary,
        "text_tertiary": scheme.text_tertiary,
        "text_on_dark": scheme.text_on_dark,
        "bg_primary": scheme.bg_primary,
        "bg_secondary": scheme.bg_secondary,
        "bg_tertiary": scheme.bg_tertiary,
        "bg_dark": scheme.bg_dark,
        "border_light": scheme.border_light,
        "border_medium": scheme.border_medium,
        "border_dark": scheme.border_dark,
        "svg_primary": scheme.svg_primary,
        "svg_secondary": scheme.svg_secondary,
        "svg_accent": scheme.svg_accent,
    }
    
    with open(output_path, 'w') as f:
        json.dump(scheme_data, f, indent=2)
    
    print(f"\n✓ Color scheme generated and saved!")
    print(f"  Name: {scheme.name}")
    print(f"  Description: {scheme.description}")
    print(f"  Primary color: {scheme.primary}")
    print(f"  Font: {scheme.font_family}")
    print(f"  Saved to: {output_path}")
    
    return scheme


def load_scheme_from_json(json_path: Path) -> ColorScheme:
    """Load a color scheme from a JSON file"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    return ColorScheme(
        name=data["name"],
        description=data.get("description", ""),
        google_font_name=data.get("google_font_name"),
        google_font_weights=data.get("google_font_weights", "400;600;700"),
        font_style=data.get("font_style", "sans-serif"),
        primary=data.get("primary", "#2563eb"),
        secondary=data.get("secondary", "#64748b"),
        accent=data.get("accent", "#1e40af"),
        text_primary=data.get("text_primary", "#1e293b"),
        text_secondary=data.get("text_secondary", "#475569"),
        text_tertiary=data.get("text_tertiary", "#64748b"),
        text_on_dark=data.get("text_on_dark", "#f1f5f9"),
        bg_primary=data.get("bg_primary", "#ffffff"),
        bg_secondary=data.get("bg_secondary", "#f8fafc"),
        bg_tertiary=data.get("bg_tertiary", "#f1f5f9"),
        bg_dark=data.get("bg_dark", "#1e293b"),
        border_light=data.get("border_light", "#e2e8f0"),
        border_medium=data.get("border_medium", "#cbd5e1"),
        border_dark=data.get("border_dark", "#94a3b8"),
        svg_primary=data.get("svg_primary"),
        svg_secondary=data.get("svg_secondary"),
        svg_accent=data.get("svg_accent"),
    )
