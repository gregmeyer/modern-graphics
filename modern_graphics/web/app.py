"""Starlette web server for the interactive gallery and live generation.

Usage: python -m modern_graphics.web.app --port 8080
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from ..rendering import generate_sync, get_layout_info, get_theme_info, OUTPUT_DIR


SITE_DIR = os.environ.get("MODERN_GRAPHICS_SITE_DIR", os.path.join(os.getcwd(), "site"))


async def index(request: Request):
    index_path = os.path.join(SITE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "Gallery not built. Run: make gallery"}, status_code=404)


async def api_layouts(request: Request):
    return JSONResponse({"layouts": get_layout_info()})


async def api_themes(request: Request):
    return JSONResponse({"themes": get_theme_info()})


async def api_generate(request: Request):
    body = await request.json()
    layout = body.get("layout", "")
    args = body.get("args", {})
    theme = body.get("theme")
    fmt = body.get("format", "png")

    output_path = os.path.join(OUTPUT_DIR, f"{layout}.{fmt}")

    from ..layouts import DEFAULT_LAYOUT_REGISTRY
    strategy = DEFAULT_LAYOUT_REGISTRY.get(layout)
    if strategy is None:
        available = DEFAULT_LAYOUT_REGISTRY.list_types()
        return JSONResponse({"error": f"Unknown layout '{layout}'. Available: {', '.join(available)}"})

    result = await asyncio.to_thread(
        generate_sync, layout, dict(args), output_path, fmt, theme
    )

    if "error" in result:
        return JSONResponse(result)

    # Build file URL for the client
    file_path = result.get("file_path", "")
    if file_path:
        filename = os.path.basename(file_path)
        result["file_url"] = f"/output/{filename}"

    # Build CLI command
    cli = f"modern-graphics create --layout {layout}"
    for k, v in args.items():
        cli += f' --{k.replace("_", "-")} "{v}"'
    if theme:
        cli += f" --theme {theme}"
    if fmt == "png":
        cli += " --png"
    cli += f" --output ./output/{layout}.{fmt}"
    result["cli_command"] = cli

    # Build MCP command
    result["mcp_command"] = {
        "tool": "generate_graphic",
        "arguments": {"layout": layout, "args": args, "format": fmt, **({"theme": theme} if theme else {})},
    }

    return JSONResponse(result)


def create_app() -> Starlette:
    routes = [
        Route("/", index),
        Route("/api/layouts", api_layouts),
        Route("/api/themes", api_themes),
        Route("/api/generate", api_generate, methods=["POST"]),
    ]

    app = Starlette(routes=routes)

    # Mount static files from the site directory
    site_path = Path(SITE_DIR)
    if site_path.exists():
        app.mount("/images", StaticFiles(directory=str(site_path / "images")), name="images")
        app.mount("/theme-images", StaticFiles(directory=str(site_path / "theme-images")), name="theme-images")
        # Serve CSS and JS from site root
        for static_file in ["style.css", "app.js"]:
            fpath = site_path / static_file
            if fpath.exists():
                app.routes.insert(0, Route(f"/{static_file}", lambda req, f=str(fpath): FileResponse(f)))

    # Mount output directory for generated files
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    app.mount("/output", StaticFiles(directory=str(output_path)), name="output")

    return app


def main():
    import uvicorn

    parser = argparse.ArgumentParser(description="Modern Graphics gallery server")
    parser.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")
    parser.add_argument("--host", default="0.0.0.0", help="Host (default: 0.0.0.0)")
    args = parser.parse_args()

    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
