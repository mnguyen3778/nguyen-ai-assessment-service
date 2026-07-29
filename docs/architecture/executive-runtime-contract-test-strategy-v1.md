# Executive Runtime Contract Test Strategy v1

## 1. Purpose

This document defines the governance test strategy for a future executive
runtime implementation of the Nguyen AI Assessment Service.

Sprint 6.10 answers:

```text
Given the Sprint 6 executive runtime contracts, what must future
implementation prove before the executive runtime can be considered
contract-conformant?
```

This is not an executable test implementation. It defines required
verification categories, contract invariants, negative cases, regression
coverage, compatibility expectations, release gates, and audit evidence for
future implementation work.

Passing the current repository test suite remains necessary, but it is not
sufficient to prove future executive runtime readiness. Future executive
runtime implementation must add tests that prove the contracts established by
Sprint 6.1 through Sprint 6.9.

## 2. Dependencies

This strategy depends on the frozen Sprint 4 and Sprint 5 baselines and the
completed Sprint 6.1 through Sprint 6.9 architecture.

Sprint 4 established:

- `BusinessDecisionPackage` as the canonical immutable deterministic domain
  output.
- `BusinessDecisionPackage` serialization as a deterministic package
  serialization contract, not an API contract.
- Package identity as:

```text
contractVersion
assessmentVersion
methodologyVersion
componentVersions
```

- `BusinessDecisionPackageValidation` as structural package contract
  validation.

Sprint 5 established:

- Architecture readiness, methodology readiness, implementation readiness,
  runtime readiness, and production-authoritative readiness are distinct.
- The current Lambda path remains:

```text
POST /assessment
  -> handle_assessment()
  -> validate_assessment_request()
  -> score_assessment()
  -> AssessmentResponse
```

- The governed executive domain pipeline is future architecture, not current
  runtime behavior.
- The public 12-question directional assessment and internal 48-question
  executive assessment are separate products and contracts.
- The executive methodology contains deterministic foundation behavior but
  remains `METHODOLOGY_PENDING` for production authority in important areas.

Sprint 6 established:

- `assessmentVersion = nguyen-ai-executive-assessment-v1`.
- `nguyen-ai-executive-assessment-v1` binds to
  `business-decision-methodology-v1`.
- No independent `inputContractVersion` is required for v1.
- Public and executive runtime boundaries must remain logically distinct.
- Runtime metadata remains outside deterministic business truth.
- Only a validated `BusinessDecisionPackage` may become a successful
  executive result.
- Internal failures use the Sprint 6.7 internal failure taxonomy.
- External errors use the Sprint 6.8 error contract.
- Successful executive responses use
  `responseContractVersion = executive-runtime-response-v1` and a minimal
  success envelope containing unchanged package serialization.

## 3. Contract Verification Categories

Future executive runtime implementation must include verification across these
contract categories:

| Category | What It Proves |
| --- | --- |
| Identity verification | Governed identity values are accepted, propagated, and kept distinct. |
| Version compatibility verification | Supported versions pass and unsupported or incompatible versions fail at the correct boundary. |
| Input contract verification | Raw executive input becomes valid canonical executive input only when it satisfies the approved contract. |
| Methodology binding verification | The service resolves the authoritative methodology version deterministically. |
| Deterministic orchestration verification | The executive pipeline is invoked in the approved sequence without adding business decisions. |
| BusinessDecisionPackage verification | Package assembly, validation, immutability, serialization, limitations, and version metadata remain intact. |
| Successful response verification | Success responses follow the Sprint 6.9 envelope and contain unchanged package serialization. |
| Error response verification | Internal failures map to safe external error responses without exposing packages or internal diagnostics. |
| Metadata boundary verification | Runtime metadata never changes deterministic package truth. |
| Exposure governance verification | Only exposure-eligible validated packages become successful runtime responses. |
| Public/executive separation verification | The public runtime cannot route, validate, score, or respond as the executive runtime. |
| Negative verification | Invalid, ambiguous, mixed, partial, or mutated states fail closed. |
| Regression verification | Frozen Sprint 4, Sprint 5, and Sprint 6 behavior remains protected. |
| Compatibility verification | Future version changes preserve governed compatibility and reject unsupported contracts. |

