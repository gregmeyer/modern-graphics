"""Example: Combo Chart Diagrams

Demonstrates creating combo charts (dual-axis charts) as standalone diagrams.
Combo charts combine two different visualizations on the same chart with dual axes.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams import generate_combo_chart

# Output directory
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "combo_charts"
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Combo Chart Examples")
print("=" * 60)
print()

generator = ModernGraphicsGenerator("Combo Charts", attribution=Attribution())

# Example 1: Ocean Heat vs Extreme Weather Events
print("1. Ocean Heat vs Extreme Weather Events (Line + Bars)...")
primary_data = [
    {"x": "2020", "y": 100},
    {"x": "2021", "y": 110},
    {"x": "2022", "y": 125},
    {"x": "2023", "y": 150},
    {"x": "2024", "y": 180}
]
secondary_data = [
    {"x": "2020", "y": 50},
    {"x": "2021", "y": 65},
    {"x": "2022", "y": 80},
    {"x": "2023", "y": 100},
    {"x": "2024", "y": 120}
]

html = generate_combo_chart(
    generator,
    primary_data=primary_data,
    secondary_data=secondary_data,
    primary_style="line",
    secondary_style="bars",
    primary_name="Ocean Heat (ZJ)",
    secondary_name="Extreme Events"
)
generator.export_to_png(html, output_dir / "01_ocean_heat_vs_weather.png")
print(f"   ✓ Saved: {output_dir / '01_ocean_heat_vs_weather.png'}")
print()

# Example 2: Revenue vs User Growth (Area + Spikes)
print("2. Revenue vs User Growth (Area + Spikes)...")
revenue_data = [
    {"x": "Q1", "y": 50000},
    {"x": "Q2", "y": 75000},
    {"x": "Q3", "y": 95000},
    {"x": "Q4", "y": 120000}
]
user_data = [
    {"x": "Q1", "y": 1000},
    {"x": "Q2", "y": 2500},
    {"x": "Q3", "y": 4500},
    {"x": "Q4", "y": 8000}
]

html = generate_combo_chart(
    generator,
    primary_data=revenue_data,
    secondary_data=user_data,
    primary_style="area",
    secondary_style="spikes",
    primary_name="Revenue ($)",
    secondary_name="Users"
)
generator.export_to_png(html, output_dir / "02_revenue_vs_users.png")
print(f"   ✓ Saved: {output_dir / '02_revenue_vs_users.png'}")
print()

# Example 3: Temperature vs Precipitation (Line + Bars with custom colors)
print("3. Temperature vs Precipitation (Custom Colors)...")
temp_data = [
    {"x": "Jan", "y": 15},
    {"x": "Feb", "y": 18},
    {"x": "Mar", "y": 22},
    {"x": "Apr", "y": 25},
    {"x": "May", "y": 28}
]
precip_data = [
    {"x": "Jan", "y": 80},
    {"x": "Feb", "y": 60},
    {"x": "Mar", "y": 40},
    {"x": "Apr", "y": 20},
    {"x": "May", "y": 10}
]

html = generate_combo_chart(
    generator,
    primary_data=temp_data,
    secondary_data=precip_data,
    primary_style="line",
    secondary_style="bars",
    primary_color="#FF6B6B",
    secondary_color="#4ECDC4",
    primary_name="Temperature (°C)",
    secondary_name="Precipitation (mm)"
)
generator.export_to_png(html, output_dir / "03_temp_vs_precip.png")
print(f"   ✓ Saved: {output_dir / '03_temp_vs_precip.png'}")
print()

print("=" * 60)
print("✓ Combo chart examples generated!")
print(f"   Output directory: {output_dir.absolute()}")
print("=" * 60)
