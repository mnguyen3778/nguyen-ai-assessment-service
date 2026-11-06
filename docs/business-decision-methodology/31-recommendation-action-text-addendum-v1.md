# Recommendation Action-Text Methodology Addendum v1

Version: `recommendation-action-text-addendum-v1`

Status: `APPROVED` for the eight exact presentation statements below.

Approval date: 2026-11-05.

Approval authority and provenance: The founder and methodology owner explicitly
approved all eight statements in the project conversation for Stage 4G.4,
exactly as proposed in Stage 4G.3. This record does not assert a signed
approval document, independent review, external certification, production
approval, or implementation approval.

## Scope and version binding

This addendum approves client-readable descriptions of the eight existing
governed recommendation decisions in [Recommendation Decision Tables v1](25-recommendation-decision-tables-v1.md).
Each mapping is bound to the exact rule ID, decision table set version
`recommendation-decision-table-set-v1`, and methodology version
`business-decision-methodology-v1`. A recommendation classification alone is
not a mapping key. The configured rejection rules do not emit recommendations
and have no action-text mapping.

## Exact approved rule-to-text mappings

| Governed recommendation rule ID | Approved client-readable action text |
| --- | --- |
| `recommendation-v1-deficiency-critical-immediate` | Take immediate action in response to the identified critical deficiency. |
| `recommendation-v1-deficiency-high-priority` | Take near-term action in response to the identified high-severity deficiency. |
| `recommendation-v1-deficiency-medium-planned` | Plan an improvement in response to the identified deficiency affecting effectiveness or consistency. |
| `recommendation-v1-deficiency-low-planned` | Plan an improvement for the identified limited weakness. |
| `recommendation-v1-observation-monitor` | Monitor the identified observation as assessment or improvement context. |
| `recommendation-v1-strength-best-practice` | Consider preserving or reusing the practice reflected in the identified strength. |
| `recommendation-v1-opportunity-best-practice` | Consider the identified opportunity as a basis for practice improvement. |
| `recommendation-v1-no-findings-monitor` | Monitor the assessment context after this completed assessment, which generated no findings. |

The first seven mappings apply only to the corresponding finding-scoped rule
and preserve the source finding linkage. The no-findings mapping applies only
when a complete governed assessment generates no findings; its recommendation
retains `findingId: null`. It does not imply absence of business risk,
guaranteed compliance or safety, or that future assessment or improvement is
unnecessary.

## Presentation-only authority and frozen methodology

The approved text describes existing deterministic recommendation decisions.
It authorizes no new recommendation rule or classification, finding severity,
assessment question or requirement, scoring weight or maturity calculation,
risk or confidence calculation, remediation instruction, owner, deadline,
cost, technology, or AI-generated recommendation meaning. Unsupported
remediation specificity must not be inferred from a classification, finding
ID, or this text. The existing 48-question canonical methodology and all
deterministic decision outcomes remain unchanged. The Assessment Service
remains the authority for recommendation decisions.

## Producer contract and implementation boundary

This wording is not yet implemented in governed producer output. Under the
existing [Governed Business Decision Package Contract v2](../architecture/business-decision-package-contract-v2.md),
each `business-decision-package-v2` recommendation retains exactly four fields:
`findingId`, `recommendationClassification`,
`recommendationDecisionIdentifier`, and `recommendationDecisionTableVersion`.
`recommendationActionText` and `business-decision-package-v3` are proposals for
a future, separately authorized producer contract and implementation. This
addendum approves neither field or schema adoption, version migration,
publication, deployment, nor downstream client display. Existing package,
attestation, and snapshot identities must not be silently modified.

## Downstream authorization boundary

Later, separately authorized changes would be required for Executive
Intelligence Platform field admission and projection, trusted EXPLAIN adapter
fact admission with fresh exact-resource authorization, and Client Engagement
Portal Website response validation and presentation. Tenant and Business
Entity isolation, revocation and currentness checks, audit controls, and
content-free DENY behavior remain required. No production authority is
granted. The [Platform EXPLAIN content eligibility addendum](../../../nguyen-ai-platform/docs/platform/cep-nonproduction-explain-content-eligibility-addendum-v1.md)
and Stage 4B EXPLAIN contract govern later content eligibility and release;
this addendum does not amend either contract.

## Source references and verification evidence

- [Recommendation Decision Tables v1](25-recommendation-decision-tables-v1.md),
  Tables A and B, define the eight emitting rule IDs, conditions,
  classifications, rationales, and version binding. Table C defines
  fail-closed rejection rules.
- [Recommendation Decision Tables Specification v1](19-recommendation-decision-tables-specification-v1.md)
  requires advisory action statements but did not approve their actual text.
- [`RECOMMENDATION_DECISION_RULES`](../../src/assessment/approved_methodology_runtime_config.py)
  configures the eight emitting rules and rejection rules under the existing
  decision table set version.
- [`RECOMMENDATION_RULE_BY_FINDING` and `recommend_governed_actions`](../../src/assessment/governed_decision_runtime.py)
  establish finding-scoped selection, the no-findings rule, stable finding
  linkage, and existing four-field governed recommendation results.
- The founder's explicit approval in the Stage 4G.4 project conversation is
  the authority for the exact statement wording recorded here.
