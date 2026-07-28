# Executive Methodology Version Binding v1

## Purpose

This document finalizes the Sprint 6.2 architecture and governance decision
for methodology-version binding in the Nguyen AI Assessment Service.

Sprint 6.1 established the executive assessment identity:

```text
nguyen-ai-executive-assessment-v1
```

Sprint 6.2 answers the next contract question:

```text
How is an executive assessmentVersion associated with the methodologyVersion
used for deterministic evaluation?
```

This is an engineering and contract decision. It does not finalize business
methodology, implement runtime orchestration, create an API route, modify the
Lambda handler, or change the frozen Sprint 3, Sprint 4, or Sprint 5
architecture.

## Scope

This document defines:

- What `methodologyVersion` identifies.
- The authoritative source of methodology version identity.
- The binding from `nguyen-ai-executive-assessment-v1` to the current governed
  methodology version.
- Selection responsibility for methodology version.
- Compatibility semantics.
- Propagation requirements.
- Reproducibility and audit requirements.
- Version-change rules.
- Minimal binding-boundary rejection responsibility.
- The distinction between methodology version identity and methodology
  readiness.
- Dependencies for Sprint 6.3 and later runtime implementation increments.

This document does not define:

- Final question weights.
- Final readiness thresholds or readiness-level assignment.
- Final scoring semantics.
- Risk caps or cross-dimension dependency rules.
- Final confidence formulas.
- Final recommendation-priority formulas.
- Recommendation generation.
- Service decision rules.
- Final executive-summary methodology.
- Runtime route, HTTP status, or error response shape.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/executive-assessment-identity-v1.md`
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

Sprint 3, Sprint 4, Sprint 5, and Sprint 6.1 behavior and contracts remain
unchanged.

## Established Frozen Facts

The repository establishes these facts:

| Evidence | Current Meaning |
| --- | --- |
| `src/assessment/methodology_config.py` | Defines `METHODOLOGY_VERSION = "business-decision-methodology-v1"` and constructs `BUSINESS_DECISION_METHODOLOGY` with that version. |
| `tests/test_methodology_config.py` | Verifies `BUSINESS_DECISION_METHODOLOGY.version` matches `business-decision-methodology-v1`. |
| `src/assessment/decision_engine.py` | Defaults deterministic evaluation to `BUSINESS_DECISION_METHODOLOGY` and validates supplied methodology configuration before evaluation. |
| `src/assessment/snapshot.py` | Writes `methodology_config.version` into `BusinessReadinessSnapshot.audit.methodologyVersion`. |
| `src/assessment/confidence.py` | Copies methodology version from snapshot audit and rejects snapshot/config mismatches. |
| `src/assessment/recommendation_priority.py` | Copies methodology version from snapshot/confidence sources and rejects mismatches. |
| `src/assessment/executive_summary.py` | Copies methodology version from snapshot/confidence/priority sources and rejects mismatches. |
| `src/assessment/business_decision_package.py` | Copies source methodology version into package audit and `versionMetadata`, and rejects source methodology-version mismatches. |
| `src/assessment/business_decision_package_validation.py` | Validates package methodology version presence and audit/version metadata consistency. |
| `docs/architecture/business-decision-package-versioning-v1.md` | Defines `methodologyVersion` as governed Business Decision Methodology identity, separate from `assessmentVersion`, `contractVersion`, and `componentVersions`. |
| `docs/architecture/executive-methodology-completeness-audit-v1.md` | Confirms `business-decision-methodology-v1` exists while final weights, thresholds, scoring semantics, confidence, priority, and summary methodology remain pending. |
| `docs/architecture/executive-assessment-identity-v1.md` | Establishes `nguyen-ai-executive-assessment-v1` and leaves methodology-version binding to Sprint 6.2. |

No runtime executive binding implementation exists today. The current Lambda
runtime remains the placeholder path and does not invoke the governed executive
Decision Engine pipeline.

## What methodologyVersion Identifies

`methodologyVersion` identifies the governed Business Decision Methodology
configuration used for deterministic evaluation and downstream foundation
outputs.

For the current repository, `business-decision-methodology-v1` identifies the
governed methodology configuration that includes:

- Canonical executive question IDs.
- Readiness dimensions.
- Evidence categories.
- Answer types and normalization ranges.
- Weight categories.
- Placeholder question weights.
- Placeholder thresholds.
- Confidence factor and level catalogs.
- Recommendation-priority level and factor catalogs.
- Executive-summary section catalog.
- Service catalog.
- Methodology-owned validation behavior.

`methodologyVersion` does not identify:

- Public assessment identity.
- Executive assessment input-contract identity.
- Business Decision Package contract shape.
- Component baseline versions.
- Runtime routes.
- Request IDs.
- Session IDs.
- Customer identity.
- Persistence records.
- Timestamps.
- Production-authoritative approval.

## Authoritative Source

The authoritative source of current methodology version identity is:

```text
BUSINESS_DECISION_METHODOLOGY.version
```

Current value:

```text
business-decision-methodology-v1
```

`BUSINESS_DECISION_METHODOLOGY` is the authoritative methodology object for
current deterministic foundation evaluation. Its version is defined in
`src/assessment/methodology_config.py` and validated by the methodology config
test suite.

Future implementation may introduce a governed methodology registry only after
architecture approval. Until such a registry exists, the repository has one
authoritative methodology configuration object.

## Sprint 6.2 Binding Decision

The current binding is:

```text
nguyen-ai-executive-assessment-v1
  ->
