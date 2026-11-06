# Recommendation Priority Governed-Input Extension — Design Draft v1

**Status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**

This document designs a minimum producer-owned input for the D2 customer
impact, D3 executive urgency, and D5 dependency role drivers identified in
the [final-priority draft](32-final-recommendation-priority-addendum-draft-v1.md).
It specifies a reviewable assertion contract, not an approved business fact,
priority formula, package contract, or implemented workflow. Proposed contract
identifier `recommendation-priority-input-assertions-draft-v1` is a draft label,
not a supported runtime version.

## 1. Scope and exclusions

The Assessment Service would validate and own recommendation-linked governed
assertions for later priority evaluation. Assertions may establish an approved
driver value or an evidence-backed exclusion. They do not select or change a
recommendation, finding, score, severity, risk, confidence, summary, or final
priority. The canonical 48 questions and current assessment input stay frozen.
No new customer-facing question, persistence service, authority administrator,
production identity, or downstream activation is proposed.

## 2. Existing authority-source inventory

| Source | Reusable guarantee | Limit for this design |
| --- | --- | --- |
| [Governed v2 input model](../../src/assessment/governed_assessment_input.py) | `ValidatedCanonicalExecutiveAssessmentInputV2` binds assessment and methodology versions. `FindingInput` has unique `finding_id`, typed finding/consequence pair, dimensions, and nonempty `source_references`; each finding reference must identify an `EvidenceProfileInput` item. | `EvidenceQualityInput` stores reference, `Basic`/`Adequate`/`Strong` quality, and optional authenticity/traceability limitation. It carries no customer, urgency, dependency, business approver, or evidence-content assertion. |
| [Governed recommendation runtime](../../src/assessment/governed_decision_runtime.py) and [approved tables](25-recommendation-decision-tables-v1.md) | Finding-scoped recommendations carry `finding_id`, rule ID, classification, and `recommendation-decision-table-set-v1`; the complete no-findings case has one null-linked `monitor`. | A rule ID can repeat for multiple findings. Rule/classification and order do not establish D2, D3, or D5 facts. |
| [Evidence catalog](03-evidence-catalog.md) and [methodology specification](09-assessment-methodology-specification-v1.md) | Evidence categories and question/evidence/rule references support traceability. Evidence Evaluation does not change scoring. | A category such as Leadership or Strategy describes potential evidence type, not a verified assertion about this recommendation. Source references alone do not prove content, absence, approval, or currentness. |
| [Executive input boundary](../architecture/executive-assessment-input-contract-v1.md) | Canonical version-bound answers and structural validation are separate from priority evaluation. | It is not an extension slot for new priority facts in the frozen 48-question submission. |
| [v2 package contract](../architecture/business-decision-package-contract-v2.md), [v3 package contract](../architecture/business-decision-package-contract-v3.md), and [producer snapshot attestation](../../src/assessment/producer_snapshot_attestation.py) | Exact governed recommendation shapes, package version binding, signed snapshot handoff, and fail-closed verification are established. | Neither package admits extra assertion fields. Existing attestation profiles sign their specified snapshot content, not an arbitrary new assertion record. |
| [Snapshot lifecycle governance](../architecture/executive-assessment-snapshot-lifecycle-governance-v1.md) | Availability and downstream consumption require validated identity and integrity. | Snapshot availability does not prove organizational approval, evidence currentness, or production authority. |

Existing mechanisms can supply **identity and integrity checks** for an
extension design. They cannot supply the missing **business meaning or
approval authority**. No existing governed evidence extension mechanism was
found that records D2/D3/D5 values or explicit exclusions. Reuse of an
`EvidenceProfileInput.source_reference` is permitted only when a separately
governed evidence record behind that reference actually supports the assertion;
the current quality tuple alone is insufficient.

## 3. D2 customer-impact assertion

**PROPOSED — NOT AUTHORITATIVE.** Driver ID: `customer-impact`.

