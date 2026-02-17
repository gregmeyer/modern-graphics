# Modern Graphics Overhaul Spec

Status: Draft for review
Owner: Greg Meyer + contributors
Priority: High

## 1) Goals

Primary goals (in order):
1. Visual quality consistency across all layout types.
2. Usability and speed-to-good-output for CLI and prompt workflows.
3. Maintainability and extensibility for contributors.

Required capabilities to preserve:
- Freeform canvas composition.
- Insight/story cards with embedded SVG.
- Themed professional output via CLI and prompt paths.

## 2) Non-Goals

- Adding many new diagram types before architecture cleanup.
- AI feature expansion before core layout/readability stability.
- Backward compatibility at any cost.

## 3) Product Principles

1. Clarity by default.
2. Dense composition is explicit opt-in.
3. Compose first, crop last.
4. Minimal padding by default for reuse.
5. Two-path UX: beginner-safe and expert-composable.
6. Theme fidelity must survive every layout/export path.

## 4) Phase Plan

## Phase 1 (First): Lock visual system + critique gates

Objective:
- Freeze a shared visual system and enforce quality gates before rewrite.

Deliverables:
- `visual-system` token contract (single source of truth):
  - typography scale
  - spacing scale
  - radius/elevation
  - semantic color roles
- Layout contract schema per type:
  - required content slots
  - optional slots
  - density budget
  - min text size
- Critique gates (auto checks + review report):
  - 3-second hierarchy legibility
  - max 2 focal points per section
  - contrast threshold checks
  - micro-label size threshold
  - whitespace/gutter guard
- Quality harness with golden fixtures across major layout families.

Acceptance criteria:
- All existing core layouts pass token lint and critique gates.
- Generated report clearly shows pass/fail by layout.
- No ad-hoc style constants in templates outside token system.

## Phase 2: Rewrite core architecture

Objective:
- Rebuild internals for composability and consistency.

Target architecture layers:
1. Content model
2. Layout composition engine
3. Theme application engine
4. Export pipeline
5. CLI + prompt adapters

Requirements:
- Keep freeform canvas and SVG embed first-class.
- Add layout strategy modules (hero/insight/story/comparison/timeline/etc.).
- Add strict template lint mode.

Acceptance criteria:
- Layout code is modular by strategy.
- New layout can be added via documented extension interface.
- Legacy feature parity reached for core generation paths.

Current implementation status (checkpoint):
- Strategy registry is active and `create --layout` routes through strategy dispatch.
- Strategy coverage includes: hero, hero-triptych, key-insight, insight-story, insight-card, comparison, timeline, funnel, grid, story.
- Typed layout payload models now validate core create inputs before render:
  - `HeroPayload`, `ComparisonPayload`, `TimelinePayload`, `FunnelPayload`, `GridPayload`.
  - `KeyInsightPayload`, `InsightCardPayload`, `InsightStoryPayload`.
- Smoke fixtures now include insight-card patterns (key insight/pull quote, data-story card, checklist-style insight story).
- Insight fixture regression harness now snapshots deterministic outputs under `reports/insight-fixtures/`.
- Strategy extension contract is documented in `docs/STRATEGY_EXTENSION.md`.

## Phase 3: UX surface redesign (CLI + prompt)

Objective:
- Reduce decision overhead for users while preserving advanced control.

CLI design:
- Unified `create` entrypoint by type.
- `clarity` mode is default.
- Density modes:
  - `clarity` (default)
  - `balanced`
  - `dense`
- Export defaults:
  - minimal padding
  - deterministic crop behavior
- Progressive disclosure:
  - essentials by default
  - advanced flags grouped under expert mode.

Acceptance criteria:
- New user can generate production-usable graphics in 1-2 commands.
- Docs focus on common workflows, not parameter sprawl.

Current implementation status (checkpoint):
- `create` command now uses progressive disclosure:
  - `core`, `layout-specific`, and `expert` argument groups.
- Clarity defaults are centralized (`CREATE_DEFAULTS`) and validated:
  - density=`clarity`, crop=`safe`, padding=`minimal`, theme=`corporate`.
- Create error handling now returns layout-specific actionable hints with example commands.
- Validator includes create success/failure smoke checks for UX guardrails.

## Phase 4: Export determinism + reliability

Objective:
- Make output bounds predictable and reusable across channels.

Requirements:
- Default output has minimal, consistent outer padding.
- Deterministic crop modes:
  - `none`
  - `safe`
  - `tight`
- Layout-specific bounds policy where needed, but same interface.

