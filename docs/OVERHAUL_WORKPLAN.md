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
Status: In progress

Tasks:
- Create semantic token model (`modern_graphics/visual_system.py`).
- Add token preset definitions for clarity mode.
- Add token-lint helpers for templates/layouts.
- Document token contract in docs.

Outputs:
- Token model + helpers
- Token contract docs

## B) Critique Gates + Quality Harness
Owner: TBD
Status: In progress

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
Status: In progress

Tasks:
- Define new command contract (`create` by layout type).
- Add parser scaffolding behind env/feature flag.
- Define compatibility adapter requirements.

Outputs:
- CLI contract doc section
- parser scaffolding (non-breaking)

## D) Export Determinism + Policy
Owner: TBD
Status: In progress

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
