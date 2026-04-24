"""Example: single-series vertical bar chart."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_bar_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Bar chart", attribution=Attribution())
html = generate_bar_chart(
    gen,
    labels=["North", "South", "East", "West", "Central"],
    values=[42, 58, 71, 34, 95],
    title="Units shipped by region",
    y_axis_label="Units (thousands)",
)
gen.save(html, output_dir / "chart_bar.html")
gen.export_to_png(html, output_dir / "chart_bar.png")
print("Done:", output_dir / "chart_bar.png")
