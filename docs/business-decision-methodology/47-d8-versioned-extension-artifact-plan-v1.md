# D8 Versioned Extension Artifact — Schema and Compatibility Plan v1

**Status: PROPOSED — NONPRODUCTION. IMPLEMENTATION NOT YET AUTHORIZED.**

## 1. Purpose and authorization

This is the Increment 2 planning delta to [Document 46](46-d8-versioned-producer-integration-plan-v1.md). It proposes one standalone, versioned local synthetic D8 extension. The extension consumes a result from the verified local producer adapter and copies its priority decision; the [D8 evaluator](../../src/assessment/local_d8_priority.py) remains the sole priority decision authority. This document authorizes no implementation, publication, production call site, downstream integration, or deployment. The [Decision Engine architecture baseline](../architecture/assessment-decision-engine-v2.md) remains unchanged.

## 2. Verified repository baseline

On 2026-11-06, repository `/Users/aiadmin/projects/nguyen-ai-assessment-service` was on `main`. HEAD, local `origin/main`, and live remote `main` all equaled `bf26834d430afeb50e8dacea15348247113e59e8`. Before this document, `git status --short` was empty and the index had no staged changes. Required SHA-256 values matched:

| Existing file | SHA-256 |
| --- | --- |
| [Document 46](46-d8-versioned-producer-integration-plan-v1.md) | `c0eaa6ad59dbb479ebf7196535099af4295807202221da81b27392be0982324b` |
| [Local producer adapter](../../src/assessment/local_d8_producer_adapter.py) | `cd7d05f90425a83c403e23e3b264404af0683aedb8c32e070a16be472c4fbf88` |
| [Adapter tests](../../tests/test_local_d8_producer_adapter.py) | `51c3c9dc79385b5e3cecbdd04d9fc2826984e615676c134b05b7dc4e146e8f39` |
| [D8 evaluator](../../src/assessment/local_d8_priority.py) | `d5039a5f9f98275bb34544ddd82d905fb9ecfadd387bca21ef9f08cbd9aa0423` |

This is a planning baseline, not an extension verification or production admission.

## 3. Approved D8 references

[Document 43](43-d8-generalized-priority-coverage-founder-decision-v1.md) provides the exact generalized rule coverage and 84-tuple ledger. [Document 44](44-founder-d8-final-priority-methodology-approval-v1.md) approves the seven emitting predicates, four priority levels, PND, blocked/rejected outcomes, precedence, D7 separation, and confidence gate. [Document 45](45-d8-nonproduction-implementation-plan-v1.md) bounds the local evaluator. [Document 46](46-d8-versioned-producer-integration-plan-v1.md) chooses a separate versioned artifact and identifies the adapter increment. The committed [84-case evaluator tests](../../tests/test_local_d8_priority.py) and [adapter tests](../../tests/test_local_d8_producer_adapter.py) exercise synthetic translation. None of these grants real client assertion authority or changes a frozen producer contract.

## 4. Existing producer interfaces

The symbols below are **confirmed existing interfaces**. The last column is a proposed read-only relationship, not a current extension interface. `business-decision-methodology-v1` is the existing producer methodology version; it is distinct from the local D8 methodology tag.

