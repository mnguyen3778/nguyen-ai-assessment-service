# Confidence Decision Tables Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the deterministic structure and governance for
Confidence Decision Tables in the Assessment Service.

Confidence Decision Tables assign one Confidence Level to each complete
assessment by consuming approved upstream Assessment Service artifacts.

Confidence represents the degree of certainty that the Assessment Service has
in the business truth it has produced.

The approved Confidence taxonomy labels are:

- Very High Confidence.
- High Confidence.
- Moderate Confidence.
- Low Confidence.
- Insufficient Confidence.

This specification does not define implementation algorithms, confidence
formulas, package contracts, or snapshot contracts. Actual deterministic
decision table rows are approved separately by Confidence Decision Tables v1.

## 2. Scope

Status: `APPROVED`

In scope:

- Confidence Decision Table structure.
- Required decision inputs.
- Required decision outputs.
- Decision table metadata.
- Validation rules.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements.

Out of scope:

- Confidence assignment implementation algorithms.
- Confidence formulas.
- Changes to approved Confidence Decision Tables v1.
- Recommendation decision tables.
- Executive Summary templates or narrative rules.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Architectural Role

Status: `APPROVED`

Confidence Decision Tables are the deterministic methodology artifacts that sit
between approved upstream assessment artifacts and Confidence Assessment.

Approved flow:

```text
Evidence Evaluation
  |
Readiness
  |
Severity-Assigned Findings
  |
Assessment-Level Risk
  |
Confidence Decision Tables
  |
Confidence Assessment
  |
Recommendations
```

Confidence Decision Tables consume approved upstream artifacts and produce one
Confidence Assessment for a complete assessment.

Confidence Decision Tables do not change Question Scores, Dimension Results,
Aggregation, Overall Assessment Result, Readiness, Evidence Evaluation,
Findings, Severity Assignment, Risk Assessment, Recommendations, or Executive
Summary output.

Confidence Decision Tables are repository-owned Assessment Service methodology
artifacts. Downstream consumers may consume Confidence Assessment but must not
reinterpret confidence rules.

## 4. Decision Table Design Principles

Status: `APPROVED`

- Every complete assessment shall resolve to exactly one Confidence Level.
- Confidence Decision Tables shall consume only approved upstream Assessment
  Service artifacts.
- Confidence expresses certainty in the produced business truth.
- Confidence shall never change Scores, Readiness, Findings, Severity, Risk,
  or Recommendations.
- Decision rules shall be deterministic.
- Decision rules shall be version-bound.
- Decision tables shall be immutable once approved.
- Invalid or incomplete inputs shall fail closed.
- Confidence shall remain independent from Readiness, Severity, Risk, and
  Recommendation priority.
- Confidence Decision Tables shall not embed Recommendation or Executive
  Summary methodology.

## 5. Required Decision Inputs

Status: `APPROVED`

Confidence Decision Tables may consume only approved producer outputs and
methodology artifacts, including:

- Evidence Evaluation.
- Evidence Availability.
- Evidence Quality.
- Findings.
- Severity Assignment.
- Risk Assessment.
- Readiness.
- Assessment completeness.
- Answer consistency, when deterministic rules are approved.
- Response quality, when deterministic rules are approved.
- Business certainty, when deterministic rules are approved.
- Methodology version.

Confidence Decision Tables shall not recalculate upstream artifacts or
reinterpret business consequence. Confidence measures certainty, not business
impact.

Unsupported, missing, malformed, incomplete, or unversioned required inputs
must fail closed.

## 6. Required Decision Outputs

Status: `APPROVED`

Each valid Confidence Decision Table evaluation must produce exactly one
Confidence Assessment for one complete assessment.

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
- Triggering decision rule reference.
- Decision table ID.
- Decision table version.
- Methodology version.
- Evidence Evaluation references.
- Finding references.
- Severity Assignment references.
- Risk Assessment references.
- Readiness references.
- Confidence rationale.

Confidence Assessment is a downstream assessment artifact. It does not modify
any upstream deterministic business truth.

## 7. Decision Table Metadata

Status: `APPROVED`

Each approved Confidence Decision Table must include:

- Decision table ID.
- Decision table version.
- Methodology version.
- Confidence taxonomy version.
- Evidence Evaluation methodology version.
- Finding methodology version.
- Severity Decision Table version.
- Risk Decision Table version.
- Readiness methodology version.
- Approval status.
- Effective version.
- Owner.
- Change rationale.
- Source methodology references.
- Complete input schema.
- Complete output schema.
- Rule coverage statement.
- Validation status.
- Retirement status, if superseded.

Each decision rule must include:

- Rule ID.
- Required input conditions.
- Confidence Level output.
- Rule rationale.
- Source methodology references.
- Traceability requirements.

This specification does not approve actual decision rule rows.

## 8. Validation Rules

Status: `APPROVED`

Confidence Decision Table validation must fail closed.

Required validation rules:

- Every approved Confidence Decision Table must reference a valid methodology
  version.
- Every approved Confidence Decision Table must reference the approved
  Confidence taxonomy.
- Every approved Confidence Decision Table must reference approved upstream
  methodology versions for Evidence Evaluation, Findings, Severity Assignment,
  Risk Assessment, and Readiness.
