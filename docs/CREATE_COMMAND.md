# Create Command Guide

Use `modern-graphics create` when you want one command path with clarity-first defaults.

## Mental Model

`create` is split into three argument groups:

1. `core`
- `--layout`
- `--output`
- `--title`
- `--theme`

2. `layout-specific`
- content inputs that depend on `--layout` (for example `--headline`, `--left/--right`, `--events`)

3. `expert`
- density and export controls (`--density`, `--png`, `--export-preset`, `--crop-mode`, `--padding-mode`)

## Defaults

- density: `clarity`
- theme: `corporate`
- crop mode: `safe`
- padding mode: `minimal`

For full PNG/export behavior details, see `docs/EXPORT.md`.
For legacy command migration, see `docs/MIGRATION.md`.

## Layout Decision Table

| If you need... | Use layout | Required inputs |
|---|---|---|
| Hero opener | `hero` | `--headline` |
| Pull quote / key insight | `insight` or `key-insight` | `--text` |
| Insight + visual panel | `insight-card` | `--text` (optional `--svg-file`) |
| Before/after insight narrative | `insight-story` | `--headline` + `--insight-text` (optional `--before-svg`, `--after-svg`) |
| Side-by-side tradeoff | `comparison` | `--left` + `--right` |
| Narrative story block | `story` | optional `--what-changed`, `--time-period`, `--what-it-means` |
| Chronology | `timeline` | `--events` |
| Stage conversion | `funnel` | `--stages` (optional `--values`) |
| Numbered concept grid | `grid` | `--items` |
| Legacy transformation layout | `before-after` (CLI command) | `--before` + `--after` |
| Multi-card transformation strip | `slide-cards` (CLI command) | `--cards` JSON |
| Card-vs-card comparison | `slide-compare` (CLI command) | `--left` JSON + `--right` JSON |
| Stacked hero/detail card | `premium-card` (CLI command) | `--config` JSON |

## Fast Recipes

### Hero

```bash
modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --output ./output/hero.html
```

### Comparison

```bash
modern-graphics create \
  --layout comparison \
  --left "Before:Manual triage:Slow" \
  --right "After:Agentic triage:Faster" \
  --output ./output/comparison.html
```

### Insight Card

```bash
modern-graphics create \
  --layout insight-card \
  --text "One-page artifacts force explicit decisions." \
  --output ./output/insight-card.html
```

### PNG Export (Expert)

```bash
modern-graphics create \
  --layout insight-story \
  --headline "When shipping gets easy, choosing gets hard." \
  --insight-text "Use a short checklist before shipping." \
  --png \
  --crop-mode safe \
  --padding-mode minimal \
  --output ./output/insight-story.png
```

### Social Presets

Use fixed channel presets when you need share-ready dimensions:

```bash
modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --png \
  --export-preset linkedin \
  --output ./output/hero-linkedin.png
```

Available presets:
- `linkedin` (1200x627)
- `x` (1600x900)
- `substack-hero` (1400x700)

Tracked social preset examples:
- `examples/output/showcase/create-first/social-preset-linkedin.png`
- `examples/output/showcase/create-first/social-preset-x.png`
- `examples/output/showcase/create-first/social-preset-substack-hero.png`

## CLI-Only Layouts (Outside `create`)

These layouts are currently available as dedicated commands instead of `create` layouts.

### Before/After

```bash
modern-graphics before-after \
  --title "Support Workflow Shift" \
  --before "Manual triage,Long queues,Status uncertainty" \
  --after "Inline help,Faster routing,Visible status" \
  --png \
  --output ./output/before-after.png
```

### Slide Cards

```bash
modern-graphics slide-cards \
  --title "Execution Shift" \
  --cards '[{"title":"Prompting","tagline":"Step 1","subtext":"Generate options"},{"title":"Constrainting","tagline":"Step 2","subtext":"Set boundaries"},{"title":"Decision gates","tagline":"Step 3","subtext":"Filter what ships"}]' \
  --png \
  --output ./output/slide-cards.png
```

### Slide Compare

```bash
modern-graphics slide-compare \
  --title "Operating Modes" \
  --left '{"title":"Motion","tagline":"Ship more","subtext":"High output, noisy relevance"}' \
  --right '{"title":"Judgment","tagline":"Ship fewer","subtext":"Lower volume, higher signal"}' \
  --png \
  --output ./output/slide-compare.png
```

### Premium Card

```bash
modern-graphics premium-card \
  --title "Ops Guardrail Premium Card" \
  --config examples/ops_guardrail_premium_card.json \
  --png \
  --output ./output/premium-card.png
```

## Error Hints

If required inputs are missing, `create` returns:

- a direct error message
- a layout-specific `Hint: try ...` command

This is intentional to keep first-time usage recoverable without reading source code.
