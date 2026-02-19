#!/usr/bin/env python3
"""Lightweight docs drift guard for README and core docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

ROOT = Path(__file__).resolve().parent.parent

# Docs that must keep task-first entry criteria language and top-level structure.
REQUIRED_HEADINGS = {
    "docs/QUICKSTART.md": ["## Use This Doc When"],
    "docs/CREATE_COMMAND.md": ["## Use This Doc When"],
    "docs/HERO_SLIDES.md": ["## Use This Doc When"],
    "docs/ADVANCED.md": ["## Use This Doc When", "## Fast Path"],
    "docs/EXPORT.md": ["## Use This Doc When", "## Fast Path"],
    "examples/README.md": ["## Use This Page When"],
}

# Index pages where repeated links usually indicate navigation drift.
NO_DUPLICATE_LINK_DOCS = [
    "README.md",
    "docs/README.md",
    "examples/README.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _iter_markdown_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "examples" / "README.md"]
    files.extend(
        p
        for p in (ROOT / "docs").rglob("*.md")
        if "archive" not in p.parts
    )
    return sorted(set(files))


def _extract_links(text: str) -> list[str]:
    return MARKDOWN_LINK_RE.findall(text)


def _is_local_link(link: str) -> bool:
    return not (
        link.startswith("http://")
        or link.startswith("https://")
        or link.startswith("mailto:")
        or link.startswith("#")
    )


def check_broken_links() -> list[str]:
    errors: list[str] = []
    for md_file in _iter_markdown_files():
        text = _read(md_file)
        for link in _extract_links(text):
            if not _is_local_link(link):
                continue
            target_rel = link.split("#", 1)[0]
            if not target_rel:
                continue
            target = (md_file.parent / target_rel).resolve()
            if not target.exists():
                rel_file = md_file.relative_to(ROOT)
                errors.append(f"{rel_file}: broken link target '{link}'")
    return errors


def check_duplicate_links() -> list[str]:
    errors: list[str] = []
    for rel in NO_DUPLICATE_LINK_DOCS:
        path = ROOT / rel
        text = _read(path)
        counts: dict[str, int] = {}
        for link in _extract_links(text):
            counts[link] = counts.get(link, 0) + 1
        dupes = [(link, count) for link, count in sorted(counts.items()) if count > 1]
        for link, count in dupes:
            errors.append(f"{rel}: duplicate link '{link}' appears {count} times")
    return errors


def check_required_headings() -> list[str]:
    errors: list[str] = []
    for rel, headings in REQUIRED_HEADINGS.items():
        text = _read(ROOT / rel)
        for heading in headings:
            if heading not in text:
                errors.append(f"{rel}: missing required heading '{heading}'")
    return errors


def main() -> int:
    failures: list[str] = []
    failures.extend(check_broken_links())
    failures.extend(check_duplicate_links())
    failures.extend(check_required_headings())

    if failures:
        print("docs drift check failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("docs drift check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
