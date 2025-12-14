"""Generate diagrams from natural language prompts using AI"""

import json
from typing import Optional, Dict, List
from .env_config import get_openai_key


# Default prompts for each diagram type
DEFAULT_DIAGRAM_PROMPTS = {
    'cycle': """Show a software development cycle with 4 steps: Plan (blue), Build (green), Test (orange), and Deploy (purple). 
    This represents a continuous process where each step leads to the next in a cycle.""",
    
    'comparison': """Compare Manual Design Approach vs Automated Generation Approach. 
    Manual Approach has: Time-intensive work, Pixel-perfect control, Hard to update, One-time use.
    Automated Approach has: Fast generation, Data-driven updates, Easy to modify, Reusable templates.
    Show the contrast between traditional manual design and modern automated graphics generation.""",
    
    'timeline': """Show a product launch timeline from Q1 2024 to Q4 2024 with 4 key milestones:
    Q1 2024: Launch - Initial release (blue)
    Q2 2024: Growth - User acquisition (green)
    Q3 2024: Scale - Expansion phase (orange)
    Q4 2024: Mature - Market leader (purple)
    Display horizontally with clear date markers.""",
    
    'story_slide': """Show how revenue model transformed from one-time payments to recurring subscriptions.
    The transformation happened from Q2 to Q4 2024, with revenue shifting from 30% recurring to 85% recurring.
    This represents a fundamental shift in business model that creates predictable revenue and better customer relationships.
    The insight is that recurring revenue creates sustainable growth and stronger partnerships.""",
    
    'grid': """Show a 5-step product development process:
    1. User Research
    2. Design & Prototype
    3. Development
    4. Testing & QA
    5. Launch & Monitor
    Display in a grid layout with numbered steps.""",
    
    'flywheel': """Show a growth loop flywheel with 4 elements: Acquire (blue), Activate (green), Retain (orange), and Refer (purple).
    The center label should be "Growth Loop".
    This represents a self-reinforcing cycle where each element feeds into the next.""",
    
    'slide_cards': """Show 3 cards representing the evolution of data visualization:
    Card 1: Data Cards (2010s) - Simple rectangles with numbers (blue)
    Card 2: Infographics (2020s) - Rich visualizations with charts (green)
    Card 3: Story Slides (2024+) - Dynamic, AI-generated presentations (purple)
    Show the progression of visualization styles over time.""",
    
    'slide_card_comparison': """Compare two approaches to creating graphics:
    Left card: Looks Great (Manual) - Pixel perfect design (blue)
    Right card: Updates Instantly (Automated) - Data-driven generation (green)
    Show the trade-off between manual perfection and automated efficiency.""",
}


def _get_openai_client():
    """Get OpenAI client with API key"""
    api_key = get_openai_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    try:
        import openai
    except ImportError:
        raise ImportError("openai package required. Install with: pip install openai")
    
    return openai.OpenAI(api_key=api_key)


