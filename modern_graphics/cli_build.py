"""Handlers for themes, build, and retheme commands."""

from pathlib import Path

from . import ModernGraphicsGenerator, Attribution
from .color_scheme import get_scheme


def handle_themes(args) -> int:
    """Handle the 'themes' command."""
    from .color_scheme import SCHEME_REGISTRY
    seen = set()
    print("\nAvailable themes:\n")
    print(f"  {'Name':<20} {'Primary':<10} {'Accent':<10} Description")
    print(f"  {'─' * 20} {'─' * 10} {'─' * 10} {'─' * 40}")
    for name, scheme in SCHEME_REGISTRY.items():
        if id(scheme) in seen:
            continue
        seen.add(id(scheme))
        aliases = [k for k, v in SCHEME_REGISTRY.items() if v is scheme and k != name]
        alias_str = f" (also: {', '.join(aliases)})" if aliases else ""
        desc = getattr(scheme, 'description', '') or ''
        primary = getattr(scheme, 'primary', '') or ''
        accent = getattr(scheme, 'accent', '') or ''
        print(f"  {name:<20} {primary:<10} {accent:<10} {desc}{alias_str}")
    print(f"\nUse with: modern-graphics create --theme <name> ...")
    return 0


def handle_build(args) -> int:
    """Handle the 'build' command (interactive graphic builder)."""
    import sys as _sys
    from .suggest import suggest_layout_top_n, LAYOUT_DESCRIPTIONS, EXAMPLE_COMMANDS
    from .color_scheme import SCHEME_REGISTRY

    if not _sys.stdin.isatty():
        print("Error: build command requires an interactive terminal.")
        print("Use: modern-graphics create --layout <layout> --output <path>")
        return 1

    print("\n── modern-graphics build ──\n")

    # Step 1: What's the message?
    try:
        desc = input("What do you want to show? ")
    except (EOFError, KeyboardInterrupt):
        print("")
        return 0

    # Step 2: Suggest layout
    results = suggest_layout_top_n(desc, n=3)
    best = results[0]
    print(f"\nSuggested: {best.layout} — {LAYOUT_DESCRIPTIONS.get(best.layout, '')}")
    if len(results) > 1:
        print("Alternatives:")
        for i, alt in enumerate(results[1:], 2):
            print(f"  {i}) {alt.layout} — {LAYOUT_DESCRIPTIONS.get(alt.layout, '')}")

    # Step 3: Confirm or pick
    try:
        pick = input(f"\nUse {best.layout}? [Y/number/layout name] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("")
        return 0

    if pick in ("", "y", "yes"):
        layout = best.layout
    elif pick.isdigit() and 1 < int(pick) <= len(results):
        layout = results[int(pick) - 1].layout
    elif pick in LAYOUT_DESCRIPTIONS:
        layout = pick
    else:
        layout = best.layout

    print(f"Layout: {layout}")

    # Step 4: Theme selection
    seen_themes = set()
    theme_names = []
    for name, scheme in SCHEME_REGISTRY.items():
        if id(scheme) not in seen_themes:
            seen_themes.add(id(scheme))
            theme_names.append(name)

    print(f"\nThemes: {', '.join(theme_names)}")
    try:
        theme_input = input("Theme? [corporate] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("")
        return 0
    theme = theme_input if theme_input and theme_input in SCHEME_REGISTRY else "corporate"
    print(f"Theme: {theme}")

    # Step 5: Collect layout-specific args
    layout_args = {}
    if layout == "hero":
        try:
            layout_args["headline"] = input("\nHeadline: ") or "Execution scales. Judgment does not."
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
    elif layout == "comparison":
        try:
            layout_args["left"] = input("\nLeft side (Title:Step1,Step2:Outcome): ")
            layout_args["right"] = input("Right side (Title:Step1,Step2:Outcome): ")
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
    elif layout in ("key-insight", "insight"):
        try:
            layout_args["text"] = input("\nInsight text: ") or "Key takeaway goes here."
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
    elif layout == "story":
        try:
            layout_args["what_changed"] = input("\nWhat changed? ") or "Execution capacity increased"
            layout_args["time_period"] = input("Over what period? ") or "this quarter"
            layout_args["what_it_means"] = input("Why it matters? ") or "Decision quality now drives outcomes"
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
    elif layout == "timeline":
        try:
            layout_args["events"] = input("\nEvents (Date|Event,Date|Event): ") or "Q1|Baseline,Q2|Adoption"
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
    elif layout == "funnel":
        try:
            layout_args["stages"] = input("\nStages (comma-separated): ") or "Visit,Trial,Paid"
            layout_args["values"] = input("Values (comma-separated): ") or "100,40,12"
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0
    elif layout == "grid":
        try:
            layout_args["items"] = input("\nItems (comma-separated): ") or "A,B,C"
        except (EOFError, KeyboardInterrupt):
            print("")
            return 0

    # Step 6: Generate
    output_path = getattr(args, 'output', None) or f"./output/{layout}.html"
    cmd_parts = ["modern-graphics", "create", "--layout", layout, "--theme", theme, "--output", output_path]
    for k, v in layout_args.items():
        flag = f"--{k.replace('_', '-')}"
        cmd_parts.extend([flag, v])

    print(f"\nGenerating: {' '.join(cmd_parts)}")

    # Build the args and call create logic inline via subprocess
    import subprocess
    result = subprocess.run(cmd_parts, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(result.stdout.strip())
        print(result.stderr.strip())
        return result.returncode

    # Step 7: Iterative loop
    while True:
        try:
            action = input("\nWhat next? [done/png/theme <name>/layout] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("")
            break

        if action in ("", "done", "q", "quit", "exit"):
            break
        elif action == "png":
            png_path = Path(output_path).with_suffix('.png')
            png_cmd = cmd_parts + ["--png"]
            png_cmd[png_cmd.index("--output") + 1] = str(png_path)
            result = subprocess.run(png_cmd, capture_output=True, text=True)
            print(result.stdout.strip() if result.returncode == 0 else result.stderr.strip())
        elif action.startswith("theme "):
            new_theme = action.split(" ", 1)[1]
            if new_theme in SCHEME_REGISTRY:
                theme = new_theme
                idx = cmd_parts.index("--theme")
                cmd_parts[idx + 1] = theme
                result = subprocess.run(cmd_parts, capture_output=True, text=True)
                print(result.stdout.strip() if result.returncode == 0 else result.stderr.strip())
            else:
                print(f"Unknown theme '{new_theme}'. Available: {', '.join(theme_names)}")
        elif action == "layout":
            print(f"\nAvailable layouts:")
            for lt, d in sorted(LAYOUT_DESCRIPTIONS.items()):
                print(f"  {lt:<20} {d}")
        else:
            print("Options: done, png, theme <name>, layout")

    return 0


def handle_retheme(args) -> int:
    """Handle the 'retheme' command."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        return 1

    scheme = get_scheme(args.theme)
    if scheme is None:
        print(f"Error: unknown theme '{args.theme}'. Use 'modern-graphics themes' to list available themes.")
        return 1

    html = input_path.read_text(encoding="utf-8")
    html = scheme.apply_to_html(html)

    out_path = Path(args.output) if args.output else input_path
    out_path.write_text(html, encoding="utf-8")
    print(f"Applied theme '{args.theme}': {out_path}")

    if getattr(args, 'png', False):
        attribution = Attribution(
            person=getattr(args, 'person', 'Greg Meyer'),
            website=getattr(args, 'website', 'gregmeyer.com'),
        )
        gen = ModernGraphicsGenerator("Retheme", attribution=attribution)
        png_path = out_path.with_suffix('.png')
        gen.export_to_png(html, png_path, crop_mode="safe")
        print(f"Exported PNG: {png_path}")

    return 0
