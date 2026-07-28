# Executive Assessment Input Contract v1

## Purpose

This document defines the architecture boundary for the internal executive
assessment input contract of the Nguyen AI Assessment Service.

The core question answered by this document is:

What constitutes a valid submission to the governed 48-question executive
assessment domain?

This is an input-contract architecture document. It does not define business
conclusions, scoring semantics, confidence formulas, recommendation rules,
service decisions, executive narratives, API routes, persistence behavior, or
Lambda integration.

The purpose of this contract is to prevent the current public/runtime
placeholder request path from being confused with the governed internal
executive assessment methodology.

## Scope

This document covers the internal executive assessment input boundary only.

It defines:

- How executive assessment input must be distinguished from public directional
  assessment input.
- What guarantees must exist before the Decision Engine receives answers.
- Which existing runtime request concepts are reusable.
- Which current runtime request concepts are placeholder, contextual, or
  inappropriate for the deterministic executive domain contract.
- Which architecture decisions are closed and which remain open before
  implementation.

This document does not create Python models or modify runtime behavior.

## Governing Baselines

This document is governed by:

- `AGENTS.md`
- `docs/architecture/assessment-boundary-architecture-v1.md`
- `docs/architecture/executive-runtime-readiness-architecture-v1.md`
- `docs/architecture/executive-methodology-completeness-audit-v1.md`
- `docs/architecture/business-decision-package-contract-v1.md`
- `docs/architecture/business-decision-package-serialization-contract-v1.md`
- `docs/architecture/business-decision-package-versioning-v1.md`
- `docs/releases/sprint3-foundation-complete-v1.md`
- `docs/releases/sprint4-business-decision-package-foundation-complete-v1.md`

Sprint 3 and Sprint 4 behavior are frozen. This document must not redefine
their contracts.

## Public vs Executive Product Boundary

Nguyen AI maintains two separate assessment products.

The public directional assessment is owned by the website repository. It is a
12-question, low-friction intake product used for business qualification,
readiness estimation, and conversation initiation. It must remain directional
and must not produce authoritative executive conclusions.

The internal executive assessment is owned by the Assessment Service. It is the
governed 48-question methodology that feeds deterministic Decision Engine
evaluation and downstream foundation outputs.

These products are intentionally separate. Public question IDs, answer values,
and directional result structures must not be silently mapped, inferred, or
expanded into executive assessment inputs.

Any future public-to-executive translation capability would require its own
approved, versioned, governed methodology. It is outside this contract.

## Existing Runtime Contract Analysis

The current Lambda runtime path accepts a placeholder request contract:

```text
POST /assessment
  -> handler
  -> validate_assessment_request
  -> AssessmentRequest
  -> score_assessment
  -> AssessmentResponse
```

The current `AssessmentRequest` contains:

- `assessment_version`
- `organization`
- `respondent`
- `answers`
- `source_payload`

The current validation layer:

- Requires `assessmentVersion`, `organization`, `respondent`, and `answers`.
- Accepts answer input as either an object keyed by question ID or a list of
  `questionId` and `value` entries.
- Rejects malformed JSON, duplicate JSON keys, missing top-level required
  fields, unsupported assessment versions, unknown top-level fields,
  non-object organization/respondent values, empty answers, duplicate list
  question IDs, and non-numeric answer values.
- Does not validate canonical executive question IDs.
- Does not require all 48 executive methodology questions.
- Does not validate answer values against methodology-configured answer ranges.
- Does not bind the request to `business-decision-methodology-v1`.
- Does not invoke the governed Decision Engine pipeline.

The current runtime path is therefore reusable only as evidence of existing
adapter behavior and validation patterns. It is not the executive assessment
domain contract.

## Executive Input Contract Principles

The executive assessment input contract must preserve these principles:

- Deterministic: identical accepted input must produce identical downstream
  deterministic evaluation behavior.
- Configuration-driven: canonical questions, answer types, ranges, dimensions,
  evidence categories, and weights originate from methodology configuration.
- Explicit: the input must be unambiguously identified as executive assessment
  input.
- Traceable: every accepted answer must trace to one configured canonical
  question.
- Complete before evaluation: the Decision Engine must not guess whether
  missing executive answers are absent, intentionally skipped, or inherited from
  another product.
- Boundary-safe: public directional assessment input must not enter the
  executive Decision Engine path without an approved translation methodology.
- Data-minimized: only data required for deterministic evaluation belongs in
  the core domain input.
- Immutable after validation: canonical input should not be mutated after the
  future input boundary accepts it.

