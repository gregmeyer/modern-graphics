"""Equation layout — renders a mathematical-style equation as the visual centerpiece.

Supports two text rendering modes:
- CSS (default): styled HTML spans with flex layout
- Pretext: SVG text elements measured by @chenglou/pretext

Designed for social graphics where the equation IS the content.
"""

from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING, Dict, List, Optional

from ..base import BaseGenerator

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_equation(equation: str) -> List[Dict[str, str]]:
    """Parse an equation string into a list of {type, value} tokens.

    Supports ``=``, ``+``, ``-``/``−``, ``×``, ``÷`` as operators.
    Everything else is a term.

    Example::

        >>> _parse_equation("Satisfaction = Perception − Expectation")
        [
            {"type": "term", "value": "Satisfaction"},
            {"type": "operator", "value": "="},
            {"type": "term", "value": "Perception"},
            {"type": "operator", "value": "−"},
            {"type": "term", "value": "Expectation"},
        ]
    """
    import re

    OPERATORS = {"=", "+", "-", "−", "×", "÷", "/"}
    # Normalize minus signs
    equation = equation.replace("—", "−").replace("–", "−")

    tokens: List[Dict[str, str]] = []
    # Split on operators but keep them
    parts = re.split(r'\s*([=+\-−×÷/])\s*', equation.strip())
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part in OPERATORS:
            # Normalize to proper unicode minus
            if part == "-":
                part = "−"
            tokens.append({"type": "operator", "value": part})
        else:
            tokens.append({"type": "term", "value": part})
    return tokens


# ---------------------------------------------------------------------------
# CSS rendering (default)
# ---------------------------------------------------------------------------

def _render_equation_css(
    tokens: List[Dict[str, str]],
    font_family: str,
    term_size: int,
    op_size: int,
    term_color: str,
    op_color: str,
    label_color: str,
) -> str:
    """Render the equation as stacked CSS flex lines."""
    lines: List[str] = []
    current_op = ""

    for token in tokens:
        if token["type"] == "operator":
            current_op = token["value"]
        else:
            term = escape(token["value"])
            if not lines:
                # First term — no operator, use spacer for alignment
                lines.append(
                    f'<div style="display:flex;align-items:baseline">'
                    f'<span style="min-width:{op_size + 12}px;padding-right:8px"></span>'
                    f'<span style="font-family:{font_family};font-size:{term_size}px;'
                    f'font-weight:700;font-style:italic;letter-spacing:-0.02em;'
                    f'color:{term_color};line-height:1.15">{term}</span>'
                    f'</div>'
                )
            else:
                lines.append(
                    f'<div style="display:flex;align-items:baseline">'
                    f'<span style="font-family:-apple-system,sans-serif;'
                    f'font-size:{op_size}px;font-weight:600;color:{op_color};'
                    f'min-width:{op_size + 12}px;text-align:left;line-height:1.15;'
                    f'padding-right:8px">{escape(current_op)}</span>'
                    f'<span style="font-family:{font_family};font-size:{term_size}px;'
                    f'font-weight:700;font-style:italic;letter-spacing:-0.02em;'
                    f'color:{term_color};line-height:1.15">{term}</span>'
                    f'</div>'
                )
                current_op = ""

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# SVG rendering (for pretext mode)
# ---------------------------------------------------------------------------

