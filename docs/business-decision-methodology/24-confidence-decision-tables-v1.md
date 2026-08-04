# Confidence Decision Tables v1

## 1. Purpose

Status: `APPROVED`

This document defines the deterministic Confidence Decision Tables for
`business-decision-methodology-v1`.

Confidence Decision Tables v1 resolves every complete valid assessment to
exactly one Confidence Level. Confidence expresses certainty in the produced
business truth.

This document does not define Recommendation rules, Executive Summary rules,
implementation code, package contracts, or snapshot contracts.

## 2. Approved Confidence Taxonomy

Status: `APPROVED`

The approved Confidence taxonomy is:

- Very High Confidence.
- High Confidence.
- Moderate Confidence.
- Low Confidence.
- Insufficient Confidence.

Confidence measures certainty, not readiness, severity, risk, or
recommendation priority.

Confidence consumes upstream artifacts. Confidence never modifies:

- Scores.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity Assignment.
- Risk Assessment.
- Recommendations.
- Executive Summary output.

## 3. Decision Table Structure

Status: `APPROVED`

Decision table ID:

```text
confidence-decision-tables-v1
```

Decision table version:

```text
confidence-decision-table-set-v1
```

Each rule includes:

- Rule ID.
- Evidence Availability condition.
- Evidence Quality condition.
- Assessment completeness condition.
- Required upstream context.
- Confidence Level output.
- Rule rationale.
- Traceability requirement.

Rule evaluation order is deterministic and proceeds from lowest certainty to
highest certainty:

1. Insufficient Confidence.
2. Low Confidence.
3. Moderate Confidence.
4. High Confidence.
5. Very High Confidence.

Risk Assessment, Readiness, Findings, and Severity Assignment are required
upstream context for traceability and completeness. They do not increase or
decrease Confidence in Confidence Decision Tables v1.

## 4. Confidence Decision Tables

Status: `APPROVED`

Table A applies to one complete valid assessment with valid upstream Assessment
Service artifacts. The rules are mutually exclusive. If a valid assertability
limitation is present, only the Insufficient Confidence rule applies; otherwise
the evidence quality rules apply.

| Rule ID | Evidence Availability Condition | Evidence Quality Condition | Assessment Completeness Condition | Required Upstream Context | Confidence Level Output | Rule Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| `confidence-v1-insufficient-unassertable` | Required evidence is present and Evidence Evaluation is complete. | One or more present required evidence items has a valid Evidence Evaluation assertability limitation under authenticity or traceability criteria. | Assessment completeness is valid. | Valid Readiness, Findings, Severity Assignment, Risk Assessment, and methodology version. | Insufficient Confidence | The Assessment Service cannot assert high certainty in produced business truth when required evidence is present but valid evidence evaluation identifies an assertability limitation. |
| `confidence-v1-low-basic-only` | Required evidence is present. | No assertability limitation is present, and all evaluated available evidence is `Basic`. | Assessment completeness is valid. | Valid Readiness, Findings, Severity Assignment, Risk Assessment, and methodology version. | Low Confidence | Basic-only evidence supports limited certainty and requires cautious interpretation. |
| `confidence-v1-moderate-mixed-basic-adequate` | Required evidence is present. | No assertability limitation is present, and available evidence includes `Adequate` and may include `Basic`, but includes no `Strong` evidence. | Assessment completeness is valid. | Valid Readiness, Findings, Severity Assignment, Risk Assessment, and methodology version. | Moderate Confidence | Adequate evidence supports directional certainty while preserving the need for validation. |
| `confidence-v1-high-strong-present` | Required evidence is present. | No assertability limitation is present, available evidence includes `Strong`, and at least one remaining evidence item is `Adequate` or `Basic`. | Assessment completeness is valid. | Valid Readiness, Findings, Severity Assignment, Risk Assessment, and methodology version. | High Confidence | Strong evidence increases certainty in the produced business truth while mixed evidence quality prevents assignment to the highest confidence level. |
| `confidence-v1-very-high-strong-only` | Required evidence is present. | No assertability limitation is present, and all evaluated available evidence is `Strong`. | Assessment completeness is valid. | Valid Readiness, Findings, Severity Assignment, Risk Assessment, and methodology version. | Very High Confidence | Strong evidence across all evaluated available evidence provides the highest approved certainty level. |

