"""MCP server exposing modern-graphics as tools for AI clients.

Run with: python -m modern_graphics.mcp_server
Or via console script: modern-graphics-mcp
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    raise ImportError(
        "MCP server requires the 'mcp' package. "
        "Install with: pip install modern-graphics-generator[mcp]"
    )

from .layouts import DEFAULT_LAYOUT_REGISTRY
from .suggest import (
    EXAMPLE_COMMANDS,
    LAYOUT_DESCRIPTIONS,
    suggest_layout_top_n,
)

app = Server("modern-graphics")

OUTPUT_DIR = os.environ.get("MODERN_GRAPHICS_OUTPUT_DIR", os.path.join(os.getcwd(), "output"))


def _json_response(data: Any) -> list:
    return [TextContent(type="text", text=json.dumps(data, indent=2))]


def _error_response(message: str) -> list:
    return [TextContent(type="text", text=json.dumps({"error": message}, indent=2))]


def _get_layout_info() -> List[Dict[str, Any]]:
    """Build layout metadata from the registry."""
    layouts = []
    for name in DEFAULT_LAYOUT_REGISTRY.list_types():
        strategy = DEFAULT_LAYOUT_REGISTRY.get(name)
        layouts.append({
            "name": name,
            "description": LAYOUT_DESCRIPTIONS.get(name, ""),
            "required_args": sorted(strategy.required_args) if strategy else [],
            "example_command": EXAMPLE_COMMANDS.get(name, ""),
        })
    return layouts


def _generate_sync(
    layout: str,
    args: Dict[str, Any],
    output_path: str,
    fmt: str = "html",
    theme: str | None = None,
) -> Dict[str, Any]:
    """Synchronous rendering — called via asyncio.to_thread."""
    from .generator import ModernGraphicsGenerator
    from .models import Attribution
    from .layouts import render_layout
    from .color_scheme import get_scheme

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    attribution = Attribution()
    generator = ModernGraphicsGenerator("Modern Graphic", attribution=attribution)

    color_scheme = get_scheme(theme) if theme else None
    render_args = dict(args)
    if color_scheme is not None:
        render_args["color_scheme"] = color_scheme

    html = render_layout(layout, generator, **render_args)

    if layout == "story" and color_scheme is not None:
        html = color_scheme.apply_to_html(html)

    result: Dict[str, Any] = {"layout": layout, "format": fmt}

    if fmt == "png":
        png_path = out.with_suffix(".png")
        try:
            generator.export_to_png(html, png_path, crop_mode="safe")
        except Exception as exc:
            return {"error": f"PNG export failed: {exc}. Try format='html' or ensure Playwright is installed."}
        result["file_path"] = str(png_path)
    else:
        html_path = out.with_suffix(".html")
        generator.save(html, html_path)
        result["file_path"] = str(html_path)
        result["html_content"] = html

    return result


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="suggest_layout",
            description="Suggest the best layout for a plain-text description of what you want to create. Returns top recommendations with confidence scores and ready-to-use commands.",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Plain-text description of the graphic you want (e.g., 'compare two approaches side by side')",
                    },
                },
                "required": ["description"],
            },
        ),
        Tool(
            name="list_layouts",
            description="List all available graphic layouts with their required arguments, descriptions, and example commands.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="generate_graphic",
            description="Generate an HTML or PNG graphic using a specified layout. Returns the file path and optionally the HTML content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "layout": {
                        "type": "string",
                        "description": "Layout type (e.g., hero, comparison, timeline, funnel, story, key-insight, grid)",
                    },
                    "args": {
                        "type": "object",
                        "description": "Layout-specific arguments (e.g., {\"headline\": \"My title\"} for hero, {\"left_column\": {...}, \"right_column\": {...}} for comparison)",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path. Defaults to ./output/<layout>.<format>",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["html", "png"],
                        "description": "Output format (default: html). PNG requires Playwright/Chromium.",
                    },
                    "theme": {
                        "type": "string",
                        "description": "Color theme (e.g., corporate, apple, dark, warm, green)",
                    },
                },
                "required": ["layout", "args"],
            },
        ),
        Tool(
            name="preview_layout",
            description="Preview what a layout would produce without actually generating it. Validates inputs and returns a description of the expected output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "layout": {
                        "type": "string",
                        "description": "Layout type to preview",
                    },
                    "args": {
                        "type": "object",
                        "description": "Layout-specific arguments to validate",
                    },
                },
                "required": ["layout", "args"],
            },
        ),
        Tool(
            name="get_layout_help",
            description="Get detailed help for a specific layout including required arguments, optional arguments, and an example command.",
            inputSchema={
                "type": "object",
                "properties": {
                    "layout": {
                        "type": "string",
                        "description": "Layout type to get help for",
                    },
                },
                "required": ["layout"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    try:
        if name == "suggest_layout":
            description = arguments.get("description", "")
            results = suggest_layout_top_n(description, n=3)
            return _json_response({
                "recommended": {
                    "layout": results[0].layout,
                    "confidence": results[0].confidence,
                    "reason": results[0].reason,
                    "description": LAYOUT_DESCRIPTIONS.get(results[0].layout, ""),
                    "example_command": results[0].example_command,
                },
                "alternatives": [
                    {
                        "layout": r.layout,
                        "confidence": r.confidence,
                        "reason": r.reason,
                        "description": LAYOUT_DESCRIPTIONS.get(r.layout, ""),
                    }
                    for r in results[1:]
                ],
            })

        elif name == "list_layouts":
            return _json_response({"layouts": _get_layout_info()})

        elif name == "generate_graphic":
            layout = arguments.get("layout", "")
            args = arguments.get("args", {})
            fmt = arguments.get("format", "html")
            theme = arguments.get("theme")
            output_path = arguments.get(
                "output_path",
                os.path.join(OUTPUT_DIR, f"{layout}.{fmt}"),
            )

            strategy = DEFAULT_LAYOUT_REGISTRY.get(layout)
            if strategy is None:
                available = DEFAULT_LAYOUT_REGISTRY.list_types()
                return _error_response(f"Unknown layout '{layout}'. Available: {', '.join(available)}")

            result = await asyncio.to_thread(
                _generate_sync, layout, args, output_path, fmt, theme
            )

            if "error" in result:
                return _error_response(result["error"])
            return _json_response(result)

        elif name == "preview_layout":
            layout = arguments.get("layout", "")
            args = arguments.get("args", {})

            strategy = DEFAULT_LAYOUT_REGISTRY.get(layout)
            if strategy is None:
                available = DEFAULT_LAYOUT_REGISTRY.list_types()
                return _error_response(f"Unknown layout '{layout}'. Available: {', '.join(available)}")

            missing = sorted(arg for arg in strategy.required_args if arg not in args or args[arg] in (None, ""))
            provided = sorted(arg for arg in args if args[arg] not in (None, ""))

            return _json_response({
                "layout": layout,
                "description": LAYOUT_DESCRIPTIONS.get(layout, ""),
                "required_args_status": {
                    "provided": [a for a in sorted(strategy.required_args) if a in provided],
                    "missing": missing,
                },
                "provided_args": provided,
                "ready": len(missing) == 0,
                "preview": f"Will generate a {layout} graphic" + (f" with {', '.join(provided)}" if provided else ""),
            })

        elif name == "get_layout_help":
            layout = arguments.get("layout", "")
            strategy = DEFAULT_LAYOUT_REGISTRY.get(layout)
            if strategy is None:
                available = DEFAULT_LAYOUT_REGISTRY.list_types()
                return _error_response(f"Unknown layout '{layout}'. Available: {', '.join(available)}")

            return _json_response({
                "layout": layout,
                "description": LAYOUT_DESCRIPTIONS.get(layout, ""),
                "required_args": sorted(strategy.required_args),
                "example_command": EXAMPLE_COMMANDS.get(layout, ""),
            })

        else:
            return _error_response(f"Unknown tool: {name}")

    except Exception as exc:
        return _error_response(str(exc))


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def run():
    """Console script entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
