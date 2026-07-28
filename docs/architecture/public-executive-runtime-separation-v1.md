# Public Executive Runtime Separation v1

## Purpose

This document finalizes the Sprint 6.4 architecture and governance decision
for runtime separation between the public directional assessment path and the
future internal executive assessment path in the Nguyen AI Assessment Service.

The core question answered by this document is:

```text
How must the Assessment Service prevent the existing public or placeholder
runtime from being silently promoted into the future executive runtime?
```

This is a runtime separation contract decision. It does not implement a new
route, handler, adapter, validator, orchestrator, response model, or API
contract. It does not change the current executable runtime.

## Scope

This document defines:

- The public runtime responsibility.
- The future executive runtime responsibility.
- Required logical separation between public and executive processing.
- Route-boundary requirements.
- Request-contract, validation, and handler/adapter separation.
- Permitted shared infrastructure.
- Prohibited semantic sharing.
- Cross-routing prevention controls.
- The role of `assessmentVersion` at the runtime boundary.
- Logical versus physical isolation requirements.
- Observability, auditability, and security separation requirements.
- Dependencies for Sprint 6.5 and later runtime implementation.

This document does not define:

- A concrete executive route URL.
- An executive request Python model.
- An executive validator implementation.
- An executive handler implementation.
- Runtime orchestration implementation.
- Internal failure classes.
- Runtime error response bodies.
- Runtime metadata fields.
- Business Decision Package API exposure rules.
- Methodology weights, thresholds, scoring semantics, confidence formulas,
  recommendation rules, service decisions, or executive-summary methodology.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/executive-assessment-identity-v1.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`
- `docs/architecture/executive-input-contract-versioning-v1.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
- `docs/architecture/executive-assessment-input-contract-v1.md`
- `docs/architecture/executive-runtime-orchestration-architecture-v1.md`
- `docs/architecture/executive-runtime-response-contract-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`
- `docs/releases/sprint5-executive-runtime-readiness-foundation-complete-v1.md`

Sprint 3, Sprint 4, Sprint 5, Sprint 6.1, Sprint 6.2, and Sprint 6.3 behavior
and contracts remain unchanged.

## Established Frozen Facts

The repository currently establishes these facts:

| Evidence | Current Meaning |
| --- | --- |
| `README.md` | Documents the current runtime route as `POST /assessment` and the Lambda entry point as `lambda_function.lambda_handler`. |
| `docs/deployment-guide.md` | Documents deployment of a protected `POST /assessment` API Gateway route. |
| `src/lambda_function.py` | Delegates every Lambda invocation directly to `handle_assessment()`. |
| `src/assessment/handler.py` | Parses the current runtime event, creates a runtime request ID, calls placeholder request validation, calls `score_assessment()`, and returns API Gateway proxy responses. |
| `src/assessment/validation.py` | Validates the current placeholder request contract using `assessmentVersion` and configured runtime fields. |
| `src/assessment/scoring.py` | Returns a deterministic placeholder `AssessmentResponse` until official rubric behavior is supplied. |
| `src/assessment/models.py` | Defines current placeholder `AssessmentRequest` and `AssessmentResponse` models. |
| `src/assessment/config.py` | Defines `nguyen-ai-readiness-v1` and TODO-backed placeholder runtime configuration. |
| `tests/test_handler.py` | Verifies the `/assessment` path returns placeholder responses and does not invoke Bedrock or DynamoDB. |
| `tests/test_validation.py` | Verifies current request validation behavior for the placeholder runtime contract. |
| `tests/test_scoring.py` | Verifies `score_assessment()` returns deterministic placeholder output. |
| `src/assessment/decision_engine.py` | Owns deterministic executive evaluation of complete canonical methodology answer sets. |
| `src/assessment/business_decision_package.py` | Assembles the canonical immutable deterministic executive domain output from Sprint 3 components. |
| `src/assessment/business_decision_package_validation.py` | Validates package structural and serialization contract integrity. |

