"""Prompt Testing Suite

Tests various prompt patterns and generates comparison outputs.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modern_graphics import (
    quick_template_from_description,
    register_template,
    ModernGraphicsGenerator,
    Attribution
)


# Test prompts organized by category
TEST_PROMPTS = [
    {
        "category": "minimalist",
        "name": "simple_minimalist",
        "prompt": "minimalist design, lots of white space, simple colors, clean sans-serif",
        "expected_qualities": ["lots of whitespace", "simple colors", "clean fonts"],
        "test_notes": "Works well for professional contexts"
    },
    {
        "category": "minimalist",
        "name": "ultra_minimalist",
        "prompt": "ultra-minimalist, monochrome, geometric shapes, no gradients, bold typography",
        "expected_qualities": ["monochrome", "geometric", "bold"],
        "test_notes": "Modern art or design portfolios"
    },
    {
        "category": "bold",
        "name": "tech_startup",
        "prompt": "bold vibrant colors, tech startup style, clean sans-serif, modern and energetic",
        "expected_qualities": ["vibrant colors", "energetic", "modern"],
        "test_notes": "Startup pitch decks, product launches"
    },
    {
        "category": "bold",
        "name": "high_contrast",
        "prompt": "bold vibrant colors with high contrast, striking typography, modern and impactful",
        "expected_qualities": ["high contrast", "striking", "impactful"],
        "test_notes": "Attention-grabbing presentations"
    },
    {
        "category": "professional",
        "name": "corporate",
        "prompt": "corporate blue and gray, professional, traditional fonts, conservative and trustworthy",
        "expected_qualities": ["corporate colors", "professional", "trustworthy"],
        "test_notes": "Business reports, executive presentations"
    },
    {
        "category": "professional",
        "name": "modern_professional",
        "prompt": "modern professional theme, navy blue and silver, clean sans-serif, authoritative but approachable",
        "expected_qualities": ["modern", "professional", "authoritative"],
        "test_notes": "Corporate communications"
    },
    {
        "category": "dark",
        "name": "dark_professional",
        "prompt": "dark professional theme with blue accents, modern sans-serif font, clean and minimalist",
        "expected_qualities": ["dark background", "blue accents", "minimalist"],
        "test_notes": "Developer presentations, tech documentation"
    },
    {
        "category": "light",
        "name": "light_airy",
        "prompt": "light minimalist design with pastel colors, elegant serif typography, spacious and airy",
        "expected_qualities": ["light background", "pastel colors", "spacious"],
        "test_notes": "Elegant presentations, lifestyle content"
    },
    {
        "category": "creative",
        "name": "artistic",
        "prompt": "creative and artistic, unique color palette, expressive typography, bold and distinctive",
        "expected_qualities": ["creative", "unique colors", "expressive"],
        "test_notes": "Artist portfolios, creative presentations"
    },
    {
        "category": "style_reference",
        "name": "apple_style",
        "prompt": "Apple-style: clean minimalist, lots of white space, SF Pro font, subtle gradients, modern and elegant",
        "expected_qualities": ["minimalist", "white space", "elegant"],
        "test_notes": "Modern tech presentations"
    }
]


def test_prompts(output_dir=None):
    """Test all prompts and generate comparison outputs"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "examples" / "output" / "generated" / "prompt_tests"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Prompt Testing Suite")
    print("=" * 60)
    print()
    print(f"Testing {len(TEST_PROMPTS)} prompts...")
    print(f"Output directory: {output_dir}")
    print()
    
    results = []
    
    for i, test_case in enumerate(TEST_PROMPTS, 1):
        print(f"{i}. Testing: {test_case['name']} ({test_case['category']})")
        print(f"   Prompt: \"{test_case['prompt']}\"")
        
        try:
            # Generate template
            template = quick_template_from_description(test_case['prompt'])
            register_template(template)
            
            # Create generator
            generator = ModernGraphicsGenerator(
                f"Test: {test_case['name']}",
                template=template,
                attribution=Attribution(copyright="")
            )
            
            # Generate a standard test diagram (cycle)
            html = generator.generate_cycle_diagram([
                {'text': 'Step 1', 'color': 'blue'},
                {'text': 'Step 2', 'color': 'green'},
                {'text': 'Step 3', 'color': 'orange'}
            ])
            
            # Save output
            output_path = output_dir / f"{test_case['category']}_{test_case['name']}.png"
            generator.export_to_png(html, output_path)
            
            results.append({
                **test_case,
                'success': True,
                'output_path': output_path,
                'template_name': template.name
            })
            
            print(f"   ✓ Generated: {output_path.name}")
            
        except Exception as e:
            results.append({
                **test_case,
                'success': False,
                'error': str(e)
            })
            print(f"   ✗ Error: {e}")
        
        print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    successful = sum(1 for r in results if r.get('success'))
    failed = len(results) - successful
    
    print(f"Total prompts tested: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    
    if successful > 0:
        print("Successful prompts:")
        for r in results:
            if r.get('success'):
                print(f"  ✓ {r['name']} ({r['category']})")
        print()
    
    if failed > 0:
        print("Failed prompts:")
        for r in results:
            if not r.get('success'):
                print(f"  ✗ {r['name']} ({r['category']}): {r.get('error', 'Unknown error')}")
        print()
    
    print(f"Outputs saved to: {output_dir}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test prompt patterns")
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory for test results"
    )
    
    args = parser.parse_args()
    
    try:
        test_prompts(args.output)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
