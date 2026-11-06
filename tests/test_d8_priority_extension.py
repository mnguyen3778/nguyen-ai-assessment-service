"""Synthetic-only extension contract and frozen producer separation tests."""

import itertools
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.d8_priority_extension import (  # noqa: E402
    CANONICALIZATION_ID, DESIGNATION, DIGEST_ALGORITHM, MAX_ARTIFACT_BYTES,
    SCHEMA_ID, SCHEMA_VERSION, build_local_d8_extension,
    validate_local_d8_extension,
)
from assessment.decision_engine import evaluate_assessment_v2  # noqa: E402
from assessment.executive_snapshot_handoff import produce_executive_assessment_snapshot  # noqa: E402
from assessment.governed_assessment_input import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION_V2, ValidatedCanonicalExecutiveAssessmentInputV2,
)
from assessment.local_d8_priority import (  # noqa: E402
    BLOCKED_REQUIRED_EVIDENCE, INSUFFICIENT_CONFIDENCE, NO_FINDINGS_MONITOR,
    PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED, REJECTED_INVALID_ASSERTION,
    METHODOLOGY_VERSION as D8_METHODOLOGY_VERSION,
    RULE_TABLE_VERSION as D8_RULE_TABLE_VERSION,
)
from assessment.local_d8_producer_adapter import (  # noqa: E402
    LocalD8ProducerRequest, LocalSyntheticProducerBinding, evaluate_local_d8_producer,
)
from assessment.local_priority_assertions import RecommendationInstance, SyntheticContext  # noqa: E402
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402
from test_golden_fixture_regression import answers, evidence  # noqa: E402
from test_local_d8_priority import DRIVERS, ELIGIBLE_IDS, ORACLE, PAIRS, RULE, VALUES  # noqa: E402
from test_local_d8_producer_adapter import producer_request, with_states  # noqa: E402


def monitor_request():
    canonical = ValidatedCanonicalExecutiveAssessmentInputV2(
        EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
        answers(75), evidence("strong"), ())
    producer = evaluate_assessment_v2(canonical)
    rec = producer.recommendations[0]
    context = SyntheticContext("snapshot-1", "assessment-1", (
        RecommendationInstance("monitor-1", None, rec.recommendation_decision_identifier),
    ), {}, {})
    binding = LocalSyntheticProducerBinding(
        "assessment-1", "snapshot-1", None, "monitor-1",
        rec.recommendation_decision_identifier, rec.recommendation_decision_table_version)
    return LocalD8ProducerRequest(canonical, producer, context, [], binding)


def artifact(request):
    result = evaluate_local_d8_producer(request)
    blob = build_local_d8_extension(request, result)
    return result, blob, validate_local_d8_extension(blob)


def edited(blob, *, payload=None, integrity=None):
    value = json.loads(blob)
    if payload:
        value["payload"].update(payload)
    if integrity:
        value["integrity"].update(integrity)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()


