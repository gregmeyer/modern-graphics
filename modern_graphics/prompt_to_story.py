"""Generate story slides from detailed prompts using AI"""

import json
from typing import Optional, Dict, List
from .env_config import get_openai_key
from .diagrams.intelligent_story_slide import generate_intelligent_story_slide


def generate_story_from_prompt(
    prompt: str,
    model: str = "gpt-4-turbo-preview"
) -> Optional[Dict]:
    """Generate story slide content from a detailed prompt
    
    Args:
        prompt: Detailed prompt describing the story/data visualization
        model: OpenAI model to use
        
    Returns:
        Dictionary with story slide parameters:
        {
            "title": str,
            "headline": str,
            "subheadline": Optional[str],
            "what_changed": str,
            "time_period": str,
            "what_it_means": str,
            "insight": Optional[str],
            "visualization_type": Optional[str],  # line, bar, area, comparison
            "data_points": Optional[List[Dict]],  # For charts
            "annotations": Optional[List[str]],
            "story_elements": Optional[List[Dict]],  # Key metrics
            "data_source": Optional[str],
            "time_range": Optional[str]
        }
    """
    api_key = get_openai_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    try:
        import openai
    except ImportError:
        raise ImportError("openai package required. Install with: pip install openai")
    
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """You are a story-driven visualization designer that extracts key narrative elements from detailed prompts.

Your job is to identify:
1. A compelling headline (the main insight)
2. What changed (the key change or trend)
3. Time period (when this change occurred)
4. What it means (the significance or implication)
5. Visualization type (line, bar, area, or comparison chart)
6. Key story elements/metrics to highlight
7. Annotations explaining the change
8. Optional: Hero headline and subheadline

Extract these elements from the user's prompt and return them as structured JSON. Be creative and extract all relevant details."""

    user_prompt = f"""Extract story elements from this detailed prompt:

{prompt}

Return a JSON object with these fields:
- title: A clear, descriptive title/category
- headline: A compelling, declarative headline (the main insight, 5-12 words)
- subheadline: Optional compelling subheadline (8-20 words)
- what_changed: What changed (the key change or trend)
- time_period: Over what time period (e.g., "last 7 days", "2020-2024", "Q1-Q4 2024")
- what_it_means: What it means (the significance or implication)
- insight: Optional key insight or takeaway
- visualization_type: Type of chart (line, bar, area, or comparison)
- data_points: Optional array of data points for visualization (e.g., [{{"x": "2020", "y": 20}}, {{"x": "2021", "y": 25}}])
- annotations: Optional array of 1-2 annotation strings explaining what changed and why it matters
- story_elements: Optional array of key metrics with label and value (e.g., [{{"label": "Temperature Increase", "value": "+3.5°C"}}])
- data_source: Optional data source attribution
- time_range: Optional time range for footer

If the prompt describes a specific visualization (line chart, bar chart, etc.), extract that. If it mentions specific data points or metrics, include them. Make reasonable assumptions based on context."""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1000
    )
    
    result = json.loads(response.choices[0].message.content)
    return result


def create_story_slide_from_prompt(
    generator,
    prompt: str,
    model: str = "gpt-4-turbo-preview",
    temperature: float = 0.5,
    use_intelligent: bool = True
) -> str:
    """Create a story slide from a detailed prompt
    
    Args:
        generator: ModernGraphicsGenerator instance
        prompt: Detailed prompt describing the story/data visualization
        model: OpenAI model to use
        temperature: Sampling temperature (0.0-2.0). Higher = more creative. Default: 0.5
        use_intelligent: If True, use AI to design the slide composition (default: True)
        
    Returns:
        HTML string for the story slide
    """
    # Use intelligent slide generator that designs the composition
    if use_intelligent:
        try:
            return generate_intelligent_story_slide(generator, prompt, model, temperature)
        except Exception as e:
            # Fallback to creative slide if intelligent fails
            print(f"Intelligent slide generation failed, falling back: {e}")
    
    # Fallback: Extract story data and use creative slide
    story_data = generate_story_from_prompt(prompt, model)
    
    if not story_data:
        raise ValueError("Failed to extract story elements from prompt")
    
    from .diagrams.creative_story_slide import generate_creative_story_slide
    
    return generate_creative_story_slide(
        generator=generator,
        title=story_data.get("title", "Data Story"),
        headline=story_data.get("headline", story_data.get("hero_headline", "Story Insight")),
        subheadline=story_data.get("subheadline", story_data.get("hero_subheadline")),
        story_elements=story_data.get("story_elements"),
        visualization_type=story_data.get("visualization_type", "line").lower(),
        data_points=story_data.get("data_points"),
        annotations=story_data.get("annotations"),
        insight=story_data.get("insight"),
        time_range=story_data.get("time_range", story_data.get("time_period")),
        data_source=story_data.get("data_source"),
        custom_prompt_context=prompt[:200]
    )