Implementation PRs should show a conformance matrix mapping tests to these
categories. Passing tests without contract traceability is not enough for a
runtime-readiness review.

## 4. Identity Verification

Future tests must prove that every governed identity has one distinct
responsibility.

Executive assessment identity:

- The future executive runtime accepts `nguyen-ai-executive-assessment-v1`
  only at the executive boundary.
- The current public runtime identity remains separate from
  `nguyen-ai-executive-assessment-v1`.
- Public assessment payloads and public question identifiers cannot be accepted
  under the executive assessment identity.
- Executive assessment identity does not imply methodology approval,
  production authority, package contract identity, response identity, request
  identity, timestamp identity, or route identity.

Methodology identity:

- The service resolves `business-decision-methodology-v1` for
  `nguyen-ai-executive-assessment-v1`.
- Caller preference must not determine the executed methodology version for v1.
- Methodology identity remains separate from methodology completeness and
  production authority.

Package identity:

- `BusinessDecisionPackage.versionMetadata.contractVersion` remains the package
  contract identity.
- `BusinessDecisionPackage.versionMetadata.assessmentVersion` matches the
  accepted executive assessment identity.
- `BusinessDecisionPackage.versionMetadata.methodologyVersion` matches the
  bound methodology version.
- `BusinessDecisionPackage.versionMetadata.componentVersions` contains the
  approved component baseline identifiers.
- Package `audit` and `versionMetadata` assessment and methodology versions
  remain consistent.

Response identity:

- Successful executive responses use
  `responseContractVersion = executive-runtime-response-v1`.
- Error responses belong to the same executive runtime response family.
- `responseContractVersion` does not replace package `contractVersion`.
- Runtime metadata identifiers do not participate in deterministic package
  identity.

## 5. Version Verification

Future version tests must prove the v1 compatibility model.

Supported version behavior:

- `nguyen-ai-executive-assessment-v1` resolves to
  `business-decision-methodology-v1`.
- No separate `inputContractVersion` is required, accepted, or inferred for v1.
- Package `contractVersion = business-decision-package-v1` remains visible in
  package serialization.
- `responseContractVersion = executive-runtime-response-v1` remains visible in
  successful runtime responses.

Unsupported or incompatible version behavior:

- Missing executive `assessmentVersion` is rejected before Decision Engine
  execution.
- Unsupported executive `assessmentVersion` is rejected before Decision Engine
  execution.
- Public assessment identity is rejected by the executive runtime.
- Incompatible caller-supplied methodology assertion, if such an assertion is
  ever supported, is rejected and cannot override service selection.
- Missing service-owned assessment-to-methodology binding is treated as a
  service-owned version configuration failure.
- Unsupported package `contractVersion` is not accepted as a successful
  executive package result.
- Unknown response contract versions must not be silently consumed as
  compatible by future consumers.

Version-change tests must distinguish:

- assessment-semantic/input compatibility changes,
- methodology changes,
- package serialization changes,
- component baseline changes,
- runtime response contract changes,
- runtime metadata changes.

Runtime metadata changes must not require package version changes unless a
future governed package contract intentionally adds deterministic domain
metadata.

## 6. Input Contract Verification

Future executive input tests must prove that raw runtime payloads become
canonical executive input only after explicit validation.

Required positive verification:

- The accepted executive `assessmentVersion` is present and equals
  `nguyen-ai-executive-assessment-v1`.
- The submitted answer set contains exactly one valid answer for each of the
  48 canonical executive questions.
- Question matching is by canonical question ID, not ordering.
- Input ordering does not change canonicalized input or deterministic package
  output.
- Configured answer types and ranges are enforced before evaluation.
- Canonicalization produces an immutable input representation before
  orchestration begins.

Required rejection verification:

- Unknown question IDs are rejected.
- Public question IDs are rejected.
- Duplicate question IDs are rejected.
- Missing required executive questions are rejected.
- Unsupported answer types are rejected.
- Wrong value types, null values, and out-of-range values are rejected.
- Malformed request structure is rejected.
- Public `AssessmentRequest` shape is not accepted as canonical executive
  input merely because it contains an `answers` mapping.

These tests belong to the future executive input boundary. They must not be
implemented by changing the current public `validate_assessment_request()`
contract.

## 7. Methodology Verification

