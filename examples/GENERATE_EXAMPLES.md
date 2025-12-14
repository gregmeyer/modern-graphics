# How to Generate Example Graphics

The example scripts create graphics when you run them. Here's how to generate examples:

## Quick Start (No AI Required)

These examples work without OpenAI API keys:

### 1. Generate All Diagram Types
```bash
python3 scripts/all_diagram_types.py
```

**Output:** `examples/output/01_cycle.png` through `12_slide_comparison.png`

### 2. Generate Batch Examples
```bash
python3 scripts/batch_generation.py
```

**Output:** `examples/output/product_cycle.png`, `feature_comparison.png`, `project_timeline.png`

### 3. Generate Attribution Examples
```bash
python3 scripts/attribution_examples.py
```

**Output:** `examples/output/attribution_*.png` (4 files)

### 3b. Generate Attribution Customization Examples (New)
```bash
python3 scripts/attribution_customization.py
```

**Output:** `examples/output/attribution_custom/*.png` (7 files showing all customization options)

### 4. Generate Export Options Examples
```bash
python3 scripts/export_options.py
```

**Output:** `examples/output/export_*.png` (5 files)

## Use Case Examples (Requires OpenAI API Key)

These require `OPENAI_API_KEY` in your `.env` file:

### 1. Tech Startup Use Case
```bash
python3 scripts/use_case_tech_startup.py
```

**Output:** `examples/output/use_cases/tech_startup/*.png` (4 files)

### 2. Corporate Use Case
```bash
python3 scripts/use_case_corporate.py
```

**Output:** `examples/output/use_cases/corporate/*.png` (4 files)

### 3. Creative Portfolio Use Case
```bash
python3 scripts/use_case_creative.py
```

**Output:** `examples/output/use_cases/creative/*.png` (4 files)

### 4. Healthcare Use Case
```bash
python3 scripts/use_case_healthcare.py
```

**Output:** `examples/output/use_cases/healthcare/*.png` (4 files)

### 5. Education Use Case
```bash
python3 scripts/use_case_education.py
```

**Output:** `examples/output/use_cases/education/*.png` (4 files)

### Run All Use Cases
```bash
python3 scripts/run_all_use_cases.py
```

## Showcase Graphics (Requires OpenAI API Key)

Generate README showcase graphics:

```bash
python3 scripts/prompts/generate_showcase.py
```

**Output:** `examples/output/showcase/[template_name]/*.png` (15 files total)

## Prompt Testing (Requires OpenAI API Key)

Test various prompt patterns:

```bash
python3 scripts/prompts/test_prompts.py
```

**Output:** `examples/output/prompt_tests/*.png` (10+ files)

## View Generated Graphics

After running scripts, view graphics:

```bash
# List all generated PNGs
find examples/output -name "*.png" -type f

# Count generated graphics
find examples/output -name "*.png" -type f | wc -l

# Open a specific graphic (macOS)
open examples/output/01_cycle.png

# Open all graphics in a directory (macOS)
open examples/output/attribution_custom/
```

## Output Directory Structure

```
examples/output/
├── 01_cycle.png                    # From all_diagram_types.py
├── 02_comparison.png
├── ...
├── use_cases/
│   ├── tech_startup/
│   │   ├── 01_product_vision.png
│   │   └── ...
│   ├── corporate/
│   ├── creative/
│   ├── healthcare/
│   └── education/
├── showcase/
│   ├── minimalist/
│   │   ├── cycle.png
│   │   ├── comparison.png
│   │   └── story_slide.png
│   ├── tech_startup/
│   └── comparison/
└── prompt_tests/
    └── [category]_[name].png
```

## Requirements

### For Basic Examples (No AI)
- Python 3.8+
- `playwright` and `pillow` installed
- `playwright install chromium` run

### For AI Examples
- Everything above, plus:
- `OPENAI_API_KEY` in `.env` file
- `pip install -e ".[ai]"` to install OpenAI package

## Troubleshooting

**No graphics generated:**
- Make sure you've run the scripts
- Check that Playwright is installed: `playwright install chromium`
- Verify output directory exists: `ls examples/output/`

**AI examples fail:**
- Check `.env` file has `OPENAI_API_KEY`
- Verify OpenAI package installed: `pip list | grep openai`
- Check API key is valid

**Graphics are low quality:**
- This is normal for quick examples
- Use `export_options.py` to see quality options
- Adjust `device_scale_factor` in export calls for higher quality
