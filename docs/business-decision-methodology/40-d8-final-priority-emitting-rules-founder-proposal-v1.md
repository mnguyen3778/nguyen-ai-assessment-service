# D8 Final Priority Emitting Rules — Founder Proposal v1

**Status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**

## 1. Purpose and scope

This document proposes four narrow, evidence-backed D8 emitting rules. Each
mapping is a **NEW PROPOSED FOUNDER BUSINESS JUDGMENT**, not approved
methodology. The rules do not cover all valid findings or assertion tuples;
uncovered cases remain non-emitting rather than defaulting to a level. No
real client fact, priority output, or implementation is asserted here.

## 2. Approved methodology authority

The [priority methodology](06-recommendation-priority.md) establishes four
levels and qualitative drivers, not an executable mapping.
[Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md)
approves a recommendation-linked assertion source model and separate client
business authority. [Document 37](37-founder-priority-applicability-approval-v1.md)
approves D2/D3/D5 evaluated and fail-closed meanings, with **no
`NOT_APPLICABLE` branch** in v1.
[Document 39](39-founder-final-priority-direction-approval-v1.md) approves
F38-D1/R1/R2/D3/D4/D5/D6/D7 direction: consequence context without an impact
grade; rule-specific assertion requirements; validation of every supplied
assertion; separate severity and risk; no automatic urgency/dependency effect;
confidence context with an insufficient-confidence block; and a separate
no-finding outcome. None approves an emitting D8 rule.

## 3. Exact producer input inventory

The [governed input model](../../src/assessment/governed_assessment_input.py),
[decision runtime](../../src/assessment/governed_decision_runtime.py),
[v3 contract](../architecture/business-decision-package-contract-v3.md),
and [golden regressions](../../tests/test_golden_fixture_regression.py)
establish these current fields. A real D2/D3/D5 assertion is **not** a
current production field.

| Input | Existing vocabulary, authority, provenance and availability | Limit for D8 |
| --- | --- | --- |
| Finding `findingType` / `businessConsequenceBasis` | Seven governed pairs: Deficiency with `material current breach`, `significant gap`, `clear deficiency`, `limited weakness`; Observation/`observation`; Strength/`strength`; Opportunity/`opportunity`. Finding ID and source references; available. | Consequence context, not a graded business-impact score. |
| Finding `severityClassification`, decision ID/version | `critical`, `high`, `medium`, `low`, `informational`; `severity-decision-table-set-v1`; finding-scoped, available. | Must remain distinct from priority. |
| `assessmentRisk.riskClassification`, decision ID/version | `critical-risk`, `elevated-risk`, `moderate-risk`, `low-risk`, `minimal-informational`; `risk-decision-table-set-v1`; assessment-wide, available. | Cannot become finding-specific exposure without an approved rule. |
| `confidence.confidenceClassification`, decision ID/version | `very-high-confidence`, `high-confidence`, `moderate-confidence`, `low-confidence`, `insufficient-confidence`; `confidence-decision-table-set-v1`; assessment-wide, available. | Four values are context; insufficient blocks finding-scoped priority under Document 39. |
| Recommendation `findingId`, decision ID/version, classification | `recommendation-decision-table-set-v1`; `immediate-action`, `priority-action`, `planned-improvement`, `best-practice`, `monitor`; available. | Bind exact snapshot, finding, rule ID/version. Rule ID alone can repeat. Class/order are not priority. |
| Finding source references / evidence profile | Governed references and `Basic`, `Adequate`, `Strong` quality, optional authenticity/traceability limitation; available. | References do not prove D2/D3/D5 client content or approval. |
| D2/D3/D5 assertions | Approved meanings and proposed separately governed source model. | No real client facts, approvers, content/currentness verifier, or production admission exist. |

Existing v2/v3 shapes and signed handoffs remain frozen.

## 4. Priority business definitions

Provisional descriptions: `critical` means highest intervention order;
`high` elevated intervention; `medium` planned corrective action; and `low`
lower intervention. They are distinct from finding severity, assessment risk,
confidence, readiness, and recommendation classification. The row predicates
below, not these descriptions, would make priority testable if approved.

