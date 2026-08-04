# Golden Fixtures v1

## 1. Purpose

Status: `APPROVED`

This document defines the Golden Fixture framework for
`business-decision-methodology-v1`.

Golden Fixtures are repository-owned deterministic validation artifacts. They
define canonical assessment scenarios, required fixture structure, expected
output coverage, regression requirements, and production-authority
relationships for Executive Assessment Rubric v1.

This document does not implement runtime behavior, test code, automation
scripts, package contracts, snapshot contracts, or production logic.

## 2. Golden Fixture Philosophy

Status: `APPROVED`

Golden Fixtures establish immutable expected outputs for deterministic
Assessment Service methodology validation.

Golden Fixture principles:

- Fixtures are repository-owned Assessment Service validation artifacts.
- Fixtures represent canonical assessment scenarios.
- Fixtures contain approved inputs and expected outputs.
- Fixtures are deterministic.
- Fixtures are reproducible under the methodology version and artifact
  versions they reference.
- Fixtures are immutable once approved.
- Fixture execution validates deterministic methodology behavior only.
- Fixture execution never creates, modifies, reinterprets, or overrides
  business truth.
- Any approved fixture change requires methodology version review.
- Invalid, malformed, incomplete, or version-mismatched fixtures fail closed.

## 3. Fixture Categories

Status: `APPROVED`

Golden Fixtures v1 defines the official fixture catalog. Each fixture category
must be capable of validating question scoring, dimension scoring, weighted
aggregation, readiness, findings, severity, risk, confidence, recommendations,
and Executive Summary output.

| Fixture ID | Category | Validation Purpose |
| --- | --- | --- |
| `fixture-v1-complete-minimal-risk` | Complete valid assessment with minimal or informational assessment-level risk. | Validates successful deterministic processing when no defect-based risk dominates the assessment. |
| `fixture-v1-complete-not-ready-readiness` | Complete valid assessment producing Not Ready readiness. | Validates question scoring, dimension scoring, aggregation, and Not Ready readiness assignment. |
| `fixture-v1-complete-developing-readiness` | Complete valid assessment producing Developing readiness. | Validates readiness threshold assignment and downstream artifact generation for developing capability. |
| `fixture-v1-complete-ready-readiness` | Complete valid assessment producing Ready readiness. | Validates readiness threshold assignment and downstream artifact generation for ready capability. |
| `fixture-v1-complete-advanced-readiness` | Complete valid assessment producing Advanced readiness. | Validates readiness threshold assignment and downstream artifact generation for advanced capability. |
| `fixture-v1-critical-finding-risk` | Complete valid assessment with at least one Critical Severity Finding. | Validates Critical Severity, Critical Risk, Recommendation, Confidence, and Executive Summary propagation. |
| `fixture-v1-high-concentration-risk` | Complete valid assessment with two or more High Severity Findings and no Critical Severity Finding. | Validates Elevated Risk assignment and downstream propagation. |
| `fixture-v1-medium-risk` | Complete valid assessment with Medium Severity Findings and no Critical or High Severity Findings. | Validates Moderate Risk assignment and downstream propagation. |
| `fixture-v1-low-risk` | Complete valid assessment with Low Severity Findings and no Critical, High, or Medium Severity Findings. | Validates Low Risk assignment and downstream propagation. |
| `fixture-v1-evidence-basic-confidence` | Complete valid assessment with Basic-only available evidence. | Validates Low Confidence assignment and downstream propagation. |
| `fixture-v1-evidence-strong-confidence` | Complete valid assessment with Strong-only available evidence. | Validates Very High Confidence assignment and downstream propagation. |
| `fixture-v1-evidence-assertability-limitation` | Complete valid assessment with present required evidence and a valid assertability limitation. | Validates Insufficient Confidence assignment and downstream propagation. |
| `fixture-v1-no-findings-recommendation` | Complete valid assessment with no generated Findings. | Validates no-Findings Recommendation rule and Executive Summary empty Finding statement. |
| `fixture-v1-invalid-input-fail-closed` | Invalid or incomplete fixture input. | Validates fail-closed behavior and confirms no partial business output is produced. |
| `fixture-v1-version-mismatch-fail-closed` | Fixture with unsupported or mismatched methodology artifact versions. | Validates version-bound fail-closed behavior. |

The catalog defines required validation scenarios only. This artifact does not
populate full fixture payloads or expected output values for each catalog entry.

## 4. Required Fixture Metadata

Status: `APPROVED`

Each approved Golden Fixture must include:

