#!/usr/bin/env python3
"""Generate tracked showcase assets for underrepresented CLI layout features.

Note: `before-after` is currently excluded because the command is wired to a
stub implementation that raises NotImplementedError.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "output" / "showcase" / "cli-layouts"


def _run(args: list[str]) -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    cmd = [sys.executable, "-m", "modern_graphics.cli", *args]
    result = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stdout}\n{result.stderr}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    slide_cards_png = OUT / "01-slide-cards.png"
    slide_compare_png = OUT / "02-slide-compare.png"
    premium_card_png = OUT / "03-premium-card.png"
    wireframe_scene_svg = OUT / "04-wireframe-scene.svg"
    wireframe_insight_png = OUT / "05-wireframe-insight-card.png"
    wireframe_story_png = OUT / "06-wireframe-insight-story.png"

    _run([
        "slide-cards",
        "--title",
        "Execution Shift",
        "--cards",
        '[{"title":"Prompting","tagline":"Step 1","subtext":"Generate options"},{"title":"Constrainting","tagline":"Step 2","subtext":"Set boundaries"},{"title":"Decision gates","tagline":"Step 3","subtext":"Filter what ships"}]',
        "--png",
        "--output",
        str(slide_cards_png),
    ])

    _run([
        "slide-compare",
        "--title",
        "Operating Modes",
        "--left",
        '{"title":"Motion","tagline":"Ship more","subtext":"High output, noisy relevance"}',
        "--right",
        '{"title":"Judgment","tagline":"Ship fewer","subtext":"Lower volume, higher signal"}',
        "--png",
        "--output",
        str(slide_compare_png),
    ])

    _run([
        "premium-card",
        "--title",
        "Ops Guardrail Premium Card",
        "--config",
        "examples/ops_guardrail_premium_card.json",
        "--png",
        "--output",
        str(premium_card_png),
    ])

    _run([
        "wireframe-scene",
        "--preset",
        "after",
        "--output",
        str(wireframe_scene_svg),
    ])

    _run([
        "create",
        "--layout",
        "insight-card",
        "--text",
        "Inline guidance reduced ticket escalations.",
        "--svg-file",
        str(wireframe_scene_svg),
        "--png",
        "--output",
        str(wireframe_insight_png),
    ])

    _run([
        "insight-story",
        "--title",
        "Support System Shift",
        "--headline",
        "From queue management to in-flow resolution",
        "--insight-text",
        "Embedding help in context cut wait time and increased completion.",
        "--generate-wireframes",
        "--png",
        "--output",
        str(wireframe_story_png),
    ])

    print(f"Generated CLI layout showcase assets in: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
