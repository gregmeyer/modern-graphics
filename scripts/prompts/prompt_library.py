"""Programmatic Prompt Library

Collection of prompts organized by category for programmatic use.
"""

# Minimalist Prompts
MINIMALIST_PROMPTS = [
    "minimalist design, lots of white space, simple colors, clean sans-serif",
    "ultra-minimalist, monochrome, geometric shapes, no gradients, bold typography",
    "minimalist design with subtle blue accents, lots of white space, clean modern sans-serif",
]

# Bold & Vibrant Prompts
BOLD_PROMPTS = [
    "bold vibrant colors, tech startup style, clean sans-serif, modern and energetic",
    "bold vibrant colors with high contrast, striking typography, modern and impactful",
    "vibrant colorful palette, playful and energetic, modern sans-serif, fun and engaging",
]

# Professional & Corporate Prompts
PROFESSIONAL_PROMPTS = [
    "corporate blue and gray, professional, traditional fonts, conservative and trustworthy",
    "modern professional theme, navy blue and silver, clean sans-serif, authoritative but approachable",
    "enterprise style, navy blue and silver, formal typography, authoritative and professional",
]

# Dark Theme Prompts
DARK_PROMPTS = [
    "dark professional theme with blue accents, modern sans-serif font, clean and minimalist",
    "dark theme with vibrant blue and purple accents, modern sans-serif, high contrast",
    "dark minimalist design, subtle colors, lots of space, clean typography",
]

# Light Theme Prompts
LIGHT_PROMPTS = [
    "light minimalist design with pastel colors, elegant serif typography, spacious and airy",
    "bright clean design, white background, subtle colors, modern sans-serif, fresh and modern",
    "soft pastel colors, light and airy, gentle typography, calming and approachable",
]

# Creative & Artistic Prompts
CREATIVE_PROMPTS = [
    "creative and artistic, unique color palette, expressive typography, bold and distinctive",
    "artistic bold design, vibrant unexpected colors, creative typography, expressive and unique",
]

# Style Reference Prompts
STYLE_REFERENCE_PROMPTS = {
    "apple": "Apple-style: clean minimalist, lots of white space, SF Pro font, subtle gradients, modern and elegant",
    "material": "Material Design: bold colors, card-based layouts, Roboto font, elevation shadows, modern and accessible",
    "brutalist": "Brutalist: bold typography, high contrast, geometric shapes, minimal decoration, raw and unpolished",
}

# Industry-Specific Prompts
INDUSTRY_PROMPTS = {
    "tech_startup": "tech startup aesthetic, bold vibrant colors with blue and purple accents, modern sans-serif, energetic and innovative",
    "healthcare": "healthcare professional, clean blue and white, accessible fonts, trustworthy and calming, approachable and clear",
    "education": "educational friendly, bright but not overwhelming, clear readable fonts, engaging and approachable, warm and inviting",
    "finance": "financial professional, conservative blue and gray, traditional fonts, trustworthy and authoritative",
}


def get_prompts_by_category(category):
    """Get prompts by category"""
    categories = {
        "minimalist": MINIMALIST_PROMPTS,
        "bold": BOLD_PROMPTS,
        "professional": PROFESSIONAL_PROMPTS,
        "dark": DARK_PROMPTS,
        "light": LIGHT_PROMPTS,
        "creative": CREATIVE_PROMPTS,
    }
    return categories.get(category.lower(), [])


def get_style_reference_prompt(style):
    """Get style reference prompt"""
    return STYLE_REFERENCE_PROMPTS.get(style.lower())


def get_industry_prompt(industry):
    """Get industry-specific prompt"""
    return INDUSTRY_PROMPTS.get(industry.lower())


def list_all_prompts():
    """List all available prompts"""
    all_prompts = []
    
    # Category prompts
    for category in ["minimalist", "bold", "professional", "dark", "light", "creative"]:
        prompts = get_prompts_by_category(category)
        for prompt in prompts:
            all_prompts.append({"category": category, "prompt": prompt})
    
    # Style references
    for style, prompt in STYLE_REFERENCE_PROMPTS.items():
        all_prompts.append({"category": "style_reference", "style": style, "prompt": prompt})
    
    # Industry prompts
    for industry, prompt in INDUSTRY_PROMPTS.items():
        all_prompts.append({"category": "industry", "industry": industry, "prompt": prompt})
    
    return all_prompts


if __name__ == "__main__":
    print("Prompt Library")
    print("=" * 60)
    print()
    
    all_prompts = list_all_prompts()
    print(f"Total prompts: {len(all_prompts)}")
    print()
    
    # Show by category
    categories = {}
    for p in all_prompts:
        cat = p.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    for category, prompts in categories.items():
        print(f"{category.title()}: {len(prompts)} prompts")
        for p in prompts[:3]:  # Show first 3
            prompt_text = p["prompt"][:60] + "..." if len(p["prompt"]) > 60 else p["prompt"]
            print(f"  - {prompt_text}")
        if len(prompts) > 3:
            print(f"  ... and {len(prompts) - 3} more")
        print()