## 5. Critical emitting predicate

**D8-C1 — PROPOSED FOUNDER BUSINESS CHOICE.** Emit `critical` only for a
bound `(Deficiency, material current breach)` finding with governed `critical`
severity **and** D2-E1 customer effect **and** D3-E1 documented time-bound
executive action **and** D5-E1 directed relation to distinct same-snapshot
work. All assertion evidence, approval, version, currentness, and binding
must validate. Assessment risk is independently validated context, not an
automatic modifier.

Proposed rationale: a material current breach with customer effect, a
time-bound executive action, and related work dependent on the recommendation
could warrant highest intervention; `high` would defer that combined
time-bound/material issue. No single fact proves `critical`, and no deadline
threshold is invented. Missing required claims block; invalid or conflicting
submitted claims reject. This judgment needs founder approval.

## 6. High emitting predicate

**D8-H1 — PROPOSED FOUNDER BUSINESS CHOICE.** Emit `high` only for bound
`(Deficiency, significant gap)` with governed `high` severity **and** D2-E1
customer effect **and** D3-E2 documented executive action without a
time-bound claim **and** D5-E1 directed same-snapshot relation. Validate all
source and authority evidence; retain assessment risk separately.

Proposed rationale: the combined gap, customer effect, executive action, and
dependency could warrant elevated intervention without C1's material-breach
and documented-timing conjunction. It is not a `high`-severity shortcut.
Missing required claims block; invalid or conflicting claims reject. Founder
approval is required.

## 7. Medium emitting predicate

**D8-M1 — PROPOSED FOUNDER BUSINESS CHOICE.** Emit `medium` only for bound
`(Deficiency, clear deficiency)` with governed `medium` severity **and**
D2-E2 reviewed no customer effect **and** D3-E3 reviewed no executive action
**and** D5-E2 reviewed no dependency. Each absence has an explicit approved
scope and is `EVALUATED`, never `NOT_APPLICABLE`. Validate risk separately.

Proposed rationale: a clear deficiency merits planned correction when these
three business dimensions were affirmatively reviewed within scope. Absence
of urgency alone cannot establish `medium`. Missing reviews block;
unsupported or contradictory reviews reject. Founder approval is required.

## 8. Low emitting predicate

**D8-L1 — PROPOSED FOUNDER BUSINESS CHOICE.** Emit `low` only for bound
`(Deficiency, limited weakness)` with governed `low` severity **and**
D2-E2, D3-E3, and D5-E2 approved scoped affirmative-absence reviews.
Validate risk, sources, authority, versions, currentness, and linkage.

Proposed rationale: a limited weakness with three evidenced scoped negative
findings could warrant lower intervention than a clear deficiency. This is
affirmative evidence, never a default for missing inputs or insufficient
confidence. It does not prove zero risk. Missing reviews block; invalid
reviews reject. Founder approval is required.

## 9. Assertion requirements

Candidate selection uses only the validated existing finding
`(findingType, businessConsequenceBasis)` pair, before inspecting assertions.
The four Deficiency pairs select C1/H1/M1/L1 respectively. Each selected
rule marks **D2, D3, and D5 `REQUIRED_BY_RULE`** to establish a match or safe
non-match; missing/unresolved claims invoke D2-B/D3-B/D5-B. Invalid supplied
claims invoke D2-I/D3-I/D5-I. For Observation, Strength, and Opportunity,
these four rows cannot match, so the drivers are `NOT_REQUIRED_BY_RULE`
*for this partial table*; those findings have no emitted priority. This is
not `NOT_APPLICABLE`. Any supplied assertion must still validate under
F38-R2. A future potentially higher row cannot be skipped because its
required evidence is missing. No blanket requirement is created.

## 10. Deterministic precedence

1. Validate complete producer snapshot, versions, finding/recommendation
   identity, every supplied assertion, business authority/approval scope,
   evidence provenance/content, revision/currentness, duplicate claims, and
   contradictions. Invalid submitted context rejects atomically.
