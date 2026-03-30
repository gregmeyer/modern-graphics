"""Smoke: story mini-tile reserves foreignObject height when Pretext is enabled."""

from modern_graphics.diagrams.story_slide import _build_static_mini_tile

_PALETTE = {
    "background": "#FFFFFF",
    "border": "#E5E5E5",
    "text_primary": "#111111",
    "text_secondary": "#555555",
    "metric_bg": "#F5F5F5",
    "metric_text": "#111111",
    "accent_primary": "#0071E3",
}


def test_mini_tile_pretext_foreign_object_geometry():
    data = {
        "tile_headline": "A" * 36,
        "subline": "B" * 48,
        "pill": "Q1 to Q4",
        "metric": "Meaning line one two",
        "chart": [70, 95, 65, 110],
    }
    html = _build_static_mini_tile(
        640, 400, _PALETTE, data, use_pretext=True
    )
    assert "pretext-slot" in html
    assert 'height="88"' in html
    assert 'height="52"' in html
    assert 'y="56"' in html
    assert 'y="152"' in html
    assert 'y="216"' in html


def test_mini_tile_pretext_legacy_foreign_object_geometry():
    data = {
        "tile_headline": "Headline text here for legacy",
        "subline": "Subline sample copy",
        "pill": "Period",
        "metric": "Metric",
        "chart": [60, 80, 70, 90],
    }
    html = _build_static_mini_tile(
        640,
        400,
        _PALETTE,
        data,
        use_pretext=True,
        pretext_foreign_object_layout="legacy",
    )
    assert "pretext-slot" in html
    assert 'height="44"' in html
    assert 'height="36"' in html
    assert 'y="164"' in html


def test_mini_tile_css_path_unchanged_geometry():
    data = {
        "tile_headline": "Short",
        "subline": "Sub",
        "pill": "Period",
        "metric": "Metric",
        "chart": [60, 80, 70, 90],
    }
    html = _build_static_mini_tile(
        640, 400, _PALETTE, data, use_pretext=False
    )
    assert "foreignObject" not in html
    assert 'y="164"' in html
