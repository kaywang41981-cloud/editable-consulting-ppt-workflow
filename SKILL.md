---
name: editable-consulting-ppt-workflow
description: Create, redesign, or research professional PowerPoint slides through a template-faithful, page-type-aware SVG approval workflow, then build and verify native-editable PPTX files. Use for PPT, PPTX, slide, deck, screenshot-to-slide, slide beautification, consulting presentation, Japanese business presentation, research deck, editable PowerPoint, SVG preview, template/master preservation, native charts, layout strategy selection, or batch slide production.
---

# Editable Consulting PPT Workflow

Produce evidence-backed, visually approved, native-editable PowerPoint slides without flattening the page or damaging the supplied template. Treat the user-provided PPTX as the required visual and structural source.

## Read the relevant references

- Read `references/workflows.md` for the screenshot-led and research-led routes.
- Read `references/design-and-build.md` before creating SVG previews or PPTX files.
- Read `references/layout-strategy-library.zh-CN.md` before selecting the composition of a consulting slide, especially for Japanese business materials, dense case pages, comparisons, mechanisms, processes, or mixed chart-and-text pages.
- Read `references/research-and-sources.md` whenever external research informs slide content.
- Read `references/qa-and-acceptance.md` before building the final PPTX and again before delivery.
- Read `references/cross-agent-adapters.md` when choosing tools or when a required capability is missing.
- Read `references/user-guide.zh-CN.md` when explaining the process to a Chinese-speaking user.

## Mandatory clarification gate

Ask exactly one question at a time until the following are known or the user explicitly authorizes professional judgment:

1. Communication objective, audience, and desired decision or takeaway.
2. User-provided PPTX template or source deck, plus the source screenshot/content.
3. Language, slide scope, output grouping, and approval batch size.
4. Output mode: projected presentation, leave-behind report, or both.
5. Research boundary, source standard, and factual cutoff date when research is required.
6. Required deliverables and acceptance conditions.

Surface one relevant blind spot with each material question. Do not begin research, SVG design, or PPTX production while a missing answer could change the result materially.

If no user-provided PPTX template exists, stop and request one. Bundled examples are tests and demonstrations only; never use them as a production default.

## Capability gate

Before promising a final editable PPTX, verify that the execution environment can:

- inspect and preserve the source deck's slide size, master, layouts, theme, headers, footers, logos, and page-number structure;
- create editable PowerPoint text, shapes, tables, connectors, and native charts;
- embed chart data in an editable Excel workbook inside the PPTX;
- export PPTX and run structural plus visual QA.

If any required capability is unavailable, explain the gap and stop final PPTX production. Never substitute a full-slide screenshot, flattened SVG, or rasterized page and call it editable.

## Layout strategy gate

Before creating an SVG, define the page's communication job and select one page-type strategy from `references/layout-strategy-library.zh-CN.md`.

Record at least:

- page type and selected pattern ID;
- why the pattern fits the page claim;
- module count and width allocation;
- output mode: projected presentation or leave-behind report;
- density tier and expected Japanese copy-expansion reserve when relevant;
- evidence status: sample-observed, professional fallback, or evidence gap.

Treat the client PPTX master, fonts, colors, margins, title bar, footer, logo, and page-number behavior as higher priority than any strategy-library measurement. Borrow information hierarchy, spatial organization, and visual narrative only. Do not copy publisher marks, screenshots, wording, data, logos, decorative signatures, or uniquely identifying visual assets from reference examples.

Prefer two to four primary information modules for projected slides. Permit up to six short, scan-friendly cards or a structured native table for leave-behind pages only when the output mode and density tier are recorded. Change the composition, split the slide, or shorten the copy before shrinking below the template's readable type scale. When several strategies could work, choose the one that makes the evidence-to-implication chain most obvious rather than the one that looks most decorative.

Do not add a full-width bottom summary or implication box merely to make a slide feel complete. Treat any bottom band as an optional, evidence-linked module rather than a default ending. Add one only when it contributes decision-critical meaning not already conveyed by the title, subtitle, chart, or body, such as a non-obvious implication, risk, assumption, or next action. Otherwise omit it.

Vary conclusion placement according to the page's communication job. Use a claim-led title, a concise subtitle that introduces the body, an in-context highlight, a side insight rail, or no separate conclusion module when those choices are clearer. Do not mechanically replace every bottom band with a subtitle block or repeat the same summary device across consecutive slides. Functional source notes, legends, and required template footers are not summary modules and remain governed by their own requirements.

## Select one route

### Route A: supplied page content or screenshot

Use when the page already contains substantially complete content and the job is design, layout, reconstruction, or beautification.

1. Extract every title, label, value, note, relationship, and visual asset.
2. Confirm the page's single communication job and content hierarchy.
3. Inspect the complete source PPTX and identify the appropriate source slide/layout.
4. Create one or more SVG previews at the exact inherited slide aspect ratio.
5. Wait for approval unless the user explicitly says to skip SVG approval.
6. Rebuild the approved design as native PowerPoint objects inside the inherited template structure.

### Route B: research-led presentation

Use when the user provides a project background or client question and needs research, storyline, detailed page outlines, and final slides.

