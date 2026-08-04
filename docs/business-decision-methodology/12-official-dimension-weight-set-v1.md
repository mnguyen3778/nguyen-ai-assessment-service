# Official Dimension Weight Set v1

## Purpose

Status: `APPROVED`

This document records Decision 7, the official Numeric Dimension Weight Set
for the approved Business Capability Dimensions in
`business-decision-methodology-v1`.

The approved philosophy is Business Capability Impact Weighted.

This document approves only the Numeric Dimension Weight Set. It does not
define aggregation formulas, scoring mathematics, readiness thresholds,
finding rules, risk methodology, confidence formulas, recommendation logic,
executive summary methodology, implementation values, package contracts, or
snapshot contracts.

## Decision Boundary

Status: `APPROVED`

Decision 7 establishes:

- The official Numeric Dimension Weight Set.
- The selected weighting philosophy.
- Business rationale for the selected weight set.
- Decision 5 criteria confirmation.

Decision 7 does not establish:

- Weight normalization methodology.
- Aggregation methodology.
- Production scoring mathematics.
- Readiness methodology.
- Finding methodology.
- Risk methodology.
- Evidence evaluation methodology.
- Confidence methodology.
- Recommendation methodology.
- Executive summary methodology.
- Golden fixtures.
- Implementation logic.

All downstream methodology remains `METHODOLOGY_PENDING`.

## Methodology Version Identity

Status: `APPROVED`

Methodology version: `business-decision-methodology-v1`

Taxonomy version: `business-capability-taxonomy-v1`

Weight set identifier: `official-dimension-weight-set-v1`

Selected philosophy: Business Capability Impact Weighted

## Official Numeric Dimension Weight Set

Status: `APPROVED`

| Business Capability Dimension | Official Weight (%) |
| --- | ---: |
| Process & Operational Control | 18 |
| Governance, Compliance & Regulatory Readiness | 24 |
| Technology & Intelligent Systems Management | 22 |
| Data, Privacy & Security Controls | 20 |
| Remediation, Verification & Continuous Improvement | 16 |
| Total | 100 |

## Business Rationale

Status: `APPROVED`

The approved weight set reflects Nguyen AI's business methodology. The
methodology prioritizes durable organizational capability rather than
temporary regulatory emphasis.

The approved weight set reflects the following principles:

- Governance, Compliance & Regulatory Readiness is the most important
  organizational capability because it establishes accountability, oversight,
  and regulatory alignment.
- Technology & Intelligent Systems Management is elevated because modern
  organizations increasingly depend upon technology, automation, and
  AI-enabled business processes.
- Data, Privacy & Security Controls remain foundational to trustworthy
  operations and technology integrity.
- Process & Operational Control remains a major contributor to operational
  reliability while recognizing that governance influences operational
  effectiveness.
- Remediation, Verification & Continuous Improvement remains essential but
  represents a downstream capability that strengthens organizational
  resilience after deficiencies are identified.

## Decision 5 Criteria Confirmation

Status: `APPROVED`

The official Numeric Dimension Weight Set satisfies every mandatory Decision 5
criterion.

| Decision 5 Criterion | Result | Confirmation |
| --- | --- | --- |
| Business Importance Basis | Pass | The selected philosophy and rationale are based on durable organizational capability and business consequence. |
| Full Taxonomy Coverage | Pass | The weight set includes all five approved Business Capability Dimensions. |
| Explainability | Pass | Each dimension weight is tied to documented business rationale. |
| Audit Defensibility | Pass | The selected weight set is documented, versioned, and traceable to approved methodology decisions. |
| Regulatory Neutrality | Pass | The weight set prioritizes durable capability rather than temporary regulatory emphasis. |
| Deterministic Compatibility | Pass | The approved values are explicit and reproducible under the methodology version. |
| Version Stability | Pass | The weight set is recorded as `official-dimension-weight-set-v1` under `business-decision-methodology-v1`. |
| Outcome Independence | Pass | The weight set is not selected or adjusted based on individual assessment results, customer outcomes, desired readiness distributions, or desired scoring distributions. |
| Methodology Consistency | Pass | The weight set is consistent with the Business Capability Taxonomy, Question Mapping Methodology, Question Mapping Matrix, and Dimension Weighting Governance. |
| Methodology Simplicity | Pass | The values are simple, readily communicated percentages without unnecessary mathematical precision. |

## Relationship To Decision 6

Status: `APPROVED`

Decision 6 documented three Reference Candidate Weight Sets for evaluation.
Decision 7 selects Candidate B, Business Capability Impact Weighted, as the
official Numeric Dimension Weight Set.

Candidate A and Candidate C remain preserved in
`docs/business-decision-methodology/11-dimension-weight-reference-candidates-v1.md`
as historical reference candidates for traceability.

## Versioning And Change Control

Status: `APPROVED`

Changes to the official Numeric Dimension Weight Set require methodology
version review, documented previous and new values, written rationale,
effective version, non-retroactive application, preserved traceability, and
controlled methodology ownership.

Weights must never be changed to influence individual assessment results,
customer outcomes, desired readiness distributions, or desired scoring
distributions.

## Remaining Methodology Pending

Status: `METHODOLOGY_PENDING`

The official Numeric Dimension Weight Set does not complete downstream
methodology required for production-authoritative rubric output.

The following remain `METHODOLOGY_PENDING`:

- Weight normalization methodology.
- Aggregation methodology.
- Final scoring semantics.
- Final numeric question weights or explicit final equal-weight approval.
- Readiness thresholds and readiness-level assignment.
- Finding methodology.
- Risk methodology.
- Evidence evaluation methodology.
- Confidence methodology.
- Recommendation methodology.
- Executive summary methodology.
- Golden fixtures.

## Repository Evidence

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/business-decision-methodology/11-dimension-weight-reference-candidates-v1.md`
