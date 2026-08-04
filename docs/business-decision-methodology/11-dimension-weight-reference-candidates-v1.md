# Dimension Weight Reference Candidates v1

## Purpose

Status: `FOUNDATION`

This document records candidate reference weight sets for evaluating future
Business Capability Dimension weighting methodology.

As Decision 6 artifacts, these percentages are Reference Candidate Weight
Sets only. Decision 6 did not approve production methodology, implementation
values, or an official numeric dimension weight set.

Decision 7 separately selects Candidate B, Business Capability Impact
Weighted, as the official Numeric Dimension Weight Set. This document
preserves all Decision 6 reference candidates for traceability.

## Decision Boundary

Status: `APPROVED`

This document establishes only:

- Reference candidate weight sets.
- Comparative evaluation.
- Governance compliance.
- Documented trade-offs.

This document does not establish:

- Approved numeric weight set.
- Production methodology.
- Implementation values.
- Aggregation formulas.
- Readiness thresholds.
- Scoring mathematics.
- Finding rules.
- Recommendation logic.
- Confidence formulas.

## Methodology Version Identity

Status: `APPROVED`

Methodology version: `business-decision-methodology-v1`

Taxonomy version: `business-capability-taxonomy-v1`

The candidate reference weight sets use the approved Decision 1 Business
Capability Taxonomy:

- Process & Operational Control.
- Governance, Compliance & Regulatory Readiness.
- Technology & Intelligent Systems Management.
- Data, Privacy & Security Controls.
- Remediation, Verification & Continuous Improvement.

## Candidate A: Equal Contribution

Status: `REFERENCE_CANDIDATE`

These percentages are a Reference Candidate Weight Set only. They are an
evaluation artifact and are not approved production methodology.

| Business Capability Dimension | Reference Candidate Weight (%) |
| --- | ---: |
| Process & Operational Control | 20 |
| Governance, Compliance & Regulatory Readiness | 20 |
| Technology & Intelligent Systems Management | 20 |
| Data, Privacy & Security Controls | 20 |
| Remediation, Verification & Continuous Improvement | 20 |

Rationale:

Equal Contribution treats each approved Business Capability Dimension as
equally important for candidate evaluation. It emphasizes methodology
simplicity, broad taxonomy coverage, and straightforward executive
explainability.

Trade-offs:

- The candidate is simple to communicate and audit.
- The candidate avoids favoring any single capability dimension.
- The candidate does not express differentiated business consequence or
  capability impact among dimensions.
- The candidate may understate dimensions that a future approved methodology
  determines have greater business consequence.

## Candidate B: Business Capability Impact Weighted

Status: `SELECTED_BY_DECISION_7`

These percentages were introduced as a Reference Candidate Weight Set in
Decision 6. Decision 7 separately approves this candidate as the official
Numeric Dimension Weight Set in
`docs/business-decision-methodology/12-official-dimension-weight-set-v1.md`.

| Business Capability Dimension | Reference Candidate Weight (%) |
| --- | ---: |
| Process & Operational Control | 18 |
| Governance, Compliance & Regulatory Readiness | 24 |
| Technology & Intelligent Systems Management | 22 |
| Data, Privacy & Security Controls | 20 |
| Remediation, Verification & Continuous Improvement | 16 |

Rationale:

Business Capability Impact Weighted evaluates a candidate that gives greater
reference emphasis to governance, compliance, regulatory readiness, and
technology and intelligent systems management while preserving full coverage
for all approved Business Capability Dimensions.

Trade-offs:

- The candidate reflects differentiated business capability impact.
- The candidate preserves explainable values and full taxonomy coverage.
- The candidate gives less reference emphasis to remediation, verification,
  and continuous improvement than to governance and technology management.
- The candidate requires more rationale than Equal Contribution because the
  dimensions do not receive identical reference weights.

## Candidate C: Business Risk Weighted

Status: `REFERENCE_CANDIDATE`

These percentages are a Reference Candidate Weight Set only. They are an
evaluation artifact and are not approved production methodology.

