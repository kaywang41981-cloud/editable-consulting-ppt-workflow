# Workflow Routes and Approval Gates

## Contents

1. Shared intake
2. Route A: supplied screenshot or complete content
3. Route B: research-led deck
4. Batch production
5. Change control

## 1. Shared intake

Ask one question per message. Continue until the agent can state:

> By the end, the audience should [understand, believe, choose, approve, or do X] because [central takeaway].

Clarify, in order of materiality:

- audience and communication objective;
- user-provided PPTX template/source deck;
- page content, language, and factual scope;
- output mode: meeting projection, leave-behind reading, or both;
- single page versus batch, individual versus combined deck;
- SVG approval batch size and whether the user explicitly waives approval;
- sources, cutoff date, and confidentiality constraints;
- macOS PowerPoint acceptance and delivery paths.

Do not ask a checklist of questions at once. Explain the concrete blind spot behind a question when it may change the result.

## 2. Route A: supplied screenshot or complete content

### A1. Extract and reconcile

- Read visible and attached content completely.
- Transcribe titles, labels, data, units, legends, footnotes, and relationships.
- Cross-check the screenshot against any editable source files.
- Identify ambiguity, omissions, contradictions, and content that is only decorative.
- Confirm the page's primary claim before designing.

### A2. Audit the template

- Read slide dimensions from the source PPTX.
- Inspect every relevant source slide, not only the screenshot.
- Identify the correct source layout, title zone, body/safe area, source rail, logo, footer, and page-number behavior.
- Inventory master, layout, theme, and placeholder structure.
- Classify the communication job and select a pattern from `layout-strategy-library.zh-CN.md`; record its evidence status and normalized body proportions.

### A3. Design the SVG preview

- Use the exact source aspect ratio.
- Retain template furniture in the preview or show a composited preview against a template render.
- Design one clear visual hierarchy around one page claim.
- Keep source notes and disclaimers visible at presentation size.
- Create multiple SVGs in one batch when requested.

### A4. Approval and build

- Do not build final PPTX before SVG approval unless the user explicitly waives the gate.
- Record approved SVG filename/version.
- Recreate the design with native PowerPoint objects; do not embed the SVG as the body.
- Run all QA gates before labeling the result final.

## 3. Route B: research-led deck

### B1. Frame the decision

Define the client question, audience, geography, period, inclusions, exclusions, decision to support, and evidence standard.

### B2. Research and challenge

- Build an issue tree and initial hypotheses.
- Prioritize primary and official sources.
- Triangulate decision-critical claims.
- Search for disconfirming evidence and alternative explanations.
- Label incomplete claims as hypotheses requiring validation.

### B3. Structure the storyline

- Convert evidence into a cumulative argument, not an inventory of facts.
- Give each slide one narrative job and one primary claim.
- Link evidence to implication and decision.
- Produce a detailed outline containing title, key message, content blocks, visual form, evidence, sources, and open questions for every slide.
- Add page type, layout pattern ID, module count, density tier, and Japanese expansion reserve to the outline or page manifest.

### B4. Approval sequence

1. User approves the detailed outline.
2. Agent creates SVG previews in the agreed batch size.
3. User approves or revises the SVGs.
4. Agent builds native-editable PPTX slides.
5. Agent verifies and delivers individual, combined, or both forms as requested.

## 4. Batch production

Batch size is flexible. Confirm it for each task or infer it only when the user authorizes judgment.

- Keep a page manifest with slide number, title, page type, output mode, layout pattern ID, evidence status, density tier, Japanese expansion reserve, SVG version, approval state, PPTX build state, source state, and QA state.
- Build only approved pages unless the SVG gate was explicitly waived.
- Run structural checks after each build batch and full visual QA near delivery.
- Allow individual page PPTX, a multi-page batch PPTX, and a final combined deck.

## 5. Change control

- Record every material deviation from the approved SVG and why it was necessary.
- Return to SVG approval when a change alters hierarchy, page claim, chart type, or major composition.
- Permit direct PPTX corrections for small fit, alignment, typo, or chart-label fixes, then rerun the relevant regression checks.
- Never silently change data or conclusions to make a layout fit.
