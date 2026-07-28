#!/usr/bin/env python3
"""Inspect PPTX structure, editability signals, charts, fonts, and relationships."""

from __future__ import annotations

import argparse
import posixpath
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from pptx_utils import (
    NS,
    broken_relationships,
    chart_embedding_status,
    collect_fonts,
    dump_json,
    open_pptx,
    parse_xml,
    parts,
    read_text,
    slide_size,
)


def nearest_shape_text(node: ET.Element, parent_map: dict[ET.Element, ET.Element]) -> str:
    current = node
    while current in parent_map:
        current = parent_map[current]
        if current.tag.endswith("}sp") or current.tag.endswith("}pic") or current.tag.endswith("}graphicFrame"):
            return "".join(child.text or "" for child in current.findall(".//a:t", NS)).strip()
    return ""


def picture_coverage(pic: ET.Element, cx: int, cy: int) -> float:
    ext = pic.find(".//p:spPr/a:xfrm/a:ext", NS)
    if ext is None:
        return 0.0
    width = int(ext.attrib.get("cx", "0"))
    height = int(ext.attrib.get("cy", "0"))
    return (width * height) / (cx * cy) if cx and cy else 0.0


def inspect(path: str, require_sources: bool = False) -> dict[str, object]:
    with open_pptx(path) as archive:
        names = set(archive.namelist())
        size = slide_size(archive)
        slide_parts = parts(archive, "ppt/slides/slide")
        notes_parts = parts(archive, "ppt/notesSlides/notesSlide")
        fonts: set[str] = set()
        slide_reports: list[dict[str, object]] = []
        flattened_risks: list[int] = []
        empty_placeholders_total = 0

        for index, slide_part in enumerate(slide_parts, start=1):
            root = parse_xml(archive, slide_part)
            fonts.update(collect_fonts(root))
            parent_map = {child: parent for parent in root.iter() for child in parent}
            placeholders = root.findall(".//p:ph", NS)
            empty_placeholders = [
                {
                    "type": ph.attrib.get("type", "unspecified"),
                    "idx": ph.attrib.get("idx", ""),
                }
                for ph in placeholders
                if not nearest_shape_text(ph, parent_map)
            ]
            empty_placeholders_total += len(empty_placeholders)
            pictures = root.findall(".//p:pic", NS)
            shape_count = len(root.findall(".//p:sp", NS))
            table_count = len(root.findall(".//a:tbl", NS))
            chart_refs = root.findall(".//c:chart", NS)
            connector_count = len(root.findall(".//p:cxnSp", NS))
            group_count = len(root.findall(".//p:grpSp", NS))
            text = "".join(node.text or "" for node in root.findall(".//a:t", NS)).strip()
            max_picture_coverage = max(
                [picture_coverage(pic, int(size.get("cx") or 0), int(size.get("cy") or 0)) for pic in pictures]
                or [0.0]
            )
            flattened_risk = (
                max_picture_coverage >= 0.80
                and shape_count <= 3
                and table_count == 0
                and len(chart_refs) == 0
                and len(text) < 120
            )
            if flattened_risk:
                flattened_risks.append(index)
            slide_reports.append(
                {
                    "slide": index,
                    "part": slide_part,
                    "textCharacters": len(text),
                    "nativeShapeCount": shape_count,
                    "pictureCount": len(pictures),
                    "nativeTableCount": table_count,
                    "chartReferenceCount": len(chart_refs),
                    "connectorCount": connector_count,
                    "groupCount": group_count,
                    "placeholderCount": len(placeholders),
                    "emptyPlaceholders": empty_placeholders,
                    "maxPictureCoverage": round(max_picture_coverage, 4),
                    "flattenedSlideRisk": flattened_risk,
                }
            )

        for prefix in ("ppt/slideMasters/", "ppt/slideLayouts/", "ppt/theme/"):
            for part in [name for name in names if name.startswith(prefix) and name.endswith(".xml")]:
                fonts.update(collect_fonts(parse_xml(archive, part)))

        notes_sources = []
        for notes_part in notes_parts:
            text = read_text(archive, notes_part)
            if "[Sources]" in text:
                notes_sources.append(notes_part)

        charts = chart_embedding_status(archive)
        charts_without_workbook = [item["chartPart"] for item in charts if not item["hasEmbeddedWorkbook"]]
        broken = broken_relationships(archive)
        errors: list[str] = []
        warnings: list[str] = []

        if not slide_parts:
            errors.append("No slides found")
        if not parts(archive, "ppt/slideMasters/slideMaster"):
            errors.append("No slide master found")
        if not parts(archive, "ppt/slideLayouts/slideLayout"):
            errors.append("No slide layout found")
        if not parts(archive, "ppt/theme/theme"):
            errors.append("No presentation theme found")
        if broken:
            errors.append(f"{len(broken)} broken internal package relationships")
        if charts_without_workbook:
            errors.append(f"{len(charts_without_workbook)} native charts lack an embedded workbook")
        if empty_placeholders_total:
            warnings.append(f"{empty_placeholders_total} empty placeholders require review")
        if flattened_risks:
            warnings.append(f"Possible flattened full-slide image on slides {flattened_risks}")
        if require_sources and slide_parts and not notes_sources:
            warnings.append("No [Sources] block found in speaker notes")

        return {
            "file": str(Path(path).resolve()),
            "status": "fail" if errors else "pass_with_warnings" if warnings else "pass",
            "slideSize": size,
            "counts": {
                "slides": len(slide_parts),
                "masters": len(parts(archive, "ppt/slideMasters/slideMaster")),
                "layouts": len(parts(archive, "ppt/slideLayouts/slideLayout")),
                "themes": len(parts(archive, "ppt/theme/theme")),
                "charts": len(charts),
                "embeddedWorkbooks": len(
                    [name for name in names if name.startswith("ppt/embeddings/") and not name.endswith("/")]
                ),
                "images": len(
                    [name for name in names if name.startswith("ppt/media/") and not name.endswith("/")]
                ),
                "notesSlides": len(notes_parts),
                "notesWithSources": len(notes_sources),
            },
            "fontsReferenced": sorted(fonts, key=str.casefold),
            "charts": charts,
            "slides": slide_reports,
            "brokenRelationships": broken,
            "errors": errors,
            "warnings": warnings,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx")
    parser.add_argument("--json-out")
    parser.add_argument("--require-sources", action="store_true")
    args = parser.parse_args()
    try:
        report = inspect(args.pptx, args.require_sources)
    except Exception as exc:  # noqa: BLE001
        print(f"inspect_pptx: {exc}", file=sys.stderr)
        return 2
    print(dump_json(report, args.json_out))
    return 2 if report["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