- Every complete valid assessment in production scope must resolve to exactly
  one Confidence Level.
- No complete valid assessment may resolve to more than one Confidence Level.
- No conflicting rules are permitted.
- Rule precedence must be explicit if precedence is required.
- No unreachable rule rows are permitted.
- No unsupported Confidence Levels are permitted.
- Required input fields must be complete and versioned.
- Decision outputs must preserve traceability to upstream inputs, decision
  table version, and methodology version.
- Unsupported decision table versions must fail closed.
- Unsupported methodology versions must fail closed.
- Missing, malformed, incomplete, or conflicting inputs must fail closed.

This specification does not define the implementation mechanism for validation.

## 9. Computational Properties

Status: `APPROVED`

Confidence Decision Tables must satisfy:

- Determinism: the same complete set of valid upstream artifacts under the same
  decision table version must always produce the same Confidence Assessment.
- Idempotence: re-evaluating Confidence from the same valid inputs under the
  same methodology version must produce identical Confidence Assessment.
- Single output: each complete valid assessment must receive exactly one
  Confidence Level.
- Complete coverage: all approved production input scenarios must resolve to a
  deterministic Confidence output.
- Non-conflict: no valid input scenario may match multiple incompatible
  Confidence outputs.
- Traceability: every Confidence Assessment must trace to upstream artifacts,
  decision rule, decision table version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions must
  be reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Confidence taxonomy version, Evidence Evaluation
  methodology version, Finding methodology version, Severity Decision Table
  version, Risk Decision Table version, and Readiness methodology version.
- Deterministic Independence: Confidence evaluation must not modify upstream
  deterministic business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules must prevent Confidence Assessment.

## 10. Governance

Status: `APPROVED`

Confidence Decision Tables are repository-owned Assessment Service methodology
artifacts.

Governance requirements:

- Actual decision table rows must be approved before production-authoritative
  Confidence Assessment is implemented.
- Confidence Decision Tables must be reviewed against Confidence Methodology.
- Confidence Decision Tables must be reviewed against Evidence Evaluation
  Methodology.
- Confidence Decision Tables must be reviewed against Finding Methodology.
- Confidence Decision Tables must be reviewed against Severity Assignment
  Methodology.
- Confidence Decision Tables must be reviewed against Risk Methodology.
- Confidence Decision Tables must be reviewed against Readiness Methodology.
- Confidence Decision Tables must preserve deterministic business truth and
  explainability.
- Confidence Decision Tables must be immutable once approved for a version.
- Each change must include documented rationale.
- Tables must never be changed to influence individual assessment outcomes,
  customer outcomes, recommendation outcomes, readiness distributions, or sales
  conclusions.
- Downstream consumers must consume Confidence Assessment and must not
  reinterpret Confidence Decision Tables.

## 11. Versioning

Status: `APPROVED`

Confidence decision tables specification identity:

```text
confidence-decision-tables-specification-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

Each approved Confidence Decision Table must have a stable decision table
version.

A new Confidence Decision Table version is required if:

- A decision rule is added.
- A decision rule is removed.
- A decision input changes.
- A Confidence Level output changes.
- Rule rationale changes in a way that changes methodology meaning.
- Confidence taxonomy version changes.
- Evidence Evaluation methodology version changes.
- Finding methodology version changes.
- Severity Decision Table version changes.
- Risk Decision Table version changes.
- Readiness methodology version changes.
- Golden Fixture expected outputs would change.

## 12. Production Readiness Requirements

Status: `APPROVED` for Confidence Decision Tables v1 deterministic rows.
`METHODOLOGY_PENDING` for Golden Fixture artifacts, regression validation, and
release documentation required before production-authoritative implementation.

This specification approves the deterministic structure and governance for
Confidence Decision Tables. Confidence Decision Tables v1 approves the
deterministic table rows required for Confidence Assessment.

Required before production-authoritative Confidence Assessment:

- Approved Confidence Decision Tables v1.
- Approved decision rules covering all production input scenarios.
- Approved rule rationale for every decision rule.
- Validation confirming complete production input coverage.
- Validation confirming no conflicting rules.
- Validation confirming every complete valid assessment resolves to exactly one
  Confidence Level.
- Validation confirming invalid or incomplete inputs fail closed.
- Validation confirming traceability to Evidence Evaluation, Findings,
  Severity Assignment, Risk Assessment, Readiness, decision table version, and
  methodology version.
- Golden Fixture artifacts containing expected Confidence Assessment.
- Regression validation for Golden Fixtures.
- Release documentation stating which Confidence outputs are
  production-authoritative.

## 13. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications and artifacts remain required:

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE CONFIDENCE DECISION TABLE STRUCTURE AND GOVERNANCE
```

Confidence Decision Tables shall be the authoritative deterministic mechanism
for assigning one Confidence Level to each complete valid assessment. This
specification approves decision table structure, inputs, outputs, metadata,
validation rules, computational properties, governance, and versioning only.

Deterministic Confidence Decision Table rows are approved by Confidence
Decision Tables v1.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
- `docs/business-decision-methodology/17-risk-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/16-severity-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
