"""Evaluation utilities for tracking AI-assisted template creation"""

from typing import Optional, Dict, Any
from .env_config import get_braintrust_key
from .config import braintrust_enabled


def log_template_creation_eval(
    description: str,
    template_name: str,
    success: bool,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Log template creation evaluation to Braintrust
    
    Args:
        description: User's description/prompt
        template_name: Name of created template
        success: Whether template creation succeeded
        metadata: Additional metadata (colors, fonts, etc.)
        
    Returns:
        True if logged successfully, False otherwise
    """
    # Check if Braintrust logging is enabled
    if not braintrust_enabled():
        return False
    
    api_key = get_braintrust_key()
    if not api_key:
        return False
    
    try:
        import braintrust
    except ImportError:
        return False
    
    try:
        # Braintrust auto-creates projects and experiments on first use
        # If project doesn't exist, it will be created automatically
        with braintrust.init(
            project="modern-graphics",
            experiment="template-creation",
            api_key=api_key,
            # Set to True to create project/experiment if they don't exist
            # (this is usually the default behavior)
        ) as experiment:
            result = experiment.log(
                input={"description": description},
                output={"template_name": template_name, "success": success},
                metadata=metadata or {},
                scores={"success": 1.0 if success else 0.0}
            )
            # Log ID returned means it was successful
            if result:
                print(f"📊 Logged to Braintrust: {result}")
            return True
    except Exception as e:
        # Log error but don't break template creation
        print(f"⚠️  Braintrust logging failed: {e}")
        return False


def log_interview_eval(
    conversation_turns: int,
    template_name: str,
    success: bool,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """Log interactive interview evaluation to Braintrust
    
    Args:
        conversation_turns: Number of conversation turns
        template_name: Name of created template
        success: Whether template creation succeeded
        metadata: Additional metadata
        
    Returns:
        True if logged successfully, False otherwise
    """
    # Check if Braintrust logging is enabled
    if not braintrust_enabled():
        return False
    
    api_key = get_braintrust_key()
    if not api_key:
        return False
    
    try:
        import braintrust
    except ImportError:
        return False
    
    try:
        with braintrust.init(
            project="modern-graphics",
            experiment="template-interview",
            api_key=api_key
        ) as experiment:
            result = experiment.log(
                input={"conversation_turns": conversation_turns},
                output={"template_name": template_name, "success": success},
                metadata=metadata or {},
                scores={"success": 1.0 if success else 0.0, "efficiency": 1.0 / max(conversation_turns, 1)}
            )
            if result:
                print(f"📊 Logged interview to Braintrust: {result}")
            return True
    except Exception as e:
        print(f"⚠️  Braintrust logging failed: {e}")
        return False
