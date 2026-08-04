# Readiness Threshold Values v1

## 1. Purpose

Status: `APPROVED`

This document defines the official numeric readiness threshold values and final
readiness boundary convention for `business-decision-methodology-v1`.

Readiness Threshold Values v1 maps validated normalized numeric results on the
approved 0-to-100 scoring scale to the approved readiness taxonomy.

This document does not define Severity rules, Risk rules, Confidence rules,
Recommendation rules, Executive Summary rules, implementation code, package
contracts, or snapshot contracts.

## 2. Approved Readiness Taxonomy

Status: `APPROVED`

Approved readiness levels:

- Not Ready.
- Developing.
- Ready.
- Advanced.

Operational processing state:

- Incomplete.

Incomplete is not a readiness level. It is an operational processing state
used when readiness cannot be assigned because one or more required inputs are
missing, invalid, unavailable, or unsupported under the approved fail-closed
methodology.

## 3. Numeric Threshold Table

Status: `APPROVED`

Threshold set ID:

```text
readiness-threshold-set-v1
```

The official readiness threshold values are:

| Readiness Level | Lower Bound | Upper Bound | Boundary Semantics |
| --- | ---: | ---: | --- |
| Not Ready | 0 | 25 | `0 <= score < 25` |
| Developing | 25 | 50 | `25 <= score < 50` |
| Ready | 50 | 75 | `50 <= score < 75` |
| Advanced | 75 | 100 | `75 <= score <= 100` |

The same threshold set applies to:

- Each approved Business Capability Dimension result.
- The Overall Assessment Result.

Readiness assignment consumes only validated numeric results. It does not
modify question scores, dimension results, aggregation results, findings,
severity assignment, risk assessment, confidence assessment, recommendations,
or executive summaries.

## 4. Boundary Convention

Status: `APPROVED`

Boundary convention version:

```text
readiness-boundary-convention-v1
```

The approved boundary convention is:

- Lower bounds are inclusive.
- Upper bounds are exclusive for Not Ready, Developing, and Ready.
- The maximum score of 100 is included in Advanced.
- The minimum score of 0 is included in Not Ready.
- Exact boundary scores assign to the higher readiness level except for 0,
  which assigns to Not Ready.
- 100 assigns to Advanced.

Boundary examples:

| Score | Readiness Assignment |
| ---: | --- |
| 0 | Not Ready |
| 24.999 | Not Ready |
| 25 | Developing |
| 49.999 | Developing |
| 50 | Ready |
| 74.999 | Ready |
| 75 | Advanced |
| 100 | Advanced |

## 5. Validation Rules

Status: `APPROVED`

Readiness threshold validation must fail closed.

Required validation rules:

- The numeric result must be present.
- The numeric result must be valid.
- The numeric result must be within the approved 0-to-100 scoring scale.
- The threshold set version must be `readiness-threshold-set-v1`.
- The boundary convention version must be `readiness-boundary-convention-v1`.
- The scoring scale version must be `scoring-scale-v1`.
- The methodology version must be `business-decision-methodology-v1`.
- Every approved readiness level must have exactly one active threshold range.
- Threshold ranges must collectively cover the full 0-to-100 scoring range.
- Threshold ranges must not overlap.
- Threshold ranges must not leave gaps.
- Every valid score must resolve to exactly one readiness level.
- Incomplete must remain an operational processing state, not a readiness
  level.

## 6. Fail-Closed Rules

Status: `APPROVED`

Readiness assignment must fail closed when:

- The numeric result is missing.
- The numeric result is invalid.
- The numeric result is below 0.
- The numeric result is above 100.
- The threshold set version is unsupported.
- The boundary convention version is unsupported.
- The scoring scale version is unsupported.
- The methodology version is unsupported.
- Threshold ranges overlap.
- Threshold ranges contain gaps.
- Threshold ranges do not cover the full 0-to-100 scoring range.
- More than one readiness level could be assigned to the same score.
- No readiness level can be assigned to a valid score.

When required input is missing, invalid, unavailable, or unsupported,
readiness must not be assigned. The result is the Incomplete operational
processing state under the approved fail-closed methodology.

## 7. Version Identity

Status: `APPROVED`

Threshold values artifact version:

```text
readiness-threshold-values-v1
```

Threshold set version:

```text
readiness-threshold-set-v1
```

Boundary convention version:

```text
readiness-boundary-convention-v1
```

Readiness taxonomy version:

```text
readiness-taxonomy-v1
```

Scoring scale version:

```text
scoring-scale-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

## 8. Computational Properties

Status: `APPROVED`

Readiness Threshold Values v1 satisfies:

- Determinism: the same valid numeric result under the same threshold set,
  boundary convention, scoring scale, and methodology versions always produces
  the same readiness assignment.
- Idempotence: reassigning readiness from the same validated inputs produces
  identical readiness assignments.
- Complete coverage: every valid score from 0 to 100 inclusive resolves to one
  readiness level.
- Mutual exclusivity: no valid score resolves to more than one readiness
  level.
- Monotonic readiness: increasing a numeric assessment result while holding
  the methodology version constant never assigns a lower readiness level.
- Traceability: every readiness assignment must trace to the source numeric
  result, threshold set version, boundary convention version, scoring scale
  version, and methodology version.
- Explainability: every readiness assignment must identify the numeric result,
  applied threshold range, and assigned readiness level.
- Fail-closed validation: invalid, missing, unavailable, or unsupported inputs
  prevent readiness assignment.

## 9. Governance

Status: `APPROVED`

Readiness Threshold Values v1 is a repository-owned Assessment Service
methodology artifact.

Governance requirements:

- Threshold values are immutable once approved.
- Boundary convention is immutable once approved.
- Any threshold value change requires a new threshold set version.
- Any boundary convention change requires a new boundary convention version.
- Changes must be non-retroactive unless a future governed methodology
  decision explicitly states otherwise.
- Frozen snapshots must remain reproducible from the threshold set, boundary
  convention, scoring scale, and methodology versions used when they were
  produced.
- Downstream consumers may consume readiness assignments but must not
  reinterpret threshold ranges.

## 10. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Complete coverage of the 0-to-100 scale. | Pass |
| No threshold gaps. | Pass |
| No threshold overlaps. | Pass |
| Exactly one readiness level per valid score. | Pass |
| Boundary behavior is deterministic. | Pass |
| Invalid scores fail closed. | Pass |
| Missing or unsupported inputs produce Incomplete. | Pass |
| Incomplete remains an operational processing state, not a readiness level. | Pass |
| Threshold set version is defined. | Pass |
| Boundary convention version is defined. | Pass |

## 11. Remaining Implementation Artifacts

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 12. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE READINESS THRESHOLD VALUES V1
```

The official readiness threshold values and final readiness boundary
convention are approved for `business-decision-methodology-v1` using
`scoring-scale-v1`.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/13-scoring-scale-specification-v1.md`
- `docs/business-decision-methodology/15-readiness-threshold-specification-v1.md`
- `docs/business-decision-methodology/20-question-scoring-tables-v1.md`
