"""SVG composition of transaction icons and labels (e.g. credit card transaction).

Use as custom_mockup (slide card), svg_content (insight card), or as a scene
element via ELEMENT_REGISTRY (type "transaction").
"""

from typing import Any, Dict, Optional

# Default colors when not from WireframeConfig
_DEFAULT_ACCENT = "#0071e3"
_DEFAULT_TEXT_PRIMARY = "#1d1d1f"
_DEFAULT_TEXT_SECONDARY = "#6e6e73"
_DEFAULT_SURFACE = "#f5f5f7"
_DEFAULT_BORDER = "#e8e8ed"


def _render_transaction_content(
    width: int,
    height: int,
    merchant: str,
    amount: str,
    date: str,
    accent: str,
    text_primary: str,
    text_secondary: str,
    surface: str,
    border: str,
    origin_x: float = 0,
    origin_y: float = 0,
) -> str:
    """Render transaction rect + card + rows at origin (origin_x, origin_y). Returns fragment only (no outer svg)."""
    pad = 20
    row_h = 44
    icon_size = 24
    icon_gap = 12
    font = "Inter, SF Pro Display, -apple-system, sans-serif"

    def card_icon(x: float, y: float) -> str:
        cx, cy = x + icon_size / 2, y + icon_size / 2
        w, h = 20, 14
        return f'<rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="2" fill="none" stroke="{accent}" stroke-width="1.5"/><rect x="{cx - w/2}" y="{cy - h/2}" width="6" height="{h}" rx="2" fill="{accent}" opacity="0.3"/>'

    def store_icon(x: float, y: float) -> str:
        cx, cy = x + icon_size / 2, y + icon_size / 2
        return f'<path d="M{cx-8},{cy+2} L{cx},{cy-6} L{cx+8},{cy+2} Z" fill="none" stroke="{text_secondary}" stroke-width="1.5"/><rect x="{cx-3}" y="{cy}" width="6" height="8" rx="1" fill="none" stroke="{text_secondary}" stroke-width="1.5"/>'

    def dollar_icon(x: float, y: float) -> str:
        cx, cy = x + icon_size / 2, y + icon_size / 2
        return f'<path d="M{cx} {cy-8} v16 M{cx-4} {cy-6} q4-2 4 2 0 4-4 6 M{cx+4} {cy+2} q-4 2-4-2 0-4 4-6" fill="none" stroke="{accent}" stroke-width="1.5" stroke-linecap="round"/>'

    def calendar_icon(x: float, y: float) -> str:
        cx, cy = x + icon_size / 2, y + icon_size / 2
        return f'<rect x="{cx-8}" y="{cy-6}" width="16" height="14" rx="2" fill="none" stroke="{text_secondary}" stroke-width="1.5"/><line x1="{cx-8}" y1="{cy-10}" x2="{cx-8}" y2="{cy-4}" stroke="{text_secondary}" stroke-width="1.5"/><line x1="{cx+8}" y1="{cy-10}" x2="{cx+8}" y2="{cy-4}" stroke="{text_secondary}" stroke-width="1.5"/>'

    card_w = 100
    card_h = 64
    card_x = origin_x + pad
    card_y = origin_y + (height - card_h) / 2
    card_svg = f'''
    <g class="transaction-card">
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="8" fill="{surface}" stroke="{border}" stroke-width="1"/>
      <rect x="{card_x}" y="{card_y}" width="{card_w}" height="14" rx="8" fill="{accent}" opacity="0.4"/>
      <rect x="{card_x+12}" y="{card_y+36}" width="40" height="6" rx="3" fill="{border}"/>
      <text x="{card_x+card_w/2}" y="{card_y+54}" font-family="{font}" font-size="9" fill="{text_secondary}" text-anchor="middle">•••• 4242</text>
    </g>'''

    start_x = origin_x + pad + card_w + pad
    start_y = origin_y + (height - 3 * row_h) / 2 + row_h / 2

    def row(icon_fn, label: str, value: str, row_index: int) -> str:
        y = start_y + row_index * row_h
        ix = start_x
        iy = y - icon_size / 2
        icon = icon_fn(ix, iy)
        tx = start_x + icon_size + icon_gap
        end_x = origin_x + width - pad
        return f'''<g class="transaction-row">
          {icon}
          <text x="{tx}" y="{y + 4}" font-family="{font}" font-size="11" font-weight="500" fill="{text_secondary}">{label}</text>
          <text x="{end_x}" y="{y + 4}" font-family="{font}" font-size="12" font-weight="600" fill="{text_primary}" text-anchor="end">{value}</text>
        </g>'''

    rows_svg = row(store_icon, "Merchant", merchant, 0) + row(dollar_icon, "Amount", amount, 1) + row(calendar_icon, "Date", date, 2)
    bg = f'<rect x="{origin_x}" y="{origin_y}" width="{width}" height="{height}" rx="12" fill="{surface}"/>'
    return f"{bg}\n  {card_svg}\n  {rows_svg}"


def render_transaction_svg(
    width: int = 360,
    height: int = 200,
    merchant: str = "Coffee Shop",
    amount: str = "$4.50",
    date: str = "Today",
    accent: str = _DEFAULT_ACCENT,
    text_primary: str = _DEFAULT_TEXT_PRIMARY,
    text_secondary: str = _DEFAULT_TEXT_SECONDARY,
    surface: str = _DEFAULT_SURFACE,
    border: str = _DEFAULT_BORDER,
) -> str:
    """Render a full SVG (viewBox) for a credit-card-style transaction with icons and labels.

    Use for standalone export, custom_mockup, or svg_content. For scene composition
    use the \"transaction\" element type (ELEMENT_REGISTRY) which calls render_transaction_at.
    """
    content = _render_transaction_content(
        width, height, merchant, amount, date,
        accent, text_primary, text_secondary, surface, border,
        origin_x=0, origin_y=0,
    )
    return f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n  {content}\n</svg>'


def render_transaction_at(
    x: float,
    y: float,
    width: int = 360,
    height: int = 200,
    merchant: str = "Coffee Shop",
    amount: str = "$4.50",
    date: str = "Today",
    accent: Optional[str] = None,
    text_primary: Optional[str] = None,
    text_secondary: Optional[str] = None,
    surface: Optional[str] = None,
    border: Optional[str] = None,
) -> str:
    """Render transaction content at (x, y) as a <g> fragment for scene composition.

    Used by wireframe_scene ELEMENT_REGISTRY when type is \"transaction\".
    """
    content = _render_transaction_content(
        width,
        height,
        merchant,
        amount,
        date,
        accent or _DEFAULT_ACCENT,
        text_primary or _DEFAULT_TEXT_PRIMARY,
        text_secondary or _DEFAULT_TEXT_SECONDARY,
        surface or _DEFAULT_SURFACE,
        border or _DEFAULT_BORDER,
        origin_x=0,
        origin_y=0,
    )
    return f'<g class="transaction-element" transform="translate({x},{y})">\n  {content}\n</g>'
