"""PNG export functionality for Modern Graphics."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional


CONTENT_BBOX_JS = """
() => {
  const isVisible = (el) => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden') return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 2 && rect.height > 2;
  };

  const unionRects = (elements) => {
    const rects = elements
      .filter(isVisible)
      .map((el) => el.getBoundingClientRect());
    if (!rects.length) return null;

    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    for (const rect of rects) {
      minX = Math.min(minX, rect.left);
      minY = Math.min(minY, rect.top);
      maxX = Math.max(maxX, rect.right);
      maxY = Math.max(maxY, rect.bottom);
    }
    if (!isFinite(minX) || !isFinite(minY) || !isFinite(maxX) || !isFinite(maxY)) {
      return null;
    }
    return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
  };

  // Preferred explicit roots. Add selectors here as new layout families are introduced.
  const rootSelectors = [
    '[data-mg-crop-root]',
    '.slide-cards-container',
    '.slide-comparison-container',
    '.story-slide-container',
    '.hero-card-container',
    '.premium-card-stage',
    '.data-card-container',
    '.infographic-container',
    '.story-driven-container',
    '.cycle-container',
    '.flywheel-container',
    '.timeline-container',
    '.timeline',
    '.comparison',
    '.tests-grid',
    '.wrapper',
    '.container',
    'main',
    '[role="main"]'
  ];

  const roots = [];
  for (const selector of rootSelectors) {
    for (const el of document.querySelectorAll(selector)) {
      if (isVisible(el)) roots.push(el);
    }
  }

  const rootBox = unionRects(roots);
  if (rootBox) return rootBox;

  // Fallback: union commonly meaningful content nodes.
  const fallbackSelectors = [
    'svg', 'canvas', 'img',
    '.card', '.panel',
    '.title', '.headline',
    'h1', 'h2', 'h3', 'p',
    '[class*="card"]', '[class*="panel"]'
  ];

  const fallbackEls = [];
  for (const selector of fallbackSelectors) {
    for (const el of document.querySelectorAll(selector)) {
      if (isVisible(el)) fallbackEls.push(el);
    }
  }

  return unionRects(fallbackEls);
}
"""


def _normalize_crop_mode(crop_mode: str) -> str:
    mode = (crop_mode or "safe").strip().lower()
    return mode if mode in {"none", "safe", "tight"} else "safe"


def _effective_padding(mode: str, padding: int) -> int:
    base = max(0, int(padding))
    if mode == "tight":
        # Tight mode still keeps minimal breathing room to prevent clipping.
        return max(0, int(round(base * 0.5)))
    return base


def _calculate_crop_box(
    bbox: dict[str, float],
    image_width: int,
    image_height: int,
    device_scale_factor: int,
    padding: int,
) -> tuple[int, int, int, int] | None:
    if not bbox:
        return None

    width = float(bbox.get("width", 0))
    height = float(bbox.get("height", 0))
    if width <= 0 or height <= 0:
        return None

    scale = max(1, int(device_scale_factor))
    scaled_padding = max(0, int(padding)) * scale

    x = int(round(float(bbox.get("x", 0)) * scale - scaled_padding))
    y = int(round(float(bbox.get("y", 0)) * scale - scaled_padding))
    w = int(round(width * scale + (scaled_padding * 2)))
    h = int(round(height * scale + (scaled_padding * 2)))

    x = max(0, min(x, image_width - 1))
    y = max(0, min(y, image_height - 1))
    w = max(1, min(w, image_width - x))
    h = max(1, min(h, image_height - y))

    return (x, y, x + w, y + h)


def export_html_to_png(
    html_content: str,
    output_path: Path,
    save_html_func,
    viewport_width: int = 2400,
    viewport_height: int = 1600,
    device_scale_factor: int = 2,
    padding: int = 8,
    crop_mode: str = "safe",
    temp_html_path: Optional[Path] = None,
    omit_background: bool = False,
) -> Path:
    """Export HTML to PNG with deterministic crop behavior."""
    try:
        from PIL import Image
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise ImportError(
            "export_to_png requires playwright and PIL. "
            "Install with: pip install playwright pillow && playwright install chromium"
        ) from e

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    resolved_crop_mode = _normalize_crop_mode(crop_mode)

    temp_dir = Path(tempfile.gettempdir())
    temp_png_path = None
    temp_html_file = None

    try:
        if temp_html_path is None:
            temp_html_file = tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".html",
                delete=False,
                dir=temp_dir,
            )
            temp_html_path = Path(temp_html_file.name)
            temp_html_file.write(html_content)
            temp_html_file.close()
        else:
            temp_html_path = Path(temp_html_path)
            save_html_func(html_content, temp_html_path)

        temp_png_file = tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
            dir=temp_dir,
        )
        temp_png_path = Path(temp_png_file.name)
        temp_png_file.close()

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception:
                chrome_path = os.environ.get("MODERN_GRAPHICS_CHROME")
                if chrome_path and Path(chrome_path).exists():
                    try:
                        browser = p.chromium.launch(
                            headless=True,
                            executable_path=chrome_path,
                            args=["--no-sandbox"],
                        )
                    except Exception:
                        browser = None
                else:
                    browser = None

                if browser is None:
                    try:
                        browser = p.chromium.launch(
                            headless=True,
                            channel="chrome",
                            args=["--no-sandbox"],
                        )
                    except Exception:
                        browser = None

                if browser is None:
                    try:
                        browser = p.chromium.launch(headless=True, chromium_sandbox=False)
                    except Exception as chromium_error:
                        try:
                            browser = p.webkit.launch(headless=True)
                        except Exception:
                            raise chromium_error

            context = browser.new_context(
                viewport={"width": viewport_width, "height": viewport_height},
                device_scale_factor=device_scale_factor,
            )
            page = context.new_page()
            page.goto(f"file://{temp_html_path.resolve()}", wait_until="networkidle")
            page.wait_for_timeout(1000)

            page.screenshot(
                path=str(temp_png_path),
                full_page=True,
                omit_background=omit_background,
            )

            if resolved_crop_mode == "none":
                temp_png_path.rename(output_path)
                browser.close()
                return output_path

            try:
                bbox = page.evaluate(CONTENT_BBOX_JS)
                effective_padding = _effective_padding(resolved_crop_mode, padding)

                with Image.open(temp_png_path) as img:
                    box = _calculate_crop_box(
                        bbox,
                        image_width=img.width,
                        image_height=img.height,
                        device_scale_factor=device_scale_factor,
                        padding=effective_padding,
                    )
                    if box is None:
                        temp_png_path.rename(output_path)
                    else:
                        img.crop(box).save(output_path)
                        temp_png_path.unlink(missing_ok=True)
            except Exception as e:
                print(f"Warning: Could not crop ({e}), using full page")
                if temp_png_path and temp_png_path.exists():
                    temp_png_path.rename(output_path)
                else:
                    page.screenshot(path=str(output_path), full_page=True)

            browser.close()

    finally:
        if temp_png_path and temp_png_path.exists() and temp_png_path != output_path:
            try:
                temp_png_path.unlink()
            except Exception:
                pass

        if temp_html_path and temp_html_path.exists():
            if temp_html_path.parent == temp_dir:
                try:
                    temp_html_path.unlink()
                except Exception:
                    pass

    return output_path
