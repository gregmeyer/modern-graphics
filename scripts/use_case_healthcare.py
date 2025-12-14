"""Use Case Example: Healthcare Conference Presentation

This example demonstrates creating appropriate graphics for a healthcare
conference presentation using sophisticated prompts with the unified story slide generator.
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
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "use_cases" / "healthcare"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(output_dir)

print("=" * 60)
print("Healthcare Conference Presentation - Use Case Example")
print("=" * 60)
print()

# Generate template from prompt
prompt = (
    "healthcare professional, clean blue and white, accessible fonts, "
    "trustworthy and calming, approachable and clear"
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
    "Healthcare Conference",
    template=template,
    attribution=Attribution(
        copyright="© Medical Research Institute 2025",
        context="Annual Healthcare Conference 2024"
    )
)

# 1. Research Findings Story Slide
print("1. Generating research findings story slide...")
prompt1 = """Present our clinical research findings showing improved treatment outcomes with the new protocol.
Patient recovery rates improved from 60% with traditional treatment to 85% with the new protocol over the 2022-2024 study period.
Recovery time decreased from 6 months to 3 months on average, significantly improving patient quality of life.
Treatment costs reduced by 30% while outcomes improved, demonstrating both clinical and economic benefits.
Show the correlation between treatment protocol adoption and patient outcomes with key metrics: 85% success rate, 3-month recovery time, 30% cost reduction, and 92% patient satisfaction."""
    html = generate_unified_story_slide(generator, prompt1, model="gpt-4-turbo-preview", temperature=0.7)
    output_file = output_dir / "01_findings.png"
    generator.export_to_png(html, output_file)
    prompt_storage.add_prompt(
        prompt=prompt1,
        output_file=output_file,
        use_case="healthcare",
        slide_type="story_slide",
        model="gpt-4-turbo-preview",
        temperature=0.7,
        metadata={"slide_number": 1, "title": "Research Findings", "study_period": "2022-2024"}
    )
print(f"   ✓ Saved: {output_file}")
print()

# 2. Study Timeline
print("2. Generating study timeline...")
html = generator.generate_timeline_diagram(
    items=[
        {'title': 'Phase 1', 'subtitle': '2022', 'description': 'Initial research and planning'},
        {'title': 'Phase 2', 'subtitle': '2023', 'description': 'Clinical trials begin'},
        {'title': 'Phase 3', 'subtitle': '2024', 'description': 'Results analysis and publication'}
    ],
    orientation='vertical'
)
generator.export_to_png(html, output_dir / "02_timeline.png")
print(f"   ✓ Saved: {output_dir / '02_timeline.png'}")
print()

# 3. Treatment Comparison
print("3. Generating treatment comparison...")
html = generator.generate_comparison_diagram(
    left_column=[{
        'title': 'Standard Treatment',
        'items': ['6-month recovery', '60% success rate', 'Higher cost'],
        'outcome': 'Standard outcomes'
    }],
    right_column=[{
        'title': 'New Protocol',
        'items': ['3-month recovery', '85% success rate', 'Lower cost'],
        'outcome': 'Improved outcomes'
    }]
)
generator.export_to_png(html, output_dir / "03_comparison.png")
print(f"   ✓ Saved: {output_dir / '03_comparison.png'}")
print()

# 4. Patient Journey Funnel
print("4. Generating patient journey funnel...")
html = generator.generate_funnel_diagram(
    stages=['Screening', 'Diagnosis', 'Treatment', 'Recovery', 'Follow-up'],
    values=[1000, 800, 600, 500, 450]
)
generator.export_to_png(html, output_dir / "04_patient_journey.png")
print(f"   ✓ Saved: {output_dir / '04_patient_journey.png'}")
print()

# Save prompts for evaluation
prompt_storage.save()
print(f"   ✓ Prompts saved to: {prompt_storage.prompts_file}")

print("=" * 60)
print("✓ Healthcare Conference graphics generated successfully!")
print(f"   Output directory: {output_dir.absolute()}")
print(f"   Prompts stored: {len(prompt_storage.prompts)}")
print("=" * 60)
