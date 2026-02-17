# Example Outputs

This directory mixes curated references (tracked in git) and local generation output (not tracked).

## What Is Tracked vs Generated

Tracked in git:
- `showcase/` (canonical reference outputs used in docs)
- `theme-demo/*.png` (gallery preview PNGs)

Generated locally (do not commit):
- `generated/` (scratch output for local runs)
- `theme-demo/index.html` (regenerated gallery page)
- ad-hoc debug files and temporary snapshots

## Canonical Showcase Locations

Use these folders when linking examples in docs:

- `showcase/create-first/` (first-run `create` command references)
- `showcase/diagram-types/` (core diagram set)
- `showcase/cli-layouts/` (underrepresented CLI layout references)
- `showcase/insight-graphics/` (insight/key-insight/card/story references)
- `showcase/hero-slides/` (hero variants)
- `showcase/attribution/` (attribution display references)

Theme gallery references:
- `theme-demo/*.png`

## How to Regenerate Safely

Regenerate curated showcase outputs:

```bash
python scripts/run_showcase.py
```

Regenerate create-first references used in docs:

```bash
python scripts/generate_readme_create_examples.py
```

Regenerate theme demo gallery:

```bash
python examples/generate_complete_theme_demo.py
```

This updates:
- tracked PNGs in `examples/output/theme-demo/`
- generated HTML at `examples/output/theme-demo/index.html`

## Do Not Commit (Anti-Bloat Rules)

Do not commit:
- `examples/output/generated/**`
- temporary local test captures
- one-off experiment outputs

If you need to add a new tracked showcase image, ensure it is:
- representative (not a one-off debug artifact)
- referenced by docs or tests
- regenerated via a scriptable path

## Quick Check Before Commit

```bash
git status -- examples/output
```

If you see large unplanned diffs under `generated/`, remove them before committing.
