"""Cohort retention heatmap (Mixpanel/Amplitude-style).

Each row is a cohort (by start date). Each column is a period offset from
that start date (week 0, 1, 2, ...). Cell color encodes the retention
percentage using an opacity ramp on the theme accent color.

Example input::

    cohorts = [
        {"date": "Sep 17", "size": 7262, "values": [95.6, 33.5, 31.3, 29.0]},
        {"date": "Sep 24", "size": 7187, "values": [95.6, 33.7, 30.5]},
        ...
    ]

Short rows (ragged) are allowed — cells without data render as empty.
"""

from __future__ import annotations

from html import escape
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING

from ..base import BaseGenerator
from .theme_utils import (
    extract_theme_colors,
    generate_css_variables,
    inject_google_fonts,
    with_alpha,
)

if TYPE_CHECKING:
    from ..color_scheme import ColorScheme


def _format_value(v: float) -> str:
    return f"{v:.2f}%"


def _cell_color(accent: str, value: float) -> str:
    """Opacity ramp: 0% → very faint, 100% → full accent."""
    pct = max(0.0, min(100.0, float(value))) / 100.0
    # Avoid invisible cells for small values; clamp alpha to [0.08, 1.0].
    alpha = 0.08 + pct * 0.92
    return with_alpha(accent, alpha)


def _is_low_contrast(value: float) -> bool:
    """Below this threshold, text is dark on a light cell; otherwise white on accent."""
    return value < 50.0


def generate_cohort_chart(
    generator: BaseGenerator,
    cohorts: Sequence[Dict[str, Any]],
    period_labels: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    date_label: str = "Date",
    size_label: str = "People",
    color_scheme: Optional["ColorScheme"] = None,
) -> str:
    """Render a cohort retention heatmap.

    Args:
        cohorts: list of {"date": str, "size": int, "values": list[float]}
        period_labels: optional column headers. If omitted, defaults to
            ["< 1 wk", "1", "2", ...] sized to the longest cohort row.
        title, subtitle: optional headline text above the table.
        date_label, size_label: header text for the first two columns.
        color_scheme: optional theme.
    """
    theme = extract_theme_colors(color_scheme)
    cohort_list = list(cohorts)
    max_cols = max((len(c.get("values", [])) for c in cohort_list), default=0)

    if period_labels is None:
        period_labels = ["< 1 wk"] + [str(i) for i in range(1, max_cols)]
    period_labels = list(period_labels)[:max_cols]

    # Header row
    header_cells = "".join(
        f'<th class="period-col">{escape(str(lbl))}</th>' for lbl in period_labels
    )

    # Body rows
    rows_html: List[str] = []
    for cohort in cohort_list:
        date = escape(str(cohort.get("date", "")))
        size = cohort.get("size", "")
        size_str = f"{int(size):,}" if isinstance(size, (int, float)) else escape(str(size))
        values = list(cohort.get("values", []))

        cells: List[str] = []
        for i in range(max_cols):
            if i < len(values) and values[i] is not None:
                v = float(values[i])
                bg = _cell_color(theme.accent, v)
                is_low = _is_low_contrast(v)
                text_color = theme.text_primary if is_low else "#ffffff"
                cls = "cell filled" + (" muted" if is_low else "")
                cells.append(
                    f'<td class="{cls}" style="background:{bg};color:{text_color};">'
                    f'{_format_value(v)}</td>'
                )
            else:
                cells.append('<td class="cell empty"></td>')
        rows_html.append(
            f'<tr><td class="date">{date}</td>'
            f'<td class="size">{size_str}</td>'
            f'{"".join(cells)}</tr>'
        )

    title_html = ""
    if title:
        title_html += f'<h1 class="cohort-title">{escape(title)}</h1>'
    if subtitle:
        title_html += f'<p class="cohort-subtitle">{escape(subtitle)}</p>'

    content = f"""
    <div class="cohort-wrapper" data-mg-crop-root>
      {title_html}
      <table class="cohort-table">
        <thead>
          <tr>
            <th class="date-col">{escape(date_label)}</th>
            <th class="size-col">{escape(size_label)}</th>
            {header_cells}
          </tr>
        </thead>
        <tbody>
          {''.join(rows_html)}
        </tbody>
      </table>
    </div>
    """

    css_vars = generate_css_variables(theme)
    grid_color = with_alpha(theme.text_primary, 0.08)
    css = f"""
    {css_vars}
    body {{
      background: var(--bg-page);
      padding: 48px;
      min-height: 100vh;
    }}
    .cohort-wrapper {{
      background: var(--bg-card);
      border-radius: 20px;
      padding: 40px 48px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 12px 40px rgba(0,0,0,0.06);
      max-width: max-content;
      margin: 0 auto;
    }}
    .cohort-title {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-1);
      margin-bottom: 4px;
    }}
    .cohort-subtitle {{
      font-family: var(--font-body);
      font-size: 16px;
      color: var(--text-2);
      margin-bottom: 24px;
    }}
    .cohort-table {{
      border-collapse: separate;
      border-spacing: 2px;
      font-family: var(--font-body);
      font-size: 14px;
    }}
    .cohort-table th {{
      font-weight: 600;
      color: var(--text-2);
      text-align: center;
      padding: 10px 14px;
      font-size: 13px;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }}
    .cohort-table th.date-col, .cohort-table th.size-col {{
      text-align: left;
    }}
    .cohort-table td {{
      padding: 12px 14px;
      text-align: center;
      font-variant-numeric: tabular-nums;
      font-weight: 500;
      border-radius: 4px;
      min-width: 64px;
    }}
    .cohort-table td.date {{
      color: var(--text-1);
      font-weight: 500;
      white-space: nowrap;
      text-align: left;
      padding-right: 20px;
    }}
    .cohort-table td.size {{
      color: var(--text-2);
      text-align: right;
      padding-right: 20px;
    }}
    .cohort-table td.cell.filled {{
      color: #fff;
      font-weight: 600;
    }}
    .cohort-table td.cell.filled.muted {{
      font-weight: 500;
    }}
    .cohort-table td.cell.empty {{
      background: transparent;
      border: 1px dashed {grid_color};
    }}
    """

    html = generator._wrap_html(content, css)
    html = inject_google_fonts(html, theme)
    return html
