"""Smoke tests for MCP server tool handlers.

Tests the handler logic directly without MCP transport.
Skips if the mcp package is not installed.
"""

import json
import pytest

try:
    import mcp  # noqa: F401
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

pytestmark = pytest.mark.skipif(not HAS_MCP, reason="mcp package not installed")


@pytest.fixture
def call_tool():
    """Helper to call an MCP tool handler and parse the JSON response."""
    import asyncio
    from modern_graphics.mcp_server import call_tool as _call_tool

    def _call(name: str, arguments: dict) -> dict:
        result = asyncio.run(_call_tool(name, arguments))
        assert len(result) == 1
        return json.loads(result[0].text)

    return _call


def test_suggest_layout(call_tool):
    result = call_tool("suggest_layout", {"description": "compare two approaches"})
    assert "recommended" in result
    assert result["recommended"]["layout"] == "comparison"
    assert result["recommended"]["confidence"] > 0


def test_suggest_layout_has_alternatives(call_tool):
    result = call_tool("suggest_layout", {"description": "compare timeline of events"})
    assert "alternatives" in result
    assert len(result["alternatives"]) > 0


def test_list_layouts(call_tool):
    result = call_tool("list_layouts", {})
    assert "layouts" in result
    layouts = result["layouts"]
    names = [l["name"] for l in layouts]
    assert "hero" in names
    assert "comparison" in names
    assert len(names) >= 8


def test_get_layout_help(call_tool):
    result = call_tool("get_layout_help", {"layout": "hero"})
    assert result["layout"] == "hero"
    assert "headline" in result["required_args"]
    assert "example_command" in result


def test_get_layout_help_unknown(call_tool):
    result = call_tool("get_layout_help", {"layout": "nonexistent"})
    assert "error" in result


def test_preview_layout_ready(call_tool):
    result = call_tool("preview_layout", {
        "layout": "hero",
        "args": {"headline": "Test headline"},
    })
    assert result["ready"] is True
    assert result["layout"] == "hero"
    assert len(result["required_args_status"]["missing"]) == 0


def test_preview_layout_missing_args(call_tool):
    result = call_tool("preview_layout", {
        "layout": "comparison",
        "args": {},
    })
    assert result["ready"] is False
    assert "left_column" in result["required_args_status"]["missing"]


def test_generate_graphic_html(call_tool, tmp_path):
    import os
    os.environ["MODERN_GRAPHICS_OUTPUT_DIR"] = str(tmp_path)
    # Reload to pick up new env var
    import modern_graphics.mcp_server as srv
    srv.OUTPUT_DIR = str(tmp_path)

    result = call_tool("generate_graphic", {
        "layout": "hero",
        "args": {"headline": "MCP test graphic"},
        "format": "html",
    })
    assert "error" not in result
    assert result["format"] == "html"
    assert result["file_path"].endswith(".html")
    assert "html_content" in result


def test_generate_graphic_unknown_layout(call_tool):
    result = call_tool("generate_graphic", {
        "layout": "nonexistent",
        "args": {},
    })
    assert "error" in result


def test_unknown_tool(call_tool):
    result = call_tool("nonexistent_tool", {})
    assert "error" in result
