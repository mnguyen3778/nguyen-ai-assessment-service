# Severity Decision Tables v1

## 1. Purpose

Status: `APPROVED`

This document defines the deterministic Severity Decision Tables for
`business-decision-methodology-v1`.

Severity Decision Tables v1 assigns exactly one approved Severity Level to each
valid generated Finding by applying the approved business-consequence Severity
taxonomy.

This document does not define Risk rules, Confidence rules, Recommendation
rules, Executive Summary rules, implementation code, package contracts, or
snapshot contracts.

## 2. Approved Severity Taxonomy

Status: `APPROVED`

The approved Severity taxonomy remains:

- Critical.
- High.
- Medium.
- Low.
- Informational.

Approved severity definitions:

| Severity Level | Approved Business Consequence Definition |
| --- | --- |
| Critical | A finding that creates a material breach of applicable law, regulation, investor requirements, or organizational governance obligations such that the organization would be considered materially non-compliant if examined today. |
| High | A significant gap materially increasing the likelihood of future non-compliance, operational failure, governance breakdown, or eligibility concerns. |
| Medium | A clear deficiency reducing effectiveness or consistency without currently representing a material breach. |
| Low | A limited weakness suitable for planned improvement. |
| Informational | An observation that is not a defect and may identify strengths, context, or improvement opportunities. |

Severity remains business-consequence based. It expresses consequence, not
certainty. Confidence remains a separate methodology responsibility.

## 3. Decision Table Structure

Status: `APPROVED`

Decision table ID:

```text
severity-decision-tables-v1
```

Decision table version:

```text
severity-decision-table-set-v1
```

Each rule includes:

- Rule ID.
- Finding Type condition.
- Business Consequence Basis condition.
- Required context condition.
- Severity output.
- Rule rationale.
- Traceability requirement.

Primary Dimension, Readiness context, Evidence Availability, and Evidence
Quality are required context inputs. They do not change the assigned Severity
unless an approved rule explicitly states that they do.

Severity Decision Tables v1 does not define any rule that changes Severity
based on Risk, Confidence, Recommendation priority, or Executive Summary
content.

## 4. Severity Decision Tables

Status: `APPROVED`

### Table A: Deficiency Severity Assignment

Table A applies only to Findings with Finding Type `Deficiency`.

| Rule ID | Finding Type | Business Consequence Basis | Required Context | Severity Output | Rule Rationale |
| --- | --- | --- | --- | --- | --- |
| `severity-v1-deficiency-critical` | `Deficiency` | Material current breach of applicable law, regulation, investor requirements, or organizational governance obligations such that the organization would be considered materially non-compliant if examined today. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | Critical | Matches the approved Critical definition. |
| `severity-v1-deficiency-high` | `Deficiency` | Significant gap materially increasing the likelihood of future non-compliance, operational failure, governance breakdown, or eligibility concerns. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | High | Matches the approved High definition. |
| `severity-v1-deficiency-medium` | `Deficiency` | Clear deficiency reducing effectiveness or consistency without currently representing a material breach. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | Medium | Matches the approved Medium definition. |
| `severity-v1-deficiency-low` | `Deficiency` | Limited weakness suitable for planned improvement. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | Low | Matches the approved Low definition. |

### Table B: Non-Defect Finding Severity Assignment

Table B applies to Findings that are not defects.

| Rule ID | Finding Type | Business Consequence Basis | Required Context | Severity Output | Rule Rationale |
| --- | --- | --- | --- | --- | --- |
| `severity-v1-observation-informational` | `Observation` | Observation that is not a defect and identifies context or an improvement opportunity. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | Informational | Matches the approved Informational definition. |
| `severity-v1-strength-informational` | `Strength` | Finding that is not a defect and identifies a strength. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | Informational | Matches the approved Informational definition for non-defect findings. |
| `severity-v1-opportunity-informational` | `Opportunity` | Finding that is not a defect and identifies an improvement opportunity. | Valid Primary Dimension, Readiness context, Evidence Availability, Evidence Quality, source references, and methodology version. | Informational | Matches the approved Informational definition for improvement opportunities. |

### Table C: Invalid Combination Rejection

Table C defines fail-closed rejection conditions for malformed or unsupported
severity inputs.

| Rule ID | Invalid Condition | Required Output |
| --- | --- | --- |
| `severity-v1-reject-nondefect-defect-consequence` | Finding Type is `Observation`, `Strength`, or `Opportunity`, but Business Consequence Basis asserts Critical, High, Medium, or Low defect consequence. | Fail closed; do not assign Severity. |
| `severity-v1-reject-deficiency-informational-consequence` | Finding Type is `Deficiency`, but Business Consequence Basis asserts only non-defect context, strength, or opportunity. | Fail closed; do not assign Severity. |
| `severity-v1-reject-unsupported-finding-type` | Finding Type is not one of `Deficiency`, `Observation`, `Strength`, or `Opportunity`. | Fail closed; do not assign Severity. |
| `severity-v1-reject-unsupported-consequence` | Business Consequence Basis does not match one approved rule condition. | Fail closed; do not assign Severity. |

## 5. Required Inputs

Status: `APPROVED`

Severity Decision Tables v1 requires:

- Finding ID.
- Finding Type.
- Finding characteristics.
- Primary Dimension.
- Related Dimensions, if present.
- Trigger Source.
- Source references.
- Readiness context.
- Business Consequence Basis.
- Evidence Availability.
- Evidence Quality.
- Finding methodology version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Severity decision table version.
- Methodology version.

Required input constraints:

- Finding Type must be one of `Deficiency`, `Observation`, `Strength`, or
  `Opportunity`.
- Business Consequence Basis must match exactly one approved decision rule.
- Evidence Availability must indicate that required evidence is present.
- Evidence Quality must be evaluated for available evidence.
- Readiness context must be valid or Incomplete under approved Readiness
  Methodology.
- Primary Dimension must be one approved Business Capability Dimension.
- Source references must preserve traceability to upstream generated Findings
  and evidence evaluation artifacts.

Evidence Quality affects assertability. It does not reduce or increase the
inherent business consequence represented by the Finding.

## 6. Required Outputs

Status: `APPROVED`

Each valid Severity Decision Table evaluation produces exactly one Severity
Assignment for one Finding.

Required output:

- Severity Level, one of:
  - Critical.
  - High.
  - Medium.
  - Low.
  - Informational.

Required output traceability:

- Finding ID.
- Finding Type.
- Assigned Severity Level.
- Business Consequence Basis.
- Triggering decision rule ID.
- Decision table ID.
- Decision table version.
- Severity taxonomy version.
- Finding methodology version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Methodology version.
- Input artifact references.
- Severity rationale.

Severity Assignment is an independent attribute of an existing Finding. It does
not modify Findings or upstream deterministic business truth.

## 7. Validation Rules

Status: `APPROVED`

Severity Decision Table validation must fail closed.

Required validation rules:

- Every valid Finding must resolve to exactly one Severity Level.
- Every valid Finding Type and Business Consequence Basis combination must
  match exactly one rule.
- No valid input combination may match more than one Severity output.
- No conflicting rules are permitted.
- No overlapping rules are permitted.
- No unsupported Severity Levels are permitted.
- Finding Type must be valid.
- Business Consequence Basis must be valid.
- Required context inputs must be present and versioned.
- Required source references must be present.
- Decision table version must be `severity-decision-table-set-v1`.
- Methodology version must be `business-decision-methodology-v1`.
- Unsupported methodology versions must fail closed.
- Unsupported decision table versions must fail closed.
- Severity must remain independent of Risk and Confidence.

## 8. Fail-Closed Rules

Status: `APPROVED`

Severity Assignment must fail closed when:

- Finding ID is missing.
- Finding Type is missing.
- Finding Type is unsupported.
- Business Consequence Basis is missing.
- Business Consequence Basis is unsupported.
- Required context inputs are missing.
- Required source references are missing.
- Evidence Availability indicates required evidence is missing.
- Evidence Quality is unavailable for present evidence.
- Required methodology versions are missing or unsupported.
- Decision table version is missing or unsupported.
- More than one Severity Level could be assigned.
- No Severity Level can be assigned.
- Rule inputs are malformed, incomplete, ambiguous, or conflicting.

Fail-closed Severity Assignment means no Severity Level is assigned. It does
not create a partial Severity Assignment and does not modify the Finding.

## 9. Version Identity

Status: `APPROVED`

Severity decision table artifact version:

```text
severity-decision-tables-v1
```

Severity decision table set version:

```text
severity-decision-table-set-v1
```

Severity taxonomy version:

```text
severity-taxonomy-v1
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

Severity Decision Tables v1 satisfies:

- Determinism: the same valid Finding and approved context under the same
  decision table version always produces the same Severity Level.
- Idempotence: reassigning Severity from the same valid inputs under the same
  methodology version produces identical Severity Assignment.
- Single output: each valid Finding receives exactly one Severity Level.
- Complete coverage: all approved valid severity input scenarios resolve to a
  deterministic Severity output.
- Non-conflict: no valid input scenario matches multiple incompatible Severity
  outputs.
- Traceability: every Severity Assignment traces to the Finding, source inputs,
  decision rule, decision table version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions are
  reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Severity taxonomy version, Finding methodology version,
  Readiness methodology version, and Evidence Evaluation methodology version.
- Severity independence: Severity Assignment does not modify Finding identity,
  Finding type, Finding content, scores, aggregation, readiness, Evidence
  Evaluation, Risk, Confidence, Recommendations, or Executive Summary output.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules prevent Severity Assignment.

## 11. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every valid input combination resolves to exactly one Severity Level. | Pass |
| No overlapping rules are present. | Pass |
| No conflicting rules are present. | Pass |
| No undefined valid states are present. | Pass |
| Invalid or incomplete inputs fail closed. | Pass |
| Decision tables remain deterministic. | Pass |
| Severity remains independent of Risk. | Pass |
| Severity remains independent of Confidence. | Pass |
| Only approved Severity Levels are emitted. | Pass |
| Decision table version is defined. | Pass |

## 12. Remaining Implementation Artifacts

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 13. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE SEVERITY DECISION TABLES V1
```

The deterministic Severity Decision Tables are approved for
`business-decision-methodology-v1`. They assign exactly one approved Severity
Level to every valid generated Finding and fail closed for malformed,
unsupported, incomplete, ambiguous, or conflicting inputs.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/16-severity-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/21-readiness-threshold-values-v1.md`
