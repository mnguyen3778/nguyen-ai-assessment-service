# D8 Nonproduction Consumer Contract Plan v1

**Status: PROPOSED — SYNTHETIC NONPRODUCTION CONSUMER CONTRACT. NO CONSUMER IMPLEMENTATION OR PRODUCTION AUTHORIZATION.**

## 1. Purpose and scope

This Increment 4 plan defines how a future local consumer may interpret a verified D8 extension artifact. It is a planning delta to [Document 46](46-d8-versioned-producer-integration-plan-v1.md) and [Document 47](47-d8-versioned-extension-artifact-plan-v1.md), within the [Assessment Service architecture baseline](../architecture/assessment-decision-engine-v2.md). Assessment Service's [D8 evaluator](../../src/assessment/local_d8_priority.py) remains the sole priority decision authority. This plan changes no methodology, producer contract, or runtime.

## 2. Authoritative producer baseline

[Document 43](43-d8-generalized-priority-coverage-founder-decision-v1.md) records generalized rule coverage; [Document 44](44-founder-d8-final-priority-methodology-approval-v1.md) approves the methodology; [Document 45](45-d8-nonproduction-implementation-plan-v1.md) bounds local evaluation. The existing [producer adapter](../../src/assessment/local_d8_producer_adapter.py) exports `LocalD8ProducerRequest`, `LocalSyntheticProducerBinding`, and `evaluate_local_d8_producer`. The [extension module](../../src/assessment/d8_priority_extension.py) exports `build_local_d8_extension(request, result) -> bytes` and `validate_local_d8_extension(blob: bytes) -> dict`; the latter returns a validated parsed artifact or raises `ValueError`. The [local pipeline](../../src/assessment/local_d8_extension_pipeline.py) exports `run_local_d8_extension_pipeline(request) -> LocalD8ExtensionPipelineResult`; its successful `VERIFIED_EXTENSION` result contains artifact bytes only after verifier success and comparison with the request and adapter evaluation. Its failure statuses are local orchestration results, not serialized D8 outcomes. The extension is separate from frozen v2/v3 packages and signed handoffs.

## 3. Consumer trust boundary

Four checks have different meanings: **integrity** detects changes to canonical artifact content under the local digest format; **artifact-to-decision binding** compares parsed fields with an independently supplied expected assessment, snapshot, decision, finding, recommendation instance, confidence decision, and versions; **issuer authenticity** would establish who issued the artifact; **consumer authorization** would establish who may receive or view it. The current SHA-256 digest establishes neither issuer authenticity nor authorization. A party able to replace both payload and digest can make a same-shape synthetic artifact. The local pipeline's synthetic binding does not establish client access rights. No existing production authority source is asserted here.

## 4. Artifact input contract

The **existing** input is one complete `bytes` artifact, at most `65536` bytes, with canonical UTF-8 JSON and exact root order `payload`, `integrity`. The supported payload has `schemaId: "nguyen-ai-local-d8-priority-extension"`, exact integer `schemaVersion: 1`, and `designation: "SYNTHETIC_NONPRODUCTION"`. The required **existing** payload fields, in canonical order, are `schemaId`, `schemaVersion`, `designation`, `assessmentIdentity`, `assessmentVersion`, `producerMethodologyVersion`, `snapshotIdentity`, `findingId`, `recommendationInstanceIdentity`, `recommendationDecisionIdentifier`, `recommendationDecisionTableVersion`, `confidenceClassification`, `confidenceDecisionIdentifier`, `confidenceDecisionTableVersion`, `d8MethodologyVersion`, `d8RuleTableVersion`, `outcome`, `confidenceGate`, `validatedAssertionIds`, `evidenceProvenance`, and `reviewRequired`. `findingId` is a nonempty string for finding-scoped outcomes and JSON null only for D7. `evidenceProvenance` contains ordered `assertionId` and `evidenceReferences` fields, with synthetic references rather than evidence content. The existing `integrity` fields are `canonicalizationId`, `digestAlgorithm`, and `payloadDigest`.

Conditional **existing** fields are `priority` and `winningRuleIds` for `PRIORITY_ASSIGNED`; `governedFindingType`, `governedConsequenceBasis`, `excludedRuleIds`, `evaluatedDriverValues`, and `reviewReference` for `PRIORITY_NOT_DETERMINED`; and no additional fields for `NO_FINDINGS_MONITOR`. No other outcome has a successful extension shape. Consumer code must treat this exact shape as input data, not as a new source of decisions.

## 5. Required verification sequence

A future local consumer must establish the following before any successful projection:

