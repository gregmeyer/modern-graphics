#!/usr/bin/env python3
"""Example: Radar diagram for support signal mapping"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Create generator
generator = ModernGraphicsGenerator(
    "Support Radar Example",
    attribution=Attribution(
        copyright="© 2025 Example",
        context="Support Signals",
    )
)

# Define signals
signals = [
    {
        "axiom": "Axiom 1: Orientation",
        "detects": '"What happens next?" spikes',
        "discovers": "Orientation failure",
        "covers": "Clear states, progress, ownership",
        "position": {"angle": 0},  # Top
        "color": "blue",
    },
    {
        "axiom": "Axiom 2: Receipts",
        "detects": '"Did it go through?" spikes',
        "discovers": "Receipt failure",
        "covers": "Confirmations, audit trails, undo",
        "position": {"angle": 72},  # Top-right
        "color": "purple",
    },
    {
        "axiom": "Axiom 3: Loud Failures",
        "detects": '"It just didn\'t work" mysteries',
        "discovers": "Silent-failure failure",
        "covers": "Error states, causes, recovery",
        "position": {"angle": 144},  # Bottom-right
        "color": "green",
    },
    {
        "axiom": "Axiom 4: Trust",
        "detects": "Billing/access panic spikes",
        "discovers": "Trust failure",
        "covers": "Previews, confirmations, reversibility",
        "position": {"angle": 216},  # Bottom-left
        "color": "orange",
    },
    {
        "axiom": "Axiom 5: Product Debt",
        "detects": "Stable top driver (month over month)",
        "discovers": "Repeat confusion = bug",
        "covers": "Root cause, simplification, guardrails",
        "position": {"angle": 288},  # Top-left
        "color": "gray",
    },
]

# Generate radar diagram
html = generator.generate_radar_diagram(
    signals=signals,
    center_label="SUPPORT\nRADAR",
    viewbox_width=1200,
    viewbox_height=700,
    radar_radius=250,
    show_sweep=True,
    show_circles=True,
)

# Save HTML
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)
html_path = output_dir / "radar_example.html"
generator.save(html, html_path)
print(f"✓ Saved: {html_path}")

# Export PNG with minimal padding for tight crop
png_path = output_dir / "radar_example.png"
generator.export_to_png(
    html,
    png_path,
    viewport_width=1400,
    viewport_height=900,
    device_scale_factor=2,
    padding=10,
)
print(f"✓ Exported: {png_path}")
