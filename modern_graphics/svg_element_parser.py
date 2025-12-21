"""Parse SVG.js code to extract visual elements for review"""

import re
import math
from typing import List, Dict, Optional, Tuple


class VariableTracker:
    """Track variable assignments in SVG.js code"""
    
    def __init__(self):
        self.variables = {}  # All variables
        self.color_variables = {}  # Color variables specifically
        self.color_objects = {}  # Color objects like {primary: '#6366F1', ...}
    
    def parse_variables(self, code: str):
        """Parse all variable assignments"""
        # Pattern: const/let/var name = value
        pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*([^;\n]+)'
        
        for match in re.finditer(pattern, code):
            var_name = match.group(1).strip()
            var_value = match.group(2).strip()
            
            # Remove comments
            var_value = re.sub(r'//.*$', '', var_value).strip()
            
            # Check if it's a color
            if self._is_color_value(var_value):
                self.color_variables[var_name] = self._parse_color(var_value)
            else:
                # Try to parse as number
                num_value = self._try_parse_number(var_value)
                if num_value is not None:
                    self.variables[var_name] = num_value
                else:
                    self.variables[var_name] = var_value
        
        # Parse color objects
        self._parse_color_objects(code)
    
    def _is_color_value(self, value: str) -> bool:
        """Check if value looks like a color"""
        value = value.strip().strip("'\"")
        # Hex colors
        if re.match(r'^#[0-9A-Fa-f]{3,6}$', value):
            return True
        # RGB/RGBA
        if re.match(r'^rgba?\(', value):
            return True
        # Named colors (basic check)
        named_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'white', 'gray', 'grey']
        if value.lower() in named_colors:
            return True
        return False
    
    def _parse_color(self, value: str) -> str:
        """Parse and normalize color value"""
        value = value.strip().strip("'\"")
        # Ensure hex colors start with #
        if re.match(r'^[0-9A-Fa-f]{3,6}$', value):
            return '#' + value
        return value
    
    def _try_parse_number(self, value: str) -> Optional[float]:
        """Try to parse value as number"""
        value = value.strip().strip("'\"")
        try:
            return float(value)
        except ValueError:
            # Try simple expressions like "1000 / 2"
            if '/' in value:
                parts = value.split('/')
                if len(parts) == 2:
                    try:
                        num = float(parts[0].strip())
                        den = float(parts[1].strip())
                        return num / den
                    except ValueError:
                        pass
            return None
    
    def _parse_color_objects(self, code: str):
        """Parse color object definitions"""
        # Pattern: const colors = {primary: '#6366F1', forward: '#10B981', ...}
        pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*\{([^}]+)\}'
        
        for match in re.finditer(pattern, code):
            obj_name = match.group(1)
            obj_content = match.group(2)
            
            # Parse properties
            props = {}
            # Handle both key: value and 'key': value formats
            prop_pattern = r'(?:^|,)\s*(?:[\'"]?(\w+)[\'"]?\s*:\s*[\'"]?([^\'",}]+)[\'"]?)'
            for prop_match in re.finditer(prop_pattern, obj_content):
                prop_name = prop_match.group(1).strip()
                prop_value = prop_match.group(2).strip().strip("'\"")
                if self._is_color_value(prop_value):
                    props[prop_name] = self._parse_color(prop_value)
            
            if props:
                self.color_objects[obj_name] = props
    
    def resolve_color(self, expression: str) -> Optional[str]:
        """Resolve color from variable or expression"""
        expression = expression.strip().strip("'\"")
        
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
                obj_name = parts[0].strip()
                prop_name = parts[1].strip()
                if obj_name in self.color_objects:
                    obj = self.color_objects[obj_name]
                    if prop_name in obj:
                        return obj[prop_name]
        
        return None


