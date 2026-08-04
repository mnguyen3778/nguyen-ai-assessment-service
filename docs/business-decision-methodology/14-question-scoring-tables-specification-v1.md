# Question Scoring Tables Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the deterministic structure and governance for
Question Scoring Tables in the Assessment Service.

Question Scoring Tables convert validated allowable canonical question
responses into normalized question scores on the approved 0-to-100 scoring
scale.

This specification does not define actual numeric response mappings for the 48
canonical questions. It does not define readiness thresholds, deterministic
decision tables, implementation algorithms, package contracts, or snapshot
contracts.

## 2. Scope

Status: `APPROVED`

In scope:

- Question Scoring Table structure.
- Allowable response model.
- Response-to-score mapping structure.
- Required scoring table metadata.
- Validation rules.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements.

Out of scope:

- Actual numeric scores for canonical question responses.
- Readiness threshold values.
- Readiness boundary convention.
- Severity, Risk, Confidence, Recommendation, or Executive Summary decision
  tables.
- Golden Fixture artifacts.
- Implementation code.
- Runtime behavior.
- Package or snapshot contract changes.

## 3. Architectural Role

Status: `APPROVED`

Question Scoring Tables are the deterministic methodology artifacts that sit
between validated canonical question responses and normalized question scores.

Approved flow:

```text
Question Response
  |
Question Scoring Table
  |
Question Score (0-to-100)
  |
Dimension Result
  |
Aggregation
  |
Overall Assessment Result
```

Each Question Scoring Table is question-specific. It defines the complete set
of allowable response values for one canonical question and maps each allowable
response to exactly one normalized score on the approved Scoring Scale
Specification v1.

Question Scoring Tables are repository-owned Assessment Service methodology
artifacts. They must not be redefined by downstream consumers.

## 4. Design Principles

Status: `APPROVED`

Every canonical question shall have:

- A unique Question ID.
- Defined allowable responses.
- Deterministic response mappings.
- One normalized score per allowable response.
- Version binding.
- Traceability.
- Auditability.

Additional principles:

- Every allowable response maps to exactly one normalized score.
- Invalid responses fail closed.
- Missing responses are handled according to the approved fail-closed
  methodology.
- Question Scoring Tables are immutable once versioned.
- Question Scoring Tables must use the approved 0-to-100 scoring scale.
- Question Scoring Tables must not encode readiness thresholds.
- Question Scoring Tables must not encode Severity, Risk, Confidence,
  Recommendation, or Executive Summary logic.

## 5. Allowable Response Model

Status: `APPROVED`

Each Question Scoring Table must define the complete allowable response set for
its canonical question.

An allowable response entry must represent a response value that can be
submitted and validated for that question. The response value may be categorical,
boolean-like, ordinal, or numeric only when the canonical question and
approved methodology support that response type.

Required allowable response properties:

- Response value.
- Response label.
- Response type.
- Response description.
- Validity status.
- Source question ID.
- Methodology version.

The allowable response model must be complete. A response value that is not
listed in the approved Question Scoring Table is unsupported and must fail
closed.

## 6. Response-to-Score Mapping Structure

Status: `APPROVED`

Each Question Scoring Table must contain one response-to-score mapping for
each allowable response.

Required mapping structure:

| Field | Requirement |
| --- | --- |
| `question_id` | Stable canonical Question ID. |
| `response_value` | Exact allowable response value. |
| `response_label` | Human-readable response label. |
| `normalized_score` | Score on the approved 0-to-100 scale. |
| `score_rationale` | Methodology rationale for the assigned score. |
| `scoring_scale_version` | Approved scoring scale version. |
| `scoring_table_version` | Question Scoring Table version. |
| `methodology_version` | Approved methodology version. |

The `normalized_score` field is required by the structure, but this
specification does not approve any actual numeric values for any canonical
question response.

## 7. Required Metadata

Status: `APPROVED`

Each Question Scoring Table must include:

- Question ID.
- Question text reference.
- Primary Dimension.
- Secondary Dimension references, if any.
- Taxonomy version.
- Scoring scale version.
- Scoring table version.
- Methodology version.
- Approval status.
- Effective version.
- Owner.
- Change rationale.
- Source methodology references.
- Complete allowable response set.
- Complete response-to-score mappings.
- Validation status.
- Retirement status, if superseded.

Each scored output must preserve traceability to:

- Question ID.
- Submitted response value.
- Matching allowable response entry.
- Normalized score.
- Scoring scale version.
- Scoring table version.
- Methodology version.

