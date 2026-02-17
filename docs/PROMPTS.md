# Prompt Workflows (Canonical)

Use this page as the single source of truth for prompt-based generation.

## What Requires OpenAI

Prompt workflows require `OPENAI_API_KEY`.

```bash
export OPENAI_API_KEY=your_key
```

Non-prompt `create` and structured-data workflows still work without OpenAI.

## Fast Start

```python
from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics import generate_cycle_diagram_from_prompt
from pathlib import Path

generator = ModernGraphicsGenerator("Prompt Demo", Attribution())
html = generate_cycle_diagram_from_prompt(generator)
generator.export_to_png(html, Path("prompt-cycle.png"))
```

## Prompt APIs

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
)
```

Use default prompts:

```python
html = generate_timeline_diagram_from_prompt(generator)
```

Use custom prompts:

```python
html = generate_timeline_diagram_from_prompt(
    generator,
    prompt="Show milestones: Q1 baseline, Q2 adoption, Q3 optimization, Q4 scale"
)
```

Inspect defaults:

```python
from modern_graphics.prompt_to_diagram import DEFAULT_DIAGRAM_PROMPTS
print(DEFAULT_DIAGRAM_PROMPTS["cycle"])
```

## CLI Prompt Workflows

### 1) Ideas Interview

```bash
modern-graphics ideas
modern-graphics ideas --name cy-graphic --save-dir ./my_prompts
modern-graphics ideas --no-save
```

Builds a single reusable prompt from a guided interview and saves it under `./prompt_versions` by default.

### 2) Generate From Prompt File

```bash
modern-graphics from-prompt-file raw/cy-example/cy-graphic-prompt-revised.md
modern-graphics from-prompt-file path/to/prompt.md --output-dir path/to/graphics
```

### 3) Hero From Prompt JSON

```bash
modern-graphics modern-hero-prompt \
  --prompt-file hero_prompt.json \
  --output hero-from-prompt.png --png
```

## Practical Prompt Checklist

Use this before running prompt generation:

1. State the graphic type (`cycle`, `comparison`, `timeline`, `hero`, `insight-story`).
2. Include explicit entities/stages and sequence order.
3. Specify outcome framing (what changed, over what period, why it matters).
4. Add visual constraints (tone, emphasis, density expectations).
5. Keep language concrete; avoid vague style-only prompts.

## Top Prompt Patterns (Copy/Adapt)

- Cycle:
  - `Show a product delivery loop: Discover, Build, Validate, Scale.`
- Comparison:
  - `Compare manual release process vs automated release pipeline.`
- Timeline:
  - `Show quarterly milestones from pilot through scale.`
- Grid:
  - `Show top 5 operating priorities ranked by impact.`
- Flywheel:
  - `Show growth loop: acquire, activate, retain, refer.`
- Slide cards:
  - `Three cards: current constraint, decision gate, expected outcome.`
- Slide comparison:
  - `Before: high motion/low relevance; After: fewer launches/higher relevance.`
- Story slide:
  - `What changed, when it changed, and why the shift matters now.`
- Insight card:
  - `Single sharp insight with one supporting visual and decision implication.`
- Hero:
  - `Executive opener with one thesis, three proof points, and a clear operating move.`

## PB&J Example (Ideas Output)

```python
from modern_graphics.prompts import EXAMPLE_ANSWERS_PBJ, EXAMPLE_PROMPT_PBJ
print(EXAMPLE_PROMPT_PBJ)
```

## Related Docs

- Mermaid integration: [MERMAID.md](MERMAID.md)
- Create command: [CREATE_COMMAND.md](CREATE_COMMAND.md)
- API signatures: [API.md](API.md)
- Troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
