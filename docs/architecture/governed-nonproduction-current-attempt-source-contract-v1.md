# Governed nonproduction current-Attempt source contract v1

## A. Purpose and scope

The Founder directive assigns the Assessment Service ownership of the current state of an Assessment Attempt for this nonproduction read. Trusted Authorization consumes the Service's evidence alongside the separately governed Attempt Binding. The read grants no permission and creates no Attempt, Binding, or Submission. It makes no changes to scoring, production interfaces, identity verification, or submission lifecycle. Engagement, Participation, Business Entity, and Principal Mapping facts retain their existing owners.

Platform's [Engagement context-legitimacy governance](../../../nguyen-ai-platform/docs/platform/trusted-authorization-assessment-engagement-context-legitimacy-governance-v1.md) §§19–24, 47, 53–56 and 60 defines the bounded Binding derivation, its provenance and revocation, and the separation from Assessment Service scoring ownership. That governance leaves runtime source selection open. The [Assessment Service identity](executive-assessment-identity-v1.md) and [snapshot lifecycle](executive-assessment-snapshot-lifecycle-governance-v1.md) govern assessment contract and immutable artifact identities. The inspected baseline contains no promoted live Attempt lifecycle, identifier issuance rule, creation or invalidation authority procedure, or effective-state reader.

## B. Canonical identities

| Field | Matching rule |
| --- | --- |
| `attempt_reference` | Exact owner-issued reference for one bounded Attempt within the governed nonproduction scope. The issuance format and uniqueness mechanism remain open. Scoring request IDs, assessment contract IDs, snapshot IDs, and resource identifiers cannot substitute. |
| `business_entity_id`, `engagement_reference` | Exact canonical IDs. The Engagement belongs to that Business Entity by the independently validated Engagement authority. |
| `participation_authority_reference`, `participation_provenance_reference` | The exact pair from the independently validated current Participation for the same principal and Engagement. The adapter carries no separate Participation ID. |
| `principal_id` | Exact canonical verified principal. Required for this SUBMIT read. The Assessment Service consumes the independently resolved principal and issues evidence only for the same scope. |
| `protected_operation` | Exact `PROTECTED_ASSESSMENT_SUBMISSION` operation. Resource Identity and exact-resource SUBMIT Entitlement remain separate predicates. |

## C. Lifecycle and currentness

A positive response requires an unambiguous, source-owned Attempt whose effective lifecycle permits the exact requested operation and whose authoritative state confirms it is current. The owner must document the eligible lifecycle states and the authorized creation and invalidation rules before any positive operational read. This contract defines no new lifecycle labels or transitions. `CURRENT` and `INVALIDATED` below are read outcomes. Snapshot governance supplies no mapping to live Attempt state.

Once a governed invalidation becomes effective, earlier positive evidence is unusable. If the source cannot establish the effective state, the invalidation status, or a valid interval covering consumption, the boundary withholds authority. The source cannot repair invalid upstream evidence, and Trusted Authorization cannot restore Attempt currentness.

## D. Revision semantics

The source issues an opaque revision for the exact Attempt state. Every effective state change, including invalidation, must progress to a distinct successor revision in the source's governed history. One revision must never describe conflicting state or scope. The adapter compares a positive revision for exact equality with independently trusted `expected_revision` set in bootstrap for the read. It does not order revisions or advance that pin. The source response under review cannot supply its own pin.

A stale, conflicting, or unsupported positive revision withholds the bundle. The owner must establish how a trusted pin advances as state changes and how a restored source can prove its history is current. Until that proof exists, a historical restore supplies no current authority. Equality with a supplied pin alone is no rollback defense.

## E. Source provenance

The private result retains the source-issued `owner_reference`, `source_reference`, `source_version`, `provenance_reference`, `revision`, `observed_at`, and `valid_until`. Bootstrap pins the approved owner, source, and supported version independently. A provenance reference must resolve to attributable source evidence connecting exact scope, state, revision, and observation. Where supported, the source's observation identity may be traced through that reference. v1 adds no observation-ID field.

The owner must preserve auditable provenance for state changes, including the actor or authority basis, exact scope, prior and new state and revision, and effective ordering. Source custody and transport must preserve integrity. The adapter checks form and equality with configured values. It does not authenticate a producer from reference strings, verify signatures, or inspect the underlying audit history.

## F. Observation validity

