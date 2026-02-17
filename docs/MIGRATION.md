# Migration Guide (Legacy CLI -> Create)

Modern Graphics keeps legacy commands working, but new workflows should use the unified `create` entrypoint.

## What changed

- Legacy command names still run but may emit deprecation warnings.
- Some old aliases are auto-remapped to canonical commands.
- `create` is the long-term path for consistent defaults and lower command-surface sprawl.

## Alias Compatibility

The CLI automatically maps these aliases:

- `slide-comparison` -> `slide-compare`
- `from-prompt` -> `from-prompt-file`
- `key_insight` -> `key-insight`
- `insight_card` -> `insight-card`
- `insight_story` -> `insight-story`
- `before_after` -> `before-after`

## Before / After Examples

### Comparison

```bash
# Before (legacy)
modern-graphics comparison \
  --title "Decision quality" \
  --left "Before:Manual triage:Slow" \
  --right "After:Agentic triage:Faster" \
  --output comparison.html

# After (recommended)
modern-graphics create \
  --layout comparison \
  --left "Before:Manual triage:Slow" \
  --right "After:Agentic triage:Faster" \
  --output comparison.html
```

### Timeline

```bash
# Before (legacy)
modern-graphics timeline \
  --title "Capability shift" \
  --events "Q1|Baseline,Q2|Adoption,Q3|Scale" \
  --output timeline.html

# After (recommended)
modern-graphics create \
  --layout timeline \
  --events "Q1|Baseline,Q2|Adoption,Q3|Scale" \
  --output timeline.html
```

### Insight Card

```bash
# Before (legacy)
modern-graphics insight-card \
  --text "Constrained execution makes quality repeatable." \
  --output insight-card.png --png

# After (recommended)
modern-graphics create \
  --layout insight-card \
  --text "Constrained execution makes quality repeatable." \
  --png \
  --output insight-card.png
```

### Story Slide -> Story Layout

```bash
# Before (legacy)
modern-graphics story-slide \
  --title "What changed" \
  --what-changed "Execution became cheap" \
  --time-period "last 12 months" \
  --what-it-means "Judgment is the bottleneck" \
  --output story.html

# After (recommended)
modern-graphics create \
  --layout story \
  --title "What changed" \
  --what-changed "Execution became cheap" \
  --time-period "last 12 months" \
  --what-it-means "Judgment is the bottleneck" \
  --output story.html
```

## Migration Tips

- Start by migrating high-volume templates first (`comparison`, `timeline`, `insight-card`).
- Keep legacy commands in existing scripts until you have a clean `create` replacement.
- Use `docs/CREATE_COMMAND.md` for layout-specific parameter recipes.