Future methodology-binding tests must prove version selection and methodology
execution boundaries without approving unresolved business methodology.

Required verification:

- `BUSINESS_DECISION_METHODOLOGY.version` is the authoritative source of the
  current methodology version.
- `nguyen-ai-executive-assessment-v1` binds to
  `business-decision-methodology-v1`.
- The binding is applied before Decision Engine invocation.
- The Decision Engine receives the approved methodology configuration, not
  caller-supplied business rules.
- The orchestrator does not choose, rewrite, or infer methodology rules.
- The package preserves the selected methodology version in audit and version
  metadata.

Methodology-readiness verification:

- Tests may prove deterministic foundation behavior.
- Tests must not imply unresolved methodology is production-authoritative.
- `METHODOLOGY_PENDING` must not be treated as a software exception unless a
  runtime context requests production-authoritative exposure that governance
  does not permit.
- No test should assert invented final weights, final thresholds, final
  confidence formulas, final recommendation-priority formulas, recommendation
  generation rules, service decision rules, or final executive-summary rules.

Future production-authority methodology tests are out of scope until business
methodology is approved.

## 8. BusinessDecisionPackage Verification

Future runtime tests must preserve and extend the existing package test
surface.

Required package verification:

- Package assembly is deterministic for identical deterministic inputs.
- Package assembly preserves upstream deterministic component objects or their
  serialized content without recomputation.
- Package dataclasses remain immutable where practical.
- Package serialization root fields remain exactly:

```text
decisionEvaluation
businessReadinessSnapshot
confidenceEvaluation
recommendationPriorityEvaluation
executiveSummaryFoundation
audit
limitations
versionMetadata
```

- Serialization does not add runtime fields such as request IDs, trace IDs,
  timestamps, HTTP status, persistence keys, or delivery state.
- `BusinessDecisionPackageValidation` passes before a package can become a
  successful executive runtime result.
- Validation failures terminate successful runtime processing.
- Package validation remains deterministic and does not mutate package content.
- Source assessment versions and methodology versions match across package
  components.
- Decision evaluation and snapshot score, question count, total weight, and
  evaluated dimensions remain aligned.
- Package limitations are preserved and visible.
- The `api-exposure-of-snapshot-consumers-not-implemented` limitation is
  explicitly reviewed at the future exposure gate before successful production
  exposure.

Package tests must also prove prohibited states fail:

- missing components,
- mismatched versions,
- component version mismatches,
- unexpected serialized fields,
- root field order mismatches,
- duplicated limitations,
- serialized invariant violations,
- non-package objects represented as packages.

## 9. Success Response Verification

Future success response tests must prove the Sprint 6.9 minimal envelope.

Required successful response body:

```text
ExecutiveRuntimeSuccessResponse
  |-- responseContractVersion
  |-- responseStatus
  |-- businessDecisionPackage
```

Required verification:

- `responseContractVersion` equals `executive-runtime-response-v1`.
- `businessDecisionPackage` contains the complete canonical package
  serialization unchanged.
- No package fields are renamed, filtered, redacted, flattened, projected, or
  duplicated outside the package.
- `responseStatus` identifies response-boundary governance state without
  mutating package truth.
- `responseStatus.packageValidation` can be asserted as `VALIDATED` only after
  `BusinessDecisionPackageValidation` passes.
- `responseStatus.runtimeEligibility` and `responseStatus.exposure` reflect
  the approved runtime and exposure gate.
- `responseStatus.productionAuthority` does not claim production authority
  unless business-methodology governance permits it.
- A `METHODOLOGY_PENDING` successful non-production context, if allowed, is
  represented as not production-authoritative rather than as a hidden software
  failure.
- The v1 success body contains no operational runtime metadata.
- Success responses contain no error object, error code, validation issue list,
  stack trace, or failure payload.
- A governance-blocked package is not serialized as a successful response.

The current `AssessmentResponse` is not the executive success response
contract and must not be reused for this surface.

## 10. Error Response Verification

Future error response tests must prove the Sprint 6.8 external error contract
and its mapping from Sprint 6.7 internal failure semantics.

Required external error codes:

