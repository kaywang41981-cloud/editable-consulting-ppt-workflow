# Design and Native Build Standard

## Contents

1. Template contract
2. Layout strategy selection
3. SVG preview standard
4. Native-object mapping
5. Typography
6. Tables and charts
7. Images and diagrams
8. File outputs

## 1. Template contract

- Require a user-provided PPTX template or source deck.
- Read slide width and height from the PPTX; never assume 16:9.
- Preserve masters, layouts, theme, background, header/footer, logo, page number, and inherited placeholder behavior.
- Prefer duplicating a suitable source slide and editing inherited elements.
- Do not rebuild a template from a screenshot, palette, or visual approximation when the PPTX exists.
- Keep unused masters and layouts when the user requires the independent output to retain the complete template structure.
- Change masters only for intentional global changes approved by the user.

## 2. Layout strategy selection

- Read `layout-strategy-library.zh-CN.md` before composing a consulting-style body area.
- Classify the page by its communication job, not by its industry vocabulary.
- Classify the output mode as `projected presentation` or `leave-behind report`; use projected-mode density when the use case is unknown.
- Select one primary pattern and record its pattern ID in the page manifest.
- Translate normalized proportions into the inherited body/safe area; never overwrite template margins with screenshot-derived coordinates.
- Use sample-observed strategies as candidates, not universal truths. The current library contains two visual families from one publishing ecosystem and requires broader validation before any pattern becomes a mandatory default.
- Learn information architecture from dense leave-behind report pages, but do not transfer their small type or high text density to projected slides.
- Reserve additional text capacity when Chinese source copy will be translated into Japanese. Reflow, shorten, or split before reducing the type scale.
- Reject a visually attractive pattern when it weakens the evidence-to-implication chain or hides uncertainty.

## 3. SVG preview standard

SVG is a visual contract, not a production shortcut.

- Match the exact slide aspect ratio and coordinate system.
- Define the inherited title zone and body/safe area.
- Show template furniture, source rail, and page-number position.
- Use real final copy where available; mark placeholders clearly.
- Keep a stable page ID and version in non-visible metadata or the filename.
- Validate XML, viewBox, fonts, and external references with `scripts/validate_svg.py`.
- Do not embed script, remote fonts, or remote images.

## 4. Native-object mapping

Map each SVG element before building:

| SVG element | PowerPoint implementation |
| --- | --- |
| title/body/labels | Native text boxes or inherited placeholders |
| panels, rules, highlights | Native shapes |
| simple process or relationship | Native shapes and connectors |
| two-dimensional information | Native PowerPoint table |
| trend/share/comparison data | Native chart with embedded Excel workbook |
| photo/product/logo/screenshot/map base | Independent image object |
| map labels/arrows/callouts | Native objects over the map image |

Do not place a full-slide SVG or PNG as the final page background when editability is required.

## 5. Typography

- New or edited Chinese text: Microsoft YaHei.
- New or edited English letters and numbers: Arial.
- New or edited Japanese text: preserve the client template's Japanese font. If the template does not define one, ask for the required font before final production and document any preview substitute.
- Mixed runs should use separate font runs when the authoring tool supports them.
- Preserve unchanged template furniture unless the user asks to restyle it.
- If required fonts are absent, permit a preview using a documented substitute, but mark it non-final.
- Match the source template's intended hierarchy and sizes. Shorten copy or change layout before shrinking text.
- Never allow a one-line title field to wrap unexpectedly.

## 6. Tables and charts

### Tables

- Use native tables for rows and columns that users will edit directly.
- Keep headers, units, totals, notes, and source references explicit.
- Use consistent cell padding, alignment, number formats, and decimal precision.

### Charts

- Use charts only when the visual relationship supports the page claim.
- Embed an editable Excel workbook inside the PPTX.
- Preserve source data, formulas, units, and number formats.
- Verify the displayed chart against the workbook and source ledger.
- For truncated labels, inspect geometry, gap width, plot area, and chart XML before reducing font size.
- Use `Not disclosed` or `未公开` rather than fabricated values.

## 7. Images and diagrams

- Photos, product images, logos, screenshots, and map bases may remain raster or SVG image objects.
- Keep images independent from native annotations.
- Use authentic official assets for real entities; do not create pseudo-official logos or fake screenshots.
- Inspect crop, resolution, aspect ratio, and licensing/source.
- Build simple diagrams natively. Use complex external visuals only when they materially improve comprehension and their editability limit is disclosed.

## 8. File outputs

Follow the user's current instruction:

- one PPTX per slide;
- one PPTX for an approved batch;
- a combined final deck;
- or any combination of these.

Use clear versioned filenames. Preserve source files and export edited copies unless the user explicitly requests in-place editing.
