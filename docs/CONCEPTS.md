# Core Concepts

Understanding these four concepts will help you use the library effectively.

## 1. The Generator

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

## 2. Diagram Types

The library includes 10+ diagram types, each optimized for different use cases.

**Visual Gallery:**

![Cycle Diagram](../examples/output/showcase/diagram-types/01-cycle.png)
![Comparison Diagram](../examples/output/showcase/diagram-types/02-comparison.png)
![Timeline Diagram](../examples/output/showcase/diagram-types/03-timeline.png)
![Story Slide](../examples/output/showcase/diagram-types/04-story-slide.png)
![Grid Diagram](../examples/output/showcase/diagram-types/05-grid.png)
![Flywheel Diagram](../examples/output/showcase/diagram-types/06-flywheel.png)
![Slide Cards](../examples/output/showcase/diagram-types/07-slide-cards.png)
![Slide Card Comparison](../examples/output/showcase/diagram-types/08-slide-comparison.png)

**Choosing the Right Type:** See [Diagram Types Guide](./DIAGRAM_TYPES.md) for a decision tree and detailed examples.

## 3. Templates

Templates control the visual style of your graphics: colors, fonts, backgrounds, and overall aesthetic.

**Why Use Templates?**
- **Consistency**: All graphics match your brand
- **Speed**: Apply styles instantly
- **Flexibility**: Switch between styles easily

**Default Template:**
Every generator uses a default template (clean, modern style). You can use it as-is or customize it.

**Custom Templates:**
Create templates to match your brand or use case:

```python
from modern_graphics import quick_template_from_description

# Generate a template from a description
template = quick_template_from_description(
    "corporate blue and gray, professional, traditional fonts"
)

# Use it
generator = ModernGraphicsGenerator("My Diagram", template=template)
```

**Template Examples:**

| Default | Corporate | Tech Startup |
|---------|-----------|--------------|
| ![Default Template](../examples/output/showcase/templates/default.png) | ![Corporate Template](../examples/output/showcase/templates/corporate.png) | ![Tech Startup Template](../examples/output/showcase/templates/tech-startup.png) |

**Learn More:** See [Custom Templates](../README.md#custom-templates) in the full documentation.

## 4. Attribution

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
| ![Default Attribution](../examples/output/showcase/attribution/default.png) | ![Custom Styled Attribution](../examples/output/showcase/attribution/custom-styled.png) | ![Attribution with Context](../examples/output/showcase/attribution/with-context.png) |

**Learn More:** See [Attribution System](../README.md#attribution-system) in the full documentation.
