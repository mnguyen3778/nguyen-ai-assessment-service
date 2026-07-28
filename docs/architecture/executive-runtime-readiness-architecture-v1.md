# Executive Runtime Readiness Architecture v1

## Purpose

This document defines when the internal executive assessment pipeline is
eligible to become an authoritative runtime capability of the Nguyen AI
Assessment Service.

The Assessment Service is the deterministic Business Decision Engine for the
Nguyen AI Executive Intelligence Platform. Sprint 3 and Sprint 4 established
tested deterministic domain artifacts, including `DecisionEvaluationResult`,
`BusinessReadinessSnapshot`, `ConfidenceEvaluation`,
`RecommendationPriorityEvaluation`, `ExecutiveSummaryFoundation`, and
`BusinessDecisionPackage`.

Those artifacts are necessary for future runtime authority, but they are not
by themselves sufficient. A component can be architecturally complete and
fully tested while the business methodology it depends on remains incomplete.
A `BusinessDecisionPackage` can be structurally valid without being eligible
to represent final executive business conclusions.

This architecture exists to prevent technically valid foundation outputs from
being presented as production-authoritative executive intelligence before the
methodology, runtime contract, orchestration, validation, and governance gates
are approved.

## Scope

This document defines readiness gates only.

It applies to the internal 48-question executive assessment path owned by the
Assessment Service. It does not apply to the public 12-question directional
assessment owned by the website.

This document does not implement runtime integration, API behavior, Lambda
handler behavior, persistence, delivery envelopes, evidence ingestion,
recommendation generation, service routing, executive reporting, or downstream
platform capabilities.

## Current Baseline

Frozen baseline:

- Sprint 3 foundation outputs are complete and frozen.
- Sprint 4 Business Decision Package foundation is complete and frozen.
- The current Sprint 4 release baseline is
  `sprint4-business-decision-package-foundation-v1`.
- The current frozen commit is `754bdb7`.
- The current test baseline is 128 passing tests.

Authoritative references:

- `AGENTS.md`
- `docs/architecture/assessment-decision-engine-v2.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`

The frozen architecture must not be redesigned to make runtime integration
easier.

## Current Runtime State

The current Lambda runtime remains the production placeholder path:

```text
POST /assessment
  ->
Lambda handler
  ->
request validation
  ->
score_assessment()
  ->
AssessmentResponse
```

Current runtime characteristics:

- The handler validates the submitted request body.
- The handler invokes `score_assessment()`.
- `score_assessment()` returns the deterministic placeholder response.
- The runtime response remains the legacy `AssessmentResponse` shape.
- The runtime does not invoke the Decision Engine.
- The runtime does not build a `BusinessReadinessSnapshot`.
- The runtime does not build a `ConfidenceEvaluation`.
- The runtime does not build a `RecommendationPriorityEvaluation`.
- The runtime does not build an `ExecutiveSummaryFoundation`.
- The runtime does not assemble or validate a `BusinessDecisionPackage`.

Current runtime status:

- Architecture status: placeholder runtime path.
- Runtime-authoritative status: not ready.
- Production-authoritative status: not ready.

## Governed Domain State

The governed deterministic domain pipeline exists separately from the Lambda
runtime:

```text
Assessment Answers
  ->
Methodology Configuration
  ->
Answer Normalization
  ->
Question Mapping
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
```

Current domain characteristics:

- Methodology configuration owns canonical business vocabulary.
- The Decision Engine evaluates complete canonical answer sets.
- The Decision Engine rejects unknown question identifiers.
- The Decision Engine rejects missing canonical questions.
- The Decision Engine validates configured answer types and ranges.
- Snapshot, confidence, priority, summary, and package layers consume upstream
  outputs.
- The package is an immutable deterministic assembly contract.
- Package validation verifies contract integrity only.

Current domain status:

- Architecture status: foundation complete through Sprint 4.
- Implementation status: tested foundation implementation exists.
- Runtime-authoritative status: not connected to the Lambda runtime.
- Production-authoritative status: blocked by methodology and runtime gates.

## Readiness Definitions

This document introduces a small readiness vocabulary because the repository
needs to distinguish architecture completeness, methodology approval,
implementation completeness, runtime eligibility, and production authority.
Without this vocabulary, a tested foundation component could be mistaken for a
final executive decision capability.

Readiness states:

