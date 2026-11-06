# D8 Generalized Priority Coverage — Founder Decision Proposal v1

**Status: PROPOSED — FOUNDER APPROVAL REQUIRED. No new D8 emitting or non-emitting predicate in this document is approved; the D7 no-finding treatment remains previously approved.**

## 1. Purpose and founder direction

F42-GENERALIZED-COVERAGE is **APPROVED — METHODOLOGY DESIGN DIRECTION**. The founder authorizes a proposal for generalized, evidence-based D8 rules and explicit non-emitting outcomes. This does not approve a row, a non-emitting predicate, a production contract, or implementation. This document reconciles the [Document 42](42-d8-final-coverage-and-precedence-founder-proposal-v1.md) domain without a numerical score, an impact grade, a new assessment question, or a default priority. Option B and F41-A through F41-E remain approved directions.

## 2. Approved methodology boundaries

[Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md) separates founder methodology approval from client business-fact approval. [Document 37](37-founder-priority-applicability-approval-v1.md) approves D2-E1/E2, D3-E1/E2/E3, and D5-E1/E2 meanings, validation, and **no D2/D3/D5 NOT_APPLICABLE branch**. [Document 39](39-founder-final-priority-direction-approval-v1.md) keeps consequence context, severity, assessment risk, confidence, and priority distinct; the first four confidence classes are context, insufficient confidence blocks finding-scoped assignment, and the exact D7 monitor has a separate no-finding outcome. [Document 41](41-d8-evidence-based-precedence-founder-proposal-v1.md) proposes seven unapproved rows; Document 42 adds four unapproved rows. Assessment-wide risk remains validated context under F41-B. F41-C preserves all matched IDs at the emitted level in deterministic order. F41-D blocks lower emission while a potentially applicable higher rule lacks required evidence. F41-E bars a finding-type-only default.

## 3. Actual producer input domain

The [governed finding input](../../src/assessment/governed_assessment_input.py) supports exactly seven pairs: Deficiency with `material current breach`, `significant gap`, `clear deficiency`, or `limited weakness`; Observation/`observation`; Strength/`strength`; Opportunity/`opportunity`. Governed severity is `critical`, `high`, `medium`, `low`, or `informational`. Assessment risk is `critical-risk`, `elevated-risk`, `moderate-risk`, `low-risk`, or `minimal-informational`. Confidence is `very-high-confidence`, `high-confidence`, `moderate-confidence`, `low-confidence`, or `insufficient-confidence`. The [recommendation runtime](../../src/assessment/governed_decision_runtime.py) binds recommendations to findings and decision ID/version; its classes are `immediate-action`, `priority-action`, `planned-improvement`, `best-practice`, and `monitor`. Rule ID alone does not identify an instance. The [golden regression](../../tests/test_golden_fixture_regression.py) preserves historical outputs.

D2 `P/A` means E1 evidenced customer effect / E2 scoped affirmed absence. D3 `T/U/A` means E1 documented timed action / E2 documented untimed action / E3 scoped affirmed absence. D5 `P/A` means E1 evidenced directed same-snapshot relation / E2 scoped affirmed absence. These are approved meanings, **not approved priority effects**. Every submitted real assertion would need exact snapshot/recommendation binding, source identity and revision, admissible evidence, client business approval, currentness, and validation. The committed local synthetic validator supplies none of the real client facts or production authority.

## 4. Reconciliation of 84 tuples

The bounded projection is seven governed pairs × two D2 values × three D3 values × two D5 values = **84 complete symbolic tuples**. It excludes missing/invalid assertions, insufficient confidence, and D7 no findings. Severity, risk, and the four eligible confidence values remain governed context rather than additional D8 cross-product axes. A tuple is a possible symbolic class, not a claim that a real client supplied it or that every combination is realizable. Document 42 covered 19 by proposed emitting rows and left 65 unresolved. The seven-row proposal below covers 21 by an emitting row and assigns the other 63 an explicit proposed `PRIORITY_NOT_DETERMINED` disposition. Two newly covered tuples are significant gap with D2-E1 and D3-E1, with either D5 value. This is **21 substantive proposed emissions, not 84 priority assignments**.

