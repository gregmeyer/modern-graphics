"""Use Case Example: Tech Startup Pitch Deck

This example demonstrates creating graphics for a tech startup pitch deck
using sophisticated prompts with the unified story slide generator.
Prompts are stored for evaluation purposes.
"""

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
from modern_graphics.diagrams import generate_unified_story_slide, generate_combo_chart
from prompt_storage import PromptStorage

# Output directory (goes to generated/ for temporary outputs)
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "use_cases" / "tech_startup"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(output_dir)

print("=" * 60)
print("Tech Startup Pitch Deck - Use Case Example")
print("=" * 60)
print()

# Generate template from prompt
prompt = (
    "bold vibrant colors with blue and purple accents, tech startup aesthetic, "
    "clean modern sans-serif font, energetic and innovative feel, high contrast for impact"
)

print(f"Generating template from prompt:")
print(f'  "{prompt}"')
print()

template = quick_template_from_description(prompt)
register_template(template)
print(f"✓ Template created: {template.name}")
print()

# Create generator with template
generator = ModernGraphicsGenerator(
    "Startup Pitch Deck",
    template=template,
    attribution=Attribution(copyright="© Startup Inc 2025")
)

# 1. Product Vision Story Slide
print("1. Generating product vision story slide...")
prompt1 = """Show how our AI platform transforms manual business processes into automated intelligence.
The transformation happened rapidly from 2024 to 2025, with efficiency improvements increasing from 1x baseline to 10x efficiency.
This represents a fundamental shift in how businesses operate, enabling teams to focus on strategic work instead of repetitive tasks.
Include metrics showing: processing time reduced from 8 hours to 45 minutes, accuracy improved from 85% to 99.5%, and cost savings of $2M annually."""
    html = generate_unified_story_slide(generator, prompt1, model="gpt-4-turbo-preview", temperature=0.5)
    output_file = output_dir / "01_product_vision.png"
    generator.export_to_png(html, output_file)
    prompt_storage.add_prompt(
        prompt=prompt1,
        output_file=output_file,
        use_case="tech_startup",
        slide_type="story_slide",
        model="gpt-4-turbo-preview",
        temperature=0.5,
        metadata={"slide_number": 1, "title": "Product Vision"}
    )
print(f"   ✓ Saved: {output_file}")
print()

# 2. Before/After Comparison
print("2. Generating before/after comparison...")
html = generator.generate_comparison_diagram(
    left_column={
        'title': 'Before AI',
        'steps': ['Manual processes', 'Hours per task', 'Error-prone', 'Slow scaling']
    },
    right_column={
        'title': 'With Our AI',
        'steps': ['Automated workflows', 'Minutes per task', '99.9% accuracy', 'Instant scaling']
    }
)
generator.export_to_png(html, output_dir / "02_comparison.png")
print(f"   ✓ Saved: {output_dir / '02_comparison.png'}")
print()

# 3. Growth Timeline
print("3. Generating growth timeline...")
html = generator.generate_timeline_diagram(
    events=[
        {'date': 'Q1 2024', 'text': 'Launch - 100 users', 'color': 'blue'},
        {'date': 'Q2 2024', 'text': 'Growth - 1,000 users', 'color': 'green'},
        {'date': 'Q3 2024', 'text': 'Scale - 10,000 users', 'color': 'orange'},
        {'date': 'Q4 2024', 'text': 'Expansion - 100,000 users', 'color': 'purple'}
    ],
    orientation='horizontal'
)
generator.export_to_png(html, output_dir / "03_growth_timeline.png")
print(f"   ✓ Saved: {output_dir / '03_growth_timeline.png'}")
print()

# 4. Revenue vs User Growth Combo Chart
print("4. Generating revenue vs user growth combo chart...")
prompt4 = """Show the correlation between user growth and revenue growth using a dual-axis combo chart.
User base grew from 1,000 in Q1 2024 to 8,000 in Q4 2024, representing 700% growth.
Simultaneously, revenue increased from $50K in Q1 to $120K in Q4, showing strong monetization.
The correlation demonstrates that as we acquire more users, revenue scales proportionally.
Visualize both metrics on a combo chart: user growth as a line (left axis) and revenue as bars (right axis)."""
    html = generate_unified_story_slide(generator, prompt4, model="gpt-4-turbo-preview", temperature=0.8)
    output_file = output_dir / "04_revenue_vs_users.png"
    generator.export_to_png(html, output_file)
    prompt_storage.add_prompt(
        prompt=prompt4,
        output_file=output_file,
        use_case="tech_startup",
        slide_type="story_slide_combo",
        model="gpt-4-turbo-preview",
        temperature=0.5,
        metadata={"slide_number": 4, "title": "Revenue vs User Growth", "chart_type": "combo"}
    )
print(f"   ✓ Saved: {output_file}")
print()

# Save prompts for evaluation
prompt_storage.save()
print(f"   ✓ Prompts saved to: {prompt_storage.prompts_file}")

print("=" * 60)
print("✓ Tech Startup Pitch Deck graphics generated successfully!")
print(f"   Output directory: {output_dir.absolute()}")
print(f"   Prompts stored: {len(prompt_storage.prompts)}")
print("=" * 60)
