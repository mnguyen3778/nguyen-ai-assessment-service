# Business Decision Package API Exposure Governance v1

## 1. Established Frozen Facts

Sprint 4 established `BusinessDecisionPackage` as the canonical immutable deterministic domain output of the Nguyen AI Assessment Service.

Sprint 4 also established that package serialization is a deterministic domain serialization contract, not an API contract, HTTP schema, persistence schema, OpenAPI schema, or delivery envelope.

Sprint 5 established that a future executive runtime response should use a minimal separate runtime response representation containing the validated `BusinessDecisionPackage` serialization unchanged.

Sprint 5 did not select direct package serialization alone as the executive API contract.

Sprint 5 did not select a projection as the baseline response strategy.

Sprint 6.1 established:

- `assessmentVersion = nguyen-ai-executive-assessment-v1`
- the public assessment identity remains separate from the executive assessment identity

Sprint 6.2 established:

- `nguyen-ai-executive-assessment-v1 -> business-decision-methodology-v1`
- the service resolves the authoritative methodology version
- caller preference does not determine methodology execution

Sprint 6.3 established:

- no independent `inputContractVersion` is required for v1
- `assessmentVersion` remains the canonical executive input compatibility identity

Sprint 6.4 established:

- future executive runtime requires a distinct route boundary
- public and executive request, validation, and adapter boundaries are distinct
- current `POST /assessment` runtime remains unchanged

Sprint 6.5 established:

- runtime, transport, observability, and persistence metadata remain outside `BusinessDecisionPackage`
- runtime metadata cannot alter package identity, serialization, or validation
- identical deterministic inputs and configuration must produce identical package serialization

## 2. Sprint 6.1-6.5 Dependencies

This document depends on the following governed decisions:

- Executive package exposure is only for the internal executive assessment family identified by `nguyen-ai-executive-assessment-v1`.
- The methodology version is bound by the service, not selected by the caller.
- The package remains the canonical deterministic domain artifact.
- The package does not absorb runtime metadata.
- The public 12-question runtime does not expose the executive package.
- The future executive response contract remains separate from package serialization.

## 3. Definition of API Exposure

`BusinessDecisionPackage` API exposure means a future executive runtime boundary may include the canonical package serialization inside a governed executive runtime response.

API exposure does not mean:

- package serialization alone becomes the API contract
- every package is safe to expose
- package validation proves production authority
- package fields may be filtered, renamed, or rewritten
- runtime metadata may be inserted into the package
- public runtime responses may emit executive package output
- downstream consumers may reinterpret deterministic truth

API exposure is a boundary governance decision, not a business methodology approval decision.

## 4. Package Validity vs Exposure Eligibility

Package validity means `BusinessDecisionPackageValidation` confirms structural and contract integrity.

Exposure eligibility means a future executive runtime boundary is allowed to include a validated package in the executive runtime response.

Package validity is required before exposure eligibility.

Package validity is not sufficient by itself to establish exposure eligibility.

Exposure eligibility additionally depends on:

- successful future executive runtime orchestration
- use of the executive route and adapter boundary
- package validation success
- preservation of package serialization unchanged
- visibility of package limitations
- compliance with public/executive separation
- compliance with runtime metadata exclusion rules
- explicit response contract governance

## 5. Runtime Eligibility vs Production Authority

Runtime eligibility means a future implementation is approved to produce and return an executive runtime result.

Production authority means the result is approved to represent final authoritative executive business intelligence.

A structurally valid package may be:

- deterministic
- reproducible
- contract-valid
- foundation-complete

while still not being production-authoritative.

Production authority remains blocked until unresolved executive methodology decisions are approved, versioned, documented, and validated.

## 6. Required Package Validation State

Only a validated `BusinessDecisionPackage` may cross the future executive runtime boundary as a successful executive result.

The required validation state is:

- all required package components are present
- serialized root fields conform to the Sprint 4 serialization contract
- version metadata is internally consistent
- audit metadata is internally consistent
- limitations are present and unchanged
- source component versions are preserved
- no unexpected serialized fields are present
- package validation result is successful

An unvalidated package must not be exposed as a successful executive result.

A partially assembled package must not be exposed as a successful executive result.

A validation-failed package must not be exposed as a successful executive result.

## 7. Exposure Authority and Ownership

Exposure authority belongs to the future executive application/runtime boundary after successful orchestration and package validation.

The Decision Engine owns deterministic evaluation truth. It does not own API exposure.

Sprint 3 downstream foundations preserve and project deterministic outputs. They do not own API exposure.

