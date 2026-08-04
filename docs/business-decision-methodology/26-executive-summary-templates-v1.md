# Executive Summary Templates v1

## 1. Purpose

Status: `APPROVED`

This document defines deterministic Executive Summary templates and narrative
composition rules for `business-decision-methodology-v1`.

Executive Summary Templates v1 consumes approved Assessment Service producer
artifacts only. Executive Summary output presents previously determined
business truth and shall never introduce, modify, reinterpret, or override
business truth.

This document does not define AI-generated narrative, presentation styling,
Website formatting, Client Portal formatting, implementation code, package
contracts, or snapshot contracts.

## 2. Executive Summary Structure

Status: `APPROVED`

Executive Summary Templates v1 uses the required Decision 17 Executive Summary
section structure:

1. Overall Assessment Overview.
2. Business Capability Highlights.
3. Significant Findings.
4. Risk Overview.
5. Confidence Statement.
6. Recommended Actions.
7. Closing Assessment Statement.

The section order is fixed and deterministic. No additional sections are
approved by this artifact.

The existing Executive Summary Foundation section catalog remains
foundation-only. It does not override the approved Decision 17 section
structure and does not authorize runtime behavior changes.

## 3. Required Sections

Status: `APPROVED`

Each Executive Summary section has one deterministic section ID, one required
heading, and approved upstream source artifacts.

| Section Order | Section ID | Required Heading | Required Source Artifacts |
| --- | --- | --- | --- |
| 1 | `overall-assessment-overview` | Overall Assessment Overview | Overall Assessment Result, Readiness, Methodology Version |
| 2 | `business-capability-highlights` | Business Capability Highlights | Dimension Results, Readiness, Evidence Evaluation |
| 3 | `significant-findings` | Significant Findings | Findings, Severity Assignment, Evidence Evaluation |
| 4 | `risk-overview` | Risk Overview | Risk Assessment, Severity Assignment, Findings |
| 5 | `confidence-statement` | Confidence Statement | Confidence Assessment, Evidence Evaluation |
| 6 | `recommended-actions` | Recommended Actions | Recommendations, Findings, Severity Assignment, Risk Assessment, Confidence Assessment |
| 7 | `closing-assessment-statement` | Closing Assessment Statement | Overall Assessment Result, Readiness, Risk Assessment, Confidence Assessment, Recommendations, Methodology Version |

Every section must preserve section-level traceability to the source artifacts
it summarizes.

## 4. Narrative Composition Rules

Status: `APPROVED`

Executive Summary narrative composition is deterministic and template-bound.

Approved composition rules:

- Each section must be rendered from the approved section template for that
  section ID.
- Each template may use only approved placeholder values sourced from required
  upstream artifacts.
- Placeholder values must be inserted exactly as produced by the upstream
  artifact.
- Templates shall summarize approved business truth only.
- Templates shall not infer causation, urgency, readiness, risk, confidence,
  severity, or recommendation priority beyond approved upstream outputs.
- Templates shall not add qualitative adjectives unless the adjective is part
  of an approved upstream taxonomy label.
- Templates shall not change upstream labels, scores, classifications,
  findings, recommendations, or rationale.
- Required sections with empty source collections must use the approved empty
  collection statement for that section.
- Template ordering must follow the fixed section order in this document.
- No duplicate sections are permitted.
- No optional sections are approved.
- No AI-generated text is permitted.

Approved placeholder rules:

- `{overall_assessment_result}` is sourced from Overall Assessment Result.
- `{readiness}` is sourced from Readiness.
- `{dimension_results}` is sourced from Dimension Results.
- `{finding_count}` is sourced from the complete Finding collection.
- `{significant_findings}` is sourced from Findings with Severity Assignment.
- `{risk_assessment}` is sourced from Risk Assessment.
- `{confidence_assessment}` is sourced from Confidence Assessment.
- `{recommendation_count}` is sourced from the Recommendation set.
- `{recommendations}` is sourced from Recommendations.
- `{methodology_version}` is sourced from the approved methodology version.
- `{artifact_versions}` is sourced from version metadata on consumed upstream
  artifacts.

## 5. Required Inputs

Status: `APPROVED`

Executive Summary Templates v1 requires:

- Overall Assessment Result.
- Dimension Results.
- Readiness.
- Evidence Evaluation.
- Findings.
- Severity Assignment.
- Risk Assessment.
- Confidence Assessment.
- Recommendations.
- Source references for every consumed artifact.
- Scoring methodology version.
- Readiness methodology version.
- Evidence Evaluation methodology version.
- Finding methodology version.
- Severity decision table version.
- Risk decision table version.
- Confidence decision table version.
- Recommendation decision table version.
- Executive Summary template version.
- Methodology version.

