"""Example: Hero slides with corporate theme

Demonstrates that hero slides support custom CSS schemes with a corporate theme:
- Professional serif font (Georgia/Times)
- Muted blues and grays
- Conservative, trustworthy aesthetic
- Clean, minimal styling
"""

from pathlib import Path
from modern_graphics import ModernGraphicsGenerator
from modern_graphics.templates import StyleTemplate

# Corporate theme template
CORPORATE_TEMPLATE = StyleTemplate(
    name="corporate",
    colors={},
    base_styles="""
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #ffffff;
            color: #1a1a1a;
            padding: 0;
        }
        
        @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&display=swap');
    """,
    attribution_styles="""
        .attribution {
            font-size: 11px;
            color: #64748b;
            opacity: 0.8;
            padding: 8px;
            text-align: center;
        }
    """,
    font_family="'Lora', Georgia, serif",
    background_color="#ffffff"
)

print("Creating hero slides with corporate theme...")
generator = ModernGraphicsGenerator(
    title="Corporate Theme Examples",
    template=CORPORATE_TEMPLATE,
    use_svg_js=True
)

# Corporate color scheme CSS override - more aggressive styling
corporate_css = """
        /* Corporate color palette: muted blues and grays */
        body {
            font-family: 'Lora', Georgia, serif !important;
            background: #f5f7fa !important;
        }
        
        /* Hero slide overrides - corporate professional look */
        .hero {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
            border: 2px solid #e2e8f0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255,255,255,0.9) !important;
        }
        
        .hero .halo {
            background: radial-gradient(circle at 30% 25%, rgba(37, 99, 235, 0.15), transparent 55%) !important;
        }
        
        .eyebrow {
            color: #64748b !important;
            font-weight: 600 !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .headline {
            color: #1e293b !important;
            font-weight: 700 !important;
            font-family: 'Lora', Georgia, serif !important;
            letter-spacing: -0.02em !important;
        }
        
        .subhead {
            color: #475569 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        /* Stats styling */
        .stat {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04) !important;
        }
        
        .stat span {
            color: #64748b !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .stat strong {
            color: #2563eb !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        /* Highlight tiles - corporate style */
        .hero-body li {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            color: #334155 !important;
            font-family: 'Lora', Georgia, serif !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        }
        
        .tile {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            color: #1e293b !important;
            font-family: 'Lora', Georgia, serif !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06) !important;
        }
        
        .tile-label {
            color: #334155 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .tile-icon svg {
            opacity: 0.8 !important;
        }
        
        /* Remove purple/colorful elements - override all purple references */
        .tile::after {
            background: linear-gradient(90deg, rgba(37, 99, 235, 0.15), rgba(37, 99, 235, 0.05)) !important;
        }
        
        .hero-flow-curved .tile-flow::before {
            border-color: rgba(37, 99, 235, 0.15) !important;
        }
        
        .hero-flow-curved .tile-flow::after {
            border-color: rgba(37, 99, 235, 0.3) !important;
        }
        
        .hero-flow-constellation .tile-flow::before {
            border-color: rgba(37, 99, 235, 0.1) !important;
        }
        
        .hero-flow-constellation .tile-flow::after {
            border-color: rgba(37, 99, 235, 0.2) !important;
        }
        
        .hero-flow-constellation .tile::before {
            border-color: rgba(37, 99, 235, 0.12) !important;
        }
        
        .flowchart-area::after {
            border-color: rgba(37, 99, 235, 0.06) !important;
        }
        
        /* Flowchart nodes - corporate style */
        .flow-node {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08) !important;
        }
        
        .flow-node .node-label {
            color: #1e293b !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .flow-svg path {
            stroke: rgba(37, 99, 235, 0.3) !important;
        }
        
        /* Ribbon panels - corporate style */
        .ribbon-panel {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            color: #1e293b !important;
        }
        
        .ribbon-label {
            font-family: 'Lora', Georgia, serif !important;
        }
        
        /* CTA styling */
        .cta {
            color: #2563eb !important;
            font-family: 'Lora', Georgia, serif !important;
        }
"""

# Example 1: Open Canvas with Highlight Tiles
print("\n1. Creating open canvas hero with highlight tiles...")
html1 = generator.generate_modern_hero(
    eyebrow="Business Strategy",
    headline="Transform Your Revenue Model",
    subheadline="Shift from upfront licenses to subscription-based revenue for predictable growth",
    highlights=[
        "Predictable revenue streams",
        "Higher customer retention",
        "Scalable business model"
    ],
    stats=[
        {"label": "ARR Growth", "value": "+24% QoQ"},
        {"label": "Retention Rate", "value": "92%"},
        {"label": "Churn", "value": "4%"}
    ]
)

# Inject corporate CSS
html1 = html1.replace('</style>', f'{corporate_css}\n    </style>', 1)

output1 = Path("examples/output/corporate-hero-open.png")
generator.export_to_png(
    html1,
    output1,
    viewport_width=2400,
    viewport_height=1600,
    padding=40
)
print(f"✓ Saved: {output1}")

