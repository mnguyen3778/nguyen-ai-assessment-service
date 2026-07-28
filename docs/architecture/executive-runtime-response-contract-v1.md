# Executive Runtime Response Contract v1

## Purpose

This document defines the architecture governing what a future executive
runtime may return after successful deterministic orchestration of the Nguyen
AI Assessment Service.

The core question answered by this document is:

Given a validated `BusinessDecisionPackage`, what representation may cross the
executive runtime boundary without changing, duplicating, or weakening
deterministic domain truth?

This is a runtime response contract architecture document. It does not
implement a response model, API route, Lambda handler behavior, serialization
change, delivery envelope, persistence model, executive report, or downstream
platform feature.

## Scope

This document applies only to a future internal executive assessment runtime
response.

In scope:

- Runtime response ownership.
- Relationship between `BusinessDecisionPackage`, package serialization, and
  external runtime response representation.
- Direct package exposure analysis.
- Projection analysis.
- Wrapper/envelope analysis.
- Version, limitation, deterministic, immutability, and compatibility rules.
- Public/executive response separation.
- Runtime metadata and data-minimization boundaries.

Out of scope:

- Public 12-question directional assessment response behavior.
- Public-to-executive translation.
- API route design.
- HTTP status code design.
- Lambda handler changes.
- Business methodology changes.
- Persistence, delivery envelopes, reports, dashboards, evidence repositories,
  portfolio intelligence, and Digital Twin behavior.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/executive-assessment-input-contract-v1.md`
- `docs/architecture/executive-runtime-orchestration-architecture-v1.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint3-foundation-complete-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`

Sprint 3 and Sprint 4 behavior and contracts remain frozen.

## Current Runtime Response State

The current runtime response is the placeholder `AssessmentResponse` returned
by `score_assessment()` through `handle_assessment()`.

Current `AssessmentResponse` fields:

- `requestId`
- `assessmentVersion`
- `overallScore`
- `readinessLevel`
- `categoryScores`
- `recommendations`
- `modelInvoked`
- `persisted`

Current response characteristics:

- It belongs to the placeholder `POST /assessment` runtime path.
- It includes a runtime-generated request ID.
- It returns placeholder readiness values.
- It does not expose `DecisionEvaluationResult`.
- It does not expose `BusinessReadinessSnapshot`.
- It does not expose `ConfidenceEvaluation`.
- It does not expose `RecommendationPriorityEvaluation`.
- It does not expose `ExecutiveSummaryFoundation`.
- It does not expose `BusinessDecisionPackage`.
- It is not the executive runtime response contract.

Repository evidence:

- `src/assessment/handler.py`
- `src/assessment/scoring.py`
- `src/assessment/models.py`
- `tests/test_handler.py`
- `tests/test_scoring.py`

## Canonical Domain Output

The canonical deterministic domain output of successful Sprint 5.4
orchestration is a validated `BusinessDecisionPackage`.

The `BusinessDecisionPackage` is:

- The immutable deterministic Assessment Service output contract.
- The package containing Decision Engine and Sprint 3 foundation outputs.
- The source of package audit metadata.
- The source of package limitation metadata.
- The source of package version metadata.

The `BusinessDecisionPackage` serialization contract defines the deterministic
serialized shape of that domain artifact. It explicitly states that package
serialization is not an API contract, HTTP schema, persistence model, OpenAPI
document, or JSON Schema.

## Response Contract Principles

The executive runtime response contract must preserve these principles:

- Domain truth remains inside the validated `BusinessDecisionPackage`.
- Runtime response representation must not mutate package contents.
- Runtime response representation must not recompute scores, confidence,
  priority, summary, limitations, or version metadata.
- Runtime response representation must not hide methodology limitations.
- Runtime response representation must not turn foundation outputs into final
  executive conclusions.
- Runtime response representation must keep public and executive responses
  unambiguous.
- Runtime response representation must remain deterministic for identical
  validated packages and identical response contract versions.
- Runtime metadata must remain outside deterministic package identity.
- Downstream consumers may enrich around the result but must not rewrite
  deterministic truth inside it.

## Response Ownership

Decision status:

- DECIDED: the future executive runtime response contract is owned by the
  Assessment Service runtime/application boundary.
- DECIDED: the deterministic domain still owns the
  `BusinessDecisionPackage`.
- DECIDED: downstream platform services do not own the Assessment Service
  runtime response contract.
- DECIDED: Lambda handlers and API adapters may implement the approved response
  contract later, but they do not define business meaning.

Rationale:

The response contract is the boundary between the Assessment Service domain
artifact and external runtime consumers. It must be governed separately from
the package because the package serialization contract is intentionally not an
API schema.

## Direct Package Exposure Analysis

Option A: return canonical `BusinessDecisionPackage` serialization directly.

Benefits:

- No duplicate business object.
- Full deterministic traceability is preserved.
- Limitations and version metadata remain visible.
- Consumer receives the complete canonical package shape.

Risks:

- It collapses package serialization and API response contract.
- It contradicts the Sprint 4 serialization document unless a future governed
  decision explicitly promotes serialization to an API contract.
- It tightly couples external API compatibility to internal package contract
  evolution.
- It leaves no response boundary for runtime eligibility or response-contract
  compatibility.
- Current package limitations include API exposure as not implemented, which
  must be resolved before any runtime exposure.

Decision status:

- DECIDED: direct package serialization is not selected as the executive
  runtime response contract for Sprint 5.5.

Repository evidence:

- `docs/architecture/business-decision-package-serialization-contract-v1.md`
  states that serialization is not an API contract.
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
  prohibits returning package serialization as an API response without an
  approved API response contract.

## Projection Analysis

Option B: return a deterministic projection or view derived from the
`BusinessDecisionPackage`.

Potential benefits:

- A projection could reduce consumer coupling to full package internals.
- A projection could present only runtime-approved fields.
- A projection could support future consumer-specific read models.

Risks:

- A projection may hide limitations or source traceability.
- A projection may rename fields in ways that imply new business meaning.
- A projection may become a second output truth if not tightly governed.
- No current repository evidence identifies a specific consumer need that
  requires a subset view.

Decision status:

- DECIDED: a projection is not selected for the baseline executive runtime
  response contract.

Rule:

Any future projection must be purely representational. It must not recompute,
reinterpret, omit material limitations, assign confidence, assign priority,
generate recommendations, select services, or produce executive narratives.

## Wrapper / Envelope Analysis

Option C: use a separate runtime response representation that contains the
validated `BusinessDecisionPackage` serialization unchanged.

Benefits:

- Preserves the package as canonical domain truth.
- Keeps API/runtime compatibility separate from package serialization
  compatibility.
- Allows response-level contract identity without changing package identity.
- Allows response-level readiness and authority labeling without modifying
  package contents.
- Keeps limitations visible by carrying the package unchanged.
- Avoids projection risk.

Risks:

- Adds a second contract boundary that must be governed.
- Could become a delivery envelope if runtime, persistence, or transport
  metadata is added casually.
- Could duplicate package version metadata if not constrained.

Decision status:

- DECIDED: a minimal separate runtime response representation is selected.
- DECIDED: it should contain the validated `BusinessDecisionPackage`
  serialization unchanged.
- DECIDED: it must not be a delivery envelope.
- DECIDED: it must not include runtime IDs, timestamps, UUIDs, persistence IDs,
  delivery IDs, session IDs, or request IDs.
- OPEN: exact field names and exact response contract version value are future
  implementation decisions.

## Selected Runtime Response Strategy

The selected strategy is Option C:

```text
Executive Runtime Response
  |
  |-- response contract identity
  |-- runtime eligibility / authority status metadata
  |-- validated BusinessDecisionPackage serialization
