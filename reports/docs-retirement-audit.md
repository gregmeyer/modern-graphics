# Docs Retirement Audit

Date: 2026-02-17
Scope: `README.md`, `docs/*.md`, `examples/README.md`

## Key Findings

- Mermaid support is active in code and CLI, but `docs/MERMAID.md` has **0 inbound links** from core docs.
- Prompt documentation is fragmented across 5 files (`PROMPTS.md`, `PROMPT_BEST_PRACTICES.md`, `PROMPT_EXAMPLES.md`, `PROMPT_PATTERNS.md`, `AI_TEMPLATE_CREATION.md`) with heavy overlap.
- Several deep reference docs have **0 inbound links** and are likely discoverability debt (`RADAR_DIAGRAM.md`, `WIREFRAME_SCENE_SPEC.md`, `OVERHAUL_PHASE1_PR_SUMMARY.md`).
- `docs/README.md` remains an index dump and can be streamlined to a task-first IA.

## Mermaid Status (Verified)

Mermaid compatibility exists and is active:
- CLI command: `modern-graphics mermaid` (`modern_graphics/cli.py`)
- CLI integration flags: `--mermaid-file` on `modern-hero` and `insight-card`
- Runtime helper: `modern_graphics/diagrams/mermaid_svg.py` (`mermaid_to_svg`)
- Guide: `docs/MERMAID.md`

Action: keep Mermaid docs, improve discoverability and trim duplication.

## Keep / Consolidate / Archive Matrix

| Doc | Current Role | Signal | Decision | Action |
|---|---|---|---|---|
| `docs/QUICKSTART.md` | first-run path | linked | Keep | tighten to CLI-first flow only |
| `docs/CREATE_COMMAND.md` | canonical CLI usage | linked | Keep | keep as command reference |
| `docs/EXPORT.md` | crop/export policy | linked | Keep | keep as canonical export policy |
| `docs/MIGRATION.md` | legacy->create mapping | linked | Keep | keep; add short timeline note |
| `docs/DEPRECATION_POLICY.md` | lifecycle policy | linked | Keep | keep concise; link from migration only |
| `docs/DIAGRAM_TYPES.md` | visual catalog | linked | Keep | keep; ensure all assets current |
| `docs/HERO_SLIDES.md` | hero layouts | linked | Keep | keep; remove duplicate prompt advice |
| `docs/ADVANCED.md` | advanced customization | linked | Keep | keep; split any basic content out |
| `docs/API.md` | API reference | linked | Keep | keep; trim repetitive prompt notes |
| `docs/TROUBLESHOOTING.md` | operational fixes | linked | Keep | keep; refresh stale issue URL placeholder |
| `docs/CONTRIBUTING.md` | contributor workflow | linked | Keep | keep |
| `docs/CONCEPTS.md` | foundational model | lightly linked | Keep | keep but trim old links to top README anchors |
| `docs/USE_CASES.md` | examples by scenario | lightly linked | Keep | keep concise |
| `docs/MERMAID.md` | mermaid integration | **0 inbound** but active feature | Keep | add inbound links from root docs + hero/insight docs |
| `docs/PROMPTS.md` | prompt workflows | linked | Keep (canonical) | expand as the single prompt guide |
| `docs/PROMPT_BEST_PRACTICES.md` | prompt tuning | large overlap | Consolidate | merge high-value sections into `PROMPTS.md`; archive remainder |
| `docs/PROMPT_EXAMPLES.md` | prompt snippets | large overlap | Consolidate | merge top examples into `PROMPTS.md`; archive long tail |
| `docs/PROMPT_PATTERNS.md` | prompt structures | large overlap | Consolidate | merge pattern framework into `PROMPTS.md`; archive remainder |
| `docs/AI_TEMPLATE_CREATION.md` | prompt/template internals | overlap + old framing | Consolidate | fold minimal "template creation" section into `PROMPTS.md` or `ADVANCED.md` |
| `docs/RADAR_DIAGRAM.md` | single layout deep dive | **0 inbound** | Archive or Relink | either archive or link from `DIAGRAM_TYPES.md` |
| `docs/WIREFRAME_SCENE_SPEC.md` | wireframe scene schema | **0 inbound** | Keep (advanced) | move under advanced section and link from `ADVANCED.md` |
| `docs/OVERHAUL_SPEC.md` | program spec | linked | Keep | internal governance doc |
| `docs/OVERHAUL_WORKPLAN.md` | execution tracker | linked | Keep (internal) | keep internal; reduce prominence in user docs |
| `docs/OVERHAUL_PHASE1_PR_SUMMARY.md` | historical summary | **0 inbound** | Archive | move to `docs/archive/` |
| `docs/SHARING_CHECKLIST.md` | publishing checklist | lightly linked | Keep (internal) | keep internal |
| `docs/STRATEGY_EXTENSION.md` | extension contract | lightly linked | Keep | keep for contributors |
| `docs/README.md` | docs index | highly linked | Keep (rewrite) | convert to task-first docs map |

## Proposed Cleanup Phases

### Phase A: Information Architecture (no deletions)

1. Rewrite `docs/README.md` to task-first buckets:
- Start
- Build graphics
- Prompt workflows
- Mermaid & wireframes
- Advanced/extensibility
- Internal program docs

2. Add missing inbound links:
- Add `MERMAID.md` links from `README.md`, `docs/README.md`, and `docs/HERO_SLIDES.md`.
- Add `WIREFRAME_SCENE_SPEC.md` link from `docs/ADVANCED.md`.

3. Fix stale links:
- `docs/TROUBLESHOOTING.md` GitHub issues placeholder.
- `docs/CONCEPTS.md` links to obsolete root README anchors.

### Phase B: Prompt Consolidation

1. Make `docs/PROMPTS.md` canonical and expand sections:
- quick-start prompt flows
- default prompt system (`DEFAULT_DIAGRAM_PROMPTS`)
- `ideas` interview flow
- `from-prompt-file` flow
- top 10 practical examples
- concise best-practice checklist

2. Convert other prompt docs to transitional stubs:
- `PROMPT_BEST_PRACTICES.md`
- `PROMPT_EXAMPLES.md`
- `PROMPT_PATTERNS.md`
- `AI_TEMPLATE_CREATION.md`

Each stub should point to canonical sections in `PROMPTS.md` and be scheduled for archive after one release cycle.

### Phase C: Retirement / Archive

1. Move historical or low-value docs to `docs/archive/`:
- `OVERHAUL_PHASE1_PR_SUMMARY.md`
- prompt stubs that are no longer needed after transition
- `RADAR_DIAGRAM.md` if not linked as an active supported doc

2. Update `docs/README.md` and `README.md` links accordingly.

## Review Gates

Before merge:
1. Every kept doc has at least one inbound link from `README.md` or `docs/README.md`.
2. No broken markdown links in `README.md`, `docs/*.md`, `examples/README.md`.
3. Prompt doc count reduced to one canonical doc + optional temporary stubs.
4. Mermaid doc linked from at least two canonical entry points.

## Recommended Next PR Slice

Title: `docs: task-first IA + mermaid discoverability + prompt doc consolidation (phase A/B)`

Scope for first PR:
- rewrite `docs/README.md`
- update `README.md` quick links to include Mermaid
- patch stale links in `CONCEPTS.md` and `TROUBLESHOOTING.md`
- consolidate prompt docs by making `PROMPTS.md` canonical and converting others to slim stubs
