"""Configuration settings for Modern Graphics"""

import os
from typing import Optional


class Config:
    """Configuration settings"""
    
    def __init__(self):
        self._braintrust_enabled: Optional[bool] = None
        self._load_from_env()
    
    def _load_from_env(self):
        """Load settings from environment variables"""
        # BRAINTRUST_ENABLED can be "true", "false", "1", "0", etc.
        braintrust_env = os.getenv("BRAINTRUST_ENABLED", "").lower()
        if braintrust_env in ("true", "1", "yes", "on"):
            self._braintrust_enabled = True
        elif braintrust_env in ("false", "0", "no", "off"):
            self._braintrust_enabled = False
        # If not set, defaults to None (auto-detect based on key presence)
    
    @property
    def braintrust_enabled(self) -> bool:
        """Whether Braintrust logging is enabled
        
        Returns True if:
        - BRAINTRUST_ENABLED env var is "true"/"1"/"yes"
        - Or if BRAINTRUST_API_KEY exists (auto-enable)
        
        Returns False if:
        - BRAINTRUST_ENABLED env var is "false"/"0"/"no"
        - Or if BRAINTRUST_API_KEY doesn't exist
        """
        if self._braintrust_enabled is not None:
            return self._braintrust_enabled
        
        # Auto-detect: enable if API key exists
        from .env_config import get_braintrust_key
        return get_braintrust_key() is not None
    
    def set_braintrust_enabled(self, enabled: bool):
        """Manually set Braintrust logging enabled/disabled"""
        self._braintrust_enabled = enabled


# Global config instance
_config = Config()


def get_config() -> Config:
    """Get global configuration instance"""
    return _config


def braintrust_enabled() -> bool:
    """Check if Braintrust logging is enabled"""
    return _config.braintrust_enabled


def set_braintrust_enabled(enabled: bool):
    """Enable or disable Braintrust logging"""
    _config.set_braintrust_enabled(enabled)
