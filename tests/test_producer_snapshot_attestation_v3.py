"""Local-only v3 producer validation and attestation with synthetic evidence."""

import base64
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from assessment.business_decision_package_validation import (
    validate_business_decision_package_serialization,
)
from assessment.executive_assessment_snapshot import (
    validate_executive_assessment_snapshot_serialization,
)
from assessment.executive_snapshot_handoff import produce_executive_assessment_snapshot
from assessment.producer_snapshot_attestation import (
    AttestationError, FailureCode, ProducerSnapshotIssuer, ProducerSnapshotVerifier,
    V3_VERIFICATION_CONTRACT_VERSION, V3_CANONICALIZATION_ID,
    _canonical_conclusions, _parse_snapshot, _signed_payload,
)
from test_governed_producer_contract import local_v3_package
from test_golden_fixture_regression import request


RELEASE = "a075a679a053ee9d0eb9a32d7f0ffa2dc796f0da"


def encode(snapshot):
    return json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def local_snapshot(canonical):
    produced = produce_executive_assessment_snapshot(canonical)
    assert produced.is_success, produced.failure
    _, v3 = local_v3_package(canonical)
    snapshot = copy.deepcopy(produced.serialized_snapshot)
    snapshot["businessDecisionPackage"] = v3.to_dict()
    return snapshot


