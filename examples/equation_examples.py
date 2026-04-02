"""Example: Generate equation layout graphics

Demonstrates the equation layout with different themes, sizes, and operators.
Equations are auto-parsed — terms and operators (=, +, −, ×, ÷) are detected
and rendered as stacked lines with operators aligned left.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.color_scheme import get_scheme
from modern_graphics.diagrams.equation import generate_equation

output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

print("Generating equation examples...\n")

# 1. The Satisfaction Gap — dark theme, large
print("1. Satisfaction Gap (dark theme, large)...")
generator = ModernGraphicsGenerator("Satisfaction Gap", attribution=Attribution())
html = generate_equation(
    generator,
    equation="Satisfaction = Perception - Expectation",
    label="The Satisfaction Gap",
    footnote="The gap is where churn lives.",
    color_scheme=get_scheme("dark"),
    size="large",
)
generator.export_to_png(html, output_dir / "equation_satisfaction_dark.png", crop_mode="none")
print("   Done: equation_satisfaction_dark.png")

# 2. The Profit Equation — apple theme, medium, multiply operator
print("2. Profit Equation (apple theme, medium)...")
generator = ModernGraphicsGenerator("Profit Equation", attribution=Attribution())
html = generate_equation(
    generator,
    equation="Revenue = Volume × Price - Cost",
    label="The Profit Equation",
    footnote="Most teams optimize only one variable.",
    color_scheme=get_scheme("apple"),
    size="medium",
)
generator.export_to_png(html, output_dir / "equation_profit_apple.png", crop_mode="none")
print("   Done: equation_profit_apple.png")

# 3. Simple two-term — corporate theme, small
print("3. Trust Equation (corporate theme, small)...")
generator = ModernGraphicsGenerator("Trust Equation", attribution=Attribution())
html = generate_equation(
    generator,
    equation="Trust = Consistency × Time",
    label="Why trust compounds",
    color_scheme=get_scheme("corporate"),
    size="small",
)
generator.export_to_png(html, output_dir / "equation_trust_corporate.png", crop_mode="none")
print("   Done: equation_trust_corporate.png")

# 4. Pretext mode — dark theme
print("4. Satisfaction Gap (dark theme, pretext SVG text)...")
generator = ModernGraphicsGenerator("Satisfaction Gap", attribution=Attribution(), use_pretext=True)
html = generate_equation(
    generator,
    equation="Satisfaction = Perception - Expectation",
    label="The Satisfaction Gap",
    footnote="The gap is where churn lives.",
    color_scheme=get_scheme("dark"),
    size="large",
)
generator.export_to_png(html, output_dir / "equation_satisfaction_pretext.png", crop_mode="none")
print("   Done: equation_satisfaction_pretext.png")

print(f"\nAll examples saved to {output_dir}/")
