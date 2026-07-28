# Executive Internal Failure Semantics v1

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

That current runtime is the public or placeholder path. It does not invoke the
executive Decision Engine pipeline and does not produce a
`BusinessDecisionPackage`.

Sprint 5.4 established that future executive orchestration coordinates
existing deterministic components and does not make business decisions.

Sprint 6.6 established that only a validated `BusinessDecisionPackage` may be
considered for successful future executive exposure.

Sprint 6.7 defines internal executive failure semantics only. It does not
implement failure models, exception classes, HTTP status codes, API error
bodies, Lambda behavior, or runtime orchestration.

## 2. Sprint 6.1-6.6 Dependencies

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
- `assessmentVersion` is the executive input compatibility identity

Sprint 6.4 established:

- public and executive runtimes require distinct logical boundaries
- the current `POST /assessment` runtime remains unchanged
- future executive processing must not fall back to public scoring

Sprint 6.5 established:

- runtime metadata remains outside deterministic package truth
- request IDs, trace IDs, invocation IDs, timestamps, and transport context do
  not alter package identity or serialization

Sprint 6.6 established:

- package validation is necessary but not sufficient for exposure eligibility
- package validity, exposure eligibility, runtime eligibility, and production
  authority remain separate
- complete canonical package serialization must remain unchanged

## 3. Success Invariant

A future executive orchestration invocation is successful only when all of the
following are true:

1. Executive input has passed the required contract and version boundary.
2. The accepted executive `assessmentVersion` is supported.
3. The methodology binding is resolved and valid.
4. Canonical executive input is complete and stable.
5. Decision Engine evaluation completes.
6. Required downstream deterministic foundations complete.
7. `BusinessDecisionPackage` assembly completes.
8. `BusinessDecisionPackageValidation` passes.
9. The validated package satisfies the applicable exposure-governance
   conditions for the runtime context.

If any required step fails, the outcome is an internal failure, not a
successful executive result.

This invariant does not make methodology-pending outputs
production-authoritative. Production authority remains governed separately.

## 4. Failure Definition

An internal executive orchestration failure occurs when the future executive
application/domain flow cannot produce an exposure-eligible validated
`BusinessDecisionPackage`.

Failure means:

- no successful executive package result is produced
- no partial package is represented as successful
- no synthetic fallback business result is produced
- no deterministic output is guessed or repaired probabilistically
- no public `AssessmentResponse` fallback is used

Failure classification is internal Assessment Service meaning. It is separate
from transport representation.

## 5. Failure Taxonomy

Sprint 6.7 establishes the following internal failure taxonomy:

| Category | Meaning | Typical Stage |
| --- | --- | --- |
| `INPUT_CONTRACT_FAILURE` | Raw or parsed executive input cannot become valid canonical executive input. | Before deterministic evaluation |
| `VERSION_COMPATIBILITY_FAILURE` | Required governed identity or binding is missing, unsupported, or incompatible. | Before deterministic evaluation |
| `DETERMINISTIC_EVALUATION_FAILURE` | A deterministic domain component cannot complete its required evaluation or projection. | Decision Engine and Sprint 3 foundations |
| `PACKAGE_INTEGRITY_FAILURE` | A complete valid `BusinessDecisionPackage` cannot be assembled or validated. | Package assembly and validation |
| `GOVERNANCE_EXPOSURE_FAILURE` | A validated package exists but is not eligible to cross the executive runtime boundary in the current context. | After package validation |
| `UNEXPECTED_INTERNAL_FAILURE` | An unclassified implementation, infrastructure, or runtime fault prevents completion. | Any stage |

This taxonomy is intentionally small. Component-specific evidence may appear in
the failure detail, but the top-level category should remain stable.

## 6. Failure-Stage Ownership

