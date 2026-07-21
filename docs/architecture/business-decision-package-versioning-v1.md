# Business Decision Package Versioning v1

## Purpose

This document defines deterministic identity and versioning semantics for the
`BusinessDecisionPackage`.

The Business Decision Package is the canonical immutable output contract of the
Nguyen AI Assessment Service. Its identity must be reproducible from governed
contract and source version metadata. It must not depend on runtime-generated
identifiers, timestamps, persistence keys, API routes, HTTP resources, Lambda
execution context, sessions, or database records.

This document defines identity semantics only. It does not introduce a Python
implementation change, API design, persistence model, or downstream consumer
workflow.

## Identity Principles

Business Decision Package identity is based on deterministic version semantics:

- Contract identity comes from the package contract version.
- Input-contract identity comes from the assessment version.
- Methodology identity comes from the governed methodology version.
- Component identity comes from the component version map.
- Source consistency comes from package audit metadata and source component
  version metadata.

The package does not require a unique runtime identifier to be meaningful. A
valid package is identified by its immutable contents and governed version
metadata.

Identity must remain:

- Deterministic.
- Reproducible.
- Explainable.
- Traceable.
- Independent of infrastructure runtime.
- Independent of downstream persistence.

## Package Identity Model

The canonical package identity model is the deterministic identity tuple:

```text
BusinessDecisionPackageIdentity
  =
(
  contractVersion,
  assessmentVersion,
  methodologyVersion,
  componentVersions
)
```

This tuple identifies the package contract family and the governed source
versions required to interpret the package.

The tuple is not a globally unique event identifier. Multiple packages may have
the same identity tuple when they were produced using the same contract,
assessment version, methodology version, and component versions. Their
serialized business outputs may still differ because assessment answers differ.

If a downstream platform needs to distinguish individual assessment events,
that responsibility belongs outside the Business Decision Package contract and
must be defined by a future approved persistence or workflow architecture.

## Contract Version

`contractVersion` identifies the Business Decision Package contract shape.

Current value:

```text
business-decision-package-v1
```

The contract version governs:

- Root package structure.
- Package-owned audit metadata structure.
- Package-owned limitation structure.
- Package-owned version metadata structure.
- Serialization shape defined by
  `docs/architecture/business-decision-package-serialization-contract-v1.md`.
- Backward compatibility expectations for downstream consumers.

The contract version does not identify:

- A runtime package instance.
- A persistence record.
- An API resource.
- A Lambda invocation.
- A specific customer or assessment event.
- A timestamped release artifact.

## Assessment Version

`assessmentVersion` identifies the assessment input contract used to construct
the package output.

The assessment version exists so downstream consumers can distinguish the
executive assessment input contract that produced the deterministic output. It
must remain separate from the public directional assessment contract.

Assessment version governance rules:

- Public directional assessment versions and internal executive assessment
  versions must remain distinct.
- Public question IDs must not be silently mapped into canonical executive
  assessment question IDs.
- Changing the executive assessment input contract requires governed
  documentation, implementation review, and tests.
- A package produced from one assessment version must not be presented as if it
  came from another assessment version.

## Methodology Version

`methodologyVersion` identifies the governed Business Decision Methodology used
by the deterministic evaluation pipeline and Sprint 3 foundation outputs.

Current methodology baseline:

```text
business-decision-methodology-v1
```

The methodology version governs:

- Canonical question IDs.
- Readiness dimensions.
- Evidence categories.
- Answer types and normalization ranges.
- Placeholder question weights.
- Confidence factor catalog.
- Recommendation priority catalog.
- Executive summary section catalog.
- Methodology-owned vocabulary and validation behavior.

Methodology version changes require governed methodology documentation,
configuration updates, deterministic tests, and release documentation before
they can affect package output.

## Component Version Relationships

`componentVersions` identifies the source component baselines included in the
package.

Contract v1 component keys:

