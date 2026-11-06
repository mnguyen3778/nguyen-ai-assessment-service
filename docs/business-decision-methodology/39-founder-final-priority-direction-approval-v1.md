# Founder Final Priority Direction Approval v1

**Status: APPROVED — F38 METHODOLOGY DIRECTION ONLY.**

## 1. Approval purpose and scope

This record captures the Nguyen AI founder's explicit approval of F38-D1,
F38-R1, F38-R2, F38-D3, F38-D4, F38-D5, F38-D6, and F38-D7 as bounded
methodology directions. The D8 four-level priority-emitting decision table
remains unapproved. This record does not authorize implementation, production
assertions, or final priority assignment.

## 2. Explicit founder authorization

The founder approves the eight directions in sections 4–11 below. Their
source is [Document 38](38-final-recommendation-priority-founder-decision-proposal-v1.md),
whose protected SHA-256 at approval recording is
`b3304ddf6578fe9ec65b8b91525642b979b60bcfda8a1eecee08295d9e7b8f64`.
Approval is limited to the actual F38 proposals as restated here and the
founder's explicit instructions. It does not approve Document 38's unfilled
D8 emitting rows, draft rule-set label, or any new business classification.

## 3. Approved source documents

[Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
approves F34 source and authority direction.
[Document 37](37-founder-priority-applicability-approval-v1.md) approves the
D2/D3/D5 evaluated and fail-closed predicates and selects no
`NOT_APPLICABLE` branch for those drivers in v1. Document 38 proposes the
remaining directions approved here. Documents 32–38 retain their original
contents and approval or proposal statuses. The producer baseline is
Assessment Service `main` at `5f2058e6a23f67e570bf7545e50f21df3b905753`.

## 4. F38-D1 — approved

Retain the linked finding's exact governed finding-type and business
consequence-basis pair, with evidence references, as business-consequence
context. No graded business-impact classification, numerical score, revenue
effect, or severity-to-impact translation is approved. Existing findings stay
unchanged. A future D8 row needing a graded impact input requires a separate
founder methodology decision and supporting evidence.

## 5. F38-R1 — approved

D2, D3, and D5 assertions are required only when an **approved D8
priority-emitting rule** explicitly needs the driver's evaluated value to
match or safely rule out that row for the bound recommendation. A missing
driver cannot silently eliminate a potentially higher or equal row and permit
a lower-priority result. There is no blanket assertion requirement. A driver
that no applicable rule needs is `NOT_REQUIRED_BY_RULE`; this is a rule
dependency, not a D2/D3/D5 business `NOT_APPLICABLE` value. No such emitting
D8 rule is approved by this record, so the exact future requirements remain
deferred.

## 6. F38-R2 — approved

Validate every supplied D2/D3/D5 assertion even when a priority rule does not
require its driver. An invalid submitted assertion rejects the evaluation;
it cannot be ignored to select a favorable result. A wholly absent,
unrequired driver supplies no evaluated value and does not lower priority.
Document 37's invalid and conflict outcomes remain authoritative methodology
direction. This approval does not create a production assertion verifier.

## 7. F38-D3 — approved

Preserve D3-E1, E2, and E3 as evidence-backed executive-action inputs. A
time-bound claim requires its authoritative documented timing source. A
documented action without that timing claim is not time-bound urgency.
Neither value automatically emits a priority level. Only a future exact D8
row may give an urgency value a priority effect. Risk, finding severity,
readiness, and recommendation classification do not establish urgency.

## 8. F38-D4 — approved

Preserve finding-scoped severity and assessment-wide risk as separate
governed inputs with their own decision IDs and versions. Do not convert
assessment risk into finding severity or recommendation priority. Neither
severity nor risk raises, lowers, caps, or assigns final priority by itself.
If they disagree, retain both; any exact combined priority effect must be
approved in D8. Severity labels are not priority labels.

## 9. F38-D5 — approved

Preserve evidence-backed directed D5-E1 relations to distinct same-snapshot
targets and D5-E2 scoped affirmative absence. Keep `blocks-related-work` and
`unlocks-related-work` as separate draft source labels without approved
distinct business or priority effects. An eventual dependency-to-priority
effect needs an exact D8 emitting rule. Recommendation order, shared
dimensions, or missing edges cannot establish a dependency or its absence.

## 10. F38-D6 — approved

The existing governed confidence vocabulary is
`very-high-confidence`, `high-confidence`, `moderate-confidence`,
`low-confidence`, and `insufficient-confidence`, as specified by the
[approved runtime configuration](../../src/assessment/approved_methodology_runtime_config.py).
The first four remain evidence-certainty context and are not automatic
priority multipliers or business-importance levels. For finding-scoped
recommendations, `insufficient-confidence` blocks final priority assignment
pending evidence review; it does not downgrade importance to `low`. Missing,
unsupported, or unversioned confidence rejects. Existing confidence decisions
and calculations are unchanged.

## 11. F38-D7 — approved

If and only if the complete finding collection is empty, risk is
`minimal-informational`, and the sole recommendation has null `findingId`,
`monitor` classification, decision ID
`recommendation-v1-no-findings-monitor`, and approved recommendation table
version, record a **separately governed priority-not-assigned-for-no-finding
outcome** with decision ID/version and no `critical`, `high`, `medium`, or
`low` classification. This is the outcome proposed in Document 38, not a
D2/D3/D5 `NOT_APPLICABLE` branch or fifth priority level. Malformed cases
reject. The existing recommendation and frozen v2/v3 packages stay unchanged.
No findings does not prove zero business risk.

## 12. Authority and evidence boundaries

The Assessment Service owns any future governed final-priority decision.
The founder approves methodology; a client-designated business owner must
approve actual client facts within authorized scope. The existing
[local synthetic validator](../../src/assessment/local_priority_assertions.py)
is a closed nonproduction test boundary, not real client approval,
cryptographic integrity, live currentness, or production authority. EIP may
only verify and consume future producer-issued priority without recalculation;
CEP may present authorized information and the AI Knowledge Assistant may
explain it. No downstream integration is authorized here.

## 13. D8 explicitly unapproved

There is no approved emitting predicate for `critical`, `high`, `medium`, or
`low`. D8 must still specify exact evidence combinations, business rationale,
rule IDs and version, recommendation/finding binding, assertion requirements,
tie handling, and conflict precedence. It must decide whether and how D1
consequence context, D3 urgency, D4 severity/risk combinations, and D5
dependency relations affect each level. No numerical weights, thresholds,
default-low outcome, automatic severity/risk/urgency/dependency mapping, or
model-generated priority is approved. No finding-scoped final priority may be
assigned from the eight directions alone.

## 14. Implementation restrictions

This approval authorizes no new impact classifications, assessment questions,
client assertions or approver designations, production source integration,
priority assignment code, contract changes, EIP/CEP integration, or AWS
deployment. Preserve the canonical 48 questions, existing scoring, findings,
recommendation selection, risk and confidence calculations, golden fixtures,
signed handoffs, frozen v2/v3 contracts, and local synthetic validator. No
source or runtime behavior changes. Stage 2 final priority is incomplete.

## 15. Next bounded action

Prepare a separate founder decision proposal for exact D8 four-level
emitting predicates and their tie/conflict precedence, using the approved
F38 directions without treating missing client facts as low priority. Do not
implement or activate a final-priority contract under this record.

**Final status: APPROVED — F38 METHODOLOGY DIRECTION ONLY.**
