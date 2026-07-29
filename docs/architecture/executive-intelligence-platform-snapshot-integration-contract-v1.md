# Executive Intelligence Platform Snapshot Integration Contract v1

## Purpose

This document defines the immutable integration contract between the Nguyen AI
Assessment Service and the Nguyen AI Executive Intelligence Platform.

An integration contract is required because `ExecutiveAssessmentSnapshot` is
the final deterministic business artifact produced by the Assessment Service.
Future Executive Intelligence Platform components may consume that artifact,
but they must never redefine, mutate, recompute, or replace the deterministic
business truth it carries.

Contracts precede implementations so future APIs, persistence, reports,
dashboards, delivery packages, portfolio capabilities, client portals, and SaaS
modules can integrate with the Assessment Service without inventing their own
interpretation of snapshot truth.

Sprint 11 established consumer governance: downstream consumers may enrich
around `ExecutiveAssessmentSnapshot`, but they must not modify it or redefine
business truth. This document builds on Sprint 11 by defining the integration
guarantees the Assessment Service provides and the assumptions the Executive
Intelligence Platform may safely rely on before any downstream implementation
exists.

Sprint 12 is architecture only. It does not introduce Python implementation,
APIs, serialization, persistence, reporting, dashboard models, PDF generation,
delivery package implementation, portfolio intelligence implementation,
workflow orchestration, AI logic, Bedrock integration, or new business objects.

## Architectural Boundary

The governed boundary is:

```text
Assessment Service
        |
        v
ExecutiveAssessmentSnapshot
==============================
Snapshot Integration Contract
==============================
Executive Intelligence Platform
```

Ownership boundaries:

- The Assessment Service owns deterministic assessment execution and immutable
  business truth up to and including `ExecutiveAssessmentSnapshot`.
- `ExecutiveAssessmentSnapshot` owns the immutable post-runtime assessment
  state created from a successful `ExecutiveRuntimeResult`.
- `BusinessDecisionPackage` remains the canonical immutable deterministic
  business truth inside the snapshot.
- The Executive Intelligence Platform owns downstream integration,
  presentation, routing, caching, persistence, delivery, workflow, portfolio,
  and user-experience concerns outside the snapshot.

Responsibility boundaries:

- The Assessment Service guarantees that an emitted snapshot preserves the
  deterministic package, response status, and response contract version
  established before the integration boundary.
- The Executive Intelligence Platform must verify compatibility before using
  the snapshot.
- The Executive Intelligence Platform may route or enrich around compatible
  snapshots in downstream-owned records.
- The Executive Intelligence Platform must fail closed when compatibility,
  integrity, or authority is not established.

This contract is not an API route, HTTP schema, persistence schema, reporting
schema, dashboard model, delivery envelope, portfolio model, or SaaS product
contract.

## Contract Guarantees

The Assessment Service guarantees the following when it provides an
`ExecutiveAssessmentSnapshot` across this integration boundary.

### Immutable Snapshot

The snapshot is immutable after creation.

The Assessment Service does not provide mutable downstream state as
deterministic assessment truth.

### Immutable BusinessDecisionPackage

The `BusinessDecisionPackage` contained by the snapshot is the same package
preserved from the successful executive runtime result.

The package is not mutated, filtered, renamed, flattened, redacted, or
rewritten by snapshot creation.

### Deterministic Business Truth

Deterministic business truth remains inside `BusinessDecisionPackage`.

The snapshot does not recompute:

- readiness scores
- readiness dimensions
- confidence outputs
- recommendation-priority outputs
- executive summary foundation outputs
- audit metadata
- limitations
- version metadata

### Stable Identity

The Assessment Service preserves the identity values established by upstream
governed components.

Snapshot integration does not replace deterministic identity with downstream
route IDs, request IDs, persistence IDs, delivery IDs, report IDs, dashboard
IDs, workflow IDs, portfolio IDs, or client portal IDs.

### Version Preservation

The snapshot preserves:

- executive runtime response contract version
- `BusinessDecisionPackage` contract version
- assessment version
- methodology version
- component versions

No version identity replaces another.

### Production Authority

The snapshot preserves the production-authority status from the successful
executive runtime response.

Snapshot integration does not upgrade
`NOT_PRODUCTION_AUTHORITATIVE` to `PRODUCTION_AUTHORITATIVE`.

Snapshot integration does not declare methodology-pending outputs production
authoritative.

### Methodology Integrity

The methodology version carried by the package remains the authoritative
methodology identity for interpreting deterministic business truth.

The integration boundary does not allow the platform to select, override,
infer, or change methodology.

### Component Version Integrity

Component versions remain attached to package identity.

The platform may inspect component versions for compatibility. It must not
change them or use unknown component versions as compatible by default.

### Runtime Metadata Separation

Runtime metadata remains outside deterministic business truth.

Request IDs, correlation IDs, trace IDs, timestamps, Lambda invocation IDs,
API Gateway metadata, persistence IDs, delivery IDs, report IDs, workflow IDs,
and platform routing metadata do not become snapshot truth.

## Platform Assumptions

Downstream Executive Intelligence Platform components may safely assume the
following for an `ExecutiveAssessmentSnapshot` that has passed compatibility
checks at the integration boundary.

### Snapshot Completeness

The snapshot represents a completed successful executive runtime result.

The platform may assume an integration-accepted snapshot is not a partial
runtime result and does not represent an error response.

### Snapshot Immutability

The snapshot is read-only deterministic assessment state.

The platform may consume it repeatedly without expecting Assessment Service
truth to mutate in place.

### Authoritative Identity

Snapshot-carried identity and package-carried identity are authoritative for
compatibility and traceability.