```text
EXECUTIVE_REQUEST_INVALID
EXECUTIVE_VERSION_INCOMPATIBLE
EXECUTIVE_VERSION_CONFIGURATION_ERROR
EXECUTIVE_PROCESSING_FAILED
EXECUTIVE_PACKAGE_INTEGRITY_FAILED
EXECUTIVE_RESULT_UNAVAILABLE
EXECUTIVE_INTERNAL_ERROR
```

Required HTTP status verification where the Assessment Service owns the
response:

| External Error | Status | Responsibility |
| --- | --- | --- |
| `EXECUTIVE_REQUEST_INVALID` | 400 | Caller-correctable executive request error |
| `EXECUTIVE_VERSION_INCOMPATIBLE` | 409 | Caller-supplied incompatible contract/version |
| `EXECUTIVE_VERSION_CONFIGURATION_ERROR` | 500 | Service-owned version binding/configuration failure |
| `EXECUTIVE_PROCESSING_FAILED` | 500 | Service-owned deterministic processing failure |
| `EXECUTIVE_PACKAGE_INTEGRITY_FAILED` | 500 | Service-owned package assembly or validation failure |
| `EXECUTIVE_RESULT_UNAVAILABLE` | 409 | Governance/exposure state prevents result availability |
| `EXECUTIVE_INTERNAL_ERROR` | 500 | Fail-safe unexpected service failure |

Required error-boundary verification:

- Error responses never contain `BusinessDecisionPackage`.
- Error responses never contain partial deterministic results.
- Error responses never contain success envelope fields as a successful result.
- Unknown or unmapped internal failures fail closed as
  `EXECUTIVE_INTERNAL_ERROR`.
- Validation details are returned only for client-safe
  `EXECUTIVE_REQUEST_INVALID` cases.
- Raw exception names, stack traces, source paths, Lambda internals, AWS
  identifiers, environment variables, secrets, internal methodology details,
  and raw unexpected exception messages are not exposed.
- External error codes remain stable across internal implementation refactors.
- Domain components remain unaware of HTTP, API Gateway, Lambda proxy response
  shapes, and client-facing JSON.

Current public `VALIDATION_ERROR` behavior is not the executive error
contract.

## 11. Metadata Boundary Verification

Future metadata tests must prove the Sprint 6.5 invariant:

```text
same validated canonical executive input
+ same bound methodology configuration
+ same deterministic component versions
= same BusinessDecisionPackage serialization
```

Required verification:

- Different request IDs do not change package serialization.
- Different correlation or trace IDs do not change package serialization.
- Different Lambda invocation IDs do not change package serialization.
- Different API Gateway request context does not change package serialization.
- Different runtime receipt or processing timestamps do not change package
  serialization.
- Runtime metadata does not enter package audit, limitations, version
  metadata, component output, validation input, equality, hashes, or
  serialization.
- Runtime metadata does not influence Decision Engine scoring, snapshot,
  confidence, recommendation priority, executive summary foundation, package
  assembly, or package validation.
- Operational correlation metadata, if implemented, appears only in approved
  non-deterministic locations such as headers, logs, traces, telemetry, or
  future separately governed operational records.
- v1 successful response body contains no runtime metadata.

If a future date/time field is intentionally approved as canonical business
input, tests must prove it is supplied, validated, and versioned as business
input rather than generated by runtime execution.

## 12. Exposure Governance Verification

Future exposure tests must prove that package validity, exposure eligibility,
runtime eligibility, and production authority are separate states.

Required verification:

- A validated package is necessary for success.
- Package validation alone does not imply exposure eligibility.
- Package validation alone does not imply runtime eligibility.
- Package validation alone does not imply production authority.
- Exposure eligibility is decided at the executive application/runtime
  boundary, not by the Decision Engine, package builder, package validator, or
  downstream consumers.
- Exposure-blocked results produce governed failure behavior, not successful
  package serialization.
- Current package limitations remain visible when package serialization is
  exposed.
- The runtime does not add an `apiExposable`, `productionAuthoritative`, error,
  delivery, request, or runtime flag inside `BusinessDecisionPackage`.
- Internal development or controlled non-production exposure does not imply
  production-authoritative executive delivery.
- Downstream consumers may enrich around the package but may not mutate,
  recompute, replace, or hide deterministic package truth.

## 13. Public / Executive Separation Verification

Future tests must prove that Sprint 6.4 separation is enforced.

Current public runtime regression tests must continue to prove:

- `POST /assessment` remains the current public/placeholder path.
- `handle_assessment()` calls current public validation and
  `score_assessment()`.
- The public path returns `AssessmentResponse`.
- The public path does not invoke the executive Decision Engine.
- The public path does not assemble or validate `BusinessDecisionPackage`.
- The public path does not invoke Bedrock, LLM reasoning, or persistence.

Future executive runtime tests must prove:

- The executive runtime uses a distinct route boundary.
- The executive runtime uses a distinct request contract.
- The executive runtime uses a distinct validation and canonicalization
  boundary.
- The executive runtime uses a distinct handler or adapter boundary.
- Public payloads cannot reach `evaluate_assessment()` through the executive
  route.
- Executive payloads cannot be interpreted by public scoring.
- Public assessment identity cannot be accepted as executive identity.
- Executive assessment identity cannot silently promote the public path.
- No hidden mapping, inferred mapping, aliases, synthetic executive answers,
  or public-answer expansion occurs.

Shared infrastructure tests may prove safe sharing of deployment utilities,
logging utilities, authentication infrastructure, or generic transport helpers,
but must also prove shared infrastructure does not imply shared product
semantics.

## 14. Negative Verification Strategy

Future implementation must include negative tests for every fail-closed
contract boundary.

At minimum, negative verification must cover:

- missing executive `assessmentVersion`,
- unsupported executive `assessmentVersion`,
- public assessment identity on executive route,
- missing methodology binding,
- unsupported or incompatible methodology assertion if supported,
- missing required executive questions,
- duplicate executive questions,
- unknown executive questions,
- public question IDs,
- wrong answer types,
- out-of-range answer values,
- malformed payloads,
- public `AssessmentRequest` reuse as executive canonical input,
- orchestrator receiving non-canonical input,
- Decision Engine failure,
- downstream deterministic component failure,
- package assembly failure,
- package validation failure,
- package exposure ineligibility,
- package mutation attempts,
- package serialization with runtime metadata injected,
- response envelope missing required fields,
- success response containing error fields,
- error response containing package fields,
- partial package returned as success,
- package projection, filtering, or redaction,
- duplicated deterministic business truth outside the package,
- raw exception details in external errors,
- LLM or Bedrock repair or fallback,
- public `AssessmentResponse` fallback from executive failures.

Negative tests should assert both the failure classification and the absence of
prohibited successful output.

## 15. Regression Strategy

Sprint 4 regression coverage must protect:

- package immutability,
- package serialization root order and field set,
- package version metadata,
- package audit metadata,
- package limitations,
- package validation determinism,
- rejection of invalid package structures,
- absence of runtime/API/persistence fields inside package serialization.

Sprint 5 regression coverage must protect:

- current runtime truth remains placeholder until explicitly replaced by a
  future governed runtime implementation,
- public and executive assessment contracts remain separate,
- BusinessDecisionPackage structural validity remains distinct from
  methodology approval and production authority,
- foundation confidence, recommendation priority, and executive summary
  behavior is not silently upgraded to production-authoritative methodology,
- orchestration coordinates existing deterministic components without adding
  business decisions.

Sprint 6 regression coverage must protect:

- executive assessment identity,
- methodology binding,
- absence of independent v1 input-contract version,
- route, request, validation, and adapter separation,
- runtime metadata exclusion,
- API exposure governance,
- internal failure taxonomy,
- external error contract,
- successful response envelope.

Current public runtime tests must remain in place. Future executive runtime
tests should be added alongside them without weakening or rewriting public
runtime assertions.

## 16. Compatibility Strategy

Future compatibility tests must prove that consumers and runtime code refuse
unknown or incompatible contracts rather than silently reinterpreting them.

Compatibility tests should cover:

- recognized executive `assessmentVersion` is accepted only with its governed
  methodology binding,
- unsupported executive `assessmentVersion` is rejected,
- no v1 `inputContractVersion` is required or inferred,
- recognized package `contractVersion` is required for successful package
  exposure,
- unknown package `contractVersion` is rejected for successful exposure,
- required package `componentVersions` are present and recognized,
- recognized `responseContractVersion` is required for response consumers,
- unknown response contract versions are rejected by consumers,
- compatible additive runtime metadata changes outside the v1 body do not
  change package identity,
