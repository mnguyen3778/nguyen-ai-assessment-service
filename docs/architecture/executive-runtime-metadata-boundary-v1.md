# Executive Runtime Metadata Boundary v1

## Purpose

This document finalizes the Sprint 6.5 architecture and governance decision
for metadata ownership and placement in the Nguyen AI Assessment Service.

The core question answered by this document is:

```text
What runtime or operational metadata may exist around executive runtime
processing without becoming deterministic BusinessDecisionPackage truth?
```

The `BusinessDecisionPackage` remains the canonical immutable deterministic
domain output. Runtime execution context must not silently become part of
deterministic business truth merely because an API invocation occurred.

Sprint 6.5 defines metadata ownership and placement. It does not implement
runtime metadata, finalize the executive response schema, modify package
serialization, create routes, modify handlers, or introduce persistence.

## Scope

This document defines:

- Metadata classification rules.
- Deterministic domain identity.
- Canonical business input.
- Runtime and transport context.
- Operational observability context.
- Persistence and delivery context.
- BusinessDecisionPackage exclusion rules.
- Runtime response placement boundaries.
- Timestamp classification rules.
- Request, correlation, and trace identity rules.
- Determinism and reproducibility invariants.
- Domain-component influence prohibitions.
- Public/executive observability separation requirements.
- Repeated-evaluation consequences.
- Dependencies for Sprint 6.6 through Sprint 6.9.

This document does not define:

- Concrete runtime metadata field names.
- Executive response field names.
- Executive response contract version.
- HTTP headers.
- Log schema.
- Metrics schema.
- Trace schema.
- Internal failure model.
- Runtime error body.
- Persistence record model.
- Delivery envelope.
- API Gateway or Lambda implementation.
- Business methodology changes.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/executive-assessment-identity-v1.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`
- `docs/architecture/executive-input-contract-versioning-v1.md`
- `docs/architecture/public-executive-runtime-separation-v1.md`
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
- `docs/architecture/executive-assessment-input-contract-v1.md`
- `docs/architecture/executive-runtime-orchestration-architecture-v1.md`
- `docs/architecture/executive-runtime-response-contract-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`
- `docs/releases/sprint5-executive-runtime-readiness-foundation-complete-v1.md`

Sprint 3, Sprint 4, Sprint 5, Sprint 6.1, Sprint 6.2, Sprint 6.3, and Sprint
6.4 behavior and contracts remain unchanged.

## Established Frozen Facts

The repository currently establishes these facts:

| Evidence | Current Meaning |
| --- | --- |
| `src/assessment/handler.py` | Current placeholder runtime creates `request_id = str(uuid4())` and places it into the placeholder response body. |
| `src/assessment/models.py` | Current `AssessmentResponse` contains `requestId`, `modelInvoked`, and `persisted`; current `AssessmentRequest` stores `source_payload`. |
| `src/assessment/business_decision_package.py` | `BusinessDecisionPackage` contains deterministic source outputs, package audit, limitations, and version metadata; it does not generate request IDs, timestamps, trace IDs, or runtime context. |
| `src/assessment/business_decision_package_validation.py` | Package validation checks package contract/version/audit/limitation/serialization integrity and does not validate runtime metadata. |
| `docs/architecture/business-decision-package-versioning-v1.md` | Package identity is `(contractVersion, assessmentVersion, methodologyVersion, componentVersions)` and explicitly excludes UUIDs, runtime IDs, timestamps, Lambda context, sessions, database keys, and HTTP resources. |
| `docs/architecture/business-decision-package-serialization-contract-v1.md` | Package serialization explicitly excludes API, HTTP, persistence, runtime timestamps, request identifiers, and generated identifiers. |
| `docs/architecture/executive-runtime-response-contract-v1.md` | Future executive runtime response is a minimal separate response representation containing package serialization unchanged; direct package serialization alone is not the API contract. |
| `docs/architecture/public-executive-runtime-separation-v1.md` | Public and executive runtime paths must be distinct, and BusinessDecisionPackage identity must not receive runtime IDs, timestamps, trace IDs, or API Gateway metadata. |
| `docs/architecture/executive-assessment-input-contract-v1.md` | Organization, respondent, source, runtime, transport, persistence, and session metadata are not required for deterministic evaluation. |

No executive runtime metadata implementation exists today.

## Sprint 6.1 Through 6.4 Dependencies

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

- No independent `inputContractVersion` is required for v1.
- `assessmentVersion` remains the canonical executive input compatibility
  identity.

Sprint 6.4 established:

- Future executive runtime requires a distinct route boundary.
- Public and executive request, validation, handler/adapter, and response
  boundaries must remain separate.
- `assessmentVersion` is necessary but not sufficient for runtime separation.
- Logical isolation is required.
- Physical deployment isolation is not required for v1.
- Current `POST /assessment` runtime remains unchanged.

Sprint 6.5 preserves those decisions and defines where runtime metadata may
exist without weakening deterministic package identity.

## Metadata Classification Model

Metadata in and around executive runtime processing must be classified before
it is added to any contract.

Sprint 6.5 uses five metadata classes:

1. Deterministic Domain Identity
2. Canonical Business Input
3. Runtime / Transport Context
4. Operational Observability Context
5. Persistence / Delivery Context

The classification controls ownership and placement. It does not automatically
add any metadata field to an API response, domain object, package, log, trace,
or persistence record.

## Deterministic Domain Identity

Deterministic domain identity identifies the governed deterministic artifacts
needed to interpret or reproduce Assessment Service outputs.

Current deterministic domain identity includes:

- `assessmentVersion`
- `methodologyVersion`
- `BusinessDecisionPackage` `contractVersion`
- `componentVersions`

These identities belong to canonical deterministic package metadata because:

- `assessmentVersion` identifies the executive assessment input contract used
  to construct package output.
- `methodologyVersion` identifies the governed methodology configuration used
  for deterministic evaluation.
- `contractVersion` identifies the Business Decision Package output contract
  and serialization shape.
- `componentVersions` identify governed component baselines represented inside
  the package.

These values are not runtime facts. They are governed compatibility and
reproducibility facts.

They may appear in:

- `BusinessDecisionPackage.audit`
- `BusinessDecisionPackage.versionMetadata`
- Package serialization.
- Future executive runtime responses that carry the package unchanged.
- Downstream compatibility checks.

They must not be replaced by:

- Request IDs.
- Trace IDs.
- Lambda invocation IDs.
- Timestamps.
- Persistence IDs.
- HTTP routes.
- Deployment environment names.

## Canonical Business Input

Canonical business input is information intentionally supplied, validated, and
approved as part of the executive assessment contract and legitimately allowed
to influence deterministic results.

Current canonical executive business input is limited to:

- Accepted executive `assessmentVersion`.
- Bound `methodologyVersion`.
- Exactly one valid answer for each configured canonical executive question
  for complete executive evaluation.

For v1, organization, respondent, source payload, request context, transport
metadata, persistence metadata, and session metadata are not required for
deterministic evaluation.

Future facts may become canonical business input only after governed approval.
For example, a business-effective date or assessment-period field could be a
deterministic input if all of the following are true:

- It is supplied intentionally by the caller or selected by a governed
  deterministic rule.
- It is validated as part of the canonical executive input contract.
- Its business meaning is documented.
- Its effect on methodology or output interpretation is approved.
- Its versioning impact is documented.
- Tests prove deterministic behavior.

A value is not runtime metadata merely because it is a date or time. The
question is ownership: was it a governed business fact used by deterministic
methodology, or was it generated because a runtime invocation occurred?

No current repository artifact defines a canonical date/time business input
for executive evaluation.

## Runtime / Transport Context

Runtime or transport context is information created because a particular
runtime invocation occurred.

Examples include:

- Request ID.
- Correlation ID.
- Trace ID.
- Lambda invocation ID.
- API Gateway request ID.
- HTTP method.
- HTTP route.
- HTTP headers.
- API Gateway request context.
- Transport receipt timestamp.
- Processing start timestamp.
- Processing completion timestamp.
- Deployment environment identifier.
- Runtime instance identifier.
- Authentication transport context.
- Session identifier.

These values may be useful for runtime operation, but they are not
deterministic business identity.

Rules:

- Runtime/transport context must not be inserted into
  `BusinessDecisionPackage`.
- Runtime/transport context must not alter Decision Engine behavior.
- Runtime/transport context must not alter package validation.
- Runtime/transport context must not be used to fill missing executive answers.
- Runtime/transport context must not select methodology arbitrarily.
- Runtime/transport context must not be treated as package equality or package
  identity.

## Operational Observability Context

Operational observability context is metadata used for logs, traces, metrics,
security review, and debugging.

Examples include:

- Request ID.
- Correlation ID.
- Trace ID.
- Runtime route label.
- Public versus executive runtime label.
- Validation outcome label.
- Component execution outcome label.
- Package validation outcome label.
- Latency measurements.
- Operational error category.
- Authentication or authorization decision summary, subject to privacy and
  security governance.

Operational observability context may be recorded in:

- Logs.
- Traces.
- Metrics.
- Security audit systems.
- Future internal failure diagnostics, if approved.

Operational observability context must remain outside:

- Decision Engine scoring.
- Snapshot construction.
- Confidence evaluation.
- Recommendation priority evaluation.
- Executive summary foundation.
- BusinessDecisionPackage assembly.
- BusinessDecisionPackage validation.
- Deterministic package identity.

Operational observability context may travel alongside orchestration for
logging or debugging only if it is isolated from domain component inputs and
cannot affect deterministic outputs.

## Persistence / Delivery Context

Persistence or delivery context is metadata created by storage, workflow, or
downstream delivery systems.

Examples include:

- Database primary key.
- Persistence record ID.
- Storage bucket/key.
- Retention policy identifier.
- Delivery ID.
- Export ID.
- Report generation ID.
- Workflow/case ID.
- Portfolio relationship ID.
- Downstream client workspace identifier.
- Persistence timestamp.
- Delivery timestamp.

These values are outside the Business Decision Package contract. They may be
needed by future downstream platform services, but they do not become
Assessment Service deterministic output truth.

Rules:

- Persistence/delivery context must not be written into the package merely
  because a package was stored or delivered.
- Downstream systems may associate persistence/delivery records with a package
  externally.
- Downstream systems must not replace package identity with persistence or
  delivery identity.
- Persistence or delivery metadata requires separate architecture before
  implementation.

## BusinessDecisionPackage Exclusion Rules

The following must never be inserted into `BusinessDecisionPackage` solely
because an API invocation occurred:

- `requestId`
- Request ID.
- Correlation ID.
- Trace ID.
- Lambda invocation ID.
- API Gateway request ID.
- HTTP route.
- HTTP method.
- HTTP headers.
- API Gateway request context.
- Runtime receipt timestamp.
- Processing timestamp.
- Current clock time.
- Deployment environment identifier.
- Runtime instance identifier.
- Session identifier.
- Authentication transport context.
- Persistence key.
- Database primary key.
- Delivery ID.
- Report ID.
- Workflow/case ID.
- Operator ID.

Adding any of these to the package contract would conflict with Sprint 4
package versioning and serialization unless a future governed contract version
explicitly changes the package architecture. Sprint 6.5 does not approve such
a change.

## Runtime Response Placement Boundary

Sprint 5.5 selected a future minimal executive runtime response strategy:

```text
Executive Runtime Response
  |
  |-- response contract identity
  |-- runtime eligibility / authority status metadata
  |-- validated BusinessDecisionPackage serialization
