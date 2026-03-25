# Examples

Runnable examples and curated showcase outputs for modern-graphics.

## Use This Page When

- You want to generate graphics now.
- You want tracked visual references before you customize.
- You want to browse example scripts by category.

## Fastest Path: Docker + MCP

The recommended workflow — no local Python setup needed:

```bash
# 1. Build once
make build

# 2. Generate directly
./generate hero --headline "Execution scales. Judgment does not."
# ✓ ./output/hero.png

# 3. Or use MCP with Claude
# Configure .mcp.json, then ask:
# "make me a comparison of manual vs automated workflows"
```

See [MCP Server Guide](../docs/MCP_SERVER.md) for AI-assisted setup.

## Pick an Example by Goal

### I need a hero slide

```bash
./generate hero --headline "Make the journey the tie-breaker"
```

Or with the CLI directly:

```bash
modern-graphics create \
  --layout hero \
  --headline "Make the journey the tie-breaker" \
  --png \
  --output examples/output/generated/hero-example.png
```

See tracked hero references: `examples/output/showcase/hero-slides/`

### I need an insight card

```bash
./generate insight-card --text "Execution scales faster than decision quality."
```

See tracked insight references: `examples/output/showcase/insight-graphics/`

### I need social exports

```bash
modern-graphics create \
  --layout hero \
  --headline "Filter what ships" \
  --png \
  --export-preset linkedin \
  --output examples/output/generated/hero-linkedin.png
```

### I need a custom theme

See [Custom Themes Guide](../docs/CUSTOM_THEMES.md) for full instructions, or run `custom_template.py` locally.

## Example Scripts

For local development with `pip install -e .`:

### Getting Started
- [simple_example.py](simple_example.py) — minimal cycle diagram
- [export_options.py](export_options.py) — PNG export with crop/padding options

### Themes and Templates
- [custom_template.py](custom_template.py) — build a branded theme
- [create_team_scheme.py](create_team_scheme.py) — interactive color scheme creation
- [generate_complete_theme_demo.py](generate_complete_theme_demo.py) — full theme gallery

### Use Cases (require OpenAI API key)
- [use_case_corporate.py](use_case_corporate.py) — quarterly report graphics
- [use_case_tech_startup.py](use_case_tech_startup.py) — pitch deck visuals
- [use_case_education.py](use_case_education.py) — course materials
- [use_case_healthcare.py](use_case_healthcare.py) — healthcare presentations
- [use_case_creative.py](use_case_creative.py) — creative portfolio

### Mermaid and Hero Composition
- [hero_mermaid_diagrams.py](hero_mermaid_diagrams.py) — hero cards with Mermaid diagrams
- [mermaid_card_hero_demo.py](mermaid_card_hero_demo.py) — Mermaid composition demo
- [hero_auth_sequence.py](hero_auth_sequence.py) — hero with auth sequence diagram

### SVG and Advanced
- [svg_js_example.py](svg_js_example.py) — SVG.js integration
- [transaction_card_demo.py](transaction_card_demo.py) — SVG composition on cards

### Prompt-Based Generation (require OpenAI API key)
- [interactive_template_creation.py](interactive_template_creation.py) — interactive template builder
- [interview_with_prompt_example.py](interview_with_prompt_example.py) — interview + prompt flow
- [story_slide_with_prompt.py](story_slide_with_prompt.py) — story slide from prompts
- [temperature_effects_demo.py](temperature_effects_demo.py) — temperature effects on AI generation
- [model_comparison_test.py](model_comparison_test.py) — compare model outputs

## Showcase Gallery

Curated reference outputs (tracked in git):
- `output/showcase/` — canonical examples by category
- `output/theme-demo/` — theme preview PNGs

Temporary local outputs (gitignored):
- `output/generated/` — your experiments go here

Detailed output policy: [output/README.md](output/README.md).

---

## Read Next

- [Create Command Guide](../docs/CREATE_COMMAND.md) -- CLI recipes and flag reference
- [Diagram Types](../docs/DIAGRAM_TYPES.md) -- choose the right layout
