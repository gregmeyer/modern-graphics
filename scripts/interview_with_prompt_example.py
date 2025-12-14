"""Example: Using interview with an initial prompt

Demonstrates how to use the interview_for_template function with an initial prompt
to guide the conversation toward your desired template design.
"""

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

print("=" * 60)
print("Template Interview with Initial Prompt")
print("=" * 60)
print()

# Example 1: Interview with a specific prompt
print("Example 1: Starting interview with a prompt")
print("-" * 60)

# You can provide an initial prompt to guide the conversation
initial_prompt = (
    "I need a template for a tech startup pitch deck. "
    "It should be modern and energetic with vibrant colors, "
    "but still professional enough for investors. "
    "I want it to feel innovative and forward-thinking."
)

print(f"Initial prompt: {initial_prompt}\n")
print("Starting interview... (this will be interactive)")
print("Type 'done' when ready to generate the template\n")

# Uncomment to run interactive interview:
# template = interview_for_template(
#     initial_prompt=initial_prompt,
#     model="gpt-4"
# )
# 
# if template:
#     register_template(template)
#     print(f"\n✓ Template '{template.name}' created and registered!")
#     
#     # Test it
#     generator = ModernGraphicsGenerator(
#         "Startup Pitch",
#         template=template,
#         attribution=Attribution(copyright="© Startup Inc 2025")
#     )
#     
#     # Generate a test diagram
#     html = generator.generate_cycle_diagram([
#         {'text': 'Ideate', 'color': 'blue'},
#         {'text': 'Build', 'color': 'green'},
#         {'text': 'Launch', 'color': 'orange'},
#         {'text': 'Scale', 'color': 'purple'}
#     ])
#     
#     output_file = Path(__file__).parent / "output" / "generated" / "interview_template_example.html"
#     output_file.parent.mkdir(parents=True, exist_ok=True)
#     generator.save(html, output_file)
#     print(f"✓ Test diagram saved to: {output_file}")

print("\n" + "=" * 60)
print("Example 2: Different prompt styles")
print("=" * 60)
print()

# Example prompts for different use cases
example_prompts = {
    "Corporate": (
        "I need a corporate template for quarterly reports. "
        "It should be professional, trustworthy, and conservative. "
        "Use corporate blue and gray colors with traditional fonts."
    ),
    "Education": (
        "Create an educational template that's friendly and engaging. "
        "Bright but not overwhelming colors, clear readable fonts, "
        "warm and inviting feel for course materials."
    ),
    "Healthcare": (
        "I need a healthcare template for medical presentations. "
        "Clean blue and white colors, accessible fonts, "
        "trustworthy and calming, approachable and clear."
    ),
    "Creative": (
        "Design a creative template for a portfolio website. "
        "Unique color palette, expressive typography, "
        "bold and distinctive but still professional."
    )
}

for use_case, prompt in example_prompts.items():
    print(f"{use_case}:")
    print(f"  {prompt}\n")

print("=" * 60)
print("Usage:")
print("=" * 60)
print("""
# Use interview with initial prompt
template = interview_for_template(
    initial_prompt="Your description here",
    model="gpt-4"
)

# The AI will use your prompt as a starting point and ask
# clarifying questions to refine the template design.
""")
