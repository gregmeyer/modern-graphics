"""Example: pie chart."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_pie_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Pie", attribution=Attribution())
html = generate_pie_chart(
    gen,
    labels=["Mobile", "Web", "API", "Other"],
    values=[48, 32, 15, 5],
    title="Traffic share by platform",
)
gen.save(html, output_dir / "chart_pie.html")
gen.export_to_png(html, output_dir / "chart_pie.png")
print("Done:", output_dir / "chart_pie.png")
