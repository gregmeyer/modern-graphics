#!/usr/bin/env python3
"""Example: Prompt-driven template creation and image generation"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import (
    quick_template_from_description,
    register_template,
    ModernGraphicsGenerator,
    Attribution
)
from modern_graphics.env_config import get_openai_key

def main():
    print("=" * 70)
    print("Prompt-Driven Template Creation")
    print("=" * 70)
    
    # Check for API key
    api_key = get_openai_key()
    if not api_key:
        print("\n⚠️  OPENAI_API_KEY not found!")
        print("   Please set it in your .env file:")
        print("   OPENAI_API_KEY=your_key_here")
        print("\n   Or set it as an environment variable:")
        print("   export OPENAI_API_KEY=your_key_here")
        return
    
    print(f"\n✓ OpenAI API key found")
    
    # Example 1: Quick template from description
    print("\n" + "-" * 70)
    print("Example 1: Quick Template Generation")
    print("-" * 70)
    
    description = "modern minimalist theme with soft pastel colors, clean sans-serif fonts, light background"
    print(f"\nPrompt: '{description}'")
    print("Generating template...")
    
    try:
        template = quick_template_from_description(description)
        if template:
            print(f"✓ Template created: '{template.name}'")
            print(f"  Colors: {list(template.colors.keys())}")
            print(f"  Font: {template.font_family}")
            print(f"  Background: {template.background_color}")
            
            # Register it
            register_template(template)
            
            # Generate a diagram with it
            print("\nGenerating diagram with this template...")
            generator = ModernGraphicsGenerator(
                "Modern Minimalist Design",
                template=template,
                attribution=Attribution(copyright="© Prompt-Driven Example 2025")
            )
            
            html = generator.generate_cycle_diagram([
                {'text': 'Design', 'color': 'blue'},
                {'text': 'Build', 'color': 'green'},
                {'text': 'Deploy', 'color': 'purple'},
            ])
            
            output_path = Path(__file__).parent / "output" / "prompt_driven_example.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            generator.export_to_png(html, output_path, viewport_width=1200, viewport_height=600)
            print(f"✓ Saved: {output_path}")
            
        else:
            print("✗ Failed to generate template")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Another style
    print("\n" + "-" * 70)
    print("Example 2: Dark Professional Theme")
    print("-" * 70)
    
    description2 = "dark professional theme with blue and gray accents, modern tech startup style"
    print(f"\nPrompt: '{description2}'")
    print("Generating template...")
    
    try:
        template2 = quick_template_from_description(description2)
        if template2:
            print(f"✓ Template created: '{template2.name}'")
            print(f"  Colors: {list(template2.colors.keys())}")
            print(f"  Font: {template2.font_family}")
            print(f"  Background: {template2.background_color}")
            
            register_template(template2)
            
            generator2 = ModernGraphicsGenerator(
                "Dark Professional Theme",
                template=template2,
                attribution=Attribution(copyright="© Prompt-Driven Example 2025")
            )
            
            html2 = generator2.generate_comparison_diagram(
                left_column={
                    'title': 'Before',
                    'steps': ['Manual design', 'Time consuming', 'Hard to update']
                },
                right_column={
                    'title': 'After',
                    'steps': ['Automated', 'Fast', 'Easy updates']
                }
            )
            
            output_path2 = Path(__file__).parent / "output" / "prompt_driven_dark.png"
            generator2.export_to_png(html2, output_path2, viewport_width=1200, viewport_height=600)
            print(f"✓ Saved: {output_path2}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✓ Prompt-driven examples complete!")
    print("=" * 70)
    print(f"\nGenerated files:")
    print(f"  - {Path(__file__).parent / 'output' / 'prompt_driven_example.png'}")
    print(f"  - {Path(__file__).parent / 'output' / 'prompt_driven_dark.png'}")

if __name__ == "__main__":
    main()