No executive runtime route, executive handler, executive request model,
executive validator, or runtime orchestrator is implemented today.

## Sprint 6.1 Through 6.3 Identity Decisions

Sprint 6.1 established:

```text
assessmentVersion = nguyen-ai-executive-assessment-v1
```

Meaning:

- It identifies the internal 48-question executive assessment input contract
  family.
- It is distinct from the current placeholder/public runtime value
  `nguyen-ai-readiness-v1`.
- It is not a runtime route, Lambda invocation, request ID, customer identity,
  timestamp, methodology version, package contract version, or production
  authority marker.

Sprint 6.2 established:

```text
nguyen-ai-executive-assessment-v1
  ->
business-decision-methodology-v1
```

Meaning:

- The v1 executive assessment identity binds to exactly one active methodology
  version.
- The service resolves the methodology version.
- Caller preference does not determine methodology execution.
- Version identity does not make unresolved methodology
  production-authoritative.

Sprint 6.3 established:

- No independent `inputContractVersion` is required for v1.
- `assessmentVersion` is the canonical executive input compatibility identity.
- A separate input-contract version may be introduced later only if a distinct
  governed compatibility concern emerges.

Sprint 6.4 uses these decisions to define runtime separation. It does not
change them.

## Current Public / Placeholder Runtime State

The current executable runtime remains:

```text
POST /assessment
  ->
lambda_function.lambda_handler()
  ->
handle_assessment()
  ->
validate_assessment_request()
  ->
score_assessment()
  ->
AssessmentResponse
```

Current runtime characteristics:

- The runtime is deployed and documented around `POST /assessment`.
- `handle_assessment()` creates a runtime request ID with `uuid4()`.
- `validate_assessment_request()` accepts the current placeholder request
  contract.
- `score_assessment()` returns deterministic placeholder output.
- `AssessmentResponse` includes placeholder readiness fields and runtime flags.
- The runtime does not invoke `evaluate_assessment()`.
- The runtime does not canonicalize 48 executive answers.
- The runtime does not build a `BusinessReadinessSnapshot`.
- The runtime does not build `ConfidenceEvaluation`.
- The runtime does not build `RecommendationPriorityEvaluation`.
- The runtime does not build `ExecutiveSummaryFoundation`.
- The runtime does not assemble or validate a `BusinessDecisionPackage`.

This path must remain current-runtime truth until a later approved runtime
implementation changes it.

## Public Runtime Responsibility

The current public or placeholder runtime responsibility is limited to the
existing `POST /assessment` behavior:

- Accept the current configured placeholder assessment version
  `nguyen-ai-readiness-v1`.
- Validate the current placeholder request shape.
- Return deterministic placeholder `AssessmentResponse`.
- Avoid Bedrock, DynamoDB, persistence, and AI model invocation.
- Preserve CORS behavior and Lambda proxy response shape as current runtime
  concerns.

The public or placeholder runtime does not own:

- Executive canonical input validation.
- The 48-question executive methodology contract.
- Methodology-version binding for executive evaluation.
- Decision Engine invocation.
- Business Decision Package assembly or validation.
- Executive runtime response construction.
- Executive recommendations, service decisions, or executive summaries.

## Future Executive Runtime Responsibility

A future executive runtime is responsible for accepting only the governed
executive assessment contract and handing validated canonical input to the
executive application/domain pipeline.

Conceptual future flow:

```text
Executive Transport Boundary
  ->
Executive Request Validation
  ->
Validated Canonical Executive Input
  ->
Application / Domain Orchestration
  ->
Decision Engine
  ->
DecisionEvaluationResult
  ->
BusinessReadinessSnapshot
  ->
ConfidenceEvaluation
  ->
RecommendationPriorityEvaluation
  ->
ExecutiveSummaryFoundation
  ->
BusinessDecisionPackage
  ->
BusinessDecisionPackageValidation
  ->
Validated BusinessDecisionPackage
```