```

Sprint 5.5 also states that the selected runtime response must not include
runtime IDs, timestamps, UUIDs, persistence IDs, delivery IDs, session IDs, or
request IDs.

Sprint 6.5 preserves that baseline:

- The future successful executive runtime response may contain deterministic
  response-boundary metadata such as response contract identity and governed
  readiness/authority status.
- The package section must contain validated `BusinessDecisionPackage`
  serialization unchanged.
- Runtime operational metadata must remain outside the package.
- Runtime operational metadata must not be added to the successful executive
  response body under the current baseline.
- Future runtime operational metadata may be placed in transport headers, logs,
  telemetry, a future error contract, or a separately governed persistence or
  delivery layer, subject to later architecture.

Sprint 6.5 does not finalize exact successful response field names, response
contract version value, headers, error fields, or log fields.

## Timestamp Classification Rules

Timestamps must be classified by ownership and purpose.

### Runtime-Generated Timestamps

Runtime-generated timestamps include:

- API receipt time.
- Lambda invocation time.
- Processing start time.
- Processing completion time.
- Current clock time used during execution.

Rules:

- Runtime-generated timestamps must not influence deterministic evaluation.
- Runtime-generated timestamps must not appear in `BusinessDecisionPackage`.
- Runtime-generated timestamps must not participate in package identity,
  package serialization identity, or package validation.
- Runtime-generated timestamps may be used for logs, traces, metrics, or
  security audit records outside package truth.

### Persistence / Delivery Timestamps

Persistence or delivery timestamps include:

- Storage creation time.
- Export time.
- Delivery time.
- Report generation time.
- Workflow status transition time.

Rules:

- Persistence/delivery timestamps belong outside the package.
- They may be associated with a package in downstream-owned records.
- They must not alter deterministic package contents.

### Canonical Business Date/Time Inputs

A date/time value may be deterministic canonical business input only when it is
approved as part of the executive assessment contract or methodology.

Rules:

- It must be supplied or selected by a governed deterministic rule, not by the
  runtime clock.
- It must be validated before deterministic evaluation.
- Its business meaning must be documented.
- Its versioning impact must be clear.
- Its impact on outputs must be tested.

No current executive assessment contract defines such a date/time input.

## Request / Correlation / Trace Identity Rules

Request, correlation, and trace identifiers are operational identities.

Rules:

- They may identify a runtime invocation, transport request, trace, or
  operational debugging flow.
- They may be useful for logs, metrics, security review, support, and future
  failure diagnostics.
- They must not identify a `BusinessDecisionPackage`.
- They must not be included in package `audit`.
- They must not be included in package `versionMetadata`.
- They must not be included in package serialization.
- They must not participate in package equality.
- They must not participate in package hashes or deterministic serialization
  identity.
- They must not determine methodology selection.
- They must not influence business evaluation.

In the current placeholder runtime, `requestId` exists only in
`AssessmentResponse` and validation-error response bodies. That current
behavior remains separate from future executive deterministic package identity.

## Boundary Termination Model

Runtime metadata may exist around the deterministic pipeline, but it must
terminate before domain components that own business output truth.

Conceptual boundary:

```text
Transport
  |  runtime IDs, trace IDs, headers, request context
  v