- `FOUNDATION_COMPLETE`: The architecture and/or implementation exists as a
  deterministic foundation, but final business methodology may still be
  incomplete.
- `METHODOLOGY_PENDING`: Required business rules, formulas, thresholds,
  mappings, or interpretation semantics are not yet approved.
- `IMPLEMENTATION_READY`: Required code exists, is deterministic, is tested,
  and conforms to approved methodology for its limited scope.
- `RUNTIME_ELIGIBLE`: The component or pipeline may be invoked by the
  Assessment Service runtime without violating methodology, contract, or
  boundary rules.
- `PRODUCTION_AUTHORITATIVE`: The component or pipeline may be represented to
  customers and downstream systems as final governed executive business
  intelligence for its approved scope.

These states are cumulative. A component cannot be
`PRODUCTION_AUTHORITATIVE` unless it is also methodologically approved,
implementation ready, runtime eligible, tested, documented, versioned, and
released.

## Executive Assessment Contract Readiness Gate

Purpose:

The authoritative executive runtime must consume the approved internal
48-question executive methodology contract. It must not silently consume,
translate, or reinterpret the public 12-question directional assessment.

Readiness requirements:

- The executive assessment version is explicitly defined.
- The executive input contract is separate from the public directional
  assessment contract.
- All canonical question identifiers are sourced from methodology
  configuration.
- The runtime requires a complete canonical answer set unless a governed
  incomplete-submission methodology is approved.
- Unknown canonical question identifiers are rejected.
- Missing canonical questions are rejected unless a governed partial-assessment
  methodology is approved.
- Public question IDs are not accepted as canonical question IDs.
- Public answer values are not silently transformed into executive answer
  values.
- Any future translation capability has its own versioned methodology,
  mapping rules, confidence impact, tests, and release approval.

Current status:

- Public/executive boundary is documented.
- Canonical executive methodology configuration exists.
- Runtime executive input contract is not approved.
- Current `POST /assessment` accepts the placeholder assessment version and
  generic numeric answers.
- Gate status: `METHODOLOGY_PENDING`.

## Methodology Readiness Gate

Purpose:

The runtime must not represent foundation outputs as final executive
intelligence until the business methodology is approved for runtime authority.

Readiness requirements:

- Canonical questions are approved and versioned.
- Readiness dimensions are approved and versioned.
- Evidence categories are approved and versioned.
- Question-to-dimension mappings are approved and versioned.
- Question-to-evidence mappings are approved and versioned.
- Answer types and normalization ranges are approved and versioned.
- Question weights are approved as final methodology, not placeholder values.
- Readiness thresholds are approved as final methodology, not placeholder
  thresholds.
- Scoring semantics are documented and approved.
- Confidence formulas are documented and approved.
- Confidence-level assignment methodology is documented and approved.
- Recommendation priority methodology is documented and approved.
- Executive summary methodology is documented and approved.
- Any service-decision methodology is explicitly approved before service
  decisions can be produced.
- Tests prove deterministic execution of every approved rule.

Current status:

- Canonical questions, dimensions, evidence categories, mappings, answer
  types, and normalization ranges exist in methodology configuration.
- Placeholder question weights exist.
- Placeholder thresholds exist.
- Final confidence formulas are not implemented.
- Final confidence-level assignment methodology is not implemented.
- Final recommendation priority assignment methodology is not implemented.
- Recommendation generation is not implemented.
- Final executive summary methodology is not implemented.
- Gate status: `METHODOLOGY_PENDING`.

## Decision Engine Readiness Gate

Purpose:

The Decision Engine must remain the source of deterministic evaluation truth
when the internal executive runtime becomes authoritative.

Readiness requirements:

- The Decision Engine consumes methodology configuration rather than embedded
  business rules.
- The Decision Engine validates complete canonical answer sets.
- The Decision Engine validates answer types and configured ranges.
- The Decision Engine normalizes answers deterministically.
- The Decision Engine aggregates scores deterministically.
- The Decision Engine preserves explanation metadata.
- The Decision Engine does not depend on Lambda, HTTP, API Gateway, Bedrock,
  databases, external services, runtime-generated identifiers, or timestamps.
- The Decision Engine does not generate recommendations, service decisions,
  executive narratives, dashboards, or reports.
- Any change to final weights, thresholds, or scoring semantics originates in
  approved methodology, not engine code.

Current status:

