# Scoring Scale Specification v1

## 1. Purpose

Status: `APPROVED`

This specification defines the methodology-wide scoring scale for deterministic
Executive Assessment Rubric v1 computation in the Assessment Service.

The approved scoring scale is:

```text
0 to 100 inclusive
```

This scale is the authoritative numeric scale for question scores, dimension
results, and the overall assessment result when those outputs are produced
under approved scoring tables and implementation specifications.

This specification does not define question-specific scoring tables, response
mappings, readiness thresholds, deterministic decision tables, or implementation
algorithms.

## 2. Scope

Status: `APPROVED`

In scope:

- Methodology-wide scoring scale identity.
- Minimum and maximum scale bounds.
- Directional interpretation of the scale.
- Candidate scale evaluation.
- Selection criteria.
- Computational properties.
- Governance and versioning requirements.
- Production readiness requirements for using the scale in implementation.

Out of scope:

- Question-specific response-to-score mappings.
- Readiness threshold values.
- Readiness boundary convention.
- Severity, Risk, Confidence, Recommendation, or Executive Summary decision
  tables.
- Implementation algorithms.
- Package or snapshot contract changes.
- Downstream consumer interpretation.

## 3. Architectural Role

Status: `APPROVED`

The Scoring Scale is the shared numeric basis used by deterministic Assessment
Service computations.

It supports:

- Deterministic conversion from validated canonical question responses to
  question scores after question-specific Scoring Tables are approved.
- Equal contribution roll-up within approved Primary Dimensions.
- Arithmetic dimension result formation.
- Weighted aggregation using the approved Decision 7 Numeric Dimension Weight
  Set and Decision 8 aggregation methodology.
- Future readiness thresholds.
- Future deterministic decision tables.
- Golden Fixture expected outputs and regression validation.

The Scoring Scale is owned by the Assessment Service. It is producer-side
methodology and must not be redefined by downstream consumers.

## 4. Design Principles

Status: `APPROVED`

- Deterministic: the same approved numeric input has the same meaning under the
  same scoring scale version.
- Auditable: scale bounds and interpretation are explicit and reviewable.
- Explainable: executives, auditors, implementation teams, and clients can
  understand the numeric range without hidden transformation.
- Aggregation-compatible: the scale supports arithmetic mean and weighted
  aggregation without changing approved business intent.
- Readiness-compatible: the scale supports future numeric readiness thresholds.
- Decision-table-compatible: future deterministic decision tables can reference
  the scale without inventing a parallel scoring vocabulary.
- Fixture-compatible: Golden Fixtures can encode expected outputs on the same
  scale used by production computation.
- Fail-closed: values outside the approved scale are invalid and must not be
  interpreted, clamped, inferred, or defaulted.
- Repository-owned: scale governance remains inside the Assessment Service.

## 5. Candidate Scoring Scale Options

Status: `FOUNDATION`

The following candidate scale options were evaluated as implementation
specification alternatives.

| Candidate | Description | Status |
| --- | --- | --- |
| Binary | Two values representing absent/present or false/true. | Rejected for v1 scale selection. |
| 3-point | Three ordered values representing low, partial, and high capability. | Rejected for v1 scale selection. |
| 5-point | Five ordered values representing maturity-like levels. | Rejected for v1 scale selection. |
| Percentage | Numeric range from 0 to 100 inclusive. | Approved for v1 scale selection. |
| Normalized | Common numeric range used to normalize heterogeneous answer types. | Approved as the architectural interpretation of the 0-to-100 scale. |

The approved v1 scale is the normalized percentage scale:

```text
0 to 100 inclusive
```

## 6. Evaluation Criteria

Status: `APPROVED`

The scoring scale was evaluated against the following criteria:

- Deterministic compatibility.
- Arithmetic aggregation support.
- Weighted aggregation support.
- Readiness threshold support.
- Decision-table support.
- Explainability.
- Audit defensibility.
- Backward compatibility with current normalized evaluation behavior.
- Golden Fixture compatibility.
- Repository ownership.
- Fail-closed validation.

## 7. Advantages and Trade-Offs

Status: `APPROVED`

Binary scale:

- Advantages: simple and easy to validate.
- Trade-offs: insufficient to represent partial readiness, maturity, or graded
  business capability.

3-point scale:

- Advantages: simple and more expressive than binary.
- Trade-offs: limited granularity for aggregation, thresholding, and executive
  explanation.

5-point scale:

- Advantages: familiar for maturity models and easier to review than broad
  numeric ranges.
