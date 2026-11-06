"""Nonproduction adapter-to-extension orchestration tests."""

import ast
import itertools
import sys
import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.d8_priority_extension import (  # noqa: E402
    SCHEMA_VERSION, build_local_d8_extension, validate_local_d8_extension,
)
from assessment.local_d8_extension_pipeline import (  # noqa: E402
    ADAPTER_OUTCOME_INELIGIBLE, EXTENSION_VALIDATION_FAILURE,
    INTEGRITY_VERIFICATION_FAILURE, INVALID_ADAPTER_RESULT, VERIFIED_EXTENSION,
    run_local_d8_extension_pipeline,
)
from assessment.local_d8_priority import (  # noqa: E402
    BLOCKED_REQUIRED_EVIDENCE, INSUFFICIENT_CONFIDENCE, NO_FINDINGS_MONITOR,
    PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED, REJECTED_INVALID_ASSERTION,
)
from assessment.local_d8_producer_adapter import evaluate_local_d8_producer  # noqa: E402
from test_d8_priority_extension import monitor_request  # noqa: E402
from test_local_d8_priority import DRIVERS, ELIGIBLE_IDS, ORACLE, PAIRS, RULE, VALUES  # noqa: E402
from test_local_d8_producer_adapter import producer_request, with_states  # noqa: E402


