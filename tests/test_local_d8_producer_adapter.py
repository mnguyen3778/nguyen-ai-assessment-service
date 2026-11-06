"""Local synthetic producer binding tests; no production integration."""

import itertools
import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from assessment.decision_engine import evaluate_assessment_v2  # noqa: E402
from assessment.governed_assessment_input import (  # noqa: E402
    EXECUTIVE_ASSESSMENT_VERSION_V2, ValidatedCanonicalExecutiveAssessmentInputV2,
)
from assessment.local_d8_priority import (  # noqa: E402
    BLOCKED_REQUIRED_EVIDENCE, INSUFFICIENT_CONFIDENCE, NO_FINDINGS_MONITOR,
    PRIORITY_ASSIGNED, PRIORITY_NOT_DETERMINED, REJECTED_INVALID_ASSERTION,
    evaluate_local_d8_priority,
)
from assessment.local_d8_producer_adapter import (  # noqa: E402
    LocalD8ProducerRequest, LocalSyntheticProducerBinding, evaluate_local_d8_producer,
)
from assessment.local_priority_assertions import (  # noqa: E402
    RecommendationInstance, SyntheticContext,
)
from assessment.methodology_config import METHODOLOGY_VERSION  # noqa: E402
from test_golden_fixture_regression import answers, evidence, finding  # noqa: E402
from test_local_d8_priority import (  # noqa: E402
    DRIVERS, ELIGIBLE_IDS, ORACLE, PAIRS, RULE, VALUES, fixture,
)


def producer_request(pair=PAIRS[0], states=("P", "T", "P"), profile="strong"):
    canonical = ValidatedCanonicalExecutiveAssessmentInputV2(
        EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
        answers(75), evidence(profile),
        tuple(finding(f"finding-{i}", pair[0], "POC", pair[1]) for i in (1, 2)),
    )
    producer = evaluate_assessment_v2(canonical)
    local = fixture(pair, states)
    recommendation = producer.recommendations[0]
    binding = LocalSyntheticProducerBinding(
        "assessment-1", "snapshot-1", "finding-1", "instance-1",
        recommendation.recommendation_decision_identifier,
        recommendation.recommendation_decision_table_version,
    )
    return LocalD8ProducerRequest(canonical, producer, local.context,
                                  local.records, binding)


def with_states(request, states):
    local = fixture((request.canonical_input.findings[0].finding_type,
                     request.canonical_input.findings[0].business_consequence_basis), states)
    return replace(request, synthetic_context=local.context,
                   synthetic_assertions=local.records)