Adapter
  |  may log operational context
  v
Executive input validation / canonicalization
  |  produces canonical business input
  v
Application / orchestration
  |  may receive side-channel observability context for logging only
  v
Domain components
  |  deterministic inputs only
  v
BusinessDecisionPackage
  |  deterministic package identity only
```

The orchestration layer may receive operational context only as side-channel
context for logging or diagnostics. That context must not be passed as an input
to deterministic domain components and must not change outputs.

## Determinism / Reproducibility Invariant

The following invariant must hold:

```text
same validated canonical executive input
+ same bound methodology configuration
+ same deterministic component versions
=
same deterministic BusinessDecisionPackage serialization
```

The invariant must hold even when runtime execution differs by:

- Request ID.
- Correlation ID.
- Trace ID.
- Lambda invocation ID.
- API Gateway request ID.
- Transport receipt time.
- Processing time.
- Deployment instance.
- Logging context.
- Persistence context.

Runtime context must not cause package serialization drift.

## Domain-Component Influence Prohibitions

Runtime metadata must not influence:

- Decision Engine scoring.
- Answer normalization.
- Question mapping.
- Dimension aggregation.
- Evaluation explanation metadata.
- BusinessReadinessSnapshot construction.
- ConfidenceEvaluation construction.
- RecommendationPriorityEvaluation construction.
- ExecutiveSummaryFoundation construction.
- BusinessDecisionPackage assembly.
- BusinessDecisionPackage validation.

Exceptions require a future governed architecture change that reclassifies a
specific fact as canonical business input and defines methodology, versioning,
validation, and tests.

## Public / Executive Observability Separation

Sprint 6.4 requires public and executive runtime activity to remain
distinguishable.

Sprint 6.5 metadata rules:

- Observability metadata may distinguish public and executive route activity.
- Observability metadata may distinguish public and executive validation
  failures.
- Observability metadata may distinguish public and executive success flows.
- Observability metadata must not imply public scoring executed executive
  methodology.
- Observability metadata must not imply executive orchestration executed
  public scoring.
- Shared logging, metrics, tracing, or security systems may be used only when
  product boundaries remain explicit.
- Public/executive labels are operational context; they do not replace
  `assessmentVersion`.

Sprint 6.5 does not define concrete log field names, metrics labels, tracing
attributes, or audit event schemas.

## Repeated Evaluation Behavior

The same canonical executive assessment may be evaluated more than once.

If the validated canonical input, bound methodology configuration, and
component versions are unchanged:

- `BusinessDecisionPackage.to_dict()` must remain reproducible.
- Package `versionMetadata` must remain the same.
- Package deterministic audit metadata must remain the same.
- Runtime request identifiers may differ.
- Runtime trace identifiers may differ.
- Runtime timestamps may differ.
- Logs and metrics may differ.
- Persistence or delivery records may differ.

Runtime differences do not make deterministic package output different. They
only identify operational executions or downstream records around the package.

## Package Equality / Hash / Validation Rules

Runtime metadata must not be used to establish:

- BusinessDecisionPackage equality.
- BusinessDecisionPackage deterministic identity.
- BusinessDecisionPackage serialization identity.
- Package validation success.
- Package validation failure.
- Package hash or checksum, if a future hashing architecture is approved.

Any future package hash or integrity mechanism must be based on deterministic
package serialization and governed package identity, not runtime context.

## Permitted Operational Uses

Runtime metadata may be used for:

- Logging.
- Tracing.
- Metrics.
- Operational debugging.
- Security investigation.
- Support correlation.
- Rate limiting, if future runtime architecture approves it.
- Abuse detection, if future security architecture approves it.
- Infrastructure troubleshooting.
- Associating an API request with a downstream persistence or workflow record,
  if future architecture approves those systems.

Operational use must not alter deterministic business outputs.

## Downstream Correlation Boundary

Downstream consumers may need to preserve operational correlation metadata
around a package.

Rules:

- Downstream consumers may store runtime request IDs, trace IDs, persistence
  IDs, delivery IDs, or timestamps in downstream-owned records.
- Downstream consumers may link those records to a package.
- Downstream consumers must treat the package as read-only deterministic truth.
- Downstream consumers must not write operational correlation metadata into
  the package and present it as Assessment Service output.
- Downstream consumers must not replace package version identity with
  downstream operational identity.

This document does not design downstream repositories, workflow systems,
reports, dashboards, delivery packages, or portfolio systems.

## Runtime Metadata Version Identity

Sprint 6.5 does not introduce a runtime metadata version identity.

Decision status:

- DECIDED: runtime metadata does not need its own version identity for Sprint
  6.5.
- DECIDED: operational metadata placement can be governed by future runtime
  response, error, logging, observability, persistence, or delivery contracts
  if those contracts are introduced.
- DECIDED: no runtime metadata version may replace package `contractVersion`,
  `assessmentVersion`, `methodologyVersion`, or `componentVersions`.

A future runtime metadata contract version may be justified only if a
specific runtime, logging, error, persistence, or delivery schema requires
independent compatibility management.

## Metadata Placement Matrix

| Metadata Class | Examples | Permitted Placement | Prohibited Placement |
| --- | --- | --- | --- |
| Deterministic Domain Identity | `assessmentVersion`, `methodologyVersion`, package `contractVersion`, `componentVersions` | Package audit/version metadata, package serialization, compatibility checks | Runtime-only replacement identifiers |
| Canonical Business Input | Canonical executive answers, approved business-effective date if later governed | Validated executive input, deterministic domain components when approved | Runtime context, hidden inference, unvalidated source payload |
| Runtime / Transport Context | request ID, trace ID, Lambda invocation ID, HTTP route, headers, request context | Adapter context, transport headers, logs, telemetry, future error contract if approved | BusinessDecisionPackage, package identity, deterministic scoring |
| Operational Observability Context | route label, validation outcome, latency, component execution outcome | Logs, traces, metrics, security audit systems | Domain scoring, package serialization, methodology selection |
| Persistence / Delivery Context | database key, delivery ID, report ID, workflow ID, persistence timestamp | Downstream-owned records after future architecture approval | BusinessDecisionPackage, Decision Engine, package validation |

## Dependencies On Sprint 6.6 Through 6.9

### Sprint 6.6 - BusinessDecisionPackage API Exposure Governance

Sprint 6.6 must preserve:

- Runtime metadata remains outside package truth.
- Package limitations remain visible.
- Package API exposure must not require adding request IDs, timestamps, trace
  IDs, or delivery identifiers to package serialization.
- Exposure governance must decide how the existing
  `api-exposure-of-snapshot-consumers-not-implemented` limitation is handled
  before runtime exposure.

### Sprint 6.7 - Deterministic Internal Failure Semantics

Sprint 6.7 must preserve:

- Internal failure results may reference operational context only as
  diagnostic side-channel metadata.
- Failure classification must not mutate package output.
- No partial or failed package becomes successful deterministic truth.
- Runtime IDs must not be required for deterministic failure meaning.

### Sprint 6.8 - Executive Runtime Error Contract

Sprint 6.8 must preserve:

- Runtime error responses may need correlation metadata for support, but exact
  fields remain future decisions.
- Error metadata must not expose implementation details unnecessarily.
- Error metadata must not alter package identity because failed requests do
  not produce successful packages.
- Public and executive error contracts remain distinguishable.

### Sprint 6.9 - Executive Runtime Response Contract Finalization

Sprint 6.9 must preserve:

- The successful executive response contains the validated package
  serialization unchanged.
- Successful response-body metadata remains deterministic response-boundary
  metadata under the current Sprint 5.5 baseline.
- Runtime operational metadata remains outside the package.
- Exact response field names and response contract version are still open
  until Sprint 6.9.
- Any proposal to include runtime operational metadata in a successful
  response body must explicitly reconcile with Sprint 5.5 and this Sprint 6.5
  boundary.

## Still-Unresolved Decisions

Sprint 6.5 leaves these decisions open:

- Exact executive response field names.
- Executive response contract version.
- HTTP header usage for request, correlation, or trace identifiers.
- Runtime log schema.
- Metrics schema.
- Trace attribute schema.
- Runtime error response fields.
- Internal failure result fields.
- Persistence record metadata.
- Delivery metadata.
- Whether any organization or respondent metadata belongs in future runtime
  adapter context.
- Whether raw source payload belongs in future runtime audit, evidence,
  observability, or nowhere.
- Whether any future canonical business date/time input is needed.

These decisions must be resolved only in their owning future increments.

## Explicit Non-Goals

Sprint 6.5 does not:

- Add runtime metadata fields.
- Add request IDs.
- Add correlation IDs.
- Add trace IDs.
- Add timestamps.
- Modify logging.
- Modify tracing.
- Modify metrics.
- Modify `BusinessDecisionPackage`.
- Modify package serialization.
- Modify package validation.
- Modify `AssessmentResponse`.
- Modify `handle_assessment()`.
- Create an executive route.
- Create an executive handler.
- Create an executive request model.
- Create an executive response model.
- Implement orchestration.
- Implement persistence.
- Implement delivery envelopes.
- Define HTTP headers.
- Define error response bodies.
- Approve methodology weights, thresholds, scoring semantics, confidence
  formulas, recommendation rules, service decisions, or executive-summary
  methodology.
- Introduce Bedrock or LLM reasoning.

## Conditions Required Before Implementation

Before implementing runtime metadata behavior, the repository needs:

- Approved Sprint 6.5 metadata boundary.
- Runtime error contract decisions.
- Executive response field and version decisions.
- Decision on any HTTP header or log/trace/metric placement.
- Tests proving runtime metadata does not change deterministic package output.
- Tests proving package serialization excludes runtime IDs, timestamps, and
  transport metadata.
- Tests proving public/executive observability remains distinguishable without
  collapsing product contracts.

## Recommended Next Increment

The next bounded increment should be:

```text
Sprint 6.6 - BusinessDecisionPackage API Exposure Governance
```

Sprint 6.6 should define what it means to expose a validated
`BusinessDecisionPackage` through a future executive runtime boundary while
preserving the Sprint 4 package contract, package limitations, and the Sprint
6.5 metadata boundary.
