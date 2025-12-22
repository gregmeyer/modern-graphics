# Plan: Adding svg.js Library Integration

## Overview
Add the `@svgdotjs/svg.js` library to enable programmatic SVG manipulation in generated graphics. This will allow for dynamic SVG generation, animations, and more complex visualizations beyond static HTML/CSS.

## Current State
- Python project that generates HTML/CSS graphics
- Uses Playwright to render HTML and export to PNG
- Currently generates SVG as static HTML strings
- No JavaScript dependencies currently managed

## Integration Strategy

### Option 1: CDN Approach (Recommended for MVP)
- Include svg.js via CDN in generated HTML
- Simplest to implement, no build step required
- Works immediately with existing Playwright rendering
- **Pros**: Fast to implement, no build complexity
- **Cons**: Requires internet connection for rendering

### Option 2: Bundled Approach (Better for production)
- Install via npm, bundle with project
- Copy bundled file to Python package
- Include local file in generated HTML
- **Pros**: Works offline, version controlled
- **Cons**: Requires npm build step, larger repo

## Implementation Plan

### Phase 1: Setup & Installation

1. **Initialize npm/package.json**
   - Create `package.json` in project root
   - Add `@svgdotjs/svg.js` as dependency
   - Add npm scripts for building if needed

2. **Install Dependencies**
   ```bash
   npm install @svgdotjs/svg.js
   ```

3. **Update .gitignore**
   - Add `node_modules/`
   - Add `package-lock.json` (optional, depending on preference)

### Phase 2: Integration

4. **Create SVG Utilities Module**
   - File: `modern_graphics/svg_utils.py`
   - Helper functions to generate SVG.js initialization code
   - Python wrappers for common SVG.js operations
   - Example:
     ```python
     def generate_svg_js_init(width: int, height: int) -> str:
         """Generate JavaScript code to initialize SVG.js"""
         return f"""
         <script>
         const draw = SVG().addTo('#svg-container').size({width}, {height});
         </script>
         """
     ```

5. **Update BaseGenerator**
   - Modify `_wrap_html()` method to include svg.js library
   - Add optional parameter to enable SVG.js support
   - Include via CDN: `<script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js@latest"></script>`
   - Or include local bundle if using Option 2

6. **Add Configuration**
   - Add `use_svg_js: bool = False` parameter to `BaseGenerator.__init__()`
   - Only include library when needed to keep HTML lightweight

### Phase 3: Python Helpers

7. **Create Python-to-SVG.js Bridge**
   - Functions to generate SVG.js code from Python data structures
   - Example:
     ```python
     def create_svg_circle(x: int, y: int, radius: int, color: str) -> str:
         """Generate SVG.js code to create a circle"""
         return f'draw.circle({radius}).move({x}, {y}).fill("{color}")'
     ```

8. **Add Convenience Methods**
   - Helper methods in `ModernGraphicsGenerator` for common SVG operations
   - Methods that return JavaScript code strings to inject into HTML

### Phase 4: Examples & Documentation

9. **Create Example Script**
   - File: `scripts/svg_js_example.py`
   - Demonstrate basic SVG.js usage
   - Show how to create dynamic SVGs
   - Example use cases: animated diagrams, interactive elements

10. **Update Documentation**
    - Add section to README.md about SVG.js integration
    - Document Python helper functions
    - Provide code examples
    - Explain when to use SVG.js vs static SVG

## File Structure Changes

```
modern-graphics/
├── package.json                    # NEW: npm dependencies
├── node_modules/                   # NEW: npm packages (gitignored)
├── modern_graphics/
│   ├── svg_utils.py                # NEW: SVG.js utilities
│   ├── base.py                     # MODIFY: Add svg.js support
│   └── ...
├── scripts/
│   └── svg_js_example.py           # NEW: Example usage
└── .gitignore                      # MODIFY: Add node_modules
```

## Implementation Details

### CDN Integration (Phase 2, Step 5)
```python
def _wrap_html(self, content: str, styles: str, use_svg_js: bool = False) -> str:
    svg_js_script = ""
    if use_svg_js:
        svg_js_script = '<script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js@latest"></script>'
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    ...
    {svg_js_script}
</head>
<body>
{content}
</body>
</html>"""
```

### Python Helper Example
```python
# modern_graphics/svg_utils.py
def generate_svg_container(container_id: str, width: int, height: int) -> str:
    """Generate HTML container for SVG.js"""
    return f'<div id="{container_id}" style="width: {width}px; height: {height}px;"></div>'

def generate_svg_init_script(container_id: str, width: int, height: int) -> str:
    """Generate SVG.js initialization script"""
    return f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const draw = SVG().addTo('#{container_id}').size({width}, {height});
        window.svgDraw = draw; // Make available globally for custom scripts
    }});
    </script>
    """
```

## Testing Strategy

1. **Unit Tests**
   - Test SVG.js code generation helpers
   - Verify HTML includes library when enabled

2. **Integration Tests**
   - Generate HTML with SVG.js
   - Render with Playwright
   - Verify SVG elements are created correctly

3. **Example Validation**
   - Run example script
   - Verify PNG export includes SVG.js generated content

## Migration Path

- **Backward Compatible**: Existing code continues to work without changes
- **Opt-in**: SVG.js only included when explicitly enabled
- **Gradual Adoption**: Can migrate diagrams one at a time

## Next Steps After Implementation

1. Identify which diagram types would benefit from SVG.js
2. Migrate complex SVG generation to use SVG.js
3. Add animation support for interactive previews
4. Consider SVG.js plugins for advanced features

## Questions to Consider

1. **CDN vs Bundled**: Start with CDN for simplicity, migrate to bundled if needed?
2. **Version Pinning**: Pin specific version or use latest?
3. **TypeScript**: Add TypeScript definitions for better IDE support?
4. **Build Process**: Add npm build step to CI/CD?

## Estimated Effort

- Phase 1 (Setup): 30 minutes
- Phase 2 (Integration): 1-2 hours
- Phase 3 (Helpers): 2-3 hours
- Phase 4 (Examples/Docs): 1-2 hours
- **Total**: ~5-8 hours
