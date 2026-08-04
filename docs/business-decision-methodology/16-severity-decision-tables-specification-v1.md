# Severity Decision Tables Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the deterministic structure and governance for
Severity Decision Tables in the Assessment Service.

Severity Decision Tables assign one approved Severity Level to each generated
Finding by consuming approved upstream Assessment Service artifacts.

The approved Severity taxonomy remains:

- Critical.
- High.
- Medium.
- Low.
- Informational.

This specification does not define actual decision table entries,
implementation algorithms, package contracts, or snapshot contracts.

## 2. Scope

Status: `APPROVED`

In scope:

- Severity Decision Table structure.
- Required decision inputs.
- Required decision outputs.
- Decision table metadata.
- Validation rules.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements.

Out of scope:

- Actual decision table rows.
- Severity assignment implementation algorithms.
- Risk decision tables.
- Confidence decision tables.
- Recommendation decision tables.
- Executive Summary templates or narrative rules.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Architectural Role

Status: `APPROVED`

Severity Decision Tables are the deterministic methodology artifacts that sit
between generated Findings and Severity Assignment.

Approved flow:

```text
Findings
  |
Severity Decision Tables
  |
Severity Assignment
  |
Risk
```

Severity Decision Tables consume generated Findings and approved context from
Readiness and Evidence Evaluation. They produce Severity Assignment as an
independent attribute of an existing Finding.

Severity Decision Tables do not create Findings, modify Findings, calculate
Risk, calculate Confidence, generate Recommendations, or generate Executive
Summary output.

Severity Decision Tables are repository-owned Assessment Service methodology
artifacts. Downstream consumers may consume Severity Assignment but must not
reinterpret severity rules.

## 4. Decision Table Design Principles

Status: `APPROVED`

- Every Finding shall resolve to exactly one Severity Level.
- Severity Decision Tables shall consume only approved upstream Assessment
  Service artifacts.
- Severity Decision Tables shall be deterministic.
- Decision rules shall be version-bound.
- Decision tables shall be immutable once approved.
- Invalid or incomplete inputs shall fail closed.
- Severity expresses consequence, not confidence.
- Severity assignment shall not modify Finding identity, Finding type, Finding
  content, scores, aggregation, readiness, Evidence Evaluation, Risk,
  Confidence, Recommendations, or Executive Summary output.
- Severity Decision Tables shall not embed Risk, Confidence, Recommendation,
  or Executive Summary methodology.

## 5. Required Decision Inputs

Status: `APPROVED`

Severity Decision Tables may consume only approved producer outputs and
methodology artifacts, including:

- Finding ID.
- Finding Type.
- Finding characteristics.
- Primary Dimension.
- Related Dimensions, if present.
- Trigger Source.
- Source references.
- Readiness context.
- Business consequence.
- Evidence Availability.
- Evidence Quality.
- Methodology version.

No input has implicit precedence unless explicitly defined by an approved
Severity Decision Table artifact.

Unsupported, missing, malformed, or unversioned required inputs must fail
closed.

## 6. Required Decision Outputs

Status: `APPROVED`

Each valid Severity Decision Table evaluation must produce exactly one
Severity Assignment for one Finding.

Required output:

- Severity Level, one of:
  - Critical.
  - High.
  - Medium.
  - Low.
  - Informational.

Required output traceability:

- Finding ID.
- Assigned Severity Level.
- Triggering decision rule reference.
- Decision table ID.
- Decision table version.
- Methodology version.
- Input artifact references.
- Severity rationale.

Severity Assignment is an independent attribute of an existing Finding. It
does not modify the Finding or any upstream deterministic business truth.

## 7. Decision Table Metadata

Status: `APPROVED`

Each approved Severity Decision Table must include:

- Decision table ID.
- Decision table version.
- Methodology version.
- Severity taxonomy version.
- Finding methodology version.
- Evidence Evaluation methodology version.
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
- Severity output.
- Rule rationale.
- Source methodology references.
- Traceability requirements.

This specification does not approve actual decision rule rows.

## 8. Validation Rules

Status: `APPROVED`

Severity Decision Table validation must fail closed.

Required validation rules:

- Every approved Severity Decision Table must reference a valid methodology
  version.
- Every approved Severity Decision Table must reference the approved Severity
  taxonomy.
- Every approved Severity Decision Table must reference approved upstream
  methodology versions for Findings, Readiness, and Evidence Evaluation.
