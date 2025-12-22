"""Parse SVG.js or raw SVG code to extract visual elements for review"""

import re
import math
import xml.etree.ElementTree as ET
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
        """Parse expression with variable context, handling Math.max/min and nested expressions"""
        expr = expr.strip()
        
        # Try direct float
        try:
            return float(expr)
        except ValueError:
            pass
        
        # Handle variables
        if expr in self.context:
            return self.context[expr]
        
        # Handle Math.max() and Math.min() - recursively parse arguments
        # Pattern: Math.max(arg1, arg2, ...) or Math.min(arg1, arg2, ...)
        math_max_match = re.match(r'Math\.max\(([^)]+)\)', expr)
        if math_max_match:
            args_str = math_max_match.group(1)
            args = self._parse_comma_separated_args(args_str)
            if args:
                values = [v for v in args if v is not None]
                if values:
                    return max(values)
        
        math_min_match = re.match(r'Math\.min\(([^)]+)\)', expr)
        if math_min_match:
            args_str = math_min_match.group(1)
            args = self._parse_comma_separated_args(args_str)
            if args:
                values = [v for v in args if v is not None]
                if values:
                    return min(values)
        
        # Handle nested Math calls: Math.max(x, Math.min(y, z))
        nested_max_min_match = re.match(r'Math\.max\(([^,]+),\s*Math\.min\(([^)]+)\)\)', expr)
        if nested_max_min_match:
            arg1 = self.parse(nested_max_min_match.group(1))
            arg2_str = nested_max_min_match.group(2)
            arg2_args = self._parse_comma_separated_args(arg2_str)
            if arg1 is not None and arg2_args:
                arg2_values = [v for v in arg2_args if v is not None]
                if arg2_values:
                    arg2 = min(arg2_values)
                    return max(arg1, arg2)
        
        nested_min_max_match = re.match(r'Math\.min\(([^,]+),\s*Math\.max\(([^)]+)\)\)', expr)
        if nested_min_max_match:
            arg1 = self.parse(nested_min_max_match.group(1))
            arg2_str = nested_min_max_match.group(2)
            arg2_args = self._parse_comma_separated_args(arg2_str)
            if arg1 is not None and arg2_args:
                arg2_values = [v for v in arg2_args if v is not None]
                if arg2_values:
                    arg2 = max(arg2_values)
                    return min(arg1, arg2)
        
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
        
        # Handle complex expressions: var1 - var2, var1 + var2, var1 * var2, var1 / var2
        var_op_var_match = re.match(r'(\w+)\s*([+\-*/])\s*(\w+)', expr)
        if var_op_var_match:
            var1_name = var_op_var_match.group(1)
            op = var_op_var_match.group(2)
            var2_name = var_op_var_match.group(3)
            if var1_name in self.context and var2_name in self.context:
                val1 = self.context[var1_name]
                val2 = self.context[var2_name]
                if op == '+':
                    return val1 + val2
                elif op == '-':
                    return val1 - val2
                elif op == '*':
                    return val1 * val2
                elif op == '/':
                    return val1 / val2 if val2 != 0 else None
        
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
        
        # Handle expressions like: width - padding - nodeRadius
        multi_sub_match = re.match(r'(\w+)\s*-\s*(\w+)\s*-\s*(\w+)', expr)
        if multi_sub_match:
            var1 = multi_sub_match.group(1)
            var2 = multi_sub_match.group(2)
            var3 = multi_sub_match.group(3)
            if var1 in self.context and var2 in self.context and var3 in self.context:
                return self.context[var1] - self.context[var2] - self.context[var3]
        
        # Handle expressions like: width / 2
        div_var_match = re.match(r'(\w+)\s*/\s*(\d+)', expr)
        if div_var_match:
            var_name = div_var_match.group(1)
            divisor = float(div_var_match.group(2))
            if var_name in self.context:
                return self.context[var_name] / divisor
        
        return None
    
    def _parse_comma_separated_args(self, args_str: str) -> List[Optional[float]]:
        """Parse comma-separated arguments, handling nested expressions"""
        args = []
        # Split by commas, but be careful with nested parentheses
        depth = 0
        current_arg = []
        for char in args_str:
            if char == '(':
                depth += 1
                current_arg.append(char)
            elif char == ')':
                depth -= 1
                current_arg.append(char)
            elif char == ',' and depth == 0:
                # Split here
                arg_str = ''.join(current_arg).strip()
                if arg_str:
                    args.append(self.parse(arg_str))
                current_arg = []
            else:
                current_arg.append(char)
        
        # Add last argument
        if current_arg:
            arg_str = ''.join(current_arg).strip()
            if arg_str:
                args.append(self.parse(arg_str))
        
        return args


