#!/usr/bin/env python3
"""Generate deterministic export-fixture snapshots for Phase 4 drift detection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT))

from modern_graphics.generator import ModernGraphicsGenerator  # noqa: E402
from modern_graphics.export_policy import DEFAULT_EXPORT_POLICY  # noqa: E402

FIXTURE_PATH = ROOT / "tests" / "smoke" / "fixtures_export_phase4.json"
REPORT_DIR = ROOT / "reports"
SNAPSHOT_DIR = REPORT_DIR / "export-fixtures"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _render_fixture(generator: ModernGraphicsGenerator, fixture: Dict) -> Dict[str, str]:
    layout = fixture["layout"]
    payload = fixture.get("payload", {})
    html = generator.generate_layout(layout, **payload)
    return {"layout": layout, "html": html}


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    fixtures: List[Dict] = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    generator = ModernGraphicsGenerator("Export Fixture Harness")

    snapshots: List[Dict[str, str]] = []
    for index, fixture in enumerate(fixtures, start=1):
        rendered = _render_fixture(generator, fixture)
        stem = f"{index:02d}-{fixture['id']}"
        html_path = SNAPSHOT_DIR / f"{stem}.html"
        html_path.write_text(rendered["html"], encoding="utf-8")
        snapshots.append(
            {
                "id": fixture["id"],
                "layout": rendered["layout"],
                "path": str(html_path.relative_to(ROOT)),
                "chars": len(rendered["html"]),
                "sha256": _sha256(rendered["html"]),
            }
        )

    payload = {
        "fixtures": snapshots,
        "summary": {
            "count": len(snapshots),
            "snapshot_dir": str(SNAPSHOT_DIR.relative_to(ROOT)),
            "default_crop_mode": DEFAULT_EXPORT_POLICY.crop_mode,
            "default_padding_mode": DEFAULT_EXPORT_POLICY.padding_mode,
            "default_padding_px": DEFAULT_EXPORT_POLICY.resolve_padding(),
        },
        "export_matrix": [
            {
                "crop_mode": "none",
                "padding_mode": "none",
                "padding_px": 0,
                "intent": "Full-page capture, no trim",
            },
            {
                "crop_mode": "safe",
                "padding_mode": "minimal",
                "padding_px": 8,
                "intent": "Default reusable output",
            },
            {
                "crop_mode": "tight",
                "padding_mode": "minimal",
                "padding_px": 4,
                "intent": "Tighter social-style crop",
            },
        ],
    }

    out_json = REPORT_DIR / "phase4-export-fixtures.json"
    out_md = REPORT_DIR / "phase4-export-fixtures.md"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Phase 4 Export Fixture Report",
        "",
        f"- fixture count: **{payload['summary']['count']}**",
        f"- snapshot dir: `{payload['summary']['snapshot_dir']}`",
        f"- default crop mode: **{payload['summary']['default_crop_mode']}**",
        f"- default padding mode: **{payload['summary']['default_padding_mode']}** ({payload['summary']['default_padding_px']}px)",
        "",
        "## Snapshot Set",
        "",
    ]
    for item in snapshots:
        lines.append(
            f"- `{item['id']}` (`{item['layout']}`): `{item['path']}` | chars={item['chars']} | sha256=`{item['sha256'][:12]}...`"
        )

    lines.extend(["", "## Export Matrix", ""])
    for row in payload["export_matrix"]:
        lines.append(
            f"- `{row['crop_mode']}` + `{row['padding_mode']}` ({row['padding_px']}px): {row['intent']}"
        )
    lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {out_json}")
    print(f"wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
