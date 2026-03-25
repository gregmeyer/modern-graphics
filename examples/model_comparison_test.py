"""Test: Compare outputs across different models

This script demonstrates how different models produce different outputs
for the same prompt, showing the variability in AI-generated designs.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams import generate_unified_story_slide
from modern_graphics.env_config import get_openai_key

# Check for API key
api_key = get_openai_key()
if not api_key:
    print("⚠️  OPENAI_API_KEY not found")
    print("   Set it in .env file to run this test")
    sys.exit(1)

# Output directory
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated" / "model_comparison"
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Model Comparison Test")
print("=" * 60)
print()
print("Testing the same prompt with different models to show variability")
print()

# Test prompt
test_prompt = """Show how renewable energy adoption has accelerated globally.
Solar and wind capacity tripled from 2020 to 2024, growing from 500 GW to 1,500 GW.
This represents a major shift toward clean energy, reducing carbon emissions by 2 billion tons annually.
Visualize the growth trajectory with key metrics: 1,500 GW capacity, 200% growth rate, and $300B investment."""

print(f"Test Prompt:")
print(f"  {test_prompt}")
print()

generator = ModernGraphicsGenerator("Model Comparison", attribution=Attribution())

# Models to test
models_to_test = [
    ("gpt-4-turbo-preview", "GPT-4 Turbo (default)"),
    ("gpt-4o", "GPT-4o (newer, faster)"),
    ("gpt-4", "GPT-4 (original)"),
    # Note: gpt-3.5-turbo may not support JSON mode as well
]

print("Generating slides with different models...")
print()

results = []

for model_name, model_description in models_to_test:
    try:
        print(f"Testing {model_description} ({model_name})...")
        
        html = generate_unified_story_slide(
            generator,
            test_prompt,
            model=model_name
        )
        
        output_file = output_dir / f"output_{model_name.replace('-', '_')}.png"
        generator.export_to_png(html, output_file)
        
        results.append({
            "model": model_name,
            "description": model_description,
            "file": output_file,
            "success": True
        })
        
        print(f"   ✓ Saved: {output_file}")
        
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append({
            "model": model_name,
            "description": model_description,
            "success": False,
            "error": str(e)
        })
    
    print()

print("=" * 60)
print("Results Summary")
print("=" * 60)
print()

for result in results:
    if result["success"]:
        print(f"✓ {result['description']}: {result['file'].name}")
    else:
        print(f"✗ {result['description']}: {result.get('error', 'Unknown error')}")

print()
print("=" * 60)
print("Key Observations:")
print("=" * 60)
print("""
1. Different models will produce DIFFERENT outputs:
   - Different headlines and subheadlines
   - Different layout choices
   - Different color schemes
   - Different visualization types (may choose line vs bar vs area)
   - Different metric selections

2. Why outputs vary:
   - Each model has different training data and capabilities
   - Temperature settings (0.8 for unified_story_slide) add randomness
   - Models interpret prompts differently
   - JSON structure allows flexibility in design choices

3. Model characteristics:
   - gpt-4-turbo-preview: Good balance, current default
   - gpt-4o: Newer, faster, may be more creative
   - gpt-4: Original, more conservative outputs
   - gpt-3.5-turbo: Faster but less capable, may struggle with complex JSON

4. For consistent outputs:
   - Use same model
   - Lower temperature (but reduces creativity)
   - More specific prompts (less room for interpretation)
   - Seed parameter (if supported by model)

5. For evaluation:
   - Test with multiple models to see range of outputs
   - Compare quality, not exact match
   - Consider which model best fits your use case
""")

print(f"\nAll outputs saved to: {output_dir.absolute()}")
print("=" * 60)
