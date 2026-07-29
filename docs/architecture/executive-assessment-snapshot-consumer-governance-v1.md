# Executive Assessment Snapshot Consumer Governance v1

## Purpose

This document defines the governance contract between the Nguyen AI Assessment
Service and all future Executive Intelligence Platform consumers.

The Assessment Service produces immutable deterministic business truth. The
`ExecutiveAssessmentSnapshot` is the final deterministic business artifact
produced by the Assessment Service boundary. Everything downstream of the
snapshot belongs to the Executive Intelligence Platform and must consume
business truth without redefining it.

This boundary exists because downstream implementation will eventually include
executive reports, dashboards, PDFs, delivery packages, client portals,
portfolio intelligence, APIs, and future SaaS capabilities. Those systems need
clear governance before implementation so they cannot accidentally become
decision engines, presentation-owned methodology layers, or alternate sources
of deterministic truth.

Governance must exist before downstream implementation because:

- consumers may need to display, cache, reference, enrich, persist, or deliver
  snapshot-derived artifacts
- those activities can introduce metadata, formatting, workflow state, and
  presentation concerns
- none of those concerns may alter deterministic assessment truth
- consumers must know which identities and versions to preserve
- consumers must fail closed when compatibility or authority is not established

Sprint 11 is architecture only. It does not introduce Python implementation,
new business objects, serialization, validation code, APIs, persistence,
reporting, dashboards, portfolio intelligence, PDF generation, or AI behavior.

## Architectural Boundary

The governed boundary is:

```text
Assessment Service
        |
        v
ExecutiveAssessmentSnapshot
=============================
Consumer Governance Boundary
=============================
Executive Intelligence Platform
```

Ownership:

- The Assessment Service owns deterministic business truth up to and including
  `ExecutiveAssessmentSnapshot`.
- `ExecutiveAssessmentSnapshot` owns the immutable post-runtime assessment
  state created from a successful `ExecutiveRuntimeResult`.
- `BusinessDecisionPackage` remains the canonical immutable deterministic
  business truth inside the snapshot.
- Executive Intelligence Platform consumers own presentation, delivery,
  workflow, persistence, portfolio, and user-experience concerns outside the
  snapshot.

Responsibility:

- The Assessment Service produces and protects immutable deterministic
  assessment state.
- The consumer governance boundary defines how future consumers may use that
  state.
- Executive Intelligence Platform consumers may enrich around the snapshot in
  downstream-owned records.
- Executive Intelligence Platform consumers must not modify, replace,
  recompute, reinterpret, or hide deterministic Assessment Service truth.

The boundary is not an API contract, persistence contract, report contract, UI
contract, PDF contract, portfolio model, or delivery envelope. Those concerns
remain future downstream architecture.

## Consumer Responsibilities

Downstream consumers are permitted to use `ExecutiveAssessmentSnapshot` as
immutable assessment state.

Consumers may:

- read the snapshot
- display snapshot-derived information
- cache the snapshot or a reference to it
- reference the snapshot from downstream-owned records
- enrich externally around the snapshot
- preserve snapshot identity
- preserve `BusinessDecisionPackage` identity
- preserve assessment version
- preserve methodology version
- preserve component versions
- preserve response contract version
- preserve response status
- preserve production-authority status
- preserve package limitations
- associate external UI, workflow, delivery, persistence, or audit metadata
  with the snapshot

Consumers must keep deterministic Assessment Service truth recognizable and
traceable when they display or reference it.

Consumers must treat the snapshot as read-only. Any downstream enrichment must
be stored outside the snapshot and must remain clearly owned by the downstream
system.

## Consumer Prohibitions

Consumers must never:

- mutate `ExecutiveAssessmentSnapshot`
- modify `BusinessDecisionPackage`
- recompute deterministic scores
- recalculate readiness
- recalculate confidence
- recalculate recommendation priority
- change methodology
- change methodology version
- change assessment version
- change package contract version
- change component versions
- change production authority
- convert runtime metadata into business truth
- replace snapshot identity
- replace package identity with persistence, delivery, report, dashboard, or
  API identifiers
- rewrite recommendations
- remove limitations
- hide limitations
- invent deterministic values
- infer deterministic values from presentation state
- use public directional assessment output as executive snapshot truth
- use AI, LLM, or Bedrock reasoning to alter deterministic truth
- present downstream enrichment as Assessment Service output

Consumers must not create a second business-decision layer in reports,
dashboards, PDFs, delivery packages, client portals, portfolio intelligence, or
future SaaS components.

## Consumer Invariants

The following invariants must hold for every downstream consumer:

- Snapshot identity never changes.
- `BusinessDecisionPackage` identity never changes.
- Package contract version never changes.
- Assessment version never changes.
- Methodology version never changes.
- Component versions never change.
- Production authority never changes.
- Runtime metadata never becomes business truth.
- Deterministic values are never recomputed downstream.
- Package limitations remain visible.
- Response status remains visible when authority or eligibility is relevant.
- Consumers may enrich externally but never modify the snapshot.
- Downstream records may reference the snapshot but must not replace it.
- Presentation state must not become deterministic assessment state.
- Persistence state must not become deterministic assessment state.
- Delivery state must not become deterministic assessment state.

If a consumer cannot preserve these invariants, it must fail closed and refuse
to treat the snapshot as consumable deterministic truth.

## Allowed External Enrichment

External enrichment is allowed only outside the snapshot.

Inside snapshot:

```text
ExecutiveAssessmentSnapshot
        |
        |-- BusinessDecisionPackage
        |-- response status
        |-- response contract version
```

Inside the snapshot, consumers must not add, remove, rename, or rewrite fields.

Outside snapshot:

```text
Downstream Consumer Record
        |
        |-- snapshot reference
        |-- UI state
        |-- report formatting
        |-- dashboard layout
        |-- delivery metadata
        |-- persistence metadata
        |-- API metadata
        |-- workflow status
        |-- notification history
```

Permitted external enrichment includes:

- UI state
- report formatting
- dashboard layout
- delivery metadata
- persistence metadata
- API metadata
- workflow status
- notification history
- client display preferences
- evidence links
- analyst notes
- report-generation status
- delivery status
- portfolio relationship metadata

External enrichment must never become business truth. It may describe how a
consumer displays, stores, delivers, routes, or correlates snapshot-derived
information. It must not change what the Assessment Service determined.

## Compatibility Requirements

Future consumers must validate compatibility before consuming a snapshot.

Consumers should verify:

- executive runtime response contract version
- `BusinessDecisionPackage` contract version
- assessment version
- methodology version
- component versions
- snapshot integrity
- package limitations
- production authority

Minimum compatibility sequence:

1. Confirm the artifact is an `ExecutiveAssessmentSnapshot` or a future
   governed representation of one.
2. Confirm the snapshot originated from a successful executive runtime result.
3. Confirm the response contract version is recognized.
4. Confirm the `BusinessDecisionPackage` contract version is recognized.
5. Confirm the assessment version is recognized.
6. Confirm the methodology version is recognized.
7. Confirm component versions are recognized or covered by a governed
   compatibility policy.
8. Confirm package limitations remain present and visible.
9. Confirm production-authority status supports the intended consumer use.

Consumers must fail closed when compatibility is unknown or incompatible.

Failing closed means the consumer refuses authoritative use. A consumer may
store an operational quarantine record or raise a compatibility error in
downstream-owned systems, but it must not reinterpret the snapshot, strip
fields, upgrade authority, or guess compatibility.

## Architectural Principles

This consumer governance boundary reinforces:

- Immutable business truth.
- Deterministic execution.
- Single source of truth.
- Separation of business and presentation.
- Governance before implementation.
- Consumer independence.
- Backward compatibility.
- Explicit compatibility checks.
- Fail-closed behavior.
- Runtime metadata isolation.
- Downstream enrichment outside deterministic truth.

The Assessment Service owns deterministic assessment state. Consumers own
presentation and platform behavior around that state.

Consumer independence means downstream systems may evolve their own UI,
workflow, delivery, reporting, persistence, and portfolio behavior without
requiring changes to deterministic Assessment Service truth. It does not mean
consumers may redefine Assessment Service outputs.

Backward compatibility means future consumers must continue honoring the
version and identity boundaries already established by Sprint 4 through Sprint
10. No consumer may treat an unknown future version as compatible by default.

## Future Consumers

Future consumers may include:

- Executive Reports
- Executive Dashboard
- Portfolio Intelligence
- Executive PDF
- Client Portal
- Delivery Package
- Future SaaS components

These examples are illustrative only. This document does not define their
implementation, data models, APIs, rendering behavior, persistence behavior,
delivery behavior, or user experience.

Each future consumer must receive its own governed architecture before
implementation if it introduces new contracts, persistence, presentation
models, delivery workflows, portfolio aggregation, evidence links, or AI
behavior.

## Out Of Scope

Sprint 11 does not define:

- Python implementation
- APIs
- persistence
- reporting
- dashboard models
- PDF generation
- serialization
- AI logic
- Bedrock integration
- portfolio intelligence implementation
- client portal implementation
- delivery package implementation
- future SaaS implementation
- new business objects
- new deterministic values
- new methodology
- new response contracts
- new package contracts
- new validation code
- runtime orchestration
- Lambda handlers
- API Gateway behavior

Sprint 11 does not modify:

- `BusinessDecisionPackage`
- `ExecutiveRuntime`
- `ExecutiveRuntimeResult`
- `ExecutiveAssessmentSnapshot`
- current public `AssessmentResponse`
- existing serialization contracts
- existing runtime metadata rules
- existing methodology configuration

This document governs future consumer behavior only. It does not implement any
future consumer.

