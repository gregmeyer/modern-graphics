# Examples Directory

This directory contains example scripts organized by category to help you learn and explore the Modern Graphics library.

## Quick Start

### No AI Required (Start Here)

These examples work immediately without any API keys:

```bash
# Generate all diagram types
python scripts/all_diagram_types.py

# See attribution options
python scripts/attribution_examples.py

# Learn export options
python scripts/export_options.py
```

### With AI (Requires OpenAI API Key)

These examples use AI-powered prompt-based generation:

```bash
# Generate use case examples
python scripts/run_all_use_cases.py

# Try AI template creation
python scripts/ai_assisted_template.py
```

## Example Categories

### 📚 Basic Examples

**No AI required** - Learn core features with structured data:

- **`all_diagram_types.py`** - Generate all 10+ diagram types
  - Output: `examples/output/generated/01_cycle.png` through `12_slide_comparison.png`
  - Shows: Cycle, comparison, timeline, story slide, grid, flywheel, slide cards, and more

- **`attribution_examples.py`** - Attribution customization
  - Output: `examples/output/generated/attribution_*.png`
  - Shows: Default, custom styled, with context, disabled

- **`attribution_customization.py`** - Advanced attribution options
  - Output: `examples/output/generated/attribution_custom/*.png`
  - Shows: All customization options (position, colors, fonts, padding, etc.)

- **`export_options.py`** - PNG export quality and settings
  - Output: `examples/output/generated/export_*.png`
  - Shows: Different resolutions, scale factors, padding options

- **`batch_generation.py`** - Generate multiple graphics efficiently
  - Output: `examples/output/generated/product_cycle.png`, `feature_comparison.png`, `project_timeline.png`
  - Shows: Batch processing patterns

- **`custom_template.py`** - Create and use custom templates
  - Output: `examples/output/generated/custom_template_*.png`
  - Shows: TemplateBuilder usage, color palettes, custom styles

- **`custom_diagram.py`** - Create custom diagram types
  - Output: `examples/output/generated/custom_diagram.png`
  - Shows: Extending the system with custom diagrams

- **`combo_chart_example.py`** - Combined chart visualizations
  - Output: `examples/output/generated/combo_chart.png`
  - Shows: Multiple chart types in one graphic

### 🤖 AI-Assisted Examples

**Require OpenAI API Key** - Explore prompt-based generation:

- **`ai_assisted_template.py`** - Generate templates from descriptions
  - Shows: `quick_template_from_description()` usage
  - Example: "dark professional theme with blue accents"

- **`interactive_template_creation.py`** - Interactive template builder
  - Shows: `interview_for_template()` conversational interface

- **`story_slide_with_prompt.py`** - Story slides from natural language
  - Shows: Prompt-based story slide generation

- **`temperature_effects_demo.py`** - Temperature effects on generation
  - Output: `examples/output/generated/temperature_demo/*.png`
  - Shows: How temperature affects AI output consistency

- **`interview_with_prompt_example.py`** - Interview with custom prompts
  - Shows: Combining interview flow with prompt customization

### 🎯 Use Case Examples

**Require OpenAI API Key** - Real-world scenarios:

- **`use_case_tech_startup.py`** - Tech startup pitch deck
  - Output: `examples/output/generated/use_cases/tech_startup/*.png`
  - Shows: Product vision, growth metrics, feature roadmap, team structure

- **`use_case_corporate.py`** - Corporate quarterly reports
  - Output: `examples/output/generated/use_cases/corporate/*.png`
  - Shows: Revenue trends, department comparisons, timeline milestones

- **`use_case_creative.py`** - Creative portfolio showcase
  - Output: `examples/output/generated/use_cases/creative/*.png`
  - Shows: Project timelines, style comparisons, creative process

- **`use_case_healthcare.py`** - Healthcare data visualization
  - Output: `examples/output/generated/use_cases/healthcare/*.png`
  - Shows: Patient journey, treatment comparisons, outcome metrics

- **`use_case_education.py`** - Educational course materials
  - Output: `examples/output/generated/use_cases/education/*.png`
  - Shows: Learning paths, concept comparisons, curriculum timelines

