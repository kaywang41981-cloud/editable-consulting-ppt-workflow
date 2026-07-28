#!/usr/bin/env python3
"""Scan a release tree for client terms, likely secrets, and unsafe public artifacts."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".mjs",
    ".js",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".svg",
    ".xml",
    ".rels",
    ".sh",
}
DEFAULT_DENY: list[str] = []
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic_secret_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
}


def scan_text(label: str, text: str, deny: list[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    folded = text.casefold()
    for term in deny:
        if term.casefold() in folded:
            findings.append({"file": label, "type": "denied_term", "match": term})
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append({"file": label, "type": name, "match": "redacted"})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    parser.add_argument("--deny", action="append", default=[])
    parser.add_argument("--json-out")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    deny = list(dict.fromkeys(DEFAULT_DENY + args.deny))
    findings: list[dict[str, str]] = []
    scanned = 0
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = str(path.relative_to(root))
        findings.extend(scan_text(relative + " [filename]", relative, deny))
        if path.suffix.casefold() in TEXT_SUFFIXES:
            scanned += 1
            findings.extend(scan_text(relative, path.read_text(encoding="utf-8", errors="ignore"), deny))
        elif path.suffix.casefold() in {".pptx", ".zip"} and zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                for member in archive.namelist():
                    if Path(member).suffix.casefold() in TEXT_SUFFIXES:
                        scanned += 1
                        text = archive.read(member).decode("utf-8", errors="ignore")
                        findings.extend(scan_text(f"{relative}!{member}", text, deny))
    report = {
        "status": "fail" if findings else "pass",
        "root": str(root),
        "scannedTextItems": scanned,
        "denyTerms": deny,
        "findings": findings,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 2 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
