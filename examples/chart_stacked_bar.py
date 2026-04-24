"""Example: stacked bar chart — composition per category."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_stacked_bar_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Stacked bar", attribution=Attribution())
html = generate_stacked_bar_chart(
    gen,
    labels=["FY22", "FY23", "FY24", "FY25", "FY26"],
    series=[
        {"name": "FY21 & prior", "values": [150, 140, 130, 120, 110]},
        {"name": "FY22 cohort",  "values": [  0,  90,  80,  72,  65]},
        {"name": "FY23 cohort",  "values": [  0,   0, 110, 100,  92]},
        {"name": "FY24 cohort",  "values": [  0,   0,   0, 135, 125]},
        {"name": "FY25 cohort",  "values": [  0,   0,   0,   0, 160]},
    ],
    title="Annual recurring revenue by cohort",
    subtitle="Stacked by acquisition year",
    y_axis_label="ARR ($K)",
)
gen.save(html, output_dir / "chart_stacked_bar.html")
gen.export_to_png(html, output_dir / "chart_stacked_bar.png")
print("Done:", output_dir / "chart_stacked_bar.png")
