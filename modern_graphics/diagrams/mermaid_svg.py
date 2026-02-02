"""Convert Mermaid diagram source to SVG for use in cards or hero.

Once you have SVG (from this helper or from Mermaid Live / mermaid-cli),
pass it to:
- Slide card: card dict with custom_mockup=svg_string
- Insight card: generate_insight_card(..., svg_content=svg_string)
- Modern hero: generate_modern_hero(..., freeform_canvas=svg_string)

Theme: pass color_scheme to apply themeVariables (Mermaid base theme) so the
diagram uses your scheme's colors and font.

Mermaid emits inline stroke="none" on sequence message lines, which hides the
horizontal connector (only arrowheads show). Injected themeCSS does not override
inline attributes in the rendered SVG, so we post-process the SVG and replace
stroke="none" with the theme stroke on messageLine0/messageLine1 elements.
"""

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme

MERMAID_CLI_MSG = (
    "Mermaid CLI not available. Install with: npm install -g @mermaid-js/mermaid-cli "
    "or use npx: npx @mermaid-js/mermaid-cli. Alternatively, render your diagram at "
    "https://mermaid.live and pass the SVG string or file content."
)

# Restore dotted/dashed connectors when using base theme (sequence: messageLine1; flowcharts: edge-pattern-dashed).
THEME_CSS_DASHED_EDGES = (
    ".messageLine1{stroke-dasharray:5 5 !important} "
    ".edge-pattern-dashed{stroke-dasharray:5 5 !important} "
    ".sequence .edge-pattern-dashed{stroke-dasharray:5 5 !important}"
)


def _flowchart_label_css(text_color: str) -> str:
    """CSS so flowchart node/edge labels (inside foreignObject) use explicit color and are visible."""
    return (
        f".nodeLabel,.edgeLabel,.nodeLabel p,.edgeLabel p,.label .nodeLabel,.label .edgeLabel"
        f"{{color:{text_color} !important;fill:{text_color} !important;}} "
        f"foreignObject div{{color:{text_color} !important;}}"
    )


def _fix_message_line_strokes(svg: str, stroke_color: str) -> str:
    """Replace stroke=\"none\" with stroke_color on sequence message line/path elements.

    Mermaid outputs inline stroke=\"none\" on these elements; CSS cannot override
    it reliably, so we fix the SVG markup directly.
    """
    def replace_in_tag(m: re.Match) -> str:
        tag, attrs = m.group(1), m.group(2)
        if ("messageLine0" not in attrs and "messageLine1" not in attrs) or "stroke=\"none\"" not in attrs:
            return m.group(0)
        fixed = attrs.replace("stroke=\"none\"", f"stroke=\"{stroke_color}\"", 1)
        return f"<{tag}{fixed}>"

    return re.sub(r"<(line|path)([^>]*?)>", replace_in_tag, svg, flags=re.DOTALL)


def _label_color_for_contrast(text_primary: str) -> str:
    """Return a label color that contrasts with light node backgrounds (flowchart/Sankey).

    If theme text is light (e.g. for dark themes), use dark so labels are readable on
    light-filled nodes; otherwise use the theme text color.
    """
    if _hex_luminance(text_primary) >= 0.5:
        return "#1d1d1f"
    return text_primary


def _fix_svg_label_visibility(svg: str, text_color: str) -> str:
    """Make diagram labels visible: fix text/tspan fill=\"none\" and foreignObject div color.

    Mermaid sometimes outputs fill=\"none\" on <text>/<tspan> (e.g. Sankey) and flowchart
    labels live in foreignObject; inline styles ensure they show and have good contrast.
    """
    # Fix <text> and <tspan> that have fill="none"
    def fix_text_fill(m: re.Match) -> str:
        tag, attrs = m.group(1), m.group(2)
        if "fill=\"none\"" not in attrs:
            return m.group(0)
        fixed = attrs.replace("fill=\"none\"", f"fill=\"{text_color}\"", 1)
        return f"<{tag}{fixed}>"

    svg = re.sub(r"<(text|tspan)([^>]*?)>", fix_text_fill, svg, flags=re.DOTALL)

    # Ensure first <div> inside each <foreignObject> has inline color for contrast
    style_attr = f" style=\"color:{text_color};fill:{text_color};\""
    def add_foreign_div_style(m: re.Match) -> str:
        prefix, div_attrs = m.group(1), m.group(2)
        if "style=" in div_attrs and "color:" in div_attrs:
            return m.group(0)
        if "style=" in div_attrs:
            div_attrs = re.sub(
                r'style="([^"]*)"',
                f'style="\\1;color:{text_color};fill:{text_color};"',
                div_attrs,
                count=1,
            )
        else:
            div_attrs = div_attrs.rstrip() + style_attr
        return prefix + div_attrs + ">"

    svg = re.sub(
        r"(<foreignObject[^>]*>\s*<div)([^>]*)>",
        add_foreign_div_style,
        svg,
    )
    return svg


