# Risk Decision Tables v1

## 1. Purpose

Status: `APPROVED`

This document defines the deterministic Risk Decision Tables for
`business-decision-methodology-v1`.

Risk Decision Tables v1 evaluates the complete assessment and assigns exactly
one Assessment-Level Risk by consuming the complete collection of
Severity-Assigned Findings.

This document does not define Finding-Level Risk, Confidence rules,
Recommendation rules, Executive Summary rules, implementation code, package
contracts, or snapshot contracts.

## 2. Approved Risk Taxonomy

Status: `APPROVED`

The approved Risk taxonomy remains:

- Critical Risk.
- Elevated Risk.
- Moderate Risk.
- Low Risk.
- Minimal / Informational.

Risk remains assessment-level only. Severity remains the business consequence
classification for individual Findings.

Risk consumes Severity-Assigned Findings. Risk never modifies Findings,
Severity Assignment, Readiness, Evidence Evaluation, scores, aggregation,
Confidence, Recommendations, or Executive Summary output.

## 3. Decision Table Structure

Status: `APPROVED`

Decision table ID:

```text
risk-decision-tables-v1
```

Decision table version:

```text
risk-decision-table-set-v1
```

Each rule includes:

- Rule ID.
- Severity distribution condition.
- Required assessment context.
- Assessment-Level Risk output.
- Rule rationale.
- Traceability requirement.

Rule evaluation order is deterministic and proceeds from highest consequence
to lowest consequence:

1. Critical Severity findings.
2. High Severity finding concentration.
3. Single High or any Medium Severity findings.
4. Low Severity findings.
5. Informational-only or no-defect findings.

Risk Decision Tables v1 establishes the deterministic high-concentration rule
for High Severity findings as:

```text
two or more High Severity Findings in the complete assessment
```

No cross-dimension dependency escalation is approved in Risk Decision Tables
v1. Cross-dimension dependency conditions remain unsupported unless separately
approved by a future methodology decision.

## 4. Risk Decision Tables

Status: `APPROVED`

Table A applies to one complete valid assessment with a complete collection of
Severity-Assigned Findings.

| Rule ID | Severity Distribution Condition | Required Assessment Context | Assessment-Level Risk Output | Rule Rationale |
| --- | --- | --- | --- | --- |
| `risk-v1-critical-any-critical` | One or more Severity-Assigned Findings has Severity `Critical`. | Complete Severity-Assigned Finding collection, valid Readiness context, valid Evidence Evaluation context, and methodology version. | Critical Risk | Presence of Critical Findings is an approved Risk evaluation condition and represents the highest assessment-level business impact. |
| `risk-v1-elevated-high-concentration` | No `Critical` Severity is present, and two or more Severity-Assigned Findings have Severity `High`. | Complete Severity-Assigned Finding collection, valid Readiness context, valid Evidence Evaluation context, and methodology version. | Elevated Risk | High concentration of High Severity Findings is an approved Risk evaluation condition and represents elevated assessment-level business impact. |
| `risk-v1-moderate-single-high` | No `Critical` Severity is present, and exactly one Severity-Assigned Finding has Severity `High`. | Complete Severity-Assigned Finding collection, valid Readiness context, valid Evidence Evaluation context, and methodology version. | Moderate Risk | A single High Severity Finding materially affects assessment-level business impact but does not meet the v1 high-concentration rule. |
| `risk-v1-moderate-any-medium` | No `Critical` or `High` Severity is present, and one or more Severity-Assigned Findings has Severity `Medium`. | Complete Severity-Assigned Finding collection, valid Readiness context, valid Evidence Evaluation context, and methodology version. | Moderate Risk | Medium Severity Findings represent clear deficiencies that reduce effectiveness or consistency and produce moderate assessment-level business impact. |
| `risk-v1-low-low-only-defects` | No `Critical`, `High`, or `Medium` Severity is present, and one or more Severity-Assigned Findings has Severity `Low`. | Complete Severity-Assigned Finding collection, valid Readiness context, valid Evidence Evaluation context, and methodology version. | Low Risk | Low Severity Findings represent limited weaknesses suitable for planned improvement and produce low assessment-level business impact. |
| `risk-v1-minimal-informational-only` | No `Critical`, `High`, `Medium`, or `Low` Severity is present, and zero or more Severity-Assigned Findings have Severity `Informational`. | Complete Severity-Assigned Finding collection, valid Readiness context, valid Evidence Evaluation context, and methodology version. | Minimal / Informational | Informational Findings are not defects and may identify strengths, context, or improvement opportunities; they do not create defect-based assessment-level risk. |

## 5. Required Inputs

Status: `APPROVED`

Risk Decision Tables v1 requires:

- Complete collection of Severity-Assigned Findings.
- Finding IDs.
- Finding Types.
- Assigned Severity Levels.
- Primary Dimensions.
- Related Dimensions, if present.
- Readiness context.
- Evidence Evaluation context.
- Severity decision table version.
- Finding methodology version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Risk decision table version.
- Methodology version.

Required input constraints:

- The Severity-Assigned Finding collection must be complete for the assessment.
- Every Finding in the collection must have exactly one approved Severity
  Level assigned under Severity Decision Tables v1.
- Assigned Severity Levels must be one of `Critical`, `High`, `Medium`, `Low`,
  or `Informational`.
- Readiness context must be valid or Incomplete under approved Readiness
  Methodology.
