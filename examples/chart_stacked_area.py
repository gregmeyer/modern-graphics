"""Example: stacked area chart — cohort revenue over time."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_stacked_area_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Stacked area", attribution=Attribution())
html = generate_stacked_area_chart(
    gen,
    labels=["2022", "2023", "2024", "2025", "2026"],
    series=[
        {"name": "2021 cohort & prior", "values": [150, 140, 135, 130, 125]},
        {"name": "2022 cohort",         "values": [0,    85,  78,  72,  68]},
        {"name": "2023 cohort",         "values": [0,    0,   92,  84,  78]},
        {"name": "2024 cohort",         "values": [0,    0,   0,   98,  90]},
        {"name": "2025 cohort",         "values": [0,    0,   0,   0,  120]},
    ],
    title="Revenue by cohort",
    subtitle="Cumulative annual revenue layered by acquisition year",
    y_axis_label="Revenue ($K)",
)
gen.save(html, output_dir / "chart_stacked_area.html")
gen.export_to_png(html, output_dir / "chart_stacked_area.png")
print("Done:", output_dir / "chart_stacked_area.png")
