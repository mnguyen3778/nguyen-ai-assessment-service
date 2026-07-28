# Executive Assessment Identity v1

## Purpose

This document finalizes the Sprint 6.1 architecture and governance decision
for executive assessment identity in the Nguyen AI Assessment Service.

The core question answered by this document is:

```text
What does executive assessmentVersion identify?
```

This is an engineering and contract decision. It does not approve final
business methodology, implement runtime behavior, define API routes, modify
Lambda handling, create an executive request model, or change the frozen Sprint
3, Sprint 4, or Sprint 5 architecture.

The Assessment Service remains the deterministic Business Decision Engine for
the Nguyen AI Executive Intelligence Platform. Executive assessment identity
exists to distinguish the governed internal 48-question executive assessment
contract from the public 12-question directional assessment and from the
current placeholder runtime path.

## Scope

This document defines:

- The governed executive `assessmentVersion` value.
- What the executive assessment version identifies.
- What changes require a new executive assessment version.
- What changes do not require a new executive assessment version.
- How executive assessment identity differs from public assessment identity,
  `methodologyVersion`, `BusinessDecisionPackage` `contractVersion`,
  component versions, and any future input-contract version.
- How the version is supplied, validated, made authoritative, and propagated.
- Minimal rejection responsibility for missing, unsupported, or incompatible
  assessment versions.
- Dependencies created for Sprint 6.2 and Sprint 6.3.

This document does not define:

- Final methodology weights.
- Readiness thresholds or levels.
- Final scoring semantics.
- Confidence formulas or confidence-level assignment.
- Recommendation-priority formulas or assignment.
- Recommendation generation.
- Service decisions.
- Executive-summary methodology.
- Runtime routes, HTTP status codes, error response bodies, or Lambda behavior.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/executive-assessment-input-contract-v1.md`
- `docs/architecture/executive-runtime-orchestration-architecture-v1.md`
- `docs/architecture/executive-runtime-response-contract-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`
- `docs/releases/sprint5-executive-runtime-readiness-foundation-complete-v1.md`

Sprint 3, Sprint 4, and Sprint 5 behavior and contracts remain frozen. This
document resolves the Sprint 5 open decision for exact executive
`assessmentVersion` only.

## Repository Evidence

The current repository establishes the following facts:

| Evidence | Current Meaning |
| --- | --- |
| `src/assessment/config.py` | Defines `nguyen-ai-readiness-v1` for the current placeholder runtime with TODO-backed question, category, weight, threshold, and recommendation configuration. |
| `src/assessment/validation.py` | Resolves incoming `assessmentVersion` against configured runtime versions and rejects unsupported versions before scoring. |
| `src/assessment/scoring.py` | Returns a deterministic placeholder response until the official rubric is supplied. |
| `src/assessment/models.py` | Defines current placeholder `AssessmentRequest` and `AssessmentResponse` shapes. |
| `src/assessment/methodology_config.py` | Defines the governed methodology version `business-decision-methodology-v1` and the canonical 48-question methodology vocabulary. |
| `src/assessment/business_decision_package.py` | Propagates assessment version into package audit and version metadata without defining which executive value is authoritative. |
| `docs/architecture/business-decision-package-versioning-v1.md` | Defines `assessmentVersion` as the assessment input contract used to construct package output. |
| `docs/architecture/executive-assessment-input-contract-v1.md` | Leaves the exact executive `assessmentVersion` value open and requires public and executive versions to remain distinct. |
| `docs/releases/sprint5-executive-runtime-readiness-foundation-complete-v1.md` | Lists exact executive `assessmentVersion` as an implementation-readiness and runtime-eligibility blocker. |

The current runtime value `nguyen-ai-readiness-v1` is not approved as the
executive assessment identity. It belongs to the current placeholder runtime
path and remains useful as repository evidence for existing validation and
version propagation behavior.

## Sprint 6.1 Decision

The governed executive assessment version is:

```text
nguyen-ai-executive-assessment-v1
```

Decision status:

- DECIDED: `nguyen-ai-executive-assessment-v1` identifies the internal
  executive assessment input contract family for the governed 48-question
  executive assessment.
- DECIDED: `nguyen-ai-executive-assessment-v1` is distinct from the current
  placeholder runtime version `nguyen-ai-readiness-v1`.
- DECIDED: `nguyen-ai-executive-assessment-v1` is distinct from any public
  directional assessment identity owned by the website.
- DECIDED: accepting this assessment version in architecture does not make the
  executive runtime implemented, runtime eligible, or production authoritative.

Rationale:

- The frozen boundary architecture requires public and executive assessment
  products to remain separate.
- The frozen package versioning architecture defines `assessmentVersion` as
  input-contract identity, not methodology identity or package-contract
  identity.
- The current placeholder version is tied to a runtime path that does not
  enforce canonical 48-question executive input and therefore must not be
  silently promoted.
- A distinct executive value gives future validators, orchestrators, package
  builders, and runtime consumers a stable identity to inspect without
  changing Decision Engine behavior.

## What assessmentVersion Identifies

`assessmentVersion` identifies the governed executive assessment input contract
used to produce deterministic Assessment Service outputs.

For `nguyen-ai-executive-assessment-v1`, the identity means:

- The submission belongs to the internal executive assessment product, not the
  public directional assessment product.
- The submission is intended for the canonical executive Decision Engine path,
  not the current placeholder scoring path.
- The accepted input must use canonical executive question IDs.
- The accepted input must provide exactly one valid answer for every configured
  canonical executive question before complete evaluation.
- The accepted input must be compatible with the methodology version bound in
  Sprint 6.2.
- The resulting deterministic outputs must preserve this assessment version
  through snapshot, confidence, priority, executive summary, package audit,
  package version metadata, and future runtime response representation.

`assessmentVersion` does not identify:

- A methodology version.
- A Business Decision Package contract version.
- A component version.
- A runtime route.
- A Lambda invocation.
- A request ID.
- A session.
- A customer.
- A persistence record.
- A timestamp.
- A specific set of submitted answers.
- Production-authoritative methodology approval.

## Public Assessment Identity Separation

The public directional assessment and internal executive assessment remain
separate products and contracts.

Rules:

- Public assessment identity must not be reused as executive assessment
  identity.
- `nguyen-ai-executive-assessment-v1` must not accept public question IDs.
- Public directional answers must not be inferred, expanded, or synthesized
  into executive answers.
- No public-to-executive mapping, aliasing, or translation is approved by this
  document.
- Any future public-to-executive translation capability requires a separate
  approved, versioned methodology and is outside Sprint 6.1.

The current `POST /assessment` placeholder runtime must not be silently
promoted into the executive runtime merely because a new executive
`assessmentVersion` is documented.

## Distinction From Other Version Identities

| Identity | Owner | Meaning | Relationship To Executive assessmentVersion |
| --- | --- | --- | --- |
| Public assessment identity | Website product boundary | Identifies the public 12-question directional assessment contract. | Must remain separate and must not be accepted as executive identity. |
| Executive `assessmentVersion` | Assessment Service input contract boundary | Identifies the internal executive assessment input contract. | Current Sprint 6.1 value is `nguyen-ai-executive-assessment-v1`. |
| `methodologyVersion` | Business Decision Methodology | Identifies governed methodology vocabulary and rules used by deterministic evaluation. | Must be bound to the executive assessment version but remains a separate identity. |
| `BusinessDecisionPackage` `contractVersion` | Package contract | Identifies package shape and serialization contract family. | Does not identify input contract. Current value remains `business-decision-package-v1`. |
| `componentVersions` | Package/component governance | Identify governed component baselines included in the package. | Do not identify assessment input contract. |
| Future input-contract version, if approved | Future input boundary | Would identify runtime input shape separately from assessment product identity. | Sprint 6.3 decides whether this is needed. It is not introduced by Sprint 6.1. |
| Runtime response version, if approved | Future runtime response boundary | Would identify external response shape. | Must not replace package or assessment identity. |

## Changes Requiring A New Executive assessmentVersion

A new executive `assessmentVersion` is required when the executive assessment
input contract changes in a way that affects the meaning, compatibility, or
required interpretation of submitted answers.

Examples:

- Adding, removing, retiring, or replacing canonical executive questions.
- Changing a canonical question ID.
- Changing the meaning of a canonical question while keeping the same ID.
- Changing which questions are required for a complete executive evaluation.
- Changing configured answer type expectations for existing questions.
- Changing configured answer ranges in a way that alters valid input meaning.
- Changing whether incomplete or draft submissions can enter evaluation.
- Introducing approved public-to-executive translation into the executive input
  contract.
- Introducing new executive assessment variants that are not backward
  compatible with v1 input expectations.
- Changing the assessment input contract so an existing v1 consumer could
  misinterpret submitted answers or resulting package identity.

These changes may also require a methodology version change, but the two
version identities remain separate.

## Changes Not Requiring A New Executive assessmentVersion

A new executive `assessmentVersion` is not required when the change does not
alter the executive input contract or the meaning of accepted submitted
answers.

Examples:

- Refactoring Python implementation without changing accepted input meaning.
- Adding tests for existing behavior.
- Updating documentation that clarifies but does not change the input contract.
- Changing Lambda, API Gateway, deployment, packaging, or infrastructure
  mechanics without changing executive input semantics.
- Adding downstream reporting, dashboarding, evidence repositories, workflow,
  persistence, or portfolio capabilities outside the deterministic assessment
  input contract.
- Updating `BusinessDecisionPackage` `contractVersion` because package shape
  changes while executive input semantics remain unchanged.
- Updating component versions for internal component implementation baselines
  without changing the executive input contract.
- Approving methodology changes that affect scoring, thresholds, confidence,
  recommendation priority, or executive summaries but do not change accepted
  input semantics. Those changes require methodology governance and may require
  a new `methodologyVersion`.

If a change affects both accepted input semantics and methodology evaluation
semantics, both `assessmentVersion` and `methodologyVersion` may need to
change.

## Relationship To methodologyVersion

`assessmentVersion` and `methodologyVersion` are related but not equivalent.

`assessmentVersion` answers:

```text
What executive assessment input contract did this submission use?
```

`methodologyVersion` answers:

```text
What governed Business Decision Methodology was used to evaluate the
submission?
```

Sprint 6.1 establishes that `nguyen-ai-executive-assessment-v1` must be bound
deterministically to an approved methodology version before runtime execution.
The current methodology baseline is:

```text
business-decision-methodology-v1
```

Sprint 6.1 does not define the binding mechanism. Sprint 6.2 must decide
whether the caller supplies `methodologyVersion`, the service resolves it from
the accepted executive `assessmentVersion`, or another governed mechanism is
required.

Binding an executive assessment version to a methodology version must not be
used to approve unresolved methodology. The Sprint 5.2 audit remains
authoritative for unresolved final weights, thresholds, scoring semantics,
confidence formulas, recommendation-priority assignment, recommendation rules,
service decisions, and executive-summary methodology.

## Caller And Service Responsibilities

Future runtime behavior must follow this responsibility split:

- The caller may present a candidate executive `assessmentVersion`.
- The service must validate the candidate against the governed set of accepted
  executive assessment versions.
- The service must reject missing, unsupported, public, placeholder, or
  incompatible assessment versions before executive canonicalization and before
  Decision Engine execution.
- The service must make the validated executive `assessmentVersion`
  authoritative at the executive input boundary.
- Downstream deterministic components must receive the validated value from the
  canonical input boundary rather than deriving it from runtime context.

Sprint 6.1 does not decide the exact runtime field placement, route structure,
HTTP behavior, or error response body.

## Authoritative Boundary

Executive `assessmentVersion` becomes authoritative at the future executive
input validation and canonicalization boundary.

Conceptual flow:

```text
Future executive runtime adapter
  ->
