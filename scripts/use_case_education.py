"""Use Case Example: Educational Course Materials

This example demonstrates creating engaging graphics for educational course
materials using sophisticated prompts with the unified story slide generator.
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
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "use_cases" / "education"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(output_dir)

print("=" * 60)
print("Educational Course Materials - Use Case Example")
print("=" * 60)
print()

# Generate template from prompt
prompt = (
    "educational friendly, bright but not overwhelming, clear readable fonts, "
    "engaging and approachable, warm and inviting"
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
    "Course Materials",
    template=template,
    attribution=Attribution(copyright="© Education Platform 2025")
)

# 1. Student Progress Story Slide
print("1. Generating student progress story slide...")
prompt1 = """Show how students progress through our course, demonstrating skill acquisition over time.
Student skill levels increase from beginner (20%) at course start to advanced (85%) by course completion over a 12-week period.
Completion rates improved from 60% in 2023 to 78% in 2024, showing the effectiveness of our new curriculum.
Average student satisfaction scores increased from 4.2/5 to 4.7/5, indicating better learning outcomes.
Visualize the learning journey with metrics: 78% completion rate, 85% skill mastery, 4.7/5 satisfaction, and 92% job placement rate."""
    html = generate_unified_story_slide(generator, prompt1, model="gpt-4-turbo-preview", temperature=0.5)
    output_file = output_dir / "01_student_progress.png"
    generator.export_to_png(html, output_file)
    prompt_storage.add_prompt(
        prompt=prompt1,
        output_file=output_file,
        use_case="education",
        slide_type="story_slide",
        model="gpt-4-turbo-preview",
        temperature=0.5,
        metadata={"slide_number": 1, "title": "Student Progress"}
    )
print(f"   ✓ Saved: {output_file}")
print()

# 2. Course Modules Grid
print("2. Generating course modules grid...")
html = generator.generate_grid_diagram(
    items=[
        {'number': '1', 'text': 'Introduction'},
        {'number': '2', 'text': 'Core Concepts'},
        {'number': '3', 'text': 'Advanced Topics'},
        {'number': '4', 'text': 'Practice Exercises'},
        {'number': '5', 'text': 'Final Project'}
    ],
    columns=5,
    goal="Complete Course",
    outcome="Master the Skills"
)
generator.export_to_png(html, output_dir / "02_modules.png")
print(f"   ✓ Saved: {output_dir / '02_modules.png'}")
print()

# 3. Course Schedule Timeline
print("3. Generating course schedule timeline...")
html = generator.generate_timeline_diagram(
    items=[
        {'title': 'Week 1', 'subtitle': 'Foundations', 'description': 'Learn basics'},
        {'title': 'Week 2', 'subtitle': 'Building', 'description': 'Apply concepts'},
        {'title': 'Week 3', 'subtitle': 'Advanced', 'description': 'Master skills'},
        {'title': 'Week 4', 'subtitle': 'Project', 'description': 'Create final work'}
    ],
    orientation='horizontal'
)
generator.export_to_png(html, output_dir / "03_schedule.png")
print(f"   ✓ Saved: {output_dir / '03_schedule.png'}")
print()

# 4. Skill Transformation
print("4. Generating skill transformation...")
html = generator.generate_before_after_diagram(
    before_items=['Beginner knowledge', 'No practical experience', 'Uncertain'],
    after_items=['Expert understanding', 'Hands-on skills', 'Confident']
)
generator.export_to_png(html, output_dir / "04_transformation.png")
print(f"   ✓ Saved: {output_dir / '04_transformation.png'}")
print()

# Save prompts for evaluation
prompt_storage.save()
print(f"   ✓ Prompts saved to: {prompt_storage.prompts_file}")

print("=" * 60)
print("✓ Educational Course Materials graphics generated successfully!")
print(f"   Output directory: {output_dir.absolute()}")
print(f"   Prompts stored: {len(prompt_storage.prompts)}")
print("=" * 60)
