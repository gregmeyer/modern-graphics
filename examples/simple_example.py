#!/usr/bin/env python3
"""Simple example: Generate a cycle diagram

This is a minimal example showing how to use the modern-graphics package
to generate a simple graphic.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Create a generator with attribution
generator = ModernGraphicsGenerator(
    "Product Development Cycle",
    attribution=Attribution(
        copyright="© 2025 Example Company",
        context="Development Process"
    )
)

# Generate a cycle diagram
html = generator.generate_cycle_diagram([
    {'text': 'Plan', 'color': 'blue'},
    {'text': 'Build', 'color': 'green'},
    {'text': 'Test', 'color': 'orange'},
    {'text': 'Deploy', 'color': 'purple'}
])

# Save HTML
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)
html_path = output_dir / "simple_cycle.html"
generator.save(html, html_path)
print(f"✓ Saved HTML: {html_path}")

# Export to PNG
png_path = output_dir / "simple_cycle.png"
generator.export_to_png(
    html,
    png_path,
    viewport_width=2400,
    viewport_height=1200,
    device_scale_factor=2,
    padding=40,
)
print(f"✓ Exported PNG: {png_path}")
print(f"\nOpen {html_path} in a browser to view the graphic!")
