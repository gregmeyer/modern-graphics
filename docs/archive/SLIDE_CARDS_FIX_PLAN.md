# Slide Cards SVG Graphics Fix Plan

## Problem
SVG graphics are not visible in slide cards. The original default design worked better from an information architecture standpoint and should be preserved.

## Design Philosophy

### Original Default Style (Preserve)
**Layout**: Badge → Title → Tagline → **Mockup** → Subtext → Features
- **Information Architecture**: Text-first approach, mockup in middle
- **Use Case**: When text context is primary, graphic supports the message
- **Visual Hierarchy**: Title/tagline establish context, then visual, then details

### Lower Third Style (New Addition)
**Layout**: Badge → **Mockup (top 2/3)** → Title/Tagline/Subtext/Features (bottom 1/3)
- **Information Architecture**: Visual-first approach, text overlay at bottom
- **Use Case**: When visual is primary, text provides context
- **Visual Hierarchy**: Graphic dominates, text provides supporting info

**Both styles should be available** - default preserves original design, lower third is an alternative.

## Current State Analysis

### SVG Generation Flow
1. **Custom Mockup Detection**: Checks if `custom_mockup` is provided
2. **SVG.js vs Raw SVG**: Determines if it's SVG.js code or raw SVG string
3. **SVG.js Wrapper**: Wraps SVG.js code in a div with script tag
4. **Container Styling**: CSS controls visibility and sizing

### Potential Issues

#### Issue 1: SVG.js Container Not Visible (Default Style)
- **Problem**: SVG.js div might not be rendering or positioned correctly
- **Impact**: SVG elements not visible in default style cards
- **Check**: Container has `height: 140px`, inner div should fill it

#### Issue 2: SVG.js Container Positioning (Lower Third)
- **Problem**: Lower third style uses `height: 0; padding-bottom: 66.67%` for aspect ratio
- **Impact**: SVG.js div inside might not be positioned correctly
- **Current Fix Attempt**: Added `position: absolute` to inner div, but may need adjustment

#### Issue 3: SVG.js Script Execution Timing
- **Problem**: SVG.js script might not execute before screenshot
- **Impact**: SVG elements not rendered when PNG is captured
- **Check**: Export function waits for SVG.js, but timing might be off
- **Solution**: May need specific wait for slide card SVG elements

#### Issue 4: SVG Size Parameter Mismatch
- **Problem**: SVG.js `.size()` call might not match container dimensions
- **Impact**: SVG renders at wrong scale or position
- **Current**: Default uses `240x140`, lower third uses `400x200` but container is responsive
- **Solution**: Ensure SVG.js size matches container aspect ratio

## Fix Plan

### Step 1: Preserve Original Default Design
**Goal**: Ensure original default style remains unchanged and functional

**Actions**:
1. Verify original layout: Badge → Title → Tagline → Mockup → Subtext → Features
2. Ensure `.card-mockup` styling matches original (140px height, centered)
3. Verify SVG.js container div fills mockup container properly
4. Test that default style works without lower third changes affecting it

**Success Criteria**: Original default design works exactly as before

### Step 2: Fix SVG Visibility in Default Style
**Goal**: Ensure default style cards show SVG graphics correctly

**Actions**:
1. Verify `.card-mockup` has correct height (140px) and display properties
2. Ensure inner SVG.js div fills container (`width: 100%; height: 100%`)
3. Check SVG.js container div has proper flexbox centering
4. Verify SVG.js script executes and creates SVG elements
5. Test with both custom mockup and default mockup

**Success Criteria**: SVG visible in default style cards, original layout preserved

### Step 3: Fix Lower Third Style Container
**Goal**: Ensure lower third style cards show SVG graphics in top 2/3

**Actions**:
1. Fix aspect ratio container (`padding-bottom: 66.67%`)
2. Position SVG.js div absolutely within container
3. Ensure SVG.js size matches container aspect ratio (landscape)
4. Adjust SVG.js `.size()` to match landscape format (400x200 or proportional)
5. Verify text content appears in bottom 1/3

**Success Criteria**: SVG visible in top 2/3 of lower third cards, text in bottom 1/3

### Step 4: Verify Export Timing
**Goal**: Ensure PNG export captures rendered SVG

**Actions**:
1. Check `export.py` waits for SVG.js rendering
2. Verify wait timeout is sufficient
3. Add explicit wait for slide card SVG elements if needed
4. Test export with both styles

**Success Criteria**: PNG exports show SVG graphics

### Step 5: Test Theme Demo Cards
**Goal**: Verify theme demo cards show graphics correctly

**Actions**:
1. Regenerate theme demo
2. Check both two-card and single-card examples
3. Verify SVG graphics are visible in exported PNGs
4. Confirm graphics are properly sized for landscape format (lower third)

**Success Criteria**: All theme demo cards show SVG graphics

## Implementation Steps

### Priority 1: Preserve and Fix Default Style
1. **Verify Original Layout**:
   - Badge (top-right)
   - Title (top)
   - Tagline (below title)
   - Mockup (middle, 140px height)
   - Subtext (below mockup)
   - Features (bottom)

2. **Fix SVG Visibility**:
   - Ensure `.card-mockup` has explicit height (140px)
   - Ensure inner SVG.js div fills container (`width: 100%; height: 100%`)
   - Verify SVG.js container div has proper flexbox centering
   - Check SVG.js script execution timing

### Priority 2: Fix Lower Third Style
1. **Container Setup**:
   - Fix aspect ratio container (`padding-bottom: 66.67%`)
   - Position SVG.js div absolutely within container
   - Match SVG.js size to container aspect ratio

2. **Layout**:
   - Mockup in top 2/3 (landscape format)
   - Text content in bottom 1/3
   - Ensure proper spacing and typography

### Priority 2: Fix SVG.js Size Parameters
1. **Default Style**: Keep `240x140` (portrait)
2. **Lower Third Style**: Use `400x200` or calculate from container width
3. Ensure SVG.js viewBox matches container aspect ratio

### Priority 3: Verify Export Timing
1. Check if export waits for SVG.js
2. Add specific wait for slide card SVG elements
3. Test export timing with both styles

### Priority 4: Test and Validate
1. Create test script with both styles
2. Generate PNGs and verify SVG visibility
3. Update theme demo
4. Verify all cards show graphics

## Testing Checklist

- [ ] Default style card shows SVG graphic
- [ ] Lower third style card shows SVG graphic in top 2/3
- [ ] SVG graphics are properly sized (not too small/large)
- [ ] SVG graphics are centered in container
- [ ] PNG export captures SVG graphics
- [ ] Theme demo cards show graphics correctly
- [ ] Both custom mockup and default mockup work
- [ ] SVG.js code executes correctly
- [ ] Container aspect ratios are correct

## Files to Modify

1. `modern_graphics/diagrams/slide_cards.py`
   - Fix `.card-mockup` CSS for both styles
   - Adjust SVG.js container div styling
   - Fix SVG.js size parameters for lower third

2. `modern_graphics/export.py` (if needed)
   - Add specific wait for slide card SVG elements
   - Verify timing for SVG.js rendering

3. `examples/generate_complete_theme_demo.py`
   - Update card mockups if needed for landscape format
   - Verify cards generate correctly

## Success Metrics

- All slide cards show visible SVG graphics
- Lower third cards have graphics in top 2/3
- Default cards have graphics in middle section
- PNG exports capture SVG graphics correctly
- Theme demo shows all graphics properly
