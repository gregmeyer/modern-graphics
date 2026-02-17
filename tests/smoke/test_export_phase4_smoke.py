"""Phase 4 smoke checks for deterministic export behavior."""

from modern_graphics.export import (
    _calculate_crop_box,
    _effective_padding,
    _normalize_crop_mode,
)


def test_normalize_crop_mode_defaults_to_safe():
    assert _normalize_crop_mode("safe") == "safe"
    assert _normalize_crop_mode("tight") == "tight"
    assert _normalize_crop_mode("none") == "none"
    assert _normalize_crop_mode("unexpected") == "safe"


def test_tight_mode_reduces_padding_deterministically():
    assert _effective_padding("safe", 8) == 8
    assert _effective_padding("tight", 8) == 4
    assert _effective_padding("tight", 7) == 4


def test_crop_box_respects_bounds_and_padding():
    box = _calculate_crop_box(
        {"x": 100, "y": 50, "width": 200, "height": 100},
        image_width=1000,
        image_height=700,
        device_scale_factor=2,
        padding=8,
    )
    assert box == (184, 84, 616, 316)


def test_crop_box_clamps_to_image_edges():
    box = _calculate_crop_box(
        {"x": -5, "y": -10, "width": 1200, "height": 900},
        image_width=1000,
        image_height=700,
        device_scale_factor=1,
        padding=10,
    )
    assert box == (0, 0, 1000, 700)
