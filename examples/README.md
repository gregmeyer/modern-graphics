# Examples

Use this page to choose one example path and run it immediately.

## Use This Page When

- You want runnable commands to make graphics now (README goal 2).
- You want tracked visual references before you customize.
- You want output paths that are safe for local experimentation.

For API-first usage, see [`docs/QUICKSTART.md`](../docs/QUICKSTART.md).
For direct CLI recipes, see [`docs/CREATE_COMMAND.md`](../docs/CREATE_COMMAND.md).
For custom themes and super custom heroes, see [`docs/ADVANCED.md`](../docs/ADVANCED.md) and [`docs/HERO_SLIDES.md`](../docs/HERO_SLIDES.md).

This page is command-first. For full flag reference and edge-case behavior, use `docs/CREATE_COMMAND.md`.

## Pick an Example by Goal

### I need a hero slide

Run:

```bash
modern-graphics create \
  --layout hero \
  --headline "Make the journey the tie-breaker" \
  --png \
  --output examples/output/generated/hero-example.png
```

Expected output: `examples/output/generated/hero-example.png`

See tracked hero references: `examples/output/showcase/hero-slides/`

### I need an insight card or insight story

Run:

```bash
modern-graphics create \
  --layout insight-card \
  --text "Execution scales faster than decision quality." \
  --png \
  --output examples/output/generated/insight-card-example.png
```

Expected output: `examples/output/generated/insight-card-example.png`

See tracked insight references: `examples/output/showcase/insight-graphics/`

### I need social exports

Run:

```bash
modern-graphics create \
  --layout hero \
  --headline "Filter what ships" \
  --png \
  --export-preset linkedin \
  --output examples/output/generated/hero-linkedin.png
```

Expected output: `examples/output/generated/hero-linkedin.png`

Tracked social preset references live in `examples/output/showcase/create-first/`.

### I need a wireframe scene I can reuse in insight graphics

Run:

```bash
modern-graphics wireframe-scene \
  --preset after \
  --output examples/output/generated/after-scene.svg
```

Expected output: `examples/output/generated/after-scene.svg`

Then pair with an insight card:

```bash
modern-graphics create \
  --layout insight-card \
  --text "Inline support reduced escalations." \
  --svg-file examples/output/generated/after-scene.svg \
  --png \
  --output examples/output/generated/insight-card-wireframe.png
```

### I need a premium stacked card

Run:

```bash
modern-graphics premium-card \
  --title "Ops Guardrail Premium Card" \
  --config examples/ops_guardrail_premium_card.json \
  --png \
  --output examples/output/generated/ops-guardrail-card.png
```

Expected output: `examples/output/generated/ops-guardrail-card.png`

Tracked Slice 2 references live in `examples/output/showcase/cli-layouts/`.

### I need the full showcase set

Run:

```bash
python scripts/run_showcase.py
```

Expected output roots:
- `examples/output/showcase/diagram-types/`
- `examples/output/showcase/hero-slides/`
- `examples/output/showcase/attribution/`

### I need the full themed gallery

Run:

```bash
python examples/generate_complete_theme_demo.py
```

Expected outputs:
- PNG previews (tracked): `examples/output/theme-demo/*.png`
- Gallery HTML (generated): `examples/output/theme-demo/index.html`

## Output Locations

- Curated, tracked references: `examples/output/showcase/`
- Theme gallery PNG references: `examples/output/theme-demo/*.png`
- Temporary local outputs: `examples/output/generated/`

Detailed output policy: [`examples/output/README.md`](output/README.md).

## Extend Or Validate

If you are extending behavior or validating output quality, use:
- `scripts/README.md`
- `docs/EXPORT.md`
- `docs/MIGRATION.md`
