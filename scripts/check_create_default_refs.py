#!/usr/bin/env python3
"""Guardrail: ensure create-default docs/scripts don't reference old feature flag."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = "MODERN_GRAPHICS_ENABLE_CREATE"

ALLOWLIST = {
    Path("docs/MIGRATION.md"),
    Path("scripts/check_create_default_refs.py"),
}


def _is_allowed(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if rel in ALLOWLIST:
        return True
    return rel.parts[:2] == ("docs", "archive")


def main() -> int:
    candidates = [
        ROOT / "README.md",
        *sorted((ROOT / "docs").rglob("*.md")),
        *sorted((ROOT / "scripts").glob("*.py")),
        *sorted((ROOT / "tests" / "smoke").glob("*.py")),
    ]

    offenders: list[tuple[Path, int, str]] = []
    for path in candidates:
        if not path.exists() or _is_allowed(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for idx, line in enumerate(text.splitlines(), start=1):
            if PATTERN in line:
                offenders.append((path.relative_to(ROOT), idx, line.strip()))

    if offenders:
        print("Found disallowed feature-flag references:")
        for path, line_no, line in offenders:
            print(f"- {path}:{line_no}: {line}")
        print("\nAllowed locations: docs/MIGRATION.md and docs/archive/*")
        return 1

    print("Create-default reference check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
