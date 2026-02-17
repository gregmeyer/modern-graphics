# Docs IA Phase 4 Outline (Batch A)

## Design Brief

- Product context: CLI/Python graphics generator with both beginner and advanced workflows.
- Primary user action: find the right command/example and get a usable output in under 5 minutes.
- Tone: calm, confident, operational.
- Constraints: preserve existing command behavior and deep docs; reduce top-level cognitive load.

## Current State (Audit)

- `README.md`: 1161 lines; mixes quick-start, showcase, advanced customization, overhaul internals.
- `examples/README.md`: 284 lines; useful but verbose and partially duplicative with top-level README.
- `examples/output/README.md`: 141 lines; output taxonomy is clear but disconnected from "which example should I run first?".

Primary cognitive-load issues:

1. Too many focal points on first read (marketing + quickstart + deep architecture in same surface).
2. Repeated guidance across sections (`create` defaults, migration posture, theme demos).
3. "Examples by goal" path is implicit; users must infer which file to open.
4. Deep overhaul checkpoint details are in README body, increasing scan cost for first-time users.

## Proposed IA (Old -> New)

### README.md (top-level)

Old:
- Why teams use it
- What can you create
- Insight graphics guide (large)
- Prompting techniques (large)
- Customization guide (large)
- Overhaul checkpoint details
- Docs index

New:
1. `Start Here` (install, first command, first PNG)
2. `Common Tasks` (task cards):
   - create first hero
   - create insight card
   - export social preset
   - switch density
   - migrate legacy command
3. `Examples by Goal` (6-8 canonical links)
4. `CLI Defaults` (small table: theme/density/crop/padding)
5. `Legacy Commands` (compatibility note + migration link)
6. `Where Next`:
   - create command guide
   - export guide
   - examples README
   - advanced customization
7. `Contributing / License`

Move out of README body:
- detailed prompting techniques -> dedicated docs page
- deep insight graphics API walkthrough -> keep in dedicated section doc, link only
- overhaul checkpoint internals -> keep in overhaul docs only, short status link from README

### examples/README.md

Old:
- category-heavy listing + learning path + troubleshooting in one stream

New:
1. `Pick an Example by Intent`:
   - "I need a hero slide"
   - "I need an insight card"
   - "I need social exports"
   - "I need full theme gallery"
2. `Run This` command per intent (single canonical command each)
3. `Output locations` concise map
4. `Advanced examples` collapsed into compact index

### examples/output/README.md

Old:
- structure + maintenance + workflows

New:
1. `What is tracked vs generated`
2. `Where to find canonical showcase outputs`
3. `How to regenerate safely`
4. `Do not commit` rules (anti-bloat guard)

## Cognitive-Load Gates (Apply to Batch B rewrite)

1. Primary path obvious in 3 seconds (`Start Here` + one command).
2. At most 2 focal points per major section.
3. Advanced details are link-outs, not embedded walls of text.
4. No duplicated default/legacy guidance across README and command guides.
5. Every command block has one expected output path.

## Parallel Execution Plan (Batch B/C)

- Workstream 1: rewrite `README.md` to new IA skeleton.
- Workstream 2: rewrite `examples/README.md` to intent-first map.
- Workstream 3: tighten `examples/output/README.md` around tracked vs generated.
- Workstream 4: link/drift audit + consistency pass (`rg` link checks + manual spot validation).

## Acceptance Criteria

- New user finds first working command in <30 seconds.
- "Which example should I run?" is answered by one section.
- README shrinks materially while preserving links to advanced docs.
- No broken internal links after rewrite.
