"""Phase 5 smoke checks for CLI migration adapters."""

from modern_graphics.cli import _adapt_legacy_command_aliases, LEGACY_CREATE_HINTS


def test_legacy_aliases_are_adapted():
    argv, warning = _adapt_legacy_command_aliases([
        "modern-graphics",
        "slide-comparison",
        "--title",
        "T",
    ])
    assert argv[1] == "slide-compare"
    assert warning and "deprecated" in warning.lower()


def test_non_legacy_command_is_unchanged():
    argv, warning = _adapt_legacy_command_aliases([
        "modern-graphics",
        "create",
        "--layout",
        "hero",
    ])
    assert argv[1] == "create"
    assert warning is None


def test_legacy_create_hints_cover_core_commands():
    for command in ["comparison", "timeline", "insight-card", "key-insight"]:
        assert command in LEGACY_CREATE_HINTS
        assert "modern-graphics create" in LEGACY_CREATE_HINTS[command]