| Assertion value | Exact proposed meaning | Required support |
| --- | --- | --- |
| `impact-present` | Approved evidence establishes a customer effect relevant to this recommendation. It states presence, not magnitude or final priority. | Recommendation-linked source record identifying the effect and affected customer context, plus evidence reference and business approval. |
| `impact-affirmed-absent` | An authorized review affirmatively found no customer effect within a stated assessment scope. | Evidence of the reviewed scope and explicit absence finding; silence or a non-customer dimension is insufficient. |
| `not-applicable` | An approved applicability predicate excludes customer impact from this recommendation's decision scope. | Predicate ID/version, scope fact, evidence reference, and rationale. The exact predicate is **FOUNDER DECISION REQUIRED**. |
| No assertion / `unknown` evaluation state | Customer impact has not been established or ruled out. `unknown` is an evaluation outcome, not an assertion value. | If a future approved rule requires this driver, return `BLOCKED_PENDING_DATA`; otherwise no D2 status can be claimed before an applicability rule exists. |

The authoritative source would be a governed business assertion attached to
the assessment and recommendation, supported by a reference to inspectable
evidence. The supplier of that evidence and approver of its business meaning
are **FOUNDER DECISION REQUIRED**; the Assessment Service validates their
recorded authority reference but does not invent the conclusion. Missing
evidence blocks a required assertion; unsupported values, false absence, wrong
link, or contradictory present/absent claims are invalid. Dimension names,
severity, and recommendation classification are never substitutes.

## 4. D3 executive-urgency assertion

**PROPOSED — NOT AUTHORITATIVE.** Driver ID: `executive-urgency`.

| Assertion value | Exact proposed meaning | Required support |
| --- | --- | --- |
| `time-bound-executive-action` | A documented leadership decision or action has a governed timing condition relevant to this recommendation. It does not itself assign priority. | Decision/action reference and exact existing timing source or condition; do not generate a deadline. |
| `executive-action-required` | A documented leadership decision or action is required, with no asserted time-bound condition. Lack of a deadline is not proof of low urgency. | Decision/action reference, evidence, and business approval. |
| `executive-action-affirmed-absent` | Authorized review affirmatively found no executive decision or action required within a stated scope. | Reviewed scope and explicit absence finding. |
| `not-applicable` | An approved applicability predicate excludes executive urgency for this recommendation. | Predicate ID/version, establishing fact, evidence, and rationale. Exact predicate is **FOUNDER DECISION REQUIRED**. |
| No assertion / `unknown` evaluation state | No urgency conclusion is supported. | Required driver: `BLOCKED_PENDING_DATA`; unapproved applicability: no D3 status. |

The source would be a governed business decision or review record linked to
this recommendation. Evidence supplier and business approver are **FOUNDER
DECISION REQUIRED**. An action reference and, for the time-bound value, a
timing source are mandatory. A missing deadline never means no urgency.
`immediate-action`, critical severity, assessment risk, and readiness do not
prove any value above. Wrong types, unsupported timing claims, stale decisions,
and contradictory required/absent assertions are invalid.

## 5. D5 dependency-role assertion

**PROPOSED — NOT AUTHORITATIVE.** Driver ID: `dependency-role`.

| Assertion value | Exact proposed meaning | Required support |
| --- | --- | --- |
| `blocks-related-work` | The action represented by this recommendation is a prerequisite for specifically identified related work. | Directed edge from this recommendation to a target governed recommendation or finding identity, relation evidence, and approval. |
| `unlocks-related-work` | Completing the action represented by this recommendation enables specifically identified related work. | Directed edge and evidence as above; any semantic distinction from `blocks-related-work` in a future priority rule needs founder approval. |
| `no-dependency-affirmed` | Authorized review found no dependency relation within a stated reviewed scope. | Explicit absence assertion, scope, evidence, and approval; no recorded edge is insufficient. |
| `not-applicable` | An approved applicability predicate excludes dependency analysis for this recommendation. | Predicate ID/version, scope fact, evidence, and rationale. Exact predicate is **FOUNDER DECISION REQUIRED**. |
| No assertion / `unknown` evaluation state | Dependency has not been established or excluded. | Required driver: `BLOCKED_PENDING_DATA`; unapproved applicability: no D5 status. |

