# File Categorization for Examples Directory Cleanup

## Files to MOVE to `scripts/` (Utility/Maintenance Scripts)

These are scripts used for maintenance, testing, or aggregation - not examples:

1. **`generate_showcase.py`** - Generates showcase examples for README (maintenance script)
   - Used to regenerate showcase graphics
   - Not an example, but a build/maintenance tool

2. **`aggregate_prompts.py`** - Aggregates prompts from all use cases for evaluation
   - Utility script for collecting evaluation data
   - Not demonstrating library usage

3. **`model_comparison_test.py`** - Test script comparing outputs across models
   - Testing/validation script
   - Not an example of library usage

## Files to KEEP in `examples/` (Example/Demo Scripts)

These demonstrate library features and usage:

### Basic Examples (No AI Required)
- `all_diagram_types.py` - Shows all diagram types
- `attribution_examples.py` - Shows attribution features
- `attribution_customization.py` - Shows attribution customization
- `batch_generation.py` - Shows batch generation pattern
- `combo_chart_example.py` - Shows combo charts
- `custom_diagram.py` - Shows custom diagram creation
- `custom_template.py` - Shows custom template creation
- `export_options.py` - Shows export options

### AI-Assisted Examples (Require OpenAI API Key)
- `ai_assisted_template.py` - Shows AI template creation
- `interactive_template_creation.py` - Shows interactive template creation
- `interview_with_prompt_example.py` - Shows interview with prompts
- `story_slide_with_prompt.py` - Shows story slides with prompts
- `temperature_effects_demo.py` - Shows temperature effects on generation

### Use Case Examples
- `use_case_tech_startup.py` - Tech startup use case
- `use_case_corporate.py` - Corporate use case
- `use_case_creative.py` - Creative use case
- `use_case_healthcare.py` - Healthcare use case
- `use_case_education.py` - Education use case
- `run_all_use_cases.py` - Runs all use cases (could stay or move to scripts/)

## Files to CONSIDER Moving (Shared Utilities)

These are imported by example files, so moving requires updating imports:

1. **`prompt_storage.py`** - Utility class for prompt storage
   - Imported by: `generate_showcase.py`, all `use_case_*.py`, `temperature_effects_demo.py`, `aggregate_prompts.py`
   - Options:
     - Keep in `examples/` (simplest)
     - Move to `scripts/` and update imports
     - Move to `modern_graphics/utils/` if it becomes part of core library

## Subdirectory: `examples/prompts/`

These are prompt management utilities:

- `prompt_builder.py` - Builds prompts programmatically
- `prompt_library.py` - Library of prompts
- `test_prompts.py` - Tests prompts
- `generate_showcase.py` - (duplicate? check if different from root one)

**Recommendation:** Move entire `prompts/` subdirectory to `scripts/prompts/` since these are utilities, not examples.

## Summary

**Move to `scripts/`:**
- `generate_showcase.py`
- `aggregate_prompts.py`
- `model_comparison_test.py`
- `prompts/` directory (entire subdirectory)

**Keep in `examples/`:**
- All `*_example.py` files
- All `use_case_*.py` files
- `prompt_storage.py` (unless moved to core library)
- `run_all_use_cases.py` (borderline - could go either way)

**Note:** If `prompt_storage.py` is moved, update imports in:
- `generate_showcase.py` (if it moves to scripts)
- All `use_case_*.py` files
- `temperature_effects_demo.py`
- `aggregate_prompts.py` (if it moves to scripts)
