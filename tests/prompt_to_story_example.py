#!/usr/bin/env python3
"""Example: Generate story slides from detailed prompts"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import (
    ModernGraphicsGenerator,
    Attribution,
    generate_story_from_prompt,
    create_story_slide_from_prompt
)
from modern_graphics.env_config import get_openai_key

def main():
    print("=" * 70)
    print("Prompt-to-Story Slide Generation")
    print("=" * 70)
    
    if not get_openai_key():
        print("\n⚠️  OPENAI_API_KEY not found!")
        return
    
    # Your weather prompt
    weather_prompt = """# Story-Driven Data Visualization Slide (Weather)

## Role
You are a **story-driven visualization designer** building presentation-ready graphics.  
Your job is to turn a narrative insight into a clear, persuasive visual — **not** to decorate data.

---

## Task
Create **one presentation slide** that visualizes a **weather-related story**.

The slide must clearly answer:

> **What changed, over what time period, and why it matters.**

---

## Inputs
You may be given — or must reasonably infer — the following:

- **Story context** (the narrative the slide supports)
- **Weather dimension(s)**  
  (e.g., temperature, precipitation, snowfall, heat index, extreme events)
- **Time range**  
  (e.g., last 7 days, seasonal trend, year-over-year)
- **Audience**  
  (executive, product, general)
- **Output format**  
  (SVG, presentation slide layout, or design spec)

If any inputs are missing, make a **reasonable assumption** and **note it explicitly** in the output.

---

## Slide Requirements

### 1. Narrative First
- Identify the **single insight** the slide should communicate.
- Choose **one chart type** that best supports the story:
  - **Line chart** → change over time
  - **Bar chart** → comparison across periods
  - **Area chart** → accumulation or intensity
- Avoid multi-chart clutter.

---

### 2. Layout & Hierarchy
Design the slide with a clear, presentation-ready hierarchy:

1. **Headline (top)**  
   - Declarative and insight-driven  
   - Example:  
     > *"Heat waves are lasting longer — not just getting hotter."*

2. **Visualization (center)**  
   - Clean, legible chart
   - Highlight the key change (annotation, accent color, or callout)
   - Minimal gridlines and labels

3. **Story Annotations (adjacent or below)**  
   - 1–2 short callouts explaining:
     - What changed
     - Why it matters

4. **Footer (small)**  
   - Data source (real or representative)
   - Time range covered

---

## Visual Style
- Presentation-grade (not dashboard-dense)
- Neutral color palette with **one accent color**
- Generous whitespace
- Readable from a distance (meeting-room test)

---

## Output Format
Return the slide as **structured JSON**:

```json
{
  "slideType": "data-story",
  "topic": "weather",
  "headline": "",
  "timeRange": "",
  "visualization": {
    "chartType": "",
    "xAxis": "",
    "yAxis": "",
    "highlight": ""
  },
  "annotations": [],
  "designNotes": "",
  "dataAssumptions": ""
}
"""
    
    print("\n📝 Processing detailed prompt...")
    print("   (This extracts story elements and generates a slide)\n")
    
    try:
        # Method 1: Extract story data first
        print("Method 1: Extract story elements from prompt")
        print("-" * 70)
        story_data = generate_story_from_prompt(weather_prompt)
        
        if story_data:
            print("\n✓ Extracted story elements:")
            print(f"  Title: {story_data.get('title')}")
            print(f"  Headline: {story_data.get('headline')}")
            print(f"  Visualization Type: {story_data.get('visualization_type')}")
            print(f"  Annotations: {len(story_data.get('annotations', []))} found")
            print(f"  Story Elements: {len(story_data.get('story_elements', []))} found")
            
            # Generate creative slide with extracted data
            generator = ModernGraphicsGenerator(
                story_data.get('title', 'Weather Story'),
                attribution=Attribution(copyright="© Prompt Example 2025")
            )
            
            # Normalize visualization type
            viz_type = story_data.get('visualization_type', 'line').lower()
            
            html = generator.generate_creative_story_slide(
                title=story_data.get('title', 'Weather Story'),
                headline=story_data.get('headline', story_data.get('hero_headline', 'Story Insight')),
                subheadline=story_data.get('subheadline', story_data.get('hero_subheadline')),
                story_elements=story_data.get('story_elements'),
                visualization_type=viz_type,
                data_points=story_data.get('data_points'),
                annotations=story_data.get('annotations'),
                insight=story_data.get('insight'),
                time_range=story_data.get('time_range', story_data.get('time_period')),
                data_source=story_data.get('data_source')
            )
            
            output_path = Path(__file__).parent / "output" / "weather_story_creative.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            generator.export_to_png(html, output_path, viewport_width=1200, viewport_height=800)
            print(f"\n✓ Saved creative slide: {output_path}")
        
        # Method 2: Direct generation
        print("\n" + "=" * 70)
        print("Method 2: Direct prompt-to-slide generation")
        print("-" * 70)
        
        generator2 = ModernGraphicsGenerator(
            "Weather Data Story",
            attribution=Attribution(copyright="© Prompt Example 2025")
        )
        
        html2 = create_story_slide_from_prompt(generator2, weather_prompt)
        
        output_path2 = Path(__file__).parent / "output" / "weather_story_direct.png"
        generator2.export_to_png(html2, output_path2, viewport_width=1200, viewport_height=800)
        print(f"✓ Saved: {output_path2}")
        
        print("\n" + "=" * 70)
        print("✓ Prompt-to-story examples complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
