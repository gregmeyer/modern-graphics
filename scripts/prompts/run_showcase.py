"""Generate Showcase Graphics for README

Creates a collection of high-quality graphics showcasing different templates
and diagram types for use in the README.
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


# Showcase templates - different styles
SHOWCASE_TEMPLATES = [
    {
        "name": "minimalist",
        "prompt": "minimalist design, lots of white space, simple colors, clean sans-serif",
        "description": "Clean and minimal"
    },
    {
        "name": "tech_startup",
        "prompt": "bold vibrant colors, tech startup style, clean sans-serif, modern and energetic",
        "description": "Bold and energetic"
    },
    {
        "name": "corporate",
        "prompt": "corporate blue and gray, professional, traditional fonts, conservative and trustworthy",
        "description": "Professional and trustworthy"
    },
    {
        "name": "dark_professional",
        "prompt": "dark professional theme with blue accents, modern sans-serif font, clean and minimalist",
        "description": "Dark and modern"
    },
    {
        "name": "creative",
        "prompt": "creative and artistic, unique color palette, expressive typography, bold and distinctive",
        "description": "Creative and distinctive"
    }
]


def generate_showcase(output_dir=None):
    """Generate showcase graphics"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "examples" / "output" / "showcase"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Generating Showcase Graphics for README")
    print("=" * 60)
    print()
    
    # Generate each template and create sample graphics
    for template_info in SHOWCASE_TEMPLATES:
        print(f"Template: {template_info['name']} ({template_info['description']})")
        print(f"  Prompt: \"{template_info['prompt']}\"")
        
        try:
            # Generate template
            template = quick_template_from_description(template_info['prompt'])
            register_template(template)
            
            # Create generator
            generator = ModernGraphicsGenerator(
                f"Showcase: {template_info['name']}",
                template=template,
                attribution=Attribution(copyright="")
            )
            
            template_dir = output_dir / template_info['name']
            template_dir.mkdir(exist_ok=True)
            
            # 1. Cycle diagram
            print("  Generating cycle diagram...")
            html = generator.generate_cycle_diagram([
                {'text': 'Plan', 'color': 'blue'},
                {'text': 'Build', 'color': 'green'},
                {'text': 'Test', 'color': 'orange'},
                {'text': 'Deploy', 'color': 'purple'}
            ])
            generator.export_to_png(html, template_dir / "cycle.png")
            print(f"    ✓ Saved: {template_dir / 'cycle.png'}")
            
            # 2. Comparison diagram
            print("  Generating comparison diagram...")
            html = generator.generate_comparison_diagram(
                left_column=[{
                    'title': 'Before',
                    'items': ['Manual', 'Slow', 'Error-prone']
                }],
                right_column=[{
                    'title': 'After',
                    'items': ['Automated', 'Fast', 'Accurate']
                }]
            )
            generator.export_to_png(html, template_dir / "comparison.png")
            print(f"    ✓ Saved: {template_dir / 'comparison.png'}")
            
            # 3. Story slide
            print("  Generating story slide...")
            html = generator.generate_story_slide(
                title="The Transformation",
                what_changed="Manual → Automated",
                time_period="2024",
                what_it_means="10x improvement"
            )
            generator.export_to_png(html, template_dir / "story_slide.png")
            print(f"    ✓ Saved: {template_dir / 'story_slide.png'}")
            
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()
    
    # Generate a "template comparison" showing same diagram in different styles
    print("Generating template comparison...")
    comparison_dir = output_dir / "comparison"
    comparison_dir.mkdir(exist_ok=True)
    
    # Same cycle diagram with different templates
    cycle_data = [
        {'text': 'Acquire', 'color': 'blue'},
        {'text': 'Activate', 'color': 'green'},
        {'text': 'Retain', 'color': 'orange'},
        {'text': 'Refer', 'color': 'purple'}
    ]
    
    for template_info in SHOWCASE_TEMPLATES[:3]:  # First 3 for comparison
        try:
            template = quick_template_from_description(template_info['prompt'])
            register_template(template)
            
            generator = ModernGraphicsGenerator(
                f"Comparison: {template_info['name']}",
                template=template,
                attribution=Attribution(copyright="")
            )
            
            html = generator.generate_cycle_diagram(cycle_data)
            generator.export_to_png(
                html,
                comparison_dir / f"cycle_{template_info['name']}.png"
            )
            print(f"  ✓ {template_info['name']} comparison saved")
        except Exception as e:
            print(f"  ✗ Error with {template_info['name']}: {e}")
    
    print()
    print("=" * 60)
    print("✓ Showcase graphics generated successfully!")
    print(f"   Output directory: {output_dir.absolute()}")
    print()
    print("Generated:")
    print("  - Individual template showcases (cycle, comparison, story_slide)")
    print("  - Template comparison (same diagram, different styles)")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate showcase graphics")
    parser.add_argument(
        "--output",
        type=str,
        help="Output directory for showcase graphics"
    )
    
    args = parser.parse_args()
    
    try:
        generate_showcase(args.output)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
