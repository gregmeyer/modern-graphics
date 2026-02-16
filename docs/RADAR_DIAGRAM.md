# Radar Diagram Type

The radar diagram type has been added to the modern-graphics package. This document explains how it was integrated and how to use it.

## What Was Added

1. **New Diagram Module**: `modern_graphics/diagrams/radar.py`
   - Contains `generate_radar_diagram()` function
   - Contains `RadarDiagramGenerator` class

2. **Updated Exports**: `modern_graphics/diagrams/__init__.py`
   - Added radar imports
   - Registered in `DIAGRAM_REGISTRY`

3. **Generator Integration**: `modern_graphics/generator.py`
   - Added `generate_radar_diagram()` method to `ModernGraphicsGenerator`

4. **Example**: `examples/radar_example.py`
   - Shows how to use the radar diagram

## Usage

### Basic Usage

```python
from modern_graphics import ModernGraphicsGenerator, Attribution

generator = ModernGraphicsGenerator(
    "Support Radar",
    attribution=Attribution(copyright="© 2025 Your Name")
)

signals = [
    {
        "axiom": "Axiom 1: Orientation",
        "detects": '"What happens next?" spikes',
        "discovers": "Orientation failure",
        "covers": "Clear states, progress, ownership",
        "position": {"angle": 0},  # 0 = top, degrees clockwise
        "color": "blue",
    },
    # ... more signals
]

html = generator.generate_radar_diagram(
    center_label="SUPPORT\nRADAR",
    signals=signals,
    viewbox_width=1200,
    viewbox_height=700,
    radar_radius=250,
    show_sweep=True,
    show_circles=True,
)
```

### Signal Dictionary Structure

Each signal in the `signals` list should have:

- **`axiom`** (str): The axiom identifier/name (e.g., "Axiom 1: Orientation")
- **`detects`** (str): What signal it detects (e.g., '"What happens next?" spikes')
- **`discovers`** (str): Type of failure discovered (e.g., "Orientation failure")
- **`covers`** (str, optional): What it covers (e.g., "Clear states, progress, ownership")
- **`position`** (dict): Position specification:
  - `angle` (int): Degrees from top (0 = top, 90 = right, 180 = bottom, 270 = left)
  - OR `x`, `y` (float): Normalized coordinates (0.0 to 1.0)
- **`color`** (str): Color key - one of: "blue", "purple", "green", "orange", "gray"

### Parameters

- **`center_label`** (str): Label for center radar dish (supports `\n` for multi-line)
- **`signals`** (List[Dict]): List of signal dictionaries (see above)
- **`viewbox_width`** (int): SVG viewBox width (default: 1200)
- **`viewbox_height`** (int): SVG viewBox height (default: 700)
- **`radar_radius`** (int): Radius of outer radar circle (default: 250)
- **`show_sweep`** (bool): Show animated radar sweep (default: True)
- **`show_circles`** (bool): Show concentric radar circles (default: True)

## Features

- **Animated radar sweep**: Rotating sweep animation
- **Pulsing signal blips**: Each signal blip pulses with unique timing
- **Annotation cards**: Each signal has a detailed annotation card showing:
  - Axiom name
  - What it detects
  - What it discovers
  - What it covers (optional)
- **Color-coded**: Signals use color keys for consistent styling
- **Flexible positioning**: Use angles or normalized coordinates

## Integration Steps Summary

To add a new diagram type to modern-graphics:

1. **Create diagram module** (`diagrams/your_diagram.py`):
   - Implement `generate_your_diagram()` function
   - Optionally create `YourDiagramGenerator` class inheriting from `DiagramGenerator`

2. **Update `diagrams/__init__.py`**:
   - Import your diagram function and generator class
   - Add to `DIAGRAM_REGISTRY` if using generator class
   - Add to `__all__` exports

3. **Update `generator.py`**:
   - Import your diagram function
   - Add method to `ModernGraphicsGenerator` class

4. **Create example** (optional):
   - Add example in `examples/` directory
   - Shows usage patterns

5. **Documentation** (optional):
   - Add to API docs
   - Create usage guide

## Example Output

The radar diagram generates an SVG visualization with:
- Center radar dish with label
- Concentric circles (optional)
- Animated sweep (optional)
- Signal blips positioned around the radar
- Connection lines from center to each signal
- Annotation cards for each signal

All styled consistently with the modern-graphics theme system.
