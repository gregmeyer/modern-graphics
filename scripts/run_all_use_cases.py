"""Run all use case examples

This script runs all use case examples to generate graphics for the repository.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
# Add scripts directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from use_case_tech_startup import *
from use_case_corporate import *
from use_case_creative import *
from use_case_healthcare import *
from use_case_education import *

print("\n" + "=" * 60)
print("All use case examples completed!")
print("=" * 60)
print("\nGenerated graphics are in:")
print("  examples/output/use_cases/")
print("\nSubdirectories:")
print("  - tech_startup/")
print("  - corporate/")
print("  - creative/")
print("  - healthcare/")
print("  - education/")
