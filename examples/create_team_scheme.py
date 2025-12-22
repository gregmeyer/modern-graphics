"""Helper script for teams to create and save color schemes

Usage:
    python examples/create_team_scheme.py
    
This interactive script helps teams define their brand colors and fonts,
then saves the scheme for reuse across all graphics.
"""

from pathlib import Path
import json
from modern_graphics.color_scheme import ColorScheme, create_custom_scheme, register_scheme

def create_scheme_interactive():
    """Interactive color scheme creation"""
    print("=" * 70)
    print("Create Your Team's Color Scheme")
    print("=" * 70)
    print()
    
    # Get basic info
    name = input("Scheme name (e.g., 'Acme Corp', 'StartupX'): ").strip()
    if not name:
        print("Name is required!")
        return None
    
    description = input("Description (optional): ").strip()
    
    # Get primary brand color
    print("\n--- Brand Colors ---")
    primary = input("Primary brand color (hex, e.g., #2563eb): ").strip()
    if not primary.startswith('#'):
        primary = '#' + primary
    
    secondary = input("Secondary color (hex, or press Enter for auto): ").strip()
    if secondary and not secondary.startswith('#'):
        secondary = '#' + secondary
    if not secondary:
        secondary = None
    
    accent = input("Accent color (hex, or press Enter for auto): ").strip()
    if accent and not accent.startswith('#'):
        accent = '#' + accent
    if not accent:
        accent = None
    
    # Get font choice
    print("\n--- Typography ---")
    print("Google Fonts examples: Inter, Roboto, Lora, Merriweather, Poppins, Open Sans")
    google_font = input("Google Font name (or press Enter for default Inter): ").strip()
    if not google_font:
        google_font = None
    
    if google_font:
        font_style = input("Font style (sans-serif/serif/monospace) [sans-serif]: ").strip() or "sans-serif"
    else:
        font_style = "sans-serif"
    
    # Create scheme
    if google_font:
        scheme = create_custom_scheme(
            name=name,
            primary=primary,
            secondary=secondary,
            accent=accent,
            google_font_name=google_font,
            font_style=font_style,
            description=description
        )
    else:
        scheme = create_custom_scheme(
            name=name,
            primary=primary,
            secondary=secondary,
            accent=accent,
            description=description
        )
    
    # Register it
    register_scheme(scheme)
    
    # Save to file
    schemes_dir = Path("examples/schemes")
    schemes_dir.mkdir(exist_ok=True)
    
    scheme_file = schemes_dir / f"{name.lower().replace(' ', '_')}.json"
    
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
    
    with open(scheme_file, 'w') as f:
        json.dump(scheme_data, f, indent=2)
    
    print(f"\n✓ Color scheme created and saved!")
    print(f"  Name: {scheme.name}")
    print(f"  Primary color: {scheme.primary}")
    print(f"  Font: {scheme.font_family}")
    print(f"  Saved to: {scheme_file}")
    print(f"\nTo use this scheme:")
    print(f"  from modern_graphics.color_scheme import get_scheme")
    print(f"  scheme = get_scheme('{name.lower()}')")
    print(f"  html = scheme.apply_to_html(generated_html)")
    
    return scheme


if __name__ == "__main__":
    create_scheme_interactive()
