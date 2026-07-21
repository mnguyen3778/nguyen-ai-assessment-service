# Business Decision Package Serialization Contract v1

## Purpose

This document defines the deterministic serialization contract for the
`BusinessDecisionPackage`.

The Business Decision Package is the canonical immutable output contract of the
Nguyen AI Assessment Service. This document specifies the exact serialized
shape produced by the package so downstream consumers can rely on stable field
names, stable ordering, explicit version metadata, audit metadata, and visible
limitations.

This is not an API contract, HTTP schema, persistence model, OpenAPI document,
or JSON Schema. It is the repository-level serialization specification for the
immutable deterministic package object.

## Serialization Principles

Serialization must preserve the same governance properties as the package:

- Deterministic: identical package inputs produce identical serialized output.
- Immutable by source: serialization reads package contents and does not mutate
  package objects or contained Sprint 3 outputs.
- Reproducible: serialized output includes assessment, methodology, contract,
  and component version metadata.
- Explainable: serialized output preserves Decision Engine explanation
  metadata and downstream foundation source metadata.
- Traceable: serialized output keeps the chain from evaluation result to
  snapshot, confidence, priority foundation, executive summary foundation,
  audit, and limitations.
- Bounded: serialization does not add recommendations, service routing,
  executive narratives, API metadata, persistence metadata, generated
  identifiers, or timestamps.

Serialization is a projection of already-created deterministic objects. It does
not calculate new business conclusions.

## Deterministic Ordering Rules

The serialized package uses deterministic ordering so downstream systems can
compare outputs reproducibly.

Root object fields are emitted in this order:

1. `decisionEvaluation`
2. `businessReadinessSnapshot`
3. `confidenceEvaluation`
4. `recommendationPriorityEvaluation`
5. `executiveSummaryFoundation`
6. `audit`
7. `limitations`
8. `versionMetadata`

Nested ordering rules:

- `decisionEvaluation.dimensions` is ordered by readiness dimension identifier.
- `decisionEvaluation.explanation.appliedWeights` is ordered by question
  identifier.
- `decisionEvaluation.explanation.questionExplanations` is ordered by question
  identifier.
- `decisionEvaluation.explanation.dimensionExplanations` is ordered by
  readiness dimension identifier.
- `businessReadinessSnapshot.domains` is emitted in the deterministic order
  produced by the snapshot foundation, currently readiness dimension
  identifier order.
- `confidenceEvaluation.factors` is emitted in the deterministic order produced
  by the confidence foundation, currently confidence factor identifier order.
- `recommendationPriorityEvaluation.configuredPriorityLevels` is emitted in
  deterministic priority rank order.
- `recommendationPriorityEvaluation.configuredPriorityFactors` is emitted in
  deterministic factor identifier order.
- `executiveSummaryFoundation.configuredSummarySections` is emitted in
  deterministic section identifier order.
- Tuple-backed values are serialized as arrays while preserving tuple order.
- Limitation arrays preserve the package-defined limitation order.
- Version metadata component versions preserve package-defined component order.

Consumers must not infer business priority from object ordering unless that
ordering is explicitly defined as ranked, such as configured recommendation
priority levels.

## Root Object Structure

The serialized root object contains exactly these fields:

| Field | Required | Owner | Description |
| --- | --- | --- | --- |
| `decisionEvaluation` | Yes | Decision Engine | Deterministic evaluation result and explanation metadata. |
| `businessReadinessSnapshot` | Yes | Snapshot Foundation | Passive readiness projection of the evaluation result. |
| `confidenceEvaluation` | Yes | Confidence Foundation | Deterministic confidence foundation output. |
| `recommendationPriorityEvaluation` | Yes | Recommendation Priority Foundation | Priority foundation output without final priority assignment. |
| `executiveSummaryFoundation` | Yes | Executive Summary Foundation | Summary foundation output without narrative generation. |
| `audit` | Yes | Business Decision Package | Package-level source and trace metadata. |
| `limitations` | Yes | Business Decision Package | Explicit current-scope limitations. |
| `versionMetadata` | Yes | Business Decision Package | Contract, assessment, methodology, and component versions. |

No root-level optional fields exist in contract v1.

## Required Fields

All root fields are required. Nested objects also emit all fields listed in this
document.

When a nested field is not currently evaluated or not applicable, the field is
still present and uses one of the following deterministic representations:

- `null` for nullable scalar fields.
- An empty array for empty tuple-backed or list-backed fields.
- An empty object only when a governed component explicitly owns an empty
  mapping.

Fields must not be omitted to represent current limitations.