1. Define the decision question, scope, exclusions, audience, evidence standard, and cutoff date.
2. Research with reliable public sources and the strongest available consulting, research, interview, and brainstorming methods.
3. Separate verified facts, third-party estimates or views, and hypotheses requiring validation.
4. Structure the fact-to-conclusion chain and produce a detailed slide-by-slide outline.
5. Wait for outline approval.
6. Create SVG previews in an agreed batch size and wait for approval unless explicitly waived.
7. Build the approved batch as native-editable PPTX slides.

When named external skills are unavailable, apply the equivalent framework in `references/research-and-sources.md` and record the substitute method.

## SVG approval contract

- Default SVG approval to mandatory; permit a bypass only after an explicit user instruction.
- Support single-slide and multi-slide approval batches.
- Size the SVG from the supplied PPTX page dimensions; never assume 16:9.
- Show the intended final hierarchy, spacing, title, body zone, visuals, source rail, and template furniture.
- Show the selected layout pattern, output mode, normalized module proportions, density tier, and Japanese expansion reserve where relevant.
- Treat SVG as a visual specification, not as the final slide body.
- Record approved SVG version, approval status, and later deviations.

## Native PPTX build contract

1. Duplicate or edit an appropriate source slide and preserve the master -> layout -> slide hierarchy. Do not rebuild the template from visual imitation.
2. Preserve all supplied masters, layouts, themes, headers, footers, logos, page-number behavior, and page dimensions unless the user explicitly requests a change.
3. Replace the inherited title content with the approved page title while retaining the intended title-bar structure.
4. Map the approved SVG body proportionally into the inherited body/safe area, then recreate it with native objects.
5. Use editable PowerPoint text boxes, shapes, tables, connectors, and charts. Keep photos, product images, logos, screenshots, maps, and other raster media as independent image objects.
6. Construct text for downstream editability, not only for visual fit:
   - Use one text container for one semantic block. Keep its paragraphs, explicit line breaks, local emphasis, colors, and mixed-language runs inside that container.
   - Set text-box width from the page grid and the parent module's content boundary. Never narrow, widen, or horizontally stretch a text box merely to force a desired number of lines.
   - Prefer placing text directly inside cards, title bars, labels, and buttons instead of overlaying separate text boxes.
   - Split text only when it requires independent movement, independent animation, or materially different alignment. If copy does not fit, shorten, reflow, enlarge the module, or split the slide before fragmenting the text or using shrink-to-fit as a workaround.
7. Use native editable tables for two-dimensional information. Use native charts with an embedded editable Excel workbook for trends, shares, comparisons, and other quantitative relationships.
8. Use Microsoft YaHei for Chinese text and Arial for English letters and numbers in new or edited content unless the supplied template specifies otherwise. For Japanese text, preserve the client template's Japanese font; do not substitute a Chinese font. If a required production font is missing, previews may use a documented substitute, but the PPTX cannot be marked final.
9. Preserve undisclosed data as `Not disclosed` or the audience-language equivalent, such as `未公开`; never invent a number.
10. Add visible concise source footnotes and put full traceability in speaker notes or the delivered source ledger.
11. Produce individual-slide files, combined files, or both according to the user's current instruction; do not impose a one-slide-only limitation.

## Verification gates

Run the bundled scripts from the skill directory:

```bash
python3 scripts/validate_svg.py approved.svg
python3 scripts/inspect_pptx.py final.pptx --json-out pptx-inspection.json
python3 scripts/check_fonts.py --pptx final.pptx --require "Microsoft YaHei" Arial
python3 scripts/compare_template.py --template source-template.pptx --final final.pptx
python3 scripts/qa_pptx.py --pptx final.pptx --template source-template.pptx --report qa-report.md
```

Use `scripts/render_pptx.py` for a preliminary render when Microsoft PowerPoint automation is unavailable. A LibreOffice or other substitute render is never the final macOS PowerPoint acceptance.

Before delivery, complete all gates in `references/qa-and-acceptance.md`, including:

- factual cross-check and adversarial review;
- native-object and embedded-workbook inspection;
- semantic-block text-container inspection, including unnecessary fragmentation, grid-aligned widths, explicit line breaks, and text placed directly inside suitable parent shapes;
- font resolution and text-fit inspection;
- full-size render of every slide;
- template/master fidelity comparison;
- empty-placeholder, clipping, overlap, crop, label-capacity, and data-match checks;
- output-mode fit, layout-pattern fit, module-count, gutter, whitespace, density, and Japanese copy-expansion checks;
- redundant-summary and repetition checks: no decorative bottom conclusion band, no restatement of the title or body, and no mechanical reuse of one conclusion placement across the deck;
- final reopen and visual inspection in Microsoft PowerPoint for macOS.

## Stop conditions

Stop and report the blocker when:

- the source template is missing;
- the communication objective remains materially ambiguous;
- research evidence is too weak to support the proposed claim;
- required fonts are missing for final delivery;
- the toolchain cannot preserve masters or create required native objects;
- a template-fidelity, editability, embedded-data, overflow, or final macOS PowerPoint gate fails.

## Delivery record

Deliver only the requested final artifacts and a concise status summary. Record:

- final PPTX path(s) and approved SVG version(s);
- source ledger path when research was used;
- tools and substitute methods used;
- QA checks passed, warnings, and any non-final status;
- explicit deviations from the approved SVG or source template.
