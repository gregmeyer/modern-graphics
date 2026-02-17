# Modern Graphics Generator

Build hero slides, insight cards, and diagrams from one CLI with clarity-first defaults.

## Start Here

Install the runtime dependencies:

```bash
pip install playwright pillow python-dotenv
playwright install chromium
```

Generate your first PNG in one command:

```bash
modern-graphics create \
  --layout hero \
  --headline "Execution scales. Judgment does not." \
  --png \
  --output ./output/hero.png
```

Expected output: `./output/hero.png`

Default behavior is tuned for immediate usability:
- `theme=corporate`
- `density=clarity`
- `crop-mode=safe`
- `padding-mode=minimal`

## Common Tasks

### 1) Create a hero opener

```bash
modern-graphics create \
  --layout hero \
  --headline "When shipping gets easy, choosing gets hard." \
  --output ./output/hero.html
```

Expected output: `./output/hero.html`

### 2) Create an insight card

```bash
modern-graphics create \
  --layout insight-card \
  --text "One-page artifacts force explicit decisions." \
  --png \
  --output ./output/insight-card.png
```

Expected output: `./output/insight-card.png`

### 3) Export a social-ready preset

```bash
modern-graphics create \
  --layout hero \
  --headline "Decision quality is the new leverage." \
  --png \
  --export-preset linkedin \
  --output ./output/hero-linkedin.png
```

Expected output: `./output/hero-linkedin.png`

Presets:
- `linkedin` (`1200x627`)
- `x` (`1600x900`)
- `substack-hero` (`1400x700`)

### 4) Switch density for denser visuals

```bash
modern-graphics create \
  --layout timeline \
  --events "Q1|Baseline,Q2|Adoption,Q3|Optimization,Q4|Scale" \
  --density dense \
  --output ./output/timeline-dense.html
```

Expected output: `./output/timeline-dense.html`

### 5) Migrate from legacy commands

Legacy commands still run, but `create` is the canonical path.

```bash
modern-graphics timeline \
  --title "Legacy Timeline" \
  --events "Q1|Baseline,Q2|Adoption,Q3|Optimization,Q4|Scale" \
  --output ./output/legacy-timeline.html
```

Migration guide: [`docs/MIGRATION.md`](docs/MIGRATION.md)

## Examples by Goal

- I need a first-run set of canonical `create` outputs:
  - `examples/output/showcase/create-first/`
  - regenerate: `python scripts/generate_readme_create_examples.py`
- I need one sample for each core diagram type:
  - `examples/output/showcase/diagram-types/`
  - regenerate: `python scripts/run_showcase.py`
- I need insight graphics examples:
  - `examples/output/showcase/insight-graphics/`
  - docs: [`docs/DIAGRAM_TYPES.md`](docs/DIAGRAM_TYPES.md)
- I need hero layout variants:
  - `examples/output/showcase/hero-slides/`
  - docs: [`docs/HERO_SLIDES.md`](docs/HERO_SLIDES.md)
- I need full themed gallery previews:
  - `examples/output/theme-demo/*.png` (tracked)
  - regenerate gallery HTML: `python examples/generate_complete_theme_demo.py`

For a guided index of runnable examples, see [`examples/README.md`](examples/README.md).

## CLI Defaults

| Setting | Default | Why |
|---|---|---|
| Theme | `corporate` | Neutral baseline for business graphics |
| Density | `clarity` | Readability-first composition |
| Crop mode | `safe` | Tight bounds without accidental clipping |
| Padding mode | `minimal` | Keeps whitespace low for publishing |

Details: [`docs/CREATE_COMMAND.md`](docs/CREATE_COMMAND.md), [`docs/EXPORT.md`](docs/EXPORT.md)

## Legacy Commands

Legacy command family remains available for compatibility and emits migration hints.

Use for new work:

```bash
modern-graphics create ...
```

Migration and deprecation policy:
- [`docs/MIGRATION.md`](docs/MIGRATION.md)
- [`docs/DEPRECATION_POLICY.md`](docs/DEPRECATION_POLICY.md)

## Where Next

- Quick start walkthrough: [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- Create command recipes: [`docs/CREATE_COMMAND.md`](docs/CREATE_COMMAND.md)
- Export and crop behavior: [`docs/EXPORT.md`](docs/EXPORT.md)
- Diagram catalog: [`docs/DIAGRAM_TYPES.md`](docs/DIAGRAM_TYPES.md)
- Hero patterns: [`docs/HERO_SLIDES.md`](docs/HERO_SLIDES.md)
- Advanced customization: [`docs/ADVANCED.md`](docs/ADVANCED.md)
- Prompting patterns: [`docs/PROMPT_BEST_PRACTICES.md`](docs/PROMPT_BEST_PRACTICES.md)
- Full docs index: [`docs/README.md`](docs/README.md)

## Contributing

- Contribution guide: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)
- Strategy and overhaul context: [`docs/OVERHAUL_SPEC.md`](docs/OVERHAUL_SPEC.md)

## License

MIT License.
