# Founder Priority Assertion Source and Authority Decision — Draft v1

**Status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**

## 1. Purpose and scope

This record presents the smallest business-source and approval decisions for
D2 customer impact, D3 executive urgency, and D5 dependency role. The founder
can review the proposed source model, value meanings, exclusion criteria, and
responsibility boundaries now. Approval of this record would approve a
methodology direction; it would not certify any client fact, appoint a client
approver, authorize production use, or assign final recommendation priority.

The [final-priority draft](32-final-recommendation-priority-addendum-draft-v1.md)
and [governed-input draft](33-recommendation-priority-governed-input-extension-draft-v1.md)
remain proposals. No new assessment question, scoring change, recommendation
selection change, priority formula, contract mutation, or downstream activation
is proposed here.

## 2. Existing approved constraints and source limits

The [decision methodology](01-decision-methodology.md),
[evidence catalog](03-evidence-catalog.md), and
[assessment methodology specification](09-assessment-methodology-specification-v1.md)
require traceable, evidence-based decisions. Evidence categories describe
possible sources; a category name does not verify a particular client fact.
The [governed input model](../../src/assessment/governed_assessment_input.py)
records finding evidence references and quality, but no D2/D3/D5 assertion,
reviewed absence, exclusion, or business approval. The
[approved recommendation tables](25-recommendation-decision-tables-v1.md)
select recommendations; their classifications and order do not establish
these drivers. The existing [v2](../architecture/business-decision-package-contract-v2.md)
and [v3](../architecture/business-decision-package-contract-v3.md) recommendation
contracts remain frozen.

The committed [local synthetic validator](../../src/assessment/local_priority_assertions.py)
and its [evidence record](../architecture/local-synthetic-priority-assertion-validation-evidence-v1.md)
test structure and binding only. Synthetic issuer references are not real
business authority. Cryptographic integrity for assertions, real evidence
content verification, live authority and revocation, production currentness,
production authorization, and final priority assignment are not implemented.
Existing signed producer snapshots do not authenticate a new assertion record.

## 3. Founder methodology authority and distinct responsibilities

**PROPOSED — NOT AUTHORITATIVE.** The Nguyen AI founder is the designated
approver of the *methodology*: admissible source types, D2/D3/D5 value meanings,
evidence and exclusion rules, and later priority decision rules. This does not
grant authority to attest a client's facts without client delegation.

For each real assertion, an evidence supplier would provide an inspectable
source and a separately identified business approver would approve its meaning
for a stated assessment, recommendation, and reviewed scope. The client or
business entity with actual authority must designate those people or functions
for its records. **FUTURE AUTHORITY DECISION REQUIRED.** The Assessment Service
would validate the approved record, binding, and provenance under a separately
authorized implementation. Production admission and runtime permissions remain
separate decisions. No standing administrator, named client approver, or
production identity is established by this draft.

## 4. D2 — customer-impact preferred source and approver

**PROPOSED — NOT AUTHORITATIVE.** Prefer one governed, recommendation-linked
business-owner assertion backed by a customer-facing process, service, or
customer outcome record that actually describes the affected scope. Existing
assessment evidence may be referenced when its inspectable content supports
the claim; an evidence-quality tuple or dimension label alone is insufficient.
The client-designated owner of the affected customer process or outcome would
supply or confirm the source and approve the D2 meaning. That designation and
the source record do not yet exist in the producer workflow.

| Proposed D2 value | Required business evidence |
| --- | --- |
| `impact-present` | Identify the customer effect, affected context, source revision, and exact recommendation link. Presence says nothing about magnitude. |
| `impact-affirmed-absent` | Record an authorized review of a stated customer-facing scope and an explicit finding of no customer effect within that scope. |
| `not-applicable` | Record an approved exclusion predicate and an affirmative source fact showing that customer-impact analysis is outside this recommendation's decision scope; include scope and rationale. |
| Unknown | No supported assertion exists. If an approved rule requires D2, remain `BLOCKED_PENDING_DATA`; silence is neither absence nor exclusion. |