class ProducerSnapshotAttestationV3Tests(unittest.TestCase):
    def setUp(self):
        self.key = Ed25519PrivateKey.generate()
        self.issuer = ProducerSnapshotIssuer(
            self.key, issuer_id="nguyen-ai-assessment", key_id="local-v3-test",
            producer_release_commit=RELEASE,
            verification_contract_version=V3_VERIFICATION_CONTRACT_VERSION,
        )
        self.verifier = ProducerSnapshotVerifier(
            trusted_issuer_id="nguyen-ai-assessment",
            trusted_keys={"local-v3-test": self.key.public_key()},
            expected_release_commit=RELEASE,
            verification_contract_version=V3_VERIFICATION_CONTRACT_VERSION,
        )
        self.snapshot = local_snapshot(request(75, "mixed-strong", "two-high"))
        self.raw = encode(self.snapshot)

    def failure(self, code, operation):
        with self.assertRaises(AttestationError) as context:
            operation()
        self.assertEqual(context.exception.code, code)

    def altered(self, edit):
        value = copy.deepcopy(self.snapshot)
        edit(value)
        return encode(value)

    def recommendations(self, snapshot):
        return snapshot["businessDecisionPackage"]["governedConclusions"]["recommendations"]

    def test_valid_v3_profile_canonical_bytes_and_digests(self):
        self.assertTrue(validate_executive_assessment_snapshot_serialization(self.snapshot).is_valid)
        sidecar = self.issuer.issue(self.raw)
        self.assertEqual(sidecar["verificationContractVersion"], V3_VERIFICATION_CONTRACT_VERSION)
        self.assertEqual(sidecar["canonicalizationId"], V3_CANONICALIZATION_ID)
        self.assertEqual(sidecar["packageContractVersion"], "business-decision-package-v3")
        self.assertEqual(sidecar["assessmentVersion"], "nguyen-ai-executive-assessment-v2")
        self.assertEqual(sidecar["snapshotResponseContractVersion"], "executive-runtime-response-v1")
        canonical = _canonical_conclusions(_parse_snapshot(self.raw), V3_VERIFICATION_CONTRACT_VERSION)
        self.assertEqual(json.loads(canonical), self.snapshot["businessDecisionPackage"]["governedConclusions"])
        self.assertIn(b'recommendationActionText', canonical)
        self.assertEqual(sidecar["governedConclusionsDigest"], hashlib.sha256(
            b"NGUYEN-CONCLUSIONS-v2\0" + canonical).hexdigest())
        self.assertEqual(sidecar["snapshotDigest"], hashlib.sha256(
            b"NGUYEN-SNAPSHOT-v1\0" + self.raw).hexdigest())
        self.assertEqual(sidecar, self.issuer.issue(self.raw))
        self.assertIsNone(self.verifier.verify(self.raw, sidecar))
        self.assertIsNone(self.verifier.verify(self.raw, sidecar))

    def test_complete_no_findings_has_single_null_link(self):
        snapshot = local_snapshot(request(50, "adequate", "none"))
        rows = self.recommendations(snapshot)
        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0]["findingId"])
        self.assertEqual(rows[0]["recommendationClassification"], "monitor")
        self.assertEqual(rows[0]["recommendationDecisionIdentifier"], "recommendation-v1-no-findings-monitor")
        raw = encode(snapshot)
        self.assertIsNone(self.verifier.verify(raw, self.issuer.issue(raw)))

    def test_two_findings_sharing_rule_keep_distinct_links_and_order(self):
        rows = self.recommendations(self.snapshot)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["recommendationDecisionIdentifier"], rows[1]["recommendationDecisionIdentifier"])
        self.assertNotEqual(rows[0]["findingId"], rows[1]["findingId"])
        self.assertEqual([row["findingId"] for row in rows], [
            row["findingId"] for row in self.snapshot["businessDecisionPackage"]
            ["governedConclusions"]["severityAssignedFindings"]])

    def test_v3_rejects_shape_type_and_text_tampering(self):
        edits = (
            lambda d: self.recommendations(d)[0].pop("recommendationActionText"),
            lambda d: self.recommendations(d)[0].__setitem__("extra", "x"),
            lambda d: self.recommendations(d)[0].update({"recommendationActionText": None}),
            lambda d: self.recommendations(d)[0].update({"recommendationActionText": ""}),
            lambda d: self.recommendations(d)[0].update({"recommendationActionText":
                self.recommendations(d)[0]["recommendationActionText"][:-1]}),
            lambda d: self.recommendations(d)[0].update({"recommendationActionText":
                self.recommendations(d)[0]["recommendationActionText"].lower()}),
            lambda d: self.recommendations(d)[0].update({"recommendationDecisionIdentifier": "unknown-rule"}),
            lambda d: self.recommendations(d)[0].update({"recommendationDecisionIdentifier": "recommendation-v1-reject-missing-risk"}),
            lambda d: self.recommendations(d)[0].update({"recommendationDecisionTableVersion": "other-version"}),
            lambda d: self.recommendations(d)[0].update({"recommendationClassification": "monitor"}),
            lambda d: self.recommendations(d)[0].update({"findingId": None}),
            lambda d: self.recommendations(d)[0].update({"findingId": "dangling"}),
            lambda d: self.recommendations(d).reverse(),
            lambda d: d["businessDecisionPackage"]["versionMetadata"].update({"methodologyVersion": "other"}),
            lambda d: d["businessDecisionPackage"]["versionMetadata"].update({"assessmentVersion": "other"}),
            lambda d: self.recommendations(d).__setitem__(0, {
                key: self.recommendations(d)[0][key] for key in reversed(self.recommendations(d)[0])}),
        )
        for index, edit in enumerate(edits):
            with self.subTest(edit=edit):
                raw = self.altered(edit)
                expected = (FailureCode.UNSUPPORTED_PRODUCER_CONTRACT if index in (13, 14)
                            else FailureCode.PRODUCER_VALIDATION_FAILURE)
                self.failure(expected,
                             lambda: self.issuer.issue(raw))

    def test_v3_rejects_wrong_severity_and_same_classification_rule(self):
        snapshot = local_snapshot(request(50, "adequate", "medium"))
        row = self.recommendations(snapshot)[0]
        row["recommendationDecisionIdentifier"] = "recommendation-v1-deficiency-low-planned"
        row["recommendationActionText"] = "Plan an improvement for the identified limited weakness."
        self.assertFalse(validate_business_decision_package_serialization(
            snapshot["businessDecisionPackage"]).is_valid)
        self.failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                     lambda: self.issuer.issue(encode(snapshot)))
        other = local_snapshot(request(50, "adequate", "medium"))
        other["businessDecisionPackage"]["governedConclusions"]["severityAssignedFindings"][0]["severityClassification"] = "low"
        self.failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                     lambda: self.issuer.issue(encode(other)))

    def test_no_findings_rule_cannot_be_reused_with_findings(self):
        altered = copy.deepcopy(self.snapshot)
        row = self.recommendations(altered)[0]
        row["recommendationDecisionIdentifier"] = "recommendation-v1-no-findings-monitor"
        row["recommendationClassification"] = "monitor"
        row["recommendationActionText"] = (
            "Monitor the assessment context after this completed assessment, which generated no findings."
        )
        self.failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                     lambda: self.issuer.issue(encode(altered)))
        empty = local_snapshot(request(50, "adequate", "none"))
        self.recommendations(empty)[0]["findingId"] = "invented-finding"
        self.failure(FailureCode.PRODUCER_VALIDATION_FAILURE,
                     lambda: self.issuer.issue(encode(empty)))

    def test_cross_version_package_and_profile_rejection(self):
        v2_snapshot = produce_executive_assessment_snapshot(request(50, "adequate", "none"))
        self.assertTrue(v2_snapshot.is_success)
        v2_raw = encode(v2_snapshot.serialized_snapshot)
        v2_issuer = ProducerSnapshotIssuer(
            self.key, issuer_id="nguyen-ai-assessment", key_id="local-v3-test",
            producer_release_commit=RELEASE,
        )
        v2_verifier = ProducerSnapshotVerifier(
            trusted_issuer_id="nguyen-ai-assessment",
            trusted_keys={"local-v3-test": self.key.public_key()},
            expected_release_commit=RELEASE,
        )
        self.failure(FailureCode.UNSUPPORTED_PRODUCER_CONTRACT,
                     lambda: self.issuer.issue(v2_raw))
        self.failure(FailureCode.UNSUPPORTED_PRODUCER_CONTRACT,
                     lambda: v2_issuer.issue(self.raw))
        v3_sidecar = self.issuer.issue(self.raw)
        v2_sidecar = v2_issuer.issue(v2_raw)
        self.failure(FailureCode.UNSUPPORTED_ATTESTATION_VERSION,
                     lambda: self.verifier.verify(self.raw, v2_sidecar))
        self.failure(FailureCode.UNSUPPORTED_ATTESTATION_VERSION,
                     lambda: v2_verifier.verify(v2_raw, v3_sidecar))
        self.failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                     lambda: self.verifier.verify(v2_raw, v3_sidecar))
        self.failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                     lambda: v2_verifier.verify(self.raw, v2_sidecar))
        self.assertIsNone(v2_verifier.verify(v2_raw, v2_sidecar))

    def test_v3_attestation_tamper_and_domain_rejection(self):
        sidecar = self.issuer.issue(self.raw)
        self.failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                     lambda: self.verifier.verify(self.altered(
                         lambda d: self.recommendations(d)[0].update({"findingId": "tampered"})), sidecar))
        self.failure(FailureCode.SNAPSHOT_DIGEST_MISMATCH,
                     lambda: self.verifier.verify(self.altered(
                         lambda d: self.recommendations(d)[0].update({"recommendationActionText": "changed"})), sidecar))
        for field, value, code in (
            ("verificationContractVersion", "producer-snapshot-attestation-v1", FailureCode.UNSUPPORTED_ATTESTATION_VERSION),
            ("canonicalizationId", "governed-conclusions-json-v1", FailureCode.MALFORMED_ATTESTATION),
            ("packageContractVersion", "business-decision-package-v2", FailureCode.PRODUCER_VERSION_MISMATCH),
            ("governedConclusionsDigest", "0" * 64, FailureCode.CONCLUSIONS_DIGEST_MISMATCH),
        ):
            with self.subTest(field=field):
                altered = dict(sidecar, **{field: value})
                altered["signature"] = base64.b64encode(self.key.sign(
                    _signed_payload(altered, V3_VERIFICATION_CONTRACT_VERSION))).decode("ascii")
                self.failure(code, lambda: self.verifier.verify(self.raw, altered))
        wrong_conclusions_domain = dict(sidecar)
        canonical = _canonical_conclusions(_parse_snapshot(self.raw), V3_VERIFICATION_CONTRACT_VERSION)
        wrong_conclusions_domain["governedConclusionsDigest"] = hashlib.sha256(
            b"NGUYEN-CONCLUSIONS-v1\0" + canonical).hexdigest()
        wrong_conclusions_domain["signature"] = base64.b64encode(self.key.sign(
            _signed_payload(wrong_conclusions_domain, V3_VERIFICATION_CONTRACT_VERSION))).decode("ascii")
        self.failure(FailureCode.CONCLUSIONS_DIGEST_MISMATCH,
                     lambda: self.verifier.verify(self.raw, wrong_conclusions_domain))
        bad = dict(sidecar)
        bad["signature"] = base64.b64encode(b"\0" * 64).decode("ascii")
        self.failure(FailureCode.INVALID_SIGNATURE,
                     lambda: self.verifier.verify(self.raw, bad))
        wrong_domain = dict(sidecar)
        wrong_domain["signature"] = base64.b64encode(self.key.sign(
            _signed_payload(wrong_domain))).decode("ascii")
        self.failure(FailureCode.INVALID_SIGNATURE,
                     lambda: self.verifier.verify(self.raw, wrong_domain))
        missing = dict(sidecar)
        missing.pop("canonicalizationId")
        self.failure(FailureCode.MISSING_ATTESTATION_FIELD,
                     lambda: self.verifier.verify(self.raw, missing))
        self.failure(FailureCode.UNSUPPORTED_ATTESTATION_VERSION,
                     lambda: ProducerSnapshotIssuer(
                         self.key, issuer_id="nguyen-ai-assessment", key_id="local-v3-test",
                         producer_release_commit=RELEASE,
                         verification_contract_version="unsupported"))


if __name__ == "__main__":
    unittest.main()