def _render_equation_svg(
    tokens: List[Dict[str, str]],
    font_family: str,
    term_size: int,
    op_size: int,
    term_color: str,
    op_color: str,
) -> str:
    """Render the equation as pretext-slot elements in a stacked layout."""
    from ..pretext_renderer import pretext_slot

    lines: List[str] = []
    current_op = ""

    for token in tokens:
        if token["type"] == "operator":
            current_op = token["value"]
        else:
            term = token["value"]
            if not lines:
                # First term — spacer + pretext slot
                slot = pretext_slot(
                    text=term,
                    font=f"italic bold {term_size}px {font_family}",
                    max_width=900,
                    line_height=1.15,
                    css_class="eq-term",
                    fill=term_color,
                )
                lines.append(
                    f'<div style="display:flex;align-items:baseline">'
                    f'<span style="min-width:{op_size + 12}px;padding-right:8px"></span>'
                    f'{slot}</div>'
                )
            else:
                slot = pretext_slot(
                    text=term,
                    font=f"italic bold {term_size}px {font_family}",
                    max_width=900,
                    line_height=1.15,
                    css_class="eq-term",
                    fill=term_color,
                )
                lines.append(
                    f'<div style="display:flex;align-items:baseline">'
                    f'<span style="font-family:-apple-system,sans-serif;'
                    f'font-size:{op_size}px;font-weight:600;color:{op_color};'
                    f'min-width:{op_size + 12}px;text-align:left;line-height:1.15;'
                    f'padding-right:8px">{escape(current_op)}</span>'
                    f'{slot}</div>'
                )
                current_op = ""

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_equation(
    generator: BaseGenerator,
    equation: str,
    label: Optional[str] = None,
    footnote: Optional[str] = None,
    color_scheme: Optional["ColorScheme"] = None,
    size: str = "large",
) -> str:
    """Generate an equation layout graphic.

    Args:
        equation: The equation string, e.g. ``"Satisfaction = Perception − Expectation"``.
            Operators ``=``, ``+``, ``-``/``−``, ``×``, ``÷`` are auto-detected.
        label: Optional small-caps label above the equation (e.g. ``"The Satisfaction Gap"``).
        footnote: Optional italic footnote below a thin rule (e.g. ``"The gap is where churn lives."``).
        color_scheme: Optional color scheme for theming.
        size: Term font size preset: ``"small"`` (64px), ``"medium"`` (84px), ``"large"`` (108px).
    """
    from ..diagrams.theme_utils import extract_theme_colors, _is_dark_color

    # Size presets
    sizes = {"small": (64, 48), "medium": (84, 64), "large": (108, 84)}
    term_size, op_size = sizes.get(size, sizes["large"])

    # Theme colors
    if color_scheme is not None:
        theme = extract_theme_colors(color_scheme)
        is_dark = theme.is_dark
        bg_primary = theme.page_bg
        bg_secondary = getattr(color_scheme, "bg_secondary", bg_primary)
        term_color = "#ffffff" if is_dark else "#1d1d1f"
        op_color = color_scheme.primary
        label_color = f"rgba(255,255,255,0.3)" if is_dark else "rgba(0,0,0,0.35)"
        footnote_color = f"rgba(255,255,255,0.25)" if is_dark else "rgba(0,0,0,0.3)"
        rule_color = f"rgba(255,255,255,0.12)" if is_dark else "rgba(0,0,0,0.08)"
        font_family = getattr(color_scheme, "font_family_display", None) or "'Playfair Display', Georgia, serif"
    else:
        is_dark = True
        bg_primary = "#1a2332"
        bg_secondary = "#0f1923"
        term_color = "#ffffff"
        op_color = "#60a5fa"
        label_color = "rgba(255,255,255,0.3)"
        footnote_color = "rgba(255,255,255,0.25)"
        rule_color = "rgba(255,255,255,0.12)"
        font_family = "'Playfair Display', Georgia, serif"

    tokens = _parse_equation(equation)

    # Choose rendering mode
    use_pretext = getattr(generator, "use_pretext", False)
    if use_pretext:
        equation_html = _render_equation_svg(
            tokens, font_family, term_size, op_size, term_color, op_color,
        )
    else:
        equation_html = _render_equation_css(
            tokens, font_family, term_size, op_size, term_color, op_color, label_color,
        )

    # Label
    label_html = ""
    if label:
        label_html = (
            f'<div style="font-size:13px;font-weight:700;letter-spacing:0.18em;'
            f'text-transform:uppercase;color:{label_color};margin-bottom:32px;'
            f'padding-left:4px;font-family:-apple-system,sans-serif">'
            f'{escape(label)}</div>'
        )

    # Footnote
    footnote_html = ""
    if footnote:
        footnote_html = (
            f'<div style="width:100%;height:1px;background:{rule_color};margin:28px 0"></div>'
            f'<div style="font-size:15px;font-weight:400;color:{footnote_color};'
            f'padding-left:4px;margin-top:4px;font-style:italic;'
            f'font-family:-apple-system,sans-serif">{escape(footnote)}</div>'
        )

    content = f"""
    <div data-mg-crop-root style="display:flex;flex-direction:column;justify-content:flex-start;
         padding:100px 72px 200px;font-family:-apple-system,sans-serif;min-height:100vh">
        {label_html}
        {equation_html}
        {footnote_html}
    </div>
    """

    css = f"""
        body {{
            margin: 0;
            background: linear-gradient(155deg, {bg_primary}, {bg_secondary});
            min-height: 100vh;
        }}
        .eq-term {{ color: {term_color}; }}
    """

    # Inject Google Fonts for Playfair Display
    google_font_link = ""
    if "Playfair" in font_family:
        google_font_link = (
            '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:'
            'ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">'
        )

    html = generator._wrap_html(content, css)

    # Inject extra Google Font if needed
    if google_font_link and google_font_link not in html:
        html = html.replace("</head>", f"    {google_font_link}\n</head>", 1)

    # Apply color scheme overrides
    if color_scheme is not None:
        html = color_scheme.apply_to_html(html)

    return html