Table B defines fail-closed rejection conditions for malformed or unsupported
confidence inputs.

| Rule ID | Invalid Condition | Required Output |
| --- | --- | --- |
| `confidence-v1-reject-missing-required-evidence` | Required evidence is missing under Evidence Availability methodology. | Fail closed; do not assign Confidence. |
| `confidence-v1-reject-incomplete-assessment` | Assessment completeness is missing, invalid, or unsupported. | Fail closed; do not assign Confidence. |
| `confidence-v1-reject-missing-upstream-artifact` | Required upstream Readiness, Finding, Severity Assignment, Risk Assessment, or Evidence Evaluation context is missing. | Fail closed; do not assign Confidence. |
| `confidence-v1-reject-unsupported-confidence-level` | A rule attempts to emit a Confidence Level outside the approved taxonomy. | Fail closed; do not assign Confidence. |

## 5. Required Inputs

Status: `APPROVED`

Confidence Decision Tables v1 requires:

- Evidence Evaluation.
- Evidence Availability.
- Evidence Quality.
- Findings.
- Severity Assignment.
- Risk Assessment.
- Readiness.
- Assessment completeness.
- Evidence Evaluation methodology version.
- Finding methodology version.
- Severity decision table version.
- Risk decision table version.
- Readiness methodology version.
- Confidence decision table version.
- Methodology version.

Required input constraints:

- Evidence Availability must determine that required evidence is present.
- Evidence Quality must be evaluated only for available evidence.
- Evidence Quality classifications must use approved levels: `Basic`,
  `Adequate`, or `Strong`.
- Evidence Authenticity and traceability criteria must be validly evaluated
  for present required evidence.
- Assessment completeness must be valid.
- Findings must be generated under approved Finding Methodology.
- Severity Assignment must be produced under Severity Decision Tables v1.
- Risk Assessment must be produced under Risk Decision Tables v1.
- Readiness must be one approved readiness level under approved Readiness
  Methodology.
- `Incomplete` is an operational processing state, not a readiness level, and
  fails closed for Confidence Assessment output.
- Confidence Decision Tables shall not recalculate or reinterpret upstream
  business truth.

Answer consistency, response quality, and business certainty remain outside
Confidence Decision Tables v1 until deterministic rules for those factors are
separately approved.

## 6. Required Outputs

Status: `APPROVED`

Each valid Confidence Decision Table evaluation produces exactly one Confidence
Assessment for one complete assessment.

Required output:

- Confidence Level, one of:
  - Very High Confidence.
  - High Confidence.
  - Moderate Confidence.
  - Low Confidence.
  - Insufficient Confidence.

Required output traceability:

- Confidence Assessment ID.
- Assigned Confidence Level.
- Triggering decision rule ID.
- Decision table ID.
- Decision table version.
- Confidence taxonomy version.
- Evidence Evaluation methodology version.
- Finding methodology version.
- Severity decision table version.
- Risk decision table version.
- Readiness methodology version.
- Methodology version.
- Evidence Evaluation references.
- Finding references.
- Severity Assignment references.
- Risk Assessment references.
- Readiness references.
- Confidence rationale.

Confidence Assessment is a downstream assessment artifact. It does not modify
any upstream deterministic business truth.

## 7. Validation Rules

Status: `APPROVED`

Confidence Decision Table validation must fail closed.

Required validation rules:

- Every complete valid assessment must resolve to exactly one Confidence Level.
- No complete valid assessment may resolve to more than one Confidence Level.
- No conflicting rules are permitted.
- No duplicate rule IDs are permitted.
- No unsupported Confidence Levels are permitted.
- Required input fields must be complete and versioned.
- Evidence Availability must be valid.
- Evidence Quality must be valid for available evidence.
- Required upstream artifacts must be present and versioned.
- Decision table version must be `confidence-decision-table-set-v1`.
- Methodology version must be `business-decision-methodology-v1`.
- Unsupported methodology versions must fail closed.
- Unsupported decision table versions must fail closed.
- Confidence must consume upstream artifacts only.
- Confidence must not modify upstream business truth.
- Confidence must remain independent of Recommendations.

