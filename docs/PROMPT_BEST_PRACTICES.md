# Prompt Best Practices

Guidelines for creating effective prompts that produce high-quality templates.

## Do's ✅

### Be Specific About Colors

**Good:**
```
"blue and gray"
"vibrant blue and purple accents"
"warm tones: orange and yellow"
"pastel pink and blue"
```

**Avoid:**
```
"some colors"
"nice colors"
"colorful"
```

**Why:** Specific colors help the AI understand your exact vision and produce consistent results.

### Mention Font Style

**Good:**
```
"modern sans-serif font"
"elegant serif typography"
"clean readable fonts"
```

**Avoid:**
```
"nice fonts"
"good typography"
```

**Why:** Font choice significantly impacts the overall aesthetic. Specifying font type helps achieve your desired look.

### Include Mood/Tone

**Good:**
```
"professional and trustworthy"
"energetic and innovative"
"calming and approachable"
```

**Avoid:**
```
"good"
"nice"
"looks good"
```

**Why:** Mood and tone guide the AI in making design decisions that align with your goals.

### Reference Known Styles When Helpful

**Good:**
```
"Apple-style: clean minimalist"
"Material Design: bold colors"
"corporate professional"
```

**Why:** Well-known design systems provide clear reference points that the AI can understand and adapt.

### Start Simple, Then Refine

**Good Approach:**
```
Iteration 1: "dark theme"
Iteration 2: "dark professional theme"
Iteration 3: "dark professional theme with blue accents"
Iteration 4: "dark professional theme with blue accents, modern sans-serif"
```

**Why:** Starting simple lets you see what the AI produces, then you can refine based on results.

### Use Clear Style Descriptions

**Good:**
```
"minimalist design"
"bold and vibrant"
"professional and corporate"
```

**Avoid:**
```
"clean looking"
"good design"
"nice style"
```

**Why:** Clear style descriptions provide concrete guidance for the AI.

## Don'ts ❌

### Don't Be Too Vague

**Bad:**
```
"make it look good"
"nice design"
"professional looking"
```

**Better:**
```
"professional corporate style with blue and gray, traditional fonts"
```

**Why:** Vague prompts produce unpredictable results. Be specific about what you want.

### Don't Use Conflicting Terms

**Bad:**
```
"minimalist but busy"
"simple but complex"
"bold but subtle"
```

**Better:**
```
"minimalist with subtle accents"
"simple design with one focal point"
"bold colors with subtle typography"
```

**Why:** Conflicting terms confuse the AI and produce inconsistent results.

### Don't Over-Specify Technical Details

**Bad:**
```
"use rgba(0, 122, 255, 0.3) for shadows, #007AFF for primary color, 
font-size 16px, line-height 1.5"
```

**Better:**
```
"blue accents with subtle shadows, modern sans-serif, readable text"
```

**Why:** The AI handles technical implementation. Focus on visual goals, not CSS specifics.

### Don't Use Brand Names Directly

**Bad:**
```
"use Apple's exact colors"
"copy Google's Material Design colors"
```

**Better:**
```
"Apple-style: clean minimalist with blue accents"
"Material Design: bold colors with elevation shadows"
```

**Why:** Use style descriptions rather than asking to copy specific brands. This produces original templates inspired by styles.

### Don't Include Too Many Requirements

**Bad:**
```
"minimalist design with lots of white space, blue and gray colors, 
sans-serif font, professional tone, high contrast, subtle shadows, 
rounded corners, modern aesthetic, clean typography, spacious layout"
```

**Better:**
```
"minimalist professional design with blue and gray, modern sans-serif, 
lots of white space"
```

**Why:** Too many requirements can conflict or overwhelm. Focus on the most important elements.

### Don't Skip Important Elements

**Missing Style:**
```
"blue and gray"  # What style? Minimalist? Bold? Professional?
```

**Better:**
```
"professional theme with blue and gray"
```

**Why:** Style provides crucial context for how colors and fonts should be applied.

## Common Mistakes

### Mistake 1: Too Generic

**Problem:**
```
"good design"
```

**Solution:**
```
"modern professional design with blue accents, clean sans-serif"
```

### Mistake 2: Missing Context

**Problem:**
```
"blue theme"
```

**Solution:**
```
"professional blue theme for corporate presentations"
```

### Mistake 3: Conflicting Instructions

**Problem:**
```
"minimalist but include lots of decorative elements"
```