1. Require an artifact of exact `bytes` type, present and within the 64 KiB bound.
2. Require valid UTF-8, strict JSON structure, canonical byte representation, supported JSON types, and no duplicate keys.
3. Require the supported schema ID, exact schema version, synthetic designation, and supported producer/D8 versions.
4. Invoke `validate_local_d8_extension` and require its documented parsed `dict` success result; require valid local integrity metadata and digest verification.
5. Use the returned parsed artifact and require its exact root, payload, conditional, and integrity shape. Reject an absent, malformed, or unexpected verifier return; absence of an exception alone is insufficient.
6. Compare every applicable identity and version field with a separately supplied, trusted expected context for this decision. The artifact cannot supply its own expected context. Reject missing or conflicting context.
7. Enforce the outcome-specific invariants below, including PND and D7 null linkage.
8. Only then construct a bounded nonproduction projection. Any failed step returns no successful projection.

Steps 2–4 are logical checks implemented together by the existing strict validator; this sequence does not call for a permissive preliminary parser. Canonical JSON uses fixed insertion order, compact separators, `ensure_ascii=False`, `allow_nan=False`, UTF-8 encoding, and byte equality after reserialization. The digest is lowercase `sha256:` plus 64 hex characters, computed over `b"NGUYEN-LOCAL-D8-EXTENSION-v1\x00"` followed by canonical payload bytes. This is local integrity, not authenticated issuance.

## 6. Schema and version handling

Support only the existing schema ID/version and `SYNTHETIC_NONPRODUCTION` designation in this plan. Require the exact existing `assessmentVersion`, `producerMethodologyVersion`, `d8MethodologyVersion`, and `d8RuleTableVersion` accepted by `validate_local_d8_extension`, plus the exact decision-table versions supplied by trusted expected context. The existing D8 tags are `founder-d8-methodology-approval-v1-local-synthetic` and `local-synthetic-d8-rule-table-v1`; these are separate from the producer methodology version. `canonicalizationId` is `local-d8-extension-json-v1`, and `digestAlgorithm` is `SHA-256`. Unsupported versions, unknown fields, noncanonical field order, and silent downgrade must fail closed. A later version needs a separately specified validation and interpretation path; no future version is presumed compatible.

## 7. Decision and identity binding

The proposed consumer receives **expected context** separately from artifact bytes. Before projecting, it compares exact `assessmentIdentity`, `assessmentVersion`, `producerMethodologyVersion`, `snapshotIdentity`, `recommendationDecisionIdentifier`, `recommendationDecisionTableVersion`, `confidenceClassification`, `confidenceDecisionIdentifier`, `confidenceDecisionTableVersion`, `d8MethodologyVersion`, and `d8RuleTableVersion`. For a finding-scoped result it also compares nonnull `findingId` and `recommendationInstanceIdentity`, including their expected link. For D7 it requires the trusted context's no-findings state, null `findingId`, and the exact monitor recommendation instance/decision binding. Compare `outcome` with the expected decision outcome when an independently verified producer evaluation is available. A matching artifact field alone cannot establish the expected value.

The local `snapshotIdentity` is a synthetic caller-supplied token, not the signed `producerSnapshotIdentity`. A future consumer must not infer package association, currentness, issuer authority, or client permission from this token, a display label, an array position, or a recommendation decision ID alone. If the consumer lacks independently trusted expected bindings, it rejects a binding-dependent successful projection; local fixture context suffices only for synthetic tests.

## 8. Assigned-priority interpretation

For `PRIORITY_ASSIGNED`, require `confidenceGate="PASSED"`, `reviewRequired=false`, nonnull linked `findingId`, `priority` in the existing `critical|high|medium|low` set, and nonempty sorted unique `winningRuleIds` from the approved rule IDs. The consumer may present the verified `priority` and `winningRuleIds` after contextual binding. It must not evaluate rules again, choose different winning IDs, re-rank, or infer a level from evidence references.

## 9. PND review-required interpretation

For `PRIORITY_NOT_DETERMINED`, require `confidenceGate="PASSED"`, `reviewRequired=true`, a linked finding and recommendation instance, and the complete conditional trace: `governedFindingType`, `governedConsequenceBasis`, `excludedRuleIds`, `evaluatedDriverValues`, and `reviewReference`. `evaluatedDriverValues` has exactly three ordered `{ "driverId", "assertedValue" }` entries for `customer-impact`, `executive-urgency`, and `dependency-role`; JSON null in `assertedValue` means no supplied value for that driver. Preserve all excluded IDs, values, and the exact deterministic `reviewReference`. Require absence of `priority` and `winningRuleIds`. The review reference is a local synthetic correlation value, not proof of a completed review or an assigned priority. External PND publication remains unapproved under Document 47.

## 10. D7 no-findings monitor interpretation

For `NO_FINDINGS_MONITOR`, require `confidenceGate="NOT_APPLICABLE_NO_FINDINGS"`, `findingId=null`, `reviewRequired=false`, empty `validatedAssertionIds` and `evidenceProvenance`, and the existing monitor `recommendationDecisionIdentifier` value `recommendation-v1-no-findings-monitor`. Require a trusted expected no-findings context and matching monitor instance and decision version. The artifact has no `priority`, `winningRuleIds`, or PND fields. The consumer may present a monitor state, without inventing a finding, recommendation occurrence, or priority. The existing monitor recommendation instance is explicit; the finding link alone is null.

