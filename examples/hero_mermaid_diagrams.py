#!/usr/bin/env python3
"""Generate hero cards with Mermaid or wireframe diagram types.

Renders flowchart, Sankey, sequence (Mermaid), or post-it flow layouts (wireframe)
into a hero freeform_canvas with optional theme. All diagram types output both
HTML and PNG.

Requires mermaid-cli for Mermaid diagrams. Run from utils/modern-graphics:

    PYTHONPATH=. python examples/hero_mermaid_diagrams.py --diagram flowchart
    PYTHONPATH=. python examples/hero_mermaid_diagrams.py --diagram postit_flow --theme corporate
    PYTHONPATH=. python examples/hero_mermaid_diagrams.py --diagram postit_flow_zigzag --png
    PYTHONPATH=. python examples/hero_mermaid_diagrams.py --diagram sankey --theme apple

Flow styles (postit_flow*, wireframe): postit_flow, postit_flow_zigzag,
postit_flow_vertical, postit_flow_arc, postit_flow_outline, postit_flow_orgchart,
postit_flow_fishbone, postit_flow_mindmap.

Output:
    examples/output/mermaid_hero/
        hero_<diagram>[_<theme>].html
        hero_<diagram>[_<theme>].png
"""

import argparse
from pathlib import Path

from modern_graphics import ModernGraphicsGenerator, Attribution, get_scheme, list_schemes
from modern_graphics.diagrams.modern_hero import generate_modern_hero
from modern_graphics.diagrams.mermaid_svg import mermaid_to_svg
from modern_graphics.diagrams.theme_utils import extract_theme_colors
from modern_graphics.diagrams.wireframe_scene import render_scene
from modern_graphics.diagrams.wireframe_elements.config import WireframeConfig

EXAMPLES_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = EXAMPLES_DIR / "output" / "mermaid_hero"

DIAGRAMS = {
    "flowchart": {
        "file": "process_flow.mmd",
        "headline": "Process flow",
        "subheadline": "Validate → Process → Transform.",
        "mermaid": True,
    },
    "postit": {
        "file": "postit_flow.mmd",
        "headline": "Ideas to action",
        "subheadline": "Sticky-note style flow.",
        "mermaid": True,
    },
    "postit_flow": {
        "preset": "postit_flow",
        "headline": "Sandwich flow",
        "subheadline": "Break any process into clear steps. Here: from bread to plate in seven moves.",
        "mermaid": False,
        "insight_callout": {
            "label": "Key insight",
            "text": "Step by step, you get from bread to plate—no magic, just process.",
        },
    },
    "postit_flow_zigzag": {
        "preset": "postit_flow_zigzag",
        "headline": "Sandwich flow (zigzag)",
        "subheadline": "Alternating steps keep the eye moving left to right.",
        "mermaid": False,
    },
    "postit_flow_vertical": {
        "preset": "postit_flow_vertical",
        "headline": "Sandwich flow (vertical)",
        "subheadline": "Top-to-bottom process with a gentle stagger.",
        "mermaid": False,
    },
    "postit_flow_arc": {
        "preset": "postit_flow_arc",
        "headline": "Sandwich flow (arc)",
        "subheadline": "Steps along a curve for a compact horizontal flow.",
        "mermaid": False,
    },
    "postit_flow_outline": {
        "preset": "postit_flow_outline",
        "headline": "Traditional outline",
        "subheadline": "Q4 Product Launch: goals, tactics, risks—hierarchical levels.",
        "mermaid": False,
    },
    "postit_flow_orgchart": {
        "preset": "postit_flow_orgchart",
        "headline": "Org chart",
        "subheadline": "CEO → CTO, CFO, COO and their reports.",
        "mermaid": False,
    },
    "postit_flow_fishbone": {
        "preset": "postit_flow_fishbone",
        "headline": "Fishbone (Ishikawa)",
        "subheadline": "Effect: Defects. Causes: Training, Equipment, Procedure, Material, Measurement, Environment.",
        "mermaid": False,
    },
    "postit_flow_mindmap": {
        "preset": "postit_flow_mindmap",
        "headline": "Mind map",
        "subheadline": "Topic: Product Launch. Subtopics: Marketing, Sales, Support, Legal, Operations.",
        "mermaid": False,
    },
    "sankey": {
        "file": "sankey_flow.mmd",
        "headline": "Energy flow",
        "subheadline": "Sources to sectors.",
        "mermaid": True,
    },
    "sequence": {
        "file": "auth_sequence.mmd",
        "headline": "How login works",
        "subheadline": "User, app, and auth service in one flow.",
        "mermaid": True,
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Hero with Mermaid or wireframe diagram; all types output HTML and PNG"
    )
    parser.add_argument(
        "--diagram",
        choices=list(DIAGRAMS),
        required=True,
        help="Diagram type to render",
    )
    parser.add_argument(
        "--theme",
        choices=list_schemes(),
        help="Apply color theme to the hero and diagram",
    )
    args = parser.parse_args()

    info = DIAGRAMS[args.diagram]
    color_scheme = get_scheme(args.theme) if args.theme else None

    if info.get("mermaid", True):
        mmd_path = EXAMPLES_DIR / info["file"]
        if not mmd_path.exists():
            raise SystemExit(f"Mermaid file not found: {mmd_path}")
        try:
            mermaid_source = mmd_path.read_text(encoding="utf-8")
            svg_content = mermaid_to_svg(mermaid_source, color_scheme=color_scheme)
        except RuntimeError as e:
            raise SystemExit(
                f"{e}\nInstall mermaid-cli: npm install -g @mermaid-js/mermaid-cli (or use npx)."
            )
    else:
        from modern_graphics.diagrams.wireframe_scene import SCENE_PRESETS
        preset = info["preset"]
        spec = SCENE_PRESETS[preset]
        scene_width = spec.get("width", 1100)
        scene_height = spec.get("height", 200)
        config = WireframeConfig.from_color_scheme(
            color_scheme, width=scene_width, height=scene_height
        ) if color_scheme else WireframeConfig(width=scene_width, height=scene_height)
        svg_content = render_scene(spec, config)

    generator = ModernGraphicsGenerator(
        title=f"Mermaid {args.diagram}",
        attribution=Attribution(copyright="© Demo 2025"),
    )
    background_variant = "light"
    if color_scheme is not None:
        theme = extract_theme_colors(color_scheme)
        background_variant = "dark" if theme.is_dark else "light"
    html = generate_modern_hero(
        generator,
        headline=info["headline"],
        subheadline=info["subheadline"],
        freeform_canvas=svg_content,
        background_variant=background_variant,
        color_scheme=color_scheme,
        highlights=info.get("highlights"),
        highlight_tiles=info.get("highlight_tiles"),
        insight_callout=info.get("insight_callout"),
        cta=info.get("cta"),
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base = f"hero_{args.diagram}"
    if args.theme:
        base = f"{base}_{args.theme}"
    path_html = OUTPUT_DIR / f"{base}.html"
    path_png = OUTPUT_DIR / f"{base}.png"
    generator.save(html, path_html)
    generator.export_to_png(html, path_png, viewport_width=1200, viewport_height=700, padding=24)
    print(f"Saved: {path_html}")
    print(f"Saved: {path_png}")


if __name__ == "__main__":
    main()