Platform-generated IDs may reference the snapshot, but they do not replace
snapshot or package identity.

### Authoritative Versions

The version values carried by the runtime response status and package metadata
are authoritative for interpreting the snapshot.

The platform must not infer compatibility from file names, API routes,
database keys, report IDs, dashboard state, timestamps, or client workspace
metadata.

### Authoritative BusinessDecisionPackage

`BusinessDecisionPackage` remains the authoritative deterministic business
artifact inside the snapshot.

Platform components may present or reference package truth. They must not
create alternate deterministic business truth.

### Preserved Production Authority

Production-authority status is preserved by the snapshot.

The platform may rely on that status to determine whether a result may be used
for production-authoritative executive purposes, subject to future platform
authorization and delivery governance.

### Repeated Consumption

The same snapshot may be consumed repeatedly by compatible platform components
without changing deterministic business truth.

Repeated consumption may create downstream logs, caches, delivery records,
workflow records, notifications, or presentation artifacts. Those records must
remain outside snapshot truth.

## Compatibility Requirements

The Executive Intelligence Platform must verify compatibility before treating
a snapshot as consumable deterministic business truth.

The platform must verify:

- executive runtime response contract version
- `BusinessDecisionPackage` contract version
- assessment version
- methodology version
- component versions
- snapshot identity
- snapshot integrity
- package limitations
- production authority

Minimum integration compatibility sequence:

1. Confirm the artifact is an `ExecutiveAssessmentSnapshot` or a future
   explicitly governed representation of one.
2. Confirm the snapshot originated from a successful executive runtime result.
3. Confirm the response contract version is recognized.
4. Confirm the `BusinessDecisionPackage` contract version is recognized.
5. Confirm the assessment version is recognized.
6. Confirm the methodology version is recognized.
7. Confirm component versions are recognized or covered by an approved
   compatibility policy.
8. Confirm snapshot integrity has not been compromised.
9. Confirm package limitations remain visible.
10. Confirm production-authority status is compatible with the intended
    platform use.

The platform must fail closed on incompatibility.

Failing closed means:

- do not consume the snapshot as authoritative business truth
- do not route it to future executive consumers as compatible
- do not strip or rewrite fields to make it appear compatible
- do not upgrade production authority
- do not infer compatibility from downstream metadata
- do not ask AI, LLMs, or probabilistic systems to reinterpret compatibility

Future platform implementations may define downstream-owned quarantine,
logging, or support records for incompatible snapshots. Those records must not
modify snapshot truth.

## Integration Invariants

The following invariants must hold across the integration boundary:

- Snapshot identity never changes.
- `BusinessDecisionPackage` identity never changes.
- Business truth is never recomputed.
- Production authority never changes.
- Runtime metadata remains outside business truth.
- Platform metadata never becomes assessment truth.
- Snapshot integrity must always be preserved.
- Package contract version remains attached to package truth.
- Assessment version remains attached to package truth.
- Methodology version remains attached to package truth.
- Component versions remain attached to package truth.
- Package limitations remain visible.
- Downstream enrichment remains external to the snapshot.
- Platform consumers never redefine deterministic Assessment Service output.

If any invariant cannot be preserved, integration must fail closed.

## Platform Responsibilities

The Executive Intelligence Platform may:

- validate snapshot compatibility
- route compatible snapshots to future governed consumers
- cache snapshots or snapshot references
- reference snapshots from downstream-owned records
- enrich externally around snapshots
- present snapshot-derived information
- persist externally if future architecture permits
- associate operational, delivery, workflow, UI, or audit metadata outside the
  snapshot

The Executive Intelligence Platform must not:

- rewrite `ExecutiveAssessmentSnapshot`
- rewrite `BusinessDecisionPackage`
- change methodology
- change version identities
- modify deterministic values
- introduce conflicting business truth
- hide limitations
- alter production authority
- convert runtime or platform metadata into assessment truth
- use AI, LLMs, or Bedrock to alter deterministic truth
- route incompatible snapshots as compatible
- treat downstream presentation artifacts as Assessment Service output

The platform owns downstream behavior around the snapshot. It does not own the
deterministic business truth inside the snapshot.

## Relationship To Future Components

Future platform components may include:

- Executive Reports
- Executive Dashboard
- Delivery Packages
- Client Portal
- Portfolio Intelligence
- Executive PDF
- Future SaaS modules

These examples identify possible consumers only. This document does not define
their implementation, data models, routes, storage schemas, rendering
behavior, delivery behavior, workflow behavior, or product experience.

Each future component requires its own governed architecture before
implementation if it introduces a new contract, projection, persistence model,
presentation model, delivery workflow, portfolio aggregation behavior, AI
behavior, or client-facing product surface.

## Out Of Scope

Sprint 12 does not define:

- Python implementation
- APIs
- serialization
- persistence
- dashboard architecture
- report architecture
- PDF generation
- delivery package implementation
- portfolio intelligence implementation
- AI logic
- Bedrock integration
- workflow orchestration
- new business objects
- new deterministic values
- new methodology
- new response contracts
- new package contracts
- new snapshot serialization contracts
- validation code
- Lambda handlers
- API Gateway behavior
- client portal implementation
- future SaaS implementation

Sprint 12 does not modify:

- `BusinessDecisionPackage`
- `ExecutiveRuntime`
- `ExecutiveRuntimeResult`
- `ExecutiveAssessmentSnapshot`
- `AssessmentResponse`
- existing serialization contracts
- existing runtime metadata rules
- existing methodology configuration
- existing public runtime behavior

This document defines the integration contract only. It does not implement the
Executive Intelligence Platform or any future consumer.

