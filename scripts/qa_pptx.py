#!/usr/bin/env python3
"""Run a portable PPTX QA suite and write a Markdown acceptance report."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run_json(command: list[str]) -> tuple[int, dict[str, object] | None, str]:
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    output = proc.stdout.strip()
    try:
        data = json.loads(output) if output else None
    except json.JSONDecodeError:
        data = None
    return proc.returncode, data, (proc.stderr or output).strip()


def status_line(name: str, code: int, data: dict[str, object] | None) -> str:
    status = data.get("status") if data else "error"
    return f"- {name}: **{status}** (exit {code})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", required=True)
    parser.add_argument("--template")
    parser.add_argument("--report", required=True)
    parser.add_argument("--require-sources", action="store_true")
    parser.add_argument("--preview-only", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--render-engine", choices=("auto", "powerpoint-mac", "libreoffice"), default="auto")
    parser.add_argument("--powerpoint-accepted", action="store_true")
    args = parser.parse_args()

    pptx = str(Path(args.pptx).resolve())
    report_path = Path(args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    result_dir = report_path.parent / f"{report_path.stem}-artifacts"
    result_dir.mkdir(parents=True, exist_ok=True)
    checks: list[tuple[str, int, dict[str, object] | None, str]] = []

    inspect_cmd = [sys.executable, str(SCRIPT_DIR / "inspect_pptx.py"), pptx]
    if args.require_sources:
        inspect_cmd.append("--require-sources")
    code, data, log = run_json(inspect_cmd)
    checks.append(("PPTX structure", code, data, log))

    font_cmd = [
        sys.executable,
        str(SCRIPT_DIR / "check_fonts.py"),
        "--pptx",
        pptx,
        "--require",
        "Microsoft YaHei",
        "Arial",
    ]
    if args.preview_only:
        font_cmd.append("--preview-only")
    code, data, log = run_json(font_cmd)
    checks.append(("Required fonts", code, data, log))

    if args.template:
        code, data, log = run_json(
            [
                sys.executable,
                str(SCRIPT_DIR / "compare_template.py"),
                "--template",
                str(Path(args.template).resolve()),
                "--final",
                pptx,
            ]
        )
        checks.append(("Template fidelity", code, data, log))

    if args.render:
        code, data, log = run_json(
            [
                sys.executable,
                str(SCRIPT_DIR / "render_pptx.py"),
                pptx,
                "--out-dir",
                str(result_dir / "render"),
                "--engine",
                args.render_engine,
            ]
        )
        checks.append(("Render", code, data, log))

    blocked = any(code != 0 for _, code, _, _ in checks)
    if blocked:
        delivery_status = "Blocked"
    elif args.preview_only:
        delivery_status = "Preview only"
    elif args.powerpoint_accepted:
        delivery_status = "Final"
    else:
        delivery_status = "Candidate"

    lines = [
        "# PPTX QA Report",
        "",
        f"- File: `{pptx}`",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Delivery status: **{delivery_status}**",
        "",
        "## Automated checks",
        "",
    ]
    for name, code, data, _ in checks:
        lines.append(status_line(name, code, data))

    lines.extend(
        [
            "",
            "## Manual full-size review",
            "",
            "- [ ] Every slide inspected individually at full size",
            "- [ ] No unintended clipping, overlap, wrapping, or off-canvas content",
            "- [ ] Titles, labels, axes, legends, units, and source footnotes are legible",
            "- [ ] Images have correct identity, crop, resolution, and aspect ratio",
            "- [ ] Final slides match approved SVGs or deviations are documented",
            "- [ ] Chart/table display matches source data and embedded workbook",
            "",
            "## Microsoft PowerPoint for macOS acceptance",
            "",
            f"- [{'x' if args.powerpoint_accepted else ' '}] Opened and inspected in Microsoft PowerPoint for macOS",
            "- [ ] Required fonts resolved without substitution",
            "- [ ] Native charts open editable embedded Excel data",
            "- [ ] Masters, layouts, headers, footers, logos, and page numbers behave correctly",
            "- [ ] Saved, closed, reopened, and rechecked where risk is high",
            "",
            "## Detailed tool output",
            "",
        ]
    )
    for name, code, data, log in checks:
        lines.extend([f"### {name}", "", "```json"])
        if data is not None:
            lines.append(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            lines.append(json.dumps({"exit": code, "log": log}, ensure_ascii=False, indent=2))
        lines.extend(["```", ""])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    summary = {
        "status": delivery_status,
        "report": str(report_path),
        "blocked": blocked,
        "checks": [
            {"name": name, "exit": code, "status": data.get("status") if data else "error"}
            for name, code, data, _ in checks
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
