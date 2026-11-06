# Founder Priority Applicability Approval v1

**Status: APPROVED — D2/D3/D5 METHODOLOGY PREDICATES ONLY.**

## 1. Purpose and approval scope

This record captures the Nguyen AI founder's explicit methodology v1 decision
for D2 customer impact, D3 executive urgency, and D5 dependency role. It
approves the evaluated and fail-closed predicate proposals in
[Document 36](36-founder-priority-applicability-predicate-decision-draft-v1.md)
and chooses no `NOT_APPLICABLE` branch for any of the three drivers. It does not
approve when an assertion must be supplied for priority evaluation, a final
priority formula, actual client assertions, or implementation.

## 2. Explicit founder decision

The founder approves D2-E1, D2-E2, D2-B, D2-I; D3-E1, D3-E2, D3-E3, D3-B,
D3-I; and D5-E1, D5-E2, D5-B, D5-I as methodology v1 predicate direction,
subject to the evidence, linkage, and authority requirements below. The
founder deliberately selects **NO `NOT_APPLICABLE` BRANCH FOR D2, D3, OR D5**.
D2-NA, D3-NA, and D5-NA from Document 36 are not approved or active rules.
Missing evidence is never affirmative absence, and no driver is automatically
required for every recommendation.

## 3. Approved Document 35 authority

[Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
approved F34-1 through F34-6 as methodology direction only. One
recommendation-linked, evidence-backed assertion model is admissible. The
Nguyen AI founder approves methodology; a client-designated business owner
must approve actual client-specific facts within authorized scope. Evidence
supply, business approval, Assessment Service validation, and production
authorization remain separate. Source revision, approval scope, supersession,
currentness reference, and material-change reassessment are required, with no
universal expiry period. This record adds no client authority or production
permission.

## 4. D2 approved predicates

| ID | Approved methodology condition | Outcome |
| --- | --- | --- |
| D2-E1 | An authorized, current, exactly recommendation-linked `impact-present` assertion is supported by inspectable customer process, service, or outcome evidence identifying the effect and affected context. | `EVALUATED`; no magnitude or priority inferred. |
| D2-E2 | An authorized, current, exactly linked `impact-affirmed-absent` assertion records the customer-facing scope reviewed and an explicit no-effect finding within it. | `EVALUATED`; scoped absence is a business fact. |
| D2-B | An approved future priority rule requires D2 for this recommendation, but required source information or an assertion is wholly missing or unresolved, with no invalid submitted claim. | `BLOCKED_PENDING_DATA`; without a requirement rule, applicability remains undetermined. |
| D2-I | A submitted D2 claim is malformed, unsupported, contradictory, stale, outside approval scope, or improperly linked; this includes unsupported absence or exclusion claims. | `INVALID`; reject the assertion set. |

There is no D2-NA branch. Finding severity and dimension labels do not prove
customer impact or absence.

## 5. D3 approved predicates

| ID | Approved methodology condition | Outcome |
| --- | --- | --- |
| D3-E1 | An authorized, current, exactly linked `time-bound-executive-action` assertion identifies the documented action or decision and its authoritative timing source. | `EVALUATED`; no deadline is invented. |
| D3-E2 | An authorized, current, exactly linked `executive-action-required` assertion identifies a documented action or decision without a time-bound claim. | `EVALUATED`; no timing claim inferred. |
| D3-E3 | An authorized, current, exactly linked `executive-action-affirmed-absent` assertion records the decision scope reviewed and an explicit no-action finding within it. | `EVALUATED`; scoped absence is a business fact. |
| D3-B | An approved future priority rule requires D3, but required source information or an assertion is missing or unresolved, with no invalid submitted claim. | `BLOCKED_PENDING_DATA`; missing timing in a submitted time-bound claim is instead invalid. |
| D3-I | A submitted D3 claim has unsupported action or timing, is malformed, contradictory, stale, outside approval scope, or improperly linked. | `INVALID`; reject the assertion set. |

There is no D3-NA branch. Risk, severity, readiness, recommendation
classification, and a missing deadline do not establish urgency or absence.

## 6. D5 approved predicates

| ID | Approved methodology condition | Outcome |
| --- | --- | --- |
| D5-E1 | An authorized, current, exactly linked assertion records an evidenced directed relation from the recommendation to a distinct existing same-snapshot target in an approved plan or prerequisite record. | `EVALUATED` as a relation claim only. |
| D5-E2 | An authorized, current, exactly linked `no-dependency-affirmed` assertion records the work set reviewed and an explicit no-relation finding within it. | `EVALUATED`; scoped absence is a business fact. |
| D5-B | An approved future priority rule requires D5, but required source information or an assertion is missing or unresolved, with no invalid submitted claim. | `BLOCKED_PENDING_DATA`. |
| D5-I | A submitted D5 claim has an unsupported relation, broken or cross-snapshot edge, contradictory claim, malformed value, stale source, invalid approval scope, or improper link. | `INVALID`; reject the assertion set. |

There is no D5-NA branch. `blocks-related-work` and
`unlocks-related-work` remain separate **draft source labels**; this decision
approves no distinct business or priority effect for them. Recommendation
order and shared dimensions do not establish dependencies.

## 7. No-NA v1 decision

For methodology v1, D2, D3, and D5 have evaluated, blocked-when-required,
and invalid outcomes only. An affirmative no-effect, no-action, or no-relation
finding is `EVALUATED` when approved and evidenced within its reviewed scope.
An unknown or missing fact cannot become affirmative absence. A submitted
`not-applicable` assertion for any of these drivers is unsupported and rejects
as `INVALID`; it never becomes a zero value or a low priority. When no future
approved rule requires a driver and no valid assertion is supplied, this
approval does not create an automatic requirement or a fabricated driver state.

## 8. Validation and evidence boundaries

Preserve the compatible precedence from Document 36: first validate structure,
versions, assessment/snapshot, finding, recommendation, and D5 target identity;
then business authority and approval scope; then exact evidence provenance,
source revision, currentness, and supersession; then duplicate and
contradictory claims. Any invalid submitted context rejects atomically. Only
after these checks may a single supported E predicate be evaluated. If a
future approved requirement rule needs missing or unresolved information, return
`BLOCKED_PENDING_DATA`. No unsupported fallback or array-order winner is
permitted. With no approved requirement rule, missing data alone does not
establish a driver result.

Actual client source content, approvers, and live authority/currentness checks
are not supplied by existing producer evidence references. The committed
[local synthetic validator](../../src/assessment/local_priority_assertions.py)
tests a separate nonproduction profile and is not a real evidence-content,
cryptographic, or production authority verifier. Its runtime behavior is not
changed by this document.

## 9. Assertion requirement limitations

This approval defines **what a supported assertion means and how bad or
missing required input is handled**. It does not define which recommendations
require D2, D3, or D5 to complete a final priority decision. D2-B, D3-B, and
D5-B apply only after a separate approved priority rule makes the respective
driver required for that recommendation. No blanket requirement or automatic
optional treatment is approved.

## 10. Deferred priority methodology

The next bounded methodology proposal must consider together: D1
business-impact contribution; D4 finding-severity and assessment-risk
contribution; D6 confidence contribution; D7 no-findings recommendation
treatment; D8 four-level priority emitting rules, tie handling, and conflict
precedence; and exact conditions under which D2/D3/D5 assertions are required
for priority evaluation. [Draft 32](32-final-recommendation-priority-addendum-draft-v1.md)
remains a proposal. No final priority can be assigned under this approval.

## 11. Explicit non-approvals

This record does not approve actual client-specific assertions or approver
identities; production source integration, authorization, live currentness,
cryptographic admission, new assessment questions, canonical scoring changes,
priority assignment, a final D1–D8 decision table, distinct priority effects
for D5 labels, frozen v2/v3 contract changes, EIP priority integration, CEP
changes, or AWS changes. It does not reopen the local synthetic validator or
claim Stage 2 completion. No implementation is authorized.

## 12. Next bounded action

Prepare one bounded founder proposal covering the remaining D1/D4/D6/D7/D8
decisions and the exact D2/D3/D5 assertion requirement conditions together.
Do not design or implement them under this approval record.

**Final status: APPROVED — D2/D3/D5 METHODOLOGY PREDICATES ONLY.**
