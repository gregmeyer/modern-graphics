"""PNG export functionality for Modern Graphics"""

import tempfile
from pathlib import Path
from typing import Optional


def export_html_to_png(
    html_content: str,
    output_path: Path,
    save_html_func,
    viewport_width: int = 2400,
    viewport_height: int = 1600,
    device_scale_factor: int = 2,
    padding: int = 20,
    temp_html_path: Optional[Path] = None,
    omit_background: bool = False
) -> Path:
    """
    Export HTML to PNG with high-resolution settings and tight cropping
    
    Args:
        html_content: HTML content to export
        output_path: Path for output PNG file
        save_html_func: Function to save HTML (takes html_content and path)
        viewport_width: Browser viewport width in CSS pixels (default: 2400)
        viewport_height: Browser viewport height in CSS pixels (default: 1600)
        device_scale_factor: Device scale factor for higher resolution (default: 2)
        padding: Padding around content in CSS pixels (default: 20)
        temp_html_path: Optional path for temporary HTML file (auto-generated if None)
    
    Returns:
        Path to generated PNG file
    
    Raises:
        ImportError: If playwright or PIL are not available
    """
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError as e:
        raise ImportError(
            "export_to_png requires playwright and PIL. "
            "Install with: pip install playwright pillow && playwright install chromium"
        ) from e
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use system temp directory for temporary files
    temp_dir = Path(tempfile.gettempdir())
    temp_png_path = None
    temp_html_file = None
    
    try:
        # Create temporary HTML file
        if temp_html_path is None:
            temp_html_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.html',
                delete=False,
                dir=temp_dir
            )
            temp_html_path = Path(temp_html_file.name)
            temp_html_file.write(html_content)
            temp_html_file.close()
        else:
            temp_html_path = Path(temp_html_path)
            save_html_func(html_content, temp_html_path)
        
        # Create temporary PNG file
        temp_png_file = tempfile.NamedTemporaryFile(
            suffix='.png',
            delete=False,
            dir=temp_dir
        )
        temp_png_path = Path(temp_png_file.name)
        temp_png_file.close()
        
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception:
                # Retry without the Chromium sandbox (required in some locked-down environments)
                try:
                    browser = p.chromium.launch(headless=True, chromium_sandbox=False)
                except Exception as chromium_error:
                    # As a final fallback, try WebKit before giving up
                    try:
                        browser = p.webkit.launch(headless=True)
                    except Exception:
                        raise chromium_error
            
            # Create context with high resolution settings
            context = browser.new_context(
                viewport={"width": viewport_width, "height": viewport_height},
                device_scale_factor=device_scale_factor
            )
            page = context.new_page()
            page.goto(f"file://{temp_html_path.resolve()}", wait_until="networkidle")
            
            # Wait for content to load
            page.wait_for_timeout(500)
            
            # Take full page screenshot first
            page.screenshot(
                path=str(temp_png_path),
                full_page=True,
                omit_background=omit_background
            )
            
            # Get bounding box of the main content using JavaScript
            try:
                # Check if this is a story slide - use container directly
                is_story_slide = page.evaluate("""() => {
                    return document.querySelector('.story-slide-container') !== null;
                }""")
                
                # Check if this is a hero card
                is_hero_card = page.evaluate("""() => {
                    return document.querySelector('.hero-card-container') !== null;
                }""")
                
                # Check if this is a minimal data card
                is_data_card = page.evaluate("""() => {
                    return document.querySelector('.data-card-container') !== null;
                }""")
                
                # Check if this is a minimal infographic
                is_infographic = page.evaluate("""() => {
                    return document.querySelector('.infographic-container') !== null;
                }""")
                
                # Check if this is a minimal story-driven slide
                is_story_driven = page.evaluate("""() => {
                    return document.querySelector('.story-driven-container') !== null;
                }""")
                
                if is_story_slide:
                    content_bbox = page.evaluate("""() => {
                        const container = document.querySelector('.story-slide-container');
                        if (!container) return null;
                        
                        const containerRect = container.getBoundingClientRect();
                        return {
                            x: containerRect.left,
                            y: containerRect.top,
                            width: containerRect.width,
                            height: containerRect.height
                        };
                    }""")
                elif is_hero_card:
                    content_bbox = page.evaluate("""() => {
                        const card = document.querySelector('.hero-card');
                        if (!card) return null;
                        
                        const cardRect = card.getBoundingClientRect();
                        return {
                            x: cardRect.left,
                            y: cardRect.top,
                            width: cardRect.width,
                            height: cardRect.height
                        };
                    }""")
                elif is_data_card:
                    content_bbox = page.evaluate("""() => {
                        const container = document.querySelector('.data-card-container');
                        if (!container) return null;
                        
                        const containerRect = container.getBoundingClientRect();
                        return {
                            x: containerRect.left,
                            y: containerRect.top,
                            width: containerRect.width,
                            height: containerRect.height
                        };
                    }""")
                elif is_infographic:
                    content_bbox = page.evaluate("""() => {
                        const container = document.querySelector('.infographic-container');
                        if (!container) return null;
                        
                        const containerRect = container.getBoundingClientRect();
                        return {
                            x: containerRect.left,
                            y: containerRect.top,
                            width: containerRect.width,
                            height: containerRect.height
                        };
                    }""")
                elif is_story_driven:
                    content_bbox = page.evaluate("""() => {
                        const container = document.querySelector('.story-driven-container');
                        if (!container) return null;
                        
                        const containerRect = container.getBoundingClientRect();
                        return {
                            x: containerRect.left,
                            y: containerRect.top,
                            width: containerRect.width,
                            height: containerRect.height
                        };
                    }""")
                else:
                    content_bbox = None
                
                if content_bbox:
                    scaled_padding = padding * device_scale_factor
                    x = max(0, int(content_bbox['x'] * device_scale_factor - scaled_padding))
                    y = max(0, int(content_bbox['y'] * device_scale_factor - scaled_padding))
                    width = int(content_bbox['width'] * device_scale_factor + scaled_padding * 2)
                    height = int(content_bbox['height'] * device_scale_factor + scaled_padding * 2)
                    
                    img = Image.open(temp_png_path)
                    img_width, img_height = img.size
                    x = max(0, min(x, img_width - 1))
                    y = max(0, min(y, img_height - 1))
                    width = min(width, img_width - x)
                    height = min(height, img_height - y)
                    
                    cropped = img.crop((x, y, x + width, y + height))
                    cropped.save(output_path)
                    temp_png_path.unlink()
                else:
                    # Fallback: try to find bounding box from elements
                    if not is_story_slide and not is_hero_card and not is_data_card and not is_infographic and not is_story_driven:
                        bbox = page.evaluate("""() => {
                    const elements = [
                        ...document.querySelectorAll('.step'),
                        ...document.querySelectorAll('.arrow'),
                        ...document.querySelectorAll('.title'),
                        ...document.querySelectorAll('.attribution'),
                        ...document.querySelectorAll('.cycle-end'),
                        ...document.querySelectorAll('.cycle'),
                        ...document.querySelectorAll('.flywheel-element'),
                        ...document.querySelectorAll('.flywheel-container'),
                        ...document.querySelectorAll('.comparison'),
                        ...document.querySelectorAll('.tests-grid'),
                        ...document.querySelectorAll('.timeline'),
                        ...document.querySelectorAll('.event'),
                        ...document.querySelectorAll('.timeline-marker'),
                        ...document.querySelectorAll('.pyramid'),
                        ...document.querySelectorAll('.layer'),
                        ...document.querySelectorAll('.before-after'),
                        ...document.querySelectorAll('.item'),
                        ...document.querySelectorAll('.funnel'),
                        ...document.querySelectorAll('.stage'),
                        ...document.querySelectorAll('.slide-card'),
                        ...document.querySelectorAll('.slide-cards-row'),
                        ...document.querySelectorAll('.card-arrow'),
                        ...document.querySelectorAll('.slide-comparison-row')
                    ];
                    
                    if (elements.length === 0) return null;
                    
                    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
                    
                    elements.forEach(el => {
                        const rect = el.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            minX = Math.min(minX, rect.left);
                            minY = Math.min(minY, rect.top);
                            maxX = Math.max(maxX, rect.right);
                            maxY = Math.max(maxY, rect.bottom);
                        }
                    });
                    
                    if (minX === Infinity) return null;
                    
                    const wrapper = document.querySelector('.wrapper');
                    if (wrapper && (wrapper.querySelector('.slide-cards-row') || wrapper.querySelector('.slide-comparison-row'))) {
                        const wrapperRect = wrapper.getBoundingClientRect();
                        return {
                            x: wrapperRect.left,
                            y: wrapperRect.top,
                            width: wrapperRect.width,
                            height: wrapperRect.height
                        };
                    }
                    
                    return {
                        x: minX,
                        y: minY,
                        width: maxX - minX,
                        height: maxY - minY
                    };
                }""")
                        
                        # Check if this is a slide card diagram
                        is_slide_card = page.evaluate("""() => {
                        return document.querySelector('.slide-cards-row') !== null || 
                               document.querySelector('.slide-comparison-row') !== null;
                        }""")
                        
                        if is_slide_card:
                            content_bbox = page.evaluate("""() => {
                            const container = document.querySelector('.slide-cards-container') || document.querySelector('.slide-comparison-container');
                            if (!container) return null;
                            
                            const containerRect = container.getBoundingClientRect();
                            return {
                                x: containerRect.left,
                                y: containerRect.top,
                                width: containerRect.width,
                                height: containerRect.height
                            };
                        }""")
                        
                        if content_bbox:
                            scaled_padding = padding * device_scale_factor
                            x = max(0, int(content_bbox['x'] * device_scale_factor - scaled_padding))
                            y = max(0, int(content_bbox['y'] * device_scale_factor - scaled_padding))
                            width = int(content_bbox['width'] * device_scale_factor + scaled_padding * 2)
                            height = int(content_bbox['height'] * device_scale_factor + scaled_padding * 2)
                            
                            img = Image.open(temp_png_path)
                            img_width, img_height = img.size
                            x = max(0, min(x, img_width - 1))
                            y = max(0, min(y, img_height - 1))
                            width = min(width, img_width - x)
                            height = min(height, img_height - y)
                            
                            cropped = img.crop((x, y, x + width, y + height))
                            cropped.save(output_path)
                            temp_png_path.unlink()
                        else:
                            temp_png_path.rename(output_path)
                    elif bbox:
                        scaled_padding = padding * device_scale_factor
                        x = max(0, int(bbox['x'] * device_scale_factor - scaled_padding))
                        y = max(0, int(bbox['y'] * device_scale_factor - scaled_padding))
                        width = int(bbox['width'] * device_scale_factor + scaled_padding * 2)
                        height = int(bbox['height'] * device_scale_factor + scaled_padding * 2)
                        
                        img = Image.open(temp_png_path)
                        img_width, img_height = img.size
                        x = max(0, min(x, img_width - 1))
                        y = max(0, min(y, img_height - 1))
                        width = min(width, img_width - x)
                        height = min(height, img_height - y)
                        
                        cropped = img.crop((x, y, x + width, y + height))
                        cropped.save(output_path)
                        temp_png_path.unlink()
                    else:
                        temp_png_path.rename(output_path)
            except Exception as e:
                print(f"Warning: Could not crop ({e}), using full page")
                if temp_png_path and temp_png_path.exists():
                    temp_png_path.rename(output_path)
                else:
                    # Fallback: save full page screenshot
                    page.screenshot(path=str(output_path), full_page=True)
            
            browser.close()
    
    finally:
        # Clean up temporary files
        if temp_png_path and temp_png_path.exists() and temp_png_path != output_path:
            try:
                temp_png_path.unlink()
            except:
                pass
        
        if temp_html_path and temp_html_path.exists():
            # Only delete if we created it (in temp directory)
            if temp_html_path.parent == temp_dir:
                try:
                    temp_html_path.unlink()
                except:
                    pass
    
    return output_path
