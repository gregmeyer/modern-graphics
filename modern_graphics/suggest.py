"""Deterministic keyword-to-layout matcher for smart layout suggestion.

Zero external dependencies. Used by both the CLI suggest fallback and
the MCP server's suggest_layout tool.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class SuggestResult:
    """A layout recommendation with confidence and a ready-to-paste command."""

    layout: str
    confidence: float
    reason: str
    example_command: str


# Each entry: (layout_type, keywords, weight).
# Keywords are matched as substrings in the lowercased description.
_KEYWORD_RULES: List[Tuple[str, List[str], int]] = [
    ("comparison", ["compare", "vs", "versus", "before and after", "tradeoff", "trade-off", "pros cons", "side by side", "side-by-side"], 10),
    ("timeline", ["timeline", "chronolog", "milestones", "roadmap", "events over time"], 10),
    ("story", ["story", "narrative", "what changed", "transformation", "journey", "evolution"], 10),
    ("key-insight", ["quote", "insight", "key point", "pullquote", "pull quote", "takeaway", "one thing"], 10),
    ("funnel", ["funnel", "conversion", "pipeline", "drop-off", "dropoff", "stages of"], 10),
    ("hero", ["hero", "opener", "headline", "banner", "title slide", "cover slide", "opening slide"], 10),
    ("grid", ["list", "grid", "items", "options", "priorities", "top ", "checklist", "inventory"], 8),
    ("insight-card", ["insight card", "insight with image", "insight with svg", "card with visual"], 10),
    ("insight-story", ["insight story", "before after insight", "before/after insight"], 10),
    ("hero-triptych", ["triptych", "three column", "three-column", "triple"], 10),
]

# Tiebreaker priority — more commonly used layouts rank higher.
_PRIORITY: Dict[str, int] = {
    "hero": 100,
    "comparison": 90,
    "story": 80,
    "key-insight": 70,
    "timeline": 60,
    "funnel": 50,
    "grid": 40,
    "insight-card": 30,
    "insight-story": 20,
    "hero-triptych": 10,
}

# Example commands per layout (mirrors CREATE_EXAMPLES in cli.py).
EXAMPLE_COMMANDS: Dict[str, str] = {
    "hero": 'modern-graphics create --layout hero --headline "Execution scales" --output hero.html',
    "key-insight": 'modern-graphics create --layout key-insight --text "Key takeaway" --output insight.html',
    "insight-card": 'modern-graphics create --layout insight-card --text "Key takeaway" --output insight-card.html',
    "insight-story": 'modern-graphics create --layout insight-story --headline "When shipping gets easy" --insight-text "Use checklist gates" --output insight-story.html',
    "comparison": 'modern-graphics create --layout comparison --left "Before:Manual:Slow" --right "After:Agentic:Faster" --output comparison.html',
    "story": 'modern-graphics create --layout story --what-changed "Execution accelerated" --output story.html',
    "timeline": 'modern-graphics create --layout timeline --events "Q1|Baseline,Q2|Adoption" --output timeline.html',
    "funnel": 'modern-graphics create --layout funnel --stages "Visit,Trial,Paid" --values "100,40,12" --output funnel.html',
    "grid": 'modern-graphics create --layout grid --items "A,B,C" --columns 3 --output grid.html',
    "hero-triptych": 'modern-graphics create --layout hero-triptych --headline "Three pillars" --columns "A,B,C" --output triptych.html',
}

# Human-readable descriptions per layout.
LAYOUT_DESCRIPTIONS: Dict[str, str] = {
    "hero": "Bold opener with headline, subheadline, and optional highlights",
    "key-insight": "Standalone pull quote or key takeaway",
    "insight-card": "Insight text paired with an SVG visual panel",
    "insight-story": "Before/after narrative with insight callout",
    "comparison": "Side-by-side comparison of two approaches",
    "story": "Narrative block: what changed, over what period, why it matters",
    "timeline": "Chronological sequence of events or milestones",
    "funnel": "Conversion funnel with stages and values",
    "grid": "Numbered item grid with optional convergence goal",
    "hero-triptych": "Three-column hero with headline and panels",
}


def suggest_layout(description: str) -> SuggestResult:
    """Return the best layout match for a plain-text description."""
    results = suggest_layout_top_n(description, n=1)
    return results[0]


def suggest_layout_top_n(description: str, n: int = 3) -> List[SuggestResult]:
    """Return the top N layout matches ranked by score, then priority."""
    desc_lower = description.lower().strip()

    # Score each layout
    scores: Dict[str, Tuple[int, List[str]]] = {}
    for layout, keywords, weight in _KEYWORD_RULES:
        matched = [kw for kw in keywords if kw in desc_lower]
        if matched:
            current_score, current_matched = scores.get(layout, (0, []))
            scores[layout] = (current_score + weight * len(matched), current_matched + matched)

    if not scores:
        # No matches — return hero as safe default
        return [
            SuggestResult(
                layout="hero",
                confidence=0.1,
                reason="no keyword matches — defaulting to hero",
                example_command=EXAMPLE_COMMANDS["hero"],
            )
        ]

    # Sort by score descending, then by priority descending
    ranked = sorted(
        scores.items(),
        key=lambda item: (item[1][0], _PRIORITY.get(item[0], 0)),
        reverse=True,
    )

    # Normalize confidence: top score / max possible single-layout score
    max_score = ranked[0][1][0]
    max_possible = max(len(kws) * w for _, kws, w in _KEYWORD_RULES)

    results: List[SuggestResult] = []
    for layout, (score, matched) in ranked[:n]:
        confidence = min(score / max_possible, 1.0)
        results.append(
            SuggestResult(
                layout=layout,
                confidence=round(confidence, 2),
                reason=f"matched: {', '.join(matched)}",
                example_command=EXAMPLE_COMMANDS.get(layout, f"modern-graphics create --layout {layout} --output {layout}.html"),
            )
        )

    return results
