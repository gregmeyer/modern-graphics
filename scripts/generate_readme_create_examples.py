#!/usr/bin/env python3
"""Generate README preview graphics using the create-first CLI workflow."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "output" / "showcase" / "create-first"


def _run(args: list[str]) -> None:
    env = dict(os.environ)
    env["MODERN_GRAPHICS_ENABLE_CREATE"] = "1"
    env["PYTHONPATH"] = str(ROOT)
    cmd = [sys.executable, "-m", "modern_graphics.cli", *args]
    result = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(args)}\n{result.stdout}\n{result.stderr}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    runs: list[list[str]] = [
        [
            "create",
            "--layout",
            "hero",
            "--headline",
            "Execution scales. Judgment does not.",
            "--subheadline",
            "Use explicit decision gates when output gets cheaper.",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "hero.png"),
        ],
        [
            "create",
            "--layout",
            "key-insight",
            "--text",
            "Execution can scale. Judgment is still human-limited.",
            "--variant",
            "default",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "key-insight-default.png"),
        ],
        [
            "create",
            "--layout",
            "key-insight",
            "--text",
            "Execution can scale. Judgment is still human-limited.",
            "--variant",
            "bold",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "key-insight-bold.png"),
        ],
        [
            "create",
            "--layout",
            "key-insight",
            "--text",
            "Execution can scale. Judgment is still human-limited.",
            "--variant",
            "quote",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "key-insight-quote.png"),
        ],
        [
            "create",
            "--layout",
            "insight-card",
            "--text",
            "One-page artifacts force explicit decisions.",
            "--svg-label",
            "Decision gate",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "insight-card.png"),
        ],
        [
            "create",
            "--layout",
            "insight-story",
            "--headline",
            "When shipping gets easy, choosing gets hard.",
            "--insight-text",
            "PM leverage shifts from pushing work to filtering consequence.",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "insight-story.png"),
        ],
        [
            "create",
            "--layout",
            "comparison",
            "--left",
            "Execution-first:Ship more:Motion without relevance",
            "--right",
            "Judgment-first:Ship fewer:Higher decision quality",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "comparison.png"),
        ],
        [
            "create",
            "--layout",
            "timeline",
            "--events",
            "Now|Prompting,Next|Constrainting,Later|Decision gates",
            "--orientation",
            "horizontal",
            "--theme",
            "corporate",
            "--png",
            "--output",
            str(OUT / "timeline.png"),
        ],
    ]

    for args in runs:
        _run(args)

    print(f"Generated {len(runs)} README create-first graphics in: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
