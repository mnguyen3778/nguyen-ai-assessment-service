# Final Recommendation Priority Addendum and Decision Table — Draft v1

**Status: PROPOSED — NOT AUTHORITATIVE.** Founder review is required before
any rule in this document becomes methodology, configuration, executable code,
contract content, or downstream output. Proposed table identifier:
`final-recommendation-priority-decision-tables-draft-v1`. This identifier is
for review only; it is not an approved decision-table version.

## 1. Scope and exclusions

This draft concerns one final priority decision for each existing governed
recommendation. The Assessment Service would own that decision. It does not
change recommendation selection, the canonical 48 questions, scoring, finding
severity, risk, confidence, executive summaries, recommendation text, or
historical package behavior. It neither authorizes implementation nor activates
production or downstream publication. All new business rules below are
**PROPOSED — NOT AUTHORITATIVE**.

## 2. Approved baseline and current foundation

The [priority methodology](06-recommendation-priority.md) names four levels:
`critical`, `high`, `medium`, and `low`, and six drivers: business impact,
customer impact, executive urgency, risk severity, dependency role, and
confidence level. Its qualitative descriptions, same-priority ordering
principles, and traceability requirements do not provide a complete executable
assignment rule. The configured rank order is catalog metadata, not a formula.

The [approved recommendation decision tables](25-recommendation-decision-tables-v1.md)
emit `immediate-action`, `priority-action`, `planned-improvement`,
`best-practice`, or `monitor` under `recommendation-decision-table-set-v1` and
`business-decision-methodology-v1`. Their eight emitting decision identifiers
include the no-findings `recommendation-v1-no-findings-monitor` rule. Section 8
expressly distinguishes stable recommendation order from priority. Neither a
recommendation label nor an array position determines final priority.

Finding severity has its own approved values: `critical`, `high`, `medium`,
`low`, and `informational`. It is a governed input, not an approved priority
mapping. The [methodology completeness audit](../architecture/executive-methodology-completeness-audit-v1.md)
classifies priority factor formulas and final assignment as
`METHODOLOGY_PENDING`. The current [priority foundation](../../src/assessment/recommendation_priority.py)
records catalogs and source references, marks all six factors `not-evaluated`,
and emits no final assignment. [Configuration](../../src/assessment/methodology_config.py)
holds the level and factor catalogs. Existing
[priority tests](../../tests/test_recommendation_priority.py) assert those
foundation semantics. [Golden fixtures](27-golden-fixtures-v1.md) and their
[payloads](28-golden-fixture-payloads-v1.md) cover governed upstream outputs;
they establish no final-priority expected value.

The producer already has recommendation decision identifier, decision-table
version, and `findingId`; each finding carries type, severity and its decision
identifier/version, dimension links, consequence basis, and evidence source
references. Assessment risk and confidence have governed classifications and
decision provenance. These values are stable within their versioned contracts.
The presence of a source reference does not establish business or customer
impact, executive urgency, or dependency role.

## 3. Six-driver evaluation proposal

**PROPOSED — NOT AUTHORITATIVE.** The first-pass status vocabulary for each driver is
`evaluated`, `not-applicable`, or `blocked-pending-data`. `not-applicable` is
valid only where a founder-approved rule explicitly permits it. Missing or
invalid required data never becomes zero impact or a low priority. The table
defines precise source and validation handling without claiming that absent
business judgments can be inferred.

**Supersession note:** This first-pass state vocabulary and the D2, D3, and D5
rows in the following table assumed that each driver would be required for
every finding-scoped recommendation. That assumption is superseded by the later **FOUNDER
CONDITIONAL APPLICABILITY — PROPOSED REFINEMENT**. Its state and applicability
rules control this draft. The first-pass rows remain as historical context.

| Driver | Exact existing source and available values | Proposed applicability and evaluation | Missing, inapplicable, unsupported; provenance | Additional founder decision |
| --- | --- | --- | --- | --- |
| Business impact | Finding `businessConsequenceBasis`, primary/related dimensions, and source references exist. No governed recommendation-level business-impact category or quantified revenue/cost/strategy effect exists. | For a finding-scoped recommendation, preserve the exact governed consequence basis as context. A graded impact value or translation from that basis is **FOUNDER DECISION REQUIRED**. Do not parse free text or infer impact from severity. | Missing or invalid consequence basis: reject; valid basis without approved impact translation: blocked. Record finding and evidence references if later evaluated. | D1: define whether existing consequence categories suffice for a bounded impact rule. |
| Customer impact | Finding dimensions and evidence references exist. No governed customer-impact classification or reliable customer-facing flag exists. | Require explicit governed customer-impact evidence for finding scope. Allowed values and test for no customer impact are **FOUNDER DECISION REQUIRED**. A dimension name is not a customer-impact proxy. | Missing: `blocked-pending-data`; approved non-customer applicability may yield `not-applicable` only after D2. Unknown value/type: invalid. Preserve exact evidence references. | D2: define values, applicability and source. |
| Executive urgency | Governed risk and recommendation classification exist, but no explicit unresolved executive-decision, sponsorship, funding, or timing indicator exists. | Require an approved urgency input or an explicit approved derivation from governed fields. Both allowed values and derivation are **FOUNDER DECISION REQUIRED**. `immediate-action` alone is not an urgency value. | Missing: `blocked-pending-data`; no default `not-applicable`. Unknown value/type: invalid. Record source decision IDs and evidence reference. | D3: define urgency evidence and rule. |
| Risk severity | Finding `severityClassification` and assessment `riskClassification` are governed and versioned. Allowed severity values are `critical`, `high`, `medium`, `low`, `informational`; risk values are `critical-risk`, `elevated-risk`, `moderate-risk`, `low-risk`, `minimal-informational`. | For finding scope, read the linked finding's severity and assessment risk as separate inputs. Whether either raises, caps, or leaves priority unchanged is **FOUNDER DECISION REQUIRED**. Do not equate either with a priority label. | Missing linked severity/risk: invalid governed context; no finding: applicability decision pending. Unknown category/type: invalid. Record both source rule IDs and versions. | D4: define their combined effect and any conflict precedence. |
| Dependency role | Related dimensions exist, but no governed “blocks/unlocks later work” relation or dependency classification exists. | Require explicit governed dependency evidence; a count of related dimensions does not prove a dependency. Allowed values and applicability are **FOUNDER DECISION REQUIRED**. | Missing: `blocked-pending-data`; approved absence may be `not-applicable` only after D5. Unknown value/type: invalid. Record relation and evidence references. | D5: define relation semantics, values, and source. |
| Confidence level | Governed `confidenceClassification` and its rule ID/version exist: `very-high-confidence`, `high-confidence`, `moderate-confidence`, `low-confidence`, `insufficient-confidence`. Foundation confidence factors are separate. | Read the governed classification for the complete assessment. Whether low or insufficient confidence redirects, caps, blocks, or changes a recommendation's priority is **FOUNDER DECISION REQUIRED**. It cannot silently change the already approved recommendation. | Missing/invalid confidence: invalid governed context. `not-applicable` is not proposed. Record confidence rule ID/version and any approved adjustment rule. | D6: define all five effects, especially insufficient confidence. |

