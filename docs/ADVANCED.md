# Advanced Topics

Learn these features when you need them.

## SVG.js Integration

Create dynamic, programmatic SVG graphics using the SVG.js library. Perfect for complex diagrams, animations, and interactive elements.

**Enable SVG.js:**

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.svg_utils import (
    generate_svg_container,
    generate_svg_init_script,
    create_svg_circle,
    create_svg_line,
    create_svg_text,
)

# Enable SVG.js support
generator = ModernGraphicsGenerator("My Diagram", Attribution(), use_svg_js=True)

# Create SVG container
container = generate_svg_container("my-svg", 800, 600)

# Generate SVG elements
svg_elements = [
    create_svg_circle(400, 300, 100, "#4A90E2", stroke="#2E5C8A", stroke_width=3),
    create_svg_line(200, 300, 300, 300, "#666", stroke_width=2),
    create_svg_text(400, 320, "Center", font_size=20, fill="#333"),
]

# Generate initialization script
elements_code = '\n        '.join(svg_elements)
script = generate_svg_init_script("my-svg", 800, 600, elements_code)

# Wrap in HTML
content = f"""
<div style="padding: 40px;">
    {container}
    {script}
</div>
"""

html = generator._wrap_html(content, "")
generator.export_to_png(html, Path("output.png"))
```

**Available SVG.js Helpers:**

- `generate_svg_container(id, width, height)` - Create HTML container
- `generate_svg_init_script(id, width, height, custom_code)` - Generate initialization script
- `create_svg_circle(x, y, radius, fill, stroke, stroke_width)` - Create circle
- `create_svg_rect(x, y, width, height, fill, rx, stroke)` - Create rectangle
- `create_svg_line(x1, y1, x2, y2, stroke, stroke_width)` - Create line
- `create_svg_path(path_data, fill, stroke, stroke_width)` - Create path
- `create_svg_text(x, y, text, font_size, fill, font_family)` - Create text
- `create_svg_group(elements, transform)` - Create group of elements

**Custom JavaScript:**

You can also write custom JavaScript code that uses the SVG.js API:

```python
custom_script = """
    // Create gradient
    const gradient = draw.gradient('linear', function(stop) {
        stop.at(0, '#4A90E2')
        stop.at(1, '#8B5CF6')
    })
    
    // Create shapes
    draw.circle(100).move(350, 250).fill(gradient)
    draw.text('SVG.js').move(360, 320).font({size: 32}).fill('#333')
"""

script = generate_svg_init_script("my-svg", 800, 600, custom_script)
```

**When to Use SVG.js:**

- ✅ Complex diagrams with many elements
- ✅ Dynamic or animated graphics
- ✅ Programmatic shape generation
- ✅ Custom visualizations

**When to Use Static SVG:**

- ✅ Simple shapes and icons
- ✅ Static diagrams
- ✅ Performance-critical graphics

See `scripts/svg_js_example.py` for complete examples.

## Custom Diagram Types

Extend the system with your own diagram types:

```python
from modern_graphics.diagrams import DiagramGenerator, register_diagram
from modern_graphics.base import BaseGenerator

class MyDiagramGenerator(DiagramGenerator):
    def generate(self, generator: BaseGenerator, title: str, items: list, **kwargs) -> str:
        """Generate diagram HTML"""
        items_html = "".join(f'<li>{item}</li>' for item in items)
        css = """
        .my-diagram { ... }
        """
        html = f"<div class='my-diagram'><h2>{title}</h2><ul>{items_html}</ul></div>"
        return generator._wrap_html(html, css)
    
    def validate_input(self, title: str, items: list, **kwargs) -> bool:
        """Validate input parameters"""
        return bool(title and items)

# Register and use
register_diagram("my_diagram", MyDiagramGenerator)

