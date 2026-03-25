# Scripts Directory

Internal tooling, CI validation, and asset generation scripts. **Not user-facing examples** — for runnable demos, see [examples/](../examples/).

## What's here

### CI and Validation
- `check_create_default_refs.py` — feature flag validation (used in CI)
- `check_docs_drift.py` — docs link and heading guard (used in CI)
- `validate_overhaul_phase1.py` — Phase 1 scaffold validator (used in CI)
- `run_phase1_quality_harness.py` — quality token debt scan

### Asset Generation
- `run_showcase.py` — regenerate showcase PNGs for README
- `generate_cli_layout_showcase.py` — generate CLI layout showcase
- `generate_readme_create_examples.py` — generate README preview graphics
- `run_export_fixture_harness.py` — deterministic export fixtures
- `run_insight_fixture_harness.py` — deterministic insight fixtures

### Shared Utilities
- `prompt_storage.py` — prompt storage class (imported by example use-case scripts)
- `aggregate_prompts.py` — prompt collection for evaluation
- `run_all_use_cases.py` — batch runner for all use-case examples

### Prompt Utilities (`prompts/`)
- `prompt_library.py` — programmatic prompt library
- `prompt_builder.py` — interactive prompt builder
- `run_showcase.py` — showcase with prompts
- `test_prompts.py` — prompt pattern testing

## Running

All scripts run from the project root:

```bash
python scripts/run_showcase.py
python scripts/check_docs_drift.py
```

## Local Smoke Tests

```bash
python3 -m venv /tmp/mg-pytest-venv
/tmp/mg-pytest-venv/bin/pip install pytest
/tmp/mg-pytest-venv/bin/python -m pytest tests/smoke -q
```

Or use Docker: `make test`
