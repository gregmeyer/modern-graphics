# Phase 4 Merge Readiness (Checkpoint)

## Scope completed in this slice
- Deterministic export/crop behavior refactor in `modern_graphics/export.py`.
- Phase 4 helper-level smoke coverage in `tests/smoke/test_export_phase4_smoke.py`.
- Validator guardrails extended in `scripts/validate_overhaul_phase1.py`.
- Overhaul status update in `docs/OVERHAUL_SPEC.md`.

## What changed
- Replaced branch-heavy layout-specific crop logic with a unified path:
  - normalize crop mode: `none | safe | tight`.
  - detect content bounds via preferred root selectors, fallback to meaningful content nodes.
  - apply one crop-box calculation and image-bounds clamp.
- Preserved existing policy defaults (`safe` + minimal padding behavior via resolved padding).

## Validation results
- `python3 -m py_compile modern_graphics/export.py scripts/validate_overhaul_phase1.py tests/smoke/test_export_phase4_smoke.py` ✅
- `python3 scripts/validate_overhaul_phase1.py` ✅
- `python3 scripts/run_phase1_quality_harness.py` ✅ (reports regenerated)
- `python3 -m pytest -q tests/smoke/test_export_phase4_smoke.py` ⚠️ not runnable in this environment (`pytest` unavailable)

## Merge readiness
- Code compiles: **Yes**
- Baseline validator passes: **Yes**
- Harness reports regenerate cleanly: **Yes**
- Dedicated smoke test file present: **Yes**
- Full pytest execution in local CI/runtime: **Pending environment dependency**

## Recommended next slice
1. Add doc consolidation for export behavior (`docs/EXPORT.md` + create guide cross-links) with explicit crop examples.
2. Add deterministic fixture corpus for known gutter/miscrop regressions (hero + insight-card + timeline).
3. Run smoke tests in CI/runtime with `pytest` available and gate merges on Phase 4 tests.
