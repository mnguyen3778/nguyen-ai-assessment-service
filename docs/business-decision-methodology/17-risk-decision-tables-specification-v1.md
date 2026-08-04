# Risk Decision Tables Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the deterministic structure and governance for Risk
Decision Tables in the Assessment Service.

Risk Decision Tables assign one Assessment-Level Risk output to each complete
assessment by consuming approved upstream Assessment Service artifacts.

The approved Risk taxonomy remains:

- Critical Risk.
- Elevated Risk.
- Moderate Risk.
- Low Risk.
- Minimal / Informational.

This specification does not define actual decision table entries,
implementation algorithms, package contracts, or snapshot contracts.

## 2. Scope

Status: `APPROVED`

In scope:

- Risk Decision Table structure.
- Required decision inputs.
- Required decision outputs.
- Decision table metadata.
- Validation rules.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements.

Out of scope:

- Risk Decision Table rows outside Risk Decision Tables v1.
- Risk assessment implementation algorithms.
- Finding-level risk artifacts.
- Confidence decision tables.
- Recommendation decision tables.
- Executive Summary templates or narrative rules.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Architectural Role

Status: `APPROVED`

Risk Decision Tables are the deterministic methodology artifacts that sit
between Severity-Assigned Findings and Risk Assessment.

Approved flow:

```text
Severity-Assigned Findings
  |
Risk Decision Tables
  |
Risk Assessment
  |
Confidence
```

Risk Decision Tables consume the complete collection of Severity-Assigned
Findings and approved context from Readiness and Evidence Evaluation. They
produce one assessment-level Risk Assessment.

Risk Decision Tables do not modify Findings, Severity Assignment, Readiness,
scores, aggregation, or Evidence Evaluation. They do not calculate Confidence,
generate Recommendations, or generate Executive Summary output.

Risk Decision Tables are repository-owned Assessment Service methodology
artifacts. Downstream consumers may consume Risk Assessment but must not
reinterpret risk rules.

## 4. Decision Table Design Principles

Status: `APPROVED`

- Every complete assessment shall resolve to exactly one Assessment-Level Risk.
- Risk Decision Tables shall consume only approved upstream Assessment Service
  artifacts.
- Risk evaluation shall be deterministic.
- Decision rules shall be version-bound.
- Decision tables shall be immutable once approved.
- Invalid or incomplete inputs shall fail closed.
- Risk shall never modify Findings, Severity, Readiness, Scores, or Evidence
  Evaluation.
- Risk represents assessment-level synthesis, not finding-level classification.
- Risk Decision Tables shall not embed Confidence, Recommendation, or
  Executive Summary methodology.

## 5. Required Decision Inputs

Status: `APPROVED`

Risk Decision Tables may consume only approved producer outputs and methodology
artifacts, including:

- Complete collection of Severity-Assigned Findings.
- Finding IDs.
- Finding Types.
- Assigned Severity Levels.
- Primary Dimensions.
- Related Dimensions, if present.
- Readiness context.
- Evidence Evaluation as contextual input only, not confidence.
- Approved cross-dimension dependency conditions, if present in approved
  methodology.
- Methodology version.

Risk Decision Tables shall not independently reinterpret Findings. Severity-
Assigned Findings remain the authoritative producer output.

Unsupported, missing, malformed, incomplete, or unversioned required inputs
must fail closed.

## 6. Required Decision Outputs

Status: `APPROVED`

Each valid Risk Decision Table evaluation must produce exactly one
Assessment-Level Risk output for one complete assessment.

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
- Triggering decision rule reference.
- Decision table ID.
- Decision table version.
- Methodology version.
- Severity-Assigned Finding references.
- Readiness references.
- Evidence Evaluation references.
- Risk rationale.

Risk Assessment is a downstream assessment artifact. It does not modify any
upstream deterministic business truth.

## 7. Decision Table Metadata

Status: `APPROVED`

Each approved Risk Decision Table must include:

- Decision table ID.
- Decision table version.
- Methodology version.
- Risk taxonomy version.
- Severity Decision Table version.
- Finding methodology version.
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
- Validation status.
- Retirement status, if superseded.

Each decision rule must include:

- Rule ID.
- Required input conditions.
- Assessment-Level Risk output.
- Rule rationale.
- Source methodology references.
- Traceability requirements.

This specification does not approve actual decision rule rows.

## 8. Validation Rules

Status: `APPROVED`

Risk Decision Table validation must fail closed.

Required validation rules:

- Every approved Risk Decision Table must reference a valid methodology
  version.
- Every approved Risk Decision Table must reference the approved Risk taxonomy.
- Every approved Risk Decision Table must reference approved upstream
  methodology versions for Findings, Severity Assignment, Readiness, and
  Evidence Evaluation.
- Every complete valid assessment in production scope must resolve to exactly
  one Assessment-Level Risk output.
- No complete valid assessment may resolve to more than one Assessment-Level
  Risk output.
