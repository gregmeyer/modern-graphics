"""Template lint helpers for strict tokenized layout checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Sequence


HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_RE = re.compile(r"(?<![\w-])\d+(?:\.\d+)?px\b")


@dataclass(frozen=True)
class TemplateLintViolation:
    path: str
    line: int
    rule: str
    literal: str
    source: str


def lint_file(path: Path) -> List[TemplateLintViolation]:
    violations: List[TemplateLintViolation] = []
    text = path.read_text(encoding="utf-8", errors="ignore")

    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        # Allow token-based CSS interpolation in f-strings.
        if "token." in line or "tokens." in line:
            continue
        if "http://" in line or "https://" in line:
            continue

        for match in PX_RE.finditer(line):
            violations.append(
                TemplateLintViolation(
                    path=str(path),
                    line=line_no,
                    rule="hardcoded_px",
                    literal=match.group(0),
                    source=raw,
                )
            )
        for match in HEX_RE.finditer(line):
            violations.append(
                TemplateLintViolation(
                    path=str(path),
                    line=line_no,
                    rule="hardcoded_hex",
                    literal=match.group(0),
                    source=raw,
                )
            )

    return violations


def run_template_lint(paths: Sequence[Path], mode: str = "advisory") -> Dict[str, object]:
    mode = (mode or "advisory").strip().lower()
    if mode not in {"advisory", "strict"}:
        mode = "advisory"

    findings: Dict[str, List[Dict[str, object]]] = {}
    total = 0
    scanned = 0

    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        scanned += 1
        violations = lint_file(path)
        if not violations:
            continue
        total += len(violations)
        findings[str(path)] = [
            {
                "line": v.line,
                "rule": v.rule,
                "literal": v.literal,
            }
            for v in violations
        ]

    status = "fail" if (mode == "strict" and total > 0) else ("warn" if total > 0 else "pass")
    return {
        "mode": mode,
        "status": status,
        "summary": {
            "files_scanned": scanned,
            "files_with_findings": len(findings),
            "total_findings": total,
        },
        "findings": findings,
    }