- Trade-offs: less compatible with existing normalized 0-to-100 architecture
  and less precise for weighted aggregation and Golden Fixture expectations.

Percentage scale:

- Advantages: business-readable, compatible with arithmetic aggregation,
  weighted aggregation, readiness thresholds, deterministic fixtures, and the
  current normalized evaluation foundation.
- Trade-offs: may imply false precision unless question-specific scoring
  tables and executive explanations remain governed and auditable.

Normalized scale:

- Advantages: supports heterogeneous canonical answer types by giving all
  deterministic question scores a common range.
- Trade-offs: requires strict scoring tables so normalization does not become
  hidden business logic.

## 8. Selection Criteria

Status: `APPROVED`

The normalized 0-to-100 scale is selected because it satisfies the approved
methodology requirements:

- It preserves the current architecture's shared normalized evaluation scale.
- It supports arithmetic dimension result formation.
- It supports weighted aggregation under the approved official dimension
  weights.
- It supports future numeric readiness thresholds.
- It supports deterministic decision tables.
- It supports explainable executive review.
- It supports auditable Golden Fixture expected outputs.
- It remains independent from question-specific response mappings.

No question-specific scoring values are approved by this specification.

## 9. Computational Properties

Status: `APPROVED`

The approved scale has the following computational properties:

- Boundedness: valid scores must remain within 0 and 100 inclusive.
- Ordering: higher values represent stronger assessed capability than lower
  values under the same methodology version.
- Monotonic compatibility: increasing a valid question score, dimension result,
  or overall assessment result shall not reduce the corresponding aggregate
  value when all other approved inputs remain unchanged.
- Arithmetic compatibility: valid values can participate in arithmetic mean
  dimension result formation.
- Weighted aggregation compatibility: valid dimension results can participate
  in Decision 8 weighted aggregation.
- Version binding: scoring scale bounds and interpretation are bound to the
  scoring scale version and methodology version.
- Auditability: every score must be traceable to the scale version and the
  approved scoring artifact that produced it.
- Fail-closed validation: missing, non-numeric, unsupported, below-minimum, or
  above-maximum values must be rejected for production-authoritative scoring.

This section does not define rounding behavior, display precision, or
implementation storage type. Those remain implementation specification details.

## 10. Governance

Status: `APPROVED`

The Scoring Scale is a repository-owned Assessment Service methodology
artifact.

Governance requirements:

- The scale must have a stable specification identifier.
- The scale must have a version.
- The scale must be traceable to Assessment Methodology Specification v1.
- The scale must be applied consistently across all approved scoring tables
  using the same methodology version.
- The scale must not be changed to influence individual assessment outcomes,
  customer outcomes, readiness distributions, or scoring distributions.
- Any scale change requires documented rationale, methodology version review,
  backward compatibility review, and Golden Fixture impact review.

## 11. Versioning

Status: `APPROVED`

Scoring scale specification identity:

```text
scoring-scale-specification-v1
```

Approved scale version:

```text
scoring-scale-v1
```

Approved methodology version:

```text
business-decision-methodology-v1
```

A new scoring scale version is required if:

- The minimum value changes.
- The maximum value changes.
- The interpretation of higher or lower values changes.
- The valid numeric domain changes.
- Rounding, precision, or storage semantics become methodology-significant.
- Backward compatibility or Golden Fixture reproducibility would be affected.

## 12. Production Readiness Requirements

Status: `METHODOLOGY_PENDING`

The scoring scale is approved, but production-authoritative rubric
implementation remains blocked until the following are approved:

- Golden Fixture artifacts covering the approved scoring scale and expected
  outputs.
- Regression implementation for Golden Fixtures.
- Release documentation stating which outputs are production-authoritative.

## 13. Outstanding Implementation Dependencies

Status: `METHODOLOGY_PENDING`

The following implementation specifications remain required before
deterministic Executive Assessment Rubric v1 implementation can safely begin:

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE NORMALIZED 0-TO-100 SCORING SCALE
```

The normalized 0-to-100 scale is the authoritative methodology-wide scoring
scale for Executive Assessment Rubric v1 implementation specifications. It is
deterministic, auditable, explainable, compatible with arithmetic aggregation,
compatible with weighted aggregation, compatible with future readiness
thresholds and deterministic decision tables, and aligned with existing
Assessment Service architecture.

No implementation code is authorized by this specification.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-intelligence/03-scoring-philosophy.md`
- `docs/architecture/assessment-decision-engine-v2.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
