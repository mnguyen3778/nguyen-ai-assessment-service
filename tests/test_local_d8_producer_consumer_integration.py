"""Synthetic-only D8 producer-to-consumer handoff using existing local interfaces."""

import itertools
import unittest
from dataclasses import replace
from unittest.mock import patch

from assessment.d8_priority_extension import (
    DESIGNATION, SCHEMA_ID, SCHEMA_VERSION,
    build_local_d8_extension, validate_local_d8_extension,
)
from assessment.local_d8_extension_consumer import (
    REJECTED, VERIFIED, LocalD8ExpectedContext, consume_local_d8_extension,
)
from assessment.local_d8_extension_pipeline import (
    ADAPTER_OUTCOME_INELIGIBLE, VERIFIED_EXTENSION,
    run_local_d8_extension_pipeline,
)
from assessment.local_d8_priority import (
    BLOCKED_REQUIRED_EVIDENCE, METHODOLOGY_VERSION as D8_METHODOLOGY_VERSION,
    RULE_TABLE_VERSION as D8_RULE_TABLE_VERSION,
    NO_FINDINGS_MONITOR, PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED,
)
from assessment.local_d8_producer_adapter import evaluate_local_d8_producer
from test_d8_priority_extension import monitor_request
from test_local_d8_priority import DRIVERS, ELIGIBLE_IDS, ORACLE, PAIRS, RULE, VALUES
from test_local_d8_producer_adapter import producer_request, with_states


_PND_REFERENCE = (
    "local-synthetic-d8-review-v1:"
    "a7209f55629e5cc609ca63812bf125c25b7796fddf1025955fe78d23e62de89f"
)


def expected_context(request, expected, *, pair=None, states=None, eligible=(),
                     producer_review_reference=None):
    """Build expected bindings from fixture input and independent ledger, not bytes.

    PND's review reference is taken only from the separate adapter evaluation
    returned by the pipeline; it is never parsed from the extension artifact.
    """
    binding = request.binding
    canonical = request.canonical_input
    confidence = request.governed_result.confidence
    pnd = expected == "-"
    monitor = expected == NO_FINDINGS_MONITOR
    if pnd or monitor:
        priority, winners = None, ()
    else:
        priority, winner = RULE[expected.split("+")[0]]
        winners = (winner,)
    return LocalD8ExpectedContext(
        schema_id=SCHEMA_ID,
        schema_version=SCHEMA_VERSION,
        designation=DESIGNATION,
        assessment_identity=binding.assessment_identity,
        assessment_version=canonical.assessment_version,
        producer_methodology_version=canonical.methodology_version,
        snapshot_identity=binding.snapshot_identity,
        finding_id=binding.finding_id,
        recommendation_instance_identity=binding.recommendation_instance_identity,
        recommendation_decision_identifier=binding.recommendation_decision_identifier,
        recommendation_decision_table_version=binding.recommendation_decision_table_version,
        confidence_classification=confidence.confidence_classification,
        confidence_decision_identifier=confidence.confidence_decision_identifier,
        confidence_decision_table_version=confidence.confidence_decision_table_version,
        d8_methodology_version=D8_METHODOLOGY_VERSION,
        d8_rule_table_version=D8_RULE_TABLE_VERSION,
        outcome=(NO_FINDINGS_MONITOR if monitor else
                 PRIORITY_NOT_DETERMINED if pnd else PRIORITY_ASSIGNED),
        priority=priority,
        winning_rule_ids=winners,
        governed_finding_type=pair[0] if pnd else None,
        governed_consequence_basis=pair[1] if pnd else None,
        excluded_rule_ids=tuple(sorted(eligible)) if pnd else (),
        evaluated_driver_values=(tuple(
            (driver, vocabulary[state])
            for driver, vocabulary, state in zip(DRIVERS, VALUES, states))
            if pnd else ()),
        review_reference=producer_review_reference if pnd else None,
    )


