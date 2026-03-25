"""Example: Slide cards with custom SVG.js mockups

Demonstrates:
1. Two slide cards side by side with custom SVG.js mockups
2. Single slide card with custom SVG.js mockup
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator

# Initialize generator with SVG.js enabled
generator = ModernGraphicsGenerator(
    title="Custom Mockup Examples",
    use_svg_js=True
)

# Example 1: Two slide cards with custom SVG.js mockups
print("Creating two-card group with custom SVG.js mockups...")

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
        # Custom SVG.js mockup - flowchart style with proper bounds checking
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
                .fill('#007AFF').opacity(0.8);
            const node2 = draw.circle(nodeRadius * 2).move(node2X - nodeRadius, nodeY - nodeRadius)
                .fill('#34C759').opacity(0.8);
            const node3 = draw.circle(nodeRadius * 2).move(node3X - nodeRadius, nodeY - nodeRadius)
                .fill('#FF9500').opacity(0.8);
            
            // Add labels with bounds checking
            const labelY = Math.min(nodeY + nodeRadius + 15, height - safeMargin);
            draw.text('Source').move(Math.max(safeMargin, node1X - 20), labelY)
                .font({size: 10, family: 'Inter'}).fill('#1D1D1F');
            draw.text('Process').move(Math.max(safeMargin, node2X - 25), labelY)
                .font({size: 10, family: 'Inter'}).fill('#1D1D1F');
            draw.text('Output').move(Math.max(safeMargin, node3X - 25), labelY)
                .font({size: 10, family: 'Inter'}).fill('#1D1D1F');
            
            // Add arrows with bounds checking
            const arrowStart1 = Math.min(node1X + nodeRadius, node2X - nodeRadius);
            const arrowEnd1 = Math.max(node1X + nodeRadius, node2X - nodeRadius);
            const arrowStart2 = Math.min(node2X + nodeRadius, node3X - nodeRadius);
            const arrowEnd2 = Math.max(node2X + nodeRadius, node3X - nodeRadius);
            draw.line(arrowStart1, nodeY, arrowEnd1, nodeY).stroke({width: 2, color: '#007AFF'});
            draw.line(arrowStart2, nodeY, arrowEnd2, nodeY).stroke({width: 2, color: '#007AFF'});
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
        # Custom SVG.js mockup - chart style with proper bounds checking
        "custom_mockup": """
            // Canvas dimensions: 240x140
            const width = 240;
            const height = 140;
            const padding = 15;
            const safeMargin = 10;
            const chartBottom = height - padding - 20; // Space for labels
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
                draw.rect(barWidth, barHeight).move(x, y).fill('#AF52DE').opacity(0.7);
            });
            
            // Trend line with bounds checking
            const points = [
                {x: startX + barWidth/2, y: chartBottom - 40},
                {x: startX + barSpacing + barWidth/2, y: chartBottom - 50},
                {x: startX + barSpacing * 2 + barWidth/2, y: chartBottom - 35},
                {x: startX + barSpacing * 3 + barWidth/2, y: chartBottom - 60},
                {x: startX + barSpacing * 4 + barWidth/2, y: chartBottom - 45}
            ];
            
            const pathData = points.map((p, i) => {
                const x = Math.max(safeMargin, Math.min(width - safeMargin, p.x));
                const y = Math.max(chartTop, Math.min(chartBottom, p.y));
                return (i === 0 ? 'M' : 'L') + ' ' + x + ' ' + y;
            }).join(' ');
            
            draw.path(pathData).stroke({width: 2, color: '#AF52DE'}).fill('none');
            
            // Data points with bounds checking
            points.forEach((p) => {
                const x = Math.max(safeMargin + 2, Math.min(width - safeMargin - 2, p.x));
                const y = Math.max(chartTop + 2, Math.min(chartBottom - 2, p.y));
                draw.circle(4).move(x - 2, y - 2).fill('#AF52DE');
            });
        """
    }
]

html_group = generator.generate_slide_card_diagram(cards_group)
output_path_group = Path("examples/output/custom-mockup-two-cards.png")
# Tight crop for two cards: ~700px wide (2 cards + gap) x ~500px tall
generator.export_to_png(
    html_group, 
    output_path_group,
    viewport_width=800,
    viewport_height=600,
    padding=20
)
print(f"✓ Saved: {output_path_group}")

# Example 2: Single slide card with custom SVG.js mockup
print("\nCreating single card with custom SVG.js mockup...")

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
        # Custom SVG.js mockup - network diagram style with proper bounds checking
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
                .fill('#1B7A4E').opacity(0.8);
            
            const hubLabelY = Math.min(hubY + hubRadius + 12, height - safeMargin);
            draw.text('Hub').move(Math.max(safeMargin, hubX - 15), hubLabelY)
                .font({size: 10, family: 'Inter', weight: 'bold'}).fill('#1D1D1F');
            
            // Nodes around hub with bounds checking
            const nodeRadius = 18;
            const nodeDistance = 50;
            const nodes = [
                {angle: -Math.PI/2, label: 'API'},      // Top
                {angle: 0, label: 'DB'},                // Right
                {angle: Math.PI/2, label: 'Cache'},      // Bottom
                {angle: Math.PI, label: 'Queue'}        // Left
            ];
            
            nodes.forEach(node => {
                const nodeX = Math.max(padding + nodeRadius, 
                    Math.min(width - padding - nodeRadius, hubX + Math.cos(node.angle) * nodeDistance));
                const nodeY = Math.max(padding + nodeRadius, 
                    Math.min(height - padding - nodeRadius - 20, hubY + Math.sin(node.angle) * nodeDistance));
                
                const circle = draw.circle(nodeRadius * 2).move(nodeX - nodeRadius, nodeY - nodeRadius)
                    .fill('#34C759').opacity(0.6);
                
                const labelY = Math.min(nodeY + nodeRadius + 12, height - safeMargin);
                const labelX = Math.max(safeMargin, Math.min(width - safeMargin - 30, nodeX - 15));
                draw.text(node.label).move(labelX, labelY)
                    .font({size: 9, family: 'Inter'}).fill('#1D1D1F');
                
                // Connection lines with bounds checking
                const startX = Math.max(safeMargin, Math.min(width - safeMargin, nodeX));
                const startY = Math.max(safeMargin, Math.min(height - safeMargin, nodeY));
                const endX = Math.max(safeMargin, Math.min(width - safeMargin, hubX));
                const endY = Math.max(safeMargin, Math.min(height - safeMargin, hubY));
                draw.line(startX, startY, endX, endY)
                    .stroke({width: 1.5, color: '#1B7A4E'}).opacity(0.4);
            });
        """
    }
]

html_single = generator.generate_slide_card_diagram(single_card)
output_path_single = Path("examples/output/custom-mockup-single-card.png")
# Tight crop for single card: ~400px wide x ~500px tall
generator.export_to_png(
    html_single, 
    output_path_single,
    viewport_width=500,
    viewport_height=600,
    padding=20
)
print(f"✓ Saved: {output_path_single}")

print("\n✓ All examples generated successfully!")
print("\nFiles created:")
print(f"  - {output_path_group}")
print(f"  - {output_path_single}")
