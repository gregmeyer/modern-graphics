# Modern Graphics Generator

Generate modern, professional graphics programmatically for articles, presentations, and documentation. Create diagrams, charts, and visualizations with clean Python code.

## Quick Navigation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get your first graphic in 5 minutes
- **[Core Concepts](docs/CONCEPTS.md)** - Learn the four essential concepts  
- **[Diagram Types](docs/DIAGRAM_TYPES.md)** - Choose the right diagram type
- **[Common Use Cases](docs/USE_CASES.md)** - Real-world examples and patterns

## What is This?

Modern Graphics Generator lets you create professional graphics programmatically. Instead of designing slides manually, write Python code to generate diagrams, timelines, comparisons, and more. Perfect for:

- **Articles & Blog Posts**: Generate graphics that match your writing
- **Presentations**: Create consistent, data-driven slides
- **Documentation**: Visualize processes, architectures, and concepts
- **Reports**: Automate quarterly reports, dashboards, and summaries

**Key Features:**
- 🎨 **10+ Diagram Types**: Cycle, comparison, timeline, story slides, grid, flywheel, and more
- 🎯 **Simple API**: Generate graphics with just a few lines of Python
- 🤖 **AI-Powered**: Generate diagrams from natural language prompts (optional)
- 🖼️ **High-Quality Export**: PNG export with automatic cropping
- 🎨 **Customizable**: Templates for consistent branding
- 🔌 **Extensible**: Add your own diagram types

## Quick Start

Get your first graphic in 5 minutes.

### Installation

```bash
pip install playwright pillow python-dotenv
playwright install chromium
```

That's it! No complex setup needed.