The complete 84-cell ledger in Section 12 specifies the eligible pair row, exact driver tuple, matching rule IDs, and proposed disposition. All three assertion values exist in that ledger; Section 7 specifies the smaller rule-dependent subset needed for a live decision.

## 5. Business-equivalent groups

The groups below partition the **65 Document 42 unresolved tuples**. They group by governed consequence and the evidence pattern that excludes an existing emitting row, not by a count of positive assertions. `*` means either allowed value of that driver; `T/U` and `U/A` mean the listed values. All groups have valid complete evidence and a proposed non-emitting disposition unless a specific new row covers them. They do **not** assert identical business importance within a group.

| Group | Exact D2,D3,D5 membership; count | Existing candidates and evidence meaning | Generalized treatment / remaining business choice |
| --- | --- | --- | --- |
| M1 | Material breach `(*,A,*)`; 4 | B-C1/B-H1/N-H4 excluded by affirmed no executive action. | Proposed PND; no justified urgency-based emission. |
| M2 | Material breach `(A,U,*)`; 2 | Untimed action but affirmed no customer effect; original high row excluded. | Proposed PND; founder could later define an untimed-action-only effect. |
| M3 | Material breach `(A,T,A)`; 1 | Timed action with affirmed no customer effect or dependency. | Proposed PND; timing alone has no approved level. |
| S0 | Significant gap `(P,T,*)`; 2 | Customer effect plus timed executive action; none of Document 42's eleven rows matched. | Proposed G-H2 high branch; exact new business effect requires founder approval. |
| S1 | Significant gap `(P,A,A)`; 1 | Customer effect alone, scoped no action/relation. | Proposed PND; no one-signal high rule. |
| S2 | Significant gap `(A,T,A)`; 1 | Timed action alone, scoped no customer effect/relation. | Proposed PND; timing source does not establish business magnitude. |
| S3 | Significant gap `(A,U,*)`; 2 | Untimed action, affirmed no customer effect; dependency varies. | Proposed PND; no untimed-action/dependency effect is established. |
| S4 | Significant gap `(A,A,*)`; 2 | No customer effect or action; dependency varies. | Proposed PND; a relation alone is not a level. |
| C1 | Clear deficiency `(P,U/A,*)`; 4 | Customer effect without timed action; B-H3 false. | Proposed PND; customer presence has no magnitude grade. |
| C2 | Clear deficiency `(A,T/U,*)`; 4 | Executive action with affirmed no customer effect; B-H3/B-M1 false. | Proposed PND; action alone has no level. |
| C3 | Clear deficiency `(A,A,P)`; 1 | Scoped no customer/action; directed relation excludes B-M1. | Proposed PND; dependency alone has no level. |
| L1 | Limited weakness `(P,*,*)`; 6 | Customer effect excludes B-L1; action/relation may vary. | Proposed PND; no automatic low or escalation. |
| L2 | Limited weakness `(A,T/U,*)`; 4 | Executive action excludes B-L1; relation may vary. | Proposed PND; no timing threshold invented. |
| L3 | Limited weakness `(A,A,P)`; 1 | Directed relation excludes B-L1. | Proposed PND; no dependency-only level. |
| N1 | Each non-deficiency pair `(P,*,*)` except `(P,T,P)`; 15 total | Customer effect with other signals varying; B-L2 false and N-H7 incomplete. | Proposed PND; Observation/Strength/Opportunity does not itself set priority. |
| N2 | Each non-deficiency pair `(A,T/U,*)`; 12 total | Executive action but affirmed no customer effect; high/low candidates false. | Proposed PND; action alone has no non-deficiency level. |
| N3 | Each non-deficiency pair `(A,A,P)`; 3 total | Directed relation with two scoped absences; B-L2 false. | Proposed PND; relation alone has no level. |

