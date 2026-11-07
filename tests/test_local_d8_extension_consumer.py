"""Synthetic D8 consumer tests with expected bindings independent of artifact bytes."""

import itertools
import json
import unittest
from dataclasses import replace
from unittest.mock import patch

from assessment.d8_priority_extension import (
    DESIGNATION, MAX_ARTIFACT_BYTES, SCHEMA_ID, SCHEMA_VERSION,
    build_local_d8_extension, validate_local_d8_extension,
)
from assessment.local_d8_extension_consumer import (
    REJECTED, VERIFIED, LocalD8ExpectedContext, consume_local_d8_extension,
)
from assessment.local_d8_priority import (
    NO_FINDINGS_MONITOR, PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED,
)
from assessment.local_d8_producer_adapter import evaluate_local_d8_producer
from test_d8_priority_extension import monitor_request
from test_local_d8_producer_adapter import producer_request, with_states
from test_local_d8_priority import ORACLE, PAIRS, RULE


def expected_context(request, evaluation):
    """Use the independently constructed request and adapter result, never the blob."""
    binding = request.binding
    canonical = request.canonical_input
    confidence = request.governed_result.confidence
    return LocalD8ExpectedContext(
        schema_id=SCHEMA_ID, schema_version=SCHEMA_VERSION, designation=DESIGNATION,
        assessment_identity=binding.assessment_identity,
        assessment_version=canonical.assessment_version,
        producer_methodology_version=canonical.methodology_version,
        snapshot_identity=binding.snapshot_identity, finding_id=binding.finding_id,
        recommendation_instance_identity=binding.recommendation_instance_identity,
        recommendation_decision_identifier=binding.recommendation_decision_identifier,
        recommendation_decision_table_version=binding.recommendation_decision_table_version,
        confidence_classification=confidence.confidence_classification,
        confidence_decision_identifier=confidence.confidence_decision_identifier,
        confidence_decision_table_version=confidence.confidence_decision_table_version,
        d8_methodology_version=evaluation.methodology_version,
        d8_rule_table_version=evaluation.rule_table_version,
        outcome=evaluation.outcome, priority=evaluation.priority,
        winning_rule_ids=evaluation.matched_rule_ids,
        governed_finding_type=evaluation.governed_finding_type,
        governed_consequence_basis=evaluation.governed_consequence_basis,
        excluded_rule_ids=(evaluation.excluded_rule_ids
                           if evaluation.outcome == PRIORITY_NOT_DETERMINED else ()),
        evaluated_driver_values=evaluation.evaluated_driver_values,
        review_reference=evaluation.review_reference,
    )


def sample(request):
    evaluation = evaluate_local_d8_producer(request)
    return build_local_d8_extension(request, evaluation), expected_context(request, evaluation)