| Exact path and existing symbol | Current version and responsibility | Compatibility constraint and proposed relationship |
| --- | --- | --- |
| [governed_assessment_input.py](../../src/assessment/governed_assessment_input.py): `ValidatedCanonicalExecutiveAssessmentInputV2`, `FindingInput` | `nguyen-ai-executive-assessment-v2`; validated answers, governed finding IDs/pairs, source references. | Read only for assessment/finding binding; source references do not approve D2/D3/D5 facts. |
| [decision_engine.py](../../src/assessment/decision_engine.py): `evaluate_assessment_v2`, `GovernedAssessmentResult` | Governed v2 result carrying findings, severity, risk, confidence, recommendations, and explanation. | Adapter input only; never add D8 to the frozen result or call the builder here. |
| [governed_decision_runtime.py](../../src/assessment/governed_decision_runtime.py): `GovernedRecommendationResult` | Recommendation has `finding_id`, classification, decision identifier, and decision-table version; no occurrence ID. | Read exact decision/version; require separate synthetic `RecommendationInstance` for occurrence identity. Decision label is not identity. |
| [approved_confidence_runtime.py](../../src/assessment/approved_confidence_runtime.py): `ApprovedConfidenceAssessmentResult` | Governed confidence classification, decision ID/version, producer methodology version. | Read only for the D6 gate and exact decision binding; no confidence-to-priority conversion. |
| [local_priority_assertions.py](../../src/assessment/local_priority_assertions.py): `SyntheticContext`, `RecommendationInstance`, `validate_local_assertions` | `local-synthetic-priority-assertion-v1`, fixed synthetic authority profile; context has assessment/snapshot IDs, instance IDs, evidence registry, current revisions. | Reuse validated synthetic references only; no real client approval, content verification, or live revocation. |
| [local_d8_producer_adapter.py](../../src/assessment/local_d8_producer_adapter.py): `LocalD8ProducerRequest`, `LocalSyntheticProducerBinding`, `evaluate_local_d8_producer` | Local synthetic adapter; validates complete producer alignment, selected finding/instance/decision/snapshot, then delegates to evaluator. | Proposed builder consumes its request and result read-only; no second priority evaluation. |
| [local_d8_priority.py](../../src/assessment/local_d8_priority.py): `LocalD8Result`, `evaluate_local_d8_priority`, `METHODOLOGY_VERSION`, `RULE_TABLE_VERSION` | `founder-d8-methodology-approval-v1-local-synthetic` and `local-synthetic-d8-rule-table-v1`; sole D8 priority decision and PND trace. | Copy outcome, priority, rule IDs, assertion IDs, driver values, and review reference without recalculation. |
| [business_decision_package.py](../../src/assessment/business_decision_package.py): `BusinessDecisionPackage`, `BusinessDecisionPackageVersionMetadata`, `build_business_decision_package`, `_governed_conclusions_to_dict` | `business-decision-package-v1`, governed default `-v2`, opt-in action-text `-v3`; exact package serialization. | No extension fields, version change, or package association in Increment 2. The existing recommendation priority foundation is not D8. |
| [business_decision_package_validation.py](../../src/assessment/business_decision_package_validation.py): `validate_business_decision_package`, `validate_business_decision_package_serialization`; [governed_producer_validation.py](../../src/assessment/governed_producer_validation.py): `validate_governed_conclusions` | Exact root order, versions, governed recommendation shapes and decision validity for v2/v3. | Remain unchanged; extension gets its own strict validator. |
| [executive_assessment_snapshot.py](../../src/assessment/executive_assessment_snapshot.py): `ExecutiveAssessmentSnapshot`, `validate_executive_assessment_snapshot_serialization`; [executive_runtime.py](../../src/assessment/executive_runtime.py): `EXECUTIVE_RUNTIME_RESPONSE_CONTRACT_VERSION` | `executive-runtime-response-v1` envelope and exact snapshot validation. | No extension field in snapshot or response status. |
| [producer_snapshot_attestation.py](../../src/assessment/producer_snapshot_attestation.py): `ProducerSnapshotIssuer`, `ProducerSnapshotVerifier`, `VERIFICATION_CONTRACT_VERSION`, `V3_VERIFICATION_CONTRACT_VERSION` | `producer-snapshot-attestation-v1` for v2 and `-v2` for v3; snapshot digest, version-specific canonical governed conclusions, Ed25519 signature verification. | Existing signatures authenticate only their existing profiles; extension hash is separate and unsigned. |
| [executive_snapshot_handoff.py](../../src/assessment/executive_snapshot_handoff.py): `produce_executive_assessment_snapshot`, `ExecutiveSnapshotProductionResult` | Version-selected producer handoff, local v3 issue/verify sidecar, failure results. | No call-site or handoff change. Downstream consumers continue receiving existing snapshot formats. |

## 5. Proposed extension architecture

