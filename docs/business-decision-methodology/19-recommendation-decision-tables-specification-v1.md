# Recommendation Decision Tables Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the deterministic structure and governance for
Recommendation Decision Tables in the Assessment Service.

Recommendation Decision Tables produce deterministic advisory Recommendation
sets for complete assessments by consuming approved upstream Assessment Service
artifacts.

The approved Recommendation taxonomy labels are:

- Immediate Action.
- Priority Action.
- Planned Improvement.
- Best Practice.
- Monitor.

This specification does not define implementation algorithms, prioritization
formulas, package contracts, or snapshot contracts. Actual deterministic
decision table rows are approved separately by Recommendation Decision Tables
v1.

## 2. Scope

Status: `APPROVED`

In scope:

- Recommendation Decision Table structure.
- Required decision inputs.
- Required decision outputs.
- Decision table metadata.
- Validation rules.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements.

Out of scope:

- Recommendation generation implementation algorithms.
- Recommendation prioritization formulas.
- Priority ordering or priority-scoring rules beyond stable output ordering.
- Changes to approved Recommendation Decision Tables v1.
- Executive Summary templates or narrative rules.
- Workflow execution, remediation ownership, task management, verification
  workflow, closure workflow, or risk acceptance workflow.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Architectural Role

Status: `APPROVED`

Recommendation Decision Tables are the deterministic methodology artifacts that
sit between approved upstream assessment artifacts and Recommendations.

Approved flow:

```text
Confidence Assessment
  |
Assessment-Level Risk
  |
Severity-Assigned Findings
  |
Recommendation Decision Tables
  |
Recommendations
  |
Executive Summary
```

Recommendation Decision Tables consume approved upstream artifacts and produce
a deterministic Recommendation set for a complete assessment.

Recommendation Decision Tables do not change Question Scores, Dimension
Results, Aggregation, Overall Assessment Result, Readiness, Evidence
Evaluation, Findings, Severity Assignment, Risk Assessment, Confidence
Assessment, or Executive Summary output.

Recommendations are advisory outputs only. They must not imply automatic
workflow execution, remediation ownership, task management, verification
workflow, closure workflow, or risk acceptance workflow.

Recommendation Decision Tables are repository-owned Assessment Service
methodology artifacts. Downstream consumers may consume Recommendations but
must not reinterpret recommendation rules.

## 4. Decision Table Design Principles

Status: `APPROVED`

- Every complete assessment shall resolve to a deterministic Recommendation
  set.
- Recommendation Decision Tables shall consume only approved upstream
  Assessment Service artifacts.
- Recommendations are advisory outputs only.
- Recommendations shall never modify Scores, Readiness, Findings, Severity,
  Risk, or Confidence.
- Recommendation rules shall be deterministic.
- Decision rules shall be version-bound.
- Decision tables shall be immutable once approved.
- Invalid or incomplete inputs shall fail closed.
- Recommendation output ordering shall be stable for identical inputs.
- Duplicate Recommendations shall be prevented.
- Recommendation Decision Tables shall not embed Executive Summary methodology.

## 5. Required Decision Inputs

Status: `APPROVED`

Recommendation Decision Tables may consume only approved producer outputs and
methodology artifacts, including:

- Findings.
- Severity Assignment.
- Risk Assessment.
- Confidence Assessment.
- Readiness.
- Evidence Evaluation.
- Source evidence references.
- Assessment completeness, when used by approved upstream Confidence
  Assessment.
- Methodology version.

Recommendations must be derived from the complete assessment context, not from
isolated Findings.

Recommendation Decision Tables shall not recalculate upstream artifacts or
reinterpret business truth.

Unsupported, missing, malformed, incomplete, or unversioned required inputs
must fail closed.

## 6. Required Decision Outputs

Status: `APPROVED`

Each valid Recommendation Decision Table evaluation must produce one
deterministic Recommendation set for one complete assessment.

Each Recommendation must include:

