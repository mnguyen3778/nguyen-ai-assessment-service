# Final Recommendation Priority — Consolidated Founder Decision Proposal v1

**Status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**

## 1. Purpose and scope

This is one bounded proposal for the remaining D1–D8 final-priority decisions.
It preserves the approved D2/D3/D5 predicate meanings and proposes how a
future rule could depend on them. It does **not** assert client facts or approve
a priority formula. Four-level emitting rules remain unresolved because no
approved business judgment relates the governed inputs to exact priority
levels. The Assessment Service remains the future decision owner.

## 2. Approved methodology baseline

[Priority methodology](06-recommendation-priority.md) approves the `critical`,
`high`, `medium`, `low` vocabulary and six qualitative drivers. Its prose is
not a complete decision table. [Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
approves the recommendation-linked, evidence-backed assertion source and
separates founder methodology approval from client fact approval.
[Document 37](37-founder-priority-applicability-approval-v1.md) approves
D2-E1/E2/B/I, D3-E1/E2/E3/B/I, and D5-E1/E2/B/I as methodology predicates.
**There is no D2, D3, or D5 `NOT_APPLICABLE` branch in v1.**
`blocks-related-work` and `unlocks-related-work` remain separate draft source
labels with no distinct approved business or priority effect. Documents
[32](32-final-recommendation-priority-addendum-draft-v1.md),
[33](33-recommendation-priority-governed-input-extension-draft-v1.md),
[34](34-founder-priority-assertion-source-authority-decision-draft-v1.md), and
[36](36-founder-priority-applicability-predicate-decision-draft-v1.md) remain
proposals. This document does not reopen F34 or Document 37.

## 3. Existing producer input inventory

All values below are producer-owned and version-bound. Their availability is
not itself evidence that they assign final priority. The
[governed input model](../../src/assessment/governed_assessment_input.py),
[decision runtime](../../src/assessment/governed_decision_runtime.py),
[v3 package contract](../architecture/business-decision-package-contract-v3.md),
and [golden regressions](../../tests/test_golden_fixture_regression.py)
establish the current fields and representative outputs.

| Source and field | Existing values, provenance, scope | Priority use and remaining approval |
| --- | --- | --- |
| `FindingInput.finding_id`, package `severityAssignedFindings[].findingId` | Unique finding ID in methodology v1; linked to one recommendation in the complete snapshot. | Exact recommendation binding; no impact or priority meaning. |
| `finding_type`, `business_consequence_basis` | Seven approved pairs: Deficiency with `material current breach`, `significant gap`, `clear deficiency`, `limited weakness`; Observation/`observation`; Strength/`strength`; Opportunity/`opportunity`. Finding-scoped with evidence references. | D1 consequence context is available; no approved graded business-impact translation. |
| `severityClassification`, severity decision ID/version | `critical`, `high`, `medium`, `low`, `informational`; `severity-decision-table-set-v1`. Finding-scoped. | D4 input available; mapping to priority requires founder choice. |
| `assessmentRisk.riskClassification`, risk decision ID/version | `critical-risk`, `elevated-risk`, `moderate-risk`, `low-risk`, `minimal-informational`; `risk-decision-table-set-v1`. Assessment-wide. | D4 context available; cannot silently become finding-specific priority. |
| `confidence.confidenceClassification`, confidence decision ID/version | `very-high-confidence`, `high-confidence`, `moderate-confidence`, `low-confidence`, `insufficient-confidence`; `confidence-decision-table-set-v1`. Assessment-wide certainty. | D6 input available; effect on priority requires founder choice. |
| `GovernedRecommendationResult.finding_id`, decision ID, table version, classification | Finding link or sole null-linked monitor; `recommendation-decision-table-set-v1`; `immediate-action`, `priority-action`, `planned-improvement`, `best-practice`, `monitor`. Rule ID can repeat across findings. | Bind the instance with snapshot, finding, rule ID/version; classification and order are not priority. |
| Finding `source_references`, `EvidenceProfileInput` | References plus `Basic`, `Adequate`, `Strong` quality and optional authenticity/traceability limitation. | Trace evidence identity, not D2/D3/D5 business content or approval. |
| D2/D3/D5 business assertions | Approved *source model and value semantics*, but no real client assertions, approvers, production content verifier, or currentness source. | Future recommendation-linked inputs only after separate client authority and production admission. |

The exact v2/v3 recommendation shapes and signed handoffs stay frozen. The
committed local synthetic validator is not a production assertion source.

## 4. D1 — business-impact proposal

**PROPOSED FOUNDER BUSINESS CHOICE D1:** retain the linked finding's exact
`(finding_type, business_consequence_basis)` pair and source references as
business-consequence context. Do not derive a graded business-impact value,
revenue loss, cost saving, or strategic importance from it. The seven pairs
are governed finding inputs, but no separate graded impact vocabulary is
approved. Severity is a different decision and cannot fill this gap.

If D8 must distinguish impact magnitude, the founder must approve a new
business-impact classification, its evidence, and exact translation or require
a separate governed impact assertion. This proposal does not choose arbitrary
grades. Missing or invalid existing consequence context rejects; a complete
but ungraded context cannot satisfy an emitting D8 row that requires graded
impact. No existing finding changes.

## 5. D2/D3/D5 assertion requirement proposal

**PROPOSED FOUNDER BUSINESS CHOICE R1:** a driver is
`NOT_REQUIRED_BY_RULE` only when every higher-or-equal-precedence emitting
D8 row that could apply to this recommendation has an approved predicate
independent of that driver. This is a rule dependency, **not** a business
`NOT_APPLICABLE` value. A driver is required when at least one such row needs
its evaluated value to establish either a match or a safe non-match. Thus a
missing D2/D3/D5 claim cannot make a higher row disappear and permit a lower
fallback. Exact row predicates are still needed to apply R1.

| Driver | Proposed exact trigger and current availability | Missing or invalid outcome; potential effect |
| --- | --- | --- |
| D2 | A founder-approved D8 row names D2-E1 or D2-E2 as a required match or non-match fact for this bound recommendation. No such D8 row currently exists; D2 assertion content is not in governed producer data. | If triggered, missing/unresolved source invokes D2-B; invalid submitted claim invokes D2-I. E1/E2 could influence only the exact approved row. |
| D3 | A founder-approved D8 row names D3-E1, E2, or E3 as a required match or non-match fact. No row or real urgency source currently exists. | If triggered, D3-B blocks; D3-I rejects. E1/E2/E3 do not independently emit a level. |
| D5 | A founder-approved D8 row names D5-E1 or E2 as a required match or non-match fact. No row or real dependency source currently exists. | If triggered, D5-B blocks; D5-I rejects. The two draft relation labels have one undifferentiated relation effect until a separate founder decision. |

**PROPOSED FOUNDER BUSINESS CHOICE R2:** validate any supplied assertion even
when a rule does not require that driver; an invalid supplied assertion rejects
the evaluation. A wholly absent, unrequired driver has no evaluated value and
does not lower priority. No new customer-facing question is proposed. R1 and
R2 are proposed methodology rules, not existing implementation behavior.

## 6. D3 — executive-urgency contribution

**PROPOSED FOUNDER BUSINESS CHOICE D3-EFFECT:** D3-E1, E2, and E3 may be named
as exact row conditions in D8. E1 proves a documented time-bound action with
its timing source; E2 proves an action without a time-bound claim; E3 proves
scoped affirmative absence. None automatically means `critical`, `high`, or
`low`. A deadline's importance, action consequence, and relation to this
recommendation would need an explicit founder-approved row. Missing required
data blocks; invalid timing or contradictory assertions reject. Risk,
severity, readiness, and recommendation classification provide no urgency
proxy.

## 7. D4 — severity and risk contribution

**PROPOSED FOUNDER BUSINESS CHOICE D4:** preserve finding-scoped severity and
assessment-wide risk independently, with both decision IDs and versions. A
future emitting row may name an exact severity and risk combination. Neither
value raises, lowers, caps, or assigns a recommendation's priority by itself.
When they differ, preserve both; do not select the larger label or convert
assessment-wide risk into finding-specific exposure. Missing, inconsistent,
or unsupported upstream classifications reject. For risk to raise or lower a
particular recommendation, the founder must approve an exact combination and
business rationale in D8. There is currently no such rule.

## 8. D5 — dependency contribution

**PROPOSED FOUNDER BUSINESS CHOICE D5-EFFECT:** a valid D5-E1 relation may be
used only by a D8 row that names it and states its priority effect. D5-E2 is
scoped affirmative absence, not `NOT_APPLICABLE` or a low-priority signal.
`blocks-related-work` and `unlocks-related-work` have no distinct effects in
this proposal. Missing required evidence blocks; conflicting edges, broken
targets, stale approvals, and invalid linkage reject. No relation is inferred
from recommendation order or shared dimensions.

## 9. D6 — confidence contribution

**PROPOSED FOUNDER BUSINESS CHOICE D6:** retain
`very-high-confidence`, `high-confidence`, `moderate-confidence`, and
`low-confidence` as evidence-certainty context; none changes the importance
level. For finding-scoped recommendations, `insufficient-confidence` blocks
final priority assignment pending evidence review rather than downgrading the
business issue. Missing, unsupported, or unversioned confidence rejects.
This is a proposed gate, not an approved runtime rule. A future output should
retain confidence separately from any eventual priority.

## 10. D7 — no-findings treatment

**PROPOSED FOUNDER BUSINESS CHOICE D7:** when the complete finding collection
is empty, assessment risk is `minimal-informational`, and exactly one
recommendation has null `findingId`, `monitor` classification, decision ID
`recommendation-v1-no-findings-monitor`, and approved recommendation table
version, record a separately governed *priority not assigned for no finding*
outcome with decision ID/version and no four-level priority classification.
This is a D7 output-state proposal, **not** a D2/D3/D5 `NOT_APPLICABLE` branch
or a fifth priority level. Do not put a new field in v2/v3. Malformed no-findings
cases reject; historical output stays unchanged. No findings is not proof of
no business risk, and `monitor` does not imply `low`.

## 11. D8 — four-level decision table

**No four-level emitting row is yet defensible from the approved methodology.**
The table below is an exact coverage and rejection proposal, not a complete
assignment table. Draft rule-set label
`final-recommendation-priority-decision-tables-proposal-v1` is not an approved
or supported version. Every eventual emitting row must bind to an exact
snapshot/recommendation/finding and retain matched driver values, source rule
IDs/versions, evidence references, a deterministic rationale, and its own
stable decision ID/version.

| Order / proposed ID | Exact condition | Proposed outcome |
| --- | --- | --- |
| 0 `priority-v1-invalid-context` | Any upstream version, finding/recommendation link, supplied assertion, authority, source, or currentness is invalid or contradictory. | Reject the complete set; no partial priority. |
| 1 `priority-v1-no-findings` | Exact D7 predicate in section 10. | Proposed separate no-finding outcome; no priority level. |
| 2 `priority-v1-insufficient-confidence` | Valid finding-scoped context with `insufficient-confidence`. | Proposed block for the set, no priority downgrade. |
| 3 `priority-v1-required-data-missing` | An approved emitting row requires D2/D3/D5 or an approved D1 input, and required facts are missing or unresolved. | Block; do not skip the row to reach a lower level. |
| 4 `priority-v1-critical` | **FOUNDER DECISION REQUIRED:** exact complete driver tuple and business rationale for critical. | No `critical` emission now. |
| 5 `priority-v1-high` | **FOUNDER DECISION REQUIRED:** exact complete driver tuple and business rationale for high. | No `high` emission now. |
| 6 `priority-v1-medium` | **FOUNDER DECISION REQUIRED:** exact complete driver tuple and business rationale for medium. | No `medium` emission now. |
| 7 `priority-v1-low` | **FOUNDER DECISION REQUIRED:** exact complete driver tuple and business rationale for low. | No `low` emission now. |
| 8 `priority-v1-no-match` | Valid finding-scoped context matches no approved emitting row, or matches conflicting same-precedence rows. | Before table approval, block as methodology incomplete; after a complete table is approved, reject unmatched or ambiguous input. Never default to low. |

No proposed numeric weight, score threshold, severity-to-priority shortcut, or
recommendation-label mapping fills rows 4–7. The exact missing business
decisions are: which evidence combinations warrant each level; whether D1
needs a graded value; whether risk can alter a finding's level; whether D3
timing or D5 dependency changes level and under what source facts; and how
competing drivers are resolved. Without these, a total mapping is invented.

## 12. Deterministic precedence proposal

1. Validate complete producer snapshot, upstream decision versions,
   recommendation-to-finding links, and every supplied assertion. Invalid
   context rejects before any business rule runs.
2. Match the exact no-findings D7 case; malformed null links reject.
3. Apply the proposed D6 insufficient-confidence block to finding-scoped
   recommendations.
4. Evaluate all possible emitting rows' required inputs under R1. If a
   potentially higher or equal row cannot be ruled out because a required
   fact is missing, block the entire set. `NOT_REQUIRED_BY_RULE` is not a
   driver value or an exclusion.
5. Only after complete evidence, evaluate founder-approved emitting rows.
   The future table must give one unambiguous winner. Equal priority across
   different recommendations is allowed; existing ordering may be retained
   but never assigns priority. Conflicting same-precedence rows reject unless
   an exact founder-approved precedence rule resolves them.
6. A valid tuple with no approved row cannot emit a level. No default low,
   model-generated priority, or partial publication is permitted.

This order is **PROPOSED — NOT AUTHORITATIVE**. It leaves D8 business
precedence unresolved while specifying fail-closed handling.

## 13. Founder decision register

Each row is a recommended *business choice for founder review*, not an
approval. `READY FOR FOUNDER DECISION` means the rule direction is concrete;
it does not mean implementation-ready. Exact emitting rows remain a concrete
methodology gap, not a software defect.

| ID / driver | Exact proposed rule and existing evidence basis | New judgment, recommendation, alternative | Approval / deferral consequence; implementation dependency | Status |
| --- | --- | --- | --- | --- |
| F38-D1 / D1 | Preserve exact governed finding type/consequence pair as context; no grade. | Recommend no grade from severity; alternative is a new approved impact taxonomy with evidence. | Approval preserves trace without false impact; deferral leaves D1 undefined. Any graded D8 row needs new approved input. | READY FOR FOUNDER DECISION |
| F38-R1 / D2,D3,D5 | Require a driver only when an approved D8 row needs it to match or safely rule out; no current row exists. | Recommend rule-specific requirement; alternative blanket requirement is unsupported. | Approval prevents a missing higher row from silently lowering priority; deferral leaves requirement semantics undefined. Needs exact D8 rows. | READY FOR FOUNDER DECISION |
| F38-R2 / D2,D3,D5 | Validate every supplied assertion even if no row requires it; Document 37 invalid cases reject. | Recommend atomic fail-closed validation; alternative ignoring an invalid extra assertion could conceal conflict. | Approval establishes rejection policy; deferral leaves conflict admission unclear. Needs authorized assertion source. | READY FOR FOUNDER DECISION |
| F38-D3 / D3 | E1/E2/E3 contribute only when exact D8 rows name them; Document 37 supplies meanings, no priority effect. | Recommend no automatic urgency-to-level mapping; alternative treating every deadline as critical lacks consequence basis. | Approval avoids a false shortcut; deferral leaves urgency effect open. Needs timing source and D8 rows. | READY FOR FOUNDER DECISION |
| F38-D4 / D4 | Keep governed finding severity and assessment risk independent; neither changes priority without exact D8 row. | Recommend no implicit risk escalation or lowering; alternative risk-to-finding conversion lacks specific exposure evidence. | Approval preserves scope; deferral leaves mixed severity/risk handling open. Needs exact combination rows. | READY FOR FOUNDER DECISION |
| F38-D5 / D5 | Valid E1 relation and E2 scoped absence affect priority only through exact D8 row; Document 37 approves values. | Recommend common relation treatment for draft labels; alternative distinct effects need a new business criterion. | Approval avoids inventing label effects; deferral leaves dependency effect open. Needs actual approved relation and D8 row. | READY FOR FOUNDER DECISION |
| F38-D6 / D6 | Four non-insufficient governed confidence classes remain context; insufficient blocks finding-scoped priority. | Recommend evidence gate, not lower importance; alternative level downgrade confuses certainty with importance. | Approval gives exact confidence behavior; deferral leaves insufficient-confidence cases unassigned. Needs versioned confidence provenance. | READY FOR FOUNDER DECISION |
| F38-D7 / D7 | Exact empty-findings/null-monitor predicate gets a separately governed no-finding priority outcome. | Recommend no four-level classification; alternative `low` has no finding basis. | Approval defines no-findings behavior; deferral leaves monitor priority unresolved. Needs future versioned representation without v2/v3 mutation. | READY FOR FOUNDER DECISION |
| F38-D8 / D8 | No approved tuple maps six drivers and D4 context to any level; rows 4–7 are empty. | Recommend founder choose exact critical/high/medium/low predicates and conflict precedence; no evidence basis supports a default. | Approval of future complete rows enables deterministic output; deferral blocks all finding-scoped priority. Needs source facts, D1/D4/D6 choices, versioned contract. | REQUIRES SPECIFIC SOURCE FACT |

## 14. Synthetic, non-executable scenario matrix

All examples are synthetic and proposed. `No assignment` means no current
founder-approved emitting D8 row; it is not an output priority value.

| ID | Inputs and matched proposed rule | Expected result and reason | Unapproved founder choice? |
| --- | --- | --- | --- |
| S01 | High-severity finding; D3-E3 no-action review; valid confidence. D4 and D8-no-match. | No assignment; high severity alone is not high priority. | Yes: D4/D8 combination. |
| S02 | Documented time-bound executive action with timing source, D3-E1. | No assignment; time bound alone has no level effect. | Yes: D3/D8. |
| S03 | D2-E1 customer impact present with source. | No assignment; impact presence has no graded priority effect. | Yes: D2/D8. |
| S04 | D2-E2 scoped affirmative absence. | No assignment; evaluated absence is not NA or low. | Yes: D8. |
| S05 | D5-E1 directed same-snapshot edge. | No assignment; labels have no distinct level effects. | Yes: D5/D8. |
| S06 | D5-E2 scoped no-dependency review. | No assignment; absence is not low. | Yes: D8. |
| S07 | Low finding severity and elevated assessment risk. D4. | No assignment; assessment risk cannot silently raise this recommendation. | Yes: exact D4/D8 combination. |
| S08 | Finding-scoped case with `insufficient-confidence`. D6 proposed gate. | Block final assignment pending founder approval of D6. | Yes: D6. |
| S09 | Higher D8 row needs D2, but D2 source missing. R1/D2-B. | Block; do not skip to lower row. | Yes: R1 and exact row. |
| S10 | Positive and absence D2 claims for same binding. D2-I. | Reject entire set; no winner. | No new D2 meaning; real authority still needed. |
| S11 | D3-E1 suggests time-bound action, D5-E2 shows no dependency, severity low. D8-no-match. | No assignment; no approved conflict precedence or combined row. | Yes: D8. |
| S12 | Empty findings, `minimal-informational` risk, sole null-linked approved monitor. D7 proposed row. | Proposed separate no-finding outcome, no priority level; current v2/v3 unchanged. | Yes: D7. |
| S13 | Fully evidenced tuple intended to yield `critical`. D8-critical row has no predicate. | No `critical` emission; founder must specify exact business condition. | Yes: D8-critical. |
| S14 | Fully evidenced tuple intended to yield `high`. D8-high row has no predicate. | No `high` emission. | Yes: D8-high. |
| S15 | Fully evidenced tuple intended to yield `medium`. D8-medium row has no predicate. | No `medium` emission. | Yes: D8-medium. |
| S16 | Fully evidenced tuple intended to yield `low`. D8-low row has no predicate. | No `low` emission or fallback. | Yes: D8-low. |

These are paper examples, not executable tests or modified golden fixtures.

## 15. Unresolved business decisions

The founder must still state exact business conditions for all four D8 levels
and their conflict precedence. Each emitting row must say which D1 consequence
facts, D2/D3/D5 evaluated values, D4 severity/risk pair, and D6 confidence
states it requires or safely does not require. A graded D1 input needs its
own vocabulary and evidence if any row depends on magnitude. A time-bound D3
claim needs the source action's business consequence before it can warrant a
level; a D5 relation needs its approved significance. Actual D2/D3/D5 client
facts and authority remain unavailable. No new question is proposed.

## 16. Explicit non-approvals

This document approves no new client fact, assertion requirement, emitting
rule, priority level assignment, production authority, source integration,
cryptographic admission, live currentness, contract version, v2/v3 mutation,
EIP calculation, CEP change, or AWS deployment. It does not modify the
canonical 48 questions, scoring, findings, recommendations, risk, confidence,
signed handoffs, golden fixtures, or the closed local synthetic validator.
Stage 2 final priority remains incomplete.

## 17. Recommended next bounded action

Founder review of F38-D1, R1, R2, D3, D4, D5, D6, and D7 can settle their
bounded policy directions. The separate D8 decision then needs exact
evidence-backed, mutually consistent predicates for `critical`, `high`,
`medium`, and `low`, including rule dependency and conflict precedence. No
implementation should begin from this partial table.

**Final status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**
