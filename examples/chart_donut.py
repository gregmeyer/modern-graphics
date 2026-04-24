"""Example: donut chart."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_donut_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Donut", attribution=Attribution())
html = generate_donut_chart(
    gen,
    labels=["Retained", "Upsold", "Churned", "New"],
    values=[62, 14, 9, 15],
    title="Customer outcomes (FY)",
)
gen.save(html, output_dir / "chart_donut.html")
gen.export_to_png(html, output_dir / "chart_donut.png")
print("Done:", output_dir / "chart_donut.png")
