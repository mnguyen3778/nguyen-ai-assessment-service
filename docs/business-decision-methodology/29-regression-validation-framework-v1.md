# Regression Validation Framework v1

## 1. Purpose

Status: `APPROVED`

This document defines the repository-owned Regression Validation Framework for
`business-decision-methodology-v1`.

Regression Validation Framework v1 governs how future Assessment Service
implementations are validated against approved Golden Fixture Payloads v1. It
defines validation philosophy, scope, categories, execution rules, expected
outcomes, failure classification, pass/fail criteria, metadata, version
binding, computational properties, and production-authority relationships.

This document does not create runtime test code, unit tests, automation
scripts, CI/CD configuration, implementation logic, production logic, package
contracts, or snapshot contracts.

## 2. Validation Philosophy

Status: `APPROVED`

Regression validation exists to prove that a future implementation of Executive
Assessment Rubric v1 reproduces the approved deterministic business truth
defined by repository-owned methodology artifacts.

Validation philosophy:

- Golden Fixture Payloads v1 provide immutable expected outputs.
- Regression validation compares actual implementation outputs to those
  immutable expected outputs.
- Validation is deterministic, reproducible, auditable, and version-bound.
- Validation never creates, modifies, reinterprets, or overrides business
  truth.
- Validation failures prevent production authority until resolved by approved
  methodology correction, fixture correction, or implementation correction.
- Validation does not grant production authority by itself; it provides
  required evidence for production authority.

## 3. Validation Scope

Status: `APPROVED`

Regression Validation Framework v1 applies only to Assessment Service
producer-owned methodology outputs.

In scope:

- Question scoring.
- Dimension scoring.
- Weighted aggregation.
- Overall Assessment Result.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity Assignment.
- Assessment-Level Risk.
- Confidence Assessment.
- Recommendations.
- Executive Summary references.
- Source references.
- Rule references.
- Methodology and artifact version references.
- Fail-closed behavior for invalid, incomplete, unsupported, or
  version-mismatched fixture inputs.

Out of scope:

- Runtime test implementation.
- Unit test code.
- CI/CD configuration.
- Automation scripts.
- API behavior.
- Lambda handler behavior.
- Persistence.
- Transport.
- Package contract changes.
- Snapshot contract changes.
- Consumer-side compatibility validation.
- Executive Intelligence Platform behavior.
- Website, Client Portal, or AI Knowledge Assistant behavior.

## 4. Regression Categories

Status: `APPROVED`

Regression validation must cover the complete deterministic assessment
pipeline represented by Golden Fixture Payloads v1.

Approved regression categories:

| Category | Validation Purpose |
| --- | --- |
| Scoring regression | Confirms question scores match approved expected scores for every canonical question in each fixture. |
| Dimension regression | Confirms dimension results match approved expected dimension outputs. |
| Aggregation regression | Confirms weighted assessment result and Overall Assessment Result match approved expected outputs. |
| Readiness regression | Confirms readiness assignment matches approved expected readiness. |
| Evidence regression | Confirms Evidence Evaluation output matches approved expected evidence-derived output. |
| Finding regression | Confirms generated Findings match approved expected Finding collection. |
| Severity regression | Confirms Severity Assignment matches approved expected Severity for every generated Finding. |
| Risk regression | Confirms Assessment-Level Risk matches approved expected Risk. |
| Confidence regression | Confirms Confidence Assessment matches approved expected Confidence. |
| Recommendation regression | Confirms Recommendation set and stable ordering match approved expected Recommendations. |
| Executive Summary regression | Confirms Executive Summary references match approved template section references. |
| Traceability regression | Confirms source references, rule references, and methodology references match approved expected metadata. |
| Fail-closed regression | Confirms invalid, incomplete, unsupported, or version-mismatched fixtures produce no partial downstream business output. |

## 5. Golden Fixture Execution Rules

Status: `APPROVED`

Golden Fixture execution under this framework is validation governance only.
This document does not define implementation code for execution.

Execution rules:

- Every approved Golden Fixture Payload must be executable in a deterministic
  manner by a future validation implementation.
- Fixture execution must use the fixture input profile exactly as approved.
- Fixture execution must use the methodology version and artifact versions
  referenced by the fixture.
