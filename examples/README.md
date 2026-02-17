# Examples

Use this page to choose one example path and run it immediately.

## Pick an Example by Intent

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

Tracked social preset references:
- `examples/output/showcase/create-first/social-preset-linkedin.png`
- `examples/output/showcase/create-first/social-preset-x.png`
- `examples/output/showcase/create-first/social-preset-substack-hero.png`

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

Tracked Slice 2 references:
- `examples/output/showcase/cli-layouts/01-slide-cards.png`
- `examples/output/showcase/cli-layouts/02-slide-compare.png`
- `examples/output/showcase/cli-layouts/03-premium-card.png`

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

Detailed output policy: [`examples/output/README.md`](output/README.md)

## Advanced Examples Index

These are useful when you are extending behavior or testing specific surfaces:

- `examples/flow_styles_example.py` (flow style matrix)
- `examples/hero_mermaid_diagrams.py` (mermaid + hero composition)
- `examples/radar_example.py` (radar chart examples)
- `examples/transaction_card_demo.py` (transaction card composition)
- `scripts/generate_cli_layout_showcase.py` (slice-2 CLI layout showcase asset generator)
- `scripts/export_options.py` (crop/padding/export tuning)
- `scripts/attribution_examples.py` (attribution variants)
- `scripts/run_phase1_quality_harness.py` (quality harness)

## Related Docs

- [`docs/QUICKSTART.md`](../docs/QUICKSTART.md)
- [`docs/CREATE_COMMAND.md`](../docs/CREATE_COMMAND.md)
- [`docs/EXPORT.md`](../docs/EXPORT.md)
- [`docs/MIGRATION.md`](../docs/MIGRATION.md)