No new assessment question or client fact is proposed. If D1, D2, D3, or D5
requires data absent from the existing governed producer inputs, founder review
must choose a governed source and its applicability. For D2, D3, and D5,
applicability itself remains unresolved until an approved predicate exists;
the later conditional-applicability section supersedes any first-pass claim
that absence alone creates `blocked-pending-data` or `not-applicable`.

## 4. Proposed decision table and precedence

**PROPOSED — NOT AUTHORITATIVE.** This is a decision table with explicit
coverage gaps, not an implementation-ready mapping. Each row applies to one
recommendation and carries its own proposed rule identifier. Table rows are
evaluated in ascending order; a terminal rejection ends evaluation. Only an
approved emitting row could assign one of the four existing priority values.
The later conditional-applicability section supersedes rows 2 and 3 below
where they assume an approved D2, D3, or D5 applicability rule exists.

| Order / draft rule ID | Exact condition | Proposed result | Status |
| --- | --- | --- | --- |
| 0 `priority-draft-v1-invalid-context` | Recommendation ID/version is unsupported, finding link disagrees with the complete finding collection, or required severity/risk/confidence/version provenance is invalid. | Reject the complete priority evaluation; emit no partial assignments. | Proposed validation. |
| 1 `priority-draft-v1-no-findings` | Complete finding collection is empty and the sole recommendation is `recommendation-v1-no-findings-monitor` with `findingId: null`. | Option A proposes valid inapplicability, subject to **FOUNDER APPROVAL REQUIRED**. `monitor` does not imply `low`. | Proposed D7; see Option A refinement. |
| 2 `priority-draft-v1-missing-driver` | A driver required by the approved applicability policy is absent or `blocked-pending-data`. | No assignment; block evaluation pending governed data. | Proposed validation, dependent on D1–D6. |
| 3 `priority-draft-v1-unsupported-driver` | A supplied driver has a wrong type, unsupported category, contradictory provenance, or an unapproved `not-applicable` claim. | Reject; emit no assignment. | Proposed validation. |
| 4 `priority-draft-v1-insufficient-confidence` | Finding-scoped recommendation and confidence is `insufficient-confidence`. | Option A proposes blocked final assignment, subject to **FOUNDER APPROVAL REQUIRED**. | Proposed D6; see Option A refinement. |
| 5 `priority-draft-v1-critical` | Finding-scoped, complete approved driver tuple matching a founder-approved critical row. | `critical`, with row ID and rationale. Exact predicate **FOUNDER DECISION REQUIRED**. | Unresolved D8. |
| 6 `priority-draft-v1-high` | Finding-scoped, complete approved driver tuple matching a founder-approved high row, after higher-precedence rows. | `high`, with row ID and rationale. Exact predicate **FOUNDER DECISION REQUIRED**. | Unresolved D8. |
| 7 `priority-draft-v1-medium` | Finding-scoped, complete approved driver tuple matching a founder-approved medium row, after higher-precedence rows. | `medium`, with row ID and rationale. Exact predicate **FOUNDER DECISION REQUIRED**. | Unresolved D8. |
| 8 `priority-draft-v1-low` | Finding-scoped, complete approved driver tuple matching a founder-approved low row, after higher-precedence rows. | `low`, with row ID and rationale. Exact predicate **FOUNDER DECISION REQUIRED**. | Unresolved D8. |
| 9 `priority-draft-v1-no-match` | After a complete table is approved, a valid complete driver tuple matches no approved emitting row. | Reject; emit no arbitrary default. Before approval, Option A row 4 instead blocks assignment. | Proposed future validation. |