```

The package section must be the canonical `BusinessDecisionPackage`
serialization emitted by `BusinessDecisionPackage.to_dict()`.

The response-level metadata must be deterministic and must not change package
meaning. Its purpose is boundary clarity, not business decision creation.

The future response contract may identify whether the result is:

- structurally valid
- methodology-eligible
- runtime-eligible
- production-authoritative

Those readiness states must follow `Executive Runtime Readiness Architecture
v1`. The response must not mark a result production-authoritative unless all
governed readiness gates are satisfied.

This document does not freeze exact field names.

## Structural Validity vs Production Authority

The response contract must preserve the distinction between:

- Structurally valid package.
- Methodology-eligible result.
- Runtime-eligible result.
- Production-authoritative result.

A validated `BusinessDecisionPackage` may be structurally valid while still
not production-authoritative.

Future runtime responses must not imply:

- Placeholder weights are final.
- Placeholder thresholds are final.
- Foundation confidence is final confidence methodology.
- Not-evaluated priority factors are final priority assignment.
- Summary section metadata is an executive narrative.
- Package validation alone makes a result production-authoritative.

## Limitations Preservation

The runtime response must preserve package limitations unchanged.

Current package limitations include:

- final confidence formulas not implemented
- final confidence-level assignment not implemented
- final recommendation assignment not implemented
- recommendation generation not implemented
- service decisions not implemented
- executive reporting not implemented
- executive narratives not implemented
- evidence ingestion not implemented
- persistence not implemented
- API exposure of snapshot consumers not implemented

The runtime response must not remove, suppress, rename, downgrade, or override
these limitation values.

Implementation blocker:

Before exposing package contents through a runtime response, the repository
must review whether the current API-exposure limitation remains accurate or
requires a governed package limitation update. That review must not silently
change Sprint 4 behavior.

## Version Identity

The response contract must reuse package version identity rather than duplicate
it as business identity.

Existing package identity:

- `versionMetadata.contractVersion`
- `versionMetadata.assessmentVersion`
- `versionMetadata.methodologyVersion`
- `versionMetadata.componentVersions`

Response-level version identity may be required only for the external response
shape. It must not replace or reinterpret package version metadata.

Decision status:

- DECIDED: package version metadata remains the authoritative identity for the
  deterministic package.
- DECIDED: a future runtime response contract version may identify the external
  response shape.
- DECIDED: response contract version is not package contract version.
- OPEN: exact response contract version value is not defined in Sprint 5.5.

## Determinism

For the same validated `BusinessDecisionPackage` and same response contract
version, the runtime response representation must be semantically identical.

If a future implementation defines canonical runtime response serialization,
it should also define deterministic field ordering.

This document distinguishes:

- Domain serialization determinism: governed by the Business Decision Package
  serialization contract.
- Transport encoding determinism: future runtime implementation concern.

Runtime response representation must not add nondeterministic fields.

## Immutability

Runtime response transformation must not mutate the `BusinessDecisionPackage`
or any contained Sprint 2/Sprint 3/Sprint 4 outputs.

Required rules:

- The package is read-only input to the response boundary.
- Package serialization is copied or referenced as an unchanged value.
- Response-level metadata is separate from package contents.
- Runtime adapters must not patch package fields to fit API needs.
- Consumers must not alter package fields and present the altered value as the
  original Assessment Service output.

## Error Boundary

Successful response architecture is separate from runtime error architecture.

The future runtime response contract defined here applies only after:

- Executive input validation succeeds.
- Orchestration succeeds.
- Package assembly succeeds.
- Package validation succeeds.

Failure cases such as invalid executive input, Decision Engine failure,
orchestration failure, package assembly failure, package validation failure, or
methodology-ineligible execution require a separate runtime error contract.

This document does not define HTTP status codes or detailed error bodies.

## Partial Result Policy

Successful executive runtime responses must not contain partial packages.

Rules:

- No partial `BusinessDecisionPackage` may be represented as complete.
- No incomplete downstream foundation output may be presented as successful
  package output.
- If orchestration fails, the successful response contract is not used.
- Failure responses should contain no authoritative business result unless a
  future error contract explicitly governs diagnostic output.

## Public / Executive Response Separation

The current `AssessmentResponse` is public/runtime placeholder-specific. It
must not be silently reused as the executive runtime response.

Current `AssessmentResponse` fields that must not carry into deterministic
executive response identity:

- `requestId`
- `modelInvoked`
- `persisted`
- placeholder `readinessLevel`
- placeholder `categoryScores`
- placeholder `recommendations`

Public and executive response contracts must remain unambiguous:

- Public directional responses remain website/public-flow concerns.
- Placeholder `POST /assessment` responses remain separate from future
  executive runtime responses.
- Executive responses must not be returned for public 12-question directional
  submissions.
- Public responses must not be labeled as executive Business Decision Package
  output.

## Consumer Compatibility

Future consumers of the executive runtime response must inspect compatibility
before consumption.

Minimum compatibility checks:

1. Recognize the runtime response contract version.
2. Confirm the response contains a validated package representation.
3. Validate or trust prior validation of the package contract.
4. Recognize `versionMetadata.contractVersion`.
5. Recognize `versionMetadata.assessmentVersion`.
6. Recognize `versionMetadata.methodologyVersion`.
7. Recognize required `versionMetadata.componentVersions`.
8. Inspect package limitations.
9. Inspect runtime eligibility and production-authority status.

Compatibility principle:

```text
recognized compatible contract
  -> consume