- Recommendation ID.
- Recommendation taxonomy label.
- Recommendation title.
- Recommendation rationale.
- Advisory action statement.
- Source Finding references.
- Source Severity Assignment references.
- Source Risk Assessment references.
- Source Confidence Assessment references.
- Source Readiness references.
- Source Evidence Evaluation references.
- Triggering decision rule reference.
- Decision table ID.
- Decision table version.
- Methodology version.

Recommendation set output must include:

- Stable deterministic ordering metadata.
- Duplicate-prevention validation status.
- Recommendation count.
- Recommendation set rationale.

This specification does not approve priority ordering beyond stable output
ordering, priority-scoring rules, prioritization formulas, or actual
Recommendation output text.

## 7. Decision Table Metadata

Status: `APPROVED`

Each approved Recommendation Decision Table must include:

- Decision table ID.
- Decision table version.
- Methodology version.
- Recommendation taxonomy version.
- Finding methodology version.
- Severity Decision Table version.
- Risk Decision Table version.
- Confidence Decision Table version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Approval status.
- Effective version.
- Owner.
- Change rationale.
- Source methodology references.
- Complete input schema.
- Complete output schema.
- Rule coverage statement.
- Ordering rule reference, if ordering is approved.
- Duplicate-prevention rule reference.
- Validation status.
- Retirement status, if superseded.

Each decision rule must include:

- Rule ID.
- Required input conditions.
- Recommendation output definition.
- Recommendation rationale.
- Source methodology references.
- Traceability requirements.

This specification does not approve actual decision rule rows.

## 8. Validation Rules

Status: `APPROVED`

Recommendation Decision Table validation must fail closed.

Required validation rules:

- Every approved Recommendation Decision Table must reference a valid
  methodology version.
- Every approved Recommendation Decision Table must reference the approved
  Recommendation taxonomy.
- Every approved Recommendation Decision Table must reference approved upstream
  methodology versions for Findings, Severity Assignment, Risk Assessment,
  Confidence Assessment, Readiness, and Evidence Evaluation.
- Every complete valid assessment in production scope must resolve to a
  deterministic Recommendation set.
- No conflicting rules are permitted.
- Rule precedence must be explicit if precedence is required.
- No unreachable rule rows are permitted.
- No unsupported Recommendation taxonomy labels are permitted.
- Required input fields must be complete and versioned.
- Decision outputs must preserve traceability to upstream inputs, decision
  table version, and methodology version.
- Recommendation ordering must be stable for identical inputs.
- Duplicate Recommendations must be prevented.
- Unsupported decision table versions must fail closed.
- Unsupported methodology versions must fail closed.
- Missing, malformed, incomplete, or conflicting inputs must fail closed.

This specification does not define the implementation mechanism for validation.

## 9. Computational Properties

Status: `APPROVED`

Recommendation Decision Tables must satisfy:

- Determinism: the same complete set of valid upstream artifacts under the same
  decision table version must always produce the same Recommendation set.
- Idempotence: regenerating Recommendations from the same valid inputs under
  the same methodology version must produce identical Recommendation sets.
- Complete coverage: all approved production input scenarios must resolve to a
  deterministic Recommendation set.
- Non-conflict: no valid input scenario may match incompatible Recommendation
  outputs.
- Stable ordering: identical valid inputs must produce the same Recommendation
  ordering.
- Duplicate prevention: the Recommendation set must not contain duplicate
  Recommendation IDs or duplicate advisory outputs.
- Traceability: every Recommendation must trace to upstream artifacts,
  decision rule, decision table version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions must
  be reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Recommendation taxonomy version, Finding methodology
  version, Severity Decision Table version, Risk Decision Table version,
  Confidence Decision Table version, Readiness methodology version, and
  Evidence Evaluation methodology version.
- Deterministic Independence: Recommendation generation must not modify
  upstream deterministic business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules must prevent Recommendation output.

## 10. Governance

Status: `APPROVED`

Recommendation Decision Tables are repository-owned Assessment Service
methodology artifacts.