An approved table must replace every `FOUNDER DECISION REQUIRED` predicate with
exact allowed driver values, applicability conditions, and a total outcome for
each supported combination. Row order alone may not resolve overlapping
business rules: D8 must state which effect wins when drivers conflict. Equal
priority values on separate recommendations are permitted; existing
recommendation order remains stable and is not an assignment tie breaker.
Ambiguous matches at the same approved precedence, contradictory driver
claims, or absent matching rows fail closed. No severity-to-priority,
classification-to-priority, risk-to-priority, or numeric score conversion is
approved by this draft.

## 5. No findings and evaluation states

The approved no-findings recommendation remains one `monitor` item with null
`findingId`; the [v2 contract](../architecture/business-decision-package-contract-v2.md)
also specifies `minimal-informational` risk. Under the founder-selected Option A
direction, D7 proposes valid inapplicability for exactly this case, subject to
explicit methodology approval. It would have no priority classification and
would not create a fifth priority level. Until D7 is approved, no final
priority or governed inapplicability is asserted for it.

**PROPOSED — NOT AUTHORITATIVE** state semantics:

| State | Meaning | May carry a priority? |
| --- | --- | --- |
| Valid assignment | Exactly one approved emitting rule matches complete valid inputs. | Yes, one of four approved levels. |
| Valid inapplicability | An approved rule explicitly allows it, potentially for no findings. | No. |
| Blocked pending data | A required governed business input has no approved source or is absent. | No. |
| Invalid/unsupported | Malformed, contradictory, unversioned, unlinked, or unsupported input or rule state. | No; reject. |

Missing required inputs, wrong types, unsupported categories or versions,
invalid links, missing provenance, ambiguous matches, and no matches cannot
produce an assignment. This does not erase or alter the existing recommendation.

## 6. Minimum priority provenance proposal

**PROPOSED — NOT AUTHORITATIVE.** Each valid assignment should carry mandatory
`recommendationDecisionIdentifier` plus `findingId` (nullable only for the
approved no-findings item), `priorityClassification`,
`priorityDecisionIdentifier`, `priorityDecisionTableVersion`,
`methodologyVersion`, driver values and applicability states, governed source
references, and a deterministic rationale tied to the matched row. The
recommendation decision identifier is a stable rule link in current output;
it is not by itself a unique recommendation-instance ID when two findings
share a rule. The pair with `findingId` identifies a finding-scoped item.

