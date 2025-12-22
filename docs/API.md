# API Reference

Complete API documentation for Modern Graphics Generator.

## ModernGraphicsGenerator

Main generator class for creating graphics.

```python
generator = ModernGraphicsGenerator(
    title: str,
    template: Optional[StyleTemplate] = None,
    attribution: Optional[Attribution] = None,
    use_svg_js: bool = False
)
```

### Diagram Generation Methods

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
  - Each card dict can include: `title`, `tagline`, `subtext`, `color`, `features`, `badge`, `custom_mockup`
  - `custom_mockup`: Optional SVG string or SVG.js code (requires `use_svg_js=True`)
- `generate_slide_card_comparison(left_card, right_card)` - Generate slide card comparison
  - Same card structure as `generate_slide_card_diagram`
- `generate_modern_hero(...)` - Generate modern hero slide (see [Hero Slides Guide](HERO_SLIDES.md))
- `generate_modern_hero_triptych(...)` - Generate triptych hero slide (see [Hero Slides Guide](HERO_SLIDES.md))

### Prompt-Based Generation Methods

- `generate_cycle_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate cycle from prompt
- `generate_comparison_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate comparison from prompt
- `generate_timeline_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate timeline from prompt
- `generate_grid_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate grid from prompt
- `generate_flywheel_diagram_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate flywheel from prompt
- `generate_slide_cards_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate slide cards from prompt
- `generate_slide_card_comparison_from_prompt(generator, prompt=None, model='gpt-4-turbo-preview')` - Generate slide card comparison from prompt

All prompt-based methods use default prompts if `prompt=None`. See `DEFAULT_DIAGRAM_PROMPTS` for available defaults.

### Export Methods

- `save(html_content, output_path)` - Save HTML to file
- `export_to_png(html_content, output_path, viewport_width=2400, viewport_height=1600, device_scale_factor=2, padding=20, temp_html_path=None)` - Export to PNG

See [Export Guide](EXPORT.md) for detailed export options.

## Convenience Functions

For quick generation without creating a generator instance:

```python
from modern_graphics import (
    generate_cycle_diagram,
    generate_comparison_diagram,
    generate_timeline_diagram,
    generate_story_slide,
    generate_grid_diagram,
    generate_flywheel_diagram,
    generate_pyramid_diagram,
    generate_before_after_diagram,
    generate_funnel_diagram,
    generate_slide_card_diagram,
    generate_slide_card_comparison,
)

# Generate HTML directly
html = generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'}
])
```

## Prompt-Based Functions

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

See [Prompts Guide](PROMPTS.md) for detailed prompt documentation.

## Attribution

```python
from modern_graphics import Attribution

attribution = Attribution(
    copyright: str = "© Greg Meyer 2025 • gregmeyer.com",
    context: Optional[str] = None,
    position: str = "bottom-right",
    show: bool = True,
    font_size: str = "12px",
    font_color: str = "#666666",
    font_weight: str = "400",
    background_color: Optional[str] = None,
    opacity: float = 1.0,
    padding: str = "8px 12px",
    border_radius: str = "4px",
    margin_top: int = 20
)
```

## TemplateBuilder

```python
from modern_graphics import TemplateBuilder

template = (TemplateBuilder("template_name")
    .add_color(name, gradient, shadow)
    .set_base_styles(css)
    .set_attribution_styles(css)
    .set_font_family(font_stack)
    .set_background_color(color)
    .copy_from(existing_template)
    .build())
```

See [Advanced Topics](ADVANCED.md) for detailed template creation.