## 11. Invalid and unsupported inputs

Reject missing or non-byte artifacts; more than 65536 bytes; BOM or invalid UTF-8; malformed or noncanonical JSON; duplicate object keys at any depth; nonfinite values or invalid JSON types; unknown/missing fields; unsupported schema, designation, methodology, rule-table, assessment, or canonicalization versions; malformed or mismatched digest; and malformed nested provenance or PND trace. Reject missing trusted expected context, mismatched assessment/snapshot/decision/finding/instance/confidence bindings, inconsistent outcome fields, and invalid D7 null linkage. `BLOCKED_REQUIRED_EVIDENCE`, `REJECTED_INVALID_ASSERTION`, `INSUFFICIENT_CONFIDENCE`, and unknown outcomes have no successful artifact schema. Do not reinterpret them as PND, D7, or low priority.

## 12. Fail-closed consumer behavior

On any verification, version, binding, or outcome failure, return a bounded rejection with no successful priority/PND/monitor projection. Do not repair a digest, rebuild an unverified artifact, retry with permissive parsing, strip unknown fields, downgrade versions, substitute identities, or expose raw exceptions to a client-facing projection. Retain only an appropriate local diagnostic reason. The consumer must not treat the pipeline's `VERIFIED_EXTENSION` status or a matching SHA-256 digest alone as sufficient consumer admission; contextual binding and authorization remain separate.

## 13. Consumer output boundaries

The fields in sections 4 and 8–10 are **existing artifact fields**. The following is a **proposed, unimplemented nonproduction consumer result**, not an existing API or producer field:

| Proposed consumer field | Meaning and condition |
| --- | --- |
| `disposition` | Consumer control result: `VERIFIED`, `REJECTED`, or `UNSUPPORTED`; these are not D8 evaluation outcomes. |
| `outcome` | Existing artifact `outcome`, only for a fully verified and bound result. |
| `projection` | Present only when `disposition=VERIFIED`; assigned: existing `priority` and `winningRuleIds`; PND: `reviewRequired`, full existing trace and `reviewReference`; D7: monitor state with null finding link and no priority. Preserve only the minimum bound identities and provenance references needed by the local use case. |
| `reasonCode` | Bounded diagnostic category only for rejection/unsupported input; no raw exception, client data, or fabricated decision. |

No proposed field creates a new business outcome. A future consumer remains an interpretation and presentation layer. It may pass through verified provenance references and traceability, subject to a later explicit access decision, but must not expose unnecessary identity data, PII, or raw assertion content.

## 14. Nonproduction isolation

This plan is limited to synthetic local development. It authorizes no production assessment access, decision publication, client-facing release, AWS deployment, EIP/CEP integration, signed handoff change, authority-source or persistence integration, or external artifact distribution. The [local pipeline](../../src/assessment/local_d8_extension_pipeline.py) and unsigned extension do not grant real issuance or access authority. Future production use requires separate explicit authorization and verification.

## 15. Future implementation prerequisites

A separately authorized local implementation would need a bounded input for artifact bytes plus independently supplied expected context, a call to the existing strict verifier, exact version and outcome binding checks, a structured fail-closed result, and tests for all three eligible outcomes and each rejection class. It must reuse the existing validator and never invoke the D8 evaluator. Before any external or production consumer, an authorized issuer binding, currentness/revocation rule, client access policy, and separately versioned association with a verified producer snapshot would need explicit decisions. None is supplied by this synthetic artifact or approved here.

## 16. Acceptance criteria

A future local consumer conforms only if it accepts the three supported v1 outcomes after strict integrity, schema, contextual identity/version, and outcome checks; preserves assigned priority and winning IDs, complete review-required PND trace, and D7 null linkage; rejects malformed, unsupported, or mismatched artifacts without a successful projection; makes no D8 decision; and leaves frozen packages, signatures, handoffs, and downstream services untouched. Local tests must distinguish digest validity from issuer authenticity and consumer authorization.

## 17. Explicit exclusions

No consumer implementation, route, persistence, external distribution, EIP or CEP change, package mutation, D8 methodology change, new priority level, rule reevaluation, production attestation, new authentication system, client authority source, deployment, or production-readiness claim is part of Increment 4 planning.

## 18. Open implementation questions

The existing local interfaces do not provide an independently trusted consumer context for expected snapshot, decision, and recommendation-instance bindings. A later nonproduction implementation must choose how a synthetic test harness supplies and pins that expected context; caller-supplied values are suitable only for local consistency testing. Any future real consumer additionally needs an authorized, authenticated source for those bindings and access rights. This plan makes no such source or approval decision.
