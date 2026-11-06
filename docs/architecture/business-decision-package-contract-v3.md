# Business Decision Package Contract v3

Contract identifier: `business-decision-package-v3`

Status: **APPROVED CONTRACT DESIGN — NOT IMPLEMENTED**

## Authority and scope

This contract defines a future, explicitly selected Assessment Service producer
representation of the eight existing governed recommendation decisions. The
founder-approved wording and its rule bindings are authoritative only in the
[Recommendation Action-Text Methodology Addendum v1](../business-decision-methodology/31-recommendation-action-text-addendum-v1.md).
This contract approves the v3 representation; it does not approve or activate
implementation, publication, downstream field admission or client display, a
production route, or deployment. The [Recommendation Decision Tables v1](../business-decision-methodology/25-recommendation-decision-tables-v1.md)
continue to determine recommendations. No new recommendation decision is
defined here.

V3 is bound to `recommendation-decision-table-set-v1` and
`business-decision-methodology-v1`. It uses the existing governed assessment
input schema `nguyen-ai-executive-assessment-v2` and the existing snapshot
envelope `executive-runtime-response-v1`. These identifiers describe different
contracts: the assessment input, nested business decision package, and
snapshot envelope are not interchangeable.

## V3 package and governed conclusions

The v3 package retains the v2 root field order and meanings:
`decisionEvaluation`, `businessReadinessSnapshot`, `confidenceEvaluation`,
`recommendationPriorityEvaluation`, `executiveSummaryFoundation`, `audit`,
`limitations`, `versionMetadata`, then required `governedConclusions`.
`versionMetadata.contractVersion` is exactly `business-decision-package-v3`;
its `assessmentVersion` is exactly `nguyen-ai-executive-assessment-v2` and its
`methodologyVersion` is exactly `business-decision-methodology-v1`. The
`governedConclusions` group and member order remain `severityAssignedFindings`,
`assessmentRisk`, `confidence`, `recommendations`, `executiveSummary`.
Only the governed `recommendations` item shape differs from v2.

Every v3 recommendation object has exactly five mandatory fields in this
serialized and canonical order:

| Order | Field | Required type and value |
| --- | --- | --- |
| 1 | `findingId` | Nonempty string identifying the triggering governed finding; `null` only for the complete no-findings recommendation. |
| 2 | `recommendationClassification` | Nonempty approved classification string equal to the selected governed rule's output. |
| 3 | `recommendationDecisionIdentifier` | Nonempty string identifying exactly one of the eight emitting rules in the approved decision tables. |
| 4 | `recommendationDecisionTableVersion` | String exactly equal to `recommendation-decision-table-set-v1`. |
| 5 | `recommendationActionText` | Nonempty string exactly equal, character for character, to the statement for `recommendationDecisionIdentifier` in the approved action-text addendum. |

No additional recommendation fields are permitted. All five are required;
`recommendationActionText` cannot be null, omitted, replaced by a
classification or rule rationale, or constructed from a finding title or ID.
The producer must use an immutable, version-bound mapping keyed by the
decision identifier. Its key set is exactly the eight emitting rules. The
configured rejection rules emit no recommendation and have no text mapping.
An unknown, missing, duplicate, or conflicting mapping fails closed. Neither
an LLM nor a downstream consumer may create or alter recommendation meaning.

For a complete assessment with no generated findings, the sole existing
`recommendation-v1-no-findings-monitor` decision has `findingId: null`, the
existing `monitor` classification, and exactly the addendum's approved
no-findings text. This does not imply absence of risk or generate an additional
recommendation. For finding-scoped decisions, `findingId` must equal the
corresponding triggering finding ID. Recommendation count, canonical finding
order, and recommendation order remain as in v2; missing or inconsistent links
are invalid.

## Explicit version selection and v2 compatibility

The existing governed package default remains `business-decision-package-v2`.
V3 requires an explicit package-version selection at package construction,
carried through executive orchestration, snapshot handoff, and all validators.
Only a supported governed `nguyen-ai-executive-assessment-v2` input may select
v3. The legacy assessment path cannot select v3. Unsupported versions and
invalid package/assessment pairings are rejected before publication. The same
deterministic governed recommendation decisions feed both version-specific
serializers; selecting v3 must not change decision selection.

The v2 serializer continues to emit exactly these four fields, in this order:
`findingId`, `recommendationClassification`,
`recommendationDecisionIdentifier`, `recommendationDecisionTableVersion`.
It must never append `recommendationActionText`. V2 serialization, validation,
default selection, golden fixtures, canonicalization, attestation verification,
and historical snapshots remain unchanged. V2 validation rejects a fifth
field. V3 output is not v2-compatible and must never be stripped, silently
downgraded, or presented to an existing v2 consumer as valid v2. Consumers
select compatibility by the nested `versionMetadata.contractVersion` and
reject unsupported versions.

