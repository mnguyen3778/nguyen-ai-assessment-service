# Executive Runtime Response Contract Finalization v1

## 1. Established Facts

The Nguyen AI Assessment Service is the deterministic Business Decision Engine
for the Nguyen AI Executive Intelligence Platform.

The current executable runtime remains:

```text
POST /assessment
-> handle_assessment()
-> validate_assessment_request()
-> score_assessment()
-> AssessmentResponse
```

The current `AssessmentResponse` is public and placeholder-runtime specific.
It is not the future executive runtime response contract.

Sprint 4 established `BusinessDecisionPackage` as the canonical immutable
deterministic domain output.

Sprint 5 selected a minimal separate runtime response representation
containing the validated `BusinessDecisionPackage` serialization unchanged.
Sprint 5 rejected direct package serialization alone as the executive API
contract and rejected a projection as the baseline.

Sprint 6.8 finalized the external executive runtime error contract. Sprint
6.9 finalizes the successful executive runtime response contract only.

## 2. Dependencies

Sprint 6.1 established:

```text
assessmentVersion = nguyen-ai-executive-assessment-v1
```

Sprint 6.2 established:

```text
nguyen-ai-executive-assessment-v1
  ->
business-decision-methodology-v1
```

Sprint 6.3 established that no independent `inputContractVersion` is required
for v1.

Sprint 6.4 established that public and executive runtime paths require
distinct logical route, request-contract, validation, adapter, and response
boundaries.

Sprint 6.5 established that operational metadata remains outside
deterministic package truth.

Sprint 6.6 established that only a validated `BusinessDecisionPackage` may
become a successful executive result and that complete package serialization
must remain unchanged.

Sprint 6.7 established fail-closed internal failure semantics and prohibited
partial successful packages.

Sprint 6.8 established the external error contract and prohibited
`BusinessDecisionPackage` from appearing in error responses.

## 3. Response Ownership

The successful executive runtime response contract is owned by the Assessment
Service runtime/application boundary.

Ownership rules:

- The `BusinessDecisionPackage` owns deterministic business truth.
- The executive response envelope owns external response compatibility.
- The future executive adapter implements the response boundary but does not
  define business meaning.
- Downstream platform services consume the response but do not own Assessment
  Service response compatibility.
- Public `AssessmentResponse` remains owned by the existing public or
  placeholder runtime path.

## 4. BusinessDecisionPackage Relationship

The `BusinessDecisionPackage` remains the only deterministic source of
executive business truth in a successful executive response.

The successful response may contain package serialization. It must not:

- mutate package fields
- rename package fields
- reorder package fields outside package serialization rules
- transform package values
- flatten package sections into response fields
- duplicate scores, recommendations, summary sections, confidence, priority,
  audit, limitations, or version metadata outside the package
- add runtime metadata inside the package
- remove or suppress package limitations

The package is read-only input to the response boundary.

## 5. Response Envelope Decision

Successful executive responses must use a minimal response envelope.

Decision status:

- DECIDED: do not return `BusinessDecisionPackage` serialization directly as
  the entire runtime response.
- DECIDED: do not use a projection as the v1 successful response.
- DECIDED: use a minimal envelope that contains the validated package
  serialization unchanged.
- DECIDED: the envelope is not a delivery envelope, persistence record,
  workflow record, report, dashboard payload, or downstream platform object.

Rationale:

- Sprint 4 serialization is not an API contract.
- Sprint 5 selected a separate runtime response boundary.
- A response envelope gives consumers a stable response contract identity
  without replacing package identity.
- A projection would create a second representation of deterministic truth.

## 6. Final Successful Response Shape

Sprint 6.9 finalizes the conceptual v1 successful response shape:

```text
ExecutiveRuntimeSuccessResponse
  |
  |-- responseContractVersion
  |-- responseStatus
  |-- businessDecisionPackage
```

Required root fields:

| Field | Required | Owner | Meaning |
| --- | --- | --- | --- |
| `responseContractVersion` | Yes | Executive runtime response contract | Identifies the external executive runtime response contract shape. |
| `responseStatus` | Yes | Executive runtime response contract | Identifies successful response status without changing package truth. |
| `businessDecisionPackage` | Yes | Business Decision Package | Contains canonical package serialization unchanged. |

Root field order for deterministic response-body serialization should be:

1. `responseContractVersion`
2. `responseStatus`
3. `businessDecisionPackage`

This document defines architecture. It does not implement Python models,
serializers, or HTTP handlers.

## 7. Response Contract Version

The successful executive response contract version is:

```text
executive-runtime-response-v1
```

The serialized field carrying this value is:

```text
responseContractVersion
```

This version identifies the external executive runtime response envelope shape.

It does not identify:

- package contract shape
- executive assessment input contract
- methodology configuration
- component baselines
- runtime request
- Lambda invocation
- persistence record
- delivery event
- customer
- timestamp

## 8. Response Status

The `responseStatus` object is required for successful executive responses.

