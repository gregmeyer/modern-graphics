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
- density and export controls (`--density`, `--png`, `--crop-mode`, `--padding-mode`)

## Defaults

- density: `clarity`
- theme: `corporate`
- crop mode: `safe`
- padding mode: `minimal`

For full PNG/export behavior details, see `docs/EXPORT.md`.

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

## Fast Recipes

### Hero

```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --output ./output/hero.html
```

### Comparison

```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout comparison \
  --left "Before:Manual triage:Slow" \
  --right "After:Agentic triage:Faster" \
  --output ./output/comparison.html
```

### Insight Card

```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout insight-card \
  --text "One-page artifacts force explicit decisions." \
  --output ./output/insight-card.html
```

### PNG Export (Expert)

```bash
MODERN_GRAPHICS_ENABLE_CREATE=1 modern-graphics create \
  --layout insight-story \
  --headline "When shipping gets easy, choosing gets hard." \
  --insight-text "Use a short checklist before shipping." \
  --png \
  --crop-mode safe \
  --padding-mode minimal \
  --output ./output/insight-story.png
```

## Error Hints

If required inputs are missing, `create` returns:

- a direct error message
- a layout-specific `Hint: try ...` command

This is intentional to keep first-time usage recoverable without reading source code.
