#!/usr/bin/env python3
"""Demo: Mermaid diagram → SVG → card and hero.

Shows that any Mermaid diagram can be rendered to SVG and then placed in:
- an insight card (svg_content)
- a modern hero (freeform_canvas)

Requires @mermaid-js/mermaid-cli (npm install -g @mermaid-js/mermaid-cli or npx).
If mmdc is not available, run with --svg-file path/to/pre-rendered.svg instead.

Run from utils/modern-graphics:
    PYTHONPATH=. python examples/mermaid_card_hero_demo.py
    PYTHONPATH=. python examples/mermaid_card_hero_demo.py --svg-file my.svg

Output:
    examples/output/mermaid_demo/
        mermaid_insight_card.html / .png
        mermaid_hero.html / .png
"""

import argparse
from pathlib import Path

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams import generate_insight_card
from modern_graphics.diagrams.modern_hero import generate_modern_hero

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "mermaid_demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MERMAID_SAMPLE = """
flowchart LR
  A[Request] --> B[Validate]
  B --> C[Process]
  C --> D[Response]
"""


def main():
    from modern_graphics import get_scheme, list_schemes

    parser = argparse.ArgumentParser(description="Mermaid → SVG → card and hero demo")
    parser.add_argument(
        "--svg-file",
        type=Path,
        help="Use this pre-rendered SVG file instead of calling mermaid-cli",
    )
    parser.add_argument(
        "--theme",
        choices=list_schemes(),
        help="Apply color theme to the Mermaid diagram (when rendering from source)",
    )
    args = parser.parse_args()

    if args.svg_file and args.svg_file.exists():
        svg_content = args.svg_file.read_text(encoding="utf-8")
        print(f"Using pre-rendered SVG from {args.svg_file}")
    else:
        try:
            from modern_graphics.diagrams.mermaid_svg import mermaid_to_svg
            color_scheme = get_scheme(args.theme) if args.theme else None
            svg_content = mermaid_to_svg(MERMAID_SAMPLE, color_scheme=color_scheme)
            print("Rendered Mermaid to SVG via mermaid-cli" + (" (theme: %s)" % args.theme if args.theme else ""))
        except RuntimeError as e:
            print(e)
            print("\nTo run without mermaid-cli, render your diagram at https://mermaid.live,")
            print("save as SVG, then: python examples/mermaid_card_hero_demo.py --svg-file your.svg")
            return 1

    generator = ModernGraphicsGenerator(
        title="Mermaid in card and hero",
        attribution=Attribution(copyright="© Demo 2025"),
    )

    # 1. Insight card with Mermaid SVG
    print("Generating insight card with Mermaid SVG...")
    html_card = generate_insight_card(
        generator,
        text="Mermaid diagrams can be rendered to SVG and dropped into cards or heroes.",
        svg_content=svg_content,
        label="Key Insight",
        svg_label="Flow",
    )
    path_card_html = OUTPUT_DIR / "mermaid_insight_card.html"
    path_card_png = OUTPUT_DIR / "mermaid_insight_card.png"
    generator.save(html_card, path_card_html)
    generator.export_to_png(html_card, path_card_png, viewport_width=1000, viewport_height=500, padding=20)
    print(f"  {path_card_html.name}, {path_card_png.name}")

    # 2. Modern hero with Mermaid SVG in freeform_canvas
    print("Generating modern hero with Mermaid SVG...")
    html_hero = generate_modern_hero(
        generator,
        headline="Mermaid in the hero",
        subheadline="Any diagram rendered to SVG can go in the hero body.",
        freeform_canvas=svg_content,
        background_variant="light",
    )
    path_hero_html = OUTPUT_DIR / "mermaid_hero.html"
    path_hero_png = OUTPUT_DIR / "mermaid_hero.png"
    generator.save(html_hero, path_hero_html)
    generator.export_to_png(html_hero, path_hero_png, viewport_width=1200, viewport_height=700, padding=20)
    print(f"  {path_hero_html.name}, {path_hero_png.name}")

    print(f"\nDone. Output in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
