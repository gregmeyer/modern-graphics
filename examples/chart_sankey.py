"""Example: sankey flow diagram."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.charts import generate_sankey_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

gen = ModernGraphicsGenerator("Sankey", attribution=Attribution())
html = generate_sankey_chart(
    gen,
    links=[
        {"from": "Visit",   "to": "Signup",  "value": 100},
        {"from": "Visit",   "to": "Bounce",  "value": 60},
        {"from": "Signup",  "to": "Trial",   "value": 80},
        {"from": "Signup",  "to": "Dropped", "value": 20},
        {"from": "Trial",   "to": "Paid",    "value": 35},
        {"from": "Trial",   "to": "Churned", "value": 45},
    ],
    title="Funnel flow",
    subtitle="Visitors → Paid customers",
)
gen.save(html, output_dir / "chart_sankey.html")
gen.export_to_png(html, output_dir / "chart_sankey.png")
print("Done:", output_dir / "chart_sankey.png")
