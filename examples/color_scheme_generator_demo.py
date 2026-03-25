"""Example: Using the color scheme generator

Demonstrates how teams can easily create and apply consistent color themes
across all graphics types (hero slides, slide cards, etc.)
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator
from modern_graphics.color_scheme import (
    ColorScheme,
    CORPORATE_SCHEME,
    create_custom_scheme,
    register_scheme,
    get_scheme
)

# Example 1: Use predefined corporate scheme
print("Example 1: Using predefined corporate scheme...")
generator1 = ModernGraphicsGenerator(
    title="Corporate Theme Demo",
    use_svg_js=True
)

# Generate hero slide
html1 = generator1.generate_modern_hero(
    eyebrow="Business Strategy",
    headline="Transform Your Revenue Model",
    subheadline="Shift from upfront licenses to subscription-based revenue",
    highlights=[
        "Predictable revenue streams",
        "Higher customer retention",
        "Scalable business model"
    ],
    stats=[
        {"label": "ARR Growth", "value": "+24% QoQ"},
        {"label": "Retention Rate", "value": "92%"}
    ]
)

# Apply corporate color scheme
html1 = CORPORATE_SCHEME.apply_to_html(html1)

output1 = Path("examples/output/scheme-corporate-hero.png")
generator1.export_to_png(html1, output1, viewport_width=2400, viewport_height=1600, padding=40)
print(f"✓ Saved: {output1}")

# Example 2: Create custom scheme from brand color with font
print("\nExample 2: Creating custom scheme from brand color with font...")
brand_scheme = create_custom_scheme(
    name="Brand",
    primary="#8B5CF6",  # Purple brand color
    google_font_name="Roboto",
    font_style="sans-serif",
    description="Custom brand theme with Roboto font"
)

# Generate slide cards with custom scheme
generator2 = ModernGraphicsGenerator(
    title="Brand Theme Demo",
    use_svg_js=True
)

cards = [
    {
        "title": "Product Launch",
        "tagline": "Q1 2025",
        "subtext": "Introducing our new platform",
        "color": "purple",
        "badge": "New",
        "features": [
            "Enhanced features",
            "Better performance",
            "Improved UX"
        ]
    }
]

html2 = generator2.generate_slide_card_diagram(cards)
html2 = brand_scheme.apply_to_html(html2)

output2 = Path("examples/output/scheme-brand-cards.png")
generator2.export_to_png(
    html2,
    output2,
    viewport_width=500,
    viewport_height=600,
    padding=20
)
print(f"✓ Saved: {output2}")

# Example 3: Fully custom scheme with font
print("\nExample 3: Creating fully custom scheme with font...")
custom_scheme = ColorScheme(
    name="Tech Startup",
    description="Bold, modern tech startup theme",
    google_font_name="Poppins",
    google_font_weights="400;600;700;900",
    font_style="sans-serif",
    primary="#00d4ff",  # Bright cyan
    secondary="#ff6b6b",  # Coral red
    accent="#4ecdc4",  # Teal
    text_primary="#1a1a1a",
    text_secondary="#4a4a4a",
    text_tertiary="#8a8a8a",
    text_on_dark="#ffffff",
    bg_primary="#ffffff",
    bg_secondary="#f5f5f5",
    bg_tertiary="#e8e8e8",
    bg_dark="#1a1a1a",
    border_light="#e0e0e0",
    border_medium="#c0c0c0",
    border_dark="#808080",
    svg_primary="#00d4ff",  # Bright cyan for SVGs
    svg_secondary="#ff6b6b",  # Coral for SVGs
    svg_accent="#4ecdc4",  # Teal for SVGs
)

# Register it for reuse
register_scheme(custom_scheme)

# Use it for a hero slide
generator3 = ModernGraphicsGenerator(
    title="Tech Startup Theme",
    use_svg_js=True
)

html3 = generator3.generate_modern_hero(
    eyebrow="Innovation",
    headline="Build the Future",
    subheadline="Cutting-edge technology for modern teams",
    highlight_tiles=[
        {"label": "Fast", "icon": "generated"},
        {"label": "Scalable", "icon": "templates"},
        {"label": "Reliable", "icon": "manual"}
    ],
    stats=[
        {"label": "Speed", "value": "10x faster"},
        {"label": "Scale", "value": "Unlimited"},
        {"label": "Uptime", "value": "99.9%"}
    ]
)

html3 = custom_scheme.apply_to_html(html3)

output3 = Path("examples/output/scheme-tech-startup-hero.png")
generator3.export_to_png(html3, output3, viewport_width=2400, viewport_height=1600, padding=40)
print(f"✓ Saved: {output3}")

# Example 4: Show how to retrieve and use registered schemes
print("\nExample 4: Retrieving registered scheme...")
retrieved_scheme = get_scheme("tech startup")
if retrieved_scheme:
    print(f"  Found scheme: {retrieved_scheme.name}")
    print(f"  Primary color: {retrieved_scheme.primary}")
    print(f"  Description: {retrieved_scheme.description}")

print("\n✓ Color scheme examples generated successfully!")
print("\nBenefits of Color Scheme Generator:")
print("  1. Define colors once, use everywhere")
print("  2. Consistent theming across all graphics types")
print("  3. Easy to create from brand colors")
print("  4. SVG color replacement included")
print("  5. Shareable schemes for team consistency")
print("\nFiles created:")
print(f"  - {output1}")
print(f"  - {output2}")
print(f"  - {output3}")
