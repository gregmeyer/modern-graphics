# Scripts Directory

This directory contains utility scripts and advanced examples for the Modern Graphics library.

## Structure

- **Utility Scripts** - Maintenance, testing, and helper scripts
- **Example Scripts** - Advanced examples (see [Examples Directory](../examples/) for organized examples)
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

### Utility Scripts

**Maintenance and helper scripts:**

- **`run_showcase.py`** - Generate showcase examples for README
  - Regenerates all showcase graphics in `examples/output/showcase/`
  - Used for documentation and examples gallery

- **`aggregate_prompts.py`** - Aggregate prompts for evaluation
  - Collects prompts from all use case scripts
  - Utility for prompt analysis and evaluation

- **`model_comparison_test.py`** - Compare model outputs
  - Tests different OpenAI models side-by-side
  - Useful for model selection and quality comparison

- **`prompt_storage.py`** - Prompt storage utility
  - Shared utility class for prompt storage
  - Imported by example scripts

### Example Scripts

**Note:** For organized examples by category, see **[Examples Directory](../examples/)**.

These scripts demonstrate library features:

- **Basic Examples** (No AI): `all_diagram_types.py`, `attribution_examples.py`, `export_options.py`, etc.
- **AI Examples** (Require OpenAI): `ai_assisted_template.py`, `story_slide_with_prompt.py`, etc.
- **Use Cases** (Require OpenAI): `use_case_*.py`, `run_all_use_cases.py`

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

## Local Smoke Tests (No Repo Bloat)

If `pytest` is unavailable in your system Python, use a temporary virtualenv:

```bash
python3 -m venv /tmp/mg-pytest-venv
/tmp/mg-pytest-venv/bin/pip install pytest
cd /path/to/modern-graphics
/tmp/mg-pytest-venv/bin/python -m pytest tests/smoke -q
```

This keeps test tooling out of the repo and avoids committing generated artifacts.

## Path References

All scripts use relative paths from the project root:
- Outputs go to `examples/output/` (not `scripts/output/`)
- Scripts add parent directory to `sys.path` for imports