2. Match the exact Document 39 no-findings special case; malformed null
   links reject. It produces no four-level priority.
3. For finding-scoped cases, `insufficient-confidence` blocks. The other
   four supported confidence classes remain context.
4. Select the candidate family by governed finding pair. If a selected row
   needs missing D2/D3/D5 evidence, block before any lower emission.
5. Match exact row values. The four finding-pair predicates are disjoint; no
   two can match one valid recommendation. Different recommendations may
   share a level without changing their stable existing order.
6. A valid tuple with no exact row match is unresolved and non-emitting.
   Future overlapping rows need founder-approved precedence; until then an
   ambiguous match rejects. No default-low, model decision, or partial
   publication is allowed.

Eventual output would need a stable decision ID/version, exact recommendation
link, matched upstream rule IDs/versions, assertion/evidence references, and
deterministic rationale. IDs here are proposal labels, not a supported table.

## 11. Conflict and missing-data policy

| Condition | Proposed handling |
| --- | --- |
| Malformed, stale, unauthorized, contradictory, duplicate, or wrongly linked supplied evidence | `INVALID`; reject complete evaluation, including an otherwise matching row. |
| Missing selected-row D2/D3/D5 claim | `BLOCKED_PENDING_DATA`; never skip the selected or potentially higher row. |
| Multiple valid rules match one recommendation | Impossible for these disjoint pairs. Future overlap rejects until exact founder precedence is approved. |
| Severity and assessment risk disagree | Preserve both; risk does not silently raise/lower these four proposed rows. |
| Customer effect, executive action, or dependency suggests a different level | Match only an exact row; otherwise unresolved. No averaging or implicit weight. |
| No row matches | Unresolved and non-emitting, never `low` by default. |

Blocked and unresolved states are not fifth priority levels.

## 12. Complete proposed decision table

This is the **complete inventory of four narrow proposed emitting rows and
their fail-closed branches, not a total mapping of all valid inputs**. Every
emitting row is a new proposed founder business choice. Required evidence is
the governed finding source plus current client-approved assertions bound to
the exact snapshot/recommendation; real authority and production admission
are unavailable.

| Rule / order / emitted level | Exact required producer predicate | D2 / D3 / D5 | Evidence and rationale | Missing / conflict; approval |
| --- | --- | --- | --- | --- |
| D8-C1 / 1 / `critical` | `(Deficiency, material current breach)`, `critical` severity, valid risk, non-insufficient confidence, D2-E1+D3-E1+D5-E1. | REQUIRED / REQUIRED / REQUIRED | Finding source; customer effect, timed action, directed relation; combined material/time-bound/dependency case. | Missing blocks; invalid rejects; **FOUNDER APPROVAL REQUIRED**. |
| D8-H1 / 2 / `high` | `(Deficiency, significant gap)`, `high` severity, valid risk/confidence, D2-E1+D3-E2+D5-E1. | REQUIRED / REQUIRED / REQUIRED | Finding source; customer effect, untimed executive action, relation; elevated intervention. | Missing blocks; invalid rejects; **FOUNDER APPROVAL REQUIRED**. |
| D8-M1 / 3 / `medium` | `(Deficiency, clear deficiency)`, `medium` severity, valid risk/confidence, D2-E2+D3-E3+D5-E2. | REQUIRED / REQUIRED / REQUIRED | Finding source and three scoped affirmative reviews; planned correction. | Missing blocks; invalid rejects; **FOUNDER APPROVAL REQUIRED**. |
| D8-L1 / 4 / `low` | `(Deficiency, limited weakness)`, `low` severity, valid risk/confidence, D2-E2+D3-E3+D5-E2. | REQUIRED / REQUIRED / REQUIRED | Finding source and three scoped affirmative reviews; lower intervention. | Missing blocks; invalid rejects; **FOUNDER APPROVAL REQUIRED**. |
| D8-NF / before emitting / no level | Exact Document 39 empty-findings/null-monitor case. | NOT_REQUIRED_BY_RULE / same / same | Governed no-findings provenance; separate no-finding outcome. | Malformed rejects; D7 direction approved, representation/implementation separate. |
| D8-IC / before emitting / block | Finding-scoped `insufficient-confidence`. | Validate any supplied assertions. | Governed confidence ID/version. | Block, never low; D6 direction approved. |
| D8-MISS / before emitting / block | Selected row needs absent/unresolved required assertion. | Required by selected row. | Missing source recorded. | Block; F38-R1 approved. |
| D8-INVALID / first / reject | Any invalid producer context or supplied assertion. | Validate all supplied. | Rejection provenance. | Reject atomically; F38-R2 approved. |
| D8-NOMATCH / last / no level | Valid tuple matches none of C1/H1/M1/L1, including non-Deficiency findings. | No blanket requirement; validate supplied. | No founder-approved business mapping for this tuple. | Unresolved, non-emitting; coverage decision required. |