## 8. Fail-Closed Rules

Status: `APPROVED`

Confidence Assessment must fail closed when:

- Evidence Evaluation is missing, malformed, or unsupported.
- Evidence Availability is missing, malformed, or unsupported.
- Required evidence is missing.
- Evidence Quality is missing for present evidence.
- Evidence Quality is unsupported.
- Assessment completeness is missing, invalid, or unsupported.
- Findings are missing, malformed, or unsupported.
- Severity Assignment is missing, malformed, or unsupported.
- Risk Assessment is missing, malformed, or unsupported.
- Readiness context is missing, malformed, or unsupported.
- Readiness is `Incomplete`.
- Required methodology versions are missing or unsupported.
- Decision table version is missing or unsupported.
- More than one Confidence Level could be assigned.
- No Confidence Level can be assigned to a complete valid assessment.
- Rule inputs are malformed, incomplete, ambiguous, or conflicting.

Fail-closed Confidence Assessment means no Confidence Level is assigned. It
does not create a partial Confidence Assessment and does not modify scores,
Readiness, Evidence Evaluation, Findings, Severity, Risk, Recommendations, or
Executive Summary output.

## 9. Version Identity

Status: `APPROVED`

Confidence decision table artifact version:

```text
confidence-decision-tables-v1
```

Confidence decision table set version:

```text
confidence-decision-table-set-v1
```

Confidence taxonomy version:

```text
confidence-taxonomy-v1
```

Evidence Evaluation methodology version:

```text
evidence-evaluation-methodology-v1
```

Finding methodology version:

```text
finding-methodology-v1
```

Severity decision table set version:

```text
severity-decision-table-set-v1
```

Risk decision table set version:

```text
risk-decision-table-set-v1
```

Readiness methodology version:

```text
readiness-methodology-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

## 10. Computational Properties

Status: `APPROVED`

Confidence Decision Tables v1 satisfies:

- Determinism: the same complete set of valid upstream artifacts under the same
  decision table version always produces the same Confidence Assessment.
- Idempotence: re-evaluating Confidence from the same valid inputs under the
  same methodology version produces identical Confidence Assessment.
- Single output: each complete valid assessment receives exactly one
  Confidence Level.
- Complete coverage: all approved valid assessment states resolve to a
  deterministic Confidence output.
- Non-conflict: no valid assessment state matches multiple incompatible
  Confidence outputs.
- Traceability: every Confidence Assessment traces to upstream artifacts,
  decision rule, decision table version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions are
  reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Confidence taxonomy version, Evidence Evaluation
  methodology version, Finding methodology version, Severity Decision Table
  version, Risk Decision Table version, and Readiness methodology version.
- Deterministic independence: Confidence evaluation does not modify upstream
  deterministic business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules prevent Confidence Assessment.

## 11. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every valid assessment resolves to exactly one Confidence Level. | Pass |
| No duplicate rule IDs are present. | Pass |
| No conflicting rules are present. | Pass |
| No undefined valid assessment states are present. | Pass |
| Invalid or incomplete inputs fail closed. | Pass |
| Confidence consumes upstream artifacts only. | Pass |
| Confidence never modifies upstream business truth. | Pass |
| Confidence remains independent of Recommendations. | Pass |
| Only approved Confidence Levels are emitted. | Pass |
| Decision table version is defined. | Pass |

## 12. Remaining Implementation Artifacts

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 13. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE CONFIDENCE DECISION TABLES V1
```

The deterministic Confidence Decision Tables are approved for
`business-decision-methodology-v1`. They assign exactly one Confidence Level to
every complete valid assessment and fail closed for malformed, unsupported,
incomplete, ambiguous, or conflicting inputs.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/18-confidence-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
- `docs/business-decision-methodology/23-risk-decision-tables-v1.md`