The source would be a governed relationship or review record. Evidence
supplier and business approver are **FOUNDER DECISION REQUIRED**. A positive
edge minimally needs source recommendation identity, target assessment and
recommendation or finding identity, direction, relation type, source evidence
reference, and approval. Cross-assessment edges are unsupported in this draft;
both ends must bind to the same assessment snapshot. Self-edges, nonexistent
targets, duplicate edges, contradictory edge/absence claims, and cycles whose
meaning has not been approved fail closed. Finding order, recommendation order,
shared dimensions or evidence, and finding count create no edge.

## 6. One common assertion contract

**PROPOSED — NOT AUTHORITATIVE.** One versioned record shape can represent all
three drivers. Driver-specific value and relation validation remain governed
rules. Proposed fields and exact structural requirements:

| Field | Required rule |
| --- | --- |
| `assertionId` | Nonempty stable identifier unique within the assessment's assertion set. |
| `assertionContractVersion` | Exact supported assertion contract version, separately selected; draft identifier above is not supported. |
| `assessmentBinding` | Exact producer snapshot identity and digest, assessment version, and methodology version. A source assessment ID alone is insufficient. |
| `recommendationBinding` | `findingId` plus `recommendationDecisionIdentifier` and `recommendationDecisionTableVersion`, matched to exactly one recommendation in the bound producer snapshot. Null finding ID is allowed only for the approved no-findings recommendation, which follows D7 rather than D2/D3/D5. |
| `driverId` | Exactly one of `customer-impact`, `executive-urgency`, `dependency-role`. |
| `applicabilityStatus` | Exactly `evaluated` or `not-applicable` on an issued assertion. Missing/unknown is not an issued assertion. |
| `assertedValue` | One approved driver value when `evaluated`; exact `not-applicable` marker only with an approved exclusion rule. A positive, affirmed-absent, and not-applicable value are distinct. |
| `applicabilityRuleId` and `applicabilityRuleVersion` | Approved deterministic predicate and version that justify evaluated or excluded status. No rule ID means no valid issued assertion. |
| `evidenceSourceReferences` | Nonempty, unique, canonical references to governed, inspectable source evidence supporting the exact claim or exclusion. Validate reference identity and source version; an evidence-quality reference without content support is insufficient. |
| `businessAuthorityReference` | Nonempty reference to the approved business decision or approval record for this assertion, bound to its approver and scope. The actual approval authority is unresolved. |
| `sourceRevision` and `currentnessReference` | Exact source-record revision plus a checkable currentness marker or valid-as-of reference; compare to the authorized source's latest applicable revision. |
| `relationTargets` | Empty for D2/D3. For positive D5 relations, one or more same-assessment target identities and edge directions. Empty for approved D5 absence or exclusion. |
| `rationale` | Deterministic reference to the approved assertion rule and source facts; no model-generated business assertion. |

The four **validation outcomes**, separate from assertion values and priority
levels, are `VALID_EVALUATED`, `VALID_NOT_APPLICABLE`,
`BLOCKED_PENDING_DATA`, and `INVALID`. The first two require an issued,
complete, current, approved assertion. `BLOCKED_PENDING_DATA` means an
approved applicable rule requires an assertion but the required source or
assertion is absent. `INVALID` means malformed, contradictory, stale,
unsupported, unapproved, or wrongly linked material; it rejects the assertion
set. Before applicability rules are approved, state remains undetermined by
methodology and no final-priority input is emitted. None is a fifth priority
level or a final-priority assignment.

## 7. Recommendation identity, evidence, and business authority

`recommendationDecisionIdentifier` is a rule ID, not an instance ID: two
findings may select the same rule. For current finding-scoped output,
`(assessmentBinding, findingId, recommendationDecisionIdentifier,
recommendationDecisionTableVersion)` is the proposed exact binding key, checked
against the signed producer snapshot. A driver may have at most one current
assertion for that key. The null-linked no-findings item remains D7 context
and does not receive fabricated D2/D3/D5 assertions.

An evidence supplier records an inspectable source; a designated business
approver decides what it means and approves the assertion. **FOUNDER DECISION
REQUIRED:** identify those functions, their scope, the governing source record,
and how approval is recorded. This draft assigns no production role or person.
The producer validates the authority reference, evidence binding, versions,
and currentness before admitting an assertion. An unsigned narrative, evidence
catalog category, model output, or existing evidence-quality tuple cannot
grant business authority. Audit trace retains assertion ID, source IDs,
revision, approver reference, decision/rule versions, validation outcome, and
the exact bound recommendation; it need not publish raw evidence.

