#!/usr/bin/env python3
"""Render PPTX to PDF/PNG using PowerPoint for macOS or LibreOffice."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def find_command(*names: str) -> str | None:
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def render_with_libreoffice(pptx: Path, out_dir: Path) -> tuple[Path, list[str]]:
    command = find_command("soffice", "libreoffice")
    if not command:
        raise RuntimeError("LibreOffice/soffice not found")
    profile = out_dir / ".libreoffice-profile"
    profile.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [
            command,
            f"-env:UserInstallation={profile.as_uri()}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(pptx),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "LibreOffice conversion failed").strip())
    pdf = out_dir / f"{pptx.stem}.pdf"
    if not pdf.exists():
        candidates = sorted(out_dir.glob("*.pdf"), key=lambda item: item.stat().st_mtime, reverse=True)
        if not candidates:
            raise RuntimeError("LibreOffice reported success but produced no PDF")
        pdf = candidates[0]
    return pdf, [proc.stdout.strip(), proc.stderr.strip()]


def render_with_powerpoint(pptx: Path, out_dir: Path) -> tuple[Path, list[str]]:
    osascript = find_command("osascript")
    if not osascript:
        raise RuntimeError("osascript not found; PowerPoint automation requires macOS")
    pdf = out_dir / f"{pptx.stem}-powerpoint.pdf"
    script = [
        "on run argv",
        "set inputPptx to item 1 of argv",
        "set outputPdf to item 2 of argv",
        'tell application "Microsoft PowerPoint"',
        "activate",
        "open POSIX file inputPptx",
        "save active presentation in POSIX file outputPdf as save as PDF",
        "close active presentation saving no",
        "end tell",
        "return outputPdf",
        "end run",
    ]
    command = [osascript]
    for line in script:
        command.extend(["-e", line])
    command.extend(["--", str(pptx), str(pdf)])
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    if proc.returncode != 0 or not pdf.exists():
        message = proc.stderr or proc.stdout or "PowerPoint automation failed"
        raise RuntimeError(message.strip())
    return pdf, [proc.stdout.strip(), proc.stderr.strip()]


def pdf_to_pngs(pdf: Path, out_dir: Path) -> list[str]:
    pdftoppm = find_command("pdftoppm")
    if pdftoppm:
        prefix = out_dir / "slide"
        proc = subprocess.run(
            [pdftoppm, "-png", "-r", "144", str(pdf), str(prefix)],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return [str(path.resolve()) for path in sorted(out_dir.glob("slide-*.png"))]
    magick = find_command("magick", "convert")
    if magick:
        output_pattern = out_dir / "slide-%03d.png"
        proc = subprocess.run(
            [magick, "-density", "144", str(pdf), str(output_pattern)],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return [str(path.resolve()) for path in sorted(out_dir.glob("slide-*.png"))]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--engine", choices=("auto", "powerpoint-mac", "libreoffice"), default="auto")
    parser.add_argument("--json-out")
    args = parser.parse_args()
    pptx = Path(args.pptx).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    attempts: list[dict[str, str]] = []
    engines = [args.engine]
    if args.engine == "auto":
        engines = ["powerpoint-mac", "libreoffice"]

    pdf: Path | None = None
    engine_used: str | None = None
    logs: list[str] = []
    for engine in engines:
        try:
            if engine == "powerpoint-mac":
                pdf, logs = render_with_powerpoint(pptx, out_dir)
            else:
                pdf, logs = render_with_libreoffice(pptx, out_dir)
            engine_used = engine
            break
        except Exception as exc:  # noqa: BLE001
            attempts.append({"engine": engine, "error": str(exc)})

    if pdf is None or engine_used is None:
        report = {"status": "fail", "file": str(pptx), "attempts": attempts}
        payload = json.dumps(report, ensure_ascii=False, indent=2)
        print(payload)
        if args.json_out:
            Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
        return 2

    pngs = pdf_to_pngs(pdf, out_dir)
    report = {
        "status": "pass",
        "file": str(pptx),
        "engine": engine_used,
        "pdf": str(pdf.resolve()),
        "pngs": pngs,
        "attempts": attempts,
        "logs": [item for item in logs if item],
        "acceptance": (
            "PowerPoint render completed; full-size human inspection is still required"
            if engine_used == "powerpoint-mac"
            else "Preliminary render only; Microsoft PowerPoint for macOS acceptance remains required"
        ),
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
