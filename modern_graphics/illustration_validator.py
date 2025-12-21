"""Tier 1: Built-in design validation for SVG.js illustrations"""

from typing import List, Dict, Tuple, Optional
import re
import math


class IllustrationValidator:
    """Lightweight design validation during generation"""
    
    def __init__(self, min_spacing: int = 20, min_size: int = 10, max_overlap_ratio: float = 0.1):
        """
        Initialize validator
        
        Args:
            min_spacing: Minimum spacing between elements (pixels)
            min_size: Minimum element size (pixels)
            max_overlap_ratio: Maximum allowed overlap ratio (0.0-1.0)
        """
        self.min_spacing = min_spacing
        self.min_size = min_size
        self.max_overlap_ratio = max_overlap_ratio
    
    def validate(self, elements: List[Dict], canvas_size: Tuple[int, int]) -> List[Dict]:
        """
        Validate illustration design
        
        Args:
            elements: List of element dictionaries with position and size info
            canvas_size: (width, height) of canvas
        
        Returns:
            List of issues found
        """
        issues = []
        
        # Check overlaps
        overlaps = self._detect_overlaps(elements)
        if overlaps:
            issues.append({
                'type': 'overlap',
                'elements': overlaps,
                'severity': 'high',
                'auto_fix': True,
                'message': f'Found {len(overlaps)} overlapping element pairs'
            })
        
        # Check spacing
        spacing_issues = self._check_spacing(elements)
        if spacing_issues:
            issues.append({
                'type': 'spacing',
                'details': spacing_issues,
                'severity': 'medium',
                'auto_fix': True,
                'message': f'Found {len(spacing_issues)} spacing violations'
            })
        
        # Check hierarchy
        hierarchy_score = self._check_hierarchy(elements)
        if hierarchy_score < 0.6:
            issues.append({
                'type': 'hierarchy',
                'score': hierarchy_score,
                'severity': 'medium',
                'auto_fix': False,
                'message': f'Weak visual hierarchy (score: {hierarchy_score:.2f})'
            })
        
        # Check boundaries
        boundary_issues = self._check_boundaries(elements, canvas_size)
        if boundary_issues:
            issues.append({
                'type': 'boundary',
                'details': boundary_issues,
                'severity': 'high',
                'auto_fix': True,
                'message': f'Found {len(boundary_issues)} elements outside canvas'
            })
        
        # Check minimum sizes
        size_issues = self._check_minimum_sizes(elements)
        if size_issues:
            issues.append({
                'type': 'size',
                'details': size_issues,
                'severity': 'low',
                'auto_fix': True,
                'message': f'Found {len(size_issues)} elements below minimum size'
            })
        
        return issues
    
    def _detect_overlaps(self, elements: List[Dict]) -> List[Tuple[int, int]]:
        """Detect overlapping elements"""
        overlaps = []
        
        for i, elem1 in enumerate(elements):
            if 'position' not in elem1 or 'size' not in elem1:
                continue
            
            for j, elem2 in enumerate(elements[i+1:], start=i+1):
                if 'position' not in elem2 or 'size' not in elem2:
                    continue
                
                if self._elements_overlap(elem1, elem2):
                    overlaps.append((i, j))
        
        return overlaps
    
    def _elements_overlap(self, elem1: Dict, elem2: Dict) -> bool:
        """Check if two elements overlap"""
        pos1 = elem1['position']
        pos2 = elem2['position']
        size1 = elem1['size']
        size2 = elem2['size']
        
        # Handle different position formats
        x1, y1 = self._get_center(pos1, size1)
        x2, y2 = self._get_center(pos2, size2)
        
        # Get bounding boxes
        w1, h1 = size1 if isinstance(size1, tuple) else (size1, size1)
        w2, h2 = size2 if isinstance(size2, tuple) else (size2, size2)
        
        r1 = max(w1, h1) / 2
        r2 = max(w2, h2) / 2
        
        # Calculate distance between centers
        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
        # Check if circles overlap (conservative for rectangles)
        return distance < (r1 + r2 - self.min_spacing)
    
    def _get_center(self, position: Dict, size) -> Tuple[float, float]:
        """Get center coordinates from position"""
        if 'x' in position and 'y' in position:
            return (position['x'], position['y'])
        elif 'center_x' in position and 'center_y' in position:
            return (position['center_x'], position['center_y'])
        else:
            # Default to (0, 0) if unknown
            return (0, 0)
    
    def _check_spacing(self, elements: List[Dict]) -> List[Dict]:
        """Check minimum spacing between elements"""
        spacing_issues = []
        
        for i, elem1 in enumerate(elements):
            if 'position' not in elem1:
                continue
            
            for j, elem2 in enumerate(elements[i+1:], start=i+1):
                if 'position' not in elem2:
                    continue
                
                distance = self._calculate_distance(elem1, elem2)
                if 0 < distance < self.min_spacing:
                    spacing_issues.append({
                        'element1': i,
                        'element2': j,
                        'distance': distance,
                        'required': self.min_spacing
                    })
        
        return spacing_issues
    
    def _calculate_distance(self, elem1: Dict, elem2: Dict) -> float:
        """Calculate distance between two elements"""
        pos1 = elem1['position']
        pos2 = elem2['position']
        size1 = elem1.get('size', 0)
        size2 = elem2.get('size', 0)
        
        x1, y1 = self._get_center(pos1, size1)
        x2, y2 = self._get_center(pos2, size2)
        
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def _check_hierarchy(self, elements: List[Dict]) -> float:
        """
        Check visual hierarchy
        
        Returns:
            Score from 0-1 (higher is better)
        """
        if len(elements) < 2:
            return 1.0  # Single element is fine
        
        sizes = []
        for elem in elements:
            if 'size' in elem:
                size = elem['size']
                if isinstance(size, tuple):
                    sizes.append(max(size))
                else:
                    sizes.append(size)
        
        if not sizes:
            return 0.5  # Can't determine hierarchy
        
        # Check size variation (hierarchy needs variation)
        size_variation = max(sizes) / min(sizes) if min(sizes) > 0 else 1.0
        
        # Good hierarchy: 2-5x size difference
        if 2.0 <= size_variation <= 5.0:
            return 1.0
        elif size_variation < 1.5:
            return 0.3  # Too similar
        elif size_variation > 10.0:
            return 0.7  # Too extreme
        else:
            return 0.8
    
    def _check_boundaries(self, elements: List[Dict], canvas_size: Tuple[int, int]) -> List[Dict]:
        """Check if elements are within canvas boundaries"""
        boundary_issues = []
        width, height = canvas_size
        
        for i, elem in enumerate(elements):
            if 'position' not in elem:
                continue
            
            pos = elem['position']
            size = elem.get('size', 0)
            
            x, y = self._get_center(pos, size)
            w, h = size if isinstance(size, tuple) else (size, size)
            
            # Check if element extends beyond boundaries
            if x - w/2 < 0 or x + w/2 > width or y - h/2 < 0 or y + h/2 > height:
                boundary_issues.append({
                    'element': i,
                    'position': (x, y),
                    'size': (w, h),
                    'canvas': (width, height)
                })
        
        return boundary_issues
    
    def _check_minimum_sizes(self, elements: List[Dict]) -> List[Dict]:
        """Check if elements meet minimum size requirements"""
        size_issues = []
        
        for i, elem in enumerate(elements):
            if 'size' not in elem:
                continue
            
            size = elem['size']
            if isinstance(size, tuple):
                min_dimension = min(size)
            else:
                min_dimension = size
            
            if min_dimension < self.min_size:
                size_issues.append({
                    'element': i,
                    'size': min_dimension,
                    'minimum': self.min_size
                })
        
        return size_issues
    
    def auto_fix(self, issues: List[Dict], elements: List[Dict], canvas_size: Tuple[int, int]) -> List[Dict]:
        """
        Automatically fix fixable issues
        
        Args:
            issues: List of issues from validate()
            elements: List of elements to fix
            canvas_size: Canvas dimensions
        
        Returns:
            Fixed elements list
        """
        fixed_elements = [elem.copy() for elem in elements]
        
        for issue in issues:
            if not issue.get('auto_fix', False):
                continue
            
            if issue['type'] == 'overlap':
                fixed_elements = self._fix_overlaps(fixed_elements, issue)
            elif issue['type'] == 'spacing':
                fixed_elements = self._fix_spacing(fixed_elements, issue)
            elif issue['type'] == 'boundary':
                fixed_elements = self._fix_boundaries(fixed_elements, issue, canvas_size)
            elif issue['type'] == 'size':
                fixed_elements = self._fix_sizes(fixed_elements, issue)
        
        return fixed_elements
    
    def _fix_overlaps(self, elements: List[Dict], issue: Dict) -> List[Dict]:
        """Fix overlapping elements by adjusting positions"""
        for i, j in issue['elements']:
            if i >= len(elements) or j >= len(elements):
                continue
            
            elem1 = elements[i]
            elem2 = elements[j]
            
            # Calculate separation needed
            pos1 = elem1['position']
            pos2 = elem2['position']
            size1 = elem1.get('size', 50)
            size2 = elem2.get('size', 50)
            
            x1, y1 = self._get_center(pos1, size1)
            x2, y2 = self._get_center(pos2, size2)
            
            # Calculate direction vector
            dx = x2 - x1
            dy = y2 - y1
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance == 0:
                # Same position, move one randomly
                dx, dy = 1, 0
            
            # Normalize
            dx /= distance
            dy /= distance
            
            # Calculate separation distance
            r1 = max(size1 if isinstance(size1, tuple) else (size1, size1)) / 2
            r2 = max(size2 if isinstance(size2, tuple) else (size2, size2)) / 2
            separation = r1 + r2 + self.min_spacing
            
            # Move elements apart
            move_distance = (separation - distance) / 2
            elements[i]['position'] = {'x': x1 - dx * move_distance, 'y': y1 - dy * move_distance}
            elements[j]['position'] = {'x': x2 + dx * move_distance, 'y': y2 + dy * move_distance}
        
        return elements
    
    def _fix_spacing(self, elements: List[Dict], issue: Dict) -> List[Dict]:
        """Fix spacing violations"""
        # Similar to overlap fixing
        return self._fix_overlaps(elements, {'elements': [(d['element1'], d['element2']) for d in issue['details']]})
    
    def _fix_boundaries(self, elements: List[Dict], issue: Dict, canvas_size: Tuple[int, int]) -> List[Dict]:
        """Fix elements outside canvas boundaries"""
        width, height = canvas_size
        
        for detail in issue['details']:
            idx = detail['element']
            if idx >= len(elements):
                continue
            
            elem = elements[idx]
            pos = elem['position']
            size = elem.get('size', 50)
            
            x, y = self._get_center(pos, size)
            w, h = size if isinstance(size, tuple) else (size, size)
            
            # Adjust position to keep within bounds
            new_x = max(w/2, min(width - w/2, x))
            new_y = max(h/2, min(height - h/2, y))
            
            elements[idx]['position'] = {'x': new_x, 'y': new_y}
        
        return elements
    
    def _fix_sizes(self, elements: List[Dict], issue: Dict) -> List[Dict]:
        """Fix elements below minimum size"""
        for detail in issue['details']:
            idx = detail['element']
            if idx >= len(elements):
                continue
            
            elem = elements[idx]
            if 'size' in elem:
                if isinstance(elem['size'], tuple):
                    elem['size'] = tuple(max(self.min_size, s) for s in elem['size'])
                else:
                    elem['size'] = max(self.min_size, elem['size'])
        
        return elements
