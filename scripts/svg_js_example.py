"""Example script demonstrating SVG.js integration with Modern Graphics Generator"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator, Attribution
from modern_graphics.svg_utils import (
    generate_svg_container,
    generate_svg_init_script,
    create_svg_circle,
    create_svg_rect,
    create_svg_line,
    create_svg_text,
    generate_complete_svg_example,
)


def example_basic_svg():
    """Example 1: Basic SVG.js usage with circles and lines"""
    print("Generating Example 1: Basic SVG.js diagram...")
    
    generator = ModernGraphicsGenerator("SVG.js Basic Example", Attribution(), use_svg_js=True)
    
    # Create SVG container
    container = generate_svg_container("svg-basic", 800, 600)
    
    # Generate SVG.js code to create elements
    svg_elements = [
        # Create circles
        create_svg_circle(200, 150, 50, "#4A90E2", stroke="#2E5C8A", stroke_width=3),
        create_svg_circle(400, 150, 50, "#50C878", stroke="#2E7D4E", stroke_width=3),
        create_svg_circle(600, 150, 50, "#FF6B6B", stroke="#CC5555", stroke_width=3),
        
        # Create connecting lines
        create_svg_line(250, 150, 350, 150, "#666", stroke_width=2),
        create_svg_line(450, 150, 550, 150, "#666", stroke_width=2),
        
        # Add labels
        create_svg_text(200, 250, "Step 1", font_size=18, fill="#333"),
        create_svg_text(400, 250, "Step 2", font_size=18, fill="#333"),
        create_svg_text(600, 250, "Step 3", font_size=18, fill="#333"),
    ]
    
    # Generate initialization script with elements
    elements_code = '\n        '.join(svg_elements)
    script = generate_svg_init_script("svg-basic", 800, 600, elements_code)
    
    # Wrap in content
    content = f"""
    <div style="padding: 40px; text-align: center;">
        <h1 style="margin-bottom: 30px; color: #333;">Basic SVG.js Diagram</h1>
        {container}
        {script}
    </div>
    """
    
    html = generator._wrap_html(content, "")
    generator.export_to_png(html, Path("examples/output/svg_js_basic.png"))
    print("✓ Generated examples/output/svg_js_basic.png")


def example_complex_diagram():
    """Example 2: More complex diagram with shapes and paths"""
    print("Generating Example 2: Complex SVG.js diagram...")
    
    generator = ModernGraphicsGenerator("SVG.js Complex Example", Attribution(), use_svg_js=True)
    
    container = generate_svg_container("svg-complex", 1000, 700)
    
    svg_elements = [
        # Background rectangle
        create_svg_rect(50, 50, 900, 600, "#F5F5F5", rx=10, stroke="#DDD"),
        
        # Central circle
        create_svg_circle(500, 350, 80, "#6366F1", stroke="#4F46E5", stroke_width=4),
        create_svg_text(500, 360, "Core", font_size=24, fill="#FFF", font_family="Arial"),
        
        # Surrounding circles
        create_svg_circle(300, 200, 60, "#10B981", stroke="#059669", stroke_width=3),
        create_svg_text(300, 210, "A", font_size=20, fill="#FFF"),
        
        create_svg_circle(700, 200, 60, "#F59E0B", stroke="#D97706", stroke_width=3),
        create_svg_text(700, 210, "B", font_size=20, fill="#FFF"),
        
        create_svg_circle(300, 500, 60, "#EF4444", stroke="#DC2626", stroke_width=3),
        create_svg_text(300, 510, "C", font_size=20, fill="#FFF"),
        
        create_svg_circle(700, 500, 60, "#8B5CF6", stroke="#7C3AED", stroke_width=3),
        create_svg_text(700, 510, "D", font_size=20, fill="#FFF"),
        
        # Connecting lines
        create_svg_line(360, 200, 440, 290, "#999", stroke_width=3),
        create_svg_line(560, 290, 640, 200, "#999", stroke_width=3),
        create_svg_line(360, 500, 440, 410, "#999", stroke_width=3),
        create_svg_line(560, 410, 640, 500, "#999", stroke_width=3),
    ]
    
    elements_code = '\n        '.join(svg_elements)
    script = generate_svg_init_script("svg-complex", 1000, 700, elements_code)
    
    content = f"""
    <div style="padding: 40px; text-align: center;">
        <h1 style="margin-bottom: 30px; color: #333;">Complex SVG.js Diagram</h1>
        {container}
        {script}
    </div>
    """
    
    html = generator._wrap_html(content, "")
    generator.export_to_png(html, Path("examples/output/svg_js_complex.png"))
    print("✓ Generated examples/output/svg_js_complex.png")


def example_flowchart():
    """Example 3: Flowchart-style diagram"""
    print("Generating Example 3: Flowchart SVG.js diagram...")
    
    generator = ModernGraphicsGenerator("SVG.js Flowchart", Attribution(), use_svg_js=True)
    
    container = generate_svg_container("svg-flowchart", 900, 500)
    
    # Flowchart elements
    svg_elements = [
        # Start node
        create_svg_rect(350, 50, 200, 60, "#4A90E2", rx=5, stroke="#2E5C8A"),
        create_svg_text(450, 85, "Start", font_size=20, fill="#FFF"),
        
        # Process nodes
        create_svg_rect(350, 150, 200, 60, "#50C878", rx=5, stroke="#2E7D4E"),
        create_svg_text(450, 185, "Process A", font_size=18, fill="#FFF"),
        
        create_svg_rect(350, 250, 200, 60, "#FF6B6B", rx=5, stroke="#CC5555"),
        create_svg_text(450, 285, "Process B", font_size=18, fill="#FFF"),
        
        # Decision node (diamond shape using path)
        'const decision = draw.path("M 400 350 L 450 380 L 500 350 L 450 320 Z").fill("#F59E0B").stroke({color: "#D97706", width: 2})',
        create_svg_text(450, 360, "Decision?", font_size=16, fill="#FFF"),
        
        # End nodes
        create_svg_rect(200, 400, 150, 60, "#8B5CF6", rx=5, stroke="#7C3AED"),
        create_svg_text(275, 435, "Yes", font_size=18, fill="#FFF"),
        
        create_svg_rect(550, 400, 150, 60, "#EF4444", rx=5, stroke="#DC2626"),
        create_svg_text(625, 435, "No", font_size=18, fill="#FFF"),
        
        # Arrows (lines)
        create_svg_line(450, 110, 450, 150, "#333", stroke_width=3),
        create_svg_line(450, 210, 450, 250, "#333", stroke_width=3),
        create_svg_line(450, 310, 450, 320, "#333", stroke_width=3),
        create_svg_line(400, 350, 275, 400, "#333", stroke_width=2),
        create_svg_line(500, 350, 625, 400, "#333", stroke_width=2),
    ]
    
    elements_code = '\n        '.join(svg_elements)
    script = generate_svg_init_script("svg-flowchart", 900, 500, elements_code)
    
    content = f"""
    <div style="padding: 40px; text-align: center;">
        <h1 style="margin-bottom: 30px; color: #333;">Flowchart with SVG.js</h1>
        {container}
        {script}
    </div>
    """
    
    html = generator._wrap_html(content, "")
    generator.export_to_png(html, Path("examples/output/svg_js_flowchart.png"))
    print("✓ Generated examples/output/svg_js_flowchart.png")


def example_custom_script():
    """Example 4: Using custom JavaScript with SVG.js"""
    print("Generating Example 4: Custom JavaScript SVG.js example...")
    
    generator = ModernGraphicsGenerator("SVG.js Custom Script", Attribution(), use_svg_js=True)
    
    container = generate_svg_container("svg-custom", 800, 600)
    
    # Custom JavaScript code
    custom_script = """
        // Create a gradient
        const gradient = draw.gradient('linear', function(stop) {
            stop.at(0, '#4A90E2')
            stop.at(1, '#8B5CF6')
        })
        
        // Create animated circle
        const circle = draw.circle(100).move(350, 250).fill(gradient)
        
        // Add text
        draw.text('SVG.js').move(360, 320).font({size: 32, family: 'Arial'}).fill('#333')
        
        // Create multiple small circles in a pattern
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2
            const x = 400 + Math.cos(angle) * 150
            const y = 300 + Math.sin(angle) * 150
            draw.circle(30).move(x - 15, y - 15).fill('#50C878').opacity(0.7)
        }
    """
    
    script = generate_svg_init_script("svg-custom", 800, 600, custom_script)
    
    content = f"""
    <div style="padding: 40px; text-align: center;">
        <h1 style="margin-bottom: 30px; color: #333;">Custom JavaScript with SVG.js</h1>
        {container}
        {script}
    </div>
    """
    
    html = generator._wrap_html(content, "")
    generator.export_to_png(html, Path("examples/output/svg_js_custom.png"))
    print("✓ Generated examples/output/svg_js_custom.png")


def main():
    """Run all SVG.js examples"""
    print("=" * 60)
    print("SVG.js Integration Examples")
    print("=" * 60)
    print()
    
    # Ensure output directory exists
    Path("examples/output").mkdir(parents=True, exist_ok=True)
    
    try:
        example_basic_svg()
        print()
        example_complex_diagram()
        print()
        example_flowchart()
        print()
        example_custom_script()
        print()
        print("=" * 60)
        print("All examples generated successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"Error generating examples: {e}")
        raise


if __name__ == "__main__":
    main()
