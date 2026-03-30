"""Python-side helpers for emitting Pretext-compatible markup.

Layout functions use these helpers to emit ``<div class="pretext-slot">``
placeholders. The Pretext bootstrap script (see pretext_utils.py) handles
measurement and SVG injection at render time.
"""

from html import escape
from typing import Optional


def pretext_slot(
    text: str,
    font: str,
    max_width: float,
    line_height: float = 1.15,
    css_class: str = "",
    fill: str = "currentColor",
    text_anchor: str = "start",
) -> str:
    """Emit a pretext-slot div that the bootstrap script will measure and render.

    Args:
        text: The text content to render.
        font: CSS font string, e.g. ``"64px 'Press Start 2P'"``.
        max_width: Maximum width in pixels for line breaking.
        line_height: Line height — values < 4 are treated as a multiplier
            of font size; values >= 4 are absolute pixels.
        css_class: Additional CSS classes for the container div.
        fill: SVG fill color. Defaults to ``currentColor`` to inherit
            from the parent CSS ``color`` property.
        text_anchor: SVG text-anchor (``start``, ``middle``, ``end``).

    Returns:
        HTML string for a pretext-slot element.
    """
    classes = f"pretext-slot {css_class}".strip()
    escaped_text = escape(text)
    return (
        f'<div class="{classes}"'
        f' data-pt-text="{escape(text, quote=True)}"'
        f' data-pt-font="{escape(font, quote=True)}"'
        f' data-pt-max-width="{max_width}"'
        f' data-pt-line-height="{line_height}"'
        f' data-pt-fill="{escape(fill, quote=True)}"'
        f' data-pt-text-anchor="{text_anchor}"'
        f'>{escaped_text}</div>'
    )


def svg_text_block(
    lines: list[str],
    font_family: str,
    font_size: float,
    line_height: float,
    fill: str = "currentColor",
    text_anchor: str = "start",
    max_width: Optional[float] = None,
) -> str:
    """Generate a static SVG text block from pre-measured lines.

    Use this when text layout has already been computed (e.g. cached
    measurements) and you want to emit SVG directly without the
    client-side bootstrap.

    Args:
        lines: List of text strings, one per line.
        font_family: Font family name (without size).
        font_size: Font size in pixels.
        line_height: Absolute line height in pixels.
        fill: SVG fill color.
        text_anchor: SVG text-anchor value.
        max_width: SVG viewBox width. Defaults to a generous estimate.

    Returns:
        Inline SVG markup string.
    """
    if not lines:
        return ""

    width = max_width or (len(max(lines, key=len)) * font_size * 0.6)
    total_height = len(lines) * line_height

    x_pos = (
        width / 2 if text_anchor == "middle"
        else width if text_anchor == "end"
        else 0
    )

    tspans = []
    for i, line_text in enumerate(lines):
        escaped = escape(line_text)
        if i == 0:
            tspans.append(
                f'<tspan x="{x_pos}" y="{font_size}">{escaped}</tspan>'
            )
        else:
            tspans.append(
                f'<tspan x="{x_pos}" dy="{line_height}">{escaped}</tspan>'
            )

    tspan_block = "\n      ".join(tspans)
    return (
        f'<svg width="{width}" height="{total_height}"'
        f' viewBox="0 0 {width} {total_height}"'
        f' style="display:block;overflow:visible">\n'
        f'  <text font-family="{escape(font_family, quote=True)}"'
        f' font-size="{font_size}" fill="{fill}"'
        f' text-anchor="{text_anchor}">\n'
        f'      {tspan_block}\n'
        f'  </text>\n'
        f'</svg>'
    )