generator = ModernGraphicsGenerator("My Diagram")
html = generator.generate_diagram("my_diagram", title="Items", items=["A", "B", "C"])
```

## AI-Assisted Template Creation

Create templates automatically using OpenAI. Requires `OPENAI_API_KEY` in your `.env` file.

**Quick Mode:**

```python
from modern_graphics import quick_template_from_description, register_template

# Generate template from description
template = quick_template_from_description(
    "dark professional theme with blue accents, modern sans-serif font"
)

# Register for use
register_template(template)

# Use it
from modern_graphics import ModernGraphicsGenerator
generator = ModernGraphicsGenerator("My Diagram", template=template)
```

**Example descriptions:**
- `"dark professional theme with blue accents, modern sans-serif font"`
- `"light minimalist design with pastel colors, elegant serif typography"`
- `"bold vibrant colors, tech startup style, clean sans-serif"`
- `"corporate blue and gray, professional, traditional fonts"`

**Interactive Interview:**

```python
from modern_graphics import interview_for_template, register_template

# Start interactive interview
template = interview_for_template()

if template:
    print(f"Created template: {template.name}")
    register_template(template)
    
    # Use it immediately
    from modern_graphics import ModernGraphicsGenerator
    generator = ModernGraphicsGenerator("My Diagram", template=template)
```

**CLI Interview:**

```bash
# Interactive interview (conversational)
python -m modern_graphics.cli_interview

# Quick generation from description
python -m modern_graphics.cli_interview --quick "dark theme with blue accents"

# Save template to file and register
python -m modern_graphics.cli_interview \
  --quick "professional theme" \
  --save my_template.json \
  --register
```

**Configuration:**

Set environment variables in `.env`:

```bash
OPENAI_API_KEY=your_openai_key_here
BRAINTRUST_API_KEY=your_braintrust_key_here  # Optional
BRAINTRUST_ENABLED=true  # Optional
```

## Custom Templates

Create your own visual style with the template system:

**Using TemplateBuilder:**

```python
from modern_graphics import TemplateBuilder, register_template, ModernGraphicsGenerator

# Create a custom template
dark_template = (TemplateBuilder("dark")
    .add_color("blue", ("#1a1a2e", "#16213e"), "rgba(0, 122, 255, 0.3)")
    .add_color("green", ("#0f5132", "#0d4228"), "rgba(52, 199, 89, 0.3)")
    .set_font_family("'Roboto', sans-serif")
    .set_background_color("#0a0a0a")
    .set_base_styles("""
        body {
            background: #0a0a0a;
            color: #ffffff;
        }
    """)
    .build())

# Register and use
register_template(dark_template)
generator = ModernGraphicsGenerator("My Diagram", template=dark_template)
```

**Template Builder Methods:**
- `.add_color(name, gradient, shadow)` - Add color to palette
- `.set_base_styles(css)` - Set base CSS styles
- `.set_attribution_styles(css)` - Set attribution CSS
- `.set_font_family(font_stack)` - Set font family
- `.set_background_color(color)` - Set default background
- `.copy_from(template)` - Copy from existing template

## Command Line Interface

For new workflows, use the unified `create` command. Keep legacy command syntax only for migration/compatibility.

**Hero:**
```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --png \
  --output hero.png
```

**Comparison Diagram:**
```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout comparison \
  --left "Left Title:Item1,Item2:Outcome" \
  --right "Right Title:Item3,Item4:Outcome" \
  --png \
  --output comparison.png
```

**Timeline Diagram:**
```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout timeline \
  --events "2024 Q1|Event1,2024 Q2|Event2,2024 Q3|Event3" \
  --orientation horizontal \
  --png \
  --output timeline.png
```

**Story Narrative:**
```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout story \
  --title "Revenue Shift" \
  --what-changed "One-time → Recurring" \
  --time-period "Q2-Q4 2025" \
  --what-it-means "Predictable revenue" \
  --png \
  --output story.png
```

See [Create Command Guide](CREATE_COMMAND.md) for layout-specific recipes, and [Migration Guide](MIGRATION.md) for legacy command mappings.
