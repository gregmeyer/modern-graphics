# Tests Directory

This directory contains test files and test output.

## Structure

- `output/` - Test output files (PNGs, HTMLs) - **excluded from git**
- `*.py` - Test scripts (if any)

## Usage

Test files generated during development should be placed in `tests/output/` to keep them organized and excluded from version control.

Example:
```python
from pathlib import Path
from modern_graphics import ModernGraphicsGenerator

gen = ModernGraphicsGenerator("Test")
html = gen.generate_cycle_diagram([...])
gen.export_to_png(html, Path("tests/output/test_diagram.png"))
```
