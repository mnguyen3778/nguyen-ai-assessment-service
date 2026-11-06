# Business Decision Package v3 Local Producer Verification v1

Date: 2026-11-05. Status: local verification evidence; no producer activation or
production authority.

## Scope, baseline, and authority

This record verifies existing local Assessment Service v3 components and
identifies the gap to an integrated producer path. It does not approve runtime,
schema, consumer, or deployment changes. The repository baseline was `main` at
`3af7770eb26307aeefe01a069268a3c24fcabe55`, synchronized with local and
live `origin/main`, with a clean tracked tree and index before this document was
created. The Platform dependency remained at
`878b873dbf938a748701e2e0354412471946e545`; its protected untracked
document had SHA-256
`14884bc189ae8a43c9e1583bd04b224f75265e8f394ccd9ac64bb222d83eb2b0`.

The [v3 contract](business-decision-package-contract-v3.md) defines the target
representation and attestation profile. The [v2 contract](business-decision-package-contract-v2.md)
defines historical behavior. The [approved action-text addendum](../business-decision-methodology/31-recommendation-action-text-addendum-v1.md)
alone authorizes the eight exact statements, bound to
`recommendation-decision-table-set-v1` and `business-decision-methodology-v1`.
The [recommendation decision tables](../business-decision-methodology/25-recommendation-decision-tables-v1.md)
remain the decision authority. This verification did not change the canonical
48 questions, scoring, maturity, severity, risk, confidence, recommendation
classification, rule selection, or approved wording.

## Producer component inventory

“Local” means callable in a synthetic, explicit v3 verification sequence;
“normal path” means reachable through `produce_executive_assessment_snapshot`.
All normal governed production remains v2.

| Component | Implementation and version support | Evidence and reachability | Constraint |
| --- | --- | --- | --- |
| A. Input validation | [`ValidatedCanonicalExecutiveAssessmentInputV2`](../../src/assessment/governed_assessment_input.py) and [`_validate_orchestration_input`](../../src/assessment/executive_orchestration.py) accept governed assessment v2. | Eight synthetic validated inputs passed through normal orchestration; governed tests passed. | V3 is a package version, not a new assessment input schema. |
| B. Governed decisions | [`evaluate_assessment_v2`](../../src/assessment/decision_engine.py) executes the existing deterministic result. | Normal path and all eight local cases passed; governed decision tests passed. | Shared v2/v3 decision object; no new decision engine. |
| C. Recommendation selection | [`recommend_governed_actions` and `RECOMMENDATION_RULE_BY_FINDING`](../../src/assessment/governed_decision_runtime.py) select finding-scoped or complete no-findings rules. | All eight emitting rule IDs observed in local cases; rule configuration tests passed. | Rejection rules emit no recommendation. |
| D. Package construction | [`build_business_decision_package`](../../src/assessment/business_decision_package.py) defaults to v2 and permits explicit local v3 for governed assessment v2. | Normal path selects v2; each local case explicitly built v3 from the same governed result. | Legacy and unsupported version requests fail closed. |
| E. Version selection | `governed_package_contract_version` is explicit at package construction. | Local v3 selection passed; normal orchestration and handoff still select v2. | Orchestration and handoff have no v3 selection parameter. |
| F. Serialization | [`BusinessDecisionPackage.to_dict`](../../src/assessment/business_decision_package.py) emits four v2 or five v3 recommendation fields. | Differential checks and package tests passed. | V3 field five is exact approved rule-bound text; no classification lookup. |
| G. Package validation | [`validate_business_decision_package` and `validate_business_decision_package_serialization`](../../src/assessment/business_decision_package_validation.py) admit exact supported version pairings. | Valid local v3 and historical v2 tests passed. | Missing, extra, reordered, or unsupported fields/versions reject. |
| H. Conclusions validation | [`validate_governed_conclusions`](../../src/assessment/governed_producer_validation.py) checks shape, text, severity, rule, order, and finding linkage by package version. | Local v3 validation and adversarial tests passed. | No-findings requires one `findingId: null` recommendation. |
| I. Canonicalization | [`_canonical_conclusions`](../../src/assessment/producer_snapshot_attestation.py) has the historical four-field profile and explicit v3 five-field profile. | Deterministic v3 digest and historical v2 tests passed. | Text bytes enter v3 canonical conclusions; no normalization. |
| J. Attestation issuance | [`ProducerSnapshotIssuer.issue`](../../src/assessment/producer_snapshot_attestation.py) defaults to historical profile; v3 requires explicit `verification_contract_version`. | All eight local candidate snapshots issued signed v3 evidence after serialized snapshot validation. | Existing key ownership and Ed25519 mechanism remain; no unsigned path. |
| K. Attestation verification | [`ProducerSnapshotVerifier.verify`](../../src/assessment/producer_snapshot_attestation.py) uses the explicitly configured profile and trusted key registry. | All eight v3 local sidecars verified; historical tests and tamper tests passed. | Cross-profile, digest, signature, and version mismatches reject. |
| L. Snapshot handoff | [`produce_executive_assessment_snapshot`](../../src/assessment/executive_snapshot_handoff.py) calls orchestration, runtime, object snapshot creation, and serialized validation. | All eight normal snapshots were v2; a direct `ExecutiveRuntime.execute` call rejected local v3. | Handoff has no v3 opt-in and does not issue an attestation sidecar. |
| M. Downstream-facing controls | [`ExecutiveRuntime`](../../src/assessment/executive_runtime.py) and object [`ExecutiveAssessmentSnapshot` validation](../../src/assessment/executive_assessment_snapshot.py) still gate v3. Serialized snapshot validation can validate a correctly versioned local v3 candidate. | Normal path stayed v2; direct runtime rejection was exercised. EIP source inspection found an explicit v2 package constant in `snapshot_compatibility/compatibility.py`. | No downstream v3 admission or client display is established by this record. |