Business process documentation alone is a candidate source of facts, not an
approval. A business-owner statement without an inspectable basis, scope, and
approval record is also insufficient. These alternatives were considered in
choosing the linked assertion plus source evidence model.

## 5. D3 — executive-urgency preferred source and approver

**PROPOSED — NOT AUTHORITATIVE.** Prefer one governed, recommendation-linked
decision or review assertion backed by an existing executive decision,
approved business timing condition, contractual or regulatory obligation, or
other documented action basis. A client-designated holder of the relevant
decision authority would approve the meaning and timing claim. No such person,
decision, deadline, or obligation is asserted to exist here.

| Proposed D3 value | Required business evidence |
| --- | --- |
| `time-bound-executive-action` | Identify the executive action or decision and the exact approved timing source or condition, its revision, and recommendation link. |
| `executive-action-required` | Identify the documented action or decision and approval; make no time-bound claim. |
| `executive-action-affirmed-absent` | Record an authorized review of the relevant decision scope and an explicit finding that no executive decision or action is required within it. |
| `not-applicable` | Record an approved exclusion predicate and affirmative source fact that executive action or decision is outside this recommendation's decision scope. |
| Unknown | No supported assertion exists. If required by an approved rule, remain `BLOCKED_PENDING_DATA`. Missing timing evidence cannot establish absence or exclusion. |

An approved deadline without recommendation linkage and business approval is
insufficient. Severity, risk, readiness, `immediate-action`, and recommendation
order cannot supply an urgency claim.

## 6. D5 — dependency-role preferred source and approver

**PROPOSED — NOT AUTHORITATIVE.** Prefer one governed relationship or reviewed
scope assertion backed by an approved implementation plan, documented
prerequisite, or client business-owner confirmation with inspectable support.
The client-designated owner of the affected work or plan would approve the
relation. No plan, edge, owner, or delegation is asserted to exist here.

| Proposed D5 value | Required business evidence |
| --- | --- |
| `blocks-related-work` or `unlocks-related-work` | A directed source-to-target relation: exact source recommendation instance, target recommendation or finding in the same assessment snapshot, relation meaning, evidence revision, and approval. The distinction between these two values for later priority remains a founder decision. |
| `no-dependency-affirmed` | Authorized review of a stated set of relevant work and explicit finding of no dependency within that scope. No recorded edge is insufficient. |
| `not-applicable` | Approved exclusion predicate and affirmative source fact that dependency analysis is outside this recommendation's decision scope. |
| Unknown | No supported assertion exists. If required by an approved rule, remain `BLOCKED_PENDING_DATA`. |

The source and target must resolve to valid, distinct identities in the same
snapshot. Cross-assessment edges, unsupported directions, contradictory
edge/absence claims, and unapproved cycle semantics fail closed. Recommendation
order, finding order, shared evidence, and dimension counts create no edge.

## 7. Proposed responsibility matrix

Every assignment below is **PROPOSED — NOT AUTHORITATIVE**. A client role is a
required future designation, not an existing appointment.

| Driver | Evidence supplier | Assertion business approver | Methodology approver | Technical validator | Production authority |
| --- | --- | --- | --- | --- | --- |
| D2 customer impact | Client-designated custodian of affected customer process/outcome records | Client-designated owner with authority over that customer scope | Nguyen AI founder, proposed | Assessment Service, after separate authorization | FUTURE AUTHORITY DECISION REQUIRED |
| D3 executive urgency | Client-designated custodian of decision, action, or timing records | Client-designated holder of relevant executive decision authority | Nguyen AI founder, proposed | Assessment Service, after separate authorization | FUTURE AUTHORITY DECISION REQUIRED |
| D5 dependency role | Client-designated custodian of implementation plan or prerequisite records | Client-designated owner of affected work and relation scope | Nguyen AI founder, proposed | Assessment Service, after separate authorization | FUTURE AUTHORITY DECISION REQUIRED |

The supplier and approver may be the same person only if the client explicitly
authorizes that arrangement; methodology approval alone does not merge them.
No row grants runtime permissions or substitutes for client approval.

## 8. Proposed applicability and exclusion rules