Severity is validated against its governed consequence pair, not used as a
standalone priority mapping. Assessment risk is validated and retained as
context; whether it should alter a row is a separate founder D8 judgment.

## 13. Synthetic scenario matrix

These are non-executable paper cases. “Would emit” means **only if** the
proposed D8 row is later approved and all real client evidence validates.

| ID | Synthetic inputs; candidates and evidence | Proposed result and rationale | Unapproved D8 choice? |
| --- | --- | --- | --- |
| S01 | Material breach, D2-E1, timed D3-E1, directed D5-E1; C1 needs all three claims. | Would emit `critical` for combined material, customer, timed, dependency case. | Yes, C1. |
| S02 | Significant gap, D2-E1, untimed D3-E2, D5-E1; H1 needs all claims. | Would emit `high` for combined elevated case. | Yes, H1. |
| S03 | Clear deficiency, D2-E2/D3-E3/D5-E2 reviewed absences; M1. | Would emit `medium` for planned correction. | Yes, M1. |
| S04 | Limited weakness, same three reviewed absences; L1. | Would emit `low` from affirmative evidence, not default. | Yes, L1. |
| S05 | Two proposed emitting rows appear to match one valid recommendation. | Impossible under disjoint finding pairs; future overlap rejects pending precedence. | Future row choice. |
| S06 | Material breach, D2-E1/D5-E1, missing D3 source; C1. | Block C1; no lower fallback. | Yes, C1. |
| S07 | Lower-like reviewed facts, but a future higher row could apply and its claim is unresolved. | Block until higher candidate ruled out; four current rows are disjoint. | Future coverage. |
| S08 | High-severity significant gap, D3-E3 reviewed no action, D2-E1/D5-E1; H1. | No match; high severity alone does not emit high. | Yes, H1/coverage. |
| S09 | Material breach and documented timed action, D2/D5 missing; C1. | Block; timing alone is not critical. | Yes, C1. |
| S10 | Customer impact present in complete H1 tuple. | Would emit high only under H1, not from D2 alone. | Yes, H1. |
| S11 | Customer impact affirmatively absent in complete M1 tuple. | Would emit medium; absence is evaluated, not NA. | Yes, M1. |
| S12 | Directed dependency in complete H1 tuple. | Would emit high; draft labels have no distinct effect. | Yes, H1. |
| S13 | Dependency affirmatively absent in complete L1 tuple. | Would emit low under L1; reviewed scope is evidence. | Yes, L1. |
| S14 | Any finding-scoped `insufficient-confidence` case. | Block before emission, never low. | No new level choice. |
| S15 | Invalid supplied D2 claim with otherwise valid H1 inputs. | Reject complete set even if a future row does not need D2. | No new level choice. |
| S16 | Positive and absence D3 claims conflict on one binding. | Reject; no array-order winner. | No new level choice. |
| S17 | Limited weakness/low severity, elevated assessment risk, complete L1 reviews. | Would emit low **only if** founder approves risk as non-modifying here; preserve both values. | Yes, risk policy. |
| S18 | Empty findings, minimal-informational risk, sole null-linked monitor. | Separate approved D7-direction outcome, no four-level priority. | No new level choice. |
| S19 | Observation finding, valid context, no assertions. | No row matches; unresolved, never default low. | Yes, coverage. |

