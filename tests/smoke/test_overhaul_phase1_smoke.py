"""Phase 1 smoke checks for overhaul scaffolding.

These are intentionally lightweight and should run in constrained environments.
"""

from modern_graphics.visual_system import CLARITY_TOKENS, token_lint
from modern_graphics.critique_gates import run_clarity_gates
from modern_graphics.export_policy import DEFAULT_EXPORT_POLICY
from modern_graphics.cli_clarity import normalize_density


def test_phase1_scaffold_smoke():
    assert CLARITY_TOKENS.typography.body >= 16
    assert CLARITY_TOKENS.spacing.md == 16

    errors = token_lint(["token.spacing.md", "17px"])
    assert len(errors) == 1

    report = run_clarity_gates(
        target="hero",
        min_text_px=13,
        observed_min_text_px=11,
        focal_points=3,
        whitespace_ratio=0.40,
    )
    statuses = {r.gate: r.status for r in report.results}
    assert statuses["min_text_size"] == "fail"
    assert statuses["focal_point_budget"] == "warn"
    assert statuses["whitespace_guard"] == "fail"

    assert DEFAULT_EXPORT_POLICY.resolve_padding() == 8
    assert normalize_density("weird") == "clarity"
