"""Test lower third style for slide cards

Demonstrates the new lower_third style option for slide cards.
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator, Attribution

generator = ModernGraphicsGenerator(
    title="Lower Third Style Demo",
    attribution=Attribution(copyright="© Demo 2025"),
    use_svg_js=True
)

output_dir = Path("examples/output/lower-third-demo")
output_dir.mkdir(parents=True, exist_ok=True)

cards = [
    {
        "title": "Product Features",
        "tagline": "Core Capabilities",
        "subtext": "Everything you need to succeed",
        "color": "blue",
        "badge": "New",
        "features": [
            "Real-time sync",
            "Advanced analytics",
            "API access"
        ],
        "custom_mockup": """
            const width = 240;
            const height = 140;
            const padding = 15;
            const nodeRadius = 20;
            const centerX = width / 2;
            const centerY = height / 2;
            
            const node1 = draw.circle(nodeRadius * 2).move(centerX - 50, centerY - nodeRadius)
                .fill('#0B64D0').opacity(0.8);
            const node2 = draw.circle(nodeRadius * 2).move(centerX, centerY - nodeRadius)
                .fill('#1B7A4E').opacity(0.8);
            const node3 = draw.circle(nodeRadius * 2).move(centerX + 50, centerY - nodeRadius)
                .fill('#0B64D0').opacity(0.8);
            
            draw.line(centerX - 30, centerY, centerX + 30, centerY)
                .stroke({width: 2, color: '#0B64D0'});
        """
    },
    {
        "title": "Enterprise Ready",
        "tagline": "Built for Scale",
        "subtext": "Trusted by leading companies",
        "color": "purple",
        "badge": "Enterprise",
        "features": [
            "SOC 2 compliant",
            "99.9% uptime",
            "24/7 support"
        ],
        "custom_mockup": """
            const width = 240;
            const height = 140;
            const padding = 15;
            const barWidth = 20;
            const barSpacing = 25;
            const startX = padding + 20;
            const chartBottom = height - padding - 20;
            const chartTop = padding + 10;
            
            const bars = [40, 55, 45, 60, 50];
            bars.forEach((height, i) => {
                const x = startX + i * barSpacing;
                const barHeight = height;
                const y = chartBottom - barHeight;
                draw.rect(barWidth, barHeight).move(x, y)
                    .fill('#8243B5').opacity(0.7);
            });
        """
    }
]

# 1. Default style (vertical layout)
print("1. Generating default style (vertical layout)...")
html1 = generator.generate_slide_card_diagram(cards, style="default")
generator.export_to_png(html1, output_dir / "01-default-style.png", viewport_width=800, viewport_height=600, padding=20)
print(f"   ✓ Saved: {output_dir / '01-default-style.png'}")

# 2. Lower third style (horizontal bar layout)
print("\n2. Generating lower third style (horizontal bar layout)...")
html2 = generator.generate_slide_card_diagram(cards, style="lower_third")
generator.export_to_png(html2, output_dir / "02-lower-third-style.png", viewport_width=800, viewport_height=600, padding=20)
print(f"   ✓ Saved: {output_dir / '02-lower-third-style.png'}")

# 3. Single card - default style
print("\n3. Generating single card (default style)...")
html3 = generator.generate_slide_card_diagram([cards[0]], style="default")
generator.export_to_png(html3, output_dir / "03-single-default.png", viewport_width=500, viewport_height=600, padding=20)
print(f"   ✓ Saved: {output_dir / '03-single-default.png'}")

# 4. Single card - lower third style
print("\n4. Generating single card (lower third style)...")
html4 = generator.generate_slide_card_diagram([cards[0]], style="lower_third")
generator.export_to_png(html4, output_dir / "04-single-lower-third.png", viewport_width=500, viewport_height=300, padding=20)
print(f"   ✓ Saved: {output_dir / '04-single-lower-third.png'}")

print("\n" + "=" * 70)
print("✓ Lower third style demo generated!")
print("=" * 70)
print(f"\nFiles saved to: {output_dir}")
print("\nGenerated examples:")
print("  1. Default style (vertical layout)")
print("  2. Lower third style (horizontal bar layout)")
print("  3. Single card (default style)")
print("  4. Single card (lower third style)")
print("\nLower third style features:")
print("  ✓ Horizontal layout: graphic on left, text on right")
print("  ✓ Compact design: perfect for lower third of slides")
print("  ✓ Smaller graphic size: optimized for horizontal bars")
print("  ✓ Compact typography: smaller fonts for bar format")