## Optional Fields

Contract v1 has no optional root fields.

The following nested fields are nullable by design:

- `decisionEvaluation.explanation` may be `null` if a raw
  `DecisionEvaluationResult` without explanation is serialized. Valid packaged
  executive assessment flows are expected to include explanation metadata
  because the snapshot foundation requires it.
- `confidenceEvaluation.factors.*.observedCount`
- `confidenceEvaluation.factors.*.expectedCount`
- `confidenceEvaluation.factors.*.coverageRatio`
- `confidenceEvaluation.factors.*.limitation`
- `recommendationPriorityEvaluation.configuredPriorityFactors.*.limitation`
- `executiveSummaryFoundation.configuredSummarySections.*.limitation`

Nullable fields must remain present even when the value is `null`.

## Field Ownership

Field ownership preserves architecture boundaries.

| Field Group | Owning Layer | Governance Rule |
| --- | --- | --- |
| `decisionEvaluation` | Decision Engine | Source of deterministic readiness evaluation truth. |
| `businessReadinessSnapshot` | Snapshot Foundation | May project evaluation data but must not recompute it. |
| `confidenceEvaluation` | Confidence Foundation | May expose confidence foundation data but must not alter readiness. |
| `recommendationPriorityEvaluation` | Recommendation Priority Foundation | May expose configured priority metadata but must not assign final priority. |
| `executiveSummaryFoundation` | Executive Summary Foundation | May expose summary section metadata but must not generate prose or reports. |
| `audit` | Business Decision Package | Records source component, version, and trace metadata. |
| `limitations` | Business Decision Package | Records current limitations and must remain visible to consumers. |
| `versionMetadata` | Business Decision Package | Records package contract and source component versions. |

Downstream consumers may enrich package output in downstream-owned records, but
they must not overwrite fields owned by the Assessment Service.

## Nested Object Definitions

### `decisionEvaluation`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `overallScore` | number | Yes | Overall deterministic normalized evaluation score from the Decision Engine. |
| `totalWeight` | number | Yes | Total applied question weight from the Decision Engine result. |
| `questionCount` | integer | Yes | Number of evaluated questions. |
| `dimensions` | object | Yes | Mapping of readiness dimension ID to dimension evaluation object. |
| `explanation` | object or null | Yes | Evaluation explanation metadata. |

`decisionEvaluation.dimensions.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `dimensionId` | string | Yes | Readiness dimension identifier. |
| `normalizedScore` | number | Yes | Dimension normalized score from the Decision Engine. |
| `totalWeight` | number | Yes | Total applied weight for the dimension. |
| `questionCount` | integer | Yes | Count of contributing questions for the dimension. |
| `contributingQuestions` | array of string | Yes | Question IDs contributing to the dimension. |

`decisionEvaluation.explanation` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `evaluatedDimensions` | array of string | Yes when explanation is present | Evaluated readiness dimension identifiers. |
| `contributingQuestions` | array of string | Yes when explanation is present | Evaluated question identifiers. |
| `appliedWeights` | object | Yes when explanation is present | Mapping of question ID to applied weight. |
| `questionExplanations` | object | Yes when explanation is present | Mapping of question ID to question explanation object. |
| `dimensionExplanations` | object | Yes when explanation is present | Mapping of dimension ID to dimension explanation object. |

`decisionEvaluation.explanation.questionExplanations.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `questionId` | string | Yes | Canonical question identifier. |
| `readinessDimension` | string | Yes | Configured readiness dimension. |
| `evidenceCategory` | string | Yes | Configured evidence category. |
| `weightCategory` | string | Yes | Configured weight category. |
| `appliedWeight` | number | Yes | Applied deterministic question weight. |
| `normalizedScore` | number | Yes | Normalized question score. |