Validated synthetic producer result and exact synthetic binding → `evaluate_local_d8_producer` → `LocalD8Result` → **proposed** standalone extension builder → **proposed** local strict validator/serializer → nonproduction artifact. The builder accepts the same `LocalD8ProducerRequest` and its adapter result as a pair, checks their compatible identities and versions, and copies the result's decision. It must not invoke `evaluate_local_d8_priority`, rerun `evaluate_local_d8_producer`, inspect D2/D3/D5 to derive a level, or mutate either input. The request is needed because `LocalD8Result` does not carry recommendation decision ID/version, confidence decision binding, or evidence reference arrays. This same-process pairing is a local consistency check, not proof that an arbitrary result object truly came from the adapter.

No production runtime, package, snapshot, handoff, handler, EIP, or CEP imports this builder. The artifact is separate from signed producer outputs and has no production publication path.

## 6. Proposed versioned schema

**Proposed identifiers, not existing constants or approved external contracts:** schema ID `nguyen-ai-local-d8-priority-extension`; schema version `1`. The complete local artifact is `{ "payload": {...}, "integrity": {...} }`, with exact field order and no extra keys. `payload.designation` is the literal `SYNTHETIC_NONPRODUCTION`. One artifact represents one selected recommendation instance, including the exact D7 null-finding monitor case.

**A. Required payload fields for every eligible outcome:** `schemaId`, `schemaVersion`, `designation`; `assessmentIdentity`, `assessmentVersion`, `producerMethodologyVersion`, `snapshotIdentity`; `findingId` (string for finding-scoped outcomes, JSON null only for D7); `recommendationInstanceIdentity`, `recommendationDecisionIdentifier`, `recommendationDecisionTableVersion`; `confidenceClassification`, `confidenceDecisionIdentifier`, `confidenceDecisionTableVersion`; `d8MethodologyVersion`, `d8RuleTableVersion`; `outcome`; `confidenceGate` (`PASSED` for assigned/PND, `NOT_APPLICABLE_NO_FINDINGS` for D7); `validatedAssertionIds` (sorted unique array); `evidenceProvenance` (sorted entries of `assertionId` and sorted unique `evidenceReferences`, synthetic references only); and `reviewRequired` (Boolean). The required integrity object has `canonicalizationId`, `digestAlgorithm`, and `payloadDigest`. Exact supported version strings come from the existing request/result constants above; reject others. `schemaVersion` is an exact integer, not an inferred package version.

**B. Conditional payload fields:** For `PRIORITY_ASSIGNED`, require `priority` equal to the adapter result's `critical|high|medium|low` value and `winningRuleIds` equal to its nonempty, sorted `matched_rule_ids`. For `PRIORITY_NOT_DETERMINED`, require `governedFindingType`, `governedConsequenceBasis`, `excludedRuleIds`, `evaluatedDriverValues` in D2/D3/D5 driver order (explicit JSON null means no supplied value), and `reviewReference`; require `reviewRequired=true`, no priority, and no winning IDs. For `NO_FINDINGS_MONITOR`, require null `findingId`, empty assertion/provenance arrays, `reviewRequired=false`, and no priority, winning IDs, or PND fields. Assigned results have `reviewRequired=false`; PND fields are absent. `validatedAssertionIds` and provenance entries must correspond exactly to the selected instance's validated records, with no evidence content copied. `reviewReference` is the existing deterministic **local synthetic correlation** value, not a completed review or production identity.

**C. Internal-only evaluation data:** `LocalD8Input`/request, full synthetic evidence registry and revisions, raw assertion records, evaluator `pending_rule_ids`, diagnostics/reason strings, intermediate candidate states, and complete governed result. Keep them in local memory/test diagnostics. The proposed artifact carries only the trace needed to preserve assigned or PND meaning.

**D. Prohibited from artifact publication:** blocked/rejected/insufficient-confidence evaluations as successful artifacts; synthetic issuer or business authority claims presented as real approval; raw evidence content, finding title, client name/contact or other unnecessary PII; signing key material; mutable package bytes; and an asserted production attestation. The synthetic artifact itself is never a publishable governed result. A future external schema and admission policy require separate approval.