`BusinessDecisionPackage` assembly owns deterministic package construction. It does not decide runtime exposure eligibility.

`BusinessDecisionPackageValidation` owns structural contract validation. It does not decide production authority.

The future executive adapter enforces the governed runtime boundary. It must not change deterministic package meaning.

Downstream consumers do not own package exposure eligibility and must not rewrite deterministic package truth after receipt.

## 8. Unchanged Serialization Requirement

For v1 exposure governance, the complete validated `BusinessDecisionPackage` serialization is the governed payload to be contained unchanged in the future executive runtime response.

Unchanged serialization means:

- canonical root field names are preserved
- canonical nesting is preserved
- canonical values are preserved
- deterministic ordering rules are preserved
- limitations remain visible
- version metadata remains visible
- audit metadata remains visible
- no package fields are omitted
- no package fields are renamed
- no deterministic values are transformed
- no runtime-generated fields are inserted into the package

The future executive response may wrap or contain the package according to the Sprint 5 response strategy, but the package itself remains unchanged.

## 9. Version Identity Preservation

The following package version identities must remain visible and unchanged when the package is exposed:

- `contractVersion`
- `assessmentVersion`
- `methodologyVersion`
- `componentVersions`

Runtime response version identity, if introduced later, must not replace or reinterpret package version identity.

Runtime metadata must not alter package version identity.

Consumer compatibility must begin by recognizing package version identity before treating package content as consumable deterministic truth.

## 10. Prohibited Transformations

API exposure does not permit:

- selecting only portions of the package as the v1 governed payload
- dropping package fields
- renaming package fields
- rewriting package values
- reordering serialized structures where ordering is contractually defined
- adding runtime metadata inside the package
- adding timestamps inside the package
- adding request IDs inside the package
- adding trace or correlation identifiers inside the package
- adding persistence or delivery identifiers inside the package
- recalculating scores
- recalculating dimensions
- recalculating confidence
- assigning recommendation priority
- generating recommendations
- generating executive narratives
- selecting services
- changing limitations
- hiding methodology-pending status
- converting package content into a projection without a separate governed contract

If exposure requires any prohibited transformation, v1 exposure remains blocked until a future explicitly governed architecture decision resolves the conflict.

## 11. Projection, Filtering, and Redaction Governance

Sprint 5 did not select a projection as the baseline executive response strategy.

Therefore, v1 exposure does not permit filtering, redaction, partial package responses, or representational projections of the package as the governed executive result.

If a future security, privacy, product, or platform requirement requires selective exposure, that requirement must be handled by one of the following governed actions:

- block exposure until the package contract is revised in a new version
- define a separate governed projection contract
- define a separate downstream presentation/reporting contract outside the Assessment Service
- revise the executive runtime response contract in a future version

Filtering or redaction must not be applied silently to canonical package serialization.

## 12. Security and Information-Exposure Findings

Repository evidence shows the current `BusinessDecisionPackage` contains deterministic assessment outputs, downstream foundation outputs, audit metadata, version metadata, and explicit limitations.

Repository evidence does not show current package fields containing:

- raw source payloads
- organization profile data
- respondent personal data
- request IDs
- trace IDs
- Lambda invocation IDs
- runtime timestamps
- HTTP headers
- persistence identifiers
- delivery identifiers
- evidence repository records
- credentials
- secrets

Repository evidence does identify an explicit limitation:

- `api-exposure-of-snapshot-consumers-not-implemented`

That limitation means executive API exposure is not currently implemented and must remain visible until a future governed increment updates exposure status.

No current package field is explicitly documented as sensitive, prohibited from exposure, or internal-only. If future review identifies such a field, exposure must remain blocked until the conflict is governed. The package must not be silently filtered.

## 13. Methodology-Readiness Constraints

Package exposure governance does not approve unresolved methodology.

The following remain outside Sprint 6.6:

- final question weights or explicit approval of equal weighting
- final readiness thresholds
- final readiness-level assignment
- final scoring semantics
- risk caps
- cross-dimension dependency rules
- final confidence formulas
- final confidence-level assignment
- final recommendation-priority formulas
- final recommendation-priority assignment
- recommendation generation rules
- service decision rules
- final executive-summary methodology

`business-decision-methodology-v1` may have deterministic version identity while remaining methodology-pending for production authority.

## 14. Internal, Testing, and Production Exposure

Controlled internal or test exposure of a validated package may be acceptable only if future runtime governance clearly marks the result as non-authoritative where methodology remains pending.

Production executive delivery requires more than package validation.

