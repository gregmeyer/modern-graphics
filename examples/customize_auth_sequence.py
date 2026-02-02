#!/usr/bin/env python3
"""Demonstrate customizing the auth sequence diagram.

Uses the theme by default so the diagram gets your scheme's colors and font.
You can override the font with --font.

Run from utils/modern-graphics:

    PYTHONPATH=. python examples/customize_auth_sequence.py
    PYTHONPATH=. python examples/customize_auth_sequence.py --variant oauth
    PYTHONPATH=. python examples/customize_auth_sequence.py --theme apple --font "Georgia, serif"
    PYTHONPATH=. python examples/customize_auth_sequence.py --input my_sequence.mmd --output-dir output/my_auth

Output:
    examples/output/auth_custom/
        hero_auth_custom.html
        hero_auth_custom.png
        (optional) auth_sequence_custom.mmd
"""

import argparse
from pathlib import Path
from typing import List, Tuple

from modern_graphics import ModernGraphicsGenerator, Attribution, get_scheme, list_schemes
from modern_graphics.diagrams.modern_hero import generate_modern_hero
from modern_graphics.diagrams.mermaid_svg import mermaid_to_svg

EXAMPLES_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = EXAMPLES_DIR / "output" / "auth_custom"


def build_sequence_mermaid(
    participants: List[Tuple[str, str]],
    steps: List[Tuple[str, str, str, bool]],
    title_comment: str = "",
) -> str:
    """Build Mermaid sequenceDiagram source from config.

    participants: list of (short_id, display_label) e.g. [("U", "User"), ("A", "App")]
    steps: list of (from_id, to_id, message, solid) e.g. [("U", "A", "Login", True)]
          solid=True uses ->>, False uses -->>
    """
    lines = ["%% " + title_comment] if title_comment else []
    lines.append("sequenceDiagram")
    for pid, label in participants:
        lines.append(f'  participant {pid} as {label}')
    lines.append("")
    for from_id, to_id, msg, solid in steps:
        arrow = "->>" if solid else "-->>"
        lines.append(f'  {from_id}{arrow}{to_id}: {msg}')
    return "\n".join(lines)


# Predefined variants: (headline, subheadline, participants, steps)
AUTH_VARIANTS = {
    "login": {
        "headline": "How login works",
        "subheadline": "User, app, auth service, and session store.",
        "mermaid": build_sequence_mermaid(
            [
                ("U", "User"),
                ("A", "App"),
                ("Auth", "Auth Service"),
                ("DB", "Session Store"),
            ],
            [
                ("U", "A", "Login (email, password)", True),
                ("A", "Auth", "Validate credentials", True),
                ("Auth", "DB", "Lookup user", True),
                ("DB", "Auth", "User record", False),
                ("Auth", "A", "JWT + refresh token", False),
                ("A", "U", "Redirect to dashboard", False),
            ],
            "Customized login sequence (built from config)",
        ),
    },
    "oauth": {
        "headline": "OAuth2 authorization code flow",
        "subheadline": "User, app, identity provider, and API.",
        "mermaid": None,  # loaded from auth_sequence_oauth.mmd
    },
    "magic-link": {
        "headline": "Passwordless magic link",
        "subheadline": "User, app, and email service.",
        "mermaid": build_sequence_mermaid(
            [
                ("U", "User"),
                ("A", "App"),
                ("E", "Email Service"),
            ],
            [
                ("U", "A", "Enter email", True),
                ("A", "E", "Send magic link", True),
                ("E", "U", "Email with link", False),
                ("U", "A", "Click link (token)", True),
                ("A", "A", "Verify token, create session", True),
                ("A", "U", "Redirect to dashboard", False),
            ],
            "Magic link auth (built from config)",
        ),
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Customize auth sequence and render to hero card",
    )
    parser.add_argument(
        "--variant",
        choices=list(AUTH_VARIANTS),
        default="login",
        help="Use built-in variant: login, oauth (from .mmd), or magic-link",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Use this .mmd file instead of --variant",
    )
    parser.add_argument(
        "--theme",
        choices=list_schemes(),
        default="apple",
        help="Apply color theme to the diagram (default: apple)",
    )
    parser.add_argument(
        "--font",
        help='Font family for the Mermaid diagram (e.g. Roboto, "Georgia, serif")',
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Output directory for HTML/PNG",
    )
    parser.add_argument(
        "--save-mmd",
        action="store_true",
        help="Save the Mermaid source to a .mmd file in output-dir",
    )
    args = parser.parse_args()

    if args.input and args.input.exists():
        mermaid_source = args.input.read_text(encoding="utf-8")
        headline = "Authentication flow"
        subheadline = "Custom sequence from file."
    else:
        variant = AUTH_VARIANTS[args.variant]
        headline = variant["headline"]
        subheadline = variant["subheadline"]
        if variant["mermaid"] is not None:
            mermaid_source = variant["mermaid"]
        else:
            # oauth: load from .mmd
            oauth_mmd = EXAMPLES_DIR / "auth_sequence_oauth.mmd"
            if not oauth_mmd.exists():
                raise SystemExit(f"OAuth variant requires {oauth_mmd}")
            mermaid_source = oauth_mmd.read_text(encoding="utf-8")

    color_scheme = get_scheme(args.theme) if args.theme else None
    try:
        svg_content = mermaid_to_svg(
            mermaid_source,
            color_scheme=color_scheme,
            font_family=getattr(args, 'font', None),
        )
    except RuntimeError as e:
        raise SystemExit(f"{e}\nInstall mermaid-cli: npx @mermaid-js/mermaid-cli")

    generator = ModernGraphicsGenerator(
        title="Auth sequence",
        attribution=Attribution(copyright="© Demo 2025"),
    )
    html = generate_modern_hero(
        generator,
        headline=headline,
        subheadline=subheadline,
        freeform_canvas=svg_content,
        background_variant="light",
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    path_html = args.output_dir / "hero_auth_custom.html"
    path_png = args.output_dir / "hero_auth_custom.png"
    generator.save(html, path_html)
    generator.export_to_png(html, path_png, viewport_width=1200, viewport_height=700, padding=24)
    print(f"Saved: {path_html}")
    print(f"Saved: {path_png}")

    if args.save_mmd:
        path_mmd = args.output_dir / "auth_sequence_custom.mmd"
        path_mmd.write_text(mermaid_source, encoding="utf-8")
        print(f"Saved: {path_mmd}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
