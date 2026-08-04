# Readiness Threshold Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the deterministic readiness threshold framework for
converting normalized assessment results into the approved readiness taxonomy
in the Assessment Service.

The approved readiness taxonomy remains:

- Not Ready.
- Developing.
- Ready.
- Advanced.

The operational processing state remains:

- Incomplete.

Incomplete is not a readiness level. It indicates that readiness cannot be
assigned because one or more required inputs are unavailable or invalid under
the approved fail-closed methodology.

This specification does not select numeric threshold values, boundary numbers,
readiness decision tables, implementation algorithms, package contracts, or
snapshot contracts.

## 2. Scope

Status: `APPROVED`

In scope:

- Readiness threshold framework.
- Threshold range structure.
- Boundary convention framework.
- Threshold metadata.
- Validation rules.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements.

Out of scope:

- Numeric threshold values.
- Boundary numbers.
- Final boundary inclusion convention.
- Readiness decision tables.
- Risk, Confidence, Recommendation, or Executive Summary decision tables.
- Implementation algorithms.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Architectural Role

Status: `APPROVED`

Readiness Thresholds are the deterministic methodology artifacts that interpret
approved dimension results and the approved overall assessment result into
readiness assignments.

Approved flow:

```text
Question Scores
  |
Dimension Results
  |
Aggregation
  |
Overall Assessment Result
  |
Readiness Threshold Specification
  |
Readiness Assignment
```

Readiness Thresholds operate only on validated numeric results using the
approved 0-to-100 scoring scale. They do not recalculate question scores,
dimension results, aggregation, findings, severity, risk, confidence,
recommendations, or executive summaries.

Readiness Thresholds are repository-owned Assessment Service methodology
artifacts. Downstream consumers may consume readiness assignments but must not
reinterpret threshold ranges.

## 4. Threshold Design Principles

Status: `APPROVED`

- Every readiness level shall have one deterministic threshold range.
- Thresholds shall operate on the approved 0-to-100 scoring scale.
- Thresholds shall be mutually exclusive.
- Thresholds shall collectively cover the full 0-to-100 scoring range.
- Threshold evaluation shall be deterministic.
- Boundary behavior shall be explicitly versioned.
- Thresholds are immutable once approved.
- Thresholds shall support both dimension-level readiness and overall
  assessment readiness.
- Thresholds shall not encode risk, confidence, recommendation priority, or
  executive summary logic.
- Thresholds shall not be changed to influence individual assessment outcomes,
  customer outcomes, readiness distributions, scoring distributions, or sales
  conclusions.

## 5. Boundary Convention Framework

Status: `APPROVED` for framework. `METHODOLOGY_PENDING` for final boundary
convention.

Boundary convention defines how exact boundary scores are assigned when a
numeric result equals a threshold boundary.

The final boundary convention must define:

- Whether each lower boundary is inclusive or exclusive.
- Whether each upper boundary is inclusive or exclusive.
- How the minimum score is handled.
- How the maximum score is handled.
- How exact boundary values are assigned.
- How boundary behavior is versioned.
- How boundary behavior is represented in Golden Fixtures.

Required boundary framework properties:

- Deterministic: exact boundary scores must always assign to exactly one
  readiness level.
- Complete: every valid score from 0 to 100 inclusive must resolve to one
  readiness level.
- Non-overlapping: no valid score may resolve to more than one readiness
  level.
- Fail-closed: unsupported, ambiguous, missing, or unversioned boundary
  behavior must prevent readiness assignment.

This specification does not approve the final boundary inclusion convention or
any boundary numbers.

## 6. Threshold Metadata

Status: `APPROVED`

Each approved readiness threshold set must include:

- Threshold set ID.
- Threshold set version.
- Methodology version.
- Scoring scale version.
- Readiness taxonomy version.
- Readiness level.
- Threshold lower bound.
- Threshold upper bound.
- Boundary convention version.
- Dimension or overall applicability.
- Approval status.
- Effective version.
- Owner.
- Change rationale.
- Source methodology references.
- Validation status.
- Retirement status, if superseded.

Each readiness assignment must preserve traceability to:

- Source numeric result.
- Result scope: dimension or overall assessment.
- Applied threshold set ID.
- Applied threshold set version.
- Applied boundary convention version.
- Scoring scale version.
- Methodology version.

## 7. Validation Rules

Status: `APPROVED`

Readiness threshold validation must fail closed.

Required validation rules:

- Every approved readiness level must have exactly one active threshold range
  for the applicable threshold set version.
- Threshold ranges must operate within the approved 0-to-100 scoring scale.
- Threshold ranges must collectively cover the full 0-to-100 range.
- Threshold ranges must not overlap.
- Threshold ranges must not leave gaps.
- Boundary handling must be deterministic and versioned.
- Every valid score must resolve to exactly one readiness level.
- Missing or invalid numeric results must produce Incomplete rather than a
  readiness level.
