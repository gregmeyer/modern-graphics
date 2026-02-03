"""Interactive graphic ideas interview.

When the user says "I need some ideas", run this interview to collect
format, subject, theme, narrative, before/after, layout, and outputs;
then build and store a prompt version.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .prompts.graphic_prompt_template import (
    GRAPHIC_PROMPT_QUESTIONS,
    build_graphic_prompt,
)


def _default_save_dir() -> Path:
    """Default directory for stored prompt versions (cwd or env)."""
    env_dir = os.getenv("MODERN_GRAPHICS_PROMPTS_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    return Path.cwd() / "prompt_versions"


def run_graphic_ideas_interview(
    save_dir: Optional[Path] = None,
    prompt_name: Optional[str] = None,
    skip_save: bool = False,
) -> Dict[str, Any]:
    """Run the graphic ideas interview: ask questions, build prompt, optionally save.

    Args:
        save_dir: Where to save the prompt version (default: cwd/prompt_versions or MODERN_GRAPHICS_PROMPTS_DIR).
        prompt_name: Optional name for the file (e.g. "cy-graphic"); otherwise timestamp.
        skip_save: If True, only return the built prompt and do not write a file.

    Returns:
        Dict with keys: answers, prompt_text, saved_path (None if skip_save or not saved).
    """
    save_dir = save_dir or _default_save_dir()
    answers: Dict[str, str] = {}

    print("Graphic ideas — a few questions to build your prompt.\n")
    print("Answer each; leave optional ones blank if you like.\n")

    for q in GRAPHIC_PROMPT_QUESTIONS:
        key = q["key"]
        label = q["label"]
        help_text = q.get("help", "")
        optional = q.get("optional", False)
        prompt_suffix = " (optional)" if optional else ""
        line = input(f"  {label}{prompt_suffix}\n    [{help_text}]\n    > ").strip()
        answers[key] = line

    prompt_text = build_graphic_prompt(answers)
    saved_path: Optional[Path] = None

    if not skip_save and prompt_text:
        save_dir.mkdir(parents=True, exist_ok=True)
        if prompt_name:
            safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in prompt_name)
            filename = f"graphic_prompt_{safe_name}.md"
        else:
            filename = f"graphic_prompt_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.md"
        saved_path = save_dir / filename
        notes = (answers.get("notes") or "").strip()
        content = f"# Graphic prompt\n\n{prompt_text}\n"
        if notes:
            content += f"\n## Notes / changes\n\n{notes}\n"
        saved_path.write_text(content, encoding="utf-8")
        print(f"\nSaved prompt to: {saved_path}")

    print("\n--- Prompt (copy/paste) ---\n")
    print(prompt_text)
    print()

    return {
        "answers": answers,
        "prompt_text": prompt_text,
        "saved_path": saved_path,
    }