The future executive runtime does not own methodology decisions. It invokes
approved deterministic components after the executive input boundary has
validated and canonicalized the submission.

## Required Logical Separation

Public and executive runtime processing must be logically separated.

Decision status:

- DECIDED: public and executive runtime paths must have distinct product
  contracts.
- DECIDED: public and executive runtime paths must have distinct request
  validation boundaries.
- DECIDED: public and executive runtime paths must have distinct
  handler/adapter responsibilities.
- DECIDED: public and executive runtime paths must have distinct response
  contracts.
- DECIDED: the current `POST /assessment` path must not accept both public and
  executive payloads.
- DECIDED: the current `handle_assessment()` path must not be promoted into
  the executive handler.

Rationale:

- The current runtime accepts placeholder answers and does not enforce the 48
  canonical executive questions.
- The executive input contract requires canonical IDs, complete answers,
  methodology binding, and no public IDs or aliases.
- A polymorphic route would make public/executive ambiguity a runtime concern
  and increase the risk of accidental contract promotion.
- The frozen boundary architecture prohibits hidden mapping, inference,
  aliases, or public-to-executive translation.

## Route Boundary Decision

Future executive runtime capability must use a distinct route boundary from
the current public or placeholder `POST /assessment` route.

Decision status:

- DECIDED: route-level separation is required for a future executive runtime.
- DECIDED: the concrete route path is not selected in Sprint 6.4.
- DECIDED: `POST /assessment` must remain the current placeholder/public path
  unless a future migration plan explicitly retires or redirects it.
- DECIDED: the future executive route must be named, documented, tested, and
  governed before implementation.
- DECIDED: the future executive route must not accept public directional
  payloads.

This decision does not require a specific URL such as `/executive-assessment`.
The architectural requirement is that the route boundary must be unambiguous
to callers, runtime adapters, operators, logs, tests, and downstream
governance.

The existing `POST /assessment` route must not become a polymorphic endpoint
that dispatches public or executive behavior solely based on payload contents.

## Request Contract Separation

Public and executive runtime requests must use distinct request contracts.

The current `AssessmentRequest` is not the executive canonical input contract.

Current `AssessmentRequest` characteristics:

- Includes `assessment_version`.
- Requires `organization`.
- Requires `respondent`.
- Stores mutable mapping payload structures.
- Stores `source_payload`.
- Accepts non-canonical placeholder question IDs through current validation.
- Does not require exactly one answer for every canonical executive question.
- Does not bind methodology version.
- Does not enforce methodology-configured answer ranges.

Future executive input contract requirements:

- Use `nguyen-ai-executive-assessment-v1`.
- Bind to `business-decision-methodology-v1` for v1.
- Require exactly one valid answer for each canonical executive question for
  complete executive evaluation.
- Reject public question IDs.
- Reject unknown executive question IDs.
- Reject missing canonical executive question IDs.
- Reject duplicate executive question IDs.
- Validate answer types and ranges from methodology configuration.
- Produce immutable validated canonical executive input before orchestration.

Reusable pattern:

- The existing request model demonstrates dataclass-based request handling and
  explicit field extraction.

Not reusable as executive contract:

- The existing `AssessmentRequest` shape and semantics.

## Validation Separation

Public and executive runtime validation must be separate.

The current `validate_assessment_request()` is not the executive canonical
validator.

Current validation responsibilities:

- Parse JSON.
- Reject duplicate JSON fields.
- Resolve the placeholder runtime assessment config.
- Validate top-level placeholder fields.
- Normalize answers from mapping or list transport shape.
- Reject duplicate list-form question IDs.
- Require numeric answer values.

Future executive validation responsibilities:

- Validate executive `assessmentVersion`.
- Reject `nguyen-ai-readiness-v1` at the executive boundary.
- Resolve the bound methodology version according to Sprint 6.2.
- Canonicalize answers into an immutable executive domain object.
- Validate canonical executive question IDs.
- Validate completeness for all 48 canonical questions for complete
  evaluation.