Governance requirements:

- Actual decision table rows must be approved before production-authoritative
  Recommendations are emitted.
- Recommendation Decision Tables must be reviewed against Recommendation
  Methodology.
- Recommendation Decision Tables must be reviewed against Confidence
  Methodology.
- Recommendation Decision Tables must be reviewed against Risk Methodology.
- Recommendation Decision Tables must be reviewed against Severity Assignment
  Methodology.
- Recommendation Decision Tables must be reviewed against Finding Methodology.
- Recommendation Decision Tables must be reviewed against Evidence Evaluation
  Methodology.
- Recommendation Decision Tables must be reviewed against Readiness
  Methodology.
- Recommendation Decision Tables must preserve deterministic business truth and
  explainability.
- Recommendation Decision Tables must be immutable once approved for a version.
- Each change must include documented rationale.
- Tables must never be changed to influence individual assessment outcomes,
  customer outcomes, readiness distributions, risk distributions, confidence
  distributions, sales conclusions, or desired recommendation distributions.
- Downstream consumers must consume Recommendations and must not reinterpret
  Recommendation Decision Tables.

## 11. Versioning

Status: `APPROVED`

Recommendation decision tables specification identity:

```text
recommendation-decision-tables-specification-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

Each approved Recommendation Decision Table must have a stable decision table
version.

A new Recommendation Decision Table version is required if:

- A decision rule is added.
- A decision rule is removed.
- A decision input changes.
- A Recommendation output changes.
- Recommendation ordering semantics change.
- Duplicate-prevention semantics change.
- Rule rationale changes in a way that changes methodology meaning.
- Recommendation taxonomy version changes.
- Finding methodology version changes.
- Severity Decision Table version changes.
- Risk Decision Table version changes.
- Confidence Decision Table version changes.
- Readiness methodology version changes.
- Evidence Evaluation methodology version changes.
- Golden Fixture expected outputs would change.

## 12. Production Readiness Requirements

Status: `APPROVED` for Recommendation Decision Tables v1 deterministic rows,
stable output ordering, and duplicate-prevention rules.
`METHODOLOGY_PENDING` for Golden Fixture artifacts, regression validation, and
release documentation required before production-authoritative implementation.

This specification approves the deterministic structure and governance for
Recommendation Decision Tables. Recommendation Decision Tables v1 approves the
deterministic table rows required for advisory Recommendation output.

Required before production-authoritative Recommendations:

- Approved Recommendation Decision Tables v1.
- Approved decision rules covering all production input scenarios.
- Approved rule rationale for every decision rule.
- Approved stable ordering rules.
- Approved duplicate-prevention rules.
- Approved prioritization rules, if Recommendation priority is emitted.
- Validation confirming complete production input coverage.
- Validation confirming no conflicting rules.
- Validation confirming deterministic Recommendation generation.
- Validation confirming stable ordering for identical inputs.
- Validation confirming duplicate Recommendation prevention.
- Validation confirming invalid or incomplete inputs fail closed.
- Validation confirming traceability to Findings, Severity Assignment, Risk
  Assessment, Confidence Assessment, Readiness, Evidence Evaluation, decision
  table version, and methodology version.
- Golden Fixture artifacts containing expected Recommendations.
- Regression validation for Golden Fixtures.
- Release documentation stating which Recommendation outputs are
  production-authoritative.

## 13. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications and artifacts remain required:

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE RECOMMENDATION DECISION TABLE STRUCTURE AND GOVERNANCE
```

Recommendation Decision Tables shall be the authoritative deterministic
mechanism for producing advisory Recommendation sets from complete valid
assessments. This specification approves decision table structure, inputs,
outputs, metadata, validation rules, computational properties, governance, and
versioning only.

Deterministic Recommendation Decision Table rows are approved by Recommendation
Decision Tables v1.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/25-recommendation-decision-tables-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
- `docs/business-decision-methodology/18-confidence-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/17-risk-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/06-recommendation-priority.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
