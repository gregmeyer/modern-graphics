#!/usr/bin/env python3
"""Generate showcase examples for README

This script generates high-quality showcase examples for the README.
All outputs go to examples/output/showcase/ and are tracked in git.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import (
    ModernGraphicsGenerator,
    Attribution,
    quick_template_from_description,
    register_template,
)
from modern_graphics.prompt_to_diagram import (
    DEFAULT_DIAGRAM_PROMPTS,
    generate_cycle_diagram_from_prompt,
    generate_comparison_diagram_from_prompt,
    generate_timeline_diagram_from_prompt,
    generate_grid_diagram_from_prompt,
    generate_flywheel_diagram_from_prompt,
    generate_slide_cards_from_prompt,
    generate_slide_card_comparison_from_prompt,
)
from modern_graphics.diagrams.unified_story_slide import generate_unified_story_slide
from prompt_storage import PromptStorage

# Output directories (relative to project root, not scripts/)
showcase_dir = Path(__file__).parent.parent / "examples" / "output" / "showcase"
diagram_types_dir = showcase_dir / "diagram-types"
templates_dir = showcase_dir / "templates"
attribution_dir = showcase_dir / "attribution"
use_cases_dir = showcase_dir / "use-cases"

# Create directories
for dir_path in [diagram_types_dir, templates_dir, attribution_dir, use_cases_dir]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(showcase_dir)

print("=" * 70)
print("Generating Showcase Examples")
print("=" * 70)
print()

# Use high-quality export settings with tight cropping
# Smaller viewport to reduce whitespace - content will be cropped automatically
export_kwargs = {
    "viewport_width": 1200,
    "viewport_height": 800,
    "device_scale_factor": 2,
    "padding": 5,  # Very minimal padding for tight crop
}

# Default attribution for showcase
showcase_attribution = Attribution(
    copyright="© Modern Graphics 2025",
    context="Showcase Example",
    position="bottom-right",
)

# ============================================================================
# DIAGRAM TYPES - One example of each type (prompt-based)
# ============================================================================
print("📊 Generating Diagram Type Examples...")
print()

generator = ModernGraphicsGenerator("Diagram Showcase", attribution=showcase_attribution)

# Optional: Override defaults with custom prompts
CUSTOM_PROMPTS = {
    # 'cycle': "Custom cycle prompt here...",
    # 'comparison': "Custom comparison prompt here...",
    # Leave empty to use defaults
}

# 1. Cycle Diagram
print("  1. Cycle Diagram...")
prompt = CUSTOM_PROMPTS.get('cycle')  # None if not overridden, will use default
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['cycle']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_cycle_diagram_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "01-cycle.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['cycle'],
    output_file=output_file,
    use_case="showcase",
    slide_type="cycle",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/01-cycle.png")

# 2. Comparison Diagram
print("  2. Comparison Diagram...")
prompt = CUSTOM_PROMPTS.get('comparison')
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['comparison']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_comparison_diagram_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "02-comparison.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['comparison'],
    output_file=output_file,
    use_case="showcase",
    slide_type="comparison",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/02-comparison.png")

# 3. Timeline Diagram
print("  3. Timeline Diagram...")
prompt = CUSTOM_PROMPTS.get('timeline')
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['timeline']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_timeline_diagram_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "03-timeline.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['timeline'],
    output_file=output_file,
    use_case="showcase",
    slide_type="timeline",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/03-timeline.png")

# 4. Story Slide
print("  4. Story Slide...")
prompt = CUSTOM_PROMPTS.get('story_slide') or DEFAULT_DIAGRAM_PROMPTS['story_slide']
html = generate_unified_story_slide(generator, prompt, model="gpt-4-turbo-preview")
output_file = diagram_types_dir / "04-story-slide.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt,
    output_file=output_file,
    use_case="showcase",
    slide_type="story_slide",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types"}
)
print("     ✓ Saved: diagram-types/04-story-slide.png")

# 5. Grid Diagram
print("  5. Grid Diagram...")
prompt = CUSTOM_PROMPTS.get('grid')
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['grid']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_grid_diagram_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "05-grid.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['grid'],
    output_file=output_file,
    use_case="showcase",
    slide_type="grid",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/05-grid.png")

# 6. Flywheel Diagram
print("  6. Flywheel Diagram...")
prompt = CUSTOM_PROMPTS.get('flywheel')
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['flywheel']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_flywheel_diagram_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "06-flywheel.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['flywheel'],
    output_file=output_file,
    use_case="showcase",
    slide_type="flywheel",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/06-flywheel.png")

# 7. Slide Cards
print("  7. Slide Cards...")
prompt = CUSTOM_PROMPTS.get('slide_cards')
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['slide_cards']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_slide_cards_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "07-slide-cards.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['slide_cards'],
    output_file=output_file,
    use_case="showcase",
    slide_type="slide_cards",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/07-slide-cards.png")

# 8. Slide Card Comparison
print("  8. Slide Card Comparison...")
prompt = CUSTOM_PROMPTS.get('slide_card_comparison')
if prompt is None:
    prompt = DEFAULT_DIAGRAM_PROMPTS['slide_card_comparison']
print(f"     Using prompt: {prompt[:80]}...")
html = generate_slide_card_comparison_from_prompt(generator, prompt=prompt)
output_file = diagram_types_dir / "08-slide-comparison.png"
generator.export_to_png(html, output_file, **export_kwargs)
prompt_storage.add_prompt(
    prompt=prompt or DEFAULT_DIAGRAM_PROMPTS['slide_card_comparison'],
    output_file=output_file,
    use_case="showcase",
    slide_type="slide_card_comparison",
    model="gpt-4-turbo-preview",
    metadata={"showcase": True, "category": "diagram_types", "used_default": prompt is None}
)
print("     ✓ Saved: diagram-types/08-slide-comparison.png")

print()

# ============================================================================
# TEMPLATES - Showcase different template styles
# ============================================================================
print("🎨 Generating Template Examples...")
print()

# Default Template
print("  1. Default Template...")
default_gen = ModernGraphicsGenerator(
    "Default Style",
    attribution=Attribution(copyright="© Example 2025")
)
html = default_gen.generate_cycle_diagram([
    {'text': 'Design', 'color': 'blue'},
    {'text': 'Develop', 'color': 'green'},
    {'text': 'Deploy', 'color': 'orange'},
])
default_gen.export_to_png(html, templates_dir / "default.png", **export_kwargs)
print("     ✓ Saved: templates/default.png")

# Corporate Template
print("  2. Corporate Template...")
corporate_prompt = (
    "corporate blue and gray, professional, traditional fonts, "
    "conservative and trustworthy, formal and authoritative"
)
corporate_template = quick_template_from_description(corporate_prompt)
corporate_gen = ModernGraphicsGenerator(
    "Corporate Style",
    template=corporate_template,
    attribution=Attribution(copyright="© Corporation Inc 2025")
)
html = corporate_gen.generate_comparison_diagram(
    left_column={
        'title': 'Q3 2024',
        'steps': ['Revenue: $50M', 'Growth: 5%', 'Margin: 22%']
    },
    right_column={
        'title': 'Q4 2024',
        'steps': ['Revenue: $58M', 'Growth: 16%', 'Margin: 25%']
    }
)
corporate_gen.export_to_png(html, templates_dir / "corporate.png", **export_kwargs)
print("     ✓ Saved: templates/corporate.png")

# Tech Startup Template
print("  3. Tech Startup Template...")
tech_prompt = (
    "bold vibrant colors with blue and purple accents, tech startup aesthetic, "
    "clean modern sans-serif font, energetic and innovative feel"
)
tech_template = quick_template_from_description(tech_prompt)
tech_gen = ModernGraphicsGenerator(
    "Tech Startup Style",
    template=tech_template,
    attribution=Attribution(copyright="© Startup Inc 2025")
)
html = tech_gen.generate_flywheel_diagram(
    elements=[
        {'text': 'Acquire', 'color': 'blue'},
        {'text': 'Activate', 'color': 'green'},
        {'text': 'Retain', 'color': 'orange'},
        {'text': 'Refer', 'color': 'purple'}
    ],
    center_label="Growth"
)
tech_gen.export_to_png(html, templates_dir / "tech-startup.png", **export_kwargs)
print("     ✓ Saved: templates/tech-startup.png")

print()

# ============================================================================
# ATTRIBUTION - Showcase different attribution configurations
# ============================================================================
print("🏷️  Generating Attribution Examples...")
print()

base_generator = ModernGraphicsGenerator("Attribution Showcase")

# Default Attribution
print("  1. Default Attribution...")
html = base_generator.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'},
])
base_generator.export_to_png(html, attribution_dir / "default.png", **export_kwargs)
print("     ✓ Saved: attribution/default.png")

# Custom Styled Attribution
print("  2. Custom Styled Attribution...")
custom_gen = ModernGraphicsGenerator(
    "Custom Attribution",
    attribution=Attribution(
        copyright="© My Company 2025",
        context="Q4 Report",
        font_size="14px",
        font_color="#FFFFFF",
        font_weight="600",
        background_color="rgba(0, 0, 0, 0.7)",
        opacity=0.9,
        padding="10px 16px",
        border_radius="8px",
    )
)
html = custom_gen.generate_cycle_diagram([
    {'text': 'Step 1', 'color': 'blue'},
    {'text': 'Step 2', 'color': 'green'},
])
custom_gen.export_to_png(html, attribution_dir / "custom-styled.png", **export_kwargs)
print("     ✓ Saved: attribution/custom-styled.png")

# Attribution with Context
print("  3. Attribution with Context...")
context_gen = ModernGraphicsGenerator(
    "Context Attribution",
    attribution=Attribution(
        copyright="© Brand Name 2025",
        context="Generated for Annual Report",
        position="bottom-center",
        font_size="12px",
    )
)
html = context_gen.generate_timeline_diagram(
    events=[
        {'date': '2024 Q1', 'text': 'Planning', 'color': 'blue'},
        {'date': '2024 Q2', 'text': 'Development', 'color': 'green'},
        {'date': '2024 Q3', 'text': 'Launch', 'color': 'orange'},
    ],
    orientation='horizontal'
)
context_gen.export_to_png(html, attribution_dir / "with-context.png", **export_kwargs)
print("     ✓ Saved: attribution/with-context.png")

print()

# ============================================================================
# USE CASES - Best use case examples
# ============================================================================
print("💼 Generating Use Case Examples...")
print()

# Corporate Report Use Case
print("  1. Corporate Quarterly Report...")
corporate_template = quick_template_from_description(
    "corporate blue and gray, professional, traditional fonts, conservative"
)
corporate_use_gen = ModernGraphicsGenerator(
    "Q4 Corporate Report",
    template=corporate_template,
    attribution=Attribution(
        copyright="© Corporation Inc 2025",
        context="Q4 2024 Quarterly Report"
    )
)
html = corporate_use_gen.generate_comparison_diagram(
    left_column={
        'title': 'Q3 2024',
        'steps': ['Revenue: $50M', 'Growth: 5%', 'Margin: 22%'],
        'outcome': 'Steady growth'
    },
    right_column={
        'title': 'Q4 2024',
        'steps': ['Revenue: $58M', 'Growth: 16%', 'Margin: 25%'],
        'outcome': 'Strong performance'
    }
)
corporate_use_gen.export_to_png(html, use_cases_dir / "corporate-report.png", **export_kwargs)
print("     ✓ Saved: use-cases/corporate-report.png")

# Tech Startup Pitch Use Case
print("  2. Tech Startup Pitch Deck...")
tech_template = quick_template_from_description(
    "bold vibrant colors with blue and purple accents, tech startup aesthetic, clean modern sans-serif"
)
tech_use_gen = ModernGraphicsGenerator(
    "Startup Pitch Deck",
    template=tech_template,
    attribution=Attribution(copyright="© Startup Inc 2025")
)
html = tech_use_gen.generate_story_slide(
    title="Product Launch",
    what_changed="User base grew from 1K to 50K",
    time_period="Q1-Q4 2024",
    what_it_means="Product-market fit achieved",
    insight="Rapid growth validates our core value proposition"
)
tech_use_gen.export_to_png(html, use_cases_dir / "tech-pitch.png", **export_kwargs)
print("     ✓ Saved: use-cases/tech-pitch.png")

# Educational Course Use Case
print("  3. Educational Course Materials...")
edu_gen = ModernGraphicsGenerator(
    "Course Materials",
    attribution=Attribution(
        copyright="© Education Inc 2025",
        context="Introduction to Data Science"
    )
)
html = edu_gen.generate_timeline_diagram(
    events=[
        {'date': 'Week 1', 'text': 'Introduction & Setup', 'color': 'blue'},
        {'date': 'Week 2', 'text': 'Data Collection', 'color': 'green'},
        {'date': 'Week 3', 'text': 'Analysis & Visualization', 'color': 'orange'},
        {'date': 'Week 4', 'text': 'Final Project', 'color': 'purple'},
    ],
    orientation='horizontal'
)
edu_gen.export_to_png(html, use_cases_dir / "educational-course.png", **export_kwargs)
print("     ✓ Saved: use-cases/educational-course.png")

print()

# Save prompts to file
prompt_storage.save()

print()
print("=" * 70)
print("✓ Showcase examples generated successfully!")
print(f"   Output directory: {showcase_dir.absolute()}")
print(f"   Prompts saved to: {prompt_storage.prompts_file}")
print("=" * 70)
