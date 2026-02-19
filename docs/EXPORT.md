# Export Guide

Use this guide when you need predictable bounds, crop behavior, and publish-ready PNGs.

## Use This Doc When

- You need to tune cropping (`none`, `safe`, `tight`) for output framing.
- You need to control padding around generated content.
- You need social-ready dimensions from CLI presets.

If you are still choosing layout/content, start with [Create Command Guide](./CREATE_COMMAND.md).

## Fast Path

### I need reliable default cropping

```python
generator.export_to_png(html, Path("default-safe.png"), crop_mode="safe")
```

Expected output: `default-safe.png` with minimal clipping risk and policy padding.

### I need denser social framing

```python
generator.export_to_png(html, Path("tight-social.png"), crop_mode="tight", padding=8)
```

Expected output: `tight-social.png` with reduced whitespace.

### I need full viewport capture (no crop)

```python
generator.export_to_png(html, Path("full-viewport.png"), crop_mode="none", padding=0)
```

Expected output: `full-viewport.png` matching the full viewport.

### I need CLI social presets

```bash
modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --png \
  --export-preset linkedin \
  --output ./output/hero-linkedin.png
```

Expected output: `./output/hero-linkedin.png`.

## Deep Dive

## Default Behavior

`export_to_png` defaults are policy-driven:

- `crop_mode="safe"`
- `padding=None` resolves to policy default (`minimal` => `8px`)

This is the recommended path for most graphics because it keeps whitespace low without clipping important content.

## API Surface

```python
generator.export_to_png(
    html_content,
    output_path,
    viewport_width=2400,
    viewport_height=1600,
    device_scale_factor=2,
    padding=None,      # None -> policy default
    crop_mode="safe", # none | safe | tight
)
```

## Crop Modes

| Crop Mode | Behavior | Best For |
|---|---|---|
| `none` | Full-page screenshot, no cropping | Exact viewport capture |
| `safe` | Crop to content bounds + policy padding | Default production export |
| `tight` | Crop to content bounds with reduced padding | Dense social/share output |

### `none`

```python
generator.export_to_png(html, Path("out.png"), crop_mode="none", padding=0)
```

### `safe` (default)

```python
generator.export_to_png(html, Path("out.png"), crop_mode="safe")
```

### `tight`

```python
generator.export_to_png(html, Path("out.png"), crop_mode="tight")
```

## Social Presets (CLI)

`modern-graphics create` supports channel presets that apply fixed viewport dimensions plus preset crop/padding defaults:

- `linkedin`: `1200x627`
- `x`: `1600x900`
- `substack-hero`: `1400x700`

Tracked social preset examples: `examples/output/showcase/create-first/`.

## Padding Guidance

- `padding=None`: use policy default (`8px` today)
- `padding=0`: edge-to-edge crop around detected bounds
- `padding>8`: adds breathing room for noisy compositions or future annotations

Examples:

```python
# Default reusable output
generator.export_to_png(html, Path("default.png"), crop_mode="safe")

# Tight social variant
generator.export_to_png(html, Path("tight.png"), crop_mode="tight", padding=8)

# Full viewport capture
generator.export_to_png(html, Path("full.png"), crop_mode="none", padding=0)
```

## Resolution Guidance

- Standard: `viewport_width=2400`, `device_scale_factor=2`
- Fast preview: `viewport_width=1200`, `device_scale_factor=1`
- High-res/print workflows: increase viewport and scale together

## Regression Harnesses

Export determinism is validated by:

- `scripts/validate_overhaul_phase1.py` (policy + crop helper invariants)
- `scripts/run_phase1_quality_harness.py` (includes export fixture snapshots)
- `tests/smoke/test_export_phase4_smoke.py` (crop mode + bounds math)

Fixture snapshots are generated under:

- `reports/export-fixtures/`
- `reports/phase4-export-fixtures.md`
- `reports/phase4-export-fixtures.json`

## Related Docs

- [Create Command Guide](./CREATE_COMMAND.md)
- [Advanced Topics](./ADVANCED.md)
- [Examples](../examples/README.md)
