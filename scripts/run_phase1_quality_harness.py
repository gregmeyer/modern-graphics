#!/usr/bin/env python3
"""Run Phase 1 quality harness and token debt scan.

Outputs:
- reports/phase1-quality.json
- reports/phase1-quality.md
- reports/phase1-token-debt.json
- reports/phase1-token-debt.md
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT))

from modern_graphics.critique_gates import (  # noqa: E402
    run_clarity_gates,
    overall_status,
)
from modern_graphics.visual_system import scan_files_for_ad_hoc_literals  # noqa: E402
from modern_graphics.template_lint import run_template_lint  # noqa: E402

FIXTURE_PATH = ROOT / "tests" / "smoke" / "fixtures_phase1.json"
REPORT_DIR = ROOT / "reports"

HARD_FAIL_GATES = {"min_text_size", "contrast_ratio", "whitespace_guard"}
SOFT_WARN_GATES = {"focal_point_budget", "density_budget"}


def _load_fixtures(path: Path) -> List[Dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("fixtures file must contain a JSON array")
    return data


def _quality_reports(fixtures: List[Dict]) -> Dict:
    reports = []
    summary = {"pass": 0, "warn": 0, "fail": 0}

    for fx in fixtures:
        report = run_clarity_gates(
            target=fx["target"],
            min_text_px=fx.get("min_text_px", 13),
            observed_min_text_px=fx["observed_min_text_px"],
            focal_points=fx["focal_points"],
            max_focal_points=fx.get("max_focal_points", 2),
            density_items=fx.get("density_items", 0),
            max_density_items=fx.get("max_density_items", 8),
            contrast_ratio=fx.get("contrast_ratio", 4.5),
            min_contrast_ratio=fx.get("min_contrast_ratio", 4.5),
            whitespace_ratio=fx.get("whitespace_ratio", 0.0),
            max_whitespace_ratio=fx.get("max_whitespace_ratio", 0.35),
            min_whitespace_ratio=fx.get("min_whitespace_ratio", 0.10),
            headline_text_px=fx.get("headline_text_px", 0),
            body_text_px=fx.get("body_text_px", 0),
            min_headline_to_body_ratio=fx.get("min_headline_to_body_ratio", 1.35),
            panel_density_items=fx.get("panel_density_items", fx.get("density_items", 0)),
            max_panel_density_items=fx.get("max_panel_density_items", 6),
            panel_balance_ratio=fx.get("panel_balance_ratio", 1.0),
            min_panel_balance_ratio=fx.get("min_panel_balance_ratio", 0.70),
            max_panel_balance_ratio=fx.get("max_panel_balance_ratio", 1.30),
        )

        gate_status = {r.gate: r.status for r in report.results}
        hard_fails = [g for g in HARD_FAIL_GATES if gate_status.get(g) == "fail"]
        soft_warns = [g for g in SOFT_WARN_GATES if gate_status.get(g) == "warn"]
        insight_warns = [
            g
            for g in {"headline_hierarchy", "panel_density_budget", "panel_balance", "whitespace_floor"}
            if gate_status.get(g) == "warn"
        ]

        status = "fail" if hard_fails else ("warn" if (soft_warns or insight_warns) else overall_status(report))
        summary[status] += 1
        reports.append(
            {
                "target": report.target,
                "status": status,
                "hard_fail_gates": hard_fails,
                "soft_warn_gates": soft_warns,
                "insight_warn_gates": insight_warns,
                "results": [asdict(r) for r in report.results],
            }
        )

    return {"summary": summary, "hard_fail_gates": sorted(HARD_FAIL_GATES), "soft_warn_gates": sorted(SOFT_WARN_GATES), "reports": reports}


def _quality_markdown(payload: Dict) -> str:
    lines = ["# Phase 1 Quality Report", ""]
    s = payload["summary"]
    lines.append(f"- pass: **{s['pass']}**")
    lines.append(f"- warn: **{s['warn']}**")
    lines.append(f"- fail: **{s['fail']}**")
    lines.append("")
    lines.append("## Per Layout")
    lines.append("")
    for report in payload["reports"]:
        lines.append(f"### {report['target']} - {report['status'].upper()}")
        if report["hard_fail_gates"]:
            lines.append(f"- hard fails: `{', '.join(report['hard_fail_gates'])}`")
        if report["soft_warn_gates"]:
            lines.append(f"- soft warns: `{', '.join(report['soft_warn_gates'])}`")
        if report.get("insight_warn_gates"):
            lines.append(f"- insight warns: `{', '.join(report['insight_warn_gates'])}`")
        for item in report["results"]:
            lines.append(f"- `{item['gate']}`: **{item['status']}** - {item['detail']}")
        lines.append("")
    return "\n".join(lines)


def _core_layout_files() -> List[Path]:
    diagrams = (ROOT / "modern_graphics" / "diagrams").glob("*.py")
    files = [p for p in diagrams if p.name != "__init__.py"]
    files.extend(
        [
            ROOT / "modern_graphics" / "color_scheme.py",
            ROOT / "modern_graphics" / "generator.py",
            ROOT / "modern_graphics" / "convenience.py",
        ]
    )
    return sorted([p for p in files if p.exists()])


def _token_debt_report() -> Dict:
    files = _core_layout_files()
    findings = scan_files_for_ad_hoc_literals(files)
    totals = {"files_scanned": len(files), "files_with_findings": len(findings), "total_findings": sum(len(v) for v in findings.values())}
    return {"summary": totals, "findings": findings}


def _token_debt_markdown(payload: Dict) -> str:
    lines = ["# Phase 1 Token Debt Report", ""]
    s = payload["summary"]
    lines.append(f"- files scanned: **{s['files_scanned']}**")
    lines.append(f"- files with findings: **{s['files_with_findings']}**")
    lines.append(f"- total findings: **{s['total_findings']}**")
    lines.append("")
    lines.append("## Top Files By Finding Count")
    lines.append("")
    ranked = sorted(payload["findings"].items(), key=lambda x: len(x[1]), reverse=True)
    for path, issues in ranked[:20]:
        lines.append(f"- `{Path(path).as_posix()}`: {len(issues)}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    fixtures = _load_fixtures(FIXTURE_PATH)
    quality = _quality_reports(fixtures)
    quality_json = REPORT_DIR / "phase1-quality.json"
    quality_md = REPORT_DIR / "phase1-quality.md"
    quality_json.write_text(json.dumps(quality, indent=2), encoding="utf-8")
    quality_md.write_text(_quality_markdown(quality), encoding="utf-8")

    debt = _token_debt_report()
    debt_json = REPORT_DIR / "phase1-token-debt.json"
    debt_md = REPORT_DIR / "phase1-token-debt.md"
    debt_json.write_text(json.dumps(debt, indent=2), encoding="utf-8")
    debt_md.write_text(_token_debt_markdown(debt), encoding="utf-8")

    strict_paths = [
        ROOT / "modern_graphics" / "layout_models.py",
        ROOT / "modern_graphics" / "layouts.py",
        ROOT / "modern_graphics" / "generator.py",
        ROOT / "modern_graphics" / "template_lint.py",
    ]
    strict_lint = run_template_lint(strict_paths, mode="strict")
    strict_json = REPORT_DIR / "phase2-strict-lint.json"
    strict_md = REPORT_DIR / "phase2-strict-lint.md"
    strict_json.write_text(json.dumps(strict_lint, indent=2), encoding="utf-8")
    strict_md.write_text(
        "\n".join(
            [
                "# Phase 2 Strict Template Lint",
                "",
                f"- mode: **{strict_lint['mode']}**",
                f"- status: **{strict_lint['status']}**",
                f"- files scanned: **{strict_lint['summary']['files_scanned']}**",
                f"- files with findings: **{strict_lint['summary']['files_with_findings']}**",
                f"- total findings: **{strict_lint['summary']['total_findings']}**",
                "",
            ]
        ),
        encoding="utf-8",
    )

    insight_harness_script = ROOT / "scripts" / "run_insight_fixture_harness.py"
    subprocess.run([sys.executable, str(insight_harness_script)], check=True, cwd=str(ROOT))

    print(f"wrote {quality_json}")
    print(f"wrote {quality_md}")
    print(f"wrote {debt_json}")
    print(f"wrote {debt_md}")
    print(f"wrote {strict_json}")
    print(f"wrote {strict_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
