# Plan: Creative Canvas Slides with SVG.js

## Overview
Leverage SVG.js to create more creative, dynamic, and visually engaging canvas slides. Enhance existing hero slides and create new creative slide types with programmatic SVG graphics, animations, patterns, and organic shapes.

## Current State Analysis

### Existing Canvas Capabilities
- **Modern Hero Slides**: Open canvas layouts with static SVG icons
- **Freeform Canvas**: Accepts raw HTML/SVG strings
- **Flow Diagrams**: Static SVG paths with nodes
- **Ribbon Collages**: CSS-based translucent panels
- **Visual Keywords**: Trigger different CSS styles (glassmorphism, warm palette, etc.)

### Limitations
- Static SVG generation (no programmatic manipulation)
- Limited to predefined shapes and paths
- No dynamic gradients, patterns, or animations
- Manual SVG string construction
- No particle effects or organic shapes

## Opportunities with SVG.js

### 1. **Dynamic Backgrounds & Patterns**
- Procedural gradient generation
- Animated patterns (dots, grids, waves)
- Organic noise-based backgrounds
- Layered transparency effects

### 2. **Animated Elements**
- Morphing shapes
- Particle systems
- Flowing connections
- Pulsing/breathing effects

### 3. **Complex Visualizations**
- Data-driven graphics
- Network graphs
- Force-directed layouts
- Interactive flowcharts

### 4. **Creative Compositions**
- Abstract art elements
- Geometric patterns
- Organic shapes (blobs, waves)
- Layered compositions

## Implementation Plan

### Phase 1: Enhanced Canvas Utilities

#### 1.1 Create Canvas Background Generators
**File**: `modern_graphics/svg_canvas.py`

Create utilities for generating creative canvas backgrounds:

```python
def generate_gradient_background(width, height, colors, type='linear', angle=0):
    """Generate animated or static gradient backgrounds"""
    
def generate_pattern_background(width, height, pattern_type='dots', density=0.1):
    """Generate pattern backgrounds (dots, grid, waves, noise)"""
    
def generate_organic_background(width, height, blob_count=5, color_scheme='warm'):
    """Generate organic blob backgrounds"""
    
def generate_particle_background(width, height, particle_count=50, animated=False):
    """Generate particle system backgrounds"""
```

#### 1.2 Create Shape Generators
**File**: `modern_graphics/svg_canvas.py` (continued)

```python
def generate_organic_blob(center_x, center_y, radius, complexity=8):
    """Generate organic blob shape using SVG.js"""
    
def generate_morphing_shape(start_shape, end_shape, steps=10):
    """Generate morphing animation between shapes"""
    
def generate_flowing_path(points, smoothness=0.5):
    """Generate smooth flowing paths between points"""
    
def generate_particle_system(count, bounds, behavior='float'):
    """Generate particle system with behaviors"""
```

### Phase 2: Enhanced Hero Slide Integration

#### 2.1 Add SVG.js Canvas Support to Modern Hero
**File**: `modern_graphics/diagrams/modern_hero.py`

Enhance `generate_modern_hero()` to support SVG.js-powered canvases:

```python
def generate_modern_hero(
    ...
    canvas_type: Optional[str] = None,  # 'gradient', 'particles', 'organic', 'pattern'
    canvas_config: Optional[Dict] = None,  # Configuration for canvas type
    animated: bool = False,  # Enable animations
    ...
):
```

#### 2.2 Create Canvas Type Handlers
**File**: `modern_graphics/diagrams/modern_hero.py` (new functions)

```python
def _render_svgjs_canvas(canvas_type: str, config: Dict, width: int, height: int) -> str:
    """Render SVG.js powered canvas based on type"""
    
def _render_gradient_canvas(config: Dict, width: int, height: int) -> str:
    """Render gradient background canvas"""
    
def _render_particle_canvas(config: Dict, width: int, height: int) -> str:
    """Render particle system canvas"""
    
def _render_organic_canvas(config: Dict, width: int, height: int) -> str:
    """Render organic blob canvas"""
```

