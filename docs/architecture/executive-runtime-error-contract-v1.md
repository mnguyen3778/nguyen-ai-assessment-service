# Executive Runtime Error Contract v1

## 1. Established Frozen Facts

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

The current public or placeholder runtime returns HTTP-shaped validation
errors for `POST /assessment`. Those errors are repository evidence, but they
are not the future executive runtime error contract.

Sprint 6.7 established internal executive failure semantics. Sprint 6.8 maps
those internal failures to a future external executive runtime error contract.

Sprint 6.8 does not implement runtime behavior, define Python models, modify
the Lambda handler, modify the public runtime, or finalize successful response
fields.

## 2. Sprint 6.1-6.7 Dependencies

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

Sprint 6.3 established:

- no independent `inputContractVersion` is required for v1
- `assessmentVersion` remains the executive input compatibility identity

Sprint 6.4 established:

- public and executive runtime boundaries are logically distinct
- route, request-contract, validation, and adapter separation is required
- current `POST /assessment` remains unchanged

Sprint 6.5 established:

- runtime and transport metadata remain outside `BusinessDecisionPackage`
- operational metadata cannot alter deterministic truth

Sprint 6.6 established:

- only a validated `BusinessDecisionPackage` may become a successful executive
  result
- package validity, exposure eligibility, runtime eligibility, and production
  authority remain distinct

Sprint 6.7 established the internal failure taxonomy:

- `INPUT_CONTRACT_FAILURE`
- `VERSION_COMPATIBILITY_FAILURE`
- `DETERMINISTIC_EVALUATION_FAILURE`
- `PACKAGE_INTEGRITY_FAILURE`
- `GOVERNANCE_EXPOSURE_FAILURE`
- `UNEXPECTED_INTERNAL_FAILURE`

## 3. Error-Contract Ownership

The executive runtime error contract is owned by the future Assessment Service
executive runtime/application boundary.

Ownership rules:

- Domain components own deterministic validation and invariant checks.
- Internal orchestration owns internal failure classification.
- The future executive adapter/runtime boundary owns translation from internal
  failure classification to external error representation.
- API Gateway, Lambda proxy mechanics, CORS, authentication providers, and
  infrastructure errors remain outside deterministic domain components.

Domain components must not know about HTTP, API Gateway response bodies,
Lambda proxy responses, headers, CORS, or client-facing JSON.

## 4. Internal vs External Failure Separation

Internal failure semantics answer:

```text
Why did executive orchestration fail inside the Assessment Service?
```

External error contract semantics answer:

```text
What can a future executive runtime safely communicate to a caller?
```

The external contract must preserve enough stable information for clients to
react safely without exposing internal implementation details.

Internal categories are mapping inputs. They are not automatically exposed as
external enum values.

## 5. External Error Taxonomy

Sprint 6.8 establishes the following external executive error taxonomy:

| External Error Code | External Category | Meaning |
| --- | --- | --- |
| `EXECUTIVE_REQUEST_INVALID` | `request-error` | The submitted executive request cannot become valid canonical executive input. |
| `EXECUTIVE_VERSION_INCOMPATIBLE` | `version-error` | The caller supplied or asserted an unsupported or incompatible executive contract identity. |
| `EXECUTIVE_VERSION_CONFIGURATION_ERROR` | `service-configuration-error` | The service cannot resolve or load the governed assessment/methodology binding it owns. |
| `EXECUTIVE_PROCESSING_FAILED` | `processing-error` | The deterministic executive pipeline cannot complete after canonical input is accepted. |
| `EXECUTIVE_PACKAGE_INTEGRITY_FAILED` | `integrity-error` | A complete valid package cannot be assembled or validated. |
| `EXECUTIVE_RESULT_UNAVAILABLE` | `governance-error` | A result cannot be exposed under the current governance or readiness state. |
| `EXECUTIVE_INTERNAL_ERROR` | `internal-error` | An unexpected internal service fault prevented completion. |

This taxonomy is external and client-facing. It is intentionally smaller than
component topology and must remain stable across internal refactors.

## 6. Internal-to-External Mapping