## 8. Applicability, currentness, and revisions

`evaluated` requires an approved positive or affirmed-absent driver value with
evidence. `not-applicable` requires a different approved exclusion predicate
and evidence of its scope. `impact-affirmed-absent`,
`executive-action-affirmed-absent`, and `no-dependency-affirmed` are evaluated
business findings, not exclusions. No record or missing reference means
unknown; if applicable, it blocks. A claimed exclusion without an approved
predicate is invalid.

The current assertion is the latest authorized revision of one
`(assessmentBinding, recommendationBinding, driverId)` key, as determined by
the named governed source. A revision retains a new source revision and
approval reference; it does not mutate a previously issued record. Old
revisions remain audit history but cannot be selected as current. The exact
source-of-truth registry and currentness check are **FOUNDER DECISION
REQUIRED**; timestamps alone cannot prove currentness. If latest revision,
approval scope, snapshot binding, or supersession chain cannot be verified,
validation fails closed. Changing the underlying assessment or recommendation
requires a new binding and reapproval, not cross-assessment reuse.

## 9. Fail-closed validation

| Condition | Deterministic proposed outcome |
| --- | --- |
| Approved applicable rule exists but assertion/evidence is missing | `BLOCKED_PENDING_DATA`; no valid driver input. Absence cannot become an exclusion. |
| No approved applicability rule exists | Methodology undetermined; no issued driver status or final-priority input. |
| Unknown driver ID, value, status, contract/methodology/rule version, or invalid type | `INVALID`; reject. |
| Wrong snapshot digest, assessment binding, finding link, recommendation rule or table version | `INVALID`; reject cross-assessment reuse and broken linkage. |
| Missing or noninspectable evidence, unsupported content claim, or invalid authority reference | `INVALID` for a submitted assertion; if the required source has not been supplied at all, `BLOCKED_PENDING_DATA`. |
| Duplicate current assertions for one binding/driver, or conflicting values/exclusion claims | `INVALID`; reject the complete assertion set. |
| Stale revision, unverifiable currentness, withdrawn approval, or incorrect supersession | `INVALID`; reject; never fall back to an old revision. |
| D5 edge to unknown or cross-assessment target, self-edge, unsupported direction, contradictory absence, or unapproved cycle semantics | `INVALID`; reject. |
| False `not-applicable` claim or exclusion lacking an approved predicate and supporting fact | `INVALID`; reject. |

Validation must be atomic for the set consumed by a future priority decision:
no invalid assertion becomes valid by dropping a conflicting row, and no
partial priority output is published. The existing recommendation set remains
unchanged even when assertions block or reject priority evaluation.

## 10. Contract versioning options and historical compatibility

| Option | Assessment |
| --- | --- |
| Separate versioned producer-owned assertion record | **Recommended design.** Binds to exact signed snapshot identity and recommendation key without altering frozen v2/v3 fields. Needs a separately specified integrity/attestation profile, source-currentness check, validator, and explicit selection. These are design prerequisites, not existing capabilities. |
| Explicitly selected new producer package representation | Could carry assertions inside a newly versioned package after approval, but changes package serialization, canonicalization, attestation, and consumer admission. More coupled than needed to establish inputs. No package number is selected. |
| Existing evidence extension mechanism | No implemented governed mechanism was found that carries business assertions, approver references, source revisions, and explicit exclusions. `EvidenceProfileInput` and the evidence catalog provide reference/quality context only. Reuse their references where substantiated, not their structure as asserted business truth. |

The separate record must never claim the existing v2/v3 snapshot signature
covers its bytes. A future independently versioned producer integrity profile
must bind its exact bytes, source snapshot identity/digest, version metadata,
and authority/currentness evidence before EIP can verify it. Historical v2/v3
packages and signed handoffs remain byte-for-byte valid and unchanged. Missing
assertions on historical packages do not retroactively invalidate them; they
simply provide no new final-priority input. Existing defaults, golden fixtures,
and local Stage 4G.6 boundaries remain untouched. No downstream production
admission is proposed.

## 11. Non-executable deterministic test scenarios

