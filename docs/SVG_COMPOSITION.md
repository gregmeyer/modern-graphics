# SVG Composition

Build custom SVG graphics and extend the diagram system with SVG.js and custom diagram types.

## Use This Doc When

- You need programmatic SVG generation with SVG.js.
- You are building a custom diagram type.
- You want dynamic or animated graphics.

If you need a custom color theme, use [Custom Themes](./CUSTOM_THEMES.md).
If you need the fastest first output, use [Quick Start Guide](./QUICKSTART.md).

## SVG.js Integration

Create dynamic, programmatic SVG graphics using the SVG.js library.

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

**When to Use SVG.js vs Static SVG:**

- SVG.js: complex diagrams, dynamic/animated graphics, programmatic shape generation
- Static SVG: simple shapes and icons, static diagrams, performance-critical graphics

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

## Deep Dive

For wireframe scene schema details, see [Wireframe Scene Spec](WIREFRAME_SCENE_SPEC.md).

---

## Read Next

- [Hero Slides Guide](./HERO_SLIDES.md) -- hero composition patterns and freeform usage
