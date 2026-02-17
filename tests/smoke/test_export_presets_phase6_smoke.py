"""Phase 6 smoke checks for social export presets."""

from modern_graphics.export_presets import list_export_presets, get_export_preset


def test_export_presets_registry_smoke():
    assert list_export_presets() == ["linkedin", "substack-hero", "x"]


def test_linkedin_preset_defaults():
    preset = get_export_preset("linkedin")
    assert preset is not None
    assert preset.viewport_width == 1200
    assert preset.viewport_height == 627
    assert preset.device_scale_factor == 1
    assert preset.crop_mode == "none"
    assert preset.padding_mode == "none"


def test_unknown_preset_returns_none():
    assert get_export_preset("unknown") is None
