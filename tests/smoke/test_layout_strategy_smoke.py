"""Smoke checks for Phase 2 layout strategy scaffolding."""

from modern_graphics.generator import ModernGraphicsGenerator
from modern_graphics.layouts import list_layout_strategies
from modern_graphics.template_lint import run_template_lint


def test_layout_strategy_registry_smoke():
    generator = ModernGraphicsGenerator("Strategy Smoke")
    strategy_types = list_layout_strategies()
    assert "hero" in strategy_types
    assert "insight-card" in strategy_types

    html = generator.generate_layout(
        "hero",
        headline="Execution scales. Judgment does not.",
        subheadline="Use explicit gates when output becomes cheap.",
    )
    assert "<div class=\"hero " in html


def test_template_lint_strict_scaffold_smoke(tmp_path):
    clean_file = tmp_path / "clean.py"
    clean_file.write_text("value = 'token.spacing.md'\n", encoding="utf-8")
    report = run_template_lint([clean_file], mode="strict")
    assert report["status"] == "pass"