- **`run_all_use_cases.py`** - Run all use cases at once
  - Generates all use case examples in one command

### 🛠️ Advanced Examples

**Explore advanced features:**

- **`svg_js_example.py`** - SVG.js integration
  - Output: `examples/output/generated/svg_js_example.png`
  - Shows: Programmatic SVG generation, custom shapes, animations

- **`model_comparison_test.py`** - Compare AI model outputs
  - Output: `examples/output/generated/model_comparison/*.png`
  - Shows: Different OpenAI models side-by-side

## Output Structure

```
examples/output/
├── showcase/              # Curated examples (tracked in git)
│   ├── diagram-types/     # One example of each type
│   ├── templates/         # Template style examples
│   ├── attribution/       # Attribution examples
│   ├── use-cases/         # Real-world use cases
│   └── hero-slides/       # Modern hero slide layouts
│
└── generated/             # Temporary outputs (gitignored)
    ├── attribution_*.png  # From attribution examples
    ├── export_*.png       # From export options
    ├── use_cases/         # From use case scripts
    └── ...                # Other generated outputs
```

## Running Examples

### From Project Root

All scripts should be run from the project root directory:

```bash
# Basic example
python scripts/all_diagram_types.py

# Use case example
python scripts/use_case_tech_startup.py

# Run all use cases
python scripts/run_all_use_cases.py
```

### Requirements

**Basic Examples:**
- Python 3.8+
- `playwright` and `pillow` installed
- `playwright install chromium` run

**AI Examples:**
- Everything above, plus:
- `OPENAI_API_KEY` in `.env` file
- OpenAI package installed: `pip install openai`

## Viewing Outputs

### Showcase Examples

Showcase examples are tracked in git and can be viewed directly:

```bash
# View diagram types
ls examples/output/showcase/diagram-types/

# View templates
ls examples/output/showcase/templates/

# View hero slides
ls examples/output/showcase/hero-slides/

# Open a specific example (macOS)
open examples/output/showcase/diagram-types/01-cycle.png
open examples/output/showcase/hero-slides/01-open-canvas.png
```

### Generated Examples

Generated examples are in `examples/output/generated/`:

```bash
# List all generated PNGs
find examples/output/generated -name "*.png" -type f

# Count generated graphics
find examples/output/generated -name "*.png" -type f | wc -l

# Open a directory (macOS)
open examples/output/generated/use_cases/tech_startup/
```

## Learning Path

### Beginner

1. Start with `all_diagram_types.py` to see all diagram types
2. Try `attribution_examples.py` to customize attribution
3. Run `export_options.py` to understand PNG export
4. Explore `custom_template.py` to create your own styles

### Intermediate

1. Try `batch_generation.py` for multiple graphics
2. Explore `use_case_tech_startup.py` for real-world patterns
3. Experiment with `ai_assisted_template.py` for AI-powered templates
4. Check out `story_slide_with_prompt.py` for prompt-based generation

### Advanced

1. Create custom diagrams with `custom_diagram.py`
2. Explore SVG.js with `svg_js_example.py`
3. Compare models with `model_comparison_test.py`
4. Build your own use case examples

## Troubleshooting

**Scripts don't run:**
- Make sure you're in the project root directory
- Check that Playwright is installed: `playwright install chromium`
- Verify Python version: `python3 --version` (needs 3.8+)

**AI examples fail:**
- Check `.env` file has `OPENAI_API_KEY`
- Verify OpenAI package: `pip list | grep openai`
- Ensure API key is valid and has credits

**No outputs generated:**
- Check that output directory exists: `ls examples/output/`
- Verify Playwright browser: `playwright install chromium`
- Check script output for error messages

**Low quality exports:**
- This is normal for quick examples
- Use `export_options.py` to see quality options
- Adjust `device_scale_factor` in export calls for higher quality

## Related Documentation

- **[README.md](../README.md)** - Main documentation
- **[Scripts README](../scripts/README.md)** - Utility scripts documentation
- **[GENERATE_EXAMPLES.md](GENERATE_EXAMPLES.md)** - Detailed generation guide
- **[Output README](output/README.md)** - Output directory structure
