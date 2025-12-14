"""Example: Creating and using a custom template"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.templates import TemplateBuilder, register_template

# Create custom dark template
dark_template = (TemplateBuilder("dark")
    .add_color("blue", ("#1a1a2e", "#16213e"), "rgba(0, 122, 255, 0.3)")
    .add_color("green", ("#0f5132", "#0d4228"), "rgba(52, 199, 89, 0.3)")
    .add_color("purple", ("#2d1b4e", "#1a0f2e"), "rgba(175, 82, 222, 0.3)")
    .add_color("gray", ("#2a2a2a", "#1a1a1a"), "rgba(0, 0, 0, 0.5)")
    .set_font_family("'Roboto', sans-serif")
    .set_background_color("#0a0a0a")
    .set_base_styles("""
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            padding: 60px 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
    """)
    .build())

# Register template
register_template(dark_template)

# Use it
generator = ModernGraphicsGenerator(
    "Dark Theme Cycle",
    template=dark_template,
    attribution=Attribution()
)

html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'},
    {'text': 'Step 3', 'color': 'purple'},
])

# Save
output_path = Path("dark_cycle_example.html")
generator.save(html, output_path)
print(f"Generated dark theme diagram: {output_path}")
