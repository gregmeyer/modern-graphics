"""Helper utilities for deciding when to use SVG.js vs HTML/CSS"""

from typing import Dict, List, Optional


def should_use_svg_js(
    graphic_type: str,
    has_custom_shapes: bool = False,
    has_complex_paths: bool = False,
    is_creative_illustration: bool = False,
    needs_animation: bool = False,
    needs_advanced_gradients: bool = False,
    has_custom_icons: bool = False
) -> bool:
    """
    Determine if SVG.js should be used for a graphic.
    
    Args:
        graphic_type: Type of graphic (e.g., 'cycle', 'comparison', 'custom_illustration')
        has_custom_shapes: Requires custom shapes (polygons, stars, etc.)
        has_complex_paths: Requires complex paths/curves
        is_creative_illustration: Is a creative/artistic illustration
        needs_animation: Requires animation
        needs_advanced_gradients: Requires advanced gradient effects
        has_custom_icons: Requires custom SVG icons
    
    Returns:
        True if SVG.js should be used, False if HTML/CSS is better
    
    Examples:
        >>> should_use_svg_js('cycle')
        False
        
        >>> should_use_svg_js('custom_illustration', is_creative_illustration=True)
        True
        
        >>> should_use_svg_js('cycle', has_complex_paths=True)
        True
    """
    # Standard diagram types - use HTML/CSS by default
    standard_diagrams = [
        'cycle', 'comparison', 'timeline', 'grid', 
        'flywheel', 'story_slide', 'slide_card', 
        'pyramid', 'funnel', 'before_after'
    ]
    
    # If it's a standard diagram and no special requirements, use HTML/CSS
    if graphic_type in standard_diagrams:
        if not any([
            has_custom_shapes,
            has_complex_paths,
            needs_animation,
            needs_advanced_gradients,
            has_custom_icons
        ]):
            return False
    
    # Use SVG.js if any of these conditions are met
    svg_js_reasons = [
        is_creative_illustration,
        has_complex_paths,
        has_custom_shapes,
        needs_animation,
        needs_advanced_gradients,
        has_custom_icons,
        graphic_type == 'custom_illustration',
        graphic_type == 'hero_canvas',
        graphic_type == 'freeform'
    ]
    
    return any(svg_js_reasons)


def get_recommendation_reason(
    graphic_type: str,
    **kwargs
) -> Dict[str, any]:
    """
    Get detailed recommendation with reasoning.
    
    Returns:
        Dictionary with 'use_svg_js', 'reason', and 'alternatives'
    """
    use_svg = should_use_svg_js(graphic_type, **kwargs)
    
    reasons = []
    alternatives = []
    
    if use_svg:
        if kwargs.get('is_creative_illustration'):
            reasons.append("Creative illustration requires SVG.js flexibility")
        if kwargs.get('has_complex_paths'):
            reasons.append("Complex paths/curves need SVG.js path API")
        if kwargs.get('has_custom_shapes'):
            reasons.append("Custom shapes require SVG.js shape generation")
        if kwargs.get('needs_animation'):
            reasons.append("Animation requires SVG.js animation API")
        if kwargs.get('needs_advanced_gradients'):
            reasons.append("Advanced gradients need SVG.js gradient support")
        if kwargs.get('has_custom_icons'):
            reasons.append("Custom icons require SVG.js path support")
        
        if not reasons:
            reasons.append("Non-standard graphic type benefits from SVG.js")
    else:
        reasons.append(f"'{graphic_type}' is a standard diagram type")
        reasons.append("HTML/CSS provides better styling control")
        reasons.append("Simpler code and easier maintenance")
        
        if kwargs.get('has_complex_paths'):
            alternatives.append("Consider if complex paths are truly necessary")
        if kwargs.get('needs_animation'):
            alternatives.append("CSS animations might suffice")
    
    return {
        'use_svg_js': use_svg,
        'reason': '; '.join(reasons) if reasons else 'Standard diagram type',
        'alternatives': alternatives,
        'recommended_approach': 'SVG.js' if use_svg else 'HTML/CSS'
    }


# Quick reference examples
EXAMPLES = {
    'cycle_diagram': {
        'graphic_type': 'cycle',
        'use_svg_js': False,
        'reason': 'Standard diagram type, HTML/CSS works perfectly'
    },
    'comparison_diagram': {
        'graphic_type': 'comparison',
        'use_svg_js': False,
        'reason': 'Standard layout, CSS flexbox handles it well'
    },
    'automation_paradox_hero': {
        'graphic_type': 'hero_canvas',
        'is_creative_illustration': True,
        'has_complex_paths': True,
        'use_svg_js': True,
        'reason': 'Creative illustration with complex paths and custom shapes'
    },
    'game_board': {
        'graphic_type': 'custom_illustration',
        'has_complex_paths': True,
        'use_svg_js': True,
        'reason': 'Winding paths require SVG.js path API'
    },
    'animated_progress': {
        'graphic_type': 'custom_illustration',
        'needs_animation': True,
        'use_svg_js': True,
        'reason': 'Animation requires SVG.js'
    }
}


def print_decision_guide():
    """Print a quick reference guide"""
    print("="*70)
    print("SVG.js vs HTML/CSS Decision Guide")
    print("="*70)
    print()
    print("Use SVG.js when:")
    print("  ✓ Custom illustrations & creative graphics")
    print("  ✓ Complex paths & curves (bezier, quadratic)")
    print("  ✓ Advanced shapes (polygons, stars, custom)")
    print("  ✓ Advanced gradients (multi-stop, radial)")
    print("  ✓ Animation requirements")
    print("  ✓ Custom SVG icons")
    print("  ✓ Precise mathematical positioning")
    print()
    print("Use HTML/CSS when:")
    print("  ✓ Standard diagrams (cycle, comparison, timeline, etc.)")
    print("  ✓ Template-based graphics")
    print("  ✓ Text-heavy layouts")
    print("  ✓ Simple shapes (rectangles, circles)")
    print("  ✓ Layout & spacing (flexbox, grid)")
    print("  ✓ Box shadows & CSS effects")
    print("  ✓ Maintainability priority")
    print()
    print("Examples:")
    for name, example in EXAMPLES.items():
        approach = 'SVG.js' if example.get('use_svg_js', False) else 'HTML/CSS'
        print(f"  {name}: {approach} - {example['reason']}")
    print("="*70)
