# D8 Final Recommendation Priority — Nonproduction Implementation Plan v1

**Status: PROPOSED — IMPLEMENTATION AUTHORIZATION REQUIRED. No D8 runtime or producer contract change is authorized by this plan.**

## 1. Purpose and scope

Plan the smallest local synthetic translation of the founder-approved D8 methodology. The first implementation should be a standalone pure evaluator, called only by focused local tests. The seven rule predicates, outcome meanings, precedence, and founder interpretations are fixed. This document describes engineering work; it does not perform or authorize it.

## 2. Verified repository baseline

Assessment Service root: `/Users/aiadmin/projects/nguyen-ai-assessment-service`; branch `main`; HEAD, local `origin/main`, and live remote `main`: `862017e15325cdd9ed3cf5505f21312f3e5d02a7`. Working tree and index were clean before this document was created. [Document 43](43-d8-generalized-priority-coverage-founder-decision-v1.md) SHA-256 `54677bd185d3ad4837d4b52df0a997fd6f2fb1f9123106b9f06ae8335878a383`; [Document 44](44-founder-d8-final-priority-methodology-approval-v1.md) SHA-256 `88d2aa9845ce0e82e063047c5cf8793580accea9670cb81a342c1da6f1a3b17f`. No frozen baseline is changed by this plan.

## 3. Approved methodology references

Document 44 is the approval authority; Document 43 supplies the exact seven predicates and 84-tuple ledger. [Document 35](35-founder-priority-assertion-methodology-direction-approval-v1.md) separates founder methodology from client fact approval; [Document 37](37-founder-priority-applicability-approval-v1.md) defines D2/D3/D5 evidence states and no `NOT_APPLICABLE` branch; [Document 39](39-founder-final-priority-direction-approval-v1.md) preserves D1/D4/D6/D7 boundaries; [Document 41](41-d8-evidence-based-precedence-founder-proposal-v1.md) records Option B candidates and precedence history. The approved rules are B-C1/critical, G-H1/high, G-H2/high, B-H3/high, N-H7/high, B-M1/medium, G-L1/low. The first four confidence classes are context; insufficient confidence blocks. Risk is context only. D7 is a separate no-finding outcome. Priority means authorized business action importance, including possible action on a non-deficiency. G-L1 is an explicit lower-intervention policy within its exact eligible classes, not a measure of intrinsic importance.

## 4. Current code inventory

| Actual file and symbol | Current responsibility | D8 relevance and proposed modification |
| --- | --- | --- |
| [governed_assessment_input.py](../../src/assessment/governed_assessment_input.py): `FindingInput`, `EvidenceProfileInput`, `ValidatedCanonicalExecutiveAssessmentInputV2`, `FINDING_CONSEQUENCE_RULES` | Validates seven finding/consequence pairs, finding IDs and source references, governed evidence profile, and canonical assessment input. | Reuse validated types read-only. Do not add questions or change validation. |
| [governed_decision_runtime.py](../../src/assessment/governed_decision_runtime.py): `assign_governed_severity`, `assess_governed_risk`, `assess_governed_confidence`, `recommend_governed_actions`, `GovernedRecommendationResult` | Produces versioned severity, assessment risk, confidence, and recommendations; recommendation has finding ID, class, decision ID, and table version. | Read validated outputs. Do not change selection or infer priority from labels/order. Decision ID alone is not a unique instance. |
| [decision_engine.py](../../src/assessment/decision_engine.py): `GovernedAssessmentResult`, `evaluate_assessment_v2` | Assembles the governed evaluation with findings, severity, risk, confidence, and recommendations. | Possible read-only source for synthetic fixtures; no runtime call-site change in Increment 1. |
| [approved_methodology_runtime_config.py](../../src/assessment/approved_methodology_runtime_config.py): `MethodologyVersionManifest`, `DecisionRuleRuntimeConfig`, `validate_approved_methodology_runtime_config` | Holds current approved severity/risk/confidence/recommendation table versions and validates config. | Version pattern to follow later; do not insert D8 into production config in the first increment. |
| [local_priority_assertions.py](../../src/assessment/local_priority_assertions.py): `SyntheticContext`, `RecommendationInstance`, `SyntheticEvidence`, `SyntheticAuthorityProfile`, `validate_local_assertions`, `AssertionSetResult` | Checks synthetic assertion schema, fixed issuer profile, same-snapshot recommendation/evidence binding, revisions, duplicates, contradictions, and D5 links. | Reuse unchanged for supplied local records. Its `required_driver_ids` applies across non-null recommendations, so call with an empty set and determine per-rule requirements in D8. Reject its legacy `VALID_NOT_APPLICABLE` result at the D8 boundary under approved v1 semantics. It does not verify real client authority or content. |
| [recommendation_priority.py](../../src/assessment/recommendation_priority.py): `build_recommendation_priority_evaluation` | Existing qualitative factor foundation marks final factors not evaluated. | Do not convert foundation ordering or classification into D8; leave unchanged. |
| [business_decision_package.py](../../src/assessment/business_decision_package.py): `build_business_decision_package` | Serializes v1, governed v2, and opt-in v3 packages. | No D8 integration in the first increment. |
| [business_decision_package_validation.py](../../src/assessment/business_decision_package_validation.py): `validate_business_decision_package`, `validate_business_decision_package_serialization`; [governed_producer_validation.py](../../src/assessment/governed_producer_validation.py): `validate_governed_conclusions` | Enforce existing package and governed conclusion shapes. | Read-only compatibility boundary. |
| [producer_snapshot_attestation.py](../../src/assessment/producer_snapshot_attestation.py): `ProducerSnapshotIssuer`, `ProducerSnapshotVerifier`; [executive_snapshot_handoff.py](../../src/assessment/executive_snapshot_handoff.py): `produce_executive_assessment_snapshot` | Version-specific signed snapshot verification and producer handoff. | No D8 fields, signature claims, or handoff changes in the first increment. |
| [test_local_priority_assertions.py](../../tests/test_local_priority_assertions.py), [test_golden_fixture_regression.py](../../tests/test_golden_fixture_regression.py) | Synthetic assertion tests and historical fixture checks. | New D8 tests should reuse synthetic patterns; historical fixtures remain untouched. |

