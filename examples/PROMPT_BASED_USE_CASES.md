# Prompt-Based Use Cases

All use case examples now use sophisticated prompts with the unified story slide generator. Prompts are automatically stored for evaluation purposes.

## Overview

Each use case example:
1. Uses `generate_unified_story_slide()` with detailed prompts
2. Stores prompts with metadata in `prompts_used.json`
3. Saves prompts alongside generated images for evaluation

## Prompt Storage

Prompts are stored in JSON format with the following structure:

```json
{
  "total_prompts": 4,
  "generated_at": "2025-01-XX...",
  "prompts": [
    {
      "timestamp": "2025-01-XX...",
      "prompt": "Full prompt text...",
      "output_file": "relative/path/to/image.png",
      "use_case": "tech_startup",
      "slide_type": "story_slide",
      "metadata": {
        "slide_number": 1,
        "title": "Product Vision"
      }
    }
  ]
}
```

## Use Cases

### Tech Startup (`use_case_tech_startup.py`)
- Product vision transformation
- Growth metrics and efficiency improvements
- Revenue vs user growth (combo chart example)

### Corporate (`use_case_corporate.py`)
- Quarterly performance reports
- Financial metrics and growth trends
- Professional business presentations

### Education (`use_case_education.py`)
- Student progress tracking
- Learning outcomes and completion rates
- Course effectiveness metrics

### Healthcare (`use_case_healthcare.py`)
- Clinical research findings
- Treatment outcomes and patient recovery
- Medical study results

### Creative (`use_case_creative.py`)
- Portfolio growth and client impact
- Creative project metrics
- Design agency performance

## Aggregating Prompts

To collect all prompts from all use cases for evaluation:

```bash
python scripts/aggregate_prompts.py
```

This creates `examples/output/generated/use_cases/all_prompts.json` with all prompts from all use cases.

## Evaluation

The stored prompts can be used for evaluation by:
1. Loading `prompts_used.json` from each use case directory
2. Or loading `all_prompts.json` for all use cases at once
3. Pairing prompts with their generated images
4. Sending to evaluation system with prompt + image pairs

## Prompt Best Practices

Good prompts for story slides:
- Describe the data/story clearly
- Include specific metrics and numbers
- Mention time periods and trends
- Request visualization type (single or combo)
- Include context about what the visualization should show

Example:
```
Show how ocean temperatures have risen dramatically over the past decade.
The data shows a steady increase from 2014 to 2024, with temperatures 
rising from 20°C to 24°C. This represents a critical climate change 
indicator that affects marine ecosystems globally.
```

## Running Use Cases

Run individual use case:
```bash
python scripts/use_case_tech_startup.py
```

Run all use cases:
```bash
python scripts/run_all_use_cases.py
```

All prompts will be automatically stored in their respective directories.