- Fixture execution must compare produced outputs to immutable expected
  outputs.
- Fixture execution must not mutate fixture inputs.
- Fixture execution must not mutate fixture expected outputs.
- Fixture execution must not mutate methodology artifacts.
- Fixture execution must not mutate produced business truth.
- Fixture execution must fail closed when required fixture metadata is missing,
  malformed, unsupported, incomplete, or version-mismatched.
- Fixture execution must fail closed when expected outputs are missing,
  malformed, unsupported, incomplete, or inconsistent with approved
  methodology artifacts.

## 6. Expected Validation Outcomes

Status: `APPROVED`

Each regression validation run must produce a deterministic validation outcome.

Approved validation outcomes:

| Outcome | Meaning |
| --- | --- |
| `pass` | Actual output exactly matches approved expected output for the fixture and category. |
| `fail` | Actual output does not match approved expected output for the fixture or category. |
| `fail_closed` | Validation cannot proceed safely because fixture input, metadata, expected output, methodology version, or artifact version is invalid, incomplete, unsupported, or mismatched. |

No partial production authority may be inferred from `fail` or `fail_closed`
outcomes.

## 7. Failure Classification

Status: `APPROVED`

Regression failures must be classified deterministically for review and audit.

Approved failure classifications:

| Failure Classification | Definition |
| --- | --- |
| Fixture input defect | Fixture input is missing, malformed, incomplete, conflicting, or not valid for its fixture category. |
| Expected output defect | Fixture expected output is missing, malformed, incomplete, conflicting, or inconsistent with approved methodology artifacts. |
| Methodology version defect | Fixture, implementation output, or validation metadata references an unsupported or mismatched methodology version. |
| Artifact version defect | Fixture, implementation output, or validation metadata references an unsupported or mismatched methodology artifact version. |
| Output mismatch | Actual implementation output differs from approved expected output. |
| Traceability mismatch | Actual source references, rule references, methodology references, or artifact references differ from approved expected metadata. |
| Ordering mismatch | Actual ordered output differs from approved deterministic ordering. |
| Partial output defect | A fail-closed fixture produces partial downstream business output. |
| Mutation defect | Validation mutates fixture inputs, expected outputs, methodology artifacts, or produced business truth. |

Failure classification is an audit label only. It does not alter methodology,
expected outputs, implementation outputs, or production authority.

## 8. Pass/Fail Criteria

Status: `APPROVED`

Pass/fail criteria are deterministic.

A fixture passes only when:

- The fixture ID is approved.
- The fixture metadata is complete and valid.
- The methodology version is supported and matches the fixture.
- All referenced artifact versions are supported and match the fixture.
- Every required actual output is present for complete-valid fixtures.
- Every actual output exactly matches the approved expected output.
- Expected output ordering is preserved where ordering is defined.
- Source references match approved expected source references.
- Rule references match approved expected rule references.
- No fixture input, expected output, methodology artifact, or produced business
  truth is mutated.

A fixture fails when:

- Actual output differs from approved expected output.
- Actual output ordering differs from approved deterministic ordering.
- Actual references differ from approved expected references.
- A complete-valid fixture omits a required output.
- A fail-closed fixture produces partial downstream business output.

A fixture fails closed when:

- Fixture ID is missing or unsupported.
- Fixture metadata is missing, malformed, incomplete, or conflicting.
- Methodology version is missing, unsupported, or mismatched.
- Required artifact version is missing, unsupported, or mismatched.
- Expected outputs are missing, malformed, incomplete, or inconsistent with
  approved methodology artifacts.
- Validation cannot determine a deterministic comparison.

## 9. Regression Metadata

Status: `APPROVED`

Every regression validation record must include metadata sufficient for
traceability, auditability, and reproducibility.

Required regression metadata:

- Validation run ID.
- Validation framework version.
- Fixture ID.
- Fixture version.
- Fixture category.
- Methodology version.
- Scoring scale version.
- Question scoring table version.
- Dimension weight set version.
- Readiness threshold version.
- Severity decision table version.
- Risk decision table version.
- Confidence decision table version.
- Recommendation decision table version.
- Executive Summary template version.
- Expected output reference.
- Actual output reference.
- Validation outcome.
- Failure classification, when applicable.
- Validation timestamp or equivalent deterministic run record metadata.
- Repository reference or equivalent implementation provenance identifier.

