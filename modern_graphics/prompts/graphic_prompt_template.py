"""Generic template for prompting hero and insight-story graphics.

Use with the graphic ideas interview: when the user says "I need some ideas",
the system asks these questions and builds a stored prompt version.
"""

from typing import Any, Dict, List

# Questions for the graphic ideas interview (key, label, help text, optional).
GRAPHIC_PROMPT_QUESTIONS: List[Dict[str, Any]] = [
    {
        "key": "format",
        "label": "Format",
        "help": "Hero only, insight-story (before/after), or diagram-only",
        "optional": False,
    },
    {
        "key": "subject",
        "label": "Subject",
        "help": "Who or what the graphic is for (person, product, brand, concept)",
        "optional": False,
    },
    {
        "key": "theme",
        "label": "Theme / mood",
        "help": "Palette, tone; font if it matters (e.g. corporate minimal, playful SaaS)",
        "optional": False,
    },
    {
        "key": "narrative",
        "label": "Narrative",
        "help": "Headline, subtitle, key insight; quoteable or specific copy",
        "optional": False,
    },
    {
        "key": "before_panel",
        "label": "Before panel (if before/after)",
        "help": "What's on screen in the old world: states, labels, what's stuck",
        "optional": True,
    },
    {
        "key": "after_panel",
        "label": "After panel (if before/after)",
        "help": "What's on screen in the new world: steps, flow, outcome",
        "optional": True,
    },
    {
        "key": "layout_constraints",
        "label": "Layout constraints",
        "help": "Alignment, style (e.g. no post-its, use pills), placement of icons/illustrations",
        "optional": True,
    },
    {
        "key": "outputs",
        "label": "Outputs",
        "help": "Paths, HTML/PNG/SVG, script name if you want one",
        "optional": True,
    },
    {
        "key": "notes",
        "label": "Notes / changes",
        "help": "Optional: implementation notes, tweaks, or 'next time do X' (appended to saved file)",
        "optional": True,
    },
]

PROMPT_CHECKLIST_ITEMS: List[str] = [
    "Format — Hero only, insight-story (before/after), or diagram-only",
    "Subject — Who or what the graphic is for",
    "Theme / mood — Palette, tone, font if it matters",
    "Narrative — Headline, subtitle, key insight (quoteable or specific copy)",
    "Before panel (if applicable) — What's on screen; states, labels, stuck or problem",
    "After panel (if applicable) — What's on screen; steps, flow, outcome",
    "Layout constraints — Alignment, style, placement of icons/illustrations",
    "Outputs — Paths, HTML/PNG/SVG, script name if you want one",
]

# Example answers: peanut butter and jelly sandwich-making process (for doc/sample output).
EXAMPLE_ANSWERS_PBJ: Dict[str, str] = {
    "format": "insight-story",
    "subject": "peanut butter and jelly sandwich-making process",
    "theme": "warm, kitchen-friendly; browns, reds, cream",
    "narrative": "From chaos to lunch: three steps, one sandwich. Key insight: The best PB&J is the one you actually make.",
    "before_panel": "kitchen chaos: bread everywhere, jars scattered, knife in the wrong place",
    "after_panel": "Spread peanut butter → Add jelly → Close and slice. Done",
    "layout_constraints": "horizontal flow, same baseline for arrows; no post-its; small sandwich icon on the right",
    "outputs": "docs/lunch-graphics/, HTML + PNG, generate_pbj_hero.py",
}


def build_graphic_prompt(answers: Dict[str, str]) -> str:
    """Turn collected answers into a single prompt paragraph for a human or model.

    Skips empty/optional answers. Result is suitable for pasting into a chat
    or saving as a prompt version.
    """
    parts: List[str] = []

    format_ = (answers.get("format") or "").strip()
    subject = (answers.get("subject") or "").strip()
    theme = (answers.get("theme") or "").strip()
    narrative = (answers.get("narrative") or "").strip()

    if format_:
        parts.append(f"Make a {format_} graphic")
    if subject:
        parts.append(f"for {subject}")
    if theme:
        parts.append(f"with theme/mood: {theme}.")
    if narrative:
        parts.append(f"Narrative: {narrative}")

    before = (answers.get("before_panel") or "").strip()
    after = (answers.get("after_panel") or "").strip()
    if before or after:
        if before:
            parts.append(f"Before panel: {before}.")
        if after:
            parts.append(f"After panel: {after}.")

    layout = (answers.get("layout_constraints") or "").strip()
    if layout:
        parts.append(f"Layout: {layout}.")

    out = (answers.get("outputs") or "").strip()
    if out:
        parts.append(f"Outputs: {out}.")

    return " ".join(parts).strip()


# Example built prompt (PB&J sandwich-making process) for docs and sample output.
EXAMPLE_PROMPT_PBJ: str = build_graphic_prompt(EXAMPLE_ANSWERS_PBJ)