## Local execution and v2/v3 differential

An ephemeral Python 3.14 command exercised eight synthetic, non-PII governed
inputs: critical, two high findings, medium, low, strength, no findings,
observation, and opportunity. Each input passed normal orchestration and
snapshot handoff as v2. The command explicitly called
`build_business_decision_package(...,
governed_package_contract_version="business-decision-package-v3")` with the
same governed result. It then placed that producer-built v3 package in a copy
of the validated v2 snapshot envelope to test the existing envelope shape.
This local assembly was **not** a handoff output or production snapshot. The
complete candidate passed `validate_executive_assessment_snapshot_serialization`
before v3 attestation issuance; no validation or signing gate was bypassed.

For all eight cases, the v2 and v3 governed result objects were equal. After
removing only `recommendationActionText` from each v3 recommendation and
resetting only nested `versionMetadata.contractVersion` to v2, the complete
serialized packages were equal. Thus finding IDs, sequence and severity, risk,
confidence, recommendation classification, decision identifier, table version,
ordering, finding linkage, and summary were identical. V2 recommendation keys
were exactly `findingId`, `recommendationClassification`,
`recommendationDecisionIdentifier`, `recommendationDecisionTableVersion`.
V3 appended exactly `recommendationActionText` as field five. All eight approved
rule IDs were observed and every text value equaled the immutable mapping. A
separate exact comparison confirmed that all eight mapping keys and statement
strings equal the addendum's approved table.
The no-findings case retained its single `monitor` recommendation and null
finding link.

Each local v3 candidate passed package and snapshot serialization validation,
produced `producer-snapshot-attestation-v2` evidence, and verified with an
ephemeral trusted Ed25519 key. Its `governed-conclusions-json-v2` canonical
bytes included action text; the conclusions digest equaled SHA-256 of
`NGUYEN-CONCLUSIONS-v2` plus a zero byte and those bytes. The existing
`executive-runtime-response-v1` envelope and
`nguyen-ai-executive-assessment-v2` input identifiers remained unchanged.
The v2 issuer rejected the v3 candidate. Altering action text after issuance
caused v3 verification to reject it in every local case.

## Negative verification and historical regressions

The eight focused v3 attestation tests in
[`test_producer_snapshot_attestation_v3.py`](../../tests/test_producer_snapshot_attestation_v3.py)
passed. They cover missing, extra, reordered, incorrectly typed, changed-case,
and changed-punctuation action text; unknown and rejection rule IDs; bad table,
assessment, and methodology versions; wrong classification, same-classification
rule exchange, severity, finding links, no-findings representation, and
recommendation order. They also cover cross-version issuer/verifier mismatch,
wrong canonicalization ID, wrong conclusions digest domain, altered snapshot
and conclusions digests, missing sidecar fields, and invalid signatures. The
local eight-case command additionally rejected v3 evidence under the v2
issuer and post-issuance action-text tampering. These are observed rejections,
not evidence of downstream v3 admission.

