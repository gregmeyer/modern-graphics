"""Example: Same slide cards with different CSS scheme

Demonstrates that the same slide cards can be generated with:
- Different base font (serif instead of sans-serif)
- Different color scheme (dark theme with different accent colors)
- Different overall styling

This proves the system's flexibility and customizability.
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator
from modern_graphics.templates import StyleTemplate

# Define a custom template with different font and colors
CUSTOM_TEMPLATE = StyleTemplate(
    name="serif-dark",
    colors={},  # We'll override colors in CSS
    base_styles="""
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #1a1a1a;
            color: #e0e0e0;
            padding: 40px 20px;
        }
        
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&display=swap');
    """,
    attribution_styles="""
        .attribution {
            font-size: 11px;
            color: #888;
            opacity: 0.7;
            padding: 8px;
            text-align: center;
        }
    """,
    font_family="'Merriweather', Georgia, serif",
    background_color="#1a1a1a"
)

# Same card data as the original example
cards_group = [
    {
        "title": "Data Pipeline",
        "tagline": "Automated Processing",
        "subtext": "Streamlined data flow from source to destination",
        "color": "blue",
        "badge": "Active",
        "features": [
            "Real-time sync",
            "Error handling",
            "Scalable architecture"
        ],
        "custom_mockup": """
            // Canvas dimensions: 240x140
            const width = 240;
            const height = 140;
            const padding = 15;
            const safeMargin = 10;
            
            // Node properties
            const nodeRadius = 25;
            const nodeSpacing = 70;
            const startX = padding + nodeRadius;
            const centerY = height / 2;
            
            // Create nodes with bounds checking
            const node1X = Math.max(startX, Math.min(width - padding - nodeRadius, startX));
            const node2X = Math.max(startX + nodeSpacing, Math.min(width - padding - nodeRadius, startX + nodeSpacing));
            const node3X = Math.max(startX + nodeSpacing * 2, Math.min(width - padding - nodeRadius, startX + nodeSpacing * 2));
            const nodeY = Math.max(padding + nodeRadius, Math.min(height - padding - nodeRadius - 20, centerY));
            
            const node1 = draw.circle(nodeRadius * 2).move(node1X - nodeRadius, nodeY - nodeRadius)
                .fill('#60A5FA').opacity(0.9);
            const node2 = draw.circle(nodeRadius * 2).move(node2X - nodeRadius, nodeY - nodeRadius)
                .fill('#34D399').opacity(0.9);
            const node3 = draw.circle(nodeRadius * 2).move(node3X - nodeRadius, nodeY - nodeRadius)
                .fill('#F87171').opacity(0.9);
            
            // Add labels with bounds checking
            const labelY = Math.min(nodeY + nodeRadius + 15, height - safeMargin);
            draw.text('Source').move(Math.max(safeMargin, node1X - 20), labelY)
                .font({size: 10, family: 'Merriweather'}).fill('#E0E0E0');
            draw.text('Process').move(Math.max(safeMargin, node2X - 25), labelY)
                .font({size: 10, family: 'Merriweather'}).fill('#E0E0E0');
            draw.text('Output').move(Math.max(safeMargin, node3X - 25), labelY)
                .font({size: 10, family: 'Merriweather'}).fill('#E0E0E0');
            
            // Add arrows with bounds checking
            const arrowStart1 = Math.min(node1X + nodeRadius, node2X - nodeRadius);
            const arrowEnd1 = Math.max(node1X + nodeRadius, node2X - nodeRadius);
            const arrowStart2 = Math.min(node2X + nodeRadius, node3X - nodeRadius);
            const arrowEnd2 = Math.max(node2X + nodeRadius, node3X - nodeRadius);
            draw.line(arrowStart1, nodeY, arrowEnd1, nodeY).stroke({width: 2, color: '#60A5FA'});
            draw.line(arrowStart2, nodeY, arrowEnd2, nodeY).stroke({width: 2, color: '#60A5FA'});
        """
    },
    {
        "title": "Analytics Dashboard",
        "tagline": "Real-time Insights",
        "subtext": "Visualize key metrics and trends",
        "color": "purple",
        "badge": "New",
        "features": [
            "Interactive charts",
            "Custom reports",
            "Export capabilities"
        ],
        "custom_mockup": """
            // Canvas dimensions: 240x140
            const width = 240;
            const height = 140;
            const padding = 15;
            const safeMargin = 10;
            const chartBottom = height - padding - 20;
            const chartTop = padding + 10;
            const chartHeight = chartBottom - chartTop;
            
            // Bar chart with bounds checking
            const barWidth = 18;
            const barSpacing = 25;
            const startX = padding + 10;
            
            const bars = [
                {x: startX, height: 40},
                {x: startX + barSpacing, height: 50},
                {x: startX + barSpacing * 2, height: 35},
                {x: startX + barSpacing * 3, height: 60},
                {x: startX + barSpacing * 4, height: 45}
            ];
            
            bars.forEach((bar, i) => {
                const x = Math.max(safeMargin, Math.min(width - safeMargin - barWidth, bar.x));
                const barHeight = Math.min(bar.height, chartHeight);
                const y = Math.max(chartTop, chartBottom - barHeight);
                draw.rect(barWidth, barHeight).move(x, y).fill('#A78BFA').opacity(0.85);
            });
        """
    }
]

single_card = [
    {
        "title": "Network Architecture",
        "tagline": "Distributed System",
        "subtext": "Scalable microservices architecture",
        "color": "green",
        "badge": "Production",
        "features": [
            "Load balancing",
            "Service mesh",
            "Auto-scaling"
        ],
        "custom_mockup": """
            // Canvas dimensions: 240x140
            const width = 240;
            const height = 140;
            const padding = 15;
            const safeMargin = 10;
            
            // Central hub with bounds checking
            const hubRadius = 20;
            const hubX = Math.max(padding + hubRadius, Math.min(width - padding - hubRadius, width / 2));
            const hubY = Math.max(padding + hubRadius, Math.min(height - padding - hubRadius - 20, height / 2));
            
            const hub = draw.circle(hubRadius * 2).move(hubX - hubRadius, hubY - hubRadius)
                .fill('#34D399').opacity(0.9);
            
            const hubLabelY = Math.min(hubY + hubRadius + 12, height - safeMargin);
            draw.text('Hub').move(Math.max(safeMargin, hubX - 15), hubLabelY)
                .font({size: 10, family: 'Merriweather', weight: 'bold'}).fill('#E0E0E0');
            
            // Nodes around hub with bounds checking
            const nodeRadius = 18;
            const nodeDistance = 50;
            const nodes = [
                {angle: -Math.PI/2, label: 'API'},
                {angle: 0, label: 'DB'},
                {angle: Math.PI/2, label: 'Cache'},
                {angle: Math.PI, label: 'Queue'}
            ];
            
            nodes.forEach(node => {
                const nodeX = Math.max(padding + nodeRadius, 
                    Math.min(width - padding - nodeRadius, hubX + Math.cos(node.angle) * nodeDistance));
                const nodeY = Math.max(padding + nodeRadius, 
                    Math.min(height - padding - nodeRadius - 20, hubY + Math.sin(node.angle) * nodeDistance));
                
                const circle = draw.circle(nodeRadius * 2).move(nodeX - nodeRadius, nodeY - nodeRadius)
                    .fill('#34D399').opacity(0.7);
                
                const labelY = Math.min(nodeY + nodeRadius + 12, height - safeMargin);
                const labelX = Math.max(safeMargin, Math.min(width - safeMargin - 30, nodeX - 15));
                draw.text(node.label).move(labelX, labelY)
                    .font({size: 9, family: 'Merriweather'}).fill('#E0E0E0');
                
                // Connection lines with bounds checking
                const startX = Math.max(safeMargin, Math.min(width - safeMargin, nodeX));
                const startY = Math.max(safeMargin, Math.min(height - safeMargin, nodeY));
                const endX = Math.max(safeMargin, Math.min(width - safeMargin, hubX));
                const endY = Math.max(safeMargin, Math.min(height - safeMargin, hubY));
                draw.line(startX, startY, endX, endY)
                    .stroke({width: 1.5, color: '#34D399'}).opacity(0.6);
            });
        """
    }
]

# Generate with custom template (dark theme, serif font)
print("Creating slide cards with custom CSS scheme (dark theme + serif font)...")
generator_custom = ModernGraphicsGenerator(
    title="Custom Theme Examples",
    template=CUSTOM_TEMPLATE,
    use_svg_js=True
)

# Generate HTML with custom styling
html_group_custom = generator_custom.generate_slide_card_diagram(cards_group)

# Inject custom dark theme CSS for cards
custom_card_css = """
        .slide-card {
            background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 24px 48px rgba(0, 0, 0, 0.5), 0 8px 16px rgba(0, 0, 0, 0.3) !important;
        }
        
        .card-title {
            color: #E0E0E0 !important;
        }
        
        .card-tagline {
            color: #B0B0B0 !important;
        }
        
        .card-subtext {
            color: #888 !important;
        }
        
        .card-feature {
            color: #C0C0C0 !important;
        }
        
        .card-badge {
            background: rgba(255, 255, 255, 0.15) !important;
            color: #E0E0E0 !important;
        }
        
        .card-mockup {
            background: rgba(0, 0, 0, 0.4) !important;
        }
        
        .title {
            color: #E0E0E0 !important;
        }
"""

# Inject the CSS into the HTML
html_group_custom = html_group_custom.replace('</style>', f'{custom_card_css}\n    </style>', 1)

output_path_group_custom = Path("examples/output/custom-theme-two-cards.png")
generator_custom.export_to_png(
    html_group_custom, 
    output_path_group_custom,
    viewport_width=800,
    viewport_height=600,
    padding=20
)
print(f"✓ Saved: {output_path_group_custom}")

html_single_custom = generator_custom.generate_slide_card_diagram(single_card)
html_single_custom = html_single_custom.replace('</style>', f'{custom_card_css}\n    </style>', 1)

output_path_single_custom = Path("examples/output/custom-theme-single-card.png")
generator_custom.export_to_png(
    html_single_custom, 
    output_path_single_custom,
    viewport_width=500,
    viewport_height=600,
    padding=20
)
print(f"✓ Saved: {output_path_single_custom}")

print("\n✓ Custom theme examples generated successfully!")
print("\nComparison:")
print("  Original: Light theme, Inter font (sans-serif)")
print("  Custom:   Dark theme, Merriweather font (serif)")
print("\nFiles created:")
print(f"  - {output_path_group_custom}")
print(f"  - {output_path_single_custom}")