| Internal Failure Category | External Error Code | Default HTTP Status | Notes |
| --- | --- | ---: | --- |
| `INPUT_CONTRACT_FAILURE` | `EXECUTIVE_REQUEST_INVALID` | 400 | Caller-correctable request or canonicalization problem. |
| `VERSION_COMPATIBILITY_FAILURE` caused by caller-supplied unsupported or incompatible identity | `EXECUTIVE_VERSION_INCOMPATIBLE` | 409 | Caller requested a contract/version the executive runtime cannot accept. |
| `VERSION_COMPATIBILITY_FAILURE` caused by missing service-owned binding or methodology configuration | `EXECUTIVE_VERSION_CONFIGURATION_ERROR` | 500 | Service configuration failed after the caller reached the executive boundary. |
| `DETERMINISTIC_EVALUATION_FAILURE` | `EXECUTIVE_PROCESSING_FAILED` | 500 | The accepted executive pipeline could not complete. |
| `PACKAGE_INTEGRITY_FAILURE` | `EXECUTIVE_PACKAGE_INTEGRITY_FAILED` | 500 | Package assembly or validation failed. |
| `GOVERNANCE_EXPOSURE_FAILURE` | `EXECUTIVE_RESULT_UNAVAILABLE` | 409 | A valid package or requested result cannot be exposed under current governance state. |
| `UNEXPECTED_INTERNAL_FAILURE` | `EXECUTIVE_INTERNAL_ERROR` | 500 | Fail-safe generic service failure. |

The same internal category may map to different external status only when the
responsibility boundary differs. Sprint 6.8 uses that rule only for
`VERSION_COMPATIBILITY_FAILURE`.

## 7. HTTP Status Semantics

HTTP status codes communicate broad responsibility. They must not expose
internal component topology.

Sprint 6.8 establishes this small status set for application-owned executive
runtime errors:

| Status | Meaning In Executive Runtime Context |
| ---: | --- |
| 400 | The executive request is malformed or violates the executive input contract. |
| 409 | The request conflicts with supported executive contract, version, governance, or readiness state. |
| 500 | The Assessment Service failed to complete processing or integrity checks it owns. |

Rationale:

- The current public runtime uses `400` for validation errors. Using `400` for
  executive input-contract failures is repository-compatible and avoids
  unnecessary 400/422 splitting before implementation.
- `409` communicates that the caller requested a contract, version, or
  governance state that cannot currently be satisfied.
- `500` communicates service-owned processing, configuration, package
  integrity, or unexpected internal failure.

Sprint 6.8 does not use 422 for v1 because the current repository does not
distinguish malformed request failures from semantic validation failures at
the HTTP status level, and the executive contract benefits from a smaller
initial mapping.

## 8. Caller-Correctable Errors

Caller-correctable errors include:

- malformed executive request body
- missing required executive input fields
- duplicate canonical answers
- unknown executive question IDs
- public question IDs submitted to the executive route
- missing required canonical answers
- invalid answer structures
- unsupported answer values or ranges
- unsupported caller-supplied executive assessment identity
- incompatible caller version assertion, if such an assertion is approved
  later

External response behavior:

- `EXECUTIVE_REQUEST_INVALID` uses 400.
- `EXECUTIVE_VERSION_INCOMPATIBLE` uses 409.
- Validation detail may be returned only when it is safe and directly helps the
  caller correct the executive request.

Caller-correctable does not mean the service should infer, repair, or fill
missing executive answers.

## 9. Service-Processing Errors

Service-processing errors occur when the future executive boundary accepted
the request but the Assessment Service cannot complete deterministic
processing or package integrity checks.

Examples:

- deterministic component invariant failure after canonical input acceptance
- invalid methodology configuration detected during domain execution
- package assembly mismatch
- package validation failure
- missing service-owned methodology binding
- unavailable service-owned methodology configuration

External response behavior:

- return a service-owned error code
- use 500 unless a more specific governance status applies
- do not expose internal component names, exception text, stack traces, or
  package-validation topology
- log internal diagnostics separately

## 10. Governance / Exposure Errors

Governance or exposure errors occur when successful exposure is blocked by
governance state rather than deterministic computation failure.

Examples:

- executive runtime exposure is not approved for the current context
- runtime response contract is not finalized
- package API-exposure limitation remains unresolved for the requested use
- methodology is not production-authoritative for a requested
  production-authoritative result
