#!/usr/bin/env python3
"""Compare a final PPTX with its source template for master/layout/theme fidelity."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pptx_utils import open_pptx, sha256_parts, slide_size


PREFIXES = ("ppt/slideMasters/", "ppt/slideLayouts/", "ppt/theme/")


def compare(template_path: str, final_path: str, mode: str = "strict") -> dict[str, object]:
    with open_pptx(template_path) as template, open_pptx(final_path) as final:
        template_size = slide_size(template)
        final_size = slide_size(final)
        template_hashes = sha256_parts(template, PREFIXES)
        final_hashes = sha256_parts(final, PREFIXES)
        missing = sorted(set(template_hashes) - set(final_hashes))
        added = sorted(set(final_hashes) - set(template_hashes))
        changed = sorted(
            part
            for part in set(template_hashes) & set(final_hashes)
            if template_hashes[part] != final_hashes[part]
        )
        errors: list[str] = []
        warnings: list[str] = []
        if template_size != final_size:
            errors.append("Slide dimensions differ from the template")
        if missing:
            errors.append(f"Missing {len(missing)} template master/layout/theme parts")
        if mode == "strict" and changed:
            errors.append(f"Changed {len(changed)} template master/layout/theme parts")
        elif changed:
            warnings.append(f"Changed {len(changed)} template structure parts require review")
        if added:
            warnings.append(f"Added {len(added)} master/layout/theme parts")
        return {
            "status": "fail" if errors else "pass_with_warnings" if warnings else "pass",
            "mode": mode,
            "template": str(Path(template_path).resolve()),
            "final": str(Path(final_path).resolve()),
            "templateSlideSize": template_size,
            "finalSlideSize": final_size,
            "templatePartCount": len(template_hashes),
            "finalPartCount": len(final_hashes),
            "missingParts": missing,
            "changedParts": changed,
            "addedParts": added,
            "errors": errors,
            "warnings": warnings,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True)
    parser.add_argument("--final", required=True)
    parser.add_argument("--mode", choices=("strict", "inventory"), default="strict")
    parser.add_argument("--json-out")
    args = parser.parse_args()
    try:
        report = compare(args.template, args.final, args.mode)
    except Exception as exc:  # noqa: BLE001
        print(f"compare_template: {exc}", file=sys.stderr)
        return 2
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 2 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