## Snapshot and producer attestation profiles

The snapshot retains `responseContractVersion` =
`executive-runtime-response-v1` and its existing envelope field order. Its
nested package version distinguishes v2 from v3. No new assessment input or
snapshot envelope version is required by this content-only package change.
Snapshot and runtime validation must explicitly admit the supported
`business-decision-package-v3` / `nguyen-ai-executive-assessment-v2` pairing;
all other unsupported pairings fail closed.

The v3 snapshot requires a separate attestation verification profile with
these design identifiers, none of which is currently implemented or accepted:

| Attestation element | V3 design value | V2 preservation |
| --- | --- | --- |
| `verificationContractVersion` | `producer-snapshot-attestation-v2` | Existing `producer-snapshot-attestation-v1` remains valid for historical v2 snapshots. |
| `canonicalizationId` | `governed-conclusions-json-v2` | Existing `governed-conclusions-json-v1` remains unchanged. |
| Conclusions digest domain | UTF-8 bytes `NGUYEN-CONCLUSIONS-v2` followed by a zero byte | Existing `NGUYEN-CONCLUSIONS-v1` plus zero byte remains unchanged. |
| Signature domain | UTF-8 bytes `NGUYEN-ATTESTATION-v2` followed by a zero byte | Existing `NGUYEN-ATTESTATION-v1` plus zero byte remains unchanged. |
| Snapshot-byte digest domain | Existing `NGUYEN-SNAPSHOT-v1` followed by a zero byte | Retains the existing exact-byte snapshot identity calculation. |

The v3 sidecar retains the existing ordered sidecar field names and explicitly
binds `snapshotResponseContractVersion`, `packageContractVersion`,
`assessmentVersion`, `methodologyVersion`, and `canonicalizationId` under its
new signed verification profile. Its `packageContractVersion` must be
`business-decision-package-v3`. V3 conclusions canonicalization retains the
existing governed group, finding, risk, confidence, summary, and array order;
the recommendation field tuple has the five fields above. Canonical JSON uses
the existing compact UTF-8, Unicode, and non-finite-value rejection rules.
The exact `recommendationActionText` bytes enter the v3 canonical conclusions
and its version-specific digest. The sidecar signature binds the digest and
all version metadata. A missing or tampered text value, wrong profile,
canonicalization ID, version pairing, signature, or conclusions digest is
rejected. V2 issuance and verification must continue using the original v1
attestation profile without reinterpretation.

## Mandatory fail-closed validation

Producer construction, serialization, snapshot validation, attestation, and
consumer compatibility checks must reject unsupported package versions;
invalid package/assessment or snapshot/attestation pairings; unknown or
rejection-rule recommendation IDs; invalid classification-to-rule pairs;
missing, altered, substituted, or conflicting approved text; classification
used as the text lookup key; invalid decision-table or methodology versions;
extra v2 fields; missing or extra v3 fields; incorrect field order or type;
invalid finding links or no-findings conditions; invalid canonicalization
identifiers; and tampered signatures or digests. Unsupported content is never
silently accepted, substituted, truncated, downgraded, or published as a
partial recommendation set. A historical v2 verification regression fails
the v3 compatibility gate.

## Frozen decisions and downstream boundary

V3 adds only an approved client-readable representation of existing
recommendation decisions. It preserves the canonical 48 questions, question
applicability, assessment answers and input validation, scoring and weights,
maturity calculations, finding severity, risk and confidence classifications,
recommendation classifications and decision identifiers, finding linkage and
ordering, and all existing deterministic outcomes. It introduces no new
remediation requirement, owner, deadline, cost, technology, or AI-generated
decision meaning.

This producer contract does not authorize changes to the Executive
Intelligence Platform, trusted EXPLAIN adapter, or Client Engagement Portal
Website. Later, separately authorized increments must admit the new producer
version and field in EIP, project only approved content, admit an explanation
fact under fresh exact-resource Trusted Authorization, and validate and
present the Website response. Tenant and Business Entity isolation,
revocation and currentness checks, audit controls, content-free `DENY`, and
Website presentation-only behavior remain required. No production route or
deployment is authorized.

## Source and implementation boundary

The current [v2 package contract](business-decision-package-contract-v2.md)
defines the frozen four-field recommendation object. Current
[`BusinessDecisionPackage.to_dict`](../../src/assessment/business_decision_package.py),
[`validate_governed_conclusions`](../../src/assessment/governed_producer_validation.py),
and [`producer_snapshot_attestation`](../../src/assessment/producer_snapshot_attestation.py)
serialize, validate, and attest that shape. Executive orchestration and
snapshot handoff select the existing v2 path; runtime and snapshot validators
recognize the current versions. This document specifies a future contract
only. Implementing mapping, serializers, validators, attestation support,
tests, or downstream admission requires separate authorization.
