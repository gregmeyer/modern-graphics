# Layout Clarity Phase 2

This folder stores local before/after snapshots for the `story`, `timeline`, and `grid` create-layout defaults.

## Before

- `before/timeline-default.png`
- `before/grid-default.png`

`before/story-default.png` is intentionally missing: baseline `create --layout story` crashed due template/attribution positional misbinding and null background handling.

## After

- `after/story-default.png`
- `after/timeline-default.png`
- `after/grid-default.png`

## Commands Used

```bash
python3 -m modern_graphics.cli create \
  --layout story \
  --what-changed "Execution scaled via automation" \
  --time-period "Q1 to Q4" \
  --what-it-means "Decision quality became the leverage point" \
  --png \
  --output reports/layout-clarity-phase2/after/story-default.png

python3 -m modern_graphics.cli create \
  --layout timeline \
  --events "Q1|Baseline workflow,Q2|Automation rollout,Q3|Decision gates added,Q4|Quality stabilized" \
  --png \
  --output reports/layout-clarity-phase2/after/timeline-default.png

python3 -m modern_graphics.cli create \
  --layout grid \
  --items "Identify constraint,Define owner,Set decision gate,Ship smallest slice,Measure outcome,Close loop" \
  --columns 3 \
  --goal "Fewer handoffs" \
  --outcome "Higher decision quality" \
  --png \
  --output reports/layout-clarity-phase2/after/grid-default.png
```