- package is structurally valid but not eligible for the requested exposure

External response behavior:

- `EXECUTIVE_RESULT_UNAVAILABLE`
- HTTP 409
- client-safe message explaining that the executive result is not available
  under the current governance state
- no package returned
- no methodology gap details exposed unless separately governed

Authorization failures are not automatically governance exposure failures.
Authentication and authorization boundaries are addressed separately in this
document.

## 11. Unexpected Errors

Unexpected internal failures must fail closed.

External response behavior:

- `EXECUTIVE_INTERNAL_ERROR`
- HTTP 500
- generic client-safe message
- no internal exception message
- no stack trace
- no package
- no partial deterministic results

Unknown or unmapped internal failures must map to
`EXECUTIVE_INTERNAL_ERROR`.

## 12. Safe Validation-Detail Disclosure

Validation details may be externally returned for
`EXECUTIVE_REQUEST_INVALID` when they are:

- stable
- caller-correctable
- bounded to input contract fields
- free of secrets
- free of raw sensitive payload data
- free of implementation internals

Safe validation detail may conceptually include:

- field or path
- stable validation issue code
- client-safe issue message

Validation detail must not include:

- Python exception names
- stack traces
- source paths
- raw request body
- raw sensitive values
- internal validator function names
- methodology implementation internals
- package assembly details

Sprint 6.8 does not freeze exact validation-detail JSON field names.

## 13. Information-Disclosure Prohibitions

External executive errors must not expose:

- Python exception class names
- stack traces
- source file names
- function names as implementation diagnostics
- Lambda internals
- API Gateway internals
- AWS account or resource identifiers
- environment variables
- credentials
- secrets
- raw unexpected exception messages
- internal package assembly details
- package validation topology beyond a safe high-level error
- hidden methodology configuration details
- supported methodology inventories
- internal runtime deployment details

Internal logs may preserve richer diagnostics according to future operational
logging governance. External errors must remain client-safe.

## 14. Machine-Readable Error Identity

External errors require a stable machine-readable error code.

Clients may branch on:

1. HTTP status for broad transport/application responsibility.
2. Stable external error code for application-level handling.

Clients must not branch on:

- raw message text
- internal failure category
- Python exception names
- internal component names
- stack trace content

The internal Sprint 6.7 taxonomy should not be exposed as the primary client
contract. It may be logged internally for support correlation.

Changing an external error code or changing the meaning of an existing code is
a breaking contract change unless a future versioned compatibility policy
explicitly allows it.

## 15. Human-Readable Message Responsibility

External messages should be:

- client-safe
- stable enough for support and documentation
- useful enough for correction or escalation
- independent of raw exception text
- free of secrets and internal implementation details

Messages may explain broad corrective action, such as correcting executive
input, using a supported executive assessment version, or contacting support
when processing fails.

Messages must not declare methodology complete or production-authoritative.

## 16. Runtime Correlation Metadata

Runtime correlation metadata may accompany external errors only outside
deterministic package truth.

Conceptually allowed correlation metadata:

- request reference
- correlation reference
- trace reference

Decision status:

- DECIDED: an external correlation reference is permitted but not required by
  Sprint 6.8.
- DECIDED: exact field names and placement are deferred.
- DECIDED: correlation metadata may be placed in a future error body, response
  headers, logs, or telemetry according to later runtime implementation
  governance.
- DECIDED: runtime timestamps are not required in external error responses.

Correlation metadata must not alter error classification, deterministic
evaluation, methodology binding, package validation, or package identity.

## 17. BusinessDecisionPackage Exclusion

An external error response must not contain a `BusinessDecisionPackage`.

Prohibited in error responses:

- successful package serialization
- partial package serialization
- unvalidated package serialization
- validation-failed package serialization
- governance-blocked package serialization
- package sections as diagnostic payload
- embedded package errors

Errors must not mutate `BusinessDecisionPackage`, add error fields to it, or
return it as a partial business result.

This preserves Sprint 6.6 exposure governance and Sprint 6.7 fail-closed
semantics.

## 18. Methodology-Readiness Behavior

`METHODOLOGY_PENDING` is not automatically a software failure.