class LocalD8ProducerAdapterTests(unittest.TestCase):
    def test_valid_bound_result_and_repeatability(self):
        request = producer_request()
        result = evaluate_local_d8_producer(request)
        self.assertEqual(result.outcome, PRIORITY_ASSIGNED)
        self.assertEqual(result.priority, "critical")
        self.assertEqual(result.matched_rule_ids, ("B-C1",))
        self.assertEqual((result.assessment_identity, result.snapshot_identity,
                          result.finding_id, result.recommendation_instance_identity),
                         ("assessment-1", "snapshot-1", "finding-1", "instance-1"))
        self.assertEqual(result, evaluate_local_d8_producer(request))

    def test_all_84_independent_document_43_cases(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "PND": 0}
        tuples = tuple(itertools.product("PA", "TUA", "PA"))
        self.assertEqual(len(PAIRS), len(ORACLE))
        for pair, expected_row, eligible in zip(PAIRS, ORACLE, ELIGIBLE_IDS):
            self.assertEqual(len(expected_row), len(tuples))
            base = producer_request(pair)
            for states, expected in zip(tuples, expected_row):
                with self.subTest(pair=pair, states=states):
                    result = evaluate_local_d8_producer(with_states(base, states))
                    self.assertEqual((result.finding_id, result.recommendation_instance_identity,
                                      result.snapshot_identity),
                                     ("finding-1", "instance-1", "snapshot-1"))
                    if expected == "-":
                        self.assertEqual(result.outcome, PRIORITY_NOT_DETERMINED)
                        self.assertIsNone(result.priority)
                        self.assertEqual((result.governed_finding_type,
                                          result.governed_consequence_basis), pair)
                        self.assertEqual(result.evaluated_driver_values,
                                         tuple((driver, vocabulary[state])
                                               for driver, vocabulary, state in
                                               zip(DRIVERS, VALUES, states)))
                        self.assertEqual(result.excluded_rule_ids,
                                         tuple(sorted(eligible)))
                        self.assertEqual(result.validated_assertion_ids,
                                         tuple(sorted(f"assertion-{driver}"
                                                      for driver in DRIVERS)))
                        self.assertEqual(result.methodology_version,
                                         "founder-d8-methodology-approval-v1-local-synthetic")
                        self.assertEqual(result.rule_table_version,
                                         "local-synthetic-d8-rule-table-v1")
                        self.assertTrue(result.review_required)
                        self.assertRegex(result.review_reference or "",
                                         r"^local-synthetic-d8-review-v1:[0-9a-f]{64}$")
                        counts["PND"] += 1
                    else:
                        winner = RULE[expected.split("+")[0]]
                        self.assertEqual(result.outcome, PRIORITY_ASSIGNED)
                        self.assertEqual((result.priority, result.matched_rule_ids),
                                         (winner[0], (winner[1],)))
                        counts[winner[0]] += 1
        self.assertEqual(counts, {"critical": 2, "high": 14,
                                  "medium": 1, "low": 4, "PND": 63})

    def test_pnd_trace_and_identity_bound_reference(self):
        request = producer_request(states=("A", "A", "A"))
        result = evaluate_local_d8_producer(request)
        self.assertEqual(result.outcome, PRIORITY_NOT_DETERMINED)
        self.assertEqual(result.review_reference,
                         evaluate_local_d8_producer(request).review_reference)
        self.assertEqual(result.review_reference,
                         evaluate_local_d8_priority(fixture(PAIRS[0], ("A", "A", "A"))).review_reference)
        self.assertEqual(result.validated_assertion_ids,
                         tuple(sorted(f"assertion-{driver}" for driver in DRIVERS)))
        self.assertTrue(result.methodology_version and result.rule_table_version)
        self.assertTrue(result.review_required)
        self.assertIsNone(result.priority)
        missing = evaluate_local_d8_producer(with_states(request, (None, "A", None)))
        self.assertEqual(missing.outcome, PRIORITY_NOT_DETERMINED)
        self.assertEqual(missing.evaluated_driver_values,
                         (("customer-impact", None),
                          ("executive-urgency", "executive-action-affirmed-absent"),
                          ("dependency-role", None)))

        records = [dict(record, recommendationInstanceIdentity="instance-2",
                        findingId="finding-2") for record in request.synthetic_assertions]
        evidence_map = {key: replace(value, instance_identity="instance-2")
                        for key, value in request.synthetic_context.evidence.items()}
        second = replace(request, synthetic_assertions=records,
                         synthetic_context=replace(request.synthetic_context,
                                                   evidence=evidence_map),
                         binding=replace(request.binding, finding_id="finding-2",
                                         recommendation_instance_identity="instance-2"))
        second_result = evaluate_local_d8_producer(second)
        self.assertEqual(second_result.outcome, PRIORITY_NOT_DETERMINED)
        self.assertNotEqual(result.review_reference, second_result.review_reference)

    def test_binding_failures_reject(self):
        request = producer_request()
        changes = (
            replace(request, binding=replace(request.binding,
                                             assessment_identity="other")),
            replace(request, binding=replace(request.binding, snapshot_identity="other")),
            replace(request, binding=replace(request.binding, finding_id="other")),
            replace(request, binding=replace(request.binding,
                                             recommendation_instance_identity="other")),
            replace(request, binding=replace(request.binding,
                                             recommendation_decision_table_version="other")),
            replace(request, binding=replace(request.binding,
                                             recommendation_decision_identifier="other")),
            replace(request, binding=replace(request.binding,
                                             recommendation_instance_identity="")),
            replace(request, synthetic_context=replace(request.synthetic_context,
                                                        snapshot_identity="other")),
            replace(request, binding=None),
            replace(request, synthetic_context=replace(request.synthetic_context,
                recommendations=(replace(request.synthetic_context.recommendations[0],
                                         finding_id="finding-2"),
                                 request.synthetic_context.recommendations[1]))),
            replace(request, synthetic_context=replace(request.synthetic_context,
                recommendations=(request.synthetic_context.recommendations[0],
                                 replace(request.synthetic_context.recommendations[1],
                                         instance_identity="instance-1")))),
            replace(request, synthetic_context=replace(request.synthetic_context,
                recommendations=(replace(request.synthetic_context.recommendations[0],
                                         decision_table_version="other"),
                                 request.synthetic_context.recommendations[1]))),
            replace(request, governed_result=replace(request.governed_result,
                findings=request.governed_result.findings[:1])),
            replace(request, governed_result=replace(request.governed_result,
                risk=None)),
            replace(request, governed_result=replace(request.governed_result,
                confidence=replace(request.governed_result.confidence,
                                   confidence_classification="unsupported"))),
            replace(request, governed_result=replace(request.governed_result,
                risk=replace(request.governed_result.risk,
                             severity_classifications=("low", "low")))),
            replace(request, governed_result=replace(request.governed_result,
                recommendations=(replace(request.governed_result.recommendations[0],
                                         finding_id="other"),
                                 request.governed_result.recommendations[1]))),
        )
        for changed in changes:
            with self.subTest(changed=changed):
                self.assertEqual(evaluate_local_d8_producer(changed).outcome,
                                 REJECTED_INVALID_ASSERTION)
        self.assertEqual(evaluate_local_d8_producer({"priority": "critical"}).outcome,
                         REJECTED_INVALID_ASSERTION)
        self.assertEqual(evaluate_local_d8_producer({"matchedRuleIds": ["B-C1"]}).outcome,
                         REJECTED_INVALID_ASSERTION)
        unsupported = object.__new__(type(request.canonical_input.findings[0]))
        object.__setattr__(unsupported, "finding_id", "finding-1")
        object.__setattr__(unsupported, "finding_type", "Unsupported")
        object.__setattr__(unsupported, "business_consequence_basis", "unknown")
        self.assertEqual(evaluate_local_d8_producer(replace(
            request, governed_result=replace(request.governed_result,
                                             findings=(unsupported,
                                                       request.governed_result.findings[1])))).outcome,
            REJECTED_INVALID_ASSERTION)

    def test_finding_id_type_gate(self):
        request = producer_request()
        for finding_id in (["finding-1"], {"id": "finding-1"}, 1, ""):
            with self.subTest(finding_id=finding_id):
                result = evaluate_local_d8_producer(replace(
                    request, binding=replace(request.binding, finding_id=finding_id)))
                self.assertEqual(result.outcome, REJECTED_INVALID_ASSERTION)
                self.assertIsNone(result.priority)
        self.assertEqual(evaluate_local_d8_producer(request).outcome,
                         PRIORITY_ASSIGNED)
        self.assertEqual(evaluate_local_d8_producer(replace(
            request, binding=replace(request.binding, finding_id=None))).outcome,
            REJECTED_INVALID_ASSERTION)

    def test_assertion_failures_and_rule_dependent_missing(self):
        request = producer_request()
        for driver, states, expected in (
            ("customer-impact", ("P", "T", "A"), BLOCKED_REQUIRED_EVIDENCE),
            ("executive-urgency", ("P", "U", "A"), BLOCKED_REQUIRED_EVIDENCE),
            ("dependency-role", ("P", "T", "A"), BLOCKED_REQUIRED_EVIDENCE),
            ("customer-impact", ("P", "T", "P"), PRIORITY_ASSIGNED),
            ("executive-urgency", ("A", "A", "A"), PRIORITY_NOT_DETERMINED),
            ("dependency-role", ("P", "A", "A"), PRIORITY_NOT_DETERMINED),
        ):
            with self.subTest(driver=driver, states=states):
                case = with_states(request, states)
                records = [record for record in case.synthetic_assertions
                           if record["driverId"] != driver]
                self.assertEqual(evaluate_local_d8_producer(
                    replace(case, synthetic_assertions=records)).outcome, expected)
        for change in ({"businessAuthorityReference": "unknown"},
                       {"sourceRevision": "stale"},
                       {"assessmentSnapshotIdentity": "other"},
                       {"assertedValue": "unsupported"}):
            with self.subTest(change=change):
                records = [dict(record) for record in request.synthetic_assertions]
                records[0].update(change)
                self.assertEqual(evaluate_local_d8_producer(
                    replace(request, synthetic_assertions=records)).outcome,
                    REJECTED_INVALID_ASSERTION)
        duplicate = [dict(record) for record in request.synthetic_assertions]
        duplicate.append(dict(duplicate[0]))
        self.assertEqual(evaluate_local_d8_producer(
            replace(request, synthetic_assertions=duplicate)).outcome,
            REJECTED_INVALID_ASSERTION)
        unneeded = with_states(producer_request(PAIRS[1]), ("P", "U", "A"))
        records = [dict(record) for record in unneeded.synthetic_assertions]
        records[-1]["businessAuthorityReference"] = "unknown"
        self.assertEqual(evaluate_local_d8_producer(
            replace(unneeded, synthetic_assertions=records)).outcome,
            REJECTED_INVALID_ASSERTION)
        bad_scope = with_states(request, ("A", "A", "A"))
        evidence_map = dict(bad_scope.synthetic_context.evidence)
        ref = bad_scope.synthetic_assertions[0]["evidenceReferences"][0]
        evidence_map[ref] = replace(evidence_map[ref], scope_confirmed=False)
        self.assertEqual(evaluate_local_d8_producer(replace(
            bad_scope, synthetic_context=replace(bad_scope.synthetic_context,
                                                 evidence=evidence_map))).outcome,
            REJECTED_INVALID_ASSERTION)

    def test_confidence_and_d7_remain_non_emitting(self):
        insufficient = producer_request(profile="limitation")
        self.assertEqual(evaluate_local_d8_producer(insufficient).outcome,
                         INSUFFICIENT_CONFIDENCE)
        canonical = ValidatedCanonicalExecutiveAssessmentInputV2(
            EXECUTIVE_ASSESSMENT_VERSION_V2, METHODOLOGY_VERSION,
            answers(75), evidence("strong"), ())
        producer = evaluate_assessment_v2(canonical)
        recommendation = producer.recommendations[0]
        context = SyntheticContext("snapshot-1", "assessment-1", (
            RecommendationInstance("monitor-1", None,
                                   recommendation.recommendation_decision_identifier),
        ), {}, {})
        binding = LocalSyntheticProducerBinding(
            "assessment-1", "snapshot-1", None, "monitor-1",
            recommendation.recommendation_decision_identifier,
            recommendation.recommendation_decision_table_version)
        request = LocalD8ProducerRequest(canonical, producer, context, [], binding)
        self.assertIsNone(request.binding.finding_id)
        monitor = evaluate_local_d8_producer(request)
        self.assertEqual(monitor.outcome, NO_FINDINGS_MONITOR)
        self.assertIsNone(monitor.priority)
        malformed = replace(request, binding=replace(binding, finding_id="finding-1"))
        self.assertEqual(evaluate_local_d8_producer(malformed).outcome,
                         REJECTED_INVALID_ASSERTION)


if __name__ == "__main__":
    unittest.main()
