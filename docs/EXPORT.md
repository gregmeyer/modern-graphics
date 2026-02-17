# Export Guide

Use this guide when you care about predictable bounds and reusable PNG output.

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

### `none`
- Behavior: no cropping, full-page screenshot.
- Use when you need exact viewport framing.

```python
generator.export_to_png(html, Path("out.png"), crop_mode="none", padding=0)
```

### `safe` (default)
- Behavior: crop to detected content bounds with configured padding.
- Use for production assets that need reliability.

```python
generator.export_to_png(html, Path("out.png"), crop_mode="safe")
```

### `tight`
- Behavior: same content bounds detection, reduced effective padding.
- Use for social/share variants where canvas density should be higher.

```python
generator.export_to_png(html, Path("out.png"), crop_mode="tight")
```

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
