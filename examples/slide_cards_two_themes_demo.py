"""Example: Same slide cards with two different themes.

Generates the same slide card diagram and slide card comparison twice—
once with a light theme (apple) and once with a dark theme—so you can
confirm theme support and compare output.

Run from utils/modern-graphics:
    PYTHONPATH=. python examples/test_slide_cards_two_themes.py

Output:
    examples/output/slide-cards-themes/
        slide_cards_theme_apple.html   (or first available light theme)
        slide_cards_theme_dark.html
        slide_compare_theme_apple.html
        slide_compare_theme_dark.html
"""

from pathlib import Path

from modern_graphics import ModernGraphicsGenerator, Attribution, get_scheme, list_schemes

OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "slide-cards-themes"

# Same card data for both themes
CARDS = [
    {
        "title": "Manual process",
        "tagline": "Step 1",
        "subtext": "Spreadsheets and one-off scripts.",
        "color": "blue",
        "features": ["Fragile", "No audit trail"],
    },
    {
        "title": "Automated pipeline",
        "tagline": "Step 2",
        "subtext": "Single source of truth.",
        "color": "green",
        "features": ["Repeatable", "Tracked"],
    },
]

LEFT_CARD = {"title": "Before", "tagline": "Legacy", "color": "gray", "features": ["Manual", "Slow"]}
RIGHT_CARD = {"title": "After", "tagline": "Modern", "color": "green", "features": ["Automated", "Fast"]}


def main():
    available = list_schemes()
    if not available:
        print("No themes registered.")
        return

    # Prefer apple (light) and dark; fallback to first two schemes
    light_theme = "apple" if "apple" in available else available[0]
    dark_theme = "dark" if "dark" in available else (available[1] if len(available) > 1 else available[0])

    themes = [(light_theme, "light"), (dark_theme, "dark")]
    print(f"Themes: {light_theme} (light), {dark_theme} (dark)")
    print(f"Output: {OUTPUT_DIR}\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for theme_name, label in themes:
        scheme = get_scheme(theme_name)
        generator = ModernGraphicsGenerator(
            title="Slide cards – theme demo",
            attribution=Attribution(copyright="© Demo 2025"),
        )

        # Slide cards (horizontal row)
        html_cards = generator.generate_slide_card_diagram(
            CARDS,
            arrow_text="→",
            style="default",
            color_scheme=scheme,
        )
        path_cards = OUTPUT_DIR / f"slide_cards_theme_{theme_name}.html"
        generator.save(html_cards, path_cards)
        print(f"  {path_cards.name}")

        # Slide compare (two cards side by side)
        html_compare = generator.generate_slide_card_comparison(
            LEFT_CARD,
            RIGHT_CARD,
            vs_text="vs",
            color_scheme=scheme,
        )
        path_compare = OUTPUT_DIR / f"slide_compare_theme_{theme_name}.html"
        generator.save(html_compare, path_compare)
        print(f"  {path_compare.name}")

    print(f"\nDone. Open the HTML files in {OUTPUT_DIR} to compare themes.")


if __name__ == "__main__":
    main()