| Component Key | Expected Baseline | Ownership |
| --- | --- | --- |
| `decisionEvaluation` | `assessment-decision-engine-v2` | Decision Engine |
| `businessReadinessSnapshot` | `sprint3-snapshot-foundation-v1` | Snapshot Foundation |
| `confidenceEvaluation` | `sprint3-confidence-foundation-v1` | Confidence Foundation |
| `recommendationPriorityEvaluation` | `sprint3-recommendation-priority-foundation-v1` | Recommendation Priority Foundation |
| `executiveSummaryFoundation` | `sprint3-executive-summary-foundation-v1` | Executive Summary Foundation |

Component versions tell consumers which governed component baselines produced
or shaped each package section. They do not authorize consumers to recompute or
override component outputs.

The package audit `sourceComponentIds` must identify the same component family
represented by `versionMetadata.componentVersions`.

## Version Compatibility Rules

Consumers should evaluate compatibility in this order:

1. Validate `contractVersion`.
2. Validate `assessmentVersion`.
3. Validate `methodologyVersion`.
4. Validate required `componentVersions` keys.
5. Validate package audit versions align with version metadata.
6. Validate required serialized fields defined by the serialization contract.

Compatible package consumption requires the consumer to understand the package
contract version and tolerate documented additive fields if its consumer policy
allows them.

Consumers must reject or quarantine a package when:

- The `contractVersion` is unknown.
- Required version metadata is missing.
- Package audit versions conflict with version metadata.
- Required component version keys are missing.
- A component version is unknown and the consumer does not have an approved
  compatibility policy for it.
- The package violates the serialization contract for its declared contract
  version.

## Identity Invariants

The following invariants define valid contract v1 identity:

- `versionMetadata.contractVersion` is present and non-empty.
- `versionMetadata.assessmentVersion` is present and non-empty.
- `versionMetadata.methodologyVersion` is present and non-empty.
- `versionMetadata.componentVersions` contains every required component key.
- `audit.assessmentVersion` matches `versionMetadata.assessmentVersion`.
- `audit.methodologyVersion` matches `versionMetadata.methodologyVersion`.
- Source Sprint 3 outputs share the same assessment version.
- Source Sprint 3 outputs share the same methodology version.
- `componentVersions` values are governed baseline identifiers, not runtime
  identifiers.
- Identity metadata does not include timestamps, UUIDs, request IDs, session
  IDs, database keys, HTTP resource identifiers, Lambda invocation identifiers,
  or generated names.

## Backward Compatibility Requirements

Backward compatibility is required within contract v1.

The following changes are backward compatible only when documented and tested
before implementation:

- Adding an optional field that does not change existing field meaning.
- Adding a new component version key only when the root contract remains
  compatible and consumers are not required to process the new component.
- Adding limitation metadata for a newly documented limitation.
- Adding downstream-readable metadata that is deterministic, non-runtime, and
  owned by the Assessment Service contract.

The following changes are backward incompatible:

- Renaming a version field.
- Removing a version field.
- Changing the meaning of `contractVersion`, `assessmentVersion`,
  `methodologyVersion`, or `componentVersions`.
- Replacing deterministic version identity with generated identifiers.
- Requiring consumers to infer identity from timestamps, persistence records,
  API paths, or runtime context.
- Changing the package root shape defined by the serialization contract.
- Changing component ownership.
- Changing public and executive assessment boundary semantics.

Backward-incompatible changes require a new contract version.

## Forward Compatibility Expectations

Downstream consumers should treat unknown future contract versions as
unsupported unless a governed compatibility policy exists.

Consumers may tolerate additive fields in known contract versions only when:

- Required fields remain present.
- Existing field meanings remain unchanged.
- Existing deterministic ordering rules remain valid.
- New fields do not introduce runtime identity, timestamps, API concerns,
  persistence concerns, AI reasoning, recommendations, service routing, or
  executive reporting semantics into contract v1.