It exists to prevent consumers from mistaking a structurally valid package for
production-authoritative executive intelligence.

Required conceptual fields:

| Field | Required | Allowed v1 Values | Meaning |
| --- | --- | --- | --- |
| `packageValidation` | Yes | `VALIDATED` | Package validation passed before response construction. |
| `runtimeEligibility` | Yes | `RUNTIME_ELIGIBLE` | The response is being emitted through an approved executive runtime context. |
| `exposure` | Yes | `EXPOSURE_ELIGIBLE` | The package is approved to cross this executive response boundary. |
| `productionAuthority` | Yes | `PRODUCTION_AUTHORITATIVE`, `NOT_PRODUCTION_AUTHORITATIVE` | Whether the result is approved as final production-authoritative executive intelligence. |

`responseStatus` is response-boundary governance metadata. It must not be
copied into `BusinessDecisionPackage`.

`responseStatus` must not contain free-form warnings, diagnostics, exception
details, methodology explanations, recommendations, or runtime identifiers.

## 9. Deterministic Truth Boundary

Deterministic business truth lives inside `businessDecisionPackage`.

The envelope must not introduce a second source of truth.

Rules:

- Do not duplicate `overallScore` outside the package.
- Do not duplicate readiness dimensions outside the package.
- Do not duplicate confidence factor outputs outside the package.
- Do not duplicate recommendation-priority outputs outside the package.
- Do not duplicate executive summary sections outside the package.
- Do not duplicate package limitations outside the package.
- Do not duplicate package version metadata outside the package.
- Do not add recommendations, service decisions, executive narrative, or
  report content outside the package.

Clients must parse the response envelope first, then parse
`businessDecisionPackage` as the deterministic business artifact.

## 10. Runtime Metadata Placement

Operational runtime metadata must not appear inside `businessDecisionPackage`.

For v1 successful response body, operational runtime metadata also does not
appear as a root response field.

Excluded from the successful response body:

- request ID
- correlation ID
- trace ID
- Lambda invocation ID
- API Gateway request ID
- runtime timestamp
- processing duration
- deployment version
- environment identifier
- persistence identifier
- delivery identifier
- workflow identifier

Operational correlation may exist outside the successful response body in
transport headers, logs, telemetry, or downstream operational systems if later
implementation governance approves it.

Runtime metadata is optional operational context. It must not affect
deterministic equality, response status, package validation, package identity,
or package serialization.

## 11. Version Ownership Model

Version ownership remains separated:

| Version Identity | Owner | Meaning |
| --- | --- | --- |
| `responseContractVersion` | Executive runtime response contract | External response envelope compatibility. |
| Package `versionMetadata.contractVersion` | Business Decision Package | Package shape and serialization compatibility. |
| Package `versionMetadata.assessmentVersion` | Executive input contract | Assessment input contract that produced the package. |
| Package `versionMetadata.methodologyVersion` | Business Decision Methodology | Methodology applied during deterministic evaluation. |
| Package `versionMetadata.componentVersions` | Package/component governance | Component baselines represented inside the package. |

Changing runtime response envelope shape is governed by
`responseContractVersion`.

Changing package serialization is governed by package `contractVersion`.

Changing executive input semantics is governed by `assessmentVersion`.

Changing methodology is governed by `methodologyVersion`.

Changing component baselines is governed by `componentVersions`.

No version identity replaces another.

## 12. Success Invariant

A successful executive runtime response may be emitted only when all of the
following are true:

1. Executive input is validated and canonicalized.
2. Executive `assessmentVersion` is supported.
3. Methodology binding is resolved and valid.
4. Deterministic Decision Engine evaluation completes.
5. Downstream deterministic foundations complete.
6. `BusinessDecisionPackage` assembly completes.
7. `BusinessDecisionPackageValidation` passes.
8. Package exposure is approved for the current executive runtime context.
9. The response can accurately state `responseStatus`.

No partial success exists.

If any condition fails, the successful response contract is not used.

## 13. Error Separation

Successful responses and error responses are mutually exclusive.

Rules:

- A successful response must not contain an `error` object.
- An error response must not contain `businessDecisionPackage`.
- A response must not contain both success and error fields.
- A package blocked by governance must not be serialized as a successful
  response.
- A package that failed validation must not be serialized as a successful
  response.
- Partial deterministic results must not be serialized in successful or error
  responses.

Sprint 6.8 governs external error codes and HTTP status mapping.

Sprint 6.9 governs only the successful response shape.

## 14. Methodology-Pending Behavior

`METHODOLOGY_PENDING` is not automatically a software failure.

A successful response may be emitted for a controlled non-production-authority
context only when package exposure governance permits it.

In that case:

- `responseStatus.productionAuthority` must be `NOT_PRODUCTION_AUTHORITATIVE`.
- package limitations must remain visible inside `businessDecisionPackage`.
- the response must not imply final weights, thresholds, confidence formulas,
  recommendation-priority assignment, recommendations, service decisions, or
  executive narratives are approved.

