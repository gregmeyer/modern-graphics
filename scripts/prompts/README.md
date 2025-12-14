# Prompt Tools

Interactive tools for building and testing prompts for AI-assisted template creation.

## Tools

### prompt_builder.py
Interactive questionnaire to build effective prompts step-by-step.

```bash
python scripts/prompts/prompt_builder.py
```

Asks questions about:
- Use case
- Style preferences
- Colors
- Fonts
- Mood/tone

Then generates an optimized prompt and optionally creates a template.

### test_prompts.py
Test suite for various prompt patterns. Generates templates from test prompts and creates comparison outputs.

```bash
python scripts/prompts/test_prompts.py
```

Tests prompts from different categories:
- Minimalist
- Bold
- Professional
- Dark
- Light
- Creative
- Style references

### generate_showcase.py
Generates high-quality showcase graphics for the README demonstrating different templates and styles.

```bash
python scripts/prompts/generate_showcase.py
```

Creates:
- Individual template showcases (cycle, comparison, story_slide)
- Template comparison (same diagram, different styles)

Outputs saved to `examples/output/showcase/`

### prompt_library.py
Programmatic access to categorized prompt collections.

```python
from examples.prompts.prompt_library import (
    get_prompts_by_category,
    get_style_reference_prompt,
    get_industry_prompt,
    list_all_prompts
)

# Get prompts by category
minimalist_prompts = get_prompts_by_category("minimalist")

# Get style reference
apple_prompt = get_style_reference_prompt("apple")

# Get industry prompt
tech_prompt = get_industry_prompt("tech_startup")
```

## Requirements

All tools require:
- OpenAI API key in `.env` file
- `openai` package installed: `pip install -e ".[ai]"`

## Output Locations

- **Test outputs**: `examples/output/prompt_tests/`
- **Showcase graphics**: `examples/output/showcase/`
