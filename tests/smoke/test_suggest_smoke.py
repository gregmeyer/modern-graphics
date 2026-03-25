"""Smoke tests for the deterministic layout suggest module."""

from modern_graphics.suggest import suggest_layout, suggest_layout_top_n


def test_comparison_keywords():
    result = suggest_layout("I want to compare two approaches")
    assert result.layout == "comparison"
    assert result.confidence > 0.0


def test_vs_keyword():
    result = suggest_layout("old way vs new way")
    assert result.layout == "comparison"


def test_timeline_keywords():
    result = suggest_layout("show a timeline of milestones")
    assert result.layout == "timeline"


def test_story_keywords():
    result = suggest_layout("tell the story of what changed")
    assert result.layout == "story"


def test_insight_keywords():
    result = suggest_layout("a key insight quote from the report")
    assert result.layout == "key-insight"


def test_funnel_keywords():
    result = suggest_layout("conversion funnel with drop-off rates")
    assert result.layout == "funnel"


def test_hero_keywords():
    result = suggest_layout("big headline opener for the deck")
    assert result.layout == "hero"


def test_grid_keywords():
    result = suggest_layout("a list of priorities in a grid")
    assert result.layout == "grid"


def test_no_match_defaults_to_hero():
    result = suggest_layout("xyzzy foobar nonsense")
    assert result.layout == "hero"
    assert result.confidence == 0.1
    assert "no keyword matches" in result.reason


def test_empty_string_defaults_to_hero():
    result = suggest_layout("")
    assert result.layout == "hero"
    assert result.confidence == 0.1


def test_top_n_returns_multiple():
    results = suggest_layout_top_n("compare and show a timeline", n=3)
    assert len(results) >= 2
    layouts = [r.layout for r in results]
    assert "comparison" in layouts
    assert "timeline" in layouts


def test_result_has_example_command():
    result = suggest_layout("funnel")
    assert "modern-graphics create" in result.example_command
    assert "--layout funnel" in result.example_command


def test_confidence_is_bounded():
    result = suggest_layout("compare vs tradeoff side by side pros cons before and after")
    assert 0.0 < result.confidence <= 1.0