## 8. Validation Rules

Status: `APPROVED`

Question Scoring Table validation must fail closed.

Required validation rules:

- Every canonical question that is in scoring scope must have exactly one
  active Question Scoring Table for the applicable methodology version.
- Every Question Scoring Table must reference a valid canonical Question ID.
- Every Question Scoring Table must reference the approved methodology version.
- Every Question Scoring Table must reference the approved scoring scale
  version.
- Every allowable response must have exactly one score mapping.
- No duplicate response mappings are permitted.
- No unreachable response values are permitted.
- No response value may map to more than one normalized score.
- Every normalized score must be within the approved 0-to-100 range.
- Missing required responses must fail closed.
- Unsupported response values must fail closed.
- Unsupported methodology versions must fail closed.
- Unsupported scoring scale versions must fail closed.
- Unsupported scoring table versions must fail closed.

This specification does not define the implementation mechanism for validation.

## 9. Computational Properties

Status: `APPROVED`

Question Scoring Tables must satisfy:

- Determinism: the same valid response for the same question under the same
  scoring table version must always produce the same normalized score.
- Idempotence: re-scoring the same validated responses under the same
  methodology and scoring table versions must produce identical question
  scores.
- Boundedness: all produced scores must remain within 0 and 100 inclusive.
- Completeness: every allowable response must have one and only one score.
- Traceability: every question score must trace to the source response,
  scoring table, scoring scale, and methodology version.
- Auditability: every mapping must include rationale and source methodology
  references.
- Version binding: response mappings are bound to methodology version, scoring
  scale version, and scoring table version.
- Fail-closed behavior: missing, malformed, duplicate, unsupported, or
  out-of-range mappings must prevent production-authoritative scoring.

## 10. Governance

Status: `APPROVED`

Question Scoring Tables are repository-owned Assessment Service methodology
artifacts.

Governance requirements:

- Question Scoring Tables must be approved before production-authoritative
  question scoring is implemented.
- Each table must be reviewed against the canonical Question Mapping Matrix.
- Each table must be reviewed against Scoring Scale Specification v1.
- Each table must preserve deterministic business truth and explainability.
- Each table must be immutable once approved for a version.
- Each change must include documented rationale.
- Tables must never be changed to influence individual assessment outcomes,
  customer outcomes, readiness distributions, scoring distributions, or sales
  conclusions.
- Downstream consumers must consume produced scores and must not reinterpret
  response-to-score mappings.

## 11. Versioning

Status: `APPROVED`

Question scoring tables specification identity:

```text
question-scoring-tables-specification-v1
```

Approved scoring scale version:

```text
scoring-scale-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

Each approved Question Scoring Table must have a stable table version.

A new Question Scoring Table version is required if:

- An allowable response is added.
- An allowable response is removed.
- An allowable response value changes.
- A normalized score changes.
- Score rationale changes in a way that changes methodology meaning.
- The referenced scoring scale version changes.
- The referenced methodology version changes.
- Golden Fixture expected outputs would change.

## 12. Production Readiness Requirements

Status: `METHODOLOGY_PENDING`

This specification approves the structure and governance for Question Scoring
Tables. Question Scoring Tables v1 approves the actual deterministic
response-to-score mappings for all 48 canonical questions.

Required before production-authoritative question scoring:

- Approved actual Question Scoring Table for each canonical question.
- Approved allowable response set for each canonical question.
- Approved numeric response-to-score mapping for every allowable response.
- Validation confirming every score is within the approved 0-to-100 scale.
- Validation confirming all 48 canonical questions are covered.
- Validation confirming scoring table versions and methodology versions are
  consistent.
- Golden Fixture artifacts containing expected question scores.
- Regression validation for Golden Fixtures.
- Release documentation stating which scoring outputs are
  production-authoritative.

## 13. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications and artifacts remain required:

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE QUESTION SCORING TABLE STRUCTURE AND GOVERNANCE
```

Question Scoring Tables shall be the authoritative deterministic mechanism for
mapping allowable canonical question responses to normalized scores on the
approved 0-to-100 scale. This specification approves table structure,
metadata, validation rules, computational properties, governance, and
versioning only.

Actual numeric response-to-score mappings for the 48 canonical questions are
approved by Question Scoring Tables v1.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/10-question-mapping-matrix-v1.md`
- `docs/business-decision-methodology/13-scoring-scale-specification-v1.md`
- `docs/architecture/assessment-decision-engine-v2.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