**PROPOSED — NOT AUTHORITATIVE.** For each driver, `EVALUATED` requires a
current, approved positive or affirmatively absent value supported by the
specific source described above. Affirmative absence is an evaluated business
finding within a reviewed scope. `NOT_APPLICABLE` requires a separately
approved predicate and an affirmative source fact that excludes the driver
from this recommendation's decision scope. It is not a priority level and
does not mean zero effect. The D2/D3/D5 tables propose business-readable
exclusion criteria; the exact predicate IDs, versions, and admissible scope
facts still require founder approval.

`BLOCKED_PENDING_DATA` applies when an approved applicable rule requires a
source or assertion that has not been supplied. Before an applicability rule
is approved, status is undetermined by methodology and no priority input is
issued. `INVALID` applies to a supplied assertion with unsupported values or
versions, broken links, contradictory claims, stale source, missing support,
or invalid authority. Neither unknown nor missing evidence can establish
absence or inapplicability. No state here assigns final priority.

## 9. Evidence, binding, and currentness requirements

**PROPOSED — NOT AUTHORITATIVE.** Each assertion needs a stable assertion ID;
driver and value; exact assessment snapshot identity and digest; finding ID;
recommendation decision ID and table version matched to exactly one
recommendation instance in that snapshot; applicability predicate ID/version;
source identity, inspectable evidence references and source revision; reviewed
scope; business approval reference and its scope; currentness reference; and
a traceable rationale. A recommendation decision ID alone is a reusable rule
ID, not an instance ID. Positive D5 assertions also need the exact directed
target identity. The null-linked no-findings monitor remains governed by the
separate D7 proposal, without fabricated D2/D3/D5 assertions.

The governing business source must identify its current approved revision and
whether an earlier record was superseded or withdrawn. A changed source,
assessment snapshot, recommendation, decision scope, timing condition, or
dependency relation requires reassessment and, where the assertion changes,
new approval. An old revision remains audit history, not a current input.
Timestamps alone do not establish currentness. There is no universal expiry
interval in this proposal. The real source-of-truth, authorized revision
checker, approval withdrawal path, and production currentness control are
**FUTURE AUTHORITY DECISION REQUIRED**; the local synthetic revision check does
not provide them.

## 10. Decisions the founder can approve now

All entries are requests for approval, not approvals. Each implementation
boundary is limited to a future separately authorized producer design;
approval of this table does not authorize code or production use.

| ID | Question requiring approval and recommended choice | Rationale and evidence basis | Alternative considered | If approved / if deferred | Exact implementation boundary |
| --- | --- | --- | --- | --- | --- |
| F34-1 | Adopt one recommendation-linked, evidence-backed business assertion as the admissible D2/D3/D5 source model? **Recommend yes.** | Draft 33 shows current evidence references have no business value or approver; one record can bind a claim and its source. | Treat existing evidence category or quality as the assertion. | Defines source admissibility / no governed source model yet. | Specify business record and validation contract separately; no v2/v3 mutation. |
| F34-2 | Designate the founder as methodology approver while requiring client-designated business approval of client facts? **Recommend yes.** | Draft 33 leaves business authority unresolved; methodology and client fact authority are distinct. | Founder approval automatically covers client facts. | Establishes role boundary / authority remains undefined. | No automatic client delegation or production permission. |
| F34-3 | Adopt the D2 present, affirmatively absent, and separately evidenced exclusion meanings in section 4? **Recommend yes, with exact applicability predicate and scope recorded.** | Drafts 32/33 reject dimension and silence proxies. | Infer no effect from missing customer data. | Enables a testable D2 methodology / D2 remains undefined. | Require source, scope, linked approval; no magnitude or priority inference. |
| F34-4 | Adopt the D3 time-bound action, action required, affirmatively absent, and separately evidenced exclusion meanings in section 5? **Recommend yes.** | Drafts 32/33 reject severity, risk, and classification proxies; a time-bound claim needs its own source. | Derive urgency from `immediate-action` or absent deadline. | Enables a testable D3 methodology / D3 remains undefined. | Require exact action and timing evidence when claimed; no priority inference. |
| F34-5 | Adopt D5 directed relation, scoped affirmative absence, and separately evidenced exclusion meanings, and decide whether `blocks-related-work` and `unlocks-related-work` are distinct business roles? **Recommend preserving distinct source claims until a later priority rule states their effects.** | Draft 33 supports explicit same-snapshot edges but leaves their priority distinction open. | Infer relation from ordering or collapse the two claims now. | Defines relation meaning and admissible evidence / D5 remains undefined. | Validate exact directed source and target; no inferred or cross-assessment edge. |
| F34-6 | Require source revision, approval scope, supersession, and material-change reassessment without a universal expiry period? **Recommend yes.** | Draft 33 requires a checkable currentness reference; timestamps and local synthetic checks do not prove live currentness. | Accept most recent timestamp as current. | Defines minimum currentness policy / assertions cannot be admitted as current. | Real registry and withdrawal operation still need future authority and separate implementation. |

