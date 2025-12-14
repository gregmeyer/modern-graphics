#!/usr/bin/env python3
"""Interactive template creation interview"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import (
    interview_for_template,
    register_template,
    ModernGraphicsGenerator,
    Attribution
)
from modern_graphics.env_config import get_openai_key

def main():
    print("=" * 70)
    print("Interactive Template Creation Interview")
    print("=" * 70)
    
    # Check for API key
    api_key = get_openai_key()
    if not api_key:
        print("\n⚠️  OPENAI_API_KEY not found!")
        print("   Please set it in your .env file:")
        print("   OPENAI_API_KEY=your_key_here")
        return
    
    print(f"\n✓ OpenAI API key found")
    print("\nThe AI will ask you questions about your design preferences.")
    print("Answer the questions, and when you're ready, type 'done' to generate the template.")
    print("Type 'quit' at any time to exit.\n")
    
    try:
        # Start the interactive interview
        template = interview_for_template()
        
        if template:
            print("\n" + "=" * 70)
            print("✓ Template Created Successfully!")
            print("=" * 70)
            print(f"\nTemplate Name: {template.name}")
            print(f"Colors: {', '.join(template.colors.keys())}")
            print(f"Font: {template.font_family}")
            print(f"Background: {template.background_color}")
            
            # Register it
            register_template(template)
            print(f"\n✓ Template registered as '{template.name}'")
            
            # Generate a test diagram
            print("\nGenerating test diagram...")
            generator = ModernGraphicsGenerator(
                "My Custom Template",
                template=template,
                attribution=Attribution(copyright="© Interactive Interview Example 2025")
            )
            
            html = generator.generate_cycle_diagram([
                {'text': 'Step 1', 'color': 'blue'},
                {'text': 'Step 2', 'color': 'green'},
                {'text': 'Step 3', 'color': 'purple'},
            ])
            
            output_path = Path(__file__).parent / "output" / "interactive_template.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            generator.export_to_png(html, output_path, viewport_width=1200, viewport_height=600)
            print(f"✓ Saved: {output_path}")
            
            print("\n" + "=" * 70)
            print("You can now use this template:")
            print(f"  from modern_graphics import get_template")
            print(f"  template = get_template('{template.name}')")
            print("=" * 70)
        else:
            print("\n✗ Template creation cancelled or failed")
            
    except KeyboardInterrupt:
        print("\n\n✗ Interview cancelled by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