- Fixture ID.
- Fixture category.
- Fixture version.
- Methodology version.
- Approval status.
- Effective version.
- Owner.
- Change rationale.
- Source methodology references.
- Fixture input schema version.
- Expected output schema version.
- Scoring scale version.
- Question scoring table version.
- Dimension weight set version.
- Readiness threshold version.
- Severity decision table version.
- Risk decision table version.
- Confidence decision table version.
- Recommendation decision table version.
- Executive Summary template version.
- Expected output checksum or equivalent deterministic integrity reference.
- Validation status.
- Retirement status, if superseded.

## 5. Required Inputs

Status: `APPROVED`

Each Golden Fixture must include canonical assessment inputs sufficient to
exercise the complete deterministic methodology pipeline.

Required fixture inputs:

- Canonical assessment question responses.
- Canonical question IDs.
- Question scoring table references.
- Business Capability Dimension mappings.
- Required evidence availability inputs.
- Required evidence quality inputs.
- Evidence source references.
- Expected Finding trigger inputs.
- Expected Finding Type inputs.
- Expected business consequence basis inputs.
- Methodology version.
- Required methodology artifact versions.

Input constraints:

- Every fixture input must be valid for its fixture category unless the fixture
  category is explicitly fail-closed.
- Every complete-valid fixture must include responses for all 48 canonical
  assessment questions.
- Every complete-valid fixture must include evidence inputs required by the
  fixture category.
- Every complete-valid fixture must reference all approved Business Capability
  Dimensions.
- Fail-closed fixtures must explicitly identify the malformed, missing,
  incomplete, or unsupported input condition being validated.

## 6. Expected Outputs

Status: `APPROVED`

Each complete-valid Golden Fixture must define expected outputs for the full
deterministic assessment pipeline.

Required expected outputs:

- Question scores for every canonical question.
- Dimension results for every approved Business Capability Dimension.
- Weighted aggregation result.
- Overall Assessment Result.
- Readiness assignment.
- Evidence Evaluation output.
- Finding collection.
- Severity Assignment for every generated Finding.
- Assessment-Level Risk.
- Confidence Assessment.
- Recommendation set.
- Executive Summary output.
- Source reference map.
- Rule reference map.
- Methodology version references.
- Artifact version references.

Each fail-closed Golden Fixture must define:

- Invalid condition being validated.
- Expected fail-closed stage.
- Expected absence of partial downstream output.
- Expected validation error category.
- Expected methodology and artifact version references.

Expected outputs are immutable once approved. Any expected-output change
requires methodology version review.

## 7. Validation Rules

Status: `APPROVED`

Golden Fixture validation must fail closed.

Required validation rules:

- Every fixture must reference `business-decision-methodology-v1`.
- Every fixture must reference approved methodology artifact versions.
- Every complete-valid fixture must contain all required inputs.
- Every complete-valid fixture must define all required expected outputs.
- Every fail-closed fixture must identify exactly one primary invalid
  condition.
- Expected outputs must be deterministic and reproducible.
- Expected outputs must be immutable once approved.
- Expected outputs must trace to fixture inputs and methodology artifacts.
- Unsupported fixture versions must fail closed.
- Unsupported methodology versions must fail closed.
- Missing, malformed, incomplete, or conflicting fixture metadata must fail
  closed.
- Fixture execution must never modify input artifacts, expected outputs, or
  produced business truth.

## 8. Regression Requirements

Status: `APPROVED`

Golden Fixtures v1 establishes regression requirements. It does not implement
regression tests or automation scripts.

Regression validation must confirm:

- Identical fixture inputs under the same methodology and artifact versions
  produce identical outputs.
- Question scores match expected outputs.
- Dimension results match expected outputs.
- Weighted aggregation matches expected outputs.
- Readiness assignment matches expected outputs.
- Evidence Evaluation output matches expected outputs.
- Findings match expected outputs.
- Severity Assignment matches expected outputs.
- Risk Assessment matches expected outputs.
- Confidence Assessment matches expected outputs.
- Recommendation set and ordering match expected outputs.
- Executive Summary sections and deterministic text match expected outputs.
- Source references and rule references match expected outputs.
- Fail-closed fixtures produce no partial downstream business output.
- Version-mismatched fixtures fail closed.

Regression validation must be version-bound and must preserve fixture
immutability.

## 9. Fail-Closed Rules

Status: `APPROVED`

Golden Fixture validation must fail closed when:

- Fixture ID is missing.
- Fixture category is missing or unsupported.
- Fixture version is missing or unsupported.
- Methodology version is missing or unsupported.
- Required methodology artifact versions are missing or unsupported.
- Required fixture metadata is missing, malformed, incomplete, or conflicting.
- Required fixture inputs are missing for a complete-valid fixture.
- Required expected outputs are missing for a complete-valid fixture.
- A fail-closed fixture identifies no invalid condition.
- A fail-closed fixture identifies more than one primary invalid condition.
- Expected outputs cannot be reproduced deterministically.
- Expected outputs conflict with approved methodology artifacts.
- Fixture execution would require modifying input, expected output, or business
  truth artifacts.

