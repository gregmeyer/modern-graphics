"""Example: PNG export options

This example demonstrates different PNG export options including
resolution, scaling, and cropping settings.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Output directory (goes to generated/ for temporary outputs)
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

generator = ModernGraphicsGenerator("Export Options", attribution=Attribution())

# Generate a sample diagram
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'},
    {'text': 'Step 3', 'color': 'orange'}
])

print("Generating PNGs with different export settings...\n")

# Example 1: Default settings (high quality)
print("1. Default export (2400x1600, scale 2x)...")
generator.export_to_png(
    html,
    output_dir / "export_default.png"
)
print("   ✓ Saved: export_default.png")

# Example 2: Higher resolution
print("2. Higher resolution (3200x2400, scale 3x)...")
generator.export_to_png(
    html,
    output_dir / "export_high_res.png",
    viewport_width=3200,
    viewport_height=2400,
    device_scale_factor=3
)
print("   ✓ Saved: export_high_res.png")

# Example 3: Lower resolution (faster)
print("3. Lower resolution (1200x800, scale 1x)...")
generator.export_to_png(
    html,
    output_dir / "export_low_res.png",
    viewport_width=1200,
    viewport_height=800,
    device_scale_factor=1
)
print("   ✓ Saved: export_low_res.png")

# Example 4: More padding
print("4. Extra padding (40px)...")
generator.export_to_png(
    html,
    output_dir / "export_extra_padding.png",
    padding=40
)
print("   ✓ Saved: export_extra_padding.png")

# Example 5: Minimal padding
print("5. Minimal padding (5px)...")
generator.export_to_png(
    html,
    output_dir / "export_minimal_padding.png",
    padding=5
)
print("   ✓ Saved: export_minimal_padding.png")

print("\n✓ Export examples generated!")
print(f"   Output directory: {output_dir.absolute()}")
print("\nNote: All PNGs are automatically cropped to content bounding box.")
