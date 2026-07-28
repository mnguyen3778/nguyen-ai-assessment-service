# Executive Input Contract Versioning v1

## Purpose

This document finalizes the Sprint 6.3 architecture and governance decision
for executive input-contract versioning in the Nguyen AI Assessment Service.

Sprint 6.1 established the executive assessment identity:

```text
nguyen-ai-executive-assessment-v1
```

Sprint 6.2 established the current methodology binding:

```text
nguyen-ai-executive-assessment-v1
  ->
business-decision-methodology-v1
```

Sprint 6.3 answers the next contract question:

```text
Does the canonical executive input contract require an independent
input-contract version identity?
```

This is an engineering and contract decision. It does not implement an
executive input model, modify runtime behavior, define API routes, approve
business methodology, or change frozen Sprint 3, Sprint 4, Sprint 5, Sprint
6.1, or Sprint 6.2 behavior.

## Scope

This document defines:

- Whether a distinct `inputContractVersion` identity is required for the
  canonical executive input contract.
- The input compatibility responsibility carried by executive
  `assessmentVersion`.
- Compatible and incompatible input evolution rules.
- How input compatibility differs from methodology evolution, package
  contract evolution, and component evolution.
- Caller and service responsibilities for input contract identity.
- Constraints created for public/executive runtime separation and later
  runtime implementation.

This document does not define:

- Executive request Python models.
- Executive input validators.
- Runtime routes or Lambda behavior.
- Runtime response models.
- Internal failure classes.
- HTTP status codes or API error bodies.
- Methodology weights, thresholds, scoring semantics, confidence formulas,
  recommendation rules, service decisions, or executive-summary rules.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/executive-assessment-identity-v1.md`
- `docs/architecture/executive-methodology-version-binding-v1.md`
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/executive-assessment-input-contract-v1.md`
- `docs/architecture/executive-runtime-orchestration-architecture-v1.md`
- `docs/architecture/executive-runtime-response-contract-v1.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`
- `docs/releases/sprint5-executive-runtime-readiness-foundation-complete-v1.md`

Sprint 3, Sprint 4, Sprint 5, Sprint 6.1, and Sprint 6.2 contracts remain
unchanged.

## Established Identity Model

The repository currently establishes these distinct version identities:

| Identity | Current Value | Governed Meaning |
| --- | --- | --- |
| Executive `assessmentVersion` | `nguyen-ai-executive-assessment-v1` | Internal 48-question executive assessment input contract family. |
| `methodologyVersion` | `business-decision-methodology-v1` | Governed Business Decision Methodology configuration used for deterministic evaluation. |
| `BusinessDecisionPackage` `contractVersion` | `business-decision-package-v1` | Business Decision Package output contract and serialization shape. |
| `componentVersions` | Component baseline map | Governed component baselines represented inside the package. |

The repository does not currently define `inputContractVersion` or
`input_contract_version` in source, tests, architecture documents, or release
documents.

## Repository Evidence

| Evidence | Current Meaning |
| --- | --- |
| `docs/architecture/executive-assessment-identity-v1.md` | Defines `nguyen-ai-executive-assessment-v1` as the internal executive assessment input contract family and assigns input compatibility responsibilities to `assessmentVersion`. |
| `docs/architecture/executive-methodology-version-binding-v1.md` | Binds `nguyen-ai-executive-assessment-v1` to `business-decision-methodology-v1` for v1 while preserving separate assessment and methodology identities. |
| `docs/architecture/executive-assessment-input-contract-v1.md` | Defines future executive input as canonical, complete, ID-based, boundary-safe, and distinct from the current public/placeholder request path. |
| `docs/architecture/business-decision-package-versioning-v1.md` | Defines `assessmentVersion` as the assessment input contract used to construct package output. |
| `src/assessment/models.py` | The current placeholder `AssessmentRequest` has `assessment_version` but no input-contract-specific version field. |
| `src/assessment/validation.py` | Current runtime validation checks `assessmentVersion` against configured assessment versions before placeholder scoring. |
| `src/assessment/methodology_config.py` | Defines the canonical methodology version separately from assessment identity. |
| `src/assessment/business_decision_package.py` | Preserves `assessment_version`, `methodology_version`, package `contract_version`, and component versions separately in package metadata. |
| `src/assessment/business_decision_package_validation.py` | Validates package version metadata and audit consistency without an input-contract-specific version identity. |

