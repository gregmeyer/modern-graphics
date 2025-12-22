# Plan: Improve SVG Element Parser for Better Color & Position Extraction

## Current State

### What Works
- ✅ Basic parsing of circles, rectangles, text, lines
- ✅ Extracts simple numeric positions
- ✅ Extracts basic color information from `.fill()` calls
- ✅ Extracts font sizes from `.font()` calls

### Limitations
1. **Color Extraction**: Only finds colors immediately after `.fill()` - misses:
   - Colors defined in variables (`const color = '#6366F1'`)
   - Colors from objects (`colors.primary`)
   - Colors in stroke calls
   - Gradient colors
   - Opacity/transparency

2. **Position Parsing**: Only handles simple numbers - misses:
   - Variables (`centerX`, `x`, `y`)
   - Calculations (`x - size/2`, `centerX + radius`)
   - Expressions (`Math.cos(angle) * radius`)
   - Relative positions

3. **Size Parsing**: Limited to direct values - misses:
   - Variables (`stepSize`, `tileSize`)
   - Calculations (`size * 1.2`)
   - Conditional sizes

4. **Element Relationships**: Doesn't understand:
   - Groups and hierarchies
   - Transformations
   - Relative positioning

## Goals

1. **Extract colors from variables** - Parse `const color = '#6366F1'` and track usage
2. **Extract colors from objects** - Parse `colors.primary` from color objects
3. **Handle complex positions** - Parse calculations, variables, expressions
4. **Track element relationships** - Understand groups, hierarchies
5. **Better stroke color extraction** - Get colors from `.stroke()` calls
6. **Gradient color extraction** - Extract colors from gradients

## Implementation Plan

### Phase 1: Variable Tracking

#### 1.1 Create Variable Tracker
**File**: `modern_graphics/svg_element_parser.py` (new class)

```python
class VariableTracker:
    """Track variable assignments in SVG.js code"""
    
    def __init__(self):
        self.variables = {}
        self.color_variables = {}
    
    def parse_variables(self, code: str):
        """Parse all variable assignments"""
        # Pattern: const/let/var name = value
        patterns = [
            r'(?:const|let|var)\s+(\w+)\s*=\s*([^;]+)',
            r'(\w+)\s*=\s*([^;]+)',  # Assignment
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, code):
                var_name = match.group(1)
                var_value = match.group(2).strip()
                
                # Check if it's a color
                if self._is_color_value(var_value):
                    self.color_variables[var_name] = self._parse_color(var_value)
                else:
                    self.variables[var_name] = var_value
    
    def _is_color_value(self, value: str) -> bool:
        """Check if value looks like a color"""
        # Hex colors: #RGB, #RRGGBB
        # Named colors: 'red', 'blue'
        # RGB: rgb(...), rgba(...)
        return bool(re.search(r'#[\dA-Fa-f]{3,6}|rgba?\(|^\w+$', value))
    
    def resolve_color(self, expression: str) -> Optional[str]:
        """Resolve color from variable or expression"""
        # If direct color, return it
        if self._is_color_value(expression):
            return self._parse_color(expression)
        
        # If variable reference, look it up
        if expression in self.color_variables:
            return self.color_variables[expression]
        
        # If object property (colors.primary), resolve
        if '.' in expression:
            parts = expression.split('.')
            if len(parts) == 2:
                obj_name = parts[0]
                prop_name = parts[1]
                if obj_name in self.variables:
                    # Try to parse object definition
                    obj_def = self.variables[obj_name]
                    # Look for prop_name: 'color' pattern
                    # ...
        
        return None
```

#### 1.2 Parse Color Objects
```python
def _parse_color_object(self, code: str) -> Dict[str, str]:
    """Parse color object definitions like:
    const colors = {
        primary: '#6366F1',
        forward: '#10B981',
        ...
    }
    """
    color_objects = {}
    
    # Find object definitions
    pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*\{([^}]+)\}'
    for match in re.finditer(pattern, code):
        obj_name = match.group(1)
        obj_content = match.group(2)
        
        # Parse properties
        props = {}
        prop_pattern = r'(\w+):\s*([^,}]+)'
        for prop_match in re.finditer(prop_pattern, obj_content):
            prop_name = prop_match.group(1).strip()
            prop_value = prop_match.group(2).strip().strip("'\"")
            props[prop_name] = prop_value
        
        color_objects[obj_name] = props
    
    return color_objects
```

### Phase 2: Enhanced Position Parsing

