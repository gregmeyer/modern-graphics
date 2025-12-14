"""Prompt storage utilities for evaluation

Stores prompts used to generate graphics so they can be sent to eval along with images.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class PromptStorage:
    """Store prompts and metadata for evaluation"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.prompts_file = output_dir / "prompts_used.json"
        self.prompts: List[Dict] = []
    
    def add_prompt(
        self,
        prompt: str,
        output_file: Path,
        use_case: str,
        slide_type: str = "story_slide",
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        metadata: Optional[Dict] = None
    ):
        """Add a prompt to storage
        
        Args:
            prompt: The prompt text used
            output_file: Path to the generated image file
            use_case: Use case name (e.g., "tech_startup", "corporate")
            slide_type: Type of slide generated (e.g., "story_slide", "combo_chart")
            model: Model used for generation (e.g., "gpt-4-turbo-preview")
            temperature: Temperature setting used (0.0-2.0)
            metadata: Optional additional metadata
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "output_file": str(output_file.relative_to(self.output_dir.parent.parent.parent)),
            "use_case": use_case,
            "slide_type": slide_type,
            "model": model,
            "temperature": temperature,
            "metadata": metadata or {}
        }
        self.prompts.append(entry)
    
    def save(self):
        """Save prompts to JSON file"""
        self.prompts_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.prompts_file, 'w') as f:
            json.dump({
                "total_prompts": len(self.prompts),
                "generated_at": datetime.now().isoformat(),
                "prompts": self.prompts
            }, f, indent=2)
    
    def get_prompts(self) -> List[Dict]:
        """Get all stored prompts"""
        return self.prompts


def load_prompts(prompts_file: Path) -> List[Dict]:
    """Load prompts from JSON file"""
    if prompts_file.exists():
        with open(prompts_file, 'r') as f:
            data = json.load(f)
            return data.get("prompts", [])
    return []
