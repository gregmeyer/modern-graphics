# Docs Coverage Backlog

Date: 2026-02-17
Status: In progress

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

### Slice 1: Coverage Lift (Docs + recipes)

Owner workstreams that can run in parallel:

1. CLI recipe coverage
- `docs/CREATE_COMMAND.md`
- Add CLI-only layout section with copy/paste examples for:
  - `before-after`
  - `slide-cards`
  - `slide-compare`
  - `premium-card`

2. Wireframe + insight workflow coverage
- `docs/WIREFRAME_SCENE_SPEC.md`
- Add:
  - scene-spec -> svg -> insight-card recipe
  - insight-story auto-wireframe recipe
  - tracked reference assets links

3. Index and discoverability
- `docs/DIAGRAM_TYPES.md`
- `docs/README.md`
- `examples/README.md`
- Add discoverability pointers to new recipe sections.

### Slice 2: Asset-backed examples (follow-up)

1. Generate and track canonical showcase assets for:
- before/after
- slide-cards
- slide-compare
- premium-card
- wireframe-scene + insight-card

2. Embed those assets in the relevant docs.

## Completion Gates

1. All listed features have at least one copy/paste CLI recipe in docs.
2. Docs index points to each feature family.
3. Link check passes across README/docs/examples README.
4. Follow-up slice adds tracked visual examples for each feature.
