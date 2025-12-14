"""Environment configuration utilities"""

import os
from typing import Optional


def get_openai_key() -> Optional[str]:
    """Get OpenAI API key from environment variable
    
    Returns:
        API key string if found, None otherwise
    """
    return os.getenv("OPENAI_API_KEY")


def get_braintrust_key() -> Optional[str]:
    """Get Braintrust API key from environment variable
    
    Returns:
        API key string if found, None otherwise
    """
    return os.getenv("BRAINTRUST_API_KEY")


def load_env_file(env_path: str = ".env") -> bool:
    """Load environment variables from .env file
    
    Args:
        env_path: Path to .env file (default: .env)
        
    Returns:
        True if file was loaded, False otherwise
    """
    try:
        from dotenv import load_dotenv
        return load_dotenv(env_path)
    except ImportError:
        # python-dotenv not installed, try manual loading
        try:
            env_file = os.path.join(os.getcwd(), env_path)
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                return True
        except Exception:
            pass
        return False


# Auto-load .env file if it exists
load_env_file()