# Example 2: Dark variant (but with corporate muted colors)
print("\n2. Creating corporate dark variant hero...")
html2 = generator.generate_modern_hero(
    eyebrow="Enterprise Solutions",
    headline="Modern Infrastructure for Scale",
    subheadline="Built for enterprise needs with reliability and performance at the core",
    highlights=[
        "99.9% uptime SLA",
        "Enterprise-grade security",
        "24/7 support"
    ],
    stats=[
        {"label": "Uptime", "value": "99.9%"},
        {"label": "Response Time", "value": "<50ms"},
        {"label": "Customers", "value": "500+"}
    ],
    background_variant="dark"
)

# Corporate dark theme CSS - more distinct
corporate_dark_css = """
        body {
            font-family: 'Lora', Georgia, serif !important;
            background: #0f172a !important;
        }
        
        .hero-dark {
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%) !important;
            border: 2px solid #334155 !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        }
        
        .hero-dark .halo {
            background: radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.25), transparent 60%) !important;
        }
        
        .hero-dark .eyebrow {
            color: #94a3b8 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .headline {
            color: #f1f5f9 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .subhead {
            color: #cbd5e1 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .stat {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid #334155 !important;
        }
        
        .hero-dark .stat span {
            color: #94a3b8 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .stat strong {
            color: #60a5fa !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .hero-body li {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid #334155 !important;
            color: #e2e8f0 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .tile {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid #334155 !important;
            color: #e2e8f0 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .tile-label {
            color: #e2e8f0 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .flow-node {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid #334155 !important;
            color: #e2e8f0 !important;
        }
        
        .hero-dark .flow-node .node-label {
            color: #e2e8f0 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .hero-dark .flow-svg path {
            stroke: rgba(96, 165, 250, 0.4) !important;
        }
        
        .hero-dark .cta {
            color: #60a5fa !important;
            font-family: 'Lora', Georgia, serif !important;
        }
"""

html2 = html2.replace('</style>', f'{corporate_dark_css}\n    </style>', 1)

output2 = Path("examples/output/corporate-hero-dark.png")
generator.export_to_png(
    html2,
    output2,
    viewport_width=2400,
    viewport_height=1600,
    padding=40
)
print(f"✓ Saved: {output2}")

# Example 3: Triptych layout
print("\n3. Creating corporate triptych hero...")
html3 = generator.generate_modern_hero_triptych(
    eyebrow="Three Pillars of Success",
    headline="Build a Foundation for Growth",
    subheadline="Three core principles that drive sustainable business expansion",
    columns=[
        {
            "title": "Strategy",
            "items": ["Data-driven decision making", "Long-term planning", "Market analysis"],
            "icon": "manual"
        },
        {
            "title": "Execution",
            "items": ["Agile operations", "Team collaboration", "Process optimization"],
            "icon": "templates"
        },
        {
            "title": "Results",
            "items": ["Measurable outcomes", "Performance metrics", "Continuous improvement"],
            "icon": "generated"
        }
    ]
)

# Additional triptych-specific corporate styling
corporate_triptych_css = corporate_css + """
        .hero-triptych {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
            border: 2px solid #e2e8f0 !important;
        }
        
        .soft-orbit circle {
            fill: rgba(37, 99, 235, 0.1) !important;
            stroke: rgba(100, 116, 139, 0.15) !important;
        }
        
        .panel {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
        }
        
        .panel:nth-child(2) {
            background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%) !important;
            border-color: #94a3b8 !important;
        }
        
        .panel-title {
            color: #1e293b !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .panel ul {
            color: #475569 !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .panel ul li::before {
            background: #2563eb !important;
        }
        
        /* Override purple gradient in triptych orbit */
        .soft-orbit circle[fill*="E4D7FF"],
        .soft-orbit circle[fill*="D5C8FA"] {
            fill: rgba(37, 99, 235, 0.1) !important;
        }
        
        .soft-orbit circle[fill="#E0D0FF"],
        .soft-orbit circle[fill="#CABAF6"],
        .soft-orbit circle[fill="#DDD6FE"] {
            fill: rgba(37, 99, 235, 0.2) !important;
        }
        
        /* Override purple in gradient definitions */
        defs stop[stop-color*="E4D7FF"],
        defs stop[stop-color*="D5C8FA"] {
            stop-color: rgba(37, 99, 235, 0.15) !important;
        }
        
        .stats .stat {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
        }
        
        .stats .stat span {
            color: #64748b !important;
            font-family: 'Lora', Georgia, serif !important;
        }
        
        .stats .stat strong {
            color: #2563eb !important;
            font-family: 'Lora', Georgia, serif !important;
        }
"""

html3 = html3.replace('</style>', f'{corporate_triptych_css}\n    </style>', 1)

output3 = Path("examples/output/corporate-hero-triptych.png")
generator.export_to_png(
    html3,
    output3,
    viewport_width=2400,
    viewport_height=1600,
    padding=40
)
print(f"✓ Saved: {output3}")

print("\n✓ Corporate theme hero slides generated successfully!")
print("\nCorporate Theme Characteristics:")
print("  - Font: Lora (serif) - professional and trustworthy")
print("  - Colors: Muted blues (#2563eb) and grays (#64748b)")
print("  - Style: Clean, minimal, conservative")
print("  - Background: White/light gray (#f8fafc)")
print("\nFiles created:")
print(f"  - {output1}")
print(f"  - {output2}")
print(f"  - {output3}")
