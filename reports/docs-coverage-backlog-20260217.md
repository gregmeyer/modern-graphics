# Docs Coverage Backlog

Date: 2026-02-17
Status: Slice 1 complete, Slice 2 in progress

## Goal

Increase visibility and usability for underrepresented but supported features.

## Underrepresented Feature Set

- `premium-card`
- `before-after`
- `slide-cards`
- `slide-compare`
- `wireframe-scene`
- insight + wireframe composition workflow
- `modern-hero-triptych` and `modern-hero-prompt` (follow-up)
- `key-insight` variants (follow-up)

## Execution Plan (Parallel Workstreams)

### Slice 1: Coverage Lift (Docs + recipes) ✅ Complete

1. CLI recipe coverage
- `docs/CREATE_COMMAND.md`
- Added CLI-only layout section with copy/paste examples for:
  - `before-after`
  - `slide-cards`
  - `slide-compare`
  - `premium-card`

2. Wireframe + insight workflow coverage
- `docs/WIREFRAME_SCENE_SPEC.md`
- Added:
  - scene-spec -> svg -> insight-card recipe
  - insight-story auto-wireframe recipe
  - tracked reference asset links

3. Index and discoverability
- `docs/DIAGRAM_TYPES.md`
- `docs/README.md`
- `examples/README.md`
- Added discoverability pointers to new recipe sections.

### Slice 2: Asset-backed examples 🚧 In progress

1. Generated and tracked canonical showcase assets under:
- `examples/output/showcase/cli-layouts/01-slide-cards.png`
- `examples/output/showcase/cli-layouts/02-slide-compare.png`
- `examples/output/showcase/cli-layouts/03-premium-card.png`
- `examples/output/showcase/cli-layouts/04-wireframe-scene.svg`
- `examples/output/showcase/cli-layouts/05-wireframe-insight-card.png`
- `examples/output/showcase/cli-layouts/06-wireframe-insight-story.png`

2. Added reproducible generator script:
- `scripts/generate_cli_layout_showcase.py`

3. Embedded/linked assets in docs:
- `docs/CREATE_COMMAND.md`
- `docs/WIREFRAME_SCENE_SPEC.md`
- `docs/DIAGRAM_TYPES.md`
- `examples/README.md`
- `examples/output/README.md`

## Blockers / Exceptions

- `before-after` command is currently wired to a stub (`NotImplementedError` in `modern_graphics/diagrams/before_after.py`).
- This command is documented as blocked and excluded from Slice 2 generated assets.

## Completion Gates

1. All listed features have at least one copy/paste CLI recipe in docs. ✅
2. Docs index points to each feature family. ✅
3. Link check passes across README/docs/examples README. (to run in PR validation)
4. Slice 2 includes tracked visual examples for all non-blocked features. ✅