class LocalD8ExtensionPipelineTests(unittest.TestCase):
    def test_assigned_calls_components_once_and_preserves_source(self):
        request = producer_request()
        original_records = [dict(record) for record in request.synthetic_assertions]
        original_producer = request.governed_result
        expected = evaluate_local_d8_producer(request)
        with (patch("assessment.local_d8_extension_pipeline.evaluate_local_d8_producer",
                    wraps=evaluate_local_d8_producer) as adapter,
              patch("assessment.local_d8_extension_pipeline.build_local_d8_extension",
                    wraps=build_local_d8_extension) as builder,
              patch("assessment.local_d8_extension_pipeline.validate_local_d8_extension",
                    wraps=validate_local_d8_extension) as verifier):
            result = run_local_d8_extension_pipeline(request)
        adapter.assert_called_once_with(request)
        builder.assert_called_once_with(request, result.evaluation)
        verifier.assert_called_once_with(result.artifact)
        self.assertEqual(result.status, VERIFIED_EXTENSION)
        self.assertTrue(result.is_verified)
        self.assertEqual(result.evaluation, expected)
        self.assertEqual(request.synthetic_assertions, original_records)
        self.assertEqual(request.governed_result, original_producer)
        payload = validate_local_d8_extension(result.artifact)["payload"]
        self.assertEqual((payload["priority"], payload["winningRuleIds"]),
                         (expected.priority, list(expected.matched_rule_ids)))
        self.assertEqual((payload["assessmentIdentity"], payload["snapshotIdentity"],
                          payload["findingId"], payload["recommendationInstanceIdentity"]),
                         (expected.assessment_identity, expected.snapshot_identity,
                          expected.finding_id, expected.recommendation_instance_identity))
        self.assertEqual((payload["recommendationDecisionIdentifier"],
                          payload["recommendationDecisionTableVersion"]),
                         (request.binding.recommendation_decision_identifier,
                          request.binding.recommendation_decision_table_version))
        self.assertEqual((payload["confidenceDecisionIdentifier"],
                          payload["confidenceDecisionTableVersion"]),
                         (request.governed_result.confidence.confidence_decision_identifier,
                          request.governed_result.confidence.confidence_decision_table_version))
        self.assertEqual((payload["d8MethodologyVersion"], payload["d8RuleTableVersion"],
                          payload["schemaVersion"]),
                         (expected.methodology_version, expected.rule_table_version,
                          SCHEMA_VERSION))

    def test_pnd_trace_and_d7_monitor_stay_distinct(self):
        pnd_request = with_states(producer_request(), ("A", "A", "A"))
        pnd = run_local_d8_extension_pipeline(pnd_request)
        self.assertTrue(pnd.is_verified)
        self.assertEqual(pnd.evaluation.outcome, PRIORITY_NOT_DETERMINED)
        p = validate_local_d8_extension(pnd.artifact)["payload"]
        self.assertTrue(p["reviewRequired"])
        self.assertNotIn("priority", p)
        self.assertEqual(p["excludedRuleIds"], list(pnd.evaluation.excluded_rule_ids))
        self.assertEqual(p["evaluatedDriverValues"], [
            {"driverId": driver, "assertedValue": value}
            for driver, value in pnd.evaluation.evaluated_driver_values])
        self.assertEqual(p["reviewReference"], pnd.evaluation.review_reference)
        self.assertEqual(p["validatedAssertionIds"], list(pnd.evaluation.validated_assertion_ids))
        monitor = run_local_d8_extension_pipeline(monitor_request())
        self.assertTrue(monitor.is_verified)
        self.assertEqual(monitor.evaluation.outcome, NO_FINDINGS_MONITOR)
        m = validate_local_d8_extension(monitor.artifact)["payload"]
        self.assertIsNone(m["findingId"])
        self.assertEqual(m["recommendationInstanceIdentity"], "monitor-1")
        self.assertEqual(m["validatedAssertionIds"], [])
        self.assertFalse(m["reviewRequired"])
        self.assertNotIn("priority", m)

    def test_ineligible_adapter_results_have_no_artifact(self):
        requests = (
            (with_states(producer_request(), ("P", "T", None)), BLOCKED_REQUIRED_EVIDENCE),
            (replace(producer_request(), binding=replace(
                producer_request().binding, snapshot_identity="wrong")),
             REJECTED_INVALID_ASSERTION),
            (producer_request(profile="limitation"), INSUFFICIENT_CONFIDENCE),
        )
        for request, expected in requests:
            with self.subTest(expected=expected):
                with patch("assessment.local_d8_extension_pipeline.build_local_d8_extension") as builder:
                    result = run_local_d8_extension_pipeline(request)
                builder.assert_not_called()
                self.assertEqual(result.evaluation.outcome, expected)
                self.assertEqual(result.status, ADAPTER_OUTCOME_INELIGIBLE)
                self.assertIsNone(result.artifact)
                self.assertFalse(result.is_verified)

    def test_malformed_request_and_unsupported_version_fail_closed(self):
        malformed = run_local_d8_extension_pipeline(None)
        self.assertEqual(malformed.evaluation.outcome, REJECTED_INVALID_ASSERTION)
        self.assertEqual(malformed.status, ADAPTER_OUTCOME_INELIGIBLE)
        self.assertIsNone(malformed.artifact)
        request = producer_request()
        wrong = replace(request, binding=replace(
            request.binding, recommendation_decision_table_version="unsupported"))
        result = run_local_d8_extension_pipeline(wrong)
        self.assertEqual(result.evaluation.outcome, REJECTED_INVALID_ASSERTION)
        self.assertIsNone(result.artifact)

    def test_unexpected_adapter_result_and_unknown_outcome_fail_closed(self):
        request = producer_request()
        base = evaluate_local_d8_producer(request)
        for fake in (object(), None, replace(base, outcome=[]),
                     replace(base, outcome="UNSUPPORTED")):
            with self.subTest(fake=fake):
                with (patch("assessment.local_d8_extension_pipeline.evaluate_local_d8_producer",
                            return_value=fake) as adapter,
                      patch("assessment.local_d8_extension_pipeline.build_local_d8_extension") as builder):
                    result = run_local_d8_extension_pipeline(request)
                adapter.assert_called_once_with(request)
                builder.assert_not_called()
                self.assertEqual(result.status, INVALID_ADAPTER_RESULT)
                self.assertIsNone(result.artifact)

    def test_extension_and_integrity_failures_have_distinct_statuses(self):
        request = producer_request()
        with patch("assessment.local_d8_extension_pipeline.build_local_d8_extension",
                   side_effect=ValueError("invalid extension")) as builder:
            invalid = run_local_d8_extension_pipeline(request)
        builder.assert_called_once()
        self.assertEqual(invalid.status, EXTENSION_VALIDATION_FAILURE)
        self.assertIsNone(invalid.artifact)
        self.assertFalse(invalid.is_verified)
        with (patch("assessment.local_d8_extension_pipeline.build_local_d8_extension",
                    return_value=b"tampered") as builder,
              patch("assessment.local_d8_extension_pipeline.validate_local_d8_extension",
                    wraps=validate_local_d8_extension) as verifier):
            corrupt = run_local_d8_extension_pipeline(request)
        builder.assert_called_once()
        verifier.assert_called_once_with(b"tampered")
        self.assertEqual(corrupt.status, INTEGRITY_VERIFICATION_FAILURE)
        self.assertIsNone(corrupt.artifact)
        self.assertFalse(corrupt.is_verified)
        with patch("assessment.local_d8_extension_pipeline.build_local_d8_extension",
                   return_value=None):
            invalid_type = run_local_d8_extension_pipeline(request)
        self.assertEqual(invalid_type.status, EXTENSION_VALIDATION_FAILURE)
        self.assertIsNone(invalid_type.artifact)

    def test_verifier_return_must_be_valid_parsed_artifact(self):
        request = producer_request()
        blob = build_local_d8_extension(request, evaluate_local_d8_producer(request))
        valid = validate_local_d8_extension(blob)
        malformed = deepcopy(valid)
        malformed["payload"] = []
        missing_integrity = deepcopy(valid)
        missing_integrity["integrity"] = {}
        invalid_digest = deepcopy(valid)
        invalid_digest["integrity"]["payloadDigest"] = "sha256:" + "x" * 64
        for returned in ({}, [], True, "verified", malformed, missing_integrity,
                         invalid_digest):
            with self.subTest(returned=returned):
                with patch("assessment.local_d8_extension_pipeline.validate_local_d8_extension",
                           return_value=returned):
                    result = run_local_d8_extension_pipeline(request)
                self.assertEqual(result.status, INTEGRITY_VERIFICATION_FAILURE)
                self.assertIsNone(result.artifact)
                self.assertFalse(result.is_verified)

    def test_valid_wrong_outcome_artifacts_are_rejected(self):
        assigned_request = producer_request()
        monitor = monitor_request()
        assigned_blob = build_local_d8_extension(
            assigned_request, evaluate_local_d8_producer(assigned_request))
        monitor_blob = build_local_d8_extension(
            monitor, evaluate_local_d8_producer(monitor))
        for request, wrong_blob in ((assigned_request, monitor_blob),
                                    (monitor, assigned_blob)):
            with self.subTest(request=request.binding.recommendation_instance_identity):
                with patch("assessment.local_d8_extension_pipeline.build_local_d8_extension",
                           return_value=wrong_blob):
                    result = run_local_d8_extension_pipeline(request)
                self.assertEqual(result.status, INTEGRITY_VERIFICATION_FAILURE)
                self.assertIsNone(result.artifact)
                self.assertFalse(result.is_verified)

    def test_verified_payload_must_match_request_and_assigned_result(self):
        request = producer_request()
        result = evaluate_local_d8_producer(request)
        baseline = validate_local_d8_extension(build_local_d8_extension(request, result))
        changes = (
            ("schemaId", "other"), ("schemaVersion", 2),
            ("designation", "PRODUCTION"),
            ("assessmentIdentity", "other"), ("assessmentVersion", "other"),
            ("producerMethodologyVersion", "other"), ("snapshotIdentity", "other"),
            ("findingId", "other"), ("recommendationInstanceIdentity", "other"),
            ("recommendationDecisionIdentifier", "other"),
            ("recommendationDecisionTableVersion", "other"),
            ("confidenceClassification", "other"),
            ("confidenceDecisionIdentifier", "other"),
            ("confidenceDecisionTableVersion", "other"),
            ("d8MethodologyVersion", "other"), ("d8RuleTableVersion", "other"),
            ("outcome", NO_FINDINGS_MONITOR), ("priority", "low"),
            ("winningRuleIds", ["G-H1"]), ("reviewRequired", True),
            ("validatedAssertionIds", []),
            ("evidenceProvenance", []),
        )
        for field, changed in changes:
            with self.subTest(field=field):
                altered = deepcopy(baseline)
                altered["payload"][field] = changed
                with patch("assessment.local_d8_extension_pipeline.validate_local_d8_extension",
                           return_value=altered):
                    pipeline = run_local_d8_extension_pipeline(request)
                self.assertEqual(pipeline.status, INTEGRITY_VERIFICATION_FAILURE)
                self.assertIsNone(pipeline.artifact)

    def test_verified_pnd_trace_must_match_evaluation(self):
        request = with_states(producer_request(), ("A", "A", "A"))
        baseline = validate_local_d8_extension(build_local_d8_extension(
            request, evaluate_local_d8_producer(request)))
        changes = (
            ("reviewRequired", False), ("excludedRuleIds", []),
            ("evaluatedDriverValues", []), ("reviewReference", "other"),
            ("validatedAssertionIds", []),
        )
        for field, changed in changes:
            with self.subTest(field=field):
                altered = deepcopy(baseline)
                altered["payload"][field] = changed
                with patch("assessment.local_d8_extension_pipeline.validate_local_d8_extension",
                           return_value=altered):
                    result = run_local_d8_extension_pipeline(request)
                self.assertEqual(result.status, INTEGRITY_VERIFICATION_FAILURE)
                self.assertIsNone(result.artifact)

    def test_all_84_independent_cases_verify_without_new_priority_oracle(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "PND": 0}
        tuples = tuple(itertools.product("PA", "TUA", "PA"))
        for pair, row, eligible in zip(PAIRS, ORACLE, ELIGIBLE_IDS):
            base = producer_request(pair)
            for states, expected in zip(tuples, row):
                with self.subTest(pair=pair, states=states):
                    request = with_states(base, states)
                    result = run_local_d8_extension_pipeline(request)
                    self.assertTrue(result.is_verified)
                    payload = validate_local_d8_extension(result.artifact)["payload"]
                    self.assertEqual(payload["outcome"], result.evaluation.outcome)
                    self.assertEqual((payload["assessmentIdentity"], payload["snapshotIdentity"],
                                      payload["findingId"], payload["recommendationInstanceIdentity"]),
                                     ("assessment-1", "snapshot-1", "finding-1", "instance-1"))
                    if expected == "-":
                        counts["PND"] += 1
                        self.assertEqual(payload["outcome"], PRIORITY_NOT_DETERMINED)
                        self.assertTrue(payload["reviewRequired"])
                        self.assertNotIn("priority", payload)
                        self.assertEqual(payload["excludedRuleIds"], sorted(eligible))
                        self.assertEqual(payload["evaluatedDriverValues"], [
                            {"driverId": driver, "assertedValue": vocabulary[state]}
                            for driver, vocabulary, state in zip(DRIVERS, VALUES, states)])
                    else:
                        level, rule_id = RULE[expected.split("+")[0]]
                        counts[level] += 1
                        self.assertEqual((payload["outcome"], payload["priority"],
                                          payload["winningRuleIds"]),
                                         (PRIORITY_ASSIGNED, level, [rule_id]))
                        self.assertEqual(payload["priority"], result.evaluation.priority)
                        self.assertEqual(payload["winningRuleIds"],
                                         list(result.evaluation.matched_rule_ids))
        self.assertEqual(counts, {"critical": 2, "high": 14, "medium": 1,
                                  "low": 4, "PND": 63})

    def test_no_production_source_imports_pipeline(self):
        package_dir = Path(__file__).resolve().parents[1] / "src" / "assessment"
        pipeline_tree = ast.parse((package_dir / "local_d8_extension_pipeline.py")
                                  .read_text(encoding="utf-8"))
        self.assertNotIn("evaluate_local_d8_priority",
                         {node.id for node in ast.walk(pipeline_tree)
                          if isinstance(node, ast.Name)})
        for path in package_dir.glob("*.py"):
            if path.name == "local_d8_extension_pipeline.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    self.assertNotEqual(node.module,
                                        "assessment.local_d8_extension_pipeline", str(path))
                elif isinstance(node, ast.Import):
                    self.assertNotIn("assessment.local_d8_extension_pipeline",
                                     [alias.name for alias in node.names], str(path))


if __name__ == "__main__":
    unittest.main()
