#!/usr/bin/env python3
"""Test intelligent story slide generation"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution, generate_intelligent_story_slide

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
"""

generator = ModernGraphicsGenerator(
    "Weather Data Story",
    attribution=Attribution(copyright="© Intelligent Slide Example 2025")
)

print("=" * 70)
print("Generating Intelligent Story Slide")
print("=" * 70)
print("\nUsing AI to design slide composition...")
print("(Combining visual primitives: charts, metrics, timelines, comparisons)\n")

html = generate_intelligent_story_slide(generator, weather_prompt)
output_path = Path(__file__).parent / "output" / "intelligent_weather_full.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
generator.export_to_png(html, output_path, viewport_width=1800, viewport_height=1200)
print(f"✓ Generated: {output_path}")
print("\nOpen it to see the AI-designed slide composition!")