unknown or incompatible contract
  -> reject or refuse authoritative consumption
```

Consumers must not silently reinterpret unknown package or response contracts.

## Runtime Metadata Boundary

Runtime metadata does not belong inside deterministic business identity.

Runtime metadata includes:

- request IDs
- trace IDs
- timestamps
- Lambda invocation identifiers
- API Gateway request context
- session identifiers
- persistence identifiers
- delivery identifiers
- operator identifiers

Decision status:

- DECIDED: runtime metadata must not be added to the
  `BusinessDecisionPackage`.
- DECIDED: runtime metadata must not be part of deterministic package
  identity.
- DECIDED: Sprint 5.5 does not define runtime metadata fields.
- OPEN: whether future runtime metadata belongs in transport headers, runtime
  logs, a future error contract, or a separate delivery/persistence layer
  remains undecided.

## Data Minimization

The executive runtime response should not include input/contextual data that
is not required to understand the deterministic package result.

Do not include by default:

- organization metadata
- respondent metadata
- source payload
- raw request body
- HTTP request metadata
- authentication claims
- client profile details

If future runtime or downstream requirements need contextual metadata, that
metadata must be governed separately and stored outside deterministic package
contents.

## Downstream Enrichment Boundary

Downstream systems may enrich around the executive result.

Examples of downstream enrichment:

- evidence links
- analyst notes
- workflow status
- report-generation state
- client metadata
- portfolio relationships
- dashboard display state

Downstream enrichment must not:

- rewrite package fields
- overwrite package version metadata
- remove package limitations
- recompute readiness scores
- reinterpret confidence foundation output
- assign recommendation priority inside the Assessment Service result
- convert foundation summary sections into executive narratives without
  approved methodology

Downstream enrichment belongs in downstream-owned records or services.

## AI / Bedrock Boundary

No runtime response transformation may use Bedrock, LLMs, or probabilistic
reasoning to reinterpret deterministic `BusinessDecisionPackage` output.

Future AI-generated narratives, if ever approved, must remain separately
governed and must not alter deterministic package truth.

The executive runtime response contract must preserve deterministic Assessment
Service outputs exactly.

## Response Contract Decision Matrix

| Concern | Current Behavior | BusinessDecisionPackage Capability | Runtime Response Requirement | Decision | Rationale | Repository Evidence | Open / Closed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Response ownership | Placeholder `AssessmentResponse` owned by current runtime path. | Package owns domain truth only. | Future executive response belongs to runtime/application boundary. | Separate ownership. | Avoids making Lambda or package serialization the API owner. | `src/assessment/models.py`, package contract docs. | DECIDED |
| Direct package exposure | Not exposed. | Package has deterministic serialization. | External response must be governed separately from serialization. | Do not expose directly as the full response contract. | Serialization document says it is not an API contract. | Serialization contract, readiness architecture. | DECIDED |
| Projection | None. | Package contains full traceable output. | Projection must not hide truth or limitations. | Do not use projection for baseline. | No repository evidence requires a subset view. | Package tests preserve all outputs. | DECIDED |
| Wrapper/envelope | Current response is a placeholder runtime object. | Package is not a delivery envelope. | Minimal runtime response representation may contain package unchanged. | Use minimal separate response representation. | Separates API compatibility from package identity. | Sprint 4 and 5.4 docs. | DECIDED |
| Version identity | Current response has only assessment version plus request ID. | Package has contract, assessment, methodology, component versions. | Reuse package versions; add response version only for response shape. | Preserve package identity. | Prevents duplicate deterministic identity. | Versioning document. | DECIDED |
| Limitations | Placeholder response has no package limitations. | Package exposes limitations. | Limitations must remain visible. | Preserve unchanged. | Prevents foundation output from appearing final. | Package and serialization docs. | DECIDED |
| Determinism | Current response includes runtime-generated request ID. | Package serialization is deterministic. | Future executive response must avoid nondeterministic business fields. | No generated IDs/timestamps. | Preserves reproducibility. | Handler and versioning docs. | DECIDED |
| Immutability | Current response is newly built from placeholder scoring. | Package is immutable. | Response must not mutate package. | Read-only package transformation. | Keeps single source of truth. | Package tests. | DECIDED |
| Runtime metadata | Current response includes `requestId`. | Package excludes runtime metadata. | Keep runtime metadata outside deterministic response/package identity. | Defer metadata placement. | Avoids corrupting package identity. | Handler, package versioning docs. | OPEN |
| Organization/respondent/source metadata | Current request accepts them; current response does not return them. | Package does not require them. | Do not include by default. | Exclude from deterministic response. | Data minimization. | Input contract and package docs. | DECIDED |
| Partial results | Current placeholder response is all-or-nothing. | Package validation requires complete structure. | Successful response cannot contain partial package. | Prohibit partial success. | Preserves contract integrity. | Orchestration architecture. | DECIDED |
| Consumer compatibility | Not defined for placeholder response. | Package version metadata supports compatibility checks. | Consumers must inspect response and package versions. | Recognize or reject. | Prevents silent reinterpretation. | Versioning document. | DECIDED |
| Public/executive separation | Current `POST /assessment` returns placeholder response. | Package applies only to executive path. | Responses must remain unambiguous. | Separate contracts. | Prevents public result from becoming executive output. | Boundary and input contract docs. | DECIDED |
| Downstream enrichment | Not part of current runtime. | Consumers may enrich around package. | Keep enrichment outside response/package truth. | Downstream-owned records only. | Preserves Assessment Service boundary. | Package contract docs. | DECIDED |

## Open Architecture Decisions

Resolved in Sprint 5.5:

- Future API response representation should not be direct package serialization
  alone.
- Future baseline executive runtime response should be a minimal separate
  response representation containing the validated package serialization
  unchanged.
- Projection is not required for the baseline response.
- Delivery envelope is not part of Sprint 5.5.
- Current `AssessmentResponse` must not become the executive response contract.

Preserved as open:

- Exact executive `assessmentVersion`.
- Methodology version binding strategy.
- Separate input-contract version necessity.
- Incomplete/draft executive submission behavior.
- Exact executive runtime route, adapter, or version separation.
- Exact runtime response field names.
- Exact runtime response contract version value.
- Runtime error response contract.
- Runtime metadata placement.
- Package limitation update strategy if API exposure becomes implemented.

## Conditions Required Before Implementation

Before implementing an executive runtime response contract, the repository
needs:

- Approved executive input contract identity.
- Approved methodology version binding strategy.
- Approved orchestration implementation plan.
- Approved response contract field names and response contract version.
- Decision on how runtime response status represents structural validity,
  methodology eligibility, runtime eligibility, and production authority.
- Package limitation review for API exposure-related limitation text.
- Runtime error contract architecture.
- Tests planned for deterministic response transformation, package immutability,
  limitation preservation, version compatibility, no runtime metadata in
  package, public/executive response separation, and unknown contract handling.

## Explicit Non-Goals

This document does not implement:

- response Python models
- serialization changes
- BusinessDecisionPackage changes
- API routes
- HTTP status codes
- Lambda changes
- handler changes
- orchestration
- persistence
- delivery envelope
- request IDs
- runtime UUIDs
- timestamps
- database schemas
- evidence repositories
- dashboards
- reports
- recommendation generation
- service routing
- portfolio intelligence
- Digital Twin
- Bedrock or LLM reasoning
- methodology changes

## Sprint 5 Readiness Implications

Approving this response contract architecture does not make the executive
runtime ready.

It establishes only the response boundary principle:

```text
validated BusinessDecisionPackage
  -> minimal executive runtime response representation
  -> external consumer
```

Runtime implementation remains blocked by:

- open executive input identity decisions
- methodology pending items from Sprint 5.2
- orchestration implementation approval
- runtime error contract architecture
- package limitation review
- runtime route/adapter decisions
- release governance

## Recommended Sprint 5.6 Closure Work

Recommended Sprint 5.6 work:

- Create the Sprint 5 runtime readiness closure review.
- Consolidate open decisions from Sprint 5.1 through Sprint 5.5.
- Identify which decisions block implementation and which block only
  production authority.
- Define the smallest post-Sprint 5 implementation candidate, if any.
- Confirm whether Sprint 5 should freeze as an architecture/governance
  baseline before any runtime code is written.
