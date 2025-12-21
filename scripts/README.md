# Scripts Directory

This directory contains all example and utility scripts for the Modern Graphics library.

## Structure

- **Example Scripts** - Demonstrate library features and usage
- **Utility Scripts** - Maintenance and helper scripts
- **`prompts/`** - Prompt management utilities

## Running Scripts

All scripts should be run from the project root:

```bash
# Example: Generate showcase
python scripts/run_showcase.py

# Example: Run all diagram types
python scripts/all_diagram_types.py

# Example: Run use cases
python scripts/run_all_use_cases.py
```

## Output Locations

- **Showcase outputs**: `examples/output/showcase/` (tracked in git)
- **Generated outputs**: `examples/output/generated/` (gitignored)

All scripts automatically create output directories as needed.

## Script Categories

### Example Scripts (No AI Required)
- `all_diagram_types.py` - Generate all diagram types
- `attribution_examples.py` - Attribution examples
- `attribution_customization.py` - Attribution customization
- `batch_generation.py` - Batch generation examples
- `combo_chart_example.py` - Combo chart examples
- `custom_diagram.py` - Custom diagram examples
- `custom_template.py` - Custom template examples
- `export_options.py` - Export options examples

### AI-Assisted Examples (Require OpenAI API Key)
- `ai_assisted_template.py` - AI template creation
- `interactive_template_creation.py` - Interactive template creation
- `interview_with_prompt_example.py` - Interview with prompts
- `story_slide_with_prompt.py` - Story slides with prompts
- `temperature_effects_demo.py` - Temperature effects demo

### Use Case Examples (Require OpenAI API Key)
- `use_case_corporate.py` - Corporate use case
- `use_case_creative.py` - Creative use case
- `use_case_education.py` - Education use case
- `use_case_healthcare.py` - Healthcare use case
- `use_case_tech_startup.py` - Tech startup use case
- `run_all_use_cases.py` - Run all use cases

### Utility Scripts
- `run_showcase.py` - Generate showcase examples for README
- `aggregate_prompts.py` - Aggregate prompts for evaluation
- `model_comparison_test.py` - Compare model outputs
- `prompt_storage.py` - Prompt storage utility (imported by other scripts)

### Prompt Utilities (`prompts/` subdirectory)
- `prompt_builder.py` - Build prompts programmatically
- `prompt_library.py` - Library of prompts
- `test_prompts.py` - Test prompts
- `run_showcase.py` - Generate showcase with prompts

## Dependencies

Most scripts require:
- `modern_graphics` package (imported from parent directory)
- `prompt_storage` module (in same directory)

AI-assisted scripts require:
- `OPENAI_API_KEY` environment variable

## Path References

All scripts use relative paths from the project root:
- Outputs go to `examples/output/` (not `scripts/output/`)
- Scripts add parent directory to `sys.path` for imports