Fail-closed Golden Fixture validation means production authority cannot be
granted from the invalid fixture. It does not create partial validation
authority.

## 10. Version Identity

Status: `APPROVED`

Golden Fixture artifact version:

```text
golden-fixtures-v1
```

Golden Fixture catalog version:

```text
golden-fixture-catalog-v1
```

Expected output schema version:

```text
golden-fixture-expected-output-schema-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

Required methodology artifact versions:

- `scoring-scale-v1`
- `question-scoring-tables-v1`
- `readiness-threshold-values-v1`
- `severity-decision-table-set-v1`
- `risk-decision-table-set-v1`
- `confidence-decision-table-set-v1`
- `recommendation-decision-table-set-v1`
- `executive-summary-template-set-v1`

## 11. Computational Properties

Status: `APPROVED`

Golden Fixtures v1 satisfies:

- Deterministic reproducibility: the same approved inputs under the same
  methodology and artifact versions produce the same expected outputs.
- Regression stability: fixtures detect unintended changes to deterministic
  output behavior.
- Immutability: expected outputs are immutable once approved.
- Version binding: fixtures, inputs, expected outputs, and validation authority
  are bound to methodology and artifact versions.
- Traceability: fixtures preserve references between inputs, methodology
  artifacts, expected outputs, rule references, and validation authority.
- Auditability: fixture inputs, expected outputs, rationale, versions, and
  validation results are reviewable.
- Explainability: fixture expected outputs must identify the methodology basis
  and rule references used to produce them.
- Fail-closed validation: missing, malformed, unsupported, or
  version-mismatched fixture inputs or expected outputs prevent production
  authority.
- Independence: fixture execution never modifies business truth.

## 12. Production Authority Relationship

Status: `APPROVED`

Golden Fixtures are required evidence for production authority. Production
authority cannot be granted solely by implementation code, runtime behavior,
downstream consumer acceptance, or manual inspection.

Production-authoritative Executive Assessment Rubric v1 requires:

- Approved methodology artifacts.
- Approved deterministic decision tables.
- Approved Golden Fixture catalog.
- Approved Golden Fixture Payloads v1 expected outputs for the fixture catalog
  entries required by the emitted production scope.
- Approved Regression Validation Framework v1.
- Regression validation against approved Golden Fixtures.
- Approved Production Authority Release v1.
- Confirmed Assessment Service architecture conformance.
- Confirmed Assessment Service repository ownership.
- Confirmed unchanged cross-repository contracts.
- Release documentation stating which outputs are production-authoritative and
  which remain foundation-only.

Golden Fixtures and Golden Fixture Payloads v1 define fixture authority.
Regression Validation Framework v1 defines validation governance. Production
Authority Release v1 records methodology governance completion.

## 13. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every fixture is deterministic. | Pass |
| Expected outputs are immutable once approved. | Pass |
| Fixtures are version-bound. | Pass |
| Fixtures are reproducible. | Pass |
| Fixtures support regression testing. | Pass |
| Invalid fixtures fail closed. | Pass |
| Fixture execution never modifies business truth. | Pass |
| Fixture catalog covers the complete deterministic methodology pipeline. | Pass |
| No runtime implementation is introduced. | Pass |
| No test automation is introduced. | Pass |

## 14. Remaining Implementation Artifacts

Status: `APPROVED`

- No remaining methodology governance artifacts are pending.
- Future implementation remains a separate bounded implementation activity.

## 15. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE GOLDEN FIXTURES V1 FRAMEWORK
```

Golden Fixtures v1 is approved as the repository-owned deterministic
validation framework for `business-decision-methodology-v1`. It defines the
official fixture catalog, required metadata, required inputs, expected output
structure, validation rules, regression requirements, fail-closed behavior,
version identity, and production-authority relationship.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/28-golden-fixture-payloads-v1.md`
- `docs/business-decision-methodology/29-regression-validation-framework-v1.md`
- `docs/business-decision-methodology/30-production-authority-release-v1.md`
- `docs/business-decision-methodology/20-question-scoring-tables-v1.md`
- `docs/business-decision-methodology/21-readiness-threshold-values-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
- `docs/business-decision-methodology/23-risk-decision-tables-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
- `docs/business-decision-methodology/25-recommendation-decision-tables-v1.md`
- `docs/business-decision-methodology/26-executive-summary-templates-v1.md`