- Unsupported scoring scale versions must fail closed.
- Unsupported threshold set versions must fail closed.
- Unsupported boundary convention versions must fail closed.
- Threshold metadata must preserve traceability to methodology version,
  scoring scale version, and readiness taxonomy version.

This specification does not define the implementation mechanism for
validation.

## 8. Computational Properties

Status: `APPROVED`

Readiness Thresholds must satisfy:

- Determinism: the same valid numeric result under the same threshold set and
  boundary convention versions must always produce the same readiness
  assignment.
- Idempotence: reassigning readiness from the same validated inputs under the
  same methodology version must produce identical readiness assignments.
- Complete coverage: every valid score from 0 to 100 inclusive must resolve to
  one readiness level.
- Mutual exclusivity: no valid score may resolve to more than one readiness
  level.
- Monotonic readiness: increasing a numeric assessment result while holding
  the methodology version constant shall never result in assignment to a lower
  readiness level.
- Traceability: every readiness assignment must trace to source result,
  threshold set, boundary convention, scoring scale, and methodology version.
- Auditability: threshold ranges, boundary behavior, rationale, and versions
  must be reviewable.
- Version binding: threshold ranges and boundary behavior are bound to
  threshold set version, boundary convention version, scoring scale version,
  readiness taxonomy version, and methodology version.
- Fail-closed behavior: missing, malformed, overlapping, incomplete,
  unsupported, or ambiguous threshold definitions must prevent readiness
  assignment.

## 9. Governance

Status: `APPROVED`

Readiness Thresholds are repository-owned Assessment Service methodology
artifacts.

Governance requirements:

- Numeric threshold values must be approved before production-authoritative
  readiness assignment is implemented.
- The final boundary convention must be approved before
  production-authoritative readiness assignment is implemented.
- Thresholds must be reviewed against Scoring Scale Specification v1.
- Thresholds must be reviewed against the approved readiness taxonomy.
- Thresholds must be reviewed against aggregation methodology.
- Thresholds must preserve deterministic business truth and explainability.
- Thresholds must be immutable once approved for a version.
- Each change must include documented rationale.
- Downstream consumers must consume readiness assignments and must not
  reinterpret threshold ranges.

## 10. Versioning

Status: `APPROVED`

Readiness threshold specification identity:

```text
readiness-threshold-specification-v1
```

Approved scoring scale version:

```text
scoring-scale-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

Each approved threshold set must have a stable threshold set version.

Each approved boundary convention must have a stable boundary convention
version.

A new threshold set version is required if:

- A numeric threshold value changes.
- A readiness threshold range changes.
- The readiness taxonomy changes.
- The scoring scale version changes.
- The boundary convention version changes.
- Threshold rationale changes in a way that changes methodology meaning.
- Golden Fixture expected outputs would change.

A new boundary convention version is required if:

- Lower-boundary handling changes.
- Upper-boundary handling changes.
- Exact-boundary assignment changes.
- Minimum or maximum score handling changes.
- Boundary rationale changes in a way that changes methodology meaning.
- Golden Fixture expected outputs would change.

## 11. Production Readiness Requirements

Status: `METHODOLOGY_PENDING`

This specification approves the deterministic readiness threshold framework.
Readiness Threshold Values v1 approves the actual numeric threshold values and
the final boundary convention.

Required before production-authoritative readiness assignment:

- Approved numeric threshold values for all readiness levels.
- Approved final boundary convention.
- Approved threshold set version.
- Approved boundary convention version.
- Validation confirming complete 0-to-100 score coverage.
- Validation confirming no overlapping threshold ranges.
- Validation confirming no threshold gaps.
- Validation confirming every valid score resolves to exactly one readiness
  level.
- Validation confirming invalid or missing results produce Incomplete.
- Golden Fixture artifacts containing expected readiness assignments.
- Regression validation for Golden Fixtures.
- Release documentation stating which readiness outputs are
  production-authoritative.

## 12. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications and artifacts remain required:

- Regression validation implementation.

## 13. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE READINESS THRESHOLD STRUCTURE AND GOVERNANCE
```

Readiness Thresholds shall be the authoritative deterministic mechanism for
mapping normalized dimension results and the overall assessment result to the
approved readiness taxonomy. This specification approves threshold structure,
boundary convention framework, metadata, validation rules, computational
properties, governance, and versioning only.

Actual numeric threshold values and final boundary convention are approved by
Readiness Threshold Values v1.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/13-scoring-scale-specification-v1.md`
- `docs/business-decision-methodology/14-question-scoring-tables-specification-v1.md`
- `docs/business-decision-methodology/21-readiness-threshold-values-v1.md`
- `docs/business-decision-methodology/04-readiness-methodology.md`
- `docs/architecture/assessment-decision-engine-v2.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
