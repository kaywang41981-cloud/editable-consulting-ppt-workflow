#!/usr/bin/env python3
"""Small standard-library helpers for inspecting PPTX OOXML packages."""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def numeric_part_key(name: str) -> tuple[str, int]:
    match = re.search(r"(\d+)(?=\.[^.]+$)", name)
    return (re.sub(r"\d+(?=\.[^.]+$)", "", name), int(match.group(1)) if match else 0)


def open_pptx(path: str | Path) -> zipfile.ZipFile:
    pptx = Path(path)
    if not pptx.is_file():
        raise FileNotFoundError(f"PPTX not found: {pptx}")
    if not zipfile.is_zipfile(pptx):
        raise ValueError(f"Not a valid ZIP-based PPTX: {pptx}")
    archive = zipfile.ZipFile(pptx)
    bad = archive.testzip()
    if bad:
        archive.close()
        raise ValueError(f"Corrupt PPTX entry: {bad}")
    return archive


def parse_xml(archive: zipfile.ZipFile, part: str) -> ET.Element:
    return ET.fromstring(archive.read(part))


def read_text(archive: zipfile.ZipFile, part: str) -> str:
    root = parse_xml(archive, part)
    return "".join(node.text or "" for node in root.findall(".//a:t", NS)).strip()


def slide_size(archive: zipfile.ZipFile) -> dict[str, int | float | str | None]:
    root = parse_xml(archive, "ppt/presentation.xml")
    size = root.find("p:sldSz", NS)
    if size is None:
        return {"cx": None, "cy": None, "ratio": None, "orientation": None}
    cx = int(size.attrib.get("cx", "0"))
    cy = int(size.attrib.get("cy", "0"))
    ratio = round(cx / cy, 6) if cy else None
    return {
        "cx": cx,
        "cy": cy,
        "ratio": ratio,
        "orientation": "landscape" if cx >= cy else "portrait",
    }


def parts(archive: zipfile.ZipFile, prefix: str, suffix: str = ".xml") -> list[str]:
    return sorted(
        [name for name in archive.namelist() if name.startswith(prefix) and name.endswith(suffix)],
        key=numeric_part_key,
    )


def sha256_parts(archive: zipfile.ZipFile, prefixes: Iterable[str]) -> dict[str, str]:
    selected: dict[str, str] = {}
    for name in sorted(archive.namelist()):
        if any(name.startswith(prefix) for prefix in prefixes) and not name.endswith("/"):
            selected[name] = hashlib.sha256(archive.read(name)).hexdigest()
    return selected


def relationship_owner(rels_part: str) -> str:
    if rels_part == "_rels/.rels":
        return ""
    directory, filename = posixpath.split(rels_part)
    if posixpath.basename(directory) != "_rels" or not filename.endswith(".rels"):
        raise ValueError(f"Unexpected relationships part: {rels_part}")
    owner_dir = posixpath.dirname(directory)
    return posixpath.join(owner_dir, filename[:-5])


def resolve_relationship_target(rels_part: str, target: str) -> str:
    owner = relationship_owner(rels_part)
    base = posixpath.dirname(owner)
    return posixpath.normpath(posixpath.join(base, target)).lstrip("/")


def broken_relationships(archive: zipfile.ZipFile) -> list[dict[str, str]]:
    names = set(archive.namelist())
    broken: list[dict[str, str]] = []
    for rels_part in [name for name in names if name.endswith(".rels")]:
        root = parse_xml(archive, rels_part)
        for rel in root.findall("rel:Relationship", NS):
            if rel.attrib.get("TargetMode") == "External":
                continue
            target = rel.attrib.get("Target", "")
            resolved = resolve_relationship_target(rels_part, target)
            if resolved and resolved not in names:
                broken.append(
                    {
                        "relationshipsPart": rels_part,
                        "id": rel.attrib.get("Id", ""),
                        "target": target,
                        "resolved": resolved,
                    }
                )
    return broken


def collect_fonts(root: ET.Element) -> set[str]:
    fonts: set[str] = set()
    for node in root.iter():
        if node.tag.endswith("}rPr") or node.tag.endswith("}defRPr") or node.tag.endswith("}endParaRPr"):
            typeface = node.attrib.get("typeface")
            if typeface:
                fonts.add(typeface)
        if node.tag.endswith("}latin") or node.tag.endswith("}ea") or node.tag.endswith("}cs"):
            typeface = node.attrib.get("typeface")
            if typeface:
                fonts.add(typeface)
    return fonts


def chart_embedding_status(archive: zipfile.ZipFile) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    names = set(archive.namelist())
    chart_parts = sorted(
        [
            name
            for name in names
            if re.search(r"(?:^|/)charts/chart\d+\.xml$", name)
        ],
        key=numeric_part_key,
    )
    for chart in chart_parts:
        rels = posixpath.join(
            posixpath.dirname(chart), "_rels", posixpath.basename(chart) + ".rels"
        )
        embeddings: list[str] = []
        if rels in names:
            root = parse_xml(archive, rels)
            for rel in root.findall("rel:Relationship", NS):
                target = rel.attrib.get("Target", "")
                resolved = resolve_relationship_target(rels, target)
                if resolved.startswith("ppt/embeddings/") and resolved in names:
                    embeddings.append(resolved)
        results.append(
            {
                "chartPart": chart,
                "embeddedWorkbookParts": sorted(set(embeddings)),
                "hasEmbeddedWorkbook": bool(embeddings),
            }
        )
    return results


def dump_json(data: object, output: str | Path | None = None) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if output:
        Path(output).write_text(payload + "\n", encoding="utf-8")
    return payload