class SVGElementParser:
    """Parse SVG.js code to extract element information"""
    
    def __init__(self):
        self.variable_tracker = VariableTracker()
        self.context = {}
    
    def parse(self, svg_code: str) -> List[Dict]:
        """
        Parse SVG.js code (and fallback to raw SVG markup) to extract visual elements
        
        Args:
            svg_code: JavaScript code using SVG.js or inline SVG markup
        
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

        # Parse raw SVG markup if present (e.g., static tiles)
        raw_svg_elements = self._parse_raw_svg(svg_code)
        if raw_svg_elements:
            elements.extend(raw_svg_elements)
        
        # Step 4: Resolve colors in elements
        elements = self._resolve_colors(elements)
        
        return elements
    
    def _build_context(self, code: str) -> Dict[str, float]:
        """Build variable context from code, handling Math.max/min and complex expressions"""
        context = {}
        
        # Common canvas variables (defaults)
        context['canvasWidth'] = 1000
        context['canvasHeight'] = 500
        context['centerX'] = 500  # canvasWidth / 2
        context['centerY'] = 250  # canvasHeight / 2
        
        # Parse variable assignments to build context
        # Handle both single-line and multi-line assignments
        pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*([^;\n]+)'
        
        # Multiple passes to handle dependencies
        max_passes = 10
        for pass_num in range(max_passes):
            new_vars_found = False
            
            for match in re.finditer(pattern, code):
                var_name = match.group(1).strip()
                
                # Skip if already parsed
                if var_name in context:
                    continue
                
                var_value = match.group(2).strip()
                
                # Remove comments
                var_value = re.sub(r'//.*$', '', var_value).strip()
                
                # Try to evaluate with current context
                expr_parser = ExpressionParser(context)
                value = expr_parser.parse(var_value)
                if value is not None:
                    context[var_name] = value
                    new_vars_found = True
            
            # If no new variables found, we're done
            if not new_vars_found:
                break
        
        # Update centerX/centerY if canvasWidth/Height were parsed
        if 'canvasWidth' in context:
            context['centerX'] = context['canvasWidth'] / 2
        if 'canvasHeight' in context:
            context['centerY'] = context['canvasHeight'] / 2
        
        # Handle common patterns like width/2, height/2
        if 'width' in context:
            if 'centerX' not in context or context['centerX'] == 500:  # Only if not already set
                context['centerX'] = context['width'] / 2
        if 'height' in context:
            if 'centerY' not in context or context['centerY'] == 250:  # Only if not already set
                context['centerY'] = context['height'] / 2
        
        return context
    
    def _extract_balanced_expression(self, code: str, start_pos: int) -> Optional[Tuple[str, int]]:
        """Extract expression with balanced parentheses, returns (expression, end_pos)"""
        if start_pos >= len(code) or code[start_pos] != '(':
            return None
        
        depth = 0
        pos = start_pos
        start = pos + 1  # Skip opening '('
        
        while pos < len(code):
            if code[pos] == '(':
                depth += 1
            elif code[pos] == ')':
                depth -= 1
                if depth == 0:
                    return (code[start:pos], pos + 1)
            pos += 1
        
        return None
    
    def _parse_circles_enhanced(self, code: str) -> List[Dict]:
        """Parse circle elements with enhanced variable resolution, handling Math.max/min"""
        circles = []
        expr_parser = ExpressionParser(self.context)
        
        # Find all draw.circle(...) patterns and extract with balanced parentheses
        circle_pattern = r'draw\.circle\('
        for match in re.finditer(circle_pattern, code):
            # Extract radius expression (balanced parentheses)
            radius_result = self._extract_balanced_expression(code, match.end() - 1)
            if not radius_result:
                continue
            radius_expr, radius_end = radius_result
            
            # Look for .move( after the circle
            move_match = re.search(r'\.move\(', code[radius_end:radius_end+50])
            if not move_match:
                continue
            
            move_start = radius_end + move_match.start() + 6  # After ".move("
            
            # Extract x expression (may have nested parentheses)
            x_result = self._extract_balanced_expression(code, move_start - 1)
            if x_result:
                x_expr, x_end = x_result
            else:
                # Try simple pattern if no parentheses
                simple_x_match = re.search(r'^([^,)]+)', code[move_start:move_start+100])
                if simple_x_match:
                    x_expr = simple_x_match.group(1).strip()
                    x_end = move_start + simple_x_match.end()
                else:
                    continue
            
            # Extract y expression (after comma)
            comma_pos = code.find(',', x_end)
            if comma_pos == -1:
                continue
            
            y_start = comma_pos + 1
            y_result = self._extract_balanced_expression(code, y_start - 1)
            if y_result:
                y_expr, y_end = y_result
            else:
                # Try simple pattern
                simple_y_match = re.search(r'^([^,)]+)', code[y_start:y_start+100])
                if simple_y_match:
                    y_expr = simple_y_match.group(1).strip()
                    y_end = y_start + simple_y_match.end()
                else:
                    continue
            
            # Resolve expressions (handles Math.max/min)
            radius = expr_parser.parse(radius_expr.strip()) or self._parse_value(radius_expr.strip())
            x = expr_parser.parse(x_expr.strip()) or self._parse_value(x_expr.strip())
            y = expr_parser.parse(y_expr.strip()) or self._parse_value(y_expr.strip())
            
            # Extract color (enhanced)
            end_pos = y_end if y_result else y_start + len(y_expr)
            color = self._extract_color_enhanced(code, end_pos)
            
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
        """Parse rectangle elements with enhanced variable resolution, handling Math.max/min"""
        rectangles = []
        expr_parser = ExpressionParser(self.context)
        
        # Find all draw.rect(...) patterns and extract with balanced parentheses
        rect_pattern = r'draw\.rect\('
        for match in re.finditer(rect_pattern, code):
            # Extract width and height expressions (balanced parentheses)
            rect_result = self._extract_balanced_expression(code, match.end() - 1)
            if not rect_result:
                continue
            rect_expr, rect_end = rect_result
            
            # Parse width, height from "width, height"
            comma_pos = rect_expr.find(',')
            if comma_pos == -1:
                continue
            
            width_expr = rect_expr[:comma_pos].strip()
            height_expr = rect_expr[comma_pos + 1:].strip()
            
            # Look for .move( after the rect
            move_match = re.search(r'\.move\(', code[rect_end:rect_end+50])
            if not move_match:
                continue
            
            move_start = rect_end + move_match.start() + 6  # After ".move("
            
            # Extract x expression (may have nested parentheses)
            x_result = self._extract_balanced_expression(code, move_start - 1)
            if x_result:
                x_expr, x_end = x_result
            else:
                # Try simple pattern if no parentheses
                simple_x_match = re.search(r'^([^,)]+)', code[move_start:move_start+100])
                if simple_x_match:
                    x_expr = simple_x_match.group(1).strip()
                    x_end = move_start + simple_x_match.end()
                else:
                    continue
            
            # Extract y expression (after comma)
            comma_pos = code.find(',', x_end)
            if comma_pos == -1:
                continue
            
            y_start = comma_pos + 1
            y_result = self._extract_balanced_expression(code, y_start - 1)
            if y_result:
                y_expr, y_end = y_result
            else:
                # Try simple pattern
                simple_y_match = re.search(r'^([^,)]+)', code[y_start:y_start+100])
                if simple_y_match:
                    y_expr = simple_y_match.group(1).strip()
                    y_end = y_start + simple_y_match.end()
                else:
                    continue
            
            # Resolve expressions (handles Math.max/min)
            width = expr_parser.parse(width_expr) or self._parse_value(width_expr)
            height = expr_parser.parse(height_expr) or self._parse_value(height_expr)
            x = expr_parser.parse(x_expr) or self._parse_value(x_expr)
            y = expr_parser.parse(y_expr) or self._parse_value(y_expr)
            
            # Extract color (enhanced)
            end_pos = y_end if y_result else y_start + len(y_expr)
            color = self._extract_color_enhanced(code, end_pos)
            
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
        """Parse text elements with enhanced variable resolution, handling Math.max/min"""
        text_elements = []
        expr_parser = ExpressionParser(self.context)
        
        # Pattern: draw.text('...').move(x, y)...
        # Enhanced to handle Math.max/min in position expressions
        pattern = r"draw\.text\(['\"]([^'\"]+)['\"]\)\.move\(([^,()]+(?:\([^)]*\)[^,()]*)*),\s*([^,()]+(?:\([^)]*\)[^,()]*)*)\)"
        
        for match in re.finditer(pattern, code):
            text = match.group(1)
            x_expr = match.group(2).strip()
            y_expr = match.group(3).strip()
            
            # Resolve expressions (handles Math.max/min)
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
        """Parse path/line elements with enhanced variable resolution, handling Math.max/min"""
        paths = []
        expr_parser = ExpressionParser(self.context)
        
        # Pattern: draw.line(x1, y1, x2, y2)...
        # Enhanced to handle Math.max/min in coordinate expressions
        pattern = r'draw\.line\(([^,()]+(?:\([^)]*\)[^,()]*)*),\s*([^,()]+(?:\([^)]*\)[^,()]*)*),\s*([^,()]+(?:\([^)]*\)[^,()]*)*),\s*([^,()]+(?:\([^)]*\)[^,()]*)*)\)'
        
        for match in re.finditer(pattern, code):
            x1_expr = match.group(1).strip()
            y1_expr = match.group(2).strip()
            x2_expr = match.group(3).strip()
            y2_expr = match.group(4).strip()
            
            # Resolve expressions (handles Math.max/min)
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

    def _parse_raw_svg(self, svg_markup: str) -> List[Dict]:
        """Parse raw SVG markup when SVG.js code is not available"""
        if "<svg" not in svg_markup.lower():
            return []
        try:
            root = ET.fromstring(svg_markup)
        except ET.ParseError:
            return []
        
        elements: List[Dict] = []
        for node in root.iter():
            tag = self._strip_namespace(node.tag)
            style = self._parse_style_dict(node.attrib.get('style'))
            color = node.attrib.get('fill') or style.get('fill') or node.attrib.get('stroke') or style.get('stroke')
            if color:
                color = color.strip()
            
            if tag == 'rect':
                width = self._parse_svg_number(node.attrib.get('width'))
                height = self._parse_svg_number(node.attrib.get('height'))
                x = self._parse_svg_number(node.attrib.get('x'))
                y = self._parse_svg_number(node.attrib.get('y'))
                elements.append({
                    'type': 'rectangle',
                    'position': {'x': x + width / 2, 'y': y + height / 2},
                    'size': (width, height),
                    'width': width,
                    'height': height,
                    'color': color,
                    'element_type': 'shape'
                })
            elif tag == 'circle':
                radius = self._parse_svg_number(node.attrib.get('r'))
                cx = self._parse_svg_number(node.attrib.get('cx'))
                cy = self._parse_svg_number(node.attrib.get('cy'))
                elements.append({
                    'type': 'circle',
                    'position': {'x': cx, 'y': cy},
                    'size': radius * 2,
                    'radius': radius,
                    'color': color,
                    'element_type': 'shape'
                })
            elif tag == 'line':
                x1 = self._parse_svg_number(node.attrib.get('x1'))
                y1 = self._parse_svg_number(node.attrib.get('y1'))
                x2 = self._parse_svg_number(node.attrib.get('x2'))
                y2 = self._parse_svg_number(node.attrib.get('y2'))
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                elements.append({
                    'type': 'line',
                    'position': {'x': center_x, 'y': center_y},
                    'size': (abs(x2 - x1), abs(y2 - y1)),
                    'points': [(x1, y1), (x2, y2)],
                    'color': color,
                    'element_type': 'connection'
                })
            elif tag == 'polyline':
                points = self._parse_svg_points(node.attrib.get('points', ''))
                if len(points) >= 2:
                    x1, y1 = points[0]
                    x2, y2 = points[-1]
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    elements.append({
                        'type': 'line',
                        'position': {'x': center_x, 'y': center_y},
                        'size': (abs(x2 - x1), abs(y2 - y1)),
                        'points': points,
                        'color': color,
                        'element_type': 'connection'
                    })
            elif tag == 'path':
                d = node.attrib.get('d', '')
                elements.append({
                    'type': 'path',
                    'position': {'x': 0, 'y': 0},
                    'size': (0, 0),
                    'path': d,
                    'color': color,
                    'element_type': 'shape'
                })
            elif tag == 'text':
                text_value = ''.join(node.itertext()).strip()
                if not text_value:
                    continue
                x = self._parse_svg_number(node.attrib.get('x', '0'))
                y = self._parse_svg_number(node.attrib.get('y', '0'))
                font_size = self._parse_svg_number(node.attrib.get('font-size') or style.get('font-size'))
                if not font_size:
                    font_size = 14
                estimated_width = max(len(text_value), 1) * font_size * 0.55
                elements.append({
                    'type': 'text',
                    'text': text_value,
                    'position': {'x': x, 'y': y},
                    'size': (estimated_width, font_size),
                    'font_size': font_size,
                    'color': color,
                    'element_type': 'text'
                })
        return elements

    def _parse_style_dict(self, style_str: Optional[str]) -> Dict[str, str]:
        """Convert inline style attribute to dict"""
        if not style_str:
            return {}
        styles: Dict[str, str] = {}
        for part in style_str.split(';'):
            if ':' in part:
                key, value = part.split(':', 1)
                styles[key.strip()] = value.strip()
        return styles

    def _strip_namespace(self, tag: str) -> str:
        """Remove XML namespace from tag"""
        if '}' in tag:
            return tag.split('}', 1)[1].lower()
        return tag.lower()

    def _parse_svg_number(self, value: Optional[str]) -> float:
        """Parse numeric attribute from SVG (handles px units)"""
        if value is None:
            return 0.0
        value = value.strip()
        if value.endswith('px'):
            value = value[:-2]
        try:
            return float(value)
        except ValueError:
            numbers = re.findall(r'-?\d+\.?\d*', value)
            if numbers:
                try:
                    return float(numbers[0])
                except ValueError:
                    return 0.0
        return 0.0

    def _parse_svg_points(self, points_str: str) -> List[Tuple[float, float]]:
        """Parse points attribute (e.g., polyline) into coordinate tuples"""
        points: List[Tuple[float, float]] = []
        if not points_str:
            return points
        for raw_point in points_str.strip().split():
            if ',' in raw_point:
                x_str, y_str = raw_point.split(',', 1)
                points.append((self._parse_svg_number(x_str), self._parse_svg_number(y_str)))
        return points
