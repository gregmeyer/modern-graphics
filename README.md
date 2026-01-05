# Modern Graphics Generator

> Build hero slides, story cards, and diagrams from prompts or structured data—one theme across every output. Designed for storytellers, marketing teams, and analysts who need branded visuals in minutes.

> **Theme demo note:** PNG thumbnails in `examples/output/theme-demo/*.png` are checked in, but the gallery `index.html` is generated locally. Run `python examples/generate_complete_theme_demo.py` before opening `examples/output/theme-demo/index.html`.

[**Jump to the theme demo →**](examples/output/theme-demo/index.html) *(PNG previews are versioned; run `python examples/generate_complete_theme_demo.py` to regenerate HTML locally.)*

## Why teams use it
- 🎨 **One theme across everything** – set colors + fonts once, reuse across heroes, cards, and diagrams
- 📊 **10+ built-in layouts** – story slides, cycles, timelines, funnels, pyramids, grids, and editorial cards
- ⚡ **Simple Python API** – instantiate a generator and export PNGs in a few lines
- 🤖 **Prompt-ready workflows** – optional AI helpers for themes, decks, or article summaries
- 🧩 **Extensible** – write your own diagram modules or SVG.js mockups
- 🖼️ **Production exports** – high-res PNGs with automatic cropping

## Quick Navigation