If deterministic foundation processing completes but the requested use demands
production-authoritative methodology that is not approved, the external error
is:

- `EXECUTIVE_RESULT_UNAVAILABLE`
- HTTP 409

The external message may state that the executive result is not available for
the requested authority level.

The external message must not:

- imply deterministic evaluation failed
- declare methodology complete
- expose detailed methodology gaps unless separately governed
- return a blocked package

## 19. Auth and Infrastructure Ownership Boundaries

Authentication and authorization errors may occur before the future executive
application boundary.

Examples outside Sprint 6.8 application-owned error contract:

- API Gateway authorization rejection
- Cognito or identity-provider rejection
- WAF or edge security rejection
- platform throttling
- API Gateway request-size rejection
- Lambda service invocation failure before application code runs

Those failures may use platform-owned statuses such as 401, 403, 429, or 503.
Sprint 6.8 does not define or implement those platform contracts.

If a future Assessment Service application layer owns an exposure authorization
decision after authentication succeeds, that requires a separately governed
authorization architecture. It must not be confused with methodology readiness
or package validation.

## 20. Compatibility and Versioning Rules

Sprint 6.8 does not introduce a separate `errorContractVersion`.

Decision status:

- DECIDED: error compatibility should be governed by the future executive
  runtime response contract family.
- DECIDED: Sprint 6.9 must decide the exact response contract identity and
  whether success and error responses share the same top-level contract
  version.
- DECIDED: external error codes are stable compatibility commitments once
  implemented.
- DECIDED: removing an error code, changing its meaning, or changing its
  default status mapping is a breaking change unless a future versioned
  compatibility policy governs it.

No package contract version changes are required by Sprint 6.8.

## 21. Public / Executive Separation

The existing public `POST /assessment` errors are not the executive runtime
error contract.

Current public behavior:

- `handle_assessment()` returns status 400 for current placeholder validation
  errors.
- current error body includes `requestId`, `error.code`, `error.message`,
  `error.details`, `modelInvoked`, and `persisted`.
- current public validation is tied to `nguyen-ai-readiness-v1`.

Future executive error behavior:

- belongs to a distinct executive route and adapter boundary
- must not reuse public `AssessmentResponse`
- must not use public scoring as fallback
- must not accept public payloads or public assessment identity as executive
  input
- must not expose `BusinessDecisionPackage` through public errors

Sprint 6.8 does not modify current public behavior.

## 22. Dependencies on Sprint 6.9-6.10

Sprint 6.9 must finalize:

- exact successful executive runtime response field names
- response contract identity/version
- whether success and error responses share a top-level contract version
- exact placement of error code, category, message, validation detail, and
  correlation reference if included
- confirmation that successful responses cannot contain failed, partial, or
  exposure-ineligible packages

Sprint 6.10 must define test strategy proving:

- every Sprint 6.7 internal category maps to a stable external error
- caller-correctable errors use the approved external status and code
- service-owned failures do not leak internal diagnostics
- package failures never return a package
- governance exposure failures do not imply deterministic computation failure
- methodology-pending status maps to result-unavailable when the requested use
  requires production authority
- public and executive error contracts remain separate
- runtime metadata remains outside `BusinessDecisionPackage`

## 23. Explicit Non-Goals

Sprint 6.8 does not implement:

- error classes
- error enums
- error response models
- serializers
- HTTP mappings in code
- executive route
- executive handler
- executive adapter
- orchestrator
- Lambda changes
- API Gateway changes
- Cognito or authentication changes
- logging changes
- request IDs
- correlation IDs
- tracing
- retry behavior
- package changes
- package validation changes
- public runtime changes
- successful executive response fields
- Bedrock or LLM behavior
- methodology changes

## 24. Still-Unresolved Implementation Decisions

The following decisions remain unresolved after Sprint 6.8:

- exact external error response field names
- exact successful response field names
- exact response contract version value
- whether success and error responses share one top-level response contract
  version
- exact correlation metadata placement
- whether a request/correlation reference is required by implementation
- exact validation-detail structure
- implementation representation of internal failures
- mapping from Python exceptions to internal failures
- operational logging schema
- authentication and authorization architecture
- infrastructure error handling owned by API Gateway, Lambda, or another
  platform layer

These decisions belong to later governed increments.
