# Export Options

Control PNG export quality, resolution, and cropping.

## Basic Export

```python
# Standard quality (default)
generator.export_to_png(html, Path('output.png'))
```

## Export Parameters

```python
generator.export_to_png(
    html_content,
    output_path,
    viewport_width=2400,        # Browser viewport width (CSS pixels)
    viewport_height=1600,       # Browser viewport height (CSS pixels)
    device_scale_factor=2,      # Scale factor for resolution (1-4 recommended)
    padding=20,                  # Padding around content (CSS pixels)
    temp_html_path=None          # Optional: custom temp HTML path
)
```

## Resolution Guidelines

### Standard Quality (Default)
- `viewport_width=2400, device_scale_factor=2`
- Good for most use cases, fast generation
- Output: ~4800px wide at 2x scale

### High Quality
- `viewport_width=3200, device_scale_factor=3`
- For print or large displays
- Output: ~9600px wide at 3x scale

### Fast/Low Quality
- `viewport_width=1200, device_scale_factor=1`
- For quick previews or small displays
- Output: ~1200px wide

## Automatic Cropping

All PNG exports automatically crop to the content bounding box, removing excess whitespace. Adjust `padding` if content is cut off:

```python
# More padding if content is too close to edges
generator.export_to_png(html, path, padding=40)

# Minimal padding for tight crop
generator.export_to_png(html, path, padding=5)
```

## Hero Slide Export

Hero slides typically use larger viewports:

```python
hero_export_kwargs = {
    "viewport_width": 1700,
    "viewport_height": 1100,
    "device_scale_factor": 2,
    "padding": 30,
}

generator.export_to_png(html, Path("hero.png"), **hero_export_kwargs)
```

## Saving HTML

Save HTML files for debugging or web use:

```python
generator.save(html, Path('output.html'))
```
