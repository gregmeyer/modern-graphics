"""Example: Creating a custom diagram type"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.diagrams import DiagramGenerator, register_diagram
from modern_graphics.base import BaseGenerator


class SimpleListDiagramGenerator(DiagramGenerator):
    """Simple list diagram generator"""
    
    def generate(self, generator: BaseGenerator, title: str, items: list, **kwargs) -> str:
        """Generate a simple list diagram"""
        items_html = "".join(f'<li class="list-item">{item}</li>' for item in items)
        
        css_content = """
        .simple-list {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .list-title {
            font-size: 28px;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 24px;
            text-align: center;
        }
        
        .list-items {
            list-style: none;
            padding: 0;
        }
        
        .list-item {
            background: #F5F5F7;
            border-radius: 12px;
            padding: 16px 24px;
            margin-bottom: 12px;
            font-size: 18px;
            font-weight: 500;
            color: #1D1D1F;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        """
        
        html_content = f"""
        <div class="simple-list">
            <h2 class="list-title">{title}</h2>
            <ul class="list-items">
                {items_html}
            </ul>
        </div>
        """
        
        return generator._wrap_html(html_content, css_content)
    
    def validate_input(self, title: str, items: list, **kwargs) -> bool:
        """Validate input"""
        return bool(title and items and isinstance(items, list))


# Register the custom diagram
register_diagram("simple_list", SimpleListDiagramGenerator)

# Use it
generator = ModernGraphicsGenerator(
    "My Custom List",
    attribution=Attribution()
)

html = generator.generate_diagram(
    "simple_list",
    title="Features",
    items=["Feature 1", "Feature 2", "Feature 3"]
)

# Save
output_path = Path("custom_diagram_example.html")
generator.save(html, output_path)
print(f"Generated custom diagram: {output_path}")