### Phase 3: New Creative Slide Types

#### 3.1 Abstract Canvas Slide
**File**: `modern_graphics/diagrams/abstract_canvas.py`

Create a new slide type for abstract, artistic compositions:

```python
def generate_abstract_canvas_slide(
    generator: BaseGenerator,
    headline: str,
    subheadline: Optional[str] = None,
    canvas_style: str = 'organic',  # 'organic', 'geometric', 'particles', 'flow'
    color_scheme: str = 'warm',
    elements: Optional[List[Dict]] = None,  # Custom SVG.js elements
    animated: bool = False,
) -> str:
```

**Features**:
- Abstract background compositions
- Floating elements
- Custom SVG.js element injection
- Multiple style presets

#### 3.2 Data Visualization Canvas
**File**: `modern_graphics/diagrams/data_canvas.py`

Create slides that visualize data with SVG.js:

```python
def generate_data_canvas_slide(
    generator: BaseGenerator,
    headline: str,
    data: List[Dict],  # Data points
    visualization_type: str = 'scatter',  # 'scatter', 'network', 'flow', 'timeline'
    style: str = 'minimal',
) -> str:
```

**Features**:
- Scatter plots
- Network graphs
- Flow visualizations
- Timeline visualizations

#### 3.3 Animated Story Canvas
**File**: `modern_graphics/diagrams/animated_canvas.py`

Create animated story slides:

```python
def generate_animated_canvas_slide(
    generator: BaseGenerator,
    headline: str,
    story_beats: List[Dict],  # Story progression points
    animation_type: str = 'flow',  # 'flow', 'morph', 'particles', 'reveal'
    duration: int = 3000,  # Animation duration in ms
) -> str:
```

**Features**:
- Animated story progression
- Morphing shapes
- Particle effects
- Reveal animations

### Phase 4: Advanced Canvas Features

#### 4.1 Interactive Elements (for HTML preview)
**File**: `modern_graphics/svg_canvas.py` (new functions)

```python
def generate_interactive_canvas(
    elements: List[Dict],
    interactions: List[Dict],  # Hover, click behaviors
) -> str:
    """Generate interactive SVG.js canvas with event handlers"""
```

#### 4.2 Canvas Presets Library
**File**: `modern_graphics/canvas_presets.py`

Create preset configurations for common canvas styles:

```python
CANVAS_PRESETS = {
    'minimal_gradient': {...},
    'warm_organic': {...},
    'cool_particles': {...},
    'geometric_pattern': {...},
    'flowing_waves': {...},
}
```

#### 4.3 Canvas Composition System
**File**: `modern_graphics/svg_canvas.py` (new class)

```python
class CanvasComposer:
    """Compose complex canvas layouts with multiple layers"""
    
    def add_background_layer(self, type: str, config: Dict):
        """Add background layer"""
    
    def add_shape_layer(self, shapes: List[Dict]):
        """Add shape layer"""
    
    def add_particle_layer(self, config: Dict):
        """Add particle layer"""
    
    def render(self) -> str:
        """Render complete canvas composition"""
```

## Implementation Details

### SVG.js Features to Leverage

1. **Gradients & Patterns**
   - Linear/radial gradients
   - Pattern fills
   - Mesh gradients (via plugins)

2. **Animations**
   - `.animate()` method for smooth transitions
   - Morphing between shapes
   - Transform animations

3. **Filters & Effects**
   - Blur, shadow effects
   - Color manipulation
   - Compositing

4. **Groups & Layers**
   - Organize elements in groups
   - Layer management
   - Transform groups

5. **Path Manipulation**
   - Bezier curve generation
   - Path morphing
   - Smooth path generation

### Code Structure

```
modern_graphics/
├── svg_canvas.py          # NEW: Canvas generation utilities
├── canvas_presets.py      # NEW: Preset configurations
├── diagrams/
│   ├── abstract_canvas.py      # NEW: Abstract canvas slides
│   ├── data_canvas.py          # NEW: Data visualization slides
│   ├── animated_canvas.py      # NEW: Animated story slides
│   └── modern_hero.py          # MODIFY: Add SVG.js canvas support
```