- Decision Engine v2 is implemented and tested as a deterministic foundation.
- The engine consumes methodology configuration.
- The engine uses configured placeholder weights.
- The engine is not currently invoked by the Lambda runtime.
- Gate status: `IMPLEMENTATION_READY` for foundation behavior.
- Runtime authority status: blocked by methodology and orchestration gates.

## Downstream Foundation Readiness Gate

Purpose:

Sprint 3 downstream foundation outputs must be eligible consumers of Decision
Engine output before they can participate in an authoritative runtime path.
Each layer must preserve upstream deterministic truth.

Readiness requirements:

- `BusinessReadinessSnapshot` remains a passive projection of
  `DecisionEvaluationResult`.
- `ConfidenceEvaluation` consumes `BusinessReadinessSnapshot` and does not
  alter readiness scores.
- `RecommendationPriorityEvaluation` consumes snapshot and confidence outputs
  and does not assign final priority until methodology is approved.
- `ExecutiveSummaryFoundation` consumes snapshot, confidence, and priority
  outputs and does not generate narrative text or executive reports until
  methodology is approved.
- Foundation outputs expose explicit limitation metadata.
- Foundation outputs do not recompute Decision Engine results.
- Foundation outputs do not hide methodology gaps.

Current status:

- `BusinessReadinessSnapshot`: `FOUNDATION_COMPLETE`.
- `ConfidenceEvaluation`: `FOUNDATION_COMPLETE`; final formulas and
  confidence-level assignment remain `METHODOLOGY_PENDING`.
- `RecommendationPriorityEvaluation`: `FOUNDATION_COMPLETE`; all configured
  priority factors remain not evaluated and final assignment remains
  `METHODOLOGY_PENDING`.
- `ExecutiveSummaryFoundation`: `FOUNDATION_COMPLETE`; all summary sections
  remain not evaluated and final narrative/report methodology remains
  `METHODOLOGY_PENDING`.
- Gate status: mixed foundation readiness; not production authoritative.

## BusinessDecisionPackage Eligibility Gate

Purpose:

The Business Decision Package must be distinguished by eligibility state. A
package may be structurally valid while still not eligible for runtime or
production-authoritative use.

Eligibility states:

- Structurally valid: the package satisfies the Sprint 4 package contract,
  serialization contract, versioning invariants, and contract validation.
- Methodologically eligible: all package contents that will be represented as
  executive conclusions are backed by approved methodology.
- Runtime eligible: the package can be produced by a governed runtime
  orchestration path from an approved executive assessment input contract.
- Production authoritative: the package can be represented to customers and
  downstream consumers as final governed executive business intelligence for
  its approved scope.

Readiness requirements:

- Package components are present.
- Package source versions are consistent.
- Package audit metadata is consistent.
- Package limitations are visible.
- Package serialization conforms to the approved contract.
- Package validation passes.
- Package contents do not contain hidden runtime metadata, generated
  identifiers, timestamps, API metadata, persistence metadata, or service
  routing.
- Package limitations accurately represent incomplete foundation behavior.
- Runtime consumers understand that structural validity is not the same as
  production-authoritative methodology.

Current status:

- Structurally valid: available when built from valid Sprint 3 outputs.
- Methodologically eligible: not ready for final executive conclusions.
- Runtime eligible: not ready because orchestration and runtime contracts are
  not approved.
- Production authoritative: not ready.
- Gate status: `FOUNDATION_COMPLETE` for structure; `METHODOLOGY_PENDING` for
  authority.

## Orchestration Readiness Gate

Purpose:

A future orchestration layer must invoke the governed deterministic pipeline
without moving business logic into runtime glue code.

Required future orchestration flow:

```text
Executive Assessment Request
  ->
executive request validation
  ->
Decision Engine
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
```

Readiness requirements:

- The orchestrator is separate from Lambda-specific code.
- The orchestrator consumes approved executive assessment inputs.
- The orchestrator does not consume public directional assessment payloads.
- The orchestrator does not duplicate request validation, methodology
  validation, answer normalization, aggregation, snapshot projection,
  confidence evaluation, priority foundation, summary foundation, package
  assembly, or package validation logic.
- The orchestrator preserves deterministic function order.
- The orchestrator returns structured domain outcomes and validation failures.
- The orchestrator does not generate request IDs, timestamps, persistence
  records, recommendations, service decisions, executive narratives, or API
  responses.
- Errors are deterministic and traceable to the failing gate or component.