- breaking response contract changes require a new response contract version,
- breaking package serialization changes require a new package contract
  version,
- breaking input compatibility changes require a new executive
  `assessmentVersion`,
- business-methodology changes require methodology version review.

Compatibility tests must not use fallback parsing to reinterpret unknown
contracts as known contracts.

## 17. Release-Gate Expectations

Before a future executive runtime implementation is considered
implementation-ready, the repository should contain:

1. Executable tests for each contract verification category in this document.
2. Positive tests for the complete successful executive runtime path.
3. Negative tests for every required fail-closed boundary.
4. Regression tests proving current public runtime behavior remains unchanged.
5. Tests proving no runtime metadata enters deterministic package truth.
6. Tests proving error responses never contain package data.
7. Tests proving successful responses never contain error payloads.
8. Tests proving `BusinessDecisionPackage` serialization is unchanged inside
   the response envelope.
9. Tests proving unsupported versions fail at the correct boundary.
10. Tests proving exposure governance is enforced before successful response
    serialization.
11. A conformance matrix mapping tests to Sprint 4, Sprint 5, and Sprint 6
    contracts.
12. Updated implementation documentation referencing the governing Sprint 6
    contracts.
13. Full repository regression suite passing.

Before a future runtime is considered runtime-eligible, the repository should
also contain:

- reviewed executive route and adapter implementation,
- reviewed executive input validation/canonicalization implementation,
- reviewed orchestration implementation,
- reviewed success and error response serializers,
- reviewed operational metadata placement,
- reviewed exposure gate implementation,
- compatibility tests for supported and unsupported versions,
- release documentation that explicitly states whether the runtime is
  production-authoritative or non-production/foundation-only.

Before a future runtime is considered production-authoritative, business
methodology approval evidence must exist for the methodology gaps identified
in Sprint 5.2. Engineering tests cannot substitute for business-methodology
approval.

## 18. Audit Evidence

Future implementation PRs and release baselines should preserve audit evidence
showing:

- contract conformance matrix,
- test files and test cases mapped to contract categories,
- full test command output,
- `git diff --check` output,
- package serialization sample or fixture proving unchanged package placement,
- success response sample or fixture proving envelope structure,
- error response sample or fixture proving error mapping and package exclusion,
- version compatibility matrix,
- negative-case matrix,
- public/executive separation evidence,
- runtime metadata exclusion evidence,
- exposure governance evidence,
- documentation links to Sprint 4, Sprint 5, and Sprint 6 architecture,
- explicit statement of methodology readiness and production-authority status.

Audit evidence should distinguish:

- contract conformance,
- deterministic correctness,
- runtime eligibility,
- production authority,
- operational readiness.

## 19. Non-Goals

Sprint 6.10 does not implement:

- Python tests,
- pytest or unittest files,
- fixtures,
- mocks,
- CI workflows,
- GitHub Actions,
- coverage thresholds,
- runtime code,
- executive route,
- executive handler,
- executive adapter,
- executive input model,
- executive validator,
- orchestrator,
- response model,
- error model,
- serializers,
- HTTP mappings in code,
- Lambda or API Gateway changes,
- runtime metadata,
- logging changes,
- persistence,
- package changes,
- public runtime changes,
- methodology changes,
- Bedrock or LLM behavior.

Sprint 6.10 also does not approve final business methodology.

## 20. Open Implementation Decisions

The following decisions remain for future implementation planning:

- Exact test module names and organization.
- Whether future executable tests use only `unittest` or add another test tool.
- Canonical executive input fixture construction.
- Canonical package fixture strategy.
- Canonical JSON serialization strategy for response bodies.
- Whether response field ordering is asserted through dict order,
  serialized JSON bytes, or both.
- Exact future executive route URL.
- Exact handler and adapter module names.
- Exact orchestration module name.
- Exact runtime metadata placement for headers, logs, traces, and telemetry.
- Exact authentication and authorization test boundary.
- Exact CI gate and coverage policy.
- Whether future compatibility fixtures are versioned files, generated
  fixtures, or both.
- How non-production executive runtime modes are named if implemented before
  production-authoritative methodology.

These are implementation decisions. They do not change the Sprint 6 contract
strategy and must not be used to reopen frozen Sprint 4, Sprint 5, or Sprint 6
architecture without explicit governance approval.