**Solution:**
```
"minimalist design with subtle decorative accents"
```

### Mistake 4: Over-Technical

**Problem:**
```
"background: #FFFFFF, text: #1D1D1F, font-family: Inter, font-size: 16px"
```

**Solution:**
```
"light background with dark text, modern sans-serif, readable size"
```

## Iteration Strategy

### Step 1: Start with Basic Prompt
```
"dark professional theme"
```

### Step 2: Add Colors
```
"dark professional theme with blue accents"
```

### Step 3: Add Fonts
```
"dark professional theme with blue accents, modern sans-serif"
```

### Step 4: Add Mood/Tone
```
"dark professional theme with blue accents, modern sans-serif, 
clean and minimalist"
```

### Step 5: Refine Based on Results
Review the generated template and adjust:
- If colors are too bright: add "subtle" or "muted"
- If fonts are wrong: specify font type more clearly
- If mood is off: adjust tone description

## Prompt Length Guidelines

### Short (5-10 words) - Quick Iterations
```
"dark professional theme with blue accents"
```
**Best for:** Quick tests, clear vision, simple needs

### Medium (10-20 words) - Most Use Cases
```
"dark professional theme with blue accents, modern sans-serif font, 
clean and minimalist"
```
**Best for:** Most templates, balanced detail, good results

### Long (20+ words) - Specific Requirements
```
"dark professional theme with blue accents, modern sans-serif font, 
clean and minimalist, high contrast, spacious layout with generous 
white space, subtle shadows"
```
**Best for:** Brand guidelines, specific requirements, detailed vision

**Recommendation:** Start with medium-length prompts (10-20 words) for best results.

## Testing Your Prompts

### Test Process

1. **Generate template** from your prompt
2. **Review the result** - does it match your vision?
3. **Identify gaps** - what's missing or wrong?
4. **Refine prompt** - add specific elements
5. **Regenerate** - test the refined prompt
6. **Iterate** until satisfied

### What to Look For

**Colors:**
- Are colors what you expected?
- Are they the right intensity (vibrant vs subtle)?
- Do they work together?

**Fonts:**
- Is the font style correct (sans-serif vs serif)?
- Is it readable?
- Does it match the mood?

**Style:**
- Does it match your description?
- Is the overall aesthetic right?
- Are there unexpected elements?

**Mood:**
- Does it feel right?
- Professional vs playful?
- Modern vs classic?

## Troubleshooting

### Problem: Colors are wrong

**Solution:** Be more specific about colors
```
Before: "some blue"
After: "navy blue and light gray"
```

### Problem: Fonts don't match

**Solution:** Specify font type clearly
```
Before: "nice fonts"
After: "modern sans-serif font"
```

### Problem: Style is off

**Solution:** Add clear style description
```
Before: "blue theme"
After: "professional blue theme"
```

### Problem: Too busy/cluttered

**Solution:** Add minimalist elements
```
Before: "blue and gray design"
After: "minimalist design with blue and gray, lots of white space"
```

### Problem: Too plain/boring

**Solution:** Add energy or vibrancy
```
Before: "professional theme"
After: "modern professional theme with vibrant blue accents"
```

## Advanced Tips

### Combine Style References with Customization

```
"Apple-style but with warmer tones, blue and orange accents instead 
of just blue"
```

### Use Comparative Descriptions

```
"more minimalist than Material Design"
"less bold than typical startup style"
"more professional than creative portfolio"
```

### Specify Use Case Context

```
"corporate presentation style, professional blue and gray, traditional 
fonts, conservative and trustworthy"
```

The use case context helps the AI make appropriate choices.

## Summary

**Best Practices:**
1. ✅ Be specific about colors, fonts, and style
2. ✅ Include mood/tone descriptions
3. ✅ Start simple, then refine
4. ✅ Use style references when helpful
5. ✅ Test and iterate

**Avoid:**
1. ❌ Vague descriptions
2. ❌ Conflicting terms
3. ❌ Over-technical details
4. ❌ Too many requirements
5. ❌ Skipping important elements

**Remember:** Good prompts are specific, clear, and focused. Start simple and refine based on results.

## Next Steps

- See [PROMPT_PATTERNS.md](./PROMPT_PATTERNS.md) for prompt structure guidance
- Check [PROMPT_EXAMPLES.md](./PROMPT_EXAMPLES.md) for ready-to-use prompts
- Review [USE_CASES.md](./USE_CASES.md) for real-world scenarios