- Validate methodology-configured answer types and ranges.
- Reject public IDs, aliases, inferred mappings, synthetic answers, and
  automatic answer expansion.

Reusable validation patterns:

- JSON parsing behavior.
- Duplicate field rejection.
- Duplicate question ID rejection.
- Structured validation-result style.

Not reusable as executive validation semantics:

- Placeholder config resolution.
- Non-empty answer sufficiency.
- Arbitrary numeric answer acceptance.
- Organization/respondent/source payload requirements.

## Handler / Adapter Separation

Public and executive runtime paths must use distinct handler or adapter
responsibilities.

Decision status:

- DECIDED: `handle_assessment()` remains the current public/placeholder
  handler.
- DECIDED: a future executive runtime must enter through a distinct
  executive adapter or handler boundary.
- DECIDED: the executive adapter may delegate into a shared application layer
  only after executive validation and canonicalization.
- DECIDED: the executive adapter must not call `score_assessment()`.
- DECIDED: the public handler must not call the executive Decision Engine.

The exact future Python module and function names are implementation decisions
for a later increment.

## Existing Function Reuse Decisions

| Existing Function / Model | Future Executive Runtime Decision | Rationale |
| --- | --- | --- |
| `lambda_function.lambda_handler()` | May remain a shared Lambda entry point only if future route dispatch is explicit and tested. | Lambda entry is infrastructure; product semantics must be separated before validation. |
| `handle_assessment()` | Must not become the executive handler. | It owns current placeholder request/response behavior and request ID creation. |
| `validate_assessment_request()` | Must not become the executive canonical validator. | It validates placeholder runtime shape, not the 48-question executive contract. |
| `score_assessment()` | Must not become or call the executive Decision Engine. | It returns placeholder scoring and includes TODO-backed rubric behavior. |
| `AssessmentRequest` | Must not become the executive canonical input model. | It contains mutable context payloads and lacks canonical executive guarantees. |
| `AssessmentResponse` | Must not become the executive runtime response. | Sprint 5.5 separated placeholder response from future executive response. |
| `evaluate_assessment()` | Must remain the deterministic executive evaluation function. | Decision Engine owns executive evaluation truth after canonical input validation. |
| `build_business_decision_package()` | Must remain the package assembly function. | Package identity and limitations are already owned by Sprint 4. |
| `validate_business_decision_package()` | Must remain the package integrity validator. | Runtime separation must not duplicate package validation. |

## Application / Orchestration Handoff

A future executive adapter must hand off to the application/domain
orchestration layer only after it has:

- Identified the request as executive, not public.
- Accepted `nguyen-ai-executive-assessment-v1`.
- Rejected public or placeholder assessment identity.
- Bound `business-decision-methodology-v1` according to Sprint 6.2.
- Canonicalized the answer set.
- Produced immutable validated canonical executive input.

The adapter ends where deterministic domain orchestration begins.

The adapter may:

- Parse transport input.
- Invoke executive request validation.
- Reject invalid executive requests.
- Pass validated canonical executive input to orchestration.
- Transform successful domain results into the approved executive runtime
  response contract.

The adapter must not:

- Score answers.
- Normalize answers directly.
- Define mappings.
- Synthesize missing answers.
- Choose methodology arbitrarily.
- Generate recommendations.
- Select services.
- Rewrite deterministic outputs.
- Add runtime identifiers to the Business Decision Package.
- Invoke Bedrock or LLMs for business reasoning.

## Decision Engine Ownership

The Decision Engine remains the owner of deterministic executive evaluation
truth.

Runtime separation must preserve this ownership:

- The public runtime must not evaluate executive methodology.
- The executive adapter must not calculate scores.
- The executive orchestrator must invoke `evaluate_assessment()` with validated
  canonical executive answers and the selected methodology configuration.