- **[How Do I Get Started?](#how-do-i-get-started)** - Get your first graphic in 5 minutes
- **[How Do I Prompt Creatively?](#how-do-i-prompt-creatively)** - AI-powered generation techniques
- **[What Can You Create?](#what-can-you-create)** - See all diagram types and examples
- **[Customization Guide](#customization-guide)** - Create custom themes and styles
- **[Examples & Showcase](#examples--showcase)** - Browse real examples
- **[Documentation](#documentation)** - Complete guides and API reference

## What Can You Create?

**Quick example:**
```python
from modern_graphics import generate_scheme_from_prompt

# Create theme from description
scheme = generate_scheme_from_prompt(
    "modern tech startup with bright cyan and coral colors"
)

# Apply to any graphic
html = generator.generate_modern_hero(...)
html = scheme.apply_to_html(html)  # Colors + fonts applied automatically
```

[View complete theme demo →](examples/output/theme-demo/index.html) | [Create Your Theme →](docs/ADVANCED.md#color-scheme-generator)

### Diagram Types

10+ built-in layouts cover everything from narrative story slides to comparison grids. Highlights:

- **Narrative slides:** story slides, editorial hero panels
- **Flow & journeys:** cycles, flywheels, funnels, pyramids, milestone timelines, roadmaps
- **Comparison & grids:** comparison cards, matrices, KPI or insight grids
- **Before/after stories:** transformation cards, makeover grids, KPI deltas

**Preview them:** PNG thumbnails live in `examples/output/showcase/diagram-types/` (tracked). For themed variants (funnel, pyramid, hero canvas cards, etc.), run `python examples/generate_complete_theme_demo.py` and open `examples/output/theme-demo/index.html`.

[Diagram reference →](docs/DIAGRAM_TYPES.md)

### Hero Slides

| Tiles | Flowchart | Triptych |
|-------|-----------|----------|
| ![Hero Tiles](examples/output/showcase/hero-slides/01-open-canvas-tiles.png) | ![Hero Flowchart](examples/output/showcase/hero-slides/02-open-canvas-flowchart.png) | ![Hero Triptych](examples/output/showcase/hero-slides/05-triptych.png) |

The thumbnails above are tracked in git for quick reference (`examples/output/showcase/hero-slides/`). To see the latest themed renderings, run `python examples/generate_complete_theme_demo.py` and open `examples/output/theme-demo/index.html`.

[Hero Slides Guide →](docs/HERO_SLIDES.md)

## How Do I Get Started?

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

### Your First Theme (Optional but Recommended)

Create a custom theme and apply it to your graphic:

```python
from modern_graphics import generate_scheme_from_prompt

# Create theme from description
scheme = generate_scheme_from_prompt(
    "modern tech startup with bright cyan and coral colors, bold sans-serif font"
)

# Apply to your graphic
html = scheme.apply_to_html(html)
generator.export_to_png(html, Path('output-themed.png'))
```

Now your graphic uses consistent branding that you can apply to all future graphics!

**Next:** Learn about [Core Concepts](docs/CONCEPTS.md) or try [How Do I Prompt Creatively?](#how-do-i-prompt-creatively)

## Examples & Showcase

- **Story slides:** Combine hero canvas, modular cards, and timelines for narratives ([story slide gallery](examples/output/showcase/diagram-types/04-story-slide.png)).  
  ![Story Slide](examples/output/theme-demo/11-story-slide.png)
- **Apply one theme everywhere:** Theme demo shows thirteen graphics sharing the same palette/fonts ([see the live set](examples/output/theme-demo/index.html)).  
  ![Theme Demo](examples/output/theme-demo/04-slide-cards-two.png) *(PNG checked in; run `python examples/generate_complete_theme_demo.py` to rebuild `index.html` locally)*
- **Illustrate long-form content:** Feed an article outline and let the system storyboard it ([use cases](examples/output/showcase/use-cases/)).  
  ![Use Case](examples/output/showcase/use-cases/corporate-report.png)
- **Ops guardrail premium cards:** The new `premium-card` CLI renders the stacked hero/detail layout we used for the Ops Leaders “questions for agents” article.  
  ```bash
  modern-graphics premium-card \
    --title "Ops Guardrail Premium Card" \
    --config examples/ops_guardrail_premium_card.json \
    --output examples/output/generated/ops-guardrail-card.png \
    --png
  ```
  Add `--top-only` (hero canvas) or `--bottom-only` (detail card) to mirror the article’s workflow. The command above drops PNGs into `examples/output/generated/` so you can compare your output to the guardrail showcase cards.

Want more? Browse diagram thumbnails in repo (e.g., `examples/output/showcase/hero-slides/01-*.png`), or run `python scripts/run_showcase.py` to regenerate the curated PNGs.

## How Do I Prompt Creatively?

Generate themes and diagrams from natural language prompts using AI. This is an **optional** feature that requires an OpenAI API key.

### Overview

**What it is:** Describe what you want in natural language, AI generates the graphic.

**When to use:**
- You want AI to interpret your description
- You're exploring creative ideas
- You want to generate themes from brand descriptions

**When to use structured data instead:**
- You have exact data structures
- You want precise control
- You don't have an OpenAI API key

### Creative Prompting Techniques

#### Theme Prompts

Generate complete color schemes and fonts from brand descriptions:

```python
from modern_graphics import generate_scheme_from_prompt

# Be specific about colors and style
scheme = generate_scheme_from_prompt(
    "modern tech startup with bright cyan primary color, coral accents, bold Poppins font"
)

# Include industry context
scheme = generate_scheme_from_prompt(
    "professional corporate theme with navy blue accents and serif font for financial services"
)

# Describe mood and aesthetic
scheme = generate_scheme_from_prompt(
    "playful startup theme with vibrant colors and rounded sans-serif font"
)
```

#### Diagram Prompts

Generate diagrams from natural language descriptions:

```python
from modern_graphics import generate_cycle_diagram_from_prompt

# Simple workflow
html = generate_cycle_diagram_from_prompt(
    generator,
    prompt="Show a customer journey: Discover, Try, Buy, Love"
)

# With colors
html = generate_cycle_diagram_from_prompt(
    generator,
    prompt="Show software development: Plan (blue), Build (green), Test (orange), Deploy (purple)"
)

# Comparison diagrams
from modern_graphics import generate_comparison_diagram_from_prompt

html = generate_comparison_diagram_from_prompt(
    generator,
    prompt="Compare manual design (slow, inconsistent) vs template-based (fast, consistent)"
)
```

#### Story Slide Prompts

Generate story-driven slides:

```python
from modern_graphics.prompt_to_diagram import generate_story_slide_from_prompt

html = generate_story_slide_from_prompt(
    generator,
    prompt="""What changed: Revenue model shifted from upfront licenses to subscriptions
Time period: Q2-Q4 2025
What it means: Predictable revenue and 20% higher retention"""
)
```

### Prompt Examples by Type

**Theme Generation:**
- `"modern tech startup with bright cyan and coral colors"`
- `"professional corporate theme with navy blue accents and serif font"`
- `"minimalist design with monochrome palette and clean sans-serif"`

**Cycle Diagrams:**
- `"Show a customer journey: Discover, Try, Buy, Love"`
- `"Marketing funnel: Awareness, Interest, Consideration, Purchase"`
- `"Product development: Research, Design, Build, Launch"`

**Comparison Diagrams:**
- `"Compare manual design vs template-based approach"`
- `"Before: Slow and inconsistent. After: Fast and consistent"`
- `"Traditional vs modern workflow comparison"`

**Timeline Diagrams:**
- `"Product milestones: Q1 Launch, Q2 Growth, Q3 Scale, Q4 Mature"`
- `"Company history: Founded 2020, Series A 2022, IPO 2025"`

### Best Practices

1. **Be Specific** - Include colors, style, mood, and context
   - ✅ `"modern tech startup with bright cyan primary color, coral accents"`
   - ❌ `"tech startup theme"`

2. **Include Context** - Mention industry, audience, or use case
   - ✅ `"professional corporate theme for financial services"`
   - ❌ `"corporate theme"`

3. **Iterate and Refine** - Start broad, then refine based on results
   - First: `"tech startup theme"`
   - Refined: `"modern tech startup with bright cyan and coral, bold sans-serif"`

4. **Combine Approaches** - Use prompts for exploration, structured data for precision
   ```python
   # Generate theme from prompt
   scheme = generate_scheme_from_prompt("...")
   
   # Use structured data for precise diagram
   html = generator.generate_cycle_diagram([
       {'text': 'Step 1', 'color': 'blue'},
       {'text': 'Step 2', 'color': 'green'}
   ])
   
   # Apply theme to structured diagram
   html = scheme.apply_to_html(html)
   ```

### Code Examples

**Generate Theme from Prompt:**
```python
from modern_graphics import generate_scheme_from_prompt

scheme = generate_scheme_from_prompt(
    "modern tech startup with bright cyan and coral colors, bold sans-serif font"
)

# Save for reuse
scheme.save_to_json("my_theme.json")
```

**Generate Diagram from Prompt:**
```python
from modern_graphics import generate_cycle_diagram_from_prompt

html = generate_cycle_diagram_from_prompt(
    generator,
    prompt="Show a customer journey: Discover, Try, Buy, Love"
)

generator.export_to_png(html, Path('customer-journey.png'))
```

**Combine Prompt + Structured Data:**
```python
# Generate theme from prompt
scheme = generate_scheme_from_prompt("corporate professional theme")

# Create diagram with structured data
html = generator.generate_cycle_diagram([
    {'text': 'Plan', 'color': 'blue'},
    {'text': 'Build', 'color': 'green'},
    {'text': 'Deploy', 'color': 'orange'}
])

# Apply theme
html = scheme.apply_to_html(html)
```

### Learn More

- **[Prompts Guide](docs/PROMPTS.md)** - Complete prompt-based generation guide
- **[Use Cases](docs/USE_CASES.md)** - Real-world prompt examples and patterns
- **[Prompt Examples](docs/PROMPT_EXAMPLES.md)** - More creative prompt examples

## Customization Guide

Create custom themes and apply consistent branding across all your graphics.

### Create Custom Themes

#### From Prompt (AI-powered) - Recommended

```python
from modern_graphics import generate_scheme_from_prompt

# Describe your brand - get complete color scheme + font
scheme = generate_scheme_from_prompt(
    "modern tech startup with bright cyan and coral colors, bold sans-serif font"
)

# Apply to any graphic
html = generator.generate_modern_hero(...)
html = scheme.apply_to_html(html)  # Colors + fonts applied automatically
```

#### Manual Creation

```python
from modern_graphics import create_custom_scheme

scheme = create_custom_scheme(
    name="My Brand",
    primary="#8B5CF6",  # Your brand color
    google_font_name="Roboto",  # Google Font
    font_style="sans-serif"
)

# Save and share
scheme.save_to_json("my_theme.json")
```

#### Use Predefined Schemes

```python
from modern_graphics import CORPORATE_SCHEME, DARK_SCHEME, WARM_SCHEME

html = CORPORATE_SCHEME.apply_to_html(generated_html)
```

### Apply Themes

```python
# Generate a graphic
html = generator.generate_modern_hero(...)

# Apply theme
html = scheme.apply_to_html(html)

# Export
generator.export_to_png(html, Path('output.png'))
```

**See complete example:** [Theme Demo Script](examples/generate_complete_theme_demo.py) | [Theme Demo Gallery (run locally)](examples/output/theme-demo/index.html)

### Advanced Customization

- **[Color Scheme Generator Guide](docs/ADVANCED.md#color-scheme-generator)** - Complete theme creation guide
- **[Custom Templates](docs/ADVANCED.md#custom-templates)** - Create custom templates
- **[SVG.js Integration](docs/ADVANCED.md#svgjs-integration)** - Custom SVG graphics
- **[Advanced Topics](docs/ADVANCED.md)** - All advanced features

## Core Concepts

Understanding these concepts will help you use the library effectively.

### 1. The Generator

The `ModernGraphicsGenerator` is the main class that creates graphics. You create one, then use it to generate different diagram types.

```python
from modern_graphics import ModernGraphicsGenerator, Attribution

generator = ModernGraphicsGenerator(
    title="My Diagram",
    attribution=Attribution()
)

# Generate different diagram types
html = generator.generate_cycle_diagram([...])
html = generator.generate_comparison_diagram(...)
html = generator.generate_timeline_diagram(...)
```

**Learn more:** [Core Concepts Guide](docs/CONCEPTS.md)

### 2. Diagram Types

The library includes 10+ diagram types, each optimized for different use cases.

**Choose the right type:**
- **Process/Flow** → Cycle Diagram
- **Comparison** → Comparison Diagram
- **Timeline** → Timeline Diagram
- **Story/Narrative** → Story Slide
- **List/Grid** → Grid Diagram
- **Hierarchy** → Pyramid Diagram
- **Growth Loop** → Flywheel Diagram

**Learn more:** [Diagram Types Guide](docs/DIAGRAM_TYPES.md)

### 3. Custom Themes

**One theme, all graphics.** Define colors and fonts once, apply consistently across hero slides, slide cards, and diagrams.

**Why Use Themes?**
- **Consistency**: All graphics match your brand automatically
- **Speed**: Apply styles instantly with one line of code
- **Team Alignment**: Share theme JSON files for consistent branding
- **Flexibility**: Switch themes or create variations easily
- **Template = Theme**: We no longer ship a separate “template gallery.” The active color scheme drives typography, card chrome, and hero styling across every diagram (see [theme demo](examples/output/theme-demo/index.html)).

**See it in action:** [Complete Theme Demo (generate locally)](examples/output/theme-demo/index.html) - 7 graphics, one theme

**Learn more:** [Color Scheme Generator Guide](docs/ADVANCED.md#color-scheme-generator)

### 4. Attribution

Attribution adds copyright and context information to your graphics. It appears at the bottom of generated images.

```python
from modern_graphics import Attribution

attribution = Attribution(
    copyright="© My Company 2025",
    context="Q4 Report",
    position="bottom-right"
)
```

**Learn more:** [Core Concepts Guide](docs/CONCEPTS.md#attribution)

## Working Without OpenAI

**Good news:** Most features work **without an OpenAI API key**! You only need OpenAI for prompt-based generation (which is optional).

### What Works Without OpenAI ✅

All structured data generation works without OpenAI:

- ✅ **Cycle diagrams** - `generate_cycle_diagram(steps)`
- ✅ **Comparison diagrams** - `generate_comparison_diagram(left, right)`
- ✅ **Timeline diagrams** - `generate_timeline_diagram(events)`
- ✅ **Story slides** - `generate_story_slide(...)`
- ✅ **Hero slides** - `generate_modern_hero(...)`
- ✅ **CLI commands** - All CLI commands work without OpenAI
- ✅ **PNG export** - Export works without OpenAI
- ✅ **Templates** - Using existing templates works without OpenAI

### What Requires OpenAI ⚠️

Only these **optional** prompt-based features require OpenAI:

- ⚠️ **Prompt-based generation** - `generate_*_from_prompt()` functions
- ⚠️ **AI theme creation** - `generate_scheme_from_prompt()`

**Bottom line:** Use structured data (dictionaries, lists) and you don't need OpenAI. Use prompts (natural language) and you'll need an OpenAI API key.

**Example without OpenAI:**
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
    "badge": "+24% QoQ"
}]

html = generator.generate_slide_card_diagram(cards)
generator.export_to_png(html, Path('output.png'))
```

## Documentation

### Getting Started
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get your first graphic in 5 minutes
- **[Core Concepts](docs/CONCEPTS.md)** - Learn the four essential concepts
- **[Diagram Types Guide](docs/DIAGRAM_TYPES.md)** - Choose the right diagram type

### Guides
- **[Use Cases](docs/USE_CASES.md)** - Real-world examples and patterns
- **[Hero Slides Guide](docs/HERO_SLIDES.md)** - Modern hero slide layouts
- **[Prompts Guide](docs/PROMPTS.md)** - Prompt-based generation
- **[Export Guide](docs/EXPORT.md)** - PNG export options and settings

### Reference
- **[API Reference](docs/API.md)** - Complete API documentation
- **[Advanced Topics](docs/ADVANCED.md)** - SVG.js, custom diagrams, templates
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Examples
- **[Examples Directory](examples/)** - All example scripts organized by category
- **[Showcase Gallery](examples/output/showcase/)** - High-quality examples for documentation

## Installation & Requirements

### Basic Requirements

```bash
pip install playwright pillow python-dotenv
playwright install chromium
```

- Python 3.8+
- Playwright (for PNG export)
- Pillow (for image processing)

### Optional: OpenAI Support

For prompt-based generation:

```bash
pip install openai
```

Set `OPENAI_API_KEY` in your `.env` file:

```bash
OPENAI_API_KEY=your_openai_key_here
```

## Next Steps

**New to the library?**
1. Start with [How Do I Get Started?](#how-do-i-get-started) - Installation + first graphic + first theme
2. Try the [Examples Directory](examples/) - See working code
3. Browse the [Showcase Gallery](examples/output/showcase/) - See what's possible

**Want to customize?**
1. **Create [Custom Themes](docs/ADVANCED.md#color-scheme-generator)** - Define colors and fonts once, apply everywhere
   - See [Complete Theme Demo](examples/output/theme-demo/index.html) (generate locally) for inspiration
   - Try [Theme Demo Script](examples/generate_complete_theme_demo.py)
2. Learn about [Templates](docs/ADVANCED.md#custom-templates)
3. Check out [Advanced Topics](docs/ADVANCED.md)

**Want to use prompts?**
1. Read [How Do I Prompt Creatively?](#how-do-i-prompt-creatively) - Techniques and examples
2. See [Prompts Guide](docs/PROMPTS.md) - Complete guide
3. Check [Use Cases](docs/USE_CASES.md) - Real-world patterns

**Need help?**
1. Check [Troubleshooting](docs/TROUBLESHOOTING.md)
2. Review [Examples Directory](examples/)
3. See [Use Cases](docs/USE_CASES.md) for patterns

## License

MIT

## Contributing

Contributions welcome! The system is designed to be extensible:
- Add new diagram types by implementing `DiagramGenerator`
- Add new templates using `TemplateBuilder`
- Submit PRs for improvements

See [Contributing Guide](docs/CONTRIBUTING.md) for more details.