## 5. Recommended local architecture

Choose **A: standalone pure evaluator** under `src/assessment/`, with an explicit local synthetic adapter/context supplied by the caller. Do not call it from `evaluate_assessment_v2`, Lambda, package serialization, snapshot handoff, EIP, or CEP. Flow: already validated governed inputs and synthetic assertion records → existing local assertion validator → exact pair-based D8 candidate selection → three-valued rule evaluation → critical/high/medium/low precedence → local result or explicit non-emitting outcome. Keep approved predicates in one versioned local rule table derived exactly from Document 44, with no scoring weights. An immutable result and pure evaluation function minimize changes to frozen runtime and contract code.

## 6. Input contract proposal

Propose a frozen `LocalD8InputV1` (name provisional) passed in memory, with no new API or persistence. **Existing validated fields:** complete `FindingInput` collection and governed pair/source references; severity assignments with decision IDs/table versions; `ApprovedRiskAssessmentResult`; `ApprovedConfidenceAssessmentResult`; `GovernedRecommendationResult` collection with finding ID/decision ID/table version. **Existing synthetic-only fields:** `SyntheticContext.snapshot_identity`, `assessment_identity`, `RecommendationInstance.instance_identity`, evidence registry/current revisions, fixed authority profile, and explicitly supplied D2/D3/D5 records. **New local D8 fields:** a caller-supplied exact mapping from each governed recommendation occurrence to one synthetic recommendation instance, snapshot identity, and the selected local D8 methodology/rule-table version. Validate one-to-one binding, the complete finding set, matching finding ID and governed recommendation decision/version, and no cross-snapshot reuse. Neither finding ID nor recommendation decision ID alone proves instance identity.

Reuse `validate_local_assertions(records, context, required_driver_ids=frozenset())` before D8 evaluation. The D8 adapter must accept only supported evaluated values, map them to Document 37 E1/E2/E3 states, and reject synthetic `VALID_NOT_APPLICABLE` even though the older local validator can return it. Local synthetic issuer IDs and source revisions are test fixtures. **Future production-only:** actual client business approval, real source-content verification, live currentness/revocation, cryptographic integrity, and a governed instance/snapshot identity binding. No such authority is inferred from the local profile.

## 7. Output contract proposal

Propose an immutable, version-tagged **local-only** result per exact recommendation instance. New local fields: logical outcome; optional priority (present only for `PRIORITY_ASSIGNED`); all matched same-level rule IDs in ascending order; candidate/excluded/pending rule IDs; finding and recommendation instance binding; D8 methodology/rule-table version; deterministic reason and required-evidence trace; and PND review trace/reference. Existing source values may be cited by ID/version without copying evidence content or PII.

Logical outcomes: `PRIORITY_ASSIGNED`, `PRIORITY_NOT_DETERMINED`, `BLOCKED_REQUIRED_EVIDENCE`, `REJECTED_INVALID_ASSERTION`, the approved D7 no-finding meaning, and a distinct insufficient-confidence block. These are proposed local field values, not existing package keys. A rejected assertion yields no priority; missing required evidence blocks; PND is review-required and non-emitting. Preserve deterministic order and no primary-rule shortcut. No new production schema authority is claimed.