## 7. Publication eligibility

Here **constructible** means a locally validated synthetic artifact, not an externally publishable result. Any malformed or mismatched request/result pair is ineligible regardless of status.

| Adapter outcome | Local artifact? | Reason and governed-result boundary |
| --- | --- | --- |
| `PRIORITY_ASSIGNED` | Yes | Valid synthetic finding-scoped decision; copy exact level and all winning rule IDs. Still not real client governed publication. |
| `PRIORITY_NOT_DETERMINED` | Yes | Founder-approved complete-exclusion, review-required non-emitting meaning; preserve full PND trace and no level. It is a local review diagnostic, not a completed priority assignment. External PND publication policy remains **unapproved**. |
| `NO_FINDINGS_MONITOR` | Yes | Exact D7 empty-finding/sole monitor case is a distinct local artifact with null finding and no four-level assignment. External representation remains unapproved. |
| `BLOCKED_REQUIRED_EVIDENCE` | No | Pending admissible evidence prevents a completed decision; retain only a local diagnostic result. |
| `REJECTED_INVALID_ASSERTION` | No | Invalid or mismatched input has no publishable governed conclusion; retain only a local diagnostic result. |
| `INSUFFICIENT_CONFIDENCE` | No | D6 blocks finding-scoped assignment; retain only a local diagnostic result. |

No status in this plan grants production publication. The builder fails closed for unknown outcomes and never converts PND or D7 into a priority.

## 8. Identity and version binding

Require exact nonempty synthetic assessment/snapshot/instance IDs from `LocalSyntheticProducerBinding`, `SyntheticContext`, and `LocalD8Result`; require equality across all three, and the canonical input's supported assessment and producer methodology versions. Require selected `finding_id` equality across binding, result, governed finding/recommendation, and synthetic instance. For D7, require all corresponding finding IDs null and exactly one monitor recommendation; do not infer D7 from a display label alone. Require selected recommendation decision ID/table version equal in binding, governed result, and synthetic instance. Require result D8 methodology/rule-table tags equal the exact supported local constants. Require confidence classification/decision ID/table version equal the governed result and consistent with an eligible outcome. Validate unique finding, recommendation, and instance collections and the same-snapshot assertion records; reject missing, duplicate, ambiguous, stale, conflicting, unsupported, or cross-snapshot bindings.

The synthetic `snapshotIdentity` is a caller-supplied local token, not the `producerSnapshotIdentity` calculated by signed snapshot attestation. Increment 2 must not pretend the token proves signed package association. A future association with real immutable snapshot bytes, package version, and verified attestation would need its own approved versioned binding. Display titles, array position, recommendation classification, decision rule ID alone, and synthetic IDs do not establish client authority.

## 9. Local integrity strategy

Existing [attestation code](../../src/assessment/producer_snapshot_attestation.py) rejects duplicate JSON fields, nonfinite values, unsupported profiles, wrong signed fields, and snapshot/conclusion digest mismatch; its v2/v3 profile signatures cover only existing snapshot bytes. The extension should use a **new local-only** canonicalization ID `local-d8-extension-json-v1` and digest domain `NGUYEN-LOCAL-D8-EXTENSION-v1` followed by a zero byte. Serialize the validated `payload` to UTF-8 JSON with a fixed explicit field order, exact conditional shape, fixed nested order, sorted arrays where specified, compact separators, `ensure_ascii=False`, `allow_nan=False`, and no Unicode normalization. Compute lowercase SHA-256 over domain plus payload bytes; `payloadDigest` is `sha256:` plus 64 lowercase hex characters. Verify by strict parse, exact schema and type checks, canonical reserialization, digest recomputation, and byte equality with the canonical form. Reject BOM, invalid UTF-8, duplicate keys at every depth, unknown/missing fields, unsupported versions, noncanonical order, oversize input (proposed 64 KiB maximum), and malformed references before accepting the local artifact. The same bound applies before parsing, to limit parser work. Use only standard-library `json` and `hashlib`; do not change existing attestation code.

