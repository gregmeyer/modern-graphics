"""Smoke checks for Phase 2 layout strategy scaffolding."""

import json
from pathlib import Path

from modern_graphics.generator import ModernGraphicsGenerator
from modern_graphics.layouts import list_layout_strategies
from modern_graphics.template_lint import run_template_lint
from modern_graphics.layout_models import (
    HeroPayload,
    GridPayload,
    KeyInsightPayload,
    InsightCardPayload,
    InsightStoryPayload,
)


def test_layout_strategy_registry_smoke():
    generator = ModernGraphicsGenerator("Strategy Smoke")
    strategy_types = list_layout_strategies()
    assert "hero" in strategy_types
    assert "insight-card" in strategy_types
    assert "comparison" in strategy_types
    assert "timeline" in strategy_types
    assert "funnel" in strategy_types
    assert "grid" in strategy_types
    assert "story" in strategy_types

    html = generator.generate_layout(
        "hero",
        headline="Execution scales. Judgment does not.",
        subheadline="Use explicit gates when output becomes cheap.",
    )
    assert "<div class=\"hero " in html

    comparison_html = generator.generate_layout(
        "comparison",
        left_column={"title": "Before", "steps": ["Manual triage"], "outcome": "Slow"},
        right_column={"title": "After", "steps": ["Agentic triage"], "outcome": "Faster"},
    )
    assert "Before" in comparison_html


def test_template_lint_strict_scaffold_smoke(tmp_path):
    clean_file = tmp_path / "clean.py"
    clean_file.write_text("value = 'token.spacing.md'\n", encoding="utf-8")
    report = run_template_lint([clean_file], mode="strict")
    assert report["status"] == "pass"


def test_layout_models_smoke():
    hero = HeroPayload(headline="Execution scales")
    assert hero.to_strategy_kwargs()["headline"] == "Execution scales"

    grid = GridPayload(items=[{"number": "1", "text": "One"}], columns=1)
    assert grid.to_strategy_kwargs()["columns"] == 1


def test_insight_payload_fixtures_smoke():
    fixture_path = Path(__file__).with_name("fixtures_insight_cards.json")
    fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
    generator = ModernGraphicsGenerator("Insight Fixture Smoke")

    for fixture in fixtures:
        kind = fixture["kind"]
        if kind == "key_insight":
            payload = KeyInsightPayload(
                text=fixture["text"],
                label=fixture.get("label", "Key Insight"),
                variant=fixture.get("variant", "bold"),
                icon=fixture.get("icon", "lightning"),
            )
            html = generator.generate_layout("key-insight", **payload.to_strategy_kwargs())
        elif kind == "insight_card":
            payload = InsightCardPayload(
                text=fixture["text"],
                svg_content=fixture["svg_content"],
                label=fixture.get("label", "Key Insight"),
                svg_label=fixture.get("svg_label"),
                layout=fixture.get("layout", "side-by-side"),
                svg_position=fixture.get("svg_position", "right"),
                variant=fixture.get("variant", "bold"),
                icon=fixture.get("icon", "lightning"),
            )
            html = generator.generate_layout("insight-card", **payload.to_strategy_kwargs())
        elif kind == "insight_story":
            payload = InsightStoryPayload(
                headline=fixture["headline"],
                insight_text=fixture["insight_text"],
                before_svg=fixture["before_svg"],
                after_svg=fixture["after_svg"],
            )
            html = generator.generate_layout("insight-story", **payload.to_strategy_kwargs())
        else:
            raise AssertionError(f"Unknown fixture kind: {kind}")

        assert "<html" in html.lower()