## 8. Deterministic evaluation flow

1. Validate complete governed input and exact snapshot/recommendation/finding/decision-version alignment; validate all supplied synthetic records and reject invalid/contradictory claims. An unneeded invalid record still rejects. Apply D8's no-NA restriction after local validation.
2. Match the exact D7 empty-findings/sole-null-monitor condition; reject malformed monitor contexts. Otherwise apply the approved insufficient-confidence gate for finding-scoped cases.
3. Select eligible rule IDs using only the validated finding/consequence pair. For each Boolean atom, use `TRUE` for valid supporting evidence, `FALSE` for valid contrary evidence, `PENDING` for missing required evidence. Never infer absence.
4. Evaluate `AND` by a false atom or all true atoms; evaluate `OR` as true if any branch is fully true, false only when every branch is conclusively false, otherwise pending. Short-circuit requests for evidence, while still validating every submitted assertion.
5. Evaluate critical, high, medium, low. A pending potentially applicable higher rule blocks lower emission. Resolve every eligible peer at the winning level; retain every matched peer ID sorted. Preserve B-C1 precedence over overlapping G-H1. If all eligible rules are false, emit review-required PND with exclusions; no default low.

## 9. Synthetic test matrix

**Planned, not executed:** parameterize seven governed pairs × D2 `P/A` × D3 `T/U/A` × D5 `P/A` = 84 complete symbolic cases against the approved Document 43 ledger. Expected: critical 2, high 14, medium 1, low 4, PND 63. Assert exact rule IDs and evidence traces, not counts alone. Use synthetic approved-looking source records only within the fixed local test profile.

| Test group | Exact planned cases | Available locally / future boundary |
| --- | --- | --- |
| Positive and precedence | Each seven-rule match, G-H2's three OR branches, overlapping B-C1/G-H1, deterministic repeatability, same-level peer behavior, risk/severity disagreement, non-deficiency action meaning, G-L1's exact classes. | Pure local evaluator; synthetic fixtures. Same-level overlap may require a hypothetical table fixture because current approved rows have no same-level overlap; do not alter approved table. |
| Missing and short circuit | Missing required D2/D3/D5 separately; higher critical pending blocks high; lower true with higher pending; D2 omitted when B-C1 true; D3 omitted when G-H2 customer/dependency branch proves true; missing versus affirmed absence; PND exclusion and review trace. | Local synthetic records; rule-dependent requirements implemented by evaluator, not validator's global required-driver option. |
| Invalid/adversarial | Invalid type/value, unsupported pair/version, wrong assessment/snapshot/recommendation/finding binding, duplicate/conflicting claims, stale revision, wrong issuer/driver, unsupported NA, invalid unneeded supplied claim, invalid D5 target/relation, wrong ordering. | Local validator plus D8 adapter; no real source-content or live authority claim. |
| Special gates | Insufficient confidence, valid D7 sole null-linked monitor, malformed monitor, no rule match, all-match peer provenance. | Local synthetic fixture; real client approval/currentness/signature tests require separately authorized future integration. |

Keep [golden regressions](../../tests/test_golden_fixture_regression.py), producer contract tests, and full suite as non-regression gates. Do not edit historical expected output.

## 10. Frozen contract compatibility

Existing package identifiers are `business-decision-package-v1`, `business-decision-package-v2`, and opt-in `business-decision-package-v3` in [business_decision_package.py](../../src/assessment/business_decision_package.py). The frozen [v2 contract](../architecture/business-decision-package-contract-v2.md) carries four recommendation fields; the frozen [v3 contract](../architecture/business-decision-package-contract-v3.md) carries exactly five, adding `recommendationActionText`. Existing v2 remains the governed default. Signed v2/v3 handoffs use their version-specific canonicalization and verification profiles in `producer_snapshot_attestation.py`; adding D8 fields would change signed content. The first local evaluator can operate entirely outside these packages, serializers, validators, signatures, and [snapshot handoff](../../src/assessment/executive_snapshot_handoff.py).

A future producer-issued priority requires a **separately versioned contract decision** with exact recommendation-instance linkage, priority or explicit non-emitting state, methodology/rule-table version, and all matched peer IDs. Do not presume a package v4 or append fields to v2/v3. Preserve historical golden fixtures and defaults.

## 11. EIP/CEP separation

EIP `/Users/aiadmin/projects/executive-intelligence-platform` was read-only at `8fc31508ab435d565c2225cce6db8aba95be4958`, clean. Platform `/Users/aiadmin/projects/nguyen-ai-platform` was read-only at `878b873dbf938a748701e2e0354412471946e545`; its pre-existing protected untracked document was not changed. No interface is needed for Increment 1. A future versioned producer output would require EIP validation/pass-through only, CEP authorized presentation only, and AI Knowledge Assistant explanation only; none may independently calculate or change priority.