class ExpressionParser:
    """Parse JavaScript expressions to extract numeric values"""
    
    def __init__(self, context: Dict[str, float]):
        self.context = context
    
    def parse(self, expr: str) -> Optional[float]:
        """Parse expression with variable context"""
        expr = expr.strip()
        
        # Try direct float
        try:
            return float(expr)
        except ValueError:
            pass
        
        # Handle variables
        if expr in self.context:
            return self.context[expr]
        
        # Handle simple arithmetic: x + 10, x - 5, x * 2, x / 2
        # Addition
        add_match = re.match(r'(\w+)\s*\+\s*(\d+(?:\.\d+)?)', expr)
        if add_match:
            var_name = add_match.group(1)
            num = float(add_match.group(2))
            if var_name in self.context:
                return self.context[var_name] + num
        
        # Subtraction
        sub_match = re.match(r'(\w+)\s*-\s*(\d+(?:\.\d+)?)', expr)
        if sub_match:
            var_name = sub_match.group(1)
            num = float(sub_match.group(2))
            if var_name in self.context:
                return self.context[var_name] - num
        
        # Multiplication
        mult_match = re.match(r'(\w+)\s*\*\s*(\d+(?:\.\d+)?)', expr)
        if mult_match:
            var_name = mult_match.group(1)
            num = float(mult_match.group(2))
            if var_name in self.context:
                return self.context[var_name] * num
        
        # Division: var / 2
        div_match = re.match(r'(\w+)\s*/\s*(\d+(?:\.\d+)?)', expr)
        if div_match:
            var_name = div_match.group(1)
            num = float(div_match.group(2))
            if var_name in self.context:
                return self.context[var_name] / num
        
        # Handle: value - var/2 (like x - stepSize/2)
        complex_match = re.match(r'(\w+)\s*-\s*(\w+)\s*/\s*(\d+)', expr)
        if complex_match:
            var1 = complex_match.group(1)
            var2 = complex_match.group(2)
            divisor = float(complex_match.group(3))
            if var1 in self.context and var2 in self.context:
                return self.context[var1] - (self.context[var2] / divisor)
        
        # Handle: value + var/2
        complex_add_match = re.match(r'(\w+)\s*\+\s*(\w+)\s*/\s*(\d+)', expr)
        if complex_add_match:
            var1 = complex_add_match.group(1)
            var2 = complex_add_match.group(2)
            divisor = float(complex_add_match.group(3))
            if var1 in self.context and var2 in self.context:
                return self.context[var1] + (self.context[var2] / divisor)
        
        return None


