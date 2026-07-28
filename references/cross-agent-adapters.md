# Cross-Agent Capability and Tool Adapters

## Contents

1. Capability contract
2. Recommended tool classes
3. Fallback rules
4. Environment record

## 1. Capability contract

The workflow is tool-neutral, but the final artifact standard is not. A valid implementation must preserve the user-supplied PPTX structure, create native objects, embed chart workbooks, export PPTX, and support inspection plus rendering.

Do not promise final output merely because an agent can draw SVGs or write OOXML partially.

## 2. Recommended tool classes

Select the strongest available tools:

- PPTX import/edit/export library that preserves masters and layouts.
- Native chart API supporting an embedded Excel workbook.
- SVG authoring or vector editor for approval previews.
- OOXML package inspection for deterministic structural QA.
- Microsoft PowerPoint for macOS for final acceptance.
- LibreOffice or OnlyOffice only for preliminary fallback rendering.

Examples include PowerPoint automation, presentation-specific artifact libraries, Office APIs, and mature PPTX libraries. Tool brand is secondary to passing the capability contract.

## 3. Fallback rules

| Missing capability | Allowed fallback | Status |
| --- | --- | --- |
| named consulting/research skill | equivalent issue-tree and evidence workflow | allowed, record method |
| SVG renderer | browser or compatible vector renderer | allowed for preview |
| required fonts | documented substitutes | preview only |
| PowerPoint automation | LibreOffice/OnlyOffice render plus manual PowerPoint reopen | candidate only |
| master-preserving PPTX editor | none | blocked |
| native charts with embedded workbook | none for quantitative final chart | blocked |
| public evidence for a claim | relabel as estimate/hypothesis or remove | allowed with disclosure |

Never fall back to a full-slide raster image for a final editable deliverable.

## 4. Environment record

Record in the QA report:

- agent/model or execution environment when known;
- presentation library and version;
- SVG renderer;
- font-check method and resolved fonts;
- preliminary renderer;
- final PowerPoint acceptance method;
- unavailable tools and substitutions;
- final/candidate/preview/blocked status.
