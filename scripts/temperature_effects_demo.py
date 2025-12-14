"""Demonstration: Temperature Effects on Story Slide Generation

This example shows how temperature affects the creativity and variability
of AI-generated story slides. Higher temperature = more creative/varied outputs.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams import generate_unified_story_slide
from modern_graphics.env_config import get_openai_key
from prompt_storage import PromptStorage

# Check for API key
api_key = get_openai_key()
if not api_key:
    print("⚠️  OPENAI_API_KEY not found")
    print("   Set it in .env file to run this demo")
    sys.exit(1)

# Output directory
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "temperature_demo"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize prompt storage
prompt_storage = PromptStorage(output_dir)

print("=" * 60)
print("Temperature Effects Demonstration")
print("=" * 60)
print()
print("Generating the same creative prompt with different temperature settings")
print("to show how temperature affects creativity and variability.")
print()

# Creative prompt designed to show temperature effects
creative_prompt = """Create a story slide about the rise of AI-generated art and its impact on the creative industry.
The transformation happened from 2020 to 2024, with AI art tools going from experimental to mainstream.
Show how AI-generated artwork sales increased from $0 in 2020 to $2.5B in 2024, while traditional art sales 
grew more slowly from $50B to $65B. Include the dramatic shift in artist adoption rates, creative tool 
usage, and the emergence of new art styles. Visualize the tension between traditional and AI-assisted 
creativity, showing both the opportunities and challenges. Make it visually striking and thought-provoking."""

print(f"Creative Prompt:")
print(f"  {creative_prompt[:100]}...")
print()

generator = ModernGraphicsGenerator(
    "Temperature Effects Demo",
    attribution=Attribution(copyright="© Temperature Demo 2025")
)

# Temperature settings to test
temperature_settings = [
    (0.3, "Low (Deterministic, Focused)"),
    (0.8, "Medium (Balanced, Default)"),
    (1.2, "High (Creative, Varied)"),
    (1.5, "Very High (Highly Creative, Unpredictable)")
]

model = "gpt-4-turbo-preview"

print(f"Model: {model}")
print(f"Testing {len(temperature_settings)} temperature settings...")
print()

for temp, description in temperature_settings:
    print(f"Temperature {temp} - {description}")
    print("-" * 60)
    
    try:
        html = generate_unified_story_slide(
            generator,
            creative_prompt,
            model=model,
            temperature=temp
        )
        
        output_file = output_dir / f"temperature_{temp:.1f}.png"
        generator.export_to_png(html, output_file)
        
        prompt_storage.add_prompt(
            prompt=creative_prompt,
            output_file=output_file,
            use_case="temperature_demo",
            slide_type="story_slide",
            model=model,
            temperature=temp,
            metadata={
                "temperature_setting": temp,
                "description": description,
                "test_type": "temperature_comparison"
            }
        )
        
        print(f"   ✓ Generated and saved: {output_file.name}")
        print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"   ✗ Failed: {e}")
    
    print()

# Save prompts
prompt_storage.save()

print("=" * 60)
print("Temperature Effects Summary")
print("=" * 60)
print()
print("Expected differences you'll see:")
print()
print("Temperature 0.3 (Low):")
print("  - More predictable, conservative designs")
print("  - Similar layouts across runs")
print("  - Standard color choices")
print("  - Straightforward headlines")
print()
print("Temperature 0.8 (Medium - Default):")
print("  - Balanced creativity and consistency")
print("  - Good variety without being too random")
print("  - Professional but interesting")
print()
print("Temperature 1.2 (High):")
print("  - More creative and varied")
print("  - Unexpected layout choices")
print("  - Bold color schemes")
print("  - More expressive headlines")
print()
print("Temperature 1.5 (Very High):")
print("  - Highly creative and unpredictable")
print("  - May have unusual design choices")
print("  - Very expressive and unique")
print("  - May occasionally be less coherent")
print()
print("=" * 60)
print("Key Insights:")
print("=" * 60)
print("""
1. Lower temperature (0.0-0.5):
   - More consistent outputs
   - Better for production/reproducibility
   - Less creative variation
   - Good for when you want predictable results

2. Medium temperature (0.6-1.0):
   - Good balance of creativity and consistency
   - Recommended for most use cases
   - Default setting (0.8) works well

3. Higher temperature (1.1-2.0):
   - More creative and varied outputs
   - Better for exploration and ideation
   - May produce unexpected but interesting results
   - Good for when you want to see different approaches

4. For evaluation:
   - Test multiple temperatures to find optimal setting
   - Lower temp for consistency, higher for creativity
   - Document temperature used for reproducibility
""")

print(f"\nAll outputs saved to: {output_dir.absolute()}")
print(f"Prompts stored in: {prompt_storage.prompts_file}")
print("=" * 60)