- Every valid input scenario in production scope must resolve to exactly one
  Severity Level.
- No valid input scenario may resolve to more than one Severity Level.
- No conflicting rules are permitted.
- Rule precedence must be explicit if precedence is required.
- No unreachable rule rows are permitted.
- No unsupported Severity Levels are permitted.
- Required input fields must be complete and versioned.
- Decision outputs must preserve traceability to the Finding, decision rule,
  decision table version, and methodology version.
- Unsupported decision table versions must fail closed.
- Unsupported methodology versions must fail closed.
- Missing, malformed, incomplete, or conflicting inputs must fail closed.

This specification does not define the implementation mechanism for
validation.

## 9. Computational Properties

Status: `APPROVED`

Severity Decision Tables must satisfy:

- Determinism: the same valid Finding and approved context under the same
  decision table version must always produce the same Severity Level.
- Idempotence: reassigning Severity from the same valid inputs under the same
  methodology version must produce identical Severity Assignment.
- Single output: each valid Finding must receive exactly one Severity Level.
- Complete coverage: all approved production input scenarios must resolve to a
  deterministic Severity output.
- Non-conflict: no valid input scenario may match multiple incompatible
  Severity outputs.
- Traceability: every Severity Assignment must trace to the Finding, source
  inputs, decision rule, decision table version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions must
  be reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Severity taxonomy version, Finding methodology version,
  Readiness methodology version, and Evidence Evaluation methodology version.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules must prevent Severity Assignment.

## 10. Governance

Status: `APPROVED`

Severity Decision Tables are repository-owned Assessment Service methodology
artifacts.

Governance requirements:

- Actual decision table rows must be approved before
  production-authoritative Severity Assignment is implemented.
- Severity Decision Tables must be reviewed against Severity Methodology.
- Severity Decision Tables must be reviewed against Finding Methodology.
- Severity Decision Tables must be reviewed against Readiness Methodology.
- Severity Decision Tables must be reviewed against Evidence Evaluation
  Methodology.
- Severity Decision Tables must preserve deterministic business truth and
  explainability.
- Severity Decision Tables must be immutable once approved for a version.
- Each change must include documented rationale.
- Tables must never be changed to influence individual assessment outcomes,
  customer outcomes, risk distributions, confidence distributions,
  recommendation outcomes, or sales conclusions.
- Downstream consumers must consume Severity Assignment and must not
  reinterpret Severity Decision Tables.

## 11. Versioning

Status: `APPROVED`

Severity decision tables specification identity:

```text
severity-decision-tables-specification-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

Each approved Severity Decision Table must have a stable decision table
version.

A new Severity Decision Table version is required if:

- A decision rule is added.
- A decision rule is removed.
- A decision input changes.
- A Severity output changes.
- Rule rationale changes in a way that changes methodology meaning.
- Severity taxonomy version changes.
- Finding methodology version changes.
- Readiness methodology version changes.
- Evidence Evaluation methodology version changes.
- Golden Fixture expected outputs would change.

## 12. Production Readiness Requirements

Status: `METHODOLOGY_PENDING`

This specification approves the deterministic structure and governance for
Severity Decision Tables. Severity Decision Tables v1 approves the actual
deterministic Severity Decision Table rows.

Required before production-authoritative Severity Assignment:

- Approved decision rules covering all production input scenarios.
- Approved rule rationale for every decision rule.
- Validation confirming complete production input coverage.
- Validation confirming no conflicting rules.
- Validation confirming every valid input resolves to exactly one Severity
  Level.
- Validation confirming invalid or incomplete inputs fail closed.
- Validation confirming traceability to Findings, Readiness, Evidence
  Evaluation, decision table version, and methodology version.
- Golden Fixture artifacts containing expected Severity Assignment.
- Regression validation for Golden Fixtures.
- Release documentation stating which Severity outputs are
  production-authoritative.

## 13. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications and artifacts remain required:

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE SEVERITY DECISION TABLE STRUCTURE AND GOVERNANCE
```

Severity Decision Tables shall be the authoritative deterministic mechanism
for assigning one approved Severity Level to each generated Finding. This
specification approves decision table structure, inputs, outputs, metadata,
validation rules, computational properties, governance, and versioning only.

Severity Decision Table rows are approved by Severity Decision Tables v1.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/15-readiness-threshold-specification-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
