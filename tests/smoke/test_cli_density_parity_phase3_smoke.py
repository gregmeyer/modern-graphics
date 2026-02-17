"""Phase 3 smoke tests for non-create density parity helpers."""

from modern_graphics.cli import (
    shape_story_fields_for_density,
    shape_timeline_events_for_density,
    shape_grid_for_density,
)


def test_story_density_clarity_shortens_fields():
    what_changed, period, meaning = shape_story_fields_for_density(
        "Execution scaled via automation and workflow orchestration across teams",
        "Q1 through Q4 with progressive rollout and governance checkpoints",
        "Decision quality became the leverage point for sustainable outcomes at scale",
        "clarity",
    )
    assert len(what_changed) <= 56
    assert len(period) <= 32
    assert len(meaning) <= 64


def test_timeline_density_clarity_caps_events_and_shortens_text():
    events = [
        {"date": "Q1", "text": "Baseline workflow with many manual approvals"},
        {"date": "Q2", "text": "Automation rollout to primary operating lane"},
        {"date": "Q3", "text": "Decision gates added to release process"},
        {"date": "Q4", "text": "Quality stabilized and escalations reduced"},
        {"date": "Q5", "text": "Should be trimmed by clarity mode"},
    ]
    shaped = shape_timeline_events_for_density(events, "clarity")
    assert len(shaped) == 4
    assert all(len(item["text"]) <= 42 for item in shaped)


def test_grid_density_clarity_caps_columns_and_items():
    items = [{"number": str(i), "text": f"Item text {i} with extended details"} for i in range(1, 10)]
    shaped_items, columns = shape_grid_for_density(items, 5, "clarity")
    assert len(shaped_items) == 6
    assert columns == 3
    assert all(len(item["text"]) <= 34 for item in shaped_items)