Regression metadata is validation evidence only. It does not modify business
truth or methodology.

## 10. Version Binding

Status: `APPROVED`

Regression validation framework version:

```text
regression-validation-framework-v1
```

Golden Fixture payload artifact version:

```text
golden-fixture-payloads-v1
```

Golden Fixture catalog version:

```text
golden-fixture-catalog-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

Required artifact versions:

- `scoring-scale-v1`
- `question-scoring-tables-v1`
- `official-dimension-weight-set-v1`
- `readiness-threshold-values-v1`
- `severity-decision-table-set-v1`
- `risk-decision-table-set-v1`
- `confidence-decision-table-set-v1`
- `recommendation-decision-table-set-v1`
- `executive-summary-template-set-v1`

Unsupported or mismatched framework, fixture, methodology, or artifact versions
must fail closed.

## 11. Computational Properties

Status: `APPROVED`

Regression Validation Framework v1 satisfies:

- Determinism: the same fixture input, methodology version, artifact versions,
  and implementation output produce the same validation outcome.
- Reproducibility: validation can be repeated under the same versions with the
  same outcome.
- Auditability: validation records identify fixture, expected output, actual
  output, version references, outcome, and failure classification.
- Traceability: validation preserves references between fixture payloads,
  methodology artifacts, implementation outputs, and validation outcomes.
- Explainability: pass, fail, and fail-closed outcomes identify the comparison
  basis and failure classification when applicable.
- Immutable expected outputs: validation compares against approved expected
  outputs without modifying them.
- Version binding: validation is bound to methodology, fixture, framework, and
  artifact versions.
- Fail-closed behavior: invalid, incomplete, unsupported, or
  version-mismatched validation conditions prevent production authority.
- Independence: regression validation never modifies business truth.

## 12. Production Authority Relationship

Status: `APPROVED`

Regression validation is required evidence for production authority.
Production authority cannot be granted solely by implementation code, runtime
behavior, downstream consumer acceptance, or manual inspection.

Production-authoritative Executive Assessment Rubric v1 requires:

- Approved methodology artifacts.
- Approved deterministic decision tables.
- Approved Golden Fixtures v1 framework and catalog.
- Approved Golden Fixture Payloads v1 expected outputs.
- Approved Regression Validation Framework v1.
- Successful validation against approved Golden Fixture Payloads v1 for the
  emitted production scope.
- Approved Production Authority Release v1.
- Confirmed Assessment Service architecture conformance.
- Confirmed Assessment Service repository ownership.
- Confirmed unchanged cross-repository contracts.
- Release documentation stating which outputs are production-authoritative and
  which remain foundation-only.

Regression Validation Framework v1 defines validation governance. It does not
grant production authority by itself and does not implement validation code.

## 13. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every Golden Fixture is executable in a deterministic manner. | Pass |
| Regression compares actual outputs to immutable expected outputs. | Pass |
| Validation is reproducible. | Pass |
| Pass/fail criteria are deterministic. | Pass |
| Version mismatches fail closed. | Pass |
| No mutation of Golden Fixture payloads occurs during validation. | Pass |
| Regression validation never modifies business truth. | Pass |
| Runtime implementation is not introduced. | Pass |
| Unit test code is not introduced. | Pass |
| CI/CD pipelines are not introduced. | Pass |
| Automation scripts are not introduced. | Pass |
| Consumer-specific behavior is not introduced. | Pass |

## 14. Remaining Implementation Artifacts

Status: `APPROVED`

- No remaining methodology governance artifacts are pending.
- Future implementation remains a separate bounded implementation activity.

## 15. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE REGRESSION VALIDATION FRAMEWORK V1
```

Regression Validation Framework v1 is approved as the repository-owned
validation governance artifact for validating future Assessment Service
implementation outputs against approved Golden Fixture Payloads v1.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/27-golden-fixtures-v1.md`
- `docs/business-decision-methodology/28-golden-fixture-payloads-v1.md`
- `docs/business-decision-methodology/30-production-authority-release-v1.md`