| Stage | Owner | Failure Responsibility |
| --- | --- | --- |
| Transport parsing | Future executive adapter | Detect malformed transport input before domain entry. |
| Executive input validation | Future executive input validator | Detect missing, malformed, duplicate, unknown, incomplete, or wrong-contract input. |
| Version binding | Future executive input/application boundary | Resolve and validate `assessmentVersion` and bound `methodologyVersion`. |
| Canonicalization | Future executive input validator | Produce stable canonical executive input or fail before evaluation. |
| Decision Engine | Decision Engine | Reject invalid answer sets, invalid configured methodology, unknown questions, missing questions, invalid answer values, invalid weights, or invalid evaluation inputs. |
| Snapshot foundation | `BusinessReadinessSnapshot` builder | Reject invalid assessment version, missing explanation metadata, unknown dimensions, or mismatched explanation data. |
| Confidence foundation | `ConfidenceEvaluation` builder | Reject snapshot/config mismatches and invalid snapshot metadata. |
| Recommendation priority foundation | `RecommendationPriorityEvaluation` builder | Reject source version mismatches, missing confidence factors, and unknown confidence factors. |
| Executive summary foundation | `ExecutiveSummaryFoundation` builder | Reject source version or methodology mismatches. |
| Package assembly | `BusinessDecisionPackage` builder | Reject source assessment/methodology mismatches or decision/snapshot inconsistencies. |
| Package validation | `BusinessDecisionPackageValidation` | Return structured validation issues for package contract, version, audit, limitation, source, and serialization violations. |
| Exposure governance | Future executive application/runtime boundary | Determine whether a validated package is eligible to become a successful executive runtime result. |

The orchestrator coordinates these stages. It does not replace their
responsibilities.

## 7. Deterministic vs Operational Failures

Deterministic failures are reproducible for the same invalid input,
configuration, and component versions.

Examples:

- unsupported executive `assessmentVersion`
- unresolved methodology binding
- missing required canonical question
- unknown question ID
- duplicate canonical answer
- out-of-range answer
- invalid methodology configuration
- source methodology-version mismatch
- package serialization contract violation

Operational failures are caused by runtime or infrastructure conditions rather
than deterministic business input.

Examples:

- process crash
- memory exhaustion
- deployment packaging fault
- unavailable runtime dependency
- unexpected unclassified exception

Operational failures may use request, trace, or invocation context for
correlation, but such context remains outside deterministic business truth.

## 8. Failure Information Requirements

An internal failure should conceptually preserve enough information for
deterministic handling and later Sprint 6.8 error mapping without coupling
domain code to HTTP.

Required conceptual information:

- stable internal failure category
- stable internal reason or code
- diagnostic description suitable for logs and review
- component or stage responsibility
- assessment version, when known
- methodology version, when resolved
- validation issues, when applicable
- indication of whether deterministic evaluation began
- indication of whether package validation ran

Operational correlation may be associated outside deterministic truth:

- request ID
- correlation ID
- trace ID
- Lambda invocation context
- runtime timestamp

Exact field names and Python models are outside Sprint 6.7.

## 9. Version / Compatibility Failures

Version and compatibility failures occur before deterministic evaluation when
the future executive boundary cannot establish governed identity.

Examples:

- missing executive `assessmentVersion`
- unsupported executive `assessmentVersion`
- public `nguyen-ai-readiness-v1` submitted to the executive boundary
- incompatible caller methodology-version assertion, if such an assertion is
  approved later
- inability to resolve the binding from `nguyen-ai-executive-assessment-v1` to
  `business-decision-methodology-v1`
- methodology configuration unavailable for the resolved version

These failures must prevent Decision Engine invocation.

The Decision Engine executes an already-selected methodology configuration. It
does not own runtime methodology selection or assessment/methodology binding.

## 10. Input / Canonicalization Failures

Input and canonicalization failures occur before deterministic evaluation when
raw or parsed executive input cannot become valid canonical executive input.

Examples:

- malformed request body
- missing required executive input field
- unknown top-level executive input field when the future contract prohibits it
- missing canonical answer
- duplicate canonical answer
- unknown executive question ID
- public question ID
- invalid answer structure
- unsupported answer type
- non-numeric value for currently normalizable numeric answer types
- out-of-range value
- incomplete submission when complete evaluation is required

These failures must prevent Decision Engine invocation.

The future executive input validator owns these failures. The orchestrator may
receive only validated canonical executive input.

## 11. Deterministic Evaluation Failures

Deterministic evaluation failures occur after canonical input has entered the
domain pipeline and a required deterministic component cannot complete.

Examples from current repository behavior:

- `evaluate_assessment()` raises on unknown questions, missing required
  questions, invalid configured weights, invalid answer types, invalid answer
  values, or invalid configured methodology.