This evidence supports a minimal governed identity model for v1. It does not
show an existing independent input-contract version responsibility.

## Versioning Question

The Sprint 6.3 question is whether executive input shape compatibility needs a
separate identity in addition to `assessmentVersion`.

A separate version identity would only be justified if it had a distinct
semantic responsibility, authoritative owner, deterministic compatibility
meaning, and audit value that cannot already be carried by:

- `assessmentVersion`
- `methodologyVersion`
- `BusinessDecisionPackage` `contractVersion`
- `componentVersions`

More version fields are not automatically better governance. Redundant
identity can make downstream interpretation less reliable by allowing multiple
fields to appear authoritative over the same concern.

## Sprint 6.3 Decision

No independent `inputContractVersion` is required for v1.

Decision status:

- DECIDED: `nguyen-ai-executive-assessment-v1` is sufficient to identify the
  canonical executive input contract family for v1.
- DECIDED: executive `assessmentVersion` carries canonical executive input
  compatibility responsibility for v1.
- DECIDED: no caller-supplied `inputContractVersion` is required for v1.
- DECIDED: no separate input-contract version must be propagated through the
  deterministic executive pipeline for v1.
- DECIDED: omission of a separate `inputContractVersion` is intentional
  governance, not an oversight.
- DECIDED: future architecture may introduce a separate input-contract version
  only if a distinct governed compatibility concern emerges that
  `assessmentVersion` cannot safely represent.

Rationale:

- Sprint 6.1 already defines `assessmentVersion` as the executive assessment
  input contract family.
- The Business Decision Package versioning baseline already describes
  `assessmentVersion` as input-contract identity.
- The current architecture does not contain multiple executive input shapes
  that canonicalize to the same assessment semantics.
- The current architecture does not contain an API/runtime adapter contract
  that needs independent schema compatibility.
- The future executive input boundary is not yet implemented, so adding a
  speculative identifier would create governance overhead without repository
  evidence.
- Methodology evolution is already governed by `methodologyVersion`.
- Package output evolution is already governed by package `contractVersion`
  and `componentVersions`.

## What assessmentVersion Carries For v1

For v1, executive `assessmentVersion` carries compatibility responsibility for:

- The governed executive assessment product identity.
- The canonical executive question set expected by the input boundary.
- Canonical executive question IDs.
- Required completeness expectations for full executive evaluation.
- Question-level answer type expectations that define valid submitted answers.
- Answer ranges and value shapes required before normalization.
- Public/executive input separation.
- Compatibility between submitted executive input and the bound methodology
  version.

`assessmentVersion` does not carry:

- The full methodology rule set.
- Scoring weights.
- Readiness thresholds.
- Confidence formulas.
- Recommendation-priority formulas.
- Package serialization shape.
- Component baseline identity.
- Runtime route identity.
- HTTP request shape.
- Request IDs, session IDs, timestamps, or persistence identifiers.

## Relationship To methodologyVersion

`assessmentVersion` and `methodologyVersion` remain separate governed
identities.

`assessmentVersion` answers:

```text
Which executive assessment input contract did this submission use?
```

`methodologyVersion` answers:

```text
Which governed business methodology was applied to evaluate that input?
```

Sprint 6.2 binds:

```text
nguyen-ai-executive-assessment-v1
  ->
business-decision-methodology-v1
```

For v1, the service resolves the authoritative methodology version from the
accepted executive assessment version. A caller does not select methodology
execution. A future caller-supplied methodology version, if ever approved,
would be a compatibility assertion to validate, not caller authority to choose
business methodology.

## Relationship To Package Versions

Sprint 6.3 does not change Business Decision Package identity.

The Business Decision Package identity tuple remains:

```text
(
  contractVersion,
  assessmentVersion,
  methodologyVersion,
  componentVersions
)
```

Version responsibilities remain distinct:

| Version Identity | Responsibility |
| --- | --- |
| `assessmentVersion` | Executive input contract compatibility and assessment product identity. |
| `methodologyVersion` | Governed methodology vocabulary and evaluation rules. |
| `contractVersion` | Business Decision Package output shape and serialization contract. |
| `componentVersions` | Component baseline provenance for package sections. |

No `inputContractVersion` is added to package identity for v1.

## Compatible Input Evolution

The following changes are compatible with
`nguyen-ai-executive-assessment-v1` only when they do not alter canonical
executive input semantics:

- Documentation clarification that does not change accepted answers.
- Test additions that preserve existing input behavior.
- Refactoring validation implementation without changing validation meaning.
- Adding optional, non-semantic runtime or transport metadata that is excluded
  from canonical executive domain input.
- Supporting a new transport representation that canonicalizes to the same
  immutable executive input, if a future runtime/API architecture explicitly
  governs the adapter behavior.
- Improving error wording without changing rejection conditions.
- Adding downstream consumers that read the validated package without changing
  input compatibility.

Compatible evolution must not cause existing v1 executive input to be
interpreted differently.

## Incompatible Input Evolution

The following changes require a new executive `assessmentVersion` because they
change canonical executive input compatibility:

- Adding a required canonical executive question.
- Removing a canonical executive question.
- Retiring or replacing a canonical executive question.
- Changing a canonical question ID.
- Changing a canonical question's meaning while retaining the same ID.
- Changing a configured answer type for an existing canonical question.
- Changing answer ranges or accepted answer value shapes in a way that changes
  valid input meaning.
- Changing a required answer to optional, or an optional answer to required.
- Changing complete-evaluation semantics for the canonical 48-question set.
- Introducing draft, partial, or incomplete evaluation semantics into the
  executive domain input contract.
- Introducing public-to-executive translation, aliases, inferred answers, or
  synthetic executive answers into the executive input contract.
- Introducing an incompatible executive assessment variant under the same
  identity.

These changes may also require a new `methodologyVersion` when they alter the
methodology configuration or evaluation semantics.

## Assessment-Semantic Evolution

Assessment-semantic evolution changes what executive assessment input means.

Examples include:

- Changing the executive assessment from 48 canonical questions to a different
  required question set.
- Changing question identity or meaning.
- Changing whether the assessment is complete-only or permits partial/draft
  execution.
- Changing the boundary between public directional intake and internal
  executive assessment.

Assessment-semantic evolution requires a new executive `assessmentVersion`.
It must not be hidden behind a separate input-contract version while preserving
the same assessment identity.

## Methodology Evolution

Methodology evolution changes how valid executive input is evaluated after the
input contract has accepted it.

Examples include:

- Changing final question weights.
- Approving equal weighting as final methodology.
- Changing readiness thresholds or readiness-level assignment.
- Changing scoring semantics.
- Adding risk caps or cross-dimension dependency rules.
- Finalizing confidence formulas or confidence levels.
- Finalizing recommendation-priority formulas or assignment rules.
- Introducing recommendation, service decision, or executive-summary
  methodology.

Methodology evolution is governed by `methodologyVersion`, not by an
input-contract version. If a methodology change also changes accepted input
semantics, both `assessmentVersion` and `methodologyVersion` may need to
change.

## Change Classification Rules

| Change | Identity Impact |
| --- | --- |
| Add a required canonical question | New `assessmentVersion`; likely new `methodologyVersion`. |
| Remove a canonical question | New `assessmentVersion`; likely new `methodologyVersion`. |
| Change canonical question identity | New `assessmentVersion`; likely new `methodologyVersion`. |
| Change answer type | New `assessmentVersion`; likely new `methodologyVersion`. |
| Change required/optional status | New `assessmentVersion`; `methodologyVersion` if evaluation semantics change. |
| Change structural request metadata that is not canonical domain input | No new `assessmentVersion`; govern through future runtime/API contract if needed. |
| Add optional non-semantic transport metadata | No new `assessmentVersion`; metadata remains outside deterministic domain identity. |
| Change methodology weights | New `methodologyVersion`; no new `assessmentVersion` unless accepted input changes. |
| Change methodology thresholds | New `methodologyVersion`; no new `assessmentVersion` unless accepted input changes. |
| Change scoring semantics | New `methodologyVersion`; no new `assessmentVersion` unless accepted input changes. |
| Change package output shape | New package `contractVersion`; no new `assessmentVersion` unless accepted input changes. |
| Change component implementation baseline | New relevant `componentVersions`; no new `assessmentVersion` unless accepted input changes. |

