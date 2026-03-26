"""MCP server exposing modern-graphics as tools for AI clients.

Run with: python -m modern_graphics.mcp_server
Or via console script: modern-graphics-mcp
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict

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
from .rendering import (
    generate_sync as _generate_sync,
    get_layout_info as _get_layout_info,
    get_theme_info as _get_theme_info,
    OUTPUT_DIR,
)


app = Server("modern-graphics")


def _json_response(data: Any) -> list:
    return [TextContent(type="text", text=json.dumps(data, indent=2))]


def _error_response(message: str) -> list:
    return [TextContent(type="text", text=json.dumps({"error": message}, indent=2))]


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
                    "transparent": {
                        "type": "boolean",
                        "description": "If true, PNG background is transparent instead of white. Default: false.",
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
        Tool(
            name="composite_image",
            description="Overlay one image on top of another at a specified position. Use to add logos, watermarks, or badges to generated graphics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "base": {
                        "type": "string",
                        "description": "Path to the base image (PNG)",
                    },
                    "overlay": {
                        "type": "string",
                        "description": "Path to the overlay image (PNG, supports transparency)",
                    },
                    "position": {
                        "type": "string",
                        "enum": ["top-left", "top-center", "top-right", "center", "bottom-left", "bottom-center", "bottom-right"],
                        "description": "Where to place the overlay (default: top-right)",
                    },
                    "x": {
                        "type": "integer",
                        "description": "Optional exact X pixel offset from left. Overrides position.",
                    },
                    "y": {
                        "type": "integer",
                        "description": "Optional exact Y pixel offset from top. Overrides position.",
                    },
                    "scale": {
                        "type": "number",
                        "description": "Scale factor for the overlay (e.g., 0.5 = half size, 2.0 = double). Default: 1.0",
                    },
                    "padding": {
                        "type": "integer",
                        "description": "Padding in pixels from the edge when using named positions. Default: 20",
                    },
                    "output": {
                        "type": "string",
                        "description": "Output path. Defaults to overwriting the base image.",
                    },
                },
                "required": ["base", "overlay"],
            },
        ),
        Tool(
            name="generate_wireframe",
            description="Generate a wireframe SVG from a scene preset, custom spec, or description. Supports theme-aware colors. Returns SVG content and optionally saves to file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "preset": {
                        "type": "string",
                        "description": "Scene preset name (e.g., 'before', 'after', 'postit_flow', 'postit_flow_orgchart', 'postit_flow_mindmap')",
                    },
                    "scene_spec": {
                        "type": "object",
                        "description": "Custom scene spec: {width, height, elements: [{type, x, y, width?, height?, props?}]}",
                    },
                    "description": {
                        "type": "string",
                        "description": "Describe what the wireframe should show — auto-matched to the best preset",
                    },
                    "theme": {
                        "type": "string",
                        "description": "Color theme — wireframe inherits theme colors (e.g., 'dark' for dark backgrounds)",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional path to save the SVG file",
                    },
                },
            },
        ),
        Tool(
            name="list_wireframe_elements",
            description="List all available wireframe element types and scene presets.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="register_wireframe_preset",
            description="Register a custom wireframe scene preset for reuse. The preset becomes available in generate_wireframe and list_wireframe_elements.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Preset name",
                    },
                    "scene_spec": {
                        "type": "object",
                        "description": "Scene spec: {width, height, elements: [{type, x, y, width?, height?, props?}]}",
                    },
                },
                "required": ["name", "scene_spec"],
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

        elif name == "list_themes":
            return _json_response({"themes": _get_theme_info()})

        elif name == "generate_graphic":
            layout = arguments.get("layout", "")
            args = arguments.get("args", {})
            fmt = arguments.get("format", "html")
            theme = arguments.get("theme")
            transparent = arguments.get("transparent", False)
            output_path = arguments.get(
                "output_path",
                os.path.join(OUTPUT_DIR, f"{layout}.{fmt}"),
            )

            strategy = DEFAULT_LAYOUT_REGISTRY.get(layout)
            if strategy is None:
                available = DEFAULT_LAYOUT_REGISTRY.list_types()
                return _error_response(f"Unknown layout '{layout}'. Available: {', '.join(available)}")

            result = await asyncio.to_thread(
                _generate_sync, layout, args, output_path, fmt, theme, transparent
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

        elif name == "composite_image":
            from PIL import Image as PILImage

            base_path = arguments.get("base", "")
            overlay_path = arguments.get("overlay", "")
            if not base_path or not overlay_path:
                return _error_response("'base' and 'overlay' are required.")

            if not os.path.exists(base_path):
                return _error_response(f"Base image not found: {base_path}")
            if not os.path.exists(overlay_path):
                return _error_response(f"Overlay image not found: {overlay_path}")

            def _composite() -> Dict[str, Any]:
                base_img = PILImage.open(base_path).convert("RGBA")
                overlay_img = PILImage.open(overlay_path).convert("RGBA")

                scale = arguments.get("scale", 1.0)
                if scale != 1.0:
                    new_w = int(overlay_img.width * scale)
                    new_h = int(overlay_img.height * scale)
                    overlay_img = overlay_img.resize((new_w, new_h), PILImage.LANCZOS)

                pad = arguments.get("padding", 20)
                bw, bh = base_img.size
                ow, oh = overlay_img.size

                if "x" in arguments and "y" in arguments:
                    x, y = arguments["x"], arguments["y"]
                else:
                    pos = arguments.get("position", "top-right")
                    positions = {
                        "top-left": (pad, pad),
                        "top-center": ((bw - ow) // 2, pad),
                        "top-right": (bw - ow - pad, pad),
                        "center": ((bw - ow) // 2, (bh - oh) // 2),
                        "bottom-left": (pad, bh - oh - pad),
                        "bottom-center": ((bw - ow) // 2, bh - oh - pad),
                        "bottom-right": (bw - ow - pad, bh - oh - pad),
                    }
                    x, y = positions.get(pos, positions["top-right"])

                base_img.paste(overlay_img, (x, y), overlay_img)

                out_path = arguments.get("output", base_path)
                if out_path.lower().endswith(".png"):
                    base_img.save(out_path)  # preserve RGBA transparency
                else:
                    base_img.convert("RGB").save(out_path)
                return {"composited": True, "output": out_path, "overlay_size": [ow, oh], "position": [x, y]}

            result = await asyncio.to_thread(_composite)
            return _json_response(result)

        elif name == "generate_wireframe":
            from .diagrams.wireframe_scene import render_scene, list_presets as _list_presets
            from .diagrams.wireframe_elements.config import WireframeConfig

            preset = arguments.get("preset")
            scene_spec = arguments.get("scene_spec")
            desc = arguments.get("description")
            wf_theme = arguments.get("theme")
            output_path = arguments.get("output_path")

            # Build config with theme colors
            config = WireframeConfig()
            if wf_theme:
                from .color_scheme import get_scheme as _get_scheme_wf
                scheme = _get_scheme_wf(wf_theme)
                if scheme:
                    config = WireframeConfig.from_color_scheme(scheme)

            # Determine spec
            if desc and not preset and not scene_spec:
                preset = _match_wireframe_description(desc)
            if preset:
                spec = preset
            elif scene_spec:
                spec = scene_spec
            else:
                return _error_response("Provide one of: preset, scene_spec, or description")

            svg = render_scene(spec, config)
            result_data: Dict[str, Any] = {"svg_content": svg}
            if isinstance(preset, str):
                result_data["preset_used"] = preset

            if output_path:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(svg, encoding="utf-8")
                result_data["file_path"] = str(out)

            return _json_response(result_data)

        elif name == "list_wireframe_elements":
            from .diagrams.wireframe_scene import list_presets as _list_presets_info, list_element_types as _list_el
            return _json_response({
                "element_types": _list_el(),
                "presets": _list_presets_info(),
            })

        elif name == "register_wireframe_preset":
            from .diagrams.wireframe_scene import register_preset
            preset_name = arguments.get("name", "")
            scene_spec = arguments.get("scene_spec", {})
            if not preset_name or not scene_spec:
                return _error_response("'name' and 'scene_spec' are required.")
            register_preset(preset_name, scene_spec)
            return _json_response({"registered": True, "name": preset_name})

        else:
            return _error_response(f"Unknown tool: {name}")

    except Exception as exc:
        return _error_response(str(exc))


_WIREFRAME_KEYWORD_MAP = [
    ("before", ["before", "old", "legacy", "manual", "current state"]),
    ("after", ["after", "new", "modern", "agentic", "improved"]),
    ("postit_flow", ["flow", "process", "steps", "sequence", "workflow"]),
    ("postit_flow_zigzag", ["zigzag", "back and forth"]),
    ("postit_flow_orgchart", ["org chart", "orgchart", "hierarchy", "reporting structure"]),
    ("postit_flow_fishbone", ["fishbone", "root cause", "cause and effect", "ishikawa"]),
    ("postit_flow_mindmap", ["mind map", "mindmap", "brainstorm", "idea map"]),
    ("postit_flow_outline", ["outline", "nested", "indented"]),
    ("postit_flow_vertical", ["vertical", "top to bottom", "top-down"]),
    ("postit_flow_arc", ["arc", "curved"]),
]


def _match_wireframe_description(description: str) -> str:
    """Match a description to the best wireframe preset."""
    desc_lower = description.lower()
    best_preset = "after"
    best_score = 0
    for preset_name, keywords in _WIREFRAME_KEYWORD_MAP:
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > best_score:
            best_score = score
            best_preset = preset_name
    return best_preset


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def run():
    """Console script entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
