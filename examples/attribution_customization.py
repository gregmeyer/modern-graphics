"""Example: Customizing Attribution Bug

Demonstrates all the customization options available for the attribution bug.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Output directory
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "attribution_custom"
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Attribution Customization Examples")
print("=" * 60)
print()

generator = ModernGraphicsGenerator("Attribution Examples", attribution=Attribution())

# Example 1: Default attribution
print("1. Default attribution...")
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "01_default.png")
print(f"   ✓ Saved: {output_dir / '01_default.png'}")
print()

# Example 2: Custom colors and size
print("2. Custom colors and font size...")
attribution = Attribution(
    copyright="© My Company 2025",
    font_size="14px",
    font_color="#007AFF",
    font_weight="600",
    opacity=1.0
)
generator = ModernGraphicsGenerator("Custom Colors", attribution=attribution)
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "02_custom_colors.png")
print(f"   ✓ Saved: {output_dir / '02_custom_colors.png'}")
print()

# Example 3: With background
print("3. Attribution with background...")
attribution = Attribution(
    copyright="© Brand Name 2025",
    background_color="rgba(0, 0, 0, 0.7)",
    font_color="#FFFFFF",
    padding="10px 16px",
    border_radius="8px",
    opacity=1.0
)
generator = ModernGraphicsGenerator("With Background", attribution=attribution)
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "03_with_background.png")
print(f"   ✓ Saved: {output_dir / '03_with_background.png'}")
print()

# Example 4: Bottom-center position
print("4. Bottom-center position...")
attribution = Attribution(
    copyright="© Center Attribution 2025",
    position="bottom-center",
    font_size="13px",
    font_color="#666666"
)
generator = ModernGraphicsGenerator("Center Position", attribution=attribution)
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "04_center_position.png")
print(f"   ✓ Saved: {output_dir / '04_center_position.png'}")
print()

# Example 5: With context
print("5. Attribution with context...")
attribution = Attribution(
    copyright="© Context Example 2025",
    context="Generated for Q4 Report",
    font_size="11px",
    font_color="#8E8E93"
)
generator = ModernGraphicsGenerator("With Context", attribution=attribution)
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "05_with_context.png")
print(f"   ✓ Saved: {output_dir / '05_with_context.png'}")
print()

# Example 6: Minimal/subtle
print("6. Minimal/subtle attribution...")
attribution = Attribution(
    copyright="© Minimal 2025",
    font_size="10px",
    font_color="#C7C7CC",
    opacity=0.6,
    padding="4px 8px"
)
generator = ModernGraphicsGenerator("Minimal", attribution=attribution)
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "06_minimal.png")
print(f"   ✓ Saved: {output_dir / '06_minimal.png'}")
print()

# Example 7: Hidden attribution
print("7. Hidden attribution (show=False)...")
attribution = Attribution(
    copyright="© Hidden 2025",
    show=False
)
generator = ModernGraphicsGenerator("Hidden", attribution=attribution)
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator.export_to_png(html, output_dir / "07_hidden.png")
print(f"   ✓ Saved: {output_dir / '07_hidden.png'}")
print()

print("=" * 60)
print("✓ Attribution customization examples generated!")
print(f"   Output directory: {output_dir.absolute()}")
print("=" * 60)