- `build_business_readiness_snapshot()` raises on empty assessment version,
  missing explanation metadata, mismatched explanation metadata, or unknown
  readiness dimensions.
- `build_confidence_evaluation()` raises on snapshot methodology mismatch,
  snapshot audit mismatch, unknown readiness dimension, or unknown question.
- `build_recommendation_priority_evaluation()` raises on source
  assessment-version mismatch, methodology-version mismatch, missing confidence
  factor, or unknown confidence factor.
- `build_executive_summary_foundation()` raises on source assessment-version
  or methodology-version mismatch.

The future orchestrator must classify these as deterministic evaluation
failures unless a more specific package-integrity boundary has already been
reached.

## 12. Package Assembly / Validation Failures

Package assembly failures occur when required deterministic source outputs
exist but cannot be assembled into a valid `BusinessDecisionPackage`.

Examples:

- source assessment versions do not match
- source methodology versions do not match
- Decision Engine score does not match snapshot score
- Decision Engine question count does not match snapshot audit
- Decision Engine total weight does not match snapshot audit
- Decision Engine dimensions do not match snapshot audit

Package validation failures occur when a package object or serialization fails
the approved Sprint 4 package validation contract.

Examples:

- missing component
- contract version mismatch
- component version mismatch
- audit mismatch
- limitation mismatch
- unexpected serialized field
- root field order mismatch
- serialized source inconsistency

`BusinessDecisionPackageValidation` failure terminates successful
orchestration.

## 13. Governance / Exposure Failures

Governance or exposure failures occur after package validation when the
validated package is not eligible to cross the future executive runtime
boundary in the current context.

Examples:

- executive runtime exposure has not been approved for the current context
- package limitation `api-exposure-of-snapshot-consumers-not-implemented`
  remains unresolved for a production exposure attempt
- runtime response contract is not finalized
- current runtime path is public/placeholder rather than executive
- package is structurally valid but methodology status does not support the
  requested production-authoritative use
- authorization, access-control, or exposure governance is not approved in a
  future implementation context

Exposure ineligibility is an internal governance failure for successful
runtime processing. It must not mutate the package.

## 14. Unexpected Internal Failures

Unexpected internal failures cover unclassified implementation, infrastructure,
or runtime faults that prevent completion.

Examples:

- unhandled implementation exception
- runtime dependency failure
- packaging or import failure
- infrastructure resource exhaustion
- corrupted runtime environment

Unexpected internal failures are not deterministic business conclusions. They
may be operationally correlated and logged outside deterministic package truth.

Sprint 6.8 will decide how such failures are represented externally.

## 15. Fail-Closed Behavior

The future executive orchestration layer must fail closed.

Fail closed means:

- no successful result is returned when deterministic truth cannot be
  established
- no default score is substituted after Decision Engine failure
- no placeholder confidence is substituted after confidence failure
- no empty recommendation priority is substituted after priority failure
- no executive summary is synthesized after summary failure
- no partial `BusinessDecisionPackage` is emitted
- no invalid package is emitted
- no unvalidated package is emitted
- no public `AssessmentResponse` fallback is emitted
- no public-to-executive translation is inferred
- no LLM or Bedrock call repairs deterministic truth

Fail-closed behavior protects deterministic truth even when a failure is
operationally inconvenient.

## 16. Partial-Result Prohibition

A failed executive orchestration must not produce a successful partial result.

The following are prohibited as successful outcomes:

- partial packages
- packages with missing components
- packages with embedded error fields
- packages with runtime status fields
- packages with exception details
- validation-failed packages
- unvalidated packages
- successful runtime responses containing only some package sections

Internal logs may record the last completed stage. That record is operational
context, not deterministic package truth.

## 17. Retry vs Fallback Distinction

Technical retry is different from business fallback.

A future implementation may retry a deterministic operation only when retry
does not change business semantics.

Examples of potentially acceptable technical retry:

- retrying a pure deterministic function after a transient process-level
  interruption
- retrying package validation against the same immutable package object

Prohibited fallback:

- substituting default scores
- skipping failed components
- using older methodology because current binding failed
- converting public input into executive input
- using AI or LLM output to fill missing deterministic results
- suppressing validation issues to produce a package