def extract_cycle_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract cycle diagram data from a prompt
    
    Args:
        prompt: Natural language description of the cycle
        model: OpenAI model to use
        
    Returns:
        Dictionary with cycle diagram parameters:
        {
            'steps': [{'text': str, 'color': str}],
            'arrow_text': str,
            'cycle_end_text': Optional[str]
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for cycle diagrams.

A cycle diagram shows a circular process where steps flow from one to the next, eventually looping back.

Extract:
1. Steps: List of step objects, each with 'text' (the step name) and 'color' (blue, green, orange, purple, gray, etc.)
2. Arrow text: Text to show between steps (default: "→")
3. Optional cycle_end_text: Text to show after the cycle completes (if mentioned)

Return JSON with this structure:
{
    "steps": [{"text": "Step name", "color": "blue"}],
    "arrow_text": "→",
    "cycle_end_text": null
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract cycle diagram data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=500
    )
    
    return json.loads(response.choices[0].message.content)


def extract_comparison_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract comparison diagram data from a prompt
    
    Args:
        prompt: Natural language description of the comparison
        model: OpenAI model to use
        
    Returns:
        Dictionary with comparison diagram parameters:
        {
            'left_column': {'title': str, 'steps': List[str], 'outcome': Optional[str]},
            'right_column': {'title': str, 'steps': List[str], 'outcome': Optional[str]},
            'vs_text': str
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for comparison diagrams.

A comparison diagram shows two columns side-by-side, comparing different approaches, options, or states.

Extract:
1. Left column: title, list of steps/features, optional outcome
2. Right column: title, list of steps/features, optional outcome
3. vs_text: Text to show between columns (default: "vs")

Return JSON with this structure:
{
    "left_column": {"title": "Left Title", "steps": ["Step 1", "Step 2"], "outcome": null},
    "right_column": {"title": "Right Title", "steps": ["Step 1", "Step 2"], "outcome": null},
    "vs_text": "vs"
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract comparison diagram data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=800
    )
    
    return json.loads(response.choices[0].message.content)


def extract_timeline_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract timeline diagram data from a prompt
    
    Args:
        prompt: Natural language description of the timeline
        model: OpenAI model to use
        
    Returns:
        Dictionary with timeline diagram parameters:
        {
            'events': [{'date': str, 'text': str, 'color': str}],
            'orientation': str
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for timeline diagrams.

A timeline diagram shows events arranged chronologically with dates and descriptions.

Extract:
1. Events: List of event objects, each with 'date' (date string), 'text' (event description), and 'color' (blue, green, orange, purple, etc.)
2. Orientation: "horizontal" or "vertical" (default: "horizontal")

Return JSON with this structure:
{
    "events": [{"date": "2024 Q1", "text": "Event description", "color": "blue"}],
    "orientation": "horizontal"
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract timeline diagram data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=800
    )
    
    return json.loads(response.choices[0].message.content)


def extract_grid_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract grid diagram data from a prompt
    
    Args:
        prompt: Natural language description of the grid
        model: OpenAI model to use
        
    Returns:
        Dictionary with grid diagram parameters:
        {
            'items': [{'number': str, 'text': str}],
            'columns': int
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for grid diagrams.

A grid diagram shows numbered items arranged in a grid layout.

Extract:
1. Items: List of item objects, each with 'number' (string like "1", "2", etc.) and 'text' (item description)
2. Columns: Number of columns for the grid (default: 5, or infer from number of items)

Return JSON with this structure:
{
    "items": [{"number": "1", "text": "Item description"}],
    "columns": 5
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract grid diagram data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=600
    )
    
    return json.loads(response.choices[0].message.content)


def extract_flywheel_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract flywheel diagram data from a prompt
    
    Args:
        prompt: Natural language description of the flywheel
        model: OpenAI model to use
        
    Returns:
        Dictionary with flywheel diagram parameters:
        {
            'elements': [{'text': str, 'color': str}],
            'center_label': Optional[str]
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for flywheel diagrams.

A flywheel diagram shows elements arranged in a circle, representing a self-reinforcing cycle.

Extract:
1. Elements: List of element objects, each with 'text' (element name) and 'color' (blue, green, orange, purple, etc.)
2. Center label: Optional text to show in the center of the flywheel

Return JSON with this structure:
{
    "elements": [{"text": "Element name", "color": "blue"}],
    "center_label": "Center Label"
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract flywheel diagram data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=500
    )
    
    return json.loads(response.choices[0].message.content)


def extract_slide_cards_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract slide cards diagram data from a prompt
    
    Args:
        prompt: Natural language description of the slide cards
        model: OpenAI model to use
        
    Returns:
        Dictionary with slide cards diagram parameters:
        {
            'cards': [{'title': str, 'tagline': str, 'subtext': str, 'color': str}]
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for slide card diagrams.

A slide card diagram shows multiple cards arranged horizontally, representing evolution or progression.

Extract:
1. Cards: List of card objects, each with:
   - 'title': Main card title
   - 'tagline': Secondary text (e.g., year, category)
   - 'subtext': Description text
   - 'color': Color theme (blue, green, purple, gray, etc.)

Return JSON with this structure:
{
    "cards": [{"title": "Card Title", "tagline": "Tagline", "subtext": "Description", "color": "blue"}]
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract slide cards diagram data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=800
    )
    
    return json.loads(response.choices[0].message.content)


def extract_slide_card_comparison_data_from_prompt(prompt: str, model: str = "gpt-4-turbo-preview") -> Dict:
    """Extract slide card comparison diagram data from a prompt
    
    Args:
        prompt: Natural language description of the comparison
        model: OpenAI model to use
        
    Returns:
        Dictionary with slide card comparison parameters:
        {
            'left_card': {'title': str, 'tagline': str, 'subtext': str, 'color': str},
            'right_card': {'title': str, 'tagline': str, 'subtext': str, 'color': str}
        }
    """
    client = _get_openai_client()
    
    system_prompt = """You are a diagram designer that extracts structured data from natural language prompts for slide card comparison diagrams.

A slide card comparison shows two cards side-by-side, comparing different approaches or options.

Extract:
1. Left card: title, tagline, subtext, color
2. Right card: title, tagline, subtext, color

Return JSON with this structure:
{
    "left_card": {"title": "Left Title", "tagline": "Tagline", "subtext": "Description", "color": "blue"},
    "right_card": {"title": "Right Title", "tagline": "Tagline", "subtext": "Description", "color": "green"}
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract slide card comparison data from this prompt:\n\n{prompt}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=600
    )
    
    return json.loads(response.choices[0].message.content)


# Wrapper functions that combine extraction + generation with default prompt support

def generate_cycle_diagram_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate a cycle diagram from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['cycle']
    data = extract_cycle_data_from_prompt(prompt, model)
    return generator.generate_cycle_diagram(**data)


def generate_comparison_diagram_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate a comparison diagram from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['comparison']
    data = extract_comparison_data_from_prompt(prompt, model)
    return generator.generate_comparison_diagram(**data)


def generate_timeline_diagram_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate a timeline diagram from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['timeline']
    data = extract_timeline_data_from_prompt(prompt, model)
    return generator.generate_timeline_diagram(**data)


def generate_grid_diagram_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate a grid diagram from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['grid']
    data = extract_grid_data_from_prompt(prompt, model)
    return generator.generate_grid_diagram(**data)


def generate_flywheel_diagram_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate a flywheel diagram from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['flywheel']
    data = extract_flywheel_data_from_prompt(prompt, model)
    return generator.generate_flywheel_diagram(**data)


def generate_slide_cards_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate slide cards diagram from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['slide_cards']
    data = extract_slide_cards_data_from_prompt(prompt, model)
    return generator.generate_slide_card_diagram(**data)


def generate_slide_card_comparison_from_prompt(
    generator,
    prompt: Optional[str] = None,
    model: str = "gpt-4-turbo-preview"
) -> str:
    """Generate slide card comparison from a prompt (uses default if prompt is None)"""
    if prompt is None:
        prompt = DEFAULT_DIAGRAM_PROMPTS['slide_card_comparison']
    data = extract_slide_card_comparison_data_from_prompt(prompt, model)
    return generator.generate_slide_card_comparison(**data)