The approved read must observe source state during the same invocation and return evidence in the consumer's local monotonic nanosecond time domain. `observed_at` must fall within the read, and `valid_until` is exclusive. The evidence must remain valid at read completion and through authority-bundle assembly. The binding reader caps its validity at the earlier of the binding and current-Attempt evidence bounds.

The source must substantiate that bound relative to effective invalidation. The adapter does one source read and checks a deadline. It cannot detect invalidation after the read on its own. A source without an enforceable validity guarantee supplies no positive result through this adapter. If the owner can only provide point-in-time evidence, the smallest consumer change to consider separately is an owner-backed validity check at final bundle acceptance, with a defined consistency boundary. This contract supplies no TTL, cross-source atomicity, guarantee beyond bundle assembly, or source clock translation.

## G. Private read interface

Use an explicitly configured read-only nonproduction source through the local adapter. Trusted Authorization forms a fresh `_Query` for `ATTEMPT` with `environment=nonproduction`, key `(business_entity_id, principal_id, engagement_reference, attempt_reference, protected_operation.value)`, and validated Mapping, Engagement, and Participation prerequisites. The source must independently match its evidence to this scope. The local response must retain the original `_Query` object. Equality of serialized fields does not satisfy this check. Pass only the exact scope needed to an underlying producer.

| Outcome | Required local response |
| --- | --- |
| `CURRENT` | One exact `_AttemptIdentity` record containing the Section B fields and one complete `_SourceEvidence`. |
| `INVALIDATED` | Zero records and attributable evidence of a confirmed non-current Attempt, including effective invalidation where applicable. |
| `CONFIRMED_ABSENT` | Zero records and attributable evidence of confirmed absence for the exact query. |
| `STALE` | Zero records with source evidence when reported by the source. The adapter can also derive this outcome from observation bounds or a positive revision mismatch. |
| `UNAVAILABLE` | Zero records and no evidence. Covers a missing source, an unavailable observation, outage, or timeout. The source must provide bounded completion before operational use. |
| `MALFORMED` | Zero records and no evidence. Covers invalid shape, ambiguous results, or contradictory records. |

Every non-positive result withholds the bundle. For evidence-bearing negative responses, the adapter checks provenance shape, configured source, and observation bounds. It checks the exact revision pin only on positive responses. Negative results carry no identity record. Exact negative scope therefore depends on the owner-controlled lookup and original query correlation.

## H. Security

Reject cross-tenant or wrong Attempt, Engagement, principal, Participation, and operation substitution. Require independently established prerequisite facts and least-privilege source access scoped to nonproduction. Caller claims, persisted Binding alone, cached results, scoring artifacts, synthetic fixtures, and LLM decisions cannot establish operational currentness. There is no production route, fallback, or mutation interface.

## I. Compatibility and acceptance

Source review used Assessment Service `9d544e4864b418478cf67f99726dde6cb4a63cad` and Trusted Authorization `44700df0a56425522d967432492cf3f3e0bf4d2a`. The table records static compatibility. Operational guarantees require separate verification.

| Requirement | Promoted consumer behavior | Operational acceptance gap |
| --- | --- | --- |
| Exact identity and isolation | `_current_attempt_provider` checks all seven identity fields and rejects wrong scope or operation. | Prove canonical issuance and owner-side exact lookup, including Participation lineage and tenant isolation. |
| Read shape and missing source | `_AttemptSourceObservation` requires original query object identity and outcome-specific cardinality. Missing source fails closed. | Prove authenticated owner access and unambiguous absence versus unavailable. |
| Provenance and revisions | Adapter checks owner, source, version and evidence shape. A positive revision must match the configured pin. | Prove provenance custody, revision progression, independent pin maintenance and safe behavior after restore. |
| Observation and invalidation | Adapter checks the same-call time bounds. The binding reader caps expiry and `_SubmissionSourceReads` checks expiry at bundle completion. | Define the source lifecycle and prove effective invalidation cannot leave stale evidence usable during the claimed interval, or withhold positive evidence. |
| Binding and scope separation | `_LocalAttemptBindingAdmin.bind_reader` reuses the existing bounded derivation and independent ledger evidence. Read-side composition creates no operational state or production path. | Verify with the actual owner-controlled source while all prerequisites remain independently enforced. |

Before operational acceptance, exercise current and invalidated reads, invalidation during composition, stale revisions and restored history, mismatched identity and source, malformed evidence, duplicate records, outage, timeout, and missing source. The existing adapter tests provide controlled examples. This contract review adds no runtime code or test result.
