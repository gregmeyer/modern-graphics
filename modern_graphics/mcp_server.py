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
        Tool(
            name="list_themes",
            description="List all available color themes with their primary/accent colors and descriptions.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="create_theme",
            description="Create a custom color theme from a primary color and optional settings. The theme is registered for immediate use in generate_graphic. Returns the full theme details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Theme name (e.g., 'my-brand')",
                    },
                    "primary": {
                        "type": "string",
                        "description": "Primary brand color as hex (e.g., '#8B5CF6')",
                    },
                    "accent": {
                        "type": "string",
                        "description": "Optional accent color as hex. Auto-generated from primary if omitted.",
                    },
                    "background": {
                        "type": "string",
                        "description": "Optional background color as hex (e.g., '#0a0a0a' for dark, '#ffffff' for light).",
                    },
                    "font": {
                        "type": "string",
                        "description": "Optional Google Font name (e.g., 'Inter', 'Lora', 'Roboto Mono').",
                    },
                    "font_style": {
                        "type": "string",
                        "enum": ["sans-serif", "serif", "monospace"],
                        "description": "Font style (default: sans-serif).",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional human-readable description of the theme.",
                    },
                },
                "required": ["name", "primary"],
            },
        ),
        Tool(
            name="preview_theme",
            description="Generate a sample hero graphic with a given theme (built-in or custom) to preview how it looks. Returns the PNG file path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": "Theme name to preview (built-in or custom)",
                    },
                },
                "required": ["theme"],
            },
        ),
        Tool(
            name="save_theme",
            description="Save a custom theme to a JSON file for reuse across sessions. The theme must have been created with create_theme first.",
            inputSchema={
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": "Name of the custom theme to save",
                    },
                    "path": {
                        "type": "string",
                        "description": "Optional file path. Defaults to examples/schemes/<name>.json",
                    },
                },
                "required": ["theme"],
            },
        ),
    ]


def _get_theme_info() -> list:
    """Build theme metadata from the registry."""
    from .color_scheme import SCHEME_REGISTRY
    seen = set()
    themes = []
    for name, scheme in SCHEME_REGISTRY.items():
        if id(scheme) in seen:
            continue
        seen.add(id(scheme))
        aliases = [k for k, v in SCHEME_REGISTRY.items() if v is scheme and k != name]
        themes.append({
            "name": name,
            "description": getattr(scheme, "description", "") or "",
            "primary": getattr(scheme, "primary", "") or "",
            "accent": getattr(scheme, "accent", "") or "",
            "aliases": aliases,
        })
    return themes


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

        elif name == "list_themes":
            return _json_response({"themes": _get_theme_info()})

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

        elif name == "create_theme":
            from .color_scheme import create_custom_scheme, register_scheme

            theme_name = arguments.get("name", "")
            primary = arguments.get("primary", "")
            if not theme_name or not primary:
                return _error_response("'name' and 'primary' are required.")

            kwargs = {}
            if arguments.get("accent"):
                kwargs["accent"] = arguments["accent"]
            if arguments.get("background"):
                kwargs["bg_primary"] = arguments["background"]
            if arguments.get("font"):
                kwargs["google_font_name"] = arguments["font"]
            if arguments.get("font_style"):
                kwargs["font_style"] = arguments["font_style"]
            if arguments.get("description"):
                kwargs["description"] = arguments["description"]

            scheme = create_custom_scheme(name=theme_name, primary=primary, **kwargs)
            register_scheme(scheme)

            return _json_response({
                "created": True,
                "theme": {
                    "name": scheme.name,
                    "primary": scheme.primary,
                    "secondary": scheme.secondary,
                    "accent": scheme.accent,
                    "bg_primary": scheme.bg_primary,
                    "font_style": scheme.font_style,
                    "google_font_name": scheme.google_font_name,
                    "description": scheme.description,
                },
                "usage": f"Use with generate_graphic: theme='{scheme.name}'",
            })

        elif name == "preview_theme":
            from .color_scheme import get_scheme as _get_scheme
            theme_name = arguments.get("theme", "")
            scheme = _get_scheme(theme_name)
            if scheme is None:
                return _error_response(f"Unknown theme '{theme_name}'. Create it with create_theme first, or use list_themes to see built-in themes.")

            preview_path = os.path.join(OUTPUT_DIR, f"theme-preview-{theme_name}.png")
            result = await asyncio.to_thread(
                _generate_sync,
                "hero",
                {"headline": f"Theme Preview: {theme_name}"},
                preview_path,
                "png",
                theme_name,
            )
            if "error" in result:
                return _error_response(result["error"])
            return _json_response({
                "theme": theme_name,
                "preview_path": result["file_path"],
                "description": getattr(scheme, "description", ""),
            })

        elif name == "save_theme":
            from .color_scheme import get_scheme as _get_scheme
            theme_name = arguments.get("theme", "")
            scheme = _get_scheme(theme_name)
            if scheme is None:
                return _error_response(f"Unknown theme '{theme_name}'. Create it with create_theme first.")

            save_path = arguments.get("path") or os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "examples", "schemes", f"{theme_name}.json",
            )
            save_dir = os.path.dirname(save_path)
            os.makedirs(save_dir, exist_ok=True)

            theme_data = {
                "name": scheme.name,
                "description": scheme.description or "",
                "primary": scheme.primary,
                "secondary": scheme.secondary,
                "accent": scheme.accent,
                "bg_primary": scheme.bg_primary,
                "bg_secondary": scheme.bg_secondary,
                "bg_tertiary": scheme.bg_tertiary,
                "bg_dark": scheme.bg_dark,
                "text_primary": scheme.text_primary,
                "text_secondary": scheme.text_secondary,
                "text_on_dark": scheme.text_on_dark,
                "border_light": scheme.border_light,
                "border_medium": scheme.border_medium,
                "font_style": scheme.font_style,
                "google_font_name": scheme.google_font_name,
            }

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(theme_data, f, indent=2)

            return _json_response({
                "saved": True,
                "path": save_path,
                "theme": theme_name,
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
