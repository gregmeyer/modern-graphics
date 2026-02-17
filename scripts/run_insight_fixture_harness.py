#!/usr/bin/env python3
"""Generate deterministic insight fixture snapshots for drift detection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT))

from modern_graphics.generator import ModernGraphicsGenerator  # noqa: E402
from modern_graphics.layout_models import (  # noqa: E402
    InsightCardPayload,
    InsightStoryPayload,
    KeyInsightPayload,
)


FIXTURE_PATH = ROOT / "tests" / "smoke" / "fixtures_insight_cards.json"
REPORT_DIR = ROOT / "reports"
SNAPSHOT_DIR = REPORT_DIR / "insight-fixtures"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _render_fixture(generator: ModernGraphicsGenerator, fixture: Dict) -> Dict[str, str]:
    kind = fixture["kind"]
    if kind == "key_insight":
        payload = KeyInsightPayload(
            text=fixture["text"],
            label=fixture.get("label", "Key Insight"),
            variant=fixture.get("variant", "bold"),
            icon=fixture.get("icon", "lightning"),
        )
        layout = "key-insight"
    elif kind == "insight_card":
        payload = InsightCardPayload(
            text=fixture["text"],
            svg_content=fixture["svg_content"],
            label=fixture.get("label", "Key Insight"),
            svg_label=fixture.get("svg_label"),
            layout=fixture.get("layout", "side-by-side"),
            svg_position=fixture.get("svg_position", "right"),
            variant=fixture.get("variant", "bold"),
            icon=fixture.get("icon", "lightning"),
        )
        layout = "insight-card"
    elif kind == "insight_story":
        payload = InsightStoryPayload(
            headline=fixture["headline"],
            insight_text=fixture["insight_text"],
            before_svg=fixture["before_svg"],
            after_svg=fixture["after_svg"],
            subtitle=fixture.get("subtitle"),
            eyebrow=fixture.get("eyebrow"),
        )
        layout = "insight-story"
    else:
        raise ValueError(f"Unknown fixture kind: {kind}")

    html = generator.generate_layout(layout, **payload.to_strategy_kwargs())
    return {"layout": layout, "html": html}


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    fixtures: List[Dict] = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    generator = ModernGraphicsGenerator("Insight Fixture Harness")

    snapshots = []
    for index, fixture in enumerate(fixtures, start=1):
        rendered = _render_fixture(generator, fixture)
        stem = f"{index:02d}-{fixture['kind']}"
        html_path = SNAPSHOT_DIR / f"{stem}.html"
        html_path.write_text(rendered["html"], encoding="utf-8")
        snapshots.append(
            {
                "fixture": fixture["kind"],
                "layout": rendered["layout"],
                "path": str(html_path.relative_to(ROOT)),
                "sha256": _sha256(rendered["html"]),
                "chars": len(rendered["html"]),
            }
        )

    payload = {
        "fixtures": snapshots,
        "summary": {
            "count": len(snapshots),
            "snapshot_dir": str(SNAPSHOT_DIR.relative_to(ROOT)),
        },
    }
    out_json = REPORT_DIR / "phase2-insight-fixtures.json"
    out_md = REPORT_DIR / "phase2-insight-fixtures.md"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Phase 2 Insight Fixture Report",
        "",
        f"- fixture count: **{payload['summary']['count']}**",
        f"- snapshot dir: `{payload['summary']['snapshot_dir']}`",
        "",
        "## Snapshots",
        "",
    ]
    for item in snapshots:
        lines.append(
            f"- `{item['fixture']}` (`{item['layout']}`): `{item['path']}` | chars={item['chars']} | sha256=`{item['sha256'][:12]}...`"
        )
    lines.append("")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {out_json}")
    print(f"wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