## 12. Incremental implementation plan

Each increment requires separate authorization; this plan grants none.

| Increment and exact prospective files | Scope and acceptance criteria | Required tests / stop condition |
| --- | --- | --- |
| 1. Create `src/assessment/local_d8_priority.py` only as the implementation work step. | Pure local types, exact seven-rule table, candidate selection, synthetic validator adapter, three-valued evaluation, precedence, non-emitting results; no production import. This work step is not accepted without Increment 2 tests. | Stop if exact synthetic instance binding cannot be proven or frozen files must change. |
| 2. Create `tests/test_local_d8_priority.py` only; complete the same authorized feature increment. | Focused synthetic positive, missing, invalid, no-NA, D7, PND, peer-order tests. | All focused cases deterministic and no AWS calls. Stop on rule/approval mismatch. |
| 3. Extend only `tests/test_local_d8_priority.py`. | Enumerate all 84 complete tuples from Document 43 with exact expected level/ID/PND; independent count check. | 2/14/1/4/63 and 84 total; no historical fixture rewrite. Stop on any mismatch. |
| 4. No new files; run existing recommendation, assertion, contract, golden, and full Assessment Service tests. | Verify local isolation and frozen v2/v3 outputs/signatures. | Stop on any unexplained regression or production import of D8. |
| 5. Separate versioned producer contract proposal **only if later authorized and necessary**; prospective path to be decided then. | Specify new producer projection and consumer validation without modifying frozen contracts. | Requires a new approval; stop before any EIP/CEP integration or production admission. |

## 13. Concrete risks and blockers

| Evidence from actual code | Impact / smallest correction | Blocks Increment 1? |
| --- | --- | --- |
| `validate_local_assertions` has a global `required_driver_ids` parameter and `VALID_NOT_APPLICABLE` from the older synthetic profile. | Call it with no global requirements; evaluate rule-specific needs locally; reject NA at D8 boundary. Do not rewrite the validator. | No, if adapter tests prove behavior. |
| `GovernedRecommendationResult` has finding ID and decision ID/version but no unique recommendation-instance ID; `SyntheticContext` has a separate instance identity. | Require an explicit one-to-one synthetic binding and reject duplicate/cross-snapshot links. Future production identity needs a versioned contract. | No for local synthetic input; yes for production admission. |
| `SyntheticEvidence` and fixed issuer profile validate local references/revisions, not real client source content, delegation, or live currentness. | Keep synthetic-only claims; defer real source/authority integration to separate authorization. | No for local; yes for production. |
| Frozen v2/v3 recommendation shapes and signed canonical conclusions exclude priority. | Keep the evaluator standalone; propose a separate versioned output later. | No for local; yes for producer publication. |
| Approved current seven rows have no same-level overlap, while F43-PREC requires all matched peer IDs. | Test peer resolution with an isolated synthetic rule-table fixture, without adding an approved rule or changing the production table. | No if evaluator exposes a test-only table seam; otherwise verify deterministic peer ordering with a focused pure helper. |

No evidence indicates a blocker to a **standalone local synthetic** Increment 1. Production source, authority, integrity, and contract requirements remain concrete later gates.

## 14. Acceptance criteria

An authorized local implementation must reproduce all seven predicates exactly, derive candidate eligibility from the governed pair, validate every supplied assertion, reject NA and invalid claims, block missing required/higher-level evidence, retain all same-level matches deterministically, distinguish all logical outcomes, and reproduce the 84-tuple ledger. It must leave existing runtime, v2/v3 packages, signed handoffs, golden fixtures, EIP, CEP, and AWS unchanged. No result may claim real client approval or production integrity.

## 15. Exact first implementation scope

The smallest complete first feature increment creates exactly **two files**: isolated module `src/assessment/local_d8_priority.py` and focused tests `tests/test_local_d8_priority.py`. The pure entry point takes explicit validated governed artifacts, an exact synthetic context/instance mapping, and supplied local assertion records. It returns a frozen local result and has no production call site. Work step 1 is not accepted until work step 2 passes. No existing file needs modification for this first feature increment.

## 16. Founder authorization boundary

Document 44 approves methodology only. This plan is **PROPOSED — IMPLEMENTATION AUTHORIZATION REQUIRED**. It does not authorize any increment, production assertion source, client approver, contract extension, EIP or CEP integration, commit, push, deployment, or AWS change. The founder's next bounded action is to authorize or correct the first two-file local synthetic feature scope and its focused test gate. Stop before implementation.
