"""Base class and utilities for Modern Graphics Generator"""

from typing import Optional
from pathlib import Path

from .models import Attribution
from .templates import StyleTemplate, DEFAULT_TEMPLATE


class BaseGenerator:
    """Base class for Modern Graphics generators"""
    
    def __init__(self, title: str, template: Optional[StyleTemplate] = None, attribution: Optional[Attribution] = None):
        self.title = title
        self.template = template or DEFAULT_TEMPLATE
        self.attribution = attribution or Attribution()
    
    def _generate_attribution_html(self) -> str:
        """Generate attribution bug HTML"""
        context_html = f'<div class="context">{self.attribution.context}</div>\n        ' if self.attribution.context else ''
        return f"""
    <div class="attribution">
        {context_html}<div class="copyright">{self.attribution.copyright}</div>
    </div>"""
    
    def _wrap_html(self, content: str, styles: str) -> str:
        """Wrap content in full HTML document using template styles"""
        # Extract font family name for Google Fonts link (simplified)
        font_name = self.template.font_family.split("'")[1] if "'" in self.template.font_family else "Inter"
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <link href="https://fonts.googleapis.com/css2?family={font_name}:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        {self.template.base_styles}
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
        temp_html_path: Optional[Path] = None
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
            temp_html_path
        )
