"""Example: grouped (multi-series) vertical bar chart."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_grouped_bar_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Grouped bar", attribution=Attribution())
html = generate_grouped_bar_chart(
    gen,
    labels=["Q1", "Q2", "Q3", "Q4"],
    series=[
        {"name": "Product A", "values": [40, 55, 62, 78]},
        {"name": "Product B", "values": [28, 42, 51, 60]},
        {"name": "Product C", "values": [15, 22, 30, 45]},
    ],
    title="Sales by product",
    y_axis_label="Units",
)
gen.save(html, output_dir / "chart_grouped_bar.html")
gen.export_to_png(html, output_dir / "chart_grouped_bar.png")
print("Done:", output_dir / "chart_grouped_bar.png")