The focused selection of ten existing/new test modules passed **196 tests**,
including **8 v3 attestation**, **6 golden fixture**, and **27 historical
attestation** tests. The full repository suite passed **513 tests** with
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /opt/homebrew/bin/python3.14 -m
unittest discover -s tests`. No golden expected output changed. Existing v2
orchestration and snapshot handoff continued to return v2. A direct local v3
package passed package validation but was rejected by `ExecutiveRuntime`,
confirming that the normal runtime gate remains closed. Historical v2
canonicalization, signatures, and digest verification passed their existing
tests; no production v3 route was exercised.

## Snapshot compatibility and remaining integration gap

The serialized `executive-runtime-response-v1` envelope can structurally hold
a correctly versioned and validated v3 package without a new envelope or
assessment input schema. The nested `versionMetadata.contractVersion` identifies
v3, and the sidecar binds that version to `producer-snapshot-attestation-v2`
and `governed-conclusions-json-v2`. Historical v2 snapshots remain valid.
Cross-version attestation issuance and verification reject substitution.

The **normal producer path is not integrated for v3**. Specifically,
`orchestrate_executive_assessment` does not pass explicit v3 selection to package
construction; `ExecutiveRuntime._validate_business_decision_package_input` and
`_validate_snapshot_package_version_compatibility` on object snapshots do not
admit v3; `produce_executive_assessment_snapshot` has no v3 selection or
profile-aware attestation handoff. Its default and all observed outputs are v2.
The local candidate was assembled outside these normal path steps solely for
verification, then passed the existing serialized snapshot validator and v3
attestation verifier. EIP source currently fixes governed package admission to
`business-decision-package-v2`; no EIP, trusted EXPLAIN, or Website v3 admission
was implemented or tested here.

## Controlled activation plan — future separate authorization

1. Add an explicit governed v3 opt-in at orchestration, passing it only for
   validated assessment-v2 inputs into the existing package builder. Retain v2
   as the default and reject unsupported or legacy/v3 combinations.
2. Admit the exact v3/assessment-v2 pair in `ExecutiveRuntime` and object
   snapshot compatibility checks while preserving historical v1/v2 gates.
   Carry the selected package version through snapshot handoff. Keep the
   existing envelope and input schema; validate the produced object and its
   serialized form before release.
3. Bind any future producer evidence issuance to the selected package version
   and its corresponding attestation profile. Require successful validation,
   canonicalization, signed issuance, and independent verification before any
   handoff. The current handoff returns only a serialized snapshot, so the
   authorized integration must define where its sidecar is carried and checked.
4. Add integration tests for explicit selection, default v2, two same-rule
   findings, no findings, exact five-field v3 shape, v2/v3 governed equality,
   digest and signature binding, tampering, bad versions, and no downstream
   publication after failure. Preserve and rerun v2 goldens and historical
   attestations.
5. Keep a controlled v2 default as rollback. Disabling a future v3 opt-in may
   return new requests to v2; an explicit v3 request that fails validation or
   attestation must fail closed, never silently downgrade to v2 or emit partial
   content. Preserve historical v2 verification.
6. Separately authorize EIP version and field admission, trusted EXPLAIN fact
   admission with exact-resource authorization, and Website response validation
   and presentation. Maintain tenant and Business Entity isolation, currentness,
   revocation, audit, and content-free DENY controls. Before any production
   activation, obtain passing producer integration, security, compatibility,
   historical regression, and downstream admission evidence plus explicit
   production authority.

## Readiness decision and limits

**READY FOR SEPARATELY AUTHORIZED PRODUCER INTEGRATION.** The local components
passed strict validation, differential comparison, canonicalization,
attestation, and adversarial checks. The normal orchestration, runtime, object
snapshot, and handoff path is still v2-only. This classification is neither
production readiness nor downstream content approval. No AWS or Bedrock call,
deployment, commit, push, runtime modification, or downstream change was part
of this verification.
