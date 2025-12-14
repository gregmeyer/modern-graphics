"""Aggregate prompts from all use cases for evaluation

Collects all prompts stored by use case examples into a single file for easy evaluation.
"""

import json
from pathlib import Path
from datetime import datetime
from prompt_storage import load_prompts


def aggregate_all_prompts():
    """Aggregate prompts from all use case directories"""
    
    examples_dir = Path(__file__).parent.parent / "examples"
    output_base = examples_dir / "output" / "generated" / "use_cases"
    
    use_cases = ["tech_startup", "corporate", "education", "healthcare", "creative"]
    
    all_prompts = []
    use_case_stats = {}
    
    for use_case in use_cases:
        use_case_dir = output_base / use_case
        prompts_file = use_case_dir / "prompts_used.json"
        
        prompts = load_prompts(prompts_file)
        all_prompts.extend(prompts)
        use_case_stats[use_case] = len(prompts)
    
    # Create aggregated output
    aggregated_file = output_base / "all_prompts.json"
    aggregated_data = {
        "generated_at": datetime.now().isoformat(),
        "total_prompts": len(all_prompts),
        "use_case_stats": use_case_stats,
        "prompts": all_prompts
    }
    
    with open(aggregated_file, 'w') as f:
        json.dump(aggregated_data, f, indent=2)
    
    print("=" * 60)
    print("Prompt Aggregation Complete")
    print("=" * 60)
    print(f"\nTotal prompts collected: {len(all_prompts)}")
    print("\nBy use case:")
    for use_case, count in use_case_stats.items():
        print(f"  - {use_case}: {count} prompts")
    print(f"\nAggregated file: {aggregated_file.absolute()}")
    print("\nThis file can be used for evaluation with:")
    print("  - Prompt text")
    print("  - Output image paths")
    print("  - Metadata (use case, slide type, etc.)")
    print("=" * 60)
    
    return aggregated_file


if __name__ == "__main__":
    aggregate_all_prompts()
