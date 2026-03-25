"""Test hero slide alignment options

Demonstrates headline/subheadline alignment and graphic positioning.
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator, Attribution

generator = ModernGraphicsGenerator(
    title="Hero Alignment Demo",
    attribution=Attribution(copyright="© Demo 2025"),
    use_svg_js=True
)

output_dir = Path("examples/output/hero-alignment")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Default (left aligned headline/subheadline, center graphic)
print("1. Generating default alignment (left/left/center)...")
html1 = generator.generate_modern_hero(
    eyebrow="Default",
    headline="Left-Aligned Headline",
    subheadline="Left-aligned subheadline with default settings",
    highlight_tiles=[
        {"label": "Fast", "icon": "generated"},
        {"label": "Scalable", "icon": "templates"},
        {"label": "Reliable", "icon": "manual"}
    ]
)
generator.export_to_png(html1, output_dir / "01-default-left-left-center.png", viewport_width=2400, viewport_height=1600, padding=40)
print(f"   ✓ Saved: {output_dir / '01-default-left-left-center.png'}")

# 2. Center aligned headline/subheadline, center graphic
print("\n2. Generating center alignment...")
html2 = generator.generate_modern_hero(
    eyebrow="Center",
    headline="Center-Aligned Headline",
    subheadline="Center-aligned subheadline with centered graphic",
    headline_align="center",
    subheadline_align="center",
    graphic_position="center",
    highlight_tiles=[
        {"label": "Fast", "icon": "generated"},
        {"label": "Scalable", "icon": "templates"},
        {"label": "Reliable", "icon": "manual"}
    ]
)
generator.export_to_png(html2, output_dir / "02-center-center-center.png", viewport_width=2400, viewport_height=1600, padding=40)
print(f"   ✓ Saved: {output_dir / '02-center-center-center.png'}")

# 3. Right aligned headline/subheadline, right graphic
print("\n3. Generating right alignment...")
html3 = generator.generate_modern_hero(
    eyebrow="Right",
    headline="Right-Aligned Headline",
    subheadline="Right-aligned subheadline with right-positioned graphic",
    headline_align="right",
    subheadline_align="right",
    graphic_position="right",
    highlight_tiles=[
        {"label": "Fast", "icon": "generated"},
        {"label": "Scalable", "icon": "templates"},
        {"label": "Reliable", "icon": "manual"}
    ]
)
generator.export_to_png(html3, output_dir / "03-right-right-right.png", viewport_width=2400, viewport_height=1600, padding=40)
print(f"   ✓ Saved: {output_dir / '03-right-right-right.png'}")

# 4. Mixed alignment: center headline, left subheadline, left graphic
print("\n4. Generating mixed alignment (center/left/left)...")
html4 = generator.generate_modern_hero(
    eyebrow="Mixed",
    headline="Center Headline, Left Subheadline",
    subheadline="Left-aligned subheadline with left-positioned graphic",
    headline_align="center",
    subheadline_align="left",
    graphic_position="left",
    highlight_tiles=[
        {"label": "Fast", "icon": "generated"},
        {"label": "Scalable", "icon": "templates"},
        {"label": "Reliable", "icon": "manual"}
    ]
)
generator.export_to_png(html4, output_dir / "04-mixed-center-left-left.png", viewport_width=2400, viewport_height=1600, padding=40)
print(f"   ✓ Saved: {output_dir / '04-mixed-center-left-left.png'}")

# 5. Triptych with center alignment
print("\n5. Generating triptych with center alignment...")
html5 = generator.generate_modern_hero_triptych(
    eyebrow="Triptych",
    headline="Center-Aligned Triptych Headline",
    subheadline="Center-aligned subheadline for triptych layout",
    headline_align="center",
    subheadline_align="center",
    columns=[
        {
            "title": "Innovation",
            "items": ["Cutting-edge tech", "Rapid iteration", "User feedback"],
            "icon": "generated"
        },
        {
            "title": "Scale",
            "items": ["Cloud infrastructure", "Auto-scaling", "Global reach"],
            "icon": "templates"
        },
        {
            "title": "Success",
            "items": ["Customer satisfaction", "Revenue growth", "Market leadership"],
            "icon": "manual"
        }
    ]
)
generator.export_to_png(html5, output_dir / "05-triptych-center.png", viewport_width=2400, viewport_height=1600, padding=40)
print(f"   ✓ Saved: {output_dir / '05-triptych-center.png'}")

# 6. Flowchart with right alignment
print("\n6. Generating flowchart with right alignment...")
html6 = generator.generate_modern_hero(
    eyebrow="Flowchart",
    headline="Right-Aligned Flowchart",
    subheadline="Right-aligned text with right-positioned flowchart graphic",
    headline_align="right",
    subheadline_align="right",
    graphic_position="right",
    flow_nodes=[
        {"id": "start", "label": "Start", "icon": "manual", "position": {"x": 0.2, "y": 0.5}},
        {"id": "process", "label": "Process", "icon": "templates", "position": {"x": 0.5, "y": 0.5}},
        {"id": "end", "label": "End", "icon": "generated", "position": {"x": 0.8, "y": 0.5}}
    ],
    flow_connections=[
        {"from": "start", "to": "process"},
        {"from": "process", "to": "end"}
    ]
)
generator.export_to_png(html6, output_dir / "06-flowchart-right.png", viewport_width=2400, viewport_height=1600, padding=40)
print(f"   ✓ Saved: {output_dir / '06-flowchart-right.png'}")

print("\n" + "=" * 70)
print("✓ Hero alignment demo generated!")
print("=" * 70)
print(f"\nFiles saved to: {output_dir}")
print("\nGenerated examples:")
print("  1. Default (left/left/center)")
print("  2. Center alignment (center/center/center)")
print("  3. Right alignment (right/right/right)")
print("  4. Mixed alignment (center/left/left)")
print("  5. Triptych center alignment")
print("  6. Flowchart right alignment")
print("\nParameters:")
print("  - headline_align: 'left', 'center', or 'right'")
print("  - subheadline_align: 'left', 'center', or 'right' (defaults to headline_align)")
print("  - graphic_position: 'left', 'center', or 'right' (for open hero only)")
