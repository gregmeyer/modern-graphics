#!/usr/bin/env python3
"""Demo: SVG composition of transaction icons on a card (insight + slide + scene).

1. Transaction is a registered scene element (type "transaction") so it can be
   used in wireframe-scene specs and composed with other elements.
2. Same composition is used on an insight card and a slide card via custom_mockup/svg_content.

Run from utils/modern-graphics:
    PYTHONPATH=. python examples/transaction_card_demo.py

Output:
    examples/output/transaction_card/
        transaction_insight_card.html / .png
        transaction_slide_card.html / .png
        transaction_scene.svg (scene spec with type "transaction")
"""

from pathlib import Path

from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams import (
    render_transaction_svg,
    render_scene,
    generate_insight_card,
    generate_slide_card_diagram,
)
from modern_graphics.diagrams.wireframe_elements.config import WireframeConfig

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "transaction_card"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

generator = ModernGraphicsGenerator(
    title="Transaction card demo",
    attribution=Attribution(copyright="© Demo 2025"),
)

# Transaction SVG: icons + labels (merchant, amount, date) — standalone
transaction_svg = render_transaction_svg(
    width=360,
    height=200,
    merchant="Coffee Shop",
    amount="$4.50",
    date="Today",
    accent="#0071e3",
)

# 1. Insight card: key insight + transaction graphic
print("Generating insight card with transaction SVG...")
html_insight = generate_insight_card(
    generator,
    text="Every transaction can be <span class=\"highlight\">one tap</span>—card, merchant, and date in one clear view.",
    svg_content=transaction_svg,
    label="Key Insight",
    svg_label="Transaction",
    eyebrow="Payments",
    context="Design for clarity, not clutter.",
    layout="side-by-side",
    svg_position="right",
)

path_insight_html = OUTPUT_DIR / "transaction_insight_card.html"
path_insight_png = OUTPUT_DIR / "transaction_insight_card.png"
generator.save(html_insight, path_insight_html)
generator.export_to_png(html_insight, path_insight_png, viewport_width=1000, viewport_height=500, padding=20)
print(f"  {path_insight_html.name}")
print(f"  {path_insight_png.name}")

# 2. Slide card: same transaction SVG as custom_mockup
print("Generating slide card with transaction mockup...")
cards = [
    {
        "title": "Transaction at a glance",
        "tagline": "Payments",
        "subtext": "Merchant, amount, and date with clear icons.",
        "color": "blue",
        "badge": "Demo",
        "features": ["Card icon", "Merchant", "Amount", "Date"],
        "custom_mockup": transaction_svg,
    },
]
html_slide = generate_slide_card_diagram(generator, cards, arrow_text="→")

path_slide_html = OUTPUT_DIR / "transaction_slide_card.html"
path_slide_png = OUTPUT_DIR / "transaction_slide_card.png"
generator.save(html_slide, path_slide_html)
generator.export_to_png(html_slide, path_slide_png, viewport_width=500, viewport_height=520, padding=20)
print(f"  {path_slide_html.name}")
print(f"  {path_slide_png.name}")

# 3. Scene spec: use registered "transaction" element (can be called again in any spec)
print("Generating scene with type \"transaction\" from ELEMENT_REGISTRY...")
config = WireframeConfig(width=600, height=400)
scene_spec = {
    "width": 600,
    "height": 400,
    "elements": [
        {"type": "browser_window", "x": 0, "y": 0, "width": 600, "height": 400, "props": {"url": "pay.example.com"}},
        {"type": "transaction", "x": 120, "y": 100, "width": 360, "height": 200, "props": {"merchant": "Coffee Shop", "amount": "$4.50", "date": "Today"}},
    ],
}
scene_svg = render_scene(scene_spec, config)
path_scene = OUTPUT_DIR / "transaction_scene.svg"
path_scene.write_text(scene_svg)
print(f"  {path_scene.name}")

print(f"\nDone. Output in {OUTPUT_DIR}")
