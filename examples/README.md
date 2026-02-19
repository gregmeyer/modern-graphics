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

### I need a custom theme (font + colors)

Run:

```bash
python - <<'PY'
from pathlib import Path
from modern_graphics import TemplateBuilder, register_template, ModernGraphicsGenerator, Attribution

theme = (
    TemplateBuilder("brand-clean")
    .add_color("primary", ("#0B1F3A", "#163A6B"), "rgba(22, 58, 107, 0.28)")
    .add_color("accent", ("#0E7490", "#155E75"), "rgba(14, 116, 144, 0.24)")
    .set_font_family("'Avenir Next', 'Segoe UI', sans-serif")
    .set_background_color("#F8FAFC")
    .build()
)

register_template(theme)
generator = ModernGraphicsGenerator("Custom Theme", Attribution(), template=theme)
html = generator.generate_cycle_diagram([
    {"text": "Capture", "color": "primary"},
    {"text": "Decide", "color": "accent"},
    {"text": "Ship", "color": "primary"},
])
generator.export_to_png(html, Path("examples/output/generated/theme-font-color.png"), crop_mode="safe")
print("Expected output: examples/output/generated/theme-font-color.png")
PY
```

Expected output: `examples/output/generated/theme-font-color.png`

### I need crop/padding variants for the same graphic

Run:

```bash
python - <<'PY'
from pathlib import Path
from modern_graphics import ModernGraphicsGenerator, Attribution

generator = ModernGraphicsGenerator("Crop Variants", Attribution())
html = generator.generate_cycle_diagram([
    {"text": "Capture", "color": "blue"},
    {"text": "Review", "color": "green"},
    {"text": "Publish", "color": "orange"},
])
generator.export_to_png(html, Path("examples/output/generated/crop-safe.png"), crop_mode="safe")
generator.export_to_png(html, Path("examples/output/generated/crop-tight.png"), crop_mode="tight", padding=8)
generator.export_to_png(html, Path("examples/output/generated/crop-none.png"), crop_mode="none", padding=0)
print("Expected outputs: crop-safe.png, crop-tight.png, crop-none.png")
PY
```

Expected outputs:
- `examples/output/generated/crop-safe.png`
- `examples/output/generated/crop-tight.png`
- `examples/output/generated/crop-none.png`

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
