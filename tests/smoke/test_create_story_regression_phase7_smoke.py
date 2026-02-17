"""Regression smoke test for create/story generation path.

Guards against the positional constructor bug where attribution was passed into
the template slot and story generation crashed.
"""

from pathlib import Path
import subprocess
import sys


def test_create_story_smoke(tmp_path: Path):
    output_path = tmp_path / "story.html"
    cmd = [
        sys.executable,
        "-m",
        "modern_graphics.cli",
        "create",
        "--layout",
        "story",
        "--what-changed",
        "Execution scaled through automation",
        "--time-period",
        "Q1 to Q4",
        "--what-it-means",
        "Decision quality now drives outcomes",
        "--output",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout
    assert output_path.exists()
    html = output_path.read_text(encoding="utf-8")
    assert "Execution scaled through automation" in html
