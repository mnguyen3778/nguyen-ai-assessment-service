# Recommendation Decision Tables v1

## 1. Purpose

Status: `APPROVED`

This document defines the deterministic Recommendation Decision Tables for
`business-decision-methodology-v1`.

Recommendation Decision Tables v1 resolves every complete valid assessment to
a deterministic Recommendation set. Recommendations are advisory outputs only
and are derived from approved Assessment Service business truth.

This document does not define Executive Summary rules, presentation
formatting, narrative templates, implementation code, package contracts, or
snapshot contracts.

## 2. Approved Recommendation Taxonomy

Status: `APPROVED`

The approved Recommendation taxonomy is:

- Immediate Action.
- Priority Action.
- Planned Improvement.
- Best Practice.
- Monitor.

Recommendations are advisory outputs. They do not imply automatic workflow
execution, remediation ownership, task management, verification workflow,
closure workflow, or risk acceptance workflow.

Recommendations consume upstream artifacts. Recommendations never modify:

- Scores.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity Assignment.
- Risk Assessment.
- Confidence Assessment.
- Executive Summary output.

## 3. Decision Table Structure

Status: `APPROVED`

Decision table ID:

```text
recommendation-decision-tables-v1
```

Decision table version:

```text
recommendation-decision-table-set-v1
```

Each rule includes:

- Rule ID.
- Source scope.
- Finding Type condition.
- Severity condition.
- Assessment-Level Risk context.
- Confidence Assessment context.
- Recommendation output.
- Rule rationale.
- Traceability requirement.

Rule evaluation is deterministic and applies to the complete assessment
context. Finding-scoped rules produce advisory Recommendations for
Severity-Assigned Findings. The assessment-scoped rule applies only when the
complete valid assessment has no generated Findings.

Recommendation Decision Tables v1 does not define prioritization formulas.
Stable ordering is defined separately in this artifact as an output ordering
rule, not as a priority-scoring method.

## 4. Recommendation Decision Tables

Status: `APPROVED`

Table A applies to each Severity-Assigned Finding in one complete valid
assessment with valid upstream Assessment Service artifacts.

| Rule ID | Source Scope | Finding Type Condition | Severity Condition | Required Assessment Context | Recommendation Output | Rule Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| `recommendation-v1-deficiency-critical-immediate` | Finding | `Deficiency` | `Critical` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Immediate Action | A Critical Deficiency represents material current business consequence and requires immediate advisory action. |
| `recommendation-v1-deficiency-high-priority` | Finding | `Deficiency` | `High` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Priority Action | A High Severity Deficiency materially increases future business consequence and requires near-term advisory action. |
| `recommendation-v1-deficiency-medium-planned` | Finding | `Deficiency` | `Medium` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Planned Improvement | A Medium Severity Deficiency reduces effectiveness or consistency and is suitable for planned improvement. |
| `recommendation-v1-deficiency-low-planned` | Finding | `Deficiency` | `Low` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Planned Improvement | A Low Severity Deficiency is a limited weakness suitable for planned improvement. |
| `recommendation-v1-observation-monitor` | Finding | `Observation` | `Informational` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Monitor | An Observation is not a defect and should be monitored as assessment context or improvement context. |
| `recommendation-v1-strength-best-practice` | Finding | `Strength` | `Informational` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Best Practice | A Strength is not a defect and may identify a practice to preserve or reuse. |
| `recommendation-v1-opportunity-best-practice` | Finding | `Opportunity` | `Informational` | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Best Practice | An Opportunity is not a defect and may identify a practice or improvement opportunity suitable for advisory guidance. |

Table B applies only when a complete valid assessment has no generated
Findings.

| Rule ID | Source Scope | Finding Collection Condition | Required Assessment Context | Recommendation Output | Rule Rationale |
| --- | --- | --- | --- | --- | --- |
| `recommendation-v1-no-findings-monitor` | Assessment | Complete assessment contains no generated Findings. | Valid Assessment-Level Risk, Confidence Assessment, Readiness, Evidence Evaluation, and methodology version. | Monitor | A complete assessment with no generated Findings still receives deterministic advisory monitoring guidance to preserve traceability and complete output semantics. |

Table C defines fail-closed rejection conditions for malformed or unsupported
recommendation inputs.

| Rule ID | Invalid Condition | Required Output |
| --- | --- | --- |
| `recommendation-v1-reject-missing-finding-collection` | Finding collection is missing or not deterministically complete. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-missing-severity` | One or more generated Findings is missing Severity Assignment. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-unsupported-finding-severity-combination` | Finding Type and Severity combination does not match one approved recommendation rule. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-missing-risk` | Assessment-Level Risk is missing, malformed, or unsupported. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-missing-confidence` | Confidence Assessment is missing, malformed, or unsupported. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-missing-context` | Required Readiness, Evidence Evaluation, source references, or methodology version context is missing. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-unsupported-recommendation-label` | A rule attempts to emit a Recommendation label outside the approved taxonomy. | Fail closed; do not emit Recommendations. |
| `recommendation-v1-reject-duplicate-output` | Recommendation output contains duplicate Recommendation IDs or duplicate canonical advisory action keys. | Fail closed; do not emit Recommendations. |