Counts: material 7, significant 8 (S0's 2 proposed emissions plus 6 PND), clear 9, limited 11, and three non-deficiency pairs 30 = **65 Document 42 unresolved tuples**. After S0, **63** remain PND. The founder's precise remaining business choice is whether these 63 complete classes should retain a review-required non-emitting disposition or receive additional explicitly justified rules. No group is mapped to a level merely because it contains a positive signal.

## 6. Generalized emitting rules

Every row below is a **PROPOSED FOUNDER BUSINESS CHOICE**. The governed pair is an eligibility fact, not a severity-to-priority conversion. `AND`/`OR` are literal Boolean operators; the `OR` alternatives in G-H2 are evidence-backed business combinations, not arithmetic weights. Each required assertion must satisfy Document 37 and the client-approved source model. Missing required evidence blocks; any invalid submitted claim rejects. Higher-priority pending rows block lower emission. Same-level matched IDs are retained in ascending order.

| ID / level / precedence | Exact predicate; eligible pair | Rule-specific D2/D3/D5 | Business rationale; count of matching complete tuples |
| --- | --- | --- | --- |
| B-C1 / critical / 1 | Material current breach AND D3-T AND D5-P. | N/R/R | Timed action and directed dependent work in a material breach may warrant highest intervention; **2**. Original candidate retained unchanged. |
| G-H1 / high / 2 | Material current breach AND D2-P AND (D3-T OR D3-U). | R/R/N; D5 becomes required only if D3-T leaves B-C1 potentially true. | Customer effect with documented executive action may warrant elevated intervention; **4 matches, 3 emitted high** because `(P,T,P)` emits critical. Merges B-H1/N-H4 without a D5-based high shortcut. |
| G-H2 / high / 2 | Significant gap AND ((D2-P AND (D3-T OR D3-U)) OR (D2-P AND D5-P) OR (D3-T AND D5-P)). | Conditional: each satisfied disjunct requires only its named drivers; to prove all disjuncts false, resolve every not-yet-excluded disjunct. | Customer plus action, customer plus dependency, or timed action plus dependency may warrant elevated intervention; **6**. Merges B-H2/N-H5/N-H6 and adds the two documented timed-action/customer tuples. |
| B-H3 / high / 2 | Clear deficiency AND D2-P AND D3-T. | R/R/N | Customer effect and timed action may warrant elevation above planned correction; **2**. Original candidate retained unchanged. |
| N-H7 / high / 2 | Pair is Observation/observation, Strength/strength, or Opportunity/opportunity AND D2-P AND D3-T AND D5-P. | R/R/R | Three independently evidenced business conditions may warrant elevated intervention without a type default; **3**, one per pair. Document 42 candidate retained unchanged. |
| B-M1 / medium / 3 | Clear deficiency AND D2-A AND D3-A AND D5-A. | R/R/R | A corrective-action need with three affirmative scoped reviews may warrant planned intervention; **1**. Original candidate retained unchanged. |
| G-L1 / low / 4 | Pair is Deficiency/limited weakness, Observation/observation, Strength/strength, or Opportunity/opportunity AND D2-A AND D3-A AND D5-A. | R/R/R | Lower intervention only after three evidence-backed scoped reviews in these explicitly named classes; **4**. Merges B-L1/B-L2; no type-only default. |

The predicates do not claim that D2-P measures customer harm magnitude, that D3-T makes every deadline critical, or that D5 draft labels have different effects. `critical/high/medium/low` are priority outputs, not renamed severity, risk, confidence, or recommendation classes. The four proposed levels are represented, but a large valid domain deliberately has no emitting row.

## 7. Assertion requirements

Select eligible rows from the validated finding/consequence pair **before** inspecting missing business claims. Evaluate each eligible Boolean predicate with `TRUE`, `FALSE`, or `PENDING_REQUIRED_EVIDENCE`. A valid contrary atom makes a conjunction false, so its other atoms are `NOT_REQUIRED_BY_RULE`. For an `OR`, one true branch proves the row; otherwise all branches must be false to exclude it. A still-possible branch lacking an atom is pending. This is noncircular and never uses missing evidence as a negative fact.

The Section 6 R/N entries are rule-local. B-C1 needs D3/D5; G-H1 needs D2/D3; B-H3 needs D2/D3; N-H7, B-M1, and G-L1 need all three; G-H2 needs the drivers of a proving branch, or enough valid contrary facts to exclude every branch. A material-breach G-H1 candidate with D3-T cannot emit until B-C1 is resolved, requiring D5; D3-U itself excludes B-C1, so D5 is not required by that path. If B-C1 is true, D2 is not needed to emit critical. A supplied assertion is validated even if no eventual row needs it. `NOT_REQUIRED_BY_RULE` is a dependency description, never `NOT_APPLICABLE`.

When all eligible rows are conclusively false, `PRIORITY_NOT_DETERMINED` requires a recorded rule-exclusion trace and review obligation. “Complete” for this disposition means enough valid evidence to exclude **every** eligible emitting row; it need not mean a blanket three-assertion collection. The 84-tuple ledger happens to provide all three. If a row remains potentially true but its required claim is absent, return `BLOCKED_REQUIRED_EVIDENCE`; do not emit a lower level or PND.

## 8. Non-emitting outcome policy

These are **proposed logical outcome names**, except for the already approved D7 no-finding treatment. They are not fifth priority levels and are not current producer contract fields.

| Outcome | Exact condition | Temporary or terminal treatment |
| --- | --- | --- |
| `NO_FINDINGS_MONITOR` | Exact approved D7 case: empty complete finding set, `minimal-informational` risk, sole null-linked `monitor` recommendation with approved no-findings decision ID/table version. | Approved separate no-finding *meaning*; this label and future representation remain proposed. No four-level priority. |
| `REJECTED_INVALID_ASSERTION` | Any supplied D2/D3/D5 assertion fails structure, binding, authority/scope, evidence, revision/currentness, version, duplicate, or contradiction checks. | Reject the submission. Repair invalid records before any D8 decision. |
| `BLOCKED_REQUIRED_EVIDENCE` | A potentially matching eligible row requires a missing or unresolved authoritative D2/D3/D5 claim. | Temporary data/evidence block; obtain authorized evidence, then reevaluate. |
| `PRIORITY_NOT_DETERMINED` | Valid governed context and sufficient evaluated assertions conclusively exclude every eligible emitting row; no four-level rule matches. | Proposed review-required non-emitting disposition. Record pair, valid assertions, excluded rule IDs, reason, rule version, and methodology review owner/reference. It is not a completed priority assignment; review for an explicit future business rule or a separately approved terminal scope decision. |

The approved insufficient-confidence gate separately blocks finding-scoped priority with its own reason; it is not evidence of low priority or a D2/D3/D5 missing-claim result. Unknown required information never becomes scoped absence. A source or authority failure is not PND. Invalid submissions reject before D7 or rule evaluation. No priority is published from a blocked, rejected, or PND case.

## 9. Deterministic precedence

1. Validate structure, versions, finding/recommendation/snapshot identity, client business authority and approval scope, evidence provenance and currentness, and all supplied assertions; reject invalid or conflicting claims atomically.
2. Apply the exact approved D7 no-findings special meaning; malformed null-linked cases reject.
3. Apply the approved insufficient-confidence gate for finding-scoped recommendations; other supported confidence classes remain context.
4. Select candidate rows solely from the governed pair. Validate severity-pair consistency and assessment risk as separate context.
5. Resolve potentially applicable candidates in `critical → high → medium → low` order. At each level, request only assertions needed by still-possible rows. A higher pending row blocks any lower emission.
6. Before emitting a level, resolve every eligible peer at that level so all true same-level IDs can be recorded in deterministic ascending order (F41-C). A pending peer blocks final emission.
7. If all eligible rows are false with sufficient valid evidence, return proposed `PRIORITY_NOT_DETERMINED` and its review trace. No default low, numerical tie-break, assessment-risk modifier, or recommendation-order shortcut exists.

Different-level matches retain their evidence trace; the highest true level wins only after validation and peer resolution. For example, material `(P,T,P)` matches B-C1 and G-H1 but emits critical. Risk/severity disagreement preserves both governed classifications and never repairs either. Dependency conflicts reject; they are not resolved by array order or an LLM.

## 10. Reconciliation of 11 candidates

| Document 42 candidate | Disposition in this proposal | Exact rationale |
| --- | --- | --- |
| B-C1 | RETAIN UNCHANGED | Same critical predicate and two matching tuples. |
| B-H1 | GENERALIZE into G-H1 | Timed or untimed documented action with customer effect; preserves B-H1's tuples. |
| B-H2 | GENERALIZE into G-H2 | Same customer/untimed-action branch, with two additional customer/timed-action tuples. |
| B-H3 | RETAIN UNCHANGED | Clear deficiency plus customer effect and timed action. |
| B-M1 | RETAIN UNCHANGED | Three scoped absences for clear deficiency. |
| B-L1 | MERGE into G-L1 | Same low predicate retained for limited weakness. |
| B-L2 | MERGE into G-L1 | Same low predicate retained for each named non-deficiency pair. |
| N-H4 | MERGE into G-H1 | Customer/timed-action branch covers the original D5-A case; B-C1 still has higher precedence when D5-P. |
| N-H5 | MERGE into G-H2 | Customer/dependency branch covers its no-action case. |
| N-H6 | MERGE into G-H2 | Timed-action/dependency branch covers its no-customer case. |
| N-H7 | RETAIN UNCHANGED | Three-positive non-deficiency predicate remains narrow. |

“Generalize” and “merge” are proposed replacements, not an approval or runtime migration. No original candidate is silently discarded. Neither G-H1 nor G-H2 creates an automatic one-signal high rule.

## 11. Consolidated decision table

The seven rows below are the **entire proposed emitting table**. Every ID is unapproved. All require a valid governed pair, exact recommendation instance/snapshot/finding link, supported severity/risk/confidence provenance, and authorized current evidence for each named assertion. `R` is `REQUIRED_BY_RULE`; `N` is `NOT_REQUIRED_BY_RULE`. G-H2's alternative branches have conditional R values as detailed in Section 7. All rows reject invalid supplied claims and block on unresolved required claims. Section 9 supplies level order and same-level conflict policy.

| ID / status | Priority | Exact predicate / eligible class | D2 | D3 | D5 | Evidence basis / precedence | Matching complete tuples |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B-C1 / unchanged candidate | critical | Material breach ∧ T ∧ D5-P; Deficiency. | N | R | R | Timed action source and directed target; first level. | 2 |
| G-H1 / proposed generalization | high | Material breach ∧ D2-P ∧ (T ∨ U); Deficiency. | R | R | N locally; R for C1 exclusion if T. | Customer evidence and documented action; C1 wins on overlap. | 4, of which 3 emit high |
| G-H2 / proposed generalization | high | Significant gap ∧ ((D2-P ∧ (T ∨ U)) ∨ (D2-P ∧ D5-P) ∨ (T ∧ D5-P)); Deficiency. | R or N by true branch | R or N by true branch | R or N by true branch | At least one listed evidenced business combination; same-level ordering applies. | 6 |
| B-H3 / unchanged candidate | high | Clear deficiency ∧ D2-P ∧ T; Deficiency. | R | R | N | Customer effect plus timed action; no severity-only high. | 2 |
| N-H7 / unchanged candidate | high | Non-deficiency governed pair ∧ D2-P ∧ T ∧ D5-P. | R | R | R | Three independent evidenced conditions; no type-only high. | 3 |
| B-M1 / unchanged candidate | medium | Clear deficiency ∧ D2-A ∧ D3-A ∧ D5-A; Deficiency. | R | R | R | Three affirmative scoped reviews; higher B-H3 false. | 1 |
| G-L1 / proposed merge | low | Named limited-weakness or non-deficiency pair ∧ D2-A ∧ D3-A ∧ D5-A. | R | R | R | Three affirmative scoped reviews; higher N-H7 false for non-deficiency. | 4 |

The table is a proposed methodology, not a producer contract. The D2/D3/D5 abbreviations in the predicate column refer to the exact approved assertion meanings and evidence conditions, never field-name inference.

## 12. Coverage counts and complete tuple ledger

Each column is a **complete** `(D2,D3,D5)` tuple: `P/A` = D2-E1/E2; `T/U/A` = D3-E1/E2/E3; final `P/A` = D5-E1/E2. Every row lists all pair-eligible candidate IDs in Section 7; every cell below identifies the matching ID or `PND` for proposed `PRIORITY_NOT_DETERMINED`. `C+H1` means both B-C1 and G-H1 match, with critical emitted by precedence. Thus each cell has known candidate eligibility, fully supplied rule evidence, matched IDs, and a disposition. No cell is invalid or evidence-blocked because this ledger deliberately contains only complete valid tuples with eligible confidence.

| Governed pair / eligible IDs | PTP | PTA | PUP | PUA | PAP | PAA | ATP | ATA | AUP | AUA | AAP | AAA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Material / B-C1,G-H1 | C+H1 | H1 | H1 | H1 | PND | PND | C | PND | PND | PND | PND | PND |
| Significant / G-H2 | H2 | H2 | H2 | H2 | H2 | PND | H2 | PND | PND | PND | PND | PND |
| Clear / B-H3,B-M1 | H3 | H3 | PND | PND | PND | PND | PND | PND | PND | PND | PND | M1 |
| Limited / G-L1 | PND | PND | PND | PND | PND | PND | PND | PND | PND | PND | PND | L1 |
| Observation / N-H7,G-L1 | H7 | PND | PND | PND | PND | PND | PND | PND | PND | PND | PND | L1 |
| Strength / N-H7,G-L1 | H7 | PND | PND | PND | PND | PND | PND | PND | PND | PND | PND | L1 |
| Opportunity / N-H7,G-L1 | H7 | PND | PND | PND | PND | PND | PND | PND | PND | PND | PND | L1 |

Ledger code mapping: `C` = B-C1/critical; `H1` = G-H1/high; `H2` = G-H2/high; `H3` = B-H3/high; `H7` = N-H7/high; `M1` = B-M1/medium; `L1` = G-L1/low. `PND` has **no** emitting rule match or priority. Candidate eligibility is by the governed pair, independent of assertion presence. In a real incomplete case, Section 7's short-circuit proof determines which assertions are required; this complete ledger does not create blanket requirements.

| Outcome in the 84 complete valid tuples | Count | Scope |
| --- | ---: | --- |
| Critical | 2 | B-C1. |
| High | 14 | G-H1 emits 3, G-H2 emits 6, B-H3 emits 2, N-H7 emits 3. |
| Medium | 1 | B-M1. |
| Low | 4 | G-L1. |
| `BLOCKED_REQUIRED_EVIDENCE` | 0 | Missing evidence is outside this complete tuple projection. |
| `REJECTED_INVALID_ASSERTION` | 0 | Invalid claims are outside this valid tuple projection. |
| `PRIORITY_NOT_DETERMINED` | 63 | Valid complete tuples with no proposed emitting match. |
| Other approved special outcome | 0 | D7 no findings is outside the seven-pair projection. |
| **Total** | **84** | **21 proposed emissions + 63 proposed non-emissions.** |

These are proposed **methodology coverage** counts, not actual Assessment Service outputs. The D7 monitor, invalid assertions, missing evidence, and insufficient confidence are separate branches, not additional members of the 84. No substantive priority is claimed for the 63 PND tuples.

## 13. Synthetic scenario matrix

All examples are non-executable paper cases. Unless otherwise stated, snapshot/recommendation binding, client approval, evidence, risk/severity provenance, and one of the four eligible confidence classes are valid. `R` lists assertions required by still-possible rules; supplied but unneeded assertions still validate. Emissions and PND depend on founder approval of the corresponding proposed rows/policy.

| ID | Synthetic inputs; eligible IDs | R | Proposed outcome and business reason | Approval dependency |
| --- | --- | --- | --- | --- |
| S01 | Material `(A,T,P)`; B-C1,G-H1. | D3,D5 | Critical via B-C1; timed action and directed relation. | B-C1. |
| S02 | Material `(P,U,A)`; B-C1,G-H1. | D2,D3 | High via G-H1; D3-U excludes critical. | G-H1. |
| S03 | Clear `(A,A,A)`; B-H3,B-M1. | D2,D3,D5 | Medium via B-M1; three scoped absences. | B-M1. |
| S04 | Limited `(A,A,A)`; G-L1. | D2,D3,D5 | Low via G-L1; explicit reviewed evidence. | G-L1. |
| S05 | Significant `(P,A,A)`; G-H2. | D2,D3,D5 supplied | PND; customer effect alone does not prove an H2 branch. | F43-PND. |
| S06 | Significant `(A,T,A)`; G-H2. | D2,D3,D5 supplied | PND; timed action alone has no high rule. | F43-PND. |
| S07 | Significant `(A,A,P)`; G-H2. | D2,D3,D5 supplied | PND; directed relation alone has no high rule. | F43-PND. |
| S08 | Significant `(P,T,P)`; G-H2. | D2,D3; D5 supplied | High; customer and timed action prove a branch, relation also supports another. | G-H2. |
| S09 | Significant `(P,T,A)`; G-H2. | D2,D3 | High; customer and timed action without dependency. | G-H2. |
| S10 | Significant `(P,A,P)`; G-H2. | D2,D5; D3 supplied | High; customer plus directed relation, scoped no action. | G-H2. |
| S11 | Significant `(A,T,P)`; G-H2. | D3,D5; D2 supplied | High; timed action plus directed relation, scoped no customer effect. | G-H2. |
| S12 | Material `(P,T,P)`; B-C1,G-H1. | D3,D5; D2 supplied | Critical; both rules match, higher level wins. | B-C1/G-H1. |
| S13 | Material `(P,T,A)`; B-C1,G-H1. | D2,D3,D5 | High; D5-A conclusively excludes critical. | G-H1. |
| S14 | Material D3-T,D5-P,D2 missing. | D3,D5 | Critical; D2 is not required after B-C1 true. | B-C1. |
| S15 | Material D2-P,D3-T,D5 missing. | D2,D3,D5 for critical exclusion | Block; potential B-C1 outranks true G-H1. | F41-D, B-C1. |
| S16 | Significant D2-P,D3 missing,D5-A. | D2,D3 | Block; G-H2 remains possible, missing is not D3-A. | G-H2. |
| S17 | Clear D2-A,D3-A,D5 missing. | D2,D3,D5 | Block B-M1; never medium from an absent review. | B-M1. |
| S18 | Significant D2-P,D5-P,D3 missing. | D2,D5 | High; customer/dependency branch true without a blanket D3 requirement. | G-H2. |
| S19 | Material D2 missing,D3-A,D5 missing. | D3 | PND with all eligible rows false; no blanket D2/D5 assertion for this disposition. | F43-PND. |
| S20 | Non-deficiency `(P,T,P)` for Observation; N-H7,G-L1. | D2,D3,D5 | High by N-H7, never by type alone. | N-H7. |
| S21 | Same tuple for Strength. | D2,D3,D5 | High by N-H7 only with real approved source evidence. | N-H7. |
| S22 | Same tuple for Opportunity. | D2,D3,D5 | High by N-H7, not from opportunity label. | N-H7. |
| S23 | Non-deficiency `(A,A,A)`. | D2,D3,D5 | Low by G-L1 after three scoped reviews. | G-L1. |
| S24 | Opportunity `(P,A,A)`. | D2,D3; D5 supplied | PND; positive customer signal excludes G-L1, and affirmed no action excludes N-H7. | F43-PND. |
| S25 | Any finding with `insufficient-confidence`; assertions valid. | Validate supplied | Block finding-scoped assignment; no lower priority. | F38-D6 already approved. |
| S26 | Complete G-H2 inputs plus invalid supplied D5 target. | Validate D2,D3,D5 | Reject invalid assertion even if another H2 branch needs no D5. | Document 37 approved. |
| S27 | Two contradictory active D2 values on one binding. | Validate both | Reject, not a selected winner or PND. | Document 37 approved. |
| S28 | Clear `(A,U,P)` with `elevated-risk` and valid severity. | D2,D3; D5 supplied | PND; risk context does not assign or modify priority. | F41-B approved; F43-PND proposed. |
| S29 | Future same-level overlapping high rows both true. | Per each rule | High with every matched high ID sorted; no primary ID invented. Current exact rows do not overlap. | F41-C already approved. |
| S30 | Valid complete material `(A,A,A)`. | D3 sufficient to exclude rows | PND; no emitting predicate matches despite complete evidence. | F43-PND. |
| S31 | Sole null-linked approved monitor, empty findings, minimal-informational risk. | No D2/D3/D5 | D7 separate no-finding outcome, no four-level level. | Approved D7 meaning; future representation proposed. |

## 14. Final founder decision register

No reapproval of Option B, F38, F41, or Documents 35/37/39 is requested. Each row below is a **new or still-unapproved decision**. Approving the direction alone does not approve these exact predicates.

| Decision ID / group | Exact proposed choice and recommendation | Rationale; material alternative | Approval consequence / rejection consequence |
| --- | --- | --- | --- |
| F43-C1 / emitting | Approve B-C1: material breach ∧ D3-T ∧ D5-P → critical. | Timed material blocker and directed work; alternative high. | Adds two critical tuples / leaves them without an approved emitting row. |
| F43-H1 / emitting | Approve G-H1: material breach ∧ D2-P ∧ (D3-T ∨ D3-U) → high, subject to B-C1 precedence. | Customer effect plus documented action; alternative retain B-H1/N-H4 separately. | Consolidates material high / leaves its three emitted-high tuples unresolved. |
| F43-H2 / emitting | Approve G-H2's exact three-branch significant-gap predicate → high. | Customer/action, customer/dependency, or timed-action/dependency; alternative retain narrower B-H2/N-H5/N-H6. | Covers six tuples including two new timed/customer cases / those two revert to PND and other former candidates need separate approval. |
| F43-H3 / emitting | Approve B-H3: clear deficiency ∧ D2-P ∧ D3-T → high. | Customer plus timed action; alternative no level absent further magnitude evidence. | Covers two high tuples / leaves both unresolved. |
| F43-H7 / emitting | Approve N-H7: named non-deficiency pair ∧ D2-P ∧ D3-T ∧ D5-P → high. | Three independent conditions; alternative type-specific predicates. | Covers three high tuples / leaves them unresolved. |
| F43-M1 / emitting | Approve B-M1: clear deficiency ∧ D2-A ∧ D3-A ∧ D5-A → medium. | Reviewed no customer/action/relation with corrective need; alternative no emission. | Covers one medium tuple / leaves it unresolved. |
| F43-L1 / emitting | Approve G-L1: named limited/non-deficiency pair ∧ D2-A ∧ D3-A ∧ D5-A → low. | Reviewed absence across three drivers; alternative B-L1/B-L2 separate. | Covers four low tuples / leaves them unresolved. |
| F43-PND / non-emitting | Approve `PRIORITY_NOT_DETERMINED` only after all eligible emitting rows are conclusively false; record exclusion trace and require methodology review. | Valid facts can lack an approved level; alternative invent a default is unsupported. | Makes 63 complete classes explicitly non-emitting, **not completed priority assignments** / they remain unresolved without a governed disposition. |
| F43-STATUS / non-emitting | Adopt the proposed names `BLOCKED_REQUIRED_EVIDENCE` and `REJECTED_INVALID_ASSERTION` for approved fail-closed meanings; retain D7 meaning without presuming a production field. | Distinct data block, invalid rejection, and no-finding case; alternative names may differ by future versioned contract. | Clarifies logical outcomes / leaves representation undecided, not the existing fail-closed obligations. |
| F43-PREC / precedence detail | Resolve every eligible peer at the winning level before emission; retain all true peer IDs sorted, and block on a pending peer. | Required to satisfy F41-C's all-match provenance; alternative emitting early could omit a true rule ID. | Makes tie evidence deterministic / an alternate implementation must still preserve all IDs. |

## 15. Exact unresolved choices

The founder can decide these seven emitting predicates and the PND/representation policies in one bounded review. There is no claim that 63 PND tuples have substantive priority. If the founder instead requires a four-level value for any of those classes, the **specific missing business judgment** is the priority effect of the relevant customer-only, executive-action-only, dependency-only, or mixed positive/affirmed-absence pattern listed in Section 5. The existing assertions establish presence, action/timing, or relation, but not magnitude, deadline criticality, or dependent-work importance. No source fact can be manufactured to close that gap. Production client authority, real evidence/content verification, currentness, integrity, and a versioned output contract remain separate future admission prerequisites, not reasons to reopen approved methodology direction.

## 16. Implementation restrictions

This document changes no runtime behavior. No canonical assessment question, scoring, finding generation, recommendation selection, risk/confidence calculation, golden fixture, frozen v2/v3 contract, signed handoff, local synthetic validator, EIP, CEP, Platform, or AWS resource is modified. No client-specific assertion, production authority, priority assignment code, or downstream activation is authorized. Proposed outcome names are not claimed as existing producer fields. Stage 2 completion is not claimed.

## 17. Recommended next action

Ask the founder to approve or correct the seven exact emitting predicates, the review-required PND predicate, the logical status naming, and the winning-level peer-resolution detail in Section 14 as one decision set. If approved, separately assess a versioned methodology and contract increment before any local implementation. Do not implement from this proposal.

**Final status: PROPOSED — FOUNDER APPROVAL REQUIRED.**
