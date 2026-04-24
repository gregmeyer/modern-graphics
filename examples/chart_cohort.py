"""Example: cohort retention heatmap (Mixpanel-style)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.cohort_chart import generate_cohort_chart

output_dir = Path(__file__).parent / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

cohorts = [
    {"date": "Jan 19, 2026", "size": 7262, "values": [95.61, 33.53, 31.34, 29.00, 28.44, 27.64, 27.61, 26.60, 26.55, 24.90, 23.70, 20.02]},
    {"date": "Jan 26, 2026", "size": 7187, "values": [95.58, 33.74, 30.51, 29.32, 29.11, 27.91, 27.29, 26.81, 24.09, 24.66, 20.72, 3.80]},
    {"date": "Feb 2, 2026",  "size": 7291, "values": [96.06, 32.53, 30.74, 28.98, 28.93, 27.91, 27.72, 24.72, 24.89, 21.44, 3.61]},
    {"date": "Feb 9, 2026",  "size": 7071, "values": [95.80, 32.84, 30.99, 30.38, 29.57, 28.95, 25.94, 26.06, 21.91, 4.09]},
    {"date": "Feb 16, 2026", "size": 7151, "values": [95.97, 32.42, 31.62, 30.02, 29.13, 26.78, 26.49, 22.30, 4.32]},
    {"date": "Feb 23, 2026", "size": 6864, "values": [95.86, 34.13, 31.86, 31.59, 28.07, 27.19, 23.28, 4.50]},
    {"date": "Mar 2, 2026",  "size": 6844, "values": [95.95, 34.13, 33.28, 29.32, 28.58, 23.99, 4.54]},
    {"date": "Mar 9, 2026",  "size": 7120, "values": [96.60, 33.69, 29.85, 29.06, 24.24, 4.40]},
    {"date": "Mar 16, 2026", "size": 7127, "values": [95.16, 31.19, 29.47, 24.41, 5.11]},
    {"date": "Mar 23, 2026", "size": 7565, "values": [96.73, 28.34, 24.18, 4.60]},
    {"date": "Mar 30, 2026", "size": 6390, "values": [95.92, 28.78, 5.34]},
]

gen = ModernGraphicsGenerator("Cohort retention", attribution=Attribution())
html = generate_cohort_chart(
    gen,
    cohorts=cohorts,
    title="Weekly retention",
    subtitle="The number of weeks later your users were retained.",
)
gen.save(html, output_dir / "chart_cohort.html")
gen.export_to_png(html, output_dir / "chart_cohort.png")
print("Done:", output_dir / "chart_cohort.png")