#### 2.1 Create Expression Parser
```python
class ExpressionParser:
    """Parse JavaScript expressions to extract values"""
    
    def parse_expression(self, expr: str, context: Dict[str, float]) -> Optional[float]:
        """Parse expression with variable context"""
        # Simple cases first
        try:
            return float(expr)
        except ValueError:
            pass
        
        # Handle variables
        if expr.strip() in context:
            return context[expr.strip()]
        
        # Handle simple arithmetic
        # x + 10, x - 5, x * 2, x / 2
        patterns = [
            r'(\w+)\s*\+\s*(\d+(?:\.\d+)?)',
            r'(\w+)\s*-\s*(\d+(?:\.\d+)?)',
            r'(\w+)\s*\*\s*(\d+(?:\.\d+)?)',
            r'(\w+)\s*/\s*(\d+(?:\.\d+)?)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, expr)
            if match:
                var_name = match.group(1)
                num = float(match.group(2))
                
                if var_name in context:
                    if '+' in expr:
                        return context[var_name] + num
                    elif '-' in expr:
                        return context[var_name] - num
                    elif '*' in expr:
                        return context[var_name] * num
                    elif '/' in expr:
                        return context[var_name] / num
        
        # Handle division: size/2
        div_match = re.match(r'(\w+)\s*/\s*(\d+)', expr)
        if div_match:
            var_name = div_match.group(1)
            divisor = float(div_match.group(2))
            if var_name in context:
                return context[var_name] / divisor
        
        return None
```

#### 2.2 Build Context from Code
```python
def build_context(self, code: str) -> Dict[str, float]:
    """Build variable context from code"""
    context = {}
    
    # Extract common variables
    # canvasWidth, canvasHeight, centerX, centerY, radius, etc.
    common_vars = {
        'canvasWidth': 1000,
        'canvasHeight': 500,
        'centerX': 500,  # canvasWidth / 2
        'centerY': 250,  # canvasHeight / 2
    }
    
    # Parse variable assignments
    var_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*([^;]+)'
    for match in re.finditer(var_pattern, code):
        var_name = match.group(1)
        var_value = match.group(2).strip()
        
        # Try to evaluate simple expressions
        value = self._evaluate_simple_expression(var_value, common_vars)
        if value is not None:
            context[var_name] = value
    
    # Update common vars with parsed values
    context.update(common_vars)
    
    return context
```

### Phase 3: Enhanced Color Extraction

#### 3.1 Track Color Usage
```python
def _extract_all_colors(self, code: str) -> Dict[str, str]:
    """Extract all colors from code, including variables"""
    colors = {}
    
    # Step 1: Parse color variables
    tracker = VariableTracker()
    tracker.parse_variables(code)
    
    # Step 2: Parse color objects
    color_objects = self._parse_color_object(code)
    
    # Step 3: Extract direct color usage
    # .fill('#color'), .fill('color'), .fill(colorVariable)
    fill_pattern = r'\.fill\([\'"]([^\'"]+)[\'"]\)|\.fill\((\w+)\)'
    for match in re.finditer(fill_pattern, code):
        color_expr = match.group(1) or match.group(2)
        resolved = tracker.resolve_color(color_expr)
        if resolved:
            colors[color_expr] = resolved
    
    # Step 4: Extract stroke colors
    stroke_pattern = r'\.stroke\(\{[^}]*color:\s*[\'"]([^\'"]+)[\'"]'
    for match in re.finditer(stroke_pattern, code):
        color = match.group(1)
        colors[f'stroke_{len(colors)}'] = color
    
    return colors
```

#### 3.2 Map Colors to Elements
```python
def _map_colors_to_elements(self, code: str, elements: List[Dict]) -> List[Dict]:
    """Map extracted colors to elements"""
    # Extract all colors with their positions
    color_usage = self._extract_color_usage_positions(code)
    
    # Match colors to elements based on proximity in code
    for i, elem in enumerate(elements):
        # Find colors used near this element's code
        # (simplified - would need actual code position tracking)
        pass
    
    return elements
```

### Phase 4: Improved Element Extraction

#### 4.1 Enhanced Circle Parsing
```python
def _parse_circles_enhanced(self, code: str, context: Dict[str, float]) -> List[Dict]:
    """Enhanced circle parsing with variable resolution"""
    circles = []
    
    # Pattern: draw.circle(radius).move(x, y)...
    pattern = r'draw\.circle\(([^)]+)\)\.move\(([^,]+),\s*([^)]+)\)'
    
    for match in re.finditer(pattern, code):
        radius_expr = match.group(1).strip()
        x_expr = match.group(2).strip()
        y_expr = match.group(3).strip()
        
        # Resolve expressions
        parser = ExpressionParser()
        radius = parser.parse_expression(radius_expr, context) or 0
        x = parser.parse_expression(x_expr, context) or 0
        y = parser.parse_expression(y_expr, context) or 0
        
        # Extract color (with variable resolution)
        color = self._extract_color_enhanced(code, match.end(), context)
        
        circles.append({
            'type': 'circle',
            'position': {'x': x, 'y': y},
            'size': radius * 2,
            'radius': radius,
            'color': color,
            'element_type': 'shape'
        })
    
    return circles
```

