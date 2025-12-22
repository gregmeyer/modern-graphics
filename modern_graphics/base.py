"""Base class and utilities for Modern Graphics Generator"""

import re
from typing import Optional
from pathlib import Path

from .models import Attribution
from .templates import StyleTemplate, DEFAULT_TEMPLATE


class BaseGenerator:
    """Base class for Modern Graphics generators"""
    
    def __init__(self, title: str, template: Optional[StyleTemplate] = None, attribution: Optional[Attribution] = None, use_svg_js: bool = False):
        self.title = title
        self.template = template or DEFAULT_TEMPLATE
        self.attribution = attribution or Attribution()
        self.use_svg_js = use_svg_js
    
    def _generate_attribution_html(self) -> str:
        """Generate attribution bug HTML with customizable styling"""
        if not self.attribution.show or not self.attribution.copyright:
            return ""
        
        # Build inline styles from attribution config
        bg_style = f"background-color: {self.attribution.background_color};" if self.attribution.background_color else ""
        
        # Position-based text alignment
        text_align = "right" if self.attribution.position == "bottom-right" else "center" if self.attribution.position == "bottom-center" else "left"
        
        attribution_style = f"""
            font-size: {self.attribution.font_size};
            color: {self.attribution.font_color};
            font-weight: {self.attribution.font_weight};
            opacity: {self.attribution.opacity};
            padding: {self.attribution.padding};
            border-radius: {self.attribution.border_radius};
            text-align: {text_align};
            {bg_style}
        """.strip()
        
        context_html = f'<div class="context" style="font-size: {self.attribution.font_size}; color: {self.attribution.font_color}; opacity: {self.attribution.opacity}; margin-bottom: 2px;">{self.attribution.context}</div>\n        ' if self.attribution.context else ''
        
        return f"""
    <div class="attribution" style="{attribution_style}">
        {context_html}<div class="copyright">{self.attribution.copyright}</div>
    </div>"""
    
    def _wrap_html(self, content: str, styles: str) -> str:
        """Wrap content in full HTML document using template styles"""
        # Extract font family name for Google Fonts link (simplified)
        if hasattr(self.template, 'font_family') and self.template.font_family:
            font_name = self.template.font_family.split("'")[1] if "'" in self.template.font_family else "Inter"
        else:
            font_name = "Inter"
        
        # Inject template's background_color and font_family into base_styles
        # Always apply template styles, overriding any existing values
        if hasattr(self.template, 'base_styles'):
            base_styles = self.template.base_styles
        else:
            base_styles = ""
        
        # Apply template styles more robustly - handle both cases where body selector exists and doesn't
        template_bg = getattr(self.template, 'background_color', None)
        template_font = getattr(self.template, 'font_family', None)
        if template_bg or template_font:
            # Try to find and replace body selector
            body_match = re.search(r'body\s*\{([^}]*)\}', base_styles, flags=re.IGNORECASE | re.DOTALL)
            
            if body_match:
                # Body selector exists - modify it
                body_content = body_match.group(1)
                
                # Remove existing background declarations
                if template_bg:
                    body_content = re.sub(r'background(-color)?\s*:\s*[^;]+;', '', body_content, flags=re.IGNORECASE)
                    body_content += f'\n            background: {template_bg};'
                
                # Remove existing font-family declarations
                if template_font:
                    body_content = re.sub(r'font-family\s*:\s*[^;]+;', '', body_content, flags=re.IGNORECASE)
                    body_content += f'\n            font-family: {template_font};'
                
                # Replace the body selector with updated content
                base_styles = base_styles[:body_match.start()] + f'body {{{body_content}\n        }}' + base_styles[body_match.end():]
            else:
                # Body selector doesn't exist - append it
                template_overrides = []
                if template_bg:
                    template_overrides.append(f'            background: {template_bg};')
                if template_font:
                    template_overrides.append(f'            font-family: {template_font};')
                
                if template_overrides:
                    overrides_text = "\n".join(template_overrides)
                    base_styles += f'\n        body {{\n{overrides_text}\n        }}'
        
        # Include SVG.js if enabled
        svg_js_script = ""
        if self.use_svg_js:
            from .svg_utils import generate_svg_js_cdn_script
            svg_js_script = generate_svg_js_cdn_script()
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <link href="https://fonts.googleapis.com/css2?family={font_name}:wght@400;500;600;700&display=swap" rel="stylesheet">
    {svg_js_script}
    <style>
        {base_styles}
        {styles}
    </style>
</head>
<body>
{content}
</body>
</html>"""
    
    def save(self, html_content: str, output_path: Path):
        """Save HTML to file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')
        return output_path
    
    def export_to_png(
        self,
        html_content: str,
        output_path: Path,
        viewport_width: int = 2400,
        viewport_height: int = 1600,
        device_scale_factor: int = 2,
        padding: int = 20,
        temp_html_path: Optional[Path] = None,
        transparent_background: bool = False
    ) -> Path:
        """Export HTML to PNG - delegates to export module"""
        from .export import export_html_to_png
        return export_html_to_png(
            html_content,
            output_path,
            self.save,
            viewport_width,
            viewport_height,
            device_scale_factor,
            padding,
            temp_html_path,
            omit_background=transparent_background
        )
