# Custom Themes

Build branded visual styles without changing diagram logic.

## Use This Doc When

- You want to customize fonts, colors, or background for your graphics.
- You need AI-assisted template generation.
- You are building a reusable branded template.

If you only need the default CLI path, use [Create Command Guide](./CREATE_COMMAND.md).
If you need SVG.js or custom diagram types, use [SVG Composition](./SVG_COMPOSITION.md).

## Fast Path: Build a Custom Theme (Font + Colors)

```python
from pathlib import Path
from modern_graphics import TemplateBuilder, register_template, ModernGraphicsGenerator, Attribution

brand_theme = (
    TemplateBuilder("brand-clean")
    .add_color("primary", ("#0B1F3A", "#163A6B"), "rgba(22, 58, 107, 0.28)")
    .add_color("accent", ("#0E7490", "#155E75"), "rgba(14, 116, 144, 0.24)")
    .set_font_family("'Avenir Next', 'Segoe UI', sans-serif")
    .set_background_color("#F8FAFC")
    .build()
)

register_template(brand_theme)
generator = ModernGraphicsGenerator("Brand Theme Example", Attribution(), template=brand_theme)

html = generator.generate_cycle_diagram([
    {"text": "Capture", "color": "primary"},
    {"text": "Decide", "color": "accent"},
    {"text": "Ship", "color": "primary"},
])
generator.export_to_png(html, Path("output/custom-theme-insight.png"), crop_mode="safe")
print("Expected output: output/custom-theme-insight.png")
```

Need crop or padding tuning after theme changes? Use [Export Guide](./EXPORT.md).

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

---

## Read Next

- [Export Guide](./EXPORT.md) -- crop, padding, and social export behavior
