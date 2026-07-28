#!/usr/bin/env python3
"""Validate an SVG approval preview for portability and basic font rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"


def dimension(value: str | None) -> float | None:
    if value is None:
        return None
    match = re.match(r"^\s*([0-9.]+)", value)
    return float(match.group(1)) if match else None


def validate(path: str, expected_width: float | None, expected_height: float | None) -> dict[str, object]:
    source = Path(path)
    root = ET.parse(source).getroot()
    errors: list[str] = []
    warnings: list[str] = []
    if root.tag not in {f"{{{SVG_NS}}}svg", "svg"}:
        errors.append("Root element is not SVG")
    view_box = root.attrib.get("viewBox", "")
    values = view_box.replace(",", " ").split()
    if len(values) != 4:
        errors.append("SVG requires a four-value viewBox")
        vb_width = vb_height = None
    else:
        try:
            vb_width, vb_height = float(values[2]), float(values[3])
            if vb_width <= 0 or vb_height <= 0:
                errors.append("SVG viewBox width and height must be positive")
        except ValueError:
            vb_width = vb_height = None
            errors.append("SVG viewBox contains non-numeric values")

    width = dimension(root.attrib.get("width")) or vb_width
    height = dimension(root.attrib.get("height")) or vb_height
    if expected_width is not None and width is not None and abs(width - expected_width) > 0.01:
        errors.append(f"SVG width {width} does not match expected {expected_width}")
    if expected_height is not None and height is not None and abs(height - expected_height) > 0.01:
        errors.append(f"SVG height {height} does not match expected {expected_height}")

    scripts = [node for node in root.iter() if node.tag.endswith("}script") or node.tag == "script"]
    if scripts:
        errors.append("SVG contains script elements")

    external_refs: list[str] = []
    font_families: set[str] = set()
    visible_text = []
    for node in root.iter():
        href = node.attrib.get("href") or node.attrib.get(f"{{{XLINK}}}href")
        if href and (href.startswith("http://") or href.startswith("https://")):
            external_refs.append(href)
        style = node.attrib.get("style", "")
        family = node.attrib.get("font-family")
        if family:
            font_families.add(family)
        match = re.search(r"font-family\s*:\s*([^;]+)", style, re.I)
        if match:
            font_families.add(match.group(1).strip())
        if node.tag.endswith("}text") or node.tag == "text" or node.tag.endswith("}tspan"):
            visible_text.append("".join(node.itertext()))
    if external_refs:
        errors.append(f"SVG contains {len(external_refs)} remote references")

    all_text = "".join(visible_text)
    contains_cjk = bool(re.search(r"[\u3400-\u9fff]", all_text))
    contains_latin_or_digits = bool(re.search(r"[A-Za-z0-9]", all_text))
    family_text = " ".join(font_families).casefold()
    if contains_cjk and "yahei" not in family_text and "雅黑" not in family_text:
        warnings.append("Chinese text found without an explicit Microsoft YaHei family")
    if contains_latin_or_digits and "arial" not in family_text:
        warnings.append("English letters or digits found without an explicit Arial family")
    if not visible_text:
        warnings.append("SVG contains no editable text elements")

    return {
        "file": str(source.resolve()),
        "status": "fail" if errors else "pass_with_warnings" if warnings else "pass",
        "width": width,
        "height": height,
        "viewBox": view_box,
        "textElementCount": len(visible_text),
        "fontFamilies": sorted(font_families),
        "externalReferences": external_refs,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg")
    parser.add_argument("--width", type=float)
    parser.add_argument("--height", type=float)
    parser.add_argument("--json-out")
    args = parser.parse_args()
    try:
        report = validate(args.svg, args.width, args.height)
    except Exception as exc:  # noqa: BLE001
        print(f"validate_svg: {exc}", file=sys.stderr)
        return 2
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 2 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
