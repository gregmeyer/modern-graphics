"""Interactive template creation using OpenAI"""

import json
from typing import Optional, Dict
from .env_config import get_openai_key
from .templates import TemplateBuilder, register_template, StyleTemplate
from .prompts import (
    TEMPLATE_INTERVIEW_SYSTEM_PROMPT,
    TEMPLATE_INTERVIEW_USER_PROMPT,
    TEMPLATE_GENERATION_PROMPT,
    parse_template_response,
)
from .eval import log_template_creation_eval, log_interview_eval


def interview_for_template(
    model: str = "gpt-4",
    conversation_history: Optional[list] = None,
    initial_prompt: Optional[str] = None,
    log_eval: bool = True
) -> Optional[StyleTemplate]:
    """Interview user to create a template using OpenAI
    
    Args:
        model: OpenAI model to use (default: "gpt-4")
        conversation_history: Optional existing conversation history
        initial_prompt: Optional initial prompt/description to start the conversation
                       (e.g., "I need a dark professional theme for corporate presentations")
        log_eval: Whether to log evaluation to Braintrust (default: True)
        
    Returns:
        StyleTemplate if successful, None otherwise
        
    Raises:
        ImportError: If openai package not installed
        ValueError: If API key not found
    """
    api_key = get_openai_key()
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Set it in .env file or environment variable."
        )
    
    try:
        import openai
    except ImportError:
        raise ImportError(
            "openai package required. Install with: pip install openai"
        )
    
    client = openai.OpenAI(api_key=api_key)
    
    # Initialize conversation
    messages = [
        {"role": "system", "content": TEMPLATE_INTERVIEW_SYSTEM_PROMPT},
        {"role": "user", "content": TEMPLATE_INTERVIEW_USER_PROMPT}
    ]
    
    # If initial prompt provided, add it to start the conversation
    if initial_prompt:
        messages.append({
            "role": "user",
            "content": f"Here's what I'm looking for: {initial_prompt}"
        })
    
    if conversation_history:
        messages.extend(conversation_history)
    
    print("=" * 60)
    print("Template Creation Interview")
    print("=" * 60)
    print("\nI'll ask you some questions to understand your design preferences.")
    print("Type 'done' when you're ready to generate the template, or 'quit' to exit.\n")
    
    conversation_turns = 0
    user_responses = []
    
    # Interview loop
    while True:
        # Get AI response
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        print(f"\n🤖 Assistant: {ai_message}\n")
        
        # Check if AI is ready to generate template
        if "json" in ai_message.lower() or "template" in ai_message.lower() and "{" in ai_message:
            # Try to parse template from response
            template_dict = parse_template_response(ai_message)
            if template_dict:
                return _build_template_from_dict(template_dict)
        
        # Get user input
        user_input = input("💬 You: ").strip()
        
        if user_input.lower() in ['done', 'finish', 'generate']:
            # Generate template
            messages.append({"role": "assistant", "content": ai_message})
            messages.append({
                "role": "user",
                "content": "I'm ready. Please generate the template specification now."
            })
            
            print("\n🔄 Generating template...")
            final_response = client.chat.completions.create(
                model=model,
                messages=messages + [{"role": "user", "content": TEMPLATE_GENERATION_PROMPT}],
                temperature=0.3  # Lower temperature for more consistent output
            )
            
            template_text = final_response.choices[0].message.content
            template_dict = parse_template_response(template_text)
            
            if template_dict:
                template = _build_template_from_dict(template_dict)
                print(f"\n✓ Template '{template.name}' created successfully!")
                
                # Log evaluation
                if log_eval:
                    log_interview_eval(
                        conversation_turns=conversation_turns,
                        template_name=template.name,
                        success=True,
                        metadata={
                            "model": model,
                            "colors": list(template.colors.keys()),
                            "font_family": template.font_family,
                            "user_responses_count": len(user_responses)
                        }
                    )
                
                return template
            else:
                print("\n⚠️  Could not parse template from response. Trying again...")
                continue
        
        if user_input.lower() in ['quit', 'exit', 'cancel']:
            print("\n👋 Interview cancelled.")
            
            # Log cancelled interview
            if log_eval:
                log_interview_eval(
                    conversation_turns=conversation_turns,
                    template_name="",
                    success=False,
                    metadata={"cancelled": True, "model": model}
                )
            
            return None
        
        # Track conversation
        conversation_turns += 1
        user_responses.append(user_input)
        
        # Add user response to conversation
        messages.append({"role": "assistant", "content": ai_message})
        messages.append({"role": "user", "content": user_input})


def _build_template_from_dict(template_dict: Dict) -> StyleTemplate:
    """Build StyleTemplate from dictionary"""
    builder = TemplateBuilder(template_dict.get("name", "custom_template"))
    
    # Add colors
    colors = template_dict.get("colors", {})
    for color_name, color_data in colors.items():
        if isinstance(color_data, dict):
            gradient = color_data.get("gradient", ["#F5F5F7", "#F5F5F7"])
            shadow = color_data.get("shadow", "rgba(0, 0, 0, 0.08)")
            builder.add_color(color_name, tuple(gradient), shadow)
    
    # Set other properties
    if "base_styles" in template_dict:
        builder.set_base_styles(template_dict["base_styles"])
    if "attribution_styles" in template_dict:
        builder.set_attribution_styles(template_dict["attribution_styles"])
    if "font_family" in template_dict:
        builder.set_font_family(template_dict["font_family"])
    if "background_color" in template_dict:
        builder.set_background_color(template_dict["background_color"])
    
    return builder.build()


def quick_template_from_description(
    description: str,
    model: str = "gpt-4",
    log_eval: bool = True
) -> Optional[StyleTemplate]:
    """Quickly generate a template from a text description
    
    Args:
        description: Text description of desired template (e.g., "dark professional theme with blue accents")
        model: OpenAI model to use
        log_eval: Whether to log evaluation to Braintrust (default: True)
        
    Returns:
        StyleTemplate if successful, None otherwise
    """
    api_key = get_openai_key()
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    try:
        import openai
    except ImportError:
        raise ImportError("openai package required. Install with: pip install openai")
    
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""Create a visual style template based on this description: "{description}"

{TEMPLATE_GENERATION_PROMPT}"""
    
    # Use gpt-4-turbo or gpt-3.5-turbo for JSON mode support
    json_model = "gpt-4-turbo-preview" if model.startswith("gpt-4") else "gpt-3.5-turbo"
    
    response = client.chat.completions.create(
        model=json_model,
        messages=[
            {"role": "system", "content": "You are a design expert that creates visual style templates. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    template_dict = json.loads(response.choices[0].message.content)
    template = _build_template_from_dict(template_dict)
    
    # Log evaluation
    if log_eval:
        log_template_creation_eval(
            description=description,
            template_name=template.name,
            success=True,
            metadata={
                "model": model,
                "colors": list(template.colors.keys()),
                "font_family": template.font_family,
                "background_color": template.background_color
            }
        )
    
    return template