class LocalD8ExtensionConsumerTests(unittest.TestCase):
    def assert_rejected(self, artifact, context):
        result = consume_local_d8_extension(artifact, context)
        self.assertEqual(result.disposition, REJECTED)
        self.assertIsNone(result.outcome)
        self.assertIsNone(result.projection)
        self.assertIsNotNone(result.reason_code)
        self.assertFalse(hasattr(result, "artifact"))

    def test_assigned_preserves_priority_binding_and_provenance(self):
        request = producer_request()
        blob, context = sample(request)
        source = [dict(record) for record in request.synthetic_assertions]
        with patch("assessment.local_d8_extension_consumer.validate_local_d8_extension",
                   wraps=validate_local_d8_extension) as verifier:
            result = consume_local_d8_extension(blob, context)
        verifier.assert_called_once_with(blob)
        self.assertEqual((result.disposition, result.outcome), (VERIFIED, PRIORITY_ASSIGNED))
        self.assertIsNone(result.reason_code)
        p = result.projection
        self.assertEqual((p.priority, p.winning_rule_ids),
                         (context.priority, context.winning_rule_ids))
        self.assertEqual((p.assessment_identity, p.snapshot_identity, p.finding_id,
                          p.recommendation_instance_identity),
                         ("assessment-1", "snapshot-1", "finding-1", "instance-1"))
        self.assertEqual(p.recommendation_decision_identifier,
                         context.recommendation_decision_identifier)
        self.assertEqual(p.d8_methodology_version, context.d8_methodology_version)
        self.assertEqual(p.d8_rule_table_version, context.d8_rule_table_version)
        self.assertEqual((p.schema_id, p.schema_version, p.designation),
                         (context.schema_id, context.schema_version, context.designation))
        self.assertEqual((p.assessment_version, p.producer_methodology_version,
                          p.confidence_classification),
                         (context.assessment_version, context.producer_methodology_version,
                          context.confidence_classification))
        self.assertEqual(p.validated_assertion_ids,
                         tuple(sorted(record["assertionId"] for record in source)))
        self.assertEqual(request.synthetic_assertions, source)
        self.assertFalse(hasattr(p, "artifact"))
        self.assertNotIn(blob, (p, result))

    def test_pnd_preserves_complete_review_trace(self):
        blob, context = sample(with_states(producer_request(), (None, "A", None)))
        result = consume_local_d8_extension(blob, context)
        self.assertEqual((result.disposition, result.outcome),
                         (VERIFIED, PRIORITY_NOT_DETERMINED))
        p = result.projection
        self.assertTrue(p.review_required)
        self.assertIsNone(p.priority)
        self.assertEqual(p.winning_rule_ids, ())
        self.assertEqual(p.excluded_rule_ids, context.excluded_rule_ids)
        self.assertEqual(p.evaluated_driver_values, context.evaluated_driver_values)
        self.assertEqual(p.review_reference, context.review_reference)
        self.assertEqual(p.governed_finding_type, context.governed_finding_type)
        self.assertEqual(p.governed_consequence_basis, context.governed_consequence_basis)

    def test_d7_monitor_preserves_null_finding_and_no_priority(self):
        blob, context = sample(monitor_request())
        result = consume_local_d8_extension(blob, context)
        self.assertEqual((result.disposition, result.outcome),
                         (VERIFIED, NO_FINDINGS_MONITOR))
        p = result.projection
        self.assertIsNone(p.finding_id)
        self.assertEqual(p.recommendation_instance_identity, "monitor-1")
        self.assertIsNone(p.priority)
        self.assertEqual((p.winning_rule_ids, p.validated_assertion_ids,
                          p.evidence_provenance), ((), (), ()))
        self.assertFalse(p.review_required)

    def test_missing_wrong_oversized_and_malformed_artifact_fail_closed(self):
        blob, context = sample(producer_request())
        invalid = (None, b"", "not bytes", bytearray(blob),
                   b"x" * (MAX_ARTIFACT_BYTES + 1), b"not-json", b"{}",
                   b'{"payload":1,"payload":2}', blob + b" ",
                   blob.replace(b'"priority":"critical"', b'"priority":"low"'))
        for value in invalid:
            with self.subTest(value=repr(value)[:50]):
                self.assert_rejected(value, context)

    def test_unsupported_artifact_schema_and_designation_fail_closed(self):
        blob, context = sample(producer_request())
        for old, new in ((b'"schemaId":"nguyen-ai-local-d8-priority-extension"',
                          b'"schemaId":"other"'),
                         (b'"schemaVersion":1', b'"schemaVersion":2'),
                         (b'"designation":"SYNTHETIC_NONPRODUCTION"',
                          b'"designation":"PRODUCTION"'),
                         (b'"d8MethodologyVersion":"founder-d8-methodology-approval-v1-local-synthetic"',
                          b'"d8MethodologyVersion":"other"'),
                         (b'"d8RuleTableVersion":"local-synthetic-d8-rule-table-v1"',
                          b'"d8RuleTableVersion":"other"')):
            with self.subTest(field=old[:30]):
                self.assertIn(old, blob)
                self.assert_rejected(blob.replace(old, new, 1), context)

    def test_malformed_context_and_unexpected_fields_fail_closed(self):
        blob, context = sample(producer_request())
        class Explosive:
            def __eq__(self, other):
                raise AssertionError("must reject type before comparison")

        for bad in (None, {},
                    {"assessment_identity": "assessment-1", "productionAuthorized": True},
                    replace(context, assessment_identity=""),
                    replace(context, assessment_identity=[]),
                    replace(context, schema_id=Explosive()),
                    replace(context, assessment_version=Explosive()),
                    replace(context, excluded_rule_ids=Explosive()),
                    replace(context, schema_version=True),
                    replace(context, winning_rule_ids=(["B-C1"],)),
                    replace(context, outcome=[])):
            with self.subTest(bad=repr(bad)[:80]):
                self.assert_rejected(blob, bad)

    def test_unsupported_context_versions_and_designation_fail_closed(self):
        blob, context = sample(producer_request())
        changes = {
            "schema_id": "other", "schema_version": 2, "designation": "PRODUCTION",
            "assessment_version": "other", "producer_methodology_version": "other",
            "recommendation_decision_table_version": "other",
            "confidence_decision_table_version": "other",
            "d8_methodology_version": "other", "d8_rule_table_version": "other",
            "outcome": "UNKNOWN",
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                self.assert_rejected(blob, replace(context, **{field: value}))

    def test_exact_identity_and_decision_mismatches_fail_closed(self):
        blob, context = sample(producer_request())
        fields = (
            "assessment_identity", "snapshot_identity", "finding_id",
            "recommendation_instance_identity", "recommendation_decision_identifier",
            "recommendation_decision_table_version", "confidence_classification",
            "confidence_decision_identifier", "confidence_decision_table_version",
            "d8_methodology_version", "d8_rule_table_version", "priority",
            "winning_rule_ids",
        )
        for field in fields:
            with self.subTest(field=field):
                value = ("G-H1",) if field == "winning_rule_ids" else "other"
                self.assert_rejected(blob, replace(context, **{field: value}))

    def test_valid_but_wrong_outcome_artifacts_fail_closed(self):
        assigned_blob, assigned_context = sample(producer_request())
        pnd_blob, _ = sample(with_states(producer_request(), ("A", "A", "A")))
        d7_blob, d7_context = sample(monitor_request())
        for blob, context in ((assigned_blob, d7_context), (d7_blob, assigned_context),
                              (pnd_blob, assigned_context)):
            with self.subTest(outcome=context.outcome, blob=blob[:20]):
                self.assert_rejected(blob, context)
        self.assertEqual(consume_local_d8_extension(assigned_blob, assigned_context).disposition,
                         VERIFIED)

    def test_pnd_trace_mismatch_and_invalid_d7_link_fail_closed(self):
        pnd_blob, pnd_context = sample(with_states(producer_request(), ("A", "A", "A")))
        for change in (
            {"review_reference": "other"},
            {"excluded_rule_ids": ("B-C1",)},
            {"evaluated_driver_values": (("customer-impact", None),)},
            {"governed_finding_type": "other"},
            {"governed_consequence_basis": "other"},
            {"priority": "low"},
        ):
            with self.subTest(change=change):
                self.assert_rejected(pnd_blob, replace(pnd_context, **change))
        malformed = json.loads(pnd_blob)
        malformed["payload"]["evaluatedDriverValues"][0]["driverId"] = "wrong"
        self.assert_rejected(json.dumps(malformed, separators=(",", ":")).encode(),
                             pnd_context)
        d7_blob, d7_context = sample(monitor_request())
        self.assert_rejected(d7_blob, replace(d7_context, finding_id="finding-1"))
        self.assert_rejected(d7_blob, replace(d7_context,
                                             recommendation_instance_identity="instance-1"))

    def test_verifier_wrong_return_and_exception_fail_closed(self):
        blob, context = sample(producer_request())
        valid = validate_local_d8_extension(blob)
        returns = ({}, [], True, None, {"payload": {}},
                   {"payload": valid["payload"], "integrity": {}},
                   {"payload": {**valid["payload"], "unexpected": True},
                    "integrity": valid["integrity"]})
        for value in returns:
            with self.subTest(value=repr(value)[:60]):
                with patch("assessment.local_d8_extension_consumer.validate_local_d8_extension",
                           return_value=value):
                    self.assert_rejected(blob, context)
        for exception in (ValueError("bad digest"), RuntimeError("verifier failure")):
            with self.subTest(exception=type(exception).__name__):
                with patch("assessment.local_d8_extension_consumer.validate_local_d8_extension",
                           side_effect=exception):
                    result = consume_local_d8_extension(blob, context)
                self.assertEqual(result.reason_code, "ARTIFACT_VERIFICATION_FAILED")
                self.assertIsNone(result.projection)

    def test_no_priority_evaluation_or_input_mutation(self):
        request = producer_request()
        blob, context = sample(request)
        original = bytes(blob), context, [dict(record) for record in request.synthetic_assertions]
        with patch("assessment.local_d8_priority.evaluate_local_d8_priority",
                   side_effect=AssertionError("consumer must not evaluate")):
            result = consume_local_d8_extension(blob, context)
        self.assertEqual(result.disposition, VERIFIED)
        self.assertEqual((blob, context, request.synthetic_assertions), original)
        self.assertEqual(result.projection.priority, context.priority)

    def test_independent_84_case_ledger_consumer_round_trip(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "PND": 0}
        states = tuple(itertools.product("PA", "TUA", "PA"))
        for pair, expected_row in zip(PAIRS, ORACLE):
            base = producer_request(pair)
            for drivers, expected in zip(states, expected_row):
                with self.subTest(pair=pair, drivers=drivers):
                    blob, context = sample(with_states(base, drivers))
                    result = consume_local_d8_extension(blob, context)
                    self.assertEqual(result.disposition, VERIFIED)
                    if expected == "-":
                        counts["PND"] += 1
                        self.assertEqual(result.outcome, PRIORITY_NOT_DETERMINED)
                        self.assertTrue(result.projection.review_required)
                        self.assertIsNone(result.projection.priority)
                        self.assertEqual(result.projection.excluded_rule_ids,
                                         context.excluded_rule_ids)
                        self.assertEqual(result.projection.evaluated_driver_values,
                                         context.evaluated_driver_values)
                    else:
                        level, rule_id = RULE[expected.split("+")[0]]
                        counts[level] += 1
                        self.assertEqual(result.outcome, PRIORITY_ASSIGNED)
                        self.assertEqual(result.projection.priority, level)
                        self.assertEqual(result.projection.winning_rule_ids, (rule_id,))
        self.assertEqual(counts, {"critical": 2, "high": 14, "medium": 1,
                                  "low": 4, "PND": 63})


if __name__ == "__main__":
    unittest.main()
