"""Use Case Example: Corporate Quarterly Report

This example demonstrates creating professional graphics for a corporate
quarterly report using sophisticated prompts with the unified story slide generator.
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
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "use_cases" / "corporate"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(output_dir)

print("=" * 60)
print("Corporate Quarterly Report - Use Case Example")
print("=" * 60)
print()

# Generate template from prompt
prompt = (
    "corporate blue and gray, professional, traditional fonts, conservative and "
    "trustworthy, formal and authoritative"
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
    "Q4 Corporate Report",
    template=template,
    attribution=Attribution(
        copyright="© Corporation Inc 2025",
        context="Q4 2024 Quarterly Report"
    )
)

# 1. Q4 Performance Story Slide
print("1. Generating Q4 performance story slide...")
prompt1 = """Visualize our Q4 2024 corporate performance showing strong growth acceleration.
Revenue increased from $50M in Q3 to $58M in Q4, representing 16% quarter-over-quarter growth compared to 5% in Q3.
Profit margins improved from 22% to 25%, demonstrating operational efficiency gains.
This performance exceeded analyst expectations and positions us well for continued growth in 2025.
Show the revenue trajectory as a line chart with key metrics: $58M revenue, 16% growth rate, 25% margin, and $14.5M profit."""
    html = generate_unified_story_slide(generator, prompt1, model="gpt-4-turbo-preview", temperature=0.7)
    output_file = output_dir / "01_q4_performance.png"
    generator.export_to_png(html, output_file)
    prompt_storage.add_prompt(
        prompt=prompt1,
        output_file=output_file,
        use_case="corporate",
        slide_type="story_slide",
        model="gpt-4-turbo-preview",
        temperature=0.7,
        metadata={"slide_number": 1, "title": "Q4 Performance", "quarter": "Q4 2024"}
    )
print(f"   ✓ Saved: {output_file}")
print()

# 2. Sales Funnel (stubbed - commented out)
# print("2. Generating sales funnel...")
# html = generator.generate_funnel_diagram(
#     stages=['Leads', 'Qualified', 'Proposals', 'Closed'],
#     values=[1000, 500, 200, 75]
# )
# generator.export_to_png(html, output_dir / "02_sales_funnel.png")
# print(f"   ✓ Saved: {output_dir / '02_sales_funnel.png'}")
# print()

# 3. Organizational Structure (stubbed - commented out)
# print("3. Generating organizational structure pyramid...")
# html = generator.generate_pyramid_diagram(
#     levels=[
#         {'title': 'Executive', 'items': ['CEO', 'CFO', 'CTO']},
#         {'title': 'VP Level', 'items': ['VP Sales', 'VP Marketing', 'VP Engineering']},
#         {'title': 'Directors', 'items': ['Sales Directors', 'Engineering Directors']},
#         {'title': 'Managers', 'items': ['Team Managers', 'Project Managers']},
#         {'title': 'Individual Contributors', 'items': ['Engineers', 'Sales Reps', 'Support']}
#     ]
# )
# generator.export_to_png(html, output_dir / "03_org_structure.png")
# print(f"   ✓ Saved: {output_dir / '03_org_structure.png'}")
# print()

# 4. Quarterly Timeline
print("4. Generating quarterly timeline...")
html = generator.generate_timeline_diagram(
    events=[
        {'date': 'Q1 2024', 'text': 'Foundation', 'color': '#007AFF'},
        {'date': 'Q2 2024', 'text': 'Growth', 'color': '#007AFF'},
        {'date': 'Q3 2024', 'text': 'Expansion', 'color': '#007AFF'},
        {'date': 'Q4 2024', 'text': 'Strong finish', 'color': '#007AFF'}
    ],
    orientation='horizontal'
)
generator.export_to_png(html, output_dir / "04_quarterly_timeline.png")
print(f"   ✓ Saved: {output_dir / '04_quarterly_timeline.png'}")
print()

# Save prompts for evaluation
prompt_storage.save()
print(f"   ✓ Prompts saved to: {prompt_storage.prompts_file}")

print("=" * 60)
print("✓ Corporate Quarterly Report graphics generated successfully!")
print(f"   Output directory: {output_dir.absolute()}")
print(f"   Prompts stored: {len(prompt_storage.prompts)}")
print("=" * 60)