## 5. Required Inputs

Status: `APPROVED`

Recommendation Decision Tables v1 requires:

- Complete Finding collection.
- Finding IDs.
- Finding Types.
- Primary Dimensions.
- Related Dimensions, if present.
- Source references.
- Severity Assignment.
- Risk Assessment.
- Confidence Assessment.
- Readiness.
- Evidence Evaluation.
- Finding methodology version.
- Severity decision table version.
- Risk decision table version.
- Confidence decision table version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Recommendation decision table version.
- Methodology version.

Required input constraints:

- The Finding collection must be complete for the assessment.
- Each generated Finding must have exactly one approved Finding Type.
- Each generated Finding must have exactly one Severity Assignment under
  Severity Decision Tables v1.
- Finding Type and Severity must match exactly one approved recommendation
  assignment rule.
- Risk Assessment must be produced under Risk Decision Tables v1.
- Confidence Assessment must be produced under Confidence Decision Tables v1.
- Readiness must be one approved readiness level under approved Readiness
  Methodology.
- Evidence Evaluation must be valid under approved Evidence Evaluation
  Methodology.
- Required upstream artifacts must be present and versioned.
- Recommendation Decision Tables shall not recalculate or reinterpret upstream
  business truth.

## 6. Required Outputs

Status: `APPROVED`

Each valid Recommendation Decision Table evaluation produces one deterministic
Recommendation set for one complete assessment.

Each Recommendation must include:

- Recommendation ID.
- Recommendation taxonomy label.
- Recommendation title.
- Advisory action statement.
- Recommendation rationale.
- Source scope.
- Source Finding references, if finding-scoped.
- Source Severity Assignment references.
- Source Risk Assessment references.
- Source Confidence Assessment references.
- Source Readiness references.
- Source Evidence Evaluation references.
- Triggering decision rule ID.
- Decision table ID.
- Decision table version.
- Recommendation taxonomy version.
- Methodology version.
- Canonical advisory action key.

Recommendation set output must include:

- Recommendation set ID.
- Recommendation count.
- Stable deterministic ordering metadata.
- Duplicate-prevention validation status.
- Recommendation set rationale.
- Methodology version.
- Recommendation decision table version.

Recommendation outputs are advisory artifacts. They do not modify any upstream
deterministic business truth.

## 7. Validation Rules

Status: `APPROVED`

Recommendation Decision Table validation must fail closed.

Required validation rules:

- Every complete valid assessment must resolve to a deterministic
  Recommendation set.
- Every generated Finding must match exactly one recommendation assignment
  rule.
- A complete valid assessment with no Findings must match the no-Findings
  assessment rule.
- No complete valid assessment may produce conflicting Recommendation outputs.
- No duplicate rule IDs are permitted.
- No unsupported Recommendation labels are permitted.
- Required input fields must be complete and versioned.
- Required upstream artifacts must be present and versioned.
- Recommendation ordering must be stable for identical inputs.
- Duplicate Recommendation IDs are not permitted.
- Duplicate canonical advisory action keys are not permitted.
- Decision table version must be `recommendation-decision-table-set-v1`.
- Methodology version must be `business-decision-methodology-v1`.
- Unsupported methodology versions must fail closed.
- Unsupported decision table versions must fail closed.
- Recommendations must consume upstream artifacts only.
- Recommendations must not modify upstream business truth.

## 8. Stable Ordering Rules

Status: `APPROVED`

Recommendation Decision Tables v1 applies the following deterministic ordering
for emitted Recommendation sets:

1. Recommendation taxonomy order:
   `Immediate Action`, `Priority Action`, `Planned Improvement`,
   `Best Practice`, `Monitor`.
2. Assessment-Level Risk order:
   `Critical Risk`, `Elevated Risk`, `Moderate Risk`, `Low Risk`,
   `Minimal / Informational`.
3. Severity order:
   `Critical`, `High`, `Medium`, `Low`, `Informational`.
4. Business Capability Dimension order:
   `Process & Operational Control`,
   `Governance, Compliance & Regulatory Readiness`,
   `Technology & Intelligent Systems Management`,
   `Data, Privacy & Security Controls`,
   `Remediation, Verification & Continuous Improvement`.
5. Lexicographic Finding ID order.
6. Lexicographic Recommendation ID order.

Stable ordering is an output determinism rule. It does not create a
Recommendation priority score, prioritization formula, or workflow priority.