## Contract Identity

`assessmentVersion` currently identifies the assessment input contract version
in runtime requests and Business Decision Package version metadata.

For the executive assessment, contract identity must unambiguously distinguish
the internal 48-question executive methodology contract from the public
12-question directional assessment contract and from the current placeholder
runtime contract.

Decision status:

- DECIDED: executive assessment input requires an explicit assessment contract
  identity.
- DECIDED: public directional assessment versions and executive assessment
  versions must remain distinct.
- DECIDED: package contract version is not input contract identity.
- DECIDED: runtime request identifiers, UUIDs, timestamps, session IDs, and
  persistence keys are not domain input identity.
- OPEN: the exact executive `assessmentVersion` value is not defined in the
  current repository.
- OPEN: whether the future input payload includes an explicit
  `methodologyVersion` field or the service resolves methodology version from
  `assessmentVersion` remains undecided.
- OPEN: whether a separate input-contract version field is needed beyond
  `assessmentVersion` remains undecided.

The minimum implementation requirement is that a future executive input boundary
must bind one accepted executive assessment version to one governed methodology
version deterministically.

## Canonical Question Requirements

The methodology configuration currently defines 48 canonical executive
questions. The Decision Engine rejects unknown question IDs and missing
configured question IDs before evaluation.

Decision status:

- DECIDED: a complete executive evaluation input must contain exactly one
  answer for each configured canonical executive question.
- DECIDED: unknown question IDs must be rejected.
- DECIDED: duplicate question IDs must be rejected.
- DECIDED: missing canonical question IDs must be rejected for complete
  evaluation.
- DECIDED: question order is not semantically meaningful; question identity is
  based on canonical question ID.
- OPEN: whether the platform will support draft, partial, or incomplete
  executive submissions is not decided. Such submissions must not be treated as
  complete executive Decision Engine inputs without an approved state model.

## Answer Representation

Current executable methodology supports normalizable numeric answer types for
the 48 configured questions:

- `scale-0-4`
- `numeric`

The methodology configuration also defines additional answer type vocabulary
such as `yes-no`, `single-select`, `multi-select`, and `text-evidence`, but
those types are not currently used by the 48 scored canonical questions and are
not currently normalizable by the Decision Engine.

Decision status:

- DECIDED: executive answers must be keyed by canonical executive question ID
  after validation.
- DECIDED: canonicalized executive input should use one deterministic answer
  representation before entering the Decision Engine.
- DECIDED: values for `scale-0-4` questions must be numeric values within the
  configured 0 to 4 range.
- DECIDED: values for `numeric` questions must be numeric values within the
  configured 0 to 100 range.
- DECIDED: booleans, null values, strings, arrays, and objects are not valid
  answer values for currently evaluated numeric question types.
- DECIDED: unsupported or non-normalizable answer types must be rejected before
  Decision Engine evaluation unless a future methodology version approves their
  evaluation behavior.
- OPEN: whether external runtime payloads may submit answers as a list, object,
  or both remains an API/adapter decision. The executive domain input must be
  canonicalized before evaluation regardless of transport shape.

## Input Validation Boundary

The future executive input boundary must validate contract structure before
calling the Decision Engine.

Input contract validation must be separate from:

- Answer normalization.
- Dimension aggregation.
- Overall scoring.
- Snapshot projection.
- Confidence evaluation.
- Recommendation priority foundation.
- Executive summary foundation.
- Business Decision Package assembly.

The input boundary must guarantee that the Decision Engine receives executive
answers that are:

- Bound to an accepted executive assessment version.
- Bound to the intended governed methodology version.
- Complete for the configured canonical question catalog.
- Free of public directional question IDs.
- Free of unknown aliases or inferred mappings.
- Type-valid for each configured question.
- Range-valid for each configured answer type.
- Canonicalized into a deterministic representation.

## Completeness Semantics

This architecture distinguishes four input states:

| State | Meaning | Current Decision |
| --- | --- | --- |
| Structurally Valid Input | Payload shape can be parsed and contains the required contract fields. | Necessary but insufficient. |
| Complete Executive Assessment | Input contains exactly one valid answer for every configured canonical executive question. | Required for Decision Engine evaluation. |
| Methodology-Eligible Input | Input is complete and compatible with the currently governed methodology configuration. | Required for deterministic executive domain evaluation. |
| Runtime-Eligible Input | Input contract, orchestration, response representation, and readiness gates are approved for runtime use. | Not yet implemented. |

A structurally valid input is not automatically complete,
methodology-eligible, runtime-eligible, or production-authoritative.

