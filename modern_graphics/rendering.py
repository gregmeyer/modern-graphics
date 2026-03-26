"""Shared rendering functions used by MCP server and web app."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from .layouts import DEFAULT_LAYOUT_REGISTRY
from .suggest import EXAMPLE_COMMANDS, LAYOUT_DESCRIPTIONS

OUTPUT_DIR = os.environ.get("MODERN_GRAPHICS_OUTPUT_DIR", os.path.join(os.getcwd(), "output"))


def get_layout_info() -> List[Dict[str, Any]]:
    """Build layout metadata from the registry, preferring strategy metadata."""
    layouts = []
    for name in DEFAULT_LAYOUT_REGISTRY.list_types():
        strategy = DEFAULT_LAYOUT_REGISTRY.get(name)
        layouts.append({
            "name": name,
            "description": (strategy.description if strategy else "") or LAYOUT_DESCRIPTIONS.get(name, ""),
            "required_args": sorted(strategy.required_args) if strategy else [],
            "example_command": (strategy.example_command if strategy else "") or EXAMPLE_COMMANDS.get(name, ""),
        })
    return layouts


def get_theme_info() -> list:
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


def generate_sync(
    layout: str,
    args: Dict[str, Any],
    output_path: str,
    fmt: str = "html",
    theme: str | None = None,
    transparent: bool = False,
) -> Dict[str, Any]:
    """Synchronous rendering — generates HTML or PNG."""
    from .generator import ModernGraphicsGenerator
    from .models import Attribution
    from .layouts import render_layout
    from .color_scheme import get_scheme

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    attribution = Attribution()
    title = args.pop("title", "") or ""
    generator = ModernGraphicsGenerator(title, attribution=attribution)

    color_scheme = get_scheme(theme) if theme else None
    render_args = dict(args)
    if color_scheme is not None:
        render_args["color_scheme"] = color_scheme

    # Preprocess image paths -> embedded data URLs
    try:
        from .image_utils import image_path_to_img_tag, image_path_to_svg_image

        if layout == "insight-card" and "image_path" in render_args and "svg_content" not in render_args:
            img_path = render_args.pop("image_path")
            w = int(render_args.pop("image_width", 360))
            h = int(render_args.pop("image_height", 260))
            render_args["svg_content"] = image_path_to_svg_image(img_path, width=w, height=h)

        if layout == "hero" and "image_path" in render_args and "freeform_canvas" not in render_args:
            img_path = render_args.pop("image_path")
            render_args["freeform_canvas"] = image_path_to_img_tag(img_path)

        if layout == "insight-story":
            for key, svg_key in [("before_image_path", "before_svg"), ("after_image_path", "after_svg")]:
                if key in render_args and svg_key not in render_args:
                    img_path = render_args.pop(key)
                    render_args[svg_key] = image_path_to_svg_image(img_path, width=360, height=260)
    except (FileNotFoundError, ValueError) as exc:
        return {"error": str(exc)}

    html = render_layout(layout, generator, **render_args)

    if layout == "story" and color_scheme is not None:
        html = color_scheme.apply_to_html(html)

    result: Dict[str, Any] = {"layout": layout, "format": fmt}

    if fmt == "png":
        png_path = out.with_suffix(".png")
        try:
            generator.export_to_png(html, png_path, crop_mode="safe", transparent_background=transparent)
        except Exception as exc:
            return {"error": f"PNG export failed: {exc}. Try format='html' or ensure Playwright is installed."}
        result["file_path"] = str(png_path)
    else:
        html_path = out.with_suffix(".html")
        generator.save(html, html_path)
        result["file_path"] = str(html_path)
        result["html_content"] = html

    # Include gallery URL if the site is running
    site_port = os.environ.get("MODERN_GRAPHICS_SITE_PORT", "8484")
    result["gallery_url"] = f"http://localhost:{site_port}"

    return result