business-decision-methodology-v1
```

Decision status:

- DECIDED: `nguyen-ai-executive-assessment-v1` binds to exactly one
  methodology version in the current architecture:
  `business-decision-methodology-v1`.
- DECIDED: methodology version is service-resolved from the accepted executive
  assessment version for the current v1 binding.
- DECIDED: callers must not select arbitrary methodology versions for the
  current v1 executive assessment path.
- DECIDED: if a caller supplies a methodology version in a future runtime
  contract, the service must treat it as a compatibility assertion to validate,
  not as caller authority to choose methodology.
- DECIDED: the Decision Engine consumes a methodology configuration selected
  before invocation; it does not own runtime methodology selection.
- DECIDED: the current binding does not make the methodology
  production-authoritative.

Rationale:

- The repository currently has one authoritative methodology configuration.
- The package versioning architecture requires `assessmentVersion` and
  `methodologyVersion` to remain separate identities.
- Deterministic reproducibility requires a known methodology version before
  evaluation begins.
- Allowing callers to choose methodology without a governed compatibility
  registry would introduce ambiguity and could weaken reproducibility.
- The Sprint 5 methodology audit confirms that the current methodology can
  have version identity while remaining foundation-level and
  methodology-pending for final executive conclusions.

## Binding Model

The selected binding model for Sprint 6.2 is:

```text
one executive assessmentVersion
  ->
