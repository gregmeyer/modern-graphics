#!/usr/bin/env python3
"""Generate article draft from plan using OpenAI

This script reads the article plan and generates a complete draft article
following the "Big Idea" style using OpenAI GPT-4-turbo-preview.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics.env_config import get_openai_key


def read_plan_file(plan_path: Path) -> str:
    """Read the plan markdown file"""
    if not plan_path.exists():
        raise FileNotFoundError(f"Plan file not found: {plan_path}")
    
    with open(plan_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_openai_client():
    """Get OpenAI client with API key"""
    api_key = get_openai_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Set it in .env file or environment variable.")
    
    try:
        import openai
    except ImportError:
        raise ImportError("openai package required. Install with: pip install openai")
    
    return openai.OpenAI(api_key=api_key)


def generate_article_draft(plan_content: str, model: str = "gpt-4-turbo-preview") -> str:
    """Generate article draft from plan using OpenAI
    
    Args:
        plan_content: Content of the article plan markdown file
        model: OpenAI model to use
        
    Returns:
        Generated article draft as markdown string
    """
    client = get_openai_client()
    
    system_prompt = """You are an expert article writer specializing in the "Big Idea" style of technical writing.

The "Big Idea" style is characterized by:
- Clear, accessible language that avoids unnecessary jargon
- Practical, actionable content focused on outcomes
- Engaging narrative flow that tells a story
- Real examples and concrete use cases
- Progressive disclosure (start simple, add complexity)
- Conversational tone that feels like talking to a colleague

Your task is to convert an article plan into a complete draft article. The plan provides:
- Article structure and sections
- Key points and bullet items
- Code examples (include them exactly as specified)
- Target word count and section breakdowns
- Tone and style guidelines

Write the article following these principles:
1. Expand bullet points into flowing prose
2. Include code examples exactly as specified in the plan
3. Add graphic placeholders where indicated (e.g., [GRAPHIC: description])
4. Maintain the target word count (~2000 words total)
5. Use the specified tone (accessible, friendly, practical)
6. Create smooth transitions between sections
7. Make it engaging and readable
8. Focus on "how to" and "why" rather than just "what"

Return the complete article in markdown format, ready for publication."""
    
    user_prompt = f"""Convert this article plan into a complete draft article following the "Big Idea" style.

Article Plan:
{plan_content}

Generate the complete article draft now. Include all sections, expand bullet points into prose, include code examples exactly as specified, and add graphic placeholders where appropriate."""
    
    print("Generating article draft using OpenAI...")
    print(f"Model: {model}")
    print()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    return response.choices[0].message.content


def save_draft(draft_content: str, output_path: Path):
    """Save the draft article to file"""
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(draft_content)
    
    print(f"✓ Draft saved to: {output_path}")


def main():
    """Main function"""
    # Paths
    project_root = Path(__file__).parent.parent
    plan_path = Path("/Users/grmeyer/playground/writing/raw/building-a-graphics-engine/source/md/build-presentation-graphics-plan.md")
    output_path = Path("/Users/grmeyer/playground/writing/raw/building-a-graphics-engine/source/md/build-presentation-graphics.md")
    
    print("=" * 70)
    print("Generate Article Draft from Plan")
    print("=" * 70)
    print()
    
    # Read plan
    print(f"Reading plan from: {plan_path}")
    plan_content = read_plan_file(plan_path)
    print(f"✓ Plan file read ({len(plan_content)} characters)")
    print()
    
    # Generate draft
    draft_content = generate_article_draft(plan_content)
    print(f"✓ Article draft generated ({len(draft_content)} characters)")
    print()
    
    # Save draft
    print(f"Saving draft to: {output_path}")
    save_draft(draft_content, output_path)
    print()
    
    print("=" * 70)
    print("✓ Article draft generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
