"""Example: Story Slide with Prompts and Visualization Heroes

Demonstrates:
1. Using prompts to generate story slides with visualization heroes
2. Unified story slide generator with visualization-first layouts
3. Combo charts as standalone diagram type
4. Both single and combo chart examples
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.env_config import get_openai_key
from modern_graphics.diagrams import generate_unified_story_slide, generate_combo_chart

# Output directory
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "story_slides"
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Story Slides with Prompts and Visualization Heroes")
print("=" * 60)
print()

# Check for OpenAI key
api_key = get_openai_key()
if not api_key:
    print("⚠️  OPENAI_API_KEY not found")
    print("   Set it in .env file to use prompt-based generation")
    print("   Some examples will be skipped")
    print()

generator = ModernGraphicsGenerator("Story-Driven Slides", attribution=Attribution())

# Example 1: Unified story slide with single chart (prompt-based)
if api_key:
    print("1. Unified story slide with single chart (prompt-based)...")
    prompt1 = """Show how ocean temperatures have risen dramatically over the past decade.
    The data shows a steady increase from 2014 to 2024, with temperatures rising from 20°C to 24°C.
    This represents a critical climate change indicator that affects marine ecosystems globally."""
    
    html = generate_unified_story_slide(generator, prompt1)
    generator.export_to_png(html, output_dir / "01_unified_single_chart.png")
    print(f"   ✓ Saved: {output_dir / '01_unified_single_chart.png'}")
    print()
    
    # Example 2: Unified story slide with combo chart (prompt-based)
    print("2. Unified story slide with combo chart (prompt-based)...")
    prompt2 = """Visualize the correlation between ocean heat content and extreme weather events.
    Ocean heat has increased from 100 zettajoules in 2010 to 180 zettajoules in 2024.
    Simultaneously, extreme weather events have increased from 50 events per year to 120 events per year.
    Show both metrics on a dual-axis combo chart to demonstrate the correlation."""
    
    html = generate_unified_story_slide(generator, prompt2)
    generator.export_to_png(html, output_dir / "02_unified_combo_chart.png")
    print(f"   ✓ Saved: {output_dir / '02_unified_combo_chart.png'}")
    print()
    
    # Example 3: Standalone combo chart
    print("3. Standalone combo chart diagram...")
    primary_data = [
        {"x": "2020", "y": 100},
        {"x": "2021", "y": 110},
        {"x": "2022", "y": 125},
        {"x": "2023", "y": 150},
        {"x": "2024", "y": 180}
    ]
    secondary_data = [
        {"x": "2020", "y": 50},
        {"x": "2021", "y": 65},
        {"x": "2022", "y": 80},
        {"x": "2023", "y": 100},
        {"x": "2024", "y": 120}
    ]
    
    html = generate_combo_chart(
        generator,
        primary_data=primary_data,
        secondary_data=secondary_data,
        primary_style="line",
        secondary_style="bars",
        primary_name="Ocean Heat (ZJ)",
        secondary_name="Extreme Events"
    )
    generator.export_to_png(html, output_dir / "03_combo_chart_standalone.png")
    print(f"   ✓ Saved: {output_dir / '03_combo_chart_standalone.png'}")
    print()
    
    # Example 4: Legacy story slide with prompt (backward compatible)
    print("4. Legacy story slide with prompt (backward compatible)...")
    html = generator.generate_story_slide(
        prompt="Show how renewable energy adoption has accelerated globally, with solar and wind capacity tripling from 2020 to 2024",
        use_unified=True
    )
    generator.export_to_png(html, output_dir / "04_legacy_with_prompt.png")
    print(f"   ✓ Saved: {output_dir / '04_legacy_with_prompt.png'}")
    print()
else:
    print("1-4. Skipping prompt-based examples (no OPENAI_API_KEY)")
    print()

# Example 5: Legacy story slide (parameter-based, still works)
print("5. Legacy story slide (parameter-based)...")
html = generator.generate_story_slide(
    title="The Future of Presentations",
    what_changed="Shift from manual slide creation to AI-powered story generation",
    time_period="2020-2024",
    what_it_means="Teams can focus on insights instead of design",
    use_ai_hero=False,
    use_unified=False
)
generator.export_to_png(html, output_dir / "05_legacy_parameters.png")
print(f"   ✓ Saved: {output_dir / '05_legacy_parameters.png'}")
print()

print("=" * 60)
print("✓ Story slide examples generated!")
print(f"   Output directory: {output_dir.absolute()}")
print("=" * 60)
