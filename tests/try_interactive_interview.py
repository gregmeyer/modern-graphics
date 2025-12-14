#!/usr/bin/env python3
"""Simple script to try the interactive interview"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import interview_for_template, register_template, ModernGraphicsGenerator, Attribution
from modern_graphics.env_config import get_openai_key

def main():
    print("=" * 70)
    print("Interactive Template Creation Interview")
    print("=" * 70)
    
    # Check for API key
    if not get_openai_key():
        print("\n⚠️  OPENAI_API_KEY not found!")
        print("   Please set it in your .env file or environment variable.")
        return
    
    print("\nThe AI will ask you questions about your design preferences.")
    print("Answer naturally, and when ready, type 'done' to generate the template.")
    print("Type 'quit' to exit.\n")
    
    # Start the interactive interview
    template = interview_for_template()
    
    if template:
        print("\n" + "=" * 70)
        print("Template Created!")
        print("=" * 70)
        print(f"\nName: {template.name}")
        print(f"Colors: {', '.join(template.colors.keys())}")
        print(f"Font: {template.font_family}")
        print(f"Background: {template.background_color}")
        
        # Register and test it
        register_template(template)
        
        generator = ModernGraphicsGenerator(
            "My Interview Template",
            template=template,
            attribution=Attribution(copyright="© Interview Example 2025")
        )
        
        html = generator.generate_cycle_diagram([
            {'text': 'Step 1', 'color': 'blue'},
            {'text': 'Step 2', 'color': 'green'},
            {'text': 'Step 3', 'color': 'purple'},
        ])
        
        output_path = Path(__file__).parent / "output" / "interview_result.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        generator.export_to_png(html, output_path, viewport_width=1200, viewport_height=600)
        print(f"\n✓ Test diagram saved: {output_path}")
    else:
        print("\nTemplate creation cancelled.")

if __name__ == "__main__":
    main()
