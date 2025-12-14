"""Example: Batch generation of multiple graphics

This example shows how to generate multiple graphics efficiently,
useful for creating a series of diagrams or processing data in bulk.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modern_graphics import ModernGraphicsGenerator, Attribution

# Output directory (goes to generated/ for temporary outputs)
output_dir = Path(__file__).parent.parent / "examples" / "output" / "generated"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize generator (reuse for efficiency)
generator = ModernGraphicsGenerator("Batch Generation", attribution=Attribution())

# Data: List of diagrams to generate
diagrams_data = [
    {
        'type': 'cycle',
        'title': 'Product Development Cycle',
        'steps': [
            {'text': 'Research', 'color': 'blue'},
            {'text': 'Design', 'color': 'green'},
            {'text': 'Develop', 'color': 'orange'},
            {'text': 'Test', 'color': 'purple'}
        ],
        'filename': 'product_cycle.png'
    },
    {
        'type': 'comparison',
        'title': 'Feature Comparison',
        'left_column': {'title': 'Basic Plan', 'steps': ['Feature A', 'Feature B']},
        'right_column': {'title': 'Pro Plan', 'steps': ['Feature A', 'Feature B', 'Feature C', 'Feature D']},
        'filename': 'feature_comparison.png'
    },
    {
        'type': 'timeline',
        'title': 'Project Timeline',
        'events': [
            {'date': 'Week 1', 'text': 'Kickoff - Project start', 'color': 'blue'},
            {'date': 'Week 2-3', 'text': 'Sprint 1 - First iteration', 'color': 'green'},
            {'date': 'Week 4-5', 'text': 'Sprint 2 - Second iteration', 'color': 'orange'},
            {'date': 'Week 6', 'text': 'Launch - Go live', 'color': 'purple'}
        ],
        'filename': 'project_timeline.png'
    }
]

print(f"Generating {len(diagrams_data)} diagrams...\n")

# Generate each diagram
for i, data in enumerate(diagrams_data, 1):
    print(f"{i}. Generating {data['type']} diagram: {data['filename']}")
    
    try:
        if data['type'] == 'cycle':
            html = generator.generate_cycle_diagram(data['steps'])
        elif data['type'] == 'comparison':
            html = generator.generate_comparison_diagram(
                left_column=data.get('left_column', {}),
                right_column=data.get('right_column', {})
            )
        elif data['type'] == 'timeline':
            html = generator.generate_timeline_diagram(
                events=data.get('events', []),
                orientation=data.get('orientation', 'horizontal')
            )
        else:
            print(f"   ⚠️  Unknown diagram type: {data['type']}")
            continue
        
        # Export to PNG
        output_path = output_dir / data['filename']
        generator.export_to_png(html, output_path)
        print(f"   ✓ Saved: {data['filename']}")
        
    except Exception as e:
        print(f"   ✗ Error generating {data['filename']}: {e}")

print(f"\n✓ Batch generation complete!")
print(f"   Output directory: {output_dir.absolute()}")
