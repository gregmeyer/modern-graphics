# Examples Output Refactor Plan

## Goal
Review and refactor `/examples/output` directory to create a curated showcase of examples suitable for README display.

## Current State Analysis

### Current Structure
```
examples/output/
├── .gitkeep
├── README.md
├── attribution_custom/          # 7 files
├── story_slides/                # 4 files
├── use_cases/
│   └── corporate/               # 2 files
└── [root level files]          # ~23 files
```

### Current Files (36 total)
- **Numbered examples**: 01_cycle.png, 02_comparison.png, etc. (from all_diagram_types.py)
- **Attribution examples**: attribution_*.png, attribution_custom/* (from attribution_examples.py)
- **Story slides**: story_slides/* (from story_slide_with_prompt.py)
- **Export examples**: export_*.png (from export_options.py)
- **Use cases**: use_cases/corporate/* (from use_case_corporate.py)
- **Miscellaneous**: product_cycle.png, project_timeline.png, feature_comparison.png, etc.

## Issues Identified

1. **Too many files**: 36 files is overwhelming for README showcase
2. **Mixed purposes**: Examples, tests, and use cases all mixed together
3. **No clear showcase**: Hard to identify "best" examples for README
4. **Inconsistent naming**: Numbered files, descriptive names, mixed conventions
5. **No organization by feature**: Hard to find examples of specific features

## Proposed Structure

### New Directory Organization
```
examples/output/
├── .gitkeep
├── README.md                    # Updated with showcase info
├── showcase/                    # NEW: Curated showcase examples
│   ├── diagram-types/          # One example of each diagram type
│   │   ├── 01-cycle.png
│   │   ├── 02-comparison.png
│   │   ├── 03-timeline.png
│   │   ├── 04-story-slide.png
│   │   ├── 05-grid.png
│   │   ├── 06-pyramid.png
│   │   ├── 07-flywheel.png
│   │   ├── 08-before-after.png
│   │   ├── 09-funnel.png
│   │   ├── 10-slide-cards.png
│   │   └── 11-slide-comparison.png
│   ├── templates/               # Template showcase
│   │   ├── default.png
│   │   ├── corporate.png
│   │   ├── creative.png
│   │   └── tech-startup.png
│   ├── attribution/             # Attribution examples
│   │   ├── default.png
│   │   ├── custom-styled.png
│   │   └── with-context.png
│   └── use-cases/               # Best use case examples
│       ├── corporate-report.png
│       ├── tech-pitch.png
│       └── educational-course.png
├── generated/                   # NEW: All generated files (gitignored)
│   ├── [all current files moved here]
│   └── [future generated files]
└── archive/                     # NEW: Old/unused examples (optional)
    └── [deprecated examples]
```

## Refactoring Steps

### Phase 1: Analysis & Planning
1. **Review all current files**
   - List all 36 files with descriptions
   - Identify showcase-worthy examples
   - Identify duplicates or low-quality examples
   - Map files to their source scripts

2. **Define showcase criteria**
   - High visual quality
   - Demonstrates key features clearly
   - Representative of diagram type capabilities
   - Professional appearance
   - Diverse use cases

### Phase 2: Create New Structure
3. **Create showcase directory structure**
   ```bash
   mkdir -p examples/output/showcase/{diagram-types,templates,attribution,use-cases}
   mkdir -p examples/output/generated
   ```

4. **Update .gitignore**
   - Ignore `examples/output/generated/**`
   - Keep `examples/output/showcase/**` tracked in git
   - Keep `examples/output/.gitkeep`

### Phase 3: Curate Examples
5. **Select diagram type examples**
   - Review all_diagram_types.py outputs
   - Pick best example of each type (11 types)
   - Ensure examples are visually appealing and clear
   - Rename with consistent naming: `{number}-{type}.png`

6. **Select template examples**
   - Review use case examples (corporate, creative, tech-startup, etc.)
   - Pick 3-4 best template showcases
   - Show variety in styles

7. **Select attribution examples**
   - Review attribution_examples.py outputs
   - Pick 2-3 best examples showing different configurations
   - Show default, custom-styled, and with-context variants

8. **Select use case examples**
   - Review use_case_*.py outputs
   - Pick 2-3 best complete use cases
   - Show real-world application

### Phase 4: Generate Showcase Script
9. **Create showcase generation script**
   - `scripts/generate_showcase.py`
   - Generates all showcase examples with consistent styling
   - Uses high-quality settings (high resolution, good padding)
   - Ensures consistent attribution styling
   - Outputs directly to `showcase/` directories

10. **Script requirements**
    - Generate one example per diagram type
    - Generate template examples from use cases
    - Generate attribution examples
    - Use professional, realistic data
    - Consistent visual style across all examples

### Phase 5: Reorganize Existing Files
11. **Move existing files**
    - Move all current files to `examples/output/generated/`
    - Keep structure but organize by source script
    - Update any hardcoded paths in scripts

12. **Update example scripts**
    - Modify scripts to output to `generated/` directory
    - Keep showcase generation separate
    - Update paths in README references

### Phase 6: Update Documentation
13. **Update examples/output/README.md**
    - Explain showcase vs generated distinction
    - Link to showcase examples
    - Document how to regenerate showcase

14. **Update main README.md**
    - Add showcase section with images
    - Reference showcase examples in relevant sections
    - Add "View Examples" links
    - Consider adding actual image references (if hosting images)

### Phase 7: Maintenance
15. **Create maintenance script**
    - Script to regenerate showcase from source
    - Can be run periodically to refresh examples
    - Ensures showcase stays up-to-date

16. **Document showcase criteria**
    - Document what makes a good showcase example
    - Guidelines for adding new showcase examples
    - Review process for showcase additions

## Showcase Selection Criteria

### Diagram Type Examples
- **Visual Quality**: Clean, professional appearance
- **Clarity**: Easy to understand at a glance
- **Representative**: Shows typical use case for that diagram type
- **Data Quality**: Realistic, meaningful data (not "Test 1", "Test 2")
- **Completeness**: Shows all key features of the diagram type

### Template Examples
- **Style Variety**: Different visual styles (corporate, creative, tech)
- **Quality**: High-quality rendering
- **Completeness**: Shows template applied to multiple diagram types
- **Real-world**: Based on actual use cases

### Attribution Examples
- **Variety**: Different configurations (default, custom, with context)
- **Clarity**: Easy to see differences between configurations
- **Professional**: Looks good in final output

### Use Case Examples
- **Completeness**: Full use case with multiple diagrams
- **Real-world**: Based on realistic scenarios
- **Quality**: Professional appearance
- **Diversity**: Different industries/contexts

## Implementation Checklist

- [ ] Phase 1: Review all current files and create inventory
- [ ] Phase 2: Create new directory structure
- [ ] Phase 3: Select showcase examples from existing files
- [ ] Phase 4: Create generate_showcase.py script
- [ ] Phase 5: Move existing files to generated/
- [ ] Phase 6: Update example scripts to use generated/
- [ ] Phase 7: Update examples/output/README.md
- [ ] Phase 8: Update main README.md with showcase references
- [ ] Phase 9: Test showcase generation script
- [ ] Phase 10: Generate initial showcase set
- [ ] Phase 11: Review showcase examples for quality
- [ ] Phase 12: Document showcase maintenance process

## Success Metrics

- **Reduced file count**: From 36 files to ~20 curated showcase files
- **Clear organization**: Easy to find examples by category
- **README ready**: Showcase examples suitable for README display
- **Maintainable**: Easy to regenerate and update showcase
- **Professional**: All showcase examples are high quality

## Notes

- Showcase examples should be tracked in git (for README display)
- Generated examples should be gitignored (temporary/test outputs)
- Consider hosting showcase images externally if README gets too large
- May want to create a simple HTML gallery page for showcase browsing
- Keep showcase examples small in number but high in quality