## Caller Responsibilities

For v1 future executive runtime input:

- The caller may present `assessmentVersion`.
- The caller must not present public assessment identity as executive identity.
- The caller does not need to present `inputContractVersion`.
- The caller does not select authoritative methodology execution.
- The caller must not rely on public question IDs, aliases, inferred mappings,
  or synthetic executive answers.

Future runtime architecture may define additional transport fields, but those
fields must remain outside canonical executive input identity unless explicitly
approved by a later architecture baseline.

## Service Responsibilities

For v1 future executive runtime input, the service must:

- Validate that the submitted assessment identity is
  `nguyen-ai-executive-assessment-v1` before executive canonicalization.
- Reject public or placeholder assessment versions at the executive boundary.
- Treat absence of `inputContractVersion` as valid for v1.
- Reject any caller attempt to use `inputContractVersion` as methodology
  selection authority or as a bypass around assessment-version validation.
- Resolve the bound methodology version according to Sprint 6.2.
- Validate canonical question identity, completeness, answer type, and answer
  range before Decision Engine execution.
- Propagate validated `assessmentVersion` and bound `methodologyVersion`
  through deterministic outputs and package metadata.

This document does not define the full failure result model, runtime error
body, or HTTP status behavior.

## Public / Executive Boundary

The public directional assessment and internal executive assessment remain
separate products and contracts.

Rules:

- `nguyen-ai-readiness-v1` must not be treated as an executive input-contract
  version.
- `nguyen-ai-executive-assessment-v1` must not accept public question IDs.
- No public-to-executive mapping is approved.
- No aliases, inferred mappings, synthetic answers, or automatic answer
  expansion are approved.
- The current `POST /assessment` placeholder runtime must not be silently
  promoted into the executive runtime.
- Future public/executive runtime separation must use explicit route, adapter,
  validation, or equivalent boundary controls; it must not rely on an
  implicit or hidden input-contract version.

## Future Extensibility

A separate input-contract version may be introduced in the future only if a
new architecture decision establishes all of the following:

- A distinct semantic responsibility not already carried by
  `assessmentVersion`.
- A clear authoritative owner.
- Deterministic compatibility rules.
- Change rules that do not duplicate `assessmentVersion`,
  `methodologyVersion`, package `contractVersion`, or `componentVersions`.
- Propagation requirements, if propagation is required.
- Validation behavior.
- Tests and release documentation.

Examples that could justify future separate input-contract versioning include:

- Multiple governed transport schemas that canonicalize to the same executive
  assessment input contract while requiring independent external compatibility
  policy.
- A runtime adapter layer whose request shape must evolve independently from
  the canonical executive assessment semantics.
- Formal publication of an external API contract that needs compatibility
  semantics distinct from deterministic domain input identity.

These examples do not exist in the current repository and are not implemented
by Sprint 6.3.

## Impact On Future Executive Input Validation

Future executive input validation should treat `assessmentVersion` as the v1
canonical input compatibility identity.

Validation must establish:

- Supported executive `assessmentVersion`.
- Bound methodology version.
- Complete canonical 48-question answer set.
- Known canonical question IDs.
- Exactly one answer per canonical question.
- Configured answer types and ranges.
- No public question IDs.
- No aliases or hidden translation.

Validation must not require a separate `inputContractVersion` for v1.

If a future transport/API contract introduces external schema versioning, the
runtime adapter may validate that separately before canonical executive input
validation. That future external schema version must not replace
`assessmentVersion`.

## Dependencies On Sprint 6.4

Sprint 6.4 must preserve these Sprint 6.3 decisions:

- Public and executive runtime paths must be unambiguous without relying on a
  separate `inputContractVersion`.
- Runtime separation must validate `assessmentVersion` explicitly.
- The current public/placeholder `POST /assessment` path must not become the
  executive runtime by implication.
