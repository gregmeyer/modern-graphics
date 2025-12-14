#!/usr/bin/env python3
"""CLI command for interactive template creation"""

import argparse
from .template_interview import interview_for_template, quick_template_from_description
from .templates import register_template
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Create a template through an AI-assisted interview'
    )
    parser.add_argument(
        '--quick',
        type=str,
        help='Quick mode: generate template from description (e.g., "dark professional theme")'
    )
    parser.add_argument(
        '--model',
        default='gpt-4',
        help='OpenAI model to use (default: gpt-4)'
    )
    parser.add_argument(
        '--register',
        action='store_true',
        help='Automatically register the template after creation'
    )
    parser.add_argument(
        '--save',
        type=str,
        help='Save template to JSON file'
    )
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            print(f"🚀 Quick mode: Generating template from description...")
            print(f"   Description: {args.quick}\n")
            template = quick_template_from_description(args.quick, model=args.model)
        else:
            template = interview_for_template(model=args.model)
        
        if template:
            print(f"\n📋 Template Details:")
            print(f"   Name: {template.name}")
            print(f"   Colors: {', '.join(template.colors.keys())}")
            print(f"   Font: {template.font_family}")
            print(f"   Background: {template.background_color}")
            
            if args.register:
                register_template(template)
                print(f"\n✓ Template '{template.name}' registered!")
            
            if args.save:
                import json
                template_dict = {
                    "name": template.name,
                    "colors": template.colors,
                    "base_styles": template.base_styles,
                    "attribution_styles": template.attribution_styles,
                    "font_family": template.font_family,
                    "background_color": template.background_color
                }
                output_path = Path(args.save)
                output_path.write_text(json.dumps(template_dict, indent=2))
                print(f"✓ Template saved to {output_path}")
        else:
            print("\n⚠️  Template creation cancelled or failed.")
            return 1
            
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        return 1
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("   Install with: pip install openai")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