## 11. Decisions requiring future client or production authority

These are bounded operational decisions, not a request to reopen Trusted
Authorization governance. The founder cannot make them on behalf of an
unidentified client or approve production access through this document.

| ID | Question and recommended choice | Rationale and evidence basis | Alternative considered | If approved / if deferred | Exact implementation boundary |
| --- | --- | --- | --- | --- | --- |
| C34-1 | Who may supply and approve each client's D2/D3/D5 assertions, and within what scope? **Recommend a client-designated supplier and business approver with recorded scope; any dual role requires explicit client authorization. FUTURE AUTHORITY DECISION REQUIRED.** | Draft 33 requires an approval reference but names no real authority; only the client can establish its delegation. | Founder methodology approval doubles as client delegation. | Establishes legitimate issuers / real assertions cannot be approved. | Configure only recorded client-specific authority after separate approval; no standing administrator implied. |
| C34-2 | Which actual source facts, absences, or exclusions are approved for each recommendation? **Recommend an inspectable, revision-bound record and explicit business approval for each claim. FUTURE AUTHORITY DECISION REQUIRED.** | Existing evidence references identify potential sources, not approved content; draft 33 requires exact recommendation binding. | Treat a reference or unreviewed statement as proof. | Supplies approved client facts / required claims remain blocked and unsupported submitted claims reject. | Admit only approved assertions tied to the exact snapshot and recommendation; no priority assignment. |
| C34-3 | Who owns the operational source-of-truth, revision, withdrawal, and currentness decisions? **Recommend the client-designated record owner for business source status, with a separately authorized producer verification path. FUTURE AUTHORITY DECISION REQUIRED.** | Draft 33 and local validator evidence show synthetic revision checks cannot prove live currentness or revocation. | Treat timestamps or the local test profile as live authority. | Defines checkable operational currentness / no production assertion admission. | Specify source registry and verification separately; no live capability claimed here. |
| C34-4 | May a future production assertion integrity and admission path be activated? **Recommend a separate explicit production authorization after business authority, evidence, versioning, and integrity are verified. FUTURE AUTHORITY DECISION REQUIRED.** | Existing signed snapshots do not authenticate new assertions; local validator evidence lists cryptographic and production controls as not implemented. | Reuse the existing snapshot signature as if it covered assertion bytes. | Allows a later bounded production decision / local synthetic boundary remains the only implementation. | No AWS, EIP, CEP, or production integration follows from this draft. |

## 12. Minimum remaining methodology decisions and next action

Founder review should resolve F34-1 through F34-6 as an explicit, versioned
methodology decision, including exact D2/D3/D5 applicability predicates. A
real client assertion remains impossible until the specific authority and
source decisions in section 11 are made. The separate [final-priority draft](32-final-recommendation-priority-addendum-draft-v1.md)
still needs founder-approved D1/D4/D6/D7 effects and a complete D8 four-level
mapping before any final priority can be assigned. This record does not supply
that mapping or claim Stage 2 completion.

The smallest next action is founder review of F34-1 through F34-6, recording
approval, rejection, or requested edits to each. Any later producer contract,
integrity profile, implementation, EIP verification, CEP presentation, or AI
Knowledge Assistant explanation requires separate authorization. EIP must
consume verified producer priority without recalculating it; no downstream
priority publication is activated here.

**Final status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**
