# Modern Graphics Generator

Generate modern, professional graphics programmatically for articles and presentations. Create custom styles and extend with new diagram types.

## Features

- 🎨 **Template System**: Create custom styles with colors, fonts, and CSS
- 🔌 **Extensible**: Add new diagram types easily
- 📊 **10+ Diagram Types**: Cycle, comparison, grid, flywheel, timeline, pyramid, before/after, funnel, slide cards, story slides
- 🖼️ **High-Quality Export**: PNG export with tight cropping and high resolution
- 🎯 **Clean API**: Simple Python API and CLI

## Installation

### Basic Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install playwright pillow python-dotenv
playwright install chromium
```

### With AI Features (Optional)

For AI-assisted template creation, install with the `ai` extra:

```bash
pip install -e ".[ai]"
```

This installs:
- `openai>=1.0.0` - For AI-assisted template creation
- `braintrust>=0.0.0` - For evaluation tracking (optional)

The package works without these, but AI features require OpenAI. Braintrust is optional for tracking evaluation metrics.

### Environment Variables (Optional)

For AI-assisted template and diagram generation:

1. Install with AI support: `pip install -e ".[ai]"`
2. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   OPENAI_API_KEY=your_openai_key_here
   BRAINTRUST_API_KEY=your_braintrust_key_here
   
   # Optional: Control Braintrust logging
   BRAINTRUST_ENABLED=true   # or false to disable
   ```

The `.env` file is automatically ignored by git to keep your keys secure.

### Disabling Braintrust Logging

You can disable Braintrust logging in several ways:

**Via environment variable:**
```bash
# In .env file
BRAINTRUST_ENABLED=false
```

**Via Python code:**
```python
from modern_graphics import set_braintrust_enabled

# Disable logging
set_braintrust_enabled(False)

# Re-enable logging
set_braintrust_enabled(True)
```

**Check status:**
```python
from modern_graphics import braintrust_enabled

if braintrust_enabled():
    print("Braintrust logging is enabled")
```

## AI-Assisted Template Creation

Create templates through an interactive interview or quick description:

### Quick Mode

```python
from modern_graphics import quick_template_from_description, register_template

# Generate template from description
template = quick_template_from_description(
    "dark professional theme with blue accents, modern sans-serif font"
)
register_template(template)
```

### Interactive Interview

```python
from modern_graphics import interview_for_template, register_template

# Have a conversation to design your template
template = interview_for_template()
if template:
    register_template(template)
```

### CLI Interview

```bash
# Interactive interview
python -m modern_graphics.cli_interview

# Quick generation
python -m modern_graphics.cli_interview --quick "dark theme with blue accents"

# Save to file
python -m modern_graphics.cli_interview --quick "professional theme" --save template.json --register
```

## Quick Start

### Basic Usage

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from pathlib import Path

generator = ModernGraphicsGenerator("My Diagram", Attribution())

# Generate a cycle diagram
html = generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'},
    {'text': 'Step 3', 'color': 'purple'},
])

# Save HTML
generator.save(html, Path('output.html'))

# Export as PNG
generator.export_to_png(html, Path('output.png'))
```

### Command Line Interface

```bash
# Generate a cycle diagram
modern-graphics cycle --title "My Cycle" --steps "Step1,Step2,Step3" --output output.html

# Export as PNG
modern-graphics cycle --title "My Cycle" --steps "Step1,Step2,Step3" --output output.png --png

# Generate a story-driven slide
modern-graphics story-slide \
  --title "Revenue Shift" \
  --what-changed "One-time → Recurring" \
  --time-period "Q2-Q4 2025" \
  --what-it-means "Predictable revenue" \
  --output slide.png --png
```

## Custom Templates

Create your own visual style with the template system:

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

### Template Builder Methods

- `.add_color(name, gradient, shadow)` - Add color to palette
- `.set_base_styles(css)` - Set base CSS styles
- `.set_attribution_styles(css)` - Set attribution CSS
- `.set_font_family(font_stack)` - Set font family
- `.set_background_color(color)` - Set default background
- `.copy_from(template)` - Copy from existing template

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

## Diagram Types

- **Cycle**: Flow diagrams with arrows
- **Comparison**: Side-by-side comparisons
- **Grid**: Numbered grid layouts
- **Flywheel**: Circular flywheel diagrams
- **Timeline**: Horizontal or vertical timelines
- **Pyramid**: Hierarchical pyramid diagrams
- **Before/After**: Transformation diagrams
- **Funnel**: Conversion funnel diagrams
- **Slide Cards**: Presentation card layouts
- **Story Slide**: Story-driven narrative slides

## API Reference

### ModernGraphicsGenerator

Main generator class for creating graphics.

```python
generator = ModernGraphicsGenerator(
    title: str,
    template: Optional[StyleTemplate] = None,
    attribution: Optional[Attribution] = None
)
```

**Methods:**
- `generate_cycle_diagram(steps, ...)` - Generate cycle diagram
- `generate_comparison_diagram(left_column, right_column, ...)` - Generate comparison
- `generate_diagram(diagram_type, **kwargs)` - Generate by type name (registry-based)
- `save(html_content, output_path)` - Save HTML to file
- `export_to_png(html_content, output_path, ...)` - Export to PNG

### Template System

```python
from modern_graphics.templates import (
    StyleTemplate,      # Template class
    DEFAULT_TEMPLATE,   # Default template
    TemplateBuilder,    # Builder for creating templates
    register_template,  # Register custom template
    get_template,       # Get template by name
)
```

### Diagram System

```python
from modern_graphics.diagrams import (
    DiagramGenerator,    # Base class for diagrams
    register_diagram,    # Register custom diagram
    get_diagram_generator,  # Get diagram class by name
    DIAGRAM_REGISTRY,    # Registry of available diagrams
)
```

## Examples

See the `examples/` directory for:
- `custom_template.py` - Creating custom templates
- `custom_diagram.py` - Creating custom diagram types

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests (when available)
pytest

# Format code
black modern_graphics/

# Lint code
ruff check modern_graphics/
```

## Architecture

The package is organized into:

- **`templates/`** - Style template system
  - `base.py` - StyleTemplate class
  - `default.py` - Default template
  - `builder.py` - TemplateBuilder for creating templates
  
- **`diagrams/`** - Diagram generators
  - `base.py` - DiagramGenerator ABC
  - Individual diagram modules (cycle, comparison, etc.)
  
- **Core modules**:
  - `generator.py` - Main ModernGraphicsGenerator class
  - `base.py` - BaseGenerator with template support
  - `export.py` - PNG export functionality
  - `utils.py` - Utility functions

## License

MIT

## Contributing

Contributions welcome! The system is designed to be extensible:
- Add new diagram types by implementing `DiagramGenerator`
- Add new templates using `TemplateBuilder`
- Submit PRs for improvements
