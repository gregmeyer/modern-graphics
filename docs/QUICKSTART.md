# Quick Start Guide

Get your first graphic in 5 minutes.

## Use This Doc When

- You want the fastest first successful output.
- You are new to `modern-graphics create`.
- You have not chosen a custom theme or advanced hero workflow yet.

If you already know your target layout and flags, use [Create Command Guide](./CREATE_COMMAND.md).

## Installation

```bash
pip install playwright pillow python-dotenv
playwright install chromium
```

That's it! No complex setup needed.

## Fastest Path (CLI)

Use the unified `create` command first:

```bash
modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --output ./output/hero.html
```

Then export directly to PNG:

```bash
modern-graphics create \
  --layout insight-card \
  --text "One-page artifacts force explicit decisions." \
  --png \
  --output ./output/insight-card.png
```

Defaults are clarity-first (`density=clarity`, `crop-mode=safe`, `padding-mode=minimal`).

For layout recipes and options:
- **[Create Command Guide](./CREATE_COMMAND.md)**
- **[Export Guide](./EXPORT.md)**

## Programmatic Path (Python)

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

## What's Included

When you install Modern Graphics Generator, you get:

**10+ Diagram Types:**
- Cycle diagrams (process flows)
- Comparison diagrams (side-by-side)
- Timeline diagrams (events over time)
- Story slides (data-driven narratives)
- Grid diagrams (numbered lists)
- Flywheel diagrams (growth loops)
- Slide cards (multiple concepts)
- Pyramid diagrams (hierarchies)
- Before/After diagrams (transformations)
- Funnel diagrams (conversion funnels)
- Slide card comparisons

**Features:**
- ✅ High-quality PNG export (automatic cropping)
- ✅ Customizable templates (colors, fonts, styles)
- ✅ Attribution system (copyright/context)
- ✅ Simple Python API
- ✅ Command-line interface
- ✅ Extensible (add your own diagram types)

## What You Just Learned

In those few lines, you:
1. **Created a generator** - The main class that creates graphics
2. **Generated a diagram** - Used `generate_cycle_diagram()` to create a flow diagram
3. **Exported to PNG** - Saved a high-quality image file

## Next Steps

- **[Create Command Guide](./CREATE_COMMAND.md)** - call the CLI directly with layout recipes
- **[Diagram Types](./DIAGRAM_TYPES.md)** - choose the right layout for your message
- **[Advanced Topics](./ADVANCED.md)** - custom themes, SVG.js, and extension paths
- **[Hero Slides Guide](./HERO_SLIDES.md)** - super custom hero composition
- **[Full Documentation](README.md)** - complete task-first docs map
