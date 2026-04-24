"""Example: line chart with two series."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_line_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Line chart", attribution=Attribution())
html = generate_line_chart(
    gen,
    labels=["Q1", "Q2", "Q3", "Q4"],
    series=[
        {"name": "2024", "values": [42, 58, 71, 88]},
        {"name": "2025", "values": [60, 75, 95, 118]},
    ],
    title="Revenue growth",
    subtitle="Quarterly, YoY",
    x_axis_label="Quarter",
    y_axis_label="Revenue ($M)",
)
gen.save(html, output_dir / "chart_line.html")
gen.export_to_png(html, output_dir / "chart_line.png")
print("Done:", output_dir / "chart_line.png")