- Evidence Evaluation context must be valid under approved Evidence Evaluation
  Methodology.
- Risk Decision Tables shall not independently reinterpret Findings or
  Severity Assignment.

## 6. Required Outputs

Status: `APPROVED`

Each valid Risk Decision Table evaluation produces exactly one Assessment-Level
Risk for one complete assessment.

Required output:

- Assessment-Level Risk, one of:
  - Critical Risk.
  - Elevated Risk.
  - Moderate Risk.
  - Low Risk.
  - Minimal / Informational.

Required output traceability:

- Risk Assessment ID.
- Assigned Assessment-Level Risk.
- Triggering decision rule ID.
- Decision table ID.
- Decision table version.
- Risk taxonomy version.
- Severity decision table version.
- Finding methodology version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Methodology version.
- Severity-Assigned Finding references.
- Readiness references.
- Evidence Evaluation references.
- Risk rationale.

Risk Assessment is a downstream assessment artifact. It does not modify any
upstream deterministic business truth.

## 7. Validation Rules

Status: `APPROVED`

Risk Decision Table validation must fail closed.

Required validation rules:

- Every complete valid assessment must resolve to exactly one Assessment-Level
  Risk.
- No complete valid assessment may resolve to more than one Assessment-Level
  Risk.
- No conflicting rules are permitted.
- No duplicate rule IDs are permitted.
- No unsupported Risk outputs are permitted.
- Required input fields must be complete and versioned.
- Every Severity-Assigned Finding must have exactly one approved Severity
  Level.
- The complete Severity-Assigned Finding collection must be evaluated.
- Decision table version must be `risk-decision-table-set-v1`.
- Methodology version must be `business-decision-methodology-v1`.
- Unsupported methodology versions must fail closed.
- Unsupported decision table versions must fail closed.
- Risk must remain independent of Confidence and Recommendations.
- Risk must consume Severity Assignment without modifying Severity Assignment.

## 8. Fail-Closed Rules

Status: `APPROVED`

Risk Assessment must fail closed when:

- The Severity-Assigned Finding collection is missing.
- The Severity-Assigned Finding collection is incomplete.
- Any Finding is missing a Severity Assignment.
- Any Finding has more than one Severity Assignment.
- Any assigned Severity Level is unsupported.
- Readiness context is missing, malformed, or unsupported.
- Evidence Evaluation context is missing, malformed, or unsupported.
- Required methodology versions are missing or unsupported.
- Decision table version is missing or unsupported.
- More than one Assessment-Level Risk could be assigned.
- No Assessment-Level Risk can be assigned to a complete valid assessment.
- Rule inputs are malformed, incomplete, ambiguous, or conflicting.

Fail-closed Risk Assessment means no Assessment-Level Risk is assigned. It does
not create a partial Risk Assessment and does not modify Findings, Severity
Assignment, Readiness, Evidence Evaluation, scores, Confidence,
Recommendations, or Executive Summary output.

## 9. Version Identity

Status: `APPROVED`

Risk decision table artifact version:

```text
risk-decision-tables-v1
```

Risk decision table set version:

```text
risk-decision-table-set-v1
```

Risk taxonomy version:

```text
risk-taxonomy-v1
```

Severity decision table set version:

```text
severity-decision-table-set-v1
```

Finding methodology version:

```text
finding-methodology-v1
```

Readiness methodology version:

```text
readiness-methodology-v1
```

Evidence Evaluation methodology version:

```text
evidence-evaluation-methodology-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

## 10. Computational Properties

Status: `APPROVED`

Risk Decision Tables v1 satisfies:

- Determinism: the same complete set of valid Severity-Assigned Findings and
  approved context under the same decision table version always produces the
  same Assessment-Level Risk.
- Idempotence: re-evaluating Risk from the same valid inputs under the same
  methodology version produces identical Risk Assessment.
- Single output: each complete valid assessment receives exactly one
  Assessment-Level Risk output.
- Complete coverage: all approved valid assessment states resolve to a
  deterministic Risk output.
- Non-conflict: no valid assessment state matches multiple incompatible Risk
  outputs.
- Traceability: every Risk Assessment traces to Severity-Assigned Findings,
  Readiness, Evidence Evaluation, decision rule, decision table version, and
  methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions are
  reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Risk taxonomy version, Severity Decision Table version,
  Finding methodology version, Readiness methodology version, and Evidence
  Evaluation methodology version.
- Risk independence: Risk evaluation does not modify upstream deterministic
  business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules prevent Risk Assessment.

## 11. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every valid assessment resolves to exactly one Assessment-Level Risk. | Pass |
| No conflicting rules are present. | Pass |
| No duplicate rule IDs are present. | Pass |
| No undefined valid assessment states are present. | Pass |
| Invalid or incomplete inputs fail closed. | Pass |
| Risk remains independent of Confidence. | Pass |
| Risk remains independent of Recommendations. | Pass |
| Risk consumes Severity but never modifies Severity. | Pass |
| Only approved Risk outputs are emitted. | Pass |
| Decision table version is defined. | Pass |

## 12. Remaining Implementation Artifacts

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 13. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE RISK DECISION TABLES V1
```

The deterministic Risk Decision Tables are approved for
`business-decision-methodology-v1`. They assign exactly one Assessment-Level
Risk to every complete valid assessment and fail closed for malformed,
unsupported, incomplete, ambiguous, or conflicting inputs.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/17-risk-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