## Organization Metadata Boundary

The current placeholder runtime requires `organization` as a top-level object.
The Decision Engine does not use organization metadata to normalize answers,
map questions, aggregate dimensions, or assemble foundation outputs.

Decision status:

- DECIDED: organization metadata is not required for deterministic Decision
  Engine evaluation.
- DECIDED: organization metadata must not affect readiness scores, confidence
  foundation output, recommendation priority foundation output, executive
  summary foundation output, or Business Decision Package identity unless a
  future governed methodology explicitly approves that behavior.
- OPEN: which organization fields, if any, belong in a future executive runtime
  request remains undecided.
- OPEN: whether organization metadata belongs in runtime adapter context,
  downstream platform context, audit context, or a separate client profile
  system remains undecided.

The executive input contract should not become a customer-profile repository.

## Respondent Metadata Boundary

The current placeholder runtime requires `respondent` as a top-level object.
The Decision Engine does not use respondent metadata for deterministic business
evaluation.

Decision status:

- DECIDED: respondent metadata is not required for deterministic Decision Engine
  evaluation.
- DECIDED: respondent metadata must not influence deterministic outputs unless
  a future governed methodology explicitly approves that behavior.
- DECIDED: unnecessary personal data must be excluded from the deterministic
  executive domain input.
- OPEN: which respondent fields, if any, belong in a future runtime adapter or
  downstream platform context remains undecided.

## Source Metadata Boundary

The current `AssessmentRequest` preserves `source_payload` as a copy of the raw
payload. This is useful for placeholder runtime behavior and diagnostics, but
it is not deterministic executive domain input.

Decision status:

- DECIDED: raw source payload must not be passed to the Decision Engine as
  business evidence.
- DECIDED: raw source payload must not be used to infer missing answers,
  question mappings, methodology version, or business meaning.
- DECIDED: source metadata is not part of the canonical executive answer set.
- OPEN: whether future source metadata belongs in runtime adapter audit
  context, Business Decision Package audit metadata, evidence systems, or
  downstream platform services remains undecided.

## Data Minimization

The deterministic executive domain input requires only:

- An accepted executive assessment contract identity.
- A canonical answer set containing exactly one valid value for each configured
  executive question.
- A deterministic binding to the governed methodology version used for
  evaluation.

Organization, respondent, runtime, source, transport, persistence, and session
metadata are not required for deterministic evaluation.

Future implementation must justify each metadata field by asking:

Does deterministic assessment evaluation require this field?

If the answer is no, the field belongs outside the core deterministic executive
domain input unless a future governed decision says otherwise.

## Decision Engine Entry Guarantees

Before calling `evaluate_assessment()`, a future executive input boundary must
guarantee:

- The input is executive assessment input, not public directional assessment
  input.
- The assessment version is accepted for the executive contract.
- The methodology version binding is deterministic and compatible.
- Every configured canonical question has exactly one answer.
- No unknown question IDs exist.
- No duplicate question IDs exist.
- No public directional question IDs exist.
- No hidden aliases or translations were applied.
- Every answer value is valid for the configured answer type.
- Every answer value is within the configured range.
- The answer set is canonicalized into a stable, immutable representation.

The Decision Engine may continue to validate its own invariants defensively,
but it must not become responsible for guessing runtime intent or product
contract identity.

## Immutability / Canonicalization Decision

Decision status:

- DECIDED: future executive input should be represented as an immutable,
  validated domain object before entering the Decision Engine.
- DECIDED: canonicalization should remove transport ordering differences before
  domain evaluation.
- DECIDED: canonical ordering should be deterministic and based on canonical
  question identifiers when serialized or inspected.
- OPEN: the future Python model name and exact fields remain implementation
  decisions for a later increment.

## Error and Rejection Semantics

The executive input contract must define deterministic rejection semantics for:

- Malformed input structure.
- Unsupported or non-executive assessment version.
- Methodology version mismatch when methodology version is supplied.
- Unknown question ID.
- Duplicate question ID.
- Missing required canonical question ID.
- Unsupported answer type.
- Invalid answer value type.
- Null answer value.
- Out-of-range answer value.
- Incomplete submission presented as complete executive input.
- Public directional input presented as executive input.

This document does not define HTTP status codes, API response bodies, or Lambda
error formatting. Those are future runtime contract decisions.

## Runtime Separation Requirements

The future runtime boundary must make public and executive contracts
unambiguous.

Decision status:

- DECIDED: the current placeholder `POST /assessment` behavior must not be
  silently promoted into the authoritative executive Decision Engine runtime.