- A future executive adapter may own transport-specific concerns, but the
  canonical executive input domain contract uses `assessmentVersion` as its
  compatibility identity for v1.
- Any future external runtime contract version must remain distinct from
  deterministic executive input identity.

## Contract Decision Matrix

| Concern | Current State | Sprint 6.3 Decision | Rationale | Open / Closed |
| --- | --- | --- | --- | --- |
| Separate `inputContractVersion` | No repository field or document defines it. | Do not introduce for v1. | `assessmentVersion` already owns canonical executive input compatibility. | Closed |
| `assessmentVersion` responsibility | Sprint 6.1 defines executive input contract family. | Carries v1 input compatibility responsibility. | Avoids redundant identity and aligns with package versioning. | Closed |
| Methodology identity | Sprint 6.2 binds v1 to `business-decision-methodology-v1`. | Remains separate from input compatibility. | Methodology evolution is governed by `methodologyVersion`. | Closed |
| Caller-supplied input identity | Future caller may present `assessmentVersion`. | Caller supplies no separate input-contract identity for v1. | No distinct required semantics exist. | Closed |
| Optional transport metadata | Runtime architecture not implemented. | Does not affect `assessmentVersion` when excluded from canonical domain input. | Runtime metadata is not deterministic business identity. | Closed |
| Incompatible input evolution | Governed by assessment identity. | Requires a new executive `assessmentVersion`. | Same version must not reinterpret submitted answers. | Closed |
| Public/executive separation | Frozen boundary prohibits hidden mapping. | Preserve distinct `assessmentVersion`; no public identity reuse. | Prevents silent promotion of public assessment to executive input. | Closed |
| Future API schema versioning | Not implemented. | Deferred; may be separate only if later justified. | API/transport compatibility is not current canonical input identity. | Open |
| Incomplete/draft submissions | Sprint 5 left product behavior open. | Not resolved here. | This affects assessment semantics and later validation policy. | Open |
| Runtime route/adapter separation | Sprint 5 left details open. | Deferred to Sprint 6.4. | Runtime separation is the next architecture boundary. | Open |

## Explicit Non-Goals

Sprint 6.3 does not:

- Create `inputContractVersion`.
- Create an executive request model.
- Create an executive input validator.
- Modify the current `AssessmentRequest`.
- Modify the current placeholder runtime.
- Modify the Decision Engine.
- Modify methodology configuration.
- Modify Business Decision Package identity or serialization.
- Define runtime routes.
- Define API schema or OpenAPI.
- Define internal failure models or HTTP error responses.
- Implement orchestration.
- Introduce public-to-executive translation.
- Approve final methodology weights, thresholds, scoring semantics,
  confidence formulas, recommendation rules, service decisions, or
  executive-summary rules.

## Still-Unresolved Business-Methodology Decisions

Sprint 6.3 does not resolve methodology decisions identified by Sprint 5.2,
including:

- Final numeric weights or explicit approval of equal weighting.
- Final readiness thresholds and readiness-level assignment.
- Final scoring semantics.
- Risk caps or cross-dimension dependency rules.
- Final confidence methodology.
- Final recommendation-priority methodology.
- Recommendation and service decision methodology.
- Final executive-summary methodology.

Version identity does not imply methodology completeness, runtime eligibility,
or production authority.

## Conditions Required Before Implementation

Before implementing future executive input validation or runtime
canonicalization, the repository must have:

- Sprint 6.4 public/executive runtime separation decision.
- Final decision on incomplete/draft submission behavior.
- Final decision on organization, respondent, source, and runtime metadata
  boundaries.
- Internal failure semantics for unsupported assessment versions and invalid
  canonical input.
- Tests proving public inputs cannot enter the executive Decision Engine path.
- Tests proving `assessmentVersion` is the v1 input compatibility identity and
  no separate `inputContractVersion` is required.

## Recommended Next Increment

The next bounded increment should be:

```text
Sprint 6.4 - Public vs Executive Runtime Separation
```

Sprint 6.4 should define how future runtime boundaries keep the current
public/placeholder path separate from the future executive path. It should use
the Sprint 6.1 assessment identity, Sprint 6.2 methodology binding, and Sprint
6.3 input-contract versioning decision without implementing runtime behavior.