Source question IDs, evidence categories, readiness dimensions, risk and
confidence adjustments, and business/customer/urgency rationales are required
by the [priority methodology](06-recommendation-priority.md#traceability-requirements)
where applicable. If a source does not exist, an assignment must not claim it.
The approved table must define whether a particular reference is conditionally
inapplicable and why. A validity or inapplicability record needs a decision ID
and version; a blocked or invalid evaluation may carry diagnostic references
internally but cannot masquerade as final priority. No free-form model rationale
is authoritative.

## 7. Contract options and compatibility

The [v2 contract](../architecture/business-decision-package-contract-v2.md)
has exactly four recommendation fields. The [v3 contract](../architecture/business-decision-package-contract-v3.md)
has exactly five, adding `recommendationActionText`; it forbids extra fields.
Neither `recommendationPriorityEvaluation` foundation metadata nor the
recommendation classification can serve as final priority.

| Option | Compatibility and assessment |
| --- | --- |
| Add priority fields to v2 or v3 | Rejected: changes frozen exact field shapes and historical validation. |
| Separate versioned, producer-signed priority projection | Possible if it binds exactly to a recommendation and source snapshot, has strict validation and version provenance, and cannot be recomputed by EIP. It adds a second linked artifact and verification path. |
| Explicit new producer package representation | Recommended for later contract design if final priority is part of governed conclusions. Version only the changed representation and its verification profile; retain existing assessment input and envelope identifiers unless a concrete compatibility need says otherwise. The next version number is not decided here. |

Historical v2 and v3 packages, defaults, golden fixtures, signatures,
canonicalization, and consumer interpretations remain unchanged. An explicit
new version must reject unsupported pairings and prevent silent downgrade.
Current local v3 work and its nonproduction boundary remain closed; this draft
does not reopen Stage 4G.6.

## 8. Deterministic test scenario matrix for a future authorized increment

Every expected final-priority behavior in this table is **PROPOSED — NOT
AUTHORITATIVE** unless marked as an existing baseline. `D1`–`D8` refer to the
founder decision register below. No executable test is added by this draft.

| Scenario | Input conditions | Expected output or rejection | Rule / evidence |
| --- | --- | --- | --- |
| P01–P04 | One complete finding-scoped tuple for each future critical, high, medium, low predicate. | Exact corresponding level only after D8 approval. | Draft rows 5–8; approved row, driver values, source IDs and rationale. |
| P05 | Business impact required, present/absent/inapplicable. | Evaluate only approved values; absent blocks; inapplicable only if D1 permits. | D1; linked finding and evidence reference. |
| P06 | Customer impact required, present/absent/inapplicable. | Same branch semantics under D2. | D2; customer-impact evidence. |
| P07 | Executive urgency required, present/absent. | Approved value or block. | D3; urgency source reference. |
| P08 | Finding severity and assessment risk each valid; then missing or conflicting. | Approved D4 effect; invalid governed context rejects. | D4; severity/risk rule IDs and versions. |
| P09 | Dependency relation present/absent/inapplicable. | Approved value; absent blocks unless D5 permits inapplicability. | D5; relation reference. |
| P10 | Each of five governed confidence classifications. | Exact D6 effect, including insufficient-confidence branch. | D6; confidence rule ID/version. |
| P11 | Two applicable approved rows or opposing driver effects. | D8 precedence result, or reject ambiguity if no precedence is approved. | D8; all matched rule IDs and driver evidence. |
| P12 | Two recommendations receive the same priority. | Both retain their assignment; existing order remains stable. | Existing recommendation IDs and ordering evidence. |
| P13 | Complete no-findings assessment and sole null-linked monitor. | Option A proposes valid inapplicability after D7 approval; never infer low. | Draft row 1; no-findings rule and complete collection. |
| P14 | Missing required driver, wrong type, unsupported category, or unsupported methodology/table version. | Block for approved absent data; otherwise reject; no partial output. | Draft rows 2–3; validation evidence. |
| P15 | Missing/duplicate/wrong `findingId`, wrong recommendation rule, or missing provenance. | Reject. | Draft row 0; finding/recommendation pair. |
| P16 | Before approval, a finding-scoped tuple has no emitting rule; after a complete table is approved, a valid tuple matches no row or same-precedence rows conflict. | Before approval, block assignment; after approval, reject no match or ambiguous match. | Option A row 4 and draft row 9; complete rule-match trace. |
| P17 | Same complete inputs and versions evaluated repeatedly. | Byte-stable priority output and rationale after approval. | All approved table rows and version binding. |
| P18 | Historical v2 and v3 golden packages. | Existing expected bytes and validation remain unchanged. | Existing golden fixtures and v2/v3 contract tests. |
| P19 | New signed producer priority representation passed to EIP. | EIP verifies and carries exact producer value, ID and version without recalculation or production publication. | Producer signature, version binding, EIP pass-through assertion. |

## 9. Founder decision register

Only these priority methodology decisions need explicit founder approval.
Approval of this draft as written would not resolve entries marked
`FOUNDER DECISION REQUIRED`.

| ID | Exact decision requested | Current status |
| --- | --- | --- |
| D1 | Define business-impact values, evidence source and applicability; approve or reject derivation from existing consequence basis. | FOUNDER DECISION REQUIRED |
| D2 | Define customer-impact values, authoritative evidence and conditions for inapplicability. | FOUNDER DECISION REQUIRED |
| D3 | Define executive-urgency values and authoritative input or explicit derivation. | FOUNDER DECISION REQUIRED |
| D4 | Define the distinct effect and conflict handling of finding severity and assessment risk on priority. | FOUNDER DECISION REQUIRED |
| D5 | Define dependency-role values, authoritative relation and inapplicability. | FOUNDER DECISION REQUIRED |
| D6 | Define the effect of all five confidence classes, including insufficient confidence, without silently rewriting recommendation decisions. | FOUNDER DECISION REQUIRED |
| D7 | Approve or reject proposed governed inapplicability for exactly the sole null-linked no-findings monitor recommendation. | FOUNDER DECISION REQUIRED |
| D8 | Approve exact, complete, mutually consistent four-level predicates and precedence for all supported driver tuples; specify ties and conflicts. | FOUNDER DECISION REQUIRED |

The priority level names, six driver names, upstream classifications and
decision identifiers, and existing no-findings recommendation are already
approved baseline facts. Selecting sources, driver semantics, final mapping,
or an inapplicability policy is new business methodology. Encoding approved
rules in configuration, implementing validation, choosing a compatible new
contract representation, and adding tests are subsequent technical work.

## 10. Implementation prerequisites and downstream boundary

Before implementation, the founder must approve D1–D8 as a complete,
version-bound table, including required inputs and traceability. The producer
must then have the governed inputs actually available; a required but absent
input blocks final assignment. Only a separately authorized increment may
implement producer evaluation, validation, versioned serialization, and tests.
EIP may then verify and pass through producer-issued priority without
recalculation. CEP may present authorized priority, and the AI Knowledge
Assistant may explain approved priority without assigning or changing it.
No LLM output, presentation normalization, website rule, or EIP calculation
becomes authoritative priority. No downstream production activation is
approved here.

## FOUNDER OPTION A — PROPOSED REFINEMENT

**Founder-selected direction: OPTION A — EXISTING GOVERNED DATA.** This selects
the source boundary for the proposal; it does not approve a priority formula.
Every rule in this section is **PROPOSED — NOT AUTHORITATIVE**. This section
refines D1–D8 above. Where it narrows an earlier open choice, the refinement is
the proposed choice for founder review. An approved priority assignment cannot
be emitted from the current Option A data for a finding-scoped recommendation
without further business decisions and, for some drivers, authoritative data.

### A. Existing governed input inventory

Values below are case-sensitive. Finding-level fields are producer-validated
under `nguyen-ai-executive-assessment-v2` and
`business-decision-methodology-v1`; output decisions carry their own approved
table versions. The [canonical input](../../src/assessment/governed_assessment_input.py),
[governed decision runtime](../../src/assessment/governed_decision_runtime.py),
and [approved runtime configuration](../../src/assessment/approved_methodology_runtime_config.py)
define these values. [Golden regression fixtures](../../tests/test_golden_fixture_regression.py)
exercise representative combinations, including no findings.

| Input and exact source | Allowed values / version or provenance | Scope and defensible meaning for priority |
| --- | --- | --- |
| `FindingInput.finding_id`; package `severityAssignedFindings[].findingId` | Nonempty, unique ID; canonical finding order; methodology v1. | Finding-specific stable link, not an impact judgment. |
| `FindingInput.finding_type`; serialized `findingType` | `Deficiency`, `Observation`, `Strength`, `Opportunity`; governed input and finding rule. | Finding-specific type. It distinguishes defect from non-defect, not final priority. |
| `FindingInput.business_consequence_basis`; serialized `businessConsequenceBasis` | For `Deficiency`: `material current breach`, `significant gap`, `clear deficiency`, `limited weakness`; for other types: `observation`, `strength`, `opportunity`. Valid pairs are in `FINDING_CONSEQUENCE_RULES` under methodology v1. | Finding-specific approved consequence basis. It does not assert revenue, customer impact, executive timing, or a dependency. |
| `severityAssignedFindings[].severityClassification`, `severityDecisionIdentifier`, `severityDecisionTableVersion` | `critical`, `high`, `medium`, `low`, `informational`; `severity-decision-table-set-v1`. | Finding-specific consequence classification and rule provenance; not a priority level. |
| `FindingInput.primary_dimension`, `related_dimensions`; serialized `primaryDimension`, `relatedDimensions` | `POC`, `GCR`, `TISM`, `DPSC`, `RVCI`; governed finding input and methodology v1. | Finding-specific capability links. They do not establish customer impact or dependency edges. |
| `FindingInput.source_references`; serialized `sourceReferences` | Nonempty references to entries in the governed `EvidenceProfileInput`; evidence quality is `Basic`, `Adequate`, or `Strong`, with optional `authenticity` or `traceability` limitation. | Finding-specific evidence identity and quality. References do not encode the underlying client's business facts. |
| `GovernedRecommendationResult.finding_id`, `recommendation_decision_identifier`, `recommendation_decision_table_version`; serialized recommendation counterparts | One approved rule for each linked finding, or `recommendation-v1-no-findings-monitor` with null link; `recommendation-decision-table-set-v1`. | Recommendation-specific rule and finding link. The rule ID can repeat across findings, so it is not a unique instance ID alone. |
| `recommendationClassification` | `immediate-action`, `priority-action`, `planned-improvement`, `best-practice`, `monitor`; recommendation table v1. | Recommendation-specific advisory category, not final priority. |
| `assessmentRisk.riskClassification`, `riskDecisionIdentifier`, `riskDecisionTableVersion` | `critical-risk`, `elevated-risk`, `moderate-risk`, `low-risk`, `minimal-informational`; `risk-decision-table-set-v1`. | Assessment-level risk from the complete severity distribution; cannot be treated as finding-specific impact. |
| `confidence.confidenceClassification`, `confidenceDecisionIdentifier`, `confidenceDecisionTableVersion` | `very-high-confidence`, `high-confidence`, `moderate-confidence`, `low-confidence`, `insufficient-confidence`; `confidence-decision-table-set-v1`. | Assessment-level certainty, not business importance. |
| `GovernedAssessmentResult.readiness.readiness_classification` | `Not Ready`, `Developing`, `Ready`, `Advanced`; approved readiness threshold set v1 and methodology v1. | Assessment-level readiness. It supplies context but no recommendation-specific impact or urgency. |
| `versionMetadata.methodologyVersion` and decision-table versions | `business-decision-methodology-v1` with the approved upstream table versions above. | Version binding and provenance, never a priority input value. |

### B. D1–D8 proposed decisions using Option A

| ID | Explicit proposed rule and exact input | Status and remaining approval |
| --- | --- | --- |
| D1 business impact | Read only the linked finding's exact `(findingType, businessConsequenceBasis)` pair. For all seven approved pairs, preserve the existing consequence basis unchanged as context. No new graded business-impact value is derivable. Missing or invalid pair rejects; a valid pair without an approved impact translation remains unsupported for final assignment. | Proposed bounded reuse; founder must approve whether consequence is sufficient for any specific business-impact rule. No revenue, cost, strategy, or financial claim is inferred. |
| D2 customer impact | Existing `sourceReferences` and dimension IDs contain no governed customer-impact flag or content. `evaluated` would require an approved affirmative source and value; `not-applicable` would require an approved explicit exclusion. Neither exists. Current finding-scoped applicability is unresolved, so no final priority is emitted. | Founder has selected conditional applicability, not its predicate. An applicable case lacking evidence would be `blocked-pending-data`; absence alone is neither exclusion nor zero impact. |
| D3 executive urgency | Risk, severity, readiness, and recommendation classification carry no direct executive decision, sponsorship, deadline, or funding state. Do not derive urgency from `immediate-action`, `critical`, or risk alone. Current finding-scoped applicability is unresolved, so no final priority is emitted. | Conditional applicability is selected, but no current governed predicate establishes evaluation or exclusion. Any proposed derivation requires explicit founder approval. |
| D4 severity and risk | Read the linked finding's exact severity value and assessment's exact risk value separately. Validate each against its approved taxonomy, rule identifier, and table version; preserve both in provenance. Neither changes the other. A mismatch or unsupported value rejects. No priority escalation, cap, or severity/risk-to-priority conversion is proposed. | Founder approval is required for any influence on D8, including mixed combinations such as low finding severity with elevated assessment risk. |
| D5 dependency role | No explicit dependency edge or role exists. Finding order, recommendation order, number of related dimensions, and shared evidence references are not dependency evidence. `evaluated` would require an approved relation naming the linked finding and blocked/unlocked work; `not-applicable` would require an approved explicit exclusion. Neither exists. Current finding-scoped applicability is unresolved, so no final priority is emitted. | Conditional applicability is selected, but its predicate and authoritative source remain unapproved. No edge is invented. |
| D6 confidence | Read the governed assessment confidence with exact rule/version. For `very-high-confidence`, `high-confidence`, `moderate-confidence`, and `low-confidence`, preserve the value as certainty context and continue to D8 without raising or lowering importance. For `insufficient-confidence`, block final priority assignment for finding-scoped recommendations; do not downgrade to `low` or change the recommendation. Missing, invalid, or unversioned confidence rejects. | Proposed conservative effect for all five classes; founder approval required. It does not claim that confidence measures business impact. |
| D7 no findings | If and only if the complete finding collection is empty, risk is `minimal-informational`, and the sole recommendation has null `findingId`, `monitor` classification, `recommendation-v1-no-findings-monitor` decision ID, and approved recommendation table version, emit a separately versioned `not-applicable` priority decision with no priority classification. Any extra finding/recommendation, wrong link, rule, risk, or version rejects. | Founder-preferred proposed inapplicability; explicit approval required. Historical v2/v3 output remains unchanged. |
| D8 final mapping | No finding-scoped emitting rule is justified by the present six-driver evidence. The proposed table below is complete as a **coverage and rejection specification**, not as a four-level assignment table. Every valid finding-scoped combination remains unassigned pending approved driver policy and mapping. | Founder must approve exact predicates for any of `critical`, `high`, `medium`, `low`; no level is filled by a severity or classification default. |

### C. Option A decision table, precedence, and conflicts

All rule identifiers below are draft identifiers only. The table processes the
complete recommendation set atomically. Validation precedes the no-findings
branch; no partial priority set is issued if any item is invalid or blocked.

| Precedence / draft rule ID | Exact predicate | Proposed outcome and rationale |
| --- | --- | --- |
| 0 `priority-option-a-v1-reject-context` | Unsupported assessment/methodology/upstream table version; incomplete finding or recommendation collection; invalid type/category; missing source decision ID/version; duplicate or incorrect finding link; recommendation rule/classification not consistent with its linked finding; or contradictory governed source values. | Reject. A malformed producer decision cannot support priority. |
| 1 `priority-option-a-v1-no-findings-na` | Empty complete finding collection; assessment risk `minimal-informational`; exactly one recommendation with `findingId: null`, `recommendationClassification: monitor`, `recommendationDecisionIdentifier: recommendation-v1-no-findings-monitor`, and approved recommendation table version. | `not-applicable`, no priority level. Monitoring guidance without a finding has no finding-scoped priority target under proposed D7. Preserve rule ID, methodology version, and null link. |
| 2 `priority-option-a-v1-insufficient-confidence-block` | At least one finding-scoped recommendation and assessment `confidenceClassification: insufficient-confidence`, with otherwise valid context. | Block final assignment for the whole set; confidence cannot establish reliable final priority. Existing recommendation remains unchanged. |
| 3 `priority-option-a-v1-unsupported-drivers-block` | At least one finding-scoped recommendation, confidence in the other four approved classes, and no approved customer-impact, executive-urgency, or dependency-role applicability rule from governed data. | No final assignment for the whole set pending rule approval. This row does not classify any driver as applicable or inapplicable; see the later conditional-applicability refinement. |
| 4 `priority-option-a-v1-no-emitting-rule` | A finding-scoped tuple passes validity checks but has no founder-approved complete six-driver predicate and output. | Block final assignment. No `critical`, `high`, `medium`, or `low` is emitted. |

There is no proposed emitting row for any of the four priority levels. In
particular, all valid `Deficiency`, `Observation`, `Strength`, and `Opportunity`
recommendations remain unassigned; varying consequence basis, severity,
assessment risk, readiness, or non-insufficient confidence does not change
that outcome. Unknown categories or contradictory claims reject under row 0.
Two future emitting rows with equal precedence or inconsistent driver effects
must reject until founder-approved conflict precedence is specified. Equal
priority values across different recommendations are permitted only after
assignment; existing stable recommendation order is not a tie-breaking formula.

### D. Fail-closed states and provenance

The proposed `not-applicable` state is a decision outcome, not a fifth level.
For D7 it requires the draft no-findings decision identifier, its future
approved table version, methodology version, null finding link, source
recommendation decision identifier/version, and complete-collection evidence.
No such output is currently issued. Finding-scoped blocked states carry an
internal reason and available upstream references, but no final priority.
Wrong types, unsupported categories/versions, missing linkage/provenance, or
contradictory governed values reject. Missing required business semantics block
pending data or approval; they never become low impact. The existing v2/v3
recommendation fields, defaults, golden fixtures, and attestation profiles
remain frozen.

### E. Feasibility and minimum remaining approvals

**OPTION A PARTIAL PROPOSAL.** Existing governed data supports exact source
validation, consequence and risk context, confidence gating, and the proposed
no-findings inapplicability rule. It does not contain authoritative customer
impact, executive urgency, or dependency relations; it also lacks an approved
translation from those drivers and existing consequence/risk context to any
of the four final priority levels. Thus Option A cannot yet produce a complete
finding-scoped final-priority methodology. This is a business-methodology and
input-availability gap, not a runtime defect.

Founder review should decide D1–D8 in the existing register, with D6 and D7
now carrying specific proposed outcomes. In particular, the founder must
approve exact conditional-applicability predicates for D2, D3, and D5, identify
an authoritative source for each applicable case, and approve exact
D8 mapping and conflict precedence. If no source exists, finding-scoped final
priority remains unassigned under Option A. Only after a complete approved
table and source binding exist may a separate authorized producer increment
implement it and design a versioned output. EIP may later verify and pass
through producer-issued priority; CEP and the AI Knowledge Assistant may only
present or explain authorized content. No production activation follows from
this draft.

## FOUNDER CONDITIONAL APPLICABILITY — PROPOSED REFINEMENT

**Design direction selected by founder:** Option A uses existing governed
producer data, and D2 customer impact, D3 executive urgency, and D5 dependency
role need not apply to every recommendation. This direction does not approve a
predicate, a priority mapping, an implementation, or a contract. Every rule
below is **PROPOSED — NOT AUTHORITATIVE**. This section supersedes the earlier
blanket-required assumption for D2, D3, and D5 and the Option A table's
unqualified blocked-state wording. It also supersedes the earlier
**OPTION A PARTIAL PROPOSAL** feasibility label; the current determination is
in section 5 below. It preserves the source inventory and historical
references above.

### 1. Driver states and evidence tests

The first three statuses below are valid only after a founder-approved,
versioned applicability rule exists. Until then, a D2, D3, or D5 state is
**undetermined by methodology**, and no final priority is assigned. This is a
drafting gap, not a fifth driver status or a priority classification.

| State | Exact condition | Required evidence and provenance |
| --- | --- | --- |
| `EVALUATED` | An approved predicate makes the driver applicable, and a governed producer fact supplies one of that predicate's approved values for this recommendation. | Driver rule ID/version, exact value, source field and source decision/evidence reference, recommendation/finding link, methodology version. |
| `NOT_APPLICABLE` | An approved deterministic predicate, supported by an affirmative governed fact about this recommendation, expressly excludes the driver. | Exclusion rule ID/version, exact establishing fact and source reference, recommendation/finding link, methodology version. No impact, urgency, dependency, zero weight, or priority value is implied. |
| `BLOCKED_PENDING_DATA` | An approved predicate makes the driver applicable, but its required authoritative value is absent or unavailable. | Applicability rule ID/version, known source context, missing field/reference, recommendation/finding link, methodology version; no final priority. |
| `INVALID` | A supplied fact has a wrong type, unsupported category/version, broken link, contradictory value, or false claim of inapplicability. | Rejection reason and offending source reference; reject the complete priority evaluation. |

An affirmative governed finding of no customer effect, no executive decision
need, or no dependency would be *evidence of absence* only if a future approved
source and rule give it that meaning. No such assertion exists now. An empty
field, unmentioned topic, or missing evidence reference is *absence of
evidence*. It cannot establish genuine inapplicability. Unavailable information
for an applicable case is `BLOCKED_PENDING_DATA`; malformed or contradictory
information is `INVALID`. A current case with no approved applicability
predicate remains undetermined by methodology and unassigned.

### 2. Conditional D2, D3, and D5 predicates

These are exact **proposed state transitions**, not claims that their
establishing facts already exist. Existing producer fields are listed so the
missing authority is reviewable. A future approved predicate must name a
governed field/value and its rule version before either `EVALUATED` or
`NOT_APPLICABLE` can be returned.

| Driver | `EVALUATED` only if | `NOT_APPLICABLE` only if | `BLOCKED_PENDING_DATA` / `INVALID` | Current determination |
| --- | --- | --- | --- | --- |
| D2 customer impact | An approved, linked governed assertion explicitly states a customer-impact category with supporting evidence reference. `findingType`, `primaryDimension`, `relatedDimensions`, `sourceReferences`, and `recommendationClassification` alone do not state one. | An approved, linked governed assertion explicitly establishes that this recommendation has no customer-impact role under a stated scope. A non-customer-named dimension or missing flag is insufficient. | Once an approved rule makes D2 applicable, absent category or supporting reference blocks. Wrong category/type, conflicting affirmative and exclusion assertions, or wrong finding link is invalid. | No affirmative or exclusion assertion exists in the current governed input; applicability is undetermined. |
| D3 executive urgency | An approved, linked governed assertion explicitly states a leadership decision, sponsorship, risk acceptance, funding need, or timing condition and its approved urgency value. `assessmentRisk`, finding severity, readiness, and recommendation rule/classification do not directly state it. | An approved, linked governed assertion explicitly establishes that no executive action or decision is required for this recommendation under a stated scope. Silence about deadlines is insufficient. | Once applicable, absent required urgency value/reference blocks. Unsupported value, contradictory assertion, or invalid version/link is invalid. | No affirmative or exclusion assertion exists in the current governed input; applicability is undetermined. |
| D5 dependency role | An approved, linked governed relation identifies this recommendation or finding and the specific work it blocks or unlocks, with an approved role value. Finding order, recommendation order, related-dimension count, and shared evidence references are insufficient. | An approved, linked governed assertion explicitly establishes no dependency role for this recommendation under a stated scope. No recorded edge is insufficient. | Once applicable, absent relation or target reference blocks. Unknown target, inconsistent edge/absence assertion, wrong type, or broken link is invalid. | No affirmative relation or exclusion assertion exists in the current governed input; applicability is undetermined. |

The smallest missing authority for each driver is **one versioned,
recommendation-linked applicability assertion** that states either an approved
value or an approved exclusion, with a governed source reference. D2 needs a
customer-effect assertion; D3 needs an executive-action/urgency assertion; D5
needs a dependency relation or explicit absence assertion. No existing field
has these semantics. This draft does not add the assertions, invent their
values, or require new assessment questions. If an existing authoritative
source is later identified, its exact field and values must be approved before
use.

### 3. Preserved D1, D4, D6, and D7 proposals

| Decision | Active proposed behavior |
| --- | --- |
| D1 | Preserve the exact `FindingInput.business_consequence_basis` for the linked finding as governed consequence context. It yields no graded business-impact value, financial estimate, or customer/urgency judgment. |
| D4 | Preserve `severityAssignedFindings[].severityClassification` and `assessmentRisk.riskClassification` independently with their rule IDs and versions. Neither automatically maps to final priority or supplies D2, D3, or D5 applicability. |
| D6 | `very-high-confidence`, `high-confidence`, `moderate-confidence`, and `low-confidence` remain assessment-certainty context and do not raise or lower recommendation importance. `insufficient-confidence` proposes a block on finding-scoped final assignment, pending explicit founder approval. All five retain their existing governed decisions. |
| D7 | Propose `NOT_APPLICABLE` priority outcome only when the complete finding collection is empty, risk is `minimal-informational`, and exactly one `monitor` recommendation has null `findingId`, rule `recommendation-v1-no-findings-monitor`, and valid source versions/provenance. Malformed cases reject. This is not a priority level; historical v2/v3 outputs stay unchanged. Founder rule approval remains pending. |

### 4. Conditional D8 table and unsupported combinations

Conditional applicability does not itself authorize an emitting priority row.
The following review table gives exact current outcomes. Its IDs are proposed
draft identifiers only and create no executable rule.

| Order / draft rule ID | Predicate | Outcome and rationale |
| --- | --- | --- |
| 0 `priority-conditional-v1-reject-invalid` | Any required producer field, link, category, source decision ID, methodology/table version, or claimed driver state is malformed, contradictory, or unsupported. | `INVALID`; reject the complete priority evaluation, with no partial assignment. |
| 1 `priority-conditional-v1-no-findings-na` | The complete D7 no-findings predicate in section 3 is true. | Proposed `NOT_APPLICABLE` outcome with decision ID/version and null link, after founder approval. No fifth level or implicit low. |
| 2 `priority-conditional-v1-insufficient-confidence` | At least one finding-scoped recommendation has valid `insufficient-confidence` assessment context. | Proposed block on final assignment after D6 approval; no priority downgrade. |
| 3 `priority-conditional-v1-applicability-undetermined` | At least one finding-scoped recommendation and no approved D2, D3, or D5 applicability predicate establishes evaluated or inapplicable status. | No final assignment. An undefined rule cannot prove inapplicability or applicable missing data. |
| 4 `priority-conditional-v1-required-data-missing` | A future approved D2, D3, or D5 predicate establishes applicability, but its required authoritative value/reference is absent. | `BLOCKED_PENDING_DATA`; no final assignment. |
| 5 `priority-conditional-v1-no-emitting-mapping` | Valid driver states are established, but no founder-approved complete four-level predicate matches. | No final assignment pending D8 approval; after a complete table is approved, an unmatched tuple would reject. |

**No emitting `critical`, `high`, `medium`, or `low` row is defensible from
current data.** All finding-scoped combinations of the seven approved finding
type/consequence pairs, five severity classes, five assessment-risk classes,
four non-insufficient confidence classes, and four readiness classes remain
unassigned because D2, D3, and D5 applicability is undetermined and D8 has no
approved mapping. The governed input validation already limits which
combinations are possible; this statement does not authorize impossible
tuples. Insufficient-confidence finding cases follow row 2. Complete no-findings
cases follow row 1 only after D7 approval. Invalid combinations follow row 0.
No driver is assigned `NOT_APPLICABLE` merely to make the table complete.

Any future emitting row must state its exact governed values for D1/D4/D6,
the evaluated or explicitly inapplicable states for D2/D3/D5, source fields,
priority output, rule ID/version, precedence, conflict behavior, and
deterministic rationale. Equal-priority recommendations may retain existing
ordering, but ordering never assigns priority. A future tie between emitting
rules or conflicting driver assertions rejects until founder-approved
precedence resolves it.

### 5. Feasibility, founder decisions, and next action

**ADDITIONAL GOVERNED INPUT REQUIRED.** Current producer data cannot
distinguish `EVALUATED`, `NOT_APPLICABLE`, and `BLOCKED_PENDING_DATA` for D2,
D3, or D5. Conditional applicability therefore does not complete D8. The
minimum missing information is the three recommendation-linked assertions
described in section 2, or an identified existing authoritative source with
equivalent explicit semantics. This is a bounded source and methodology gap,
not a software defect or a request to redesign the assessment.

Founder approval remains needed for the exact D2/D3/D5 applicability
predicates and value/exclusion sources, the D6 insufficient-confidence block,
the D7 no-findings inapplicability, and complete D8 four-level predicates with
conflict precedence. D1 consequence use and D4 severity/risk effects also
remain subject to the original D1/D4 decisions. The smallest next action is
founder review of the exact source and applicability semantics for three
recommendation-linked assertions, then the D8 mapping. Current producer fields
do not supply those assertions; their governance must be decided before
final-priority mapping can be completed. No new question,
producer contract, implementation, EIP calculation, CEP change, or production
activation is authorized by this draft. The Assessment Service remains the
decision owner; EIP may later verify and pass through producer-issued priority,
while CEP and the AI Knowledge Assistant may present or explain approved
information only. Historical v2/v3 contracts, golden fixtures, and completed
Stage 4G.6 boundaries remain unchanged.

**Final approval status: NOT APPROVED — FOUNDER REVIEW REQUIRED.**
