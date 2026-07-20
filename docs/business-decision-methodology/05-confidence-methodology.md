# Confidence Methodology

## Purpose

This document defines deterministic confidence methodology for Nguyen AI's
Business Decision Framework. Confidence explains how strongly the platform can
stand behind a readiness conclusion or recommendation.

This document does not define formulas. It defines the factors, levels,
adjustment principles, and traceability requirements that will later become
business rules.

Methodology version: `business-decision-methodology-v1`

## Confidence Principle

Confidence is separate from readiness.

An organization may show high readiness signals with low confidence if evidence
is incomplete, inconsistent, vague, or narrow. The platform must not convert low
confidence into positive readiness.

## Confidence Factors

| Factor | Purpose | Positive Signal | Negative Signal |
| --- | --- | --- | --- |
| Assessment Completeness | Measures whether required questions were answered. | Required and important questions are answered across dimensions. | Missing answers in foundational or risk-control areas. |
| Answer Consistency | Measures whether related answers support each other. | Related answers align across governance, operations, and technology. | Answers conflict, such as high automation maturity with no documented processes. |
| Evidence Coverage | Measures whether enough evidence categories support conclusions. | Multiple evidence categories support a readiness dimension. | A conclusion depends on one narrow evidence category. |
| Response Quality | Measures whether answers are specific enough to support decisions. | Responses indicate ownership, maturity, measurement, or control. | Responses are vague, unknown, or unsupported. |
| Business Certainty | Measures whether business outcomes, sponsorship, and risk appetite are clear. | Goals, sponsors, metrics, and decision cadence are defined. | Business intent is unclear or leadership alignment is missing. |

## Confidence Levels

| Level | Meaning | Executive Interpretation |
| --- | --- | --- |
| `low` | Evidence is incomplete, inconsistent, vague, or narrow. | Use the assessment to guide discovery before making major commitments. |
| `moderate` | Evidence is sufficient for directional recommendations but may need validation. | Proceed with priority planning while validating key assumptions. |
| `high` | Evidence is broad, consistent, and specific enough for confident action. | Proceed with recommended action sequence and engagement planning. |

## Deterministic Adjustment Principles

Assessment completeness:

- Missing foundational-control questions reduce confidence.
- Missing strategic-alignment questions reduce confidence in executive
  recommendations.
- Missing risk-control questions reduce confidence in readiness and service
  mapping.

Answer consistency:

- Conflicts between related dimensions reduce confidence.
- Examples of conflicts include high AI ambition with no governance owner,
  high automation interest with undocumented processes, or high cloud usage with
  no cost controls.

Evidence coverage:

- Broad evidence coverage increases confidence.
- Narrow evidence coverage limits confidence even when individual answers are
  favorable.

Response quality:

- Specific answers with ownership, cadence, measurement, or controls increase
  confidence.
- Unknown, partial, or unsupported answers reduce confidence.

Business certainty:

- Defined outcomes, executive alignment, financial rationale, and risk appetite
  increase confidence in recommendations.
- Unclear outcomes or weak sponsorship reduce confidence and may route to
  assessment-only or workshop services.

## Confidence Suppression Rules

Low confidence should suppress:

- Aggressive implementation recommendations.
- Managed service recommendations.
- Claims of strategic readiness.
- Highly specific ROI or business outcome claims.

Low confidence should favor:

- Assessment Only.
- AI Strategy Workshop.
- Evidence discovery.
- Executive alignment work.

## Confidence Traceability

Every confidence result should include:

- Confidence level.
- Confidence rationale.
- Positive contributors.
- Negative contributors.
- Missing evidence references.
- Conflicting evidence references.
- Affected recommendations.

Future reference pattern:

```text
confidence.<factor>.<finding>
```

Examples:

- `confidence.completeness.missing-security-controls`
- `confidence.consistency.ai-governance-conflict`
- `confidence.coverage.cloud-evidence-gap`

## Testability Requirements

Future tests must validate:

- Completeness changes confidence deterministically.
- Conflicting answers reduce confidence deterministically.
- Low confidence suppresses implementation and managed service recommendations.
- Confidence does not increase readiness scores.
- Confidence outputs include evidence references.