def _hex_luminance(hex_color: str) -> float:
    """Relative luminance (0 dark, 1 light). Handles #rgb and #rrggbb."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return 0.299 * r + 0.587 * g + 0.114 * b


def _scheme_to_mermaid_config(
    scheme: "ColorScheme",
    font_family_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Build Mermaid config (theme base + themeVariables) from a ColorScheme.

    Mermaid only allows custom themeVariables when theme is "base".
    font_family_override: if set, overrides scheme.font_family for the diagram font.
    """
    bg = scheme.bg_primary
    primary = scheme.primary
    text_primary = scheme.text_primary
    border = scheme.border_medium
    dark_mode = _hex_luminance(bg) < 0.4
    primary_text = "#ffffff" if _hex_luminance(primary) < 0.5 else text_primary
    font = (
        (font_family_override or getattr(scheme, "font_family_display", None) or scheme.font_family or "").strip("'\"")
        or "Inter, sans-serif"
    )

    return {
        "theme": "base",
        "themeVariables": {
            "darkMode": dark_mode,
            "background": bg,
            "primaryColor": primary,
            "primaryTextColor": primary_text,
            "primaryBorderColor": primary,
            "secondaryColor": scheme.bg_secondary,
            "secondaryTextColor": text_primary,
            "secondaryBorderColor": border,
            "tertiaryColor": scheme.bg_tertiary,
            "tertiaryTextColor": text_primary,
            "tertiaryBorderColor": border,
            "lineColor": border,
            "textColor": text_primary,
            "mainBkg": scheme.bg_secondary,
            "fontFamily": font,
            "fontSize": "16px",
            "noteBkgColor": scheme.bg_tertiary,
            "noteTextColor": text_primary,
            "actorBkg": scheme.bg_secondary,
            "actorBorder": border,
            "actorTextColor": text_primary,
            "signalColor": text_primary,
            "signalTextColor": text_primary,
        },
        "themeCSS": THEME_CSS_DASHED_EDGES
        + " "
        + _flowchart_label_css(_label_color_for_contrast(text_primary))
        + (" " + (getattr(scheme, "mermaid_flowchart_extra_css", None) or "")),
        "flowchart": {"htmlLabels": False, "useMaxWidth": True},
    }


def _font_only_mermaid_config(font_family: str) -> Dict[str, Any]:
    """Minimal Mermaid config (theme base) with only fontFamily set.

    Use when you want to customize only the diagram font, no theme.
    """
    font = font_family.strip("'\"") if font_family else "Inter, sans-serif"
    return {
        "theme": "base",
        "themeVariables": {
            "fontFamily": font,
            "fontSize": "16px",
        },
        "themeCSS": THEME_CSS_DASHED_EDGES + " " + _flowchart_label_css("#333333"),
        "flowchart": {"htmlLabels": False, "useMaxWidth": True},
    }


def mermaid_to_svg(
    mermaid_source: str,
    mmdc_path: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    color_scheme: Optional["ColorScheme"] = None,
    font_family: Optional[str] = None,
) -> str:
    """Convert Mermaid diagram source to an SVG string.

    Requires @mermaid-js/mermaid-cli (mmdc) on PATH or via npx. If mmdc is not
    found, raises RuntimeError with install instructions.

    Args:
        mermaid_source: Mermaid diagram text (e.g. "flowchart LR\\n  A --> B").
        mmdc_path: Optional path to mmdc executable; if None, uses npx.
        width: Optional SVG width (mmdc -w).
        height: Optional SVG height (mmdc -H).
        color_scheme: Optional ColorScheme; if set, applies themeVariables (base theme)
            so the diagram uses the scheme's colors and font.
        font_family: Optional font for the diagram (e.g. "Roboto", "Georgia, serif").
            Overrides the theme font when color_scheme is set; when no theme, only
            the font is applied via a minimal config.

    Returns:
        SVG document as a string.

    Raises:
        RuntimeError: If mmdc is not available or returns an error.
    """
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".mmd",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(mermaid_source)
        mmd_path = f.name
    out_path = mmd_path + ".svg"
    config_path = mmd_path + ".config.json"
    try:
        cmd = []
        if mmdc_path:
            cmd = [mmdc_path]
        else:
            cmd = ["npx", "-y", "@mermaid-js/mermaid-cli"]
        cmd.extend(["-i", mmd_path, "-o", out_path, "-b", "transparent"])
        if width is not None:
            cmd.extend(["-w", str(width)])
        if height is not None:
            cmd.extend(["-H", str(height)])
        if color_scheme is not None:
            config = _scheme_to_mermaid_config(
                color_scheme, font_family_override=font_family
            )
            Path(config_path).write_text(json.dumps(config), encoding="utf-8")
            cmd.extend(["-c", config_path])
        elif font_family is not None:
            config = _font_only_mermaid_config(font_family)
            Path(config_path).write_text(json.dumps(config), encoding="utf-8")
            cmd.extend(["-c", config_path])
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            try:
                Path(mmd_path).unlink(missing_ok=True)
                Path(out_path).unlink(missing_ok=True)
                Path(config_path).unlink(missing_ok=True)
            except OSError:
                pass
            raise RuntimeError(
                f"mmdc failed: {result.stderr or result.stdout or 'unknown'}. {MERMAID_CLI_MSG}"
            )
        svg = Path(out_path).read_text(encoding="utf-8")
        if color_scheme is not None:
            stroke_color = color_scheme.text_primary
            label_color = _label_color_for_contrast(stroke_color)
            svg = _fix_message_line_strokes(svg, stroke_color)
        else:
            label_color = "#1d1d1f"
            if font_family is not None:
                svg = _fix_message_line_strokes(svg, "#333333")
        svg = _fix_svg_label_visibility(svg, label_color)
        return svg
    except FileNotFoundError:
        try:
            Path(mmd_path).unlink(missing_ok=True)
        except OSError:
            pass
        raise RuntimeError(MERMAID_CLI_MSG)
    finally:
        try:
            Path(mmd_path).unlink(missing_ok=True)
            Path(out_path).unlink(missing_ok=True)
            Path(config_path).unlink(missing_ok=True)
        except OSError:
            pass