## 14. Founder decision register

Approval of these narrow rows would still leave other valid tuples unmapped.
All recommendations below are **PROPOSED**, not approvals.

| Decision ID; status | Exact proposed rule and evidence basis | Recommendation, rationale, material alternative | Consequence and specific blocker |
| --- | --- | --- | --- |
| F40-C1; READY FOR FOUNDER APPROVAL | D8-C1 exact material-breach+D2-E1+D3-E1+D5-E1; governed finding pair and future client-approved assertions. | Recommend critical for combined material breach, customer effect, timed action, dependency; alternative high leaves that combined case less urgent. | One row if approved; real client evidence/authority still absent. |
| F40-H1; READY FOR FOUNDER APPROVAL | D8-H1 exact significant-gap+D2-E1+D3-E2+D5-E1. | Recommend high for evidenced customer, executive, and dependency intervention without C1 timing/material pair; alternative critical ignores C1 distinction. | One row if approved; other high combinations unmapped. |
| F40-M1; READY FOR FOUNDER APPROVAL | D8-M1 exact clear-deficiency+three scoped absence reviews. | Recommend medium for planned correction; alternative missing-evidence-to-medium violates Document 37. | One row if approved; needs three real approved reviews. |
| F40-L1; READY FOR FOUNDER APPROVAL | D8-L1 exact limited-weakness+three scoped absence reviews. | Recommend low for evidenced lower intervention; alternative default low is unsupported. | One row if approved; needs three real approved reviews. |
| F40-RISK; REQUIRES BUSINESS CHOICE | Validate assessment risk, but do not let it change these four rows; finding severity must match consequence pair. | Recommend contextual risk because assessment-wide risk is not finding exposure; alternative exact risk-specific rows need rationale. | Founder choice needed for S17 and mixed severity/risk cases. |
| F40-COVER; REQUIRES BUSINESS CHOICE | All other valid tuples, including Observation/Strength/Opportunity, stay non-emitting. | Recommend exact additional rows or expressly approved bounded non-emitting domain; no severity/classification default. | No complete methodology until coverage is decided. |
| F40-CONFLICT; REQUIRES BUSINESS CHOICE | Current four pairs disjoint; any future overlap requires precedence. | Recommend reject ambiguity until founder defines precedence; alternative highest-label-wins is unapproved. | Complete future table needs overlap/tie policy. |

## 15. Explicit unresolved choices

The founder must decide whether the four conjunctions warrant their levels,
whether assessment-wide risk may alter them, and how to handle other valid
Deficiency combinations and Observation/Strength/Opportunity findings.
Future overlapping rules need exact precedence. A row needing graded
business impact requires a separately approved vocabulary and evidence;
Document 39 approved no such grade. Real client assertions, approvers,
content verification, currentness, and production integrity are unavailable.
These are business/source dependencies, not defects in the local validator.

## 16. Non-approvals and restrictions

No proposed D8 row is approved or implemented. No client fact, approver,
impact grade, numeric weight, deadline threshold, D2/D3/D5 `NOT_APPLICABLE`
branch, blanket assertion requirement, automatic severity/risk/urgency/
dependency mapping, or low fallback is created. No canonical question,
scoring, finding, recommendation, risk, confidence, golden fixture, signed
handoff, frozen v2/v3 contract, EIP, CEP, Platform, or AWS behavior changes.
The local synthetic validator remains closed. Stage 2 remains incomplete.

## 17. Recommended next bounded action

Founder review should decide F40-C1/H1/M1/L1 and F40-RISK, then make exact
coverage and overlap decisions for F40-COVER and F40-CONFLICT. A complete
versioned D8 table and real authorized assertion sources are prerequisites
to any implementation. Do not implement this partial proposal.

**Final status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**
