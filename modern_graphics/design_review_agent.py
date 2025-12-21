"""Tier 2: AI-powered design review agent for SVG.js illustrations"""

from typing import Dict, List, Optional, Tuple
from .env_config import get_openai_key
from .svg_element_parser import SVGElementParser


class DesignReviewAgent:
    """AI-powered design review agent"""
    
    def __init__(self):
        self.parser = SVGElementParser()
    
    def review(
        self,
        svg_code: str,
        design_spec: Optional[Dict] = None,
        canvas_size: Tuple[int, int] = (1000, 500)
    ) -> Dict:
        """
        Comprehensive design review using AI
        
        Args:
            svg_code: SVG.js JavaScript code
            design_spec: Optional design specification
            canvas_size: Canvas dimensions (width, height)
        
        Returns:
            Review dictionary with score, evaluation, and suggestions
        """
        # Parse elements from SVG code
        elements = self.parser.parse(svg_code)
        
        # Basic analysis (rule-based)
        basic_analysis = self._analyze_basic(elements, canvas_size)
        
        # AI-powered review
        ai_review = self._ai_review(svg_code, elements, canvas_size, design_spec)
        
        # Combine results
        overall_score = self._calculate_overall_score(basic_analysis, ai_review)
        
        return {
            'score': overall_score,
            'basic_analysis': basic_analysis,
            'ai_review': ai_review,
            'suggestions': self._generate_suggestions(basic_analysis, ai_review),
            'passed': overall_score >= 70,
            'elements_count': len(elements)
        }
    
    def _analyze_basic(self, elements: List[Dict], canvas_size: Tuple[int, int]) -> Dict:
        """Basic rule-based analysis"""
        if not elements:
            return {
                'hierarchy': {'score': 0, 'issues': ['No elements found']},
                'composition': {'score': 0, 'issues': ['Empty canvas']},
                'color': {'score': 50, 'issues': []},
                'spacing': {'score': 50, 'issues': []},
                'typography': {'score': 50, 'issues': []}
            }
        
        analysis = {
            'hierarchy': self._analyze_hierarchy(elements),
            'composition': self._analyze_composition(elements, canvas_size),
            'color': self._analyze_color(elements),
            'spacing': self._analyze_spacing(elements),
            'typography': self._analyze_typography(elements)
        }
        
        return analysis
    
    def _analyze_hierarchy(self, elements: List[Dict]) -> Dict:
        """Analyze visual hierarchy"""
        shapes = [e for e in elements if e.get('element_type') == 'shape']
        
        if len(shapes) < 2:
            return {'score': 70, 'issues': ['Need at least 2 elements for hierarchy']}
        
        # Check size variation
        sizes = []
        for elem in shapes:
            size = elem.get('size', 0)
            if isinstance(size, tuple):
                sizes.append(max(size))
            else:
                sizes.append(size)
        
        if not sizes:
            return {'score': 50, 'issues': ['Cannot determine sizes']}
        
        max_size = max(sizes)
        min_size = min(sizes)
        size_ratio = max_size / min_size if min_size > 0 else 1.0
        
        # Check position (central vs peripheral)
        central_elements = 0
        for elem in shapes:
            pos = elem.get('position', {})
            x = pos.get('x', 0)
            y = pos.get('y', 0)
            # Check if near center (within 30% of canvas center)
            # This is approximate since we don't have canvas size here
            if abs(x) < 200 and abs(y) < 200:
                central_elements += 1
        
        issues = []
        score = 70
        
        # Size hierarchy check
        if size_ratio < 1.5:
            issues.append('Elements are too similar in size - need clearer hierarchy')
            score -= 20
        elif size_ratio >= 2.0:
            score += 10
        
        # Central focus check
        if central_elements == 0:
            issues.append('No clear central focal point')
            score -= 15
        elif central_elements > 1:
            issues.append('Multiple central elements - may lack focus')
            score -= 10
        
        return {'score': max(0, min(100, score)), 'issues': issues, 'size_ratio': size_ratio}
    
    def _analyze_composition(self, elements: List[Dict], canvas_size: Tuple[int, int]) -> Dict:
        """Analyze composition and balance"""
        width, height = canvas_size
        
        if not elements:
            return {'score': 0, 'issues': ['No elements']}
        
        # Check distribution across canvas
        x_positions = []
        y_positions = []
        
        for elem in elements:
            pos = elem.get('position', {})
            if 'x' in pos:
                x_positions.append(pos['x'])
            if 'y' in pos:
                y_positions.append(pos['y'])
        
        issues = []
        score = 70
        
        # Check if elements are clustered
        if x_positions:
            x_range = max(x_positions) - min(x_positions)
            if x_range < width * 0.3:
                issues.append('Elements clustered too tightly - spread out more')
                score -= 15
        
        if y_positions:
            y_range = max(y_positions) - min(y_positions)
            if y_range < height * 0.3:
                issues.append('Elements clustered vertically - use more vertical space')
                score -= 15
        
        # Check balance (left vs right)
        if x_positions:
            center_x = width / 2
            left_count = sum(1 for x in x_positions if x < center_x)
            right_count = len(x_positions) - left_count
            imbalance = abs(left_count - right_count) / len(x_positions)
            if imbalance > 0.4:
                issues.append('Elements unbalanced - distribute more evenly')
                score -= 10
        
        return {'score': max(0, min(100, score)), 'issues': issues}
    
    def _analyze_color(self, elements: List[Dict]) -> Dict:
        """Analyze color usage"""
        colors = []
        for elem in elements:
            color = elem.get('color')
            if color:
                colors.append(color)
        
        if not colors:
            return {'score': 50, 'issues': ['No color information found']}
        
        unique_colors = len(set(colors))
        total_elements = len([e for e in elements if e.get('element_type') == 'shape'])
        
        issues = []
        score = 70
        
        # Check color variety
        if unique_colors < 2 and total_elements > 3:
            issues.append('Too few colors - add more variety for visual interest')
            score -= 15
        elif unique_colors > 8:
            issues.append('Too many colors - may lack cohesion')
            score -= 10
        
        return {'score': max(0, min(100, score)), 'issues': issues, 'unique_colors': unique_colors}
    
    def _analyze_spacing(self, elements: List[Dict]) -> Dict:
        """Analyze spacing consistency"""
        import math
        
        if len(elements) < 2:
            return {'score': 70, 'issues': []}
        
        distances = []
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                pos1 = elem1.get('position', {})
                pos2 = elem2.get('position', {})
                x1, y1 = pos1.get('x', 0), pos1.get('y', 0)
                x2, y2 = pos2.get('x', 0), pos2.get('y', 0)
                dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
                if dist > 0:
                    distances.append(dist)
        
        if not distances:
            return {'score': 50, 'issues': ['Cannot calculate spacing']}
        
        # Check consistency
        avg_distance = sum(distances) / len(distances)
        variance = sum((d - avg_distance)**2 for d in distances) / len(distances)
        std_dev = math.sqrt(variance)
        coefficient = std_dev / avg_distance if avg_distance > 0 else 1.0
        
        issues = []
        score = 70
        
        if coefficient > 0.5:
            issues.append('Inconsistent spacing - elements should be more evenly spaced')
            score -= 20
        
        return {'score': max(0, min(100, score)), 'issues': issues, 'avg_spacing': avg_distance}
    
    def _analyze_typography(self, elements: List[Dict]) -> Dict:
        """Analyze typography"""
        text_elements = [e for e in elements if e.get('element_type') == 'text']
        
        if not text_elements:
            return {'score': 70, 'issues': ['No text elements']}
        
        font_sizes = [e.get('font_size', 12) for e in text_elements if e.get('font_size')]
        
        issues = []
        score = 70
        
        if font_sizes:
            min_size = min(font_sizes)
            max_size = max(font_sizes)
            
            if min_size < 12:
                issues.append('Some text too small - minimum 12px recommended')
                score -= 15
            
            if max_size / min_size < 1.5 and len(font_sizes) > 1:
                issues.append('Text sizes too similar - create hierarchy with size variation')
                score -= 10
        
        return {'score': max(0, min(100, score)), 'issues': issues}
    
    def _ai_review(
        self,
        svg_code: str,
        elements: List[Dict],
        canvas_size: Tuple[int, int],
        design_spec: Optional[Dict]
    ) -> Dict:
        """AI-powered design review"""
        api_key = get_openai_key()
        if not api_key:
            return {'score': 0, 'message': 'OpenAI API key not found', 'suggestions': []}
        
        try:
            import openai
        except ImportError:
            return {'score': 0, 'message': 'openai package required', 'suggestions': []}
        
        client = openai.OpenAI(api_key=api_key)
        
        # Prepare context
        elements_summary = self._summarize_elements(elements)
        
        system_prompt = """You are an expert design reviewer specializing in data visualization and illustration design.

Review the SVG.js illustration code and provide:
1. Overall design quality score (0-100)
2. Evaluation of design principles:
   - Visual hierarchy (is there a clear focal point?)
   - Composition (balance, use of space)
   - Color usage (meaningful, consistent, readable)
   - Spacing (consistent, adequate)
   - Typography (readable, hierarchical)
3. Specific improvement suggestions

Be constructive and specific. Focus on actionable improvements."""
        
        user_prompt = f"""Review this SVG.js illustration:

Canvas size: {canvas_size[0]}x{canvas_size[1]}

Elements found: {len(elements)}
{elements_summary}

SVG.js code:
```javascript
{svg_code[:2000]}  // Truncated for context
```

Provide a JSON response with:
- score: number (0-100)
- hierarchy_score: number (0-100)
- composition_score: number (0-100)
- color_score: number (0-100)
- spacing_score: number (0-100)
- typography_score: number (0-100)
- strengths: array of strings
- suggestions: array of objects with 'area', 'issue', 'suggestion', 'priority'"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            ai_result = json.loads(response.choices[0].message.content)
            return ai_result
            
        except Exception as e:
            return {
                'score': 0,
                'message': f'AI review failed: {str(e)}',
                'suggestions': []
            }
    
    def _summarize_elements(self, elements: List[Dict]) -> str:
        """Create summary of elements for AI context"""
        summary_parts = []
        
        shapes = [e for e in elements if e.get('element_type') == 'shape']
        text_elements = [e for e in elements if e.get('element_type') == 'text']
        connections = [e for e in elements if e.get('element_type') == 'connection']
        
        summary_parts.append(f"- {len(shapes)} shapes (circles, rectangles)")
        summary_parts.append(f"- {len(text_elements)} text elements")
        summary_parts.append(f"- {len(connections)} connections/lines")
        
        if shapes:
            sizes = []
            for s in shapes:
                size = s.get('size', 0)
                if isinstance(size, tuple):
                    sizes.append(max(size))
                else:
                    sizes.append(size)
            if sizes:
                summary_parts.append(f"- Size range: {min(sizes):.0f} - {max(sizes):.0f}px")
        
        return '\n'.join(summary_parts)
    
    def _calculate_overall_score(self, basic_analysis: Dict, ai_review: Dict) -> float:
        """Calculate overall score from basic and AI analysis"""
        # Weight: 40% basic analysis, 60% AI review
        basic_score = sum(
            v.get('score', 50) if isinstance(v, dict) else 50
            for v in basic_analysis.values()
        ) / len(basic_analysis) if basic_analysis else 50
        
        ai_score = ai_review.get('score', basic_score)
        
        # If AI review failed, use basic score
        if ai_score == 0 and 'message' in ai_review:
            return basic_score
        
        return (basic_score * 0.4) + (ai_score * 0.6)
    
    def _generate_suggestions(self, basic_analysis: Dict, ai_review: Dict) -> List[Dict]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # From basic analysis
        for area, analysis in basic_analysis.items():
            if isinstance(analysis, dict) and analysis.get('issues'):
                for issue in analysis['issues']:
                    suggestions.append({
                        'area': area,
                        'issue': issue,
                        'suggestion': self._get_suggestion_for_issue(area, issue),
                        'priority': 'medium',
                        'source': 'basic_analysis'
                    })
        
        # From AI review
        if isinstance(ai_review, dict) and 'suggestions' in ai_review:
            suggestions.extend(ai_review['suggestions'])
        
        return suggestions
    
    def _get_suggestion_for_issue(self, area: str, issue: str) -> str:
        """Get suggestion text for common issues"""
        suggestions_map = {
            'hierarchy': {
                'too similar': 'Increase size contrast: make primary element 2-3x larger than secondary elements',
                'no focal point': 'Add a central focal point element that is larger and more prominent',
                'multiple central': 'Choose one primary element and make others clearly secondary'
            },
            'composition': {
                'clustered': 'Spread elements more evenly across the canvas',
                'unbalanced': 'Distribute elements more evenly left-to-right and top-to-bottom'
            },
            'color': {
                'too few': 'Add 2-3 more colors to create visual variety and meaning',
                'too many': 'Reduce to 4-6 colors for better cohesion'
            },
            'spacing': {
                'inconsistent': 'Use consistent spacing between similar elements (e.g., 40-60px gaps)'
            },
            'typography': {
                'too small': 'Increase minimum font size to 14-16px for readability',
                'too similar': 'Create hierarchy: use 24px for primary, 18px for secondary, 14px for labels'
            }
        }
        
        area_suggestions = suggestions_map.get(area, {})
        for key, suggestion in area_suggestions.items():
            if key.lower() in issue.lower():
                return suggestion
        
        return f'Review {area} design principles and improve based on best practices'