Forward compatibility is a consumer concern. The Assessment Service must still
document and test every package contract change before release.

## Rules for Future Version Evolution

Future version evolution must follow these rules:

1. Define the architectural reason for the version change.
2. Identify whether the change is contract-level, assessment-level,
   methodology-level, or component-level.
3. Update the relevant architecture document before implementation.
4. Update serialization documentation when serialized shape changes.
5. Add or update deterministic contract tests.
6. Preserve explicit limitation metadata until a governed capability replaces
   the limitation.
7. Publish release documentation for the version change.
8. Provide migration guidance for downstream consumers when compatibility is
   affected.

Version changes must not be used to bypass methodology governance. Business
methodology still belongs in governed methodology documentation and
configuration.

## Explicit Non-Goals

This versioning document does not define:

- UUID generation.
- Runtime package IDs.
- Persistence identifiers.
- Database primary keys.
- API resource identifiers.
- HTTP route naming.
- Lambda invocation identifiers.
- Request IDs.
- Session IDs.
- Timestamps.
- Customer identifiers.
- Evidence record identifiers.
- Workflow identifiers.
- Portfolio identifiers.
- Storage lifecycle rules.
- OpenAPI.
- JSON Schema.
- API response envelopes.
- Public directional assessment translation.
- Recommendation generation.
- Service routing.
- Executive narrative generation.
- Executive report generation.

Any future need for these concepts must be addressed by a separate approved
architecture document outside the deterministic package identity model.

## Relationship to Downstream Consumers

The Business Decision Package is the deterministic handoff contract from the
Assessment Service to downstream platform components.

Downstream consumers may use package identity metadata to:

- Confirm they understand the package contract shape.
- Confirm the assessment version.
- Confirm the methodology version.
- Confirm component baseline versions.
- Route package handling to compatible downstream logic.
- Preserve audit and reproducibility context.

Downstream consumers may not:

- Mutate package identity metadata.
- Replace package identity with downstream persistence IDs.
- Treat a persistence ID as the package identity.
- Use timestamps or runtime context to reinterpret deterministic outputs.
- Change Assessment Service outputs to fit downstream workflow needs.
- Hide version or limitation metadata from downstream audit flows.

Downstream systems that persist, display, enrich, or aggregate package output
must store their own metadata separately from the immutable Assessment Service
package.

## Governance Requirements for Future Breaking Changes

Breaking changes require formal governance before implementation.

Required governance artifacts:

- Updated Business Decision Package contract architecture.
- Updated serialization contract.
- Updated versioning architecture.
- Release documentation.
- Migration guidance for downstream consumers.
- Deterministic contract tests.
- Compatibility review for known consumers.
- Explicit approval of any methodology change, if methodology is affected.

Breaking changes must not be implemented solely as code changes. They must be
introduced through documented architecture, test coverage, and release
governance.

## Implementation Readiness Review

The current implementation in
`src/assessment/business_decision_package.py` supports this versioning strategy.

Current implementation alignment:

- `BusinessDecisionPackageVersionMetadata` includes `contract_version`,
  `assessment_version`, `methodology_version`, and `component_versions`.
- `BusinessDecisionPackageAudit` includes `assessment_version`,
  `methodology_version`, `source_component_ids`, evaluated dimensions, question
  count, and total weight.
- Package construction validates source assessment-version consistency.
- Package construction validates source methodology-version consistency.
- Package construction validates alignment between `DecisionEvaluationResult`
  and `BusinessReadinessSnapshot`.
- The implementation does not generate UUIDs, timestamps, request IDs,
  persistence keys, API identifiers, session identifiers, or Lambda-specific
  metadata.

No implementation changes are required to support this approved versioning
strategy.

Recommended future work:

- Add deterministic contract tests that assert the identity invariants in this
  document when Milestone 4 moves from architecture documentation into
  implementation validation.
- Define downstream compatibility review procedures before exposing the package
  outside the Assessment Service repository.