def handoff(request, expected, *, pair=None, states=None, eligible=()):
    """Test-only handoff: never call the consumer after producer failure."""
    produced = run_local_d8_extension_pipeline(request)
    if not produced.is_verified:
        return produced, None, None
    context = expected_context(
        request, expected, pair=pair, states=states, eligible=eligible,
        producer_review_reference=produced.evaluation.review_reference,
    )
    consumed = consume_local_d8_extension(produced.artifact, context)
    return produced, consumed, context


class LocalD8ProducerConsumerIntegrationTests(unittest.TestCase):
    def assert_no_projection(self, result):
        self.assertEqual(result.disposition, REJECTED)
        self.assertIsNone(result.outcome)
        self.assertIsNone(result.projection)
        self.assertIsNotNone(result.reason_code)
        self.assertFalse(hasattr(result, "artifact"))

    def test_six_approved_outcomes_round_trip(self):
        cases = (
            (PAIRS[0], ("P", "T", "P"), "C+H1", "critical", ("B-C1",)),
            (PAIRS[1], ("P", "T", "P"), "H2", "high", ("G-H2",)),
            (PAIRS[2], ("A", "A", "A"), "M1", "medium", ("B-M1",)),
            (PAIRS[3], ("A", "A", "A"), "L1", "low", ("G-L1",)),
            (PAIRS[0], ("A", "A", "A"), "-", None, ()),
        )
        for pair, states, expected, priority, winners in cases:
            with self.subTest(pair=pair, states=states):
                request = with_states(producer_request(pair), states)
                eligible = ELIGIBLE_IDS[PAIRS.index(pair)]
                produced, consumed, context = handoff(
                    request, expected, pair=pair, states=states, eligible=eligible)
                self.assertEqual(produced.status, VERIFIED_EXTENSION)
                self.assertTrue(produced.is_verified)
                self.assertEqual(consumed.disposition, VERIFIED)
                self.assertEqual(consumed.outcome, context.outcome)
                projection = consumed.projection
                self.assertEqual((projection.priority, projection.winning_rule_ids),
                                 (priority, winners))
                self.assertEqual((projection.assessment_identity,
                                  projection.snapshot_identity, projection.finding_id,
                                  projection.recommendation_instance_identity),
                                 ("assessment-1", "snapshot-1", "finding-1", "instance-1"))
                self.assertEqual(projection.recommendation_decision_identifier,
                                 request.binding.recommendation_decision_identifier)
                self.assertEqual(projection.recommendation_decision_table_version,
                                 request.binding.recommendation_decision_table_version)
                self.assertEqual((projection.confidence_decision_identifier,
                                  projection.confidence_decision_table_version),
                                 (request.governed_result.confidence.confidence_decision_identifier,
                                  request.governed_result.confidence.confidence_decision_table_version))
                self.assertEqual((projection.schema_id, projection.schema_version,
                                  projection.designation),
                                 (SCHEMA_ID, SCHEMA_VERSION, DESIGNATION))
                self.assertEqual((projection.d8_methodology_version,
                                  projection.d8_rule_table_version),
                                 (D8_METHODOLOGY_VERSION, D8_RULE_TABLE_VERSION))
                if expected == "-":
                    self.assertTrue(projection.review_required)
                    self.assertEqual(projection.excluded_rule_ids, tuple(sorted(eligible)))
                    self.assertEqual(projection.evaluated_driver_values,
                                     context.evaluated_driver_values)
                    self.assertEqual((projection.governed_finding_type,
                                      projection.governed_consequence_basis), pair)
                    self.assertEqual(projection.review_reference, _PND_REFERENCE)
                    self.assertEqual(projection.review_reference,
                                     produced.evaluation.review_reference)
                else:
                    self.assertFalse(projection.review_required)
                    self.assertIsNone(projection.review_reference)
        monitor = monitor_request()
        produced, consumed, context = handoff(monitor, NO_FINDINGS_MONITOR)
        self.assertEqual(produced.status, VERIFIED_EXTENSION)
        self.assertEqual((consumed.disposition, consumed.outcome),
                         (VERIFIED, NO_FINDINGS_MONITOR))
        self.assertIsNone(context.finding_id)
        self.assertIsNone(consumed.projection.finding_id)
        self.assertEqual(consumed.projection.recommendation_instance_identity, "monitor-1")
        self.assertEqual(consumed.projection.recommendation_decision_identifier,
                         monitor.binding.recommendation_decision_identifier)
        self.assertIsNone(consumed.projection.priority)
        self.assertEqual(consumed.projection.winning_rule_ids, ())
        self.assertEqual((consumed.projection.validated_assertion_ids,
                          consumed.projection.evidence_provenance), ((), ()))
        self.assertFalse(consumed.projection.review_required)

    def test_existing_components_are_invoked_without_second_priority_evaluation(self):
        request = producer_request()
        original_records = [dict(record) for record in request.synthetic_assertions]
        with (patch("assessment.local_d8_extension_pipeline.evaluate_local_d8_producer",
                    wraps=evaluate_local_d8_producer) as adapter,
              patch("assessment.local_d8_extension_pipeline.build_local_d8_extension",
                    wraps=build_local_d8_extension) as builder,
              patch("assessment.local_d8_extension_pipeline.validate_local_d8_extension",
                    wraps=validate_local_d8_extension) as producer_verifier,
              patch("assessment.local_d8_extension_consumer.validate_local_d8_extension",
                    wraps=validate_local_d8_extension) as consumer_verifier):
            produced, consumed, _ = handoff(request, "C+H1")
        adapter.assert_called_once_with(request)
        builder.assert_called_once_with(request, produced.evaluation)
        producer_verifier.assert_called_once_with(produced.artifact)
        consumer_verifier.assert_called_once_with(produced.artifact)
        self.assertEqual(consumed.disposition, VERIFIED)
        self.assertEqual(request.synthetic_assertions, original_records)
        self.assertFalse(hasattr(consumed, "artifact"))

    def test_digest_valid_artifact_rejects_wrong_expected_bindings(self):
        request = producer_request()
        produced, consumed, context = handoff(request, "C+H1")
        self.assertEqual(consumed.disposition, VERIFIED)
        self.assertIsInstance(validate_local_d8_extension(produced.artifact), dict)
        changes = {
            "assessment_identity": "other",
            "snapshot_identity": "other",
            "recommendation_decision_identifier": "other",
            "recommendation_decision_table_version": "other",
            "finding_id": "other",
            "recommendation_instance_identity": "other",
            "confidence_decision_identifier": "other",
            "confidence_decision_table_version": "other",
            "d8_methodology_version": "other",
            "d8_rule_table_version": "other",
            "schema_id": "other",
            "schema_version": 2,
            "designation": "PRODUCTION",
            "outcome": PRIORITY_NOT_DETERMINED,
            "priority": "high",
            "winning_rule_ids": ("G-H1",),
        }
        for field, wrong in changes.items():
            with self.subTest(field=field):
                self.assert_no_projection(consume_local_d8_extension(
                    produced.artifact, replace(context, **{field: wrong})))

    def test_all_six_cross_outcome_substitutions_reject(self):
        assigned = handoff(producer_request(), "C+H1")
        pnd_request = with_states(producer_request(), ("A", "A", "A"))
        pnd = handoff(pnd_request, "-", pair=PAIRS[0], states=("A", "A", "A"),
                      eligible=ELIGIBLE_IDS[0])
        d7 = handoff(monitor_request(), NO_FINDINGS_MONITOR)
        for produced, consumed, _ in (assigned, pnd, d7):
            self.assertTrue(produced.is_verified)
            self.assertEqual(consumed.disposition, VERIFIED)
        for source, target in ((assigned, pnd), (assigned, d7),
                               (pnd, assigned), (pnd, d7),
                               (d7, assigned), (d7, pnd)):
            with self.subTest(source=source[1].outcome, target=target[1].outcome):
                self.assert_no_projection(consume_local_d8_extension(
                    source[0].artifact, target[2]))

    def test_tampering_malformed_inputs_and_context_fail_closed(self):
        produced, _, context = handoff(producer_request(), "C+H1")
        blob = produced.artifact
        tampered = blob.replace(b'"priority":"critical"', b'"priority":"high"', 1)
        wrong_version = blob.replace(b'"schemaVersion":1', b'"schemaVersion":2', 1)
        self.assertNotEqual(tampered, blob)
        self.assertNotEqual(wrong_version, blob)
        for bad_blob, expected in ((tampered, context), (wrong_version, context),
                                   (b"not-json", context), (b"", context),
                                   (blob, None), (blob, {}),
                                   (blob, replace(context, assessment_identity="")),
                                   (blob, replace(context, outcome="UNKNOWN"))):
            with self.subTest(blob=bad_blob[:30], context=repr(expected)[:30]):
                self.assert_no_projection(consume_local_d8_extension(bad_blob, expected))

    def test_failed_producer_has_no_artifact_or_consumer_call(self):
        request = with_states(producer_request(), ("P", "T", None))
        with patch("test_local_d8_producer_consumer_integration.consume_local_d8_extension") as consumer:
            produced, consumed, context = handoff(
                request, "C+H1", pair=PAIRS[0], states=("P", "T", None),
                eligible=ELIGIBLE_IDS[0])
        self.assertEqual(produced.status, ADAPTER_OUTCOME_INELIGIBLE)
        self.assertEqual(produced.evaluation.outcome, BLOCKED_REQUIRED_EVIDENCE)
        self.assertFalse(produced.is_verified)
        self.assertIsNone(produced.artifact)
        self.assertIsNone(consumed)
        self.assertIsNone(context)
        consumer.assert_not_called()

    def test_all_84_independent_ledger_cases_cross_complete_handoff(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "PND": 0}
        states = tuple(itertools.product("PA", "TUA", "PA"))
        self.assertEqual(len(PAIRS), len(ORACLE))
        for pair, row, eligible in zip(PAIRS, ORACLE, ELIGIBLE_IDS):
            self.assertEqual(len(row), len(states))
            base = producer_request(pair)
            for drivers, expected in zip(states, row):
                with self.subTest(pair=pair, drivers=drivers):
                    request = with_states(base, drivers)
                    produced, consumed, context = handoff(
                        request, expected, pair=pair, states=drivers, eligible=eligible)
                    self.assertTrue(produced.is_verified)
                    self.assertEqual(produced.status, VERIFIED_EXTENSION)
                    self.assertEqual(consumed.disposition, VERIFIED)
                    self.assertEqual(consumed.outcome, context.outcome)
                    if expected == "-":
                        counts["PND"] += 1
                        self.assertTrue(consumed.projection.review_required)
                        self.assertIsNone(consumed.projection.priority)
                        self.assertEqual(consumed.projection.winning_rule_ids, ())
                        self.assertEqual(consumed.projection.excluded_rule_ids,
                                         tuple(sorted(eligible)))
                        self.assertEqual(consumed.projection.evaluated_driver_values,
                                         context.evaluated_driver_values)
                        self.assertEqual(consumed.projection.review_reference,
                                         produced.evaluation.review_reference)
                    else:
                        level, winner = RULE[expected.split("+")[0]]
                        counts[level] += 1
                        self.assertEqual(consumed.projection.priority, level)
                        self.assertEqual(consumed.projection.winning_rule_ids, (winner,))
                    self.assertEqual(consumed.projection.finding_id, "finding-1")
                    self.assertEqual(consumed.projection.snapshot_identity, "snapshot-1")
        self.assertEqual(counts, {"critical": 2, "high": 14, "medium": 1,
                                  "low": 4, "PND": 63})


if __name__ == "__main__":
    unittest.main()
