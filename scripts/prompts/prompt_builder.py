"""Interactive Prompt Builder

Helps users build effective prompts for AI-assisted template creation through
a step-by-step questionnaire.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modern_graphics import quick_template_from_description, register_template


def prompt_builder():
    """Interactive prompt builder"""
    print("=" * 60)
    print("AI Template Prompt Builder")
    print("=" * 60)
    print()
    print("Answer these questions to build your prompt:")
    print()
    
    # Step 1: Use case
    print("1. What's your use case?")
    print("   Examples: pitch deck, corporate report, portfolio, presentation")
    use_case = input("   > ").strip()
    print()
    
    # Step 2: Style
    print("2. What style are you looking for?")
    print("   Options: minimalist, bold, professional, creative, modern, classic")
    style = input("   > ").strip()
    print()
    
    # Step 3: Colors
    print("3. What colors do you want?")
    print("   Examples: blue and gray, vibrant colors, pastels, monochrome")
    colors = input("   > ").strip()
    print()
    
    # Step 4: Fonts
    print("4. What font style?")
    print("   Options: sans-serif, serif, modern, traditional, expressive")
    fonts = input("   > ").strip()
    print()
    
    # Step 5: Mood/Tone
    print("5. What mood or tone?")
    print("   Examples: professional, energetic, calming, elegant, playful")
    mood = input("   > ").strip()
    print()
    
    # Build prompt
    prompt_parts = []
    
    if style:
        prompt_parts.append(style)
    if colors:
        prompt_parts.append(f"with {colors}")
    if fonts:
        prompt_parts.append(f"{fonts} font")
    if mood:
        prompt_parts.append(f"{mood}")
    if use_case:
        # Add use case context if provided
        prompt_parts.append(f"for {use_case}")
    
    prompt = ", ".join(prompt_parts)
    
    print("=" * 60)
    print("Generated Prompt:")
    print("=" * 60)
    print(f'  "{prompt}"')
    print()
    
    # Offer to generate template
    generate = input("Generate template from this prompt? (y/n): ").strip().lower()
    
    if generate == 'y':
        print()
        print("Generating template...")
        try:
            template = quick_template_from_description(prompt)
            register_template(template)
            print(f"✓ Template created: {template.name}")
            print()
            print("You can now use this template:")
            print(f'  from modern_graphics import get_template')
            print(f'  template = get_template("{template.name}")')
        except Exception as e:
            print(f"✗ Error generating template: {e}")
            print("Try refining your prompt or check your OpenAI API key.")
    else:
        print()
        print("Prompt saved. You can use it with:")
        print(f'  quick_template_from_description("{prompt}")')
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        prompt_builder()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}")
