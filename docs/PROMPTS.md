# Prompt-Based Generation

Generate diagrams from natural language prompts using AI. All diagram types support prompt-based generation with default prompts that work out of the box.

## Basic Usage

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

## Available Prompt Functions

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

## When to Use Prompts vs Hardcoded Data

- **Use Prompts**: When you want AI to interpret natural language and extract structure
- **Use Hardcoded Data**: When you have exact data structures and want precise control

Both approaches work - choose based on your needs!

## Requirements

Prompt-based generation requires `OPENAI_API_KEY` in your `.env` file:

```bash
OPENAI_API_KEY=your_openai_key_here
```

## Default Prompts

Each diagram type has a default prompt that works automatically. View them:

```python
from modern_graphics.prompt_to_diagram import DEFAULT_DIAGRAM_PROMPTS

print(DEFAULT_DIAGRAM_PROMPTS['cycle'])
print(DEFAULT_DIAGRAM_PROMPTS['comparison'])
print(DEFAULT_DIAGRAM_PROMPTS['timeline'])
# ... etc
```

## Custom Prompts

Provide your own prompt for more control:

```python
html = generate_cycle_diagram_from_prompt(
    generator,
    prompt="Show a customer journey: Discover (blue), Try (green), Buy (purple), Love (orange)"
)
```

## Prompt Examples

### Cycle Diagram
```
Show a software development cycle with 4 steps: Plan (blue), Build (green), Test (orange), Deploy (purple)
```

### Comparison Diagram
```
Compare Manual Design Approach vs Automated Generation Approach. 
Manual Approach: Slow, Inconsistent, Time-consuming, Hard to update
Automated Approach: Fast, Consistent, Efficient, Easy to update
```

### Timeline Diagram
```
Show a product launch timeline from Q1 2024 to Q4 2024 with 4 key milestones:
Q1: Planning and Research (blue)
Q2: Development (green)
Q3: Testing and Refinement (orange)
Q4: Launch (purple)
```

### Story Slide
```
What changed: Revenue model shifted from upfront licenses to subscriptions
Time period: Q2-Q4 2025
What it means: Predictable revenue and 20% higher retention
```

See [Prompt Best Practices](PROMPT_BEST_PRACTICES.md) and [Prompt Examples](PROMPT_EXAMPLES.md) for more guidance.

## Graphic ideas interview ("I need some ideas")

When you need ideas for a hero or insight-story graphic, run the **ideas** interview. It asks you for format, subject, theme, narrative, before/after panels, layout constraints, and outputs, then builds a single prompt and stores it.

**CLI:**

```bash
modern-graphics ideas
```

- Saves a prompt version under `./prompt_versions/` (or `MODERN_GRAPHICS_PROMPTS_DIR`).
- Use `--name my-graphic` to name the file (e.g. `graphic_prompt_my-graphic.md`).
- Use `--save-dir ./my_prompts` to choose the directory.
- Use `--no-save` to only print the prompt without saving.

**Python:**

```python
from modern_graphics import run_graphic_ideas_interview
from pathlib import Path

result = run_graphic_ideas_interview(
    save_dir=Path("./prompt_versions"),
    prompt_name="my-graphic",
    skip_save=False,
)
# result["prompt_text"] — built prompt
# result["saved_path"] — path to saved file, or None
```

The interview uses a generic checklist (format, subject, theme, narrative, before/after, layout, outputs). Use the saved prompt when briefing a human or model to generate the graphic.

**Example built prompt (peanut butter and jelly sandwich-making process):**

```python
from modern_graphics.prompts import EXAMPLE_ANSWERS_PBJ, EXAMPLE_PROMPT_PBJ

# EXAMPLE_ANSWERS_PBJ is the filled-in checklist (format, subject, theme, etc.)
# EXAMPLE_PROMPT_PBJ is the single paragraph built from it:
print(EXAMPLE_PROMPT_PBJ)
```

Output:

```
Make a insight-story graphic for peanut butter and jelly sandwich-making process with theme/mood: warm, kitchen-friendly; browns, reds, cream. Narrative: From chaos to lunch: three steps, one sandwich. Key insight: The best PB&J is the one you actually make. Before panel: kitchen chaos: bread everywhere, jars scattered, knife in the wrong place. After panel: Spread peanut butter → Add jelly → Close and slice. Done. Layout: horizontal flow, same baseline for arrows; no post-its; small sandwich icon on the right. Outputs: docs/lunch-graphics/, HTML + PNG, generate_pbj_hero.py.
```