`decisionEvaluation.explanation.dimensionExplanations.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `dimensionId` | string | Yes | Readiness dimension identifier. |
| `contributingQuestions` | array of string | Yes | Contributing question identifiers. |
| `appliedWeights` | object | Yes | Mapping of contributing question ID to applied weight. |
| `normalizedScore` | number | Yes | Dimension normalized score. |
| `totalWeight` | number | Yes | Total applied weight for the dimension. |

### `businessReadinessSnapshot`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `assessmentVersion` | string | Yes | Assessment input contract version. |
| `overallReadiness` | object | Yes | Overall readiness projection. |
| `domains` | array of object | Yes | Readiness domain projections. |
| `audit` | object | Yes | Snapshot audit metadata. |

`businessReadinessSnapshot.overallReadiness` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `score` | number | Yes | Overall readiness score copied from the Decision Engine result. |
| `contributingDimensions` | array of string | Yes | Dimension IDs contributing to the overall projection. |

`businessReadinessSnapshot.domains[]` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `domainId` | string | Yes | Readiness domain identifier. |
| `label` | string | Yes | Configured readiness domain label. |
| `score` | number | Yes | Domain score copied from dimension evaluation. |
| `questionCount` | integer | Yes | Number of contributing questions. |
| `totalWeight` | number | Yes | Total applied domain weight. |
| `contributingQuestions` | array of string | Yes | Contributing canonical question IDs. |

`businessReadinessSnapshot.audit` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `methodologyVersion` | string | Yes | Methodology version used by the snapshot. |
| `evaluatedDimensions` | array of string | Yes | Evaluated readiness dimension IDs. |
| `questionCount` | integer | Yes | Total evaluated question count. |
| `totalWeight` | number | Yes | Total applied evaluation weight. |

### `confidenceEvaluation`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `assessmentVersion` | string | Yes | Assessment input contract version. |
| `methodologyVersion` | string | Yes | Methodology version used by confidence foundation. |
| `factors` | object | Yes | Mapping of confidence factor ID to factor evaluation. |
| `evaluatedFactorIds` | array of string | Yes | Evaluated confidence factor IDs. |
| `notEvaluatedFactorIds` | array of string | Yes | Configured but not evaluated confidence factor IDs. |

`confidenceEvaluation.factors.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `factorId` | string | Yes | Confidence factor identifier. |
| `label` | string | Yes | Configured confidence factor label. |
| `status` | string | Yes | Current foundation status. |
| `observedCount` | integer or null | Yes | Observed count for evaluated count-based factors. |
| `expectedCount` | integer or null | Yes | Expected count for evaluated count-based factors. |
| `coverageRatio` | number or null | Yes | Deterministic foundation coverage ratio when available. |
| `questionRefs` | array of string | Yes | Source question references. |
| `dimensionRefs` | array of string | Yes | Source dimension references. |
| `evidenceCategories` | array of string | Yes | Source evidence categories. |
| `limitation` | string or null | Yes | Limitation text for not-yet-evaluated factors. |

### `recommendationPriorityEvaluation`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `assessmentVersion` | string | Yes | Assessment input contract version. |
| `methodologyVersion` | string | Yes | Methodology version used by priority foundation. |
| `configuredPriorityLevels` | object | Yes | Mapping of configured priority ID to priority level metadata. |
| `configuredPriorityFactors` | object | Yes | Mapping of configured priority factor ID to factor foundation output. |
| `evaluatedFactorIds` | array of string | Yes | Evaluated priority factor IDs. Contract v1 emits an empty array. |
| `notEvaluatedFactorIds` | array of string | Yes | Not-yet-evaluated priority factor IDs. |
| `sourceSnapshotMetadata` | object | Yes | Snapshot source metadata used by the foundation. |
| `sourceConfidenceMetadata` | object | Yes | Confidence source metadata used by the foundation. |

`recommendationPriorityEvaluation.configuredPriorityLevels.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `priorityId` | string | Yes | Configured priority level identifier. |
| `label` | string | Yes | Configured priority level label. |
| `rank` | integer | Yes | Deterministic configured priority rank. |

`recommendationPriorityEvaluation.configuredPriorityFactors.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `factorId` | string | Yes | Configured priority factor identifier. |
| `label` | string | Yes | Configured priority factor label. |
| `status` | string | Yes | Foundation status. Contract v1 marks factors as not evaluated. |
| `snapshotSourceRefs` | array of string | Yes | Snapshot source references. |
| `confidenceSourceRefs` | array of string | Yes | Confidence source references. |
| `limitation` | string or null | Yes | Limitation explaining final formulas and targets are not approved. |

`recommendationPriorityEvaluation.sourceSnapshotMetadata` fields:

| Field | Type | Required |
| --- | --- | --- |
| `assessmentVersion` | string | Yes |
| `methodologyVersion` | string | Yes |
| `overallReadinessScore` | number | Yes |
| `evaluatedDimensions` | array of string | Yes |
| `questionCount` | integer | Yes |
| `totalWeight` | number | Yes |

`recommendationPriorityEvaluation.sourceConfidenceMetadata` fields:

| Field | Type | Required |
| --- | --- | --- |
| `assessmentVersion` | string | Yes |
| `methodologyVersion` | string | Yes |
| `evaluatedFactorIds` | array of string | Yes |
| `notEvaluatedFactorIds` | array of string | Yes |

