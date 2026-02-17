"""Phase 3 create CLI smoke checks (success + actionable failure hints)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _run(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["MODERN_GRAPHICS_ENABLE_CREATE"] = "1"
    env["PYTHONPATH"] = str(root)
    return subprocess.run(
        [sys.executable, "-m", "modern_graphics.cli", *args],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
    )


def test_create_cli_success_and_error_hints(tmp_path):
    root = Path(__file__).resolve().parents[2]

    ok = _run(
        root,
        [
            "create",
            "--layout",
            "hero",
            "--headline",
            "Execution scales",
            "--output",
            str(tmp_path / "hero.html"),
        ],
    )
    assert ok.returncode == 0
    assert "Generated create/hero" in ok.stdout

    fail = _run(
        root,
        [
            "create",
            "--layout",
            "comparison",
            "--left",
            "Before:Manual:Slow",
            "--output",
            str(tmp_path / "comparison.html"),
        ],
    )
    assert fail.returncode != 0
    assert "--left and --right are required" in fail.stdout
    assert "Hint: try `" in fail.stdout