- DECIDED: executive runtime integration requires a distinct, governed input
  contract.
- DECIDED: the public directional assessment must not be connected directly to
  `evaluate_assessment()`.
- OPEN: whether separation is implemented through a distinct route, distinct
  adapter, distinct assessment version, or a combination remains undecided.
- OPEN: whether the Business Decision Package serialization becomes part of an
  API response remains undecided and is outside this document.

The minimum requirement is that public and executive contracts are
unambiguous at the runtime boundary.

## Contract Decision Matrix

| Concern | Current Runtime Behavior | Executive Domain Requirement | Decision | Rationale | Repository Evidence | Implementation Impact | Open / Closed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contract identity | Uses `assessmentVersion` with placeholder config. | Must distinguish internal executive input from public/placeholder input. | Require explicit executive assessment identity. | Prevents accidental public-to-executive execution. | `src/assessment/config.py`, `src/assessment/validation.py`, package versioning docs. | Future input boundary must validate accepted executive version. | DECIDED |
| Exact executive assessment version | Current value is `nguyen-ai-readiness-v1`. | Needs governed executive version value. | Do not choose in this document. | Repository does not yet approve a final executive input version value. | Runtime config differs from methodology version `business-decision-methodology-v1`. | Future governance decision required. | OPEN |
| Methodology version in input | Runtime request does not include it. | Evaluation must bind to governed methodology version. | Binding required; explicit client field undecided. | Avoids redundant identifiers until runtime strategy is approved. | `src/assessment/methodology_config.py`, versioning docs. | Future input boundary must define binding behavior. | OPEN |
| Separate input contract version | Not present. | May or may not be needed beyond assessment version. | Defer. | Existing package docs treat assessment version as input contract version. | `docs/architecture/business-decision-package-versioning-v1.md`. | Avoid extra version field unless justified. | OPEN |
| Question completeness | Current validation accepts any non-empty numeric answers. | Complete evaluation requires all 48 canonical questions. | Require all 48 for complete executive evaluation. | Decision Engine rejects missing configured questions. | `src/assessment/decision_engine.py`, `src/assessment/methodology_config.py`. | Future boundary must reject incomplete complete-submission requests. | DECIDED |
| Incomplete/draft submissions | Not modeled. | Could exist outside complete evaluation. | Defer. | No repository-approved draft state exists. | Sprint 5.1 readiness gates. | Must not call complete evaluation without a new state model. | OPEN |
| Known question IDs | Current runtime accepts non-canonical IDs. | Only canonical executive IDs are valid. | Reject unknown IDs. | Prevents public IDs and aliases from entering executive path. | Decision Engine unknown-ID validation. | Future validation must use methodology config. | DECIDED |
| Duplicate question IDs | Current validation rejects duplicates in JSON/list forms. | Duplicates invalid. | Reject duplicates. | One answer per canonical question preserves traceability. | `src/assessment/validation.py`. | Reuse duplicate-rejection pattern. | DECIDED |
| Question ordering | Current mapping order not meaningful. | Identity by question ID; deterministic canonicalization. | Ordering is not semantic. | Decision Engine sorts generated evaluations by question ID. | `src/assessment/decision_engine.py`. | Future model should serialize in stable order. | DECIDED |
| Answer representation | Runtime accepts object or list transport shapes. | Canonical domain answer set required. | Canonicalize before evaluation. | Transport flexibility must not affect domain behavior. | `src/assessment/validation.py`, Decision Engine tests. | Future adapter may accept transport variants but domain model should be stable. | DECIDED |
| Answer types | Runtime accepts numeric values only. | Must follow methodology-configured answer type and range. | Numeric configured types only for current evaluated questions. | All current 48 evaluated questions use normalizable numeric answer types. | `src/assessment/methodology_config.py`, `src/assessment/normalization.py`. | Reject non-normalizable types until methodology approves evaluation. | DECIDED |
| Answer ranges | Runtime does not enforce canonical ranges. | Enforce configured answer ranges. | Reject out-of-range values before evaluation. | Normalization requires min/max range. | `src/assessment/normalization.py`, Decision Engine tests. | Future input validation must be configuration-driven. | DECIDED |
| Organization metadata | Required object in current runtime. | Not required by Decision Engine. | Exclude from core deterministic domain input unless future governance approves. | Data minimization and no evaluation dependency. | `src/assessment/models.py`, `src/assessment/decision_engine.py`. | Treat as adapter/downstream context if retained. | DECIDED |
| Organization exact fields | Current runtime accepts arbitrary object. | Unknown. | Defer. | No approved domain need is documented. | Runtime validation only checks object shape. | Future contract must define or exclude fields. | OPEN |
| Respondent metadata | Required object in current runtime. | Not required by Decision Engine. | Exclude from core deterministic domain input unless future governance approves. | Avoid unnecessary personal data in deterministic contract. | `src/assessment/models.py`, `src/assessment/decision_engine.py`. | Treat as adapter/downstream context if retained. | DECIDED |
| Respondent exact fields | Current runtime accepts arbitrary object. | Unknown. | Defer. | No approved domain need is documented. | Runtime validation only checks object shape. | Future privacy and governance decision required. | OPEN |
| Source metadata | Runtime stores raw payload as `source_payload`. | Not part of canonical answer set. | Exclude from core domain input. | Raw payload must not create hidden inference behavior. | `src/assessment/models.py`. | Future audit context requires separate decision. | DECIDED |
| Immutability | Current AssessmentRequest is frozen but contains mutable dicts. | Canonical executive input should be immutable. | Require immutable validated domain object in future implementation. | Preserves reproducibility after validation. | Existing foundation models favor frozen dataclasses and immutable mappings. | Future model should avoid mutable dict fields. | DECIDED |
| Public/executive separation | Current `/assessment` placeholder can accept non-canonical answers. | Executive path must be unambiguous. | Do not reuse current placeholder path directly. | Avoids hidden contract promotion. | Boundary architecture and handler tests. | Future route/adapter decision required. | DECIDED |