exactly one active methodologyVersion
```

For v1:

| Executive assessmentVersion | Bound methodologyVersion | Binding Status |
| --- | --- | --- |
| `nguyen-ai-executive-assessment-v1` | `business-decision-methodology-v1` | Active governed v1 binding |

This model is intentionally conservative.

It avoids:

- Multi-methodology caller selection without a registry.
- Silent evaluation against a methodology version not approved for the
  executive assessment version.
- Reinterpreting the same executive input under multiple methodology versions
  without governed compatibility rules.
- Collapsing assessment identity and methodology identity into one field.

Future support for one assessment version binding to a governed set of
compatible methodology versions is not prohibited, but it requires a separate
approved compatibility registry, version selection policy, tests, and release
documentation.

## Selection Responsibility

Methodology selection responsibilities are:

| Boundary | Responsibility |
| --- | --- |
| Caller | May identify the executive assessment version. May later provide a methodology-version compatibility assertion only if a future input contract approves that field. |
| Executive input boundary | Validates accepted executive assessment identity and resolves the bound methodology version. |
| Application/orchestration layer | Receives or obtains the already-bound methodology configuration and passes it to deterministic components. |
| Methodology configuration | Owns methodology vocabulary, validation, and version identity. |
| Decision Engine | Executes the selected methodology configuration; does not decide which methodology version is allowed for the assessment version. |
| Business Decision Package | Preserves selected assessment and methodology versions; does not select methodology. |
| Package validation | Verifies version consistency and structural contract integrity; does not decide methodology compatibility. |

The service, not the caller, owns authoritative methodology selection for the
current v1 executive path.

## Caller-Supplied methodologyVersion

Sprint 6.2 does not introduce a required caller-supplied `methodologyVersion`
field.

Decision status:

- DECIDED: the current binding can be service-resolved from
  `nguyen-ai-executive-assessment-v1`.
- DECIDED: caller-supplied methodology version is not required for v1
  deterministic reproducibility.
- DECIDED: if a later input contract permits caller-supplied
  `methodologyVersion`, the value must be validated against the service-owned
  binding and cannot override the bound methodology.
- DECIDED: missing caller-supplied `methodologyVersion` is not a binding error
  for v1 if the service can resolve the bound version from
  `assessmentVersion`.

Sprint 6.3 must decide whether a distinct input-contract version or additional
input field is required. That decision must not alter the binding semantics
defined here unless a new architecture increment approves the change.

## Authoritative Binding Boundary

The assessment/methodology binding becomes authoritative at the future
executive input validation and canonicalization boundary.

Conceptual flow:

```text
Future executive runtime adapter
  ->
candidate assessmentVersion
  ->
executive input validation and canonicalization
  ->
accepted assessmentVersion = nguyen-ai-executive-assessment-v1
  ->
bound methodologyVersion = business-decision-methodology-v1
  ->
validated canonical executive input
  ->
runtime orchestration
```

Before this boundary, methodology version is not authoritative. After this
boundary, the selected methodology version is a service-governed domain
identity that must propagate through the deterministic pipeline.

## Propagation Requirements

The selected methodology version must propagate unchanged through the future
pipeline:

```text
Validated Canonical Executive Input
  ->
selected methodology configuration
  ->
Decision Engine
  ->
DecisionEvaluationResult
  ->
BusinessReadinessSnapshot.audit.methodologyVersion
  ->
ConfidenceEvaluation.methodologyVersion
  ->
RecommendationPriorityEvaluation.methodologyVersion
  ->
ExecutiveSummaryFoundation.methodologyVersion
  ->
BusinessDecisionPackage.audit.methodologyVersion
  ->
BusinessDecisionPackage.versionMetadata.methodologyVersion
  ->
BusinessDecisionPackageValidation
  ->
