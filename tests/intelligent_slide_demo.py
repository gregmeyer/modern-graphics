#!/usr/bin/env python3
"""Demo: Intelligent story slide generation combining visual primitives"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution, generate_intelligent_story_slide

def main():
    print("=" * 70)
    print("Intelligent Story Slide Generator")
    print("=" * 70)
    print("\nThis uses AI to design slide compositions by combining:")
    print("  • Data visualizations (charts)")
    print("  • Story metrics (key numbers)")
    print("  • Visual primitives (timelines, comparisons)")
    print("  • Narrative structure")
    print()
    
    generator = ModernGraphicsGenerator(
        "Data-Driven Stories",
        attribution=Attribution(copyright="© Intelligent Slide Demo 2025")
    )
    
    # Example 1: Weather data story
    print("Example 1: Weather Data Story")
    print("-" * 70)
    weather_prompt = """Create a weather data visualization showing urban heat island effect. 
    Cities are getting hotter faster than rural areas. Temperature difference increased from 
    1.5°C in 2000 to 3.2°C in 2023. This impacts energy consumption, health, and urban planning."""
    
    html1 = generate_intelligent_story_slide(generator, weather_prompt)
    output1 = Path(__file__).parent / "output" / "intelligent_weather.png"
    output1.parent.mkdir(parents=True, exist_ok=True)
    generator.export_to_png(html1, output1, viewport_width=1800, viewport_height=1200)
    print(f"✓ Generated: {output1}")
    
    # Example 2: Business growth story
    print("\nExample 2: Business Growth Story")
    print("-" * 70)
    business_prompt = """Show how our SaaS product grew from $500K ARR to $5M ARR over 3 years.
    Key milestones: Q1 2022 launched, Q4 2022 hit $1M, Q2 2023 hit $2.5M, Q4 2024 hit $5M.
    The acceleration happened after we added enterprise features."""
    
    html2 = generate_intelligent_story_slide(generator, business_prompt)
    output2 = Path(__file__).parent / "output" / "intelligent_business.png"
    generator.export_to_png(html2, output2, viewport_width=1800, viewport_height=1200)
    print(f"✓ Generated: {output2}")
    
    # Example 3: Comparison story
    print("\nExample 3: Before/After Comparison")
    print("-" * 70)
    comparison_prompt = """Compare manual slide creation vs AI-powered story generation.
    Before: 8 hours per slide, pixel-perfect but hard to update, requires design skills.
    After: 5 minutes per slide, data-driven and instantly updatable, focuses on narrative."""
    
    html3 = generate_intelligent_story_slide(generator, comparison_prompt)
    output3 = Path(__file__).parent / "output" / "intelligent_comparison.png"
    generator.export_to_png(html3, output3, viewport_width=1800, viewport_height=1200)
    print(f"✓ Generated: {output3}")
    
    print("\n" + "=" * 70)
    print("✓ All intelligent slides generated!")
    print("=" * 70)
    print("\nEach slide uses AI to:")
    print("  • Determine the best layout (data-focused, narrative-focused, comparison-focused)")
    print("  • Choose appropriate visual primitives")
    print("  • Create compelling headlines and insights")
    print("  • Combine charts, metrics, and annotations intelligently")

if __name__ == "__main__":
    main()
