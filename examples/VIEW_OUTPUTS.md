# Where to View Generated Outputs

All generated images and prompts are stored in the `examples/output/generated/` directory.

## Quick Access Paths

### Temperature Effects Demo (Creative Example)
**Location:** `examples/output/generated/temperature_demo/`

**Files:**
- `temperature_0.3.png` - Low temperature (deterministic, focused)
- `temperature_0.8.png` - Medium temperature (balanced, default)
- `temperature_1.2.png` - High temperature (creative, varied)
- `temperature_1.5.png` - Very high temperature (highly creative)
- `prompts_used.json` - All prompts with model & temperature metadata

**Full path:**
```
/Users/grmeyer/playground/writing/utils/modern-graphics/examples/output/generated/temperature_demo/
```

### Use Case Examples

#### Tech Startup
**Location:** `examples/output/generated/use_cases/tech_startup/`
- `01_product_vision.png` - AI platform transformation story
- `02_comparison.png` - Before/after comparison
- `03_growth_timeline.png` - Growth timeline
- `04_revenue_vs_users.png` - Combo chart (revenue vs users)
- `prompts_used.json` - Stored prompts with metadata

#### Corporate
**Location:** `examples/output/generated/use_cases/corporate/`
- `01_q4_performance.png` - Q4 performance story slide
- `prompts_used.json` - Stored prompts

#### Education
**Location:** `examples/output/generated/use_cases/education/`
- `01_student_progress.png` - Student progress story slide
- `prompts_used.json` - Stored prompts

#### Healthcare
**Location:** `examples/output/generated/use_cases/healthcare/`
- `01_findings.png` - Research findings story slide
- `prompts_used.json` - Stored prompts

#### Creative
**Location:** `examples/output/generated/use_cases/creative/`
- `01_portfolio_growth.png` - Portfolio growth story slide
- `prompts_used.json` - Stored prompts

### Story Slide Examples
**Location:** `examples/output/generated/story_slides/`
- `01_unified_single_chart.png` - Single chart visualization hero
- `02_unified_combo_chart.png` - Combo chart visualization hero
- `03_combo_chart_standalone.png` - Standalone combo chart
- `04_legacy_with_prompt.png` - Legacy API with prompt
- `05_legacy_parameters.png` - Legacy parameter-based

## Viewing Options

### Option 1: File Browser
Open Finder (macOS) and navigate to:
```
/Users/grmeyer/playground/writing/utils/modern-graphics/examples/output/generated/
```

### Option 2: Terminal
```bash
# View temperature demo outputs
open examples/output/generated/temperature_demo/

# View tech startup outputs
open examples/output/generated/use_cases/tech_startup/

# View all use cases
open examples/output/generated/use_cases/
```

### Option 3: VS Code / Editor
Open the files directly in your editor - most editors can preview PNG files.

### Option 4: Quick View (macOS)
```bash
# Quick view a specific file
qlmanage -p examples/output/generated/temperature_demo/temperature_0.8.png
```

## Viewing Prompts

All prompts are stored in JSON format alongside the images:

```bash
# View temperature demo prompts
cat examples/output/generated/temperature_demo/prompts_used.json | python3 -m json.tool

# View tech startup prompts
cat examples/output/generated/use_cases/tech_startup/prompts_used.json | python3 -m json.tool

# View all aggregated prompts (after running aggregate_prompts.py)
cat examples/output/generated/use_cases/all_prompts.json | python3 -m json.tool
```

## Comparing Temperature Effects

To see how temperature affects outputs, compare these files side-by-side:
1. `temperature_demo/temperature_0.3.png` - Most conservative
2. `temperature_demo/temperature_0.8.png` - Balanced (default)
3. `temperature_demo/temperature_1.2.png` - More creative
4. `temperature_demo/temperature_1.5.png` - Most creative

You'll notice differences in:
- Headlines and subheadlines
- Layout styles
- Color schemes
- Visualization types
- Metric selections

## File Sizes

Temperature demo outputs:
- `temperature_0.3.png`: ~304 KB
- `temperature_0.8.png`: ~332 KB
- `temperature_1.2.png`: ~213 KB
- `temperature_1.5.png`: ~238 KB

Tech startup outputs:
- `01_product_vision.png`: ~240 KB
- `04_revenue_vs_users.png`: ~1.6 MB (combo chart, larger)

## Quick Command Reference

```bash
# Navigate to outputs directory
cd examples/output/generated

# List all temperature demo files
ls -lh temperature_demo/

# List all use case directories
ls -d use_cases/*/

# Open temperature demo in Finder
open temperature_demo/

# View prompts for a specific use case
cat use_cases/tech_startup/prompts_used.json | python3 -m json.tool
```
