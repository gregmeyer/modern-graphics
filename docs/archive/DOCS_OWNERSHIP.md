# Docs Ownership Map

Use this map to keep docs focused, reduce overlap, and prevent drift.

## Canonical Audience Goals

1. Use the package
2. Make graphics
3. Build a custom theme
4. Build a super custom hero
5. Call the CLI directly

## Doc Ownership

| Document | Primary Audience Goal | Canonical Purpose | Should Not Duplicate |
|---|---|---|---|
| `README.md` | All (entry) | Top-level navigation, above-the-fold examples, one first command | Full command matrix, long advanced implementation detail |
| `docs/README.md` | All (routing hub) | Task-first docs map and routing | Deep tutorials, repeated command snippets |
| `docs/QUICKSTART.md` | 1 | Fastest successful output path | Full flag reference, advanced customization guides |
| `examples/README.md` | 2 | Run-now cookbook by outcome with expected outputs | Full CLI argument reference, API internals |
| `docs/CREATE_COMMAND.md` | 5 | Canonical CLI argument model, layouts, and flags | Long intent cookbook, repeated showcase galleries |
| `docs/ADVANCED.md` | 3 | Custom templates, SVG.js, extensions, and advanced workflows | First-run setup or basic create usage |
| `docs/HERO_SLIDES.md` | 4 | Super custom hero composition patterns and freeform strategies | Generic non-hero layout catalog |
| `docs/EXPORT.md` | 5 | Export behavior, crop, padding, and preset policy | General layout selection guidance |
| `docs/DIAGRAM_TYPES.md` | 2 | Layout selection and diagram catalog | Full CLI flag semantics |
| `docs/MIGRATION.md` | 5 | Legacy-to-create migration steps and compatibility notes | New-user first run instructions |

## Editing Rules

- Add new command flags in `docs/CREATE_COMMAND.md` first, then reference from other docs.
- Keep runnable outcome recipes in `examples/README.md`.
- Keep top-level navigation changes synchronized in both `README.md` and `docs/README.md`.
- Keep `## Use This Doc When` (or `## Use This Page When`) in core entry docs.

## Required Checks

Run before opening a PR:

```bash
npm run check-docs-drift
```

If this fails, fix links, duplicate navigation links, or required entry headings before merging.
