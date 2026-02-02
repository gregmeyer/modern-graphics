#!/usr/bin/env python3
"""Generate a hero card with an authentication sequence diagram.

Uses the Mermaid sequence diagram in auth_sequence.mmd (User → App → Auth Service
→ Session Store) and renders it into the hero body via freeform_canvas.

Requires mermaid-cli (npx @mermaid-js/mermaid-cli). Run from utils/modern-graphics:

    PYTHONPATH=. python examples/hero_auth_sequence.py
    PYTHONPATH=. python examples/hero_auth_sequence.py --theme apple

Output:
    examples/output/auth_hero/
        hero_auth_sequence.html
        hero_auth_sequence.png
"""

import argparse
from pathlib import Path

from modern_graphics import ModernGraphicsGenerator, Attribution, get_scheme, list_schemes
from modern_graphics.diagrams.modern_hero import generate_modern_hero
from modern_graphics.diagrams.mermaid_svg import mermaid_to_svg

EXAMPLES_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = EXAMPLES_DIR / "output" / "auth_hero"
AUTH_MMD = EXAMPLES_DIR / "auth_sequence.mmd"


def main():
    parser = argparse.ArgumentParser(description="Hero with auth sequence diagram")
    parser.add_argument("--theme", choices=list_schemes(), help="Apply color theme to the Mermaid diagram")
    args = parser.parse_args()

    if not AUTH_MMD.exists():
        raise SystemExit(f"Mermaid file not found: {AUTH_MMD}")

    color_scheme = get_scheme(args.theme) if args.theme else None
    try:
        mermaid_source = AUTH_MMD.read_text(encoding="utf-8")
        svg_content = mermaid_to_svg(mermaid_source, color_scheme=color_scheme)
    except RuntimeError as e:
        raise SystemExit(
            f"{e}\nInstall mermaid-cli: npm install -g @mermaid-js/mermaid-cli (or use npx)."
        )

    generator = ModernGraphicsGenerator(
        title="Authentication flow",
        attribution=Attribution(copyright="© Demo 2025"),
    )
    html = generate_modern_hero(
        generator,
        headline="How login works",
        subheadline="User, app, and auth service in one flow.",
        freeform_canvas=svg_content,
        background_variant="light",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path_html = OUTPUT_DIR / "hero_auth_sequence.html"
    path_png = OUTPUT_DIR / "hero_auth_sequence.png"
    generator.save(html, path_html)
    generator.export_to_png(html, path_png, viewport_width=1200, viewport_height=700, padding=24)
    print(f"Saved: {path_html}")
    print(f"Saved: {path_png}")


if __name__ == "__main__":
    main()
