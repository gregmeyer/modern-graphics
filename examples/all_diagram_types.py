"""Example: Generate all diagram types with sample data

This script demonstrates all available diagram types in the modern_graphics package.
Run this script to generate example outputs for each diagram type.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import modern_graphics
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Output directory (goes to generated/ for temporary outputs)
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize generator
generator = ModernGraphicsGenerator("All Diagram Types", attribution=Attribution())

print("Generating example diagrams...\n")

# 1. Cycle Diagram
print("1. Generating cycle diagram...")
html = generator.generate_cycle_diagram([
    {'text': 'Plan', 'color': 'blue'},
    {'text': 'Build', 'color': 'green'},
    {'text': 'Test', 'color': 'orange'},
    {'text': 'Deploy', 'color': 'purple'}
])
generator.export_to_png(html, output_dir / "01_cycle.png")
print("   ✓ Saved: 01_cycle.png")

# 2. Comparison Diagram
print("2. Generating comparison diagram...")
html = generator.generate_comparison_diagram(
    left_column={
        'title': 'Manual Approach',
        'steps': ['Time-intensive', 'Pixel perfect', 'Hard to update', 'One-time use']
    },
    right_column={
        'title': 'Automated Approach',
        'steps': ['Fast generation', 'Data-driven', 'Easy updates', 'Reusable']
    }
)
generator.export_to_png(html, output_dir / "02_comparison.png")
print("   ✓ Saved: 02_comparison.png")

# 3. Timeline Diagram (Horizontal)
print("3. Generating timeline diagram (horizontal)...")
html = generator.generate_timeline_diagram(
    events=[
        {'date': '2024 Q1', 'text': 'Launch - Initial release', 'color': 'blue'},
        {'date': '2024 Q2', 'text': 'Growth - User acquisition', 'color': 'green'},
        {'date': '2024 Q3', 'text': 'Scale - Expansion phase', 'color': 'orange'}
    ],
    orientation='horizontal'
)
generator.export_to_png(html, output_dir / "03_timeline_horizontal.png")
print("   ✓ Saved: 03_timeline_horizontal.png")

# 4. Timeline Diagram (Vertical)
print("4. Generating timeline diagram (vertical)...")
html = generator.generate_timeline_diagram(
    events=[
        {'date': 'Planning', 'text': 'Phase 1 - Requirements gathering', 'color': 'blue'},
        {'date': 'Development', 'text': 'Phase 2 - Building features', 'color': 'green'},
        {'date': 'Launch', 'text': 'Phase 3 - Go to market', 'color': 'orange'}
    ],
    orientation='vertical'
)
generator.export_to_png(html, output_dir / "04_timeline_vertical.png")
print("   ✓ Saved: 04_timeline_vertical.png")

# 5. Story Slide
print("5. Generating story slide...")
html = generator.generate_story_slide(
    title="The Transformation",
    what_changed="Revenue model shifted from one-time to recurring",
    time_period="Q2-Q4 2024",
    what_it_means="Predictable revenue and better customer relationships"
)
generator.export_to_png(html, output_dir / "05_story_slide.png")
print("   ✓ Saved: 05_story_slide.png")

# 6. Grid Diagram
print("6. Generating grid diagram...")
html = generator.generate_grid_diagram(
    items=[
        {'number': '1', 'text': 'First priority'},
        {'number': '2', 'text': 'Second priority'},
        {'number': '3', 'text': 'Third priority'},
        {'number': '4', 'text': 'Fourth priority'},
        {'number': '5', 'text': 'Fifth priority'}
    ],
    columns=5
)
generator.export_to_png(html, output_dir / "06_grid.png")
print("   ✓ Saved: 06_grid.png")

# 7. Pyramid Diagram
print("7. Generating pyramid diagram...")
# Note: Pyramid diagram is currently a stub - skipping for now
print("   ⚠️  Skipping pyramid (not implemented yet)")
# html = None  # Stub - not implemented yet
# generator.export_to_png(html, output_dir / "07_pyramid.png")

# 8. Flywheel Diagram
print("8. Generating flywheel diagram...")
html = generator.generate_flywheel_diagram(
    elements=[
        {'text': 'Acquire', 'color': 'blue'},
        {'text': 'Activate', 'color': 'green'},
        {'text': 'Retain', 'color': 'orange'},
        {'text': 'Refer', 'color': 'purple'}
    ],
    center_label="Growth Loop"
)
generator.export_to_png(html, output_dir / "08_flywheel.png")
print("   ✓ Saved: 08_flywheel.png")

# 9. Before/After Diagram
print("9. Generating before/after diagram...")
# Note: Before/after diagram is currently a stub - skipping for now
print("   ⚠️  Skipping before/after (not implemented yet)")
# html = generator.generate_before_after_diagram(
#     before_items=['Legacy system', 'Manual processes', 'Slow updates', 'High maintenance'],
#     after_items=['Modern platform', 'Automated workflows', 'Real-time updates', 'Low maintenance']
# )
# generator.export_to_png(html, output_dir / "09_before_after.png")

# 10. Funnel Diagram
print("10. Generating funnel diagram...")
# Note: Funnel diagram is currently a stub - skipping for now
print("   ⚠️  Skipping funnel (not implemented yet)")
# html = None  # Stub - not implemented yet
# generator.export_to_png(html, output_dir / "10_funnel.png")

# 11. Slide Cards
print("11. Generating slide cards...")
html = generator.generate_slide_card_diagram(
    cards=[
        {'title': 'Data Cards', 'tagline': '2010s', 'subtext': 'Simple rectangles with numbers', 'color': 'blue'},
        {'title': 'Infographics', 'tagline': '2020s', 'subtext': 'Rich visualizations with charts', 'color': 'green'},
        {'title': 'Story Slides', 'tagline': '2024+', 'subtext': 'Dynamic, AI-generated presentations', 'color': 'purple'}
    ]
)
generator.export_to_png(html, output_dir / "11_slide_cards.png")
print("   ✓ Saved: 11_slide_cards.png")

# 12. Slide Card Comparison
print("12. Generating slide card comparison...")
html = generator.generate_slide_card_comparison(
    left_card={'title': 'Looks Great', 'tagline': 'Manual', 'subtext': 'Pixel perfect design', 'color': 'blue'},
    right_card={'title': 'Updates Instantly', 'tagline': 'Automated', 'subtext': 'Data-driven generation', 'color': 'green'}
)
generator.export_to_png(html, output_dir / "12_slide_comparison.png")
print("   ✓ Saved: 12_slide_comparison.png")

print("\n✓ All diagrams generated successfully!")
print(f"   Output directory: {output_dir.absolute()}")
