# Phase 4 Merge Readiness (Checkpoint)

## Scope completed in this slice
- Deterministic export/crop behavior refactor in `modern_graphics/export.py`.
- Phase 4 helper-level smoke coverage in `tests/smoke/test_export_phase4_smoke.py`.
- Deterministic export fixture corpus + snapshots for key layouts.
- Export docs consolidation and create-guide cross-link updates.
- Overhaul status update in `docs/OVERHAUL_SPEC.md`.

## What changed
- Replaced branch-heavy layout-specific crop logic with a unified path:
  - normalize crop mode: `none | safe | tight`
  - detect content bounds via preferred root selectors, then fallback nodes
  - apply one crop-box calculation with bounds clamp
- Added export fixture harness for regression coverage:
  - fixtures: `tests/smoke/fixtures_export_phase4.json`
  - snapshots: `reports/export-fixtures/*.html`
  - report: `reports/phase4-export-fixtures.md`
- Updated docs:
  - `docs/EXPORT.md` rewritten with deterministic mode semantics and examples
  - `docs/CREATE_COMMAND.md` now links to export guide for PNG behavior

## Validation results
- `python3 -m py_compile modern_graphics/export.py scripts/run_export_fixture_harness.py scripts/run_phase1_quality_harness.py scripts/validate_overhaul_phase1.py tests/smoke/test_export_phase4_smoke.py` ✅
- `python3 scripts/run_export_fixture_harness.py` ✅
- `python3 scripts/run_phase1_quality_harness.py` ✅
- `python3 scripts/validate_overhaul_phase1.py` ✅
- `python3 -m pytest -q tests/smoke/test_export_phase4_smoke.py` ⚠️ not runnable in this environment (`pytest` unavailable)

## Merge readiness
- Deterministic crop implementation: **Ready**
- Export fixture corpus present: **Ready**
- Harness integration complete: **Ready**
- Docs reflect current behavior: **Ready**
- CI/runtime pytest execution: **Pending environment dependency**

## Recommended next slice
1. Add CI gate that runs export smoke tests where `pytest` is available.
2. Optionally add PNG artifact smoke for one fixture per layout family in a controlled environment.
3. Move to Phase 5 migration/adoption tasks.