class SVGElementParser:
    """Parse SVG.js code to extract element information"""
    
    def __init__(self):
        self.variable_tracker = VariableTracker()
        self.context = {}
    
    def parse(self, svg_code: str) -> List[Dict]:
        """
        Parse SVG.js code and extract visual elements
        
        Args:
            svg_code: JavaScript code using SVG.js
        
        Returns:
            List of element dictionaries with type, position, size, color, etc.
        """
        # Step 1: Build context (extract common variables)
        self.context = self._build_context(svg_code)
        
        # Step 2: Track variables (including colors)
        self.variable_tracker.parse_variables(svg_code)
        
        # Step 3: Parse elements with enhanced parsing
        elements = []
        
        # Parse circles (enhanced)
        circles = self._parse_circles_enhanced(svg_code)
        elements.extend(circles)
        
        # Parse rectangles (enhanced)
        rectangles = self._parse_rectangles_enhanced(svg_code)
        elements.extend(rectangles)
        
        # Parse text (enhanced)
        text_elements = self._parse_text_enhanced(svg_code)
        elements.extend(text_elements)
        
        # Parse paths/lines
        paths = self._parse_paths_enhanced(svg_code)
        elements.extend(paths)
        
        # Step 4: Resolve colors in elements
        elements = self._resolve_colors(elements)
        
        return elements
    
    def _build_context(self, code: str) -> Dict[str, float]:
        """Build variable context from code"""
        context = {}
        
        # Common canvas variables (defaults)
        context['canvasWidth'] = 1000
        context['canvasHeight'] = 500
        context['centerX'] = 500  # canvasWidth / 2
        context['centerY'] = 250  # canvasHeight / 2
        
        # Parse variable assignments to build context
        pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*([^;\n]+)'
        for match in re.finditer(pattern, code):
            var_name = match.group(1).strip()
            var_value = match.group(2).strip()
            
            # Remove comments
            var_value = re.sub(r'//.*$', '', var_value).strip()
            
            # Try to evaluate
            expr_parser = ExpressionParser(context)
            value = expr_parser.parse(var_value)
            if value is not None:
                context[var_name] = value
        
        # Update centerX/centerY if canvasWidth/Height were parsed
        if 'canvasWidth' in context:
            context['centerX'] = context['canvasWidth'] / 2
        if 'canvasHeight' in context:
            context['centerY'] = context['canvasHeight'] / 2
        
        return context
    
    def _parse_circles_enhanced(self, code: str) -> List[Dict]:
        """Parse circle elements with enhanced variable resolution"""
        circles = []
        expr_parser = ExpressionParser(self.context)
        
        # Pattern: draw.circle(radius).move(x, y)...
        # Enhanced to handle variables in radius
        pattern = r'draw\.circle\(([^)]+)\)\.move\(([^,]+),\s*([^)]+)\)'
        
        for match in re.finditer(pattern, code):
            radius_expr = match.group(1).strip()
            x_expr = match.group(2).strip()
            y_expr = match.group(3).strip()
            
            # Resolve expressions
            radius = expr_parser.parse(radius_expr) or self._parse_value(radius_expr)
            x = expr_parser.parse(x_expr) or self._parse_value(x_expr)
            y = expr_parser.parse(y_expr) or self._parse_value(y_expr)
            
            # Extract color (enhanced)
            color = self._extract_color_enhanced(code, match.end())
            
            circles.append({
                'type': 'circle',
                'position': {'x': x, 'y': y},
                'size': radius * 2,  # Diameter
                'radius': radius,
                'color': color,
                'element_type': 'shape'
            })
        
        return circles
    
    def _parse_rectangles_enhanced(self, code: str) -> List[Dict]:
        """Parse rectangle elements with enhanced variable resolution"""
        rectangles = []
        expr_parser = ExpressionParser(self.context)
        
        # Pattern: draw.rect(width, height).move(x, y)...
        pattern = r'draw\.rect\(([^,]+),\s*([^)]+)\)\.move\(([^,]+),\s*([^)]+)\)'
        
        for match in re.finditer(pattern, code):
            width_expr = match.group(1).strip()
            height_expr = match.group(2).strip()
            x_expr = match.group(3).strip()
            y_expr = match.group(4).strip()
            
            # Resolve expressions
            width = expr_parser.parse(width_expr) or self._parse_value(width_expr)
            height = expr_parser.parse(height_expr) or self._parse_value(height_expr)
            x = expr_parser.parse(x_expr) or self._parse_value(x_expr)
            y = expr_parser.parse(y_expr) or self._parse_value(y_expr)
            
            # Extract color (enhanced)
            color = self._extract_color_enhanced(code, match.end())
            
            rectangles.append({
                'type': 'rectangle',
                'position': {'x': x + width/2, 'y': y + height/2},  # Center
                'size': (width, height),
                'width': width,
                'height': height,
                'color': color,
                'element_type': 'shape'
            })
        
        return rectangles
    
    def _parse_text_enhanced(self, code: str) -> List[Dict]:
        """Parse text elements with enhanced variable resolution"""
        text_elements = []
        expr_parser = ExpressionParser(self.context)
        
        # Pattern: draw.text('...').move(x, y)...
        pattern = r"draw\.text\(['\"]([^'\"]+)['\"]\)\.move\(([^,]+),\s*([^)]+)\)"
        
        for match in re.finditer(pattern, code):
            text = match.group(1)
            x_expr = match.group(2).strip()
            y_expr = match.group(3).strip()
            
            # Resolve expressions
            x = expr_parser.parse(x_expr) or self._parse_value(x_expr)
            y = expr_parser.parse(y_expr) or self._parse_value(y_expr)
            
            # Try to extract font size
            font_size = self._extract_font_size_after(code, match.end())
            
            # Extract color (enhanced)
            color = self._extract_color_enhanced(code, match.end())
            
            # Estimate size based on text length and font size
            estimated_width = len(text) * (font_size or 12) * 0.6
            estimated_height = font_size or 12
            
            text_elements.append({
                'type': 'text',
                'position': {'x': x, 'y': y},
                'size': (estimated_width, estimated_height),
                'content': text,
                'font_size': font_size,
                'color': color,
                'element_type': 'text'
            })
        
        return text_elements
    
    def _parse_paths_enhanced(self, code: str) -> List[Dict]:
        """Parse path/line elements with enhanced variable resolution"""
        paths = []
        expr_parser = ExpressionParser(self.context)
        
        # Pattern: draw.line(x1, y1, x2, y2)...
        pattern = r'draw\.line\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)'
        
        for match in re.finditer(pattern, code):
            x1_expr = match.group(1).strip()
            y1_expr = match.group(2).strip()
            x2_expr = match.group(3).strip()
            y2_expr = match.group(4).strip()
            
            # Resolve expressions
            x1 = expr_parser.parse(x1_expr) or self._parse_value(x1_expr)
            y1 = expr_parser.parse(y1_expr) or self._parse_value(y1_expr)
            x2 = expr_parser.parse(x2_expr) or self._parse_value(x2_expr)
            y2 = expr_parser.parse(y2_expr) or self._parse_value(y2_expr)
            
            # Extract color from stroke
            color = self._extract_stroke_color(code, match.end())
            
            # Calculate center and bounding box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            paths.append({
                'type': 'line',
                'position': {'x': center_x, 'y': center_y},
                'size': (width, height),
                'points': [(x1, y1), (x2, y2)],
                'color': color,
                'element_type': 'connection'
            })
        
        return paths
    
    def _parse_value(self, value_str: str) -> float:
        """Parse a numeric value (handles variables, calculations, etc.)"""
        value_str = value_str.strip()
        
        # Try direct float
        try:
            return float(value_str)
        except ValueError:
            pass
        
        # Try to extract number from expressions like "centerX", "x + 10", etc.
        # For now, return 0 as fallback (could be improved with AST parsing)
        numbers = re.findall(r'\d+\.?\d*', value_str)
        if numbers:
            return float(numbers[0])
        
        return 0.0
    
    def _extract_color_enhanced(self, code: str, start_pos: int) -> Optional[str]:
        """Extract color from .fill() calls with variable resolution"""
        # Look for .fill('color'), .fill("#color"), or .fill(colorVariable)
        # Pattern 1: Direct color string
        pattern1 = r'\.fill\([\'"](#?[A-Za-z0-9]+)[\'"]\)'
        match1 = re.search(pattern1, code[start_pos:start_pos+300])
        if match1:
            color_expr = match1.group(1)
            # Try to resolve from variables
            resolved = self.variable_tracker.resolve_color(color_expr)
            return resolved or color_expr
        
        # Pattern 2: Variable reference .fill(colorVariable)
        pattern2 = r'\.fill\((\w+)\)'
        match2 = re.search(pattern2, code[start_pos:start_pos+300])
        if match2:
            var_name = match2.group(1)
            resolved = self.variable_tracker.resolve_color(var_name)
            return resolved
        
        return None
    
    def _extract_stroke_color(self, code: str, start_pos: int) -> Optional[str]:
        """Extract color from .stroke() calls"""
        # Look for .stroke({color: '...'})
        pattern = r'\.stroke\(\{[^}]*color:\s*[\'"]?([^\'",}]+)[\'"]?'
        match = re.search(pattern, code[start_pos:start_pos+300])
        if match:
            color_expr = match.group(1).strip().strip("'\"")
            resolved = self.variable_tracker.resolve_color(color_expr)
            return resolved or color_expr
        return None
    
    def _resolve_colors(self, elements: List[Dict]) -> List[Dict]:
        """Resolve color variables in elements"""
        for elem in elements:
            if 'color' in elem and elem['color']:
                resolved = self.variable_tracker.resolve_color(elem['color'])
                if resolved:
                    elem['color'] = resolved
        return elements
    
    def _extract_font_size_after(self, code: str, start_pos: int) -> Optional[int]:
        """Extract font size from .font() calls"""
        # Look for .font({size: 24})
        pattern = r'\.font\(\{[^}]*size:\s*(\d+)'
        match = re.search(pattern, code[start_pos:start_pos+200])
        if match:
            return int(match.group(1))
        return None
