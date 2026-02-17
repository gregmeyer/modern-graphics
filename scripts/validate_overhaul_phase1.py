#!/usr/bin/env python3
"""Lightweight Phase 1 scaffold validator.

Used until pytest environment is standardized in this repo.
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modern_graphics.visual_system import CLARITY_TOKENS, token_lint
from modern_graphics.critique_gates import run_clarity_gates, overall_status
from modern_graphics.export_policy import DEFAULT_EXPORT_POLICY
from modern_graphics.cli_clarity import normalize_density, CREATE_DEFAULTS
from modern_graphics.template_lint import run_template_lint


def main() -> int:
    assert CLARITY_TOKENS.typography.body >= 16
    assert CLARITY_TOKENS.spacing.md == 16

    errors = token_lint(["token.spacing.md", "17px"])
    assert len(errors) == 1

    report = run_clarity_gates(
        target="hero",
        min_text_px=13,
        observed_min_text_px=11,
        focal_points=3,
        density_items=9,
        max_density_items=8,
        contrast_ratio=4.2,
        whitespace_ratio=0.40,
    )
    statuses = {r.gate: r.status for r in report.results}
    assert statuses["min_text_size"] == "fail"
    assert statuses["focal_point_budget"] == "warn"
    assert statuses["density_budget"] == "warn"
    assert statuses["contrast_ratio"] == "fail"
    assert statuses["whitespace_guard"] == "fail"
    assert overall_status(report) == "fail"

    assert DEFAULT_EXPORT_POLICY.padding_mode == "minimal"
    assert DEFAULT_EXPORT_POLICY.resolve_padding() == 8
    assert normalize_density("weird") == "clarity"
    assert CREATE_DEFAULTS.density == "clarity"
    assert CREATE_DEFAULTS.crop_mode == "safe"
    assert CREATE_DEFAULTS.padding_mode == "minimal"

    strict_paths = [
        Path(__file__).resolve().parents[1] / "modern_graphics" / "layout_models.py",
        Path(__file__).resolve().parents[1] / "modern_graphics" / "layouts.py",
        Path(__file__).resolve().parents[1] / "modern_graphics" / "generator.py",
        Path(__file__).resolve().parents[1] / "modern_graphics" / "template_lint.py",
    ]
    strict_report = run_template_lint(strict_paths, mode="strict")
    assert strict_report["status"] == "pass"

    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["MODERN_GRAPHICS_ENABLE_CREATE"] = "1"
    env["PYTHONPATH"] = str(root)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        success_cmd = [
            sys.executable,
            "-m",
            "modern_graphics.cli",
            "create",
            "--layout",
            "hero",
            "--headline",
            "Execution scales",
            "--output",
            str(tmp / "hero.html"),
        ]
        success = subprocess.run(success_cmd, cwd=str(root), env=env, capture_output=True, text=True)
        assert success.returncode == 0, success.stderr or success.stdout
        assert "Generated create/hero" in success.stdout

        failure_cmd = [
            sys.executable,
            "-m",
            "modern_graphics.cli",
            "create",
            "--layout",
            "comparison",
            "--left",
            "Before:Manual:Slow",
            "--output",
            str(tmp / "comparison.html"),
        ]
        failure = subprocess.run(failure_cmd, cwd=str(root), env=env, capture_output=True, text=True)
        assert failure.returncode != 0
        assert "--left and --right are required" in failure.stdout
        assert "Hint: try `" in failure.stdout

    print("Phase 1 scaffold validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