### Example Usage

#### Enhanced Hero with SVG.js Canvas

```python
from modern_graphics import ModernGraphicsGenerator, Attribution

generator = ModernGraphicsGenerator("Creative Slide", Attribution(), use_svg_js=True)

html = generator.generate_modern_hero(
    headline="Build Creative Graphics",
    subheadline="With SVG.js powered canvases",
    canvas_type="organic",
    canvas_config={
        "blob_count": 5,
        "color_scheme": "warm",
        "animated": True
    },
    animated=True
)
```

#### Abstract Canvas Slide

```python
html = generator.generate_abstract_canvas_slide(
    headline="Abstract Composition",
    canvas_style="organic",
    color_scheme="warm",
    elements=[
        {"type": "blob", "x": 200, "y": 300, "radius": 100},
        {"type": "particle", "count": 30, "behavior": "float"},
    ],
    animated=True
)
```

#### Data Visualization Canvas

```python
html = generator.generate_data_canvas_slide(
    headline="Data Insights",
    data=[
        {"x": 100, "y": 200, "value": 50, "label": "A"},
        {"x": 300, "y": 150, "value": 75, "label": "B"},
        {"x": 500, "y": 250, "value": 60, "label": "C"},
    ],
    visualization_type="scatter",
    style="minimal"
)
```

## Migration Strategy

### Backward Compatibility
- All existing slides continue to work
- SVG.js is opt-in via `use_svg_js=True`
- New canvas features are additive

### Gradual Adoption
1. **Phase 1**: Add canvas utilities (no breaking changes)
2. **Phase 2**: Enhance hero slides (backward compatible)
3. **Phase 3**: Add new slide types (new features)
4. **Phase 4**: Advanced features (optional)

## Testing Strategy

### Unit Tests
- Test canvas generation functions
- Test shape generators
- Test composition system

### Visual Tests
- Generate example outputs for each canvas type
- Compare before/after for hero slides
- Validate PNG export quality

### Integration Tests
- Test SVG.js integration with Playwright
- Verify animations render correctly
- Test performance with complex canvases

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Only include SVG.js when needed
2. **Animation Control**: Disable animations for PNG export
3. **Complexity Limits**: Set max elements/particles
4. **Caching**: Cache generated canvas code

### PNG Export Considerations
- Animations won't be visible in static PNGs
- Use final frame for export
- Consider animation preview mode

## Documentation Updates

### README Updates
- Add "Creative Canvas Slides" section
- Document new slide types
- Provide examples for each canvas type

### Example Scripts
- `scripts/creative_canvas_examples.py` - All canvas types
- `scripts/animated_canvas_demo.py` - Animation examples
- `scripts/data_visualization_demo.py` - Data viz examples

## Success Metrics

1. **Visual Quality**: More engaging, modern slides
2. **Flexibility**: More creative options for users
3. **Performance**: No degradation in PNG export speed
4. **Adoption**: Users start using creative canvases

## Future Enhancements

1. **SVG.js Plugins**: Integrate additional plugins (e.g., morphing, physics)
2. **Template System**: Canvas templates for common styles
3. **AI Integration**: Generate canvas styles from descriptions
4. **Export Options**: Animated GIF export for animations
5. **Interactive Mode**: HTML preview with interactions

## Estimated Effort

- **Phase 1** (Canvas Utilities): 4-6 hours
- **Phase 2** (Hero Integration): 3-4 hours
- **Phase 3** (New Slide Types): 6-8 hours
- **Phase 4** (Advanced Features): 4-6 hours
- **Testing & Documentation**: 3-4 hours
- **Total**: ~20-28 hours

## Next Steps

1. Review and approve plan
2. Start with Phase 1 (Canvas Utilities)
3. Create example outputs for review
4. Iterate based on feedback
5. Proceed to subsequent phases