All expected behavior below is **PROPOSED — NOT AUTHORITATIVE**. A later
authorized implementation would need exact approved value and authority
fixtures. The scenarios add no executable tests now.

| ID | Input condition | Expected validation outcome |
| --- | --- | --- |
| A01 | Current D2 `impact-present` with approved rule, linked evidence and authority. | `VALID_EVALUATED`; preserve source and recommendation binding, no priority. |
| A02 | Current D2 `impact-affirmed-absent` with reviewed scope and explicit evidence. | `VALID_EVALUATED`; distinct from exclusion. |
| A03 | Current D3 `time-bound-executive-action` with exact timing source; then `executive-action-required` without a time-bound claim. | Each `VALID_EVALUATED` under its own value; neither invents a deadline. |
| A04 | Current D5 positive relation with same-assessment target, direction and evidence. | `VALID_EVALUATED`; preserve edge identity. |
| A05 | Each driver has a supported exclusion assertion, approved predicate, scope evidence, and authority. | `VALID_NOT_APPLICABLE` for each; no impact/urgency/dependency or priority value inferred. |
| A06 | Approved predicate makes a driver applicable; required assertion or source evidence is absent. | `BLOCKED_PENDING_DATA`; no exclusion or low-value default. |
| A07 | Wrong assertion field type or unsupported driver/value/status. | `INVALID`; reject complete set. |
| A08 | Submitted assertion cites missing or noninspectable evidence. | `INVALID`; do not accept claimed value. |
| A09 | Wrong finding, recommendation rule/version, or snapshot digest. | `INVALID`; reject link. |
| A10 | Two current assertions use same key/driver, or positive and absence/exclusion values conflict. | `INVALID`; no first-wins behavior. |
| A11 | Superseded source revision, unverifiable currentness, or withdrawn approval. | `INVALID`; do not use old value. |
| A12 | Assertion from another assessment or unsupported business-authority reference. | `INVALID`; reject. |
| A13 | Unsupported assertion contract, methodology, or applicability-rule version. | `INVALID`; reject. |
| A14 | D5 self-edge, unknown/cross-assessment target, unsupported direction, or conflicting absence. | `INVALID`; reject. |
| A15 | Identical current assertions, source revisions, snapshot identity, and rule versions repeated. | Identical validation outcomes, canonical order, and audit references. |
| A16 | Historical v2/v3 snapshots and golden fixtures without assertion records. | Existing validation and bytes unchanged; no new priority input asserted. |
| A17 | Complete no-findings monitor with null finding ID and no D2/D3/D5 assertions. | Existing recommendation unchanged; D7 inapplicability remains a separate unapproved proposal in draft 32. |
| A18 | Valid D2/D3/D5 assertion set but no separately approved final-priority table. | Valid input context only; no final priority assignment or downstream activation. |

## 12. Founder decisions and minimum implementation prerequisites

The exact remaining business approvals are:

1. Name the governed business source for D2, D3, and D5 claims and explicit
   exclusions; decide who may supply evidence and approve its meaning, with
   scope and recorded authority. **FOUNDER DECISION REQUIRED.**
2. Approve or revise each proposed value vocabulary, the evidence necessary
   for affirmative absence versus inapplicability, and exact applicability
   predicates. **FOUNDER DECISION REQUIRED.**
3. Define the source's revision/currentness authority and how withdrawal or
   supersession is checked. **FOUNDER DECISION REQUIRED.**
4. Approve the meaning of D5 directed relations and whether both `blocks` and
   `unlocks` values are necessary. **FOUNDER DECISION REQUIRED.**

Only after those decisions may a separate increment specify an actual contract
version, producer source adapter, validation, integrity profile, and tests.
Final priority assignment additionally requires its own approved D1–D8
methodology and decision table; this input design does not satisfy that gate.

## 13. Nonproduction and downstream boundary

The Assessment Service remains owner of governed assertion validation and any
future priority decision. EIP may later verify producer-issued records and
priority without recalculation. CEP may present authorized information; the AI
Knowledge Assistant may explain it without changing it. No LLM output or
presentation normalization becomes business authority. This document does not
alter trusted authorization, publish a record, or activate production.

**Final status: PROPOSED — NOT AUTHORITATIVE. FOUNDER APPROVAL REQUIRED.**