future executive runtime response
```

Rules:

- The future input boundary must bind methodology version before Decision
  Engine execution.
- The orchestrator must pass the selected methodology configuration to
  `evaluate_assessment()`.
- The orchestrator must pass the same methodology configuration to downstream
  builders that require it.
- `DecisionEvaluationResult` does not currently carry methodology version.
  Methodology version enters serialized output through snapshot audit and
  downstream foundation outputs.
- Downstream foundation builders must continue rejecting source/config
  methodology mismatches.
- `BusinessDecisionPackage` assembly must continue rejecting source
  methodology-version mismatches.
- `BusinessDecisionPackageValidation` must continue validating package audit
  and version metadata consistency.
- Runtime response transformation must not rewrite package methodology
  metadata.

## Reproducibility And Audit Requirements

The binding preserves reproducibility by requiring:

- Accepted executive assessment identity.
- Deterministically resolved methodology version.
- Validated methodology configuration.
- Package audit metadata containing the selected methodology version.
- Package version metadata containing the selected methodology version.
- Consumer compatibility checks that inspect `methodologyVersion`.

For identical canonical executive answers, identical
`nguyen-ai-executive-assessment-v1` input identity, identical
`business-decision-methodology-v1` configuration, and identical component
versions, deterministic domain outputs must be reproducible.

The binding must not depend on:

- Runtime-generated IDs.
- Timestamps.
- Lambda invocation context.
- API Gateway metadata.
- Persistence records.
- Caller preference.
- Environment-specific defaults.
- Bedrock, LLM, or probabilistic reasoning.

## Methodology Readiness vs Version Identity

Version identity is not methodology approval.

`business-decision-methodology-v1` can be a valid methodology version while
some methodology areas remain foundation-level, placeholder, or pending.

Current readiness status from the Sprint 5.2 audit:

| Methodology Area | Current Status |
| --- | --- |
| Canonical question catalog | `APPROVED_IMPLEMENTED` for foundation scope |
| Readiness dimensions | `APPROVED_IMPLEMENTED` for catalog; foundation scoring remains limited |
| Evidence categories | `APPROVED_IMPLEMENTED` for catalog and traceability |
| Answer normalization for current question types | `APPROVED_IMPLEMENTED` |
| Numeric question weights | `PLACEHOLDER` |
| Readiness thresholds | `PLACEHOLDER` |
| Final scoring semantics | `METHODOLOGY_PENDING` |
| Confidence formulas and level assignment | `METHODOLOGY_PENDING` |
| Recommendation-priority assignment | `METHODOLOGY_PENDING` |
| Recommendation generation | `DEFERRED` |
| Service decisions | `DEFERRED` |
| Executive-summary conclusions/narratives | `METHODOLOGY_PENDING` or `DEFERRED` |

Therefore:

- `business-decision-methodology-v1` is an approved version identity for the
  current deterministic foundation.
- It is not approval to present every downstream field as
  production-authoritative executive intelligence.
- Runtime eligibility still depends on input, orchestration, response, failure,
  limitation, and release-governance decisions.
- Production authority still depends on final business-methodology approval.

## Changes Requiring A New methodologyVersion

A new methodology version is required when methodology meaning, deterministic
evaluation behavior, or methodology-owned output semantics change.

Examples:

- Changing canonical question IDs.
- Changing canonical question meaning.
- Changing question-to-readiness-dimension mapping.
- Changing question-to-evidence-category mapping.
- Changing expected answer type for an existing question.
- Changing answer normalization range or semantics.
- Replacing placeholder question weights with approved numeric weights.
- Approving final equal-weight methodology as final methodology, if that
  changes the status or meaning of current placeholder weights.
- Replacing placeholder thresholds with approved readiness thresholds.
- Adding readiness-level assignment methodology.
- Adding final scoring semantics.
- Adding risk caps or cross-dimension dependency rules.
- Adding final confidence formulas.
- Adding final confidence-level assignment.
- Adding recommendation-priority factor formulas.
- Adding final recommendation-priority assignment or tie-breaking.
- Adding recommendation generation rules, if recommendations are emitted.
- Adding service decision rules, if service outputs are emitted.
- Adding executive-summary methodology that produces evaluated conclusions,
  deterministic narrative templates, or report-ready sections.
- Changing methodology-owned validation behavior in a way that changes what
  answer sets are accepted or how they are evaluated.

These changes may also require an executive `assessmentVersion` change if they
alter accepted input semantics.

## Changes Not Requiring A New methodologyVersion

A new methodology version is not required when a change does not alter
methodology meaning, deterministic evaluation rules, or methodology-owned
output semantics.

Examples:

- Refactoring Python implementation while preserving behavior.
- Adding tests for existing methodology behavior.
- Updating deployment packaging or AWS infrastructure.
- Changing Lambda handler code without altering deterministic methodology.
- Adding runtime adapter code that validates an already-approved contract.
- Adding orchestration code that coordinates existing components without
  changing methodology.
- Updating Business Decision Package contract shape without changing the
  methodology used to evaluate answers.
- Updating package component versions for implementation baselines when
  methodology semantics remain unchanged.
- Clarifying documentation without changing methodology meaning.
- Changing public website directional assessment behavior, provided it remains
  separate and does not alter internal executive methodology.

If a non-methodology change affects package shape, runtime response shape, or
component baselines, other version identities may need to change even when
`methodologyVersion` does not.

## Binding Boundary Failures

Sprint 6.2 defines only methodology-version binding responsibility. It does
not define a full internal failure model or runtime error contract.

Minimum required behavior:

- Missing executive `assessmentVersion`: reject before binding.
- Unsupported executive `assessmentVersion`: reject before binding.
- Public or placeholder assessment version presented to executive binding:
  reject before binding.
- Missing caller-supplied `methodologyVersion`: not an error for v1 if the
  service resolves the bound methodology version from the accepted
  assessment version.
- Unsupported caller-supplied `methodologyVersion`, if a future input contract
  allows the field: reject before Decision Engine execution.
- Caller-supplied methodology version incompatible with
  `nguyen-ai-executive-assessment-v1`: reject before Decision Engine
  execution.
- Missing methodology configuration for the bound version: reject before
  Decision Engine execution.
- Methodology configuration version mismatch: reject before Decision Engine
  execution.
- Invalid methodology configuration: reject before Decision Engine execution.

Later Sprint 6 increments own:

- Internal failure result representation.
- Runtime error response shape.
- HTTP status code strategy.
- Runtime route and adapter behavior.

## BusinessDecisionPackage Interaction

The Business Decision Package identity tuple remains unchanged:

```text
(
  contractVersion,
  assessmentVersion,
  methodologyVersion,
  componentVersions
)
```

Sprint 6.2 does not redesign this tuple.

Methodology binding affects package identity by determining the
`methodologyVersion` value that appears in:

- `BusinessDecisionPackage.audit.methodologyVersion`
- `BusinessDecisionPackage.versionMetadata.methodologyVersion`
- serialized `audit.methodologyVersion`
- serialized `versionMetadata.methodologyVersion`

Package validation currently verifies:

- methodology version is present and non-empty
- package audit methodology version matches package version metadata
- source Sprint 3 methodology versions match
- serialized audit and metadata methodology versions match

Package validation does not decide whether an assessment version is compatible
with a methodology version. That compatibility must be established before
package assembly by the future executive input boundary and orchestration
layer.

## Compatibility Rules

Future consumers and runtime components must evaluate methodology
compatibility through governed identities.

Rules:

- `nguyen-ai-executive-assessment-v1` is currently compatible only with
  `business-decision-methodology-v1`.
- Unknown methodology versions must not be silently treated as compatible.
- Unknown assessment/methodology pairs must not be evaluated.
- Known methodology version does not imply production authority.
- Consumers must inspect package limitations and readiness status before
  treating output as authoritative.
- A future compatibility registry may define additional allowed pairs only
  through governed architecture, configuration, tests, and release
  documentation.

## Binding Decision Matrix

| Concern | Sprint 6.2 Decision | Rationale | Evidence | Status |
| --- | --- | --- | --- | --- |
| Current methodology version | `business-decision-methodology-v1`. | Single authoritative methodology config exists today. | `methodology_config.py`, `test_methodology_config.py`. | DECIDED |
| Authoritative methodology source | `BUSINESS_DECISION_METHODOLOGY.version`. | Source code and tests already use this as methodology identity. | `methodology_config.py`, Decision Engine/default builders. | DECIDED |
| Binding model | One executive assessment version to exactly one methodology version for v1. | Avoids caller-selected ambiguity without a registry. | Sprint 6.1 identity, package versioning docs. | DECIDED |
| Active v1 binding | `nguyen-ai-executive-assessment-v1` -> `business-decision-methodology-v1`. | Connects the approved executive assessment identity to the current governed methodology baseline. | Sprint 6.1 and methodology config. | DECIDED |
| Caller methodology selection | Not allowed for v1. | Service must own deterministic methodology selection. | Current repository has no compatibility registry. | DECIDED |
| Caller methodology assertion | May be allowed later only as a value to validate. | Preserves compatibility checks without transferring authority to caller. | Sprint 5.3 left field placement open. | DEFERRED |
| Decision Engine responsibility | Execute supplied methodology config; do not select runtime methodology. | Keeps engine focused on deterministic evaluation. | `decision_engine.py`, AGENTS architecture boundaries. | DECIDED |
| Package validation responsibility | Validate version consistency; do not decide binding compatibility. | Preserves Sprint 4 package contract. | `business_decision_package_validation.py`. | DECIDED |
| Methodology readiness | Version identity can exist while methodology remains pending. | Prevents version field from implying production authority. | Sprint 5.2 audit. | DECIDED |
| Future multi-methodology compatibility | Requires separate registry and governance. | Avoids unreviewed compatibility assumptions. | Versioning architecture. | OPEN/FUTURE |
| Separate input-contract version | Not decided here. | Sprint 6.3 owns whether assessment version is sufficient. | Sprint 6.1 dependencies. | OPEN |

## Consequences For Sprint 6.3

Sprint 6.3 must evaluate executive input-contract versioning with these
constraints:

- `assessmentVersion` already identifies the executive assessment input
  contract family.
- `methodologyVersion` is service-resolved from the accepted assessment
  version for v1.
- A separate input-contract version must not duplicate either
  `assessmentVersion` or `methodologyVersion`.
- If a future input-contract version is introduced, it must identify transport
  or input-shape compatibility only, not methodology selection authority.
- Any input-contract version field must not allow callers to bypass the
  approved assessment/methodology binding.
- Canonical input must carry or be associated with both accepted
  `assessmentVersion` and bound `methodologyVersion` before orchestration.

## Conditions Required Before Runtime Implementation

Before executive runtime implementation begins, later Sprint 6 increments must
still resolve:

1. Whether a distinct executive input-contract version is required.
2. Public/executive runtime route or adapter separation.
3. Runtime metadata boundary.
4. Business Decision Package API exposure governance.
5. Deterministic internal failure semantics.
6. Runtime error contract.
7. Runtime response field names and response contract version.
8. Contract test strategy.

Sprint 6.2 alone does not make the executive runtime implementation-ready.

## Explicitly Unresolved Business-Methodology Decisions

Sprint 6.2 does not resolve:

- Final question weights or final equal-weight approval.
- Final readiness thresholds.
- Final readiness-level assignment.
- Final scoring semantics.
- Risk caps or cross-dimension dependency rules.
- Final confidence formula.
- Final confidence-level assignment.
- Final recommendation-priority formula.
- Final recommendation-priority assignment.
- Recommendation generation rules.
- Service decision rules.
- Final executive-summary methodology.

These remain business-methodology decisions requiring separate governance.

## Explicit Non-Goals

This document does not:

- Modify Python source code.
- Modify tests.
- Modify methodology configuration.
- Modify the current Lambda runtime.
- Modify `BusinessDecisionPackage`.
- Modify package serialization.
- Create a methodology registry.
- Create compatibility-selection code.
- Create an executive input model.
- Create an orchestrator.
- Create an executive response model.
- Define API routes.
- Define HTTP status codes.
- Define persistence behavior.
- Introduce request IDs, UUIDs, runtime timestamps, session IDs, or database
  identifiers.
- Introduce public-to-executive translation.
- Approve final weights, thresholds, scoring semantics, confidence formulas,
  recommendation rules, service decisions, or executive-summary methodology.
- Introduce Bedrock, LLM, or probabilistic business reasoning.

## Recommended Next Increment

The next bounded Sprint 6 increment should be:

```text
Sprint 6.3 -- Executive Input-Contract Versioning
```

Reason:

Sprint 6.1 defined executive assessment identity. Sprint 6.2 defined the
service-owned methodology binding for that identity. The next unresolved
contract question is whether the future executive input contract needs an
additional version identity for input shape or whether `assessmentVersion` plus
service-resolved `methodologyVersion` is sufficient.