#### 4.2 Handle Groups
```python
def _parse_groups(self, code: str) -> List[Dict]:
    """Parse group definitions and track element membership"""
    groups = []
    
    # Pattern: const group = draw.group()
    # Then elements added to group: group.circle(...)
    
    group_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*draw\.group\(\)'
    for match in re.finditer(group_pattern, code):
        group_name = match.group(1)
        groups.append({
            'name': group_name,
            'elements': []
        })
    
    # Find elements added to groups
    # group.circle(...), group.rect(...)
    for group in groups:
        pattern = rf'{group["name"]}\.(circle|rect|text)\(([^)]+)\)'
        # ... extract elements in group
    
    return groups
```

### Phase 5: Integration

#### 5.1 Enhanced Parser Class
```python
class EnhancedSVGElementParser(SVGElementParser):
    """Enhanced parser with variable tracking and expression parsing"""
    
    def __init__(self):
        super().__init__()
        self.variable_tracker = VariableTracker()
        self.expression_parser = ExpressionParser()
    
    def parse(self, svg_code: str) -> List[Dict]:
        """Enhanced parse with variable resolution"""
        # Step 1: Build context
        context = self._build_context(svg_code)
        
        # Step 2: Track variables
        self.variable_tracker.parse_variables(svg_code)
        
        # Step 3: Parse elements with context
        elements = []
        elements.extend(self._parse_circles_enhanced(svg_code, context))
        elements.extend(self._parse_rectangles_enhanced(svg_code, context))
        elements.extend(self._parse_text_enhanced(svg_code, context))
        
        # Step 4: Resolve colors
        elements = self._resolve_colors(elements, svg_code)
        
        return elements
    
    def _resolve_colors(self, elements: List[Dict], code: str) -> List[Dict]:
        """Resolve color variables in elements"""
        for elem in elements:
            if 'color' in elem and elem['color']:
                resolved = self.variable_tracker.resolve_color(elem['color'])
                if resolved:
                    elem['color'] = resolved
        return elements
```

## Implementation Roadmap

### Week 1: Variable Tracking
- [ ] Create `VariableTracker` class
- [ ] Parse `const/let/var` assignments
- [ ] Identify color variables
- [ ] Test with simple examples

### Week 2: Expression Parsing
- [ ] Create `ExpressionParser` class
- [ ] Handle simple arithmetic (+, -, *, /)
- [ ] Handle variable references
- [ ] Build context from code
- [ ] Test with calculations

### Week 3: Enhanced Color Extraction
- [ ] Extract colors from variables
- [ ] Parse color objects
- [ ] Extract stroke colors
- [ ] Map colors to elements
- [ ] Test color resolution

### Week 4: Enhanced Position Parsing
- [ ] Parse complex positions
- [ ] Handle calculations in positions
- [ ] Resolve variable references
- [ ] Test with real examples

### Week 5: Integration & Testing
- [ ] Integrate all enhancements
- [ ] Test with automation paradox illustration
- [ ] Measure improvement in review accuracy
- [ ] Document usage

## Success Metrics

1. **Color Extraction Rate**: % of colors correctly extracted (target: >90%)
2. **Position Accuracy**: % of positions correctly parsed (target: >85%)
3. **Review Score Improvement**: Better scores after parser improvements
4. **False Positive Rate**: Reduce false "no color found" issues

## Example: Before vs After

### Before (Current)
```javascript
const colorPrimary = '#6366F1';
draw.circle(50).move(centerX, centerY).fill(colorPrimary);
```
**Parsed**: No color found (misses variable)

### After (Improved)
```javascript
const colorPrimary = '#6366F1';
draw.circle(50).move(centerX, centerY).fill(colorPrimary);
```
**Parsed**: 
- Variable: `colorPrimary = '#6366F1'`
- Circle color: `#6366F1` (resolved from variable)
- Position: `x: 500, y: 250` (resolved `centerX`, `centerY`)

## Files to Modify

```
modern_graphics/
├── svg_element_parser.py          # MODIFY: Add enhancements
└── (new classes)
    ├── variable_tracker.py         # NEW: Track variables
    └── expression_parser.py        # NEW: Parse expressions
```

## Estimated Effort

- **Phase 1** (Variable Tracking): 4-6 hours
- **Phase 2** (Expression Parsing): 6-8 hours
- **Phase 3** (Color Extraction): 4-6 hours
- **Phase 4** (Position Parsing): 4-6 hours
- **Phase 5** (Integration): 3-4 hours
- **Testing**: 3-4 hours

**Total**: ~24-34 hours
