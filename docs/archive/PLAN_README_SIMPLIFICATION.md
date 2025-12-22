# Plan: Simplify README for Better Readability

## Current Problems

1. **Too Long**: 1,152 lines - overwhelming for new users
2. **Too Much Detail**: Hero layouts section alone is 150+ lines with multiple examples
3. **Mixed Levels**: Basic and advanced content mixed together
4. **Repetitive**: Same concepts explained multiple times
5. **Hard to Scan**: Too many code blocks and examples inline
6. **Examples Overload**: All showcase examples shown inline (tables with images)

## Goals

1. **Quick to Understand**: New users should understand what this is in < 2 minutes
2. **Easy Navigation**: Clear structure with links to detailed docs
3. **Examples Accessible**: Examples visible but not overwhelming
4. **Progressive Disclosure**: Basic → Intermediate → Advanced
5. **Scannable**: Use tables, lists, and clear headings

## Proposed Structure

### New README Structure (Target: ~300-400 lines)

```
# Modern Graphics Generator

[Brief intro - 2-3 sentences]

## Quick Start (5 minutes)
- Installation
- Your first graphic (one simple example)
- Link to full quick start guide

## What Can You Create? (Visual Gallery)
- One image per category (diagram types, hero slides, templates)
- Link to full gallery

## Core Concepts (Brief)
- Generator, Diagram Types, Templates, Attribution
- One paragraph each + link to detailed guide

## Examples & Gallery
- Link to showcase directory
- Small preview table (3-4 examples max)
- Link to examples/README.md for more

## Common Tasks
- Quick links to common use cases
- Link to USE_CASES.md for details

## Documentation
- Links to all detailed guides
- API reference link
- Examples directory link

## Installation & Requirements
- Basic requirements
- Optional (OpenAI) requirements

## Next Steps
- Links to guides based on what you want to do
```

## Content to Move Out

### Move to Separate Files:

1. **Hero Layouts Details** → `docs/HERO_SLIDES.md`
   - All the detailed hero slide examples
   - Flow nodes, freeform canvas details
   - JSON examples

2. **Advanced Topics** → `docs/ADVANCED.md`
   - SVG.js integration
   - Custom diagram types
   - AI-assisted template creation
   - Custom templates (detailed)

3. **API Reference** → `docs/API.md`
   - All method signatures
   - Parameter details
   - Return types

4. **Export Options** → `docs/EXPORT.md`
   - Detailed export settings
   - Resolution guidelines
   - Quality options

5. **Prompt-Based Generation** → `docs/PROMPTS.md`
   - All prompt examples
   - Default prompts
   - Custom prompts

6. **Troubleshooting** → `docs/TROUBLESHOOTING.md`
   - Common issues
   - Solutions
   - FAQ

## Examples Strategy

### In README:
- **One simple example** in Quick Start
- **Visual gallery** with 1-2 examples per category (not all 20+)
- **Link to showcase** for full gallery

### Separate:
- **examples/README.md** - Already exists, keep it
- **examples/output/showcase/** - Visual gallery (already exists)
- **examples/output/README.md** - Explains showcase structure

## Specific Changes

### 1. Simplify Hero Layouts Section
**Current**: 150+ lines with 3 detailed examples, JSON, CLI examples
**New**: 
- Brief intro (2-3 sentences)
- Visual table showing 3 examples
- Link to `docs/HERO_SLIDES.md` for details

### 2. Simplify Common Use Cases
**Current**: Multiple detailed examples inline
**New**:
- Brief descriptions
- Visual preview (small table)
- Link to `docs/USE_CASES.md` for details

### 3. Simplify Diagram Types
**Current**: Visual gallery + detailed guide section
**New**:
- Visual gallery (keep it - it's good)
- Brief descriptions
- Link to `docs/DIAGRAM_TYPES.md` for decision tree

### 4. Simplify Examples Section
**Current**: Shows all showcase examples inline with tables
**New**:
- Brief intro
- Small preview (3-4 examples max)
- Link to showcase directory
- Link to examples/README.md

### 5. Move Advanced Content
**Current**: Advanced topics mixed in
**New**:
- Brief mention
- Link to `docs/ADVANCED.md`

## Implementation Steps

1. **Create new doc files**:
   - `docs/HERO_SLIDES.md`
   - `docs/ADVANCED.md`
   - `docs/API.md`
   - `docs/EXPORT.md`
   - `docs/PROMPTS.md`
   - `docs/TROUBLESHOOTING.md`

2. **Extract content from README**:
   - Move hero layouts details → HERO_SLIDES.md
   - Move advanced topics → ADVANCED.md
   - Move API reference → API.md
   - Move export details → EXPORT.md
   - Move prompt examples → PROMPTS.md
   - Move troubleshooting → TROUBLESHOOTING.md

3. **Simplify README**:
   - Keep Quick Start (simplify)
   - Keep Core Concepts (brief)
   - Keep Visual Gallery (simplify)
   - Add Examples section (brief + links)
   - Add Documentation section (links)
   - Remove detailed examples
   - Remove advanced content

4. **Update navigation**:
   - Update Quick Navigation section
   - Add links to new docs
   - Update examples/README.md links

5. **Test**:
   - Verify all links work
   - Check that examples are still accessible
   - Ensure nothing is lost

## Target Metrics

- **README length**: ~300-400 lines (down from 1,152)
- **Time to understand**: < 2 minutes
- **Examples visible**: Yes, but not overwhelming
- **Details accessible**: Yes, via linked docs

## Example Gallery Strategy

### In README:
Show a **curated selection** (not all):
- 2-3 diagram types
- 1-2 hero slides
- 1 template example
- 1 use case example

### Full Gallery:
- Link to `examples/output/showcase/` directory
- Users can browse all examples there
- examples/README.md explains structure

## Benefits

1. **Faster Onboarding**: New users get started quickly
2. **Less Overwhelming**: Focused content, not everything at once
3. **Better Organization**: Related content grouped together
4. **Easier Maintenance**: Update docs in one place
5. **Better Discoverability**: Clear navigation to what you need
6. **Examples Still Accessible**: Just not overwhelming in main README