## Open Architecture Decisions

The following decisions must be resolved before implementation of the executive
input contract:

- The exact executive `assessmentVersion` value.
- Whether `methodologyVersion` is supplied by callers or resolved by the
  service from the accepted executive `assessmentVersion`.
- Whether a separate input-contract version field is needed or whether
  `assessmentVersion` remains sufficient.
- Whether incomplete/draft executive submissions are supported and, if so,
  whether they are outside the Decision Engine evaluation path.
- Which organization metadata, if any, belongs in a future runtime adapter
  contract.
- Which respondent metadata, if any, belongs in a future runtime adapter
  contract.
- Whether raw source metadata belongs in audit context, evidence systems, or
  nowhere in the deterministic domain boundary.
- Whether future runtime separation uses a distinct route, distinct adapter,
  distinct version, or a combination.
- Whether Business Decision Package serialization is exposed through any future
  API representation.

## Conditions Required Before Implementation

Before implementing an executive input model or validator, the repository needs
approval for:

- Executive assessment contract identity.
- Methodology version binding strategy.
- Complete-submission behavior versus any future incomplete/draft behavior.
- Metadata inclusion and data-minimization rules.
- Runtime separation strategy between public and executive assessments.
- Error taxonomy at the domain validation level.

These decisions are separate from final methodology approval for production
authoritative scoring, confidence, priority, recommendations, service decisions,
and executive summaries.

## Explicit Non-Goals

This document does not implement or define:

- Python domain models.
- API routes.
- Lambda handler behavior.
- Runtime orchestration.
- Business Decision Package changes.
- Persistence.
- Delivery envelopes.
- Public-to-executive translation.
- Methodology changes.
- New weights.
- New thresholds.
- Scoring changes.
- Confidence formulas.
- Recommendation rules.
- Executive narratives.
- Evidence ingestion.
- Dashboards.
- Portfolio Intelligence.
- Bedrock or LLM reasoning.

## Future Runtime Integration Boundary

A future executive runtime path must follow this boundary:

```text
Executive Runtime Request
  -> executive input contract validation
  -> immutable canonical executive input
  -> Decision Engine
  -> Sprint 3 foundation outputs
  -> Business Decision Package
  -> Business Decision Package validation
  -> runtime response adapter
```

The runtime response adapter is outside this input contract. It must not mutate,
recompute, reinterpret, or hide deterministic outputs produced by the governed
domain pipeline.

## Recommended Next Increment

The recommended next increment is Sprint 5.4, Runtime Orchestration
Architecture.

That increment should define how a future orchestrator consumes a validated
immutable executive input and invokes the existing deterministic pipeline:

```text
Decision Engine
  -> BusinessReadinessSnapshot
  -> ConfidenceEvaluation
  -> RecommendationPriorityEvaluation
  -> ExecutiveSummaryFoundation
  -> BusinessDecisionPackage
  -> BusinessDecisionPackageValidation
```

It should remain architecture-only until the open input contract decisions are
approved.
