#!/usr/bin/env python3
"""Generate all flow layout styles (post-it and optional other node types).

Renders every flow preset (linear, zigzag, vertical, arc, outline, orgchart,
fishbone, mindmap) as PNG so you can see them in one place. Optionally
generates a linear flow with content_card nodes to show build_flow_elements
with a non-postit type.

Run from utils/modern-graphics:

    PYTHONPATH=. python examples/flow_styles_example.py
    PYTHONPATH=. python examples/flow_styles_example.py --svg   # also write SVG
    PYTHONPATH=. python examples/flow_styles_example.py --content-card   # also content_card linear

Output:
    examples/output/flow_styles/
        postit_flow.png, postit_flow_zigzag.png, ... postit_flow_mindmap.png
        content_card_linear.png   (if --content-card)
        *.svg   (if --svg)
"""

import argparse
from pathlib import Path

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams.wireframe_scene import (
    render_scene,
    SCENE_PRESETS,
    build_flow_elements,
)
from modern_graphics.diagrams.wireframe_elements.config import WireframeConfig

EXAMPLES_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = EXAMPLES_DIR / "output" / "flow_styles"

FLOW_PRESETS = [
    "postit_flow",
    "postit_flow_zigzag",
    "postit_flow_vertical",
    "postit_flow_arc",
    "postit_flow_outline",
    "postit_flow_orgchart",
    "postit_flow_fishbone",
    "postit_flow_mindmap",
]


def main():
    parser = argparse.ArgumentParser(
        description="Generate all flow layout styles as PNG"
    )
    parser.add_argument(
        "--svg",
        action="store_true",
        help="Also write SVG files",
    )
    parser.add_argument(
        "--content-card",
        action="store_true",
        help="Also generate a linear flow with content_card nodes",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generator = ModernGraphicsGenerator(
        title="Flow styles",
        attribution=Attribution(copyright="© Demo"),
    )
    from modern_graphics.cli import wrap_svg_for_png_export

    scheme = None

    for preset in FLOW_PRESETS:
        if preset not in SCENE_PRESETS:
            continue
        spec = SCENE_PRESETS[preset]
        config = WireframeConfig(
            width=spec.get("width", 600),
            height=spec.get("height", 400),
        )
        svg = render_scene(spec, config)
        w, h = spec.get("width", 600), spec.get("height", 400)

        if args.svg:
            path_svg = OUTPUT_DIR / f"{preset}.svg"
            path_svg.write_text(svg)
            print(f"  {path_svg.relative_to(EXAMPLES_DIR)}")

        html = wrap_svg_for_png_export(svg, scheme, w, h)
        path_png = OUTPUT_DIR / f"{preset}.png"
        generator.export_to_png(
            html,
            path_png,
            viewport_width=w + 40,
            viewport_height=h + 40,
            padding=20,
        )
        print(f"  {path_png.relative_to(EXAMPLES_DIR)}")

    if args.content_card:
        elements = build_flow_elements(
            labels=["Step 1", "Step 2", "Step 3", "Step 4"],
            layout="linear",
            width=600,
            height=140,
            node_type="content_card",
            node_props_fn=lambda n: {},
        )
        spec = {"width": 600, "height": 140, "elements": elements}
        config = WireframeConfig(width=600, height=140)
        svg = render_scene(spec, config)

        if args.svg:
            path_svg = OUTPUT_DIR / "content_card_linear.svg"
            path_svg.write_text(svg)
            print(f"  {path_svg.relative_to(EXAMPLES_DIR)} (content_card nodes)")

        html = wrap_svg_for_png_export(svg, scheme, 600, 140)
        path_png = OUTPUT_DIR / "content_card_linear.png"
        generator.export_to_png(
            html,
            path_png,
            viewport_width=640,
            viewport_height=180,
            padding=20,
        )
        print(f"  {path_png.relative_to(EXAMPLES_DIR)}")

    print(f"\nOutput: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
