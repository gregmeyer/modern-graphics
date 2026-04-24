"""Example: grouped stacked bar — products stacked, years side-by-side per quarter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_grouped_stacked_bar_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Grouped stacked bar", attribution=Attribution())
html = generate_grouped_stacked_bar_chart(
    gen,
    labels=["Q1", "Q2", "Q3", "Q4"],
    series=[
        # 2024 stack
        {"name": "Product A", "stack": "2024", "values": [40, 52, 60, 72]},
        {"name": "Product B", "stack": "2024", "values": [28, 35, 41, 48]},
        {"name": "Product C", "stack": "2024", "values": [12, 18, 22, 28]},
        # 2025 stack
        {"name": "Product A", "stack": "2025", "values": [55, 68, 80, 95]},
        {"name": "Product B", "stack": "2025", "values": [38, 47, 55, 65]},
        {"name": "Product C", "stack": "2025", "values": [20, 28, 34, 42]},
    ],
    title="Revenue by product (2024 vs 2025)",
    subtitle="Two bars per quarter — 2024 left, 2025 right — stacked by product",
    y_axis_label="Revenue ($K)",
)
gen.save(html, output_dir / "chart_grouped_stacked_bar.html")
gen.export_to_png(html, output_dir / "chart_grouped_stacked_bar.png")
print("Done:", output_dir / "chart_grouped_stacked_bar.png")
