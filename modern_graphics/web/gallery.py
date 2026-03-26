"""Static gallery site generator.

Usage: python -m modern_graphics.web.gallery --output site/
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def generate_gallery(output_dir: str) -> None:
    """Generate a static gallery site from registry metadata and showcase images."""
    from ..rendering import get_layout_info, get_theme_info

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Build gallery data
    data = {
        "layouts": get_layout_info(),
        "themes": get_theme_info(),
    }

    # Read template
    template_dir = Path(__file__).parent / "templates"
    template = (template_dir / "index.html").read_text(encoding="utf-8")

    # Inject data
    html = template.replace("<!-- GALLERY_DATA -->", json.dumps(data, indent=2))

    # Write HTML
    (out / "index.html").write_text(html, encoding="utf-8")

    # Copy static assets
    static_dir = Path(__file__).parent / "static"
    for f in static_dir.iterdir():
        if f.is_file():
            shutil.copy2(f, out / f.name)

    # Copy showcase images
    project_root = Path(__file__).parent.parent.parent
    showcase_dir = project_root / "examples" / "output" / "showcase"
    images_dir = out / "images"
    images_dir.mkdir(exist_ok=True)

    if showcase_dir.exists():
        for subdir in showcase_dir.iterdir():
            if subdir.is_dir():
                for img in subdir.iterdir():
                    if img.suffix.lower() in (".png", ".svg", ".jpg"):
                        dest_name = f"{subdir.name}--{img.name}"
                        shutil.copy2(img, images_dir / dest_name)

        # Also create layout-named copies for card images
        _LAYOUT_IMAGE_MAP = {
            "hero": "create-first--hero.png",
            "comparison": "diagram-types--02-comparison.png",
            "timeline": "diagram-types--03-timeline.png",
            "story": "diagram-types--04-story-slide.png",
            "funnel": "diagram-types--06-funnel.png",
            "grid": "diagram-types--05-grid.png",
            "key-insight": "create-first--key-insight-quote.png",
            "insight-card": "create-first--insight-card.png",
            "insight-story": "create-first--insight-story.png",
            "hero-triptych": "hero-slides--05-triptych.png",
        }
        for layout_name, source_name in _LAYOUT_IMAGE_MAP.items():
            src = images_dir / source_name
            if src.exists():
                shutil.copy2(src, images_dir / f"{layout_name}.png")

    # Copy theme demo images
    theme_demo_dir = project_root / "examples" / "output" / "theme-demo"
    theme_images_dir = out / "theme-images"
    theme_images_dir.mkdir(exist_ok=True)

    if theme_demo_dir.exists():
        for img in theme_demo_dir.iterdir():
            if img.suffix.lower() == ".png":
                shutil.copy2(img, theme_images_dir / img.name)

    # Generate per-theme named images for card display
    for theme in data["themes"]:
        # Try to find a matching theme demo image
        for img in theme_images_dir.iterdir():
            if img.suffix == ".png":
                # Use the first available as the theme preview
                dest = theme_images_dir / f"theme-{theme['name']}.png"
                if not dest.exists():
                    shutil.copy2(img, dest)
                break

    print(f"Gallery generated: {out / 'index.html'}")
    print(f"  Layouts: {len(data['layouts'])}")
    print(f"  Themes: {len(data['themes'])}")
    print(f"  Images: {sum(1 for _ in images_dir.iterdir())}")


def main():
    parser = argparse.ArgumentParser(description="Generate static gallery site")
    parser.add_argument("--output", default="site", help="Output directory (default: site)")
    args = parser.parse_args()
    generate_gallery(args.output)


if __name__ == "__main__":
    main()
