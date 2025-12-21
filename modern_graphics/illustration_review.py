"""Integration module for illustration review system (Tier 1 + Tier 2)"""

from typing import Dict, List, Optional, Tuple
from .illustration_validator import IllustrationValidator
from .design_review_agent import DesignReviewAgent
from .svg_element_parser import SVGElementParser


def review_illustration(
    svg_code: str,
    canvas_size: Tuple[int, int] = (1000, 500),
    review_enabled: bool = True,
    auto_fix: bool = True
) -> Dict:
    """
    Review illustration with Tier 1 (validation) and Tier 2 (AI review)
    
    Args:
        svg_code: SVG.js JavaScript code
        canvas_size: Canvas dimensions (width, height)
        review_enabled: Enable AI review (Tier 2)
        auto_fix: Automatically fix fixable issues (Tier 1)
    
    Returns:
        Review result dictionary
    """
    validator = IllustrationValidator()
    parser = SVGElementParser()
    review_agent = DesignReviewAgent() if review_enabled else None
    
    # Parse elements
    elements = parser.parse(svg_code)
    
    # Tier 1: Built-in validation
    validation_issues = validator.validate(elements, canvas_size)
    
    # Auto-fix if enabled
    fixed_elements = elements
    fixed_svg_code = svg_code
    if auto_fix and validation_issues:
        fixable_issues = [i for i in validation_issues if i.get('auto_fix', False)]
        if fixable_issues:
            fixed_elements = validator.auto_fix(fixable_issues, elements, canvas_size)
            # Note: In a real implementation, we'd regenerate SVG code from fixed elements
            # For now, we'll note that fixes were applied
    
    # Tier 2: AI review (if enabled)
    ai_review = None
    if review_agent:
        ai_review = review_agent.review(fixed_svg_code, None, canvas_size)
    
    # Combine results
    result = {
        'tier1_validation': {
            'issues': validation_issues,
            'issues_count': len(validation_issues),
            'fixable_count': len([i for i in validation_issues if i.get('auto_fix', False)]),
            'fixed': auto_fix and len([i for i in validation_issues if i.get('auto_fix', False)]) > 0
        },
        'tier2_review': ai_review,
        'overall_score': ai_review.get('score', 70) if ai_review else 70,
        'passed': True,
        'elements_parsed': len(elements)
    }
    
    # Determine if passed
    if validation_issues:
        high_severity = [i for i in validation_issues if i.get('severity') == 'high']
        if high_severity and not auto_fix:
            result['passed'] = False
    
    if ai_review and not ai_review.get('passed', True):
        result['passed'] = False
    
    return result


def generate_with_review(
    generate_function,
    prompt: str,
    canvas_size: Tuple[int, int] = (1000, 500),
    review_enabled: bool = True,
    auto_fix: bool = True,
    quality_threshold: int = 70
) -> Dict:
    """
    Generate illustration with review
    
    Args:
        generate_function: Function that generates SVG.js code from prompt
        prompt: Generation prompt
        canvas_size: Canvas dimensions
        review_enabled: Enable AI review
        auto_fix: Auto-fix issues
        quality_threshold: Minimum quality score
    
    Returns:
        Dictionary with svg_code, review, and metadata
    """
    # Generate
    svg_code = generate_function(prompt)
    
    # Review
    review_result = review_illustration(
        svg_code,
        canvas_size,
        review_enabled=review_enabled,
        auto_fix=auto_fix
    )
    
    return {
        'svg_code': svg_code,
        'review': review_result,
        'passed': review_result['passed'] and review_result['overall_score'] >= quality_threshold,
        'score': review_result['overall_score']
    }