Required input constraints:

- Overall Assessment Result must be complete and valid.
- Dimension Results must be complete for all approved Business Capability
  Dimensions.
- Readiness must be one approved readiness level under approved Readiness
  Methodology.
- Evidence Evaluation must be valid under approved Evidence Evaluation
  Methodology.
- Findings must be generated under approved Finding Methodology.
- Every generated Finding must have Severity Assignment under Severity
  Decision Tables v1.
- Risk Assessment must be produced under Risk Decision Tables v1.
- Confidence Assessment must be produced under Confidence Decision Tables v1.
- Recommendations must be produced under Recommendation Decision Tables v1.
- Required source references must be present and versioned.
- Executive Summary Templates shall not recalculate, reinterpret, or modify
  upstream business truth.

## 6. Output Metadata

Status: `APPROVED`

Each Executive Summary output must include:

- Summary ID.
- Executive Summary template version.
- Methodology version.
- Section count.
- Stable section ordering metadata.
- Consumed artifact version metadata.
- Source Overall Assessment Result references.
- Source Dimension Result references.
- Source Readiness references.
- Source Evidence Evaluation references.
- Source Finding references.
- Source Severity Assignment references.
- Source Risk Assessment references.
- Source Confidence Assessment references.
- Source Recommendation references.
- Section-level traceability rationale.
- Validation status.

Each Executive Summary section must include:

- Section ID.
- Section heading.
- Section order.
- Template ID.
- Template version.
- Rendered deterministic text.
- Source artifact references.
- Placeholder source map.
- Section validation status.

## 7. Validation Rules

Status: `APPROVED`

Executive Summary validation must fail closed.

Required validation rules:

- Every Executive Summary must consume approved upstream artifacts only.
- No business truth may be created, modified, reinterpreted, or overridden.
- Every required section must be present exactly once.
- No duplicate sections are permitted.
- No unapproved sections are permitted.
- Section ordering must match this artifact.
- Every section must use the approved template for its section ID.
- Every placeholder must have exactly one approved source artifact.
- Placeholder values must match the upstream artifact values.
- Missing required placeholder values must fail closed.
- Missing required upstream artifacts must fail closed.
- Unsupported upstream artifact versions must fail closed.
- Unsupported template versions must fail closed.
- Narrative rules must remain deterministic.
- Output must be version-bound.

## 8. Fail-Closed Rules

Status: `APPROVED`

Executive Summary generation must fail closed when:

- Overall Assessment Result is missing, malformed, or unsupported.
- Dimension Results are missing, malformed, incomplete, or unsupported.
- Readiness is missing, malformed, unsupported, or `Incomplete`.
- Evidence Evaluation is missing, malformed, or unsupported.
- Finding collection is missing or not deterministically complete.
- Severity Assignment is missing for one or more generated Findings.
- Risk Assessment is missing, malformed, or unsupported.
- Confidence Assessment is missing, malformed, or unsupported.
- Recommendation set is missing, malformed, or unsupported.
- Required source references are missing.
- Required methodology versions are missing or unsupported.
- Executive Summary template version is missing or unsupported.
- A required section is missing.
- A duplicate section is present.
- An unapproved section is present.
- A template contains an unsupported placeholder.
- A placeholder cannot be resolved from approved upstream artifacts.
- A section attempts to introduce new business truth.
- Rule inputs are malformed, incomplete, ambiguous, or conflicting.

Fail-closed Executive Summary generation means no Executive Summary is emitted.
It does not create a partial Executive Summary and does not modify scores,
Readiness, Evidence Evaluation, Findings, Severity, Risk, Confidence, or
Recommendations.

## 9. Version Identity

Status: `APPROVED`

Executive Summary template artifact version:

```text
executive-summary-templates-v1
```

Executive Summary template set version:

```text
executive-summary-template-set-v1
```

Methodology version:

```text
business-decision-methodology-v1
```

Required upstream artifact versions:

- `scoring-scale-v1`
- `question-scoring-tables-v1`
- `readiness-threshold-values-v1`
- `severity-decision-table-set-v1`
- `risk-decision-table-set-v1`
- `confidence-decision-table-set-v1`
- `recommendation-decision-table-set-v1`

## 10. Computational Properties