Production executive delivery requires:

- runtime implementation approval
- response contract finalization
- exposure governance compliance
- methodology readiness for the emitted conclusions
- visible limitations
- consumer compatibility rules
- public/executive runtime separation

No package produced under methodology-pending status may be represented as final production-authoritative executive intelligence.

## 15. Runtime Metadata Exclusion

Runtime metadata remains outside `BusinessDecisionPackage`.

The following must not be inserted into package serialization because an API invocation occurred:

- request ID
- correlation ID
- trace ID
- Lambda invocation ID
- API Gateway request ID
- HTTP route or method
- HTTP headers
- API receipt timestamp
- processing timestamp
- deployment identifier
- environment identifier
- persistence key
- delivery identifier
- workflow identifier
- report-generation timestamp

Runtime metadata may be used for logging, tracing, security investigation, observability, and operational support outside package truth.

## 16. Public / Executive Exposure Boundary

The current public runtime remains:

```text
POST /assessment
-> handle_assessment()
-> validate_assessment_request()
-> score_assessment()
-> AssessmentResponse
```

This public runtime must not expose `BusinessDecisionPackage`.

The future executive runtime requires its own route boundary, adapter boundary, validation boundary, orchestration boundary, and response contract.

Public assessment payloads must never be mapped, inferred, expanded, aliased, or promoted into executive package exposure.

Executive package exposure must never be routed through the current public placeholder scoring path.

## 17. Downstream Immutability Expectations

Downstream consumers may consume the package as deterministic truth.

Downstream consumers must not:

- mutate package fields
- recompute deterministic outputs
- replace package version identity
- hide package limitations
- reinterpret methodology-pending outputs as production-authoritative
- use AI or probabilistic reasoning to change deterministic package truth
- treat a runtime response wrapper as a replacement for package identity

Downstream systems receiving a package must preserve the package as received if they retain or display deterministic assessment truth.

## 18. Permitted Downstream Enrichment

Downstream consumers may enrich around the package in downstream-owned records.

Permitted downstream enrichment may include:

- evidence links
- analyst notes
- workflow state
- report-generation state
- client metadata
- portfolio relationships
- delivery status
- operational correlation metadata

Such enrichment must remain outside the canonical package and must not overwrite deterministic package truth.

## 19. Platform Ownership Exclusions

BusinessDecisionPackage API exposure does not move downstream platform responsibilities into the Assessment Service.

The Assessment Service does not own:

- evidence ingestion
- evidence repositories
- executive dashboards
- executive reports
- portfolio intelligence
- Portfolio Digital Twin capabilities
- workflow orchestration
- case management
- remediation execution
- client delivery systems
- AI-generated business decisions
- Bedrock decision making
- recommendation generation
- service routing

Future platform services may consume the package, but they must not rewrite deterministic truth inside it.

## 20. Dependencies on Sprint 6.7-6.9

Sprint 6.7 must define deterministic internal failure semantics for cases where package exposure cannot occur because input validation, version binding, orchestration, package assembly, or package validation fails.

Sprint 6.8 must define the executive runtime error contract corresponding to governed runtime failures without exposing partial package truth as a successful result.

Sprint 6.9 must finalize the executive runtime response contract, including response identity and exact field names, while containing the validated package serialization unchanged.

Sprint 6.9 must also determine how to handle the current package limitation:

- `api-exposure-of-snapshot-consumers-not-implemented`

That limitation cannot be silently removed or hidden.

## 21. Explicit Non-Goals

Sprint 6.6 does not implement:

- executive API exposure
- executive response models
- package projections
- package filtering
- package redaction
- package mutation
- package eligibility flags
- new package fields
- executive route
- executive handler
- executive adapter
- orchestration
- runtime metadata
- persistence
- API Gateway changes
- Lambda changes
- authentication or authorization
- methodology changes
- recommendation generation
- service routing
- executive narratives
- executive reports
- dashboards
- evidence repositories
- portfolio intelligence
- Digital Twin capabilities
- Bedrock or LLM reasoning

## 22. Still-Unresolved Decisions

The following decisions remain unresolved after Sprint 6.6:

- deterministic internal failure result strategy
- executive runtime error contract
- exact executive runtime response field names
- executive runtime response contract version
- exact response placement of package serialization
- runtime metadata placement in future transport or operational systems
- governance action required to update the current API-exposure limitation
- production-authority approval for methodology-pending outputs
- authorization and access-control design for any future executive route

These decisions must be resolved in later governed increments before executive runtime implementation is treated as complete.
