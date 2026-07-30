# PPTX QA and Acceptance Standard

## Contents

1. Gate sequence
2. Structural checks
3. Visual checks
4. Template fidelity
5. Data and research checks
6. macOS PowerPoint acceptance
7. Delivery status labels

## 1. Gate sequence

Run QA in this order:

1. Factual and adversarial review.
2. Native-object and embedded-data inspection.
3. Font and text-fit inspection.
4. Automated overflow and placeholder checks.
5. Full-size rendering of every slide.
6. Template/master fidelity comparison.
7. Chart/table/data reconciliation.
8. Microsoft PowerPoint for macOS reopen and visual inspection.

Do not call the deck final when a mandatory gate fails.

## 2. Structural checks

- Slide dimensions match the supplied template.
- Required masters, layouts, and themes are preserved.
- Text, shapes, tables, connectors, and charts remain native-editable.
- Photos and other permitted images remain independent objects.
- No full-slide screenshot or flattened SVG substitutes for editable content.
- Every native chart has an embedded editable workbook.
- No empty required slide-level placeholder remains.
- No broken relationship, missing media, or corrupted package part exists.
- Speaker notes or the source ledger contain traceable sources.

Run `inspect_pptx.py`, `check_fonts.py`, `compare_template.py`, and `qa_pptx.py`.

## 3. Visual checks

Render and inspect every slide individually at full size. Check:

- title hierarchy and one-line title fit;
- clipping, overflow, unintended overlap, and off-canvas objects;
- body density, alignment, spacing rhythm, and visual balance;
- output mode is explicit, and projected slides do not inherit leave-behind report density;
- selected layout-pattern fit, module count, width allocation, gutters, and whitespace against the page manifest;
- chart labels, legends, axes, units, and table readability;
- image crop, sharpness, identity, and aspect ratio;
- source footnote legibility;
- consistency with the approved SVG;
- slide-to-slide consistency and variation in a multi-page deck.
- Japanese copy capacity in the production font, including the documented expansion reserve when translation follows Chinese drafting.

A montage is useful for flow but never replaces full-size inspection.

## 4. Template fidelity

Compare source and final PPTX packages:

- slide width and height;
- master, layout, and theme inventory;
- exact master/layout/theme XML hashes where strict preservation is required;
- header, footer, logo, and page-number behavior;
- intentional deviations recorded in a deviation log.

Treat known inherited placeholder behavior carefully. Never hide an empty placeholder by covering it with a new object; fill or delete the inherited placeholder intentionally.

## 5. Data and research checks

- Recompute or re-read every decision-critical number.
- Match chart series, categories, labels, units, number formats, and workbook data.
- Verify data did not change during geometry or label fixes.
- Match source footnotes and ledger IDs to the displayed claim.
- Separate facts, estimates/views, and hypotheses.
- Preserve explicit evidence-status labels for sample-observed layout rules, professional fallbacks, and evidence gaps.
- Preserve the `projected` versus `leave-behind` output-mode label and challenge any high-density projected page.
- Use `未公开` or `Not disclosed` when a figure is unavailable.

## 6. macOS PowerPoint acceptance

The priority target is Microsoft PowerPoint for macOS.

- Open the final exported PPTX in PowerPoint for macOS.
- Confirm fonts resolve and mixed Chinese/Latin runs display correctly.
- Confirm charts open their embedded Excel data and remain editable.
- Confirm masters/layouts and inherited page furniture behave correctly.
- Confirm no labels truncate after PowerPoint recalculates layout.
- Save, close, reopen, and inspect representative slides after a round trip when risk is high.

If automation is unavailable, request a manual reopen. LibreOffice, OnlyOffice, or another renderer provides preliminary evidence only.

## 7. Delivery status labels

- **Final:** all mandatory gates, including macOS PowerPoint acceptance, passed.
- **Candidate:** structural and preliminary visual QA passed; macOS PowerPoint acceptance remains pending.
- **Preview only:** approval-stage SVG or PPTX rendered with substitute fonts/tools.
- **Blocked:** a mandatory input, capability, evidence, or QA gate failed.
