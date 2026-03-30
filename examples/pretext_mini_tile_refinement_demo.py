#!/usr/bin/env python3
"""Generate side-by-side HTML: legacy vs refined story mini-tile Pretext foreignObject bands.

 Open the output file in a browser (network needed for Pretext CDN and fonts).

 Run from repo root:

    python3 examples/pretext_mini_tile_refinement_demo.py

 Or with PYTHONPATH if needed:

    PYTHONPATH=. python3 examples/pretext_mini_tile_refinement_demo.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.story_slide import _build_static_mini_tile

OUT = REPO_ROOT / "output" / "pretext-mini-tile-refinement-demo.html"

_PALETTE = {
    "background": "#FFFFFF",
    "border": "#E5E5E5",
    "text_primary": "#111111",
    "text_secondary": "#555555",
    "metric_bg": "#F0F4F8",
    "metric_text": "#111111",
    "accent_primary": "#0071E3",
}

_DATA = {
    "tile_headline": "Revenue acceleration outpaced linear forecast",
    "subline": "Pipeline quality improved as cycle times compressed across regions.",
    "pill": "FY 2025",
    "metric": "Decision quality drives outcomes",
    "chart": [72, 98, 68, 105],
}


def main() -> None:
    gen = ModernGraphicsGenerator(
        "Pretext mini-tile refinement demo",
        Attribution(copyright="© Demo", show=False),
        use_pretext=True,
    )
    left = _build_static_mini_tile(
        640,
        400,
        _PALETTE,
        _DATA,
        use_pretext=True,
        pretext_foreign_object_layout="legacy",
    )
    right = _build_static_mini_tile(
        640,
        400,
        _PALETTE,
        _DATA,
        use_pretext=True,
        pretext_foreign_object_layout="refined",
    )
    body = f"""
    <div class="page">
      <h1>Mini-tile Pretext: legacy vs refined <code>foreignObject</code></h1>
      <p class="lede">Same headline and subline. Left: pre-refinement band heights (44px / 36px) with Pretext—multi-line SVG text is clipped. Right: reserved bands (88px / 52px) with the chart and pill shifted down.</p>
      <div class="row">
        <figure>
          <figcaption>Legacy bands (clips)</figcaption>
          <div class="tile-wrap">{left}</div>
        </figure>
        <figure>
          <figcaption>Refined (current default)</figcaption>
          <div class="tile-wrap">{right}</div>
        </figure>
      </div>
    </div>
    """
    css = """
    * { box-sizing: border-box; }
    body { font-family: system-ui, sans-serif; margin: 0; padding: 32px 48px;
           background: #f4f4f5; color: #18181b; }
    .page { max-width: 1400px; margin: 0 auto; }
    h1 { font-size: 1.35rem; font-weight: 650; margin: 0 0 12px; }
    .lede { max-width: 72ch; line-height: 1.5; color: #52525b; margin: 0 0 28px; }
    .row { display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start; }
    figure { margin: 0; flex: 1 1 420px; background: #fff; padding: 20px;
             border-radius: 16px; border: 1px solid #e4e4e7; }
    figcaption { font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
                 letter-spacing: 0.06em; color: #71717a; margin-bottom: 12px; }
    .tile-wrap { max-width: 100%; }
    .tile-wrap svg { width: 100%; height: auto; display: block; }
    code { font-size: 0.9em; }
    """
    html = gen._wrap_html(body, css)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")
    print("Open in a browser (network for Pretext CDN + Google Fonts).")


if __name__ == "__main__":
    main()
