# When to Use SVG.js vs HTML/CSS

## Decision Framework

Use this guide to determine whether SVG.js or HTML/CSS is the right choice for your graphic.

## Use SVG.js When:

### 1. **Custom Illustrations & Creative Graphics**
- ✅ Freeform creative illustrations (like automation paradox hero canvas)
- ✅ Artistic/complex visualizations
- ✅ Custom shapes that don't fit standard diagram patterns
- ✅ Illustrations that need creative freedom

**Example**: Hero slide with creative canvas showing automation paradox concept

### 2. **Complex Paths & Curves**
- ✅ Smooth bezier curves and quadratic paths
- ✅ Custom path shapes (not just rectangles/circles)
- ✅ Complex line drawings
- ✅ Artistic paths that CSS can't handle

**Example**: Winding game board paths, organic shapes

### 3. **Advanced Shapes**
- ✅ Polygons, stars, custom geometric shapes
- ✅ Shapes that require mathematical precision
- ✅ Complex shape combinations
- ✅ Shapes that need programmatic generation

**Example**: Hexagons for tech diagrams, custom icons

### 4. **Gradients & Advanced Visual Effects**
- ✅ Multi-stop gradients
- ✅ Radial gradients for depth
- ✅ Mesh gradients
- ✅ Complex color transitions

**Example**: Depth effects, 3D-like visuals

### 5. **Animation Requirements**
- ✅ Animated elements (fade-in, rotation, etc.)
- ✅ Progressive reveals
- ✅ Interactive elements
- ✅ Dynamic visualizations

**Example**: Animated progress indicators, rotating elements

### 6. **Precise Mathematical Positioning**
- ✅ Complex calculations for element placement
- ✅ Coordinate-based positioning
- ✅ Transformations (rotate, scale, translate)
- ✅ Precise alignment requirements

**Example**: Circular arrangements with calculated angles

### 7. **Icon Integration**
- ✅ Custom SVG icons/paths
- ✅ Icon libraries
- ✅ Complex iconography
- ✅ Icon transformations

**Example**: Custom checkmarks, arrows, symbols

## Use HTML/CSS When:

### 1. **Standard Diagram Types**
- ✅ Cycle diagrams
- ✅ Comparison diagrams
- ✅ Timeline diagrams
- ✅ Grid layouts
- ✅ Flywheel diagrams
- ✅ Story slides
- ✅ Slide cards

**Why**: CSS provides better styling control, simpler code, easier maintenance

### 2. **Template-Based Graphics**
- ✅ Graphics that use templates
- ✅ Consistent styling requirements
- ✅ Brand consistency needs
- ✅ Style variations

**Why**: CSS templates are easier to manage and modify

### 3. **Text-Heavy Graphics**
- ✅ Graphics with lots of text
- ✅ Typography-focused layouts
- ✅ Text wrapping needs
- ✅ Responsive text sizing

**Why**: CSS handles typography better than SVG.js

### 4. **Simple Shapes**
- ✅ Rectangles
- ✅ Circles
- ✅ Basic rounded corners
- ✅ Simple borders

**Why**: CSS is simpler and more maintainable

### 5. **Layout & Spacing**
- ✅ Flexbox layouts
- ✅ Grid layouts
- ✅ Responsive spacing
- ✅ Alignment needs

**Why**: CSS layout systems are more powerful

### 6. **Box Shadows & Effects**
- ✅ Drop shadows
- ✅ Hover effects
- ✅ Transitions
- ✅ CSS filters

**Why**: CSS effects are easier to apply and maintain

### 7. **Maintainability Priority**
- ✅ Team familiarity with CSS
- ✅ Easy style updates
- ✅ Consistent with existing codebase
- ✅ Lower complexity

**Why**: HTML/CSS is more familiar and maintainable

## Decision Tree

```
Start: What type of graphic?

├─ Is it a standard diagram type?
│  ├─ YES → Use HTML/CSS ✅
│  └─ NO → Continue...
│
├─ Does it need custom shapes/paths?
│  ├─ YES → Use SVG.js ✅
│  └─ NO → Continue...
│
├─ Does it need complex curves/beziers?
│  ├─ YES → Use SVG.js ✅
│  └─ NO → Continue...
│
├─ Is it a creative/artistic illustration?
│  ├─ YES → Use SVG.js ✅
│  └─ NO → Continue...
│
├─ Does it need advanced gradients/effects?
│  ├─ YES → Use SVG.js ✅
│  └─ NO → Continue...
│
├─ Does it need animation?
│  ├─ YES → Use SVG.js ✅
│  └─ NO → Continue...
│
└─ Default → Use HTML/CSS ✅
```

## Examples

### ✅ Use SVG.js

**Automation Paradox Hero Canvas**
- Custom illustration
- Complex paths and curves
- Creative visualization
- Not a standard diagram type

**Custom Game Board**
- Winding paths
- Custom tile shapes
- Complex path calculations
- Artistic design

**Animated Progress Indicator**
- Animation requirements
- Custom shapes
- Dynamic updates

### ✅ Use HTML/CSS

**Cycle Diagram**
- Standard diagram type
- Simple rectangles/circles
- Text-heavy
- Template-based

**Comparison Diagram**
- Standard layout
- Text-focused
- CSS flexbox works perfectly
- Easy to style

**Story Slide**
- Template-based
- Typography-focused
- Standard layout
- CSS handles it well

## Code Complexity Comparison

### HTML/CSS (Simple)
```python
def generate_cycle_diagram(steps):
    html = f"""
    <div class="cycle-container">
        {generate_steps_html(steps)}
    </div>
    """
    return wrap_html(html, css)
```

### SVG.js (More Complex)
```python
def generate_cycle_diagram_svg(steps):
    code = """
    const centerX = width/2;
    const centerY = height/2;
    // ... complex calculations ...
    for (let i = 0; i < steps; i++) {
        const angle = angleStep * i;
        const x = centerX + Math.cos(angle) * radius;
        // ... more calculations ...
    }
    """
    return wrap_svg_code(code)
```

## Performance Considerations

- **HTML/CSS**: Faster to generate, simpler code
- **SVG.js**: More JavaScript execution, but still fast
- **Both**: Export to PNG equally well

## Maintenance Considerations

- **HTML/CSS**: Easier to modify, familiar to developers
- **SVG.js**: More complex, requires JavaScript knowledge
- **Both**: Can be reviewed by design review agent

## Quick Decision Helper

Use the helper function for programmatic decisions:

```python
from modern_graphics.svg_decision_helper import should_use_svg_js, get_recommendation_reason

# Quick check
if should_use_svg_js('cycle'):
    # Use SVG.js
    pass
else:
    # Use HTML/CSS
    pass

# Get detailed reasoning
rec = get_recommendation_reason(
    'hero_canvas',
    is_creative_illustration=True,
    has_complex_paths=True
)
print(rec['recommended_approach'])  # "SVG.js"
print(rec['reason'])  # Detailed explanation
```

## Summary

**Use SVG.js when you need:**
- Custom illustrations
- Complex shapes/paths
- Advanced visual effects
- Animation
- Mathematical precision

**Use HTML/CSS when you need:**
- Standard diagrams
- Template-based graphics
- Text-heavy layouts
- Simple shapes
- Easy maintenance

**Default**: Use HTML/CSS unless SVG.js provides clear advantages.

## Quick Reference

```python
# Standard diagrams → HTML/CSS
cycle, comparison, timeline, grid, flywheel, story_slide, slide_card

# Custom illustrations → SVG.js
hero_canvas, custom_illustration, freeform, game_board, creative_visuals
```
