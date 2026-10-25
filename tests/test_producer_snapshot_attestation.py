"""Local, ephemeral-key verification of the internal producer sidecar."""

import base64
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cryptography.exceptions import InvalidSignature  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

from assessment.decision_engine import evaluate_assessment_v2  # noqa: E402
from assessment.executive_assessment_snapshot import (  # noqa: E402
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_snapshot_handoff import produce_executive_assessment_snapshot  # noqa: E402
from assessment.producer_snapshot_attestation import (  # noqa: E402
    AttestationError, FailureCode, ProducerSnapshotIssuer,
    ProducerSnapshotVerifier, SIDECAR_FIELDS, _canonical_conclusions,
    _parse_snapshot, _signed_payload,
)
from test_golden_fixture_regression import request  # noqa: E402


RELEASE = "a075a679a053ee9d0eb9a32d7f0ffa2dc796f0da"
ISSUER = "nguyen-ai-assessment"
KEY_ID = "stage1c-ephemeral-test"


def snapshot_bytes(snapshot):
    return json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def changed(raw, change):
    document = json.loads(raw)
    change(document)
    return snapshot_bytes(document)


class ProducerSnapshotAttestationTests(unittest.TestCase):
    def setUp(self):
        self.canonical_input = request(75, "mixed-strong", "two-high")
        produced = produce_executive_assessment_snapshot(self.canonical_input)
        self.assertTrue(produced.is_success, produced.failure)
        self.snapshot = produced.serialized_snapshot
        self.raw = snapshot_bytes(self.snapshot)
        self.key = Ed25519PrivateKey.generate()
        self.issuer = ProducerSnapshotIssuer(
            self.key, issuer_id=ISSUER, key_id=KEY_ID,
            producer_release_commit=RELEASE,
        )
        self.verifier = ProducerSnapshotVerifier(
            trusted_issuer_id=ISSUER, trusted_keys={KEY_ID: self.key.public_key()},
            expected_release_commit=RELEASE,
        )
        self.sidecar = self.issuer.issue(self.raw)

    def assert_failure(self, code, operation):
        with self.assertRaises(AttestationError) as context:
            operation()
        self.assertEqual(context.exception.code, code)
        self.assertEqual(str(context.exception), code.value)

    def resign(self, sidecar):
        sidecar["signature"] = base64.b64encode(
            self.key.sign(_signed_payload(sidecar))
        ).decode("ascii")
        return sidecar

    def test_golden_fixture_passes_frozen_validation_and_receives_exact_sidecar(self):
        self.assertTrue(validate_executive_assessment_snapshot_serialization(self.snapshot).is_valid)
        self.assertEqual(tuple(self.sidecar), SIDECAR_FIELDS)
        self.assertEqual(self.sidecar["verificationContractVersion"],
                         "producer-snapshot-attestation-v1")
        self.assertEqual(self.sidecar["snapshotResponseContractVersion"],
                         "executive-runtime-response-v1")
        self.assertEqual(self.sidecar["packageContractVersion"],
                         "business-decision-package-v2")
        self.assertEqual(self.sidecar["assessmentVersion"],
                         "nguyen-ai-executive-assessment-v2")
        self.assertEqual(self.sidecar["methodologyVersion"],
                         "business-decision-methodology-v1")
        self.assertIsNone(self.verifier.verify(self.raw, self.sidecar))

    def test_snapshot_digest_identity_and_conclusion_digest_are_deterministic(self):
        expected_snapshot_digest = hashlib.sha256(b"NGUYEN-SNAPSHOT-v1\0" + self.raw).hexdigest()
        expected_conclusions = hashlib.sha256(
            b"NGUYEN-CONCLUSIONS-v1\0" + _canonical_conclusions(_parse_snapshot(self.raw))
        ).hexdigest()
        self.assertEqual(self.sidecar["snapshotDigest"], expected_snapshot_digest)
        self.assertEqual(self.sidecar["producerSnapshotIdentity"], "sha256:" + expected_snapshot_digest)
        self.assertEqual(self.sidecar["governedConclusionsDigest"], expected_conclusions)
        self.assertEqual(self.issuer.issue(self.raw), self.sidecar)
        self.assertIsNone(self.verifier.verify(self.raw, self.sidecar))
        self.assertIsNone(self.verifier.verify(self.raw, self.sidecar))

    def test_canonical_groups_and_original_array_orders(self):
        governed = self.snapshot["businessDecisionPackage"]["governedConclusions"]
        canonical = json.loads(_canonical_conclusions(_parse_snapshot(self.raw)))
        self.assertEqual(tuple(canonical), (
            "severityAssignedFindings", "assessmentRisk", "confidence",
            "recommendations", "executiveSummary",
        ))
        self.assertEqual(canonical, governed)
        self.assertEqual([item["findingId"] for item in canonical["severityAssignedFindings"]],
                         [item["findingId"] for item in governed["severityAssignedFindings"]])
        self.assertEqual([item["findingId"] for item in canonical["recommendations"]],
                         [item["findingId"] for item in governed["recommendations"]])
        self.assertEqual(tuple(canonical["executiveSummary"]["sectionText"]), (
            "overall-assessment-overview", "business-capability-highlights",
            "significant-findings", "risk-overview", "confidence-statement",
            "recommended-actions", "closing-assessment-statement",
        ))

    def test_signature_binds_every_sidecar_field_except_signature(self):
        signature = base64.b64decode(self.sidecar["signature"])
        for field in SIDECAR_FIELDS[:-1]:
            with self.subTest(field=field):
                altered = dict(self.sidecar)
                altered[field] += "x"
                with self.assertRaises(InvalidSignature):
                    self.key.public_key().verify(signature, _signed_payload(altered))

    def test_issuer_and_verifier_preserve_snapshot_and_methodology(self):
        before_bytes = bytes(self.raw)
        before_snapshot = copy.deepcopy(self.snapshot)
        before_sidecar = copy.deepcopy(self.sidecar)
        before_methodology = evaluate_assessment_v2(self.canonical_input)
        self.verifier.verify(self.raw, self.sidecar)
        self.assertEqual(self.raw, before_bytes)
        self.assertEqual(self.snapshot, before_snapshot)
        self.assertEqual(self.sidecar, before_sidecar)
        self.assertEqual(evaluate_assessment_v2(self.canonical_input), before_methodology)
        self.assertEqual(snapshot_bytes(produce_executive_assessment_snapshot(
            self.canonical_input).serialized_snapshot), before_bytes)

    def test_each_post_issuance_governed_group_mutation_fails_digest(self):
        edits = (
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["severityAssignedFindings"][0].__setitem__("title", "changed"),
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["assessmentRisk"].__setitem__("riskClassification", "low-risk"),
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["confidence"].__setitem__("confidenceClassification", "low-confidence"),
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["recommendations"][0].__setitem__("recommendationClassification", "monitor"),
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["executiveSummary"]["sectionText"].__setitem__("risk-overview", "changed"),
        )
        for edit in edits:
            with self.subTest(edit=edit):
                altered = changed(self.raw, edit)
                self.assert_failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                                    lambda: self.verifier.verify(altered, self.sidecar))

    def test_invalid_risk_classification_and_decision_id_rejected_before_issuance(self):
        for field, value in (("riskClassification", "unknown-risk"),
                             ("riskDecisionIdentifier", "unknown-rule")):
            with self.subTest(field=field):
                altered = changed(self.raw, lambda d: d["businessDecisionPackage"][
                    "governedConclusions"]["assessmentRisk"].__setitem__(field, value))
                self.assert_failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                                    lambda: self.issuer.issue(altered))

    def test_valid_risk_pair_substitution_fails_against_original_sidecar(self):
        other = produce_executive_assessment_snapshot(request(75, "adequate", "critical"))
        self.assertTrue(other.is_success)
        valid_pair = other.serialized_snapshot["businessDecisionPackage"][
            "governedConclusions"]["assessmentRisk"]
        self.assertNotEqual(valid_pair, self.snapshot["businessDecisionPackage"][
            "governedConclusions"]["assessmentRisk"])
        altered = changed(self.raw, lambda d: d["businessDecisionPackage"][
            "governedConclusions"].__setitem__("assessmentRisk", valid_pair))
        self.assertTrue(validate_executive_assessment_snapshot_serialization(
            json.loads(altered)).is_valid)
        self.assert_failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                            lambda: self.verifier.verify(altered, self.sidecar))

    def test_invalid_confidence_and_summary_rejected_before_issuance(self):
        edits = (
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["confidence"].__setitem__("confidenceClassification", "invalid"),
            lambda d: d["businessDecisionPackage"]["governedConclusions"]["executiveSummary"]["sectionText"].pop("risk-overview"),
        )
        for edit in edits:
            with self.subTest(edit=edit):
                self.assert_failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                                    lambda: self.issuer.issue(changed(self.raw, edit)))

    def test_reordered_findings_and_recommendations_rejected_before_issuance_and_after(self):
        for group in ("severityAssignedFindings", "recommendations"):
            with self.subTest(group=group):
                altered = changed(self.raw, lambda d: d["businessDecisionPackage"][
                    "governedConclusions"][group].reverse())
                self.assert_failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                                    lambda: self.issuer.issue(altered))
                self.assert_failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                                    lambda: self.verifier.verify(altered, self.sidecar))

    def test_modified_snapshot_identity(self):
        altered = dict(self.sidecar, producerSnapshotIdentity="sha256:" + "0" * 64)
        self.assert_failure(FailureCode.SNAPSHOT_IDENTITY_MISMATCH,
                            lambda: self.verifier.verify(self.raw, altered))

    def test_modified_snapshot_digest_with_matching_identity(self):
        altered = dict(self.sidecar, snapshotDigest="0" * 64,
                       producerSnapshotIdentity="sha256:" + "0" * 64)
        self.resign(altered)
        self.assert_failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                            lambda: self.verifier.verify(self.raw, altered))

    def test_modified_conclusions_digest_with_valid_new_signature(self):
        altered = dict(self.sidecar, governedConclusionsDigest="0" * 64)
        self.resign(altered)
        self.assert_failure(FailureCode.CONCLUSIONS_DIGEST_MISMATCH,
                            lambda: self.verifier.verify(self.raw, altered))

    def test_release_and_producer_version_bindings(self):
        for field in ("producerReleaseCommit", "methodologyVersion",
                      "packageContractVersion", "assessmentVersion",
                      "snapshotResponseContractVersion"):
            with self.subTest(field=field):
                altered = dict(self.sidecar)
                altered[field] = "0" * 40 if field == "producerReleaseCommit" else "other-version"
                self.resign(altered)
                self.assert_failure(FailureCode.PRODUCER_VERSION_MISMATCH,
                                    lambda: self.verifier.verify(self.raw, altered))

    def test_modified_key_id_signature_and_unknown_issuer(self):
        self.assert_failure(FailureCode.UNKNOWN_KEY_ID,
                            lambda: self.verifier.verify(self.raw,
                                dict(self.sidecar, keyId="other-key")))
        self.assert_failure(FailureCode.UNKNOWN_ISSUER,
                            lambda: self.verifier.verify(self.raw,
                                dict(self.sidecar, issuerId="other-issuer")))
        raw = bytearray(base64.b64decode(self.sidecar["signature"]))
        raw[-1] ^= 1
        self.assert_failure(FailureCode.INVALID_SIGNATURE,
                            lambda: self.verifier.verify(self.raw,
                                dict(self.sidecar, signature=base64.b64encode(raw).decode("ascii"))))

    def test_untrusted_and_caller_supplied_replacement_keys(self):
        wrong_key = Ed25519PrivateKey.generate().public_key()
        wrong_verifier = ProducerSnapshotVerifier(
            trusted_issuer_id=ISSUER, trusted_keys={KEY_ID: wrong_key},
            expected_release_commit=RELEASE,
        )
        self.assert_failure(FailureCode.INVALID_SIGNATURE,
                            lambda: wrong_verifier.verify(self.raw, self.sidecar))
        self.assert_failure(FailureCode.UNEXPECTED_ATTESTATION_FIELD,
                            lambda: self.verifier.verify(self.raw,
                                dict(self.sidecar, publicKey="attacker-key")))
        with self.assertRaises(TypeError):
            self.verifier.verify(self.raw, self.sidecar, public_key=wrong_key)

    def test_missing_unexpected_and_malformed_sidecar_fields(self):
        self.assert_failure(FailureCode.MISSING_ATTESTATION,
                            lambda: self.verifier.verify(self.raw, None))
        missing = dict(self.sidecar)
        missing.pop("keyId")
        self.assert_failure(FailureCode.MISSING_ATTESTATION_FIELD,
                            lambda: self.verifier.verify(self.raw, missing))
        self.assert_failure(FailureCode.UNEXPECTED_ATTESTATION_FIELD,
                            lambda: self.verifier.verify(self.raw,
                                dict(self.sidecar, extra="value")))
        self.assert_failure(FailureCode.MALFORMED_ATTESTATION,
                            lambda: self.verifier.verify(self.raw,
                                dict(self.sidecar, signature="not base64!")))

    def test_strict_snapshot_json_rejections(self):
        duplicate = self.raw.replace(b'"riskClassification":',
                                     b'"riskClassification":"duplicate","riskClassification":', 1)
        nonfinite = self.raw.replace(b'"findingCount":2', b'"findingCount":NaN', 1)
        overflow = self.raw.replace(b'"findingCount":2', b'"findingCount":1e999', 1)
        cases = (b"\xff", b"\xef\xbb\xbf" + self.raw, self.raw[:-1],
                 self.raw + b"{}", b"[]", duplicate, nonfinite, overflow,
                 self.raw.replace(b'"findingCount":2', b'"findingCount":Infinity', 1))
        for raw in cases:
            with self.subTest(raw=raw[:30]):
                self.assert_failure(FailureCode.INVALID_SNAPSHOT_ENCODING,
                                    lambda: self.issuer.issue(raw))
                self.assert_failure(FailureCode.INVALID_SNAPSHOT_ENCODING,
                                    lambda: self.verifier.verify(raw, self.sidecar))

    def test_strict_governed_numeric_type_even_if_frozen_validator_accepts_equality(self):
        empty = produce_executive_assessment_snapshot(request(50, "adequate", "none"))
        self.assertTrue(empty.is_success)
        altered = copy.deepcopy(empty.serialized_snapshot)
        altered["businessDecisionPackage"]["governedConclusions"]["executiveSummary"]["findingCount"] = False
        self.assertTrue(validate_executive_assessment_snapshot_serialization(altered).is_valid)
        self.assert_failure(FailureCode.INVALID_CONCLUSION_STRUCTURE,
                            lambda: self.issuer.issue(snapshot_bytes(altered)))

    def test_sidecar_field_types_are_strict(self):
        for field in SIDECAR_FIELDS:
            with self.subTest(field=field):
                altered = dict(self.sidecar)
                altered[field] = 1
                self.assert_failure(FailureCode.MALFORMED_ATTESTATION,
                                    lambda: self.verifier.verify(self.raw, altered))

    def test_explicit_null_finding_id_for_empty_findings(self):
        empty = produce_executive_assessment_snapshot(request(50, "adequate", "none"))
        self.assertTrue(empty.is_success)
        raw = snapshot_bytes(empty.serialized_snapshot)
        sidecar = self.issuer.issue(raw)
        canonical = json.loads(_canonical_conclusions(_parse_snapshot(raw)))
        self.assertEqual(canonical["severityAssignedFindings"], [])
        self.assertIsNone(canonical["recommendations"][0]["findingId"])
        self.assertIsNone(self.verifier.verify(raw, sidecar))

    def test_malformed_unicode_is_rejected_before_signing_or_verification(self):
        malformed_snapshot = self.raw.replace(
            b'"riskClassification":"elevated-risk"',
            b'"riskClassification":"\\ud800"', 1,
        )
        self.assert_failure(FailureCode.INVALID_SNAPSHOT_ENCODING,
                            lambda: self.issuer.issue(malformed_snapshot))
        malformed_sidecar = dict(self.sidecar, methodologyVersion="\ud800")
        self.assert_failure(FailureCode.MALFORMED_ATTESTATION,
                            lambda: self.verifier.verify(self.raw, malformed_sidecar))

    def test_frozen_producer_validation_cannot_be_skipped(self):
        with patch('assessment.producer_snapshot_attestation.validate_executive_assessment_snapshot_serialization',
                   return_value=SimpleNamespace(is_valid=False)):
            self.assert_failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                                lambda: self.issuer.issue(self.raw))
        with patch('assessment.producer_snapshot_attestation.validate_executive_assessment_snapshot_serialization',
                   return_value=None):
            self.assert_failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                                lambda: self.issuer.issue(self.raw))
        with patch('assessment.producer_snapshot_attestation.validate_executive_assessment_snapshot_serialization',
                   side_effect=RuntimeError('validator unavailable')):
            self.assert_failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                                lambda: self.issuer.issue(self.raw))
        with self.assertRaises(TypeError):
            self.issuer.issue(self.raw, validated=True)

    def test_unsupported_producer_contract_and_methodology(self):
        for path, value in (
            (("responseContractVersion",), "other-response"),
            (("businessDecisionPackage", "versionMetadata", "contractVersion"), "business-decision-package-v1"),
            (("businessDecisionPackage", "versionMetadata", "methodologyVersion"), "other-methodology"),
        ):
            with self.subTest(path=path):
                def edit(document):
                    target = document
                    for key in path[:-1]:
                        target = target[key]
                    target[path[-1]] = value
                self.assert_failure(FailureCode.UNSUPPORTED_PRODUCER_CONTRACT,
                                    lambda: self.issuer.issue(changed(self.raw, edit)))

    def test_unsupported_attestation_version_digest_and_canonicalization(self):
        for field, value, code in (
            ("verificationContractVersion", "v2", FailureCode.UNSUPPORTED_ATTESTATION_VERSION),
            ("digestAlgorithm", "SHA-512", FailureCode.MALFORMED_ATTESTATION),
            ("canonicalizationId", "other", FailureCode.MALFORMED_ATTESTATION),
        ):
            with self.subTest(field=field):
                self.assert_failure(code, lambda: self.verifier.verify(
                    self.raw, dict(self.sidecar, **{field: value})))

    def test_valid_sidecar_cannot_be_reused_with_different_snapshot(self):
        other = produce_executive_assessment_snapshot(request(50, "adequate", "medium"))
        self.assertTrue(other.is_success)
        self.assert_failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                            lambda: self.verifier.verify(
                                snapshot_bytes(other.serialized_snapshot), self.sidecar))

    def test_whitespace_byte_change_alters_identity_without_changing_business_values(self):
        altered = json.dumps(self.snapshot, ensure_ascii=False).encode("utf-8")
        self.assertEqual(json.loads(altered), json.loads(self.raw))
        self.assertNotEqual(self.issuer.issue(altered)["snapshotDigest"],
                            self.sidecar["snapshotDigest"])
        self.assert_failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                            lambda: self.verifier.verify(altered, self.sidecar))


if __name__ == "__main__":
    unittest.main()
