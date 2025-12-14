"""Example: Interactive template creation with OpenAI"""

from modern_graphics import interview_for_template, quick_template_from_description, register_template, ModernGraphicsGenerator, Attribution
from pathlib import Path

# Method 1: Quick generation from description
print("=" * 60)
print("Method 1: Quick Template Generation")
print("=" * 60)

template = quick_template_from_description(
    "dark professional theme with blue and purple accents, modern sans-serif font"
)

if template:
    register_template(template)
    print(f"\n✓ Created template: {template.name}")
    
    # Test it
    generator = ModernGraphicsGenerator("Test", template=template)
    html = generator.generate_cycle_diagram([
        {'text': 'Step 1', 'color': 'blue'},
        {'text': 'Step 2', 'color': 'purple'},
    ])
    generator.save(html, Path("quick_template_example.html"))
    print("✓ Generated example diagram with quick template")

# Method 2: Interactive interview
print("\n" + "=" * 60)
print("Method 2: Interactive Interview")
print("=" * 60)
print("\nUncomment the line below to try interactive interview:")
print("# template = interview_for_template()")

# Uncomment to try:
# template = interview_for_template()
# if template:
#     register_template(template)
#     print(f"\n✓ Created template: {template.name}")