Sprint 6.7 does not implement retry behavior.

## 18. Runtime Metadata / Correlation Boundary

Runtime correlation may be attached to internal failure handling outside
deterministic package truth.

Permitted operational correlation concepts include:

- request ID
- correlation ID
- trace ID
- Lambda invocation ID
- runtime timestamp
- deployment context

These values must not:

- enter `BusinessDecisionPackage`
- alter package validation
- alter Decision Engine output
- become package equality criteria
- replace assessment, methodology, contract, or component version identity

Sprint 6.8 may map internal failures to external runtime errors, but it must
preserve this metadata boundary.

## 19. Methodology-Readiness Distinction

`METHODOLOGY_PENDING` is not automatically a software failure.

Current unresolved methodology includes final weights, thresholds, scoring
semantics, confidence formulas, recommendation-priority formulas,
recommendation rules, service decision rules, and executive-summary
methodology.

Those gaps block production authority for affected conclusions. They do not
mean deterministic foundation code failed to execute.

If a future runtime context requests production-authoritative output that the
current methodology cannot support, the correct classification is
`GOVERNANCE_EXPOSURE_FAILURE`, not `DETERMINISTIC_EVALUATION_FAILURE`.

Readiness states must not be collapsed into exception handling:

- `FOUNDATION_COMPLETE` may execute deterministically.
- `METHODOLOGY_PENDING` may block production authority.
- `IMPLEMENTATION_READY` does not imply runtime eligibility.
- `RUNTIME_ELIGIBLE` does not imply production authority.
- `PRODUCTION_AUTHORITATIVE` requires explicit methodology approval.

## 20. BusinessDecisionPackage Exclusion Rules

`BusinessDecisionPackage` must not contain:

- failure category
- error code
- exception message
- stack trace
- HTTP status
- request ID
- trace ID
- runtime timestamp
- exposure flag
- production-authority flag
- retry state
- fallback state
- partial-success state

Failure semantics belong around orchestration and runtime boundaries, not
inside the canonical deterministic package.

If a future implementation appears to require package error fields, the package
contract must not be modified silently. A new governed architecture decision
and package contract version would be required.

## 21. Domain / API Decoupling

Internal failures must remain decoupled from external API transport.

Domain components should not know about:

- HTTP status codes
- API Gateway response shapes
- response headers
- CORS
- Lambda proxy response bodies
- client-facing error messages

The future executive adapter may translate internal failure classifications
into an external error contract after Sprint 6.8 approves that mapping.

Internal failure categories provide stable mapping inputs. They are not
themselves HTTP response bodies.

## 22. Dependencies on Sprint 6.8-6.10

Sprint 6.8 must define how internal failure categories map to external
executive runtime errors without leaking implementation details or exposing
partial business truth.

Sprint 6.9 must finalize the successful executive runtime response contract
and ensure successful responses cannot contain failed, partial, or
exposure-ineligible packages.

Sprint 6.10 must define the contract test strategy proving:

- every failure category maps deterministically
- package failures never produce successful executive results
- public and executive failure paths remain separate
- runtime metadata remains outside package truth
- methodology-pending status is not mislabeled as software failure

## 23. Explicit Non-Goals

Sprint 6.7 does not implement:

- exception classes
- failure enums
- result classes
- orchestrator
- executive handler
- executive route
- HTTP status-code mapping
- API error JSON
- retry logic
- logging changes
- runtime metadata
- package changes
- package validation changes
- Decision Engine changes
- methodology changes
- public runtime changes
- Bedrock or LLM recovery
- recommendation generation
- service routing
- executive reporting
- dashboard behavior
- persistence

## 24. Still-Unresolved Decisions

The following decisions remain unresolved after Sprint 6.7:

- exact internal failure model field names
- exact Python representation of internal failures
- whether future implementation uses result objects, exceptions, or a hybrid
  boundary approach
- external executive runtime error contract
- HTTP status-code mapping
- client-facing error messages
- operational logging schema
- runtime correlation placement in external error handling
- successful executive runtime response field names
- executive response contract version
- contract test structure for Sprint 6.10
- authorization and access-control failure placement

These decisions belong to later governed Sprint 6 increments.