Executive input validation and canonicalization
  ->
accepted assessmentVersion = nguyen-ai-executive-assessment-v1
  ->
Decision Engine orchestration
```

Before this boundary, `assessmentVersion` is caller-supplied or transport
input. After this boundary, it is service-validated domain identity.

The Decision Engine itself does not own assessment identity. It evaluates
canonical answers against methodology configuration. Assessment identity is
introduced into downstream outputs when the future orchestrator builds the
`BusinessReadinessSnapshot`.

## Propagation Rules

The validated executive `assessmentVersion` must propagate unchanged through
the governed future pipeline:

```text
Canonical Executive Input
  ->
BusinessReadinessSnapshot.assessmentVersion
  ->
ConfidenceEvaluation.assessmentVersion
  ->
RecommendationPriorityEvaluation.assessmentVersion
  ->
ExecutiveSummaryFoundation.assessmentVersion
  ->
BusinessDecisionPackage.audit.assessmentVersion
  ->
BusinessDecisionPackage.versionMetadata.assessmentVersion
  ->
Future executive runtime response
```

Rules:

- The Decision Engine does not need to carry `assessmentVersion` in
  `DecisionEvaluationResult`.
- The future orchestrator must pass the validated executive assessment version
  into `build_business_readiness_snapshot()`.
- Every downstream Sprint 3 foundation output must preserve the same
  assessment version.
- `BusinessDecisionPackage` assembly and validation must continue rejecting
  mismatched source assessment versions.
- Runtime adapters must not rewrite package assessment version metadata.
- Downstream consumers must not present a package as if it were produced from a
  different assessment version.

## Unsupported Or Incompatible Versions

Sprint 6.1 defines only version identity responsibility, not full failure or
runtime error semantics.

Minimum required behavior:

- Missing executive `assessmentVersion`: reject before executive
  canonicalization.
- Non-string executive `assessmentVersion`: reject before executive
  canonicalization.
- Unsupported executive `assessmentVersion`: reject before executive
  canonicalization.
- Public directional assessment version: reject before executive
  canonicalization.
- Current placeholder runtime version `nguyen-ai-readiness-v1`: reject from
  future executive runtime canonicalization unless a later governed decision
  explicitly changes its status.
- Methodology-incompatible executive `assessmentVersion`: reject before
  Decision Engine execution once Sprint 6.2 binding rules are approved.

Later Sprint 6 increments own:

- Internal failure representation.
- External runtime error response contract.
- HTTP status code strategy.
- Runtime route and adapter behavior.

## Compatibility Rules

Consumers and future runtime components must treat
`nguyen-ai-executive-assessment-v1` as a governed compatibility boundary.

Rules:

- A component that does not recognize the executive assessment version must not
  consume the result as authoritative.
- A package produced from one assessment version must not be relabeled as
  another assessment version.
- Compatibility decisions must validate the package identity tuple in the
  order defined by the Business Decision Package versioning architecture:
  `contractVersion`, `assessmentVersion`, `methodologyVersion`, then
  `componentVersions`.
- Future additive response metadata must not change the meaning of the
  package's `assessmentVersion`.
- Runtime metadata must remain outside package identity.

## Decision Matrix

| Concern | Sprint 6.1 Decision | Rationale | Evidence | Status |
| --- | --- | --- | --- | --- |
| Exact executive `assessmentVersion` | Use `nguyen-ai-executive-assessment-v1`. | Separates the governed executive 48-question assessment from public and placeholder runtime contracts. | Sprint 5.3 left the value open; Sprint 4 versioning defines assessment version as input-contract identity. | DECIDED |
| Reuse `nguyen-ai-readiness-v1` | Do not reuse it as executive identity. | Current code ties it to placeholder validation and TODO-backed scoring config. | `src/assessment/config.py`, `src/assessment/scoring.py`, Sprint 5.2 audit. | DECIDED |
| Public assessment identity | Keep separate. | Public assessment is website-owned and directional. | `assessment-boundary-architecture-v1.md`. | DECIDED |
| Methodology identity | Keep separate from assessment identity. | Methodology governs evaluation vocabulary and rules, not input contract identity. | `methodology_config.py`, package versioning docs. | DECIDED |
| Package contract identity | Keep separate. | Package contract version governs package shape, not input contract. | `business-decision-package-versioning-v1.md`. | DECIDED |
| Component identity | Keep separate. | Component versions identify output component baselines, not assessment input. | `business_decision_package.py`. | DECIDED |
| Future input-contract version | Do not introduce in Sprint 6.1. | Sprint 6.3 must decide whether a separate input-contract version is necessary. | Sprint 5.3 open decision. | OPEN |
| Caller supplied vs service selected | Caller may present candidate; service must validate and make accepted value authoritative. | Preserves runtime validation responsibility without designing API shape. | Current validator resolves supported versions; Sprint 5.3 requires accepted executive identity. | DECIDED |
| Unsupported version behavior | Reject before executive canonicalization and Decision Engine execution. | Prevents public, placeholder, or incompatible input from entering executive pipeline. | Sprint 5.1 and 5.3 readiness gates. | DECIDED |
| Methodology binding mechanism | Defer to Sprint 6.2. | Binding is required but distinct from naming the assessment contract. | Sprint 5.3 open decision. | OPEN |

## Consequences

Sprint 6.1 creates these consequences for future work:

- Future executive runtime input validation must recognize
  `nguyen-ai-executive-assessment-v1` as the accepted executive assessment
  identity.
- Future executive runtime input validation must reject the current placeholder
  `nguyen-ai-readiness-v1` from the executive path unless a later governed
  decision changes that status.
- Future Business Decision Packages produced by the executive path must carry
  `nguyen-ai-executive-assessment-v1` in audit and version metadata.
- Existing placeholder runtime tests and fixtures using `nguyen-ai-readiness-v1`
  remain evidence of current behavior only; they are not the future executive
  identity.
- Sprint 6.2 must define methodology-version binding for the accepted
  executive assessment version.
- Sprint 6.3 must decide whether `assessmentVersion` alone is sufficient input
  contract identity or whether a separate input-contract version is required.

## Explicitly Unresolved Decisions

Sprint 6.1 intentionally leaves these decisions unresolved:

- Whether the future executive input payload includes caller-supplied
  `methodologyVersion`.
- Whether the service resolves methodology version from
  `nguyen-ai-executive-assessment-v1`.
- Whether a separate executive input-contract version field is required.
- The future executive runtime route or adapter design.
- Internal failure result representation.
- External runtime error response contract.
- Exact executive runtime response field names.
- Future runtime metadata placement.
- Governance action required to remove or revise the current
  `api-exposure-of-snapshot-consumers-not-implemented` package limitation.
- Any production-authoritative methodology decision identified in the Sprint
  5.2 audit.

## Conditions Required Before Implementation

Before executive runtime implementation begins, the following Sprint 6 decisions
must be completed:

1. Methodology-version binding for `nguyen-ai-executive-assessment-v1`.
2. Input-contract versioning decision.
3. Public/executive runtime separation strategy.
4. Runtime metadata boundary.
5. Business Decision Package API exposure governance.
6. Internal failure semantics.
7. Runtime error contract.
8. Runtime response contract final field and version decisions.
9. Contract test strategy.

Sprint 6.1 alone does not make the executive runtime implementation-ready.

## Explicit Non-Goals

This document does not:

- Modify Python source code.
- Modify tests.
- Modify methodology configuration.
- Modify the current Lambda runtime.
- Modify the current public `POST /assessment` placeholder behavior.
- Create an executive input model.
- Create an orchestrator.
- Create an executive response model.
- Define an API route.
- Define HTTP status codes.
- Define persistence behavior.
- Introduce request IDs, UUIDs, runtime timestamps, session IDs, or database
  identifiers.
- Approve final weights, thresholds, scoring semantics, confidence formulas,
  recommendation rules, service decisions, or executive-summary methodology.
- Introduce Bedrock, LLM, or probabilistic business reasoning.

## Recommended Next Increment

The next bounded Sprint 6 increment should be:

```text
Sprint 6.2 -- Methodology-Version Binding
```

Reason:

`nguyen-ai-executive-assessment-v1` now identifies the future internal
executive assessment input contract. The next required decision is how that
accepted assessment identity binds to the governed methodology version without
collapsing assessment identity and methodology identity into the same concept
or silently approving unresolved methodology.
