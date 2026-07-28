# Research, Evidence, and Source Standard

## Contents

1. Decision-led research
2. Evidence hierarchy
3. Claim classification
4. Cross-validation and adversarial review
5. Slide outline fields
6. Source ledger

## 1. Decision-led research

For every research item, record:

- why it is being investigated;
- which decision or page claim it supports;
- what evidence would confirm or reject the hypothesis;
- whether the result is fact, estimate/view, or hypothesis.

Use a consulting skill, research skill, interview framework, or brainstorming skill when available. When unavailable, reproduce the underlying method: issue tree, hypotheses, prioritized evidence collection, synthesis, and challenge.

## 2. Evidence hierarchy

Prefer, in order:

1. Laws, regulators, exchanges, courts, government statistics, official registries, and standards bodies.
2. Company filings, audited reports, official product documentation, official announcements, and direct executive statements.
3. Reputable industry bodies, academic papers, and established research institutions with disclosed methods.
4. High-quality media and specialist publications with attributable reporting.
5. Third-party databases, estimates, aggregators, and search summaries.

Do not cite a search-result snippet as final evidence. Open and verify the underlying source.

## 3. Claim classification

Every material claim must be classified:

- **Verified fact:** directly supported by a reliable source and correct in scope, entity, geography, time, and unit.
- **Third-party estimate or view:** attributed, method-limited, and not presented as official fact.
- **Hypothesis requiring validation:** plausible but not publicly confirmed.

Association membership, event participation, registration, or corporate relationship does not by itself prove supplier qualification, procurement responsibility, outsourcing, customer status, market share, willingness to switch, or a first order.

## 4. Cross-validation and adversarial review

Before outlining or delivering:

- confirm names, dates, geography, units, currency, period, denominator, and legal entity;
- distinguish current facts from forecasts and historical facts;
- search for a second independent source for decision-critical claims;
- search for contradictory evidence and alternative explanations;
- test whether the claim is broader than the evidence;
- verify that the visual does not imply false precision or causality;
- remove or relabel unsupported claims.

## 5. Slide outline fields

For every proposed slide, provide:

- slide number and working title;
- narrative job and one-sentence takeaway;
- audience decision supported;
- content blocks and visual form;
- verified facts;
- estimates/views with attribution;
- hypotheses/open questions;
- source footnote text;
- full source-ledger IDs;
- dependencies and approval questions.

## 6. Source ledger

Maintain a CSV, XLSX, JSON, or Markdown ledger with at least:

| Field | Meaning |
| --- | --- |
| source_id | Stable ID used by slides and notes |
| slide_ids | Slides using the source |
| claim | Exact supported claim |
| classification | fact, estimate/view, or hypothesis |
| organization | Publisher or source owner |
| title | Document/page title |
| url | Direct URL when public |
| publication_date | Source date |
| access_date | Date verified |
| evidence_quote | Relevant quotation or data excerpt |
| scope_notes | Entity, geography, time, unit, denominator |
| verification_status | verified, partial, blocked, or superseded |
| confidence | high, medium, or low with reason |

Place a concise source footnote on the slide. Put full URLs and traceability in speaker notes or the delivered ledger. Include a `[Sources]` notes block when the presentation tool supports speaker notes.