Acceptance criteria:
- Reduced miscrop/gutter regressions in fixture corpus.
- Export behavior documented and test-covered.

Current implementation status (checkpoint):
- Export pipeline now uses deterministic crop flow:
  - crop mode normalization (`none|safe|tight`, invalid values fallback to `safe`).
  - single content-bounds detector with explicit root selectors + generic fallback.
  - unified crop-box math path with bounds clamping.
- Tight mode now applies a consistent reduced-padding rule from the configured base padding.
- Phase validator now checks export mode normalization and crop-box math invariants.
- Added smoke tests for export helper behavior:
  - mode normalization
  - padding behavior (`safe` vs `tight`)
  - crop-box bounds clamping

## Phase 5: Migration + adoption

Objective:
- Enable transition with clear compatibility policy.

Requirements:
- Compatibility adapter for legacy CLI signatures.
- Deprecation warnings and migration tips in CLI output.
- Migration guide with before/after examples.

Acceptance criteria:
- Existing projects can migrate with clear path and low risk.

## 5) Visual System Contract (Phase 1)

Required token groups:
- Typography: display/headline/body/caption sizes + line heights.
- Spacing: canonical scale (no arbitrary values in templates).
- Shape: radius levels and border weights.
- Elevation: shadow levels.
- Colors (semantic):
  - background/surface/overlay
  - text primary/secondary/muted
  - accent/positive/warning/danger/info
  - border subtle/strong

Rules:
- Templates consume semantic tokens only.
- Themes map to semantic tokens; templates do not directly own brand hex values.

## 6) Critique Gate Spec (Phase 1)

Gate checks:
1. Hierarchy check:
- headline and primary message visible at first scan.
2. Focus check:
- maximum two focal points per major section.
3. Legibility check:
- enforce minimum body/caption sizes.
4. Contrast check:
- required contrast thresholds for text layers.
5. Density check:
- cap list lengths and micro-label count per panel.
6. Whitespace check:
- reject excessive gutter/empty frame area.

Output:
- Machine-readable report + human summary.

## 7) Extension Model

Requirements:
- Register new layout via layout registry.
- Implement contract schema for required/optional slots.
- Pass quality harness and critique gates.
- Ship one minimal example + one themed example.

## 8) Testing Strategy

Test tiers:
1. Unit tests:
- token mapping
- layout contract validation
- CLI arg parsing
2. Snapshot tests:
- canonical fixtures for all core layout types
3. Quality tests:
- contrast/size/density/whitespace gates
4. Export tests:
- crop mode behavior
- padding consistency

## 9) Risks + Mitigations

Risk: rewrite stalls due to scope.
- Mitigation: phase gates with acceptance criteria and hard cut lines.

Risk: compatibility pain for current users.
- Mitigation: adapter + migration warnings + docs.

Risk: over-constraining kills creativity.
- Mitigation: strict defaults + explicit expert escape hatches.

## 10) Review Checklist

Use this checklist before approving implementation start:
- Phase order accepted (Phase 1 gates first, then rewrite).
- Token contract scope accepted.
- Critique gate thresholds accepted.
- Compatibility policy accepted.
- Success metrics accepted.

## 11) Documentation Gate (Required Every Phase)

Each phase is not complete until documentation updates ship with code updates.

Required phase docs:
- Update `docs/OVERHAUL_SPEC.md` with what changed and what is next.
- Update `docs/OVERHAUL_WORKPLAN.md` status for impacted workstreams.
- Update user-facing docs (`README.md` and relevant files under `docs/`).
- Add migration notes when CLI/API behavior changes.
- Update or add runnable examples for the new default path.

Acceptance criteria:
- Reviewer can run the documented commands as written.
- Docs describe default behavior and any feature-flag/legacy behavior.
- New quality checks are documented with pass/fail interpretation.

## 12) Locked Decisions

1. Compatibility window length:
- two releases.
2. Baseline default aspect policy:
- layout-specific defaults with documented baseline families.
3. Channel presets (`newsletter`, `linkedin`, `slides`):
- Phase 3.
4. Decorative effects in `clarity` mode:
- disabled by default, opt-in for decorative chrome.

## 13) Phase 1 Initial Execution Scope

Workstream A: visual system + token contract.
- Deliver token definitions and token-lint checks for core templates.

Workstream B: critique gates + quality harness.
- Deliver gate runner, fixture corpus, and report artifacts.

Workstream C: CLI clarity redesign (scaffold only in Phase 1).
- Deliver command contract and parser scaffolding behind feature flag.

Workstream D: export policy + deterministic defaults.
- Deliver minimal-padding default policy and crop mode contract.
