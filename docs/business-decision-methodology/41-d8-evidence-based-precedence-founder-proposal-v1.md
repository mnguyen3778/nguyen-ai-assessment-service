# D8 Evidence-Based Precedence — Founder Proposal v1

**Status: PROPOSED — FOUNDER APPROVAL REQUIRED.**

## 1. Purpose and approved Option B

The founder approved **F40-OPTION-B: evidence-based precedence** as a
methodology design direction. Explicit business triggers, deterministic
precedence, rule-specific D2/D3/D5 requirements, evidence-backed treatment of
all actual finding types, separate severity/risk/confidence/priority, and
fail-closed missing evidence are approved design constraints. **No individual
D8 emitting rule is approved.** This document proposes a finite, partial
rule set for founder review; it does not assign priority or implement it.

## 2. Existing authority and constraints

The [priority methodology](06-recommendation-priority.md) establishes four
levels and qualitative drivers, not an executable D8 table.
[Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
separates founder methodology authority from client fact approval.
[Document 37](37-founder-priority-applicability-approval-v1.md) approves D2/D3/D5
evaluated and fail-closed meanings with **no `NOT_APPLICABLE` branch**.
[Document 39](39-founder-final-priority-direction-approval-v1.md) approves
F38-D1/R1/R2/D3/D4/D5/D6/D7 direction. In particular, no graded D1 impact
exists; assessment risk is separate from finding severity; insufficient
confidence blocks finding-scoped priority; all supplied assertions validate;
the sole valid null-linked monitor gets a separate no-finding outcome.
[Document 40](40-d8-final-priority-emitting-rules-founder-proposal-v1.md)
contains **unapproved** narrow candidates C1/H1/M1/L1. Option B does not
promote those rows or reopen F34, F38, or Document 37.

## 3. Exact producer input inventory

The [governed input model](../../src/assessment/governed_assessment_input.py),
[decision runtime](../../src/assessment/governed_decision_runtime.py),
[producer validation](../../src/assessment/governed_producer_validation.py),
and [golden fixtures](../../tests/test_golden_fixture_regression.py)
establish the existing producer vocabulary and linkage. No real D2/D3/D5
assertion, client approver, evidence-content verifier, or live currentness
source currently exists in the production path.

| Source | Exact existing values and provenance | D8 authority and availability |
| --- | --- | --- |
| `findingType` + `businessConsequenceBasis` | Seven governed pairs: Deficiency with `material current breach`, `significant gap`, `clear deficiency`, `limited weakness`; Observation/`observation`; Strength/`strength`; Opportunity/`opportunity`. Finding ID and source references under methodology v1. | Available finding-scoped consequence context, not a graded impact value. |
| `severityClassification`, severity decision ID/version | `critical`, `high`, `medium`, `low`, `informational`; `severity-decision-table-set-v1`. | Available finding-scoped classification; validate consistency with pair, never equate with priority. |
| `assessmentRisk.riskClassification`, risk decision ID/version | `critical-risk`, `elevated-risk`, `moderate-risk`, `low-risk`, `minimal-informational`; `risk-decision-table-set-v1`. | Available assessment-wide context, not a finding-level risk assertion. |
| `confidence.confidenceClassification`, decision ID/version | `very-high-confidence`, `high-confidence`, `moderate-confidence`, `low-confidence`, `insufficient-confidence`; `confidence-decision-table-set-v1`. | Available assessment-wide certainty; first four contextual, insufficient blocks finding-scoped emission. |
| Recommendation `findingId`, rule ID/version, classification | `recommendation-decision-table-set-v1`; `immediate-action`, `priority-action`, `planned-improvement`, `best-practice`, `monitor`. | Available. Bind exact snapshot + finding + rule ID/version; rule ID alone repeats. Classification/order are not priority. |
| Finding evidence references/profile | Governed references; `Basic`, `Adequate`, `Strong` and optional authenticity/traceability limitation. | Available traceability, not client D2/D3/D5 fact or approval. |
| D2, D3, D5 assertion | Document 37 E/B/I meanings and separately governed recommendation-linked source model. | No real approved source or authority yet; a future client-designated owner must approve the exact fact and scope. |

Existing v2/v3 shapes, signed handoffs, and golden fixtures stay frozen.

## 4. Proposed priority definitions

`critical` means highest intervention order for a specifically evidenced
material, time-bound blocker. `high` means elevated intervention for a
documented gap with an additional business trigger. `medium` means planned
correction after an affirmative review rules out specified customer,
executive, and dependency triggers. `low` means lower intervention supported
by a limited or non-deficiency finding **and** affirmative scoped reviews.
These are **proposed business meanings**, not synonyms for severity, risk,
confidence, readiness, or recommendation classification. Exact predicates
appear below; no level is a fallback.

## 5. Proposed emitting rule table

Every row is a **NEW PROPOSED FOUNDER BUSINESS CHOICE**. `R` means
`REQUIRED_BY_RULE`; `N` means `NOT_REQUIRED_BY_RULE`. Neither means
`NOT_APPLICABLE`. Every row requires valid producer snapshot, exact
recommendation/finding link, governed finding-pair/severity consistency,
supported risk, one of the four non-insufficient confidence classes, and
current authorized source evidence for each required assertion. Risk is
retained as context only under proposed choice F41-RISK.

| ID / level / order | Exact Boolean predicate and applicable finding type | D2 / D3 / D5 | Business rationale; missing/conflict behavior |
| --- | --- | --- | --- |
| B-C1 / `critical` / 1 | `(Deficiency, material current breach)` AND D3-E1 documented timed action AND D5-E1 directed same-snapshot relation. | N / R / R | Material breach with timed executive action and dependent work could require highest intervention. Missing D3/D5 blocks; invalid supplied claim rejects. D2 cannot alter this row by itself. |
| B-H1 / `high` / 2 | `(Deficiency, material current breach)` AND D3-E2 documented untimed executive action AND D2-E1 customer effect. | R / R / N | Material breach plus customer effect and executive action warrants elevated intervention without C1 timing. D3-E2 proves C1 false, so D5 is not required to rule out critical. |
| B-H2 / `high` / 3 | `(Deficiency, significant gap)` AND D2-E1 customer effect AND D3-E2 untimed executive action. | R / R / N | Significant gap with customer and executive evidence warrants elevated intervention; no D5 edge is presumed. |
| B-H3 / `high` / 4 | `(Deficiency, clear deficiency)` AND D2-E1 customer effect AND D3-E1 documented timed action. | R / R / N | Clear deficiency with an independently documented customer effect and timed action may warrant elevation; no severity-to-high shortcut. |
| B-M1 / `medium` / 5 | `(Deficiency, clear deficiency)` AND D2-E2 scoped no customer effect AND D3-E3 scoped no executive action AND D5-E2 scoped no dependency. | R / R / R | Clear deficiency supports planned correction only after three affirmative reviews. D2-E2/D3-E3 rule out H3; absence is evaluated, not NA. |
| B-L1 / `low` / 6 | `(Deficiency, limited weakness)` AND D2-E2 AND D3-E3 AND D5-E2, each approved within reviewed scope. | R / R / R | Limited weakness and three affirmative reviews could warrant lower intervention. Missing evidence never yields low. |
| B-L2 / `low` / 7 | `(findingType, businessConsequenceBasis)` is exactly one of `(Observation, observation)`, `(Strength, strength)`, `(Opportunity, opportunity)` AND D2-E2 AND D3-E3 AND D5-E2, each approved within reviewed scope. | R / R / R | **Proposed founder choice:** non-deficiency finding plus three scoped negative reviews could warrant lower action order. Type alone never yields low; positive or unknown business signals leave this row unmatched. |

All assertions must be bound to the same assessment snapshot and exact
recommendation instance. D3-E1 needs its authoritative timing source. D5-E1
needs a distinct same-snapshot target; its `blocks-related-work` and
`unlocks-related-work` draft labels receive no distinct effects. The rows do
not invent client source records, deadline thresholds, impact grades, or
numerical weights. The exact combinations and their levels remain unapproved.

## 6. Finding-type coverage

| Actual type | Proposed eligibility | Uncovered valid cases |
| --- | --- | --- |
| Deficiency / material current breach | B-C1 or B-H1, selected from producer pair. | Other valid D2/D3/D5 combinations, including scoped absence with no timed action, have no emitting row. |
| Deficiency / significant gap | B-H2. | Other valid combinations have no row. |
| Deficiency / clear deficiency | B-H3 or B-M1. | Other valid combinations have no row. |
| Deficiency / limited weakness | B-L1. | Other valid combinations have no row. |
| Observation, Strength, Opportunity | B-L2 only with three explicit scoped absence reviews. | Positive or unknown customer, urgency, or dependency evidence has no row; no automatic low or separate non-priority outcome is approved. |
| Empty findings | Approved D7 separate no-finding outcome, not a D2/D3/D5 NA branch. | Malformed monitor cases reject. |

No other finding type is accepted by the governed input. The table is finite
but **partial**, not a total priority mapping. Uncovered classes need an
additional exact founder business rule or an explicitly approved non-emitting
domain; this document creates neither automatically.

## 7. D2/D3/D5 requirement policy

**Noncircular eligibility:** first validate producer identity and the exact
finding pair. That pair alone selects the candidate IDs shown in section 6.
Evaluate higher-level candidates before lower ones using three-valued
`TRUE`, `FALSE`, `UNKNOWN` reasoning: a candidate is `FALSE` when an existing
producer pair differs or a valid evaluated assertion contradicts a required
atom; `TRUE` when every required atom is supported; `UNKNOWN` when no known
fact rules it out but a required assertion is missing. A row requires a driver
only if its exact predicate names that driver and it has not already been
ruled `FALSE` by other validated facts. A supplied invalid assertion rejects
regardless of row relevance under F38-R2.

Before emitting level L, every eligible row above L must be `FALSE` or have
the **same output level with a deterministic selected decision ID**. A
higher-level `UNKNOWN` blocks even if a lower row is `TRUE`; no missing
assertion is treated as E2/E3 absence. For the present row set, pair
eligibility is disjoint across most rows. Material-breach B-H1 cannot emit
until B-C1 is `FALSE`; D3-E2 proves that because it contradicts D3-E1,
without requiring D5. Clear-deficiency B-M1 cannot emit until B-H3 is
`FALSE`; D2-E2 and D3-E3 prove it. If an eligible row has already become
`FALSE`, its remaining D2/D3/D5 atoms are `NOT_REQUIRED_BY_RULE` for that
decision. No driver is automatically required for every recommendation.

## 8. Deterministic precedence

1. Validate schema, version, snapshot, finding/recommendation identity,
   authority and approval scope, evidence provenance/content, source
   revision/currentness, duplicate claims, and contradictions for **every
   supplied assertion**. Invalid submissions reject atomically.
2. Match the exact approved no-findings D7 case. Malformed null links reject;
   valid case receives its separate no-finding outcome, no four-level value.
3. For finding-scoped cases, `insufficient-confidence` blocks; other four
   supported classes remain contextual.
4. Select candidate IDs from the validated finding pair, independent of
   assertion presence. Evaluate eligible candidates in order C, H, M, L.
5. Resolve each required atom as true, false, or unknown. A higher unknown
   blocks before a lower emission. A single highest matching level wins.
   For two same-level true rules, choose the lexicographically first rule ID
   as decision ID and preserve all matched IDs in rationale; this tie rule is
   a **proposed founder choice**, not approved methodology.
6. Preserve finding severity and assessment risk separately. They validate
   upstream context but do not automatically raise/lower these rows.
   Unmatched valid tuples remain non-emitting and unresolved; no low fallback.

## 9. Assessment-wide risk decision

**F41-RISK — PROPOSED FOUNDER BUSINESS CHOICE:** choose **A, context only**
for D8 v1. Assessment risk summarizes the complete finding distribution; it
does not identify the business consequence of this specific recommendation.
An exact risk-specific escalation could be proposed later with a finding-linked
business rationale, but using the assessment label alone would convert a
global fact into a local one. Under this proposal, risk is validated and
retained in provenance but does not change priority. Alternatives B and C
would require exact source-linked predicates and approval. A low-severity
finding with elevated assessment risk retains both classifications; the row
matches only its own evidence. Founder approval of F41-RISK is required.

## 10. Missing and conflicting evidence

| Case | Proposed fail-closed outcome |
| --- | --- |
| Invalid submitted claim, unsupported value/version, stale evidence, invalid authority, duplicate or contradictory assertions, broken D5 edge | `INVALID`; reject complete evaluation even if driver is not required by a selected row. |
| Required atom absent or unresolved for a potentially matching higher rule | `BLOCKED_PENDING_DATA`; do not emit a lower level. |
| Valid lower row true and higher row false by a known contrary assertion | Lower row may emit after all checks; contrary evidence is not missing evidence. |
| Severity and risk disagree | Keep both; no implicit adjustment. |
| Customer impact without urgency, urgency without dependency, or dependency without customer effect | Evaluate exact eligible predicates; if none matches, unresolved. No averaging or proxy. |
| Multiple same-level true rows | Proposed stable ID tie rule above, with all matches retained; different-level matches choose highest only after no higher unknown. |
| No matching row | Unresolved and non-emitting; never `low` by default. |

Blocked and unresolved are not fifth priority levels. Existing
recommendations remain unchanged.

## 11. Coverage analysis

Covered classes are exactly the seven rows' source-pair and assertion
conjunctions, subject to valid producer context and approved client evidence.
Invalid classes reject; missing required evidence blocks; the D7 case has its
separate outcome. Uncovered classes include all other valid D2/D3/D5 value
combinations for each finding pair, plus non-deficiency findings with positive
business signals. There are no real client assertions in the production path,
so these are paper classes only. The proposal is **not implementation-ready**:
founder approval of rows and an explicit coverage or non-emitting policy are
still needed. No table can be called total merely because it has a no-match
branch.

## 12. Synthetic verification matrix

All 24 examples are non-executable. “Would emit” means *only if* the stated
row and tie/risk policies receive founder approval and real evidence validates.
`D2/D3/D5` in the requirements column names the exact required drivers;
`none` means no D2/D3/D5 claim is needed by that example's approved branch.

| ID | Governed synthetic inputs; candidate IDs | Required assertions | Proposed outcome and rationale | Founder dependency |
| --- | --- | --- | --- | --- |
| S01 | Material breach; D3-E1, D5-E1; B-C1/B-H1. | D3,D5; D2 not required because C1 is already highest true. | Would emit critical from timed material blocker. | B-C1. |
| S02 | Significant gap; D2-E1, D3-E2; B-H2. | D2,D3. | Would emit high for gap plus customer and executive evidence. | B-H2. |
| S03 | Clear deficiency; D2-E2,D3-E3,D5-E2; B-H3/B-M1. | D2,D3,D5. | Would emit medium; H3 false by reviewed absence. | B-M1. |
| S04 | Limited weakness; D2-E2,D3-E3,D5-E2; B-L1. | D2,D3,D5. | Would emit low from affirmative scoped reviews, not default. | B-L1. |
| S05 | Two true same-level rows in a future overlap. | Per those rows. | First stable rule ID selected; all matches retained. Current exact rows do not overlap. | Tie rule. |
| S06 | Material breach; D3 missing, D5-E1; B-C1/B-H1. | D3 for C1; other atoms as needed. | Block; higher C1 unresolved. | B-C1. |
| S07 | Material breach; D3-E2,D2-E1, D5 absent; B-C1/B-H1. | D3,D2; D5 not required because D3-E2 makes C1 false. | Would emit high under H1; lower row safe after higher false. | B-H1. |
| S08 | Significant gap, D2-E1, D3-E3; B-H2. | D2,D3. | No match; customer effect alone is not high. | Coverage choice. |
| S09 | Clear deficiency, D3-E1, D2-E2; B-H3/B-M1. | D2,D3; D5 only if M1 remains possible. | No match; urgency alone does not assign high and M1 is false. | Coverage choice. |
| S10 | Significant gap, D5-E1 only; B-H2. | D2,D3 for H2; supplied D5 validated. | Block if D2/D3 unresolved; dependency alone does not assign high. | B-H2. |
| S11 | Significant gap, D2-E1,D3-E2; B-H2. | D2,D3; D5 not required. | Would emit high; customer plus urgency with valid producer gap. | B-H2. |
| S12 | Material breach, D3-E1,D5-E1,D2 absent; B-C1. | D3,D5; D2 not required for C1. | Would emit critical if approved; no blanket D2 requirement. | B-C1. |
| S13 | Significant gap,D2-E1,D3-E3,D5-E1; B-H2. | D2,D3; supplied D5 validated. | No match; customer plus dependency without required action has no row. | Coverage choice. |
| S14 | Limited weakness, three scoped absence reviews; B-L1. | D2,D3,D5. | Would emit low; affirmative absence is EVALUATED, never NA. | B-L1. |
| S15 | Clear deficiency, D2-E2,D3-E3,D5 missing; B-M1. | D2,D3,D5. | Block, not medium. | B-M1. |
| S16 | Invalid supplied D5 on complete B-H2 inputs. | D2,D3; D5 supplied but invalid. | Reject even though B-H2 does not require D5. | F38-R2 already approved. |
| S17 | Conflicting D2-E1/E2 claims on same binding. | Depends on pair; both supplied. | Reject atomically. | Document 37 already approved. |
| S18 | Any finding-scoped insufficient confidence. | Validate supplied claims first. | Block before D8 emission, never low. | F38-D6 already approved. |
| S19 | Limited weakness, elevated assessment risk, complete B-L1 evidence. | D2,D3,D5. | Would emit low only if F41-RISK context-only choice approved; retain both classifications. | F41-RISK. |
| S20 | Observation/observation, three scoped absence reviews; B-L2. | D2,D3,D5. | Would emit low only under new evidence-backed B-L2 choice. | B-L2. |
| S21 | Strength/strength, three scoped absence reviews; B-L2. | D2,D3,D5. | Would emit low only under B-L2, not from Strength label alone. | B-L2. |
| S22 | Opportunity/opportunity, D2-E1 customer effect; B-L2 false. | D2 supplied; D3/D5 not needed to prove B-L2 false. | No match; positive signal needs a new business row. | Coverage choice. |
| S23 | Empty findings, minimal-informational risk, sole null-linked monitor. | none. | Separate approved D7-direction no-finding outcome, no four-level value. | Future representation only. |
| S24 | Observation/observation, D2-E1,D3-E3,D5-E2. | All supplied validated; B-L2 false by D2. | No matching row, unresolved, never default low. | Coverage choice. |

## 13. Final founder decision register

The founder has **already approved Option B design direction**. The rows
below are **new proposals**, not approvals. Approving a row would not appoint
a client business approver or authorize runtime work.

| ID; category | Exact proposed choice and evidence basis | Recommendation and business justification | Material alternative; consequence of approval / rejection |
| --- | --- | --- | --- |
| F40-OPTION-B; approved direction | Evidence-based rule precedence and rule-specific assertions. | Preserve; no reapproval requested. | Strict four-way conjunctions or automatic severity mapping are outside this approved direction. |
| F41-C1; emitting | B-C1 material breach + D3-E1 + D5-E1. | Recommend critical for timed material blocker with dependent work; D2 not automatically required. | Alternative high; approval adds narrow critical row / rejection leaves this class unresolved. |
| F41-H1; emitting | B-H1 material breach + D3-E2 + D2-E1. | Recommend high for customer effect plus untimed executive action after C1 is false. | Alternative critical without timing; approval adds row / rejection leaves class unresolved. |
| F41-H2; emitting | B-H2 significant gap + D2-E1 + D3-E2. | Recommend high for two evidenced business triggers. | Alternative require dependency too; approval adds row / rejection leaves class unresolved. |
| F41-H3; emitting | B-H3 clear deficiency + D2-E1 + D3-E1. | Recommend high for customer effect and timed action despite medium severity. | Alternative medium by severity; approval adds row / rejection leaves class unresolved. |
| F41-M1; emitting | B-M1 clear deficiency + three scoped absences. | Recommend planned correction from affirmative reviewed evidence. | Alternative no row; approval adds medium / rejection leaves class unresolved. |
| F41-L1; emitting | B-L1 limited weakness + three scoped absences. | Recommend low only from affirmative evidence. | Alternative no row; approval adds low / rejection leaves class unresolved. |
| F41-L2; emitting/coverage | B-L2 Observation, Strength, or Opportunity + three scoped absences. | Recommend one evidence-backed low rule for non-deficiencies; type alone is insufficient. | Alternative separate non-priority outcome needs its own founder decision; approval covers narrow class / rejection leaves it unresolved. |
| F41-RISK; risk role | Validate/retain assessment risk as context, no automatic local adjustment. | Recommend A because assessment-wide risk is not finding-specific evidence. | B/C need exact source-linked rows; approval resolves disagreement policy / rejection requires new risk predicates. |
| F41-TIE; conflict | Same-level true rules select first stable rule ID, retain all matches; higher level wins only after no higher unknown. | Recommend deterministic provenance and fail-closed evidence precedence. | Reject all same-level overlap; approval fixes tie policy / rejection needs alternate deterministic policy. |
| F41-COVER; coverage | Unmatched valid combinations remain non-emitting until exact additional rows or an approved bounded non-emitting domain exists. | Recommend no silent fallback while founder chooses significance of positive or mixed signals. | Default low is unsupported; approval makes partial scope explicit / rejection needs complete alternative rows. |

## 14. Remaining blockers

This proposal is not a total mapping. Founder approval is needed for each
emitting rule, the risk role, same-level tie policy, and explicit treatment of
uncovered valid input classes. The most important uncovered classes are
mixed positive/absence driver tuples and non-deficiency findings with
positive business signals. Real client-approved D2/D3/D5 sources and
production content, authority, currentness, and integrity verification are
also absent. No unsupported impact grade, client fact, numerical threshold,
or priority effect is smuggled into the current producer contract.

## 15. Next bounded action

Founder review can decide F41-C1/H1/H2/H3/M1/L1/L2, F41-RISK, F41-TIE, and
F41-COVER in one bounded step. If coverage remains partial, explicitly retain
non-emitting unmatched cases or specify additional exact evidence-backed
rows before any implementation proposal. No D8 rule in this document is
approved or executable; no Stage 2 completion is claimed.

**Final status: PROPOSED — FOUNDER APPROVAL REQUIRED.**