If the caller or runtime context requires production-authoritative output and
the methodology cannot support it, the successful response contract is not
used. Sprint 6.8 maps that condition to `EXECUTIVE_RESULT_UNAVAILABLE`.

## 15. Warnings, Notices, and Diagnostics

The v1 successful response does not include free-form warnings, notices, or
diagnostics.

Governance and methodology limitations belong in:

- package `limitations`
- response `productionAuthority` status
- future documentation or downstream presentation layers

Diagnostics belong in:

- internal logs
- telemetry
- future error responses where governed

The successful response must not contain:

- exception text
- validation issues
- internal component diagnostics
- package validation details
- support-only notes
- hidden methodology notes

## 16. Public vs Executive Separation

The current public `AssessmentResponse` remains separate from the future
executive response.

Public response fields that must not define executive response identity:

- `requestId`
- placeholder `readinessLevel`
- placeholder `categoryScores`
- placeholder `recommendations`
- `modelInvoked`
- `persisted`

The current public `POST /assessment` route must not return
`ExecutiveRuntimeSuccessResponse`.

The future executive route must not return public `AssessmentResponse`.

Public directional assessment payloads must never be promoted, mapped, or
expanded into executive response output.

## 17. Compatibility Strategy

Consumers must inspect response compatibility before consuming package truth.

Minimum client sequence:

1. Confirm `responseContractVersion` is recognized.
2. Confirm the response is the success variant.
3. Inspect `responseStatus`.
4. Parse `businessDecisionPackage`.
5. Confirm package `versionMetadata.contractVersion` is recognized.
6. Confirm package `versionMetadata.assessmentVersion` is recognized.
7. Confirm package `versionMetadata.methodologyVersion` is recognized.
8. Confirm package `versionMetadata.componentVersions` are recognized or
   governed by a compatibility policy.
9. Inspect package limitations.
10. Refuse production-authoritative use unless `responseStatus` permits it.

Unknown response contract versions must be rejected or quarantined by
consumers.

Unknown package contract versions must be handled according to package
compatibility policy, not inferred from the response envelope.

## 18. Success and Error Response Family

Success and error responses belong to one executive runtime response contract
family:

```text
executive-runtime-response-v1
```

They are mutually exclusive variants of that family.

Sprint 6.8 governs the error variant's external error codes and status
mapping.

Sprint 6.9 finalizes the success variant fields.

No separate `errorContractVersion` is introduced.

## 19. Future Evolution Strategy

Future response evolution must preserve deterministic package truth.

Backward-compatible response changes may include additive optional envelope
metadata only when all of the following are true:

- package serialization remains unchanged
- existing root fields keep their meaning
- deterministic package truth is not duplicated
- runtime metadata does not become package identity
- consumers can ignore the additive field safely
- the change is documented and tested

Breaking response changes require a new `responseContractVersion`.

Breaking response changes include:

- renaming root response fields
- removing required root response fields
- changing `responseStatus` meaning
- changing package placement
- replacing package serialization with a projection
- adding successful-response operational metadata that consumers must process
- allowing partial packages
- mixing success and error fields

Package serialization changes require package `contractVersion` review. They
do not automatically require a response contract version change unless the
response envelope shape, package placement, or package compatibility policy
also changes.

Runtime metadata changes outside the response body do not require package
version changes.

Adding runtime metadata to the successful response body would require response
contract review and likely a new `responseContractVersion`.

## 20. Open Implementation Decisions

The following decisions remain open after Sprint 6.9:

- Python response model name and location.
- Serializer implementation strategy.
- Exact implementation type for `responseStatus` values.
- Whether canonical JSON serialization is required for response-body testing.
- Whether operational correlation appears in headers, logs, telemetry, or not
  at all.
- Executive route URL.
- Executive handler and adapter implementation.
- Orchestrator implementation.
- Auth and authorization integration.
- CORS and API Gateway response mechanics.
- Test strategy for response contract implementation.

## 21. Explicit Non-Goals

Sprint 6.9 does not implement:

- Python models
- response serializers
- handlers
- routes
- Lambda changes
- API Gateway changes
- orchestrator
- package changes
- package validation changes
- public runtime changes
- error response implementation
- runtime metadata implementation
- persistence
- delivery envelope
- dashboards
- reports
- recommendation generation
- service routing
- evidence repositories
- portfolio intelligence
- Bedrock or LLM behavior
- methodology changes

## 22. Conditions Before Implementation

Before implementing the executive response contract, the repository must have:

- approved executive route and adapter boundary
- approved executive input validator implementation plan
- approved orchestration implementation plan
- approved mapping from orchestrator success to response construction
- approved test strategy for success and error variants
- explicit review of the current package limitation
  `api-exposure-of-snapshot-consumers-not-implemented`
- confirmation that non-production-authoritative responses are allowed for the
  targeted runtime context, if methodology remains pending

Implementation must not begin from this document alone.
