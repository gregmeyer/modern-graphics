"""Utilities for embedding images as data URLs in layouts."""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Optional


def file_to_dataurl(path: str, max_size_mb: float = 5.0) -> str:
    """Convert an image file to a base64 data URL.

    Supports PNG, JPEG, GIF, SVG, WebP.
    Raises FileNotFoundError if path doesn't exist.
    Raises ValueError if file exceeds max_size_mb or has unsupported type.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(f"Image file too large: {size_mb:.1f}MB (max {max_size_mb}MB)")

    mime, _ = mimetypes.guess_type(str(p))
    if mime is None or not mime.startswith("image/"):
        raise ValueError(f"Unsupported image type for {p.name}")

    data = p.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def image_path_to_img_tag(
    path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> str:
    """Convert an image file path to an <img> tag with embedded data URL."""
    dataurl = file_to_dataurl(path)
    style_parts = []
    if width:
        style_parts.append(f"max-width:{width}px")
    if height:
        style_parts.append(f"max-height:{height}px")
    style_parts.append("object-fit:contain")
    style = f' style="{";".join(style_parts)}"'
    return f'<img src="{dataurl}"{style} />'


def image_path_to_svg_image(
    path: str,
    x: int = 0,
    y: int = 0,
    width: int = 360,
    height: int = 260,
) -> str:
    """Convert an image file path to a wrapped SVG with embedded <image> element."""
    dataurl = file_to_dataurl(path)
    return (
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f'<image href="{dataurl}" x="{x}" y="{y}" width="{width}" height="{height}" '
        f'preserveAspectRatio="xMidYMid meet" />'
        f'</svg>'
    )