- The Decision Engine owns answer normalization, question mapping, validation
  against methodology configuration, score aggregation, and explanation
  metadata.
- Downstream Sprint 3 and Sprint 4 components consume Decision Engine outputs
  without recomputing them.

No runtime adapter, handler, route, or shared infrastructure component may
replace the Decision Engine as deterministic evaluation authority.

## Permitted Shared Infrastructure

Public and executive runtime paths may share infrastructure when sharing does
not collapse product semantics.

Potentially permitted shared infrastructure:

- AWS account.
- API Gateway.
- Lambda deployment package.
- Lambda function, if explicit route dispatch is governed and tested.
- Authentication infrastructure.
- CORS utilities.
- Generic JSON parsing helpers.
- Generic duplicate-key detection helpers.
- Generic response serialization utilities.
- Generic logging library.
- Generic metrics library.
- Common immutable domain utilities.
- Packaging and deployment tooling.
- Test helper patterns.

Shared infrastructure does not authorize shared request semantics, validation
semantics, response semantics, scoring semantics, or assessment identity.

## Prohibited Semantic Sharing

The following sharing is prohibited:

- Reusing the public request contract as executive input.
- Reusing public validation semantics as executive validation semantics.
- Reusing public placeholder scoring as executive evaluation.
- Reusing `score_assessment()` as an executive Decision Engine adapter.
- Reusing public response fields as executive response identity.
- Accepting `nguyen-ai-readiness-v1` as executive assessment identity.
- Accepting public question IDs as canonical executive question IDs.
- Treating public answer values as executive methodology answers.
- Adding aliases from public IDs to executive IDs.
- Inferring executive answers from public answers.
- Synthesizing missing executive answers.
- Expanding public answers into the 48-question executive set.
- Sharing methodology binding authority with the caller.
- Hiding methodology limitations in executive responses.
- Treating the Business Decision Package as produced by public input.

## Cross-Routing Prevention

Runtime implementation must use defense-in-depth to prevent cross-routing.

Controls required for future implementation:

1. Distinct route boundary for executive runtime.
2. Distinct executive adapter or handler boundary.
3. Explicit `assessmentVersion` validation at the executive boundary.
4. Explicit rejection of `nguyen-ai-readiness-v1` by the executive boundary.
5. Explicit rejection of `nguyen-ai-executive-assessment-v1` by the public
   placeholder path unless a future governed migration retires that path.
6. Canonical executive question ID validation.
7. Complete 48-question answer-set validation for complete executive
   evaluation.
8. Rejection of unknown, duplicate, missing, aliased, inferred, or synthetic
   question answers.
9. Tests proving public payloads cannot reach the executive Decision Engine.
10. Tests proving executive payloads cannot be interpreted by public
    placeholder scoring.
11. Observability labels that distinguish public and executive activity.

These controls are architectural requirements. They are not implemented by
Sprint 6.4.

## assessmentVersion Boundary Role

`assessmentVersion` is necessary but not sufficient for runtime separation.

For the executive boundary:

- `nguyen-ai-executive-assessment-v1` identifies the canonical executive input
  compatibility family.
- The executive boundary must reject missing, unsupported, public, or
  placeholder assessment versions.
- The accepted executive assessment version triggers service-owned
  methodology-version binding.

For the public or placeholder boundary:

- `nguyen-ai-readiness-v1` remains tied to the current placeholder runtime
  configuration.
- The public/placeholder path must not accept executive assessment identity as
  a shortcut into the executive Decision Engine.

Runtime separation must also rely on route, adapter, request-contract, and
validation boundaries. Payload-level version checks alone are not enough
because a polymorphic route can still make public/executive behavior ambiguous
for callers, logs, tests, operations, and future compatibility.

## Logical Versus Physical Isolation

Logical isolation is required for v1.

Physical deployment isolation is not required by Sprint 6.4.

Decision status:

- DECIDED: public and executive runtime contracts must be logically isolated.
- DECIDED: distinct route and adapter boundaries are required.
- DECIDED: separate AWS accounts, separate API Gateway instances, separate
  Lambda functions, or separate repositories are not required by this
  architecture decision.
- DECIDED: physical separation may be chosen later for security, compliance,
  scaling, cost, operational, or blast-radius reasons, but it is not a
  prerequisite for the contract boundary itself.

If a future implementation shares a Lambda function, route dispatch must occur
before request validation and must be explicit, deterministic, and tested.

## Observability / Audit Separation Requirements

Future runtime activity must remain distinguishable for logging,
observability, metrics, auditability, and security review.

Minimum requirements:

- Public and executive route activity must be distinguishable.
- Public and executive validation failures must be distinguishable.
- Public and executive success responses must be distinguishable.
- Public and executive assessment versions must be logged or observable only
  according to future runtime metadata governance.
- Public runtime logs must not imply executive methodology execution.
- Executive runtime logs must not imply public directional scoring.
- Business Decision Package identity must remain deterministic and must not
  receive runtime IDs, timestamps, trace IDs, or API Gateway metadata.

Sprint 6.4 does not define concrete log fields, trace fields, metrics labels,
headers, or runtime metadata placement. Those belong to later Sprint 6
increments.

## Runtime Separation Decision Matrix

| Concern | Current Runtime Behavior | Future Executive Requirement | Sprint 6.4 Decision | Rationale | Evidence |
| --- | --- | --- | --- | --- | --- |
| Current route | `POST /assessment` | Must not be polymorphic public/executive runtime. | Keep as current placeholder/public path. | Avoids silent promotion. | `README.md`, `docs/deployment-guide.md`, `handler.py`. |
| Executive route | Not implemented. | Must be unambiguous. | Require distinct route boundary; exact URL deferred. | Route-level clarity supports governance and operations. | Sprint 5 readiness docs. |
| Public request model | `AssessmentRequest`. | Not executive canonical input. | Do not reuse as executive contract. | Lacks 48-question completeness and methodology binding. | `models.py`, `validation.py`. |
| Executive request model | Not implemented. | Immutable canonical input after validation. | Separate future model required. | Preserves deterministic domain entry guarantees. | Sprint 5.3 input contract. |
| Public validation | `validate_assessment_request()`. | Not canonical executive validation. | Separate executive validator required. | Current validation accepts any non-empty numeric answers. | `validation.py`, tests. |
| Public scoring | `score_assessment()`. | Not executive evaluation. | Must not call or become executive Decision Engine path. | Placeholder TODO-backed behavior. | `scoring.py`, `test_scoring.py`. |
| Executive evaluation | Domain pipeline exists separately. | Must invoke Decision Engine after canonical input. | Future adapter hands off to orchestration. | Preserves Decision Engine ownership. | `decision_engine.py`, orchestration docs. |
| Response contract | `AssessmentResponse`. | Future executive response contains validated package serialization unchanged. | Keep separate. | Placeholder response is not executive output. | Sprint 5.5 response contract. |
| Shared infrastructure | Lambda/API currently public path. | Sharing possible if semantics isolated. | Permit shared infrastructure with explicit separation. | Avoids unnecessary physical isolation. | README, deployment docs. |
| Cross-routing | No executive route exists. | Must be prevented. | Require route, adapter, version, and validation controls. | Defense-in-depth protects boundary. | Sprint 6.1-6.3. |
| Runtime metadata | Request ID exists in current handler. | Must not enter package identity. | Defer exact metadata placement. | Sprint 6.5 owns runtime metadata boundary. | `handler.py`, Sprint 5.5. |

## Current POST /assessment Decision

The existing `POST /assessment` route must not accept both public and
executive payloads.

Reasons:

- It would blur public and executive product contracts.
- It would make request validation polymorphic.
- It would increase the risk of hidden public-to-executive promotion.
- It would make route-level observability ambiguous.
- It would make consumer compatibility harder to reason about.
- It would allow future implementation shortcuts that bypass the explicit
  executive input boundary.

Any future migration of `POST /assessment` requires a separate migration
architecture. Sprint 6.4 does not approve such a migration.

## Current handle_assessment() Decision

`handle_assessment()` must not become the executive handler.

Reasons:

- It owns current placeholder request validation.
- It creates a runtime request ID and inserts it into placeholder response
  output.
- It returns current API Gateway proxy responses.
- It calls `score_assessment()`.
- It does not distinguish executive canonical input from public/placeholder
  input.
- It does not invoke package validation.

Future implementation may factor generic response-header utilities only if the
shared code remains free of public or executive business semantics.

## Current validate_assessment_request() Decision

`validate_assessment_request()` must not become the executive canonical
validator.

Reasons:

- It validates the current placeholder runtime config.
- It does not require canonical executive question IDs.
- It does not require all 48 executive answers.
- It does not bind methodology version.
- It does not validate methodology-configured answer ranges before Decision
  Engine execution.
- It treats organization and respondent as required runtime objects, while the
  executive input contract excludes them from core deterministic domain input
  unless later governance approves otherwise.

Reusable validation techniques include JSON parsing, duplicate detection, and
structured validation results.

## Current score_assessment() Decision

`score_assessment()` must not become or call the executive Decision Engine.

Reasons:

- It is explicitly a deterministic placeholder until the official rubric is
  supplied.
- It reads placeholder runtime configuration.
- It returns `AssessmentResponse`.
- It contains TODO-backed category, weight, threshold, and recommendation
  behavior.
- It does not produce `DecisionEvaluationResult`.
- It does not assemble or validate a `BusinessDecisionPackage`.

The future executive path must invoke the Decision Engine through the
application/domain orchestration layer described by Sprint 5.4.

## Future Executive Adapter Boundary

A future executive adapter should be responsible for transport-entry concerns
only.

Adapter responsibilities:

- Confirm the request reached the executive route boundary.
- Parse runtime transport input.
- Invoke executive input validation and canonicalization.
- Reject invalid executive inputs.
- Pass validated canonical executive input to orchestration.
- Receive successful domain result or internal failure result.
- Convert that result to the future executive runtime response or error
  contract.

Adapter prohibited behavior:

- Calculate readiness scores.
- Normalize answers outside the Decision Engine.
- Create question mappings or aliases.
- Infer missing answers.
- Convert public answers into executive answers.
- Select methodology arbitrarily.
- Generate recommendations.
- Generate executive narrative.
- Modify Business Decision Package content.
- Add runtime metadata into the package.

## Transport / Domain Boundary

Transport responsibility ends when the executive adapter has produced a
validated canonical executive input and resolved the governed methodology
binding.

Deterministic domain processing begins when orchestration receives:

- Accepted `assessmentVersion = nguyen-ai-executive-assessment-v1`.
- Bound `methodologyVersion = business-decision-methodology-v1`.
- Immutable canonical executive answers.
- Complete 48-question answer set for complete executive evaluation.
- No public IDs, aliases, inferred answers, synthetic answers, or raw transport
  payload dependency.

At that point, orchestration coordinates deterministic domain components. It
does not perform transport parsing or API response construction.

## Public Payload Protection

A public payload must be prevented from reaching the executive Decision Engine
by:

- Route-level separation.
- Executive adapter entry checks.
- Rejection of public or placeholder `assessmentVersion`.
- Rejection of public question IDs.
- Rejection of missing canonical executive questions.
- Rejection of unknown executive question IDs.
- No translation, aliases, inference, or answer expansion.
- Boundary tests that assert public payloads cannot invoke
  `evaluate_assessment()`.

## Executive Payload Protection

An executive payload must be prevented from being interpreted by public scoring
by:

- Keeping executive runtime on a distinct route boundary.
- Keeping `nguyen-ai-executive-assessment-v1` out of the current placeholder
  `ASSESSMENT_CONFIGS` unless a future migration explicitly governs otherwise.
- Rejecting unsupported versions in the current public/placeholder validation
  path.
- Avoiding assessment-version dispatch inside the current `POST /assessment`
  handler.
- Testing that executive identity is not accepted by the public placeholder
  path.

## Dependencies On Later Sprint 6 Increments

Sprint 6.4 creates these dependencies:

### Sprint 6.5 - Runtime Metadata Boundary

Sprint 6.5 must decide where runtime metadata belongs without adding it to
Business Decision Package identity.

Runtime metadata decisions must preserve:

- Public/executive route distinguishability.
- Public/executive validation distinguishability.
- Business Decision Package immutability.
- No request IDs, trace IDs, timestamps, or API Gateway context inside package
  identity.

### Sprint 6.6 - BusinessDecisionPackage API Exposure Governance

Future API exposure governance must preserve:

- BusinessDecisionPackage as canonical deterministic executive domain output.
- Public payloads cannot produce BusinessDecisionPackage output.
- Executive response does not hide package limitations.
- Package serialization is not silently repurposed as a public response.

### Later Runtime Implementation

Implementation must provide:

- Distinct executive route boundary.
- Distinct executive adapter or handler.
- Distinct executive input validation.
- Boundary tests for public/executive cross-routing prevention.
- Tests proving current `POST /assessment` behavior remains unchanged unless
  an approved migration changes it.
- Tests proving executive runtime does not call `score_assessment()`.
- Tests proving public runtime does not call `evaluate_assessment()`.

## Still-Unresolved Decisions

Sprint 6.4 leaves these decisions open:

- Concrete future executive route path.
- Future executive adapter/module/function names.
- Exact executive request model fields.
- Incomplete/draft executive submission behavior.
- Organization/respondent/source runtime-context placement.
- Runtime metadata field names and placement.
- Internal failure result strategy.
- External runtime error contract.
- Exact executive runtime response field names and response version.
- BusinessDecisionPackage API exposure governance.
- Physical deployment isolation, if future security or operational review
  requires it.

These open decisions must not be forced closed by implementation shortcuts.

## Explicit Non-Goals

Sprint 6.4 does not:

- Create a new API route.
- Modify API Gateway configuration.
- Modify Lambda behavior.
- Modify `lambda_function.py`.
- Modify `handle_assessment()`.
- Modify `validate_assessment_request()`.
- Modify `score_assessment()`.
- Create an executive request model.
- Create an executive validator.
- Create an executive handler or adapter.
- Implement runtime orchestration.
- Invoke the Decision Engine from runtime.
- Expose BusinessDecisionPackage through an API.
- Define runtime metadata fields.
- Define internal failure models.
- Define HTTP error contracts.
- Modify methodology configuration.
- Approve final weights, thresholds, scoring semantics, confidence formulas,
  recommendation rules, service decisions, or executive-summary methodology.
- Introduce public-to-executive translation.
- Introduce persistence, evidence repositories, dashboards, portfolio
  intelligence, Digital Twin capabilities, Bedrock, or LLM reasoning.

## Conditions Required Before Implementation

Before implementing public/executive runtime separation, the repository needs:

- Approval of this Sprint 6.4 architecture artifact.
- Runtime metadata boundary decision.
- Internal failure semantics.
- Runtime error contract.
- Executive runtime response field and version decisions.
- BusinessDecisionPackage API exposure governance.
- Test plan for route, adapter, version, validation, and cross-routing
  boundaries.

## Recommended Next Increment

The next bounded increment should be:

```text
Sprint 6.5 - Runtime Metadata Boundary
```

Sprint 6.5 should define what runtime metadata may exist around public and
executive runtime processing, where it belongs, and how it remains outside
BusinessDecisionPackage deterministic identity.
