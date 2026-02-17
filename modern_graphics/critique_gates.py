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
    density_items: int = 0,
    max_density_items: int = 8,
    contrast_ratio: float = 4.5,
    min_contrast_ratio: float = 4.5,
    whitespace_ratio: float = 0.0,
    max_whitespace_ratio: float = 0.35,
    min_whitespace_ratio: float = 0.10,
    headline_text_px: int = 0,
    body_text_px: int = 0,
    min_headline_to_body_ratio: float = 1.35,
    panel_density_items: int = 0,
    max_panel_density_items: int = 6,
    panel_balance_ratio: float = 1.0,
    min_panel_balance_ratio: float = 0.70,
    max_panel_balance_ratio: float = 1.30,
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

    if density_items > max_density_items:
        results.append(
            GateResult(
                gate="density_budget",
                status="warn",
                detail=f"Density items {density_items} above target {max_density_items}",
            )
        )
    else:
        results.append(GateResult(gate="density_budget", status="pass", detail="OK"))

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

    if whitespace_ratio < min_whitespace_ratio:
        results.append(
            GateResult(
                gate="whitespace_floor",
                status="warn",
                detail=(
                    f"Whitespace ratio {whitespace_ratio:.2f} below recommended "
                    f"minimum {min_whitespace_ratio:.2f}"
                ),
            )
        )
    else:
        results.append(GateResult(gate="whitespace_floor", status="pass", detail="OK"))

    if headline_text_px > 0 and body_text_px > 0:
        ratio = headline_text_px / max(body_text_px, 1)
        if ratio < min_headline_to_body_ratio:
            results.append(
                GateResult(
                    gate="headline_hierarchy",
                    status="warn",
                    detail=(
                        f"Headline/body ratio {ratio:.2f} below target "
                        f"{min_headline_to_body_ratio:.2f}"
                    ),
                )
            )
        else:
            results.append(
                GateResult(gate="headline_hierarchy", status="pass", detail="OK")
            )

    if panel_density_items > max_panel_density_items:
        results.append(
            GateResult(
                gate="panel_density_budget",
                status="warn",
                detail=(
                    f"Panel density {panel_density_items} above target "
                    f"{max_panel_density_items}"
                ),
            )
        )
    else:
        results.append(GateResult(gate="panel_density_budget", status="pass", detail="OK"))

    if panel_balance_ratio < min_panel_balance_ratio or panel_balance_ratio > max_panel_balance_ratio:
        results.append(
            GateResult(
                gate="panel_balance",
                status="warn",
                detail=(
                    f"Panel balance ratio {panel_balance_ratio:.2f} outside "
                    f"[{min_panel_balance_ratio:.2f}, {max_panel_balance_ratio:.2f}]"
                ),
            )
        )
    else:
        results.append(GateResult(gate="panel_balance", status="pass", detail="OK"))

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