- No conflicting rules are permitted.
- Rule precedence must be explicit if precedence is required.
- No unreachable rule rows are permitted.
- No unsupported Risk outputs are permitted.
- Required input fields must be complete and versioned.
- Decision outputs must preserve traceability to Severity-Assigned Findings,
  Readiness, Evidence Evaluation, decision table version, and methodology
  version.
- Unsupported decision table versions must fail closed.
- Unsupported methodology versions must fail closed.
- Missing, malformed, incomplete, or conflicting inputs must fail closed.

This specification does not define the implementation mechanism for validation.

## 9. Computational Properties

Status: `APPROVED`

Risk Decision Tables must satisfy:

- Determinism: the same complete set of valid Severity-Assigned Findings and
  approved context under the same decision table version must always produce
  the same Risk Assessment.
- Idempotence: re-evaluating Risk from the same valid inputs under the same
  methodology version must produce identical Risk Assessment.
- Single output: each complete valid assessment must receive exactly one
  Assessment-Level Risk output.
- Complete coverage: all approved production input scenarios must resolve to a
  deterministic Risk output.
- Non-conflict: no valid input scenario may match multiple incompatible Risk
  outputs.
- Traceability: every Risk Assessment must trace to Severity-Assigned
  Findings, Readiness, Evidence Evaluation, decision rule, decision table
  version, and methodology version.
- Auditability: decision rules, rationale, inputs, outputs, and versions must
  be reviewable.
- Version binding: decision rules are bound to decision table version,
  methodology version, Risk taxonomy version, Severity Decision Table version,
  Finding methodology version, Readiness methodology version, and Evidence
  Evaluation methodology version.
- Risk Independence: Risk evaluation must not modify upstream deterministic
  business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting decision inputs or rules must prevent Risk Assessment.

## 10. Governance

Status: `APPROVED`

Risk Decision Tables are repository-owned Assessment Service methodology
artifacts.

Governance requirements:

- Actual decision table rows must be approved before production-authoritative
  Risk Assessment is implemented.
- Risk Decision Tables must be reviewed against Risk Methodology.
- Risk Decision Tables must be reviewed against Severity Assignment
  Methodology.
- Risk Decision Tables must be reviewed against Finding Methodology.
- Risk Decision Tables must be reviewed against Readiness Methodology.
- Risk Decision Tables must be reviewed against Evidence Evaluation
  Methodology.
- Risk Decision Tables must preserve deterministic business truth and
  explainability.
- Risk Decision Tables must be immutable once approved for a version.
- Each change must include documented rationale.
- Tables must never be changed to influence individual assessment outcomes,
  customer outcomes, confidence distributions, recommendation outcomes, or
  sales conclusions.
- Downstream consumers must consume Risk Assessment and must not reinterpret
  Risk Decision Tables.

## 11. Versioning

Status: `APPROVED`

Risk decision tables specification identity:

```text
risk-decision-tables-specification-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

Each approved Risk Decision Table must have a stable decision table version.

A new Risk Decision Table version is required if:

- A decision rule is added.
- A decision rule is removed.
- A decision input changes.
- A Risk output changes.
- Rule rationale changes in a way that changes methodology meaning.
- Risk taxonomy version changes.
- Severity Decision Table version changes.
- Finding methodology version changes.
- Readiness methodology version changes.
- Evidence Evaluation methodology version changes.
- Golden Fixture expected outputs would change.

## 12. Production Readiness Requirements

Status: `METHODOLOGY_PENDING`

This specification approves the deterministic structure and governance for Risk
Decision Tables. Risk Decision Tables v1 approves the actual deterministic Risk
Decision Table rows.

Required before production-authoritative Risk Assessment:

- Approved decision rules covering all production input scenarios.
- Approved rule rationale for every decision rule.
- Validation confirming complete production input coverage.
- Validation confirming no conflicting rules.
- Validation confirming every complete valid assessment resolves to exactly one
  Assessment-Level Risk output.
- Validation confirming invalid or incomplete inputs fail closed.
- Validation confirming traceability to Severity-Assigned Findings, Readiness,
  Evidence Evaluation, decision table version, and methodology version.
- Golden Fixture artifacts containing expected Risk Assessment.
- Regression validation for Golden Fixtures.
- Release documentation stating which Risk outputs are production-authoritative.

## 13. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications and artifacts remain required:

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE RISK DECISION TABLE STRUCTURE AND GOVERNANCE
```

Risk Decision Tables shall be the authoritative deterministic mechanism for
assigning one Assessment-Level Risk output to each complete valid assessment.
This specification approves decision table structure, inputs, outputs,
metadata, validation rules, computational properties, governance, and
versioning only.

Risk Decision Table rows are approved by Risk Decision Tables v1.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/16-severity-decision-tables-specification-v1.md`
- `docs/business-decision-methodology/23-risk-decision-tables-v1.md`
- `docs/business-decision-methodology/15-readiness-threshold-specification-v1.md`
- `docs/business-decision-methodology/03-evidence-catalog.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
