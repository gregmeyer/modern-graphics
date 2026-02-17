"""Phase 1 critique gate scaffolding.

This module provides clarity-first checks and a report format used by the
quality harness.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class GateResult:
    gate: str
    status: str  # pass|warn|fail
    detail: str


@dataclass
class CritiqueReport:
    target: str
    results: List[GateResult]

    def to_dict(self) -> Dict:
        return {
            "target": self.target,
            "results": [asdict(r) for r in self.results],
        }


def run_clarity_gates(
    target: str,
    min_text_px: int,
    observed_min_text_px: int,
    focal_points: int,
    max_focal_points: int = 2,
    contrast_ratio: float = 4.5,
    min_contrast_ratio: float = 4.5,
    whitespace_ratio: float = 0.0,
    max_whitespace_ratio: float = 0.35,
) -> CritiqueReport:
    """Run initial quality gates for visual clarity.

    This is a first-pass scaffold. Future versions will read rendered output
    and compute these metrics automatically.
    """
    results: List[GateResult] = []

    if observed_min_text_px < min_text_px:
        results.append(
            GateResult(
                gate="min_text_size",
                status="fail",
                detail=f"Observed {observed_min_text_px}px below minimum {min_text_px}px",
            )
        )
    else:
        results.append(GateResult(gate="min_text_size", status="pass", detail="OK"))

    if focal_points > max_focal_points:
        results.append(
            GateResult(
                gate="focal_point_budget",
                status="warn",
                detail=f"Observed {focal_points} focal points above target {max_focal_points}",
            )
        )
    else:
        results.append(GateResult(gate="focal_point_budget", status="pass", detail="OK"))

    if contrast_ratio < min_contrast_ratio:
        results.append(
            GateResult(
                gate="contrast_ratio",
                status="fail",
                detail=(
                    f"Contrast ratio {contrast_ratio:.2f} below minimum "
                    f"{min_contrast_ratio:.2f}"
                ),
            )
        )
    else:
        results.append(GateResult(gate="contrast_ratio", status="pass", detail="OK"))

    if whitespace_ratio > max_whitespace_ratio:
        results.append(
            GateResult(
                gate="whitespace_guard",
                status="fail",
                detail=(
                    f"Whitespace ratio {whitespace_ratio:.2f} above maximum "
                    f"{max_whitespace_ratio:.2f}"
                ),
            )
        )
    else:
        results.append(GateResult(gate="whitespace_guard", status="pass", detail="OK"))

    return CritiqueReport(target=target, results=results)


def overall_status(report: CritiqueReport) -> str:
    """Return overall status: fail > warn > pass."""
    statuses = {r.status for r in report.results}
    if "fail" in statuses:
        return "fail"
    if "warn" in statuses:
        return "warn"
    return "pass"


def report_to_markdown(report: CritiqueReport) -> str:
    """Render a compact markdown report."""
    lines = [f"# Critique Report: {report.target}", ""]
    lines.append(f"Overall: **{overall_status(report)}**")
    lines.append("")
    for result in report.results:
        lines.append(f"- `{result.gate}`: **{result.status}** - {result.detail}")
    lines.append("")
    return "\n".join(lines)