### `executiveSummaryFoundation`

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `assessmentVersion` | string | Yes | Assessment input contract version. |
| `methodologyVersion` | string | Yes | Methodology version used by summary foundation. |
| `configuredSummarySections` | object | Yes | Mapping of configured summary section ID to section foundation output. |
| `evaluatedSectionIds` | array of string | Yes | Evaluated section IDs. Contract v1 emits an empty array. |
| `notEvaluatedSectionIds` | array of string | Yes | Not-yet-evaluated section IDs. |
| `sourceSnapshotMetadata` | object | Yes | Snapshot source metadata. |
| `sourceConfidenceMetadata` | object | Yes | Confidence source metadata. |
| `sourcePriorityMetadata` | object | Yes | Recommendation priority source metadata. |

`executiveSummaryFoundation.configuredSummarySections.*` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `sectionId` | string | Yes | Configured executive summary section identifier. |
| `label` | string | Yes | Configured section label. |
| `status` | string | Yes | Foundation status. Contract v1 marks sections as not evaluated. |
| `snapshotSourceRefs` | array of string | Yes | Snapshot source references. |
| `confidenceSourceRefs` | array of string | Yes | Confidence source references. |
| `prioritySourceRefs` | array of string | Yes | Priority source references. |
| `limitation` | string or null | Yes | Limitation explaining narrative and reporting behavior is not approved. |

`executiveSummaryFoundation.sourceSnapshotMetadata` fields:

| Field | Type | Required |
| --- | --- | --- |
| `assessmentVersion` | string | Yes |
| `methodologyVersion` | string | Yes |
| `overallReadinessScore` | number | Yes |
| `evaluatedDimensions` | array of string | Yes |
| `questionCount` | integer | Yes |
| `totalWeight` | number | Yes |

`executiveSummaryFoundation.sourceConfidenceMetadata` fields:

| Field | Type | Required |
| --- | --- | --- |
| `assessmentVersion` | string | Yes |
| `methodologyVersion` | string | Yes |
| `evaluatedFactorIds` | array of string | Yes |
| `notEvaluatedFactorIds` | array of string | Yes |

`executiveSummaryFoundation.sourcePriorityMetadata` fields:

| Field | Type | Required |
| --- | --- | --- |
| `assessmentVersion` | string | Yes |
| `methodologyVersion` | string | Yes |
| `configuredPriorityLevelIds` | array of string | Yes |
| `configuredPriorityFactorIds` | array of string | Yes |
| `evaluatedFactorIds` | array of string | Yes |
| `notEvaluatedFactorIds` | array of string | Yes |

## Version Metadata Structure

`versionMetadata` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `contractVersion` | string | Yes | Business Decision Package serialization contract version. |
| `assessmentVersion` | string | Yes | Assessment input contract version. |
| `methodologyVersion` | string | Yes | Governed methodology version. |
| `componentVersions` | object | Yes | Mapping of source component ID to component baseline version. |

Contract v1 component version keys:

- `decisionEvaluation`
- `businessReadinessSnapshot`
- `confidenceEvaluation`
- `recommendationPriorityEvaluation`
- `executiveSummaryFoundation`

Version metadata must not include generated build IDs, request IDs, timestamps,
or deployment-environment values.

## Audit Metadata Structure

`audit` fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `assessmentVersion` | string | Yes | Assessment input contract version. |
| `methodologyVersion` | string | Yes | Governed methodology version. |
| `sourceComponentIds` | array of string | Yes | Component IDs included in the package. |
| `evaluatedDimensions` | array of string | Yes | Readiness dimensions evaluated by the source Decision Engine output. |
| `questionCount` | integer | Yes | Evaluated question count copied from source audit data. |
| `totalWeight` | number | Yes | Total applied source evaluation weight. |

Audit metadata is package-level trace metadata. It must not introduce runtime
state, generated identifiers, timestamps, operator identifiers, deployment
metadata, persistence references, or HTTP metadata in contract v1.

## Limitations Structure

`limitations` is a required array of strings.

Contract v1 limitation values:

- `final-confidence-formulas-not-implemented`
- `final-confidence-level-assignment-not-implemented`
- `final-recommendation-assignment-not-implemented`
- `recommendation-generation-not-implemented`
- `service-decisions-not-implemented`
- `executive-reporting-not-implemented`
- `executive-narratives-not-implemented`
- `evidence-ingestion-not-implemented`
- `persistence-not-implemented`
- `api-exposure-of-snapshot-consumers-not-implemented`

