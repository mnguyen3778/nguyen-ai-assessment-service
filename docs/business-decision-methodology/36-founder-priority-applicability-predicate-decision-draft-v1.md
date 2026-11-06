# Founder Priority Applicability Predicates — Decision Draft v1

**Status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**

## 1. Purpose and scope

This document proposes bounded D2 customer-impact, D3 executive-urgency, and
D5 dependency-role predicate decisions. It identifies exact conditions that
could be evaluated from a future authorized, recommendation-linked business
assertion. No client fact or production source is presumed to exist. In
particular, no separate defensible `NOT_APPLICABLE` condition is established by
the present authority record. This is a partial proposal, not a final priority
methodology or an implementation instruction.

## 2. Approved F34 authority

[Approval record 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
approves F34-1 through F34-6 as *methodology direction only*: one
recommendation-linked evidence-backed assertion model; founder methodology
approval separate from client fact approval; D2/D3/D5 value and evidence
standards; documented timing for time-bound D3; directed D5 relations; source
revision, approval scope, supersession, and material-change reassessment.
`blocks-related-work` and `unlocks-related-work` remain separate draft source
labels without distinct approved business or priority effects. Exact exclusion
predicates were expressly withheld. [Draft 32](32-final-recommendation-priority-addendum-draft-v1.md),
[Draft 33](33-recommendation-priority-governed-input-extension-draft-v1.md),
and [Draft 34](34-founder-priority-assertion-source-authority-decision-draft-v1.md)
remain proposals. This document does not reopen F34 approval.

## 3. Common predicate semantics

All proposed rules below require a common admissibility envelope **G**:

1. A supported, versioned assertion identifies the assessment and exact
   producer snapshot identity/digest, the finding, and exactly one matching
   recommendation instance. A recommendation decision ID alone is insufficient.
2. Its source identity, revision, inspectable evidence reference, reviewed
   scope, business approval reference and scope, applicability rule ID/version,
   and currentness reference are present and consistent. A client-designated
   approver must have authority for the stated business scope. This designation
   and a production verifier do not currently exist.
3. The approved current source revision supports the precise asserted content;
   the record is not withdrawn or superseded. Reassess after a material change.
   A timestamp alone cannot prove currentness.
4. At most one active claim exists per snapshot, recommendation, and driver.
   A positive claim, an affirmative-absence claim, and an exclusion claim
   cannot compete for the same driver. D5 targets must resolve within the same
   snapshot.

`EVALUATED` means G and an approved positive or scoped affirmative-absence
value are established. Affirmative absence is a business fact about a reviewed
scope, not `NOT_APPLICABLE`. `NOT_APPLICABLE` would require G *and* a separately
approved deterministic exclusion condition with an affirmative source fact.
None is defined here. `BLOCKED_PENDING_DATA` means an approved applicable rule
requires a source/claim that is wholly missing; an absent assertion does not
prove absence or exclusion. Before such an applicability rule is approved,
the current methodology state is undetermined, and no status or priority input
is issued. `INVALID` means a submitted assertion is malformed, stale,
contradictory, unsupported, unapproved, or wrongly bound. Invalid input rejects
the complete assertion set; no favorable claim wins by order.

The rule IDs in this draft are proposal labels. Proposed rule version
`priority-applicability-predicates-draft-v1` is **not a supported runtime or
approved methodology version**. No `NA` row may emit an outcome until a
separate exact predicate and version receive founder approval.

## 4. D2 exact predicate proposals

The admissible future source is the F34-approved recommendation-linked
assertion backed by an inspectable customer process, service, or outcome
record. Its source and client business approver must be designated before real
use. All rows require G unless the row describes a missing record or invalid G.

| ID | Exact proposed condition | Outcome |
| --- | --- | --- |
| D2-E1 | Current approved `customer-impact` assertion has value `impact-present`; referenced source identifies a customer effect and affected context for the bound recommendation. | `EVALUATED`; preserve the effect, not a magnitude or priority. |
| D2-E2 | Current approved assertion has value `impact-affirmed-absent`; source records the reviewed customer-facing scope and an explicit no-effect finding for that scope. | `EVALUATED`; absence is scoped, not exclusion. |
| D2-NA | **UNRESOLVED.** Neither an internal-process label nor a scoped no-effect finding proves a distinct condition that excludes customer-impact analysis. No affirmative exclusion fact, exact predicate, or rule version is established. | No `NOT_APPLICABLE` emission. |
| D2-B | A future approved rule requires D2 for this recommendation, but no required source or assertion was supplied. | `BLOCKED_PENDING_DATA`; if no applicability rule is approved, remain methodologically undetermined instead. |
| D2-I | A submitted D2 claim fails G, has unsupported value/content, conflicts with another current D2 claim, or asserts absence/exclusion without its required reviewed scope and evidence. | `INVALID`; reject. |

Severity, finding dimension, and an uninspected evidence reference cannot
establish D2-E1, D2-E2, or D2-NA. The missing business condition for D2-NA is
an evidence-backed reason why the customer-impact driver is *outside* the
decision scope, distinct from a review finding no effect within that scope.

## 5. D3 exact predicate proposals

The future source is a recommendation-linked executive decision or review
record. A time-bound claim needs its actual approved timing source. No
deadline, decision, or client approver is asserted to exist here.

| ID | Exact proposed condition | Outcome |
| --- | --- | --- |
| D3-E1 | Current approved `executive-urgency` assertion has value `time-bound-executive-action`; source identifies the action/decision and an existing authoritative timing condition linked to this recommendation. | `EVALUATED`; retain timing provenance, no invented deadline or priority. |
| D3-E2 | Current approved assertion has value `executive-action-required`; source identifies the documented action/decision and makes no time-bound claim. | `EVALUATED`; no timing claim is inferred. |
| D3-E3 | Current approved assertion has value `executive-action-affirmed-absent`; source documents review of the decision scope and an explicit no-action finding within it. | `EVALUATED`; absence is scoped, not exclusion. |
| D3-NA | **UNRESOLVED.** No separate governed condition establishes that executive-action analysis does not apply, as opposed to an authorized review finding no action required. No affirmative exclusion fact, exact predicate, or rule version is established. | No `NOT_APPLICABLE` emission. |
| D3-B | A future approved rule requires D3, but no required source or assertion was supplied. A purported time-bound claim without its timing support is invalid submitted data, not a lower urgency. | `BLOCKED_PENDING_DATA` only for wholly missing required data; otherwise `INVALID`. |
| D3-I | A submitted D3 claim fails G, asserts unsupported timing/action content, conflicts with an absence or exclusion claim, or lacks its required action, review, or timing evidence. | `INVALID`; reject. |

Finding severity, assessment risk, readiness, recommendation classification,
and a missing deadline cannot establish any D3 value or exclusion.

## 6. D5 exact predicate proposals

The future source is an approved implementation plan or prerequisite record
with a directed relation. Positive claims need exact source recommendation
and same-snapshot target identities. Neither target nor plan is invented here.

| ID | Exact proposed condition | Outcome |
| --- | --- | --- |
| D5-E1 | Current approved `dependency-role` assertion records `blocks-related-work` or `unlocks-related-work`, an evidenced directed relation from the bound recommendation to a distinct existing same-snapshot target, and source-approved relation meaning. | `EVALUATED` as a relation claim only; no distinct business or priority effect for the two draft labels. |
| D5-E2 | Current approved assertion has value `no-dependency-affirmed`; source identifies a reviewed set of relevant work and an explicit finding of no directed relation within that set. | `EVALUATED`; absence is scoped, not exclusion. |
| D5-NA | **UNRESOLVED.** No separate governed condition establishes that dependency analysis is outside this recommendation's decision scope rather than a review finding no relation. No affirmative exclusion fact, exact predicate, or rule version is established. | No `NOT_APPLICABLE` emission. |
| D5-B | A future approved rule requires D5, but no required source or assertion was supplied. | `BLOCKED_PENDING_DATA`; before applicability approval, remain undetermined. |
| D5-I | A submitted D5 claim fails G, uses a nonexistent, self, or cross-snapshot target, unsupported direction, unapproved relation meaning/cycle, or conflicts with scoped absence or exclusion. | `INVALID`; reject. |

Order, shared dimensions, shared evidence, and finding count create no edge.
The missing D5-NA business condition must exclude *dependency analysis itself*;
an empty relation list or scoped no-dependency finding does not do so.

## 7. Predicate precedence

Evaluate the complete assertion set atomically in this proposed order:

1. Validate schema, versions, snapshot, assessment, finding, recommendation,
   and D5 target identities. Any failure is `INVALID`.
2. Validate business authority reference and approval scope. Any supplied
   unsupported approval is `INVALID`.
3. Validate exact evidence content/provenance, source revision, currentness,
   and supersession. Any supplied unsupported or stale claim is `INVALID`.
4. Reject duplicate active claims, contradictory values/statuses, conflicting
   revisions, and incompatible D5 relations as `INVALID`. Never choose by
   array order or allow exclusion to override a competing claim.
5. Only after 1–4 pass, match a single E1/E2/E3 evaluated row. If an exact,
   separately approved NA predicate later exists, match it only when no
   evaluated or conflicting assertion exists. No NA row is active today.
6. If an approved applicable rule requires missing data, return
   `BLOCKED_PENDING_DATA`. With no approved applicability rule, report
   methodology undetermined, not a fabricated driver status.

No priority is assigned at any step. The current local synthetic validator
tests an isolated profile; it is not a production content, authority,
currentness, or cryptographic verifier.

## 8. Admissible evidence requirements

| Predicate family | Required source fact and evidence type | Scope, approval, binding, and currentness |
| --- | --- | --- |
| D2-E1 | Inspectable customer process, service, or outcome record naming an effect and affected context. | Source ID/revision, client-designated approval, affected customer scope, exact snapshot/recommendation, current revision; reassess after a material customer-process or outcome change. |
| D2-E2 | Same source type plus explicit reviewed no-effect finding. | Reviewed customer-facing scope and approval must identify what was examined; same binding/currentness rules. |
| D3-E1 | Executive decision/action record and separately identifiable approved timing source or condition. | Decision and timing source IDs/revisions, authorized decision scope, exact recommendation, current approval; reassess on action or timing change. |
| D3-E2/E3 | Action record for E2; decision-scope review with explicit no-action finding for E3. | Source ID/revision, client-designated decision approver, exact reviewed scope and binding; reassess on decision change. |
| D5-E1 | Approved plan/prerequisite record naming directed source, target, and relation evidence. | Plan ID/revision, approved work scope, exact same-snapshot identities, current relation; reassess on plan or edge change. |
| D5-E2 | Approved plan/review record naming the work set reviewed and explicit no-relation finding. | Source ID/revision, work-scope approval and binding; reassess when plan or work set changes. |
| D2/D3/D5-NA | **UNRESOLVED:** a separate affirmative exclusion fact and exact predicate are absent. | No exclusion may be issued merely because a source is missing or an absence was affirmed. |

The existing governed producer input records finding evidence references and
quality, but not these client assertions, their content, approvals, or live
currentness. F34 approves a source *model*, not an existing source record.
Actual evidence, approvers, production verification, and integrity remain
future authority and implementation decisions.

## 9. Founder decision register

All recommendations are Codex review recommendations for a **future explicit
founder decision**. `G` supplies the common required source identity,
revision, snapshot/recommendation link, client approval, and currentness.
Every row remains proposed, and approval of an E row would not authorize its
production admission.

| Predicate ID / driver | Exact condition and affirmative fact | Required evidence and business approver | Expected outcome and conflict behavior | Recommendation / founder decision required |
| --- | --- | --- | --- | --- |
| D2-E1 / D2 | G + approved `impact-present` and identified customer effect/context. | Customer process/service/outcome record; client-designated customer-scope owner. | `EVALUATED`; conflicting D2 claim `INVALID`. | APPROVE AS PROPOSED; approve value predicate, not a client fact. |
| D2-E2 / D2 | G + approved `impact-affirmed-absent` and explicit no-effect review finding. | Reviewed customer scope record; same owner. | `EVALUATED`; competing positive/exclusion claim `INVALID`. | APPROVE AS PROPOSED; approve scoped absence predicate. |
| D2-NA / D2 | No distinct affirmative exclusion condition or approved rule version exists. | Missing exclusion fact/predicate; client scope approval would be required. | No NA outcome; submitted unapproved exclusion `INVALID`. | DEFER — SPECIFIC BLOCKER: founder must identify a condition distinct from D2-E2, or decide NA is unsupported. |
| D2-B / D2 | Approved applicable rule requires D2; required source/assertion wholly absent. | Missing customer source/approval; future client owner. | `BLOCKED_PENDING_DATA`; conflicts in submitted records instead `INVALID`. | APPROVE AS PROPOSED, conditional on an applicable rule being approved. |
| D2-I / D2 | Supplied D2 input fails G or supported value/evidence/scope. | Offending customer record/reference; authority check. | `INVALID`; reject whole set. | APPROVE AS PROPOSED. |
| D3-E1 / D3 | G + approved `time-bound-executive-action`, action and real timing condition. | Decision record plus timing source; client-designated decision authority. | `EVALUATED`; missing timing in submitted claim `INVALID`. | APPROVE AS PROPOSED; no invented deadline. |
| D3-E2 / D3 | G + approved `executive-action-required` and documented action without timing claim. | Action/decision record; same authority. | `EVALUATED`; contradictory absence `INVALID`. | APPROVE AS PROPOSED. |
| D3-E3 / D3 | G + approved `executive-action-affirmed-absent` and explicit no-action review. | Reviewed decision-scope record; same authority. | `EVALUATED`; competing action/exclusion `INVALID`. | APPROVE AS PROPOSED. |
| D3-NA / D3 | No distinct affirmative exclusion condition or approved rule version exists. | Missing exclusion fact/predicate; decision-scope approval would be required. | No NA outcome; unapproved exclusion `INVALID`. | DEFER — SPECIFIC BLOCKER: founder must identify a condition distinct from D3-E3, or decide NA is unsupported. |
| D3-B / D3 | Approved applicable rule requires D3; required source/assertion wholly absent. | Missing decision source/approval; future client authority. | `BLOCKED_PENDING_DATA`; submitted unsupported claim `INVALID`. | APPROVE AS PROPOSED, conditional on an applicable rule being approved. |
| D3-I / D3 | Supplied D3 input fails G or action/timing/review support. | Offending decision/timing record; authority check. | `INVALID`; reject whole set. | APPROVE AS PROPOSED. |
| D5-E1 / D5 | G + approved draft relation label, directed source and same-snapshot target. | Approved plan/prerequisite edge; client-designated work owner. | `EVALUATED` relation only; contradictory absence or bad edge `INVALID`. | APPROVE WITH TARGETED CORRECTION: approval cannot give the two labels distinct business/priority effects. |
| D5-E2 / D5 | G + approved `no-dependency-affirmed` and explicit no-edge finding within reviewed work set. | Work-scope plan/review; same owner. | `EVALUATED`; competing edge/exclusion `INVALID`. | APPROVE AS PROPOSED. |
| D5-NA / D5 | No distinct affirmative exclusion condition or approved rule version exists. | Missing exclusion fact/predicate; work-scope approval would be required. | No NA outcome; unapproved exclusion `INVALID`. | DEFER — SPECIFIC BLOCKER: founder must identify a condition distinct from D5-E2, or decide NA is unsupported. |
| D5-B / D5 | Approved applicable rule requires D5; required source/assertion wholly absent. | Missing plan/review source and approval; future client owner. | `BLOCKED_PENDING_DATA`; submitted unsupported claim `INVALID`. | APPROVE AS PROPOSED, conditional on an applicable rule being approved. |
| D5-I / D5 | Supplied D5 input fails G, relation identity, direction, or scope. | Offending plan/edge record; authority check. | `INVALID`; reject whole set. | APPROVE AS PROPOSED. |

## 10. Synthetic, non-executable example matrix

These examples assume only *synthetic* source facts, exact snapshot binding,
valid G, and an approved applicable rule where a blocked result is expected.
They claim no actual client evidence or approved production predicate.

| Scenario | Synthetic condition | Proposed result |
| --- | --- | --- |
| X01 D2 presence | Approved synthetic customer-service record names an effect for linked recommendation. | D2-E1 `EVALUATED`. |
| X02 D2 scoped absence | Approved review identifies customer scope and explicitly finds no effect. | D2-E2 `EVALUATED`, not NA. |
| X03 D2 NA attempt | No distinct approved exclusion predicate; synthetic record merely says internal process. | `BLOCKED_PENDING_DATA` if D2 is required and no valid evaluated assertion exists; a submitted unsupported NA claim is `INVALID`. |
| X04 D3 timing | Approved synthetic action and timing record name the same recommendation. | D3-E1 `EVALUATED`. |
| X05 D3 action | Approved synthetic action record makes no timing claim. | D3-E2 `EVALUATED`. |
| X06 D3 scoped absence | Approved decision-scope review expressly finds no executive action required. | D3-E3 `EVALUATED`, not NA. |
| X07 D3 NA attempt | No distinct approved exclusion predicate; no deadline is recorded. | `BLOCKED_PENDING_DATA` if required and no valid evaluated assertion exists; submitted unsupported NA is `INVALID`. |
| X08 D5 edge | Approved synthetic plan links source recommendation to a distinct same-snapshot target. | D5-E1 `EVALUATED` relation only. |
| X09 D5 scoped absence | Approved review of specified work set expressly finds no dependency. | D5-E2 `EVALUATED`, not NA. |
| X10 D5 NA attempt | No distinct approved exclusion predicate; plan lists no edge. | `BLOCKED_PENDING_DATA` if required and no valid evaluated assertion exists; submitted unsupported NA is `INVALID`. |
| X11 missing evidence | Applicable driver has no source or assertion. | `BLOCKED_PENDING_DATA`; no absence or NA inferred. |
| X12 contradiction | Same recommendation/driver has current positive and absence claims. | `INVALID`; reject set, no winner. |
| X13 stale revision | Submitted source revision is superseded. | `INVALID`; reject. |
| X14 wrong approval scope | Approver reference does not cover the asserted business scope. | `INVALID`; reject. |
| X15 wrong binding | Assertion points to another recommendation or snapshot. | `INVALID`; reject. |

## 11. Unresolved predicates

**D2-NA, D3-NA, and D5-NA are UNRESOLVED.** F34 approved value/evidence
direction but expressly withheld exact exclusions. For each driver the only
documented negative fact is an affirmative absence *within a reviewed scope*;
it already belongs to E2 or E3. No separate authoritative business condition
establishes genuine inapplicability. The founder must either provide an exact
business exclusion condition and admissible affirmative source fact, or decide
that this driver has no NA branch. Until then no NA rule ID/version is valid,
and no NA assertion can become a final-priority input.

## 12. Remaining D1–D8 decisions

D1 still needs a business-impact use or translation decision; D4 needs the
independent severity/risk influence and conflict policy; D6 needs founder
approval of confidence effects; D7 needs approval of the no-findings monitor
outcome. D2/D3/D5 still need exact applicability policy, especially the NA
question above. D8 needs complete four-level emitting predicates, tie and
conflict precedence. No severity, risk, recommendation label, or ordering
shortcut supplies those decisions. [Draft 32](32-final-recommendation-priority-addendum-draft-v1.md)
remains the unapproved final-priority proposal.

## 13. Explicit non-approvals

This draft approves no predicate, client fact, client approver, real source,
production authority, source integration, integrity profile, live currentness,
new assessment question, final priority mapping, runtime code, v2/v3 contract
change, EIP/CEP behavior, or AWS deployment. The committed local synthetic
validator remains closed at `5f2058e6a23f67e570bf7545e50f21df3b905753`.
Assessment Service retains any future governed priority decision; EIP may only
verify and pass through producer-issued output.

## 14. Recommended next action

Ask the founder to decide the three exact NA questions in section 11 in one
bounded review: supply a distinct evidence-backed exclusion condition for each
driver, or mark that driver as having no NA branch. The E and fail-closed rows
can be reviewed at the same time. No implementation follows automatically.

**Final status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**