**Note:** Most features work **without an OpenAI API key**. Only prompt-based generation (optional) requires OpenAI. See [Working Without OpenAI](#working-without-openai) below.

### Your First Graphic

Copy and paste this code:

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from pathlib import Path

# Create a generator
generator = ModernGraphicsGenerator("My First Diagram", Attribution())

# Generate a cycle diagram
html = generator.generate_cycle_diagram([
    {'text': 'Plan', 'color': 'blue'},
    {'text': 'Build', 'color': 'green'},
    {'text': 'Deploy', 'color': 'orange'}
])

# Export as PNG
generator.export_to_png(html, Path('output.png'))
print("✓ Generated output.png")
```

Run it and you'll have your first graphic!

### What You Just Learned

In those few lines, you:
1. **Created a generator** - The main class that creates graphics
2. **Generated a diagram** - Used `generate_cycle_diagram()` to create a flow diagram
3. **Exported to PNG** - Saved a high-quality image file

**Next:** Learn about [Core Concepts](#core-concepts) to understand how the library works.

## Core Concepts

Understanding these four concepts will help you use the library effectively.

### 1. The Generator

The `ModernGraphicsGenerator` is the main class that creates graphics. You create one, then use it to generate different diagram types.

```python
from modern_graphics import ModernGraphicsGenerator, Attribution

# Create a generator
generator = ModernGraphicsGenerator(
    title="My Diagram",           # Title for the graphic
    attribution=Attribution()     # Copyright/context info (optional)
)

# Generate different diagram types
html = generator.generate_cycle_diagram([...])
html = generator.generate_comparison_diagram(...)
html = generator.generate_timeline_diagram(...)
# ... and more
```

**Key Points:**
- One generator can create multiple graphics
- All graphics share the same title and attribution settings
- Generator methods return HTML that you can export to PNG

### 2. Diagram Types

The library includes 10+ diagram types, each optimized for different use cases.

**Visual Gallery:**

![Cycle Diagram](examples/output/showcase/diagram-types/01-cycle.png)
![Comparison Diagram](examples/output/showcase/diagram-types/02-comparison.png)
![Timeline Diagram](examples/output/showcase/diagram-types/03-timeline.png)
![Story Slide](examples/output/showcase/diagram-types/04-story-slide.png)
![Grid Diagram](examples/output/showcase/diagram-types/05-grid.png)
![Flywheel Diagram](examples/output/showcase/diagram-types/06-flywheel.png)
![Slide Cards](examples/output/showcase/diagram-types/07-slide-cards.png)
![Slide Card Comparison](examples/output/showcase/diagram-types/08-slide-comparison.png)

**Choosing the Right Type:** See [Diagram Types Guide](#diagram-types-guide) for a decision tree and detailed examples.

### 3. Templates

Templates control the visual style of your graphics: colors, fonts, backgrounds, and overall aesthetic.

**Why Use Templates?**
- **Consistency**: All graphics match your brand
- **Speed**: Apply styles instantly
- **Flexibility**: Switch between styles easily

**Default Template:**
Every generator uses a default template (clean, modern style). You can use it as-is or customize it.

**Template Examples:**

| Default | Corporate | Tech Startup |
|---------|-----------|--------------|
| ![Default Template](examples/output/showcase/templates/default.png) | ![Corporate Template](examples/output/showcase/templates/corporate.png) | ![Tech Startup Template](examples/output/showcase/templates/tech-startup.png) |

**Learn More:** See [Custom Templates](#custom-templates) in Advanced Topics.

### 4. Attribution

Attribution adds copyright and context information to your graphics. It appears at the bottom of generated images.

**Default Behavior:**
- Attribution is included automatically
- Shows copyright: "© Greg Meyer 2025 • gregmeyer.com"
- Positioned at bottom-right

**Customize It:**
```python
from modern_graphics import Attribution

# Custom attribution
attribution = Attribution(
    copyright="© My Company 2025",
    context="Q4 Report",
    position="bottom-center"
)

generator = ModernGraphicsGenerator("My Diagram", attribution=attribution)
```

**Attribution Examples:**

| Default | Custom Styled | With Context |
|---------|---------------|--------------|
| ![Default Attribution](examples/output/showcase/attribution/default.png) | ![Custom Styled Attribution](examples/output/showcase/attribution/custom-styled.png) | ![Attribution with Context](examples/output/showcase/attribution/with-context.png) |

**Learn More:** See [Attribution System](#attribution-system) for all options.

## Common Use Cases

Practical patterns for real-world usage.

### Quick Graphics

Use convenience functions for fast generation without creating a generator instance:

```python
from modern_graphics import generate_cycle_diagram

# Generate HTML directly
html = generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
```

### Custom Styling

Apply templates for consistent branding:

```python
from modern_graphics import quick_template_from_description, register_template, ModernGraphicsGenerator

# Generate a template from a description
template = quick_template_from_description(
    "corporate blue and gray, professional, traditional fonts"
)

# Use it
generator = ModernGraphicsGenerator("My Diagram", template=template)
```

### Batch Generation

Generate multiple graphics efficiently:

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from pathlib import Path

generator = ModernGraphicsGenerator("Batch Graphics", Attribution())

data = [
    {'title': 'Q1 Results', 'steps': [...]},
    {'title': 'Q2 Results', 'steps': [...]},
    {'title': 'Q3 Results', 'steps': [...]},
]

for item in data:
    html = generator.generate_cycle_diagram(item['steps'])
    generator.export_to_png(html, Path(f"{item['title']}.png"))
```

### Prompt-Based Generation

Generate diagrams from natural language prompts using AI. All diagram types support prompt-based generation with default prompts that work out of the box.

**Basic Usage:**

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics import generate_cycle_diagram_from_prompt
from pathlib import Path

generator = ModernGraphicsGenerator("My Diagram", Attribution())

# Use default prompt (works automatically)
html = generate_cycle_diagram_from_prompt(generator)

# Or provide a custom prompt
html = generate_cycle_diagram_from_prompt(
    generator,
    prompt="Show a marketing funnel: Awareness (red), Interest (blue), Consideration (green), Purchase (purple)"
)

generator.export_to_png(html, Path('output.png'))
```

**Available Prompt Functions:**

All diagram types have prompt-based generators:

```python
from modern_graphics import (
    generate_cycle_diagram_from_prompt,
    generate_comparison_diagram_from_prompt,
    generate_timeline_diagram_from_prompt,
    generate_grid_diagram_from_prompt,
    generate_flywheel_diagram_from_prompt,
    generate_slide_cards_from_prompt,
    generate_slide_card_comparison_from_prompt,
    DEFAULT_DIAGRAM_PROMPTS
)

# Use defaults
html = generate_cycle_diagram_from_prompt(generator)

# Custom prompt
html = generate_timeline_diagram_from_prompt(
    generator,
    prompt="Show product milestones: Q1 Launch, Q2 Growth, Q3 Scale, Q4 Mature"
)

# View default prompts
print(DEFAULT_DIAGRAM_PROMPTS['cycle'])
```

**When to Use Prompts vs Hardcoded Data:**

- **Use Prompts**: When you want AI to interpret natural language and extract structure
- **Use Hardcoded Data**: When you have exact data structures and want precise control

Both approaches work - choose based on your needs!

**Requirements:** Prompt-based generation requires `OPENAI_API_KEY` in your `.env` file.

## Working Without OpenAI

**Good news:** Most features work **without an OpenAI API key**! You only need OpenAI for prompt-based generation (which is optional).

### What Works Without OpenAI ✅

All structured data generation works without OpenAI:

- ✅ **Cycle diagrams** - `generate_cycle_diagram(steps)`
- ✅ **Comparison diagrams** - `generate_comparison_diagram(left, right)`
- ✅ **Timeline diagrams** - `generate_timeline_diagram(events)`
- ✅ **Grid diagrams** - `generate_grid_diagram(items)`
- ✅ **Flywheel diagrams** - `generate_flywheel_diagram(elements)`
- ✅ **Slide cards** - `generate_slide_card_diagram(cards)`
- ✅ **Story slides** - `generate_story_slide(title, what_changed, time_period, what_it_means)`
- ✅ **Before/After diagrams** - `generate_before_after_diagram(before, after)`
- ✅ **Funnel diagrams** - `generate_funnel_diagram(stages, values)`
- ✅ **Pyramid diagrams** - `generate_pyramid_diagram(layers)`
- ✅ **CLI commands** - All CLI commands work without OpenAI
- ✅ **PNG export** - Export works without OpenAI
- ✅ **Templates** - Using existing templates works without OpenAI

### What Requires OpenAI ⚠️

Only these **optional** prompt-based features require OpenAI:

- ⚠️ **Prompt-based generation** - `generate_*_from_prompt()` functions
- ⚠️ **AI template creation** - `quick_template_from_description()`
- ⚠️ **Story slides from prompts** - `create_story_slide_from_prompt()`

### Example: No OpenAI Needed

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from pathlib import Path

# Works without OpenAI API key!
generator = ModernGraphicsGenerator("My Diagram", Attribution())

# Generate slide card (structured data - no OpenAI)
cards = [{
    "title": "Revenue Transformation",
    "tagline": "Q2-Q4 2025",
    "subtext": "Revenue model shifted from licenses to subscriptions",
    "color": "blue",
    "badge": "+24% QoQ",
    "features": ["Predictable revenue", "20% higher retention"]
}]

html = generator.generate_slide_card_diagram(cards)
generator.export_to_png(html, Path('output.png'))
# ✓ Generated without OpenAI!
```

**Bottom line:** Use structured data (dictionaries, lists) and you don't need OpenAI. Use prompts (natural language) and you'll need an OpenAI API key.

### Export Options

Control PNG export quality and resolution:

```python
# Standard quality (default)
generator.export_to_png(html, Path('output.png'))

# High quality for print
generator.export_to_png(
    html, 
    Path('output.png'),
    viewport_width=3200,
    device_scale_factor=3
)

# Fast/low quality for previews
generator.export_to_png(
    html,
    Path('output.png'),
    viewport_width=1200,
    device_scale_factor=1
)
```

See [Export Options](#export-options) for complete details.

## Diagram Types Guide

Choose the right diagram type for your use case:

**Decision Tree:**
- **Process/Flow** → Cycle Diagram
- **Comparison** → Comparison Diagram
- **Timeline** → Timeline Diagram
- **Story/Narrative** → Story Slide
- **List/Grid** → Grid Diagram
- **Hierarchy** → Pyramid Diagram
- **Growth Loop** → Flywheel Diagram
- **Transformation** → Before/After Diagram
- **Conversion** → Funnel Diagram
- **Cards** → Slide Cards

For detailed examples and code for each type, see **[Diagram Types Guide](docs/DIAGRAM_TYPES.md)**.

## Advanced Topics

Learn these features when you need them.

### Attribution System

All graphics can include attribution information (copyright, context) that appears at the bottom of generated images. Fully customizable styling and positioning.

**Attribution Examples:**

| Default | Custom Styled | With Context |
|---------|---------------|--------------|
| ![Default Attribution](examples/output/showcase/attribution/default.png) | ![Custom Styled Attribution](examples/output/showcase/attribution/custom-styled.png) | ![Attribution with Context](examples/output/showcase/attribution/with-context.png) |

**Default Attribution:**

```python
Attribution(
    copyright="© Greg Meyer 2025 • gregmeyer.com",
    position="bottom-right",
    margin_top=20
)
```

**Custom Attribution:**

```python
from modern_graphics import Attribution

attribution = Attribution(
    copyright="© My Company 2025",
    context="Generated for Q4 Report",
    position="bottom-center",
    font_size="14px",
    font_color="#007AFF",
    font_weight="600",
    background_color="rgba(0, 0, 0, 0.7)",
    opacity=0.9,
    padding="10px 16px",
    border_radius="8px"
)

generator = ModernGraphicsGenerator("My Diagram", attribution=attribution)
```

**Disable Attribution:**

```python
# Method 1: Set show=False
attribution = Attribution(show=False)

# Method 2: Empty copyright
attribution = Attribution(copyright="")
```

### Custom Templates

Create your own visual style with the template system:

**Template Examples:**

| Default | Corporate | Tech Startup |
|---------|-----------|--------------|
| ![Default Template](examples/output/showcase/templates/default.png) | ![Corporate Template](examples/output/showcase/templates/corporate.png) | ![Tech Startup Template](examples/output/showcase/templates/tech-startup.png) |

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

### Custom Diagram Types

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

### AI-Assisted Template Creation

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

### Command Line Interface

The CLI provides commands for all diagram types. Use `--png` flag to export as PNG instead of HTML.

**Cycle Diagram:**
```bash
modern-graphics cycle \
  --title "My Cycle" \
  --steps "Step1,Step2,Step3" \
  --output output.png --png
```

**Comparison Diagram:**
```bash
modern-graphics comparison \
  --title "Comparison" \
  --left "Left Title:Item1,Item2:Outcome" \
  --right "Right Title:Item3,Item4:Outcome" \
  --output comparison.png --png
```

**Timeline Diagram:**
```bash
modern-graphics timeline \
  --title "Timeline" \
  --events "2024 Q1|Event1,2024 Q2|Event2,2024 Q3|Event3" \
  --orientation horizontal \
  --output timeline.png --png
```

**Story Slide:**
```bash
modern-graphics story-slide \
  --title "Revenue Shift" \
  --what-changed "One-time → Recurring" \
  --time-period "Q2-Q4 2025" \
  --what-it-means "Predictable revenue" \
  --output slide.png --png
```

**Common Options:**
- `--copyright "Text"` - Custom copyright text
- `--context "Text"` - Optional context line for attribution
- `--png` - Export as PNG instead of HTML

## Reference Sections

Complete documentation for when you need it.

### API Reference

#### ModernGraphicsGenerator

Main generator class for creating graphics.

```python
generator = ModernGraphicsGenerator(
    title: str,
    template: Optional[StyleTemplate] = None,
    attribution: Optional[Attribution] = None
)
```

**Diagram Generation Methods:**

- `generate_cycle_diagram(steps, arrow='→', cycle_end=None)` - Generate cycle diagram
- `generate_comparison_diagram(left_column, right_column, comparison_title='vs')` - Generate comparison
- `generate_timeline_diagram(events, orientation='horizontal')` - Generate timeline
- `generate_story_slide(title, what_changed, time_period, what_it_means, insight=None)` - Generate story slide
- `generate_grid_diagram(items, columns=5)` - Generate grid layout
- `generate_pyramid_diagram(levels)` - Generate pyramid
- `generate_flywheel_diagram(elements, center_label=None, radius=220)` - Generate flywheel
- `generate_before_after_diagram(before_items, after_items)` - Generate before/after
- `generate_funnel_diagram(stages, values)` - Generate funnel
- `generate_slide_card_diagram(cards)` - Generate slide cards
- `generate_slide_card_comparison(left_card, right_card)` - Generate slide card comparison

**Prompt-Based Generation Methods:**

- `generate_cycle_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate cycle from prompt
- `generate_comparison_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate comparison from prompt
- `generate_timeline_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate timeline from prompt
- `generate_grid_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate grid from prompt
- `generate_flywheel_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate flywheel from prompt
- `generate_slide_cards_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate slide cards from prompt
- `generate_slide_card_comparison_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate slide card comparison from prompt

All prompt-based methods use default prompts if `prompt=None`. See `DEFAULT_DIAGRAM_PROMPTS` for available defaults.

**Export Methods:**

- `save(html_content, output_path)` - Save HTML to file
- `export_to_png(html_content, output_path, viewport_width=2400, viewport_height=1600, device_scale_factor=2, padding=20, temp_html_path=None)` - Export to PNG

#### Convenience Functions

For quick generation without creating a generator instance:

```python
from modern_graphics import (
    generate_cycle_diagram,
    generate_comparison_diagram,
    generate_timeline_diagram,
    generate_story_slide,
    # ... etc
)

# Generate HTML directly
html = generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
```

#### Prompt-Based Functions

Generate diagrams from natural language prompts:

```python
from modern_graphics import (
    generate_cycle_diagram_from_prompt,
    generate_comparison_diagram_from_prompt,
    generate_timeline_diagram_from_prompt,
    generate_grid_diagram_from_prompt,
    generate_flywheel_diagram_from_prompt,
    generate_slide_cards_from_prompt,
    generate_slide_card_comparison_from_prompt,
    DEFAULT_DIAGRAM_PROMPTS,
    ModernGraphicsGenerator,
    Attribution
)

generator = ModernGraphicsGenerator("My Diagram", Attribution())

# Use default prompt
html = generate_cycle_diagram_from_prompt(generator)

# Custom prompt
html = generate_cycle_diagram_from_prompt(
    generator,
    prompt="Show a customer journey: Discover, Try, Buy, Love"
)
```

### Examples & Showcase

#### Showcase Examples

High-quality showcase examples are available in `examples/output/showcase/`:

- **Diagram Types** (`showcase/diagram-types/`) - One example of each diagram type (8 examples)
- **Templates** (`showcase/templates/`) - Different template styles (default, corporate, tech startup)
- **Attribution** (`showcase/attribution/`) - Different attribution configurations
- **Use Cases** (`showcase/use-cases/`) - Real-world use case examples

**Use Case Examples:**

| Corporate Report | Tech Startup Pitch | Educational Course |
|------------------|-------------------|-------------------|
| ![Corporate Report](examples/output/showcase/use-cases/corporate-report.png) | ![Tech Startup Pitch](examples/output/showcase/use-cases/tech-pitch.png) | ![Educational Course](examples/output/showcase/use-cases/educational-course.png) |

**Regenerate showcase:** Run `python scripts/generate_showcase.py` to regenerate all showcase examples. Showcase examples use prompt-based generation with default prompts (see `modern_graphics.prompt_to_diagram.DEFAULT_DIAGRAM_PROMPTS`).

#### Example Scripts

The `scripts/` directory contains comprehensive example and utility scripts:

- **`all_diagram_types.py`** - Generate all diagram types
- **`batch_generation.py`** - Batch generate multiple graphics
- **`custom_template.py`** - Creating and using custom templates
- **`attribution_examples.py`** - Customizing attribution
- **`export_options.py`** - PNG export options and settings
- **`use_case_*.py`** - Real-world use case examples
- **`generate_showcase.py`** - Generate showcase examples for README

**Output Location:** All example scripts save outputs to `examples/output/generated/` (not tracked in git).

**Note:** Showcase examples in `examples/output/showcase/` are tracked in git and can be viewed directly.

PNG export provides high-quality output with automatic tight cropping to content.

#### Export Parameters

```python
generator.export_to_png(
    html_content,
    output_path,
    viewport_width=2400,        # Browser viewport width (CSS pixels)
    viewport_height=1600,       # Browser viewport height (CSS pixels)
    device_scale_factor=2,      # Scale factor for resolution (1-4 recommended)
    padding=20,                  # Padding around content (CSS pixels)
    temp_html_path=None          # Optional: custom temp HTML path
)
```

#### Resolution Guidelines

- **Standard Quality**: `viewport_width=2400, device_scale_factor=2` (default)
  - Good for most use cases, fast generation
  - Output: ~4800px wide at 2x scale
  
- **High Quality**: `viewport_width=3200, device_scale_factor=3`
  - For print or large displays
  - Output: ~9600px wide at 3x scale
  
- **Fast/Low Quality**: `viewport_width=1200, device_scale_factor=1`
  - For quick previews or small displays
  - Output: ~1200px wide

#### Automatic Cropping

All PNG exports automatically crop to the content bounding box, removing excess whitespace. Adjust `padding` if content is cut off:

```python
# More padding if content is too close to edges
generator.export_to_png(html, path, padding=40)

# Minimal padding for tight crop
generator.export_to_png(html, path, padding=5)
```

### Troubleshooting

#### Installation Issues

**Playwright browser not found:**
```bash
playwright install chromium
```

**Python version error:**
- Ensure Python 3.8+ is installed: `python3 --version`

#### PNG Export Issues

**"playwright not found" error:**
```bash
pip install playwright
playwright install chromium
```

**Low quality exports:**
- Increase `device_scale_factor` (default: 2, try 3 or 4)
- Increase `viewport_width` and `viewport_height`

**Cropping issues:**
- Adjust `padding` parameter if content is cut off: `export_to_png(html, path, padding=40)`

#### AI Features Issues

**"OPENAI_API_KEY not found" error:**
- **You only see this if using prompt-based features** (optional)
- **Solution 1**: Use structured data instead (no OpenAI needed) - see [Working Without OpenAI](#working-without-openai)
  ```python
  # Instead of: generate_cycle_diagram_from_prompt(generator, prompt="...")
  # Use: generator.generate_cycle_diagram([{'text': 'Step 1', 'color': 'blue'}])
  ```
- **Solution 2**: If you want prompt-based generation:
  - Ensure `.env` file exists with `OPENAI_API_KEY=your_key`
  - Or set environment variable: `export OPENAI_API_KEY=your_key`
  - Verify API key is valid and has credits
  - Check OpenAI model availability

**Template generation fails:**
- Only affects AI-assisted template creation (optional)
- Use existing templates or create templates manually (no OpenAI needed)
- If using AI template creation, verify API key is valid and has credits

## Additional Resources

### Documentation

- **[Core Concepts](docs/CONCEPTS.md)** - Detailed explanation of the four concepts
- **[Diagram Types Guide](docs/DIAGRAM_TYPES.md)** - Decision tree and all diagram types
- **[Common Use Cases](docs/USE_CASES.md)** - Practical examples and patterns
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes

### Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Format code
black modern_graphics/

# Lint code
ruff check modern_graphics/
```

## License

MIT

## Contributing

Contributions welcome! The system is designed to be extensible:
- Add new diagram types by implementing `DiagramGenerator`
- Add new templates using `TemplateBuilder`
- Submit PRs for improvements

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for more details.