Limitations must remain visible to downstream consumers. Consumers may display
or copy limitation values, but they must not remove or suppress them when using
the package as the deterministic Assessment Service output.

## Backward Compatibility Rules

Business Decision Package serialization must remain backward compatible within
contract v1.

Backward-compatible changes:

- Adding a new optional field through an approved additive contract update.
- Adding a new nested field only when it does not change the meaning of
  existing fields and is documented before implementation.
- Adding limitation values when a new limitation is explicitly approved and
  documented.

Backward-incompatible changes:

- Renaming any existing field.
- Removing any existing field.
- Changing field type.
- Changing field meaning.
- Changing deterministic ordering guarantees.
- Moving a field to a different owner.
- Adding runtime timestamps or generated identifiers to contract v1.
- Treating foundation limitation fields as final recommendations or decisions.

Backward-incompatible changes require a new serialization contract version,
updated architecture documentation, release documentation, migration guidance,
and deterministic contract tests.

## Serialization Invariants

The following invariants must hold for valid package serialization:

- Root fields match the contract v1 root structure.
- All required fields are present.
- Nullable fields are present even when their value is `null`.
- Tuple-backed source fields serialize as arrays.
- Mapping-backed source fields serialize as objects.
- Sorted mapping outputs remain sorted according to the ordering rules in this
  document.
- `businessReadinessSnapshot.overallReadiness.score` matches
  `decisionEvaluation.overallScore`.
- Package audit assessment and methodology versions match package version
  metadata.
- Package audit question count and total weight preserve source snapshot audit
  values.
- `versionMetadata.componentVersions` identifies every package source
  component.
- `limitations` remains non-empty while contract v1 limitations exist.
- No serialization field introduces API, HTTP, persistence, runtime timestamp,
  request identifier, generated identifier, service routing, recommendation
  generation, executive narrative, or executive report semantics.

## Consumer Expectations

Downstream consumers may:

- Read serialized package contents.
- Validate package contract, assessment, methodology, and component versions.
- Display deterministic outputs with appropriate labels and limitations.
- Link package contents to downstream evidence, reporting, workflow, or
  portfolio systems in downstream-owned records.
- Store a copy of the serialized package as an immutable assessment output when
  a future persistence architecture is approved.

Downstream consumers must not:

- Modify serialized package fields and present the result as the original
  Assessment Service output.
- Recompute Decision Engine outputs from serialized fields.
- Override readiness scores, dimension scores, confidence outputs, priority
  foundation outputs, or summary foundation outputs.
- Hide current limitations.
- Treat not-yet-evaluated foundation metadata as final recommendations,
  service decisions, executive narratives, or executive reports.
- Infer public directional assessment behavior from this internal executive
  assessment package.

## Future Additive Field Policy

Future additive fields are permitted only when all of the following are true:

- The field is approved through governed architecture documentation.
- The field owner is explicit.
- The field does not change the meaning of existing fields.
- The field does not introduce hidden business logic.
- The field does not introduce AI reasoning, recommendations, service routing,
  persistence, API behavior, or runtime state into the package contract.
- Deterministic ordering expectations are documented.
- Unit tests verify the new serialized shape.

Additive fields should be grouped under their owning component whenever
possible. Root-level additions require stronger governance because they expand
the canonical downstream contract.

## Explicit Non-Goals

This serialization contract does not define:

- API routes.
- Lambda handler behavior.
- HTTP request or response shape.
- OpenAPI.
- JSON Schema.
- Persistence tables, indexes, partitions, or storage lifecycle.
- Runtime timestamps.
- Request IDs.
- Generated identifiers.
- Evidence ingestion.
- Evidence repository behavior.
- Recommendation generation.
- Service routing.
- Service tier selection.
- Executive report generation.
- Executive narrative generation.
- Dashboard rendering.
- Portfolio aggregation.
- Public directional assessment serialization.

## Implementation Alignment Review

The current implementation in
`src/assessment/business_decision_package.py` aligns with this serialization
contract:

- Every root field emitted by `BusinessDecisionPackage.to_dict()` is documented.
- Every package-owned nested field emitted by package audit and version
  metadata serialization is documented.
- Sprint 3 nested component fields emitted by their existing `to_dict()`
  methods are documented.
- Deterministic ordering behavior is documented for sorted package-managed
  mappings and existing Sprint 3 component mappings.
- No undocumented root fields are emitted.
- No runtime metadata, generated identifiers, timestamps, API fields, HTTP
  fields, persistence fields, recommendation objects, service routing fields,
  executive narratives, or executive reports are emitted.

No implementation/documentation differences were identified during this
Milestone 3 review.