This digest detects local accidental or adversarial modification **when the expected digest is retained independently**. An attacker able to replace both payload and digest can forge the artifact. No signing key, cryptographic signature, trusted issuer, currentness authority, or production attestation is created by Increment 2. The existing signed handoffs remain untouched and do not authenticate this extension.

## 10. Frozen contract compatibility

The [v2 package contract](../architecture/business-decision-package-contract-v2.md) has exactly four recommendation fields; the [v3 package contract](../architecture/business-decision-package-contract-v3.md) has five, adding action text. Package v2 remains the governed default and v3 requires explicit selection. `BusinessDecisionPackage.to_dict`, package validation, `ExecutiveAssessmentSnapshot`, version-specific canonicalization, sidecar signatures, and `produce_executive_assessment_snapshot` retain their exact current behavior. The new artifact is neither appended to packages nor inserted into signed envelopes. No frozen package hash changes; no fixture rewrite or signature regeneration is allowed.

Increment 2 tests should compare baseline v2/v3 package bytes, schema version metadata, validation results, signed handoff results/sidecars, and golden fixtures before and after local extension construction. Existing [package tests](../../tests/test_business_decision_package.py), [validation tests](../../tests/test_business_decision_package_validation.py), [producer contract tests](../../tests/test_governed_producer_contract.py), [v2 attestation tests](../../tests/test_producer_snapshot_attestation.py), [v3 attestation tests](../../tests/test_producer_snapshot_attestation_v3.py), [handoff tests](../../tests/test_executive_snapshot_handoff.py), and [golden regression](../../tests/test_golden_fixture_regression.py) remain unchanged. Any future package-to-extension association needs a separate versioned contract and authorization.

## 11. EIP/CEP separation

Assessment Service owns deterministic D8 evaluation and the proposed local artifact builder. EIP has no Increment 2 work; a future approved consumer would need explicit schema/version negotiation, exact identity and snapshot binding, producer authenticity and currentness checks, fail-closed parsing, and pass-through of the producer's outcome and trace. It must not recalculate priority. CEP may present only authorized results; the AI Knowledge Assistant may explain them without assigning or overriding a level. Neither EIP nor CEP changes are required or authorized here. The current downstream package path remains unaffected.

## 12. Exact implementation file plan

These are **proposed new files only**, with no current exported extension interface:

| Exact proposed path | Responsibility; input → output | Validation, dependency boundary, acceptance |
| --- | --- | --- |
| `src/assessment/d8_priority_extension.py` | Proposed `build_local_d8_extension(request: LocalD8ProducerRequest, result: LocalD8Result) -> bytes` plus `validate_local_d8_extension(blob: bytes) -> validated local artifact`. Define frozen local schema model/constants and canonical serializer in the same module. | Check exact supported versions, eligible outcomes, request/result/producer identity and provenance, strict schema and digest. Copy priority/rules/PND fields from result. Depend on existing adapter/evaluator types and standard library only; no evaluator call, package/handoff/handler import, or production call site. |
| `tests/test_d8_priority_extension.py` | Focused local synthetic construction and validation tests using actual adapter results and existing fixtures/ledger. | Exercise exact schema, eligibility, identity, provenance, canonical bytes, tampering, no input mutation, D7/PND separation, and frozen-contract non-regression. No second priority oracle or fixture changes. |

No separate schema file, attestation module, dependency, infrastructure file, or existing-source edit is needed for this bounded increment. If a strict local contract cannot be implemented without changing the evaluator, adapter, or frozen types, stop and return BLOCKED for implementation review.

## 13. Test and acceptance plan

