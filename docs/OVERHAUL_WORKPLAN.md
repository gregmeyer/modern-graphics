# Overhaul Workplan (Phase 1 Start)

Branch: `feat/overhaul-clarity-system-v1`
Scope: lock visual system + critique gates before rewrite.

## Milestone

Phase 1 done when:
- Token contract exists and token lint runs on core templates.
- Critique gates run against fixture corpus and output machine/human reports.
- Export policy defaults are deterministic (minimal padding by default).
- CLI clarity contract is documented and scaffolded behind a feature flag.
- Documentation gate passes for this phase (`OVERHAUL_SPEC`, `OVERHAUL_WORKPLAN`, `README`, relevant docs).

## Parallel Workstreams

## A) Visual System + Tokens
Owner: TBD
Status: Checkpoint complete (baseline established)

Tasks:
- Create semantic token model (`modern_graphics/visual_system.py`).
- Add token preset definitions for clarity mode.
- Add token-lint helpers for templates/layouts.
- Document token contract in docs.

Outputs:
- Token model + helpers
- Token contract docs
- Token debt baseline reports (`reports/phase1-token-debt.*`)

## B) Critique Gates + Quality Harness
Owner: TBD
Status: Checkpoint complete (baseline established)

Tasks:
- Add gate runner (`modern_graphics/critique_gates.py`).
- Implement baseline checks:
  - min text size
  - max focal points per section
  - contrast threshold
  - whitespace guard
- Define fixture corpus path and report format.

Outputs:
- Gate runner
- JSON report schema + markdown summary helper
- Harness runner script (`scripts/run_phase1_quality_harness.py`)
- Generated baseline reports under `reports/`

## C) CLI Clarity Surface (Scaffold)
Owner: TBD
Status: Checkpoint complete (feature-flagged scaffold)

Tasks:
- Define new command contract (`create` by layout type).
- Add parser scaffolding behind env/feature flag.
- Define compatibility adapter requirements.

Outputs:
- CLI contract doc section
- parser scaffolding (non-breaking)

## D) Export Determinism + Policy
Owner: TBD
Status: Checkpoint complete (policy defaults wired)

Tasks:
- Add export policy object (`modern_graphics/export_policy.py`).
- Set default behavior to minimal padding.
- Define crop modes (`none`, `safe`, `tight`).
- Wire policy to export path in incremental PRs.

Outputs:
- Export policy model
- compatibility notes for migration

## Implementation Notes

- Keep compatibility: no breaking runtime change in first scaffolding pass.
- Prefer additive APIs before replacement.
- Each workstream ships independently, then integrated in a phase gate review.

## Phase 1 Gate Baseline (Current)

From `reports/phase1-quality.md`:
- pass: 8
- warn: 0
- fail: 0

Hard fail gates:
- `min_text_size`
- `contrast_ratio`
- `whitespace_guard`

Soft warn gates:
- `focal_point_budget`
- `density_budget`

Current warn-only layouts:
- none (all core Phase 1 fixtures are passing)

From `reports/phase1-token-debt.md`:
- files scanned: 28
- files with findings: 25
- total findings: 2033

Top debt files:
1. `modern_graphics/diagrams/modern_hero.py`
2. `modern_graphics/diagrams/insight.py`
3. `modern_graphics/color_scheme.py`

## Phase 2 Slice 1 Plan (Token-Driven Rewrite)

Objective:
- reduce quality fails and token debt in the highest-leverage layouts first.

Scope (first slice):
1. `modern_graphics/diagrams/modern_hero.py`
2. `modern_graphics/diagrams/insight.py`
3. `modern_graphics/diagrams/comparison.py`

Work items:
- Replace ad-hoc literals with semantic token references.
- Enforce min text size >= 13px in default/clarity mode.
- Reduce focal point overload in default templates.
- Normalize spacing/radius usage to token contract.
- Keep canvas + embedded SVG composition paths intact.

Success targets for slice 1:
- Keep all core Phase 1 fixture layouts at pass.
- Treat any future warn/fail as regressions to be addressed before phase close.
- total findings reduced by >= 20% in slice files.
- no regression in feature-flagged `create` scaffold.

Validation commands:
```bash
python scripts/validate_overhaul_phase1.py
python scripts/run_phase1_quality_harness.py
```

Exit criteria for Slice 1:
- reports updated and committed
- docs updated for any behavior/default changes
- migration notes added if CLI/API defaults change