class LocalD8ExtensionTests(unittest.TestCase):
    def test_assigned_schema_versions_provenance_integrity_and_no_mutation(self):
        request = producer_request()
        result = evaluate_local_d8_producer(request)
        original_records = [dict(record) for record in request.synthetic_assertions]
        original_findings = request.governed_result.findings
        blob = build_local_d8_extension(request, result)
        self.assertEqual(blob, build_local_d8_extension(request, result))
        self.assertEqual(result, evaluate_local_d8_producer(request))
        self.assertEqual(request.synthetic_assertions, original_records)
        self.assertEqual(request.governed_result.findings, original_findings)
        value = validate_local_d8_extension(blob)
        p = value["payload"]
        self.assertEqual((p["schemaId"], p["schemaVersion"], p["designation"]),
                         (SCHEMA_ID, SCHEMA_VERSION, DESIGNATION))
        self.assertEqual((p["assessmentIdentity"], p["snapshotIdentity"], p["findingId"],
                          p["recommendationInstanceIdentity"]),
                         ("assessment-1", "snapshot-1", "finding-1", "instance-1"))
        self.assertEqual((p["assessmentVersion"], p["producerMethodologyVersion"]),
                         (EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION))
        self.assertEqual((p["d8MethodologyVersion"], p["d8RuleTableVersion"]),
                         (D8_METHODOLOGY_VERSION, D8_RULE_TABLE_VERSION))
        self.assertEqual((p["recommendationDecisionIdentifier"],
                          p["recommendationDecisionTableVersion"]),
                         (request.binding.recommendation_decision_identifier,
                          request.binding.recommendation_decision_table_version))
        self.assertEqual((p["confidenceClassification"], p["confidenceDecisionIdentifier"],
                          p["confidenceDecisionTableVersion"]),
                         (request.governed_result.confidence.confidence_classification,
                          request.governed_result.confidence.confidence_decision_identifier,
                          request.governed_result.confidence.confidence_decision_table_version))
        self.assertEqual((p["outcome"], p["priority"], p["winningRuleIds"],
                          p["reviewRequired"], p["confidenceGate"]),
                         (PRIORITY_ASSIGNED, result.priority, list(result.matched_rule_ids),
                          False, "PASSED"))
        self.assertEqual(p["validatedAssertionIds"], list(result.validated_assertion_ids))
        self.assertEqual([e["assertionId"] for e in p["evidenceProvenance"]],
                         p["validatedAssertionIds"])
        self.assertEqual(value["integrity"]["canonicalizationId"], CANONICALIZATION_ID)
        self.assertEqual(value["integrity"]["digestAlgorithm"], DIGEST_ALGORITHM)
        self.assertRegex(value["integrity"]["payloadDigest"], r"^sha256:[0-9a-f]{64}$")

    def test_pnd_complete_trace_and_missing_values(self):
        request = with_states(producer_request(), ("A", "A", "A"))
        result, _, value = artifact(request)
        p = value["payload"]
        self.assertEqual(p["outcome"], PRIORITY_NOT_DETERMINED)
        self.assertNotIn("priority", p)
        self.assertNotIn("winningRuleIds", p)
        self.assertTrue(p["reviewRequired"])
        self.assertEqual(p["excludedRuleIds"], list(result.excluded_rule_ids))
        self.assertEqual(p["reviewReference"], result.review_reference)
        self.assertEqual(p["evaluatedDriverValues"], [
            {"driverId": driver, "assertedValue": state}
            for driver, state in result.evaluated_driver_values])
        missing = with_states(producer_request(), (None, "A", None))
        missing_result, _, missing_value = artifact(missing)
        self.assertEqual(missing_result.outcome, PRIORITY_NOT_DETERMINED)
        self.assertEqual([item["assertedValue"] for item in
                          missing_value["payload"]["evaluatedDriverValues"]],
                         [None, "executive-action-affirmed-absent", None])
        self.assertEqual(missing_value["payload"]["reviewReference"],
                         missing_result.review_reference)

    def test_d7_null_finding_and_monitor_separation(self):
        request = monitor_request()
        result, _, value = artifact(request)
        self.assertEqual(result.outcome, NO_FINDINGS_MONITOR)
        p = value["payload"]
        self.assertIsNone(p["findingId"])
        self.assertEqual(p["recommendationInstanceIdentity"], "monitor-1")
        self.assertEqual(p["confidenceGate"], "NOT_APPLICABLE_NO_FINDINGS")
        self.assertEqual(p["validatedAssertionIds"], [])
        self.assertEqual(p["evidenceProvenance"], [])
        self.assertNotIn("priority", p)
        self.assertNotIn("reviewReference", p)
        self.assertFalse(p["reviewRequired"])

    def test_all_84_independent_document_43_cases(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "PND": 0}
        tuples = tuple(itertools.product("PA", "TUA", "PA"))
        for pair, row, eligible in zip(PAIRS, ORACLE, ELIGIBLE_IDS):
            base = producer_request(pair)
            for states, expected in zip(tuples, row):
                with self.subTest(pair=pair, states=states):
                    request = with_states(base, states)
                    result, blob, value = artifact(request)
                    p = value["payload"]
                    self.assertEqual(blob, build_local_d8_extension(request, result))
                    self.assertEqual((p["assessmentIdentity"], p["snapshotIdentity"],
                                      p["findingId"], p["recommendationInstanceIdentity"]),
                                     ("assessment-1", "snapshot-1", "finding-1", "instance-1"))
                    if expected == "-":
                        counts["PND"] += 1
                        self.assertEqual(p["outcome"], PRIORITY_NOT_DETERMINED)
                        self.assertNotIn("priority", p)
                        self.assertEqual(p["excludedRuleIds"], sorted(eligible))
                        self.assertEqual(p["evaluatedDriverValues"], [
                            {"driverId": driver, "assertedValue": vocabulary[state]}
                            for driver, vocabulary, state in zip(DRIVERS, VALUES, states)])
                        self.assertEqual(p["reviewReference"], result.review_reference)
                    else:
                        level, rule_id = RULE[expected.split("+")[0]]
                        counts[level] += 1
                        self.assertEqual((p["outcome"], p["priority"], p["winningRuleIds"]),
                                         (PRIORITY_ASSIGNED, level, [rule_id]))
        self.assertEqual(counts, {"critical": 2, "high": 14, "medium": 1,
                                  "low": 4, "PND": 63})

    def test_ineligible_diagnostics_and_invalid_request_result_bindings(self):
        blocked = with_states(producer_request(), ("P", "T", None))
        rejected = replace(producer_request(), binding=replace(
            producer_request().binding, snapshot_identity="wrong"))
        insufficient = producer_request(profile="limitation")
        for request, status in ((blocked, BLOCKED_REQUIRED_EVIDENCE),
                                (rejected, REJECTED_INVALID_ASSERTION),
                                (insufficient, INSUFFICIENT_CONFIDENCE)):
            with self.subTest(status=status):
                result = evaluate_local_d8_producer(request)
                self.assertEqual(result.outcome, status)
                with self.assertRaises(ValueError):
                    build_local_d8_extension(request, result)
        request = producer_request()
        result = evaluate_local_d8_producer(request)
        changes = (
            replace(request, binding=replace(request.binding, assessment_identity="")),
            replace(request, binding=replace(request.binding, snapshot_identity="wrong")),
            replace(request, binding=replace(request.binding,
                    recommendation_instance_identity="wrong")),
            replace(request, binding=replace(request.binding,
                    recommendation_decision_table_version="wrong")),
        )
        for changed in changes:
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    build_local_d8_extension(changed, result)
        for changed in (
            replace(result, methodology_version="unsupported"),
            replace(result, rule_table_version="unsupported"),
            replace(result, priority="override"),
            replace(result, matched_rule_ids=("OVERRIDE",)),
            replace(result, outcome="UNSUPPORTED"),
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    build_local_d8_extension(request, changed)

    def test_strict_json_and_integrity_failures(self):
        _, blob, _ = artifact(producer_request())
        for bad in (
            edited(blob, payload={"schemaVersion": 2}),
            edited(blob, payload={"d8MethodologyVersion": "other"}),
            edited(blob, payload={"d8RuleTableVersion": "other"}),
            edited(blob, payload={"designation": "PRODUCTION"}),
            edited(blob, payload={"productionAuthorized": True}),
            edited(blob, payload={"priority": "low"}),
            edited(blob, payload={"winningRuleIds": ["G-H1"]}),
            edited(blob, payload={"assessmentIdentity": "other"}),
            edited(blob, integrity={"payloadDigest": "sha256:" + "0" * 64}),
            edited(blob, integrity={"payloadDigest": "malformed"}),
            b"{}", b"not-json", b"\xef\xbb\xbf" + blob, b"{\"payload\":1,\"payload\":2}",
            blob.replace(b'"schemaVersion":1', b'"schemaVersion":NaN'),
            blob.replace(b'"schemaVersion":1', b'"schemaVersion":Infinity'),
            blob.replace(b'"schemaVersion":1', b'"schemaVersion":1.0'),
            blob.replace(b'"schemaVersion":1', b'"schemaVersion":[]'),
            blob.replace(b'"outcome":"PRIORITY_ASSIGNED"', b'"outcome":[]'),
            blob.replace(b'"schemaVersion":1', b'"schemaVersion":1,"schemaVersion":1'),
            blob + b" ", b"x" * (MAX_ARTIFACT_BYTES + 1),
        ):
            with self.subTest(bad=bad[:80]):
                with self.assertRaises(ValueError):
                    validate_local_d8_extension(bad)
        pnd = artifact(with_states(producer_request(), ("A", "A", "A")))[1]
        for bad in (
            edited(pnd, payload={"excludedRuleIds": []}),
            edited(pnd, payload={"reviewReference": "other"}),
            edited(pnd, payload={"evaluatedDriverValues": []}),
        ):
            with self.assertRaises(ValueError):
                validate_local_d8_extension(bad)
        monitor = artifact(monitor_request())[1]
        for bad in (
            edited(monitor, payload={"findingId": "fabricated"}),
            edited(monitor, payload={"confidenceGate": "PASSED"}),
            edited(monitor, payload={"priority": "low"}),
        ):
            with self.assertRaises(ValueError):
                validate_local_d8_extension(bad)

    def test_malformed_result_and_stale_provenance_fail_closed(self):
        request = producer_request()
        result = evaluate_local_d8_producer(request)
        for changed in (
            replace(result, outcome=[]),
            replace(result, priority=[]),
            replace(result, matched_rule_ids=(["B-C1"],)),
            replace(result, validated_assertion_ids=("wrong",)),
        ):
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    build_local_d8_extension(request, changed)
        records = [dict(item) for item in request.synthetic_assertions]
        records[0]["sourceRevision"] = "stale"
        with self.assertRaises(ValueError):
            build_local_d8_extension(replace(request, synthetic_assertions=records), result)
        pnd_request = with_states(request, ("A", "A", "A"))
        pnd_result = evaluate_local_d8_producer(pnd_request)
        with self.assertRaises(ValueError):
            build_local_d8_extension(pnd_request, replace(
                pnd_result, evaluated_driver_values=(("customer-impact", "impact-present"),)
                + pnd_result.evaluated_driver_values[1:]))

    def test_default_producer_handoff_is_unchanged(self):
        request = producer_request()
        before = produce_executive_assessment_snapshot(request.canonical_input)
        self.assertTrue(before.is_success)
        original = json.dumps(before.serialized_snapshot, ensure_ascii=False,
                              separators=(",", ":"), allow_nan=False).encode()
        self.assertEqual(before.serialized_snapshot["businessDecisionPackage"]
                         ["versionMetadata"]["contractVersion"], "business-decision-package-v2")
        self.assertIsNone(before.attestation_sidecar)
        artifact(request)
        after = produce_executive_assessment_snapshot(request.canonical_input)
        current = json.dumps(after.serialized_snapshot, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode()
        self.assertEqual(current, original)
        self.assertIsNone(after.attestation_sidecar)


if __name__ == "__main__":
    unittest.main()