Current status:

- Complete domain components exist.
- End-to-end orchestration exists in tests as helper construction, not as a
  production runtime component.
- No production orchestration component connects the complete pipeline to the
  handler.
- Gate status: not ready.

## Runtime Contract Readiness Gate

Purpose:

An executive runtime endpoint cannot exist safely until its input, validation,
response, and compatibility behavior are approved.

Readiness requirements:

- Executive input contract is defined separately from public directional
  input.
- Required input fields are documented.
- Canonical answer format is documented.
- Answer value types are documented.
- Incomplete submission behavior is documented.
- Unknown question behavior is documented.
- Invalid answer value behavior is documented.
- Unsupported assessment version behavior is documented.
- Methodology version compatibility behavior is documented.
- Runtime error response semantics are documented.
- Runtime success response representation is documented.
- The response decision explicitly distinguishes package serialization from
  API response shape.
- CORS and authentication behavior remain infrastructure/runtime concerns and
  do not change deterministic domain outputs.

Current status:

- Existing Lambda validation supports the placeholder assessment request.
- Existing Lambda response supports the placeholder `AssessmentResponse`.
- Business Decision Package serialization is documented but explicitly not an
  API contract.
- Executive runtime input contract is not approved.
- Executive runtime response contract is not approved.
- Gate status: not ready.

## Public / Executive Boundary Gate

Purpose:

The platform must preserve the approved distinction between the public
12-question directional assessment and the internal 48-question executive
assessment.

Readiness requirements:

- Public and executive assessment versions remain distinct.
- Public and executive question identifiers remain distinct.
- Public and executive answer models remain distinct.
- Public directional scoring is not presented as executive methodology
  coverage.
- Executive Business Decision Package output is not produced from public
  directional answers.
- No hidden mapping, inference, translation, or identifier substitution bridges
  public and executive contracts.
- Any future translation capability is separately approved, versioned,
  documented, tested, and released.

Current status:

- Boundary architecture is documented and frozen.
- Current website/public integration remains outside this repository's
  executive runtime path.
- Current handler path remains placeholder and should not be treated as the
  internal executive runtime.
- Gate status: governance-ready; runtime integration must preserve it.

## Governance and Release Readiness Gate

Purpose:

Runtime authority requires governance beyond successful unit tests.

Readiness requirements:

- All methodology changes are documented, versioned, tested, and approved.
- All architecture changes are documented before implementation.
- All contract changes have serialization, versioning, and validation coverage.
- Full unit test suite passes.
- Any new runtime path has deterministic tests.
- Any new orchestration path has invalid-input and boundary tests.
- Public/executive boundary tests prevent silent mapping.
- Limitation metadata remains visible until approved capabilities replace it.
- Release documentation identifies what is and is not authoritative.
- A release baseline and tag are created only after verification.

Current status:

- Sprint 3 and Sprint 4 release governance exists.
- Current test baseline is 128 passing tests.
- Runtime-authoritative governance does not yet exist.
- Gate status: foundation governance ready; runtime-authoritative governance
  pending.

## Prohibited Shortcuts

The following shortcuts are prohibited:

- Connecting the current public or placeholder `POST /assessment` payload
  directly to the executive Decision Engine.
- Accepting public 12-question IDs as canonical executive methodology IDs.
- Creating hidden public-to-executive mappings.
- Treating placeholder weights as final approved weights.
- Treating placeholder thresholds as final approved thresholds.
- Treating structural package validity as production-authoritative business
  readiness.
- Treating foundation confidence outputs as final confidence methodology.
- Treating not-evaluated priority factors as final priority assignments.
- Treating executive summary section metadata as executive narrative output.
- Returning `BusinessDecisionPackage` serialization as an API response without
  an approved API response contract.
- Adding runtime IDs, timestamps, persistence identifiers, request IDs, or
  transport metadata to the package contract.
- Moving business rules into Lambda handlers, API adapters, orchestration glue,
  dashboards, reports, or downstream consumers.
- Using AI, LLM, or Bedrock reasoning to alter deterministic readiness,
  confidence, priority, summary, package, or validation outputs.

## Explicit Non-Goals

Increment 5.1 does not:

- Implement an orchestrator.
- Modify the Lambda handler.
- Modify `score_assessment()`.
- Modify the Decision Engine.
- Modify methodology configuration.
- Modify Sprint 3 foundation behavior.
- Modify Sprint 4 package behavior.
- Modify tests.
- Define a new API route.
- Define OpenAPI or JSON Schema.
- Expose the Business Decision Package through an API.
- Persist packages.
- Create a delivery envelope.
- Implement final confidence formulas.
- Implement final confidence-level assignment.
- Implement final recommendation priority assignment.
- Generate recommendations.
- Generate service decisions.
- Generate executive narratives.
- Generate executive reports.
- Implement evidence ingestion.
- Implement dashboards, workflow, case management, portfolio intelligence, or
  Digital Twin behavior.

## Readiness Decision Matrix

| Gate | Current Status | Evidence | Runtime Impact |
| --- | --- | --- | --- |
| Executive Assessment Contract | `METHODOLOGY_PENDING` | Boundary exists; executive runtime input contract is not approved. | Runtime integration must wait. |
| Methodology | `METHODOLOGY_PENDING` | Canonical vocabulary exists; placeholder weights and thresholds remain; final confidence, priority, and summary rules are incomplete. | Production-authoritative output must wait. |
| Decision Engine | `IMPLEMENTATION_READY` for foundation behavior | Deterministic mapping, normalization, aggregation, and explanation exist. | Can support future runtime after methodology and orchestration gates. |
| Business Readiness Snapshot | `FOUNDATION_COMPLETE` | Passive projection exists and preserves Decision Engine values. | Can be consumed internally, not API-exposed. |
| Confidence Evaluation | `FOUNDATION_COMPLETE` with `METHODOLOGY_PENDING` final behavior | Foundation factors exist; final formulas and level assignment are not implemented. | Must be labeled foundation-level. |
| Recommendation Priority | `FOUNDATION_COMPLETE` with `METHODOLOGY_PENDING` final behavior | Configured factors exist; all factors remain not evaluated. | Must not be used as final priority. |
| Executive Summary | `FOUNDATION_COMPLETE` with `METHODOLOGY_PENDING` final behavior | Configured sections exist; all sections remain not evaluated. | Must not be used as narrative/report output. |
| Business Decision Package | Structurally valid when built from valid sources | Package assembly and validation exist. | Not runtime eligible until orchestration and contract gates pass. |
| Orchestration | Not ready | No production orchestration component exists. | Required before runtime authority. |
| Runtime Contract | Not ready | Package serialization is not an API contract; placeholder runtime response remains current. | Required before endpoint changes. |
| Public / Executive Boundary | Governance-ready | Boundary architecture is frozen. | Must constrain all runtime work. |
| Governance and Release | Foundation-ready | Sprint 3 and Sprint 4 baselines exist. | Runtime-authoritative release governance still required. |

## Conditions Required Before Runtime Integration

Runtime integration may begin only after these conditions are satisfied:

1. Executive assessment input contract is approved.
2. Public and executive runtime paths are explicitly separated.
3. Canonical methodology readiness gaps are resolved or explicitly versioned as
   foundation-only limitations.
4. Final or foundation-limited methodology scope is approved for runtime use.
5. Orchestration architecture is approved.
6. Runtime response representation is approved.
7. Runtime validation behavior is approved for incomplete submissions, unknown
   questions, invalid values, and version mismatches.
8. Business Decision Package eligibility rules are approved for runtime use.
9. Tests are planned for deterministic orchestration, boundary enforcement,
   invalid inputs, package validation, and limitation preservation.
10. Release documentation defines whether the runtime is foundation-level,
    runtime-eligible, or production-authoritative.

## Future Sprint Boundaries

Potential future Sprint 5 increments:

- Methodology completeness audit.
- Executive assessment input contract architecture.
- Runtime orchestration architecture.
- Runtime response contract decision.
- Runtime eligibility verification.
- Sprint 5 release baseline.

Potential future implementation work after architecture approval:

- Executive pipeline orchestration module.
- Runtime validation adapter for the executive assessment contract.
- Handler integration for an explicitly approved executive runtime path.
- Deterministic tests for orchestration and contract boundaries.

Deferred beyond Sprint 5 unless separately approved:

- Delivery envelope.
- API exposure of package outputs.
- Persistence.
- Evidence ingestion.
- Executive reports.
- Recommendations.
- Service routing.
- Dashboards.
- Portfolio Intelligence.
- Digital Twin.

Future work must consume the existing Decision Engine and Business Decision
Package rather than replacing or redefining them.
