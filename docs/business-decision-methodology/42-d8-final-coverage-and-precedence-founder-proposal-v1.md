# D8 Final Coverage and Precedence — Founder Proposal v1

**Status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**

## 1. Purpose and approved directions

This is one founder-reviewable D8 coverage proposal. The founder approved
Option B and F41-A through F41-E as **methodology design directions only**:
retain the seven [Document 41](41-d8-evidence-based-precedence-founder-proposal-v1.md)
candidates without approving them; keep assessment risk as validated context;
preserve the priority and all matching rule IDs in deterministic order for a
same-level tie; require D2/D3/D5 only when candidate rules need them; block a
lower emission while a higher candidate lacks required evidence; and address
mixed signals and non-deficiency findings without a type-only default.
**No D8 emitting predicate is approved.** This document proposes four new
bounded rows and classifies all remaining valid symbolic input classes. It
does not implement priority or claim a total four-level mapping.

## 2. Existing methodology authority

The [priority methodology](06-recommendation-priority.md) establishes four
levels and qualitative drivers, not an executable table.
[Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
approves the assertion source and authority separation.
[Document 37](37-founder-priority-applicability-approval-v1.md) approves D2/D3/D5
evaluated and fail-closed meanings and **no `NOT_APPLICABLE` branch**.
[Document 39](39-founder-final-priority-direction-approval-v1.md) approves
F38-D1/R1/R2/D3/D4/D5/D6/D7 direction: consequence context without a new
impact grade, rule-dependent assertions, validation of every submitted
assertion, separate severity/risk, confidence gating, and a separate D7
no-finding outcome. The [governed input model](../../src/assessment/governed_assessment_input.py),
[decision runtime](../../src/assessment/governed_decision_runtime.py), and
[golden regressions](../../tests/test_golden_fixture_regression.py) establish
the actual producer vocabulary. No real client-approved D2/D3/D5 assertions
or production content/currentness authority are available.

The seven valid `(findingType, businessConsequenceBasis)` pairs are listed
in Section 7. Governed finding severity is `critical`, `high`, `medium`,
`low`, or `informational`, linked to its severity decision ID/version.
Assessment risk is `critical-risk`, `elevated-risk`, `moderate-risk`,
`low-risk`, or `minimal-informational`, with its risk decision ID/version.
Confidence is `very-high-confidence`, `high-confidence`,
`moderate-confidence`, `low-confidence`, or `insufficient-confidence`, with
its confidence decision ID/version. Recommendation class is
`immediate-action`, `priority-action`, `planned-improvement`,
`best-practice`, or `monitor`, with its recommendation decision ID/version
and exact snapshot/finding link. None of these labels alone emits D8
priority. D2 has E1/E2, D3 has E1/E2/E3, and D5 has E1/E2 under the
approved meanings; each future real assertion also needs client business
approval and governed source provenance.

## 3. Original seven candidates

The following are the **exact Document 41 predicates**, reproduced as
unapproved candidates. Their evidence requirements are: exact snapshot and
recommendation/finding binding, valid governed finding-pair/severity, risk and
confidence provenance, and current client-approved evidence for each named
D2/D3/D5 assertion. `R` means `REQUIRED_BY_RULE`; `N` means
`NOT_REQUIRED_BY_RULE`. None is `NOT_APPLICABLE`.

| ID / proposed level | Exact Boolean predicate | D2/D3/D5 | Finding type, rationale, and uncovered combinations |
| --- | --- | --- | --- |
| B-C1 / critical | `(Deficiency, material current breach)` AND D3-E1 AND D5-E1. | N/R/R | Timed material blocker with directed dependent work; other material-breach tuples uncovered unless another row matches. |
| B-H1 / high | `(Deficiency, material current breach)` AND D3-E2 AND D2-E1. | R/R/N | Material breach with customer effect and untimed executive action; other tuples uncovered. |
| B-H2 / high | `(Deficiency, significant gap)` AND D2-E1 AND D3-E2. | R/R/N | Significant gap with customer and executive evidence; other tuples uncovered. |
| B-H3 / high | `(Deficiency, clear deficiency)` AND D2-E1 AND D3-E1. | R/R/N | Clear deficiency with customer effect and timed action; other tuples uncovered. |
| B-M1 / medium | `(Deficiency, clear deficiency)` AND D2-E2 AND D3-E3 AND D5-E2. | R/R/R | Planned correction after three scoped affirmative absences; mixed tuples uncovered. |
| B-L1 / low | `(Deficiency, limited weakness)` AND D2-E2 AND D3-E3 AND D5-E2. | R/R/R | Lower intervention supported by three scoped reviews; mixed tuples uncovered. |
| B-L2 / low | Pair is `(Observation, observation)`, `(Strength, strength)`, or `(Opportunity, opportunity)` AND D2-E2 AND D3-E3 AND D5-E2. | R/R/R | Non-deficiency with three scoped reviews; positive-signal tuples uncovered. |

No row is modified or promoted by this reproduction. Document 41's proposed
lexicographically first *single* decision ID for same-level ties is
**superseded by F41-C**: preserve all matching IDs in deterministic order;
do not choose a primary ID without a separate contract decision.

## 4. Mixed-signal coverage proposal

Four additional rows address selected mixed signals. Each is a **NEW
PROPOSED FOUNDER BUSINESS CHOICE**. They use approved assertion *meanings*
but propose new priority *effects*. Neither a missing claim nor a scoped
absence is inferred from another field.

| ID / proposed level | Exact Boolean predicate | D2/D3/D5 | Business rationale and higher-rule exclusion |
| --- | --- | --- | --- |
| N-H4 / high | `(Deficiency, material current breach)` AND D2-E1 AND D3-E1 AND D5-E2. | R/R/R | Customer effect plus timed action despite an affirmed no-dependency review could warrant elevated intervention. D5-E2 conclusively excludes critical B-C1; no lower fallback from missing D5. |
| N-H5 / high | `(Deficiency, significant gap)` AND D2-E1 AND D3-E3 AND D5-E1. | R/R/R | Customer effect and directed dependency despite reviewed no executive action could warrant elevated intervention. The exact D3-E3 value excludes B-H2's D3-E2. |
| N-H6 / high | `(Deficiency, significant gap)` AND D2-E2 AND D3-E1 AND D5-E1. | R/R/R | Timed executive action and directed dependency despite reviewed no customer effect could warrant elevated intervention. D2-E2 excludes B-H2's D2-E1. |
| N-H7 / high | Pair is `(Observation, observation)`, `(Strength, strength)`, or `(Opportunity, opportunity)` AND D2-E1 AND D3-E1 AND D5-E1. | R/R/R | Three independent, approved positive business signals could warrant elevated intervention even for a non-deficiency. Finding type alone never emits high. |

These new rows do not claim that D2-E1 measures magnitude or direction of
customer effect, that a time-bound action is automatically critical, or that
the two D5 draft labels have distinct effects. Other customer-only,
urgency-only, dependency-only, two-signal, and mixed combinations remain
unmapped unless an exact row above matches. This is an intentional gap,
not a hidden medium/low default.

## 5. Non-deficiency coverage

The actual non-deficiency pairs are Observation/`observation`,
Strength/`strength`, and Opportunity/`opportunity`; no other type is accepted
by the governed input. B-L2 proposes low only after three documented scoped
absences. N-H7 proposes high only when D2-E1, D3-E1 with its timing source,
and D5-E1 with a same-snapshot target are all established. Any other valid
combination is **UNRESOLVED_FOUNDER_CHOICE**, not automatically low, medium,
or a new non-priority outcome. `insufficient-confidence` blocks
finding-scoped assignment for all types; invalid, contradictory, or stale
supplied evidence rejects. Existing finding generation and recommendation
selection are unchanged.

## 6. Minimum sufficient rule design

The consolidated proposed set has seven unchanged and four new emitting
rows. New rows were added only where multiple approved business assertions
provide a concrete mixed-signal rationale. There is no rule for every
permutation: D2-E1 says presence, not magnitude; D3-E1 says documented
timing, not deadline importance; D5-E1 says a directed relation, not size of
the dependent work. An arbitrary complete four-level mapping would exceed
those facts. Assessment risk remains validated context under F41-B, never a
silent modifier. Finding severity and business-consequence basis are distinct
governed fields; neither alone is priority. All eleven rows remain proposals.

## 7. Candidate eligibility algorithm

Use the validated producer `(findingType, businessConsequenceBasis)` pair
**before** reading D2/D3/D5 assertions to select candidate IDs:

| Governed pair | Eligible candidate IDs, highest level first |
| --- | --- |
| Deficiency / material current breach | B-C1; B-H1, N-H4 |
| Deficiency / significant gap | B-H2, N-H5, N-H6 |
| Deficiency / clear deficiency | B-H3; B-M1 |
| Deficiency / limited weakness | B-L1 |
| Observation / observation | N-H7; B-L2 |
| Strength / strength | N-H7; B-L2 |
| Opportunity / opportunity | N-H7; B-L2 |

For each eligible row, resolve its Boolean atoms in three-valued logic:
`TRUE` when all required atoms have valid evidence; `FALSE` when an existing
governed fact or valid evaluated assertion contradicts any required atom;
`PENDING_REQUIRED_EVIDENCE` when no known fact excludes it but a required
assertion is missing or unresolved. Invalid submitted context is `INVALID`
before this stage, regardless of candidate relevance. A row excluded by the
producer pair or a valid contrary assertion is
`EXCLUDED_BY_GOVERNED_FACT`; its remaining atoms are
`NOT_REQUIRED_BY_RULE` for that decision. An eligible row's still-needed
atoms are `REQUIRED_BY_RULE`. This selection is noncircular and never uses
missing evidence to exclude a higher row.

Before emitting a lower level, every higher eligible row must be `FALSE`.
At the winning level, every other eligible row must also be resolved to
`TRUE` or `FALSE` before emission, so the required all-match ID list cannot
omit a still-pending peer. A pending peer blocks final emission even when
another row at that level is already true.
For example, B-H1 can emit for material breach with D3-E2 because D3-E2
excludes B-C1's D3-E1; it need not require D5. B-M1 can emit for clear
deficiency only after D2-E2/D3-E3 rule out B-H3. B-L2 can emit for a
non-deficiency only after D2-E2/D3-E3/D5-E2 rule out N-H7. A higher
`PENDING_REQUIRED_EVIDENCE` blocks; no lower row emits.

## 8. Deterministic precedence

1. Validate structure, supported versions, exact assessment/snapshot,
   finding and recommendation identity, every supplied assertion's business
   authority and approval scope, evidence provenance/content,
   revision/currentness, duplicates, and contradictions. Any invalid
   submitted assertion rejects the complete set, even if no row needs it.
2. Apply the approved D7 sole null-linked no-findings outcome, with no
   four-level priority. Malformed monitor context rejects.
3. Apply the approved finding-scoped insufficient-confidence block; other
   four confidence classes remain contextual.
4. Select candidates from the governed pair; resolve `critical` candidates,
   then `high`, `medium`, and `low`. Missing required evidence for a
   potentially matching higher row blocks lower emission.
5. The highest true priority level wins only after higher candidates are
   false and every peer at that level is resolved. For same-level true rules,
   preserve that priority and **all matched
   rule IDs in deterministic ascending ID order**, as F41-C directs. No
   unapproved primary decision ID is selected. Different recommendations
   may share priority; existing recommendation order never assigns it.
6. A valid class with no true rule is non-emitting and unresolved, not low.
   There is no model-generated or partial priority publication.

## 9. Consolidated D8 decision table

All emitting rows are **PROPOSED — NOT AUTHORITATIVE**. `U` means unchanged
Document 41 candidate; `N` means new candidate. Required producer facts for
all rows are valid snapshot/finding/recommendation identity, governed pair
and severity consistency, supported risk and confidence provenance, and
current evidence/approval for each `R` assertion. `R/N` in three driver
columns means `REQUIRED_BY_RULE`/`NOT_REQUIRED_BY_RULE`. The exact predicate
column is the full row-specific Boolean condition; precedence is the listed
priority order, with F41-C same-level handling. Missing required evidence
blocks; invalid or conflicting supplied evidence rejects for every row.

| ID / status | Priority | Exact predicate; applicable finding class | D2 | D3 | D5 | Evidence and business rationale | Coverage / founder status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B-C1 / U | critical | Material current breach AND D3-E1 AND D5-E1; Deficiency. | N | R | R | Timed material blocker with dependent work; customer claim not needed. | Narrow class; FOUNDER APPROVAL REQUIRED. |
| B-H1 / U | high | Material current breach AND D3-E2 AND D2-E1; Deficiency. | R | R | N | Untimed action plus customer effect; D3-E2 excludes B-C1. | Narrow class; FOUNDER APPROVAL REQUIRED. |
| B-H2 / U | high | Significant gap AND D2-E1 AND D3-E2; Deficiency. | R | R | N | Customer effect and untimed executive action. | Narrow class; FOUNDER APPROVAL REQUIRED. |
| B-H3 / U | high | Clear deficiency AND D2-E1 AND D3-E1; Deficiency. | R | R | N | Customer effect plus documented timed action. | Narrow class; FOUNDER APPROVAL REQUIRED. |
| N-H4 / N | high | Material current breach AND D2-E1 AND D3-E1 AND D5-E2; Deficiency. | R | R | R | Customer/timed action, reviewed no dependency; B-C1 false. | Mixed class; FOUNDER APPROVAL REQUIRED. |
| N-H5 / N | high | Significant gap AND D2-E1 AND D3-E3 AND D5-E1; Deficiency. | R | R | R | Customer/dependency despite reviewed no action. | Mixed class; FOUNDER APPROVAL REQUIRED. |
| N-H6 / N | high | Significant gap AND D2-E2 AND D3-E1 AND D5-E1; Deficiency. | R | R | R | Timed action/dependency despite reviewed no customer effect. | Mixed class; FOUNDER APPROVAL REQUIRED. |
| N-H7 / N | high | Observation/observation OR Strength/strength OR Opportunity/opportunity, AND D2-E1 AND D3-E1 AND D5-E1. | R | R | R | Three positive business signals for a non-deficiency; type alone insufficient. | Non-deficiency class; FOUNDER APPROVAL REQUIRED. |
| B-M1 / U | medium | Clear deficiency AND D2-E2 AND D3-E3 AND D5-E2; Deficiency. | R | R | R | Planned correction after three scoped reviews; B-H3 false. | Narrow class; FOUNDER APPROVAL REQUIRED. |
| B-L1 / U | low | Limited weakness AND D2-E2 AND D3-E3 AND D5-E2; Deficiency. | R | R | R | Lower intervention from affirmative reviews. | Narrow class; FOUNDER APPROVAL REQUIRED. |
| B-L2 / U | low | Observation/observation OR Strength/strength OR Opportunity/opportunity, AND D2-E2 AND D3-E3 AND D5-E2. | R | R | R | Three scoped reviews; N-H7 false. | Non-deficiency class; FOUNDER APPROVAL REQUIRED. |

No original candidate is revised or superseded. F41-C supersedes only the
Document 41 single-primary-ID *tie representation*, not an emitting row.
No rule uses a numerical weight, deadline threshold, graded impact, or
automatic assessment-risk modifier.

## 10. Coverage matrix

Let `P/A` denote D2-E1/E2, `T/U/A` denote D3-E1/E2/E3, and `P/A` denote
D5-E1/E2. For each of seven governed finding pairs there are twelve
symbolic complete driver tuples. These are equivalence classes for D8
analysis, **not a claim that every cross-product is present in a real
assessment**. The four eligible non-insufficient confidence classes and five
risk classes retain the same proposed priority behavior; insufficient
confidence blocks. Invalid types/versions/links/assertions reject first;
missing required evidence blocks; the sole valid no-findings monitor has its
approved separate outcome.

| Finding pair | `COVERED_BY_PROPOSED_RULE` tuples (D2,D3,D5) | Other complete valid tuples | Missing/invalid/no findings |
| --- | --- | --- | --- |
| Deficiency / material current breach | B-C1: `(P,T,P)` or `(A,T,P)`; B-H1: `(P,U,P)` or `(P,U,A)`; N-H4: `(P,T,A)`. | `UNRESOLVED_FOUNDER_CHOICE`; no default level. | Candidate-required missing is `BLOCKED_REQUIRED_EVIDENCE`; invalid rejects. |
| Deficiency / significant gap | B-H2: `(P,U,P)` or `(P,U,A)`; N-H5: `(P,A,P)`; N-H6: `(A,T,P)`. | `UNRESOLVED_FOUNDER_CHOICE`. | Same fail-closed branches. |
| Deficiency / clear deficiency | B-H3: `(P,T,P)` or `(P,T,A)`; B-M1: `(A,A,A)`. | `UNRESOLVED_FOUNDER_CHOICE`. | Same fail-closed branches. |
| Deficiency / limited weakness | B-L1: `(A,A,A)`. | `UNRESOLVED_FOUNDER_CHOICE`. | Same fail-closed branches. |
| Observation / observation | N-H7: `(P,T,P)`; B-L2: `(A,A,A)`. | `UNRESOLVED_FOUNDER_CHOICE`. | Same fail-closed branches. |
| Strength / strength | N-H7: `(P,T,P)`; B-L2: `(A,A,A)`. | `UNRESOLVED_FOUNDER_CHOICE`. | Same fail-closed branches. |
| Opportunity / opportunity | N-H7: `(P,T,P)`; B-L2: `(A,A,A)`. | `UNRESOLVED_FOUNDER_CHOICE`. | Same fail-closed branches. |
| Empty finding collection | No four-level tuple. | None. | `SEPARATE_APPROVED_OUTCOME` only for exact D7 monitor; malformed case `INVALID_INPUT`. |

The table explicitly classifies every symbolic complete tuple as covered or
unresolved: 19 of 84 tuples are covered by a proposed row; 65 remain
unresolved. This count does **not** assert that every tuple is realizable in
a client assessment. It does **not** demonstrate total four-level coverage. The
remaining exact business question is how to assign priority, or whether to
approve a bounded non-emitting domain, for valid mixed tuples not listed.
No fifth priority level or automatic low is proposed.

## 11. Synthetic verification matrix

All 30 cases are non-executable paper checks. `R` lists the required
D2/D3/D5 assertions; `—` means no driver is required by the stated branch.
“Would emit” depends on founder approval of its rule and real valid client
evidence. Every example assumes otherwise valid producer provenance unless
it explicitly tests invalidity.

| ID | Synthetic governed inputs; candidate IDs | R | Proposed result and business reason | Approval dependency |
| --- | --- | --- | --- | --- |
| S01 | Material breach `(A,T,P)`; B-C1/B-H1/N-H4. | D3,D5 | Would emit critical for timed material blocker with dependent work. | B-C1. |
| S02 | Significant gap `(P,U,A)`; B-H2/N-H5/N-H6. | D2,D3 | Would emit high for customer effect and executive action. | B-H2. |
| S03 | Clear deficiency `(A,A,A)`; B-H3/B-M1. | D2,D3,D5 | Would emit medium for planned correction after reviews. | B-M1. |
| S04 | Limited weakness `(A,A,A)`; B-L1. | D2,D3,D5 | Would emit low from three scoped reviews, not a default. | B-L1. |
| S05 | Significant gap `(P,A,A)`; B-H2/N-H5/N-H6. | D2,D3,D5 to resolve candidates. | Unresolved; customer effect alone proves no listed high row. | Coverage choice. |
| S06 | Significant gap `(A,T,A)`; same IDs. | D2,D3,D5. | Unresolved; timed action alone has no row. | Coverage choice. |
| S07 | Significant gap `(A,A,P)`; same IDs. | D2,D3,D5. | Unresolved; dependency alone has no row. | Coverage choice. |
| S08 | Clear deficiency `(P,T,A)`; B-H3/B-M1. | D2,D3 | Would emit high for customer effect plus timed action without dependency. | B-H3. |
| S09 | Significant gap `(P,A,P)`; B-H2/N-H5/N-H6. | D2,D3,D5 | Would emit high for customer/dependency, reviewed no action. | N-H5. |
| S10 | Significant gap `(A,T,P)`; same IDs. | D2,D3,D5 | Would emit high for timed action/dependency, reviewed no customer effect. | N-H6. |
| S11 | Non-deficiency `(P,T,P)`; N-H7/B-L2. | D2,D3,D5 | Would emit high from all three positive signals. | N-H7. |
| S12 | Non-deficiency `(A,A,A)`; N-H7/B-L2. | D2,D3,D5 | Would emit low from three scoped absences, not type alone. | B-L2. |
| S13 | Material breach `(P,T,A)`; B-C1/B-H1/N-H4. | D2,D3,D5 | Would emit high; D5-E2 excludes critical B-C1. | N-H4. |
| S14 | Material breach D3-E1,D5-E1,D2 absent; same IDs. | D3,D5 | Would emit critical; D2 is not needed after C1 true. | B-C1. |
| S15 | Significant gap D2 missing,D3-E2,D5-E2. | D2,D3 | Block: B-H2 could match; absence is not D2-E2. | B-H2. |
| S16 | Material breach D3 missing,D5-E1. | D3,D5 | Block: higher B-C1 unresolved. | B-C1. |
| S17 | Limited weakness D2-E2,D3-E3,D5 missing. | D2,D3,D5 | Block B-L1, never low from missing dependency review. | B-L1. |
| S18 | Material breach D3 missing,D5-E1,D2-E1. | D3 plus supplied D2,D5. | Block higher B-C1 although B-H1 could match if D3-E2 were established. | B-C1. |
| S19 | Material breach `(P,U,A)`; B-C1/B-H1/N-H4. | D2,D3; D5 supplied. | Would emit high; D3-E2 excludes critical. | B-H1. |
| S20 | Two hypothetical critical rows true for one recommendation. | Their rule atoms. | Critical retained; all matched IDs sorted. Current table has one critical row. | F41-C already approved. |
| S21 | Two hypothetical high rows true for one recommendation. | Their rule atoms. | High retained; all matched IDs sorted. Current exact high rows are disjoint. | F41-C already approved. |
| S22 | Same-level tie across different recommendations. | Per each row. | Each retains its priority and matched IDs; existing order does not assign priority. | F41-C already approved. |
| S23 | Limited weakness `(A,A,A)` with elevated assessment risk. | D2,D3,D5 | Would emit low under B-L1 only if F41-B context-only risk direction and B-L1 accepted; retain both upstream labels. | B-L1; F41-B approved direction. |
| S24 | Observation `(P,T,P)`. | D2,D3,D5 | Would emit high only under N-H7, not from type alone. | N-H7. |
| S25 | Strength `(P,T,P)`. | D2,D3,D5 | Would emit high only under N-H7; source facts required. | N-H7. |
| S26 | Opportunity `(P,A,A)`. | D2,D3,D5 to resolve N-H7/B-L2. | Unresolved; positive customer signal alone has no justified row. | Coverage choice. |
| S27 | Any finding with `insufficient-confidence`, supplied claims otherwise valid. | Validate supplied. | Block finding-scoped priority, no downgrade. | F38-D6 already approved. |
| S28 | Invalid supplied D5 on otherwise complete B-H2 tuple. | D2,D3; D5 supplied. | Reject atomically even if B-H2 does not need D5. | F38-R2 already approved. |
| S29 | Conflicting current D2-E1/E2 assertions. | Validate both. | Reject; no selected winner. | Document 37 already approved. |
| S30 | Sole null-linked monitor, empty findings, minimal-informational risk. | — | Approved D7 separate no-finding outcome, no four-level priority. | Future representation only. |

S05–S07 and S26 also demonstrate `NO MATCH` for complete valid inputs;
they remain unresolved, not invalid or low.

## 12. Final founder decision register

The founder has **already approved** F40-OPTION-B and F41-A–E direction;
no reapproval is requested. The seven B rows are unchanged proposals. Four
N rows are new proposals. Approval of any row does not appoint a client
approver or authorize code.

| Decision ID / group | Exact proposed choice and recommendation | Business basis and material alternative | Approval / rejection consequence |
| --- | --- | --- | --- |
| F42-B / original seven | Review B-C1,B-H1,B-H2,B-H3,B-M1,B-L1,B-L2 **as written in Document 41**; recommend approval only after founder accepts each exact level/conjunction. | Governed finding pair plus approved assertion meanings; alternative is to reject a specific row without replacing it by a severity default. | Approval adds narrow evidence-backed rows; rejection leaves their classes unresolved. |
| F42-H4 / mixed | Recommend N-H4 high for material breach with customer effect, timed action, and affirmed no dependency. | D5-E2 excludes critical B-C1; alternative medium would discount documented timing/customer effect. | Approval covers one mixed class; rejection leaves it unresolved. |
| F42-H5 / mixed | Recommend N-H5 high for significant gap with customer effect, dependency, affirmed no executive action. | Two evidenced business triggers; alternative medium requires a separate rationale. | Approval covers one mixed class; rejection leaves it unresolved. |
| F42-H6 / mixed | Recommend N-H6 high for significant gap with timed action, dependency, affirmed no customer effect. | Timed action plus dependent work; alternative critical lacks material-breach basis. | Approval covers one mixed class; rejection leaves it unresolved. |
| F42-H7 / non-deficiency | Recommend N-H7 high for Observation/Strength/Opportunity only with all three positive approved assertions. | Type alone has no priority effect; alternative separate type-specific rules increase policy surface. | Approval covers a narrow non-deficiency class; rejection leaves it unresolved. |
| F42-COVER / unresolved | Recommend retain non-emitting status for all other valid tuples until founder approves exact additional rows or a bounded non-emitting domain. | D2 presence lacks magnitude/direction and D3/D5 lack standalone priority effect; alternative default low is unsupported. | Approval documents partial scope; rejection requires explicit replacement predicates before a total mapping is claimed. |
| F42-PROVENANCE / tie | Apply F41-C: retain priority and every same-level matched rule ID in ascending order, without an unapproved primary ID. | Exact deterministic trace; alternative first-ID-only representation was not approved. | Approval of later contract can encode this; rejection must still preserve F41-C's all-match evidence. |

## 13. Exact remaining blockers

The proposed table does **not** map every complete valid tuple. The precise
remaining business decision is the priority effect, if any, of mixed
positive/affirmative-absence combinations outside the listed rows and of
non-deficiency findings with one or two positive business signals. The
founder must either specify additional exact evidence-backed predicates or
approve a bounded non-emitting domain for those classes. No new input grade,
numerical threshold, automatic risk modifier, or fifth priority level is
justified by current evidence. Actual client-approved assertions, authority,
content verification, currentness, and integrity are separate production
prerequisites. This is a methodology/source gap, not a local-validator defect.

## 14. Implementation restrictions

No row in this document is approved or executable. No source code, canonical
48-question assessment, scoring, finding generation, recommendation
selection, risk/confidence calculations, golden fixture, frozen v2/v3
contract, signed handoff, local synthetic validator, EIP, CEP, Platform, or
AWS resource is changed. No client fact or production authority is
invented. No priority assignment or Stage 2 completion is claimed.

## 15. Recommended next action

In one founder review, decide the seven unchanged B rows, four new N rows,
and the single F42-COVER question: approve exact additional predicates for
the remaining symbolic classes or explicitly retain a bounded non-emitting
domain. Then a complete versioned methodology can be assessed separately
for implementation readiness. Do not implement from this partial proposal.

**Final status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**