## 9. Duplicate Prevention Rules

Status: `APPROVED`

Recommendation Decision Tables v1 prevents duplicates through deterministic
identity and advisory action keys.

Recommendation ID format:

```text
recommendation::{methodology_version}::{recommendation_decision_table_version}::{source_scope}::{source_identifier}::{recommendation_label}
```

Canonical advisory action key format:

```text
{source_scope}::{source_identifier}::{recommendation_label}
```

Duplicate-prevention requirements:

- Each Recommendation ID must be unique within the Recommendation set.
- Each canonical advisory action key must be unique within the Recommendation
  set.
- Finding-scoped Recommendations must use the source Finding ID as the source
  identifier.
- The no-Findings assessment-scoped Recommendation must use the deterministic
  source identifier `assessment-no-findings`.
- If duplicate Recommendation IDs or duplicate canonical advisory action keys
  are detected, Recommendation output must fail closed.

## 10. Fail-Closed Rules

Status: `APPROVED`

Recommendation generation must fail closed when:

- Finding collection is missing or not deterministically complete.
- A generated Finding is missing Finding Type.
- A generated Finding has an unsupported Finding Type.
- A generated Finding is missing Severity Assignment.
- A generated Finding has an unsupported Severity Assignment.
- Finding Type and Severity combination does not match exactly one approved
  recommendation rule.
- Risk Assessment is missing, malformed, or unsupported.
- Confidence Assessment is missing, malformed, or unsupported.
- Readiness context is missing, malformed, unsupported, or `Incomplete`.
- Evidence Evaluation is missing, malformed, or unsupported.
- Required source references are missing.
- Required methodology versions are missing or unsupported.
- Decision table version is missing or unsupported.
- More than one Recommendation output could be assigned to the same source
  scope and source identifier.
- No Recommendation set can be produced for a complete valid assessment.
- Duplicate Recommendation IDs are detected.
- Duplicate canonical advisory action keys are detected.
- Rule inputs are malformed, incomplete, ambiguous, or conflicting.

Fail-closed Recommendation generation means no Recommendation set is emitted.
It does not create a partial Recommendation set and does not modify scores,
Readiness, Evidence Evaluation, Findings, Severity, Risk, Confidence, or
Executive Summary output.

## 11. Version Identity

Status: `APPROVED`

Recommendation decision table artifact version:

```text
recommendation-decision-tables-v1
```

Recommendation decision table set version:

```text
recommendation-decision-table-set-v1
```

Recommendation taxonomy version:

```text
recommendation-taxonomy-v1
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

Confidence decision table set version:

```text
confidence-decision-table-set-v1
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

## 12. Computational Properties

Status: `APPROVED`

Recommendation Decision Tables v1 satisfies:

- Determinism: the same complete set of valid upstream artifacts under the same
  decision table version always produces the same Recommendation set.
- Idempotence: regenerating Recommendations from the same valid inputs under
  the same methodology version produces identical Recommendation sets.
- Complete coverage: all approved valid assessment states resolve to a
  deterministic Recommendation set.
- Non-conflict: no valid assessment state matches incompatible Recommendation
  outputs.
- Stable ordering: identical valid inputs produce the same Recommendation
  ordering.
- Duplicate prevention: the Recommendation set does not contain duplicate
  Recommendation IDs or duplicate canonical advisory action keys.
- Traceability: every Recommendation traces to upstream artifacts, decision
  rule, decision table version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions are
  reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Recommendation taxonomy version, Finding methodology
  version, Severity Decision Table version, Risk Decision Table version,
  Confidence Decision Table version, Readiness methodology version, and
  Evidence Evaluation methodology version.
- Deterministic independence: Recommendation generation does not modify
  upstream deterministic business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules prevent Recommendation output.

## 13. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every complete assessment resolves to a deterministic Recommendation set. | Pass |
| Stable ordering for identical inputs is defined. | Pass |
| Duplicate Recommendations cannot occur. | Pass |
| No duplicate rule IDs are present. | Pass |
| No conflicting rules are present. | Pass |
| Invalid or incomplete inputs fail closed. | Pass |
| Recommendations consume upstream artifacts only. | Pass |
| Recommendations never modify upstream business truth. | Pass |
| Only approved Recommendation labels are emitted. | Pass |
| Decision table version is defined. | Pass |

## 14. Remaining Implementation Artifacts

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 15. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE RECOMMENDATION DECISION TABLES V1
```

The deterministic Recommendation Decision Tables are approved for
`business-decision-methodology-v1`. They produce a deterministic advisory
Recommendation set for every complete valid assessment and fail closed for
malformed, unsupported, incomplete, ambiguous, or conflicting inputs.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/19-recommendation-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
- `docs/business-decision-methodology/23-risk-decision-tables-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