| Business Capability Dimension | Reference Candidate Weight (%) |
| --- | ---: |
| Process & Operational Control | 16 |
| Governance, Compliance & Regulatory Readiness | 26 |
| Technology & Intelligent Systems Management | 24 |
| Data, Privacy & Security Controls | 20 |
| Remediation, Verification & Continuous Improvement | 14 |

Rationale:

Business Risk Weighted evaluates a candidate that gives the greatest reference
emphasis to governance, compliance, regulatory readiness, and technology and
intelligent systems management while retaining explicit coverage for every
approved Business Capability Dimension.

Trade-offs:

- The candidate expresses stronger emphasis on business consequence and risk
  exposure.
- The candidate keeps all approved dimensions represented.
- The candidate gives the lowest reference emphasis to remediation,
  verification, and continuous improvement.
- The candidate requires the strongest documented rationale because it creates
  the greatest spread between approved dimensions.

## Comparative Evaluation

Status: `FOUNDATION`

The Decision 6 candidate evaluation remains preserved for traceability.
Decision 6 did not rank candidates, recommend a preferred candidate, or imply
methodology approval. Decision 7 separately selected Candidate B as the
official Numeric Dimension Weight Set.

| Candidate | Approved Terminology | Evaluation Character |
| --- | --- | --- |
| Candidate A | Equal Contribution | Simple, neutral, and evenly distributed across approved dimensions. |
| Candidate B | Business Capability Impact Weighted | Differentiates reference emphasis by business capability impact; selected by Decision 7. |
| Candidate C | Business Risk Weighted | Differentiates reference emphasis by business consequence and risk exposure. |

## Decision 5 Compliance Matrix

Status: `APPROVED`

Each reference candidate is evaluated against the approved Decision 5
mandatory criteria. Compliance means the candidate is valid for evaluation. It
does not mean the candidate is approved for production use.

| Decision 5 Criterion | Candidate A: Equal Contribution | Candidate B: Business Capability Impact Weighted | Candidate C: Business Risk Weighted |
| --- | --- | --- | --- |
| Business Importance Basis | Pass | Pass | Pass |
| Full Taxonomy Coverage | Pass | Pass | Pass |
| Explainability | Pass | Pass | Pass |
| Audit Defensibility | Pass | Pass | Pass |
| Regulatory Neutrality | Pass | Pass | Pass |
| Deterministic Compatibility | Pass | Pass | Pass |
| Version Stability | Pass | Pass | Pass |
| Outcome Independence | Pass | Pass | Pass |
| Methodology Consistency | Pass | Pass | Pass |
| Methodology Simplicity | Pass | Pass | Pass |

Decision 5 compliance confirmation:

- Business Importance Basis: each candidate is framed as a business capability
  evaluation artifact.
- Full Taxonomy Coverage: each candidate includes all five approved Business
  Capability Dimensions.
- Explainability: each candidate uses simple named dimensions and simple
  reference values.
- Audit Defensibility: each candidate includes rationale, trade-offs, and an
  explicit decision boundary.
- Regulatory Neutrality: no candidate is tied to temporary regulatory emphasis
  or vendor-specific requirements.
- Deterministic Compatibility: each candidate is explicit, stable, and
  reproducible as a reference artifact.
- Version Stability: each candidate is recorded under
  `business-decision-methodology-v1`.
- Outcome Independence: no candidate is selected or adjusted based on
  assessment results, customer outcomes, desired readiness distributions, or
  desired scoring distributions.
- Methodology Consistency: each candidate uses the approved Business
  Capability Taxonomy, Question Mapping Methodology, Question Mapping Matrix,
  and Dimension Weighting Governance.
- Methodology Simplicity: each candidate uses simple, easily communicated
  values and avoids unnecessary mathematical precision.

## Future Methodology Decision Required

Status: `METHODOLOGY_PENDING`

Decision 7 approves the official Numeric Dimension Weight Set. Future
methodology remains required before production-authoritative scoring can apply
the official weights.

The following remain `METHODOLOGY_PENDING`:

- Weight normalization methodology.
- Aggregation methodology.
- Final scoring semantics.
- Readiness thresholds and readiness-level assignment.
- Golden fixtures.

## Repository Evidence

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/business-decision-methodology/12-official-dimension-weight-set-v1.md`
