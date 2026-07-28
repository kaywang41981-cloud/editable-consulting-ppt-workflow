#!/usr/bin/env python3
"""Check required presentation fonts against installed system font families."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from inspect_pptx import inspect


def normalize(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def installed_families() -> set[str]:
    families: set[str] = set()
    fc_list = shutil.which("fc-list")
    if fc_list:
        proc = subprocess.run(
            [fc_list, "--format", "%{family}\n"], capture_output=True, text=True, check=False
        )
        for line in proc.stdout.splitlines():
            for family in line.split(","):
                if family.strip():
                    families.add(family.strip())

    for directory in (
        Path.home() / "Library/Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
        Path("C:/Windows/Fonts"),
        Path.home() / ".fonts",
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
    ):
        if directory.exists():
            for file in directory.rglob("*"):
                if file.suffix.casefold() in {".ttf", ".otf", ".ttc"}:
                    families.add(file.stem)
    return families


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx")
    parser.add_argument("--require", nargs="+", default=["Microsoft YaHei", "Arial"])
    parser.add_argument("--preview-only", action="store_true")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    installed = installed_families()
    installed_normalized = {normalize(item): item for item in installed}
    required = list(dict.fromkeys(args.require))
    resolved: dict[str, str | None] = {}
    for font in required:
        target = normalize(font)
        exact = installed_normalized.get(target)
        if not exact:
            exact = next(
                (
                    original
                    for norm, original in installed_normalized.items()
                    if target in norm
                    or (len(norm) >= max(6, int(len(target) * 0.8)) and norm in target)
                ),
                None,
            )
        resolved[font] = exact

    referenced: list[str] = []
    if args.pptx:
        try:
            referenced = list(inspect(args.pptx).get("fontsReferenced", []))
        except Exception as exc:  # noqa: BLE001
            print(f"check_fonts: unable to inspect PPTX fonts: {exc}", file=sys.stderr)

    missing = [font for font, match in resolved.items() if match is None]
    report = {
        "status": "preview_only" if missing and args.preview_only else "fail" if missing else "pass",
        "required": required,
        "resolved": resolved,
        "missing": missing,
        "pptxFontsReferenced": referenced,
        "installedFamilyCount": len(installed),
        "finalDeliveryAllowed": not missing,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 0 if not missing or args.preview_only else 2


if __name__ == "__main__":
    raise SystemExit(main())
