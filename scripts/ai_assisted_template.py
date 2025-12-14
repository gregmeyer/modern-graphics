"""Example: Using OpenAI to generate a template (requires OPENAI_API_KEY in .env)"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator, Attribution, get_openai_key, TemplateBuilder, register_template

# Check if OpenAI key is available
api_key = get_openai_key()
if not api_key:
    print("⚠️  OPENAI_API_KEY not found in environment variables")
    print("   Create a .env file with: OPENAI_API_KEY=your_key_here")
    print("   Or set it as an environment variable")
    exit(1)

try:
    import openai
    
    # Use OpenAI to generate a template description
    client = openai.OpenAI(api_key=api_key)
    
    # Example: Generate a template based on a description
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a design expert. Generate color palettes and CSS styles."},
            {"role": "user", "content": "Create a modern, professional color palette with 5 colors suitable for business presentations. Return as JSON with color names and hex codes."}
        ],
        response_format={"type": "json_object"}
    )
    
    # Parse response and create template
    # (This is a simplified example - you'd parse the JSON response)
    print("✓ OpenAI integration ready")
    print("   You can now use OpenAI to generate templates and diagram content")
    
except ImportError:
    print("⚠️  openai package not installed")
    print("   Install with: pip install openai")
except Exception as e:
    print(f"⚠️  Error: {e}")

# Example: Manual template creation (fallback)
template = (TemplateBuilder("ai_generated")
    .add_color("blue", ("#007AFF", "#0051D5"), "rgba(0, 122, 255, 0.12)")
    .add_color("green", ("#34C759", "#28A745"), "rgba(52, 199, 89, 0.12)")
    .build())

register_template(template)

generator = ModernGraphicsGenerator("AI-Assisted Template", template=template)
print("✓ Template created successfully")
