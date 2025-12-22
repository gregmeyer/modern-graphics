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
