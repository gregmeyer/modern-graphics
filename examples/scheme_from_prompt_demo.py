"""Example: Generate color scheme from prompt

Demonstrates how teams can describe their brand in natural language
and get a complete color scheme with fonts automatically generated.
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator
from modern_graphics.scheme_from_prompt import generate_scheme_from_prompt, load_scheme_from_json

# Example 1: Corporate theme
print("Example 1: Generating corporate theme from prompt...")
print("Prompt: 'professional corporate theme with navy blue accents and serif font'")

corporate_scheme = generate_scheme_from_prompt(
    "professional corporate theme with navy blue accents and serif font",
    output_path=Path("examples/schemes/corporate_from_prompt.json")
)

# Generate hero slide with the scheme
generator1 = ModernGraphicsGenerator(
    title="Corporate Theme Demo",
    use_svg_js=True
)

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

html1 = corporate_scheme.apply_to_html(html1)
output1 = Path("examples/output/prompt-corporate-hero.png")
generator1.export_to_png(html1, output1, viewport_width=2400, viewport_height=1600, padding=40)
print(f"✓ Saved: {output1}")

# Example 2: Tech startup theme
print("\nExample 2: Generating tech startup theme from prompt...")
print("Prompt: 'modern tech startup with bright cyan and coral colors, bold sans-serif font'")

tech_scheme = generate_scheme_from_prompt(
    "modern tech startup with bright cyan and coral colors, bold sans-serif font",
    output_path=Path("examples/schemes/tech_startup_from_prompt.json")
)

generator2 = ModernGraphicsGenerator(
    title="Tech Startup Theme",
    use_svg_js=True
)

html2 = generator2.generate_modern_hero(
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

html2 = tech_scheme.apply_to_html(html2)
output2 = Path("examples/output/prompt-tech-startup-hero.png")
generator2.export_to_png(html2, output2, viewport_width=2400, viewport_height=1600, padding=40)
print(f"✓ Saved: {output2}")

# Example 3: Load and reuse saved scheme
print("\nExample 3: Loading saved scheme from JSON...")
loaded_scheme = load_scheme_from_json(Path("examples/schemes/corporate_from_prompt.json"))
print(f"  Loaded: {loaded_scheme.name}")
print(f"  Primary: {loaded_scheme.primary}")
print(f"  Font: {loaded_scheme.font_family}")

# Use it for slide cards
generator3 = ModernGraphicsGenerator(
    title="Corporate Cards",
    use_svg_js=True
)

cards = [
    {
        "title": "Enterprise Solution",
        "tagline": "Q1 2025",
        "subtext": "Built for scale and reliability",
        "color": "blue",
        "badge": "New",
        "features": [
            "99.9% uptime",
            "Enterprise security",
            "24/7 support"
        ]
    }
]

html3 = generator3.generate_slide_card_diagram(cards)
html3 = loaded_scheme.apply_to_html(html3)
output3 = Path("examples/output/prompt-corporate-cards.png")
generator3.export_to_png(
    html3,
    output3,
    viewport_width=500,
    viewport_height=600,
    padding=20
)
print(f"✓ Saved: {output3}")

print("\n✓ All examples generated successfully!")
print("\nBenefits:")
print("  1. Describe your brand in plain English")
print("  2. Get complete color scheme + font suggestions")
print("  3. Scheme saved as JSON for team reuse")
print("  4. Consistent theming across all graphics")
print("\nFiles created:")
print(f"  - {output1}")
print(f"  - {output2}")
print(f"  - {output3}")
print(f"  - examples/schemes/corporate_from_prompt.json")
print(f"  - examples/schemes/tech_startup_from_prompt.json")
