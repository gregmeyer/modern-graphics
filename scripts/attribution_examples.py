"""Example: Customizing attribution

This example shows different ways to customize attribution
on generated graphics.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Output directory (goes to generated/ for temporary outputs)
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

# Example 1: Default attribution
print("1. Default attribution (bottom-right)...")
generator1 = ModernGraphicsGenerator(
    "Default Attribution",
    attribution=Attribution()  # Uses default copyright
)
html1 = generator1.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator1.export_to_png(html1, output_dir / "attribution_default.png")
print("   ✓ Saved: attribution_default.png")

# Example 2: Custom copyright and context
print("2. Custom copyright with context...")
generator2 = ModernGraphicsGenerator(
    "Custom Attribution",
    attribution=Attribution(
        copyright="© My Company 2025",
        context="Generated for Q4 Report",
        position="bottom-right"
    )
)
html2 = generator2.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator2.export_to_png(html2, output_dir / "attribution_custom.png")
print("   ✓ Saved: attribution_custom.png")

# Example 3: Bottom-center position
print("3. Attribution at bottom-center...")
generator3 = ModernGraphicsGenerator(
    "Center Attribution",
    attribution=Attribution(
        copyright="© Example Corp 2025",
        position="bottom-center",
        margin_top=30
    )
)
html3 = generator3.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator3.export_to_png(html3, output_dir / "attribution_center.png")
print("   ✓ Saved: attribution_center.png")

# Example 4: No attribution
print("4. No attribution (empty copyright)...")
generator4 = ModernGraphicsGenerator(
    "No Attribution",
    attribution=Attribution(copyright="")  # Empty string disables attribution
)
html4 = generator4.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
generator4.export_to_png(html4, output_dir / "attribution_none.png")
print("   ✓ Saved: attribution_none.png")

print("\n✓ Attribution examples generated!")
print(f"   Output directory: {output_dir.absolute()}")
