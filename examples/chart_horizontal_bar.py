"""Example: horizontal bar chart (ranked categories)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_horizontal_bar_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Horizontal bar", attribution=Attribution())
html = generate_horizontal_bar_chart(
    gen,
    labels=["Search", "Email", "Social", "Referral", "Direct"],
    values=[320, 245, 198, 140, 92],
    title="Sessions by channel",
    x_axis_label="Sessions (thousands)",
)
gen.save(html, output_dir / "chart_horizontal_bar.html")
gen.export_to_png(html, output_dir / "chart_horizontal_bar.png")
print("Done:", output_dir / "chart_horizontal_bar.png")
