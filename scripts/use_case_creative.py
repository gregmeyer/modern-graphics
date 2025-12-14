"""Use Case Example: Creative Portfolio Website

This example demonstrates creating unique graphics for a creative portfolio
using sophisticated prompts with the unified story slide generator.
Prompts are stored for evaluation purposes.
"""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from modern_graphics import (
    quick_template_from_description,
    register_template,
    ModernGraphicsGenerator,
    Attribution
)
from modern_graphics.diagrams import generate_unified_story_slide
from prompt_storage import PromptStorage

# Output directory (goes to generated/ for temporary outputs)
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "use_cases" / "creative"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(output_dir)

print("=" * 60)
print("Creative Portfolio Website - Use Case Example")
print("=" * 60)
print()

# Generate template from prompt
prompt = (
    "creative and artistic, unique color palette, expressive typography, "
    "bold and distinctive, unconventional but professional"
)

print(f"Generating template from prompt:")
print(f'  "{prompt}"')
print()

template = quick_template_from_description(prompt)
register_template(template)
print(f"✓ Template created: {template.name}")
print()

# Create generator
generator = ModernGraphicsGenerator(
    "Creative Portfolio",
    template=template,
    attribution=Attribution(copyright="© Designer Name 2025")
)

# 1. Portfolio Growth Story Slide
print("1. Generating portfolio growth story slide...")
prompt1 = """Show the evolution of my creative portfolio and client impact over the past three years.
Client projects increased from 12 in 2022 to 35 in 2024, representing 192% growth in creative output.
Average project value grew from $5K to $15K, reflecting increased expertise and market recognition.
Client satisfaction scores consistently above 4.8/5, with 95% repeat client rate demonstrating strong relationships.
Visualize the creative journey with metrics: 35 projects in 2024, $15K average project value, 95% repeat rate, and 4.8/5 satisfaction."""
    html = generate_unified_story_slide(generator, prompt1, model="gpt-4-turbo-preview", temperature=1.0)
    output_file = output_dir / "01_portfolio_growth.png"
    generator.export_to_png(html, output_file)
    prompt_storage.add_prompt(
        prompt=prompt1,
        output_file=output_file,
        use_case="creative",
        slide_type="story_slide",
        model="gpt-4-turbo-preview",
        temperature=1.0,
        metadata={"slide_number": 1, "title": "Portfolio Growth"}
    )
print(f"   ✓ Saved: {output_file}")
print()

# 2. Before/After Transformation
print("2. Generating before/after transformation...")
html = generator.generate_before_after_diagram(
    before_items=['Old brand identity', 'Outdated website', 'Inconsistent messaging'],
    after_items=['Modern brand system', 'Redesigned platform', 'Cohesive experience']
)
generator.export_to_png(html, output_dir / "02_transformation.png")
print(f"   ✓ Saved: {output_dir / '02_transformation.png'}")
print()

# 3. Creative Process Flywheel
print("3. Generating creative process flywheel...")
html = generator.generate_flywheel_diagram(
    elements=[
        {'text': 'Research', 'color': 'blue'},
        {'text': 'Ideate', 'color': 'purple'},
        {'text': 'Design', 'color': 'orange'},
        {'text': 'Refine', 'color': 'green'}
    ],
    center_label="Creative Process"
)
generator.export_to_png(html, output_dir / "03_process.png")
print(f"   ✓ Saved: {output_dir / '03_process.png'}")
print()

# 4. Skills Grid
print("4. Generating skills grid...")
html = generator.generate_grid_diagram(
    items=[
        {'number': '1', 'text': 'Branding'},
        {'number': '2', 'text': 'Web Design'},
        {'number': '3', 'text': 'Print Design'},
        {'number': '4', 'text': 'Illustration'},
        {'number': '5', 'text': 'Typography'}
    ],
    columns=5
)
generator.export_to_png(html, output_dir / "04_skills.png")
print(f"   ✓ Saved: {output_dir / '04_skills.png'}")
print()

# Save prompts for evaluation
prompt_storage.save()
print(f"   ✓ Prompts saved to: {prompt_storage.prompts_file}")

print("=" * 60)
print("✓ Creative Portfolio graphics generated successfully!")
print(f"   Output directory: {output_dir.absolute()}")
print(f"   Prompts stored: {len(prompt_storage.prompts)}")
print("=" * 60)