Status: `APPROVED`

Executive Summary Templates v1 satisfies:

- Determinism: the same complete set of valid upstream artifacts under the same
  template version always produces the same Executive Summary.
- Idempotence: regenerating Executive Summary output from the same valid inputs
  under the same methodology version produces identical Executive Summary
  output.
- Complete coverage: all approved required sections are produced for every
  complete valid assessment.
- Stable ordering: identical valid inputs produce the same section ordering.
- No duplicate sections: the Executive Summary contains each approved section
  exactly once.
- Traceability: every section traces to upstream artifacts, template version,
  and methodology version.
- Auditability: templates, placeholders, input sources, outputs, and versions
  are reviewable.
- Version binding: templates are bound to Executive Summary template version,
  methodology version, and consumed upstream artifact versions.
- Deterministic independence: Executive Summary generation does not modify
  upstream deterministic business truth.
- Fail-closed behavior: missing, malformed, unsupported, ambiguous, or
  conflicting inputs prevent Executive Summary output.

## 11. Template Examples

Status: `APPROVED`

The following templates define deterministic text composition. Bracketed
placeholders are replaced only with approved upstream artifact values.

### Overall Assessment Overview

Template ID: `executive-summary-v1-overall-assessment-overview`

Template:

```text
The overall assessment result is {overall_assessment_result}. The assigned readiness state is {readiness}. This summary was produced under {methodology_version}.
```

### Business Capability Highlights

Template ID: `executive-summary-v1-business-capability-highlights`

Template:

```text
Business capability results are: {dimension_results}. These results are summarized from approved Dimension Results and Evidence Evaluation.
```

### Significant Findings

Template ID: `executive-summary-v1-significant-findings`

Template when Findings are present:

```text
The assessment produced {finding_count} Findings. Significant Findings are summarized from Severity-Assigned Findings: {significant_findings}.
```

Template when no Findings are present:

```text
The assessment produced no Findings.
```

### Risk Overview

Template ID: `executive-summary-v1-risk-overview`

Template:

```text
The assessment-level risk is {risk_assessment}. This Risk Assessment is summarized from approved Severity-Assigned Findings.
```

### Confidence Statement

Template ID: `executive-summary-v1-confidence-statement`

Template:

```text
The confidence assessment is {confidence_assessment}. This Confidence Assessment is summarized from approved Evidence Evaluation and required upstream context.
```

### Recommended Actions

Template ID: `executive-summary-v1-recommended-actions`

Template:

```text
The assessment produced {recommendation_count} Recommendations: {recommendations}.
```

### Closing Assessment Statement

Template ID: `executive-summary-v1-closing-assessment-statement`

Template:

```text
This Executive Summary presents approved Assessment Service outputs only. It is bound to {methodology_version} and source artifact versions {artifact_versions}.
```

## 12. Validation Summary

Status: `APPROVED`

| Validation Requirement | Result |
| --- | --- |
| Every Executive Summary consumes approved upstream artifacts only. | Pass |
| No business truth is created or modified. | Pass |
| Every section has deterministic input sources. | Pass |
| Missing required inputs fail closed. | Pass |
| Template ordering is deterministic. | Pass |
| No duplicate sections are permitted. | Pass |
| Narrative rules remain deterministic. | Pass |
| Output is version-bound. | Pass |
| No AI-generated narrative is authorized. | Pass |
| Presentation formatting is not introduced. | Pass |

## 13. Remaining Implementation Artifacts

Status: `METHODOLOGY_PENDING`

- Regression validation implementation.

## 14. Recommendation

Status: `APPROVED`

Recommendation:

```text
APPROVE EXECUTIVE SUMMARY TEMPLATES V1
```

The deterministic Executive Summary Templates are approved for
`business-decision-methodology-v1`. They produce deterministic sectioned
Executive Summary output from approved upstream Assessment Service artifacts
only and fail closed for malformed, unsupported, incomplete, ambiguous, or
conflicting inputs.

No implementation code is authorized by this artifact.

Repository evidence:

- `docs/business-decision-methodology/09-assessment-methodology-specification-v1.md`
- `docs/business-decision-methodology/21-readiness-threshold-values-v1.md`
- `docs/business-decision-methodology/22-severity-decision-tables-v1.md`
- `docs/business-decision-methodology/23-risk-decision-tables-v1.md`
- `docs/business-decision-methodology/24-confidence-decision-tables-v1.md`
- `docs/business-decision-methodology/25-recommendation-decision-tables-v1.md`