Focused tests should cover repeated byte-identical output; exact schema/methodology/rule-table versions; assessment/snapshot/finding/instance/decision/confidence binding; unchanged adapter priority and all winning IDs; sorted assertion/evidence references; PND excluded IDs, driver values including explicit missing, review flag/reference; distinct D7 monitor; denial of blocked/rejected/insufficient-confidence and unknown outcomes; malformed/ambiguous/stale/mismatched inputs; duplicate and unknown JSON fields; unsupported versions; oversize payload; digest tampering and noncanonical bytes; no mutation; and no production import/call site. Reuse the independently authored 84-case synthetic ledger for representative and complete eligible-result round trips where useful; expected priority comes from the existing ledger and adapter result, never a new evaluator in the builder.

Run `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_d8_priority_extension.py' -v`, then `PYTHONPATH=src python3 -m unittest discover -s tests -v`. The stated current full-suite baseline is **550 passed**; Increment 2 must pass the then-current full suite, including frozen package, attestation, handoff, and golden tests. Inspect source imports/call sites and compare frozen fixture bytes and Git diffs. No local pass implies production authorization.

**PASS:** explicit v1 local schema; standalone builder; evaluator and adapter untouched; no priority derivation; exact identity/version and PND trace; unsupported input fails closed; canonical digest verification; frozen package bytes, versions, validation, signatures, fixtures, and handoffs unchanged; full regression green; no production integration. **BLOCKED:** any required frozen-contract edit, unexplained regression, inability to prove local binding, lost PND trace, accepted malformed artifact, or production call site. A local integrity hash never satisfies a future signing/admission gate.

## 14. Concrete risks and blockers

| Exact evidence | Consequence and smallest mitigation | Blocks Increment 2? / founder approval |
| --- | --- | --- |
| [LocalD8Result](../../src/assessment/local_d8_priority.py) lacks recommendation decision ID/version and evidence reference arrays; [request/context](../../src/assessment/local_d8_producer_adapter.py) carries the binding and records. | Result alone cannot form a traceable artifact. Require the exact request/result pair and cross-check selected records, without deriving priority. | No for local synthetic tests; real producer binding needs later contract approval. |
| [Adapter result](../../src/assessment/local_d8_producer_adapter.py) is a plain dataclass return; there is no signed or opaque proof of origin. | A fabricated same-shape result can pass local consistency checks. Keep artifact synthetic/nonproduction, use actual adapter results in tests, and require separate authenticated producer issuance before external admission. | No for Increment 2; yes for production; founder authorization later. |
| [SyntheticContext](../../src/assessment/local_priority_assertions.py) uses caller-supplied snapshot IDs, a fixed local issuer profile, and revision map. | Local binding/currentness is not signed snapshot identity or real client approval. Mark provenance synthetic and refuse production claims. | No for local; yes for production; founder approval of future authority source. |
| [Package serializer/validator](../../src/assessment/business_decision_package.py) and [attestation profiles](../../src/assessment/producer_snapshot_attestation.py) enforce exact v2/v3 shapes. | Appended fields would alter validation or signed bytes. Keep extension separate and test unchanged outputs. | No with standalone design; future association needs separate versioned approval. |
| [D8 evaluator](../../src/assessment/local_d8_priority.py) has blocked/rejected/insufficient-confidence outcomes alongside assigned/PND/D7. | A generic serializer could mislabel an incomplete evaluation as success. Use the explicit eligibility table and strict conditional schema. | No if tests pass; external PND/D7 publication remains an unapproved policy decision. |

These are implementation and later production boundaries supported by current code. No frozen root, bootstrap, or custodian decision is reopened.

## 15. Founder authorization boundary

The founder authorized this planning document only. The proposed schema ID/version, local digest profile, file paths, and eligibility choices are **not yet approved for implementation or external publication**. This plan does not designate client approvers, authenticate real evidence, create production keys, change signed handoffs, authorize EIP/CEP work, or permit AWS activity, deployment, commit, or push. Production admission would need a separately approved versioned association, real source/currentness authority, authenticated extension issuance, and explicit operational authorization.

## 16. Smallest next action

Founder reviews this exact two-file Increment 2 proposal and either authorizes it for separate nonproduction implementation or requests a bounded correction. Stop after Document 47 verification and report; do not implement the extension in this planning task.
